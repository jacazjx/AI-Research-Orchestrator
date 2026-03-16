from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from exceptions import PhaseTransitionError
from generate_dashboard import generate_dashboard
from quality_gate import evaluate_quality_gate
from validate_substep import (
    STATUS_APPROVED,
    STATUS_IN_PROGRESS,
    STATUS_PENDING,
    can_advance_substep,
    get_first_substep,
    load_orchestrator_config,
)

from orchestrator_common import (
    NEXT_PHASE,
    PHASE_LOOP_KEY,
    PHASE_TO_GATE,
    PHASE_TO_REVIEW,
    allowed_return_phases,
    append_state_log,
    ensure_project_structure,
    gitmem_check_loop,
    gitmem_checkpoint,
    gitmem_get_loop_info,
    gitmem_is_initialized,
    load_state,
    logger,
    normalize_phase_name,
    reset_state_for_phase,
    save_state,
    suggest_return_phase,
)

PHASE_AGENT_PAIRS = {
    # Semantic names only (legacy names are normalized)
    "survey": ("survey", "critic"),
    "pilot": ("code", "adviser"),
    "experiments": ("code", "adviser"),
    "paper": ("paper-writer", "reviewer-editor"),
    "reflection": ("reflector", "curator"),
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
    substep: str | None = None,
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

    # Load orchestrator config for substep management
    config = load_orchestrator_config(project_root)

    # Initialize current_substep if not set or entering a new phase
    if state.get("current_substep") is None or state.get("previous_phase") != phase_name:
        first_substep = get_first_substep(config, phase_name)
        if first_substep:
            state["current_substep"] = first_substep
            # Set the first substep to in_progress in state
            if "substep_status" not in state:
                state["substep_status"] = {}
            if phase_name not in state["substep_status"]:
                state["substep_status"][phase_name] = {}
            if first_substep not in state["substep_status"][phase_name]:
                state["substep_status"][phase_name][first_substep] = {"status": STATUS_PENDING}
            state["substep_status"][phase_name][first_substep]["status"] = STATUS_IN_PROGRESS

    # Track previous phase for transition detection
    state["previous_phase"] = phase_name

    # Update current_substep if provided
    if substep:
        state["current_substep"] = substep

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

        # Handle substep status updates based on review_status
        current_substep = state.get("current_substep")
        if current_substep:
            # Ensure substep_status structure exists
            if "substep_status" not in state:
                state["substep_status"] = {}
            if phase_name not in state["substep_status"]:
                state["substep_status"][phase_name] = {}
            if current_substep not in state["substep_status"][phase_name]:
                state["substep_status"][phase_name][current_substep] = {"status": STATUS_PENDING}

            if review_status == "approved":
                # Mark substep as approved in state
                state["substep_status"][phase_name][current_substep]["status"] = STATUS_APPROVED
                state["substep_status"][phase_name][current_substep]["review_result"] = "approved"

                # Save state BEFORE creating checkpoint so checkpoint captures approved state
                save_state(project_root, state)

                # Create GitMem checkpoint for substep approval
                if gitmem_is_initialized(project_root):
                    checkpoint_name = f"{phase_name}-{current_substep}-approved"
                    gitmem_checkpoint(project_root, checkpoint_name)
                    logger.info(f"Created GitMem checkpoint: {checkpoint_name}")

                # Check if we can advance to next substep
                # Reload state to get the updated substep_status for can_advance_substep
                state = load_state(project_root)
                advance_result = can_advance_substep(project_root, phase_name, current_substep)
                state = load_state(project_root)

                if advance_result["can_advance"]:
                    next_substep = advance_result["details"].get("next_substep")
                    if next_substep:
                        state["current_substep"] = next_substep
                        # Set next substep to in_progress
                        if next_substep not in state["substep_status"][phase_name]:
                            state["substep_status"][phase_name][next_substep] = {
                                "status": STATUS_PENDING
                            }
                        state["substep_status"][phase_name][next_substep][
                            "status"
                        ] = STATUS_IN_PROGRESS
                        logger.info(f"Advanced to next substep: {next_substep}")
                    else:
                        # Last substep approved, phase gate will handle transition
                        logger.info(f"All substeps completed for phase: {phase_name}")
            elif review_status == "revise":
                # Increment attempts for current substep
                current_attempts = state["substep_status"][phase_name][current_substep].get(
                    "attempts", 0
                )
                state["substep_status"][phase_name][current_substep]["attempts"] = (
                    current_attempts + 1
                )
                state["substep_status"][phase_name][current_substep]["status"] = STATUS_IN_PROGRESS
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
        # Create checkpoint on human gate approval
        if gate_status == "approved" and gitmem_is_initialized(project_root):
            # Save state BEFORE creating checkpoint so checkpoint captures approved state
            save_state(project_root, state)
            checkpoint_name = f"phase-gate-{phase_name}-approved"
            gitmem_checkpoint(project_root, checkpoint_name)
            logger.info(f"Created GitMem checkpoint: {checkpoint_name}")

    save_state(project_root, state)
    gate_result = evaluate_quality_gate(project_root, phase=phase_name)
    state = load_state(project_root)
    score = int(round(sum(gate_result["scores"].values()) / max(len(gate_result["scores"]), 1)))
    state["gate_scores"][gate_key] = score
    state["progress"]["last_gate_result"] = gate_result["decision"]
    state["progress"]["active_blocker"] = (
        gate_result["blockers"][0] if gate_result["blockers"] else "none"
    )
    state["progress"]["next_action"] = _next_action(gate_result["decision"], phase_name)
    state["progress"]["allowed_return_phases"] = allowed_return_phases(phase_name)
    state["progress"]["suggested_return_phase"] = suggest_return_phase(
        phase_name, gate_result["blockers"]
    )
    # Create checkpoint on substep approval when gate passes
    if (
        review_status == "approved"
        and gate_result["decision"] in ("advance", "approve")
        and gitmem_is_initialized(project_root)
    ):
        loop_count = state["loop_counts"].get(loop_key, 0)
        checkpoint_name = f"{phase_name}-{loop_count}-approved"
        gitmem_checkpoint(project_root, checkpoint_name)
    if _should_continue_internal_iteration(gate_result["decision"], review_status, gate_status):
        next_agent = _next_loop_agent(phase_name, actor)
        state["progress"]["current_agent"] = next_agent
        state["subphase"] = f"iteration-{state['loop_counts'][loop_key]}"
        state["progress"]["next_action"] = f"run-{next_agent}"

        # Loop guard: check for edit loops on phase deliverables
        loop_warnings = _check_phase_loop_guard(project_root, phase_name, state)
        if loop_warnings:
            state["progress"]["loop_warnings"] = loop_warnings
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
            # Reset current_substep for the new phase
            state["current_substep"] = None
            state["previous_phase"] = return_phase
    if auto_transition and gate_result["decision"] == "advance":
        transitioned_to = NEXT_PHASE.get(phase_name)
        if transitioned_to:
            state["outer_loop"] = int(state.get("outer_loop", 0)) + 1
            reset_state_for_phase(state, transitioned_to)
            state["progress"]["current_agent"] = "orchestrator"
            state["progress"]["active_blocker"] = "none"
            state["progress"]["next_action"] = (
                "project-complete"
                if transitioned_to == "06-archive"
                else f"start-{transitioned_to}"
            )
            state["progress"]["completion_percent"] = _completion_percent(transitioned_to)
            # Reset current_substep for the new phase
            state["current_substep"] = None
            state["previous_phase"] = transitioned_to

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
        "loop_warnings": state["progress"].get("loop_warnings", []),
        "current_substep": state.get("current_substep"),
    }


