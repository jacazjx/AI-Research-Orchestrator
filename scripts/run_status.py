#!/usr/bin/env python3
"""Status snapshot for AI Research Orchestrator project.

Returns a dict with phase, gate, decision, scores, blockers, next_actions.
The model handles all formatting and display.

Usage:
    python3 scripts/run_status.py --project-root /path/to/project
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

from orchestrator_common import (  # noqa: E402
    PHASE_TO_GATE,
    allowed_return_phases,
)
from quality_gate import evaluate_quality_gate  # noqa: E402
from reload_project import get_next_actions, load_project_state  # noqa: E402

# Map phases to their execution commands
PHASE_COMMANDS: dict[str, str] = {
    "survey": "/run-survey",
    "pilot": "/run-pilot",
    "experiments": "/run-experiments",
    "paper": "/write-paper",
    "reflection": "/reflect",
}


def _build_available_commands(
    state: dict[str, Any], decision: str, phase: str
) -> list[dict[str, str]]:
    """Build ranked list of available commands for the current state."""
    commands: list[dict[str, str]] = []
    approval = state.get("approval_status", {})
    gate_key = PHASE_TO_GATE.get(phase, "gate_1")
    gate_approved = approval.get(gate_key) == "approved"

    if decision == "advance" and gate_approved:
        # Phase complete, suggest next phase
        from constants.phases import get_next_phase_for_state

        next_phase = get_next_phase_for_state(state)
        if next_phase and next_phase != "06-archive":
            cmd = PHASE_COMMANDS.get(next_phase, f"/run-{next_phase}")
            commands.append({"command": cmd, "reason": f"Gate passed — advance to {next_phase}"})
        elif next_phase == "06-archive":
            commands.append({"command": "/status", "reason": "Project complete"})
    elif decision == "advance" and not gate_approved:
        commands.append(
            {"command": "/status", "reason": f"Gate ready — approve {gate_key} to advance"}
        )
    elif decision == "revise":
        cmd = PHASE_COMMANDS.get(phase, f"/run-{phase}")
        commands.append({"command": cmd, "reason": f"Continue {phase} to address blockers"})
    elif decision == "escalate_to_user":
        commands.append({"command": "/pivot", "reason": "Propose a direction change"})
        commands.append(
            {"command": PHASE_COMMANDS.get(phase, ""), "reason": "Revise with targeted fixes"}
        )
    elif decision == "pivot":
        commands.append({"command": "/pivot", "reason": "Review pending pivot proposals"})

    # Always available
    allowed_returns = allowed_return_phases(phase, state)
    if allowed_returns:
        commands.append(
            {
                "command": f"/run-stage-loop --gate-status rejected --return-phase {allowed_returns[0]}",
                "reason": f"Rollback to {allowed_returns[0]}",
            }
        )
    commands.append({"command": "/configure", "reason": "Adjust project settings"})
    commands.append({"command": "/abandon", "reason": "Archive and exit the project"})

    return commands


def run_status(
    project_root: Path,
    verbose: bool = False,
) -> dict[str, Any]:
    """Collect and return a status snapshot for the given project.

    Args:
        project_root: Absolute path to the research project root.
        verbose: Include extra detail (missing/existing deliverables).

    Returns:
        Status dict with phase, gate, decision, scores, blockers, next_actions,
        and available_commands.
    """
    project_root = Path(project_root).resolve()
    state = load_project_state(project_root)
    gate_result = evaluate_quality_gate(project_root)
    next_actions = get_next_actions(state)
    available_commands = _build_available_commands(
        state, gate_result["decision"], gate_result["phase"]
    )

    result: dict[str, Any] = {
        "phase": gate_result["phase"],
        "gate": gate_result["gate"],
        "decision": gate_result["decision"],
        "scores": gate_result["scores"],
        "blockers": gate_result["blockers"],
        "loop_count": gate_result["loop_count"],
        "loop_limit": gate_result["loop_limit"],
        "next_actions": next_actions,
        "available_commands": available_commands,
    }

    if verbose:
        result["existing_deliverables"] = gate_result["existing_deliverables"]
        result["missing_deliverables"] = gate_result["missing_deliverables"]
        result["placeholder_deliverables"] = gate_result["placeholder_deliverables"]

    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Show research project status snapshot")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Path to the project root. Defaults to the nearest parent containing .autoresearch/.",
    )
    parser.add_argument("--verbose", action="store_true", default=False)
    parser.add_argument("--json", dest="json_output", action="store_true", default=False)
    return parser


def main() -> int:
    args = build_parser().parse_args()

    from utils.path_utils import find_project_root

    project_root: Path | None = args.project_root
    if project_root is not None:
        project_root = project_root.resolve()
        if not (project_root / ".autoresearch").exists():
            project_root = find_project_root(project_root)
    else:
        project_root = find_project_root()

    if project_root is None:
        print(
            "Error: no AI Research project found in the current directory or its parents.",
            file=sys.stderr,
        )
        return 1

    try:
        result = run_status(project_root, verbose=args.verbose)
        print(json.dumps(result, indent=2))
        return 0
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
