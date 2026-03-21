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

from quality_gate import evaluate_quality_gate  # noqa: E402
from reload_project import get_next_actions, load_project_state  # noqa: E402


def run_status(
    project_root: Path,
    verbose: bool = False,
) -> dict[str, Any]:
    """Collect and return a status snapshot for the given project.

    Args:
        project_root: Absolute path to the research project root.
        verbose: Include extra detail (missing/existing deliverables).

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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Show research project status snapshot"
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Path to the project root. Defaults to the nearest parent containing .autoresearch/.",
    )
    parser.add_argument("--verbose", action="store_true", default=False)
    parser.add_argument(
        "--json", dest="json_output", action="store_true", default=False
    )
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
