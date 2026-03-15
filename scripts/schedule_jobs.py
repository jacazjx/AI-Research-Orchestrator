from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from exceptions import ConfigurationError
from generate_dashboard import generate_dashboard

from orchestrator_common import (
    DEFAULT_DELIVERABLES,
    load_project_config,
    load_state,
    read_yaml,
    save_state,
    write_yaml,
)

IMPLEMENTED_BACKENDS = {"local", "ssh"}


def schedule_job(
    project_root: Path,
    command: str,
    backend: str = "local",
    phase: str | None = None,
    gpu_id: str = "unassigned",
    cwd: str = ".",
    remote_host: str = "",
) -> dict[str, object]:
    project_root = project_root.resolve()
    state = load_state(project_root)
    config = load_project_config(project_root)
    if backend not in IMPLEMENTED_BACKENDS:
        raise ConfigurationError(
            f"Backend is not implemented by the runtime: {backend}",
            key="backend",
        )
    if config["backends"].get(backend) != "enabled":
        raise ConfigurationError(
            f"Backend is not enabled in orchestrator-config.yaml: {backend}",
            config_file="orchestrator-config.yaml",
            key=f"backends.{backend}",
        )
    registry = _load_job_registry(project_root)
    devices = _load_gpu_registry(project_root)
    backends = _load_backend_registry(project_root)
    if config["runtime"].get("auto_discover_gpu") and gpu_id == "auto" and not devices["devices"]:
        devices["devices"] = _discover_gpus()

    job_id = f"job-{len(registry['jobs']) + 1}"
    assigned_gpu = _assign_gpu(devices, gpu_id, job_id)
    backends["backends"][backend] = {"status": "enabled", "remote_host": remote_host or "local"}
    registry["jobs"][job_id] = {
        "command": command,
        "backend": backend,
        "phase": phase or state["current_phase"],
        "cwd": (
            cwd
            if backend == "ssh"
            else str((project_root / cwd).resolve()) if not Path(cwd).is_absolute() else cwd
        ),
        "gpu": assigned_gpu,
        "remote_host": remote_host,
        "status": "scheduled",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    write_yaml(project_root / DEFAULT_DELIVERABLES["job_registry"], registry)
    write_yaml(project_root / DEFAULT_DELIVERABLES["gpu_registry"], devices)
    write_yaml(project_root / DEFAULT_DELIVERABLES["backend_registry"], backends)

    active_jobs = list(state.get("active_jobs", []))
    if job_id not in active_jobs:
        active_jobs.append(job_id)
    state["active_jobs"] = active_jobs
    state["progress"]["active_backend"] = backend
    state["progress"]["active_gpu"] = assigned_gpu
    state["progress"]["next_action"] = f"run-{job_id}"
    save_state(project_root, state)
    generate_dashboard(project_root)

    return {
        "project_root": str(project_root),
        "job_id": job_id,
        "backend": backend,
        "gpu": assigned_gpu,
        "status": "scheduled",
    }


def _assign_gpu(devices: dict[str, object], gpu_id: str, job_id: str) -> str:
    if devices["devices"] == {} and gpu_id == "unassigned":
        return "unassigned"
    if gpu_id == "auto":
        gpu_id = "unassigned"
    if gpu_id == "unassigned":
        for candidate, info in devices["devices"].items():
            if info.get("status") != "allocated":
                info["status"] = "allocated"
                info["allocated_to"] = job_id
                return candidate
        return "unassigned"
    if gpu_id not in devices["devices"]:
        devices["devices"][gpu_id] = {"status": "allocated", "allocated_to": job_id}
        return gpu_id
    devices["devices"][gpu_id]["status"] = "allocated"
    devices["devices"][gpu_id]["allocated_to"] = job_id
    return gpu_id


def _load_job_registry(project_root: Path) -> dict[str, object]:
    path = project_root / DEFAULT_DELIVERABLES["job_registry"]
    if not path.exists():
        return {"jobs": {}}
    data = read_yaml(path)
    jobs = data.get("jobs", {})
    if isinstance(jobs, list):
        jobs = {}
    return {"jobs": jobs}


def _load_gpu_registry(project_root: Path) -> dict[str, object]:
    path = project_root / DEFAULT_DELIVERABLES["gpu_registry"]
    if not path.exists():
        return {"devices": {}}
    data = read_yaml(path)
    devices = data.get("devices", {})
    if isinstance(devices, list):
        devices = {}
    return {"devices": devices}


def _load_backend_registry(project_root: Path) -> dict[str, object]:
    path = project_root / DEFAULT_DELIVERABLES["backend_registry"]
    if not path.exists():
        return {"backends": {"local": {"status": "enabled", "remote_host": "local"}}}
    data = read_yaml(path)
    backends = data.get("backends", {})
    if isinstance(backends, list):
        normalized = {"local": {"status": "enabled", "remote_host": "local"}}
        for item in backends:
            normalized[str(item)] = {"status": "enabled", "remote_host": str(item)}
        backends = normalized
    return {"backends": backends or {"local": {"status": "enabled", "remote_host": "local"}}}


def _discover_gpus() -> dict[str, dict[str, str]]:
    try:
        completed = subprocess.run(
            ["nvidia-smi", "--query-gpu=index,name", "--format=csv,noheader"],
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError:
        return {}
    if completed.returncode != 0:
        return {}
    devices: dict[str, dict[str, str]] = {}
    for line in completed.stdout.splitlines():
        if not line.strip():
            continue
        index, _, name = line.partition(",")
        gpu_id = index.strip()
        devices[gpu_id] = {
            "status": "idle",
            "name": name.strip() or f"gpu-{gpu_id}",
            "allocated_to": "",
        }
    return devices


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Register a runtime job and allocate backend/GPU metadata."
    )
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--command", required=True)
    parser.add_argument("--backend", default="local")
    parser.add_argument("--phase")
    parser.add_argument("--gpu-id", default="unassigned")
    parser.add_argument("--cwd", default=".")
    parser.add_argument("--remote-host", default="")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    result = schedule_job(
        Path(args.project_root),
        command=args.command,
        backend=args.backend,
        phase=args.phase,
        gpu_id=args.gpu_id,
        cwd=args.cwd,
        remote_host=args.remote_host,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
