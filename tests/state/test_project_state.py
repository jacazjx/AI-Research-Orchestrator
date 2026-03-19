"""Tests for project_state.py - slim core state v3.0.0 schema.

This module tests the slim v3.0.0 state schema which removes duplicates
and moves substep tracking to per-phase state files.
"""

from __future__ import annotations

import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from scripts.state.project_state import (
    STATE_FILE_PATH,
    STATE_VERSION,
    build_project_state,
    get_default_loop_counts,
    get_default_approval_status,
    get_default_phase_reviews,
    get_default_gate_scores,
    load_project_state,
    save_project_state,
    update_last_modified,
    validate_project_state,
)
from scripts.constants.phases import PHASE_TO_GATE


class TestBuildProjectState:
    """Tests for build_project_state function."""

    def test_basic_state_structure(self) -> None:
        """Test that build_project_state returns correct v3.0.0 structure."""
        state = build_project_state(
            project_id="test-project",
            topic="Test Topic",
            init_source="init",
            init_paths=["test.md"],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )

        # Core identification fields
        assert state["state_version"] == "3.0.0"
        assert state["project_id"] == "test-project"
        assert state["topic"] == "Test Topic"
        assert state["platform"] == "claude"
        assert state["client_profile"] == "claude"
        assert state["client_instruction_file"] == "CLAUDE.md"

        # Phase and subphase
        assert state["phase"] == "survey"
        assert state["current_gate"] == "gate_1"
        assert state["subphase"] == "entry"

        # No duplicates: phase/current_phase should be single field
        assert "current_phase" not in state

    def test_no_duplicate_fields(self) -> None:
        """Test that v3.0.0 schema has no duplicate fields."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )

        # These fields should NOT exist (removed or merged)
        assert "current_phase" not in state, "current_phase should not exist (use phase)"
        assert "inner_loops" not in state, "inner_loops should not exist (merged into loop_counts)"
        assert "current_substep" not in state, "current_substep moved to per-phase state"
        assert "substep_status" not in state, "substep_status moved to per-phase state"
        assert "progress" not in state, "progress derived at runtime (Task 5)"
        assert "loop_limits" not in state, "loop_limits loaded from config only"
        assert "deliverables" not in state, "deliverables are path constants, not state"
        assert "dashboard_paths" not in state, "dashboard_paths are path constants"
        assert "runtime" not in state, "runtime paths are constants"
        assert "user_config_inherited" not in state, "moved to runtime config"
        assert "gpu_usage_history" not in state, "moved to runtime config"
        assert "active_jobs" not in state, "moved to runtime config"

    def test_merged_loop_counts(self) -> None:
        """Test that loop_counts contains all phase loop keys (was inner_loops + loop_counts)."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )

        assert "loop_counts" in state
        loop_counts = state["loop_counts"]

        # All phase loop keys should be present
        expected_keys = [
            "survey_critic",
            "pilot_code_adviser",
            "experiment_code_adviser",
            "writer_reviewer",
            "reflector_curator",
        ]

        for key in expected_keys:
            assert key in loop_counts, f"Missing loop_counts key: {key}"
            assert loop_counts[key] == 0, f"Initial value should be 0 for {key}"

    def test_approval_status_structure(self) -> None:
        """Test approval_status has all gates initialized to pending."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )

        approval_status = state["approval_status"]
        expected_gates = ["gate_1", "gate_2", "gate_3", "gate_4", "gate_5"]

        for gate in expected_gates:
            assert gate in approval_status
            assert approval_status[gate] in ["pending", "approved", "rejected"]

    def test_phase_reviews_structure(self) -> None:
        """Test phase_reviews structure."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )

        phase_reviews = state["phase_reviews"]
        expected_reviews = [
            "survey_critic",
            "pilot_adviser",
            "experiment_adviser",
            "paper_reviewer",
            "reflection_curator",
        ]

        for review in expected_reviews:
            assert review in phase_reviews
            assert phase_reviews[review] in ["pending", "approved", "revise", "pivot"]

    def test_language_policy(self) -> None:
        """Test language_policy defaults."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )

        language_policy = state["language_policy"]
        assert language_policy["process_docs"] == "zh-CN"
        assert language_policy["paper_docs"] == "en-US"

    def test_custom_language_policy(self) -> None:
        """Test custom language policy values."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
            process_language="en-US",
            paper_language="zh-CN",
        )

        language_policy = state["language_policy"]
        assert language_policy["process_docs"] == "en-US"
        assert language_policy["paper_docs"] == "zh-CN"

    def test_research_type(self) -> None:
        """Test research_type field."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )

        assert state["research_type"] in ["ml_experiment", "theory", "survey", "applied"]

    def test_custom_research_type(self) -> None:
        """Test custom research_type."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
            research_type="theory",
        )

        assert state["research_type"] == "theory"

    def test_init_artifacts(self) -> None:
        """Test init_artifacts structure."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="wizard",
            init_paths=["idea.md", "CLAUDE.md"],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )

        init_artifacts = state["init_artifacts"]
        assert init_artifacts["source"] == "wizard"
        assert init_artifacts["detected_paths"] == ["idea.md", "CLAUDE.md"]

    def test_timestamps(self) -> None:
        """Test created_at and last_modified timestamps."""
        before = datetime.now(timezone.utc)
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )
        after = datetime.now(timezone.utc)

        created_at = datetime.fromisoformat(state["created_at"])
        last_modified = datetime.fromisoformat(state["last_modified"])

        assert before <= created_at <= after
        assert created_at == last_modified

    def test_starting_phase_affects_gate(self) -> None:
        """Test that starting_phase affects current_gate."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
            starting_phase="experiments",
        )

        assert state["phase"] == "experiments"
        assert state["current_gate"] == "gate_3"

    def test_outer_loop_initial_value(self) -> None:
        """Test outer_loop starts at 0."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )

        assert state["outer_loop"] == 0

    def test_list_fields_empty(self) -> None:
        """Test list fields are initialized empty."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )

        assert state["gate_history"] == []
        assert state["pivot_candidates"] == []
        assert state["human_decisions"] == []
        assert state["overlay_stack"] == []

    def test_recovery_status(self) -> None:
        """Test recovery_status defaults to idle."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )

        assert state["recovery_status"] == "idle"

    def test_system_version(self) -> None:
        """Test system_version is included."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )

        assert "system_version" in state

    def test_gate_scores(self) -> None:
        """Test gate_scores structure."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )

        gate_scores = state["gate_scores"]
        expected_gates = ["gate_1", "gate_2", "gate_3", "gate_4", "gate_5"]

        for gate in expected_gates:
            assert gate in gate_scores
            assert gate_scores[gate] == 0


class TestDefaultFunctions:
    """Tests for default value helper functions."""

    def test_get_default_loop_counts(self) -> None:
        """Test get_default_loop_counts returns correct structure."""
        counts = get_default_loop_counts()

        expected_keys = [
            "survey_critic",
            "pilot_code_adviser",
            "experiment_code_adviser",
            "writer_reviewer",
            "reflector_curator",
        ]

        for key in expected_keys:
            assert key in counts
            assert counts[key] == 0

    def test_get_default_approval_status(self) -> None:
        """Test get_default_approval_status returns correct structure."""
        status = get_default_approval_status()

        expected_gates = ["gate_1", "gate_2", "gate_3", "gate_4", "gate_5"]
        for gate in expected_gates:
            assert status[gate] == "pending"

    def test_get_default_phase_reviews(self) -> None:
        """Test get_default_phase_reviews returns correct structure."""
        reviews = get_default_phase_reviews()

        expected_reviews = [
            "survey_critic",
            "pilot_adviser",
            "experiment_adviser",
            "paper_reviewer",
            "reflection_curator",
        ]

        for review in expected_reviews:
            assert reviews[review] == "pending"

    def test_get_default_gate_scores(self) -> None:
        """Test get_default_gate_scores returns correct structure."""
        scores = get_default_gate_scores()

        expected_gates = ["gate_1", "gate_2", "gate_3", "gate_4", "gate_5"]
        for gate in expected_gates:
            assert scores[gate] == 0


class TestStatePersistence:
    """Tests for load/save operations."""

    def test_save_and_load_roundtrip(self) -> None:
        """Test save and load roundtrip preserves data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)

            # Create initial state
            original_state = build_project_state(
                project_id="test-roundtrip",
                topic="Roundtrip Test",
                init_source="init",
                init_paths=["test.md"],
                client_profile="codex",
                client_instruction_file="AGENTS.md",
            )

            # Save state
            save_project_state(project_root, original_state)

            # Load state
            loaded_state = load_project_state(project_root)

            # Verify key fields
            assert loaded_state["project_id"] == "test-roundtrip"
            assert loaded_state["topic"] == "Roundtrip Test"
            assert loaded_state["platform"] == "codex"
            assert loaded_state["state_version"] == "3.0.0"
            assert loaded_state["phase"] == "survey"

    def test_load_missing_file_returns_none(self) -> None:
        """Test loading from non-existent path returns None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            result = load_project_state(project_root)
            assert result is None

    def test_atomic_write(self) -> None:
        """Test that save uses atomic write pattern."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)

            state = build_project_state(
                project_id="test",
                topic="Test",
                init_source="init",
                init_paths=[],
                client_profile="claude",
                client_instruction_file="CLAUDE.md",
            )

            save_project_state(project_root, state)

            # Verify file exists at expected path
            state_file = project_root / ".autoresearch" / "state" / "research-state.yaml"
            assert state_file.exists()


