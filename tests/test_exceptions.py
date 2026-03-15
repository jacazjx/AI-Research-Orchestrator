import importlib.util
import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def load_script_module(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


EXCEPTIONS = load_script_module("exceptions")


class ExceptionsTest(unittest.TestCase):
    def test_orchestrator_error_basic(self) -> None:
        """Test basic OrchestratorError."""
        error = EXCEPTIONS.OrchestratorError("Test error")

        self.assertEqual(str(error), "Test error")
        self.assertEqual(error.message, "Test error")
        self.assertEqual(error.context, {})

    def test_orchestrator_error_with_context(self) -> None:
        """Test OrchestratorError with context."""
        error = EXCEPTIONS.OrchestratorError("Test error", context={"key": "value"})

        self.assertEqual(error.context, {"key": "value"})

    def test_state_error_basic(self) -> None:
        """Test basic StateError."""
        error = EXCEPTIONS.StateError("State error")

        self.assertEqual(error.message, "State error")
        self.assertIsNone(error.state_file)
        self.assertIsNone(error.field)

    def test_state_error_with_params(self) -> None:
        """Test StateError with all parameters."""
        error = EXCEPTIONS.StateError(
            "State error",
            state_file="state.yaml",
            field="current_phase",
            context={"extra": "info"},
        )

        self.assertEqual(error.state_file, "state.yaml")
        self.assertEqual(error.field, "current_phase")
        self.assertEqual(error.context, {"extra": "info"})

    def test_validation_error_basic(self) -> None:
        """Test basic ValidationError."""
        error = EXCEPTIONS.ValidationError("Validation failed")

        self.assertEqual(error.message, "Validation failed")
        self.assertEqual(error.errors, [])

    def test_validation_error_with_errors(self) -> None:
        """Test ValidationError with errors list."""
        error = EXCEPTIONS.ValidationError(
            "Validation failed",
            errors=["Error 1", "Error 2"],
            context={"field": "test"},
        )

        self.assertEqual(error.errors, ["Error 1", "Error 2"])
        self.assertEqual(error.context, {"field": "test"})

    def test_path_security_error_basic(self) -> None:
        """Test basic PathSecurityError."""
        error = EXCEPTIONS.PathSecurityError("Path violation")

        self.assertEqual(error.message, "Path violation")
        self.assertIsNone(error.path)
        self.assertIsNone(error.reason)

    def test_path_security_error_with_params(self) -> None:
        """Test PathSecurityError with parameters."""
        error = EXCEPTIONS.PathSecurityError(
            "Path violation",
            path="../../../etc/passwd",
            reason="Directory traversal detected",
            context={"user": "test"},
        )

        self.assertEqual(error.path, "../../../etc/passwd")
        self.assertEqual(error.reason, "Directory traversal detected")

    def test_command_execution_error_basic(self) -> None:
        """Test basic CommandExecutionError."""
        error = EXCEPTIONS.CommandExecutionError("Command failed")

        self.assertEqual(error.message, "Command failed")
        self.assertIsNone(error.command)
        self.assertIsNone(error.exit_code)
        self.assertIsNone(error.stdout)
        self.assertIsNone(error.stderr)

    def test_command_execution_error_with_params(self) -> None:
        """Test CommandExecutionError with all parameters."""
        error = EXCEPTIONS.CommandExecutionError(
            "Command failed",
            command=["python", "script.py"],
            exit_code=1,
            stdout="output",
            stderr="error",
            context={"cwd": "/tmp"},
        )

        self.assertEqual(error.command, ["python", "script.py"])
        self.assertEqual(error.exit_code, 1)
        self.assertEqual(error.stdout, "output")
        self.assertEqual(error.stderr, "error")
        self.assertEqual(error.context, {"cwd": "/tmp"})

    def test_configuration_error_basic(self) -> None:
        """Test basic ConfigurationError."""
        error = EXCEPTIONS.ConfigurationError("Config error")

        self.assertEqual(error.message, "Config error")
        self.assertIsNone(error.config_file)
        self.assertIsNone(error.key)

    def test_configuration_error_with_params(self) -> None:
        """Test ConfigurationError with parameters."""
        error = EXCEPTIONS.ConfigurationError(
            "Missing config key",
            config_file="config.yaml",
            key="api_key",
            context={"env": "prod"},
        )

        self.assertEqual(error.config_file, "config.yaml")
        self.assertEqual(error.key, "api_key")

    def test_phase_transition_error_basic(self) -> None:
        """Test basic PhaseTransitionError."""
        error = EXCEPTIONS.PhaseTransitionError("Invalid transition")

        self.assertEqual(error.message, "Invalid transition")
        self.assertIsNone(error.from_phase)
        self.assertIsNone(error.to_phase)
        self.assertIsNone(error.reason)

    def test_phase_transition_error_with_params(self) -> None:
        """Test PhaseTransitionError with parameters."""
        error = EXCEPTIONS.PhaseTransitionError(
            "Invalid phase transition",
            from_phase="survey",
            to_phase="paper",
            reason="Must go through pilot phase first",
            context={"gate": "gate_2"},
        )

        self.assertEqual(error.from_phase, "survey")
        self.assertEqual(error.to_phase, "paper")
        self.assertEqual(error.reason, "Must go through pilot phase first")

    def test_template_error_basic(self) -> None:
        """Test basic TemplateError."""
        error = EXCEPTIONS.TemplateError("Template error")

        self.assertEqual(error.message, "Template error")
        self.assertIsNone(error.template_path)
        self.assertIsNone(error.variable)

    def test_template_error_with_params(self) -> None:
        """Test TemplateError with parameters."""
        error = EXCEPTIONS.TemplateError(
            "Missing template variable",
            template_path="templates/report.md",
            variable="topic",
            context={"role": "survey"},
        )

        self.assertEqual(error.template_path, "templates/report.md")
        self.assertEqual(error.variable, "topic")

    def test_dependency_error_basic(self) -> None:
        """Test basic DependencyError."""
        error = EXCEPTIONS.DependencyError("Dependency missing")

        self.assertEqual(error.message, "Dependency missing")
        self.assertIsNone(error.dependency)
        self.assertIsNone(error.path)

    def test_dependency_error_with_params(self) -> None:
        """Test DependencyError with parameters."""
        error = EXCEPTIONS.DependencyError(
            "Missing dependency",
            dependency="latex-citation-curator",
            path="/skills/latex-citation-curator",
            context={"version": "1.0"},
        )

        self.assertEqual(error.dependency, "latex-citation-curator")
        self.assertEqual(error.path, "/skills/latex-citation-curator")

    def test_exception_inheritance(self) -> None:
        """Test that all exceptions inherit from OrchestratorError."""
        self.assertTrue(issubclass(EXCEPTIONS.StateError, EXCEPTIONS.OrchestratorError))
        self.assertTrue(issubclass(EXCEPTIONS.ValidationError, EXCEPTIONS.OrchestratorError))
        self.assertTrue(issubclass(EXCEPTIONS.PathSecurityError, EXCEPTIONS.OrchestratorError))
        self.assertTrue(issubclass(EXCEPTIONS.CommandExecutionError, EXCEPTIONS.OrchestratorError))
        self.assertTrue(issubclass(EXCEPTIONS.ConfigurationError, EXCEPTIONS.OrchestratorError))
        self.assertTrue(issubclass(EXCEPTIONS.PhaseTransitionError, EXCEPTIONS.OrchestratorError))
        self.assertTrue(issubclass(EXCEPTIONS.TemplateError, EXCEPTIONS.OrchestratorError))
        self.assertTrue(issubclass(EXCEPTIONS.DependencyError, EXCEPTIONS.OrchestratorError))

    def test_exception_catch_as_base(self) -> None:
        """Test that exceptions can be caught as OrchestratorError."""
        with self.assertRaises(EXCEPTIONS.OrchestratorError):
            raise EXCEPTIONS.StateError("Test")

        with self.assertRaises(EXCEPTIONS.OrchestratorError):
            raise EXCEPTIONS.ValidationError("Test")

        with self.assertRaises(EXCEPTIONS.OrchestratorError):
            raise EXCEPTIONS.ConfigurationError("Test")

    def test_exception_is_exception(self) -> None:
        """Test that OrchestratorError is an Exception."""
        self.assertTrue(issubclass(EXCEPTIONS.OrchestratorError, Exception))

        with self.assertRaises(Exception):
            raise EXCEPTIONS.OrchestratorError("Test")


if __name__ == "__main__":
    unittest.main()
