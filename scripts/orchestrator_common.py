"""Backward-compatible re-export hub for AI Research Orchestrator.

DEPRECATED: This module re-exports everything from the new modular structure.
New code should import directly from submodules:
- from state import load_state, save_state, build_state
- from project import ensure_project_structure, detect_platform
- from gitmem import gitmem_init, gitmem_commit
- from constants import PHASE_SEQUENCE, SYSTEM_VERSION

This file will be kept for backward compatibility and will not be removed.
"""

from __future__ import annotations

import json
import logging
import re
import shlex
from pathlib import Path
from typing import Any

# ============================================================================
# Re-export from constants module
# ============================================================================

from constants import (  # noqa: F401
    AGENT_DIRECTORIES,
    DEFAULT_ARIS_CONFIG,
    DEFAULT_DELIVERABLES,
    DEFAULT_LOOP_LIMITS,
    EXPECTED_DELIVERABLE_PREFIXES,
    HANDOFF_REQUIREMENTS,
    IDEA_STATE_FILENAME,
    LEGACY_TO_SEMANTIC_PHASE,
    LOOP_REQUIREMENTS,
    MAIN_DIRECTORIES,
    MAX_REVIEW_ROUNDS,
    NEXT_PHASE,
    OLD_TO_NEW_PATH_MAPPING,
    PHASE_AGENT_PAIRS,
    PHASE_COMPLETION,
    PHASE_DIRECTORIES,
    PHASE_LOOP_KEY,
    PHASE_REQUIRED_DELIVERABLES,
    PHASE_SEQUENCE,
    PHASE_TO_GATE,
    PHASE_TO_REVIEW,
    POSITIVE_SCORE_THRESHOLD,
    POSITIVE_VERDICT_KEYWORDS,
    REQUIRED_DIRECTORIES,
    REVIEW_STATE_FILENAME,
    SCRIPT_DIR,
    SEMANTIC_TO_LEGACY_PHASE,
    SKILL_DIR,
    STRUCTURED_SIGNAL_REQUIREMENTS,
    SYSTEM_DIRECTORIES,
    SYSTEM_VERSION,
    SYSTEM_VERSION_NAME,
    TEMPLATE_ROOT,
    VERSION_HISTORY,
    get_all_phase_aliases,
    get_legacy_phase_name,
    get_phase_agents,
    normalize_phase_name,
)

# ============================================================================
# Re-export from utils module
# ============================================================================

from utils import (  # noqa: F401
    build_template_variables,
    normalize_relative_path,
    read_yaml,
    render_template_string,
    render_template_tree,
    slugify,
    write_text_if_needed,
    write_yaml,
    yaml_dump,
    yaml_load,
)

# ============================================================================
# Re-export from state module
# ============================================================================

from state import (  # noqa: F401
    build_state,
    ensure_complete_deliverables,
    is_unmodified_template,
    load_json,
    load_state,
    normalize_signal_value,
    parse_markdown_fields,
    save_state,
    validate_deliverable_content,
    validate_deliverable_location,
    validate_state_schema,
    validate_structured_signals,
    write_json,
)

# ============================================================================
# Re-export from project module
# ============================================================================

from project import (  # noqa: F401
    DEFAULT_LANGUAGE_POLICY,
    DEFAULT_REVIEWER_CONFIG,
    DEFAULT_RUNTIME_CONFIG,
    allowed_return_phases,
    build_client_instruction_text,
    detect_client_profile,
    detect_platform,
    ensure_project_structure,
    load_project_config,
    reset_state_for_phase,
    select_client_template,
    suggest_return_phase,
    warn_starting_phase_prerequisites,
)

# ============================================================================
# Re-export from gitmem module
# ============================================================================

from gitmem import (  # noqa: F401
    GITMEM_DIR,
    GITMEM_LOOP_THRESHOLD,
    GITMEM_TRACKED_DIRS,
    gitmem_check_loop,
    gitmem_checkpoint,
    gitmem_commit,
    gitmem_diff,
    gitmem_get_loop_info,
    gitmem_history,
    gitmem_init,
    gitmem_is_initialized,
    gitmem_list_tags,
    gitmem_rollback,
)


# ============================================================================
# Configure module logger
# ============================================================================

logger = logging.getLogger(__name__)


# ============================================================================
# Remaining local constants
# ============================================================================

# Markdown field parsing regex (re-exported from state.validator)
MARKDOWN_FIELD_RE = re.compile(r"^- ([^:\n]+):\s*(.+)$", re.MULTILINE)


# ============================================================================
# Remaining local utility functions
# ============================================================================


def detect_client_init_artifacts(project_root: Path) -> list[str]:
    """Detect client init artifacts in the project root."""
    artifacts: list[str] = []
    for candidate in sorted(project_root.glob("*.md")):
        if candidate.name in {"workspace-manifest.md"}:
            continue
        artifacts.append(candidate.relative_to(project_root).as_posix())
    return artifacts


