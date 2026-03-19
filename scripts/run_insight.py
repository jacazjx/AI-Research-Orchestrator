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
    python3 scripts/run_insight.py --idea "Your idea" --interactive false --json
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import local modules
from constants import DEFAULT_DELIVERABLES  # noqa: E402
from intent_clarification import (  # noqa: E402
    BRAINSTORM_THRESHOLD,
    MAX_CLARIFICATION_ROUNDS,
    MIN_CONFIRMATION_SCORE,
    assess_intent_clarity,
    generate_clarification_questions,
)

from orchestrator_common import read_yaml  # noqa: E402

# Configure module logger
logger = logging.getLogger(__name__)


def detect_project_root(start_path: Path) -> Path | None:
    """Detect project root by searching for .autoresearch/ directory.

    Args:
        start_path: Path to start searching from.

    Returns:
        Project root path if found, None otherwise.
    """
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".autoresearch").exists():
            return current
        current = current.parent
    return None


def get_existing_idea(project_root: Path) -> str | None:
    """Get existing research idea from project state.

    Args:
        project_root: Project root directory.

    Returns:
        Existing idea string, or None if not found.
    """
    state_path = project_root / DEFAULT_DELIVERABLES["research_state"]
    if not state_path.exists():
        return None

    state = read_yaml(state_path)
    if state:
        return state.get("topic")
    return None


def format_clarity_bar(score: float, width: int = 20) -> str:
    """Format a clarity score as a progress bar.

    Args:
        score: Score value (0.0-1.0).
        width: Bar width in characters.

    Returns:
        Formatted progress bar string.
    """
    filled = int(score * width)
    empty = width - filled
    return "█" * filled + "░" * empty


def format_assessment_output(
    idea: str,
    assessment: dict[str, Any],
    verbose: bool = False,
) -> str:
    """Format assessment output for display.

    Args:
        idea: The research idea.
        assessment: Assessment dictionary.
        verbose: Whether to include detailed information.

    Returns:
        Formatted output string.
    """
    lines = []
    lines.append("💡 意图澄清助手")
    lines.append("━" * 50)
    lines.append("")

    # Current idea
    lines.append("当前研究想法:")
    lines.append(f'"{idea}"')
    lines.append("")

    # Overall score
    score = assessment["score"]
    if score >= MIN_CONFIRMATION_SCORE:
        status = "✅ 清晰"
    elif score >= BRAINSTORM_THRESHOLD:
        status = "⚠️  需要澄清"
    else:
        status = "❌ 需要brainstorming"

    lines.append(f"清晰度评估: {score:.2f}/1.0 ({status})")
    lines.append("")

    # Dimension scores
    dim_labels = {
        "problem": "Problem",
        "solution": "Solution",
        "contribution": "Contribution",
        "constraints": "Constraints",
        "novelty": "Novelty",
    }

    lines.append("维度评分:")
    for dim, dim_score in assessment["dimension_scores"].items():
        label = dim_labels.get(dim, dim)
        bar = format_clarity_bar(dim_score)
        lines.append(f"  {label:12} {dim_score:.1f} {bar}")

    lines.append("")

    # Gaps
    if assessment["gaps"]:
        lines.append("需要改进:")
        for gap in assessment["gaps"][:3]:  # Limit to 3 gaps
            lines.append(f"  • {gap}")
        lines.append("")

    # Suggested action
    action = assessment["suggested_action"]
    if action == "brainstorm":
        lines.append("建议: 使用 research-ideation 技能进行头脑风暴")
    elif action == "clarify":
        lines.append("建议: 继续澄清回答问题")
    else:
        lines.append("建议: 可以开始研究")

    if verbose:
        lines.append("")
        lines.append("详细分析:")
        lines.append(assessment["reasoning"])

    return "\n".join(lines)


def format_questions_output(questions: list[str], round_num: int) -> str:
    """Format questions for display.

    Args:
        questions: List of questions.
        round_num: Current round number.

    Returns:
        Formatted questions string.
    """
    lines = []
    lines.append(f"\n📝 澄清问题 (第 {round_num} 轮)")
    lines.append("━" * 50)

    for i, q in enumerate(questions, 1):
        lines.append(f"\nQ{i}: {q}")

    lines.append("")
    return "\n".join(lines)


