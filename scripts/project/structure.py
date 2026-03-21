"""Project structure validation and creation."""

from __future__ import annotations

import logging
from pathlib import Path

from constants import DEFAULT_DELIVERABLES, REQUIRED_DIRECTORIES

logger = logging.getLogger(__name__)


def ensure_project_structure(
    project_root: Path, create_if_missing: bool = True
) -> bool:
    """Ensure project directory structure is valid.

    Args:
        project_root: Path to the project root directory
        create_if_missing: If True, create missing directories automatically

    Returns:
        True if structure is valid (all directories exist)
        False if structure is invalid and create_if_missing is False
    """
    project_root = project_root.resolve()
    if not project_root.exists():
        if create_if_missing:
            project_root.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created project root: {project_root}")
        else:
            logger.error(f"Project root does not exist: {project_root}")
            return False

    missing_dirs: list[str] = []
    for dir_path in REQUIRED_DIRECTORIES:
        full_path = project_root / dir_path
        if not full_path.exists():
            missing_dirs.append(dir_path)

    if missing_dirs:
        if create_if_missing:
            for dir_path in missing_dirs:
                full_path = project_root / dir_path
                full_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {dir_path}")
        else:
            logger.warning(f"Missing directories: {missing_dirs}")
            return False

    state_file = project_root / DEFAULT_DELIVERABLES["research_state"]
    if not state_file.exists():
        logger.info(f"State file not found (expected): {state_file}")

    return True
