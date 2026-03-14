import importlib.util
import sys
import tempfile
import unittest
from unittest.mock import patch
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


COMMON = load_script_module("orchestrator_common")
INIT = load_script_module("init_research_project")
SCHEDULE = load_script_module("schedule_jobs")
RUNNER = load_script_module("run_remote_job")
EXCEPTIONS = load_script_module("exceptions")


class RuntimeJobsTest(unittest.TestCase):
    def test_schedule_and_run_local_job(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "runtime-jobs"
            INIT.initialize_research_project(project_root=project_root, topic="Runtime jobs")

            scheduled = SCHEDULE.schedule_job(
                project_root,
                command="printf 'job-ok'",
                backend="local",
                phase="experiments",  # Use new semantic name
            )
            self.assertEqual("scheduled", scheduled["status"])

            executed = RUNNER.run_job(project_root, scheduled["job_id"], execute=True)
            self.assertEqual("completed", executed["status"])
            stdout_text = (project_root / executed["stdout_log"]).read_text(encoding="utf-8")
            self.assertEqual("job-ok", stdout_text)

            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")
            self.assertEqual([], state["active_jobs"])

    def test_ssh_job_wraps_remote_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "runtime-ssh"
            INIT.initialize_research_project(project_root=project_root, topic="Runtime ssh")

            scheduled = SCHEDULE.schedule_job(
                project_root,
                command="python train.py",
                backend="ssh",
                cwd="/remote/workdir",
                remote_host="example.com",
            )

            with patch("subprocess.run") as mocked_run:
                mocked_run.return_value.stdout = ""
                mocked_run.return_value.stderr = ""
                mocked_run.return_value.returncode = 0
                RUNNER.run_job(project_root, scheduled["job_id"], execute=True)

            args = mocked_run.call_args[0][0]
            self.assertEqual(["ssh", "example.com"], args[:2])
            self.assertIn("cd /remote/workdir && python train.py", args[2])

    def test_rejects_unimplemented_backend(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "runtime-invalid-backend"
            INIT.initialize_research_project(project_root=project_root, topic="Invalid backend")

            with self.assertRaises(Exception) as context:
                SCHEDULE.schedule_job(project_root, command="echo hi", backend="slurm")
            self.assertIn("ConfigurationError", type(context.exception).__name__)


if __name__ == "__main__":
    unittest.main()
