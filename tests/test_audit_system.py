import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def load_script_module(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load_script_module("audit_system")


class AuditSystemTest(unittest.TestCase):
    def test_check_scripts_exist_all_present(self) -> None:
        result = AUDIT.check_scripts_exist()
        self.assertEqual("scripts", result["category"])
        self.assertTrue(result["passed"])
        self.assertTrue(len(result["checks"]) > 0)
        for check in result["checks"]:
            self.assertIn("name", check)
            self.assertIn("exists", check)
            self.assertIn("status", check)

    def test_check_templates_exist(self) -> None:
        result = AUDIT.check_templates_exist()
        self.assertEqual("templates", result["category"])
        self.assertIn("passed", result)
        self.assertIn("checks", result)

    def test_check_prompts_exist(self) -> None:
        result = AUDIT.check_prompts_exist()
        self.assertEqual("prompts", result["category"])
        self.assertIn("passed", result)
        self.assertIn("checks", result)

    def test_check_references_exist(self) -> None:
        result = AUDIT.check_references_exist()
        self.assertEqual("references", result["category"])
        self.assertIn("passed", result)
        self.assertIn("checks", result)

    def test_check_quality_enforcement(self) -> None:
        result = AUDIT.check_quality_enforcement()
        self.assertEqual("quality_enforcement", result["category"])
        self.assertIn("passed", result)
        self.assertTrue(len(result["checks"]) >= 5)

    def test_check_human_gate_enforcement(self) -> None:
        result = AUDIT.check_human_gate_enforcement()
        self.assertEqual("human_gates", result["category"])
        self.assertIn("passed", result)

    def test_check_test_coverage_runs_tests(self) -> None:
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="Ran 42 tests\nOK",
                stderr="",
                returncode=0,
            )
            result = AUDIT.check_test_coverage()
            self.assertEqual("tests", result["category"])
            self.assertTrue(result["passed"])

    def test_check_test_coverage_handles_failure(self) -> None:
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="FAILED (errors=3)",
                stderr="",
                returncode=1,
            )
            result = AUDIT.check_test_coverage()
            self.assertFalse(result["passed"])

    def test_check_test_coverage_handles_timeout(self) -> None:
        import subprocess

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="test", timeout=120)
            result = AUDIT.check_test_coverage()
            self.assertFalse(result["passed"])
            self.assertTrue(any("timed out" in str(c).lower() for c in result["checks"]))

    def test_run_audit_returns_complete_structure(self) -> None:
        with patch.object(
            AUDIT,
            "check_test_coverage",
            return_value={"category": "tests", "passed": True, "checks": []},
        ):
            result = AUDIT.run_audit()
            self.assertIn("audit_time", result)
            self.assertIn("skill_dir", result)
            self.assertIn("categories", result)
            self.assertIn("overall_passed", result)
            self.assertIn("delivery_readiness", result)

    def test_run_audit_delivery_readiness_ready(self) -> None:
        with patch.object(
            AUDIT,
            "check_test_coverage",
            return_value={"category": "tests", "passed": True, "checks": []},
        ):
            result = AUDIT.run_audit()
            self.assertIn(
                result["delivery_readiness"], ["READY", "CONDITIONALLY_READY", "NOT_READY"]
            )

    def test_format_report_outputs_markdown(self) -> None:
        report = {
            "audit_time": "2024-01-01T00:00:00+00:00",
            "skill_dir": "/test/skill",
            "delivery_readiness": "READY",
            "overall_passed": True,
            "categories": [
                {
                    "category": "scripts",
                    "passed": True,
                    "checks": [{"name": "test.py", "status": "pass"}],
                },
            ],
        }
        output = AUDIT.format_report(report)
        self.assertIn("# System Audit Report", output)
        self.assertIn("READY", output)
        self.assertIn("Scripts", output)

    def test_format_report_handles_failures(self) -> None:
        report = {
            "audit_time": "2024-01-01T00:00:00+00:00",
            "skill_dir": "/test/skill",
            "delivery_readiness": "NOT_READY",
            "overall_passed": False,
            "categories": [
                {
                    "category": "scripts",
                    "passed": False,
                    "checks": [{"name": "missing.py", "status": "fail", "error": "File not found"}],
                },
            ],
        }
        output = AUDIT.format_report(report)
        self.assertIn("FAIL", output)
        self.assertIn("missing.py", output)
        self.assertIn("File not found", output)


if __name__ == "__main__":
    unittest.main()
