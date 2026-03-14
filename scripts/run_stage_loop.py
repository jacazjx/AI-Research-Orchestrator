from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from exceptions import PhaseTransitionError
from generate_dashboard import generate_dashboard
from orchestrator_common import (
    NEXT_PHASE,
    PHASE_LOOP_KEY,
    PHASE_TO_GATE,
    PHASE_TO_REVIEW,
    allowed_return_phases,
    append_state_log,
    ensure_project_structure,
    load_state,
    reset_state_for_phase,
    save_state,
    suggest_return_phase,
)
from quality_gate import evaluate_quality_gate


PHASE_AGENT_PAIRS = {
    # New semantic names
    "survey": ("survey", "critic"),
    "pilot": ("code", "adviser"),
    "experiments": ("code", "adviser"),
    "paper": ("paper-writer", "reviewer-editor"),
    "reflection": ("reflector", "curator"),
    # Legacy names for backward compatibility
    "01-survey": ("survey", "critic"),
    "02-pilot-analysis": ("code", "adviser"),
    "03-full-experiments": ("code", "adviser"),
    "04-paper": ("paper-writer", "reviewer-editor"),
    "05-reflection-evolution": ("reflector", "curator"),
}


def run_stage_loop(
    project_root: Path,
    phase: str | None = None,
    actor: str = "orchestrator",
    review_status: str | None = None,
    gate_status: str | None = None,
    increment_loop: bool = False,
    auto_transition: bool = False,
    return_phase: str | None = None,
    note: str = "",
) -> dict[str, object]:
    project_root = project_root.resolve()
    state = load_state(project_root)
    phase_name = phase or state["current_phase"]
    gate_key = PHASE_TO_GATE.get(phase_name, state["current_gate"])
    review_key = PHASE_TO_REVIEW[phase_name]
    loop_key = PHASE_LOOP_KEY[phase_name]

    state["current_phase"] = phase_name
    state["phase"] = phase_name
    state["current_gate"] = gate_key
    state["progress"]["current_agent"] = actor

    loop_incremented = False
    if increment_loop:
        state["inner_loops"][loop_key] = int(state["inner_loops"].get(loop_key, 0)) + 1
        state["loop_counts"][loop_key] = int(state["loop_counts"].get(loop_key, 0)) + 1
        loop_incremented = True

    if review_status is not None:
        state["phase_reviews"][review_key] = review_status
        if review_status == "revise" and not loop_incremented:
            state["inner_loops"][loop_key] = int(state["inner_loops"].get(loop_key, 0)) + 1
            state["loop_counts"][loop_key] = int(state["loop_counts"].get(loop_key, 0)) + 1
            loop_incremented = True
    if gate_status is not None:
        state["approval_status"][gate_key] = gate_status
        append_state_log(
            state,
            "human_decisions",
            {
                "type": "gate_update",
                "gate": gate_key,
                "status": gate_status,
                "phase": phase_name,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "note": note,
            },
        )

    save_state(project_root, state)
    gate_result = evaluate_quality_gate(project_root, phase=phase_name)
    state = load_state(project_root)
    score = int(round(sum(gate_result["scores"].values()) / max(len(gate_result["scores"]), 1)))
    state["gate_scores"][gate_key] = score
    state["progress"]["last_gate_result"] = gate_result["decision"]
    state["progress"]["active_blocker"] = gate_result["blockers"][0] if gate_result["blockers"] else "none"
    state["progress"]["next_action"] = _next_action(gate_result["decision"], phase_name)
    state["progress"]["allowed_return_phases"] = allowed_return_phases(phase_name)
    state["progress"]["suggested_return_phase"] = suggest_return_phase(phase_name, gate_result["blockers"])
    if _should_continue_internal_iteration(gate_result["decision"], review_status, gate_status):
        next_agent = _next_loop_agent(phase_name, actor)
        state["progress"]["current_agent"] = next_agent
        state["subphase"] = f"iteration-{state['loop_counts'][loop_key]}"
        state["progress"]["next_action"] = f"run-{next_agent}"
    append_state_log(
        state,
        "gate_history",
        {
            "phase": phase_name,
            "gate": gate_key,
            "decision": gate_result["decision"],
            "score": score,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "note": note,
        },
    )

    transitioned_to = None
    returned_to = None
    if gate_status == "rejected":
        state["progress"]["next_action"] = "await-human-return-phase-selection"
        if return_phase:
            allowed_phases = allowed_return_phases(phase_name)
            if return_phase not in allowed_phases:
                raise PhaseTransitionError(
                    f"Unsupported return phase for {phase_name}: {return_phase}",
                    from_phase=phase_name,
                    to_phase=return_phase,
                    reason="invalid_return_phase",
                )
            reset_state_for_phase(state, return_phase)
            returned_to = return_phase
            state["outer_loop"] = int(state.get("outer_loop", 0)) + 1
            state["progress"]["current_agent"] = "orchestrator"
            state["progress"]["active_blocker"] = "none"
            state["progress"]["next_action"] = f"resume-{return_phase}"
            state["progress"]["completion_percent"] = _completion_percent(return_phase)
    if auto_transition and gate_result["decision"] == "advance":
        transitioned_to = NEXT_PHASE.get(phase_name)
        if transitioned_to:
            state["outer_loop"] = int(state.get("outer_loop", 0)) + 1
            reset_state_for_phase(state, transitioned_to)
            state["progress"]["current_agent"] = "orchestrator"
            state["progress"]["active_blocker"] = "none"
            state["progress"]["next_action"] = (
                "project-complete" if transitioned_to == "06-archive" else f"start-{transitioned_to}"
            )
            state["progress"]["completion_percent"] = _completion_percent(transitioned_to)

    save_state(project_root, state)
    generate_dashboard(project_root)
    return {
        "project_root": str(project_root),
        "phase": phase_name,
        "decision": gate_result["decision"],
        "gate": gate_key,
        "score": score,
        "transitioned_to": transitioned_to,
        "returned_to": returned_to,
        "loop_count": state["loop_counts"].get(loop_key, 0),
        "allowed_return_phases": state["progress"]["allowed_return_phases"],
        "suggested_return_phase": state["progress"]["suggested_return_phase"],
    }


