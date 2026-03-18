import importlib.util
import json
import sys
import tempfile
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

    def test_schedule_with_gpu_assignment(self) -> None:
        """Test scheduling with GPU assignment."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "gpu-assign"
            INIT.initialize_research_project(project_root=project_root, topic="GPU assign")

            # Add GPU to registry
            gpu_path = project_root / ".autoresearch/runtime/gpu-registry.yaml"
            gpu_data = COMMON.read_yaml(gpu_path)
            gpu_data["devices"] = {"0": {"status": "idle", "name": "GPU-0"}}
            COMMON.write_yaml(gpu_path, gpu_data)

            result = SCHEDULE.schedule_job(project_root, command="echo test", backend="local")
            self.assertEqual("0", result["gpu"])

    def test_schedule_with_explicit_gpu(self) -> None:
        """Test scheduling with explicit GPU ID."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "explicit-gpu"
            INIT.initialize_research_project(project_root=project_root, topic="Explicit GPU")

            result = SCHEDULE.schedule_job(
                project_root, command="echo test", backend="local", gpu_id="1"
            )
            self.assertEqual("1", result["gpu"])

    def test_assign_gpu_auto_mode(self) -> None:
        """Test GPU assignment in auto mode."""
        devices = {
            "devices": {
                "0": {"status": "idle", "name": "GPU-0"},
                "1": {"status": "allocated", "allocated_to": "job-1"},
            }
        }
        result = SCHEDULE._assign_gpu(devices, "auto", "job-2")
        self.assertEqual("0", result)

    def test_assign_gpu_no_devices_available(self) -> None:
        """Test GPU assignment when no devices available."""
        devices = {"devices": {"0": {"status": "allocated", "allocated_to": "job-1"}}}
        result = SCHEDULE._assign_gpu(devices, "unassigned", "job-2")
        self.assertEqual("unassigned", result)

    def test_assign_gpu_empty_devices(self) -> None:
        """Test GPU assignment with empty devices."""
        devices = {"devices": {}}
        result = SCHEDULE._assign_gpu(devices, "unassigned", "job-1")
        self.assertEqual("unassigned", result)

    def test_assign_gpu_new_device(self) -> None:
        """Test GPU assignment with new GPU ID."""
        devices = {"devices": {}}
        result = SCHEDULE._assign_gpu(devices, "2", "job-1")
        self.assertEqual("2", result)
        self.assertEqual("allocated", devices["devices"]["2"]["status"])

    def test_assign_gpu_already_allocated(self) -> None:
        """Test GPU assignment to already allocated GPU."""
        devices = {"devices": {"0": {"status": "idle"}}}
        result = SCHEDULE._assign_gpu(devices, "0", "job-1")
        self.assertEqual("0", result)
        self.assertEqual("allocated", devices["devices"]["0"]["status"])

    def test_discover_gpus_success(self) -> None:
        """Test GPU discovery with nvidia-smi."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="0, NVIDIA RTX 3090\n1, NVIDIA RTX 3080\n", returncode=0
            )
            result = SCHEDULE._discover_gpus()
            self.assertIn("0", result)
            self.assertIn("1", result)
            self.assertEqual("idle", result["0"]["status"])

    def test_discover_gpus_failure(self) -> None:
        """Test GPU discovery when nvidia-smi fails."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="", returncode=1)
            result = SCHEDULE._discover_gpus()
            self.assertEqual({}, result)

    def test_discover_gpus_not_found(self) -> None:
        """Test GPU discovery when nvidia-smi not found."""
        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = SCHEDULE._discover_gpus()
            self.assertEqual({}, result)

    def test_load_job_registry_missing(self) -> None:
        """Test loading job registry when file missing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = SCHEDULE._load_job_registry(Path(temp_dir))
            self.assertEqual({}, result["jobs"])

    def test_load_gpu_registry_missing(self) -> None:
        """Test loading GPU registry when file missing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = SCHEDULE._load_gpu_registry(Path(temp_dir))
            self.assertEqual({}, result["devices"])

    def test_load_backend_registry_missing(self) -> None:
        """Test loading backend registry when file missing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = SCHEDULE._load_backend_registry(Path(temp_dir))
            self.assertIn("local", result["backends"])

    def test_main_with_json_output(self) -> None:
        """Test main with --json flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-json"
            INIT.initialize_research_project(project_root=project_root, topic="Main JSON")

            args = [
                "--project-root",
                str(project_root),
                "--command",
                "echo test",
                "--backend",
                "local",
                "--json",
            ]
            with patch("sys.argv", ["schedule_jobs.py"] + args):
                with patch("builtins.print") as mock_print:
                    SCHEDULE.main()
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertEqual("scheduled", parsed["status"])

    def test_build_parser_accepts_all_options(self) -> None:
        """Test that parser accepts all options."""
        parser = SCHEDULE.build_parser()
        args = parser.parse_args(
            [
                "--project-root",
                "/tmp",
                "--command",
                "echo test",
                "--backend",
                "local",
                "--phase",
                "experiments",
                "--gpu-id",
                "0",
                "--cwd",
                "/work",
                "--remote-host",
                "server.com",
                "--json",
            ]
        )
        self.assertEqual("local", args.backend)
        self.assertEqual("experiments", args.phase)
        self.assertEqual("0", args.gpu_id)

    def test_schedule_with_ssh_backend(self) -> None:
        """Test scheduling with SSH backend."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "ssh-backend"
            INIT.initialize_research_project(project_root=project_root, topic="SSH backend")

            result = SCHEDULE.schedule_job(
                project_root,
                command="python train.py",
                backend="ssh",
                cwd="/remote/path",
                remote_host="gpu-server",
            )
            self.assertEqual("ssh", result["backend"])

    def test_schedule_updates_state(self) -> None:
        """Test that scheduling updates state correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "state-update"
            INIT.initialize_research_project(project_root=project_root, topic="State update")

            SCHEDULE.schedule_job(project_root, command="echo test", backend="local")

            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")
            self.assertIn("job-1", state["active_jobs"])
            self.assertEqual("local", state["progress"]["active_backend"])


