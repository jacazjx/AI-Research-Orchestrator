#!/usr/bin/env python3
"""SessionStart Hook: Runtime issue detection on session resume.

Behavior:
- Detects if CWD is inside an AI Research project
- If yes: runs inspect_runtime checks and outputs issues as JSON
- If no: silent exit (no output, no error)
- Never blocks session start, even on errors

This hook is triggered automatically when a Claude Code session resumes.
It checks for:
- Missing deliverables
- Stale jobs (running jobs without recent heartbeat)
- Runtime registry issues

Usage (automatic via hooks.json):
    Triggered by SessionStart event with matcher "resume"

Manual test:
    echo '{"cwd": "/path/to/project"}' | python3 scripts/hooks/session_resume_sentinel.py

Input (from Claude Code via stdin):
    JSON with session_id, transcript_path, cwd, permission_mode, hook_event_name

Output:
    Exit 0 with JSON on stdout containing runtime inspection results
    Exit 0 with no output if not in a project (silent)
    Exit 0 on any error (never blocks session)

Output format:
    {
        "hook": "session-resume-sentinel",
        "success": true,
        "project_root": "/path/to/project",
        "issues": [
            {"type": "missing_deliverable", "target": "docs/survey/..."},
            {"type": "stale_job", "target": "job-001"}
        ],
        "status": "healthy" | "attention"
    }
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Setup path for imports - scripts directory is parent of hooks
SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import from existing scripts
from reload_project import detect_project_root
from sentinel import inspect_runtime


def read_hook_input() -> dict:
    """Read hook input JSON from stdin.

    Returns:
        Dictionary with hook input data, or empty dict if no input.
    """
    try:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read().strip()
            if input_data:
                return json.loads(input_data)
    except (json.JSONDecodeError, IOError):
        pass
    return {}


def main() -> int:
    """Main entry point for SessionStart resume sentinel hook.

    Returns:
        0 on success, failure, or when not in a project (never blocks session).
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
        # Run runtime inspection using sentinel.py's inspect_runtime function
        result = inspect_runtime(project_root)

        # Build output JSON
        output = {
            "hook": "session-resume-sentinel",
            "success": True,
            "project_root": result.get("project_root", str(project_root)),
            "issues": result.get("issues", []),
            "status": result.get("status", "healthy"),
        }

        # Output JSON - this will be shown to user
        print(json.dumps(output, ensure_ascii=False))
        return 0

    except Exception as e:
        # Catch all exceptions to never block session start
        # Output error status but still return 0
        output = {
            "hook": "session-resume-sentinel",
            "success": False,
            "project_root": str(project_root),
            "issues": [{"type": "error", "target": str(e)}],
            "status": "error",
        }
        print(json.dumps(output, ensure_ascii=False))
        return 0


if __name__ == "__main__":
    sys.exit(main())