def _next_action(decision: str, phase_name: str) -> str:
    if decision == "advance":
        return f"prepare-transition-from-{phase_name}"
    if decision == "pivot":
        return "await-human-pivot-decision"
    if decision == "escalate_to_user":
        return "escalate-to-user"
    return f"continue-{phase_name}-loop"


def _check_phase_loop_guard(
    project_root: Path, phase_name: str, state: dict[str, object]
) -> list[str]:
    """Check for edit loops on phase deliverables and warn if detected.

    Args:
        project_root: Project root directory.
        phase_name: Current phase name.
        state: Current state dictionary.

    Returns:
        List of warning messages for files in edit loops.
    """
    warnings: list[str] = []

    # Get phase deliverables to check
    from orchestrator_common import PHASE_REQUIRED_DELIVERABLES

    deliverables = PHASE_REQUIRED_DELIVERABLES.get(phase_name, ())
    if not deliverables:
        return warnings

    # Check each deliverable for edit loops
    for deliverable_key in deliverables:
        relative_path = state.get("deliverables", {}).get(deliverable_key, "")
        if not relative_path:
            continue

        # Check if file is in edit loop
        if gitmem_check_loop(project_root, relative_path):
            loop_info = gitmem_get_loop_info(project_root, relative_path)
            warning = (
                f"Edit loop detected: {relative_path} has {loop_info['change_count']} "
                f"consecutive changes without checkpoint. "
                f"Consider creating a checkpoint with gitmem_checkpoint()."
            )
            logger.warning(warning)
            warnings.append(warning)

    return warnings


def _completion_percent(phase_name: str) -> int:
    phase_progress = {
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
    }
    normalized = normalize_phase_name(phase_name)
    if normalized not in phase_progress:
        raise ValueError(f"Unknown phase name: {phase_name}")
    return phase_progress[normalized]


def _next_loop_agent(phase_name: str, actor: str) -> str:
    # Normalize phase name to support both semantic and legacy names
    normalized = normalize_phase_name(phase_name)
    pair = PHASE_AGENT_PAIRS[normalized]
    normalized_actor = actor.strip().lower()
    if normalized_actor == pair[0]:
        return pair[1]
    if normalized_actor == pair[1]:
        return pair[0]
    return pair[0]


def _should_continue_internal_iteration(
    decision: str, review_status: str | None, gate_status: str | None
) -> bool:
    if decision != "revise":
        return False
    if gate_status == "rejected":
        return False
    return review_status != "approved"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Advance a phase-local stage loop and refresh gate status."
    )
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--phase", choices=sorted(PHASE_TO_REVIEW))
    parser.add_argument("--actor", default="orchestrator")
    parser.add_argument("--review-status")
    parser.add_argument("--gate-status")
    parser.add_argument("--increment-loop", action="store_true")
    parser.add_argument("--auto-transition", action="store_true")
    parser.add_argument("--return-phase")
    parser.add_argument("--note", default="")
    parser.add_argument("--substep", help="Current substep name to track")
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
        substep=args.substep,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
