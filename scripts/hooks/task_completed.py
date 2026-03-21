#!/usr/bin/env python3
"""Hook: Handle TaskCompleted events from Agent Teams.

This hook validates task completion quality and logs the event.

Input (via stdin):
    {
        "event": "TaskCompleted",
        "task_id": "survey-primary",
        "task_status": "completed",
        "agent_name": "survey",
        "deliverables": [...]
    }

Output:
    - Exit 0: Success (task validated)
    - Exit 2: Blocking (task needs review)
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def get_project_root() -> Path | None:
    """Try to find project root."""
    cwd = Path.cwd()
    if (cwd / ".autoresearch").exists():
        return cwd
    for parent in cwd.parents:
        if (parent / ".autoresearch").exists():
            return parent
    return None


def validate_deliverables(deliverables: list[str] | None, project_root: Path) -> list[str]:
    """Validate that deliverables exist and are not empty."""
    issues = []
    if not deliverables:
        return issues

    for deliverable in deliverables:
        path = project_root / deliverable
        if not path.exists():
            issues.append(f"Missing deliverable: {deliverable}")
        elif path.stat().st_size == 0:
            issues.append(f"Empty deliverable: {deliverable}")

    return issues


def main() -> int:
    """Main hook entry point."""
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        return 1

    event_type = hook_input.get("event", "")
    if event_type != "TaskCompleted":
        print(f"Error: Expected TaskCompleted event, got {event_type}", file=sys.stderr)
        return 1

    task_id = hook_input.get("task_id", "unknown")
    task_status = hook_input.get("task_status", "unknown")
    agent_name = hook_input.get("agent_name", "unknown")
    deliverables = hook_input.get("deliverables", [])

    project_root = get_project_root()

    if project_root:
        sentinel_path = project_root / ".autoresearch" / "runtime" / "sentinel-events.ndjson"
        sentinel_path.parent.mkdir(parents=True, exist_ok=True)

        event = {
            "type": "task_completed",
            "task_id": task_id,
            "task_status": task_status,
            "agent_name": agent_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        with open(sentinel_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

        issues = validate_deliverables(deliverables, project_root)
        if issues:
            response = {"status": "warning", "issues": issues}
            print(json.dumps(response, ensure_ascii=False))
            return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
