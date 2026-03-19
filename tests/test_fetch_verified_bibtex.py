"""Tests for citation/fetch_verified_bibtex.py module."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Set up path for imports
SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "citation"))

# Import after path setup
from fetch_verified_bibtex import (  # noqa: E402
    EMPIRICAL_TERMS,
    STOPWORDS,
    FetchError,
    PersistentCache,
    codex_home_path,
    current_date_iso,
    truncate_box_text,
)


class TestFetchError(unittest.TestCase):
    """Tests for FetchError exception."""

    def test_fetch_error_basic(self) -> None:
        """Test basic FetchError creation."""
        error = FetchError("Test error")
        self.assertEqual(str(error), "Test error")
        self.assertIsNone(error.status_code)
        self.assertFalse(error.retryable)

    def test_fetch_error_with_status_code(self) -> None:
        """Test FetchError with status code."""
        error = FetchError("Rate limited", status_code=429, retryable=True)
        self.assertEqual(str(error), "Rate limited")
        self.assertEqual(error.status_code, 429)
        self.assertTrue(error.retryable)


class TestTruncateBoxText(unittest.TestCase):
    """Tests for truncate_box_text function."""

    def test_truncate_box_text_short(self) -> None:
        """Test that short text is not truncated."""
        result = truncate_box_text("short", 20)
        self.assertEqual(result, "short")

    def test_truncate_box_text_exact_length(self) -> None:
        """Test that exact length text is not truncated."""
        text = "exactly fifteen"
        result = truncate_box_text(text, 15)
        self.assertEqual(result, text)

    def test_truncate_box_text_long(self) -> None:
        """Test that long text is truncated with ellipsis."""
        text = "a" * 100
        result = truncate_box_text(text, 50)
        self.assertEqual(len(result), 50)
        self.assertTrue(result.endswith("…"))


class TestPersistentCache(unittest.TestCase):
    """Tests for PersistentCache class."""

    def test_cache_get_missing_key(self) -> None:
        """Test that missing key returns None."""
        with tempfile.TemporaryDirectory() as d:
            cache = PersistentCache(Path(d) / "cache.json")
            self.assertIsNone(cache.get("missing"))

    def test_cache_set_and_get(self) -> None:
        """Test that set and get work correctly."""
        with tempfile.TemporaryDirectory() as d:
            cache = PersistentCache(Path(d) / "cache.json")
            cache.set("key", {"data": "value"})
            self.assertEqual(cache.get("key"), {"data": "value"})

    def test_cache_set_overwrites(self) -> None:
        """Test that set overwrites existing value."""
        with tempfile.TemporaryDirectory() as d:
            cache = PersistentCache(Path(d) / "cache.json")
            cache.set("key", {"data": "old"})
            cache.set("key", {"data": "new"})
            self.assertEqual(cache.get("key"), {"data": "new"})

    def test_cache_persistence(self) -> None:
        """Test that cache persists to disk."""
        with tempfile.TemporaryDirectory() as d:
            cache_path = Path(d) / "cache.json"
            cache = PersistentCache(cache_path)
            cache.set("key", {"data": "persistent"})

            # Create new cache instance
            cache2 = PersistentCache(cache_path)
            self.assertEqual(cache2.get("key"), {"data": "persistent"})


class TestCurrentDateIso(unittest.TestCase):
    """Tests for current_date_iso function."""

    def test_current_date_iso_returns_string(self) -> None:
        """Test that current_date_iso returns a string."""
        result = current_date_iso()
        self.assertIsInstance(result, str)
        # Should be in YYYY-MM-DD format
        self.assertEqual(len(result), 10)
        self.assertEqual(result.count("-"), 2)


class TestConstants(unittest.TestCase):
    """Tests for module constants."""

    def test_stopwords_is_set(self) -> None:
        """Test that STOPWORDS is a set."""
        self.assertIsInstance(STOPWORDS, set)
        self.assertIn("the", STOPWORDS)
        self.assertIn("and", STOPWORDS)

    def test_empirical_terms_is_set(self) -> None:
        """Test that EMPIRICAL_TERMS is a set."""
        self.assertIsInstance(EMPIRICAL_TERMS, set)
        self.assertIn("experiment", EMPIRICAL_TERMS)
        self.assertIn("results", EMPIRICAL_TERMS)


class TestCodexHomePath(unittest.TestCase):
    """Tests for codex_home_path function."""

    def test_codex_home_path_returns_path(self) -> None:
        """Test that codex_home_path returns a Path."""
        result = codex_home_path()
        self.assertIsInstance(result, Path)

    @patch.dict("os.environ", {"CODEX_HOME": "/tmp/test_codex"})
    def test_codex_home_path_respects_env(self) -> None:
        """Test that CODEX_HOME environment variable is respected."""
        result = codex_home_path()
        self.assertEqual(str(result), "/tmp/test_codex")


if __name__ == "__main__":
    unittest.main()
