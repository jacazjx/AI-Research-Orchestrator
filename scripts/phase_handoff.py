#!/usr/bin/env python3
"""Phase handoff summary management script.

This script handles saving and loading phase handoff summaries when
transitioning between phases.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from orchestrator_common import DEFAULT_DELIVERABLES, ensure_project_structure, load_state, save_state, write_yaml


def get_handoff_dir(project_root: Path) -> Path:
    """Get the handoff summaries directory."""
    return project_root / "00-admin" / "runtime" / "handoff-summaries"


def save_handoff_summary(
    project_root: Path,
    phase: str,
    agent_role: str,
    summary: dict[str, Any],
) -> dict[str, Any]:
    """Save a handoff summary for a phase and agent."""
    handoff_dir = get_handoff_dir(project_root)
    handoff_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).isoformat()
    filename = f"{phase}-{agent_role}-handoff.yaml"
    filepath = handoff_dir / filename

    # Add metadata
    summary["metadata"] = {
        "phase": phase,
        "agent_role": agent_role,
        "timestamp": timestamp,
    }

    write_yaml(filepath, summary)

    return {
        "status": "saved",
        "path": str(filepath.relative_to(project_root)),
        "phase": phase,
        "agent_role": agent_role,
        "timestamp": timestamp,
    }


def load_handoff_summary(
    project_root: Path,
    phase: str,
    agent_role: str,
) -> dict[str, Any] | None:
    """Load a handoff summary for a phase and agent."""
    handoff_dir = get_handoff_dir(project_root)
    filename = f"{phase}-{agent_role}-handoff.yaml"
    filepath = handoff_dir / filename

    if not filepath.exists():
        return None

    from orchestrator_common import read_yaml
    return read_yaml(filepath)


def get_phase_handoff_summaries(project_root: Path, phase: str) -> dict[str, Any]:
    """Get all handoff summaries for a phase."""
    handoff_dir = get_handoff_dir(project_root)

    # Map phase to agent roles
    phase_agents = {
        "01-survey": ["survey", "critic"],
        "02-pilot-analysis": ["code", "adviser"],
        "03-full-experiments": ["code", "adviser"],
        "04-paper": ["writer", "reviewer"],
        "05-reflection-evolution": ["reflector", "curator"],
    }

    agents = phase_agents.get(phase, [])
    summaries = {}

    for agent in agents:
        summary = load_handoff_summary(project_root, phase, agent)
        if summary:
            summaries[agent] = summary

    return {
        "phase": phase,
        "summaries": summaries,
        "available_agents": list(summaries.keys()),
    }


def list_all_handoff_summaries(project_root: Path) -> dict[str, Any]:
    """List all handoff summaries in the project."""
    handoff_dir = get_handoff_dir(project_root)

    if not handoff_dir.exists():
        return {"summaries": [], "count": 0}

    summaries = []
    for filepath in handoff_dir.glob("*.yaml"):
        summaries.append({
            "path": str(filepath.relative_to(project_root)),
            "name": filepath.stem,
        })

    return {
        "summaries": summaries,
        "count": len(summaries),
        "directory": str(handoff_dir.relative_to(project_root)),
    }


def create_handoff_summary_template(
    phase: str,
    agent_role: str,
) -> dict[str, Any]:
    """Create a template for handoff summary."""
    return {
        "phase": phase,
        "agent_role": agent_role,
        "key_findings": [],
        "decisions_made": [],
        "deliverables_status": {},
        "open_issues": [],
        "blockers": [],
        "recommendations_for_next_phase": [],
        "context_for_resume": "",
    }


def format_handoff_report(handoff_data: dict[str, Any]) -> str:
    """Format handoff data as human-readable report."""
    lines = [
        "# Phase Handoff Summary",
        "",
        f"**Phase**: {handoff_data.get('phase', 'unknown')}",
        f"**Agent**: {handoff_data.get('agent_role', 'unknown')}",
        f"**Timestamp**: {handoff_data.get('metadata', {}).get('timestamp', 'unknown')}",
        "",
    ]

    if handoff_data.get("key_findings"):
        lines.append("## Key Findings")
        lines.append("")
        for finding in handoff_data["key_findings"]:
            lines.append(f"- {finding}")
        lines.append("")

    if handoff_data.get("decisions_made"):
        lines.append("## Decisions Made")
        lines.append("")
        for decision in handoff_data["decisions_made"]:
            lines.append(f"- {decision}")
        lines.append("")

    if handoff_data.get("open_issues"):
        lines.append("## Open Issues")
        lines.append("")
        for issue in handoff_data["open_issues"]:
            lines.append(f"- {issue}")
        lines.append("")

    if handoff_data.get("recommendations_for_next_phase"):
        lines.append("## Recommendations for Next Phase")
        lines.append("")
        for rec in handoff_data["recommendations_for_next_phase"]:
            lines.append(f"- {rec}")
        lines.append("")

    if handoff_data.get("context_for_resume"):
        lines.append("## Context for Resume")
        lines.append("")
        lines.append(handoff_data["context_for_resume"])
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Manage phase handoff summaries"
    )
    parser.add_argument("--project-root", required=True, help="Path to project root")
    parser.add_argument(
        "--action",
        choices=["save", "load", "list", "template", "get-phase"],
        required=True,
        help="Action to perform",
    )
    parser.add_argument("--phase", help="Phase identifier (e.g., 01-survey)")
    parser.add_argument("--agent", help="Agent role (e.g., survey, critic)")
    parser.add_argument("--summary", help="Summary content as JSON string")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()

    # Ensure project structure
    ensure_project_structure(project_root, create_if_missing=False)

    if not project_root.exists():
        print(f"Error: Project root does not exist: {project_root}", file=sys.stderr)
        return 1

    if args.action == "save":
        if not args.phase or not args.agent or not args.summary:
            print("Error: --phase, --agent, and --summary required for save", file=sys.stderr)
            return 1

        summary = json.loads(args.summary)
        result = save_handoff_summary(project_root, args.phase, args.agent, summary)

    elif args.action == "load":
        if not args.phase or not args.agent:
            print("Error: --phase and --agent required for load", file=sys.stderr)
            return 1

        result = load_handoff_summary(project_root, args.phase, args.agent)
        if result is None:
            print(f"No handoff summary found for {args.phase}/{args.agent}", file=sys.stderr)
            return 1

    elif args.action == "list":
        result = list_all_handoff_summaries(project_root)

    elif args.action == "template":
        if not args.phase or not args.agent:
            print("Error: --phase and --agent required for template", file=sys.stderr)
            return 1

        result = create_handoff_summary_template(args.phase, args.agent)

    elif args.action == "get-phase":
        if not args.phase:
            print("Error: --phase required for get-phase", file=sys.stderr)
            return 1

        result = get_phase_handoff_summaries(project_root, args.phase)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        if isinstance(result, dict):
            print(format_handoff_report(result))
        else:
            print(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())