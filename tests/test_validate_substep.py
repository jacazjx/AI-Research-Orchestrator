"""Tests for validate_substep.py module."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
import yaml

from scripts.validate_substep import (
    REVIEW_APPROVED,
    REVIEW_PENDING,
    STATUS_APPROVED,
    STATUS_PENDING,
    can_advance_substep,
    check_required_artifacts,
    check_review_approval,
    get_first_substep,
    get_next_substep,
    get_phase_substeps,
    get_substep_config,
    load_orchestrator_config,
    load_research_state,
    update_substep_status,
    validate_substep,
)


@pytest.fixture
def temp_project_root():
    """Create a temporary project directory with required structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)

        # Create required directories
        (root / ".autoresearch" / "state").mkdir(parents=True)
        (root / ".autoresearch" / "config").mkdir(parents=True)
        (root / "docs" / "reports" / "survey").mkdir(parents=True)
        (root / "docs" / "reports" / "pilot").mkdir(parents=True)
        (root / "paper").mkdir(parents=True)

        yield root


@pytest.fixture
def sample_state():
    """Sample research state dictionary."""
    return {
        "project_id": "test-project",
        "topic": "Test topic",
        "current_phase": "survey",
        "approval_status": {
            "gate_1": "pending",
            "gate_2": "pending",
        },
        "substep_status": {
            "survey": {
                "literature_survey": {
                    "status": "approved",
                    "review_result": "approved",
                    "attempts": 1,
                },
                "idea_definition": {
                    "status": "in_progress",
                    "review_result": "pending",
                },
                "research_plan": {
                    "status": "pending",
                },
            },
            "pilot": {
                "problem_analysis": {"status": "pending"},
                "pilot_design": {"status": "pending"},
                "pilot_execution": {"status": "pending"},
            },
        },
    }


@pytest.fixture
def sample_config():
    """Sample orchestrator config dictionary."""
    return {
        "phases": {
            "survey": {
                "agents": {"primary": "survey", "reviewer": "critic"},
                "substeps": [
                    {
                        "name": "literature_survey",
                        "primary_skill": "research-lit",
                        "reviewer_skill": "audit-survey",
                        "required_artifacts": ["docs/reports/survey/literature-review.md"],
                    },
                    {
                        "name": "idea_definition",
                        "primary_skill": "define-idea",
                        "reviewer_skill": "novelty-check",
                        "required_artifacts": ["docs/reports/survey/idea-definition.md"],
                    },
                    {
                        "name": "research_plan",
                        "primary_skill": "research-plan",
                        "reviewer_skill": "audit-plan",
                        "required_artifacts": ["docs/reports/survey/research-readiness-report.md"],
                    },
                ],
            },
        },
    }


class TestCheckRequiredArtifacts:
    """Tests for check_required_artifacts function."""

    def test_all_artifacts_exist(self, temp_project_root):
        """Test when all required artifacts exist."""
        # Create artifacts
        artifact1 = temp_project_root / "docs/reports/survey/literature-review.md"
        artifact2 = temp_project_root / "docs/reports/survey/idea-definition.md"
        artifact1.parent.mkdir(parents=True, exist_ok=True)
        artifact1.write_text("content")
        artifact2.write_text("content")

        result = check_required_artifacts(
            temp_project_root,
            [
                "docs/reports/survey/literature-review.md",
                "docs/reports/survey/idea-definition.md",
            ],
        )

        assert result["all_exist"] is True
        assert len(result["missing"]) == 0
        assert len(result["existing"]) == 2

    def test_some_artifacts_missing(self, temp_project_root):
        """Test when some artifacts are missing."""
        artifact1 = temp_project_root / "docs/reports/survey/literature-review.md"
        artifact1.parent.mkdir(parents=True, exist_ok=True)
        artifact1.write_text("content")

        result = check_required_artifacts(
            temp_project_root,
            [
                "docs/reports/survey/literature-review.md",
                "docs/reports/survey/missing.md",
            ],
        )

        assert result["all_exist"] is False
        assert len(result["missing"]) == 1
        assert "docs/reports/survey/missing.md" in result["missing"]
        assert "docs/reports/survey/literature-review.md" in result["existing"]

    def test_no_artifacts_required(self, temp_project_root):
        """Test when no artifacts are required."""
        result = check_required_artifacts(temp_project_root, [])

        assert result["all_exist"] is True
        assert len(result["missing"]) == 0
        assert len(result["existing"]) == 0


