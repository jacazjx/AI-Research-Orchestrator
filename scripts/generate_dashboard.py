from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from orchestrator_common import DEFAULT_DELIVERABLES, ensure_project_structure, load_state, write_text_if_needed


def generate_dashboard(project_root: Path) -> dict[str, object]:
    project_root = project_root.resolve()
    state = load_state(project_root)

    status_payload = {
        "project_id": state["project_id"],
        "topic": state["topic"],
        "phase": state["current_phase"],
        "gate": state["current_gate"],
        "inner_loops": state["inner_loops"],
        "outer_loop": state["outer_loop"],
        "phase_reviews": state["phase_reviews"],
        "approval_status": state["approval_status"],
        "progress": state["progress"],
        "active_jobs": state["active_jobs"],
        "pivot_candidates": state["pivot_candidates"],
    }
    status_path = project_root / DEFAULT_DELIVERABLES["dashboard_status"]
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps(status_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    progress_lines = [
        "# Runtime Progress Dashboard",
        "",
        f"- Project ID: `{state['project_id']}`",
        f"- Topic: {state['topic']}",
        f"- Current phase: `{state['current_phase']}`",
        f"- Current gate: `{state['current_gate']}`",
        f"- Current agent: `{state['progress']['current_agent']}`",
        f"- Completion percent: `{state['progress']['completion_percent']}`",
        f"- Last gate result: `{state['progress']['last_gate_result']}`",
        f"- Active blocker: `{state['progress']['active_blocker']}`",
        f"- Next action: `{state['progress']['next_action']}`",
        f"- Active backend: `{state['progress']['active_backend']}`",
        f"- Active GPU: `{state['progress']['active_gpu']}`",
        "",
        "## Reviews",
        "",
    ]
    for key, value in state["phase_reviews"].items():
        progress_lines.append(f"- `{key}`: `{value}`")
    progress_lines.extend(["", "## Human Gates", ""])
    for key, value in state["approval_status"].items():
        progress_lines.append(f"- `{key}`: `{value}`")
    progress_lines.extend(["", "## Active Jobs", ""])
    active_jobs = state.get("active_jobs", [])
    if active_jobs:
        for job in active_jobs:
            progress_lines.append(f"- `{job}`")
    else:
        progress_lines.append("- none")

    progress_path = project_root / DEFAULT_DELIVERABLES["dashboard_progress"]
    progress_path.parent.mkdir(parents=True, exist_ok=True)
    progress_path.write_text("\n".join(progress_lines) + "\n", encoding="utf-8")

    timeline_event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "phase": state["current_phase"],
        "gate": state["current_gate"],
        "next_action": state["progress"]["next_action"],
        "last_gate_result": state["progress"]["last_gate_result"],
    }
    timeline_path = project_root / DEFAULT_DELIVERABLES["dashboard_timeline"]
    timeline_path.parent.mkdir(parents=True, exist_ok=True)
    with timeline_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(timeline_event, ensure_ascii=False) + "\n")

    # Keep placeholder runtime registries present for later scripts.
    write_text_if_needed(project_root / DEFAULT_DELIVERABLES["job_registry"], "jobs: []\n")
    write_text_if_needed(project_root / DEFAULT_DELIVERABLES["gpu_registry"], "devices: []\n")
    write_text_if_needed(project_root / DEFAULT_DELIVERABLES["backend_registry"], "backends:\n- local\n")
    write_text_if_needed(project_root / DEFAULT_DELIVERABLES["sentinel_events"], "")

    return {
        "project_root": str(project_root),
        "status_path": DEFAULT_DELIVERABLES["dashboard_status"],
        "progress_path": DEFAULT_DELIVERABLES["dashboard_progress"],
        "timeline_path": DEFAULT_DELIVERABLES["dashboard_timeline"],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate the runtime dashboard from research-state.yaml.")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()

    # Ensure project structure
    ensure_project_structure(project_root, create_if_missing=False)

    result = generate_dashboard(project_root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Status: {result['status_path']}")
        print(f"Progress: {result['progress_path']}")
        print(f"Timeline: {result['timeline_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
