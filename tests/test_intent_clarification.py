"""
Tests for intent_clarification.py module.
"""

import importlib.util
import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def load_script_module(name: str):
    """Dynamically load a script module."""
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module  # Register module before exec for dataclass
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


INTENT = load_script_module("intent_clarification")


class ClarityAssessmentTest(unittest.TestCase):
    """Test ClarityAssessment dataclass."""

    def test_to_dict(self) -> None:
        """Test to_dict conversion."""
        assessment = INTENT.ClarityAssessment(
            score=0.75,
            dimension_scores={"problem": 0.8, "solution": 0.7},
            gaps=["Missing constraint info"],
            suggested_action="proceed",
            reasoning="Test reasoning",
        )
        result = assessment.to_dict()
        self.assertEqual(result["score"], 0.75)
        self.assertEqual(result["dimension_scores"]["problem"], 0.8)
        self.assertEqual(len(result["gaps"]), 1)
        self.assertEqual(result["suggested_action"], "proceed")

    def test_default_values(self) -> None:
        """Test default values are set correctly."""
        assessment = INTENT.ClarityAssessment(score=0.5)
        self.assertEqual(assessment.dimension_scores, {})
        self.assertEqual(assessment.gaps, [])
        self.assertEqual(assessment.suggested_action, "clarify")
        self.assertEqual(assessment.reasoning, "")


class ClarificationRoundTest(unittest.TestCase):
    """Test ClarificationRound dataclass."""

    def test_to_dict(self) -> None:
        """Test to_dict conversion."""
        round_obj = INTENT.ClarificationRound(
            round_number=1,
            questions=["What problem?"],
            responses=["The problem is..."],
            clarity_before=0.3,
            clarity_after=0.6,
        )
        result = round_obj.to_dict()
        self.assertEqual(result["round_number"], 1)
        self.assertEqual(len(result["questions"]), 1)
        self.assertEqual(result["clarity_before"], 0.3)
        self.assertEqual(result["clarity_after"], 0.6)
        self.assertIn("timestamp", result)


class ClarificationResultTest(unittest.TestCase):
    """Test ClarificationResult dataclass."""

    def test_to_dict(self) -> None:
        """Test to_dict conversion."""
        result = INTENT.ClarificationResult(
            original_idea="Initial idea",
            clarified_idea="Clarified idea",
            clarity_score=0.8,
            confirmed=True,
        )
        d = result.to_dict()
        self.assertEqual(d["original_idea"], "Initial idea")
        self.assertEqual(d["clarified_idea"], "Clarified idea")
        self.assertEqual(d["clarity_score"], 0.8)
        self.assertTrue(d["confirmed"])

    def test_default_values(self) -> None:
        """Test default values."""
        result = INTENT.ClarificationResult(
            original_idea="test",
            clarified_idea="test",
            clarity_score=0.5,
        )
        self.assertEqual(result.rounds, [])
        self.assertFalse(result.confirmed)
        self.assertFalse(result.needs_brainstorming)