class TestCheckReviewApproval:
    """Tests for check_review_approval function."""

    def test_review_approved(self, sample_state):
        """Test when review is approved."""
        result = check_review_approval(sample_state, "survey", "literature_survey")

        assert result["approved"] is True
        assert result["status"] == STATUS_APPROVED
        assert result["review_result"] == REVIEW_APPROVED

    def test_review_pending(self, sample_state):
        """Test when review is pending."""
        result = check_review_approval(sample_state, "survey", "idea_definition")

        assert result["approved"] is False
        assert result["status"] == "in_progress"
        assert result["review_result"] == REVIEW_PENDING

    def test_substep_not_found(self, sample_state):
        """Test when substep is not in state."""
        result = check_review_approval(sample_state, "survey", "nonexistent")

        assert result["approved"] is False
        assert result["status"] == STATUS_PENDING
        assert result["review_result"] == REVIEW_PENDING

    def test_phase_not_in_state(self, sample_state):
        """Test when phase is not in substep_status."""
        result = check_review_approval(sample_state, "nonexistent", "substep")

        assert result["approved"] is False


class TestGetPhaseSubsteps:
    """Tests for get_phase_substeps function."""

    def test_get_substeps_from_config(self, sample_config):
        """Test getting substeps from config."""
        substeps = get_phase_substeps(sample_config, "survey")

        assert len(substeps) == 3
        assert substeps[0]["name"] == "literature_survey"
        assert substeps[1]["name"] == "idea_definition"
        assert substeps[2]["name"] == "research_plan"

    def test_get_substeps_missing_phase(self, sample_config):
        """Test getting substeps for missing phase."""
        substeps = get_phase_substeps(sample_config, "nonexistent")

        assert substeps == []

    def test_get_substeps_default_config(self):
        """Test getting substeps from default config."""
        substeps = get_phase_substeps({}, "pilot")

        # Uses DEFAULT_SUBSTEPS
        assert len(substeps) == 3


class TestGetSubstepConfig:
    """Tests for get_substep_config function."""

    def test_get_existing_substep(self, sample_config):
        """Test getting existing substep config."""
        substep = get_substep_config(sample_config, "survey", "literature_survey")

        assert substep is not None
        assert substep["primary_skill"] == "research-lit"
        assert substep["reviewer_skill"] == "audit-survey"

    def test_get_nonexistent_substep(self, sample_config):
        """Test getting nonexistent substep."""
        substep = get_substep_config(sample_config, "survey", "nonexistent")

        assert substep is None


class TestGetNextSubstep:
    """Tests for get_next_substep function."""

    def test_get_next_substep_success(self, sample_config):
        """Test getting next substep."""
        next_substep = get_next_substep(sample_config, "survey", "literature_survey")

        assert next_substep == "idea_definition"

    def test_get_next_substep_last(self, sample_config):
        """Test getting next substep when current is last."""
        next_substep = get_next_substep(sample_config, "survey", "research_plan")

        assert next_substep is None

    def test_get_next_substep_nonexistent(self, sample_config):
        """Test getting next substep for nonexistent current."""
        next_substep = get_next_substep(sample_config, "survey", "nonexistent")

        assert next_substep is None


class TestGetFirstSubstep:
    """Tests for get_first_substep function."""

    def test_get_first_substep(self, sample_config):
        """Test getting first substep."""
        first = get_first_substep(sample_config, "survey")

        assert first == "literature_survey"

    def test_get_first_substep_empty_phase(self):
        """Test getting first substep for empty phase."""
        first = get_first_substep({}, "nonexistent")

        assert first is None


class TestLoadResearchState:
    """Tests for load_research_state function."""

    def test_load_existing_state(self, temp_project_root, sample_state):
        """Test loading existing state file."""
        state_path = temp_project_root / ".autoresearch" / "state" / "research-state.yaml"
        state_path.write_text(yaml.dump(sample_state), encoding="utf-8")

        state = load_research_state(temp_project_root)

        assert state["project_id"] == "test-project"
        assert state["current_phase"] == "survey"

    def test_load_missing_state(self, temp_project_root):
        """Test loading missing state file."""
        with pytest.raises(FileNotFoundError):
            load_research_state(temp_project_root)


