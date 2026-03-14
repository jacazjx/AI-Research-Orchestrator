#!/usr/bin/env python3
"""Project analysis script.

This script analyzes an existing project directory and identifies its structure,
components, and current status to help with project onboarding.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from orchestrator_common import PHASE_DIRECTORIES, REQUIRED_DIRECTORIES, DEFAULT_DELIVERABLES


# Common patterns for research project detection
RESEARCH_PATTERNS = {
    "paper_draft": ["*.tex", "*.md", "paper*", "draft*", "manuscript*"],
    "experiment_code": ["*.py", "train*.py", "eval*.py", "experiment*.py", "run*.py"],
    "data_files": ["*.csv", "*.json", "*.pkl", "*.pt", "*.pth", "data*"],
    "config_files": ["*.yaml", "*.yml", "*.json", "config*", "settings*"],
    "notebooks": ["*.ipynb"],
    "readme": ["README*", "readme*"],
    "bibliography": ["*.bib", "references*"],
}


def detect_file_patterns(project_root: Path) -> dict[str, list[str]]:
    """Detect files matching common research patterns."""
    results = {}

    for category, patterns in RESEARCH_PATTERNS.items():
        matches = []
        for pattern in patterns:
            for match in project_root.rglob(pattern):
                if match.is_file():
                    relative = match.relative_to(project_root)
                    # Skip hidden directories and common exclusions
                    if not any(part.startswith(".") for part in relative.parts):
                        if "node_modules" not in relative.parts and "__pycache__" not in relative.parts:
                            matches.append(str(relative))
        results[category] = sorted(set(matches))

    return results


def detect_directory_structure(project_root: Path) -> dict[str, Any]:
    """Detect the directory structure of the project."""
    results = {
        "top_level_dirs": [],
        "total_files": 0,
        "total_dirs": 0,
        "phase_dirs_found": [],
        "required_dirs_found": [],
        "custom_dirs": [],
    }

    # Get top-level directories
    for item in project_root.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            results["top_level_dirs"].append(item.name)

    # Count total files and directories
    for item in project_root.rglob("*"):
        if item.is_file():
            results["total_files"] += 1
        elif item.is_dir():
            results["total_dirs"] += 1

    # Check for legacy phase directories
    for phase_dir in PHASE_DIRECTORIES:
        if (project_root / phase_dir).exists():
            results["phase_dirs_found"].append(phase_dir)

    # Check for new required directories
    for req_dir in REQUIRED_DIRECTORIES:
        if (project_root / req_dir).exists():
            results["required_dirs_found"].append(req_dir)

    # Find custom directories (top-level that aren't phase dirs)
    known_top_level = {"paper", "code", "docs", "agents"}
    for dir_name in results["top_level_dirs"]:
        if dir_name not in known_top_level and dir_name not in PHASE_DIRECTORIES:
            results["custom_dirs"].append(dir_name)

    return results


def detect_existing_deliverables(project_root: Path) -> dict[str, dict[str, Any]]:
    """Check which standard deliverables already exist."""
    results = {}

    for key, relative_path in DEFAULT_DELIVERABLES.items():
        file_path = project_root / relative_path
        exists = file_path.exists()

        result = {
            "key": key,
            "path": relative_path,
            "exists": exists,
        }

        if exists:
            # Get file size and modification time
            stat = file_path.stat()
            result["size_bytes"] = stat.st_size
            result["modified"] = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()

            # Check if file has content
            try:
                content = file_path.read_text(encoding="utf-8")
                result["line_count"] = len(content.splitlines())
                result["has_content"] = bool(content.strip())
            except Exception:
                result["has_content"] = False

        results[key] = result

    return results


def detect_research_state(project_root: Path) -> dict[str, Any]:
    """Check if research-state.yaml exists and parse it."""
    state_path = project_root / DEFAULT_DELIVERABLES["research_state"]
    results = {
        "exists": False,
        "valid": False,
        "current_phase": None,
        "current_gate": None,
        "parsed_state": None,
    }

    if not state_path.exists():
        return results

    results["exists"] = True

    try:
        from orchestrator_common import yaml_load
        content = state_path.read_text(encoding="utf-8")
        state = yaml_load(content)

        results["valid"] = True
        results["current_phase"] = state.get("current_phase")
        results["current_gate"] = state.get("current_gate")
        results["parsed_state"] = {
            "project_id": state.get("project_id"),
            "topic": state.get("topic"),
            "phase": state.get("phase"),
            "current_phase": state.get("current_phase"),
            "current_gate": state.get("current_gate"),
            "phase_reviews": state.get("phase_reviews"),
            "approval_status": state.get("approval_status"),
            "loop_counts": state.get("loop_counts"),
        }
    except Exception as e:
        results["error"] = str(e)

    return results


def detect_experiment_evidence(project_root: Path) -> dict[str, Any]:
    """Detect experiment-related evidence."""
    results = {
        "experiment_dirs": [],
        "log_files": [],
        "checkpoint_files": [],
        "result_files": [],
        "config_files": [],
    }

    # Look for experiment-related directories
    exp_indicators = ["experiment", "exp", "results", "outputs", "logs", "checkpoints", "runs"]
    for item in project_root.iterdir():
        if item.is_dir():
            name_lower = item.name.lower()
            if any(ind in name_lower for ind in exp_indicators):
                results["experiment_dirs"].append(item.name)

    # Look for log files
    for pattern in ["**/*.log", "**/log*", "**/train*.txt", "**/output*.txt"]:
        for match in project_root.glob(pattern):
            if match.is_file():
                results["log_files"].append(str(match.relative_to(project_root)))

    # Look for checkpoint files
    for pattern in ["**/*.pt", "**/*.pth", "**/*.ckpt", "**/checkpoint*", "**/model*"]:
        for match in project_root.glob(pattern):
            if match.is_file():
                results["checkpoint_files"].append(str(match.relative_to(project_root)))

    # Look for result files
    for pattern in ["**/result*.json", "**/result*.csv", "**/metrics*", "**/eval*"]:
        for match in project_root.glob(pattern):
            if match.is_file():
                results["result_files"].append(str(match.relative_to(project_root)))

    # Look for config files
    for pattern in ["**/*config*.yaml", "**/*config*.yml", "**/*config*.json"]:
        for match in project_root.glob(pattern):
            if match.is_file():
                results["config_files"].append(str(match.relative_to(project_root)))

    # Sort and deduplicate
    for key in results:
        results[key] = sorted(set(results[key]))[:20]  # Limit to 20 each

    return results


def detect_literature_evidence(project_root: Path) -> dict[str, Any]:
    """Detect literature-related evidence."""
    results = {
        "bib_files": [],
        "reference_papers": [],
        "survey_documents": [],
        "notes_documents": [],
    }

    # Look for BibTeX files
    for pattern in ["**/*.bib"]:
        for match in project_root.glob(pattern):
            if match.is_file():
                results["bib_files"].append(str(match.relative_to(project_root)))

    # Look for reference papers (PDFs)
    for pattern in ["**/*.pdf", "**/papers/*", "**/references/*"]:
        for match in project_root.glob(pattern):
            if match.is_file() and match.suffix == ".pdf":
                results["reference_papers"].append(str(match.relative_to(project_root)))

    # Look for survey-like documents
    for pattern in ["**/survey*.md", "**/literature*.md", "**/related_work*.md"]:
        for match in project_root.glob(pattern):
            if match.is_file():
                results["survey_documents"].append(str(match.relative_to(project_root)))

    # Look for notes
    for pattern in ["**/notes/*.md", "**/*notes*.md"]:
        for match in project_root.glob(pattern):
            if match.is_file():
                results["notes_documents"].append(str(match.relative_to(project_root)))

    # Sort and limit
    for key in results:
        results[key] = sorted(set(results[key]))[:20]

    return results


def estimate_project_phase(project_root: Path) -> dict[str, Any]:
    """Estimate the current project phase based on existing artifacts."""
    results = {
        "estimated_phase": None,
        "estimated_gate": None,
        "confidence": "low",
        "evidence": [],
    }

    # Check for existing deliverables
    deliverables = detect_existing_deliverables(project_root)

    # Phase detection logic
    has_final_acceptance = deliverables.get("final_acceptance_report", {}).get("exists", False)
    has_paper_draft = deliverables.get("paper_draft", {}).get("exists", False)
    has_evidence_package = deliverables.get("evidence_package_index", {}).get("exists", False)
    has_experiment_results = deliverables.get("results_summary", {}).get("exists", False)
    has_pilot_results = deliverables.get("pilot_results", {}).get("exists", False)
    has_readiness_report = deliverables.get("readiness_report", {}).get("exists", False)

    # Check for file patterns
    patterns = detect_file_patterns(project_root)
    has_experiment_code = bool(patterns.get("experiment_code", []))
    has_paper_files = bool(patterns.get("paper_draft", []))

    # Determine phase (using new semantic names)
    if has_final_acceptance:
        results["estimated_phase"] = "reflection"
        results["estimated_gate"] = "gate_4"
        results["confidence"] = "high"
        results["evidence"].append("Final acceptance report exists")
    elif has_paper_draft:
        results["estimated_phase"] = "paper"
        results["estimated_gate"] = "gate_3"
        results["confidence"] = "medium"
        results["evidence"].append("Paper draft exists")
    elif has_evidence_package or has_experiment_results:
        results["estimated_phase"] = "experiments"
        results["estimated_gate"] = "gate_2"
        results["confidence"] = "medium"
        results["evidence"].append("Experiment results exist")
    elif has_pilot_results:
        results["estimated_phase"] = "pilot"
        results["estimated_gate"] = "gate_1"
        results["confidence"] = "medium"
        results["evidence"].append("Pilot results exist")
    elif has_readiness_report:
        results["estimated_phase"] = "survey"
        results["estimated_gate"] = "gate_1"
        results["confidence"] = "medium"
        results["evidence"].append("Research readiness report exists")
    elif has_experiment_code:
        results["estimated_phase"] = "pilot"
        results["estimated_gate"] = "gate_1"
        results["confidence"] = "low"
        results["evidence"].append("Experiment code detected")
    elif has_paper_files:
        results["estimated_phase"] = "paper"
        results["estimated_gate"] = "gate_3"
        results["confidence"] = "low"
        results["evidence"].append("Paper files detected")
    else:
        results["estimated_phase"] = "survey"
        results["estimated_gate"] = None
        results["confidence"] = "low"
        results["evidence"].append("No standard deliverables found")

    return results


def analyze_project(project_root: Path) -> dict[str, Any]:
    """Perform comprehensive project analysis."""
    analysis_time = datetime.now(timezone.utc).isoformat()

    results = {
        "analysis_time": analysis_time,
        "project_root": str(project_root),
        "project_exists": project_root.exists(),
        "directory_structure": detect_directory_structure(project_root),
        "file_patterns": detect_file_patterns(project_root),
        "existing_deliverables": detect_existing_deliverables(project_root),
        "research_state": detect_research_state(project_root),
        "experiment_evidence": detect_experiment_evidence(project_root),
        "literature_evidence": detect_literature_evidence(project_root),
        "phase_estimate": estimate_project_phase(project_root),
    }

    # Calculate summary stats
    deliverable_count = sum(1 for d in results["existing_deliverables"].values() if d.get("exists", False))
    results["summary"] = {
        "total_files": results["directory_structure"]["total_files"],
        "total_dirs": results["directory_structure"]["total_dirs"],
        "deliverables_found": deliverable_count,
        "phase_dirs_found": len(results["directory_structure"]["phase_dirs_found"]),
        "estimated_phase": results["phase_estimate"]["estimated_phase"],
        "is_orchestrated_project": results["research_state"]["exists"],
    }

    return results


def format_report(analysis: dict[str, Any]) -> str:
    """Format analysis report as human-readable text."""
    lines = [
        "# Project Analysis Report",
        "",
        f"**Analysis Time**: {analysis['analysis_time']}",
        f"**Project Root**: `{analysis['project_root']}`",
        "",
    ]

    # Summary
    summary = analysis["summary"]
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total Files**: {summary['total_files']}")
    lines.append(f"- **Total Directories**: {summary['total_dirs']}")
    lines.append(f"- **Standard Deliverables Found**: {summary['deliverables_found']}")
    lines.append(f"- **Phase Directories Found**: {summary['phase_dirs_found']}")
    lines.append(f"- **Estimated Phase**: `{summary['estimated_phase']}`")
    lines.append(f"- **Is Orchestrated Project**: {'Yes' if summary['is_orchestrated_project'] else 'No'}")
    lines.append("")

    # Phase Estimate
    phase = analysis["phase_estimate"]
    lines.append("## Phase Estimation")
    lines.append("")
    lines.append(f"- **Estimated Phase**: `{phase['estimated_phase']}`")
    lines.append(f"- **Estimated Gate**: `{phase['estimated_gate']}`")
    lines.append(f"- **Confidence**: {phase['confidence']}")
    lines.append("**Evidence**:")
    for evidence in phase["evidence"]:
        lines.append(f"- {evidence}")
    lines.append("")

    # Directory Structure
    dirs = analysis["directory_structure"]
    lines.append("## Directory Structure")
    lines.append("")
    lines.append(f"- **Top-level directories**: {', '.join(dirs['top_level_dirs'][:10]) or 'None'}")
    if dirs["phase_dirs_found"]:
        lines.append(f"- **Phase directories found**: {', '.join(dirs['phase_dirs_found'])}")
    if dirs["custom_dirs"]:
        lines.append(f"- **Custom directories**: {', '.join(dirs['custom_dirs'][:10])}")
    lines.append("")

    # Research State
    state = analysis["research_state"]
    lines.append("## Research State")
    lines.append("")
    if state["exists"]:
        lines.append(f"- **State file exists**: Yes")
        lines.append(f"- **Valid**: {'Yes' if state['valid'] else 'No'}")
        if state["current_phase"]:
            lines.append(f"- **Current Phase**: `{state['current_phase']}`")
        if state["current_gate"]:
            lines.append(f"- **Current Gate**: `{state['current_gate']}`")
    else:
        lines.append("- **State file exists**: No")
    lines.append("")

    # Existing Deliverables
    lines.append("## Existing Deliverables")
    lines.append("")
    deliverables = analysis["existing_deliverables"]
    found_deliverables = [(k, v) for k, v in deliverables.items() if v.get("exists", False)]
    if found_deliverables:
        for key, info in found_deliverables:
            lines.append(f"- ✅ `{info['path']}` ({info.get('line_count', '?')} lines)")
    else:
        lines.append("- No standard deliverables found")
    lines.append("")

    # File Patterns
    patterns = analysis["file_patterns"]
    lines.append("## Detected File Patterns")
    lines.append("")
    for category, files in patterns.items():
        count = len(files)
        if count > 0:
            lines.append(f"- **{category}**: {count} files")
            for f in files[:3]:
                lines.append(f"  - `{f}`")
            if count > 3:
                lines.append(f"  - ... and {count - 3} more")
    lines.append("")

    # Experiment Evidence
    exp = analysis["experiment_evidence"]
    lines.append("## Experiment Evidence")
    lines.append("")
    if any(exp.values()):
        for key, files in exp.items():
            if files:
                lines.append(f"- **{key}**: {len(files)} files")
    else:
        lines.append("- No experiment evidence detected")
    lines.append("")

    # Literature Evidence
    lit = analysis["literature_evidence"]
    lines.append("## Literature Evidence")
    lines.append("")
    if any(lit.values()):
        for key, files in lit.items():
            if files:
                lines.append(f"- **{key}**: {len(files)} files")
    else:
        lines.append("- No literature evidence detected")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze an existing project")
    parser.add_argument("--project-root", required=True, help="Path to project root")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--quiet", action="store_true", help="Only output estimated phase")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()

    if not project_root.exists():
        print(f"Error: Project root does not exist: {project_root}", file=sys.stderr)
        return 1

    analysis = analyze_project(project_root)

    if args.json:
        print(json.dumps(analysis, indent=2, default=str))
    elif args.quiet:
        print(analysis["phase_estimate"]["estimated_phase"] or "unknown")
    else:
        print(format_report(analysis))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())