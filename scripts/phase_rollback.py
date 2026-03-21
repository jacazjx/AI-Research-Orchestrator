"""Phase rollback file handling.

This module provides functions for handling deliverables when
rolling back to an earlier phase via Gate rejection.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from constants.phases import DEFAULT_DELIVERABLES, HANDOFF_REQUIREMENTS

# Map each phase to its handoff transition key
_PHASE_TO_HANDOFF_KEY: dict[str, str] = {
    "survey": "survey-to-pilot",
    "pilot": "pilot-to-experiments",
    "experiments": "experiments-to-paper",
    "paper": "paper-to-reflection",
    "reflection": "reflection-closeout",
}


def _build_phase_deliverables() -> dict[str, list[str]]:
    """Derive phase deliverable paths from HANDOFF_REQUIREMENTS and DEFAULT_DELIVERABLES."""
    result: dict[str, list[str]] = {}
    for phase, handoff_key in _PHASE_TO_HANDOFF_KEY.items():
        handoff = HANDOFF_REQUIREMENTS.get(handoff_key, {})
        deliverable_keys = handoff.get("deliverables", ())
        paths: list[str] = []
        for key in deliverable_keys:
            path = DEFAULT_DELIVERABLES.get(key)
            if path is not None:
                paths.append(path)
        result[phase] = paths
    return result


# Derived once at import time from the canonical source
PHASE_DELIVERABLES: dict[str, list[str]] = _build_phase_deliverables()


def get_deliverables_for_phase(phase: str) -> list[str]:
    """Get list of deliverable paths for a phase."""
    return PHASE_DELIVERABLES.get(phase, [])


def archive_phase_deliverables(
    project_root: Path,
    phase: str,
    reason: str = "gate_rejection",
) -> list[str]:
    """Archive deliverables for a phase before rollback.

    Files are copied to .autoresearch/archive/ with timestamp prefix.
    Original files are preserved (not deleted).
    """
    deliverables = get_deliverables_for_phase(phase)
    archived: list[str] = []

    archive_dir = project_root / ".autoresearch" / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    phase_archive_dir = archive_dir / f"{phase}-{timestamp}"
    phase_archive_dir.mkdir(parents=True, exist_ok=True)

    metadata: dict[str, Any] = {
        "phase": phase,
        "reason": reason,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "files": [],
    }

    for deliverable in deliverables:
        src_path = project_root / deliverable
        if src_path.exists():
            relative = Path(deliverable)
            dest_path = phase_archive_dir / relative.name

            counter = 1
            while dest_path.exists():
                stem = relative.stem
                suffix = relative.suffix
                dest_path = phase_archive_dir / f"{stem}-{counter}{suffix}"
                counter += 1

            shutil.copy2(src_path, dest_path)
            archived.append(str(dest_path.relative_to(project_root)))
            metadata["files"].append(
                {
                    "original": deliverable,
                    "archived": str(dest_path.relative_to(project_root)),
                }
            )

    metadata_path = phase_archive_dir / "archive-metadata.json"
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return archived


def get_rollback_policy(phase: str) -> dict[str, Any]:
    """Get rollback policy for a phase."""
    return {
        "archive": True,
        "delete": False,
        "description": f"Archive {phase} deliverables to .autoresearch/archive/",
    }
