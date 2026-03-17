#!/usr/bin/env python3
"""GitMem CLI - Lightweight version control for agent-generated documents.

GitMem provides lightweight version control for agent-generated documents
during the research workflow. It maintains a separate git repository in
.gitmem/ to track changes without polluting the main project history.

Usage:
    python3 scripts/gitmem.py init --project-root <path>
    python3 scripts/gitmem.py commit --project-root <path> --file <file> --message <msg>
    python3 scripts/gitmem.py checkpoint --project-root <path> --name <name>
    python3 scripts/gitmem.py check-loop --project-root <path> --file <file>
    python3 scripts/gitmem.py history --project-root <path> --file <file>
    python3 scripts/gitmem.py diff --project-root <path> --file <file> [--from <rev>] [--to <rev>]
    python3 scripts/gitmem.py rollback --project-root <path> --file <file> [--to <rev>]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Add scripts directory to path for imports
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

from orchestrator_common import (
    gitmem_checkpoint,
    gitmem_check_loop,
    gitmem_commit,
    gitmem_diff,
    gitmem_get_loop_info,
    gitmem_history,
    gitmem_init,
    gitmem_is_initialized,
    gitmem_rollback,
)


def cmd_init(args: argparse.Namespace) -> int:
    """Initialize a .gitmem directory with a separate git repository."""
    project_root = Path(args.project_root).resolve()

    if gitmem_is_initialized(project_root):
        print(f"GitMem already initialized at {project_root / '.gitmem'}")
        return 0

    gitmem_init(project_root)
    print(f"GitMem initialized at {project_root / '.gitmem'}")
    return 0


def cmd_commit(args: argparse.Namespace) -> int:
    """Commit a file change to GitMem history."""
    project_root = Path(args.project_root).resolve()

    if not gitmem_is_initialized(project_root):
        print("Error: GitMem not initialized. Run 'gitmem init' first.", file=sys.stderr)
        return 1

    try:
        commit_hash = gitmem_commit(project_root, args.file, args.message)
        print(commit_hash)
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_checkpoint(args: argparse.Namespace) -> int:
    """Create a named checkpoint (annotated tag)."""
    project_root = Path(args.project_root).resolve()

    if not gitmem_is_initialized(project_root):
        print("Error: GitMem not initialized. Run 'gitmem init' first.", file=sys.stderr)
        return 1

    gitmem_checkpoint(project_root, args.name)
    print(f"Checkpoint created: {args.name}")
    return 0


def cmd_check_loop(args: argparse.Namespace) -> int:
    """Check if a file is in an edit loop."""
    project_root = Path(args.project_root).resolve()

    if not gitmem_is_initialized(project_root):
        result = {"in_loop": False, "change_count": 0, "last_checkpoint": None}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    in_loop = gitmem_check_loop(project_root, args.file)
    loop_info = gitmem_get_loop_info(project_root, args.file)

    result = {
        "in_loop": in_loop,
        "change_count": loop_info["change_count"],
        "last_checkpoint": loop_info["last_checkpoint"],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_history(args: argparse.Namespace) -> int:
    """View version history for a file."""
    project_root = Path(args.project_root).resolve()

    if not gitmem_is_initialized(project_root):
        print("Error: GitMem not initialized. Run 'gitmem init' first.", file=sys.stderr)
        return 1

    history = gitmem_history(project_root, args.file, limit=args.limit)

    if args.json:
        print(json.dumps(history, ensure_ascii=False, indent=2))
    else:
        for entry in history:
            print(f"{entry['hash'][:8]}  {entry['date']}  {entry['message']}")

    return 0


def cmd_diff(args: argparse.Namespace) -> int:
    """Compare versions of a file."""
    project_root = Path(args.project_root).resolve()

    if not gitmem_is_initialized(project_root):
        print("Error: GitMem not initialized. Run 'gitmem init' first.", file=sys.stderr)
        return 1

    diff = gitmem_diff(
        project_root,
        args.file,
        from_rev=args.from_rev,
        to_rev=args.to_rev,
    )
    print(diff)
    return 0


def cmd_rollback(args: argparse.Namespace) -> int:
    """Rollback a file to a previous version."""
    project_root = Path(args.project_root).resolve()

    if not gitmem_is_initialized(project_root):
        print("Error: GitMem not initialized. Run 'gitmem init' first.", file=sys.stderr)
        return 1

    success = gitmem_rollback(project_root, args.file, to_rev=args.to_rev)

    if success:
        print(f"Rolled back {args.file} to {args.to_rev or 'HEAD~1'}")
        return 0
    else:
        print("Error: Rollback failed", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="gitmem",
        description="Lightweight version control for agent-generated documents.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize GitMem repository")
    init_parser.add_argument("--project-root", required=True, help="Project root directory")
    init_parser.set_defaults(func=cmd_init)

    # commit command
    commit_parser = subparsers.add_parser("commit", help="Commit a file change")
    commit_parser.add_argument("--project-root", required=True, help="Project root directory")
    commit_parser.add_argument("--file", required=True, help="File to commit (relative path)")
    commit_parser.add_argument("--message", required=True, help="Commit message")
    commit_parser.set_defaults(func=cmd_commit)

    # checkpoint command
    checkpoint_parser = subparsers.add_parser("checkpoint", help="Create a named checkpoint")
    checkpoint_parser.add_argument("--project-root", required=True, help="Project root directory")
    checkpoint_parser.add_argument("--name", required=True, help="Checkpoint name")
    checkpoint_parser.set_defaults(func=cmd_checkpoint)

    # check-loop command
    check_loop_parser = subparsers.add_parser("check-loop", help="Check for edit loops")
    check_loop_parser.add_argument("--project-root", required=True, help="Project root directory")
    check_loop_parser.add_argument("--file", required=True, help="File to check (relative path)")
    check_loop_parser.set_defaults(func=cmd_check_loop)

    # history command
    history_parser = subparsers.add_parser("history", help="View file version history")
    history_parser.add_argument("--project-root", required=True, help="Project root directory")
    history_parser.add_argument("--file", required=True, help="File to view history for")
    history_parser.add_argument("--limit", type=int, default=20, help="Max entries to show")
    history_parser.add_argument("--json", action="store_true", help="Output as JSON")
    history_parser.set_defaults(func=cmd_history)

    # diff command
    diff_parser = subparsers.add_parser("diff", help="Compare file versions")
    diff_parser.add_argument("--project-root", required=True, help="Project root directory")
    diff_parser.add_argument("--file", required=True, help="File to diff")
    diff_parser.add_argument("--from", dest="from_rev", help="Starting revision")
    diff_parser.add_argument("--to", dest="to_rev", help="Ending revision")
    diff_parser.set_defaults(func=cmd_diff)

    # rollback command
    rollback_parser = subparsers.add_parser("rollback", help="Rollback to previous version")
    rollback_parser.add_argument("--project-root", required=True, help="Project root directory")
    rollback_parser.add_argument("--file", required=True, help="File to rollback")
    rollback_parser.add_argument("--to", dest="to_rev", help="Target revision (default: HEAD~1)")
    rollback_parser.set_defaults(func=cmd_rollback)

    return parser


def main() -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())