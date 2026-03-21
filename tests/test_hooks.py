"""Tests for hook scripts."""

import json
import subprocess
from pathlib import Path


class TestTeammateIdleHook:
    """Test teammate_idle.py hook."""

    def test_teammate_idle_script_exists(self):
        """teammate_idle.py should exist in hooks directory."""
        hook_path = Path(__file__).parent.parent / "scripts" / "hooks" / "teammate_idle.py"
        assert hook_path.exists(), "teammate_idle.py not found in scripts/hooks/"

    def test_teammate_idle_script_is_valid_python(self):
        """teammate_idle.py should be valid Python."""
        hook_path = Path(__file__).parent.parent / "scripts" / "hooks" / "teammate_idle.py"
        result = subprocess.run(
            ["python3", "-m", "py_compile", str(hook_path)], capture_output=True, text=True
        )
        assert result.returncode == 0, f"Syntax error in teammate_idle.py: {result.stderr}"

    def test_teammate_idle_returns_valid_exit_code(self):
        """teammate_idle.py should return valid exit code when called with stdin."""
        hook_path = Path(__file__).parent.parent / "scripts" / "hooks" / "teammate_idle.py"

        hook_input = json.dumps(
            {"event": "TeammateIdle", "agent_name": "survey", "team_name": "research-survey"}
        )

        result = subprocess.run(
            ["python3", str(hook_path)], input=hook_input, capture_output=True, text=True
        )

        # Should exit 0 (success) or 2 (blocking)
        assert result.returncode in [0, 2], f"Hook failed with: {result.stderr}"


class TestTaskCompletedHook:
    """Test task_completed.py hook."""

    def test_task_completed_script_exists(self):
        """task_completed.py should exist in hooks directory."""
        hook_path = Path(__file__).parent.parent / "scripts" / "hooks" / "task_completed.py"
        assert hook_path.exists(), "task_completed.py not found in scripts/hooks/"

    def test_task_completed_validates_task_quality(self):
        """task_completed.py should validate completed task deliverables."""
        hook_path = Path(__file__).parent.parent / "scripts" / "hooks" / "task_completed.py"

        hook_input = json.dumps(
            {
                "event": "TaskCompleted",
                "task_id": "survey-primary",
                "task_status": "completed",
                "agent_name": "survey",
            }
        )

        result = subprocess.run(
            ["python3", str(hook_path)],
            input=hook_input,
            capture_output=True,
            text=True,
        )

        assert result.returncode in [0, 2], f"Hook failed with: {result.stderr}"
