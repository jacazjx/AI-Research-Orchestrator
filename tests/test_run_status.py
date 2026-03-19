#!/usr/bin/env python3
"""Tests for run_status.py module."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import init_research_project as INIT  # noqa: E402
from run_status import (  # noqa: E402
    format_blockers,
    format_gate_scores,
    format_phase_bar,
    get_decision_label,
    run_status,
)


class TestFormatPhaseBar:
    def test_survey_phase(self) -> None:
        bar = format_phase_bar("survey")
        assert "[Survey]" in bar
        assert "Pilot" in bar

    def test_pilot_phase(self) -> None:
        bar = format_phase_bar("pilot")
        assert "[Pilot]" in bar
        assert "Survey" in bar

    def test_paper_phase(self) -> None:
        bar = format_phase_bar("paper")
        assert "[Paper]" in bar


class TestFormatGateScores:
    def test_all_zero(self) -> None:
        scores = {"evidence_completeness": 0, "review_readiness": 0, "human_gate": 0}
        text = format_gate_scores(scores)
        assert "0%" in text
        assert "evidence" in text.lower()

    def test_full_scores(self) -> None:
        scores = {"evidence_completeness": 100, "review_readiness": 100, "human_gate": 100}
        text = format_gate_scores(scores)
        assert "100%" in text


class TestGetDecisionLabel:
    def test_advance(self) -> None:
        assert "Advance" in get_decision_label("advance")

    def test_revise(self) -> None:
        assert "Revise" in get_decision_label("revise")

    def test_pivot(self) -> None:
        assert "Pivot" in get_decision_label("pivot")

    def test_escalate(self) -> None:
        label = get_decision_label("escalate_to_user")
        assert label  # non-empty


class TestFormatBlockers:
    def test_empty(self) -> None:
        text = format_blockers([])
        assert text == "" or "none" in text.lower()

    def test_missing_deliverables(self) -> None:
        text = format_blockers(["required_deliverables_missing"])
        assert "deliverable" in text.lower()

    def test_loop_limit(self) -> None:
        text = format_blockers(["loop_limit_reached"])
        assert "loop" in text.lower()


class TestRunStatus:
    def test_run_status_initialized_project(self, tmp_path: Path) -> None:
        INIT.initialize_research_project(project_root=tmp_path, topic="Status test")
        result = run_status(tmp_path)
        assert "phase" in result
        assert "gate" in result
        assert "decision" in result
        assert "scores" in result

    def test_run_status_json_output(self, tmp_path: Path) -> None:
        INIT.initialize_research_project(project_root=tmp_path, topic="JSON test")
        result = run_status(tmp_path, json_output=True)
        # Must be JSON-serialisable
        json.dumps(result)

    def test_run_status_missing_project(self, tmp_path: Path) -> None:
        with pytest.raises((FileNotFoundError, SystemExit, KeyError)):
            run_status(tmp_path / "nonexistent")
