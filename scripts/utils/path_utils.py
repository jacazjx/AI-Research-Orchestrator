"""Path utility functions for AI Research Orchestrator.

Provides path normalization and security validation for file operations.
"""

from __future__ import annotations

from pathlib import Path

from exceptions import PathSecurityError  # type: ignore[import-untyped]


def normalize_relative_path(project_root: Path, path_value: str | Path) -> str:
    """Normalize a path to a project-relative path.

    Converts absolute paths to project-relative paths and validates
    that the path stays within the project root for security.

    Args:
        project_root: The root directory of the project.
        path_value: The path to normalize (absolute or relative).

    Returns:
        A POSIX-style relative path from project_root.

    Raises:
        PathSecurityError: If the path attempts to escape the project root.
    """
    path = Path(path_value)
    root = project_root.resolve()
    resolved = path.resolve() if path.is_absolute() else (root / path).resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError as exc:
        raise PathSecurityError(
            f"Path must stay inside project root: {path}",
            path=str(path),
            reason="traversal",
        ) from exc