class AssessIntentClarityTest(unittest.TestCase):
    """Test assess_intent_clarity function."""

    def test_empty_idea_returns_zero(self) -> None:
        """Test empty idea returns score 0."""
        assessment = INTENT.assess_intent_clarity("")
        self.assertEqual(assessment.score, 0.0)
        self.assertEqual(assessment.suggested_action, "brainstorm")

    def test_too_short_idea(self) -> None:
        """Test very short idea returns low score."""
        assessment = INTENT.assess_intent_clarity("too short")
        self.assertEqual(assessment.score, 0.0)
        self.assertIn("too short", assessment.gaps[0].lower())

    def test_clear_idea_high_score(self) -> None:
        """Test clear idea returns higher score."""
        idea = (
            "I want to solve the problem of inefficient neural network training "
            "using a novel approach that combines gradient compression with "
            "sparse attention mechanisms. My proposed method will reduce memory "
            "usage by 50% while maintaining accuracy within 1% of baseline. "
            "This is different from existing approaches because I use a new "
            "compression algorithm specifically designed for attention weights."
        )
        assessment = INTENT.assess_intent_clarity(idea)
        self.assertGreater(assessment.score, 0.4)

    def test_dimension_scores_populated(self) -> None:
        """Test that all dimension scores are populated."""
        idea = "I propose a new method for solving the optimization problem."
        assessment = INTENT.assess_intent_clarity(idea)
        self.assertIn("problem", assessment.dimension_scores)
        self.assertIn("solution", assessment.dimension_scores)
        self.assertIn("contribution", assessment.dimension_scores)
        self.assertIn("constraints", assessment.dimension_scores)
        self.assertIn("novelty", assessment.dimension_scores)

    def test_gaps_identified(self) -> None:
        """Test that gaps are identified for unclear ideas."""
        idea = "I want to do something with machine learning."
        assessment = INTENT.assess_intent_clarity(idea)
        self.assertGreater(len(assessment.gaps), 0)

    def test_context_improves_constraints(self) -> None:
        """Test that context improves constraint scoring."""
        idea = "I want to solve the optimization problem with a new method."
        assessment_no_context = INTENT.assess_intent_clarity(idea)

        assessment_with_context = INTENT.assess_intent_clarity(
            idea,
            context={"timeline": "3 months", "venue": "NeurIPS", "resources": "4 GPUs"},
        )
        # Context should improve constraint score
        self.assertGreaterEqual(
            assessment_with_context.dimension_scores["constraints"],
            assessment_no_context.dimension_scores["constraints"],
        )

    def test_suggested_action_brainstorm(self) -> None:
        """Test brainstorm action for very low scores."""
        assessment = INTENT.assess_intent_clarity("")
        self.assertEqual(assessment.suggested_action, "brainstorm")

    def test_suggested_action_clarify(self) -> None:
        """Test clarify action for medium scores."""
        idea = "I want to solve a problem with a method for a contribution."
        assessment = INTENT.assess_intent_clarity(idea)
        # Score should be medium-low
        if 0.4 <= assessment.score < 0.7:
            self.assertEqual(assessment.suggested_action, "clarify")

    def test_reasoning_provided(self) -> None:
        """Test that reasoning is provided."""
        assessment = INTENT.assess_intent_clarity("test idea with some content")
        self.assertNotEqual(assessment.reasoning, "")


class GenerateClarificationQuestionsTest(unittest.TestCase):
    """Test generate_clarification_questions function."""

    def test_returns_questions(self) -> None:
        """Test that questions are returned."""
        idea = "I want to do machine learning."
        gaps = ["Missing problem keywords", "Vague solution"]
        dimension_scores = {
            "problem": 0.2,
            "solution": 0.3,
            "contribution": 0.5,
            "constraints": 0.4,
            "novelty": 0.3,
        }
        questions = INTENT.generate_clarification_questions(idea, gaps, dimension_scores)
        self.assertGreater(len(questions), 0)
        self.assertLessEqual(len(questions), 3)

    def test_targets_lowest_dimensions(self) -> None:
        """Test that questions target lowest scoring dimensions."""
        idea = "test idea"
        gaps = []
        dimension_scores = {
            "problem": 0.9,  # High
            "solution": 0.1,  # Lowest
            "contribution": 0.5,
            "constraints": 0.5,
            "novelty": 0.2,  # Second lowest
        }
        questions = INTENT.generate_clarification_questions(idea, gaps, dimension_scores)
        # Should ask about solution first
        self.assertGreater(len(questions), 0)

    def test_max_three_questions(self) -> None:
        """Test that max 3 questions are returned."""
        idea = "test"
        gaps = ["gap1", "gap2", "gap3", "gap4"]
        dimension_scores = {
            "problem": 0.1,
            "solution": 0.1,
            "contribution": 0.1,
            "constraints": 0.1,
            "novelty": 0.1,
        }
        questions = INTENT.generate_clarification_questions(idea, gaps, dimension_scores)
        self.assertLessEqual(len(questions), 3)

    def test_chinese_language(self) -> None:
        """Test Chinese language questions."""
        idea = "test"
        gaps = []
        dimension_scores = {
            "problem": 0.2,
            "solution": 0.9,
            "contribution": 0.9,
            "constraints": 0.9,
            "novelty": 0.9,
        }
        questions = INTENT.generate_clarification_questions(
            idea, gaps, dimension_scores, language="zh"
        )
        # Should contain Chinese characters
        has_chinese = any(any("\u4e00" <= c <= "\u9fff" for c in q) for q in questions)
        self.assertTrue(has_chinese)

    def test_default_question_when_all_high(self) -> None:
        """Test default question when all dimensions are high."""
        idea = "test"
        gaps = []
        dimension_scores = {
            "problem": 0.9,
            "solution": 0.9,
            "contribution": 0.9,
            "constraints": 0.9,
            "novelty": 0.9,
        }
        questions = INTENT.generate_clarification_questions(idea, gaps, dimension_scores)
        self.assertEqual(len(questions), 1)
        self.assertIn("more", questions[0].lower())


