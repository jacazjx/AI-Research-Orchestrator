"""State validation functions."""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

from constants import (
    DEFAULT_DELIVERABLES,
    EXPECTED_DELIVERABLE_PREFIXES,
    LEGACY_TO_SEMANTIC_PHASE,
    PHASE_SEQUENCE,
)

from utils import build_template_variables, render_template_string
from constants.paths import TEMPLATE_ROOT

logger = logging.getLogger(__name__)

# Markdown field parsing regex
MARKDOWN_FIELD_RE = re.compile(r"^- ([^:\n]+):\s*(.+)$", re.MULTILINE)


def validate_state_schema(state: dict[str, Any]) -> list[str]:
    """Validate that a loaded state dict contains all required top-level keys.

    Args:
        state: Loaded state dictionary.

    Returns:
        List of error messages. Empty list means the schema is valid.
    """
    errors: list[str] = []
    required_keys = [
        "current_phase",
        "deliverables",
        "approval_status",
        "phase_reviews",
        "loop_counts",
    ]
    for key in required_keys:
        if key not in state:
            errors.append(f"State is missing required key: '{key}'")

    if "current_phase" in state:
        phase = state["current_phase"]
        valid_phases = (
            set(PHASE_SEQUENCE)
            | set(LEGACY_TO_SEMANTIC_PHASE)
            | {"archive", "06-archive"}
        )
        if phase not in valid_phases:
            errors.append(
                f"State 'current_phase' has unknown value: '{phase}'. "
                f"Expected one of: {sorted(valid_phases)}"
            )

    # Validate approval_status structure
    if "approval_status" in state:
        expected_gates = {"gate_1", "gate_2", "gate_3", "gate_4", "gate_5"}
        actual_gates = (
            set(state["approval_status"].keys())
            if isinstance(state["approval_status"], dict)
            else set()
        )
        missing_gates = expected_gates - actual_gates
        if missing_gates:
            errors.append(f"approval_status missing gates: {sorted(missing_gates)}")

    # Validate phase_reviews structure
    if "phase_reviews" in state:
        expected_reviews = {
            "survey_critic",
            "pilot_adviser",
            "experiment_adviser",
            "paper_reviewer",
            "reflection_curator",
        }
        actual_reviews = (
            set(state["phase_reviews"].keys())
            if isinstance(state["phase_reviews"], dict)
            else set()
        )
        missing_reviews = expected_reviews - actual_reviews
        if missing_reviews:
            errors.append(f"phase_reviews missing keys: {sorted(missing_reviews)}")

    # Validate loop_counts structure
    if "loop_counts" in state:
        from constants import PHASE_LOOP_KEY

        expected_loop_keys = set(PHASE_LOOP_KEY.values())
        actual_loop_keys = (
            set(state["loop_counts"].keys())
            if isinstance(state["loop_counts"], dict)
            else set()
        )
        missing_loop_keys = expected_loop_keys - actual_loop_keys
        if missing_loop_keys:
            errors.append(f"loop_counts missing keys: {sorted(missing_loop_keys)}")

    return errors


def validate_deliverable_content(
    project_root: Path, state: dict[str, Any], key: str
) -> list[str]:
    """Validate that a deliverable has been modified from template.

    Args:
        project_root: Project root directory.
        state: Project state dictionary.
        key: Deliverable key.

    Returns:
        List of validation error messages.
    """
    relative_path = state["deliverables"][key]
    if is_unmodified_template(project_root, state, relative_path):
        return [
            f"{relative_path} is still the unedited template and does not satisfy the gate."
        ]
    if not (project_root / relative_path).read_text(encoding="utf-8").strip():
        return [f"{relative_path} is empty and does not satisfy the gate."]
    return []


def validate_structured_signals(
    project_root: Path, state: dict[str, Any], phase_name: str
) -> list[str]:
    """Validate structured signals for gate validation.

    Note: Structured signal requirements were removed (gate validation now uses
    reviewer agent judgment). This function is retained for backward compatibility
    but always returns an empty list.

    Args:
        project_root: Project root directory.
        state: Project state dictionary.
        phase_name: Phase name to validate.

    Returns:
        Empty list (no structured signal requirements are defined).
    """
    return []


def validate_deliverable_location(
    project_root: Path, relative_path: str, key: str
) -> list[str]:
    """Validate a deliverable path location.

    Args:
        project_root: Project root directory.
        relative_path: Relative path to validate.
        key: Deliverable key.

    Returns:
        List of error messages (empty if valid).
    """
    errors: list[str] = []
    relative = Path(relative_path)
    expected_prefix = EXPECTED_DELIVERABLE_PREFIXES[key]
    if relative.is_absolute():
        errors.append(
            f"{key} must be project-relative, got absolute path: {relative_path}"
        )
        return errors
    if ".." in relative.parts:
        errors.append(f"{key} must stay inside the project root, got: {relative_path}")
        return errors
    normalized = relative.as_posix()
    if not normalized.startswith(expected_prefix):
        errors.append(f"{key} must live under {expected_prefix}, got: {relative_path}")
    return errors


def parse_markdown_fields(path: Path) -> dict[str, str]:
    """Parse markdown key-value fields from a file.

    Args:
        path: Path to markdown file.

    Returns:
        Dictionary of field names to values.
    """
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    fields: dict[str, str] = {}
    for key, value in MARKDOWN_FIELD_RE.findall(text):
        fields[key.strip()] = value.strip().strip("`")
    return fields


def normalize_signal_value(value: str | None) -> str:
    """Normalize a signal value for comparison.

    Args:
        value: Raw signal value.

    Returns:
        Normalized lowercase string.
    """
    if value is None:
        return ""
    normalized = value.strip().strip("`").lower()
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized


def is_unmodified_template(
    project_root: Path, state: dict[str, Any], relative_path: str
) -> bool:
    """Check if a file is still an unmodified template.

    Args:
        project_root: Project root directory.
        state: Project state dictionary.
        relative_path: Relative path to the file.

    Returns:
        True if the file matches the original template.
    """
    target_path = project_root / relative_path
    if not target_path.exists():
        return False
    template_path = TEMPLATE_ROOT / f"{relative_path}.tmpl"
    if not template_path.exists():
        return False
    variables = build_template_variables(project_root, state)
    expected = render_template_string(
        template_path.read_text(encoding="utf-8"), variables
    ).strip()
    actual = target_path.read_text(encoding="utf-8").strip()
    return actual == expected


def ensure_complete_deliverables(state: dict[str, Any]) -> dict[str, Any]:
    """Ensure all required deliverables exist in the state.

    Args:
        state: The current state dictionary.

    Returns:
        The state with complete deliverables.
    """
    if "deliverables" not in state:
        state["deliverables"] = {}

    for key, default_path in DEFAULT_DELIVERABLES.items():
        if key not in state["deliverables"]:
            state["deliverables"][key] = default_path
            logger.info(f"Added missing deliverable: {key} = {default_path}")

    return state