class RunRemoteJobTest(unittest.TestCase):
    def test_run_job_prepare_mode(self) -> None:
        """Test run_job in prepare mode (no execute)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "prepare-mode"
            INIT.initialize_research_project(project_root=project_root, topic="Prepare mode")

            scheduled = SCHEDULE.schedule_job(
                project_root,
                command="echo test",
                backend="local",
            )

            result = RUNNER.run_job(project_root, scheduled["job_id"], execute=False)
            self.assertEqual("prepared", result["status"])

    def test_run_job_unknown_job_id(self) -> None:
        """Test run_job with unknown job ID."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "unknown-job"
            INIT.initialize_research_project(project_root=project_root, topic="Unknown job")

            with self.assertRaises(Exception) as context:
                RUNNER.run_job(project_root, "nonexistent-job", execute=False)
            self.assertIn("StateError", type(context.exception).__name__)

    def test_validate_cwd_path_traversal(self) -> None:
        """Test that path traversal in cwd is rejected."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "path-traversal"
            project_root.mkdir()

            with self.assertRaises(Exception) as context:
                RUNNER._validate_cwd(Path("/etc/passwd"), project_root)
            self.assertIn("PathSecurityError", type(context.exception).__name__)

    def test_parse_command_safely(self) -> None:
        """Test safe command parsing."""
        result = RUNNER._parse_command_safely("echo 'hello world'")
        self.assertEqual(["echo", "hello world"], result)

    def test_parse_command_safely_invalid(self) -> None:
        """Test that invalid command raises error."""
        with self.assertRaises(Exception) as context:
            RUNNER._parse_command_safely("echo 'unclosed quote")
        self.assertIn("CommandExecutionError", type(context.exception).__name__)

    def test_build_ssh_command(self) -> None:
        """Test SSH command building."""
        result = RUNNER._build_ssh_command("server.com", "/remote/path", ["python", "train.py"])
        self.assertEqual(["ssh", "server.com"], result[:2])
        self.assertIn("cd /remote/path", result[2])
        self.assertIn("python train.py", result[2])

    def test_run_job_with_failed_execution(self) -> None:
        """Test run_job when command fails."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "failed-job"
            INIT.initialize_research_project(project_root=project_root, topic="Failed job")

            scheduled = SCHEDULE.schedule_job(
                project_root,
                command="bash -c 'exit 1'",
                backend="local",
            )

            result = RUNNER.run_job(project_root, scheduled["job_id"], execute=True)
            self.assertEqual("failed", result["status"])
            self.assertNotEqual(0, result["exit_code"])

            # Check state reflects failure
            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")
            self.assertEqual("needs-attention", state["recovery_status"])

    def test_run_job_ssh_missing_remote_host(self) -> None:
        """Test SSH job without remote host results in failure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "ssh-no-host"
            INIT.initialize_research_project(project_root=project_root, topic="SSH no host")

            # Schedule a job first to get proper structure
            scheduled = SCHEDULE.schedule_job(project_root, command="echo test", backend="local")

            # Modify job to use SSH backend without remote host
            registry_path = project_root / ".autoresearch/runtime/job-registry.yaml"
            registry = COMMON.read_yaml(registry_path)
            # Jobs is a dict with job IDs as keys
            if scheduled["job_id"] in registry.get("jobs", {}):
                registry["jobs"][scheduled["job_id"]]["backend"] = "ssh"
                registry["jobs"][scheduled["job_id"]]["remote_host"] = ""
            COMMON.write_yaml(registry_path, registry)

            # The job should fail gracefully
            result = RUNNER.run_job(project_root, scheduled["job_id"], execute=True)
            self.assertEqual("failed", result["status"])

    def test_run_job_ssh_invalid_remote_host(self) -> None:
        """Test SSH job with invalid remote host format results in failure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "ssh-invalid-host"
            INIT.initialize_research_project(project_root=project_root, topic="SSH invalid host")

            # Schedule a job first
            scheduled = SCHEDULE.schedule_job(project_root, command="echo test", backend="local")

            # Modify job to use invalid SSH host
            registry_path = project_root / ".autoresearch/runtime/job-registry.yaml"
            registry = COMMON.read_yaml(registry_path)
            if scheduled["job_id"] in registry.get("jobs", {}):
                registry["jobs"][scheduled["job_id"]]["backend"] = "ssh"
                registry["jobs"][scheduled["job_id"]]["remote_host"] = "invalid;host"
            COMMON.write_yaml(registry_path, registry)

            # The job should fail gracefully
            result = RUNNER.run_job(project_root, scheduled["job_id"], execute=True)
            self.assertEqual("failed", result["status"])

    def test_run_remote_job_main_with_json(self) -> None:
        """Test main function with --json flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-json"
            INIT.initialize_research_project(project_root=project_root, topic="Main JSON")

            scheduled = SCHEDULE.schedule_job(project_root, command="echo test", backend="local")

            args = [
                "--project-root",
                str(project_root),
                "--job-id",
                scheduled["job_id"],
                "--execute",
                "--json",
            ]
            with patch("sys.argv", ["run_remote_job.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = RUNNER.main()
                    self.assertEqual(0, result)
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertIn("status", parsed)

    def test_run_remote_job_main_prepare_mode(self) -> None:
        """Test main function in prepare mode."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "main-prepare"
            INIT.initialize_research_project(project_root=project_root, topic="Main prepare")

            scheduled = SCHEDULE.schedule_job(project_root, command="echo test", backend="local")

            args = [
                "--project-root",
                str(project_root),
                "--job-id",
                scheduled["job_id"],
            ]
            with patch("sys.argv", ["run_remote_job.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = RUNNER.main()
                    self.assertEqual(0, result)
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertEqual("prepared", parsed["status"])

    def test_run_remote_job_build_parser(self) -> None:
        """Test build_parser for run_remote_job."""
        parser = RUNNER.build_parser()
        args = parser.parse_args(
            [
                "--project-root",
                "/tmp",
                "--job-id",
                "job-1",
                "--execute",
                "--json",
            ]
        )
        self.assertEqual("/tmp", args.project_root)
        self.assertEqual("job-1", args.job_id)
        self.assertTrue(args.execute)
        self.assertTrue(args.json)


if __name__ == "__main__":
    unittest.main()