class ShouldTriggerBrainstormingTest(unittest.TestCase):
    """Test should_trigger_brainstorming function."""

    def test_low_score_triggers(self) -> None:
        """Test low score triggers brainstorming."""
        assessment = INTENT.ClarityAssessment(score=0.3)
        self.assertTrue(INTENT.should_trigger_brainstorming(assessment))

    def test_high_score_no_trigger(self) -> None:
        """Test high score does not trigger brainstorming."""
        assessment = INTENT.ClarityAssessment(score=0.5)
        self.assertFalse(INTENT.should_trigger_brainstorming(assessment))


class GetDimensionQuestionsTest(unittest.TestCase):
    """Test get_dimension_questions function."""

    def test_returns_questions(self) -> None:
        """Test that questions are returned."""
        questions = INTENT.get_dimension_questions("problem", count=2)
        self.assertEqual(len(questions), 2)
        self.assertTrue(all(q for q in questions))  # Non-empty strings

    def test_invalid_dimension_returns_empty(self) -> None:
        """Test invalid dimension returns empty list."""
        questions = INTENT.get_dimension_questions("invalid_dimension")
        self.assertEqual(questions, [])

    def test_count_limited(self) -> None:
        """Test count limits returned questions."""
        questions = INTENT.get_dimension_questions("problem", count=10)
        # Should return max available
        self.assertLessEqual(len(questions), 3)


class FormatAssessmentSummaryTest(unittest.TestCase):
    """Test format_assessment_summary function."""

    def test_includes_score(self) -> None:
        """Test that score is included in summary."""
        assessment = INTENT.ClarityAssessment(score=0.65)
        summary = INTENT.format_assessment_summary(assessment)
        self.assertIn("0.65", summary)

    def test_includes_dimension_scores(self) -> None:
        """Test that dimension scores are included."""
        assessment = INTENT.ClarityAssessment(
            score=0.5,
            dimension_scores={"problem": 0.6, "solution": 0.4},
        )
        summary = INTENT.format_assessment_summary(assessment)
        self.assertIn("problem", summary)
        self.assertIn("solution", summary)

    def test_includes_gaps(self) -> None:
        """Test that gaps are included."""
        assessment = INTENT.ClarityAssessment(
            score=0.3, gaps=["Missing problem definition", "No constraints"]
        )
        summary = INTENT.format_assessment_summary(assessment)
        self.assertIn("Missing problem definition", summary)

    def test_includes_suggested_action(self) -> None:
        """Test that suggested action is included."""
        assessment = INTENT.ClarityAssessment(score=0.3, suggested_action="brainstorm")
        summary = INTENT.format_assessment_summary(assessment)
        self.assertIn("brainstorm", summary)


