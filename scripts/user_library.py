"""User-level library management for AI Research Orchestrator.

This module provides functions to manage user-level storage for lessons learned
and approved overlays that persist across all research projects.

Storage locations:
- ~/.autoresearch/lessons-library/ - Cross-project lessons library
- ~/.autoresearch/approved-overlays/ - Approved overlay library

This enables knowledge accumulation and reuse across multiple research projects.
"""

from __future__ import annotations

import json
import logging
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# Configure module logger
logger = logging.getLogger(__name__)

# Directory names
LESSONS_LIBRARY_DIR_NAME = "lessons-library"
OVERLAYS_DIR_NAME = "approved-overlays"
INDEX_FILENAME = "index.yaml"


def get_user_config_dir() -> Path:
    """Get the user configuration directory path.

    Returns the path to ~/.autoresearch/. Creates the directory if it
    does not exist.

    Returns:
        Path to the user configuration directory.
    """
    config_dir = Path.home() / ".autoresearch"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_lessons_library_dir() -> Path:
    """Get the lessons library directory path.

    Returns the path to ~/.autoresearch/lessons-library/. Creates the
    directory and subdirectories if they do not exist.

    Returns:
        Path to the lessons library directory.
    """
    lessons_dir = get_user_config_dir() / LESSONS_LIBRARY_DIR_NAME
    lessons_dir.mkdir(parents=True, exist_ok=True)

    # Create category subdirectories
    for category in ["methodology", "process", "tools"]:
        (lessons_dir / "by-category" / category).mkdir(parents=True, exist_ok=True)

    # Create by-project directory
    (lessons_dir / "by-project").mkdir(parents=True, exist_ok=True)

    return lessons_dir


def get_overlays_dir() -> Path:
    """Get the approved overlays directory path.

    Returns the path to ~/.autoresearch/approved-overlays/. Creates the
    directory and subdirectories if they do not exist.

    Returns:
        Path to the approved overlays directory.
    """
    overlays_dir = get_user_config_dir() / OVERLAYS_DIR_NAME
    overlays_dir.mkdir(parents=True, exist_ok=True)

    # Create by-role subdirectories
    for role in ["survey", "code", "writer", "adviser", "reflector"]:
        (overlays_dir / "by-role" / role).mkdir(parents=True, exist_ok=True)

    # Create by-phase subdirectories
    for phase in ["survey", "pilot", "experiments", "paper", "reflection"]:
        (overlays_dir / "by-phase" / phase).mkdir(parents=True, exist_ok=True)

    return overlays_dir


def _load_yaml_file(path: Path) -> dict[str, Any]:
    """Load a YAML file with error handling.

    Args:
        path: Path to the YAML file.

    Returns:
        Parsed YAML content, or empty dict if file doesn't exist.
    """
    if not path.exists():
        return {}
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        logger.warning("Failed to parse YAML file: %s", path)
        return {}


def _save_yaml_file(path: Path, data: dict[str, Any]) -> None:
    """Save data to a YAML file atomically.

    Args:
        path: Path to save the YAML file.
        data: Data to save.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Atomic write
        fd, temp_path = tempfile.mkstemp(
            dir=path.parent,
            prefix=path.name + ".",
            suffix=".tmp",
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            os.replace(temp_path, path)
        except Exception:
            Path(temp_path).unlink(missing_ok=True)
            raise
    except OSError as exc:
        logger.error("Failed to save YAML file %s: %s", path, exc)
        raise


def generate_lesson_id() -> str:
    """Generate a unique lesson ID.

    Returns:
        Unique lesson ID in format 'lesson-YYYYMMDD-HHMMSS'.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"lesson-{timestamp}"


