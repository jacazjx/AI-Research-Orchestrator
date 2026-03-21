#!/usr/bin/env python3
"""Project migration script.

This script helps migrate an existing project to the AI research orchestrator format
by creating the required directory structure, state files, and importing existing artifacts.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from orchestrator_common import (  # noqa: E402
    DEFAULT_DELIVERABLES,
    DEFAULT_LANGUAGE_POLICY,
    DEFAULT_LOOP_LIMITS,
    REQUIRED_DIRECTORIES,
    build_state,
    ensure_project_structure,
    write_yaml,
)


def create_phase_directories(project_root: Path) -> dict[str, bool]:
    """Create the new semantic directory structure."""
    results = {}

    # Ensure the new project structure exists
    ensure_project_structure(project_root, create_if_missing=True)

    for dir_name in REQUIRED_DIRECTORIES:
        dir_path = project_root / dir_name
        existed = dir_path.exists()
        results[dir_name] = not existed  # True if newly created

    return results


def create_admin_structure(project_root: Path, topic: str) -> dict[str, Any]:
    """Create the system directory structure (.autoresearch/)."""
    results = {
        "created": [],
        "skipped": [],
    }

    # System directories are now under .autoresearch/
    system_dirs = [
        ".autoresearch/state",
        ".autoresearch/config",
        ".autoresearch/dashboard",
        ".autoresearch/runtime",
        ".autoresearch/reference-papers",
        ".autoresearch/templates",
        ".autoresearch/archive",
    ]

    for dir_path in system_dirs:
        full_path = project_root / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            results["created"].append(dir_path)

    return results


def create_research_state(
    project_root: Path,
    topic: str,
    starting_phase: str = "01-survey",
    project_id: str | None = None,
) -> dict[str, Any]:
    """Create the research-state.yaml file."""
    results = {
        "created": False,
        "existed": False,
        "path": None,
    }

    state_path = project_root / DEFAULT_DELIVERABLES["research_state"]

    if state_path.exists():
        results["existed"] = True
        return results

    # Generate project ID if not provided
    if not project_id:
        # Use directory name as base
        project_id = re.sub(r"[^a-z0-9-]", "-", project_root.name.lower()).strip("-")
        if not project_id:
            project_id = f"research-project-{datetime.now().strftime('%Y%m%d')}"

    # Build state with starting_phase
    state = build_state(
        project_id=project_id,
        topic=topic,
        init_source="migrate",
        init_paths=[],
        client_profile="auto",
        client_instruction_file="CLAUDE.md",
        starting_phase=starting_phase,
    )

    # Write state
    write_yaml(state_path, state)
    results["created"] = True
    results["path"] = str(state_path)

    return results


def create_workspace_manifest(project_root: Path, topic: str) -> dict[str, Any]:
    """Create the workspace-manifest.md file."""
    results = {
        "created": False,
        "existed": False,
    }

    manifest_path = project_root / DEFAULT_DELIVERABLES["workspace_manifest"]

    if manifest_path.exists():
        results["existed"] = True
        return results

    content = f"""# Workspace Manifest

## Project Overview

- **Topic**: {topic}
- **Created**: {datetime.now(timezone.utc).isoformat()}
- **Source**: Migrated from existing project

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `paper/` | Paper development and outputs |
| `code/` | Source code and experiments |
| `docs/` | Documentation and reports |
| `agents/` | Agent workspaces by role |
| `.autoresearch/` | System files (state, config, dashboard) |

## State File

- **Location**: `.autoresearch/state/research-state.yaml`
- **Purpose**: Machine-readable project state

## Important Files

- `.autoresearch/idea-brief.md` - Research idea description
- `.autoresearch/reference-papers/` - Reference papers and notes
- `.autoresearch/dashboard/` - Progress dashboard
"""

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(content, encoding="utf-8")
    results["created"] = True

    return results


def create_idea_brief(project_root: Path, topic: str, description: str = "") -> dict[str, Any]:
    """Create the idea-brief.md file."""
    results = {
        "created": False,
        "existed": False,
    }

    idea_path = project_root / DEFAULT_DELIVERABLES["idea_brief"]

    if idea_path.exists():
        results["existed"] = True
        return results

    content = f"""# Research Idea Brief

## Topic

{topic}

## Problem Statement

