#!/usr/bin/env python3
"""State version migration system for AI Research Orchestrator.

This module provides automatic migration of research state files between
different versions, ensuring backward compatibility as the state schema evolves.

Migration Chain:
    1.0.0 -> 1.1.0 -> 1.12.0 -> 2.0.0

Usage:
    from state_migrator import migrate_state, needs_migration

    if needs_migration(state):
        state, logs = migrate_state(state)
        save_state(project_root, state)
"""

from __future__ import annotations

import logging
from typing import Any, Callable

# Configure module logger
logger = logging.getLogger(__name__)

# Current state version
CURRENT_STATE_VERSION = "2.0.0"

# State version history with descriptions
STATE_VERSIONS: dict[str, str] = {
    "1.0.0": "Initial state structure",
    "1.1.0": "Added substep_status",
    "1.12.0": "ARIS integration (review state, loop tracking)",
    "2.0.0": "User config integration, GPU history, research type",
}

# Version order for migration chain
VERSION_ORDER = ["1.0.0", "1.1.0", "1.12.0", "2.0.0"]

# Migration function type
MigrationFunc = Callable[[dict[str, Any]], tuple[dict[str, Any], str]]


def get_state_version(state: dict[str, Any]) -> str:
    """Get the version from a state dictionary.

    Args:
        state: The state dictionary to check.

    Returns:
        The state version string, or "1.0.0" if no version is present or None.
    """
    version = state.get("state_version", "1.0.0")
    return version if version is not None else "1.0.0"


def needs_migration(state: dict[str, Any]) -> bool:
    """Check if a state dictionary needs migration.

    Args:
        state: The state dictionary to check.

    Returns:
        True if the state version is older than the current version.
    """
    current = get_state_version(state)
    return current != CURRENT_STATE_VERSION


def _deep_copy_state(state: dict[str, Any]) -> dict[str, Any]:
    """Create a deep copy of the state dictionary.

    Uses JSON serialization for a simple deep copy implementation.

    Args:
        state: The state dictionary to copy.

    Returns:
        A deep copy of the state dictionary.
    """
    import json

    return json.loads(json.dumps(state))


def migrate_1_0_to_1_1(state: dict[str, Any]) -> tuple[dict[str, Any], str]:
    """Migrate state from version 1.0.0 to 1.1.0.

    Changes:
        - Add substep_status field with default structure for all phases

    Args:
        state: The state dictionary to migrate.

    Returns:
        Tuple of (migrated state, migration log message).
    """
    migrated = _deep_copy_state(state)

    # Default substep status structure for each phase
    default_substep = {
        "status": "pending",
        "review_result": "pending",
        "attempts": 0,
        "last_agent": None,
    }

    # Build substep_status if not present
    if "substep_status" not in migrated:
        migrated["substep_status"] = {
            "survey": {
                "literature_survey": dict(default_substep),
                "idea_definition": dict(default_substep),
                "research_plan": dict(default_substep),
            },
            "pilot": {
                "problem_analysis": dict(default_substep),
                "pilot_design": dict(default_substep),
                "pilot_execution": dict(default_substep),
            },
            "experiments": {
                "experiment_design": dict(default_substep),
                "experiment_execution": dict(default_substep),
                "results_analysis": dict(default_substep),
            },
            "paper": {
                "paper_planning": dict(default_substep),
                "paper_writing": dict(default_substep),
                "citation_curation": dict(default_substep),
            },
            "reflection": {
                "lessons_extraction": dict(default_substep),
                "overlay_proposal": dict(default_substep),
            },
        }

    # Update version
    migrated["state_version"] = "1.1.0"

    log = "Migrated from 1.0.0 to 1.1.0: Added substep_status field"
    logger.info(log)
    return migrated, log


def migrate_1_1_to_1_12(state: dict[str, Any]) -> tuple[dict[str, Any], str]:
    """Migrate state from version 1.1.0 to 1.12.0.

    Changes:
        - Ensure ARIS integration fields exist (REVIEW_STATE support)
        - Add loop tracking fields if missing
        - Add system_version field if missing

    Args:
        state: The state dictionary to migrate.

    Returns:
        Tuple of (migrated state, migration log message).
    """
    migrated = _deep_copy_state(state)

    changes = []

    # Ensure system_version exists
    if "system_version" not in migrated:
        migrated["system_version"] = "1.12.0"
        changes.append("system_version")

    # Ensure inner_loops exists
    if "inner_loops" not in migrated:
        migrated["inner_loops"] = {
            "survey_critic": 0,
            "pilot_code_adviser": 0,
            "experiment_code_adviser": 0,
            "writer_reviewer": 0,
            "reflector_curator": 0,
        }
        changes.append("inner_loops")

    # Ensure loop_counts exists
    if "loop_counts" not in migrated:
        migrated["loop_counts"] = {
            "survey_critic": 0,
            "pilot_code_adviser": 0,
            "experiment_code_adviser": 0,
            "writer_reviewer": 0,
            "reflector_curator": 0,
        }
        changes.append("loop_counts")

    # Ensure outer_loop exists
    if "outer_loop" not in migrated:
        migrated["outer_loop"] = 0
        changes.append("outer_loop")

    # Ensure loop_limits exists
    if "loop_limits" not in migrated:
        migrated["loop_limits"] = {
            "survey_critic": 5,
            "pilot_code_adviser": 5,
            "experiment_code_adviser": 5,
            "writer_reviewer": 5,
            "reflector_curator": 3,
        }
        changes.append("loop_limits")

    # Ensure recovery_status exists
    if "recovery_status" not in migrated:
        migrated["recovery_status"] = "idle"
        changes.append("recovery_status")

    # Ensure active_jobs exists
    if "active_jobs" not in migrated:
        migrated["active_jobs"] = []
        changes.append("active_jobs")

    # Update version
    migrated["state_version"] = "1.12.0"

    log = f"Migrated from 1.1.0 to 1.12.0: Added ARIS fields ({', '.join(changes)})"
    logger.info(log)
    return migrated, log