class TestLoadOrchestratorConfig:
    """Tests for load_orchestrator_config function."""

    def test_load_existing_config(self, temp_project_root, sample_config):
        """Test loading existing config file."""
        config_path = temp_project_root / ".autoresearch" / "config" / "orchestrator-config.yaml"
        config_path.write_text(yaml.dump(sample_config), encoding="utf-8")

        config = load_orchestrator_config(temp_project_root)

        assert "phases" in config
        assert "survey" in config["phases"]

    def test_load_missing_config(self, temp_project_root):
        """Test loading missing config returns default."""
        config = load_orchestrator_config(temp_project_root)

        # Should return default config with phases
        assert "phases" in config


class TestValidateSubstep:
    """Tests for validate_substep function."""

    def test_validate_substep_can_proceed(self, temp_project_root, sample_state, sample_config):
        """Test validation when substep can proceed."""
        # Setup state
        state_path = temp_project_root / ".autoresearch" / "state" / "research-state.yaml"
        state_path.write_text(yaml.dump(sample_state), encoding="utf-8")

        # Setup config
        config_path = temp_project_root / ".autoresearch" / "config" / "orchestrator-config.yaml"
        config_path.write_text(yaml.dump(sample_config), encoding="utf-8")

        # literature_survey is first substep, should be able to proceed
        result = validate_substep(temp_project_root, "survey", "literature_survey")

        assert result["can_proceed"] is True
        assert result["previous_substeps_complete"] is True
        assert len(result["errors"]) == 0

    def test_validate_substep_previous_not_approved(self, temp_project_root, sample_config):
        """Test validation when previous substep not approved."""
        # Setup state where literature_survey is pending
        state = {
            "project_id": "test",
            "substep_status": {
                "survey": {
                    "literature_survey": {
                        "status": "in_progress",
                        "review_result": "pending",
                    },
                    "idea_definition": {"status": "pending"},
                    "research_plan": {"status": "pending"},
                }
            },
        }
        state_path = temp_project_root / ".autoresearch" / "state" / "research-state.yaml"
        state_path.write_text(yaml.dump(state), encoding="utf-8")

        config_path = temp_project_root / ".autoresearch" / "config" / "orchestrator-config.yaml"
        config_path.write_text(yaml.dump(sample_config), encoding="utf-8")

        # idea_definition is second substep, cannot proceed without first being approved
        result = validate_substep(temp_project_root, "survey", "idea_definition")

        assert result["can_proceed"] is False
        assert result["previous_substeps_complete"] is False
        assert len(result["errors"]) > 0
        assert "literature_survey" in result["errors"][0]

    def test_validate_substep_missing_state(self, temp_project_root):
        """Test validation with missing state file."""
        result = validate_substep(temp_project_root, "survey", "literature_survey")

        assert result["can_proceed"] is False
        assert "Research state file not found" in result["errors"]


class TestCanAdvanceSubstep:
    """Tests for can_advance_substep function."""

    def test_can_advance_success(self, temp_project_root, sample_state, sample_config):
        """Test when substep can advance."""
        # Create artifact
        artifact = temp_project_root / "docs/reports/survey/literature-review.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("content")

        # Setup state with approved review
        state_path = temp_project_root / ".autoresearch" / "state" / "research-state.yaml"
        state_path.write_text(yaml.dump(sample_state), encoding="utf-8")

        config_path = temp_project_root / ".autoresearch" / "config" / "orchestrator-config.yaml"
        config_path.write_text(yaml.dump(sample_config), encoding="utf-8")

        result = can_advance_substep(temp_project_root, "survey", "literature_survey")

        assert result["can_advance"] is True
        assert result["reason"] == "All checks passed"
        assert result["details"]["next_substep"] == "idea_definition"

    def test_cannot_advance_review_not_approved(self, temp_project_root, sample_config):
        """Test when review not approved."""
        state = {
            "project_id": "test",
            "substep_status": {
                "survey": {
                    "literature_survey": {
                        "status": "in_progress",
                        "review_result": "pending",
                    },
                }
            },
        }
        state_path = temp_project_root / ".autoresearch" / "state" / "research-state.yaml"
        state_path.write_text(yaml.dump(state), encoding="utf-8")

        config_path = temp_project_root / ".autoresearch" / "config" / "orchestrator-config.yaml"
        config_path.write_text(yaml.dump(sample_config), encoding="utf-8")

        result = can_advance_substep(temp_project_root, "survey", "literature_survey")

        assert result["can_advance"] is False
        assert "Review not approved" in result["reason"]

    def test_cannot_advance_artifacts_missing(self, temp_project_root, sample_config):
        """Test when artifacts are missing."""
        state = {
            "project_id": "test",
            "substep_status": {
                "survey": {
                    "literature_survey": {
                        "status": "approved",
                        "review_result": "approved",
                    },
                }
            },
        }
        state_path = temp_project_root / ".autoresearch" / "state" / "research-state.yaml"
        state_path.write_text(yaml.dump(state), encoding="utf-8")

        config_path = temp_project_root / ".autoresearch" / "config" / "orchestrator-config.yaml"
        config_path.write_text(yaml.dump(sample_config), encoding="utf-8")

        result = can_advance_substep(temp_project_root, "survey", "literature_survey")

        assert result["can_advance"] is False
        assert "artifacts missing" in result["reason"]


