#!/usr/bin/env python3
"""Substep validation utilities for Agent-Skill Coupling workflow.

This module provides functions to validate substep transitions and check
required artifacts and review approvals according to the Agent-Skill Coupling Design.

Usage:
    python validate_substep.py --project-root /path/to/project \
        --phase survey --substep literature_survey
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

import yaml

# Configure module logger
logger = logging.getLogger(__name__)

# Default substep configuration per phase
DEFAULT_SUBSTEPS = {
    "survey": [
        {
            "name": "literature_survey",
            "primary_skill": "research-lit",
            "reviewer_skill": "audit-survey",
            "required_artifacts": ["docs/reports/survey/literature-review.md"],
        },
        {
            "name": "idea_definition",
            "primary_skill": "define-idea",
            "reviewer_skill": "novelty-check",
            "required_artifacts": ["docs/reports/survey/idea-definition.md"],
        },
        {
            "name": "research_plan",
            "primary_skill": "research-plan",
            "reviewer_skill": "audit-plan",
            "required_artifacts": ["docs/reports/survey/research-readiness-report.md"],
        },
    ],
    "pilot": [
        {
            "name": "problem_analysis",
            "primary_skill": "analyze-problem",
            "reviewer_skill": "audit-analysis",
            "required_artifacts": ["docs/reports/pilot/problem-analysis.md"],
        },
        {
            "name": "pilot_design",
            "primary_skill": "design-pilot",
            "reviewer_skill": "audit-design",
            "required_artifacts": ["docs/reports/pilot/pilot-design.md"],
        },
        {
            "name": "pilot_execution",
            "primary_skill": "run-pilot",
            "reviewer_skill": "audit-pilot",
            "required_artifacts": ["docs/reports/pilot/pilot-validation-report.md"],
        },
    ],
    "experiments": [
        {
            "name": "experiment_design",
            "primary_skill": "design-exp",
            "reviewer_skill": "audit-exp-design",
            "required_artifacts": ["docs/reports/experiments/experiment-spec.md"],
        },
        {
            "name": "experiment_execution",
            "primary_skill": "run-experiment",
            "reviewer_skill": "monitor-experiment",
            "required_artifacts": ["docs/reports/experiments/run-registry.md"],
        },
        {
            "name": "results_analysis",
            "primary_skill": "analyze-results",
            "reviewer_skill": "audit-results",
            "required_artifacts": ["docs/reports/experiments/evidence-package-index.md"],
        },
    ],
    "paper": [
        {
            "name": "paper_planning",
            "primary_skill": "paper-plan",
            "reviewer_skill": "audit-paper-plan",
            "required_artifacts": ["paper/paper-outline.md"],
        },
        {
            "name": "paper_writing",
            "primary_skill": "paper-write",
            "reviewer_skill": "audit-paper",
            "required_artifacts": ["paper/paper-draft.md"],
        },
        {
            "name": "citation_curation",
            "primary_skill": "curate-citation",
            "reviewer_skill": "audit-citation",
            "required_artifacts": ["paper/citation-audit-report.md"],
        },
    ],
    "reflection": [
        {
            "name": "lessons_extraction",
            "primary_skill": "extract-lessons",
            "reviewer_skill": "audit-lessons",
            "required_artifacts": ["docs/reports/reflection/lessons-learned.md"],
        },
        {
            "name": "overlay_proposal",
            "primary_skill": "propose-overlay",
            "reviewer_skill": "audit-overlay",
            "required_artifacts": ["docs/reports/reflection/runtime-improvement-report.md"],
        },
    ],
}

# Substep status values
STATUS_PENDING = "pending"
STATUS_IN_PROGRESS = "in_progress"
STATUS_APPROVED = "approved"
STATUS_BLOCKED = "blocked"

# Review result values
REVIEW_PENDING = "pending"
REVIEW_APPROVED = "approved"
REVIEW_REVISION = "needs_revision"


def load_research_state(project_root: Path) -> dict[str, Any]:
    """Load research-state.yaml from project.

    Args:
        project_root: Path to the project root directory.

    Returns:
        Parsed state dictionary.

    Raises:
        FileNotFoundError: If state file doesn't exist.
        yaml.YAMLError: If state file is invalid YAML.
    """
    state_path = project_root / ".autoresearch" / "state" / "research-state.yaml"
    if not state_path.exists():
        raise FileNotFoundError(f"Research state not found: {state_path}")
    return yaml.safe_load(state_path.read_text(encoding="utf-8"))


def load_orchestrator_config(project_root: Path) -> dict[str, Any]:
    """Load orchestrator-config.yaml from project.

    Args:
        project_root: Path to the project root directory.

    Returns:
        Parsed config dictionary, or default config if not found.
    """
    config_path = project_root / ".autoresearch" / "config" / "orchestrator-config.yaml"
    if config_path.exists():
        return yaml.safe_load(config_path.read_text(encoding="utf-8"))
    return {"phases": DEFAULT_SUBSTEPS}


def get_phase_substeps(config: dict[str, Any], phase: str) -> list[dict[str, Any]]:
    """Get substeps for a phase from config.

    Args:
        config: Orchestrator config dictionary.
        phase: Phase name (e.g., 'survey', 'pilot').

    Returns:
        List of substep configurations.
    """
    phases = config.get("phases", {})
    phase_config = phases.get(phase, {})
    return phase_config.get("substeps", DEFAULT_SUBSTEPS.get(phase, []))


def check_required_artifacts(project_root: Path, artifacts: list[str]) -> dict[str, Any]:
    """Check if required artifacts exist.

    Args:
        project_root: Path to the project root directory.
        artifacts: List of artifact paths relative to project root.

    Returns:
        Dictionary with 'all_exist', 'missing', and 'existing' keys.
    """
    missing = []
    existing = []

    for artifact in artifacts:
        artifact_path = project_root / artifact
        if artifact_path.exists():
            existing.append(artifact)
        else:
            missing.append(artifact)

    return {
        "all_exist": len(missing) == 0,
        "missing": missing,
        "existing": existing,
    }


def check_review_approval(state: dict[str, Any], phase: str, substep: str) -> dict[str, Any]:
    """Check if substep has reviewer approval.

    Args:
        state: Research state dictionary.
        phase: Phase name.
        substep: Substep name.

    Returns:
        Dictionary with 'approved', 'status', and 'review_result' keys.
    """
    substep_status = state.get("substep_status", {}).get(phase, {}).get(substep, {})

    status = substep_status.get("status", STATUS_PENDING)
    review_result = substep_status.get("review_result", REVIEW_PENDING)

    return {
        "approved": review_result == REVIEW_APPROVED,
        "status": status,
        "review_result": review_result,
    }


def get_substep_config(config: dict[str, Any], phase: str, substep: str) -> dict[str, Any] | None:
    """Get configuration for a specific substep.

    Args:
        config: Orchestrator config dictionary.
        phase: Phase name.
        substep: Substep name.

    Returns:
        Substep configuration or None if not found.
    """
    substeps = get_phase_substeps(config, phase)
    for s in substeps:
        if s.get("name") == substep:
            return s
    return None


def get_next_substep(config: dict[str, Any], phase: str, current_substep: str) -> str | None:
    """Get the next substep name after the current one.

    Args:
        config: Orchestrator config dictionary.
        phase: Phase name.
        current_substep: Current substep name.

    Returns:
        Next substep name or None if current is the last substep.
    """
    substeps = get_phase_substeps(config, phase)

    for i, substep in enumerate(substeps):
        if substep.get("name") == current_substep:
            if i + 1 < len(substeps):
                return substeps[i + 1].get("name")
            return None

    return None


def get_first_substep(config: dict[str, Any], phase: str) -> str | None:
    """Get the first substep name for a phase.

    Args:
        config: Orchestrator config dictionary.
        phase: Phase name.

    Returns:
        First substep name or None if phase has no substeps.
    """
    substeps = get_phase_substeps(config, phase)
    if substeps:
        return substeps[0].get("name")
    return None


def validate_substep(project_root: Path, phase: str, substep: str) -> dict[str, Any]:
    """Validate if a substep can proceed.

    This checks:
    1. Previous substeps in the same phase are approved
    2. Required artifacts exist (if substep is being completed)
    3. Review has been approved (for transition validation)

    Args:
        project_root: Path to the project root directory.
        phase: Phase name.
        substep: Substep name.

    Returns:
        Dictionary with validation results:
        - can_proceed: bool
        - previous_substeps_complete: bool
        - artifacts_check: dict
        - review_check: dict
        - errors: list of error messages
        - warnings: list of warning messages
    """
    errors = []
    warnings = []

    # Load state and config
    try:
        state = load_research_state(project_root)
    except FileNotFoundError:
        return {
            "can_proceed": False,
            "previous_substeps_complete": False,
            "artifacts_check": {"all_exist": False, "missing": [], "existing": []},
            "review_check": {"approved": False, "status": "pending", "review_result": "pending"},
            "errors": ["Research state file not found"],
            "warnings": [],
        }

    config = load_orchestrator_config(project_root)

    # Check if substep exists in config
    substep_config = get_substep_config(config, phase, substep)
    if not substep_config:
        errors.append(f"Substep '{substep}' not found in phase '{phase}'")
        return {
            "can_proceed": False,
            "previous_substeps_complete": False,
            "artifacts_check": {"all_exist": False, "missing": [], "existing": []},
            "review_check": {"approved": False, "status": "pending", "review_result": "pending"},
            "errors": errors,
            "warnings": warnings,
        }

    # Check if previous substeps are complete
    substeps = get_phase_substeps(config, phase)
    current_index = next((i for i, s in enumerate(substeps) if s.get("name") == substep), -1)

    previous_complete = True
    for i in range(current_index):
        prev_substep_name = substeps[i].get("name")
        prev_review = check_review_approval(state, phase, prev_substep_name)
        if not prev_review["approved"]:
            previous_complete = False
            errors.append(
                f"Previous substep '{prev_substep_name}' not approved "
                f"(status: {prev_review['status']}, review: {prev_review['review_result']})"
            )

    # Check required artifacts
    required_artifacts = substep_config.get("required_artifacts", [])
    artifacts_check = check_required_artifacts(project_root, required_artifacts)

    if not artifacts_check["all_exist"]:
        warnings.append(f"Missing artifacts: {', '.join(artifacts_check['missing'])}")

    # Check review approval
    review_check = check_review_approval(state, phase, substep)

    # Determine if can proceed
    can_proceed = previous_complete

    return {
        "can_proceed": can_proceed,
        "previous_substeps_complete": previous_complete,
        "artifacts_check": artifacts_check,
        "review_check": review_check,
        "errors": errors,
        "warnings": warnings,
    }


def can_advance_substep(project_root: Path, phase: str, substep: str) -> dict[str, Any]:
    """Check if a substep can advance to the next one.

    This requires:
    1. Review approval
    2. All required artifacts exist

    Args:
        project_root: Path to the project root directory.
        phase: Phase name.
        substep: Substep name.

    Returns:
        Dictionary with 'can_advance', 'reason', and 'details' keys.
    """
    try:
        state = load_research_state(project_root)
    except FileNotFoundError:
        return {
            "can_advance": False,
            "reason": "Research state file not found",
            "details": {},
        }

    config = load_orchestrator_config(project_root)
    substep_config = get_substep_config(config, phase, substep)

    if not substep_config:
        return {
            "can_advance": False,
            "reason": f"Substep '{substep}' not found in phase '{phase}'",
            "details": {},
        }

    # Check review approval
    review_check = check_review_approval(state, phase, substep)
    if not review_check["approved"]:
        return {
            "can_advance": False,
            "reason": "Review not approved",
            "details": {"review_check": review_check},
        }

    # Check artifacts
    required_artifacts = substep_config.get("required_artifacts", [])
    artifacts_check = check_required_artifacts(project_root, required_artifacts)
    if not artifacts_check["all_exist"]:
        return {
            "can_advance": False,
            "reason": "Required artifacts missing",
            "details": {"artifacts_check": artifacts_check},
        }

    # Get next substep
    next_substep = get_next_substep(config, phase, substep)

    return {
        "can_advance": True,
        "reason": "All checks passed",
        "details": {
            "review_check": review_check,
            "artifacts_check": artifacts_check,
            "next_substep": next_substep,
        },
    }


def update_substep_status(
    project_root: Path,
    phase: str,
    substep: str,
    status: str,
    review_result: str | None = None,
    last_agent: str | None = None,
    attempts: int | None = None,
) -> None:
    """Update substep status in research state.

    Args:
        project_root: Path to the project root directory.
        phase: Phase name.
        substep: Substep name.
        status: New status value.
        review_result: Optional review result value.
        last_agent: Optional last agent name.
        attempts: Optional attempt count.
    """
    state = load_research_state(project_root)

    # Ensure substep_status structure exists
    if "substep_status" not in state:
        state["substep_status"] = {}
    if phase not in state["substep_status"]:
        state["substep_status"][phase] = {}
    if substep not in state["substep_status"][phase]:
        state["substep_status"][phase][substep] = {"status": STATUS_PENDING}

    # Update fields
    state["substep_status"][phase][substep]["status"] = status

    if review_result is not None:
        state["substep_status"][phase][substep]["review_result"] = review_result

    if last_agent is not None:
        state["substep_status"][phase][substep]["last_agent"] = last_agent

    if attempts is not None:
        state["substep_status"][phase][substep]["attempts"] = attempts
    elif "attempts" not in state["substep_status"][phase][substep]:
        state["substep_status"][phase][substep]["attempts"] = 1

    # Write updated state
    state_path = project_root / ".autoresearch" / "state" / "research-state.yaml"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        yaml.dump(state, allow_unicode=True, default_flow_style=False), encoding="utf-8"
    )


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser for CLI."""
    parser = argparse.ArgumentParser(
        description="Validate substep transitions in Agent-Skill Coupling workflow."
    )
    parser.add_argument(
        "--project-root",
        required=True,
        help="Path to the project root directory.",
    )
    parser.add_argument(
        "--phase",
        required=True,
        choices=["survey", "pilot", "experiments", "paper", "reflection"],
        help="Phase name.",
    )
    parser.add_argument(
        "--substep",
        required=True,
        help="Substep name to validate.",
    )
    parser.add_argument(
        "--check-artifacts",
        action="store_true",
        help="Check if required artifacts exist.",
    )
    parser.add_argument(
        "--check-review",
        action="store_true",
        help="Check if review is approved.",
    )
    parser.add_argument(
        "--get-next",
        action="store_true",
        help="Get the next substep name after the current one.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON.",
    )
    return parser


