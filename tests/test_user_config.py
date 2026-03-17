"""
Tests for user_config.py module.
"""

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def load_script_module(name: str):
    """Dynamically load a script module."""
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


USER_CONFIG = load_script_module("user_config")
EXCEPTIONS = load_script_module("exceptions")


class UserConfigDirTest(unittest.TestCase):
    """Test user config directory functions."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.original_home = os.environ.get("HOME")

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        if self.original_home:
            os.environ["HOME"] = self.original_home

    def test_get_user_config_dir(self) -> None:
        """Test that user config directory is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir
            # Reload module to pick up new HOME
            config_dir = USER_CONFIG.get_user_config_dir()

            self.assertTrue(config_dir.exists())
            self.assertEqual(config_dir.name, ".autoresearch")
            self.assertEqual(config_dir.parent, Path(tmpdir))

    def test_get_user_config_path(self) -> None:
        """Test user config file path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir
            config_path = USER_CONFIG.get_user_config_path()

            self.assertEqual(config_path.name, "user-config.yaml")
            self.assertTrue(str(config_path).endswith(".autoresearch/user-config.yaml"))


class DefaultUserConfigTest(unittest.TestCase):
    """Test default user configuration."""

    def test_get_default_user_config(self) -> None:
        """Test that default config has all required fields."""
        defaults = USER_CONFIG.get_default_user_config()

        self.assertIn("version", defaults)
        self.assertIn("author", defaults)
        self.assertIn("preferences", defaults)
        self.assertIn("research_defaults", defaults)

    def test_default_author_fields(self) -> None:
        """Test default author fields."""
        defaults = USER_CONFIG.get_default_user_config()
        author = defaults["author"]

        self.assertIn("name", author)
        self.assertIn("email", author)
        self.assertIn("institution", author)
        self.assertIn("orcid", author)
        self.assertEqual(author["name"], "")

    def test_default_preferences_fields(self) -> None:
        """Test default preferences fields."""
        defaults = USER_CONFIG.get_default_user_config()
        prefs = defaults["preferences"]

        self.assertIn("default_venue", prefs)
        self.assertIn("default_language", prefs)
        self.assertEqual(prefs["default_venue"], "")

        lang = prefs["default_language"]
        self.assertIn("process_docs", lang)
        self.assertIn("paper_docs", lang)
        self.assertEqual(lang["process_docs"], "zh-CN")
        self.assertEqual(lang["paper_docs"], "en-US")

    def test_default_research_defaults(self) -> None:
        """Test default research defaults."""
        defaults = USER_CONFIG.get_default_user_config()
        research = defaults["research_defaults"]

        self.assertIn("research_type", research)
        self.assertIn("gpu_preference", research)
        self.assertEqual(research["research_type"], "ml_experiment")
        self.assertEqual(research["gpu_preference"], "auto")


class LoadSaveUserConfigTest(unittest.TestCase):
    """Test loading and saving user configuration."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.original_home = os.environ.get("HOME")

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        if self.original_home:
            os.environ["HOME"] = self.original_home

    def test_load_user_config_not_exists(self) -> None:
        """Test loading config when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir
            config = USER_CONFIG.load_user_config()

            # Should return defaults
            self.assertEqual(config["version"], USER_CONFIG.CONFIG_VERSION)
            self.assertEqual(config["author"]["name"], "")

    def test_save_and_load_user_config(self) -> None:
        """Test saving and loading user configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            # Save config
            config = {
                "version": "1.0.0",
                "author": {
                    "name": "Test User",
                    "email": "test@example.com",
                    "institution": "Test University",
                    "orcid": "0000-0000-0000-0000",
                },
                "preferences": {
                    "default_venue": "NeurIPS",
                    "default_language": {
                        "process_docs": "en-US",
                        "paper_docs": "en-US",
                    },
                },
                "research_defaults": {
                    "research_type": "theoretical",
                    "gpu_preference": "local",
                },
            }
            USER_CONFIG.save_user_config(config)

            # Load config
            loaded = USER_CONFIG.load_user_config()

            self.assertEqual(loaded["author"]["name"], "Test User")
            self.assertEqual(loaded["author"]["email"], "test@example.com")
            self.assertEqual(loaded["preferences"]["default_venue"], "NeurIPS")
            self.assertEqual(loaded["research_defaults"]["research_type"], "theoretical")

    def test_save_user_config_creates_directory(self) -> None:
        """Test that save creates the config directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            config = USER_CONFIG.get_default_user_config()
            USER_CONFIG.save_user_config(config)

            config_path = USER_CONFIG.get_user_config_path()
            self.assertTrue(config_path.exists())
            self.assertTrue(config_path.parent.exists())


class MergeConfigsTest(unittest.TestCase):
    """Test configuration merging."""

    def test_merge_configs_basic(self) -> None:
        """Test basic config merging."""
        user = {
            "author": {"name": "User Name", "email": "user@example.com"},
            "preferences": {"default_venue": "ICML"},
        }
        project = {
            "author": {"name": "Project Name"},
            "research_defaults": {"research_type": "experimental"},
        }

        merged = USER_CONFIG.merge_configs(project, user)

        # Project should override user
        self.assertEqual(merged["author"]["name"], "Project Name")
        # User value should be preserved when not in project
        self.assertEqual(merged["author"]["email"], "user@example.com")
        # Project-only values should be present
        self.assertEqual(merged["research_defaults"]["research_type"], "experimental")
        # User-only values should be present
        self.assertEqual(merged["preferences"]["default_venue"], "ICML")

    def test_merge_configs_deep_nested(self) -> None:
        """Test deep nested config merging."""
        user = {
            "preferences": {
                "default_venue": "NeurIPS",
                "default_language": {
                    "process_docs": "zh-CN",
                    "paper_docs": "en-US",
                },
            }
        }
        project = {
            "preferences": {
                "default_language": {
                    "paper_docs": "zh-CN",  # Override
                },
            }
        }

        merged = USER_CONFIG.merge_configs(project, user)

        # Nested merge should work correctly
        self.assertEqual(merged["preferences"]["default_venue"], "NeurIPS")
        self.assertEqual(merged["preferences"]["default_language"]["process_docs"], "zh-CN")
        self.assertEqual(merged["preferences"]["default_language"]["paper_docs"], "zh-CN")

    def test_merge_configs_empty_project(self) -> None:
        """Test merge with empty project config."""
        user = {"author": {"name": "User"}}
        project = {}

        merged = USER_CONFIG.merge_configs(project, user)

        self.assertEqual(merged["author"]["name"], "User")

    def test_merge_configs_empty_user(self) -> None:
        """Test merge with empty user config."""
        user = {}
        project = {"author": {"name": "Project"}}

        merged = USER_CONFIG.merge_configs(project, user)

        self.assertEqual(merged["author"]["name"], "Project")


class DataclassesTest(unittest.TestCase):
    """Test dataclass implementations."""

    def test_author_info(self) -> None:
        """Test AuthorInfo dataclass."""
        author = USER_CONFIG.AuthorInfo(
            name="Test User",
            email="test@example.com",
            institution="Test University",
            orcid="0000-0000-0000-0000",
        )

        d = author.to_dict()
        self.assertEqual(d["name"], "Test User")
        self.assertEqual(d["email"], "test@example.com")

        loaded = USER_CONFIG.AuthorInfo.from_dict(d)
        self.assertEqual(loaded.name, "Test User")
        self.assertEqual(loaded.email, "test@example.com")

    def test_language_preferences(self) -> None:
        """Test LanguagePreferences dataclass."""
        lang = USER_CONFIG.LanguagePreferences(
            process_docs="en-US",
            paper_docs="en-US",
        )

        d = lang.to_dict()
        self.assertEqual(d["process_docs"], "en-US")

        loaded = USER_CONFIG.LanguagePreferences.from_dict(d)
        self.assertEqual(loaded.process_docs, "en-US")

    def test_user_preferences(self) -> None:
        """Test UserPreferences dataclass."""
        prefs = USER_CONFIG.UserPreferences(
            default_venue="NeurIPS",
            default_language=USER_CONFIG.LanguagePreferences(),
        )

        d = prefs.to_dict()
        self.assertEqual(d["default_venue"], "NeurIPS")

        loaded = USER_CONFIG.UserPreferences.from_dict(d)
        self.assertEqual(loaded.default_venue, "NeurIPS")

    def test_research_defaults(self) -> None:
        """Test ResearchDefaults dataclass."""
        defaults = USER_CONFIG.ResearchDefaults(
            research_type="theoretical",
            gpu_preference="remote",
        )

        d = defaults.to_dict()
        self.assertEqual(d["research_type"], "theoretical")

        loaded = USER_CONFIG.ResearchDefaults.from_dict(d)
        self.assertEqual(loaded.research_type, "theoretical")

    def test_user_config(self) -> None:
        """Test UserConfig dataclass."""
        config = USER_CONFIG.UserConfig(
            author=USER_CONFIG.AuthorInfo(name="Test"),
            preferences=USER_CONFIG.UserPreferences(),
            research_defaults=USER_CONFIG.ResearchDefaults(),
        )

        d = config.to_dict()
        self.assertIn("version", d)
        self.assertIn("author", d)

        loaded = USER_CONFIG.UserConfig.from_dict(d)
        self.assertEqual(loaded.author.name, "Test")


class HelperFunctionsTest(unittest.TestCase):
    """Test helper functions."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.original_home = os.environ.get("HOME")

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        if self.original_home:
            os.environ["HOME"] = self.original_home

    def test_get_author_info(self) -> None:
        """Test get_author_info function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            # Save config with author info
            config = USER_CONFIG.get_default_user_config()
            config["author"]["name"] = "Test Author"
            config["author"]["email"] = "author@test.com"
            USER_CONFIG.save_user_config(config)

            author = USER_CONFIG.get_author_info()

            self.assertEqual(author.name, "Test Author")
            self.assertEqual(author.email, "author@test.com")

    def test_set_author_info(self) -> None:
        """Test set_author_info function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            author = USER_CONFIG.AuthorInfo(
                name="New Author",
                email="new@test.com",
                institution="New Institution",
            )
            USER_CONFIG.set_author_info(author)

            loaded = USER_CONFIG.get_author_info()
            self.assertEqual(loaded.name, "New Author")
            self.assertEqual(loaded.email, "new@test.com")
            self.assertEqual(loaded.institution, "New Institution")

    def test_get_research_defaults(self) -> None:
        """Test get_research_defaults function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            defaults = USER_CONFIG.get_research_defaults()

            self.assertEqual(defaults.research_type, "ml_experiment")
            self.assertEqual(defaults.gpu_preference, "auto")

    def test_set_research_defaults(self) -> None:
        """Test set_research_defaults function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            defaults = USER_CONFIG.ResearchDefaults(
                research_type="theoretical",
                gpu_preference="local",
            )
            USER_CONFIG.set_research_defaults(defaults)

            loaded = USER_CONFIG.get_research_defaults()
            self.assertEqual(loaded.research_type, "theoretical")
            self.assertEqual(loaded.gpu_preference, "local")

    def test_init_user_config(self) -> None:
        """Test init_user_config function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            config_path = USER_CONFIG.init_user_config(
                name="Init User",
                email="init@test.com",
                institution="Init Institution",
                default_venue="CVPR",
                research_type="empirical",
            )

            self.assertTrue(config_path.exists())

            loaded = USER_CONFIG.load_user_config()
            self.assertEqual(loaded["author"]["name"], "Init User")
            self.assertEqual(loaded["preferences"]["default_venue"], "CVPR")
            self.assertEqual(loaded["research_defaults"]["research_type"], "empirical")


class ConfigurationErrorTest(unittest.TestCase):
    """Test configuration error handling."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.original_home = os.environ.get("HOME")

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        if self.original_home:
            os.environ["HOME"] = self.original_home

    def test_load_invalid_yaml(self) -> None:
        """Test loading invalid YAML raises ConfigurationError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["HOME"] = tmpdir

            # Create invalid YAML file
            config_path = USER_CONFIG.get_user_config_path()
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text("invalid: yaml: content: [", encoding="utf-8")

            with self.assertRaises(USER_CONFIG.ConfigurationError):
                USER_CONFIG.load_user_config()


if __name__ == "__main__":
    unittest.main()