class TestUpdateSubstepStatus:
    """Tests for update_substep_status function."""

    def test_update_status(self, temp_project_root, sample_state):
        """Test updating substep status."""
        state_path = temp_project_root / ".autoresearch" / "state" / "research-state.yaml"
        state_path.write_text(yaml.dump(sample_state), encoding="utf-8")

        update_substep_status(
            temp_project_root,
            "survey",
            "idea_definition",
            STATUS_APPROVED,
            review_result=REVIEW_APPROVED,
            last_agent="survey",
        )

        updated_state = load_research_state(temp_project_root)
        substep = updated_state["substep_status"]["survey"]["idea_definition"]

        assert substep["status"] == STATUS_APPROVED
        assert substep["review_result"] == REVIEW_APPROVED
        assert substep["last_agent"] == "survey"

    def test_update_attempts(self, temp_project_root, sample_state):
        """Test updating attempts count."""
        state_path = temp_project_root / ".autoresearch" / "state" / "research-state.yaml"
        state_path.write_text(yaml.dump(sample_state), encoding="utf-8")

        update_substep_status(
            temp_project_root,
            "survey",
            "idea_definition",
            "in_progress",
            attempts=2,
        )

        updated_state = load_research_state(temp_project_root)
        substep = updated_state["substep_status"]["survey"]["idea_definition"]

        assert substep["attempts"] == 2

    def test_create_missing_substep(self, temp_project_root):
        """Test creating missing substep in state."""
        state = {
            "project_id": "test",
            "substep_status": {
                "survey": {},
            },
        }
        state_path = temp_project_root / ".autoresearch" / "state" / "research-state.yaml"
        state_path.write_text(yaml.dump(state), encoding="utf-8")

        update_substep_status(
            temp_project_root,
            "survey",
            "new_substep",
            "in_progress",
        )

        updated_state = load_research_state(temp_project_root)
        substep = updated_state["substep_status"]["survey"]["new_substep"]

        assert substep["status"] == "in_progress"
        assert substep["attempts"] == 1


