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

    def test_exception_inheritance(self) -> None:
        """Test that all exceptions inherit from OrchestratorError."""
        self.assertTrue(issubclass(EXCEPTIONS.StateError, EXCEPTIONS.OrchestratorError))
        self.assertTrue(issubclass(EXCEPTIONS.PathSecurityError, EXCEPTIONS.OrchestratorError))
        self.assertTrue(issubclass(EXCEPTIONS.ConfigurationError, EXCEPTIONS.OrchestratorError))
        self.assertTrue(issubclass(EXCEPTIONS.PhaseTransitionError, EXCEPTIONS.OrchestratorError))

    def test_exception_catch_as_base(self) -> None:
        """Test that exceptions can be caught as OrchestratorError."""
        with self.assertRaises(EXCEPTIONS.OrchestratorError):
            raise EXCEPTIONS.StateError("Test")

        with self.assertRaises(EXCEPTIONS.OrchestratorError):
            raise EXCEPTIONS.ConfigurationError("Test")

    def test_exception_is_exception(self) -> None:
        """Test that OrchestratorError is an Exception."""
        self.assertTrue(issubclass(EXCEPTIONS.OrchestratorError, Exception))

        with self.assertRaises(Exception):
            raise EXCEPTIONS.OrchestratorError("Test")


if __name__ == "__main__":
    unittest.main()
