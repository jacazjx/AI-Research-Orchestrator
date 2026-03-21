"""State management module for AI Research Orchestrator.

This module provides state read/write/migration functions.
Import from orchestrator_common for backward compatibility.
"""

from __future__ import annotations

import logging
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


def load_state(project_root: Path) -> dict[str, Any]:
    """Load project state from YAML file."""
    from orchestrator_common import load_state as _load_state

    return _load_state(project_root)


def save_state(project_root: Path, state: dict[str, Any]) -> None:
    """Save project state to YAML file."""
    from orchestrator_common import save_state as _save_state

    return _save_state(project_root, state)


def build_state(
    project_id: str,
    topic: str,
    init_source: str,
    init_paths: list[str],
    client_profile: str,
    client_instruction_file: str,
    process_language: str = "zh-CN",
    paper_language: str = "en-US",
    starting_phase: str = "survey",
) -> dict[str, Any]:
    """Build new project state."""
    from orchestrator_common import build_state as _build_state

    return _build_state(
        project_id=project_id,
        topic=topic,
        init_source=init_source,
        init_paths=init_paths,
        client_profile=client_profile,
        client_instruction_file=client_instruction_file,
        process_language=process_language,
        paper_language=paper_language,
        starting_phase=starting_phase,
    )


def validate_state_schema(state: dict[str, Any]) -> list[str]:
    """Validate state schema and return error messages."""
    from orchestrator_common import validate_state_schema as _validate

    return _validate(state)