def run_interactive_clarification(
    idea: str,
    max_rounds: int = MAX_CLARIFICATION_ROUNDS,
    language: str = "zh",
) -> dict[str, Any]:
    """Run interactive clarification loop.

    Args:
        idea: Initial research idea.
        max_rounds: Maximum number of clarification rounds.
        language: Language for questions.

    Returns:
        Dictionary with clarification results.
    """
    current_idea = idea
    rounds_data = []

    for round_num in range(1, max_rounds + 1):
        # Assess current clarity
        assessment = assess_intent_clarity(current_idea)

        # Check if we're done
        if assessment.score >= MIN_CONFIRMATION_SCORE:
            return {
                "original_idea": idea,
                "clarified_idea": current_idea,
                "clarity_score": assessment.score,
                "dimension_scores": assessment.dimension_scores,
                "rounds": rounds_data,
                "confirmed": True,
                "needs_brainstorming": False,
                "status": "clarified",
            }

        # Check if brainstorming needed
        if assessment.score < BRAINSTORM_THRESHOLD:
            return {
                "original_idea": idea,
                "clarified_idea": current_idea,
                "clarity_score": assessment.score,
                "dimension_scores": assessment.dimension_scores,
                "rounds": rounds_data,
                "confirmed": False,
                "needs_brainstorming": True,
                "status": "needs_brainstorming",
            }

        # Generate questions
        questions = generate_clarification_questions(
            current_idea,
            assessment.gaps,
            assessment.dimension_scores,
            language,
        )

        # Display questions
        print(format_questions_output(questions, round_num))

        # Collect responses
        responses = []
        for i, q in enumerate(questions, 1):
            try:
                response = input("> ").strip()
                responses.append(response)
            except (EOFError, KeyboardInterrupt):
                print("\n操作已取消")
                return {
                    "original_idea": idea,
                    "clarified_idea": current_idea,
                    "clarity_score": assessment.score,
                    "dimension_scores": assessment.dimension_scores,
                    "rounds": rounds_data,
                    "confirmed": False,
                    "needs_brainstorming": False,
                    "status": "cancelled",
                }

        # Synthesize responses into updated idea
        if responses:
            # Simple synthesis: append key points to idea
            new_points = []
            for r in responses:
                if r and len(r) > 10:
                    # Extract key part of response
                    new_points.append(r[:100])  # Limit length

            if new_points:
                current_idea = f"{current_idea}\n\n补充信息:\n" + "\n".join(
                    f"- {p}" for p in new_points
                )

        # Record round
        rounds_data.append(
            {
                "round_number": round_num,
                "questions": questions,
                "responses": responses,
                "clarity_before": assessment.score,
            }
        )

    # Max rounds reached
    final_assessment = assess_intent_clarity(current_idea)
    return {
        "original_idea": idea,
        "clarified_idea": current_idea,
        "clarity_score": final_assessment.score,
        "dimension_scores": final_assessment.dimension_scores,
        "rounds": rounds_data,
        "confirmed": final_assessment.score >= MIN_CONFIRMATION_SCORE,
        "needs_brainstorming": final_assessment.score < BRAINSTORM_THRESHOLD,
        "status": "max_rounds_reached",
    }


