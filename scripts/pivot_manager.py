from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from exceptions import StateError
from generate_dashboard import generate_dashboard

from orchestrator_common import (
    PHASE_TO_GATE,
    append_state_log,
    ensure_project_structure,
    load_state,
    normalize_phase_name,
    save_state,
)


def propose_pivot(
    project_root: Path,
    pivot_type: str,
    rationale: str,
    alternative: str = "",
    affected_phase: str | None = None,
    proposed_by: str = "orchestrator",
) -> dict[str, object]:
    project_root = project_root.resolve()
    state = load_state(project_root)
    phase = affected_phase or state["current_phase"]
    pivot_id = f"pivot-{len(state.get('pivot_candidates', [])) + 1}"
    entry = {
        "id": pivot_id,
        "type": pivot_type,
        "phase": phase,
        "rationale": rationale,
        "alternative": alternative,
        "proposed_by": proposed_by,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    append_state_log(state, "pivot_candidates", entry)
    state["phase_reviews"][_phase_review_key(phase)] = "pivot"
    state["progress"]["last_gate_result"] = "pivot"
    state["progress"]["active_blocker"] = f"pivot:{pivot_type}"
    state["progress"]["next_action"] = "await-human-pivot-decision"
    save_state(project_root, state)
    generate_dashboard(project_root)
    return {
        "project_root": str(project_root),
        "pivot_id": pivot_id,
        "phase": phase,
        "status": "proposed",
    }


def review_pivot(
    project_root: Path, pivot_id: str, decision: str, note: str = ""
) -> dict[str, object]:
    project_root = project_root.resolve()
    state = load_state(project_root)
    serialized = list(state.get("pivot_candidates", []))
    matching = [item for item in serialized if f'"id": "{pivot_id}"' in item]
    if not matching:
        raise StateError(
            f"Unknown pivot id: {pivot_id}",
            state_file="research-state.yaml",
            field="pivot_candidates",
        )
    pivot_entry = json.loads(matching[0])
    phase = pivot_entry["phase"]

    state["pivot_candidates"] = [item for item in serialized if item != matching[0]]
    append_state_log(
        state,
        "human_decisions",
        {
            "type": "pivot_review",
            "pivot_id": pivot_id,
            "decision": decision,
            "note": note,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )

    if decision == "approve":
        _execute_pivot(state, pivot_entry)
        state["progress"]["last_gate_result"] = "pivot_approved"
        state["progress"]["next_action"] = "execute-approved-pivot"
    else:
        state["phase_reviews"][_phase_review_key(phase)] = "pending"
        state["progress"]["last_gate_result"] = "pivot_rejected"
        state["progress"]["next_action"] = f"resume-{phase}"
    state["progress"]["active_blocker"] = "none"

    save_state(project_root, state)
    generate_dashboard(project_root)
    return {
        "project_root": str(project_root),
        "pivot_id": pivot_id,
        "decision": decision,
        "current_phase": state["current_phase"],
    }


def _execute_pivot(state: dict[str, object], pivot_entry: dict[str, str]) -> None:
    pivot_type = pivot_entry["type"]
    phase = pivot_entry["phase"]
    if pivot_type == "downgrade_to_pilot":
        state["current_phase"] = "pilot"  # Semantic name
        state["phase"] = "pilot"
        state["current_gate"] = PHASE_TO_GATE["pilot"]
    elif pivot_type == "archive_branch":
        state["current_phase"] = "06-archive"
        state["phase"] = "06-archive"
        state["current_gate"] = "complete"
    else:
        state["current_phase"] = phase
        state["phase"] = phase
        state["current_gate"] = PHASE_TO_GATE.get(phase, state["current_gate"])
    state["phase_reviews"][_phase_review_key(state["current_phase"])] = "pending"


def _phase_review_key(phase: str) -> str:
    # Normalize to semantic name, then map to review key
    normalized = normalize_phase_name(phase)
    review_keys = {
        "survey": "survey_critic",
        "pilot": "pilot_adviser",
        "experiments": "experiment_adviser",
        "paper": "paper_reviewer",
        "reflection": "reflection_curator",
        "06-archive": "reflection_curator",
    }
    return review_keys.get(normalized, f"{normalized}_review")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage pivot proposals and approvals.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    propose = subparsers.add_parser("propose")
    propose.add_argument("--project-root", required=True)
    propose.add_argument("--pivot-type", required=True)
    propose.add_argument("--rationale", required=True)
    propose.add_argument("--alternative", default="")
    propose.add_argument("--affected-phase")
    propose.add_argument("--proposed-by", default="orchestrator")

    review = subparsers.add_parser("review")
    review.add_argument("--project-root", required=True)
    review.add_argument("--pivot-id", required=True)
    review.add_argument("--decision", required=True, choices=("approve", "reject"))
    review.add_argument("--note", default="")

    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()

    # Ensure project structure
    ensure_project_structure(project_root, create_if_missing=False)

    if args.command == "propose":
        result = propose_pivot(
            project_root,
            pivot_type=args.pivot_type,
            rationale=args.rationale,
            alternative=args.alternative,
            affected_phase=args.affected_phase,
            proposed_by=args.proposed_by,
        )
    else:
        result = review_pivot(project_root, args.pivot_id, args.decision, note=args.note)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
