"""YAML utility functions for AI Research Orchestrator.

Provides YAML serialization and deserialization with:
- Atomic write pattern for file safety
- Unicode support
- Preservation of key ordering
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any

import yaml


def yaml_dump(value: Any, indent: int = 0) -> str:
    """Dump a Python object to a YAML string using PyYAML.

    Args:
        value: Python object to serialize.
        indent: Ignored (kept for backward compatibility).

    Returns:
        YAML string representation.
    """
    return yaml.dump(value, allow_unicode=True, default_flow_style=False, sort_keys=False)


def yaml_load(text: str) -> Any:
    """Parse a YAML document string into a Python object using PyYAML.

    Supports all standard YAML features including:
    - Comments (preserved in round-trip but stripped in output)
    - Complex nested structures
    - Multi-line strings
    - All scalar types

    Args:
        text: YAML document string to parse.

    Returns:
        Parsed Python object (dict, list, or scalar).
    """
    return yaml.safe_load(text)


def read_yaml(path: Path) -> Any:
    """Read and parse a YAML file.

    Args:
        path: Path to the YAML file.

    Returns:
        Parsed Python object (dict, list, or scalar).
    """
    return yaml_load(path.read_text(encoding="utf-8"))


def write_yaml(path: Path, data: Any) -> None:
    """Write data to a YAML file with atomic write pattern.

    Uses a temporary file and atomic replace to prevent corruption
    if the process crashes mid-write.

    Args:
        path: Path to the target YAML file.
        data: Python object to serialize.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    content = yaml_dump(data) + "\n"

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