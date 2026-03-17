"""Constants module for AI Research Orchestrator.

This module provides centralized access to all system constants:
- version: System version and version history
- paths: Directory paths and deliverable paths
- phases: Phase-related constants and helper functions
"""

from .paths import (
    AGENT_DIRECTORIES,
    EXPECTED_DELIVERABLE_PREFIXES,
    MAIN_DIRECTORIES,
    OLD_TO_NEW_PATH_MAPPING,
    PHASE_DIRECTORIES,
    REQUIRED_DIRECTORIES,
    SCRIPT_DIR,
    SKILL_DIR,
    SYSTEM_DIRECTORIES,
    TEMPLATE_ROOT,
)
from .phases import (
    DEFAULT_DELIVERABLES,
    DEFAULT_LOOP_LIMITS,
    HANDOFF_REQUIREMENTS,
    LEGACY_TO_SEMANTIC_PHASE,
    LOOP_REQUIREMENTS,
    NEXT_PHASE,
    NEXT_PHASE_LEGACY,
    PHASE_AGENT_PAIRS,
    PHASE_COMPLETION,
    PHASE_LOOP_KEY,
    PHASE_REQUIRED_DELIVERABLES,
    PHASE_SEQUENCE,
    PHASE_TO_GATE,
    PHASE_TO_GATE_LEGACY,
    PHASE_TO_REVIEW,
    SEMANTIC_TO_LEGACY_PHASE,
    STRUCTURED_SIGNAL_REQUIREMENTS,
    get_all_phase_aliases,
    get_legacy_phase_name,
    get_phase_agents,
    normalize_phase_name,
)
from .version import SYSTEM_VERSION, SYSTEM_VERSION_NAME, VERSION_HISTORY

__all__ = [
    # Version constants
    "SYSTEM_VERSION",
    "SYSTEM_VERSION_NAME",
    "VERSION_HISTORY",
    # Path constants
    "SCRIPT_DIR",
    "SKILL_DIR",
    "TEMPLATE_ROOT",
    "PHASE_DIRECTORIES",
    "MAIN_DIRECTORIES",
    "AGENT_DIRECTORIES",
    "SYSTEM_DIRECTORIES",
    "REQUIRED_DIRECTORIES",
    "DEFAULT_DELIVERABLES",
    "EXPECTED_DELIVERABLE_PREFIXES",
    "OLD_TO_NEW_PATH_MAPPING",
    # Phase constants
    "PHASE_SEQUENCE",
    "PHASE_AGENT_PAIRS",
    "LEGACY_TO_SEMANTIC_PHASE",
    "SEMANTIC_TO_LEGACY_PHASE",
    "PHASE_TO_GATE",
    "PHASE_TO_GATE_LEGACY",
    "NEXT_PHASE",
    "NEXT_PHASE_LEGACY",
    "HANDOFF_REQUIREMENTS",
    "LOOP_REQUIREMENTS",
    "PHASE_REQUIRED_DELIVERABLES",
    "PHASE_TO_REVIEW",
    "PHASE_LOOP_KEY",
    "PHASE_COMPLETION",
    "DEFAULT_LOOP_LIMITS",
    "STRUCTURED_SIGNAL_REQUIREMENTS",
    # Phase helper functions
    "normalize_phase_name",
    "get_legacy_phase_name",
    "get_all_phase_aliases",
    "get_phase_agents",
]