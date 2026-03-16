from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from exceptions import CommandExecutionError, PathSecurityError, StateError
from generate_dashboard import generate_dashboard

from orchestrator_common import DEFAULT_DELIVERABLES, load_state, read_yaml, save_state, write_yaml


def _validate_cwd(cwd: Path, project_root: Path) -> Path:
    """Validate that the working directory is within the project root."""
    try:
        resolved_cwd = cwd.resolve()
        resolved_root = project_root.resolve()
        resolved_cwd.relative_to(resolved_root)
        return resolved_cwd
    except ValueError as exc:
        raise PathSecurityError(
            "Working directory must be inside project root",
            path=str(cwd),
            reason="path_traversal",
        ) from exc


def _parse_command_safely(command: str) -> list[str]:
    """Parse a command string into a list of arguments without shell execution.

    This function safely parses command strings to avoid shell injection vulnerabilities.
    It uses shlex.split() which properly handles quoted arguments and escape sequences.
    """
    try:
        return shlex.split(command)
    except ValueError as exc:
        raise CommandExecutionError(
            f"Failed to parse command: {exc}",
            command=None,
        ) from exc


def _build_ssh_command(remote_host: str, remote_cwd: str, command: list[str]) -> list[str]:
    """Build a safe SSH command list without shell injection.

    The remote command is constructed as a shell command string, but
    all user-provided components are properly quoted to prevent injection.
    """
    # Quote the remote directory and each command argument
    quoted_cwd = shlex.quote(remote_cwd)
    quoted_command = " ".join(shlex.quote(arg) for arg in command)
    remote_command = f"cd {quoted_cwd} && {quoted_command}"
    return ["ssh", remote_host, remote_command]


def run_job(project_root: Path, job_id: str, execute: bool = False) -> dict[str, object]:
    project_root = project_root.resolve()
    state = load_state(project_root)
    registry_path = project_root / DEFAULT_DELIVERABLES["job_registry"]
    registry = read_yaml(registry_path)
    jobs = registry.get("jobs", {})
    if job_id not in jobs:
        raise StateError(
            f"Unknown job id: {job_id}",
            state_file="runtime/job-registry.yaml",
            field="jobs",
        )

    job = jobs[job_id]
    log_dir = project_root / ".autoresearch/runtime/logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = log_dir / f"{job_id}.stdout.log"
    stderr_path = log_dir / f"{job_id}.stderr.log"

    job["status"] = "running" if execute else "prepared"
    job["started_at"] = datetime.now(timezone.utc).isoformat()
    job["heartbeat_at"] = job["started_at"]
    result_status = "prepared"
    exit_code = 0
    stdout_text = ""
    stderr_text = ""

    if execute:
        try:
            completed = _execute(job, project_root)
            stdout_text = completed.stdout
            stderr_text = completed.stderr
            exit_code = completed.returncode
            result_status = "completed" if exit_code == 0 else "failed"
            job["completed_at"] = datetime.now(timezone.utc).isoformat()
        except (CommandExecutionError, PathSecurityError) as exc:
            stderr_text = f"{type(exc).__name__}: {str(exc)}"
            exit_code = 1
            result_status = "failed"
            job["completed_at"] = datetime.now(timezone.utc).isoformat()

    stdout_path.write_text(stdout_text, encoding="utf-8")
    stderr_path.write_text(stderr_text, encoding="utf-8")
    job["status"] = result_status
    job["exit_code"] = exit_code
    job["stdout_log"] = stdout_path.relative_to(project_root).as_posix()
    job["stderr_log"] = stderr_path.relative_to(project_root).as_posix()
    job["heartbeat_at"] = datetime.now(timezone.utc).isoformat()

    registry["jobs"][job_id] = job
    write_yaml(registry_path, registry)

    active_jobs = [item for item in state.get("active_jobs", []) if item != job_id]
    if execute and result_status != "completed":
        active_jobs.append(job_id)
        state["recovery_status"] = "needs-attention"
        state["progress"]["active_blocker"] = f"job_failed:{job_id}"
        state["progress"]["next_action"] = "recover-stage"
    else:
        state["recovery_status"] = "idle"
        state["progress"]["active_blocker"] = "none"
        state["progress"]["next_action"] = f"job-{result_status}:{job_id}"
    state["active_jobs"] = active_jobs
    save_state(project_root, state)
    generate_dashboard(project_root)

    return {
        "project_root": str(project_root),
        "job_id": job_id,
        "status": result_status,
        "exit_code": exit_code,
        "stdout_log": job["stdout_log"],
        "stderr_log": job["stderr_log"],
    }


def _execute(job: dict[str, str], project_root: Path) -> subprocess.CompletedProcess[str]:
    """Execute a job command safely without shell injection.

    Args:
        job: Job configuration dictionary containing command, cwd, and backend info.
        project_root: The project root directory for path validation.

    Returns:
        CompletedProcess with stdout, stderr, and returncode.

    Raises:
        CommandExecutionError: If command execution fails.
        PathSecurityError: If working directory is outside project root.
    """
    command_str = job["command"]
    cwd = Path(job.get("cwd") or ".")
    backend = job.get("backend", "local")

    if backend == "ssh":
        remote_host = job.get("remote_host")
        if not remote_host:
            raise CommandExecutionError(
                "ssh backend requires remote_host",
                command=None,
            )
        # Validate remote host format (basic check)
        if not remote_host.replace("-", "").replace(".", "").replace("_", "").isalnum():
            raise CommandExecutionError(
                f"Invalid remote host format: {remote_host}",
                command=None,
            )
        remote_cwd = job.get("cwd") or "."
        command_args = _parse_command_safely(command_str)
        ssh_command = _build_ssh_command(remote_host, remote_cwd, command_args)
        try:
            return subprocess.run(
                ssh_command,
                text=True,
                capture_output=True,
                cwd=project_root,
                timeout=3600,  # 1 hour timeout
            )
        except subprocess.TimeoutExpired as exc:
            raise CommandExecutionError(
                "Command timed out after 3600 seconds",
                command=ssh_command,
            ) from exc
        except FileNotFoundError as exc:
            raise CommandExecutionError(
                f"SSH executable not found: {exc}",
                command=ssh_command,
            ) from exc
    else:
        # Local execution: validate cwd and use safe command parsing
        validated_cwd = _validate_cwd(cwd, project_root)
        command_args = _parse_command_safely(command_str)
        try:
            return subprocess.run(
                command_args,
                text=True,
                capture_output=True,
                cwd=validated_cwd,
                timeout=3600,  # 1 hour timeout
            )
        except subprocess.TimeoutExpired as exc:
            raise CommandExecutionError(
                "Command timed out after 3600 seconds",
                command=command_args,
            ) from exc
        except FileNotFoundError as exc:
            raise CommandExecutionError(
                f"Executable not found: {command_args[0] if command_args else 'unknown'}",
                command=command_args,
            ) from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Execute or prepare a scheduled runtime job.")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    result = run_job(Path(args.project_root), args.job_id, execute=args.execute)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] in {"prepared", "completed"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