def migrate_1_12_to_2_0(state: dict[str, Any]) -> tuple[dict[str, Any], str]:
    """Migrate state from version 1.12.0 to 2.0.0.

    Changes:
        - Add research_type field (default: "ml_experiment")
        - Add user_config_inherited field (default: {})
        - Add gpu_usage_history field (default: [])
        - Update state version to 2.0.0

    Args:
        state: The state dictionary to migrate.

    Returns:
        Tuple of (migrated state, migration log message).
    """
    migrated = _deep_copy_state(state)

    changes = []

    # Add research_type field
    if "research_type" not in migrated:
        migrated["research_type"] = "ml_experiment"
        changes.append("research_type")

    # Add user_config_inherited field
    if "user_config_inherited" not in migrated:
        migrated["user_config_inherited"] = {}
        changes.append("user_config_inherited")

    # Add gpu_usage_history field
    if "gpu_usage_history" not in migrated:
        migrated["gpu_usage_history"] = []
        changes.append("gpu_usage_history")

    # Update version
    migrated["state_version"] = "2.0.0"

    log = f"Migrated from 1.12.0 to 2.0.0: Added fields ({', '.join(changes)})"
    logger.info(log)
    return migrated, log


# Migration function mapping
MIGRATIONS: dict[tuple[str, str], MigrationFunc] = {
    ("1.0.0", "1.1.0"): migrate_1_0_to_1_1,
    ("1.1.0", "1.12.0"): migrate_1_1_to_1_12,
    ("1.12.0", "2.0.0"): migrate_1_12_to_2_0,
}


def get_migration_path(from_version: str, to_version: str) -> list[tuple[str, str]]:
    """Determine the migration path between two versions.

    Args:
        from_version: Starting version.
        to_version: Target version.

    Returns:
        List of (from_version, to_version) tuples representing migration steps.

    Raises:
        ValueError: If no migration path exists between the versions.
    """
    try:
        from_idx = VERSION_ORDER.index(from_version)
        to_idx = VERSION_ORDER.index(to_version)
    except ValueError as e:
        raise ValueError(f"Unknown version in migration path: {e}") from e

    if from_idx > to_idx:
        raise ValueError(
            f"Cannot migrate backwards from {from_version} to {to_version}"
        )

    path = []
    for i in range(from_idx, to_idx):
        path.append((VERSION_ORDER[i], VERSION_ORDER[i + 1]))

    return path


def migrate_state(state: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Execute state migration to the current version.

    This function applies all necessary migrations in sequence to bring
    the state up to the current version.

    Args:
        state: The state dictionary to migrate.

    Returns:
        Tuple of (migrated state, list of migration log messages).

    Raises:
        ValueError: If migration fails or no path exists.
    """
    current_version = get_state_version(state)

    # Already at current version
    if current_version == CURRENT_STATE_VERSION:
        return state, []

    # Get migration path
    try:
        migration_path = get_migration_path(current_version, CURRENT_STATE_VERSION)
    except ValueError as e:
        logger.error(f"Migration path error: {e}")
        raise

    migrated = _deep_copy_state(state)
    logs: list[str] = []

    # Apply migrations in sequence
    for from_ver, to_ver in migration_path:
        migration_func = MIGRATIONS.get((from_ver, to_ver))
        if migration_func is None:
            raise ValueError(f"No migration function for {from_ver} -> {to_ver}")

        logger.info(f"Applying migration: {from_ver} -> {to_ver}")
        migrated, log = migration_func(migrated)
        logs.append(log)

        # Verify migration updated the version
        actual_version = get_state_version(migrated)
        if actual_version != to_ver:
            raise ValueError(
                f"Migration {from_ver} -> {to_ver} failed: "
                f"version is {actual_version}, expected {to_ver}"
            )

    logger.info(f"Migration complete: {current_version} -> {CURRENT_STATE_VERSION}")
    return migrated, logs


def validate_state_version(state: dict[str, Any]) -> bool:
    """Validate that the state version is supported.

    Args:
        state: The state dictionary to validate.

    Returns:
        True if the state version is valid and supported.
    """
    version = get_state_version(state)
    return version in VERSION_ORDER


def get_migration_info(state: dict[str, Any]) -> dict[str, Any]:
    """Get information about the migration status of a state.

    Args:
        state: The state dictionary to check.

    Returns:
        Dictionary with migration information including:
        - current_version: Current state version
        - target_version: Target version (CURRENT_STATE_VERSION)
        - needs_migration: Whether migration is needed
        - migration_steps: Number of migration steps required
        - migration_path: List of migration steps
    """
    current = get_state_version(state)
    needs = needs_migration(state)

    result: dict[str, Any] = {
        "current_version": current,
        "target_version": CURRENT_STATE_VERSION,
        "needs_migration": needs,
        "migration_steps": 0,
        "migration_path": [],
        "is_valid_version": current in VERSION_ORDER,
    }

    if needs:
        if current not in VERSION_ORDER:
            result["error"] = f"Unknown version: {current}"
        else:
            try:
                path = get_migration_path(current, CURRENT_STATE_VERSION)
                result["migration_steps"] = len(path)
                result["migration_path"] = [
                    f"{frm} -> {to}" for frm, to in path
                ]
            except ValueError as e:
                result["error"] = str(e)

    return result