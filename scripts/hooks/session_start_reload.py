#!/usr/bin/env python3
"""SessionStart Hook: Auto-reload project context.

Behavior:
- Detects if CWD is inside an AI Research project
- If yes: outputs JSON with project state and compact statusline
- If no: silent exit (no output, no error)

This hook is triggered automatically when a new Claude Code session starts.
It restores project context without requiring explicit /reload command.

Usage (automatic via hooks.json):
    Triggered by SessionStart event with matcher "startup" or "resume"

Manual test:
    echo '{"cwd": "/path/to/project"}' | python3 scripts/hooks/session_start_reload.py

Input (from Claude Code via stdin):
    JSON with session_id, transcript_path, cwd, permission_mode, hook_event_name

Output:
    Exit 0 with JSON on stdout for project context
    Exit 0 with no output if not in a project (silent)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Setup path for imports - scripts directory is parent of hooks
SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import from existing scripts
from reload_project import (  # noqa: E402
    detect_project_root,
    load_gpu_registry,
    load_project_state,
)


from hooks import read_hook_input  # noqa: E402


def main() -> int:
    """Main entry point for SessionStart hook.

    Returns:
        0 on success or when not in a project (never blocks session)
    """
    # Read hook input to get cwd
    hook_input = read_hook_input()

    # Determine working directory
    # Use cwd from hook input, fallback to actual cwd
    cwd_str = hook_input.get("cwd", str(Path.cwd()))
    cwd = Path(cwd_str)

    # Detect if we're inside an AI Research project
    project_root = detect_project_root(cwd)

    if project_root is None:
        # Not in an AI Research project - silent exit
        # No output means the hook didn't match, session continues normally
        return 0

    try:
        # Load project state and configuration
        state = load_project_state(project_root)
        gpu_registry = load_gpu_registry()

        # Build output with essential context
        # This output will be shown to the user when session starts
        output = {
            # Hook metadata
            "hook": "session-start-reload",
            "success": True,
            "project_root": str(project_root),
            # Project identification
            "project_id": state.get("project_id", "unknown"),
            "topic": state.get("topic", ""),
            "research_type": state.get("research_type", "ml_experiment"),
            # Current progress
            "current_phase": state.get("current_phase", "survey"),
            "current_gate": state.get("current_gate", "gate_1"),
            "state_version": state.get("state_version", "2.0.0"),
            # Additional context for session restoration
            "progress": {
                "completion_percent": state.get("progress", {}).get("completion_percent", 0),
                "current_agent": state.get("progress", {}).get("current_agent", "orchestrator"),
                "next_action": state.get("progress", {}).get("next_action", ""),
            },
            "config": {
                "language_policy": state.get("language_policy", {}),
                "loop_limits": state.get("loop_limits", {}),
            },
        }

        # Add active GPU info if available
        active_gpu = state.get("progress", {}).get("active_gpu", "unassigned")
        if active_gpu != "unassigned" and gpu_registry.get("gpus", {}).get(active_gpu):
            output["resources"] = {
                "active_gpu": active_gpu,
                "gpu_name": gpu_registry["gpus"][active_gpu].get("name", active_gpu),
            }

        # Output JSON - this will be shown to user
        print(json.dumps(output, ensure_ascii=False))
        return 0

    except FileNotFoundError:
        # State file not found - output warning so user knows
        output = {
            "hook": "session-start-reload",
            "success": False,
            "project_root": str(project_root),
            "error": "research-state.yaml not found — project may be corrupted or incomplete",
        }
        print(json.dumps(output, ensure_ascii=False))
        return 0

    except Exception as e:
        # Output error context so user can diagnose, but never block session
        output = {
            "hook": "session-start-reload",
            "success": False,
            "project_root": str(project_root),
            "error": f"Failed to reload project state: {e}",
        }
        print(json.dumps(output, ensure_ascii=False))
        return 0


if __name__ == "__main__":
    sys.exit(main())
