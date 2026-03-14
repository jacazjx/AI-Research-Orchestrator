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

            recovered = RECOVER.recover_stage(project_root, mode="retry-job", job_id=scheduled["job_id"])
            self.assertEqual("completed", recovered["status"])
            registry = COMMON.read_yaml(registry_path)
            self.assertEqual("scheduled", registry["jobs"][scheduled["job_id"]]["status"])


if __name__ == "__main__":
    unittest.main()
