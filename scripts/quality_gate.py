from __future__ import annotations

import argparse
import json
from pathlib import Path

from orchestrator_common import (
    PHASE_LOOP_KEY,
    PHASE_REQUIRED_DELIVERABLES,
    PHASE_TO_GATE,
    PHASE_TO_REVIEW,
    allowed_return_phases,
    ensure_project_structure,
    load_state,
    normalize_phase_name,
    validate_deliverable_content,
    validate_structured_signals,
)


def evaluate_quality_gate(
    project_root: Path,
    phase: str | None = None,
    state: dict[str, object] | None = None,
) -> dict[str, object]:
    project_root = project_root.resolve()
    if state is None:
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
    _normalized_phase = normalize_phase_name(phase_name)
    _loop_key = PHASE_LOOP_KEY.get(_normalized_phase, f"{_normalized_phase}_loop")
    loop_count = int(state["loop_counts"].get(_loop_key, 0))
    loop_limit = int(state["loop_limits"].get(_loop_key, 0))
    pivot_candidates = list(state.get("pivot_candidates", []))
    signal_errors = validate_structured_signals(project_root, state, phase_name)

    if review_status == "pivot" or pivot_candidates:
        decision = "pivot"
        # Validate pivot candidates against allowed return phases
        allowed_phases = allowed_return_phases(phase_name)
        invalid_pivots = [p for p in pivot_candidates if p not in allowed_phases]
        if invalid_pivots:
            signal_errors.append(
                f"Invalid pivot targets {invalid_pivots}; allowed: {allowed_phases}"
            )
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
        blockers.append(f"Missing: {', '.join(missing)}")
    if placeholder:
        blockers.append(f"Placeholders: {', '.join(placeholder)}")
    if signal_errors:
        for error in signal_errors:
            blockers.append(f"Signal: {error}")
    if review_status not in {"approved", "pivot"}:
        blockers.append(f"Review: {review_status}")
    if gate_status != "approved":
        blockers.append(f"Gate: {gate_status}")
    if loop_count >= loop_limit and decision == "escalate_to_user":
        blockers.append(f"Loop limit ({loop_count}/{loop_limit})")

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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate quality gate for a project phase."
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
        print(f"Review: {result['review_status']}")
        print(f"Completeness: {result['scores']['evidence_completeness']}%")
        if result["blockers"]:
            print("\nBlockers:")
            for blocker in result["blockers"]:
                print(f"  - {blocker}")
    return 0 if result["decision"] == "advance" else 1


if __name__ == "__main__":
    raise SystemExit(main())