def main() -> int:
    """Main entry point for CLI."""
    parser = build_parser()
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()

    if args.get_next:
        config = load_orchestrator_config(project_root)
        next_substep = get_next_substep(config, args.phase, args.substep)
        if args.json:
            print(json.dumps({"next_substep": next_substep}))
        else:
            print(f"Next substep: {next_substep or 'None (last substep)'}")
        return 0

    if args.check_artifacts:
        config = load_orchestrator_config(project_root)
        substep_config = get_substep_config(config, args.phase, args.substep)
        if not substep_config:
            print(f"Error: Substep '{args.substep}' not found", file=sys.stderr)
            return 1
        artifacts = substep_config.get("required_artifacts", [])
        result = check_required_artifacts(project_root, artifacts)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result["all_exist"]:
                print("All required artifacts exist.")
            else:
                print(f"Missing artifacts: {', '.join(result['missing'])}")
        return 0 if result["all_exist"] else 1

    if args.check_review:
        try:
            state = load_research_state(project_root)
            result = check_review_approval(state, args.phase, args.substep)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                if result["approved"]:
                    print(f"Review approved (status: {result['status']})")
                else:
                    print(f"Review not approved (result: {result['review_result']})")
            return 0 if result["approved"] else 1
        except FileNotFoundError:
            print("Error: Research state file not found", file=sys.stderr)
            return 1

    # Default: full validation
    result = validate_substep(project_root, args.phase, args.substep)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Substep: {args.substep}")
        print(f"Phase: {args.phase}")
        print(f"Can proceed: {result['can_proceed']}")

        if result["errors"]:
            print("\nErrors:")
            for error in result["errors"]:
                print(f"  - {error}")

        if result["warnings"]:
            print("\nWarnings:")
            for warning in result["warnings"]:
                print(f"  - {warning}")

        if result["artifacts_check"]["missing"]:
            print(f"\nMissing artifacts: {', '.join(result['artifacts_check']['missing'])}")

        print(f"\nReview status: {result['review_check']['status']}")
        print(f"Review result: {result['review_check']['review_result']}")

    return 0 if result["can_proceed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