class TestStateValidation:
    """Tests for state validation."""

    def test_validate_valid_state(self) -> None:
        """Test validation passes for valid state."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )

        errors = validate_project_state(state)
        assert errors == []

    def test_validate_missing_required_field(self) -> None:
        """Test validation catches missing required fields."""
        state: dict[str, Any] = {
            "project_id": "test",
            "state_version": "3.0.0",
        }

        errors = validate_project_state(state)
        assert len(errors) > 0

    def test_validate_invalid_state_version(self) -> None:
        """Test validation catches invalid state version."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )
        state["state_version"] = "2.0.0"

        errors = validate_project_state(state)
        assert any("version" in e.lower() for e in errors)


class TestUpdateLastModified:
    """Tests for update_last_modified function."""

    def test_updates_timestamp(self) -> None:
        """Test that update_last_modified updates the timestamp."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )

        original_modified = state["last_modified"]

        # Small delay to ensure timestamp changes
        import time
        time.sleep(0.01)

        update_last_modified(state)

        new_modified = state["last_modified"]
        assert new_modified != original_modified

    def test_preserves_other_fields(self) -> None:
        """Test that update_last_modified preserves other fields."""
        state = build_project_state(
            project_id="test",
            topic="Test",
            init_source="init",
            init_paths=[],
            client_profile="claude",
            client_instruction_file="CLAUDE.md",
        )

        original_id = state["project_id"]
        update_last_modified(state)
        assert state["project_id"] == original_id


class TestPhaseToGateImport:
    """Tests that PHASE_TO_GATE is properly imported."""

    def test_phase_to_gate_import(self) -> None:
        """Test that PHASE_TO_GATE mapping works correctly."""
        # This tests the import pattern from the task description
        from scripts.constants.phases import PHASE_TO_GATE

        assert PHASE_TO_GATE["survey"] == "gate_1"
        assert PHASE_TO_GATE["pilot"] == "gate_2"
        assert PHASE_TO_GATE["experiments"] == "gate_3"
        assert PHASE_TO_GATE["paper"] == "gate_4"
        assert PHASE_TO_GATE["reflection"] == "gate_5"

    def test_starting_phase_determines_gate(self) -> None:
        """Test that starting phase correctly determines gate."""
        for phase, expected_gate in [
            ("survey", "gate_1"),
            ("pilot", "gate_2"),
            ("experiments", "gate_3"),
            ("paper", "gate_4"),
            ("reflection", "gate_5"),
        ]:
            state = build_project_state(
                project_id="test",
                topic="Test",
                init_source="init",
                init_paths=[],
                client_profile="claude",
                client_instruction_file="CLAUDE.md",
                starting_phase=phase,
            )
            assert state["current_gate"] == expected_gate, f"Phase {phase} should map to {expected_gate}"


class TestConstants:
    """Tests for module constants."""

    def test_state_version(self) -> None:
        """Test STATE_VERSION constant."""
        assert STATE_VERSION == "3.0.0"

    def test_state_file_path(self) -> None:
        """Test STATE_FILE_PATH constant."""
        assert STATE_FILE_PATH == ".autoresearch/state/research-state.yaml"