[Describe the problem you're trying to solve]

## Proposed Approach

[Describe your proposed approach or method]

## Goals

1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

## Constraints

- [Constraint 1]
- [Constraint 2]

## Target Venue

[Target conference or journal]

## References

- Add reference papers to `.autoresearch/reference-papers/`
"""

    idea_path.parent.mkdir(parents=True, exist_ok=True)
    idea_path.write_text(content, encoding="utf-8")
    results["created"] = True

    return results


def create_config(project_root: Path) -> dict[str, Any]:
    """Create the orchestrator-config.yaml file."""
    results = {
        "created": False,
        "existed": False,
    }

    config_path = project_root / DEFAULT_DELIVERABLES["project_config"]

    if config_path.exists():
        results["existed"] = True
        return results

    config = {
        "languages": dict(DEFAULT_LANGUAGE_POLICY),
        "loop_limits": dict(DEFAULT_LOOP_LIMITS),
        "runtime": {
            "stale_after_minutes": 30,
            "auto_discover_gpu": True,
        },
    }

    write_yaml(config_path, config)
    results["created"] = True

    return results


def import_existing_files(
    project_root: Path,
    analysis: dict[str, Any],
    dry_run: bool = False,
) -> dict[str, Any]:
    """Import existing files into the standard structure."""
    results = {
        "imported": [],
        "skipped": [],
        "errors": [],
    }

    # Import BibTeX files to reference-papers
    for bib_file in analysis.get("literature_evidence", {}).get("bib_files", []):
        src = project_root / bib_file
        dst = project_root / ".autoresearch" / "reference-papers" / Path(bib_file).name
        if src.exists() and not dst.exists():
            if not dry_run:
                try:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                    results["imported"].append(f"{bib_file} -> .autoresearch/reference-papers/")
                except Exception as e:
                    results["errors"].append(f"Failed to copy {bib_file}: {e}")
            else:
                results["imported"].append(
                    f"[DRY RUN] {bib_file} -> .autoresearch/reference-papers/"
                )

    # Import PDFs to reference-papers
    for pdf_file in analysis.get("literature_evidence", {}).get("reference_papers", []):
        src = project_root / pdf_file
        dst = project_root / ".autoresearch" / "reference-papers" / Path(pdf_file).name
        if src.exists() and not dst.exists():
            if not dry_run:
                try:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                    results["imported"].append(f"{pdf_file} -> .autoresearch/reference-papers/")
                except Exception as e:
                    results["errors"].append(f"Failed to copy {pdf_file}: {e}")
            else:
                results["imported"].append(
                    f"[DRY RUN] {pdf_file} -> .autoresearch/reference-papers/"
                )

    return results


def migrate_project(
    project_root: Path,
    topic: str,
    project_id: str | None = None,
    dry_run: bool = False,
    starting_phase: str | None = None,
) -> dict[str, Any]:
    """Perform complete project migration."""
    migration_time = datetime.now(timezone.utc).isoformat()

    results = {
        "migration_time": migration_time,
        "project_root": str(project_root),
        "dry_run": dry_run,
        "success": True,
        "steps": {},
    }

    # Step 1: Determine starting phase
    effective_starting_phase = starting_phase or "survey"
    results["steps"]["analysis"] = {
        "status": "completed",
        "estimated_phase": effective_starting_phase,
    }

    # Minimal analysis for file import: detect bib/pdf files
    analysis: dict[str, Any] = {"literature_evidence": {"bib_files": [], "reference_papers": []}}
    for f in project_root.rglob("*.bib"):
        analysis["literature_evidence"]["bib_files"].append(
            str(f.relative_to(project_root))
        )
    for f in project_root.rglob("*.pdf"):
        analysis["literature_evidence"]["reference_papers"].append(
            str(f.relative_to(project_root))
        )

    if dry_run:
        results["steps"]["create_directories"] = {"status": "skipped", "reason": "dry_run"}
        results["steps"]["create_admin"] = {"status": "skipped", "reason": "dry_run"}
        results["steps"]["create_state"] = {"status": "skipped", "reason": "dry_run"}
        results["steps"]["create_manifest"] = {"status": "skipped", "reason": "dry_run"}
        results["steps"]["create_idea"] = {"status": "skipped", "reason": "dry_run"}
        results["steps"]["create_config"] = {"status": "skipped", "reason": "dry_run"}
        results["steps"]["import_files"] = import_existing_files(
            project_root, analysis, dry_run=True
        )
    else:
        # Step 2: Create phase directories
        try:
            dir_results = create_phase_directories(project_root)
            results["steps"]["create_directories"] = {
                "status": "completed",
                "created": [k for k, v in dir_results.items() if v],
            }
        except Exception as e:
            results["steps"]["create_directories"] = {"status": "error", "error": str(e)}
            results["success"] = False

        # Step 3: Create admin structure
        try:
            admin_results = create_admin_structure(project_root, topic)
            results["steps"]["create_admin"] = {
                "status": "completed",
                **admin_results,
            }
        except Exception as e:
            results["steps"]["create_admin"] = {"status": "error", "error": str(e)}
            results["success"] = False

        # Step 4: Create research state
        try:
            state_results = create_research_state(
                project_root,
                topic,
                starting_phase=effective_starting_phase,
                project_id=project_id,
            )
            results["steps"]["create_state"] = {
                "status": "completed" if state_results["created"] else "skipped",
                "starting_phase": effective_starting_phase,
                **state_results,
            }
        except Exception as e:
            results["steps"]["create_state"] = {"status": "error", "error": str(e)}
            results["success"] = False

        # Step 5: Create workspace manifest
        try:
            manifest_results = create_workspace_manifest(project_root, topic)
            results["steps"]["create_manifest"] = {
                "status": "completed" if manifest_results["created"] else "skipped",
                **manifest_results,
            }
        except Exception as e:
            results["steps"]["create_manifest"] = {"status": "error", "error": str(e)}

        # Step 6: Create idea brief
        try:
            idea_results = create_idea_brief(project_root, topic)
            results["steps"]["create_idea"] = {
                "status": "completed" if idea_results["created"] else "skipped",
                **idea_results,
            }
        except Exception as e:
            results["steps"]["create_idea"] = {"status": "error", "error": str(e)}

        # Step 7: Create config
        try:
            config_results = create_config(project_root)
            results["steps"]["create_config"] = {
                "status": "completed" if config_results["created"] else "skipped",
                **config_results,
            }
        except Exception as e:
            results["steps"]["create_config"] = {"status": "error", "error": str(e)}

        # Step 8: Import existing files
        try:
            import_results = import_existing_files(project_root, analysis)
            results["steps"]["import_files"] = {
                "status": "completed",
                **import_results,
            }
        except Exception as e:
            results["steps"]["import_files"] = {"status": "error", "error": str(e)}

    return results


def format_report(results: dict[str, Any]) -> str:
    """Format migration report as human-readable text."""
    lines = [
        "# Project Migration Report",
        "",
        f"**Migration Time**: {results['migration_time']}",
        f"**Project Root**: `{results['project_root']}`",
        f"**Dry Run**: {'Yes' if results['dry_run'] else 'No'}",
        f"**Overall Status**: {'✅ Success' if results['success'] else '❌ Failed'}",
        "",
    ]

    for step_name, step_data in results["steps"].items():
        status = step_data.get("status", "unknown")
        icon = "✅" if status == "completed" else "⏭️" if status == "skipped" else "❌"

        lines.append(f"## {icon} {step_name.replace('_', ' ').title()}")
        lines.append("")

        if status == "completed":
            # Show relevant details
            if "created" in step_data:
                lines.append(f"- Created: {step_data['created']}")
            if "path" in step_data:
                lines.append(f"- Path: `{step_data['path']}`")
            if "imported" in step_data and step_data["imported"]:
                lines.append("**Imported**:")
                for item in step_data["imported"][:10]:
                    lines.append(f"- {item}")
        elif status == "skipped":
            lines.append(f"- Reason: {step_data.get('reason', 'already exists')}")
        elif status == "error":
            lines.append(f"- Error: {step_data.get('error', 'unknown')}")

        lines.append("")

    if results["dry_run"]:
        lines.append("---")
        lines.append("")
        lines.append("This was a dry run. No changes were made.")
        lines.append("Run without --dry-run to apply changes.")

    return "\n".join(lines)


# Support both new semantic names and legacy numbered names
VALID_PHASES = [
    "survey",
    "pilot",
    "experiments",
    "paper",
    "reflection",
    "01-survey",
    "02-pilot-analysis",
    "03-full-experiments",
    "04-paper",
    "05-reflection-evolution",
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Migrate an existing project to orchestrator format"
    )
    parser.add_argument("--project-root", required=True, help="Path to project root")
    parser.add_argument("--topic", required=True, help="Research topic or idea")
    parser.add_argument("--project-id", help="Optional project ID")
    parser.add_argument(
        "--starting-phase",
        default=None,
        choices=VALID_PHASES,
        help="Phase to start the project at. Defaults to auto-detected phase.",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done without making changes"
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--quiet", action="store_true", help="Only output success/failure")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()

    if not project_root.exists():
        print(f"Error: Project root does not exist: {project_root}", file=sys.stderr)
        return 1

    results = migrate_project(
        project_root,
        topic=args.topic,
        project_id=args.project_id,
        dry_run=args.dry_run,
        starting_phase=args.starting_phase,
    )

    if args.json:
        print(json.dumps(results, indent=2, default=str))
    elif args.quiet:
        print("success" if results["success"] else "failed")
    else:
        print(format_report(results))

    return 0 if results["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