def build_list_section(items: list[str], empty_message: str) -> str:
    """Build a markdown list section."""
    if not items:
        return f"- {empty_message}"
    return "\n".join(f"- {item}" for item in items)


def resolve_deliverable_path(
    project_root: Path, state: dict[str, Any], key: str
) -> Path:
    """Resolve a deliverable path from state."""
    relative_value = state["deliverables"][key]
    return (project_root / relative_value).resolve()


def append_state_log(
    state: dict[str, Any], key: str, entry: dict[str, Any] | str
) -> None:
    """Append an entry to a state log list."""
    items = list(state.get(key, []))
    if isinstance(entry, str):
        items.append(entry)
    else:
        items.append(json.dumps(entry, ensure_ascii=False, sort_keys=True))
    state[key] = items


def shell_join(parts: list[str]) -> str:
    """Join shell command parts with proper quoting."""
    return " ".join(shlex.quote(part) for part in parts)


def setup_logging(level: int = logging.INFO, log_file: Path | None = None) -> None:
    """Configure logging for the orchestrator."""
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers,
    )


# ============================================================================
# Public API (backward compatibility)
# ============================================================================

__all__ = [
    # Version constants
    "SYSTEM_VERSION", "SYSTEM_VERSION_NAME", "VERSION_HISTORY",
    # Path constants
    "SCRIPT_DIR", "SKILL_DIR", "TEMPLATE_ROOT",
    "PHASE_DIRECTORIES", "MAIN_DIRECTORIES", "AGENT_DIRECTORIES",
    "SYSTEM_DIRECTORIES", "REQUIRED_DIRECTORIES",
    "DEFAULT_DELIVERABLES", "EXPECTED_DELIVERABLE_PREFIXES", "OLD_TO_NEW_PATH_MAPPING",
    # Phase constants
    "PHASE_SEQUENCE", "PHASE_AGENT_PAIRS",
    "LEGACY_TO_SEMANTIC_PHASE", "SEMANTIC_TO_LEGACY_PHASE",
    "PHASE_TO_GATE",
    "NEXT_PHASE",
    "HANDOFF_REQUIREMENTS", "LOOP_REQUIREMENTS",
    "PHASE_REQUIRED_DELIVERABLES", "PHASE_TO_REVIEW",
    "PHASE_LOOP_KEY", "PHASE_COMPLETION",
    "DEFAULT_LOOP_LIMITS", "STRUCTURED_SIGNAL_REQUIREMENTS",
    # Phase helper functions
    "normalize_phase_name", "get_legacy_phase_name",
    "get_all_phase_aliases", "get_phase_agents",
    # YAML utilities
    "yaml_dump", "yaml_load", "read_yaml", "write_yaml",
    # Path utilities
    "normalize_relative_path",
    # Text utilities
    "slugify",
    # Template utilities
    "build_template_variables", "render_template_string",
    "render_template_tree", "write_text_if_needed",
    # Local constants
    "DEFAULT_LANGUAGE_POLICY", "DEFAULT_REVIEWER_CONFIG",
    "REVIEW_STATE_FILENAME", "MAX_REVIEW_ROUNDS",
    "POSITIVE_SCORE_THRESHOLD", "POSITIVE_VERDICT_KEYWORDS",
    "DEFAULT_ARIS_CONFIG", "IDEA_STATE_FILENAME",
    "DEFAULT_RUNTIME_CONFIG", "MARKDOWN_FIELD_RE",
    "GITMEM_DIR", "GITMEM_LOOP_THRESHOLD", "GITMEM_TRACKED_DIRS",
    # JSON utilities
    "load_json", "write_json",
    # Platform and client detection
    "detect_platform", "select_client_template",
    "detect_client_profile", "build_client_instruction_text",
    # State management
    "detect_client_init_artifacts", "build_state",
    "build_list_section", "resolve_deliverable_path",
    "validate_deliverable_location", "ensure_complete_deliverables",
    "load_state", "save_state",
    "warn_starting_phase_prerequisites", "validate_state_schema",
    "load_project_config", "append_state_log",
    # Deliverable validation
    "is_unmodified_template", "validate_deliverable_content",
    "parse_markdown_fields", "validate_structured_signals",
    "normalize_signal_value",
    # Phase transition helpers
    "shell_join", "allowed_return_phases",
    "reset_state_for_phase", "suggest_return_phase",
    # Logging
    "setup_logging",
    # Project structure
    "ensure_project_structure",
    # GitMem functions
    "gitmem_is_initialized", "gitmem_init", "gitmem_commit",
    "gitmem_checkpoint", "gitmem_list_tags",
    "gitmem_check_loop", "gitmem_get_loop_info",
    "gitmem_history", "gitmem_diff", "gitmem_rollback",
]
