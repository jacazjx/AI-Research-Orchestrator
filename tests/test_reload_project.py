#!/usr/bin/env python3
"""Tests for reload_project.py module."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

# Add scripts directory to path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from reload_project import (
    detect_project_root,
    generate_json_output,
    generate_status_report,
    get_completed_work,
    get_next_actions,
    get_phase_progress,
    load_dashboard_status,
    load_gpu_registry,
    load_project_config,
    load_project_state,
    load_user_config,
    reload_project,
)


class TestDetectProjectRoot:
    """Tests for detect_project_root function."""

    def test_detect_existing_project(self, tmp_path: Path) -> None:
        """Test detecting an existing project."""
        # Create .autoresearch directory
        autoresearch = tmp_path / ".autoresearch"
        autoresearch.mkdir()

        result = detect_project_root(tmp_path)
        assert result == tmp_path

    def test_detect_nested_directory(self, tmp_path: Path) -> None:
        """Test detecting project from nested directory."""
        # Create .autoresearch directory
        autoresearch = tmp_path / ".autoresearch"
        autoresearch.mkdir()

        # Create nested directory
        nested = tmp_path / "subdir" / "nested"
        nested.mkdir(parents=True)

        result = detect_project_root(nested)
        assert result == tmp_path

    def test_no_project_found(self, tmp_path: Path) -> None:
        """Test when no project is found."""
        result = detect_project_root(tmp_path)
        assert result is None

    def test_detect_from_subdir(self, tmp_path: Path) -> None:
        """Test detecting project from a subdirectory."""
        # Create project structure
        autoresearch = tmp_path / ".autoresearch"
        autoresearch.mkdir()
        subdir = tmp_path / "code" / "src"
        subdir.mkdir(parents=True)

        result = detect_project_root(subdir)
        assert result == tmp_path


class TestLoadProjectState:
    """Tests for load_project_state function."""

    def test_load_valid_state(self, tmp_path: Path) -> None:
        """Test loading a valid state file."""
        # Create state directory
        state_dir = tmp_path / ".autoresearch" / "state"
        state_dir.mkdir(parents=True)

        # Create state file
        state_data = {
            "project_id": "test-project",
            "topic": "Test Topic",
            "current_phase": "survey",
            "state_version": "2.0.0",
        }
        state_file = state_dir / "research-state.yaml"
        state_file.write_text(yaml.dump(state_data), encoding="utf-8")

        result = load_project_state(tmp_path)
        assert result["project_id"] == "test-project"
        assert result["topic"] == "Test Topic"

    def test_load_missing_state(self, tmp_path: Path) -> None:
        """Test loading when state file is missing."""
        with pytest.raises(FileNotFoundError):
            load_project_state(tmp_path)

    def test_load_malformed_state(self, tmp_path: Path) -> None:
        """Test loading a malformed state file."""
        # Create state directory
        state_dir = tmp_path / ".autoresearch" / "state"
        state_dir.mkdir(parents=True)

        # Create malformed state file
        state_file = state_dir / "research-state.yaml"
        state_file.write_text("::: invalid yaml :::", encoding="utf-8")

        # Should raise either ValueError or yaml.scanner.ScannerError
        with pytest.raises(Exception):  # noqa: B017
            load_project_state(tmp_path)


class TestLoadProjectConfig:
    """Tests for load_project_config function."""

    def test_load_valid_config(self, tmp_path: Path) -> None:
        """Test loading a valid config file."""
        # Create config directory
        config_dir = tmp_path / ".autoresearch" / "config"
        config_dir.mkdir(parents=True)

        # Create config file
        config_data = {"max_loops": 5, "auto_advance": False}
        config_file = config_dir / "orchestrator-config.yaml"
        config_file.write_text(yaml.dump(config_data), encoding="utf-8")

        result = load_project_config(tmp_path)
        assert result["max_loops"] == 5

    def test_load_missing_config(self, tmp_path: Path) -> None:
        """Test loading when config file is missing."""
        result = load_project_config(tmp_path)
        assert result == {}


class TestLoadDashboardStatus:
    """Tests for load_dashboard_status function."""

    def test_load_valid_status(self, tmp_path: Path) -> None:
        """Test loading a valid status file."""
        # Create dashboard directory
        dashboard_dir = tmp_path / ".autoresearch" / "dashboard"
        dashboard_dir.mkdir(parents=True)

        # Create status file
        status_data = {"phase": "survey", "completion_percent": 10}
        status_file = dashboard_dir / "status.json"
        status_file.write_text(json.dumps(status_data), encoding="utf-8")

        result = load_dashboard_status(tmp_path)
        assert result["phase"] == "survey"

    def test_load_missing_status(self, tmp_path: Path) -> None:
        """Test loading when status file is missing."""
        result = load_dashboard_status(tmp_path)
        assert result == {}


class TestLoadUserConfig:
    """Tests for load_user_config function."""

    def test_load_missing_config(self) -> None:
        """Test loading when user config is missing."""
        with patch.object(Path, "home", return_value=Path("/nonexistent")):
            result = load_user_config()
            assert result == {}


class TestLoadGpuRegistry:
    """Tests for load_gpu_registry function."""

    def test_load_missing_registry(self) -> None:
        """Test loading when GPU registry is missing."""
        with patch.object(Path, "home", return_value=Path("/nonexistent")):
            result = load_gpu_registry()
            assert result == {}


class TestGetPhaseProgress:
    """Tests for get_phase_progress function."""

    def test_survey_phase_progress(self) -> None:
        """Test progress calculation for survey phase."""
        state = {
            "current_phase": "survey",
            "gate_scores": {"gate_1": 0},
            "approval_status": {"gate_1": "pending"},
        }

        result = get_phase_progress(state)

        assert result["survey"]["status"] == "in_progress"
        assert result["pilot"]["status"] == "pending"
        assert result["experiments"]["status"] == "pending"

    def test_completed_phase(self) -> None:
        """Test progress calculation with completed phase."""
        state = {
            "current_phase": "pilot",
            "gate_scores": {"gate_1": 4.5, "gate_2": 0},
            "approval_status": {"gate_1": "approved", "gate_2": "pending"},
        }

        result = get_phase_progress(state)

        assert result["survey"]["status"] == "completed"
        assert result["pilot"]["status"] == "in_progress"


class TestGetCompletedWork:
    """Tests for get_completed_work function."""

    def test_no_completed_work(self) -> None:
        """Test when no work is completed."""
        state = {
            "phase_reviews": {},
            "gate_scores": {},
            "approval_status": {},
        }

        result = get_completed_work(state)
        assert result == []

    def test_one_completed_phase(self) -> None:
        """Test with one completed phase."""
        state = {
            "phase_reviews": {"survey_critic": "approved"},
            "gate_scores": {"gate_1": 4.5},
            "approval_status": {"gate_1": "approved"},
        }

        result = get_completed_work(state)

        assert len(result) == 1
        assert result[0]["phase"] == "survey"
        assert result[0]["score"] == 4.5


class TestGetNextActions:
    """Tests for get_next_actions function."""

    def test_survey_actions(self) -> None:
        """Test next actions for survey phase."""
        state = {"current_phase": "survey", "current_substep": None}

        result = get_next_actions(state)

        assert len(result) > 0
        assert "开始" in result[0] or "Survey" in result[0] or "调研" in result[0]

    def test_waiting_for_gate(self) -> None:
        """Test actions when waiting for gate approval."""
        state = {
            "current_phase": "survey",
            "current_substep": "literature_survey",
            "gate_scores": {"gate_1": 4.0},
            "approval_status": {"gate_1": "pending"},
        }

        result = get_next_actions(state)

        assert len(result) == 1
        assert "等待" in result[0] or "gate" in result[0].lower()


class TestGenerateStatusReport:
    """Tests for generate_status_report function."""

    def test_basic_report(self, tmp_path: Path) -> None:
        """Test generating a basic status report."""
        state = {
            "project_id": "test-project",
            "topic": "Test Research Topic",
            "research_type": "ml_experiment",
            "created_at": "2026-03-18T00:00:00Z",
            "state_version": "2.0.0",
            "current_phase": "survey",
            "current_gate": "gate_1",
            "language_policy": {"process_docs": "zh-CN", "paper_docs": "en-US"},
            "loop_limits": {"survey_critic": 3},
            "progress": {"active_gpu": "unassigned"},
        }

        report = generate_status_report(
            project_root=tmp_path,
            state=state,
            project_config={},
            dashboard_status={},
            user_config={},
            gpu_registry={},
            verbose=False,
        )

        assert "test-project" in report
        assert "Test Research Topic" in report
        assert "survey" in report

    def test_verbose_report(self, tmp_path: Path) -> None:
        """Test generating a verbose report."""
        state = {
            "project_id": "test-project",
            "topic": "Test Topic",
            "research_type": "ml_experiment",
            "created_at": "2026-03-18T00:00:00Z",
            "state_version": "2.0.0",
            "current_phase": "survey",
            "current_gate": "gate_1",
            "platform": "claude-code",
            "subphase": "entry",
            "language_policy": {"process_docs": "zh-CN", "paper_docs": "en-US"},
            "loop_limits": {},
            "progress": {"active_gpu": "unassigned"},
        }

        report = generate_status_report(
            project_root=tmp_path,
            state=state,
            project_config={"max_loops": 5},
            dashboard_status={},
            user_config={"author": {"name": "Test User", "email": "test@example.com"}},
            gpu_registry={},
            verbose=True,
        )

        assert "详细信息" in report
        assert "claude-code" in report
        assert "Test User" in report


class TestGenerateJsonOutput:
    """Tests for generate_json_output function."""

    def test_json_output_structure(self) -> None:
        """Test JSON output has correct structure."""
        state = {
            "project_id": "test-project",
            "topic": "Test Topic",
            "research_type": "ml_experiment",
            "current_phase": "survey",
            "current_gate": "gate_1",
            "state_version": "2.0.0",
            "created_at": "2026-03-18T00:00:00Z",
            "last_modified": "2026-03-18T01:00:00Z",
            "language_policy": {"process_docs": "zh-CN", "paper_docs": "en-US"},
            "loop_limits": {},
            "progress": {"active_gpu": "gpu-001"},
        }

        result = generate_json_output(
            state=state,
            project_config={},
            dashboard_status={},
            user_config={},
            gpu_registry={"gpus": {"gpu-001": {"name": "RTX 4090"}}},
        )

        assert result["project_id"] == "test-project"
        assert result["current_phase"] == "survey"
        assert "progress" in result
        assert "config" in result
        assert "user" in result
        assert "resources" in result


class TestReloadProject:
    """Tests for reload_project function."""

    def test_reload_valid_project(self, tmp_path: Path) -> None:
        """Test reloading a valid project."""
        # Create project structure
        autoresearch = tmp_path / ".autoresearch"
        state_dir = autoresearch / "state"
        state_dir.mkdir(parents=True)

        # Create state file
        state_data = {
            "project_id": "test-project",
            "topic": "Test Topic",
            "current_phase": "survey",
            "current_gate": "gate_1",
            "state_version": "2.0.0",
            "created_at": "2026-03-18T00:00:00Z",
            "language_policy": {"process_docs": "zh-CN", "paper_docs": "en-US"},
            "loop_limits": {},
            "progress": {"active_gpu": "unassigned"},
        }
        state_file = state_dir / "research-state.yaml"
        state_file.write_text(yaml.dump(state_data), encoding="utf-8")

        result = reload_project(tmp_path, json_output=False)

        assert "project_root" in result
        assert "report" in result
        assert "test-project" in result["report"]

    def test_reload_missing_project(self, tmp_path: Path) -> None:
        """Test reloading when project doesn't exist."""
        with pytest.raises(FileNotFoundError):
            reload_project(tmp_path)

    def test_reload_json_output(self, tmp_path: Path) -> None:
        """Test reloading with JSON output."""
        # Create project structure
        autoresearch = tmp_path / ".autoresearch"
        state_dir = autoresearch / "state"
        state_dir.mkdir(parents=True)

        # Create state file
        state_data = {
            "project_id": "test-project",
            "topic": "Test Topic",
            "current_phase": "survey",
            "current_gate": "gate_1",
            "state_version": "2.0.0",
            "created_at": "2026-03-18T00:00:00Z",
            "language_policy": {"process_docs": "zh-CN", "paper_docs": "en-US"},
            "loop_limits": {},
            "progress": {"active_gpu": "unassigned"},
        }
        state_file = state_dir / "research-state.yaml"
        state_file.write_text(yaml.dump(state_data), encoding="utf-8")

        result = reload_project(tmp_path, json_output=True)

        assert result["project_id"] == "test-project"
        assert "progress" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
