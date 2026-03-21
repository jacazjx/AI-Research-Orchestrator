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

# Deliverables for each phase (relative to project root)
PHASE_DELIVERABLES: dict[str, list[str]] = {
    "survey": [
        "docs/survey/survey-round-summary.md",
        "docs/survey/critic-round-review.md",
        "docs/survey/research-readiness-report.md",
        "docs/survey/phase-scorecard.md",
    ],
    "pilot": [
        "docs/pilot/problem-validation-report.md",
        "docs/pilot/problem-analysis.md",
        "docs/pilot/pilot-results.md",
        "docs/pilot/pilot-validation-report.md",
        "docs/pilot/phase-scorecard.md",
    ],
    "experiments": [
        "docs/experiments/results-summary.md",
        "docs/experiments/evidence-package-index.md",
        "docs/experiments/phase-scorecard.md",
    ],
    "paper": [
        "paper/paper-draft.md",
        "paper/citation-audit-report.md",
        "docs/paper/final-acceptance-report.md",
        "docs/paper/phase-scorecard.md",
    ],
    "reflection": [
        "docs/reflection/lessons-learned.md",
        "docs/reflection/runtime-improvement-report.md",
        "docs/reflection/phase-scorecard.md",
    ],
}


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
