#!/usr/bin/env python3
"""Tests for configure_project.py module."""

from __future__ import annotations

# Add scripts directory to path
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from configure_project import (  # noqa: E402
    configure_project,
    get_nested_value,
    load_project_config,
    load_project_state,
    load_user_config,
    save_project_config,
    save_project_state,
    set_nested_value,
    show_current_config,
    update_config,
    validate_config_value,
)
from constants import DEFAULT_DELIVERABLES  # noqa: E402


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
            "research_type": "ml_experiment",
        }
        state_file = state_dir / "research-state.yaml"
        state_file.write_text(yaml.dump(state_data), encoding="utf-8")

        result = load_project_state(tmp_path)
        assert result["project_id"] == "test-project"
        assert result["topic"] == "Test Topic"

    def test_load_missing_state(self, tmp_path: Path) -> None:
        """Test loading when state file is missing."""
        result = load_project_state(tmp_path)
        assert result == {}


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


class TestLoadUserConfig:
    """Tests for load_user_config function."""

    def test_load_missing_config(self) -> None:
        """Test loading when user config is missing."""
        with patch.object(Path, "home", return_value=Path("/nonexistent")):
            result = load_user_config()
            assert result == {}


class TestSaveProjectState:
    """Tests for save_project_state function."""

    def test_save_state(self, tmp_path: Path) -> None:
        """Test saving state to file."""
        state_data = {
            "project_id": "test-project",
            "topic": "Test Topic",
        }

        save_project_state(tmp_path, state_data)

        # Verify file was created
        state_file = tmp_path / DEFAULT_DELIVERABLES["research_state"]
        assert state_file.exists()

        # Verify content
        loaded = load_project_state(tmp_path)
        assert loaded["project_id"] == "test-project"


class TestSaveProjectConfig:
    """Tests for save_project_config function."""

    def test_save_config(self, tmp_path: Path) -> None:
        """Test saving config to file."""
        config_data = {"max_loops": 5}

        save_project_config(tmp_path, config_data)

        # Verify file was created
        config_file = tmp_path / DEFAULT_DELIVERABLES["project_config"]
        assert config_file.exists()

        # Verify content
        loaded = load_project_config(tmp_path)
        assert loaded["max_loops"] == 5


class TestGetNestedValue:
    """Tests for get_nested_value function."""

    def test_get_simple_value(self) -> None:
        """Test getting a simple value."""
        data = {"name": "test"}
        result = get_nested_value(data, "name")
        assert result == "test"

    def test_get_nested_value(self) -> None:
        """Test getting a nested value."""
        data = {"author": {"name": "John", "email": "john@example.com"}}
        result = get_nested_value(data, "author.name")
        assert result == "John"

    def test_get_missing_value(self) -> None:
        """Test getting a missing value."""
        data = {"name": "test"}
        result = get_nested_value(data, "missing")
        assert result is None

    def test_get_deep_nested_value(self) -> None:
        """Test getting a deeply nested value."""
        data = {"a": {"b": {"c": "value"}}}
        result = get_nested_value(data, "a.b.c")
        assert result == "value"


class TestSetNestedValue:
    """Tests for set_nested_value function."""

    def test_set_simple_value(self) -> None:
        """Test setting a simple value."""
        data = {"name": "old"}
        result = set_nested_value(data, "name", "new")
        assert result["name"] == "new"
        # Original should not be modified
        assert data["name"] == "old"

    def test_set_nested_value(self) -> None:
        """Test setting a nested value."""
        data = {"author": {"name": "old"}}
        result = set_nested_value(data, "author.name", "new")
        assert result["author"]["name"] == "new"

    def test_set_new_nested_path(self) -> None:
        """Test setting a value at a new nested path."""
        data = {}
        result = set_nested_value(data, "author.name", "John")
        assert result["author"]["name"] == "John"


class TestValidateConfigValue:
    """Tests for validate_config_value function."""

    def test_validate_int_valid(self) -> None:
        """Test validating a valid integer."""
        schema = {"type": "int", "min": 1, "max": 10}
        is_valid, error, value = validate_config_value("test", "5", schema)
        assert is_valid
        assert value == 5

    def test_validate_int_out_of_range(self) -> None:
        """Test validating an integer out of range."""
        schema = {"type": "int", "min": 1, "max": 10}
        is_valid, error, value = validate_config_value("test", "15", schema)
        assert not is_valid
        assert "10" in error

    def test_validate_enum_valid(self) -> None:
        """Test validating a valid enum value."""
        schema = {"type": "enum", "values": ["a", "b", "c"]}
        is_valid, error, value = validate_config_value("test", "b", schema)
        assert is_valid
        assert value == "b"

    def test_validate_enum_invalid(self) -> None:
        """Test validating an invalid enum value."""
        schema = {"type": "enum", "values": ["a", "b", "c"]}
        is_valid, error, value = validate_config_value("test", "d", schema)
        assert not is_valid

    def test_validate_string(self) -> None:
        """Test validating a string value."""
        schema = {"type": "string"}
        is_valid, error, value = validate_config_value("test", "hello", schema)
        assert is_valid
        assert value == "hello"


