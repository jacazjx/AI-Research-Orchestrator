from __future__ import annotations

import argparse
import json
from pathlib import Path

from orchestrator_common import (
    HANDOFF_REQUIREMENTS,
    LOOP_REQUIREMENTS,
    load_state,
    validate_structured_signals,
    validate_deliverable_content,
    validate_deliverable_location,
    ensure_project_structure,
)


def validate_handoff(project_root: Path, target: str) -> dict[str, object]:
    project_root = project_root.resolve()
    state = load_state(project_root)

    if target in LOOP_REQUIREMENTS:
        loop_key, status_group, status_key = LOOP_REQUIREMENTS[target]
        current_count = int(state["loop_counts"].get(loop_key, 0))
        limit = int(state["loop_limits"].get(loop_key, 0))
        approved = state[status_group].get(status_key)
        escalate = current_count >= limit and approved != "approved"
        return {
            "ok": not escalate,
            "status": "escalate" if escalate else "pass",
            "target": target,
            "project_root": str(project_root),
            "loop_key": loop_key,
            "current_count": current_count,
            "limit": limit,
            "status_group": status_group,
            "gate": status_key,
            "gate_status": approved,
            "errors": [] if not escalate else [f"{loop_key} reached limit {limit}; escalate to the user."],
        }

    requirement = HANDOFF_REQUIREMENTS[target]
    errors: list[str] = []
    missing_files: list[str] = []

    status_checks: list[dict[str, str]] = []
    for status_group, status_key in requirement["statuses"]:
        current_status = state[status_group].get(status_key)
        status_checks.append(
            {
                "group": status_group,
                "key": status_key,
                "status": current_status,
            }
        )
        if current_status != "approved":
            errors.append(
                f"{status_group}.{status_key} must be approved before {target}; current status is {current_status}."
            )

    deliverables: dict[str, str] = state["deliverables"]
    checked_files: dict[str, str] = {}
    placeholder_files: list[str] = []
    for key in requirement["deliverables"]:
        relative_path = deliverables.get(key)
        if not relative_path:
            errors.append(f"Missing deliverable entry in research-state.yaml: {key}")
            continue
        checked_files[key] = relative_path
        errors.extend(validate_deliverable_location(project_root, relative_path, key))
        candidate_path = (project_root / relative_path).resolve()
        if not candidate_path.exists():
            missing_files.append(relative_path)
            continue
        content_errors = validate_deliverable_content(project_root, state, key)
        if content_errors:
            placeholder_files.append(relative_path)
            errors.extend(content_errors)

    if missing_files:
        errors.append("Required deliverable files are missing.")

    phase_name = requirement["next_phase"]
    # Map next_phase to source phase for signal validation
    source_phase_map = {
        "pilot": "survey",
        "experiments": "pilot",
        "paper": "experiments",
        "reflection": "paper",
        "handoff-user": "reflection",
    }
    source_phase = source_phase_map.get(phase_name, phase_name)
    signal_errors = validate_structured_signals(project_root, state, source_phase)
    errors.extend(signal_errors)

    return {
        "ok": not errors,
        "status": "pass" if not errors else "fail",
        "target": target,
        "project_root": str(project_root),
        "status_checks": status_checks,
        "next_phase": requirement["next_phase"],
        "checked_files": checked_files,
        "missing_files": missing_files,
        "placeholder_files": placeholder_files,
        "signal_errors": signal_errors,
        "errors": errors,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate whether a research project can advance to the next gate or phase.")
    parser.add_argument("--project-root", required=True)
    parser.add_argument(
        "--target",
        required=True,
        choices=sorted(tuple(HANDOFF_REQUIREMENTS) + tuple(LOOP_REQUIREMENTS)),
        help="Gate or loop validation target.",
    )
    parser.add_argument("--json", action="store_true", help="Print a JSON summary.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    ensure_project_structure(Path(args.project_root))
    result = validate_handoff(Path(args.project_root), args.target)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Target: {result['target']}")
        print(f"Project root: {result['project_root']}")
        print(f"Status: {result['status']}")
        if "loop_key" in result:
            print(f"Loop: {result['loop_key']} ({result['current_count']}/{result['limit']})")
            print(f"Gate status: {result['gate_status']}")
        else:
            print(f"Next phase: {result['next_phase']}")
            print("Status checks:")
            for item in result["status_checks"]:
                print(f"- {item['group']}.{item['key']}: {item['status']}")
            if result["checked_files"]:
                print("Checked files:")
                for key, path in result["checked_files"].items():
                    print(f"- {key}: {path}")
            if result["missing_files"]:
                print("Missing files:")
                for path in result["missing_files"]:
                    print(f"- {path}")
            if result.get("placeholder_files"):
                print("Placeholder files:")
                for path in result["placeholder_files"]:
                    print(f"- {path}")
            if result.get("signal_errors"):
                print("Signal errors:")
                for error in result["signal_errors"]:
                    print(f"- {error}")
        if result["errors"]:
            print("Errors:")
            for error in result["errors"]:
                print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