def _next_action(decision: str, phase_name: str) -> str:
    if decision == "advance":
        return f"prepare-transition-from-{phase_name}"
    if decision == "pivot":
        return "await-human-pivot-decision"
    if decision == "escalate_to_user":
        return "escalate-to-user"
    return f"continue-{phase_name}-loop"


def _completion_percent(phase_name: str) -> int:
    return {
        # New semantic names
        "survey": 10,
        "pilot": 30,
        "experiments": 55,
        "paper": 80,
        "reflection": 95,
        # Legacy names for backward compatibility
        "01-survey": 10,
        "02-pilot-analysis": 30,
        "03-full-experiments": 55,
        "04-paper": 80,
        "05-reflection-evolution": 95,
        "06-archive": 100,
    }[phase_name]


def _next_loop_agent(phase_name: str, actor: str) -> str:
    pair = PHASE_AGENT_PAIRS[phase_name]
    normalized_actor = actor.strip().lower()
    if normalized_actor == pair[0]:
        return pair[1]
    if normalized_actor == pair[1]:
        return pair[0]
    return pair[0]


def _should_continue_internal_iteration(decision: str, review_status: str | None, gate_status: str | None) -> bool:
    if decision != "revise":
        return False
    if gate_status == "rejected":
        return False
    return review_status != "approved"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Advance a phase-local stage loop and refresh gate status.")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--phase", choices=sorted(PHASE_TO_REVIEW))
    parser.add_argument("--actor", default="orchestrator")
    parser.add_argument("--review-status")
    parser.add_argument("--gate-status")
    parser.add_argument("--increment-loop", action="store_true")
    parser.add_argument("--auto-transition", action="store_true")
    parser.add_argument("--return-phase")
    parser.add_argument("--note", default="")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()

    # Ensure project structure
    ensure_project_structure(project_root, create_if_missing=False)

    result = run_stage_loop(
        project_root,
        phase=args.phase,
        actor=args.actor,
        review_status=args.review_status,
        gate_status=args.gate_status,
        increment_loop=args.increment_loop,
        auto_transition=args.auto_transition,
        return_phase=args.return_phase,
        note=args.note,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