def run_insight(
    project_root: Path | None = None,
    idea: str | None = None,
    interactive: bool = True,
    max_rounds: int = MAX_CLARIFICATION_ROUNDS,
    json_output: bool = False,
) -> dict[str, Any]:
    """Run intent clarification.

    Args:
        project_root: Optional project root directory.
        idea: Optional initial research idea.
        interactive: Whether to run in interactive mode.
        max_rounds: Maximum number of clarification rounds.
        json_output: Whether to output as JSON.

    Returns:
        Dictionary with clarification results.
    """
    # Determine idea source
    if idea is None:
        if project_root:
            idea = get_existing_idea(project_root)
            if idea is None:
                if interactive:
                    try:
                        print("\n请输入您的研究想法:")
                        idea = input("> ").strip()
                    except (EOFError, KeyboardInterrupt):
                        print("\n操作已取消")
                        return {"status": "cancelled"}
                else:
                    return {
                        "status": "error",
                        "error": "No idea provided and no project found",
                    }
        else:
            if interactive:
                try:
                    print("\n请输入您的研究想法:")
                    idea = input("> ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\n操作已取消")
                    return {"status": "cancelled"}
            else:
                return {
                    "status": "error",
                    "error": "No idea provided",
                }

    # Initial assessment
    assessment = assess_intent_clarity(idea)

    # Non-interactive mode: just return assessment
    if not interactive:
        return {
            "status": "assessed",
            "original_idea": idea,
            "clarified_idea": idea,
            "clarity_score": assessment.score,
            "dimension_scores": assessment.dimension_scores,
            "needs_brainstorming": assessment.score < BRAINSTORM_THRESHOLD,
        }

    # Display initial assessment
    print(format_assessment_output(idea, assessment.to_dict()))

    # Check if already clear or needs brainstorming
    if assessment.score >= MIN_CONFIRMATION_SCORE:
        print("\n✅ 您的研究想法足够清晰，可以开始研究。")
        print("建议: 运行 /init-research 初始化项目")
        return {
            "status": "already_clear",
            "original_idea": idea,
            "clarified_idea": idea,
            "clarity_score": assessment.score,
            "dimension_scores": assessment.dimension_scores,
            "confirmed": True,
            "needs_brainstorming": False,
        }

    if assessment.score < BRAINSTORM_THRESHOLD:
        print("\n❌ 您的研究想法需要进一步发展。")
        print("建议: 使用 research-ideation 技能进行头脑风暴")
        return {
            "status": "needs_brainstorming",
            "original_idea": idea,
            "clarified_idea": idea,
            "clarity_score": assessment.score,
            "dimension_scores": assessment.dimension_scores,
            "confirmed": False,
            "needs_brainstorming": True,
        }

    # Run interactive clarification
    print("\n让我问您几个问题来澄清您的研究想法...")
    result = run_interactive_clarification(idea, max_rounds)

    # Display final result
    print("\n" + "━" * 50)
    print("澄清后的研究想法:")
    print(f'"{result["clarified_idea"]}"')
    print(f"\n清晰度评分: {result["clarity_score"]:.2f}/1.0")

    if result["confirmed"]:
        print("\n✅ 澄清完成!")
        print("建议下一步:")
        print("1. 运行 /init-research 初始化项目")
    elif result["needs_brainstorming"]:
        print("\n建议进行头脑风暴来进一步发展想法。")
    else:
        print("\n可以继续澄清或直接开始研究。")

    return result


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser."""
    parser = argparse.ArgumentParser(
        description="Run intent clarification for AI Research Orchestrator."
    )
    parser.add_argument(
        "--project-root",
        help="Path to the AI Research project root directory (optional).",
    )
    parser.add_argument(
        "--idea",
        help="Initial research idea to clarify.",
    )
    parser.add_argument(
        "--interactive",
        type=lambda x: x.lower() not in ("false", "0", "no"),
        default=True,
        help="Run in interactive mode (default: true).",
    )
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=MAX_CLARIFICATION_ROUNDS,
        help=f"Maximum clarification rounds (default: {MAX_CLARIFICATION_ROUNDS}).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format.",
    )
    return parser


def main() -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args()

    # Resolve project root
    project_root = None
    if args.project_root:
        project_root = Path(args.project_root).resolve()
    else:
        # Try to auto-detect
        project_root = detect_project_root(Path.cwd())
        if project_root:
            logger.info("Auto-detected project root: %s", project_root)

    try:
        result = run_insight(
            project_root=project_root,
            idea=args.idea,
            interactive=args.interactive,
            max_rounds=args.max_rounds,
            json_output=args.json,
        )

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))

        # Return appropriate exit code
        if result.get("status") == "cancelled":
            return 130  # Standard exit code for SIGINT
        elif result.get("status") == "error":
            return 1
        elif result.get("confirmed"):
            return 0
        elif result.get("needs_brainstorming"):
            return 2  # Special code for brainstorming needed
        else:
            return 0

    except Exception as e:
        logger.exception("Failed to run insight")
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
