"""Text utility functions for AI Research Orchestrator.

Provides text processing utilities for slug generation and sanitization.
"""

from __future__ import annotations

import re


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
