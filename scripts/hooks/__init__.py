# scripts/hooks/__init__.py
"""Hook scripts for AI Research Orchestrator.

Shared utilities used by all hook scripts.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def read_hook_input() -> dict:
    """Read hook input JSON from stdin.

    Returns:
        Dictionary with hook input data, or empty dict if no input.
    """
    try:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read().strip()
            if input_data:
                return json.loads(input_data)
    except (json.JSONDecodeError, IOError):
        pass
    return {}


def get_project_root() -> Path | None:
    """Try to find project root from current directory.

    Walks up from cwd looking for .autoresearch directory.

    Returns:
        Project root Path, or None if not inside a project.
    """
    cwd = Path.cwd()
    if (cwd / ".autoresearch").exists():
        return cwd
    for parent in cwd.parents:
        if (parent / ".autoresearch").exists():
            return parent
    return None
