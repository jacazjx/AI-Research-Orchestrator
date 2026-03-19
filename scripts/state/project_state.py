"""Project state management - slim core state v3.0.0 schema.

This module provides the slim v3.0.0 state schema which removes duplicate fields
and moves substep tracking to per-phase state files.

Key changes from v2.0.0:
- Removed: current_phase (use phase instead - deduplicated)
- Removed: inner_loops (merged into loop_counts)
- Removed: current_substep, substep_status (moved to per-phase state)
- Removed: progress, loop_limits, deliverables, dashboard_paths, runtime
- Removed: user_config_inherited, gpu_usage_history, active_jobs (moved to runtime config)
"""

from __future__ import annotations

import logging
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from scripts.constants.phases import PHASE_TO_GATE  # type: ignore

logger = logging.getLogger(__name__)

# State file path relative to project root
STATE_FILE_PATH = ".autoresearch/state/research-state.yaml"

# State version for v3.0.0 schema
STATE_VERSION = "3.0.0"


def get_default_loop_counts() -> dict[str, int]:
    """Get default loop counts for all phases.

    Returns:
        Dictionary mapping phase loop keys to their initial count (0).
    """
    return {
        "survey_critic": 0,
        "pilot_code_adviser": 0,
        "experiment_code_adviser": 0,
        "writer_reviewer": 0,
        "reflector_curator": 0,
    }


def get_default_approval_status() -> dict[str, str]:
    """Get default approval status for all gates.

    Returns:
        Dictionary mapping gate names to their initial status ("pending").
    """
    return {
        "gate_1": "pending",
        "gate_2": "pending",
        "gate_3": "pending",
        "gate_4": "pending",
        "gate_5": "pending",
    }


def get_default_phase_reviews() -> dict[str, str]:
    """Get default phase review statuses.

    Returns:
        Dictionary mapping phase review keys to their initial status ("pending").
    """
    return {
        "survey_critic": "pending",
        "pilot_adviser": "pending",
        "experiment_adviser": "pending",
        "paper_reviewer": "pending",
        "reflection_curator": "pending",
    }


def get_default_gate_scores() -> dict[str, int]:
    """Get default gate scores.

    Returns:
        Dictionary mapping gate names to their initial score (0).
    """
    return {
        "gate_1": 0,
        "gate_2": 0,
        "gate_3": 0,
        "gate_4": 0,
        "gate_5": 0,
    }


def build_project_state(
    project_id: str,
    topic: str,
    init_source: str,
    init_paths: list[str],
    client_profile: str,
    client_instruction_file: str,
    process_language: str = "zh-CN",
    paper_language: str = "en-US",
    starting_phase: str = "survey",
    research_type: str = "ml_experiment",
) -> dict[str, Any]:
    """Build a new project state dictionary with slim v3.0.0 schema.

    This function creates the persistent project-level state including:
    - Gate approvals
    - Phase position
    - Loop counts (merged from inner_loops + loop_counts)
    - Project metadata

    Substep tracking is managed separately in per-phase state files.

    Args:
        project_id: Unique project identifier.
        topic: Research topic string.
        init_source: Source of initialization ("init", "wizard", etc.).
        init_paths: List of detected init artifact paths.
        client_profile: Client profile name ("claude" or "codex").
        client_instruction_file: Client instruction filename.
        process_language: Language for process documents (default: zh-CN).
        paper_language: Language for paper documents (default: en-US).
        starting_phase: Starting phase name (default: "survey").
        research_type: Type of research (ml_experiment, theory, survey, applied).

    Returns:
        Complete project state dictionary with v3.0.0 schema.
    """
    # Determine the starting gate based on phase
    starting_gate = PHASE_TO_GATE.get(starting_phase, "gate_1")

    # Get current timestamp
    now = datetime.now(timezone.utc).isoformat()

    return {
        # State version
        "state_version": STATE_VERSION,

        # Project identification
        "project_id": project_id,
        "topic": topic,
        "platform": client_profile,
        "client_profile": client_profile,
        "client_instruction_file": client_instruction_file,

        # Phase state (single field - was duplicated as phase + current_phase)
        "phase": starting_phase,
        "current_gate": starting_gate,
        "subphase": "entry",  # entry | active | review

        # System metadata
        "system_version": STATE_VERSION,
        "created_at": now,
        "last_modified": now,

        # Gate and review approvals
        "approval_status": get_default_approval_status(),
        "phase_reviews": get_default_phase_reviews(),

        # Loop counts (merged: was inner_loops + loop_counts)
        "loop_counts": get_default_loop_counts(),
        "outer_loop": 0,

        # Gate scores and history
        "gate_scores": get_default_gate_scores(),
        "gate_history": [],

        # Pivot and decision tracking
        "pivot_candidates": [],
        "human_decisions": [],
        "overlay_stack": [],

        # Recovery status
        "recovery_status": "idle",

        # Research configuration
        "research_type": research_type,
        "language_policy": {
            "process_docs": process_language,
            "paper_docs": paper_language,
        },

        # Initialization artifacts
        "init_artifacts": {
            "source": init_source,
            "detected_paths": init_paths,
        },
    }


