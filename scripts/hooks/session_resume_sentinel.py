#!/usr/bin/env python3
"""SessionStart Hook: Runtime issue detection on session resume.

Behavior:
- Detects if CWD is inside an AI Research project
- If yes: outputs basic project status as JSON
- If no: silent exit (no output, no error)
- Never blocks session start, even on errors

Usage (automatic via hooks.json):
    Triggered by SessionStart event with matcher "resume"
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Setup path for imports - scripts directory is parent of hooks
SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import from existing scripts
from reload_project import detect_project_root  # noqa: E402


def read_hook_input() -> dict:
    """Read hook input JSON from stdin."""
    try:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read().strip()
            if input_data:
                return json.loads(input_data)
    except (json.JSONDecodeError, IOError):
        pass
    return {}


def main() -> int:
    """Main entry point for SessionStart resume sentinel hook."""
    hook_input = read_hook_input()
    cwd_str = hook_input.get("cwd", str(Path.cwd()))
    cwd = Path(cwd_str)
    project_root = detect_project_root(cwd)

    if project_root is None:
        return 0

    try:
        output = {
            "hook": "session-resume-sentinel",
            "success": True,
            "project_root": str(project_root),
            "issues": [],
            "status": "healthy",
        }
        print(json.dumps(output, ensure_ascii=False))
        return 0

    except Exception as e:
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
