#!/usr/bin/env python3
"""Tests for run_status.py module (simplified — formatting removed)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import init_research_project as INIT  # noqa: E402
from run_status import run_status  # noqa: E402


class TestRunStatus:
    def test_run_status_initialized_project(self, tmp_path: Path) -> None:
        INIT.initialize_research_project(project_root=tmp_path, topic="Status test")
        result = run_status(tmp_path)
        assert "phase" in result
        assert "gate" in result
        assert "decision" in result
        assert "scores" in result

    def test_run_status_serializable(self, tmp_path: Path) -> None:
        INIT.initialize_research_project(project_root=tmp_path, topic="JSON test")
        result = run_status(tmp_path)
        # Must be JSON-serializable
        json.dumps(result)

    def test_run_status_verbose(self, tmp_path: Path) -> None:
        INIT.initialize_research_project(project_root=tmp_path, topic="Verbose test")
        result = run_status(tmp_path, verbose=True)
        assert "missing_deliverables" in result or "existing_deliverables" in result

    def test_run_status_missing_project(self, tmp_path: Path) -> None:
        with pytest.raises((FileNotFoundError, SystemExit, KeyError)):
            run_status(tmp_path / "nonexistent")
