from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from generate_dashboard import generate_dashboard
from orchestrator_common import DEFAULT_DELIVERABLES, PHASE_REQUIRED_DELIVERABLES, ensure_project_structure, load_project_config, load_state, read_yaml, save_state


def inspect_runtime(project_root: Path, stale_after_minutes: int | None = None) -> dict[str, object]:
    project_root = project_root.resolve()
    state = load_state(project_root)
    config = load_project_config(project_root)
    stale_after = stale_after_minutes or int(config["runtime"].get("stale_after_minutes", 30))
    issues: list[dict[str, str]] = []
    now = datetime.now(timezone.utc)

    for key in PHASE_REQUIRED_DELIVERABLES.get(state["current_phase"], ()):
        relative_path = state["deliverables"][key]
        if not (project_root / relative_path).exists():
            issues.append({"type": "missing_deliverable", "target": relative_path})

    registry_path = project_root / DEFAULT_DELIVERABLES["job_registry"]
    if registry_path.exists():
        registry = read_yaml(registry_path)
        for job_id in state.get("active_jobs", []):
            job = registry.get("jobs", {}).get(job_id)
            if job is None:
                issues.append({"type": "missing_job_registry_entry", "target": job_id})
                continue
            heartbeat = job.get("heartbeat_at") or job.get("started_at") or job.get("created_at")
            if job.get("status") == "running" and heartbeat:
                heartbeat_at = datetime.fromisoformat(heartbeat)
                if now - heartbeat_at > timedelta(minutes=stale_after):
                    issues.append({"type": "stale_job", "target": job_id})

    event_path = project_root / DEFAULT_DELIVERABLES["sentinel_events"]
    event_path.parent.mkdir(parents=True, exist_ok=True)
    with event_path.open("a", encoding="utf-8") as handle:
        for issue in issues:
            payload = {
                "timestamp": now.isoformat(),
                "phase": state["current_phase"],
                **issue,
            }
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")

    state["recovery_status"] = "needs-attention" if issues else "idle"
    state["progress"]["active_blocker"] = issues[0]["type"] if issues else "none"
    state["progress"]["next_action"] = "recover-stage" if issues else state["progress"]["next_action"]
    save_state(project_root, state)
    generate_dashboard(project_root)
    return {
        "project_root": str(project_root),
        "issues": issues,
        "status": "attention" if issues else "healthy",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect runtime registries for missing artifacts or stale jobs.")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--stale-after-minutes", type=int)
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()

    # Ensure project structure
    ensure_project_structure(project_root, create_if_missing=False)

    result = inspect_runtime(project_root, stale_after_minutes=args.stale_after_minutes)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "healthy" else 1


if __name__ == "__main__":
    raise SystemExit(main())
