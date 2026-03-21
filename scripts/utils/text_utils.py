"""Text utility functions for AI Research Orchestrator.

Provides text processing utilities for slug generation, sanitization,
list formatting, and shell quoting.
"""

from __future__ import annotations

import re
import shlex


def build_list_section(items: list[str], empty_message: str) -> str:
    """Build a markdown list section.

    Args:
        items: List of items to format as a markdown list.
        empty_message: Message to show when the list is empty.

    Returns:
        Formatted markdown list string.
    """
    if not items:
        return f"- {empty_message}"
    return "\n".join(f"- {item}" for item in items)


def shell_join(parts: list[str]) -> str:
    """Join shell command parts with proper quoting.

    Args:
        parts: List of shell command parts.

    Returns:
        Properly quoted shell command string.
    """
    return " ".join(shlex.quote(part) for part in parts)


def slugify(value: str) -> str:
    """Convert a string to a URL-safe slug.

    Transforms the input string by:
    1. Stripping leading/trailing whitespace
    2. Converting to lowercase
    3. Replacing non-alphanumeric characters with hyphens
    4. Removing leading/trailing hyphens

    Args:
        value: The string to slugify.

    Returns:
        A URL-safe slug string. Returns "research-project" if the result
        would be empty.
    """
    collapsed = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    collapsed = collapsed.strip("-")
    return collapsed or "research-project"