def load_project_state(project_root: Path) -> dict[str, Any] | None:
    """Load project state from file.

    Args:
        project_root: Project root directory.

    Returns:
        Project state dictionary, or None if state file doesn't exist.
    """
    state_path = project_root / STATE_FILE_PATH
    if not state_path.exists():
        logger.debug(f"State file not found: {state_path}")
        return None

    try:
        state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
        logger.debug(f"Loaded state from {state_path}")
        return state
    except Exception as e:
        logger.error(f"Failed to load state from {state_path}: {e}")
        return None


def save_project_state(project_root: Path, state: dict[str, Any]) -> None:
    """Save project state to file using atomic write pattern.

    Writes to a temporary file first, then uses os.replace() for atomic rename.

    Args:
        project_root: Project root directory.
        state: Project state dictionary.
    """
    state_path = project_root / STATE_FILE_PATH
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update last_modified before saving
    state["last_modified"] = datetime.now(timezone.utc).isoformat()

    # Atomic write: write to temp file, then replace
    fd, temp_path = tempfile.mkstemp(
        dir=state_path.parent, prefix=state_path.name + ".", suffix=".tmp"
    )
    try:
        content = yaml.dump(state, allow_unicode=True, default_flow_style=False, sort_keys=False)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
            f.write("\n")
        # Atomic replace on POSIX systems
        os.replace(temp_path, state_path)
        logger.debug(f"Saved state to {state_path}")
    except Exception:
        # Clean up temp file on error
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


def update_last_modified(state: dict[str, Any]) -> None:
    """Update the last_modified timestamp in state.

    Args:
        state: Project state dictionary (mutated in place).
    """
    state["last_modified"] = datetime.now(timezone.utc).isoformat()


def validate_project_state(state: dict[str, Any]) -> list[str]:
    """Validate that a state dict contains all required top-level keys for v3.0.0.

    Args:
        state: State dictionary to validate.

    Returns:
        List of error messages. Empty list means the schema is valid.
    """
    errors: list[str] = []

    # Required top-level keys for v3.0.0
    required_keys = [
        "state_version",
        "project_id",
        "topic",
        "platform",
        "client_profile",
        "client_instruction_file",
        "phase",
        "current_gate",
        "subphase",
        "system_version",
        "created_at",
        "last_modified",
        "approval_status",
        "phase_reviews",
        "loop_counts",
        "outer_loop",
        "gate_scores",
        "gate_history",
        "pivot_candidates",
        "human_decisions",
        "overlay_stack",
        "recovery_status",
        "research_type",
        "language_policy",
        "init_artifacts",
    ]

    for key in required_keys:
        if key not in state:
            errors.append(f"State is missing required key: '{key}'")

    # Validate state version
    if "state_version" in state and state["state_version"] != STATE_VERSION:
        errors.append(
            f"Invalid state_version: expected '{STATE_VERSION}', got '{state['state_version']}'"
        )

    # Validate phase value
    valid_phases = {"survey", "pilot", "experiments", "paper", "reflection", "archive"}
    if "phase" in state and state["phase"] not in valid_phases:
        errors.append(
            f"Invalid phase: '{state['phase']}'. Expected one of: {sorted(valid_phases)}"
        )

    # Validate that removed fields are not present
    removed_fields = [
        ("current_phase", "use 'phase' instead (deduplicated)"),
        ("inner_loops", "merged into 'loop_counts'"),
        ("current_substep", "moved to per-phase state file"),
        ("substep_status", "moved to per-phase state file"),
        ("progress", "derived at runtime"),
        ("loop_limits", "loaded from config only"),
        ("deliverables", "path constants, not state"),
        ("dashboard_paths", "path constants, not state"),
        ("runtime", "path constants, not state"),
        ("user_config_inherited", "moved to runtime config"),
        ("gpu_usage_history", "moved to runtime config"),
        ("active_jobs", "moved to runtime config"),
    ]

    for field, reason in removed_fields:
        if field in state:
            errors.append(f"Deprecated field '{field}' found in state: {reason}")

    return errors
