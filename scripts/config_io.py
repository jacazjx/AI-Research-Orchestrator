#!/usr/bin/env python3
"""Configuration I/O for AI Research Orchestrator.

Provides get_config, set_config, and validate_config_value.
All interactive logic and display formatting is handled by the model.

Usage:
    python3 scripts/config_io.py --project-root /path --action get --key max-loops
    python3 scripts/config_io.py --project-root /path --action set --key max-loops --value 5
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import local modules
from constants import DEFAULT_DELIVERABLES, PHASE_SEQUENCE  # noqa: E402

from orchestrator_common import (  # noqa: E402
    DEFAULT_LANGUAGE_POLICY,
    DEFAULT_LOOP_LIMITS,
    read_yaml,
    write_yaml,
)

# Configure module logger
logger = logging.getLogger(__name__)

# Configuration schema
PROJECT_CONFIG_KEYS = {
    "idea": {
        "type": "string",
        "description": "Research idea",
        "state_key": "topic",
    },
    "research-type": {
        "type": "enum",
        "values": ["ml_experiment", "theory", "survey", "applied"],
        "description": "Research type",
        "state_key": "research_type",
    },
    "max-loops": {
        "type": "int",
        "min": 1,
        "max": 10,
        "description": "Maximum loop count per phase",
        "config_key": "loop_limits",
    },
    "language": {
        "type": "string",
        "description": "Language settings (format: process_lang,paper_lang)",
        "state_key": "language_policy",
    },
    "starting-phase": {
        "type": "enum",
        "values": list(PHASE_SEQUENCE),
        "description": "Starting phase",
        "state_key": "starting_phase",
    },
    "gpu": {
        "type": "string",
        "description": "GPU ID",
        "state_key": "progress.active_gpu",
    },
}

USER_CONFIG_KEYS = {
    "author.name": {
        "type": "string",
        "description": "Author name",
        "config_key": "author.name",
    },
    "author.email": {
        "type": "string",
        "description": "Author email",
        "config_key": "author.email",
    },
    "author.institution": {
        "type": "string",
        "description": "Institution",
        "config_key": "author.institution",
    },
    "preferences.venue": {
        "type": "string",
        "description": "Default venue",
        "config_key": "preferences.default_venue",
    },
}


def _load_project_state(project_root: Path) -> dict[str, Any]:
    """Load project state from research-state.yaml."""
    state_path = project_root / DEFAULT_DELIVERABLES["research_state"]
    if not state_path.exists():
        return {}
    state = read_yaml(state_path)
    return state if state else {}


def _save_project_state(project_root: Path, state: dict[str, Any]) -> None:
    """Save project state to research-state.yaml."""
    state_path = project_root / DEFAULT_DELIVERABLES["research_state"]
    state_path.parent.mkdir(parents=True, exist_ok=True)
    write_yaml(state_path, state)


def _load_project_config(project_root: Path) -> dict[str, Any]:
    """Load project configuration from orchestrator-config.yaml."""
    config_path = project_root / DEFAULT_DELIVERABLES["project_config"]
    if not config_path.exists():
        return {}
    config = read_yaml(config_path)
    return config if config else {}


def _save_project_config(project_root: Path, config: dict[str, Any]) -> None:
    """Save project configuration to orchestrator-config.yaml."""
    config_path = project_root / DEFAULT_DELIVERABLES["project_config"]
    config_path.parent.mkdir(parents=True, exist_ok=True)
    write_yaml(config_path, config)


def _get_user_config_path() -> Path:
    return Path.home() / ".autoresearch" / "user-config.yaml"


def _load_user_config() -> dict[str, Any]:
    config_path = _get_user_config_path()
    if not config_path.exists():
        return {}
    config = read_yaml(config_path)
    return config if config else {}


def _save_user_config(config: dict[str, Any]) -> None:
    config_path = _get_user_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    write_yaml(config_path, config)


def _get_nested_value(data: dict[str, Any], key: str) -> Any:
    """Get a nested value from a dictionary using dot notation."""
    keys = key.split(".")
    current = data
    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            return None
    return current


def _set_nested_value(data: dict[str, Any], key: str, value: Any) -> dict[str, Any]:
    """Set a nested value in a dictionary using dot notation."""
    result = dict(data)
    keys = key.split(".")
    if len(keys) == 1:
        result[keys[0]] = value
    else:
        current = result
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
    return result


def validate_config_value(
    key: str, value: str, schema: dict[str, Any] | None = None
) -> tuple[bool, str, Any]:
    """Validate a configuration value against its schema.

    Args:
        key: Configuration key.
        value: Configuration value as string.
        schema: Configuration schema (auto-detected if None).

    Returns:
        Tuple of (is_valid, error_message, parsed_value).
    """
    if schema is None:
        schema = PROJECT_CONFIG_KEYS.get(key) or USER_CONFIG_KEYS.get(key) or {}
    value_type = schema.get("type", "string")

    try:
        if value_type == "int":
            min_val = schema.get("min")
            max_val = schema.get("max")
            parsed = int(value)
            if min_val is not None and parsed < min_val:
                return False, f"Value must be >= {min_val}", None
            if max_val is not None and parsed > max_val:
                return False, f"Value must be <= {max_val}", None
            return True, "", parsed

        elif value_type == "enum":
            values = schema.get("values", [])
            if value not in values:
                return False, f"Valid values: {', '.join(values)}", None
            return True, "", value

        elif value_type == "string":
            if key == "language":
                parts = value.split(",")
                if len(parts) != 2:
                    return False, "Format: process_lang,paper_lang (e.g. zh-CN,en-US)", None
            return True, "", value

        else:
            return True, "", value

    except ValueError as e:
        return False, f"Type error: {e}", None


def get_config(project_root: Path, key: str) -> dict[str, Any]:
    """Get a configuration value.

    Args:
        project_root: Project root directory.
        key: Configuration key.

    Returns:
        Dict with key, value, scope, and description.
    """
    # Check project config keys first
    if key in PROJECT_CONFIG_KEYS:
        schema = PROJECT_CONFIG_KEYS[key]
        state = _load_project_state(project_root)
        state_key = schema.get("state_key")
        config_key = schema.get("config_key")

        value = None
        if state_key:
            value = _get_nested_value(state, state_key)
        elif config_key == "loop_limits":
            value = state.get("loop_limits", DEFAULT_LOOP_LIMITS)

        return {
            "key": key,
            "value": value,
            "scope": "project",
            "description": schema.get("description", ""),
        }

    # Check user config keys
    if key in USER_CONFIG_KEYS:
        schema = USER_CONFIG_KEYS[key]
        user_config = _load_user_config()
        config_key = schema.get("config_key", key)
        value = _get_nested_value(user_config, config_key)
        return {
            "key": key,
            "value": value,
            "scope": "user",
            "description": schema.get("description", ""),
        }

    return {"key": key, "value": None, "scope": "unknown", "error": f"Unknown key: {key}"}


def set_config(project_root: Path, key: str, value: str) -> dict[str, Any]:
    """Set a configuration value.

    Args:
        project_root: Project root directory.
        key: Configuration key.
        value: Configuration value as string.

    Returns:
        Dict with key, value, scope, and message.
    """
    # Determine scope
    if key.startswith("author.") or key.startswith("preferences.") or key in USER_CONFIG_KEYS:
        schema = USER_CONFIG_KEYS.get(key, {})
        if not schema:
            return {"key": key, "error": f"Unknown user config key: {key}"}

        is_valid, error, parsed_value = validate_config_value(key, value, schema)
        if not is_valid:
            return {"key": key, "error": error}

        user_config = _load_user_config()
        config_key = schema.get("config_key", key)
        updated = _set_nested_value(user_config, config_key, parsed_value)
        _save_user_config(updated)
        return {"key": key, "value": parsed_value, "scope": "user", "message": f"Updated {key}"}

    else:
        schema = PROJECT_CONFIG_KEYS.get(key, {})
        if not schema:
            return {"key": key, "error": f"Unknown project config key: {key}"}

        is_valid, error, parsed_value = validate_config_value(key, value, schema)
        if not is_valid:
            return {"key": key, "error": error}

        state = _load_project_state(project_root)
        project_config = _load_project_config(project_root)

        state_key = schema.get("state_key")
        config_key = schema.get("config_key")

        if state_key:
            if "." in state_key:
                state = _set_nested_value(state, state_key, parsed_value)
            else:
                state[state_key] = parsed_value

        if config_key == "loop_limits":
            current_limits = state.get("loop_limits", dict(DEFAULT_LOOP_LIMITS))
            state["loop_limits"] = {k: parsed_value for k in current_limits}

        _save_project_state(project_root, state)
        if project_config:
            _save_project_config(project_root, project_config)

        return {"key": key, "value": parsed_value, "scope": "project", "message": f"Updated {key}"}


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser."""
    parser = argparse.ArgumentParser(description="Configuration I/O for AI Research Orchestrator.")
    parser.add_argument(
        "--project-root",
        default=None,
        help="Path to the project root.",
    )
    parser.add_argument(
        "--action",
        choices=["get", "set"],
        required=True,
        help="Configuration action to perform.",
    )
    parser.add_argument(
        "--key",
        required=True,
        help="Configuration key.",
    )
    parser.add_argument(
        "--value",
        help="Configuration value (for 'set' action).",
    )
    return parser


def main() -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args()

    from utils.path_utils import find_project_root

    if args.project_root is not None:
        project_root: Path | None = Path(args.project_root).resolve()
        if not (project_root / ".autoresearch").exists():
            project_root = find_project_root(project_root)
    else:
        project_root = find_project_root()

    if project_root is None:
        print(
            "Error: no AI Research project found.",
            file=sys.stderr,
        )
        return 1

    try:
        if args.action == "get":
            result = get_config(project_root, args.key)
        elif args.action == "set":
            if args.value is None:
                print("Error: --value is required for 'set' action.", file=sys.stderr)
                return 1
            result = set_config(project_root, args.key, args.value)
        else:
            print(f"Error: unknown action: {args.action}", file=sys.stderr)
            return 1

        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    except Exception as e:
        logger.exception("Failed to configure project")
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
