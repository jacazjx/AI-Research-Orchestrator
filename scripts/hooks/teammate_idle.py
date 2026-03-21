#!/usr/bin/env python3
"""Hook: Handle TeammateIdle events from Agent Teams.

This hook is triggered when an agent teammate goes idle.
It logs the event and optionally notifies the Orchestrator.

Input (via stdin):
    {
        "event": "TeammateIdle",
        "agent_name": "survey",
        "team_name": "research-survey",
        "session_id": "...",
        "message_summary": "..."
    }

Output:
    - Exit 0: Success (no action needed)
    - Exit 2: Blocking (requires Orchestrator attention)
    - stdout: JSON response (optional)
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def get_project_root() -> Path | None:
    """Try to find project root from environment or current directory."""
    cwd = Path.cwd()
    if (cwd / ".autoresearch").exists():
        return cwd
    for parent in cwd.parents:
        if (parent / ".autoresearch").exists():
            return parent
    return None


def log_idle_event(agent_name: str, team_name: str, message_summary: str | None = None) -> None:
    """Log idle event to sentinel events file."""
    project_root = get_project_root()
    if not project_root:
        return

    sentinel_path = project_root / ".autoresearch" / "runtime" / "sentinel-events.ndjson"
    sentinel_path.parent.mkdir(parents=True, exist_ok=True)

    event = {
        "type": "teammate_idle",
        "agent_name": agent_name,
        "team_name": team_name,
        "message_summary": message_summary,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    with open(sentinel_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> int:
    """Main hook entry point."""
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        return 1

    event_type = hook_input.get("event", "")
    if event_type != "TeammateIdle":
        print(f"Error: Expected TeammateIdle event, got {event_type}", file=sys.stderr)
        return 1

    agent_name = hook_input.get("agent_name", "unknown")
    team_name = hook_input.get("team_name", "unknown")
    message_summary = hook_input.get("message_summary")

    log_idle_event(agent_name, team_name, message_summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
