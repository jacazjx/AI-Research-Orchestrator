#!/usr/bin/env python3
"""System integrity verification script.

This script performs comprehensive checks on the research project workspace
to ensure all required components are present and valid.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from orchestrator_common import (  # noqa: E402
    DEFAULT_DELIVERABLES,
    PHASE_REQUIRED_DELIVERABLES,
    REQUIRED_DIRECTORIES,
    load_project_config,
    load_state,
)

try:
    from preflight import run_preflight_checks

    _PREFLIGHT_AVAILABLE = True
except ImportError:
    _PREFLIGHT_AVAILABLE = False


def check_directory_structure(project_root: Path) -> dict[str, Any]:
    """Check that all required directories exist."""
    results = {
        "passed": True,
        "checks": [],
    }

    # Check new required directories
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
    results = {
        "passed": True,
        "checks": [],
    }

    required_files = [
        "research_state",
        "workspace_manifest",
        "idea_brief",
        "project_config",
    ]

    for key in required_files:
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
    results = {
        "passed": True,
        "checks": [],
        "errors": [],
    }

    state_path = project_root / DEFAULT_DELIVERABLES["research_state"]

    if not state_path.exists():
        results["passed"] = False
        results["errors"].append("research-state.yaml does not exist")
        return results

    try:
        state = load_state(project_root)

        # Check required fields
        required_fields = [
            "project_id",
            "topic",
            "current_phase",
            "current_gate",
            "phase_reviews",
            "approval_status",
            "loop_counts",
            "deliverables",
        ]

        for field in required_fields:
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

        # Check current_phase is valid (support both new semantic and legacy names)
        valid_phases = [
            # New semantic names
            "survey",
            "pilot",
            "experiments",
            "paper",
            "reflection",
            # Legacy names for backward compatibility
            "01-survey",
            "02-pilot-analysis",
            "03-full-experiments",
            "04-paper",
            "05-reflection-evolution",
            "06-archive",
        ]
        current_phase = state.get("current_phase", "")
        valid_phase = current_phase in valid_phases
        results["checks"].append(
            {
                "type": "state_value",
                "name": "current_phase validity",
                "value": current_phase,
                "status": "pass" if valid_phase else "fail",
            }
        )
        if not valid_phase:
            results["passed"] = False

    except Exception as e:
        results["passed"] = False
        results["errors"].append(f"Failed to parse state: {e}")

    return results


def check_config_integrity(project_root: Path) -> dict[str, Any]:
    """Check that orchestrator-config.yaml is valid."""
    results = {
        "passed": True,
        "checks": [],
        "errors": [],
    }

    config_path = project_root / DEFAULT_DELIVERABLES["project_config"]

    if not config_path.exists():
        # Config may not exist yet, use defaults
        results["checks"].append(
            {
                "type": "config",
                "name": "config file",
                "exists": False,
                "status": "warn",
                "message": "Config file does not exist, using defaults",
            }
        )
        return results

    try:
        config = load_project_config(project_root)

        # Check for required sections
        required_sections = ["loop_limits", "languages"]
        for section in required_sections:
            has_section = section in config
            results["checks"].append(
                {
                    "type": "config_section",
                    "name": section,
                    "exists": has_section,
                    "status": "pass" if has_section else "warn",
                }
            )

    except Exception as e:
        results["passed"] = False
        results["errors"].append(f"Failed to parse config: {e}")

    return results


def check_phase_deliverables(project_root: Path) -> dict[str, Any]:
    """Check that required deliverables for current phase exist."""
    results = {
        "passed": True,
        "checks": [],
        "phase_results": {},
    }

    # Check each phase's deliverables
    for phase, deliverable_keys in PHASE_REQUIRED_DELIVERABLES.items():
        phase_checks = []
        all_present = True

        for key in deliverable_keys:
            relative_path = DEFAULT_DELIVERABLES[key]
            file_path = project_root / relative_path
            exists = file_path.exists()
            phase_checks.append(
                {
                    "deliverable": key,
                    "path": relative_path,
                    "exists": exists,
                }
            )
            if not exists:
                all_present = False

        results["phase_results"][phase] = {
            "all_present": all_present,
            "checks": phase_checks,
        }

    return results


def check_gate_status(project_root: Path) -> dict[str, Any]:
    """Check the gate approval status."""
    results = {
        "passed": True,
        "checks": [],
        "gates": {},
    }

    try:
        state = load_state(project_root)
        approval_status = state.get("approval_status", {})
        phase_reviews = state.get("phase_reviews", {})
    except Exception:
        results["passed"] = False
        results["errors"] = ["Cannot load state to check gate status"]
        return results

    gates = ["gate_1", "gate_2", "gate_3", "gate_4", "gate_5"]
    reviews = [
        "survey_critic",
        "pilot_adviser",
        "experiment_adviser",
        "paper_reviewer",
        "reflection_curator",
    ]

    for gate in gates:
        status = approval_status.get(gate, "pending")
        results["gates"][gate] = status
        results["checks"].append(
            {
                "gate": gate,
                "status": status,
            }
        )

    for review in reviews:
        status = phase_reviews.get(review, "pending")
        results["checks"].append(
            {
                "review": review,
                "status": status,
            }
        )

    return results


def run_all_checks(project_root: Path) -> dict[str, Any]:
    """Run all integrity checks."""
    result = {
        "project_root": str(project_root),
        "directory_structure": check_directory_structure(project_root),
        "required_files": check_required_files(project_root),
        "state_integrity": check_state_integrity(project_root),
        "config_integrity": check_config_integrity(project_root),
        "phase_deliverables": check_phase_deliverables(project_root),
        "gate_status": check_gate_status(project_root),
    }
    if _PREFLIGHT_AVAILABLE:
        try:
            preflight = run_preflight_checks()
            result["preflight"] = {
                "passed": True,  # always True — advisory only
                "warnings": preflight["warnings"],
                "latex": preflight["latex"]["available"],
                "semantic_scholar": preflight["semantic_scholar"]["reachable"],
                "gpu": preflight["gpu"]["available"],
            }
        except Exception:  # noqa: BLE001
            result["preflight"] = {"passed": True, "warnings": ["preflight check failed"]}
    return result


def format_report(report: dict[str, Any]) -> str:
    """Format the verification report as human-readable text."""
    lines = [
        "# System Integrity Report",
        "",
        f"Project: `{report['project_root']}`",
        "",
    ]

    # Overall status
    all_passed = all(
        check.get("passed", True)
        for key, check in report.items()
        if isinstance(check, dict) and "passed" in check
    )
    lines.append(f"**Overall Status**: {'✅ PASS' if all_passed else '❌ FAIL'}")
    lines.append("")

    # Directory structure
    lines.append("## Directory Structure")
    dir_check = report.get("directory_structure", {})
    for check in dir_check.get("checks", []):
        status = "✅" if check["status"] == "pass" else "❌"
        lines.append(f"- {status} `{check['name']}`")
    lines.append("")

    # Required files
    lines.append("## Required Files")
    file_check = report.get("required_files", {})
    for check in file_check.get("checks", []):
        status = "✅" if check["status"] == "pass" else "❌"
        lines.append(f"- {status} `{check['name']}`")
    lines.append("")

    # State integrity
    lines.append("## State Integrity")
    state_check = report.get("state_integrity", {})
    for check in state_check.get("checks", []):
        status = "✅" if check["status"] == "pass" else "❌"
        lines.append(f"- {status} {check['name']}")
    for error in state_check.get("errors", []):
        lines.append(f"- ❌ {error}")
    lines.append("")

    # Gate status
    lines.append("## Gate Status")
    gate_check = report.get("gate_status", {})
    for gate, status in gate_check.get("gates", {}).items():
        icon = "✅" if status == "approved" else "⏳" if status == "pending" else "❌"
        lines.append(f"- {icon} `{gate}`: {status}")
    lines.append("")

    # Phase deliverables
    lines.append("## Phase Deliverables")
    phase_check = report.get("phase_deliverables", {})
    for phase, phase_data in phase_check.get("phase_results", {}).items():
        status = "✅" if phase_data["all_present"] else "⚠️"
        lines.append(f"- {status} `{phase}`")
        for check in phase_data.get("checks", []):
            icon = "✅" if check["exists"] else "❌"
            lines.append(f"  - {icon} {check['deliverable']}")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify system integrity")
    parser.add_argument("--project-root", required=True, help="Path to project root")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--quiet", action="store_true", help="Only output pass/fail")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    report = run_all_checks(project_root)

    if args.json:
        print(json.dumps(report, indent=2, default=str))
    elif args.quiet:
        all_passed = all(
            check.get("passed", True)
            for key, check in report.items()
            if isinstance(check, dict) and "passed" in check
        )
        print("PASS" if all_passed else "FAIL")
    else:
        print(format_report(report))

    # Return exit code
    all_passed = all(
        check.get("passed", True)
        for key, check in report.items()
        if isinstance(check, dict) and "passed" in check
    )
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
