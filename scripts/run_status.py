#!/usr/bin/env python3
"""Show live status snapshot for AI Research Orchestrator project.

Usage:
    python3 scripts/run_status.py --project-root /path/to/project
    python3 scripts/run_status.py --project-root /path/to/project --verbose
    python3 scripts/run_status.py --project-root /path/to/project --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from constants import PHASE_SEQUENCE
from quality_gate import evaluate_quality_gate
from reload_project import get_next_actions, load_project_state

# Maps decision key → human label
_DECISION_LABELS: dict[str, str] = {
    "advance": "✅ Advance — ready to proceed to next phase",
    "revise": "🔄 Revise — complete missing work before advancing",
    "pivot": "⚠️  Pivot — consider changing research direction",
    "escalate_to_user": "🔔 Escalate — loop limit reached, human decision required",
}

# Maps blocker key → human explanation
_BLOCKER_MESSAGES: dict[str, str] = {
    "required_deliverables_missing": "Required deliverables are missing",
    "deliverables_still_template": "Some files still contain placeholder text",
    "structured_gate_signals_invalid": "Structured gate signals are invalid",
    "loop_limit_reached": "Phase loop limit reached",
}


def format_phase_bar(current_phase: str) -> str:
    """Return an ASCII phase progress bar with current phase in brackets."""
    parts = []
    for phase in PHASE_SEQUENCE:
        label = phase.capitalize()
        if phase == current_phase:
            parts.append(f"[{label}]")
        else:
            parts.append(label)
    return " → ".join(parts)


def format_gate_scores(scores: dict[str, int]) -> str:
    """Format gate score dict as a readable block."""
    lines = [
        f"  Evidence completeness : {scores.get('evidence_completeness', 0):3d}%",
        f"  Review readiness      : {scores.get('review_readiness', 0):3d}%",
        f"  Human gate            : {scores.get('human_gate', 0):3d}%",
    ]
    return "\n".join(lines)


def get_decision_label(decision: str) -> str:
    """Return a human-readable label for the gate decision."""
    return _DECISION_LABELS.get(decision, decision)


def format_blockers(blockers: list[str]) -> str:
    """Return a formatted list of human-readable blockers."""
    if not blockers:
        return ""
    lines = []
    for b in blockers:
        # Handle dynamic blocker keys like "phase_review_pending"
        if b in _BLOCKER_MESSAGES:
            lines.append(f"  • {_BLOCKER_MESSAGES[b]}")
        elif b.startswith("phase_review_"):
            status = b.replace("phase_review_", "")
            lines.append(f"  • Phase review status: {status}")
        elif b.startswith("user_gate_"):
            status = b.replace("user_gate_", "")
            lines.append(f"  • Human gate status: {status}")
        else:
            lines.append(f"  • {b}")
    return "\n".join(lines)


def run_status(
    project_root: Path,
    verbose: bool = False,
    json_output: bool = False,
) -> dict[str, Any]:
    """Collect and return a status snapshot for the given project.

    Args:
        project_root: Absolute path to the research project root.
        verbose: Include extra detail (missing/existing deliverables).
        json_output: Return JSON-serialisable dict (no formatting changes).

    Returns:
        Status dict with phase, gate, decision, scores, blockers, next_actions.
    """
    project_root = Path(project_root).resolve()
    state = load_project_state(project_root)
    gate_result = evaluate_quality_gate(project_root)
    next_actions = get_next_actions(state)

    result: dict[str, Any] = {
        "phase": gate_result["phase"],
        "gate": gate_result["gate"],
        "decision": gate_result["decision"],
        "scores": gate_result["scores"],
        "blockers": gate_result["blockers"],
        "loop_count": gate_result["loop_count"],
        "loop_limit": gate_result["loop_limit"],
        "next_actions": next_actions,
    }

    if verbose:
        result["existing_deliverables"] = gate_result["existing_deliverables"]
        result["missing_deliverables"] = gate_result["missing_deliverables"]
        result["placeholder_deliverables"] = gate_result["placeholder_deliverables"]

    return result


def format_status_report(result: dict[str, Any]) -> str:
    """Format the status result as a human-readable Markdown report."""
    phase = result["phase"]
    gate = result["gate"]
    decision = result["decision"]
    scores = result["scores"]
    blockers = result["blockers"]
    next_actions = result.get("next_actions", [])
    loop_count = result.get("loop_count", 0)
    loop_limit = result.get("loop_limit", 0)

    lines = [
        "## Research Project Status",
        "",
        f"**Phase:** {phase.capitalize()}  |  "
        f"**Gate:** {gate}  |  "
        f"**Loops:** {loop_count}/{loop_limit}",
        "",
        f"**Progress:** {format_phase_bar(phase)}",
        "",
        "### Gate Scores",
        format_gate_scores(scores),
        "",
        f"**Decision:** {get_decision_label(decision)}",
    ]

    if blockers:
        lines += ["", "### Blockers", format_blockers(blockers)]

    if next_actions:
        lines += ["", "### Next Actions"]
        for i, action in enumerate(next_actions, 1):
            lines.append(f"{i}. {action}")

    # Verbose extras
    if "missing_deliverables" in result and result["missing_deliverables"]:
        lines += ["", "### Missing Deliverables"]
        for d in result["missing_deliverables"]:
            lines.append(f"  - `{d}`")

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Show research project status snapshot")
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--verbose", action="store_true", default=False)
    parser.add_argument("--json", dest="json_output", action="store_true", default=False)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = run_status(args.project_root, verbose=args.verbose, json_output=args.json_output)
        if args.json_output:
            print(json.dumps(result, indent=2))
        else:
            print(format_status_report(result))
        return 0
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print("Hint: run /init-research first, or check --project-root", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
