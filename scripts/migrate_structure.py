#!/usr/bin/env python3
"""Migrate existing project from old numbered structure to new semantic structure.

Usage:
    python3 scripts/migrate_structure.py --project-root /path/to/project [--dry-run] [--no-backup]
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from orchestrator_common import (  # noqa: E402
    OLD_TO_NEW_PATH_MAPPING,
    REQUIRED_DIRECTORIES,
    load_state,
    save_state,
)

# Legacy phase directories to check
LEGACY_PHASE_DIRECTORIES = [
    "00-admin",
    "01-survey",
    "02-pilot-analysis",
    "03-full-experiments",
    "04-paper",
    "05-reflection-evolution",
    "06-archive",
]

# Phase name mapping from old to new
PHASE_NAME_MAPPING = {
    "01-survey": "survey",
    "02-pilot-analysis": "pilot",
    "03-full-experiments": "experiments",
    "04-paper": "paper",
    "05-reflection-evolution": "reflection",
    "06-archive": "archive",
}


def has_old_structure(project_root: Path) -> bool:
    """Check if project has old numbered structure.

    Args:
        project_root: Path to the project root

    Returns:
        True if any old directory exists
    """
    return any((project_root / old_dir).exists() for old_dir in LEGACY_PHASE_DIRECTORIES)


def create_backup(project_root: Path) -> Path:
    """Create backup of old directories in .autoresearch/migration_backup/.

    Args:
        project_root: Path to the project root

    Returns:
        Path to the backup directory
    """
    backup_dir = project_root / ".autoresearch" / "migration_backup"
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_subdir = backup_dir / f"backup_{timestamp}"
    backup_subdir.mkdir(parents=True, exist_ok=True)

    for old_dir in LEGACY_PHASE_DIRECTORIES:
        old_path = project_root / old_dir
        if old_path.exists():
            backup_path = backup_subdir / old_dir
            if backup_path.exists():
                shutil.rmtree(backup_path)
            shutil.copytree(old_path, backup_path)

    return backup_subdir


def create_new_structure(project_root: Path, dry_run: bool = False) -> list[str]:
    """Create new directory structure.

    Args:
        project_root: Path to the project root
        dry_run: If True, only report what would be done

    Returns:
        List of created directories
    """
    created = []

    if dry_run:
        return [f"[DRY RUN] Would create: {d}" for d in REQUIRED_DIRECTORIES]

    for dir_path in REQUIRED_DIRECTORIES:
        full_path = project_root / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            created.append(dir_path)

    return created


def migrate_files(project_root: Path, dry_run: bool = False) -> dict[str, list[tuple[str, str]]]:
    """Migrate files from old paths to new paths.

    Args:
        project_root: Path to the project root
        dry_run: If True, only report what would be done

    Returns:
        Dictionary with migration results
    """
    results = {
        "migrated_files": [],
        "migrated_dirs": [],
        "skipped": [],
        "errors": [],
    }

    for old_rel_path, new_rel_path in OLD_TO_NEW_PATH_MAPPING.items():
        src = project_root / old_rel_path
        dst = project_root / new_rel_path

        if not src.exists():
            continue

        try:
            if dry_run:
                if src.is_dir():
                    results["migrated_dirs"].append((old_rel_path, new_rel_path))
                else:
                    results["migrated_files"].append((old_rel_path, new_rel_path))
                continue

            # Ensure parent directory exists
            dst.parent.mkdir(parents=True, exist_ok=True)

            if src.is_dir():
                if dst.exists():
                    # Merge directories
                    for item in src.iterdir():
                        item_dst = dst / item.name
                        if item.is_dir():
                            if item_dst.exists():
                                shutil.rmtree(item_dst)
                            shutil.copytree(item, item_dst)
                        else:
                            shutil.copy2(item, item_dst)
                else:
                    shutil.copytree(src, dst)
                results["migrated_dirs"].append((old_rel_path, new_rel_path))
            else:
                if dst.exists():
                    # Backup existing file before overwriting
                    backup_path = dst.with_suffix(dst.suffix + ".old")
                    shutil.copy2(dst, backup_path)
                shutil.copy2(src, dst)
                results["migrated_files"].append((old_rel_path, new_rel_path))

        except Exception as e:
            results["errors"].append((old_rel_path, str(e)))

    return results


def update_state_file(project_root: Path, dry_run: bool = False) -> dict[str, Any]:
    """Update state file with new phase names.

    Args:
        project_root: Path to the project root
        dry_run: If True, only report what would be done

    Returns:
        Dictionary with update results
    """
    results = {"updated": False, "old_phase": None, "new_phase": None}

    state_path = project_root / ".autoresearch" / "state" / "research-state.yaml"
    if not state_path.exists():
        # Try old path
        state_path = project_root / "00-admin" / "research-state.yaml"
        if not state_path.exists():
            return results

    if dry_run:
        return {"updated": True, "dry_run": True}

    try:
        state = load_state(project_root)
        current_phase = state.get("current_phase", "")

        # Update current_phase if it uses old format
        if current_phase in PHASE_NAME_MAPPING:
            results["old_phase"] = current_phase
            results["new_phase"] = PHASE_NAME_MAPPING[current_phase]
            state["current_phase"] = results["new_phase"]
            results["updated"] = True

        # Also update phase_reviews keys
        if "phase_reviews" in state:
            new_reviews = {}
            for phase, review in state["phase_reviews"].items():
                if phase in PHASE_NAME_MAPPING:
                    new_reviews[PHASE_NAME_MAPPING[phase]] = review
                else:
                    new_reviews[phase] = review
            state["phase_reviews"] = new_reviews

        # Update approval_status keys
        if "approval_status" in state:
            new_approvals = {}
            for phase, status in state["approval_status"].items():
                if phase in PHASE_NAME_MAPPING:
                    new_approvals[PHASE_NAME_MAPPING[phase]] = status
                else:
                    new_approvals[phase] = status
            state["approval_status"] = new_approvals

        # Update loop_counts keys
        if "loop_counts" in state:
            new_counts = {}
            for phase, count in state["loop_counts"].items():
                if phase in PHASE_NAME_MAPPING:
                    new_counts[PHASE_NAME_MAPPING[phase]] = count
                else:
                    new_counts[phase] = count
            state["loop_counts"] = new_counts

        save_state(project_root, state)

    except Exception as e:
        results["error"] = str(e)

    return results


def remove_old_directories(project_root: Path, dry_run: bool = False) -> list[str]:
    """Remove old numbered directories after migration.

    Args:
        project_root: Path to the project root
        dry_run: If True, only report what would be done

    Returns:
        List of removed directories
    """
    removed = []

    for old_dir in LEGACY_PHASE_DIRECTORIES:
        old_path = project_root / old_dir
        if old_path.exists():
            if dry_run:
                removed.append(f"[DRY RUN] Would remove: {old_dir}")
            else:
                try:
                    shutil.rmtree(old_path)
                    removed.append(old_dir)
                except Exception as e:
                    removed.append(f"{old_dir} (error: {e})")

    return removed


def migrate_project(
    project_root: Path,
    dry_run: bool = False,
    backup: bool = True,
) -> dict[str, Any]:
    """Migrate a project from old numbered structure to new semantic structure.

    Args:
        project_root: Path to the project root
        dry_run: If True, only print what would be done without making changes
        backup: If True, create a backup of old directories before migration

    Returns:
        Dictionary with migration results
    """
    project_root = project_root.resolve()
    results = {
        "project_root": str(project_root),
        "dry_run": dry_run,
        "success": True,
        "has_old_structure": False,
        "backup_path": None,
        "created_directories": [],
        "migrated_files": [],
        "migrated_dirs": [],
        "state_updated": {},
        "removed_directories": [],
        "errors": [],
    }

    # Check if project has old structure
    if not has_old_structure(project_root):
        results["message"] = "No old structure detected, project may already be migrated"
        return results

    results["has_old_structure"] = True

    # Create backup if requested
    if backup:
        if dry_run:
            results["backup_path"] = (
                "[DRY RUN] Would create backup in .autoresearch/migration_backup/"
            )
        else:
            try:
                backup_path = create_backup(project_root)
                results["backup_path"] = str(backup_path)
            except Exception as e:
                results["errors"].append(f"Backup failed: {e}")
                results["success"] = False
                return results

    # Create new directory structure
    try:
        results["created_directories"] = create_new_structure(project_root, dry_run)
    except Exception as e:
        results["errors"].append(f"Directory creation failed: {e}")
        results["success"] = False
        return results

    # Migrate files using OLD_TO_NEW_PATH_MAPPING
    try:
        migration_results = migrate_files(project_root, dry_run)
        results["migrated_files"] = migration_results["migrated_files"]
        results["migrated_dirs"] = migration_results["migrated_dirs"]
        results["errors"].extend(migration_results["errors"])
    except Exception as e:
        results["errors"].append(f"File migration failed: {e}")
        results["success"] = False

    # Update state file
    try:
        results["state_updated"] = update_state_file(project_root, dry_run)
    except Exception as e:
        results["errors"].append(f"State update failed: {e}")

    # Remove old directories
    try:
        results["removed_directories"] = remove_old_directories(project_root, dry_run)
    except Exception as e:
        results["errors"].append(f"Directory removal failed: {e}")

    return results


def format_report(results: dict[str, Any]) -> str:
    """Format migration results as human-readable text.

    Args:
        results: Migration results dictionary

    Returns:
        Formatted report string
    """
    lines = [
        "# Project Structure Migration Report",
        "",
        f"**Project Root**: `{results['project_root']}`",
        f"**Dry Run**: {'Yes' if results['dry_run'] else 'No'}",
        "",
    ]

    if results.get("message"):
        lines.append(f"**Status**: {results['message']}")
        return "\n".join(lines)

    lines.append(f"**Success**: {'Yes' if results['success'] else 'No'}")
    lines.append("")

    if results.get("backup_path"):
        lines.append(f"**Backup**: `{results['backup_path']}`")
        lines.append("")

    if results.get("created_directories"):
        lines.append("## Created Directories")
        lines.append("")
        for d in results["created_directories"]:
            lines.append(f"- {d}")
        lines.append("")

    if results.get("migrated_files"):
        lines.append("## Migrated Files")
        lines.append("")
        for old_path, new_path in results["migrated_files"]:
            lines.append(f"- `{old_path}` -> `{new_path}`")
        lines.append("")

    if results.get("migrated_dirs"):
        lines.append("## Migrated Directories")
        lines.append("")
        for old_path, new_path in results["migrated_dirs"]:
            lines.append(f"- `{old_path}/` -> `{new_path}/`")
        lines.append("")

    if results.get("state_updated", {}).get("updated"):
        lines.append("## State File Updated")
        lines.append("")
        state_update = results["state_updated"]
        if state_update.get("old_phase"):
            lines.append(f"- Phase: `{state_update['old_phase']}` -> `{state_update['new_phase']}`")
        lines.append("")

    if results.get("removed_directories"):
        lines.append("## Removed Old Directories")
        lines.append("")
        for d in results["removed_directories"]:
            lines.append(f"- {d}")
        lines.append("")

    if results.get("errors"):
        lines.append("## Errors")
        lines.append("")
        for error in results["errors"]:
            if isinstance(error, tuple):
                lines.append(f"- `{error[0]}`: {error[1]}")
            else:
                lines.append(f"- {error}")
        lines.append("")

    if results.get("dry_run"):
        lines.append("---")
        lines.append("")
        lines.append("This was a dry run. No changes were made.")
        lines.append("Run without --dry-run to apply changes.")

    return "\n".join(lines)


def main() -> int:
    """Main entry point for the migration script.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description="Migrate project from old numbered structure to new semantic structure."
    )
    parser.add_argument(
        "--project-root",
        required=True,
        help="Path to project root",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip creating backup before migration",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only output success/failure",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()

    if not project_root.exists():
        print(f"Error: Project root does not exist: {project_root}", file=sys.stderr)
        return 1

    results = migrate_project(
        project_root,
        dry_run=args.dry_run,
        backup=not args.no_backup,
    )

    if args.json:
        import json

        print(json.dumps(results, indent=2, default=str))
    elif args.quiet:
        print("success" if results["success"] else "failed")
    else:
        print(format_report(results))

    return 0 if results["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
