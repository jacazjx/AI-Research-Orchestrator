#!/usr/bin/env python3
"""Tests for config_io.py module (renamed from configure_project.py)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from config_io import (  # noqa: E402
    get_config,
    set_config,
    validate_config_value,
)
from constants import DEFAULT_DELIVERABLES  # noqa: E402


class TestValidateConfigValue:
    """Tests for validate_config_value function."""

    def test_validate_int_valid(self) -> None:
        schema = {"type": "int", "min": 1, "max": 10}
        is_valid, error, value = validate_config_value("test", "5", schema)
        assert is_valid
        assert value == 5

    def test_validate_int_out_of_range(self) -> None:
        schema = {"type": "int", "min": 1, "max": 10}
        is_valid, error, value = validate_config_value("test", "15", schema)
        assert not is_valid

    def test_validate_enum_valid(self) -> None:
        schema = {"type": "enum", "values": ["a", "b", "c"]}
        is_valid, error, value = validate_config_value("test", "b", schema)
        assert is_valid
        assert value == "b"

    def test_validate_enum_invalid(self) -> None:
        schema = {"type": "enum", "values": ["a", "b", "c"]}
        is_valid, error, value = validate_config_value("test", "d", schema)
        assert not is_valid

    def test_validate_string(self) -> None:
        schema = {"type": "string"}
        is_valid, error, value = validate_config_value("test", "hello", schema)
        assert is_valid
        assert value == "hello"

    def test_validate_auto_detect_schema(self) -> None:
        """Test auto-detection of schema from known keys."""
        is_valid, error, value = validate_config_value("research-type", "theory")
        assert is_valid
        assert value == "theory"

    def test_validate_auto_detect_unknown_key(self) -> None:
        """Unknown key with no schema defaults to string."""
        is_valid, error, value = validate_config_value("unknown-key", "anything")
        assert is_valid


class TestGetConfig:
    """Tests for get_config function."""

    def test_get_project_config(self, tmp_path: Path) -> None:
        state_dir = tmp_path / ".autoresearch" / "state"
        state_dir.mkdir(parents=True)
        state_data = {
            "project_id": "test",
            "topic": "Test Topic",
            "research_type": "ml_experiment",
        }
        state_file = state_dir / "research-state.yaml"
        state_file.write_text(yaml.dump(state_data), encoding="utf-8")

        result = get_config(tmp_path, "idea")
        assert result["value"] == "Test Topic"
        assert result["scope"] == "project"

    def test_get_unknown_key(self, tmp_path: Path) -> None:
        result = get_config(tmp_path, "nonexistent-key")
        assert "error" in result

    def test_get_missing_state(self, tmp_path: Path) -> None:
        result = get_config(tmp_path, "idea")
        assert result["value"] is None


class TestSetConfig:
    """Tests for set_config function."""

    def test_set_idea(self, tmp_path: Path) -> None:
        state_dir = tmp_path / ".autoresearch" / "state"
        state_dir.mkdir(parents=True)
        state_data = {"project_id": "test", "topic": "Old"}
        state_file = state_dir / "research-state.yaml"
        state_file.write_text(yaml.dump(state_data), encoding="utf-8")

        result = set_config(tmp_path, "idea", "New Idea")
        assert result["value"] == "New Idea"
        assert result["scope"] == "project"

    def test_set_unknown_key(self, tmp_path: Path) -> None:
        result = set_config(tmp_path, "nonexistent-key", "value")
        assert "error" in result

    def test_set_invalid_value(self, tmp_path: Path) -> None:
        state_dir = tmp_path / ".autoresearch" / "state"
        state_dir.mkdir(parents=True)
        state_data = {"project_id": "test"}
        state_file = state_dir / "research-state.yaml"
        state_file.write_text(yaml.dump(state_data), encoding="utf-8")

        result = set_config(tmp_path, "research-type", "invalid-type")
        assert "error" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
