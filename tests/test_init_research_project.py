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


class InitializeResearchProjectTest(unittest.TestCase):
    def test_bootstrap_without_client_init_creates_new_structure(self) -> None:
        """Test that initialization creates the new folder structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "moe-routing"
            result = INIT.initialize_research_project(
                project_root=project_root,
                topic="Sparse mixture-of-experts routing for recommendation",
            )

            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")

            self.assertEqual("moe-routing", result["project_id"])
            self.assertEqual("skill-bootstrap", state["init_artifacts"]["source"])
            self.assertEqual("codex", state["client_profile"])
            self.assertEqual("zh-CN", state["language_policy"]["process_docs"])
            self.assertEqual("en-US", state["language_policy"]["paper_docs"])
            # New semantic phase name
            self.assertEqual("survey", state["current_phase"])

            # Check new directory structure
            for directory in COMMON.MAIN_DIRECTORIES:
                self.assertTrue((project_root / directory).is_dir(), directory)
            for directory in COMMON.AGENT_DIRECTORIES:
                self.assertTrue((project_root / directory).is_dir(), directory)
            for directory in COMMON.SYSTEM_DIRECTORIES:
                self.assertTrue((project_root / directory).is_dir(), directory)

            # Check main work subdirectories
            self.assertTrue((project_root / "paper/sections").is_dir())
            self.assertTrue((project_root / "paper/figures").is_dir())
            self.assertTrue((project_root / "code/src").is_dir())
            self.assertTrue((project_root / "code/experiments").is_dir())
            self.assertTrue((project_root / "code/configs").is_dir())
            self.assertTrue((project_root / "code/checkpoints").is_dir())
            self.assertTrue((project_root / "docs/reports/survey").is_dir())
            self.assertTrue((project_root / "docs/reports/pilot").is_dir())
            self.assertTrue((project_root / "docs/reports/experiments").is_dir())
            self.assertTrue((project_root / "docs/reports/paper").is_dir())
            self.assertTrue((project_root / "docs/reports/reflection").is_dir())

            self.assertTrue((project_root / "AGENTS.md").exists())
            # Note: workspace-manifest is in .autoresearch/ per template location
            self.assertTrue((project_root / ".autoresearch/workspace-manifest.md").exists())
            self.assertTrue(
                (project_root / ".autoresearch/config/orchestrator-config.yaml").exists()
            )
            self.assertTrue((project_root / ".autoresearch/idea-brief.md").exists())
            self.assertTrue((project_root / ".autoresearch/reference-papers/README.md").exists())
            self.assertTrue((project_root / ".autoresearch/dashboard/progress.md").exists())
            self.assertTrue(
                (project_root / "docs/reports/pilot/pilot-validation-report.md").exists()
            )
            self.assertTrue(
                (project_root / "docs/reports/experiments/evidence-package-index.md").exists()
            )
            # runtime-improvement-report is now in docs/reports/reflection/
            self.assertTrue(
                (project_root / "docs/reports/reflection/runtime-improvement-report.md").exists()
            )
            self.assertTrue((project_root / ".autoresearch/archive/archive-index.md").exists())

    def test_existing_client_init_artifact_is_recorded(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "graph-agent"
            project_root.mkdir(parents=True, exist_ok=True)
            (project_root / "client-bootstrap.md").write_text(
                "# Existing init artifact\n", encoding="utf-8"
            )

            INIT.initialize_research_project(
                project_root=project_root,
                topic="Graph reasoning agents",
            )

            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")
            # Note: workspace-manifest is in .autoresearch/ per template location
            manifest_text = (project_root / ".autoresearch/workspace-manifest.md").read_text(
                encoding="utf-8"
            )

            self.assertEqual("client-init", state["init_artifacts"]["source"])
            self.assertEqual(["client-bootstrap.md"], state["init_artifacts"]["detected_paths"])
            self.assertIn("client-bootstrap.md", manifest_text)

    def test_can_generate_claude_instruction_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "claude-client"

            INIT.initialize_research_project(
                project_root=project_root,
                topic="Claude workspace",
                client_type="claude",
            )

            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")

            self.assertEqual("claude", state["client_profile"])
            self.assertEqual("CLAUDE.md", state["client_instruction_file"])
            self.assertTrue((project_root / "CLAUDE.md").exists())

    def test_starting_phase_sets_correct_state(self) -> None:
        """Test that starting_phase parameter sets the correct phase and gate."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "mid-project"

            result = INIT.initialize_research_project(
                project_root=project_root,
                topic="Mid-project research",
                starting_phase="experiments",
            )

            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")

            # Result should show normalized phase name
            self.assertEqual("experiments", result["starting_phase"])
            self.assertEqual("gate_3", result["starting_gate"])
            self.assertEqual("experiments", state["current_phase"])
            self.assertEqual("gate_3", state["current_gate"])

    def test_starting_phase_paper_sets_gate_4(self) -> None:
        """Test that starting at paper phase sets gate_4."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "paper-phase-project"

            result = INIT.initialize_research_project(
                project_root=project_root,
                topic="Paper phase research",
                starting_phase="paper",
            )

            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")

            self.assertEqual("paper", result["starting_phase"])
            self.assertEqual("gate_4", result["starting_gate"])
            self.assertEqual("paper", state["current_phase"])
            self.assertEqual("gate_4", state["current_gate"])

    def test_starting_phase_legacy_format_normalized(self) -> None:
        """Test that legacy phase names are normalized to new format."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "legacy-phase-project"

            result = INIT.initialize_research_project(
                project_root=project_root,
                topic="Legacy phase test",
                starting_phase="03-full-experiments",  # Legacy format
            )

            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")

            # Should be normalized to new semantic name
            self.assertEqual("experiments", result["starting_phase"])
            self.assertEqual("experiments", state["current_phase"])
            self.assertEqual("gate_3", state["current_gate"])

    def test_starting_phase_affects_completion_percent(self) -> None:
        """Test that starting phase affects completion percentage."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "progress-project"

            # Test with survey phase (0%)
            _ = INIT.initialize_research_project(
                project_root=project_root / "project1",
                topic="Test project 1",
                starting_phase="survey",
            )

            # Test with paper phase (60%)
            _ = INIT.initialize_research_project(
                project_root=project_root / "project2",
                topic="Test project 2",
                starting_phase="paper",
            )

            state1 = COMMON.read_yaml(
                project_root / "project1" / ".autoresearch/state/research-state.yaml"
            )
            state2 = COMMON.read_yaml(
                project_root / "project2" / ".autoresearch/state/research-state.yaml"
            )

            # Later phases should have higher completion percent
            self.assertLess(
                state1["progress"]["completion_percent"], state2["progress"]["completion_percent"]
            )

    def test_normalize_phase_name_helper(self) -> None:
        """Test the normalize_phase_name helper function."""
        # Legacy to new
        self.assertEqual("survey", INIT.normalize_phase_name("01-survey"))
        self.assertEqual("pilot", INIT.normalize_phase_name("02-pilot-analysis"))
        self.assertEqual("experiments", INIT.normalize_phase_name("03-full-experiments"))
        self.assertEqual("paper", INIT.normalize_phase_name("04-paper"))
        self.assertEqual("reflection", INIT.normalize_phase_name("05-reflection-evolution"))

        # New stays the same
        self.assertEqual("survey", INIT.normalize_phase_name("survey"))
        self.assertEqual("pilot", INIT.normalize_phase_name("pilot"))
        self.assertEqual("experiments", INIT.normalize_phase_name("experiments"))
        self.assertEqual("paper", INIT.normalize_phase_name("paper"))
        self.assertEqual("reflection", INIT.normalize_phase_name("reflection"))

    def test_detect_codex_mcp_returns_true_when_configured(self) -> None:
        """Test that Codex MCP is detected when configured."""
        with patch.object(Path, "home", return_value=Path("/fake/home")):
            with patch.object(Path, "exists", return_value=True):
                with patch.object(
                    Path, "read_text", return_value=json.dumps({"mcpServers": {"codex": {}}})
                ):
                    result = INIT.detect_codex_mcp()
                    self.assertTrue(result)

    def test_detect_codex_mcp_returns_false_when_not_configured(self) -> None:
        """Test that Codex MCP returns False when not configured."""
        with patch.object(Path, "home", return_value=Path("/fake/home")):
            with patch.object(Path, "exists", return_value=False):
                result = INIT.detect_codex_mcp()
                self.assertFalse(result)

    def test_detect_codex_mcp_handles_malformed_config(self) -> None:
        """Test that malformed config doesn't crash detection."""
        with patch.object(Path, "home", return_value=Path("/fake/home")):
            with patch.object(Path, "exists", return_value=True):
                with patch.object(Path, "read_text", return_value="not valid json"):
                    result = INIT.detect_codex_mcp()
                    self.assertFalse(result)

    def test_explicit_init_paths_are_normalized(self) -> None:
        """Test that explicit init paths are normalized."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "explicit-init"
            project_root.mkdir(parents=True, exist_ok=True)

            result = INIT.initialize_research_project(
                project_root=project_root,
                topic="Explicit init paths",
                explicit_init_paths=["./docs/notes.md", "./README.md"],
            )

            # Paths should be normalized (without leading ./)
            self.assertIn("docs/notes.md", result["init_paths"])
            self.assertIn("README.md", result["init_paths"])

    def test_main_outputs_json_when_requested(self) -> None:
        """Test that main outputs JSON when --json flag is used."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "json-output"
            args = [
                "--project-root",
                str(project_root),
                "--topic",
                "JSON output test",
                "--json",
            ]
            with patch("sys.argv", ["init_research_project.py"] + args):
                with patch("builtins.print") as mock_print:
                    INIT.main()
                    # Check that JSON was printed
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    # Verify JSON contains expected project_root
                    self.assertIn("project_root", parsed)
                    self.assertIn("project_id", parsed)

    def test_main_outputs_human_readable_by_default(self) -> None:
        """Test that main outputs human-readable text by default."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "human-output"
            args = [
                "--project-root",
                str(project_root),
                "--topic",
                "Human readable test",
            ]
            with patch("sys.argv", ["init_research_project.py"] + args):
                with patch("builtins.print") as mock_print:
                    INIT.main()
                    calls = [str(call) for call in mock_print.call_args_list]
                    combined = " ".join(calls)
                    self.assertIn("Project root", combined)

    def test_main_with_overwrite_templates(self) -> None:
        """Test that --overwrite-templates flag works."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "overwrite-test"
            args = [
                "--project-root",
                str(project_root),
                "--topic",
                "Overwrite test",
                "--overwrite-templates",
            ]
            with patch("sys.argv", ["init_research_project.py"] + args):
                result = INIT.main()
                self.assertEqual(0, result)

    def test_main_with_custom_project_id(self) -> None:
        """Test that custom project ID is used."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "custom-id"
            args = [
                "--project-root",
                str(project_root),
                "--topic",
                "Custom ID test",
                "--project-id",
                "my-custom-project",
            ]
            with patch("sys.argv", ["init_research_project.py"] + args):
                with patch("builtins.print"):
                    result = INIT.main()
                    self.assertEqual(0, result)

            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")
            self.assertEqual("my-custom-project", state["project_id"])

    def test_main_with_custom_languages(self) -> None:
        """Test that custom process and paper languages work."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "custom-lang"
            args = [
                "--project-root",
                str(project_root),
                "--topic",
                "Custom language test",
                "--process-language",
                "en-US",
                "--paper-language",
                "zh-CN",
            ]
            with patch("sys.argv", ["init_research_project.py"] + args):
                result = INIT.main()
                self.assertEqual(0, result)

            state = COMMON.read_yaml(project_root / ".autoresearch/state/research-state.yaml")
            self.assertEqual("en-US", state["language_policy"]["process_docs"])
            self.assertEqual("zh-CN", state["language_policy"]["paper_docs"])

    def test_build_parser_accepts_all_valid_phases(self) -> None:
        """Test that parser accepts both new and legacy phase names."""
        parser = INIT.build_parser()
        # Test new semantic names
        for phase in INIT.VALID_PHASES:
            args = parser.parse_args(["--project-root", "/tmp", "--starting-phase", phase])
            self.assertEqual(phase, args.starting_phase)
        # Test legacy names
        for phase in INIT.VALID_PHASES_LEGACY:
            args = parser.parse_args(["--project-root", "/tmp", "--starting-phase", phase])
            self.assertEqual(phase, args.starting_phase)


if __name__ == "__main__":
    unittest.main()