class TestEdgeCases:
    """Edge case tests for validate_substep module."""

    def test_malformed_yaml_state(self, temp_project_root):
        """Test handling of malformed YAML in state file."""
        state_path = temp_project_root / ".autoresearch" / "state" / "research-state.yaml"
        state_path.write_text("invalid: yaml: content: [", encoding="utf-8")

        with pytest.raises(yaml.YAMLError):
            load_research_state(temp_project_root)

    def test_empty_state_file(self, temp_project_root):
        """Test handling of empty state file."""
        state_path = temp_project_root / ".autoresearch" / "state" / "research-state.yaml"
        state_path.write_text("", encoding="utf-8")

        state = load_research_state(temp_project_root)
        assert state is None

    def test_phase_not_in_default_substeps(self, temp_project_root):
        """Test getting substeps for phase not in DEFAULT_SUBSTEPS."""
        substeps = get_phase_substeps({}, "nonexistent_phase")

        assert substeps == []

    def test_artifact_in_nested_directory(self, temp_project_root):
        """Test artifact check with deeply nested directory."""
        artifact = temp_project_root / "docs" / "reports" / "survey" / "nested" / "deep" / "file.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("content", encoding="utf-8")

        result = check_required_artifacts(
            temp_project_root,
            ["docs/reports/survey/nested/deep/file.md"],
        )

        assert result["all_exist"] is True

    def test_substep_config_with_missing_fields(self, temp_project_root, sample_state):
        """Test substep config with missing optional fields."""
        config = {
            "phases": {
                "survey": {
                    "substeps": [
                        {
                            "name": "minimal_substep",
                            # Missing primary_skill, reviewer_skill, required_artifacts
                        }
                    ]
                }
            }
        }

        substep = get_substep_config(config, "survey", "minimal_substep")

        assert substep is not None
        assert substep["name"] == "minimal_substep"
        assert substep.get("primary_skill") is None
        assert substep.get("required_artifacts", []) == []

    def test_validate_substep_not_in_config(self, temp_project_root, sample_state, sample_config):
        """Test validation when substep is not in config."""
        state_path = temp_project_root / ".autoresearch" / "state" / "research-state.yaml"
        state_path.write_text(yaml.dump(sample_state), encoding="utf-8")

        config_path = temp_project_root / ".autoresearch" / "config" / "orchestrator-config.yaml"
        config_path.write_text(yaml.dump(sample_config), encoding="utf-8")

        result = validate_substep(temp_project_root, "survey", "nonexistent_substep")

        assert result["can_proceed"] is False
        assert any("not found" in err for err in result["errors"])

    def test_can_advance_with_no_artifacts_required(self, temp_project_root, sample_config):
        """Test can_advance when substep has no required artifacts."""
        # Add substep with no required artifacts
        config = {
            "phases": {
                "survey": {
                    "substeps": [
                        {
                            "name": "no_artifacts_substep",
                            "primary_skill": "test",
                            "reviewer_skill": "test-review",
                            "required_artifacts": [],
                        }
                    ]
                }
            }
        }

        state = {
            "project_id": "test",
            "substep_status": {
                "survey": {
                    "no_artifacts_substep": {
                        "status": "approved",
                        "review_result": "approved",
                    }
                }
            },
        }

        state_path = temp_project_root / ".autoresearch" / "state" / "research-state.yaml"
        state_path.write_text(yaml.dump(state), encoding="utf-8")

        config_path = temp_project_root / ".autoresearch" / "config" / "orchestrator-config.yaml"
        config_path.write_text(yaml.dump(config), encoding="utf-8")

        result = can_advance_substep(temp_project_root, "survey", "no_artifacts_substep")

        assert result["can_advance"] is True

    def test_update_substep_status_with_all_fields(self, temp_project_root, sample_state):
        """Test updating substep status with all optional fields."""
        state_path = temp_project_root / ".autoresearch" / "state" / "research-state.yaml"
        state_path.write_text(yaml.dump(sample_state), encoding="utf-8")

        update_substep_status(
            temp_project_root,
            "survey",
            "idea_definition",
            STATUS_APPROVED,
            review_result=REVIEW_APPROVED,
            last_agent="critic",
            attempts=5,
        )

        updated_state = load_research_state(temp_project_root)
        substep = updated_state["substep_status"]["survey"]["idea_definition"]

        assert substep["status"] == STATUS_APPROVED
        assert substep["review_result"] == REVIEW_APPROVED
        assert substep["last_agent"] == "critic"
        assert substep["attempts"] == 5

    def test_check_review_approval_with_empty_substep_status(self, temp_project_root):
        """Test check_review_approval with empty substep_status."""
        state = {"project_id": "test", "substep_status": {}}

        result = check_review_approval(state, "survey", "literature_survey")

        assert result["approved"] is False
        assert result["status"] == STATUS_PENDING

    def test_get_next_substep_with_single_substep(self, temp_project_root):
        """Test get_next_substep when phase has only one substep."""
        config = {
            "phases": {"survey": {"substeps": [{"name": "only_substep", "primary_skill": "test"}]}}
        }

        next_substep = get_next_substep(config, "survey", "only_substep")

        assert next_substep is None

    def test_artifact_with_special_characters_in_path(self, temp_project_root):
        """Test artifact check with special characters in path."""
        artifact = (
            temp_project_root
            / "docs"
            / "reports"
            / "survey"
            / "file-with-dashes_and_underscores.md"
        )
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("content", encoding="utf-8")

        result = check_required_artifacts(
            temp_project_root,
            ["docs/reports/survey/file-with-dashes_and_underscores.md"],
        )

        assert result["all_exist"] is True
