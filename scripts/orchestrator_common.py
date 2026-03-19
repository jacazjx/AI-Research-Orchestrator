"""Compatibility layer for AI Research Orchestrator.

This module provides backward-compatible imports from the new modular structure.
All constants are now in scripts/constants/ and utilities are in scripts/utils/.

DEPRECATED: New code should import directly from submodules:
- from scripts.constants import SYSTEM_VERSION, PHASE_SEQUENCE, ...
- from scripts.utils import yaml_dump, read_yaml, write_yaml, ...

This file will be kept for backward compatibility and will not be removed.
"""

from __future__ import annotations

import json
import logging
import os
import re
import shlex
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Import all constants from constants module
# noqa: I001,I004 -- Use simple imports (not scripts.*)
# for script compatibility
# type: ignore[import-untyped]
from constants import (  # Version constants  # noqa: F401
    AGENT_DIRECTORIES,
    DEFAULT_DELIVERABLES,
    DEFAULT_LOOP_LIMITS,
    EXPECTED_DELIVERABLE_PREFIXES,
    HANDOFF_REQUIREMENTS,
    LEGACY_TO_SEMANTIC_PHASE,
    LOOP_REQUIREMENTS,
    MAIN_DIRECTORIES,
    NEXT_PHASE,
    NEXT_PHASE_LEGACY,
    OLD_TO_NEW_PATH_MAPPING,
    PHASE_AGENT_PAIRS,
    PHASE_COMPLETION,
    PHASE_DIRECTORIES,
    PHASE_LOOP_KEY,
    PHASE_REQUIRED_DELIVERABLES,
    PHASE_SEQUENCE,
    PHASE_TO_GATE,
    PHASE_TO_GATE_LEGACY,
    PHASE_TO_REVIEW,
    REQUIRED_DIRECTORIES,
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

# Import all utilities from utils module
# noqa: I001,I004 -- Use simple imports (not scripts.*)
# for script compatibility
# type: ignore[import-untyped]
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
# Import from new modular structure
# Use direct imports for script-level compatibility (scripts run from scripts/ dir)
# ============================================================================


# Configure module logger
logger = logging.getLogger(__name__)

# ============================================================================
# Local constants (not yet moved to submodules)
# ============================================================================

# Language policy defaults
DEFAULT_LANGUAGE_POLICY = {
    "process_docs": "zh-CN",
    "paper_docs": "en-US",
}

# ARIS Integration: Cross-model review configuration
# Default reviewer model for Codex MCP integration (GPT-5.4 with xhigh reasoning)
DEFAULT_REVIEWER_CONFIG = {
    "model": "gpt-5.4",
    "reasoning_effort": "xhigh",
    "enabled": False,  # Disabled by default, use local sub-agent
}

# ARIS Integration: Review state for long-running loops
# This file survives context compaction and allows loop resumption
REVIEW_STATE_FILENAME = "REVIEW_STATE.json"

# ARIS Integration: Maximum rounds for auto-review-loop
MAX_REVIEW_ROUNDS = 4

# ARIS Integration: Positive assessment threshold
POSITIVE_SCORE_THRESHOLD = 6.0
POSITIVE_VERDICT_KEYWORDS = ("accept", "sufficient", "ready for submission", "almost")

# ARIS Integration: Complete configuration
# Note: GPU protection fields are defined here but enforcement is v1.13.0
DEFAULT_ARIS_CONFIG = {
    "auto_proceed": False,
    "pilot_max_hours": 2,  # v1.13.0: enforcement pending
    "pilot_timeout_hours": 3,  # v1.13.0: enforcement pending
    "max_pilot_ideas": 3,  # v1.13.0: enforcement pending
    "max_total_gpu_hours": 8,  # v1.13.0: enforcement pending
    "reviewer": {
        "enabled": False,
        "model": "gpt-5.4",
        "reasoning_effort": "xhigh",
    },
    "max_review_rounds": 4,
    "positive_score_threshold": 6.0,
    "feishu": {
        "enabled": False,
        "mode": "off",  # off / push / interactive
    },
}

# ARIS Integration: Idea state filename for idea-discovery pipeline
IDEA_STATE_FILENAME = "IDEA_STATE.json"

DEFAULT_RUNTIME_CONFIG = {
    "languages": dict(DEFAULT_LANGUAGE_POLICY),
    "loop_limits": dict(DEFAULT_LOOP_LIMITS),
    "runtime": {
        "stale_after_minutes": 30,
        "auto_discover_gpu": True,
    },
    "backends": {
        "local": "enabled",
        "ssh": "enabled",
    },
    "reviewer": dict(DEFAULT_REVIEWER_CONFIG),
}

# Markdown field parsing regex
MARKDOWN_FIELD_RE = re.compile(r"^- ([^:\n]+):\s*(.+)$", re.MULTILINE)

# GitMem configuration
GITMEM_DIR = ".gitmem"
GITMEM_LOOP_THRESHOLD = 5  # Warn if file has 5+ changes without checkpoint
GITMEM_TRACKED_DIRS = ("docs/", "paper/", "code/", "agents/")


# ============================================================================
# JSON utilities
# ============================================================================


def load_json(path: Path, default: Any) -> Any:
    """Load JSON file with default fallback.

    Args:
        path: Path to JSON file.
        default: Default value if file doesn't exist or is empty.

    Returns:
        Parsed JSON data or default value.
    """
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    """Write data to a JSON file with atomic write pattern.

    Uses a temporary file and atomic replace to prevent corruption
    if the process crashes mid-write.

    Args:
        path: Target file path.
        payload: Python object to serialize as JSON.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    # Atomic write: write to temp file, then replace
    fd, temp_path = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        # Atomic replace on POSIX systems
        os.replace(temp_path, path)
    except Exception:
        # Clean up temp file on error
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


# ============================================================================
# Platform and client detection
# ============================================================================


def detect_platform() -> str:
    """Detect the current running platform.

    Returns:
        Platform name: "claude-code", "codex", or "unknown".
    """
    # Check for Claude Code environment
    if os.environ.get("CLAUDE_CODE"):
        return "claude-code"

    # Check for Codex/OpenAI environment
    if os.environ.get("OPENAI_API_KEY") and not os.environ.get("ANTHROPIC_API_KEY"):
        return "codex"

    # Default to Claude Code as it's the primary platform
    return "claude-code"


def select_client_template(platform: str, template_root: Path) -> Path | None:
    """Select the appropriate client instruction template.

    Args:
        platform: Platform name.
        template_root: Root directory for templates.

    Returns:
        Path to the appropriate template file, or None if not found.
    """
    template_name = "CLAUDE.md.tmpl" if platform in ("claude-code", "claude") else "AGENTS.md.tmpl"
    template_path = template_root / "project-root" / template_name

    # Fall back to default if template doesn't exist
    if not template_path.exists():
        logger.warning(f"Template not found: {template_path}, using default")
        return None

    return template_path


def detect_client_profile(project_root: Path, init_paths: list[str], client_type: str) -> str:
    """Detect the client profile based on existing files or explicit type.

    Args:
        project_root: Project root directory.
        init_paths: List of detected init artifact paths.
        client_type: Explicit client type ("codex", "claude", or "auto").

    Returns:
        Detected client profile name.
    """
    if client_type in {"codex", "claude"}:
        return client_type

    candidates = [Path(path).name for path in init_paths]
    if (project_root / "CLAUDE.md").exists() or "CLAUDE.md" in candidates:
        return "claude"
    if (project_root / "AGENTS.md").exists() or "AGENTS.md" in candidates:
        return "codex"
    return "codex"


def build_client_instruction_text(client_profile: str, state: dict[str, Any]) -> str:
    """Build the client instruction text for AGENTS.md or CLAUDE.md.

    Args:
        client_profile: Client profile name ("codex" or "claude").
        state: Project state dictionary.

    Returns:
        Client instruction text.
    """
    filename = "CLAUDE.md" if client_profile == "claude" else "AGENTS.md"
    return "\n".join(
        [
            f"# {filename}",
            "",
            "This workspace is initialized by the ai-research-orchestrator skill.",
            "",
            "## Core contracts",
            "",
            f"- Machine-readable state: `{DEFAULT_DELIVERABLES['research_state']}`",
            f"- Human-readable manifest: `{DEFAULT_DELIVERABLES['workspace_manifest']}`",
            f"- User IDEA template: `{DEFAULT_DELIVERABLES['idea_brief']}`",
            f"- User reference library: `{DEFAULT_DELIVERABLES['reference_library_index']}`",
            f"- Dashboard status: `{DEFAULT_DELIVERABLES['dashboard_progress']}`",
            "",
            "## Required phases",
            "",
            "- Phase 1: Survey <-> Critic",
            "- Phase 2: Pilot Code <-> Pilot Adviser",
            "- Phase 3: Experiment Code <-> Experiment Adviser",
            "- Phase 4: Paper Writer <-> Reviewer & Editor",
            "- Phase 5: Reflector <-> Curator",
            "",
            "## Required gates",
            "",
            "- Gate 1: research-readiness report approved by the user",
            "- Gate 2: pilot validation pack approved by the user",
            "- Gate 3: experiment evidence package approved by the user",
            "- Gate 4: paper package approved by the user",
            "- Gate 5: reflection/evolution package approved by the user "
            "before overlays or policy changes apply",
            "",
            "## Runtime rules",
            "",
            "- Keep every phase as a two-agent loop under the user-facing orchestrator.",
            "- Update dashboard and runtime registries as phase status changes.",
            "- Do not bypass `research-state.yaml`.",
            "- Do not pivot without explicit human approval.",
            "- Do not claim plagiarism clearance, AI-detection clearance, "
            "or formal proof verification in v1.",
            "",
            "## Language policy",
            "",
            f"- Process documents: `{state['language_policy']['process_docs']}`",
            f"- Paper-facing documents: `{state['language_policy']['paper_docs']}`",
            "",
        ]
    )


# ============================================================================
# State management functions
# ============================================================================


def detect_client_init_artifacts(project_root: Path) -> list[str]:
    """Detect client init artifacts in the project root.

    Args:
        project_root: Project root directory.

    Returns:
        List of detected artifact paths.
    """
    artifacts: list[str] = []
    for candidate in sorted(project_root.glob("*.md")):
        if candidate.name in {"workspace-manifest.md"}:
            continue
        artifacts.append(candidate.relative_to(project_root).as_posix())
    return artifacts


def build_state(
    project_id: str,
    topic: str,
    init_source: str,
    init_paths: list[str],
    client_profile: str,
    client_instruction_file: str,
    process_language: str = DEFAULT_LANGUAGE_POLICY["process_docs"],
    paper_language: str = DEFAULT_LANGUAGE_POLICY["paper_docs"],
    starting_phase: str = "survey",
) -> dict[str, Any]:
    """Build a new project state dictionary.

    Args:
        project_id: Unique project identifier.
        topic: Research topic string.
        init_source: Source of initialization ("init", "wizard", etc.).
        init_paths: List of detected init artifact paths.
        client_profile: Client profile name.
        client_instruction_file: Client instruction filename.
        process_language: Language for process documents.
        paper_language: Language for paper documents.
        starting_phase: Starting phase name.

    Returns:
        Complete project state dictionary.

    Note (Agent Teams Migration):
        Task-level tracking (individual subtask status, agent assignments,
        inter-agent dependencies) is now managed by Claude Code Task tools
        (TaskCreate, TaskUpdate, TaskGet, TaskList) rather than this file.
        This state dictionary tracks phase-level status, gate approvals, loop
        counts, and battle/substep status for persistence across context resets.
        Do NOT add per-task fields here; use Task tools instead.
    """
    # Determine the starting gate based on phase
    starting_gate = PHASE_TO_GATE.get(starting_phase, "gate_1")

    # Get current timestamp
    created_at = datetime.now(timezone.utc).isoformat()

    return {
        "project_id": project_id,
        "topic": topic,
        "platform": client_profile,
        "client_profile": client_profile,
        "client_instruction_file": client_instruction_file,
        "phase": starting_phase,
        "subphase": "entry",
        "current_phase": starting_phase,
        "current_gate": starting_gate,
        "system_version": SYSTEM_VERSION,
        "created_at": created_at,
        "last_modified": created_at,
        "approval_status": {
            "gate_1": "pending",
            "gate_2": "pending",
            "gate_3": "pending",
            "gate_4": "pending",
            "gate_5": "pending",
        },
        "phase_reviews": {
            "survey_critic": "pending",
            "pilot_adviser": "pending",
            "experiment_adviser": "pending",
            "paper_reviewer": "pending",
            "reflection_curator": "pending",
        },
        "current_substep": None,
        "substep_status": _build_default_substep_status(),
        "language_policy": {
            "process_docs": process_language,
            "paper_docs": paper_language,
        },
        "inner_loops": {
            "survey_critic": 0,
            "pilot_code_adviser": 0,
            "experiment_code_adviser": 0,
            "writer_reviewer": 0,
            "reflector_curator": 0,
        },
        "loop_counts": {
            "survey_critic": 0,
            "pilot_code_adviser": 0,
            "experiment_code_adviser": 0,
            "writer_reviewer": 0,
            "reflector_curator": 0,
        },
        "outer_loop": 0,
        "loop_limits": dict(DEFAULT_LOOP_LIMITS),
        "gate_scores": {
            "gate_1": 0,
            "gate_2": 0,
            "gate_3": 0,
            "gate_4": 0,
            "gate_5": 0,
        },
        "gate_history": [],
        "pivot_candidates": [],
        "human_decisions": [],
        "overlay_stack": [],
        "active_jobs": [],
        "recovery_status": "idle",
        "init_artifacts": {
            "source": init_source,
            "detected_paths": init_paths,
        },
        "dashboard_paths": {
            "status": DEFAULT_DELIVERABLES["dashboard_status"],
            "progress": DEFAULT_DELIVERABLES["dashboard_progress"],
            "timeline": DEFAULT_DELIVERABLES["dashboard_timeline"],
        },
        "runtime": {
            "job_registry": DEFAULT_DELIVERABLES["job_registry"],
            "gpu_registry": DEFAULT_DELIVERABLES["gpu_registry"],
            "backend_registry": DEFAULT_DELIVERABLES["backend_registry"],
            "sentinel_events": DEFAULT_DELIVERABLES["sentinel_events"],
        },
        "progress": {
            "completion_percent": PHASE_COMPLETION.get(starting_phase, 0),
            "current_agent": "orchestrator",
            "last_gate_result": "not_started",
            "active_blocker": "none",
            "next_action": f"prepare-phase-{starting_phase}",
            "active_backend": "local",
            "active_gpu": "unassigned",
            "allowed_return_phases": [],
            "suggested_return_phase": starting_phase,
        },
        "deliverables": dict(DEFAULT_DELIVERABLES),
        "starting_phase": starting_phase,
        "state_version": "2.0.0",
        "research_type": "ml_experiment",
        "user_config_inherited": {},
        "gpu_usage_history": [],
    }


def _build_default_substep_status() -> dict[str, Any]:
    """Build the default substep status structure."""
    return {
        "survey": {
            "literature_survey": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "idea_definition": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "research_plan": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
        },
        "pilot": {
            "problem_analysis": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "pilot_design": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "pilot_execution": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
        },
        "experiments": {
            "experiment_design": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "experiment_execution": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "results_analysis": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
        },
        "paper": {
            "paper_planning": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "paper_writing": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "citation_curation": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
        },
        "reflection": {
            "lessons_extraction": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
            "overlay_proposal": {
                "status": "pending",
                "review_result": "pending",
                "attempts": 0,
                "last_agent": None,
            },
        },
    }


def build_list_section(items: list[str], empty_message: str) -> str:
    """Build a markdown list section.

    Args:
        items: List of items to include.
        empty_message: Message to show if list is empty.

    Returns:
        Markdown formatted string.
    """
    if not items:
        return f"- {empty_message}"
    return "\n".join(f"- {item}" for item in items)


def resolve_deliverable_path(project_root: Path, state: dict[str, Any], key: str) -> Path:
    """Resolve a deliverable path from state.

    Args:
        project_root: Project root directory.
        state: Project state dictionary.
        key: Deliverable key.

    Returns:
        Resolved absolute path.
    """
    relative_value = state["deliverables"][key]
    return (project_root / relative_value).resolve()


def validate_deliverable_location(project_root: Path, relative_path: str, key: str) -> list[str]:
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
        errors.append(f"{key} must be project-relative, got absolute path: {relative_path}")
        return errors
    if ".." in relative.parts:
        errors.append(f"{key} must stay inside the project root, got: {relative_path}")
        return errors
    normalized = relative.as_posix()
    if not normalized.startswith(expected_prefix):
        errors.append(f"{key} must live under {expected_prefix}, got: {relative_path}")
    return errors


def ensure_complete_deliverables(state: dict[str, Any]) -> dict[str, Any]:
    """Ensure all required deliverables exist in the state.

    This function adds any missing deliverables from DEFAULT_DELIVERABLES
    to the state, ensuring backward compatibility with older project states.

    Args:
        state: The current state dictionary.

    Returns:
        The state with complete deliverables.
    """
    if "deliverables" not in state:
        state["deliverables"] = {}

    # Add any missing deliverables from defaults
    for key, default_path in DEFAULT_DELIVERABLES.items():
        if key not in state["deliverables"]:
            state["deliverables"][key] = default_path
            logger.info(f"Added missing deliverable: {key} = {default_path}")

    return state


def load_state(project_root: Path) -> dict[str, Any]:
    """Load project state from file.

    Args:
        project_root: Project root directory.

    Returns:
        Project state dictionary.
    """
    state = read_yaml(project_root / DEFAULT_DELIVERABLES["research_state"])
    schema_errors = validate_state_schema(state)
    if schema_errors:
        from exceptions import StateSchemaError  # type: ignore[import-untyped]

        raise StateSchemaError(
            f"research-state.yaml has schema errors in '{project_root}':\n"
            + "\n".join(f"  - {e}" for e in schema_errors)
        )
    config = load_project_config(project_root)
    state["loop_limits"] = dict(config["loop_limits"])
    state["language_policy"] = dict(config["languages"])

    # State version migration
    from state_migrator import migrate_state, needs_migration  # type: ignore[import-untyped]

    if needs_migration(state):
        state, migration_logs = migrate_state(state)
        for log in migration_logs:
            logger.info(log)
        # Save migrated state
        save_state(project_root, state)
        logger.info("State migration completed and saved")

    # Ensure all deliverables exist (backward compatibility)
    state = ensure_complete_deliverables(state)
    return state


def save_state(
    project_root: Path,
    state: dict[str, Any],
    previous_state: dict[str, Any] | None = None,
) -> None:
    """Save project state to file.

    Args:
        project_root: Project root directory.
        state: Project state dictionary.
        previous_state: Optional previous state for detecting gate status changes.
                        When provided, gate_decision events are appended to
                        sentinel_events.ndjson for any approval_status changes.
    """
    if previous_state is not None:
        _append_gate_audit_events(project_root, previous_state, state)
    write_yaml(project_root / DEFAULT_DELIVERABLES["research_state"], state)


def _append_gate_audit_events(
    project_root: Path,
    old_state: dict[str, Any],
    new_state: dict[str, Any],
) -> None:
    """Append gate_decision events to sentinel_events.ndjson when approval_status changes.

    Args:
        project_root: Project root directory.
        old_state: Previous state before the change.
        new_state: New state being saved.
    """
    old_approvals = old_state.get("approval_status", {})
    new_approvals = new_state.get("approval_status", {})
    changed = {
        gate: status for gate, status in new_approvals.items() if status != old_approvals.get(gate)
    }
    if not changed:
        return
    sentinel_path = project_root / DEFAULT_DELIVERABLES["sentinel_events"]
    sentinel_path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    with open(sentinel_path, "a", encoding="utf-8") as f:
        for gate, status in changed.items():
            event = json.dumps(
                {"type": "gate_decision", "gate": gate, "status": status, "timestamp": now},
                ensure_ascii=False,
            )
            f.write(event + "\n")


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
        f"Starting at '{phase}' skips phase '{p}' — "
        f"deliverables from that phase will NOT exist in this project."
        for p in skipped
    ]
    warnings.append(
        "If you have existing work from prior phases, add deliverables manually "
        "or use 'migrate-project' to import an existing project structure."
    )
    return warnings


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
            set(PHASE_SEQUENCE) | set(LEGACY_TO_SEMANTIC_PHASE) | {"archive", "06-archive"}
        )
        if phase not in valid_phases:
            errors.append(
                f"State 'current_phase' has unknown value: '{phase}'. "
                f"Expected one of: {sorted(valid_phases)}"
            )

    return errors


def load_project_config(project_root: Path) -> dict[str, Any]:
    """Load project configuration with defaults.

    Args:
        project_root: Project root directory.

    Returns:
        Merged configuration dictionary.
    """
    path = project_root / DEFAULT_DELIVERABLES["project_config"]
    if not path.exists():
        return json.loads(json.dumps(DEFAULT_RUNTIME_CONFIG))
    config = read_yaml(path)
    merged = json.loads(json.dumps(DEFAULT_RUNTIME_CONFIG))
    for key, value in config.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key].update(value)
        else:
            merged[key] = value
    return merged


def append_state_log(state: dict[str, Any], key: str, entry: dict[str, Any] | str) -> None:
    """Append an entry to a state log list.

    Args:
        state: Project state dictionary.
        key: Log key in state.
        entry: Entry to append (dict or string).
    """
    items = list(state.get(key, []))
    if isinstance(entry, str):
        items.append(entry)
    else:
        items.append(json.dumps(entry, ensure_ascii=False, sort_keys=True))
    state[key] = items


# ============================================================================
# ARIS Integration: Review State Management
# ============================================================================


def build_review_state(
    phase: str,
    round_num: int = 1,
    thread_id: str | None = None,
    status: str = "in_progress",
    last_score: float = 0.0,
    last_verdict: str = "not_started",
    pending_experiments: list[str] | None = None,
) -> dict[str, Any]:
    """Build a new REVIEW_STATE structure for ARIS auto-review-loop.

    Args:
        phase: Current phase name (e.g., "02-pilot-analysis").
        round_num: Current round number (1-based).
        thread_id: Codex MCP conversation thread ID for context continuity.
        status: Loop status ("in_progress", "completed", "stale").
        last_score: Last review score (1-10).
        last_verdict: Last verdict ("ready", "almost", "not_ready").
        pending_experiments: List of experiment IDs still running.

    Returns:
        REVIEW_STATE dictionary.
    """
    return {
        "phase": phase,
        "round": round_num,
        "max_rounds": MAX_REVIEW_ROUNDS,
        "threadId": thread_id,
        "status": status,
        "last_score": last_score,
        "last_verdict": last_verdict,
        "pending_experiments": pending_experiments or [],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def save_review_state(project_root: Path, review_state: dict[str, Any]) -> None:
    """Save REVIEW_STATE.json to project root.

    This file persists loop state across context compaction,
    allowing long-running auto-review-loops to resume.

    Args:
        project_root: Project root directory.
        review_state: Review state dictionary.
    """
    # Update timestamp on every save
    review_state["timestamp"] = datetime.now(timezone.utc).isoformat()
    path = project_root / REVIEW_STATE_FILENAME
    write_json(path, review_state)
    logger.info(
        f"Saved review state: round {review_state['round']}, status {review_state['status']}"
    )


def load_review_state(project_root: Path) -> dict[str, Any] | None:
    """Load REVIEW_STATE.json from project root.

    Args:
        project_root: Project root directory.

    Returns:
        Review state dictionary if file exists and is valid, None otherwise.
    """
    path = project_root / REVIEW_STATE_FILENAME
    if not path.exists():
        return None

    try:
        state = load_json(path, None)
        if state is None:
            return None

        # Check for stale state (older than 24 hours with in_progress status)
        if state.get("status") == "in_progress":
            timestamp_str = state.get("timestamp", "")
            if timestamp_str:
                try:
                    timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                    age_hours = (datetime.now(timezone.utc) - timestamp).total_seconds() / 3600
                    if age_hours > 24:
                        logger.warning(
                            f"Review state is stale ({age_hours:.1f} hours old), starting fresh"
                        )
                        return None
                except Exception as e:
                    logger.warning(f"Failed to parse timestamp: {e}")

        return state
    except Exception as e:
        logger.warning(f"Failed to load review state: {e}")
        return None


def clear_review_state(project_root: Path) -> None:
    """Remove REVIEW_STATE.json (call on completion).

    Args:
        project_root: Project root directory.
    """
    path = project_root / REVIEW_STATE_FILENAME
    if path.exists():
        path.unlink()
        logger.info("Cleared review state file")


def is_positive_assessment(score: float, verdict: str) -> bool:
    """Check if review result meets positive assessment threshold.

    Args:
        score: Review score (1-10).
        verdict: Review verdict string.

    Returns:
        True if assessment is positive (loop can stop).
    """
    if score >= POSITIVE_SCORE_THRESHOLD:
        verdict_lower = verdict.lower()
        if any(kw in verdict_lower for kw in POSITIVE_VERDICT_KEYWORDS):
            return True
    return False


def get_reviewer_config(project_root: Path) -> dict[str, Any]:
    """Get reviewer configuration from project config.

    Args:
        project_root: Project root directory.

    Returns:
        Reviewer configuration dictionary.
    """
    config = load_project_config(project_root)
    return config.get("reviewer", DEFAULT_REVIEWER_CONFIG)


def is_cross_model_review_enabled(project_root: Path) -> bool:
    """Check if cross-model review via Codex MCP is enabled.

    Args:
        project_root: Project root directory.

    Returns:
        True if cross-model review is enabled.
    """
    reviewer_config = get_reviewer_config(project_root)
    return reviewer_config.get("enabled", False)


# ============================================================================
# ARIS Integration: Idea State Management
# ============================================================================


def build_idea_state(
    direction: str,
    phase: str = "literature-survey",
    ideas_generated: int = 0,
    ideas_filtered: int = 0,
    pilots_run: int = 0,
    pilots_positive: int = 0,
    top_idea_id: str | None = None,
) -> dict[str, Any]:
    """Build a new IDEA_STATE structure for idea-discovery pipeline.

    Args:
        direction: Research direction string.
        phase: Current phase (literature-survey, idea-generation, novelty-check, pilot, review).
        ideas_generated: Total ideas generated.
        ideas_filtered: Ideas that passed filtering.
        pilots_run: Number of pilot experiments run.
        pilots_positive: Pilots with positive signal.
        top_idea_id: ID of the top-ranked idea.

    Returns:
        IDEA_STATE dictionary.
    """
    return {
        "direction": direction,
        "phase": phase,
        "ideas_generated": ideas_generated,
        "ideas_filtered": ideas_filtered,
        "pilots_run": pilots_run,
        "pilots_positive": pilots_positive,
        "top_idea_id": top_idea_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def save_idea_state(project_root: Path, idea_state: dict[str, Any]) -> None:
    """Save IDEA_STATE.json to project root.

    Args:
        project_root: Project root directory.
        idea_state: Idea state dictionary.
    """
    idea_state["timestamp"] = datetime.now(timezone.utc).isoformat()
    path = project_root / IDEA_STATE_FILENAME
    write_json(path, idea_state)
    logger.info(
        f"Saved idea state: phase {idea_state['phase']}, ideas {idea_state['ideas_generated']}"
    )


def load_idea_state(project_root: Path) -> dict[str, Any] | None:
    """Load IDEA_STATE.json from project root.

    Args:
        project_root: Project root directory.

    Returns:
        Idea state dictionary if file exists and is valid, None otherwise.
    """
    path = project_root / IDEA_STATE_FILENAME
    if not path.exists():
        return None

    try:
        state = load_json(path, None)
        if state is None:
            return None

        # Check for stale state (older than 7 days)
        timestamp_str = state.get("timestamp", "")
        if timestamp_str:
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                age_days = (datetime.now(timezone.utc) - timestamp).total_seconds() / 86400
                if age_days > 7:
                    logger.warning(f"Idea state is stale ({age_days:.1f} days old), starting fresh")
                    return None
            except Exception as e:
                logger.warning(f"Failed to parse timestamp: {e}")

        return state
    except Exception as e:
        logger.warning(f"Failed to load idea state: {e}")
        return None


def clear_idea_state(project_root: Path) -> None:
    """Remove IDEA_STATE.json (call on completion).

    Args:
        project_root: Project root directory.
    """
    path = project_root / IDEA_STATE_FILENAME
    if path.exists():
        path.unlink()
        logger.info("Cleared idea state file")


def load_aris_config(project_root: Path) -> dict[str, Any]:
    """Load ARIS configuration from project config.

    Args:
        project_root: Project root directory.

    Returns:
        ARIS configuration dictionary.
    """
    config = load_project_config(project_root)
    return config.get("aris", DEFAULT_ARIS_CONFIG)


def is_auto_proceed(project_root: Path) -> bool:
    """Check if auto-proceed mode is enabled.

    Args:
        project_root: Project root directory.

    Returns:
        True if auto-proceed is enabled.
    """
    aris_config = load_aris_config(project_root)
    return aris_config.get("auto_proceed", False)


# ============================================================================
# Deliverable validation
# ============================================================================


def is_unmodified_template(project_root: Path, state: dict[str, Any], relative_path: str) -> bool:
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
    expected = render_template_string(template_path.read_text(encoding="utf-8"), variables).strip()
    actual = target_path.read_text(encoding="utf-8").strip()
    return actual == expected


def validate_deliverable_content(project_root: Path, state: dict[str, Any], key: str) -> list[str]:
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
        return [f"{relative_path} is still the unedited template and does not satisfy the gate."]
    if not (project_root / relative_path).read_text(encoding="utf-8").strip():
        return [f"{relative_path} is empty and does not satisfy the gate."]
    return []


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


def validate_structured_signals(
    project_root: Path, state: dict[str, Any], phase_name: str
) -> list[str]:
    """Validate structured signals for gate validation.

    Args:
        project_root: Project root directory.
        state: Project state dictionary.
        phase_name: Phase name to validate.

    Returns:
        List of validation error messages.
    """
    errors: list[str] = []
    requirements = STRUCTURED_SIGNAL_REQUIREMENTS.get(phase_name, {})
    for deliverable_key, field_requirements in requirements.items():
        relative_path = state["deliverables"][deliverable_key]
        candidate = project_root / relative_path
        if not candidate.exists():
            errors.append(f"{relative_path} is missing; cannot read structured gate signals.")
            continue
        fields = parse_markdown_fields(candidate)
        for field_name, expected_values in field_requirements.items():
            actual = fields.get(field_name)
            normalized = normalize_signal_value(actual)
            if normalized not in expected_values:
                errors.append(
                    f"{relative_path} must set '{field_name}' to one of "
                    f"{sorted(expected_values)}, got {actual!r}."
                )
    return errors


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


# ============================================================================
# Phase transition helpers
# ============================================================================


def shell_join(parts: list[str]) -> str:
    """Join shell command parts with proper quoting.

    Args:
        parts: List of command parts.

    Returns:
        Shell-safe command string.
    """
    return " ".join(shlex.quote(part) for part in parts)


def allowed_return_phases(phase_name: str) -> list[str]:
    """Get list of phases that can be returned to from a given phase.

    Args:
        phase_name: Current phase name.

    Returns:
        List of valid return phase names.
    """
    if phase_name not in PHASE_SEQUENCE:
        return []
    index = PHASE_SEQUENCE.index(phase_name)
    return list(PHASE_SEQUENCE[: index + 1])


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
    state["progress"]["allowed_return_phases"] = allowed_return_phases(phase_name)
    state["progress"]["suggested_return_phase"] = phase_name


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


# ============================================================================
# Logging setup
# ============================================================================


def setup_logging(level: int = logging.INFO, log_file: Path | None = None) -> None:
    """Configure logging for the orchestrator.

    Args:
        level: Logging level (default: INFO).
        log_file: Optional file path to write logs.
    """
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
# Project structure validation
# ============================================================================


def ensure_project_structure(project_root: Path, create_if_missing: bool = True) -> bool:
    """Ensure project directory structure is valid.

    This function checks and optionally creates the required directory structure.
    Every script should call this at startup to guarantee consistent structure.

    Args:
        project_root: Path to the project root directory
        create_if_missing: If True, create missing directories automatically

    Returns:
        True if structure is valid (all directories exist)
        False if structure is invalid and create_if_missing is False
    """
    # Resolve and validate project_root path
    project_root = project_root.resolve()
    if not project_root.exists():
        if create_if_missing:
            project_root.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created project root: {project_root}")
        else:
            logger.error(f"Project root does not exist: {project_root}")
            return False

    # Track missing directories
    missing_dirs: list[str] = []

    for dir_path in REQUIRED_DIRECTORIES:
        full_path = project_root / dir_path
        if not full_path.exists():
            missing_dirs.append(dir_path)

    # Create missing directories if requested
    if missing_dirs:
        if create_if_missing:
            for dir_path in missing_dirs:
                full_path = project_root / dir_path
                full_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {dir_path}")
        else:
            logger.warning(f"Missing directories: {missing_dirs}")
            return False

    # Check if state file exists (log info if not, but don't fail)
    state_file = project_root / DEFAULT_DELIVERABLES["research_state"]
    if not state_file.exists():
        logger.info(f"State file not found (expected): {state_file}")

    return True


# ============================================================================
# GitMem Integration: Lightweight Version Control for Agent Edits
# ============================================================================


def _run_git_command(project_root: Path, args: list[str], check: bool = True) -> str:
    """Run a git command in the GitMem repository.

    Args:
        project_root: Project root directory.
        args: Git command arguments (without 'git' prefix).
        check: If True, raise exception on non-zero exit.

    Returns:
        Command stdout.

    Raises:
        RuntimeError: If git command fails and check=True.
    """
    gitmem_path = project_root / GITMEM_DIR
    cmd = ["git", "-C", str(gitmem_path)] + args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check,
            timeout=30,
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Git command timed out: {' '.join(args)}")
    except subprocess.CalledProcessError as e:
        if check:
            raise RuntimeError(f"Git command failed: {e.stderr}") from e
        return ""


def gitmem_is_initialized(project_root: Path) -> bool:
    """Check if GitMem is initialized for the project.

    Args:
        project_root: Project root directory.

    Returns:
        True if GitMem is initialized.
    """
    gitmem_path = project_root / GITMEM_DIR
    return (gitmem_path / ".git").exists()


def gitmem_init(project_root: Path) -> None:
    """Initialize GitMem for a project.

    Creates a .gitmem directory with a separate git repository
    for tracking agent-generated document changes.

    Args:
        project_root: Project root directory.
    """
    gitmem_path = project_root / GITMEM_DIR

    # Skip if already initialized
    if gitmem_is_initialized(project_root):
        logger.info(f"GitMem already initialized at {gitmem_path}")
        return

    # Create .gitmem directory
    gitmem_path.mkdir(parents=True, exist_ok=True)

    # Initialize git repo
    _run_git_command(project_root, ["init"])

    # Configure git user
    _run_git_command(project_root, ["config", "user.name", "GitMem"])
    _run_git_command(project_root, ["config", "user.email", "gitmem@orchestrator"])

    # Create .gitignore in .gitmem to NOT ignore tracked directories
    # We want to track docs/, paper/, code/, agents/ inside .gitmem
    gitignore_content = """# GitMem tracks these directories
!docs/
!paper/
!code/
!agents/
"""
    (gitmem_path / ".gitignore").write_text(gitignore_content.strip(), encoding="utf-8")

    # Create README in .gitmem to explain the directory
    readme_content = """# GitMem Version Tracking

This directory contains a git repository that tracks changes to files in:
- docs/
- paper/
- code/
- agents/

Files are mirrored here with the same directory structure for version tracking.
This keeps the main project's git history clean while enabling iterative refinement.

Use the gitmem_* functions in orchestrator_common.py to interact with this repository.
"""
    (gitmem_path / "README.md").write_text(readme_content, encoding="utf-8")

    # Create initial commit
    _run_git_command(project_root, ["add", ".gitignore", "README.md"])
    _run_git_command(project_root, ["commit", "-m", "GitMem initialized"])

    # Update main project's .gitignore to ignore .gitmem
    main_gitignore = project_root / ".gitignore"
    if main_gitignore.exists():
        content = main_gitignore.read_text(encoding="utf-8")
        if GITMEM_DIR not in content:
            main_gitignore.write_text(
                content + f"\n# GitMem version tracking\n{GITMEM_DIR}/\n",
                encoding="utf-8",
            )
    else:
        main_gitignore.write_text(f"# GitMem version tracking\n{GITMEM_DIR}/\n", encoding="utf-8")

    logger.info(f"Initialized GitMem at {gitmem_path}")


def gitmem_commit(project_root: Path, file_path: str, message: str) -> str:
    """Commit a file change to GitMem history.

    Args:
        project_root: Project root directory.
        file_path: Relative path to the file (from project root).
        message: Commit message.

    Returns:
        Commit hash.

    Raises:
        ValueError: If GitMem is not initialized.
    """
    if not gitmem_is_initialized(project_root):
        raise ValueError("GitMem not initialized. Call gitmem_init() first.")

    # Normalize the file path
    file_path = Path(file_path).as_posix()

    # Check if file is in tracked directories
    is_tracked = any(file_path.startswith(tracked) for tracked in GITMEM_TRACKED_DIRS)
    if not is_tracked:
        logger.warning(f"File {file_path} is not in GitMem tracked directories")

    # Copy the file to .gitmem for tracking
    source_path = project_root / file_path
    gitmem_path = project_root / GITMEM_DIR

    if not source_path.exists():
        raise ValueError(f"File does not exist: {file_path}")

    # Create the same directory structure in .gitmem
    gitmem_file_path = gitmem_path / file_path
    gitmem_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Copy file content
    gitmem_file_path.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")

    # Stage the file in .gitmem repo
    _run_git_command(project_root, ["add", file_path])

    # Check if there are changes to commit
    status = _run_git_command(project_root, ["status", "--porcelain"])
    if not status:
        logger.info(f"No changes to commit for {file_path}")
        # Get current HEAD hash
        return _run_git_command(project_root, ["rev-parse", "HEAD"])

    _run_git_command(project_root, ["commit", "-m", message])

    # Get commit hash
    commit_hash = _run_git_command(project_root, ["rev-parse", "HEAD"])
    logger.info(f"GitMem commit: {commit_hash[:8]} - {message}")

    return commit_hash


def gitmem_checkpoint(project_root: Path, name: str) -> None:
    """Create a named checkpoint (annotated tag).

    Checkpoints mark stable states for easy rollback.

    Args:
        project_root: Project root directory.
        name: Checkpoint name (e.g., "survey-1.1-approved").

    Raises:
        ValueError: If GitMem is not initialized.
    """
    if not gitmem_is_initialized(project_root):
        raise ValueError("GitMem not initialized. Call gitmem_init() first.")

    # Create annotated tag
    timestamp = datetime.now(timezone.utc).isoformat()
    _run_git_command(
        project_root,
        ["tag", "-a", name, "-m", f"Checkpoint: {name} at {timestamp}"],
    )

    logger.info(f"GitMem checkpoint created: {name}")


def gitmem_list_tags(project_root: Path) -> list[str]:
    """List all tags (checkpoints) in the GitMem repository.

    Args:
        project_root: Project root directory.

    Returns:
        List of tag names, or empty list if GitMem not initialized.
    """
    if not gitmem_is_initialized(project_root):
        return []

    tags_output = _run_git_command(project_root, ["tag", "-l"], check=False)
    if not tags_output:
        return []
    return [tag.strip() for tag in tags_output.split("\n") if tag.strip()]


def gitmem_check_loop(project_root: Path, file_path: str) -> bool:
    """Check if a file is in an edit loop.

    A file is considered in a loop if it has 5+ consecutive changes
    without a checkpoint.

    Args:
        project_root: Project root directory.
        file_path: Relative path to the file.

    Returns:
        True if file appears to be in an edit loop.
    """
    loop_info = gitmem_get_loop_info(project_root, file_path)

    if loop_info["in_loop"]:
        logger.warning(
            f"Loop detected: {file_path} has {loop_info['change_count']} "
            f"changes without checkpoint"
        )

    return loop_info["in_loop"]


def gitmem_get_loop_info(project_root: Path, file_path: str) -> dict[str, Any]:
    """Get detailed loop information for a file.

    Args:
        project_root: Project root directory.
        file_path: Relative path to the file.

    Returns:
        Dictionary with 'in_loop', 'change_count', and 'last_checkpoint' keys.
    """
    result: dict[str, Any] = {
        "in_loop": False,
        "change_count": 0,
        "last_checkpoint": None,
    }

    if not gitmem_is_initialized(project_root):
        return result

    # Get log for this file
    log_output = _run_git_command(
        project_root,
        ["log", "--oneline", "--follow", "--", file_path],
        check=False,
    )

    if not log_output:
        return result

    commits = log_output.split("\n")
    result["change_count"] = len(commits)

    # Check if any commit is tagged (checkpoint)
    for commit_line in commits[:10]:  # Check last 10 commits
        commit_hash = commit_line.split()[0] if commit_line else ""
        if commit_hash:
            # Check if this commit has tags
            tags_output = _run_git_command(
                project_root,
                ["tag", "--points-at", commit_hash],
                check=False,
            )
            if tags_output:
                result["last_checkpoint"] = tags_output.split("\n")[0]
                break

    # Determine if in loop
    result["in_loop"] = (
        result["change_count"] >= GITMEM_LOOP_THRESHOLD and result["last_checkpoint"] is None
    )

    return result


def gitmem_history(project_root: Path, file_path: str, limit: int = 20) -> list[dict[str, str]]:
    """Get commit history for a file.

    Args:
        project_root: Project root directory.
        file_path: Relative path to the file.
        limit: Maximum number of commits to return.

    Returns:
        List of commit info dictionaries.
    """
    if not gitmem_is_initialized(project_root):
        return []

    log_format = "--format=%H|%s|%ci"
    log_output = _run_git_command(
        project_root,
        ["log", log_format, f"-{limit}", "--follow", "--", file_path],
        check=False,
    )

    if not log_output:
        return []

    history: list[dict[str, str]] = []
    for line in log_output.split("\n"):
        if "|" in line:
            parts = line.split("|", 2)
            if len(parts) >= 3:
                history.append(
                    {
                        "hash": parts[0],
                        "message": parts[1],
                        "date": parts[2],
                    }
                )

    return history


def gitmem_diff(
    project_root: Path,
    file_path: str,
    from_rev: str = "HEAD~1",
    to_rev: str = "HEAD",
) -> str:
    """Compare versions of a file.

    Args:
        project_root: Project root directory.
        file_path: Relative path to the file.
        from_rev: Source revision (default: HEAD~1).
        to_rev: Target revision (default: HEAD).

    Returns:
        Diff output as string.
    """
    if not gitmem_is_initialized(project_root):
        return "GitMem not initialized"

    file_path = Path(file_path).as_posix()

    diff_output = _run_git_command(
        project_root,
        ["diff", from_rev, to_rev, "--", file_path],
        check=False,
    )

    return diff_output


def gitmem_rollback(
    project_root: Path,
    file_path: str,
    to_rev: str = "HEAD~1",
) -> bool:
    """Rollback a file to a previous version.

    Creates a new commit with the rollback (never rewrites history).

    Args:
        project_root: Project root directory.
        file_path: Relative path to the file.
        to_rev: Target revision (default: HEAD~1).

    Returns:
        True if rollback succeeded.
    """
    if not gitmem_is_initialized(project_root):
        logger.warning("GitMem not initialized, cannot rollback")
        return False

    file_path = Path(file_path).as_posix()

    # Get the file content from the target revision
    try:
        content = _run_git_command(
            project_root,
            ["show", f"{to_rev}:{file_path}"],
            check=True,
        )
    except RuntimeError as e:
        logger.error(f"Cannot find revision {to_rev}: {e}")
        return False

    # Write the content back
    source_path = project_root / file_path
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text(content, encoding="utf-8")

    # Create a commit for the rollback
    gitmem_commit(project_root, file_path, f"Rollback {file_path} to {to_rev}")

    logger.info(f"Rolled back {file_path} to {to_rev}")
    return True


# ============================================================================
# Public API (backward compatibility)
# ============================================================================

__all__ = [
    # Version constants (from constants.version)
    "SYSTEM_VERSION",
    "SYSTEM_VERSION_NAME",
    "VERSION_HISTORY",
    # Path constants (from constants.paths)
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
    # Phase constants (from constants.phases)
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
    # Phase helper functions (from constants.phases)
    "normalize_phase_name",
    "get_legacy_phase_name",
    "get_all_phase_aliases",
    "get_phase_agents",
    # YAML utilities (from utils.yaml_utils)
    "yaml_dump",
    "yaml_load",
    "read_yaml",
    "write_yaml",
    # Path utilities (from utils.path_utils)
    "normalize_relative_path",
    # Text utilities (from utils.text_utils)
    "slugify",
    # Template utilities (from utils.template_utils)
    "build_template_variables",
    "render_template_string",
    "render_template_tree",
    "write_text_if_needed",
    # Local constants
    "DEFAULT_LANGUAGE_POLICY",
    "DEFAULT_REVIEWER_CONFIG",
    "REVIEW_STATE_FILENAME",
    "MAX_REVIEW_ROUNDS",
    "POSITIVE_SCORE_THRESHOLD",
    "POSITIVE_VERDICT_KEYWORDS",
    "DEFAULT_ARIS_CONFIG",
    "IDEA_STATE_FILENAME",
    "DEFAULT_RUNTIME_CONFIG",
    "MARKDOWN_FIELD_RE",
    "GITMEM_DIR",
    "GITMEM_LOOP_THRESHOLD",
    "GITMEM_TRACKED_DIRS",
    # JSON utilities
    "load_json",
    "write_json",
    # Platform and client detection
    "detect_platform",
    "select_client_template",
    "detect_client_profile",
    "build_client_instruction_text",
    # State management
    "detect_client_init_artifacts",
    "build_state",
    "build_list_section",
    "resolve_deliverable_path",
    "validate_deliverable_location",
    "ensure_complete_deliverables",
    "load_state",
    "save_state",
    "warn_starting_phase_prerequisites",
    "validate_state_schema",
    "load_project_config",
    "append_state_log",
    # ARIS Review State
    "build_review_state",
    "save_review_state",
    "load_review_state",
    "clear_review_state",
    "is_positive_assessment",
    "get_reviewer_config",
    "is_cross_model_review_enabled",
    # ARIS Idea State
    "build_idea_state",
    "save_idea_state",
    "load_idea_state",
    "clear_idea_state",
    "load_aris_config",
    "is_auto_proceed",
    # Deliverable validation
    "is_unmodified_template",
    "validate_deliverable_content",
    "parse_markdown_fields",
    "validate_structured_signals",
    "normalize_signal_value",
    # Phase transition helpers
    "shell_join",
    "allowed_return_phases",
    "reset_state_for_phase",
    "suggest_return_phase",
    # Logging
    "setup_logging",
    # Project structure
    "ensure_project_structure",
    # GitMem functions
    "gitmem_is_initialized",
    "gitmem_init",
    "gitmem_commit",
    "gitmem_checkpoint",
    "gitmem_list_tags",
    "gitmem_check_loop",
    "gitmem_get_loop_info",
    "gitmem_history",
    "gitmem_diff",
    "gitmem_rollback",
]