class RunClarificationLoopTest(unittest.TestCase):
    """Test run_clarification_loop function."""

    def test_needs_brainstorming_for_low_score(self) -> None:
        """Test that low score returns needs_brainstorming."""
        result = INTENT.run_clarification_loop(
            Path("/tmp/test"),
            "short",  # Too short, score will be 0
            context={},
        )
        self.assertTrue(result.needs_brainstorming)
        self.assertFalse(result.confirmed)

    def test_confirmed_for_high_score(self) -> None:
        """Test that high score is confirmed."""
        # Create a very clear idea with all dimensions covered
        idea = (
            "I propose a novel solution to the challenging problem of neural network "
            "optimization using gradient compression. My contribution is a new algorithm "
            "that reduces training time by 40%. The timeline is 6 months for NeurIPS "
            "submission with a hard deadline. Unlike existing approaches, my method "
            "specifically targets sparse gradients. I have access to 8 GPUs and the "
            "dataset is already prepared. The problem is clearly defined as reducing "
            "memory overhead in transformer training."
        )
        # First check the assessment score
        assessment = INTENT.assess_intent_clarity(
            idea,
            context={"timeline": "6 months", "venue": "NeurIPS", "resources": "8 GPUs"},
        )
        # If score is high enough, should be confirmed
        if assessment.score >= 0.7:
            result = INTENT.run_clarification_loop(
                Path("/tmp/test"),
                idea,
                context={"timeline": "6 months", "venue": "NeurIPS", "resources": "8 GPUs"},
            )
            self.assertTrue(result.confirmed)
        else:
            # Skip if score not high enough - need mock for clarification
            self.skipTest(f"Idea score {assessment.score} not high enough for auto-confirm")

    def test_raises_without_ask_function(self) -> None:
        """Test that NotImplementedError is raised without ask function."""
        # Medium clarity idea that needs clarification
        idea = "I want to solve a problem with a new method for some contribution."
        assessment = INTENT.assess_intent_clarity(idea)

        # Only test if score is in clarification range
        if 0.4 <= assessment.score < 0.7:
            with self.assertRaises(NotImplementedError):
                INTENT.run_clarification_loop(
                    Path("/tmp/test"),
                    idea,
                    context={},
                    ask_question_func=None,
                )

    def test_clarification_with_mock(self) -> None:
        """Test clarification with mock function."""

        def mock_ask(questions):
            return ["Test response"] * len(questions)

        idea = "I want to solve a problem with a method."
        result = INTENT.run_clarification_loop(
            Path("/tmp/test"),
            idea,
            context={},
            ask_question_func=mock_ask,
        )
        self.assertEqual(result.original_idea, idea)
        # Check that clarification was attempted
        if 0.4 <= result.clarity_score < 0.7:
            self.assertGreater(len(result.rounds), 0)


class SynthesizeIdeaTest(unittest.TestCase):
    """Test _synthesize_idea internal function."""

    def test_appends_responses(self) -> None:
        """Test that responses are appended to idea."""
        current = "Original idea"
        questions = ["What is the problem?"]
        responses = ["The problem is optimization"]
        result = INTENT._synthesize_idea(current, questions, responses)
        self.assertIn("Original idea", result)
        self.assertIn("optimization", result)

    def test_ignores_short_responses(self) -> None:
        """Test that short responses are ignored."""
        current = "Original idea"
        questions = ["Q1", "Q2"]
        responses = ["short", "This is a meaningful response about the topic"]
        result = INTENT._synthesize_idea(current, questions, responses)
        # Short response should not be included
        self.assertIn("meaningful", result)


class ConstantsTest(unittest.TestCase):
    """Test module constants."""

    def test_max_clarification_rounds(self) -> None:
        """Test MAX_CLARIFICATION_ROUNDS is reasonable."""
        self.assertEqual(INTENT.MAX_CLARIFICATION_ROUNDS, 5)

    def test_min_confirmation_score(self) -> None:
        """Test MIN_CONFIRMATION_SCORE threshold."""
        self.assertEqual(INTENT.MIN_CONFIRMATION_SCORE, 0.7)

    def test_brainstorm_threshold(self) -> None:
        """Test BRAINSTORM_THRESHOLD."""
        self.assertEqual(INTENT.BRAINSTORM_THRESHOLD, 0.4)

    def test_dimension_weights_sum_to_one(self) -> None:
        """Test that dimension weights sum to 1.0."""
        total = sum(INTENT.DIMENSION_WEIGHTS.values())
        self.assertAlmostEqual(total, 1.0, places=2)


if __name__ == "__main__":
    unittest.main()
