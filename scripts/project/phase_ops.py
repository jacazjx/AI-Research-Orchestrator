"""Phase transition operations."""

from __future__ import annotations

from typing import Any

from constants import PHASE_SEQUENCE, PHASE_TO_GATE, PHASE_TO_REVIEW
from constants.phases import normalize_phase_name


def allowed_return_phases(phase_name: str, state: dict[str, Any] | None = None) -> list[str]:
    """Get list of phases that can be returned to from a given phase.

    Args:
        phase_name: Current phase name.
        state: Optional project state dict. If provided and contains
            ``phase_sequence``, only phases in that sequence are offered.

    Returns:
        List of valid return phase names.
    """
    seq = tuple(state.get("phase_sequence", PHASE_SEQUENCE)) if state else PHASE_SEQUENCE
    if phase_name not in seq:
        return []
    index = seq.index(phase_name)
    return list(seq[: index + 1])


def reset_state_for_phase(state: dict[str, Any], phase_name: str) -> None:
    """Reset state for returning to an earlier phase.

    Args:
        state: Project state dictionary.
        phase_name: Phase to reset to.

    Raises:
        PhaseTransitionError: If phase name is invalid.
    """
    if phase_name not in PHASE_SEQUENCE:
        from exceptions import PhaseTransitionError  # type: ignore[import-untyped]

        raise PhaseTransitionError(
            f"Unsupported phase: {phase_name}",
            to_phase=phase_name,
            reason="invalid_phase",
        )
    index = PHASE_SEQUENCE.index(phase_name)
    for candidate in PHASE_SEQUENCE[index:]:
        gate = PHASE_TO_GATE[candidate]
        review = PHASE_TO_REVIEW[candidate]
        state["approval_status"][gate] = "pending"
        state["phase_reviews"][review] = "pending"
    state["current_phase"] = phase_name
    state["phase"] = phase_name
    state["current_gate"] = PHASE_TO_GATE[phase_name]
    state["subphase"] = "entry"
    state["progress"]["allowed_return_phases"] = allowed_return_phases(phase_name, state)
    state["progress"]["suggested_return_phase"] = phase_name


def warn_starting_phase_prerequisites(starting_phase: str) -> list[str]:
    """Return warnings when starting a project at a non-survey phase.

    Args:
        starting_phase: Requested starting phase (semantic or legacy name).

    Returns:
        List of warning strings. Empty list means no warnings (survey start).
    """
    phase = normalize_phase_name(starting_phase)
    if phase not in PHASE_SEQUENCE:
        return []
    idx = list(PHASE_SEQUENCE).index(phase)
    if idx == 0:
        return []

    skipped = list(PHASE_SEQUENCE)[:idx]
    warnings = [
        f"Starting at '{phase}' skips phase '{p}' -- "
        f"deliverables from that phase will NOT exist in this project."
        for p in skipped
    ]
    warnings.append(
        "If you have existing work from prior phases, add deliverables manually "
        "or use 'migrate-project' to import an existing project structure."
    )
    return warnings


def suggest_return_phase(phase_name: str, blockers: list[str]) -> str:
    """Suggest a return phase based on blockers.

    Args:
        phase_name: Current phase name.
        blockers: List of blocker identifiers.

    Returns:
        Suggested return phase name.
    """
    if "deliverables_still_template" in blockers or "phase_review_pending" in blockers:
        return phase_name
    options = allowed_return_phases(phase_name)
    if len(options) >= 2:
        return options[-2]
    return phase_name
