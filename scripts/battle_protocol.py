#!/usr/bin/env python3
"""Battle Protocol: State machine for Primary/Reviewer agent debate."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# sys.path setup to find sibling scripts
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# File I/O helpers
# ---------------------------------------------------------------------------


def _debate_path(project_root: Path, primary_agent: str) -> Path:
    """Return path to debate.json for the given primary agent."""
    return project_root / "agents" / primary_agent / "battle" / "debate.json"


def _read_debate(path: Path) -> dict[str, Any]:
    """Read and parse debate.json."""
    if not path.exists():
        raise FileNotFoundError(f"debate.json not found at {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _write_debate(path: Path, state: dict[str, Any]) -> None:
    """Write debate state to debate.json with atomic write pattern."""
    import os
    import tempfile

    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(state, ensure_ascii=False, indent=2) + "\n"

    fd, temp_path = tempfile.mkstemp(dir=path.parent, prefix="debate.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(temp_path, path)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


def _now_iso() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# State machine actions
# ---------------------------------------------------------------------------


def init_battle(
    project_root: Path,
    phase: str,
    primary_agent: str,
    reviewer_agent: str,
) -> dict[str, Any]:
    """Initialize a new battle. Creates debate.json. Returns state dict."""
    state: dict[str, Any] = {
        "schema_version": "1.0",
        "phase": phase,
        "primary_agent": primary_agent,
        "reviewer_agent": reviewer_agent,
        "status": "pending",
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
        "turns": [],
        "unresolved_issues": [],
        "resolved_issues": [],
        "verdict": None,
    }
    path = _debate_path(project_root, primary_agent)
    _write_debate(path, state)
    logger.debug("Initialized battle at %s", path)
    return state


def submit_challenge(
    project_root: Path,
    primary_agent: str,
    disputed_points: list[dict[str, Any]],
) -> dict[str, Any]:
    """Primary submits challenge against reviewer's findings.

    disputed_points schema:
        [{"point_id": "P1", "original_claim": "...",
          "challenge_reason": "...", "proposed_alternative": "..."}]
    """
    path = _debate_path(project_root, primary_agent)
    state = _read_debate(path)

    turn: dict[str, Any] = {
        "turn_index": len(state["turns"]),
        "type": "challenge",
        "agent": primary_agent,
        "timestamp": _now_iso(),
        "disputed_points": disputed_points,
    }
    state["turns"].append(turn)
    state["status"] = "debating"
    state["updated_at"] = _now_iso()

    # Add points to unresolved_issues (avoid duplicates by point_id)
    existing_ids = {issue["point_id"] for issue in state["unresolved_issues"]}
    for point in disputed_points:
        if point.get("point_id") not in existing_ids:
            state["unresolved_issues"].append(point)
            existing_ids.add(point["point_id"])

    _write_debate(path, state)
    logger.debug(
        "Challenge submitted by %s: %d disputed points",
        primary_agent,
        len(disputed_points),
    )
    return state


def submit_response(
    project_root: Path,
    reviewer_agent: str,
    point_responses: list[dict[str, Any]],
) -> dict[str, Any]:
    """Reviewer responds to challenge.

    point_responses schema:
        [{"point_id": "P1", "action": "accept|reject|modify",
          "reason": "...", "modified_position": "..."}]

    For "accept" actions the point is moved from unresolved_issues to
    resolved_issues.
    """
    # Locate debate.json by searching for the reviewer's counterpart.
    # The debate.json lives under the primary agent's directory, so we need to
    # find which primary agent this reviewer is paired with.  We search all
    # existing debate.json files and find one whose reviewer_agent matches.
    battle_base = project_root / "agents"
    matched_path: Path | None = None
    if battle_base.exists():
        candidates = sorted(
            battle_base.glob("*/battle/debate.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        for candidate in candidates:
            try:
                data = json.loads(candidate.read_text(encoding="utf-8"))
                if data.get("reviewer_agent") == reviewer_agent:
                    matched_path = candidate
                    break
            except Exception:
                continue

    if matched_path is None:
        raise FileNotFoundError(
            f"No active debate.json found for reviewer_agent '{reviewer_agent}'"
        )

    state = json.loads(matched_path.read_text(encoding="utf-8"))

    turn: dict[str, Any] = {
        "turn_index": len(state["turns"]),
        "type": "response",
        "agent": reviewer_agent,
        "timestamp": _now_iso(),
        "point_responses": point_responses,
    }
    state["turns"].append(turn)
    state["updated_at"] = _now_iso()

    # Resolve accepted points
    accepted_ids = {r["point_id"] for r in point_responses if r.get("action") == "accept"}
    if accepted_ids:
        remaining: list[dict[str, Any]] = []
        for issue in state["unresolved_issues"]:
            if issue["point_id"] in accepted_ids:
                resolved_entry = dict(issue)
                resolved_entry["resolution"] = "accepted"
                resolved_entry["resolved_at"] = _now_iso()
                # Attach the matching response for context
                for r in point_responses:
                    if r["point_id"] == issue["point_id"]:
                        resolved_entry["reviewer_response"] = r
                        break
                state["resolved_issues"].append(resolved_entry)
            else:
                remaining.append(issue)
        state["unresolved_issues"] = remaining

    _write_debate(matched_path, state)
    logger.debug(
        "Response submitted by %s: %d accepted, %d still unresolved",
        reviewer_agent,
        len(accepted_ids),
        len(state["unresolved_issues"]),
    )
    return state


def check_consensus(project_root: Path, primary_agent: str) -> dict[str, Any]:
    """Check if consensus has been reached (no unresolved issues).

    Returns:
        {"consensus": bool, "unresolved_count": int, "resolved_count": int}
    """
    path = _debate_path(project_root, primary_agent)
    state = _read_debate(path)

    unresolved_count = len(state["unresolved_issues"])
    resolved_count = len(state["resolved_issues"])
    consensus = (
        unresolved_count == 0
        and state["status"] in {"debating", "pending"}
        and len(state.get("turns", [])) > 0
    )

    return {
        "consensus": consensus,
        "unresolved_count": unresolved_count,
        "resolved_count": resolved_count,
        "status": state["status"],
    }


def arbitrate(
    project_root: Path,
    primary_agent: str,
    decision: str,
    reasoning: str,
    required_actions: list[str],
) -> dict[str, Any]:
    """Orchestrator issues verdict.

    decision: "approve" | "revise" | "reject"
    Sets status to "completed" and populates the verdict field.
    Returns final state.
    """
    valid_decisions = {"approve", "revise", "reject"}
    if decision not in valid_decisions:
        raise ValueError(
            f"Invalid decision '{decision}'. Must be one of: {sorted(valid_decisions)}"
        )

    path = _debate_path(project_root, primary_agent)
    state = _read_debate(path)

    state["verdict"] = {
        "decision": decision,
        "reasoning": reasoning,
        "required_actions": required_actions,
        "issued_at": _now_iso(),
    }
    state["status"] = "completed"
    state["updated_at"] = _now_iso()

    _write_debate(path, state)
    logger.debug("Arbitration issued for %s: decision=%s", primary_agent, decision)
    return state


def get_battle_status(project_root: Path, primary_agent: str) -> dict[str, Any]:
    """Return current battle state."""
    path = _debate_path(project_root, primary_agent)
    return _read_debate(path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Battle Protocol: state machine for Primary/Reviewer agent debate."
    )
    parser.add_argument(
        "--project-root",
        required=True,
        help="Absolute path to the project root directory.",
    )
    parser.add_argument(
        "--action",
        required=True,
        choices=["init", "challenge", "respond", "consensus", "arbitrate", "status"],
        help="Action to perform.",
    )
    parser.add_argument(
        "--agent",
        help="Agent name (primary agent for most actions, reviewer for 'respond').",
    )
    parser.add_argument(
        "--phase",
        help="Phase name (required for --action init).",
    )
    parser.add_argument(
        "--primary",
        help="Primary agent name (required for --action init).",
    )
    parser.add_argument(
        "--reviewer",
        help="Reviewer agent name (required for --action init).",
    )
    parser.add_argument(
        "--points",
        help="JSON array of disputed points (required for --action challenge).",
    )
    parser.add_argument(
        "--responses",
        help="JSON array of point responses (required for --action respond).",
    )
    parser.add_argument(
        "--decision",
        choices=["approve", "revise", "reject"],
        help="Arbitration decision (required for --action arbitrate).",
    )
    parser.add_argument(
        "--reasoning",
        help="Reasoning for arbitration decision (required for --action arbitrate).",
    )
    parser.add_argument(
        "--actions",
        help="JSON array of required actions (required for --action arbitrate).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON.",
    )
    return parser


def _print_human_readable(action: str, result: Any) -> None:
    """Print a human-readable summary of the result."""
    if action == "init":
        print("Battle initialized.")
        print(f"  Phase:    {result['phase']}")
        print(f"  Primary:  {result['primary_agent']}")
        print(f"  Reviewer: {result['reviewer_agent']}")
        print(f"  Status:   {result['status']}")
        print(f"  Created:  {result['created_at']}")

    elif action == "challenge":
        print("Challenge submitted.")
        print(f"  Status:             {result['status']}")
        print(f"  Unresolved issues:  {len(result['unresolved_issues'])}")
        print(f"  Total turns:        {len(result['turns'])}")

    elif action == "respond":
        print("Response submitted.")
        print(f"  Unresolved issues:  {len(result['unresolved_issues'])}")
        print(f"  Resolved issues:    {len(result['resolved_issues'])}")
        print(f"  Total turns:        {len(result['turns'])}")

    elif action == "consensus":
        consensus_str = "YES" if result["consensus"] else "NO"
        print(f"Consensus reached: {consensus_str}")
        print(f"  Unresolved issues: {result['unresolved_count']}")
        print(f"  Resolved issues:   {result['resolved_count']}")
        print(f"  Status:            {result['status']}")

    elif action == "arbitrate":
        verdict = result.get("verdict") or {}
        print("Arbitration issued.")
        print(f"  Decision:  {verdict.get('decision')}")
        print(f"  Status:    {result['status']}")
        actions_list = verdict.get("required_actions", [])
        if actions_list:
            print("  Required actions:")
            for act in actions_list:
                print(f"    - {act}")

    elif action == "status":
        verdict = result.get("verdict") or {}
        print(f"Battle status: {result['status']}")
        print(f"  Phase:             {result['phase']}")
        print(f"  Primary agent:     {result['primary_agent']}")
        print(f"  Reviewer agent:    {result['reviewer_agent']}")
        print(f"  Turns:             {len(result['turns'])}")
        print(f"  Unresolved issues: {len(result['unresolved_issues'])}")
        print(f"  Resolved issues:   {len(result['resolved_issues'])}")
        if verdict:
            print(f"  Verdict decision:  {verdict.get('decision')}")
        print(f"  Updated:           {result['updated_at']}")

    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


def main() -> int:
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s: %(message)s",
    )

    parser = build_parser()
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()

    try:
        result: Any

        if args.action == "init":
            if not args.phase:
                parser.error("--phase is required for --action init")
            if not args.primary:
                parser.error("--primary is required for --action init")
            if not args.reviewer:
                parser.error("--reviewer is required for --action init")
            result = init_battle(
                project_root=project_root,
                phase=args.phase,
                primary_agent=args.primary,
                reviewer_agent=args.reviewer,
            )

        elif args.action == "challenge":
            if not args.agent:
                parser.error("--agent is required for --action challenge")
            if not args.points:
                parser.error("--points is required for --action challenge")
            try:
                disputed_points = json.loads(args.points)
            except json.JSONDecodeError as exc:
                print(f"ERROR: --points is not valid JSON: {exc}", file=sys.stderr)
                return 1
            result = submit_challenge(
                project_root=project_root,
                primary_agent=args.agent,
                disputed_points=disputed_points,
            )

        elif args.action == "respond":
            if not args.agent:
                parser.error("--agent is required for --action respond")
            if not args.responses:
                parser.error("--responses is required for --action respond")
            try:
                point_responses = json.loads(args.responses)
            except json.JSONDecodeError as exc:
                print(f"ERROR: --responses is not valid JSON: {exc}", file=sys.stderr)
                return 1
            result = submit_response(
                project_root=project_root,
                reviewer_agent=args.agent,
                point_responses=point_responses,
            )

        elif args.action == "consensus":
            if not args.agent:
                parser.error("--agent is required for --action consensus")
            result = check_consensus(
                project_root=project_root,
                primary_agent=args.agent,
            )

        elif args.action == "arbitrate":
            if not args.agent:
                parser.error("--agent is required for --action arbitrate")
            if not args.decision:
                parser.error("--decision is required for --action arbitrate")
            if not args.reasoning:
                parser.error("--reasoning is required for --action arbitrate")
            required_actions: list[str] = []
            if args.actions:
                try:
                    required_actions = json.loads(args.actions)
                except json.JSONDecodeError as exc:
                    print(f"ERROR: --actions is not valid JSON: {exc}", file=sys.stderr)
                    return 1
            result = arbitrate(
                project_root=project_root,
                primary_agent=args.agent,
                decision=args.decision,
                reasoning=args.reasoning,
                required_actions=required_actions,
            )

        elif args.action == "status":
            if not args.agent:
                parser.error("--agent is required for --action status")
            result = get_battle_status(
                project_root=project_root,
                primary_agent=args.agent,
            )

        else:
            # Should be unreachable due to choices= constraint
            print(f"ERROR: Unknown action '{args.action}'", file=sys.stderr)
            return 1

    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: Unexpected failure: {exc}", file=sys.stderr)
        logger.exception("Unexpected error in battle_protocol")
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_human_readable(args.action, result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
