from __future__ import annotations

import argparse
import json
from pathlib import Path

from orchestrator_common import (
    PHASE_REQUIRED_DELIVERABLES,
    PHASE_TO_GATE,
    PHASE_TO_REVIEW,
    ensure_project_structure,
    load_state,
    validate_deliverable_content,
    validate_structured_signals,
)


def evaluate_quality_gate(project_root: Path, phase: str | None = None) -> dict[str, object]:
    project_root = project_root.resolve()
    state = load_state(project_root)
    phase_name = phase or state["current_phase"]

    required_deliverables = PHASE_REQUIRED_DELIVERABLES[phase_name]
    review_key = PHASE_TO_REVIEW[phase_name]
    gate_key = PHASE_TO_GATE[phase_name]

    existing: list[str] = []
    missing: list[str] = []
    placeholder: list[str] = []
    for key in required_deliverables:
        relative_path = state["deliverables"][key]
        if (project_root / relative_path).exists():
            content_errors = validate_deliverable_content(project_root, state, key)
            if content_errors:
                placeholder.append(relative_path)
            else:
                existing.append(relative_path)
        else:
            missing.append(relative_path)

    completeness = (
        int(round((len(existing) / len(required_deliverables)) * 100))
        if required_deliverables
        else 100
    )
    review_status = state["phase_reviews"][review_key]
    gate_status = state["approval_status"][gate_key]
    loop_count = int(state["loop_counts"].get(_phase_loop_key(phase_name), 0))
    loop_limit = int(state["loop_limits"].get(_phase_loop_key(phase_name), 0))
    pivot_candidates = list(state.get("pivot_candidates", []))
    signal_errors = validate_structured_signals(project_root, state, phase_name)

    if review_status == "pivot" or pivot_candidates:
        decision = "pivot"
    elif (
        review_status == "approved"
        and not missing
        and not placeholder
        and not signal_errors
        and gate_status == "approved"
    ):
        decision = "advance"
    elif loop_count >= loop_limit and review_status != "approved":
        decision = "escalate_to_user"
    else:
        decision = "revise"

    blockers: list[str] = []
    if missing:
        blockers.append("required_deliverables_missing")
    if placeholder:
        blockers.append("deliverables_still_template")
    if signal_errors:
        blockers.append("structured_gate_signals_invalid")
    if review_status not in {"approved", "pivot"}:
        blockers.append(f"phase_review_{review_status}")
    if gate_status != "approved":
        blockers.append(f"user_gate_{gate_status}")
    if loop_count >= loop_limit and decision == "escalate_to_user":
        blockers.append("loop_limit_reached")

    return {
        "project_root": str(project_root),
        "phase": phase_name,
        "gate": gate_key,
        "decision": decision,
        "scores": {
            "evidence_completeness": completeness,
            "review_readiness": 100 if review_status == "approved" else 0,
            "human_gate": 100 if gate_status == "approved" else 0,
        },
        "review_status": review_status,
        "gate_status": gate_status,
        "loop_count": loop_count,
        "loop_limit": loop_limit,
        "existing_deliverables": existing,
        "missing_deliverables": missing,
        "placeholder_deliverables": placeholder,
        "signal_errors": signal_errors,
        "pivot_candidates": pivot_candidates,
        "blockers": blockers,
    }


def _phase_loop_key(phase_name: str) -> str:
    # Support both new semantic and legacy phase names
    phase_mapping = {
        "survey": "survey_critic",
        "pilot": "pilot_code_adviser",
        "experiments": "experiment_code_adviser",
        "paper": "writer_reviewer",
        "reflection": "reflector_curator",
        # Legacy names for backward compatibility
        "01-survey": "survey_critic",
        "02-pilot-analysis": "pilot_code_adviser",
        "03-full-experiments": "experiment_code_adviser",
        "04-paper": "writer_reviewer",
        "05-reflection-evolution": "reflector_curator",
    }
    return phase_mapping[phase_name]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate the scored quality gate for a project phase."
    )
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--phase", choices=sorted(PHASE_REQUIRED_DELIVERABLES))
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    project_root = Path(args.project_root)
    ensure_project_structure(project_root)
    result = evaluate_quality_gate(project_root, phase=args.phase)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Phase: {result['phase']}")
        print(f"Decision: {result['decision']}")
        print(f"Gate: {result['gate']} ({result['gate_status']})")
        print(f"Phase review: {result['review_status']}")
        print(
            "Scores: "
            f"evidence={result['scores']['evidence_completeness']}, "
            f"review={result['scores']['review_readiness']}, "
            f"gate={result['scores']['human_gate']}"
        )
        if result["blockers"]:
            print("Blockers:")
            for blocker in result["blockers"]:
                print(f"- {blocker}")
    return 0 if result["decision"] == "advance" else 1


if __name__ == "__main__":
    raise SystemExit(main())
