from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from exceptions import ConfigurationError, StateError, ValidationError
from generate_dashboard import generate_dashboard
from orchestrator_common import DEFAULT_DELIVERABLES, ensure_project_structure, load_state, read_yaml, save_state, write_yaml


def recover_stage(project_root: Path, mode: str, job_id: str = "") -> dict[str, object]:
    project_root = project_root.resolve()
    state = load_state(project_root)
    registry_path = project_root / DEFAULT_DELIVERABLES["job_registry"]
    registry = read_yaml(registry_path) if registry_path.exists() else {"jobs": {}}

    if mode == "regen-dashboard":
        generate_dashboard(project_root)
        return {"project_root": str(project_root), "mode": mode, "status": "completed"}

    if not job_id:
        raise ValidationError("job_id is required for job recovery modes")
    if job_id not in registry.get("jobs", {}):
        raise StateError(
            f"Unknown job id: {job_id}",
            state_file="runtime/job-registry.yaml",
            field="jobs",
        )

    job = registry["jobs"][job_id]
    now = datetime.now(timezone.utc).isoformat()
    if mode == "retry-job":
        job["status"] = "scheduled"
        job["retry_count"] = int(job.get("retry_count", 0)) + 1
        state["progress"]["next_action"] = f"rerun:{job_id}"
    elif mode == "resume-job":
        job["status"] = "running"
        job["heartbeat_at"] = now
        state["progress"]["next_action"] = f"resume:{job_id}"
    else:
        raise ConfigurationError(
            f"Unsupported recovery mode: {mode}",
            key="mode",
        )

    registry["jobs"][job_id] = job
    write_yaml(registry_path, registry)
    active_jobs = list(state.get("active_jobs", []))
    if job_id not in active_jobs:
        active_jobs.append(job_id)
    state["active_jobs"] = active_jobs
    state["recovery_status"] = "recovering"
    state["progress"]["active_blocker"] = "none"
    save_state(project_root, state)
    generate_dashboard(project_root)
    return {"project_root": str(project_root), "mode": mode, "job_id": job_id, "status": "completed"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Recover a stale or failed stage runtime.")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--mode", required=True, choices=("retry-job", "resume-job", "regen-dashboard"))
    parser.add_argument("--job-id", default="")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()

    # Ensure project structure
    ensure_project_structure(project_root, create_if_missing=False)

    result = recover_stage(project_root, mode=args.mode, job_id=args.job_id)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
