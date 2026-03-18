#!/usr/bin/env python3
"""SessionStart Hook: System integrity verification.

Behavior:
- Detects if CWD is inside an AI Research project
- If yes: runs system integrity checks and outputs results as JSON
- If no: silent exit (no output, no error)
- Never blocks session start, even on errors

This hook is triggered automatically when a new Claude Code session starts.
It verifies project integrity and warns about issues without blocking.

Usage (automatic via hooks.json):
    Triggered by SessionStart event with matcher "startup"

Manual test:
    echo '{"cwd": "/path/to/project"}' | python3 scripts/hooks/session_start_verify.py

Input (from Claude Code via stdin):
    JSON with session_id, transcript_path, cwd, permission_mode, hook_event_name

Output:
    Exit 0 with JSON on stdout containing verification results
    Exit 0 with no output if not in a project (silent)
    Exit 0 on any error (never blocks session)

Output format:
    {
        "hook": "session-start-verify",
        "success": true,
        "project_root": "/path/to/project",
        "checks": {
            "directory_structure": {"passed": true, "issues": []},
            "required_files": {"passed": true, "issues": []},
            "state_validity": {"passed": true, "issues": []}
        },
        "overall_status": "healthy" | "degraded" | "error"
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
from verify_system import (
    check_directory_structure,
    check_required_files,
    check_state_integrity,
)


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


def extract_issues(check_result: dict) -> list[str]:
    """Extract issue messages from a check result.

    Args:
        check_result: Result dict from a check function.

    Returns:
        List of issue strings.
    """
    issues = []

    # Collect errors first
    for error in check_result.get("errors", []):
        issues.append(f"Error: {error}")

    # Collect failed checks
    for check in check_result.get("checks", []):
        status = check.get("status", "")
        if status == "fail":
            name = check.get("name", check.get("deliverable", "unknown"))
            check_type = check.get("type", "check")
            issues.append(f"{check_type}: {name}")

    return issues


def determine_overall_status(
    dir_passed: bool,
    files_passed: bool,
    state_passed: bool,
    had_exception: bool = False,
) -> str:
    """Determine the overall status based on check results.

    Args:
        dir_passed: Whether directory structure check passed.
        files_passed: Whether required files check passed.
        state_passed: Whether state validity check passed.
        had_exception: Whether an exception occurred during checks.

    Returns:
        Overall status string: "healthy", "degraded", or "error".
    """
    if had_exception:
        return "error"

    all_passed = dir_passed and files_passed and state_passed
    any_passed = dir_passed or files_passed or state_passed

    if all_passed:
        return "healthy"
    elif any_passed:
        return "degraded"
    else:
        return "error"


def main() -> int:
    """Main entry point for SessionStart verification hook.

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
        # Run verification checks
        dir_result = check_directory_structure(project_root)
        files_result = check_required_files(project_root)
        state_result = check_state_integrity(project_root)

        # Extract pass/fail status
        dir_passed = dir_result.get("passed", False)
        files_passed = files_result.get("passed", False)
        state_passed = state_result.get("passed", False)

        # Extract issues
        dir_issues = extract_issues(dir_result)
        files_issues = extract_issues(files_result)
        state_issues = extract_issues(state_result)

        # Determine overall status
        overall_status = determine_overall_status(
            dir_passed, files_passed, state_passed, had_exception=False
        )

        # Build output JSON
        output = {
            "hook": "session-start-verify",
            "success": True,
            "project_root": str(project_root),
            "checks": {
                "directory_structure": {
                    "passed": dir_passed,
                    "issues": dir_issues,
                },
                "required_files": {
                    "passed": files_passed,
                    "issues": files_issues,
                },
                "state_validity": {
                    "passed": state_passed,
                    "issues": state_issues,
                },
            },
            "overall_status": overall_status,
        }

        # Output JSON - this will be shown to user
        print(json.dumps(output, ensure_ascii=False))
        return 0

    except Exception as e:
        # Catch all exceptions to never block session start
        # Output error status but still return 0
        output = {
            "hook": "session-start-verify",
            "success": False,
            "project_root": str(project_root),
            "checks": {
                "directory_structure": {"passed": False, "issues": []},
                "required_files": {"passed": False, "issues": []},
                "state_validity": {"passed": False, "issues": []},
            },
            "overall_status": "error",
            "error": str(e),
        }
        print(json.dumps(output, ensure_ascii=False))
        return 0


if __name__ == "__main__":
    sys.exit(main())
