import importlib.util
import sys
import tempfile
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


INIT = load_script_module("init_research_project")
VERIFY = load_script_module("verify_system")


class VerifySystemTest(unittest.TestCase):
    def test_verify_passes_for_initialized_project(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "verify-demo"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Verify system test",
            )

            report = VERIFY.run_all_checks(project_root)

            # Directory structure should pass
            self.assertTrue(report["directory_structure"]["passed"])

            # Required files should pass
            self.assertTrue(report["required_files"]["passed"])

            # State integrity should pass
            self.assertTrue(report["state_integrity"]["passed"])

    def test_verify_fails_for_missing_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "verify-missing"
            # Don't initialize, so directories will be missing

            report = VERIFY.run_all_checks(project_root)

            # Directory structure should fail
            self.assertFalse(report["directory_structure"]["passed"])

    def test_check_directory_structure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "verify-dirs"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Directory test",
            )

            result = VERIFY.check_directory_structure(project_root)

            self.assertTrue(result["passed"])
            # Check that we have the expected number of required directories
            # Main: paper, code, docs (3)
            # Agents: 8 directories
            # System: 7 directories
            # Total: 18 required directories
            self.assertGreaterEqual(len(result["checks"]), 18)

    def test_check_required_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "verify-files"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Files test",
            )

            result = VERIFY.check_required_files(project_root)

            self.assertTrue(result["passed"])

    def test_check_state_integrity(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "verify-state"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="State test",
            )

            result = VERIFY.check_state_integrity(project_root)

            self.assertTrue(result["passed"])
            # Check for required fields
            field_names = [c["name"] for c in result["checks"]]
            self.assertIn("project_id", field_names)
            self.assertIn("current_phase", field_names)

    def test_format_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "verify-report"
            INIT.initialize_research_project(
                project_root=project_root,
                topic="Report test",
            )

            report = VERIFY.run_all_checks(project_root)
            formatted = VERIFY.format_report(report)

            self.assertIn("System Integrity Report", formatted)
            self.assertIn("Directory Structure", formatted)
            self.assertIn("Required Files", formatted)
            self.assertIn("State Integrity", formatted)


if __name__ == "__main__":
    unittest.main()
