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
    spec.loader.exec_module(module)
    return module


INIT = load_script_module("init_research_project")


class TestSystemEvalRegistry(unittest.TestCase):
    def _load_registry(self):
        return load_script_module("system_eval_registry")

    def _sample_scores(self):
        return {
            "workflow_effectiveness": 4.0,
            "agent_collaboration": 3.5,
            "gate_accuracy": 4.5,
            "template_effectiveness": 3.0,
            "resource_efficiency": 4.0,
            "user_experience": 3.5,
        }

    def test_record_creates_registry_file(self):
        registry = self._load_registry()
        with tempfile.TemporaryDirectory() as tmp:
            registry_path = Path(tmp) / "system-eval-history.yaml"
            project_root = Path(tmp) / "project"
            INIT.initialize_research_project(project_root=project_root, topic="Test project")
            registry.record_evaluation(
                project_root=project_root,
                scores=self._sample_scores(),
                weighted_total=3.82,
                recommendation="System performed well",
                top_issues=["issue1"],
                registry_path=registry_path,
            )
            self.assertTrue(registry_path.exists())

    def test_record_appends_to_existing_registry(self):
        registry = self._load_registry()
        with tempfile.TemporaryDirectory() as tmp:
            registry_path = Path(tmp) / "system-eval-history.yaml"
            project_root = Path(tmp) / "project"
            INIT.initialize_research_project(project_root=project_root, topic="Test project")
            registry.record_evaluation(
                project_root=project_root,
                scores=self._sample_scores(),
                weighted_total=3.82,
                recommendation="First eval",
                top_issues=[],
                registry_path=registry_path,
            )
            registry.record_evaluation(
                project_root=project_root,
                scores=self._sample_scores(),
                weighted_total=4.0,
                recommendation="Second eval",
                top_issues=[],
                registry_path=registry_path,
            )
            history = registry.query_history(registry_path=registry_path)
            self.assertEqual(2, len(history))

    def test_record_stores_correct_fields(self):
        registry = self._load_registry()
        with tempfile.TemporaryDirectory() as tmp:
            registry_path = Path(tmp) / "system-eval-history.yaml"
            project_root = Path(tmp) / "project"
            INIT.initialize_research_project(project_root=project_root, topic="Field test")
            scores = self._sample_scores()
            registry.record_evaluation(
                project_root=project_root,
                scores=scores,
                weighted_total=3.82,
                recommendation="Good",
                top_issues=["issue1", "issue2"],
                registry_path=registry_path,
            )
            history = registry.query_history(registry_path=registry_path)
            entry = history[0]
            self.assertEqual("Field test", entry["topic"])
            self.assertIn("project_id", entry)
            self.assertIn("evaluated_at", entry)
            self.assertEqual(scores, entry["scores"])
            self.assertAlmostEqual(3.82, entry["weighted_total"])
            self.assertEqual("Good", entry["recommendation"])
            self.assertEqual(["issue1", "issue2"], entry["top_issues"])
            self.assertIn("report_path", entry)

    def test_query_history_with_last_filter(self):
        registry = self._load_registry()
        with tempfile.TemporaryDirectory() as tmp:
            registry_path = Path(tmp) / "system-eval-history.yaml"
            project_root = Path(tmp) / "project"
            INIT.initialize_research_project(project_root=project_root, topic="History test")
            for i in range(5):
                registry.record_evaluation(
                    project_root=project_root,
                    scores=self._sample_scores(),
                    weighted_total=float(i),
                    recommendation=f"Eval {i}",
                    top_issues=[],
                    registry_path=registry_path,
                )
            history = registry.query_history(registry_path=registry_path, last=3)
            self.assertEqual(3, len(history))
            self.assertEqual("Eval 4", history[0]["recommendation"])

    def test_query_history_with_project_id_filter(self):
        registry = self._load_registry()
        with tempfile.TemporaryDirectory() as tmp:
            registry_path = Path(tmp) / "system-eval-history.yaml"
            project_root = Path(tmp) / "project"
            INIT.initialize_research_project(project_root=project_root, topic="Filter test")
            state = load_script_module("orchestrator_common").load_state(project_root)
            project_id = state["project_id"]
            registry.record_evaluation(
                project_root=project_root,
                scores=self._sample_scores(),
                weighted_total=3.0,
                recommendation="Match",
                top_issues=[],
                registry_path=registry_path,
            )
            history = registry.query_history(registry_path=registry_path, project_id=project_id)
            self.assertEqual(1, len(history))
            self.assertEqual(project_id, history[0]["project_id"])

    def test_query_empty_registry(self):
        registry = self._load_registry()
        with tempfile.TemporaryDirectory() as tmp:
            registry_path = Path(tmp) / "nonexistent.yaml"
            history = registry.query_history(registry_path=registry_path)
            self.assertEqual([], history)

    def test_compute_trend(self):
        registry = self._load_registry()
        with tempfile.TemporaryDirectory() as tmp:
            registry_path = Path(tmp) / "system-eval-history.yaml"
            project_root = Path(tmp) / "project"
            INIT.initialize_research_project(project_root=project_root, topic="Trend test")
            for i in range(3):
                scores = self._sample_scores()
                scores["workflow_effectiveness"] = 3.0 + i * 0.5
                registry.record_evaluation(
                    project_root=project_root,
                    scores=scores,
                    weighted_total=3.0 + i * 0.5,
                    recommendation=f"Eval {i}",
                    top_issues=[],
                    registry_path=registry_path,
                )
            trend = registry.compute_trend(
                registry_path=registry_path, dimension="workflow_effectiveness"
            )
            self.assertEqual(3, len(trend))
            self.assertAlmostEqual(3.0, trend[0]["value"])
            self.assertAlmostEqual(4.0, trend[2]["value"])

    def test_compute_trend_all_dimensions(self):
        registry = self._load_registry()
        with tempfile.TemporaryDirectory() as tmp:
            registry_path = Path(tmp) / "system-eval-history.yaml"
            project_root = Path(tmp) / "project"
            INIT.initialize_research_project(project_root=project_root, topic="Trend all")
            registry.record_evaluation(
                project_root=project_root,
                scores=self._sample_scores(),
                weighted_total=3.82,
                recommendation="Eval",
                top_issues=[],
                registry_path=registry_path,
            )
            trend = registry.compute_trend(registry_path=registry_path)
            self.assertEqual(1, len(trend))
            self.assertIn("scores", trend[0])

    def test_corrupt_registry_backup(self):
        registry = self._load_registry()
        with tempfile.TemporaryDirectory() as tmp:
            registry_path = Path(tmp) / "system-eval-history.yaml"
            registry_path.write_text("{{invalid yaml::", encoding="utf-8")
            project_root = Path(tmp) / "project"
            INIT.initialize_research_project(project_root=project_root, topic="Corrupt test")
            registry.record_evaluation(
                project_root=project_root,
                scores=self._sample_scores(),
                weighted_total=3.0,
                recommendation="After corrupt",
                top_issues=[],
                registry_path=registry_path,
            )
            backup_path = registry_path.with_suffix(".yaml.bak")
            self.assertTrue(backup_path.exists())
            history = registry.query_history(registry_path=registry_path)
            self.assertEqual(1, len(history))

    def test_validate_scores_rejects_missing_dimension(self):
        registry = self._load_registry()
        incomplete_scores = {"workflow_effectiveness": 4.0}
        with self.assertRaises(ValueError):
            registry.validate_scores(incomplete_scores)

    def test_validate_scores_rejects_out_of_range(self):
        registry = self._load_registry()
        scores = self._sample_scores()
        scores["gate_accuracy"] = 6.0
        with self.assertRaises(ValueError):
            registry.validate_scores(scores)

    def test_main_record_action(self):
        registry = self._load_registry()
        with tempfile.TemporaryDirectory() as tmp:
            registry_path = Path(tmp) / "system-eval-history.yaml"
            project_root = Path(tmp) / "project"
            INIT.initialize_research_project(project_root=project_root, topic="CLI test")
            args = [
                "--action",
                "record",
                "--project-root",
                str(project_root),
                "--scores",
                json.dumps(self._sample_scores()),
                "--weighted-total",
                "3.82",
                "--recommendation",
                "Good",
                "--top-issues",
                json.dumps(["issue1"]),
                "--registry-path",
                str(registry_path),
            ]
            with patch("sys.argv", ["system_eval_registry.py"] + args):
                result = registry.main()
                self.assertEqual(0, result)
            history = registry.query_history(registry_path=registry_path)
            self.assertEqual(1, len(history))

    def test_main_history_action(self):
        registry = self._load_registry()
        with tempfile.TemporaryDirectory() as tmp:
            registry_path = Path(tmp) / "system-eval-history.yaml"
            project_root = Path(tmp) / "project"
            INIT.initialize_research_project(project_root=project_root, topic="CLI history")
            registry.record_evaluation(
                project_root=project_root,
                scores=self._sample_scores(),
                weighted_total=3.82,
                recommendation="Eval",
                top_issues=[],
                registry_path=registry_path,
            )
            args = ["--action", "history", "--registry-path", str(registry_path)]
            with patch("sys.argv", ["system_eval_registry.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = registry.main()
                    self.assertEqual(0, result)
                    output = mock_print.call_args[0][0]
                    parsed = json.loads(output)
                    self.assertEqual(1, len(parsed))

    def test_main_trend_action(self):
        registry = self._load_registry()
        with tempfile.TemporaryDirectory() as tmp:
            registry_path = Path(tmp) / "system-eval-history.yaml"
            project_root = Path(tmp) / "project"
            INIT.initialize_research_project(project_root=project_root, topic="CLI trend")
            registry.record_evaluation(
                project_root=project_root,
                scores=self._sample_scores(),
                weighted_total=3.82,
                recommendation="Eval",
                top_issues=[],
                registry_path=registry_path,
            )
            args = [
                "--action",
                "trend",
                "--dimension",
                "gate_accuracy",
                "--registry-path",
                str(registry_path),
            ]
            with patch("sys.argv", ["system_eval_registry.py"] + args):
                with patch("builtins.print") as mock_print:
                    result = registry.main()
                    self.assertEqual(0, result)
                    output = mock_print.call_args[0][0]
                    parsed = json.loads(output)
                    self.assertEqual(1, len(parsed))


if __name__ == "__main__":
    unittest.main()