def generate_overlay_id() -> str:
    """Generate a unique overlay ID.

    Returns:
        Unique overlay ID in format 'overlay-YYYYMMDD-HHMMSS'.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"overlay-{timestamp}"


def save_lesson_to_library(
    lesson_content: str,
    lesson_id: str | None = None,
    category: str = "methodology",
    source_project: str = "",
    title: str = "",
    tags: list[str] | None = None,
) -> Path:
    """Save a lesson to the user-level lessons library.

    Args:
        lesson_content: The lesson content (markdown).
        lesson_id: Unique identifier. Generated if not provided.
        category: Category (methodology, process, tools).
        source_project: Name/path of the source project.
        title: Optional title for the lesson.
        tags: Optional list of tags for searching.

    Returns:
        Path to the saved lesson file.
    """
    lessons_dir = get_lessons_library_dir()

    if lesson_id is None:
        lesson_id = generate_lesson_id()

    tags = tags or []
    timestamp = datetime.now(timezone.utc).isoformat()

    # Create lesson file with metadata
    lesson_data = {
        "id": lesson_id,
        "title": title or f"Lesson from {source_project}",
        "category": category,
        "source_project": source_project,
        "tags": tags,
        "created_at": timestamp,
        "content": lesson_content,
    }

    # Save to by-category directory
    category_path = lessons_dir / "by-category" / category / f"{lesson_id}.yaml"
    _save_yaml_file(category_path, lesson_data)

    # Update index
    index_path = lessons_dir / INDEX_FILENAME
    index = _load_yaml_file(index_path)

    if "lessons" not in index:
        index["lessons"] = {}

    index["lessons"][lesson_id] = {
        "title": lesson_data["title"],
        "category": category,
        "source_project": source_project,
        "tags": tags,
        "created_at": timestamp,
        "path": str(category_path.relative_to(lessons_dir)),
    }

    _save_yaml_file(index_path, index)

    logger.info("Saved lesson %s to library", lesson_id)
    return category_path


def save_overlay_to_library(
    overlay_content: str,
    overlay_id: str | None = None,
    target_roles: list[str] | None = None,
    target_phases: list[str] | None = None,
    source_project: str = "",
    title: str = "",
    description: str = "",
) -> Path:
    """Save an overlay to the user-level approved overlays library.

    Args:
        overlay_content: The overlay content (markdown).
        overlay_id: Unique identifier. Generated if not provided.
        target_roles: List of roles this overlay applies to.
        target_phases: List of phases this overlay applies to.
        source_project: Name/path of the source project.
        title: Optional title for the overlay.
        description: Optional description of what the overlay does.

    Returns:
        Path to the saved overlay file.
    """
    overlays_dir = get_overlays_dir()

    if overlay_id is None:
        overlay_id = generate_overlay_id()

    target_roles = target_roles or []
    target_phases = target_phases or []
    timestamp = datetime.now(timezone.utc).isoformat()

    # Create overlay file with metadata
    overlay_data = {
        "id": overlay_id,
        "title": title or f"Overlay from {source_project}",
        "description": description,
        "roles": target_roles,
        "phases": target_phases,
        "source_project": source_project,
        "created_at": timestamp,
        "content": overlay_content,
    }

    # Save to main directory
    overlay_path = overlays_dir / f"{overlay_id}.yaml"
    _save_yaml_file(overlay_path, overlay_data)

    # Create symlinks/references in by-role directories
    for role in target_roles:
        role_ref_path = overlays_dir / "by-role" / role / f"{overlay_id}.yaml"
        # Store reference instead of symlink for cross-platform compatibility
        ref_data = {"ref": str(overlay_path.relative_to(overlays_dir))}
        _save_yaml_file(role_ref_path, ref_data)

    # Create symlinks/references in by-phase directories
    for phase in target_phases:
        phase_ref_path = overlays_dir / "by-phase" / phase / f"{overlay_id}.yaml"
        ref_data = {"ref": str(overlay_path.relative_to(overlays_dir))}
        _save_yaml_file(phase_ref_path, ref_data)

    # Update index
    index_path = overlays_dir / INDEX_FILENAME
    index = _load_yaml_file(index_path)

    if "overlays" not in index:
        index["overlays"] = {}

    index["overlays"][overlay_id] = {
        "title": overlay_data["title"],
        "description": description,
        "roles": target_roles,
        "phases": target_phases,
        "source_project": source_project,
        "created_at": timestamp,
        "path": str(overlay_path.relative_to(overlays_dir)),
    }

    _save_yaml_file(index_path, index)

    logger.info("Saved overlay %s to library", overlay_id)
    return overlay_path


def load_all_overlays() -> list[dict[str, Any]]:
    """Load all overlays from the user-level library.

    Returns:
        List of overlay dictionaries, each containing:
        - id: Overlay ID
        - title: Overlay title
        - description: Overlay description
        - roles: List of target roles
        - phases: List of target phases
        - content: Overlay content
        - created_at: Creation timestamp
    """
    overlays_dir = get_overlays_dir()
    index_path = overlays_dir / INDEX_FILENAME

    index = _load_yaml_file(index_path)
    overlays = []

    for overlay_id, metadata in index.get("overlays", {}).items():
        overlay_path = overlays_dir / metadata.get("path", f"{overlay_id}.yaml")
        if overlay_path.exists():
            overlay_data = _load_yaml_file(overlay_path)
            overlays.append({
                "id": overlay_id,
                "title": overlay_data.get("title", ""),
                "description": overlay_data.get("description", ""),
                "roles": overlay_data.get("roles", []),
                "phases": overlay_data.get("phases", []),
                "content": overlay_data.get("content", ""),
                "created_at": overlay_data.get("created_at", ""),
                "source_project": overlay_data.get("source_project", ""),
            })

    return overlays


def load_all_lessons() -> list[dict[str, Any]]:
    """Load all lessons from the user-level library.

    Returns:
        List of lesson dictionaries, each containing:
        - id: Lesson ID
        - title: Lesson title
        - category: Lesson category
        - content: Lesson content
        - tags: List of tags
        - created_at: Creation timestamp
    """
    lessons_dir = get_lessons_library_dir()
    index_path = lessons_dir / INDEX_FILENAME

    index = _load_yaml_file(index_path)
    lessons = []

    for lesson_id, metadata in index.get("lessons", {}).items():
        lesson_path = lessons_dir / metadata.get("path", "")
        if lesson_path.exists():
            lesson_data = _load_yaml_file(lesson_path)
            lessons.append({
                "id": lesson_id,
                "title": lesson_data.get("title", ""),
                "category": lesson_data.get("category", ""),
                "content": lesson_data.get("content", ""),
                "tags": lesson_data.get("tags", []),
                "created_at": lesson_data.get("created_at", ""),
                "source_project": lesson_data.get("source_project", ""),
            })

    return lessons


def delete_lesson_from_library(lesson_id: str) -> bool:
    """Delete a lesson from the library.

    Args:
        lesson_id: ID of the lesson to delete.

    Returns:
        True if deleted, False if not found.
    """
    lessons_dir = get_lessons_library_dir()
    index_path = lessons_dir / INDEX_FILENAME

    index = _load_yaml_file(index_path)

    if lesson_id not in index.get("lessons", {}):
        return False

    metadata = index["lessons"][lesson_id]
    lesson_path = lessons_dir / metadata.get("path", "")

    # Delete the lesson file
    if lesson_path.exists():
        lesson_path.unlink()

    # Update index
    del index["lessons"][lesson_id]
    _save_yaml_file(index_path, index)

    logger.info("Deleted lesson %s from library", lesson_id)
    return True


def delete_overlay_from_library(overlay_id: str) -> bool:
    """Delete an overlay from the library.

    Args:
        overlay_id: ID of the overlay to delete.

    Returns:
        True if deleted, False if not found.
    """
    overlays_dir = get_overlays_dir()
    index_path = overlays_dir / INDEX_FILENAME

    index = _load_yaml_file(index_path)

    if overlay_id not in index.get("overlays", {}):
        return False

    metadata = index["overlays"][overlay_id]

    # Delete the main overlay file
    overlay_path = overlays_dir / metadata.get("path", "")
    if overlay_path.exists():
        overlay_path.unlink()

    # Delete references in by-role directories
    for role in metadata.get("roles", []):
        role_ref = overlays_dir / "by-role" / role / f"{overlay_id}.yaml"
        if role_ref.exists():
            role_ref.unlink()

    # Delete references in by-phase directories
    for phase in metadata.get("phases", []):
        phase_ref = overlays_dir / "by-phase" / phase / f"{overlay_id}.yaml"
        if phase_ref.exists():
            phase_ref.unlink()

    # Update index
    del index["overlays"][overlay_id]
    _save_yaml_file(index_path, index)

    logger.info("Deleted overlay %s from library", overlay_id)
    return True


def search_lessons_by_tag(tag: str) -> list[dict[str, Any]]:
    """Search lessons by tag.

    Args:
        tag: Tag to search for.

    Returns:
        List of matching lessons.
    """
    all_lessons = load_all_lessons()
    return [l for l in all_lessons if tag in l.get("tags", [])]


def search_lessons_by_category(category: str) -> list[dict[str, Any]]:
    """Search lessons by category.

    Args:
        category: Category to search for (methodology, process, tools).

    Returns:
        List of matching lessons.
    """
    all_lessons = load_all_lessons()
    return [l for l in all_lessons if l.get("category") == category]


def search_overlays_by_role(role: str) -> list[dict[str, Any]]:
    """Search overlays by target role.

    Args:
        role: Role to search for.

    Returns:
        List of matching overlays.
    """
    all_overlays = load_all_overlays()
    return [o for o in all_overlays if role in o.get("roles", [])]


def search_overlays_by_phase(phase: str) -> list[dict[str, Any]]:
    """Search overlays by target phase.

    Args:
        phase: Phase to search for.

    Returns:
        List of matching overlays.
    """
    all_overlays = load_all_overlays()
    return [o for o in all_overlays if phase in o.get("phases", [])]