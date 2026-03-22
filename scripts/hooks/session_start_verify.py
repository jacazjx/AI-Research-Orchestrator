#!/usr/bin/env python3
"""SessionStart Hook: System integrity verification.

Behavior:
- Detects if CWD is inside an AI Research project
- If yes: runs system integrity checks and outputs results as JSON
- If no: silent exit (no output, no error)
- Never blocks session start, even on errors

Usage (automatic via hooks.json):
    Triggered by SessionStart event with matcher "startup"
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# Setup path for imports - scripts directory is parent of hooks
SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from reload_project import detect_project_root  # noqa: E402

# Import from existing scripts
from orchestrator_common import (  # noqa: E402
    DEFAULT_DELIVERABLES,
    REQUIRED_DIRECTORIES,
    load_state,
)


from hooks import read_hook_input  # noqa: E402


def check_directory_structure(project_root: Path) -> dict[str, Any]:
    """Check that all required directories exist."""
    results: dict[str, Any] = {"passed": True, "checks": []}
    for dir_name in REQUIRED_DIRECTORIES:
        dir_path = project_root / dir_name
        exists = dir_path.exists() and dir_path.is_dir()
        results["checks"].append(
            {
                "type": "directory",
                "name": dir_name,
                "exists": exists,
                "status": "pass" if exists else "fail",
            }
        )
        if not exists:
            results["passed"] = False
    return results


def check_required_files(project_root: Path) -> dict[str, Any]:
    """Check that all required files exist."""
    results: dict[str, Any] = {"passed": True, "checks": []}
    for key in ["research_state", "workspace_manifest", "idea_brief", "project_config"]:
        relative_path = DEFAULT_DELIVERABLES[key]
        file_path = project_root / relative_path
        exists = file_path.exists()
        results["checks"].append(
            {
                "type": "file",
                "name": relative_path,
                "exists": exists,
                "status": "pass" if exists else "fail",
            }
        )
        if not exists:
            results["passed"] = False
    return results


def check_state_integrity(project_root: Path) -> dict[str, Any]:
    """Check that research-state.yaml is valid."""
    results: dict[str, Any] = {"passed": True, "checks": [], "errors": []}
    state_path = project_root / DEFAULT_DELIVERABLES["research_state"]
    if not state_path.exists():
        results["passed"] = False
        results["errors"].append("research-state.yaml does not exist")
        return results
    try:
        state = load_state(project_root)
        for field in [
            "project_id",
            "topic",
            "current_phase",
            "current_gate",
            "phase_reviews",
            "approval_status",
            "loop_counts",
            "deliverables",
        ]:
            has_field = field in state
            results["checks"].append(
                {
                    "type": "state_field",
                    "name": field,
                    "exists": has_field,
                    "status": "pass" if has_field else "fail",
                }
            )
            if not has_field:
                results["passed"] = False
    except Exception as e:
        results["passed"] = False
        results["errors"].append(f"Failed to parse state: {e}")
    return results


def extract_issues(check_result: dict) -> list[str]:
    """Extract issue messages from a check result."""
    issues = []
    for error in check_result.get("errors", []):
        issues.append(f"Error: {error}")
    for check in check_result.get("checks", []):
        if check.get("status") == "fail":
            name = check.get("name", check.get("deliverable", "unknown"))
            check_type = check.get("type", "check")
            issues.append(f"{check_type}: {name}")
    return issues


def main() -> int:
    """Main entry point for SessionStart verification hook."""
    hook_input = read_hook_input()
    cwd_str = hook_input.get("cwd", str(Path.cwd()))
    cwd = Path(cwd_str)
    project_root = detect_project_root(cwd)

    if project_root is None:
        return 0

    try:
        dir_result = check_directory_structure(project_root)
        files_result = check_required_files(project_root)
        state_result = check_state_integrity(project_root)

        dir_passed = dir_result.get("passed", False)
        files_passed = files_result.get("passed", False)
        state_passed = state_result.get("passed", False)

        all_passed = dir_passed and files_passed and state_passed
        any_passed = dir_passed or files_passed or state_passed

        if all_passed:
            overall_status = "healthy"
        elif any_passed:
            overall_status = "degraded"
        else:
            overall_status = "error"

        output = {
            "hook": "session-start-verify",
            "success": True,
            "project_root": str(project_root),
            "checks": {
                "directory_structure": {"passed": dir_passed, "issues": extract_issues(dir_result)},
                "required_files": {"passed": files_passed, "issues": extract_issues(files_result)},
                "state_validity": {"passed": state_passed, "issues": extract_issues(state_result)},
            },
            "overall_status": overall_status,
        }
        print(json.dumps(output, ensure_ascii=False))
        return 0

    except Exception as e:
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
