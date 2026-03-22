"""Constants module for AI Research Orchestrator.

This module provides centralized access to all system constants:
- version: System version and version history
- paths: Directory paths and deliverable paths
- phases: Phase-related constants and helper functions
- aris: ARIS integration constants
"""

from .aris import (
    DEFAULT_ARIS_CONFIG,
    IDEA_STATE_FILENAME,
    MAX_REVIEW_ROUNDS,
    POSITIVE_SCORE_THRESHOLD,
    POSITIVE_VERDICT_KEYWORDS,
    REVIEW_STATE_FILENAME,
)
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
    PHASE_AGENT_PAIRS,
    PHASE_COMPLETION,
    PHASE_LOOP_KEY,
    PHASE_REQUIRED_DELIVERABLES,
    PHASE_SEQUENCE,
    PHASE_TO_GATE,
    PHASE_TO_REVIEW,
    RESEARCH_TYPE_PHASE_SEQUENCE,
    SEMANTIC_TO_LEGACY_PHASE,
    get_all_phase_aliases,
    get_legacy_phase_name,
    get_phase_agents,
    get_phase_sequence_for_research_type,
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
    "RESEARCH_TYPE_PHASE_SEQUENCE",
    "PHASE_AGENT_PAIRS",
    "LEGACY_TO_SEMANTIC_PHASE",
    "SEMANTIC_TO_LEGACY_PHASE",
    "PHASE_TO_GATE",
    "NEXT_PHASE",
    "HANDOFF_REQUIREMENTS",
    "LOOP_REQUIREMENTS",
    "PHASE_REQUIRED_DELIVERABLES",
    "PHASE_TO_REVIEW",
    "PHASE_LOOP_KEY",
    "PHASE_COMPLETION",
    "DEFAULT_LOOP_LIMITS",
    # Phase helper functions
    "normalize_phase_name",
    "get_legacy_phase_name",
    "get_all_phase_aliases",
    "get_phase_agents",
    "get_phase_sequence_for_research_type",
    # ARIS constants
    "REVIEW_STATE_FILENAME",
    "IDEA_STATE_FILENAME",
    "MAX_REVIEW_ROUNDS",
    "POSITIVE_SCORE_THRESHOLD",
    "POSITIVE_VERDICT_KEYWORDS",
    "DEFAULT_ARIS_CONFIG",
]