class TestShowCurrentConfig:
    """Tests for show_current_config function."""

    def test_show_basic_config(self, tmp_path: Path) -> None:
        """Test showing basic configuration."""
        state = {
            "topic": "Test Research",
            "research_type": "ml_experiment",
            "loop_limits": {"survey_critic": 3},
            "progress": {"active_gpu": "unassigned"},
            "language_policy": {"process_docs": "zh-CN", "paper_docs": "en-US"},
        }

        result = show_current_config(tmp_path, state, {}, {})

        assert "Test Research" in result
        assert "ml_experiment" in result
        assert "zh-CN" in result

    def test_show_with_user_config(self, tmp_path: Path) -> None:
        """Test showing configuration with user info."""
        state = {
            "topic": "Test",
            "research_type": "ml_experiment",
            "loop_limits": {},
            "progress": {},
            "language_policy": {},
        }
        user_config = {
            "author": {
                "name": "Test User",
                "email": "test@example.com",
            }
        }

        result = show_current_config(tmp_path, state, {}, user_config)

        assert "Test User" in result
        assert "test@example.com" in result


class TestUpdateConfig:
    """Tests for update_config function."""

    def test_update_idea(self, tmp_path: Path) -> None:
        """Test updating research idea."""
        state = {"topic": "Old idea", "research_type": "ml_experiment"}
        project_config = {}
        user_config = {}

        new_state, new_project_config, new_user_config, message = update_config(
            "idea", "New idea", "project", state, project_config, user_config
        )

        assert new_state["topic"] == "New idea"
        assert "已更新" in message

    def test_update_max_loops(self, tmp_path: Path) -> None:
        """Test updating max loops."""
        state = {
            "topic": "Test",
            "loop_limits": {"survey_critic": 3, "pilot_code_adviser": 3},
        }
        project_config = {}
        user_config = {}

        new_state, new_project_config, new_user_config, message = update_config(
            "max-loops", "5", "project", state, project_config, user_config
        )

        assert new_state["loop_limits"]["survey_critic"] == 5
        assert new_state["loop_limits"]["pilot_code_adviser"] == 5

    def test_update_invalid_key(self, tmp_path: Path) -> None:
        """Test updating with invalid key."""
        state = {}
        project_config = {}
        user_config = {}

        new_state, new_project_config, new_user_config, message = update_config(
            "invalid-key", "value", "project", state, project_config, user_config
        )

        assert "未知" in message

    def test_update_user_config(self, tmp_path: Path) -> None:
        """Test updating user configuration."""
        state = {}
        project_config = {}
        user_config = {}

        new_state, new_project_config, new_user_config, message = update_config(
            "author.name", "John Doe", "user", state, project_config, user_config
        )

        assert new_user_config["author"]["name"] == "John Doe"


class TestConfigureProject:
    """Tests for configure_project function."""

    def test_show_action(self, tmp_path: Path) -> None:
        """Test show action."""
        # Create project structure
        autoresearch = tmp_path / ".autoresearch"
        state_dir = autoresearch / "state"
        state_dir.mkdir(parents=True)

        # Create state file
        state_data = {
            "project_id": "test",
            "topic": "Test Topic",
            "research_type": "ml_experiment",
            "loop_limits": {},
            "progress": {},
            "language_policy": {},
        }
        state_file = state_dir / "research-state.yaml"
        state_file.write_text(yaml.dump(state_data), encoding="utf-8")

        result = configure_project(tmp_path, action="show")

        assert result["action"] == "show"
        assert "message" in result
        assert "Test Topic" in result["message"]

    def test_set_action(self, tmp_path: Path) -> None:
        """Test set action."""
        # Create project structure
        autoresearch = tmp_path / ".autoresearch"
        state_dir = autoresearch / "state"
        state_dir.mkdir(parents=True)

        # Create state file
        state_data = {
            "project_id": "test",
            "topic": "Old Topic",
            "research_type": "ml_experiment",
            "loop_limits": {},
            "progress": {},
            "language_policy": {},
        }
        state_file = state_dir / "research-state.yaml"
        state_file.write_text(yaml.dump(state_data), encoding="utf-8")

        result = configure_project(
            tmp_path,
            action="set",
            key="idea",
            value="New Topic",
        )

        assert result["action"] == "set"
        assert result["state"]["topic"] == "New Topic"

    def test_set_missing_params(self, tmp_path: Path) -> None:
        """Test set action with missing parameters."""
        # Create project structure
        autoresearch = tmp_path / ".autoresearch"
        state_dir = autoresearch / "state"
        state_dir.mkdir(parents=True)

        state_data = {"project_id": "test"}
        state_file = state_dir / "research-state.yaml"
        state_file.write_text(yaml.dump(state_data), encoding="utf-8")

        with pytest.raises(ValueError):
            configure_project(tmp_path, action="set")

    def test_missing_project(self, tmp_path: Path) -> None:
        """Test with missing project."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        # configure_project doesn't raise, it returns None or error dict
        # The main() function handles the project check
        result = configure_project(empty_dir, action="show")
        # Should still work but with empty state
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
