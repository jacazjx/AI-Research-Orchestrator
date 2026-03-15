import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def load_script_module(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


COMMON = load_script_module("orchestrator_common")
INIT = load_script_module("init_research_project")
SCHEDULE = load_script_module("schedule_jobs")
SENTINEL = load_script_module("sentinel")
RECOVER = load_script_module("recover_stage")


class SentinelRecoverTest(unittest.TestCase):
    def test_detects_stale_job_and_retries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "sentinel-demo"
            INIT.initialize_research_project(project_root=project_root, topic="Sentinel demo")

            scheduled = SCHEDULE.schedule_job(project_root, command="printf 'x'", backend="local")
            # Use new path
            registry_path = project_root / ".autoresearch/runtime/job-registry.yaml"
            registry = COMMON.read_yaml(registry_path)
            registry["jobs"][scheduled["job_id"]]["status"] = "running"
            registry["jobs"][scheduled["job_id"]]["heartbeat_at"] = "2000-01-01T00:00:00+00:00"
            COMMON.write_yaml(registry_path, registry)

            health = SENTINEL.inspect_runtime(project_root, stale_after_minutes=1)
            self.assertEqual("attention", health["status"])
            self.assertTrue(any(issue["type"] == "stale_job" for issue in health["issues"]))

            recovered = RECOVER.recover_stage(
                project_root, mode="retry-job", job_id=scheduled["job_id"]
            )
            self.assertEqual("completed", recovered["status"])
            registry = COMMON.read_yaml(registry_path)
            self.assertEqual("scheduled", registry["jobs"][scheduled["job_id"]]["status"])

    def test_regen_dashboard_mode(self) -> None:
        """Test regen-dashboard recovery mode."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "regen-dashboard"
            INIT.initialize_research_project(project_root=project_root, topic="Regen dashboard")

            result = RECOVER.recover_stage(project_root, mode="regen-dashboard")
            self.assertEqual("completed", result["status"])
            self.assertEqual("regen-dashboard", result["mode"])

    def test_resume_job_mode(self) -> None:
        """Test resume-job recovery mode."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "resume-job"
            INIT.initialize_research_project(project_root=project_root, topic="Resume job")

            scheduled = SCHEDULE.schedule_job(project_root, command="echo test", backend="local")
            registry_path = project_root / ".autoresearch/runtime/job-registry.yaml"
            registry = COMMON.read_yaml(registry_path)
            registry["jobs"][scheduled["job_id"]]["status"] = "running"
            COMMON.write_yaml(registry_path, registry)

            result = RECOVER.recover_stage(
                project_root, mode="resume-job", job_id=scheduled["job_id"]
            )
            self.assertEqual("completed", result["status"])
            self.assertEqual("resume-job", result["mode"])

            registry = COMMON.read_yaml(registry_path)
            self.assertEqual("running", registry["jobs"][scheduled["job_id"]]["status"])
            self.assertIn("heartbeat_at", registry["jobs"][scheduled["job_id"]])

    def test_retry_job_increments_retry_count(self) -> None:
        """Test that retry-job increments retry count."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "retry-count"
            INIT.initialize_research_project(project_root=project_root, topic="Retry count")

            scheduled = SCHEDULE.schedule_job(project_root, command="echo test", backend="local")
            registry_path = project_root / ".autoresearch/runtime/job-registry.yaml"
            registry = COMMON.read_yaml(registry_path)

            result = RECOVER.recover_stage(
                project_root, mode="retry-job", job_id=scheduled["job_id"]
            )
            registry = COMMON.read_yaml(registry_path)
            self.assertEqual(1, registry["jobs"][scheduled["job_id"]]["retry_count"])

    def test_main_regen_dashboard(self) -> None:
        """Test main with regen-dashboard mode."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-regen"
            INIT.initialize_research_project(project_root=project_root, topic="Main regen")

            args = [
                "--project-root",
                str(project_root),
                "--mode",
                "regen-dashboard",
            ]
            with patch("sys.argv", ["recover_stage.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = RECOVER.main()
                    self.assertEqual(0, result)

    def test_main_retry_job(self) -> None:
        """Test main with retry-job mode."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-retry"
            INIT.initialize_research_project(project_root=project_root, topic="Main retry")

            scheduled = SCHEDULE.schedule_job(project_root, command="echo test", backend="local")

            args = [
                "--project-root",
                str(project_root),
                "--mode",
                "retry-job",
                "--job-id",
                scheduled["job_id"],
            ]
            with patch("sys.argv", ["recover_stage.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = RECOVER.main()
                    self.assertEqual(0, result)

    def test_main_with_json_output(self) -> None:
        """Test main with --json flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "json-output"
            INIT.initialize_research_project(project_root=project_root, topic="JSON output")

            args = [
                "--project-root",
                str(project_root),
                "--mode",
                "regen-dashboard",
                "--json",
            ]
            with patch("sys.argv", ["recover_stage.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = RECOVER.main()
                    self.assertEqual(0, result)
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertIn("status", parsed)

    def test_build_parser_accepts_all_modes(self) -> None:
        """Test that parser accepts all valid modes."""
        parser = RECOVER.build_parser()
        for mode in ["retry-job", "resume-job", "regen-dashboard"]:
            args = parser.parse_args(["--project-root", "/tmp", "--mode", mode])
            self.assertEqual(mode, args.mode)


class SentinelTest(unittest.TestCase):
    def test_sentinel_healthy_when_no_issues(self) -> None:
        """Test sentinel returns healthy when no issues."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "sentinel-healthy"
            INIT.initialize_research_project(project_root=project_root, topic="Sentinel healthy")

            # Create required deliverables to avoid missing_deliverable issue
            for relative_path in (
                "docs/reports/survey/survey-round-summary.md",
                "docs/reports/survey/critic-round-review.md",
                "docs/reports/survey/research-readiness-report.md",
                "docs/reports/survey/phase-scorecard.md",
            ):
                file_path = project_root / relative_path
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text("content\n", encoding="utf-8")

            result = SENTINEL.inspect_runtime(project_root)

            self.assertEqual("healthy", result["status"])
            self.assertEqual([], result["issues"])

    def test_sentinel_detects_missing_deliverable(self) -> None:
        """Test sentinel detects missing deliverable."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "sentinel-missing"
            INIT.initialize_research_project(project_root=project_root, topic="Sentinel missing")

            # Set current phase to survey and remove a required deliverable
            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["current_phase"] = "survey"
            COMMON.write_yaml(state_path, state)

            # Delete the actual required files for survey phase
            # PHASE_REQUIRED_DELIVERABLES['survey'] = ('readiness_report', 'survey_scorecard')
            readiness_path = project_root / "docs/reports/survey/research-readiness-report.md"
            if readiness_path.exists():
                readiness_path.unlink()

            result = SENTINEL.inspect_runtime(project_root)

            # Should detect missing deliverables
            self.assertEqual("attention", result["status"])
            self.assertTrue(
                any(issue["type"] == "missing_deliverable" for issue in result["issues"])
            )

    def test_sentinel_detects_missing_job_registry_entry(self) -> None:
        """Test sentinel detects missing job registry entry."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "sentinel-registry"
            INIT.initialize_research_project(project_root=project_root, topic="Sentinel registry")

            # Create required deliverables
            for relative_path in (
                "docs/reports/survey/survey-round-summary.md",
                "docs/reports/survey/critic-round-review.md",
                "docs/reports/survey/research-readiness-report.md",
                "docs/reports/survey/phase-scorecard.md",
            ):
                file_path = project_root / relative_path
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text("content\n", encoding="utf-8")

            # Schedule a job first to have proper registry structure
            scheduled = SCHEDULE.schedule_job(project_root, command="echo test", backend="local")

            # Add active job that doesn't exist in registry
            state_path = project_root / ".autoresearch/state/research-state.yaml"
            state = COMMON.read_yaml(state_path)
            state["active_jobs"] = ["nonexistent-job"]
            COMMON.write_yaml(state_path, state)

            result = SENTINEL.inspect_runtime(project_root)

            self.assertEqual("attention", result["status"])
            self.assertTrue(
                any(issue["type"] == "missing_job_registry_entry" for issue in result["issues"])
            )

    def test_sentinel_build_parser(self) -> None:
        """Test sentinel build_parser."""
        parser = SENTINEL.build_parser()

        args = parser.parse_args(["--project-root", "/tmp"])
        self.assertEqual("/tmp", args.project_root)
        self.assertIsNone(args.stale_after_minutes)
        self.assertFalse(args.json)

    def test_sentinel_main_with_json(self) -> None:
        """Test sentinel main with --json flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "sentinel-main"
            INIT.initialize_research_project(project_root=project_root, topic="Sentinel main")

            args = [
                "--project-root",
                str(project_root),
                "--json",
            ]
            with patch("sys.argv", ["sentinel.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = SENTINEL.main()
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertIn("status", parsed)

    def test_sentinel_main_with_stale_after_minutes(self) -> None:
        """Test sentinel main with --stale-after-minutes flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "sentinel-stale"
            INIT.initialize_research_project(project_root=project_root, topic="Sentinel stale")

            args = [
                "--project-root",
                str(project_root),
                "--stale-after-minutes",
                "60",
            ]
            with patch("sys.argv", ["sentinel.py"] + args):
                with patch("builtins.print"):
                    result = SENTINEL.main()
                    # Should return 0 if healthy
                    self.assertIn(result, [0, 1])

    def test_sentinel_main_human_readable(self) -> None:
        """Test sentinel main with human readable output."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "sentinel-human"
            INIT.initialize_research_project(project_root=project_root, topic="Sentinel human")

            args = [
                "--project-root",
                str(project_root),
            ]
            with patch("sys.argv", ["sentinel.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = SENTINEL.main()
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertIn("status", parsed)


if __name__ == "__main__":
    unittest.main()
