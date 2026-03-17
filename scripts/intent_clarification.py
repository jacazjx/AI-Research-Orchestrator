#!/usr/bin/env python3
"""Intent clarification module for AI Research Orchestrator.

This module provides functionality to assess research intent clarity and
run clarification loops to ensure mutual understanding between the
orchestrator and researcher.

Key Functions:
    - assess_intent_clarity: Evaluate clarity of research idea
    - generate_clarification_questions: Generate targeted questions
    - run_clarification_loop: Execute iterative clarification

Usage:
    from intent_clarification import assess_intent_clarity, run_clarification_loop

    assessment = assess_intent_clarity(idea, context)
    if assessment.score < 0.4:
        # Trigger brainstorming
        ...
    else:
        result = run_clarification_loop(project_root, idea, context)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

# Constants
MAX_CLARIFICATION_ROUNDS = 5
MIN_CONFIRMATION_SCORE = 0.7
BRAINSTORM_THRESHOLD = 0.4

# Dimension weights for clarity scoring
DIMENSION_WEIGHTS = {
    "problem": 0.25,
    "solution": 0.25,
    "contribution": 0.20,
    "constraints": 0.15,
    "novelty": 0.15,
}

# First-principles question bank
QUESTION_BANK: dict[str, list[dict[str, str]]] = {
    "problem": [
        {
            "en": "What specific problem are you trying to solve?",
            "zh": "你试图解决的具体问题是什么？",
            "followup": "Can you be more specific about the problem scope?",
        },
        {
            "en": "Why is this problem important? What's the impact?",
            "zh": "这个问题为什么重要？有什么影响？",
            "followup": "Who would benefit most from solving this?",
        },
        {
            "en": "What happens if this problem isn't solved?",
            "zh": "如果不解决这个问题会怎样？",
            "followup": "Is there a deadline or critical timeline?",
        },
    ],
    "solution": [
        {
            "en": "What attempts have been made? Why aren't they good enough?",
            "zh": "之前有哪些尝试？为什么不够好？",
            "followup": "What specifically was lacking in prior approaches?",
        },
        {
            "en": "What's your intuition about what might work?",
            "zh": "你的直觉是什么方法可能有效？",
            "followup": "What evidence supports this intuition?",
        },
        {
            "en": "What constraints limit possible solutions?",
            "zh": "有什么约束限制可能的解决方案？",
            "followup": "Are these constraints hard or soft?",
        },
    ],
    "contribution": [
        {
            "en": "What type of contribution do you want to make?",
            "zh": "你希望做出什么类型的贡献？",
            "followup": "Is this a method, theory, application, or benchmark contribution?",
        },
        {
            "en": "What would constitute a successful outcome?",
            "zh": "什么样的成果算成功？",
            "followup": "Can you define specific success metrics?",
        },
        {
            "en": "What's the minimum viable contribution?",
            "zh": "最小可行贡献是什么？",
            "followup": "What's the absolute minimum that would be valuable?",
        },
    ],
    "constraints": [
        {
            "en": "What's the target venue?",
            "zh": "目标期刊/会议是什么？",
            "followup": "Is there a specific deadline?",
        },
        {
            "en": "What's the timeline?",
            "zh": "时间线是怎样的？",
            "followup": "Are there hard deadlines or milestones?",
        },
        {
            "en": "What compute resources and data are available?",
            "zh": "有什么计算资源和数据可用？",
            "followup": "Are there any budget constraints?",
        },
    ],
    "novelty": [
        {
            "en": "What's your key insight or idea?",
            "zh": "你的关键洞察或想法是什么？",
            "followup": "What makes this insight unique?",
        },
        {
            "en": "Which assumptions in existing work can be challenged?",
            "zh": "现有工作的哪些假设可以被挑战？",
            "followup": "What happens if those assumptions don't hold?",
        },
        {
            "en": "Is there similar work? If so, how is yours different?",
            "zh": "有没有类似的工作？如果有，你的不同之处？",
            "followup": "Can you articulate the key differentiator?",
        },
    ],
}

# Keywords for evaluating idea content
PROBLEM_KEYWORDS = [
    "problem",
    "issue",
    "challenge",
    "solve",
    "address",
    "improve",
    "问题",
    "挑战",
    "解决",
    "改进",
]

SOLUTION_KEYWORDS = [
    "approach",
    "method",
    "technique",
    "algorithm",
    "model",
    "framework",
    "方法",
    "算法",
    "模型",
    "框架",
    "技术",
]

CONTRIBUTION_KEYWORDS = [
    "contribution",
    "novel",
    "new",
    "propose",
    "introduce",
    "贡献",
    "创新",
    "新",
    "提出",
]

CONSTRAINT_KEYWORDS = [
    "deadline",
    "timeline",
    "resource",
    "gpu",
    "data",
    "budget",
    "期限",
    "资源",
    "预算",
]

NOVELTY_KEYWORDS = [
    "novelty",
    "unique",
    "different",
    "insight",
    "innovation",
    "新颖",
    "独特",
    "不同",
    "创新",
    "洞察",
]


@dataclass
class ClarityAssessment:
    """Result of intent clarity assessment.

    Attributes:
        score: Overall clarity score (0.0-1.0).
        dimension_scores: Scores for each dimension.
        gaps: Identified information gaps.
        suggested_action: Recommended next action.
        reasoning: Explanation of the assessment.
    """

    score: float
    dimension_scores: dict[str, float] = field(default_factory=dict)
    gaps: list[str] = field(default_factory=list)
    suggested_action: str = "clarify"
    reasoning: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "score": self.score,
            "dimension_scores": self.dimension_scores,
            "gaps": self.gaps,
            "suggested_action": self.suggested_action,
            "reasoning": self.reasoning,
        }


@dataclass
class ClarificationRound:
    """A single round of clarification Q&A.

    Attributes:
        round_number: Round number (1-indexed).
        questions: Questions asked.
        responses: User responses.
        clarity_before: Clarity score before this round.
        clarity_after: Clarity score after this round.
        timestamp: When this round occurred.
    """

    round_number: int
    questions: list[str]
    responses: list[str]
    clarity_before: float
    clarity_after: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "round_number": self.round_number,
            "questions": self.questions,
            "responses": self.responses,
            "clarity_before": self.clarity_before,
            "clarity_after": self.clarity_after,
            "timestamp": self.timestamp,
        }


@dataclass
class ClarificationResult:
    """Result of the clarification process.

    Attributes:
        original_idea: The initial research idea.
        clarified_idea: The clarified research idea.
        clarity_score: Final clarity score.
        rounds: List of clarification rounds.
        confirmed: Whether the intent was confirmed.
        needs_brainstorming: Whether brainstorming is recommended.
    """

    original_idea: str
    clarified_idea: str
    clarity_score: float
    rounds: list[ClarificationRound] = field(default_factory=list)
    confirmed: bool = False
    needs_brainstorming: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "original_idea": self.original_idea,
            "clarified_idea": self.clarified_idea,
            "clarity_score": self.clarity_score,
            "rounds": [r.to_dict() for r in self.rounds],
            "confirmed": self.confirmed,
            "needs_brainstorming": self.needs_brainstorming,
        }


def _evaluate_dimension(
    idea: str,
    dimension: str,
    context: dict[str, Any],
) -> tuple[float, list[str]]:
    """Evaluate a single dimension of clarity.

    Args:
        idea: The research idea text.
        dimension: Dimension name (problem, solution, etc.).
        context: Additional context information.

    Returns:
        Tuple of (score, list of gaps identified).
    """
    idea_lower = idea.lower()
    keywords_map = {
        "problem": PROBLEM_KEYWORDS,
        "solution": SOLUTION_KEYWORDS,
        "contribution": CONTRIBUTION_KEYWORDS,
        "constraints": CONSTRAINT_KEYWORDS,
        "novelty": NOVELTY_KEYWORDS,
    }

    keywords = keywords_map.get(dimension, [])
    gaps = []

    # Check for keyword presence
    keyword_matches = sum(1 for kw in keywords if kw in idea_lower)
    keyword_score = min(1.0, keyword_matches / 2.0)  # 2 keywords = full score

    # Check for specificity indicators
    specificity_indicators = {
        "problem": ["specifically", "exactly", "precisely", "具体", "明确"],
        "solution": ["using", "by", "through", "approach", "用", "通过", "方法"],
        "contribution": ["contribute", "provide", "offer", "贡献", "提供"],
        "constraints": ["within", "limited", "deadline", "以内", "限制", "期限"],
        "novelty": ["unlike", "different from", "compared to", "不同于", "相比"],
    }

    indicators = specificity_indicators.get(dimension, [])
    specificity_matches = sum(1 for ind in indicators if ind in idea_lower)
    specificity_score = min(1.0, specificity_matches / 1.0)

    # Check context for this dimension
    context_score = 0.0
    if dimension == "constraints" and context:
        if context.get("timeline") or context.get("deadline"):
            context_score = 0.3
        if context.get("venue"):
            context_score += 0.3
        if context.get("resources"):
            context_score += 0.4

    # Calculate dimension score
    base_score = 0.4 * keyword_score + 0.4 * specificity_score + 0.2 * context_score

    # Identify gaps
    if keyword_score < 0.5:
        gaps.append(f"Missing {dimension} keywords - unclear {dimension} definition")
    if specificity_score < 0.5:
        gaps.append(f"Vague {dimension} statement - needs more specificity")

    return base_score, gaps


def assess_intent_clarity(
    idea: str,
    context: dict[str, Any] | None = None,
) -> ClarityAssessment:
    """Assess the clarity of a research idea.

    Evaluates the idea across five dimensions and returns an overall
    clarity score with suggested actions.

    Args:
        idea: The research idea or problem statement.
        context: Optional context (venue, timeline, resources, etc.).

    Returns:
        ClarityAssessment with score, dimension scores, gaps, and suggestions.
    """
    if context is None:
        context = {}

    # Check for empty or very short idea
    if not idea or len(idea.strip()) < 20:
        return ClarityAssessment(
            score=0.0,
            dimension_scores={dim: 0.0 for dim in DIMENSION_WEIGHTS},
            gaps=["Research idea is too short or empty"],
            suggested_action="brainstorm",
            reasoning="The research idea needs substantial development.",
        )

    # Evaluate each dimension
    dimension_scores = {}
    all_gaps = []

    for dimension in DIMENSION_WEIGHTS:
        score, gaps = _evaluate_dimension(idea, dimension, context)
        dimension_scores[dimension] = score
        all_gaps.extend(gaps)

    # Calculate weighted overall score
    overall_score = sum(dimension_scores[dim] * weight for dim, weight in DIMENSION_WEIGHTS.items())

    # Determine suggested action
    if overall_score < BRAINSTORM_THRESHOLD:
        suggested_action = "brainstorm"
        reasoning = (
            f"Clarity score ({overall_score:.2f}) is below threshold ({BRAINSTORM_THRESHOLD}). "
            "Recommend using research-ideation skill to develop the idea."
        )
    elif overall_score < MIN_CONFIRMATION_SCORE:
        suggested_action = "clarify"
        reasoning = (
            f"Clarity score ({overall_score:.2f}) needs improvement. "
            "Run clarification loop to address identified gaps."
        )
    else:
        suggested_action = "proceed"
        reasoning = (
            f"Clarity score ({overall_score:.2f}) is sufficient. "
            "Ready to proceed with initialization."
        )

    return ClarityAssessment(
        score=overall_score,
        dimension_scores=dimension_scores,
        gaps=all_gaps,
        suggested_action=suggested_action,
        reasoning=reasoning,
    )


def generate_clarification_questions(
    idea: str,
    gaps: list[str],
    dimension_scores: dict[str, float],
    language: str = "en",
) -> list[str]:
    """Generate targeted clarification questions.

    Selects questions from the question bank based on the weakest
    dimensions and identified gaps.

    Args:
        idea: The research idea.
        gaps: List of identified gaps.
        dimension_scores: Scores for each dimension.
        language: Language for questions ("en" or "zh").

    Returns:
        List of 2-3 targeted questions.
    """
    # Sort dimensions by score (ascending)
    sorted_dims = sorted(dimension_scores.items(), key=lambda x: x[1])

    questions = []
    lang_key = language if language in ("en", "zh") else "en"

    # Select questions from lowest-scoring dimensions
    for dim, score in sorted_dims:
        if score < 0.7:  # Only for dimensions that need improvement
            dim_questions = QUESTION_BANK.get(dim, [])
            if dim_questions:
                # Take first question from this dimension
                q = dim_questions[0].get(lang_key, dim_questions[0].get("en", ""))
                questions.append(q)
                if len(questions) >= 3:
                    break

    # If no questions generated, use default
    if not questions:
        default_q = (
            "Can you tell me more about your research idea?"
            if language == "en"
            else "你能告诉我更多关于你研究想法的内容吗？"
        )
        questions.append(default_q)

    return questions


def run_clarification_loop(
    project_root: Path,
    idea: str,
    context: dict[str, Any] | None = None,
    ask_question_func: callable | None = None,
) -> ClarificationResult:
    """Execute the clarification loop.

    Runs iterative Q&A until clarity threshold is reached or max rounds
    are exhausted.

    Args:
        project_root: Path to the project root.
        idea: The research idea.
        context: Optional context information.
        ask_question_func: Function to ask questions (for testing/CLI).
                          If None, will raise NotImplementedError for
                          interactive mode.

    Returns:
        ClarificationResult with final idea and confirmation status.
    """
    if context is None:
        context = {}

    # Initial assessment
    assessment = assess_intent_clarity(idea, context)
    current_idea = idea
    rounds = []

    # Check if brainstorming is needed
    if assessment.score < BRAINSTORM_THRESHOLD:
        return ClarificationResult(
            original_idea=idea,
            clarified_idea=current_idea,
            clarity_score=assessment.score,
            rounds=rounds,
            confirmed=False,
            needs_brainstorming=True,
        )

    # If already clear enough, return early
    if assessment.score >= MIN_CONFIRMATION_SCORE:
        return ClarificationResult(
            original_idea=idea,
            clarified_idea=current_idea,
            clarity_score=assessment.score,
            rounds=rounds,
            confirmed=True,
            needs_brainstorming=False,
        )

    # Run clarification rounds
    for round_num in range(1, MAX_CLARIFICATION_ROUNDS + 1):
        # Generate questions
        questions = generate_clarification_questions(
            current_idea,
            assessment.gaps,
            assessment.dimension_scores,
            context.get("language", "en"),
        )

        if ask_question_func is None:
            raise NotImplementedError(
                "Interactive clarification requires ask_question_func. "
                "Use init_wizard.py for interactive sessions."
            )

        # Ask questions and get responses
        responses = ask_question_func(questions)

        # Synthesize responses into updated idea
        current_idea = _synthesize_idea(current_idea, questions, responses)

        # Re-assess
        new_assessment = assess_intent_clarity(current_idea, context)

        # Record round
        round_record = ClarificationRound(
            round_number=round_num,
            questions=questions,
            responses=responses,
            clarity_before=assessment.score,
            clarity_after=new_assessment.score,
        )
        rounds.append(round_record)

        # Update assessment
        assessment = new_assessment

        # Check if clear enough
        if assessment.score >= MIN_CONFIRMATION_SCORE:
            break

    return ClarificationResult(
        original_idea=idea,
        clarified_idea=current_idea,
        clarity_score=assessment.score,
        rounds=rounds,
        confirmed=assessment.score >= MIN_CONFIRMATION_SCORE,
        needs_brainstorming=False,
    )


def _synthesize_idea(
    current_idea: str,
    questions: list[str],
    responses: list[str],
) -> str:
    """Synthesize Q&A into an updated idea.

    Args:
        current_idea: Current research idea.
        questions: Questions asked.
        responses: User responses.

    Returns:
        Updated research idea incorporating responses.
    """
    # Simple synthesis: append key insights from responses
    synthesis_parts = [current_idea.strip()]

    for i, (q, r) in enumerate(zip(questions, responses)):
        if r and r.strip():
            # Extract key points from response
            r_clean = r.strip()
            if len(r_clean) > 10:  # Significant response
                synthesis_parts.append(f"[Clarification {i+1}: {r_clean[:200]}]")

    return "\n\n".join(synthesis_parts)


def should_trigger_brainstorming(assessment: ClarityAssessment) -> bool:
    """Determine if brainstorming should be triggered.

    Args:
        assessment: The clarity assessment.

    Returns:
        True if brainstorming is recommended.
    """
    return assessment.score < BRAINSTORM_THRESHOLD


def get_dimension_questions(dimension: str, count: int = 2) -> list[str]:
    """Get questions for a specific dimension.

    Args:
        dimension: Dimension name.
        count: Number of questions to return.

    Returns:
        List of questions for the dimension.
    """
    questions = QUESTION_BANK.get(dimension, [])
    return [q.get("en", "") for q in questions[:count]]


def format_assessment_summary(assessment: ClarityAssessment) -> str:
    """Format assessment for display.

    Args:
        assessment: The clarity assessment.

    Returns:
        Formatted summary string.
    """
    lines = [
        f"Intent Clarity Score: {assessment.score:.2f}",
        "",
        "Dimension Scores:",
    ]

    for dim, score in sorted(
        assessment.dimension_scores.items(),
        key=lambda x: x[1],
    ):
        bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
        lines.append(f"  {dim:15s} [{bar}] {score:.2f}")

    if assessment.gaps:
        lines.append("")
        lines.append("Identified Gaps:")
        for gap in assessment.gaps[:5]:
            lines.append(f"  - {gap}")

    lines.append("")
    lines.append(f"Suggested Action: {assessment.suggested_action}")

    return "\n".join(lines)


def main() -> int:
    """CLI entry point for testing."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Assess research intent clarity")
    parser.add_argument("idea", help="Research idea to assess")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    assessment = assess_intent_clarity(args.idea)

    if args.json:
        print(json.dumps(assessment.to_dict(), indent=2))
    else:
        print(format_assessment_summary(assessment))

        if args.verbose:
            print("\nReasoning:")
            print(assessment.reasoning)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
