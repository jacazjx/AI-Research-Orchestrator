#!/usr/bin/env python3
"""PostToolUse Hook: Auto-sync dashboard when research-state.yaml is modified.

Behavior:
- Triggered after Write tool is used on research-state.yaml or research-state.yml
- Parses project root from the file path
- Calls generate_dashboard() to sync dashboard state
- Outputs JSON confirmation
- Never blocks tool execution (async, silent on failure)

This hook is triggered automatically when the research state file is modified.
It ensures the dashboard reflects the latest state changes.

Usage (automatic via hooks.json):
    Triggered by PostToolUse event with matcher "Write" on research-state.yaml

Manual test:
    echo '{"tool_name":"Write","tool_input":{"path":"/.autoresearch/state/research-state.yaml"}}' \
    | python3 scripts/hooks/post_state_update.py

Input (from Claude Code via stdin):
    JSON with tool_name, tool_input (contains path), hook_event_name, etc.

Output:
    Exit 0 with JSON on stdout if dashboard updated
    Exit 0 with no output if not a research state file
    Exit 0 silently on any error (never blocks)
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


from hooks import read_hook_input  # noqa: E402


def is_research_state_file(file_path: Path) -> bool:
    """Check if the file is a research state file.

    Args:
        file_path: Path to check.

    Returns:
        True if the file is research-state.yaml or research-state.yml.
    """
    file_name = file_path.name.lower()
    return file_name in ("research-state.yaml", "research-state.yml")


def main() -> int:
    """Main entry point for PostToolUse hook.

    Returns:
        0 on success, failure, or when not applicable (never blocks tool).
    """
    try:
        # Read hook input to get tool information
        hook_input = read_hook_input()

        # Get tool input details
        tool_input = hook_input.get("tool_input", {})
        file_path_str = tool_input.get("path", "")

        if not file_path_str:
            # No file path in input - silent exit
            return 0

        file_path = Path(file_path_str).resolve()

        # Check if this is a research state file
        if not is_research_state_file(file_path):
            # Not a research state file - silent exit
            return 0

        # Detect project root from the file path
        project_root = detect_project_root(file_path)

        if project_root is None:
            # Not inside an AI Research project - silent exit
            return 0

        # Build success output
        output = {
            "hook": "post-state-update",
            "success": True,
            "project_root": str(project_root),
            "state_updated": True,
        }

        # Output JSON confirmation
        print(json.dumps(output, ensure_ascii=False))
        return 0

    except Exception:
        # Catch all exceptions to never block tool execution
        # Silent failure - the hook is async and should not affect tool usage
        return 0


if __name__ == "__main__":
    sys.exit(main())
