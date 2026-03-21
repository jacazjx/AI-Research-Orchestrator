"""State I/O: load_state, save_state, load_json, write_json."""

from __future__ import annotations

import json
import logging
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from constants import DEFAULT_DELIVERABLES

from utils import read_yaml, write_yaml

logger = logging.getLogger(__name__)


def resolve_deliverable_path(
    project_root: Path, state: dict[str, Any], key: str
) -> Path:
    """Resolve a deliverable path from state.

    Args:
        project_root: Project root directory.
        state: Project state dictionary.
        key: Deliverable key.

    Returns:
        Resolved absolute path to the deliverable.
    """
    relative_value = state["deliverables"][key]
    return (project_root / relative_value).resolve()


def append_state_log(
    state: dict[str, Any], key: str, entry: dict[str, Any] | str
) -> None:
    """Append an entry to a state log list.

    Args:
        state: Project state dictionary.
        key: State key for the log list.
        entry: Entry to append (string or dict, dicts are JSON-serialized).
    """
    items = list(state.get(key, []))
    if isinstance(entry, str):
        items.append(entry)
    else:
        items.append(json.dumps(entry, ensure_ascii=False, sort_keys=True))
    state[key] = items


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

    Args:
        path: Target file path.
        payload: Python object to serialize as JSON.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    fd, temp_path = tempfile.mkstemp(
        dir=path.parent, prefix=path.name + ".", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(temp_path, path)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


def load_state(project_root: Path) -> dict[str, Any]:
    """Load project state from file.

    Args:
        project_root: Project root directory.

    Returns:
        Project state dictionary.
    """
    from state.validator import validate_state_schema

    state = read_yaml(project_root / DEFAULT_DELIVERABLES["research_state"])
    schema_errors = validate_state_schema(state)
    if schema_errors:
        from exceptions import StateSchemaError  # type: ignore[import-untyped]

        raise StateSchemaError(
            f"research-state.yaml has schema errors in '{project_root}':\n"
            + "\n".join(f"  - {e}" for e in schema_errors)
        )

    from project.client import load_project_config

    config = load_project_config(project_root)
    state["loop_limits"] = dict(config["loop_limits"])
    state["language_policy"] = dict(config["languages"])

    from state_migrator import migrate_state, needs_migration  # type: ignore[import-untyped]

    if needs_migration(state):
        state, migration_logs = migrate_state(state)
        for log in migration_logs:
            logger.info(log)
        save_state(project_root, state)
        logger.info("State migration completed and saved")

    from state.validator import ensure_complete_deliverables

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
    """
    if previous_state is not None:
        _append_gate_audit_events(project_root, previous_state, state)
    write_yaml(project_root / DEFAULT_DELIVERABLES["research_state"], state)


def _append_gate_audit_events(
    project_root: Path,
    old_state: dict[str, Any],
    new_state: dict[str, Any],
) -> None:
    """Append gate_decision events to sentinel_events.ndjson when approval_status changes."""
    old_approvals = old_state.get("approval_status", {})
    new_approvals = new_state.get("approval_status", {})
    changed = {
        gate: status
        for gate, status in new_approvals.items()
        if status != old_approvals.get(gate)
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
