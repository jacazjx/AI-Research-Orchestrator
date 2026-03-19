#!/usr/bin/env python3
"""Validate agent communication message formats for the AI Research Orchestrator.

This script validates YAML/JSON messages exchanged between agents and the orchestrator,
catching malformed communications before they cause runtime failures.

Usage:
    python3 scripts/validate_agent_comm.py --type <TYPE> --file <path> [--json]

Supported types:
    dispatch    Orchestrator → Agent Task Dispatch
    completion  Agent → Orchestrator Completion Report
    challenge   Primary → Orchestrator Battle Challenge
    response    Reviewer → Orchestrator Battle Response
    debate      debate.json structure validation
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

# Valid enum values per field
VALID_PHASES = {"survey", "pilot", "experiments", "paper", "reflection"}
VALID_COMPLETION_STATUSES = {"completed", "failed", "in_progress"}
VALID_DELIVERABLE_STATUSES = {"created", "updated", "failed"}
VALID_CHALLENGE_TYPES = {"derivation_audit", "survey_audit"}
VALID_RESPONSE_TYPES = {"accept", "reject", "partial"}
VALID_POINT_ACTIONS = {"accept", "reject", "modify"}
VALID_DEBATE_STATUSES = {"debating", "completed"}
VALID_VERDICT_DECISIONS = {"approve", "revise", "reject"}


def _require_string(data: dict[str, Any], field: str, errors: list[str]) -> str | None:
    """Check that a field exists and is a non-empty string."""
    value = data.get(field)
    if value is None:
        errors.append(f"Missing required field: '{field}'")
        return None
    if not isinstance(value, str):
        errors.append(f"Field '{field}' must be a string, got {type(value).__name__}")
        return None
    if not value.strip():
        errors.append(f"Field '{field}' must not be empty")
        return None
    return value


def _require_enum(
    data: dict[str, Any], field: str, valid_values: set[str], errors: list[str]
) -> str | None:
    """Check that a field is a string and one of the allowed enum values."""
    value = _require_string(data, field, errors)
    if value is None:
        return None
    if value not in valid_values:
        errors.append(
            f"Field '{field}' has invalid value '{value}'; "
            f"must be one of: {', '.join(sorted(valid_values))}"
        )
        return None
    return value


def _require_list(
    data: dict[str, Any], field: str, errors: list[str], non_empty: bool = False
) -> list | None:
    """Check that a field exists and is a list (optionally non-empty)."""
    value = data.get(field)
    if value is None:
        errors.append(f"Missing required field: '{field}'")
        return None
    if not isinstance(value, list):
        errors.append(f"Field '{field}' must be a list, got {type(value).__name__}")
        return None
    if non_empty and len(value) == 0:
        errors.append(f"Field '{field}' must not be empty")
        return None
    return value


def _require_dict(data: dict[str, Any], field: str, errors: list[str]) -> dict | None:
    """Check that a field exists and is a dict."""
    value = data.get(field)
    if value is None:
        errors.append(f"Missing required field: '{field}'")
        return None
    if not isinstance(value, dict):
        errors.append(f"Field '{field}' must be an object/mapping, got {type(value).__name__}")
        return None
    return value


def validate_dispatch(data: dict[str, Any]) -> list[str]:
    """Validate an Orchestrator → Agent Task Dispatch message.

    Required fields:
        task_id: string
        skill: string
        context.research_topic: string
        context.current_phase: one of VALID_PHASES
        deliverables: non-empty list of strings
    """
    errors: list[str] = []

    _require_string(data, "task_id", errors)
    _require_string(data, "skill", errors)

    context = _require_dict(data, "context", errors)
    if context is not None:
        _require_string(context, "research_topic", errors)
        _require_enum(context, "current_phase", VALID_PHASES, errors)

    deliverables = _require_list(data, "deliverables", errors, non_empty=True)
    if deliverables is not None:
        for i, item in enumerate(deliverables):
            if not isinstance(item, str):
                errors.append(
                    f"Field 'deliverables[{i}]' must be a string, got {type(item).__name__}"
                )

    return errors


def validate_completion(data: dict[str, Any]) -> list[str]:
    """Validate an Agent → Orchestrator Completion Report message.

    Required fields:
        task_id: string
        status: one of VALID_COMPLETION_STATUSES
        deliverables: list (can be empty) each with path/status/summary strings
        errors: list (can be empty)
    """
    errors: list[str] = []

    _require_string(data, "task_id", errors)
    _require_enum(data, "status", VALID_COMPLETION_STATUSES, errors)

    deliverables = _require_list(data, "deliverables", errors, non_empty=False)
    if deliverables is not None:
        for i, item in enumerate(deliverables):
            if not isinstance(item, dict):
                errors.append(
                    f"Field 'deliverables[{i}]' must be an object, got {type(item).__name__}"
                )
                continue
            prefix = f"deliverables[{i}]"
            # Validate nested fields manually to include index in error messages
            for sub_field in ("path", "summary"):
                sub_val = item.get(sub_field)
                if sub_val is None:
                    errors.append(f"Missing required field: '{prefix}.{sub_field}'")
                elif not isinstance(sub_val, str):
                    errors.append(
                        f"Field '{prefix}.{sub_field}' must be a string, "
                        f"got {type(sub_val).__name__}"
                    )
            # Validate status enum
            sub_status = item.get("status")
            if sub_status is None:
                errors.append(f"Missing required field: '{prefix}.status'")
            elif sub_status not in VALID_DELIVERABLE_STATUSES:
                errors.append(
                    f"Field '{prefix}.status' has invalid value '{sub_status}'; "
                    f"must be one of: {', '.join(sorted(VALID_DELIVERABLE_STATUSES))}"
                )

    _require_list(data, "errors", errors, non_empty=False)

    return errors


def validate_challenge(data: dict[str, Any]) -> list[str]:
    """Validate a Primary → Orchestrator Battle Challenge message.

    Required fields:
        challenge_type: one of VALID_CHALLENGE_TYPES
        disputed_points: non-empty list, each with point_id/original_claim/
                         challenge_reason/proposed_alternative strings
    """
    errors: list[str] = []

    _require_enum(data, "challenge_type", VALID_CHALLENGE_TYPES, errors)

    points = _require_list(data, "disputed_points", errors, non_empty=True)
    if points is not None:
        for i, item in enumerate(points):
            if not isinstance(item, dict):
                errors.append(
                    f"Field 'disputed_points[{i}]' must be an object, got {type(item).__name__}"
                )
                continue
            prefix = f"disputed_points[{i}]"
            for sub_field in ("point_id", "original_claim", "challenge_reason", "proposed_alternative"):
                sub_val = item.get(sub_field)
                if sub_val is None:
                    errors.append(f"Missing required field: '{prefix}.{sub_field}'")
                elif not isinstance(sub_val, str):
                    errors.append(
                        f"Field '{prefix}.{sub_field}' must be a string, "
                        f"got {type(sub_val).__name__}"
                    )
                elif not sub_val.strip():
                    errors.append(f"Field '{prefix}.{sub_field}' must not be empty")

    return errors


def validate_response(data: dict[str, Any]) -> list[str]:
    """Validate a Reviewer → Orchestrator Battle Response message.

    Required fields:
        response_type: one of VALID_RESPONSE_TYPES
        point_responses: non-empty list, each with point_id/action/reason strings,
                         and modified_position required when action=modify
    """
    errors: list[str] = []

    _require_enum(data, "response_type", VALID_RESPONSE_TYPES, errors)

    points = _require_list(data, "point_responses", errors, non_empty=True)
    if points is not None:
        for i, item in enumerate(points):
            if not isinstance(item, dict):
                errors.append(
                    f"Field 'point_responses[{i}]' must be an object, got {type(item).__name__}"
                )
                continue
            prefix = f"point_responses[{i}]"
            for sub_field in ("point_id", "reason"):
                sub_val = item.get(sub_field)
                if sub_val is None:
                    errors.append(f"Missing required field: '{prefix}.{sub_field}'")
                elif not isinstance(sub_val, str):
                    errors.append(
                        f"Field '{prefix}.{sub_field}' must be a string, "
                        f"got {type(sub_val).__name__}"
                    )
                elif not sub_val.strip():
                    errors.append(f"Field '{prefix}.{sub_field}' must not be empty")
            # Validate action enum
            action = item.get("action")
            if action is None:
                errors.append(f"Missing required field: '{prefix}.action'")
            elif action not in VALID_POINT_ACTIONS:
                errors.append(
                    f"Field '{prefix}.action' has invalid value '{action}'; "
                    f"must be one of: {', '.join(sorted(VALID_POINT_ACTIONS))}"
                )
            elif action == "modify":
                # modified_position is required when action=modify
                mod_pos = item.get("modified_position")
                if mod_pos is None:
                    errors.append(
                        f"Field '{prefix}.modified_position' is required when "
                        f"'{prefix}.action' is 'modify'"
                    )
                elif not isinstance(mod_pos, str):
                    errors.append(
                        f"Field '{prefix}.modified_position' must be a string, "
                        f"got {type(mod_pos).__name__}"
                    )

    return errors


def validate_debate(data: dict[str, Any]) -> list[str]:
    """Validate a debate.json structure.

    Required fields:
        round: integer >= 1
        phase: string
        primary_agent: string
        reviewer_agent: string
        status: one of VALID_DEBATE_STATUSES
        turns: list (can be empty)
        resolved_issues: list
        unresolved_issues: list
        verdict: required when status=completed, with decision/verdict_by/scores/required_actions
    """
    errors: list[str] = []

    # round: integer >= 1
    round_val = data.get("round")
    if round_val is None:
        errors.append("Missing required field: 'round'")
    elif not isinstance(round_val, int):
        errors.append(f"Field 'round' must be an integer, got {type(round_val).__name__}")
    elif round_val < 1:
        errors.append(f"Field 'round' must be >= 1, got {round_val}")

    _require_string(data, "phase", errors)
    _require_string(data, "primary_agent", errors)
    _require_string(data, "reviewer_agent", errors)

    status = _require_enum(data, "status", VALID_DEBATE_STATUSES, errors)

    _require_list(data, "turns", errors, non_empty=False)
    _require_list(data, "resolved_issues", errors, non_empty=False)
    _require_list(data, "unresolved_issues", errors, non_empty=False)

    # verdict is required when status=completed
    if status == "completed":
        verdict = _require_dict(data, "verdict", errors)
        if verdict is not None:
            decision = verdict.get("decision")
            if decision is None:
                errors.append("Missing required field: 'verdict.decision'")
            elif decision not in VALID_VERDICT_DECISIONS:
                errors.append(
                    f"Field 'verdict.decision' has invalid value '{decision}'; "
                    f"must be one of: {', '.join(sorted(VALID_VERDICT_DECISIONS))}"
                )
            _require_string(verdict, "verdict_by", errors)
            scores = verdict.get("scores")
            if scores is None:
                errors.append("Missing required field: 'verdict.scores'")
            elif not isinstance(scores, dict):
                errors.append(
                    f"Field 'verdict.scores' must be an object, got {type(scores).__name__}"
                )
            required_actions = verdict.get("required_actions")
            if required_actions is None:
                errors.append("Missing required field: 'verdict.required_actions'")
            elif not isinstance(required_actions, list):
                errors.append(
                    f"Field 'verdict.required_actions' must be a list, "
                    f"got {type(required_actions).__name__}"
                )
    elif "verdict" in data and data["verdict"] is not None:
        # verdict present when not completed — not an error, just ignore
        pass

    return errors


VALIDATORS: dict[str, Any] = {
    "dispatch": validate_dispatch,
    "completion": validate_completion,
    "challenge": validate_challenge,
    "response": validate_response,
    "debate": validate_debate,
}


def load_file(path: Path) -> Any:
    """Load a YAML or JSON file.

    JSON files are loaded with json.loads; everything else is loaded with yaml.safe_load
    (YAML is a superset of JSON, so this handles .yaml files).
    """
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def validate_message(msg_type: str, file_path: Path) -> dict[str, Any]:
    """Validate a message file of the given type.

    Returns a dict with keys:
        valid: bool
        errors: list[str]
    """
    errors: list[str] = []

    if not file_path.exists():
        errors.append(f"File not found: {file_path}")
        return {"valid": False, "errors": errors}

    try:
        data = load_file(file_path)
    except (yaml.YAMLError, json.JSONDecodeError) as exc:
        errors.append(f"Failed to parse file: {exc}")
        return {"valid": False, "errors": errors}

    if not isinstance(data, dict):
        errors.append(
            f"Message must be a YAML/JSON object (mapping), got {type(data).__name__}"
        )
        return {"valid": False, "errors": errors}

    validator = VALIDATORS[msg_type]
    errors.extend(validator(data))

    return {"valid": len(errors) == 0, "errors": errors}


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Validate agent communication message formats."
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=sorted(VALIDATORS),
        dest="msg_type",
        help="Message type to validate.",
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to the YAML or JSON message file.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output validation result as JSON.",
    )
    return parser


def main() -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args()

    file_path = Path(args.file)
    result = validate_message(args.msg_type, file_path)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result["valid"]:
            print(f"OK: {args.file} is a valid '{args.msg_type}' message.")
        else:
            print(
                f"INVALID: {args.file} failed validation as '{args.msg_type}' message.",
                file=sys.stderr,
            )
            for error in result["errors"]:
                print(f"  - {error}", file=sys.stderr)

    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
