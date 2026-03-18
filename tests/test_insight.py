#!/usr/bin/env python3
"""Tests for run_insight.py module."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

# Add scripts directory to path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from constants import DEFAULT_DELIVERABLES
from run_insight import (
    detect_project_root,
    format_assessment_output,
    format_clarity_bar,
    format_questions_output,
    get_existing_idea,
    run_insight,
)


class TestDetectProjectRoot:
    """Tests for detect_project_root function."""

    def test_detect_existing_project(self, tmp_path: Path) -> None:
        """Test detecting an existing project."""
        autoresearch = tmp_path / ".autoresearch"
        autoresearch.mkdir()

        result = detect_project_root(tmp_path)
        assert result == tmp_path

    def test_no_project_found(self, tmp_path: Path) -> None:
        """Test when no project is found."""
        result = detect_project_root(tmp_path)
        assert result is None


class TestGetExistingIdea:
    """Tests for get_existing_idea function."""

    def test_get_idea_from_state(self, tmp_path: Path) -> None:
        """Test getting idea from project state."""
        # Create state directory
        state_dir = tmp_path / ".autoresearch" / "state"
        state_dir.mkdir(parents=True)

        # Create state file
        state_data = {"project_id": "test", "topic": "Test Research Idea"}
        state_file = state_dir / "research-state.yaml"
        state_file.write_text(yaml.dump(state_data), encoding="utf-8")

        result = get_existing_idea(tmp_path)
        assert result == "Test Research Idea"

    def test_no_state_file(self, tmp_path: Path) -> None:
        """Test when state file doesn't exist."""
        result = get_existing_idea(tmp_path)
        assert result is None


class TestFormatClarityBar:
    """Tests for format_clarity_bar function."""

    def test_full_bar(self) -> None:
        """Test full bar."""
        result = format_clarity_bar(1.0, width=10)
        assert result == "█" * 10

    def test_empty_bar(self) -> None:
        """Test empty bar."""
        result = format_clarity_bar(0.0, width=10)
        assert result == "░" * 10

    def test_half_bar(self) -> None:
        """Test half bar."""
        result = format_clarity_bar(0.5, width=10)
        assert result == "█" * 5 + "░" * 5


class TestFormatAssessmentOutput:
    """Tests for format_assessment_output function."""

    def test_basic_output(self) -> None:
        """Test basic assessment output."""
        idea = "Test research idea about machine learning"
        assessment = {
            "score": 0.65,
            "dimension_scores": {
                "problem": 0.7,
                "solution": 0.6,
                "contribution": 0.7,
                "constraints": 0.5,
                "novelty": 0.6,
            },
            "gaps": ["Missing novelty keywords"],
            "suggested_action": "clarify",
            "reasoning": "Test reasoning",
        }

        result = format_assessment_output(idea, assessment)

        assert "Test research idea" in result
        assert "0.65" in result
        assert "Problem" in result

    def test_clear_idea(self) -> None:
        """Test output for clear idea."""
        idea = "Well-defined research idea"
        assessment = {
            "score": 0.85,
            "dimension_scores": {
                "problem": 0.9,
                "solution": 0.8,
                "contribution": 0.9,
                "constraints": 0.8,
                "novelty": 0.8,
            },
            "gaps": [],
            "suggested_action": "proceed",
            "reasoning": "Good clarity",
        }

        result = format_assessment_output(idea, assessment)

        assert "清晰" in result


class TestFormatQuestionsOutput:
    """Tests for format_questions_output function."""

    def test_format_questions(self) -> None:
        """Test formatting questions."""
        questions = [
            "What problem are you solving?",
            "What's your approach?",
        ]

        result = format_questions_output(questions, 1)

        assert "第 1 轮" in result
        assert "Q1:" in result
        assert "What problem" in result


class TestRunInsight:
    """Tests for run_insight function."""

    def test_non_interactive_with_idea(self) -> None:
        """Test non-interactive mode with idea."""
        result = run_insight(
            project_root=None,
            idea="I want to improve transformer attention for long sequences",
            interactive=False,
            json_output=True,
        )

        assert result["status"] == "assessed"
        assert "clarity_score" in result
        assert "dimension_scores" in result

    def test_non_interactive_no_idea(self) -> None:
        """Test non-interactive mode without idea."""
        result = run_insight(
            project_root=None,
            idea=None,
            interactive=False,
            json_output=True,
        )

        assert result["status"] == "error"

    def test_with_project_idea(self, tmp_path: Path) -> None:
        """Test with project containing existing idea."""
        # Create state directory
        state_dir = tmp_path / ".autoresearch" / "state"
        state_dir.mkdir(parents=True)

        # Create state file
        state_data = {"topic": "Existing research idea from project"}
        state_file = state_dir / "research-state.yaml"
        state_file.write_text(yaml.dump(state_data), encoding="utf-8")

        result = run_insight(
            project_root=tmp_path,
            idea=None,
            interactive=False,
            json_output=True,
        )

        assert result["original_idea"] == "Existing research idea from project"

    def test_short_idea_needs_brainstorming(self) -> None:
        """Test that short idea suggests brainstorming."""
        result = run_insight(
            project_root=None,
            idea="test",  # Too short
            interactive=False,
            json_output=True,
        )

        assert result["clarity_score"] < 0.4


class TestAssessmentScores:
    """Tests for assessment scoring."""

    def test_well_defined_idea(self) -> None:
        """Test a well-defined research idea."""
        idea = """
        I want to solve the problem of long-sequence time series forecasting,
        where prediction accuracy degrades significantly for horizons beyond 100 steps.
        I propose to use an improved attention mechanism that better captures
        long-range dependencies. My goal is to achieve state-of-the-art results
        on benchmark datasets. The target venue is ICML 2026 with a deadline
        in May. I have access to 4 RTX 4090 GPUs and existing benchmark datasets.
        This is novel because existing attention mechanisms struggle with
        sequences longer than the training context.
        """

        result = run_insight(
            project_root=None,
            idea=idea,
            interactive=False,
            json_output=True,
        )

        # Well-defined idea should have reasonable score
        # The exact score depends on the assessment algorithm
        assert result["clarity_score"] > 0.2
        assert "dimension_scores" in result

    def test_vague_idea(self) -> None:
        """Test a vague research idea."""
        idea = "I want to do something with AI."

        result = run_insight(
            project_root=None,
            idea=idea,
            interactive=False,
            json_output=True,
        )

        # Vague idea should have low score
        assert result["clarity_score"] < 0.5
        assert result["needs_brainstorming"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
