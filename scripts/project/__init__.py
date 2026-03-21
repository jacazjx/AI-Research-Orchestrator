"""Project management module for AI Research Orchestrator.

Provides:
- structure: ensure_project_structure
- phase_ops: reset_state_for_phase, allowed_return_phases,
  warn_starting_phase_prerequisites, suggest_return_phase
- client: detect_platform, select_client_template, detect_client_profile,
  build_client_instruction_text, load_project_config
"""

from project.client import (  # noqa: F401
    DEFAULT_LANGUAGE_POLICY,
    DEFAULT_REVIEWER_CONFIG,
    DEFAULT_RUNTIME_CONFIG,
    build_client_instruction_text,
    detect_client_profile,
    detect_platform,
    load_project_config,
    select_client_template,
)
from project.phase_ops import (  # noqa: F401
    allowed_return_phases,
    reset_state_for_phase,
    suggest_return_phase,
    warn_starting_phase_prerequisites,
)
from project.structure import ensure_project_structure  # noqa: F401

__all__ = [
    "ensure_project_structure",
    "reset_state_for_phase",
    "allowed_return_phases",
    "warn_starting_phase_prerequisites",
    "suggest_return_phase",
    "detect_platform",
    "select_client_template",
    "detect_client_profile",
    "build_client_instruction_text",
    "load_project_config",
    "DEFAULT_LANGUAGE_POLICY",
    "DEFAULT_REVIEWER_CONFIG",
    "DEFAULT_RUNTIME_CONFIG",
]
