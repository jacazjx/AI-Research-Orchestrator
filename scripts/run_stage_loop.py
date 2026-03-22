from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from exceptions import PhaseTransitionError
from quality_gate import evaluate_quality_gate

from orchestrator_common import (
    NEXT_PHASE,
    PHASE_AGENT_PAIRS,
    PHASE_LOOP_KEY,
    PHASE_TO_GATE,
    PHASE_TO_REVIEW,
    allowed_return_phases,
    append_state_log,
    ensure_project_structure,
    gitmem_checkpoint,
    gitmem_is_initialized,
    load_state,
    logger,
    normalize_phase_name,
    reset_state_for_phase,
    save_state,
    suggest_return_phase,
)

GPU_REQUIRED_PHASES = {"pilot", "experiments"}


def _initialize_gpu_for_phase(
    project_root: Path, state: dict[str, object], phase_name: str
) -> None:
    research_type = state.get("research_type", "")
    if research_type in {"theory", "survey"}:
        return
    normalized_phase = normalize_phase_name(phase_name)
    if normalized_phase not in GPU_REQUIRED_PHASES:
        return
    try:
        from gpu_manager import load_user_gpu_registry

        registry = load_user_gpu_registry()
        devices = registry.get("devices", [])
        available = [
            d for d in devices if isinstance(d, dict) and d.get("status") == "available"
        ]
        if available:
            state.setdefault("progress", {})["gpu_status"] = "available"
            state["progress"]["gpu_count"] = len(available)
            logger.info(f"GPU initialized: {len(available)} device(s) available")
        else:
            state.setdefault("progress", {})["gpu_status"] = "none_available"
            logger.warning("No GPUs available for this phase")
    except ImportError:
        logger.debug("GPU manager not available, skipping GPU initialization")
        state.setdefault("progress", {})["gpu_status"] = "not_configured"
    except FileNotFoundError:
        logger.debug("GPU registry not found, skipping GPU initialization")
        state.setdefault("progress", {})["gpu_status"] = "not_configured"
    except Exception as exc:
        logger.warning(f"Unexpected error during GPU initialization: {exc}")
        state.setdefault("progress", {})["gpu_status"] = "error"


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

    if state.get("previous_phase") != phase_name:
        _initialize_gpu_for_phase(project_root, state, phase_name)

    state["previous_phase"] = phase_name

    loop_incremented = False
    if increment_loop:
        state["inner_loops"][loop_key] = int(state["inner_loops"].get(loop_key, 0)) + 1
        state["loop_counts"][loop_key] = int(state["loop_counts"].get(loop_key, 0)) + 1
        loop_incremented = True

    if review_status is not None:
        state["phase_reviews"][review_key] = review_status
        if review_status == "revise" and not loop_incremented:
            state["inner_loops"][loop_key] = (
                int(state["inner_loops"].get(loop_key, 0)) + 1
            )
            state["loop_counts"][loop_key] = (
                int(state["loop_counts"].get(loop_key, 0)) + 1
            )
            loop_incremented = True

        if review_status == "approved" and gitmem_is_initialized(project_root):
            save_state(project_root, state)
            checkpoint_name = f"{phase_name}-approved"
            gitmem_checkpoint(project_root, checkpoint_name)
            logger.info(f"Created GitMem checkpoint: {checkpoint_name}")

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
        if gate_status == "approved" and gitmem_is_initialized(project_root):
            save_state(project_root, state)
            checkpoint_name = f"phase-gate-{phase_name}-approved"
            gitmem_checkpoint(project_root, checkpoint_name)
            logger.info(f"Created GitMem checkpoint: {checkpoint_name}")

    save_state(project_root, state)
    gate_result = evaluate_quality_gate(project_root, phase=phase_name, state=state)
    score = int(
        round(sum(gate_result["scores"].values()) / max(len(gate_result["scores"]), 1))
    )
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
    if _should_continue_internal_iteration(
        gate_result["decision"], review_status, gate_status
    ):
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
            state["progress"]["completion_percent"] = _completion_percent(
                transitioned_to
            )
            state["previous_phase"] = transitioned_to

    save_state(project_root, state)
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
    from constants import PHASE_COMPLETION

    normalized = normalize_phase_name(phase_name)
    if normalized not in PHASE_COMPLETION:
        if normalized in ("archive", "06-archive"):
            return 100
        raise ValueError(f"Unknown phase name: {phase_name}")
    return PHASE_COMPLETION[normalized]


def _next_loop_agent(phase_name: str, actor: str) -> str:
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
    parser.add_argument(
        "--project-root",
        default=None,
        help="Path to the project root. Defaults to the nearest parent containing .autoresearch/.",
    )
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

    from utils.path_utils import find_project_root

    if args.project_root is not None:
        project_root: Path | None = Path(args.project_root).resolve()
        if not (project_root / ".autoresearch").exists():
            project_root = find_project_root(project_root)
    else:
        project_root = find_project_root()

    if project_root is None:
        import sys as _sys

        print(
            "Error: no AI Research project found in the current directory or its parents.",
            file=_sys.stderr,
        )
        print(
            "Hint: run /init-research first, or pass --project-root explicitly.",
            file=_sys.stderr,
        )
        return 1

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
