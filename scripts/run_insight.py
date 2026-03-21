#!/usr/bin/env python3
"""Run intent clarification for AI Research Orchestrator.

This script provides a standalone entry point for the insight command,
allowing users to clarify their research intent before or during a project.

Usage:
    # Interactive mode
    python3 scripts/run_insight.py

    # With initial idea
    python3 scripts/run_insight.py --idea "Your research idea"

    # Non-interactive (assessment only)
    python3 scripts/run_insight.py --idea "Your idea" --json
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from constants import DEFAULT_DELIVERABLES  # noqa: E402
from orchestrator_common import read_yaml  # noqa: E402

logger = logging.getLogger(__name__)

CLARIFICATION_QUESTIONS = [
    "What specific problem are you trying to solve?",
    "What's your intuition about what might work?",
    "What would constitute a successful outcome?",
]


def detect_project_root(start_path: Path) -> Path | None:
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".autoresearch").exists():
            return current
        current = current.parent
    return None


def get_existing_idea(project_root: Path) -> str | None:
    state_path = project_root / DEFAULT_DELIVERABLES["research_state"]
    if not state_path.exists():
        return None
    state = read_yaml(state_path)
    if state:
        return state.get("topic")
    return None


def assess_idea(idea: str) -> dict[str, Any]:
    word_count = len(idea.split())
    if word_count < 10:
        score = 0.3
        status = "brief"
    elif word_count < 20:
        score = 0.6
        status = "partial"
    else:
        score = 0.9
        status = "clear"
    return {"score": score, "status": status, "word_count": word_count}


def run_interactive_clarification(idea: str) -> dict[str, Any]:
    current_idea = idea
    responses = []

    for i, question in enumerate(CLARIFICATION_QUESTIONS, 1):
        print(f"\nQ{i}: {question}")
        try:
            response = input("> ").strip()
            if response:
                responses.append({"question": question, "answer": response})
                current_idea += f"\n\n[Clarification] {question}\n{response}"
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled")
            break

    assessment = assess_idea(current_idea)
    return {
        "original_idea": idea,
        "clarified_idea": current_idea,
        "clarity_score": assessment["score"],
        "status": assessment["status"],
        "responses": responses,
    }


def run_insight(
    project_root: Path | None = None,
    idea: str | None = None,
    interactive: bool = True,
    json_output: bool = False,
) -> dict[str, Any]:
    if idea is None:
        if project_root:
            idea = get_existing_idea(project_root)
        if idea is None:
            if interactive:
                try:
                    print("\nEnter your research idea:")
                    idea = input("> ").strip()
                except (EOFError, KeyboardInterrupt):
                    return {"status": "cancelled"}
            else:
                return {"status": "error", "error": "No idea provided"}

    assessment = assess_idea(idea)

    if not interactive:
        return {
            "status": "assessed",
            "original_idea": idea,
            "clarified_idea": idea,
            "clarity_score": assessment["score"],
            "word_count": assessment["word_count"],
        }

    print(
        f"\n💡 Idea clarity: {assessment['score']:.1%} ({assessment['word_count']} words)"
    )

    if assessment["status"] == "clear":
        print("✅ Your idea is clear enough to proceed.")
        print("Next step: Run /init-research to initialize your project.")
        return {
            "status": "clear",
            "original_idea": idea,
            "clarified_idea": idea,
            "clarity_score": assessment["score"],
        }

    if assessment["status"] == "brief":
        print("📊 Your idea needs more development.")
        print("Let me ask a few questions to help clarify.")
    else:
        print("📈 Your idea has some detail. Let's refine it further.")

    result = run_interactive_clarification(idea)

    print(f"\n{'=' * 50}")
    print(
        f"Clarity improved: {assessment['score']:.1%} → {result['clarity_score']:.1%}"
    )
    print(f'\nClarified idea:\n"{result["clarified_idea"][:200]}..."')

    if result["clarity_score"] >= 0.7:
        print("\n✅ Clarification complete!")
        print("Next step: Run /init-research to initialize your project.")
    else:
        print("\nConsider using /research-ideation for deeper brainstorming.")

    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run intent clarification for AI Research Orchestrator."
    )
    parser.add_argument("--project-root", help="Path to project root directory.")
    parser.add_argument("--idea", help="Initial research idea to clarify.")
    parser.add_argument(
        "--interactive",
        type=lambda x: x.lower() not in ("false", "0", "no"),
        default=True,
        help="Run in interactive mode (default: true).",
    )
    parser.add_argument("--json", action="store_true", help="Output in JSON format.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    project_root = None
    if args.project_root:
        project_root = Path(args.project_root).resolve()
    else:
        project_root = detect_project_root(Path.cwd())

    try:
        result = run_insight(
            project_root=project_root,
            idea=args.idea,
            interactive=args.interactive,
            json_output=args.json,
        )

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))

        if result.get("status") == "cancelled":
            return 130
        elif result.get("status") == "error":
            return 1
        else:
            return 0

    except Exception as e:
        logger.exception("Failed to run insight")
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
