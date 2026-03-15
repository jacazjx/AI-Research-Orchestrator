"""Tests for latex-citation-curator integration."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts" / "citation"


class ExtractCitationNeedsTest(unittest.TestCase):
    """Tests for extract_citation_needs.py script."""

    def test_extracts_literal_cite_marker(self) -> None:
        """Test extraction of [cite] marker."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as f:
            f.write("This claim needs support [cite].\n")
            f.flush()
            result = subprocess.run(
                ["python3", str(SCRIPTS_DIR / "extract_citation_needs.py"), f.name, "--json"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode)
            import json

            data = json.loads(result.stdout)
            self.assertEqual(1, len(data))
            self.assertIn("literal-cite-marker", data[0]["triggers"])

    def test_extracts_todo_cite_command(self) -> None:
        """Test extraction of \\todo{cite} command."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as f:
            f.write(r"\todo{cite: add reference here}" + "\n")
            f.flush()
            result = subprocess.run(
                ["python3", str(SCRIPTS_DIR / "extract_citation_needs.py"), f.name, "--json"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode)
            import json

            data = json.loads(result.stdout)
            self.assertEqual(1, len(data))
            self.assertIn("todo-cite-command", data[0]["triggers"])

    def test_extracts_zh_support_paper(self) -> None:
        """Test extraction of Chinese citation request."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as f:
            f.write("我想找一篇论文来支撑论点。\n")
            f.flush()
            result = subprocess.run(
                ["python3", str(SCRIPTS_DIR / "extract_citation_needs.py"), f.name, "--json"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode)
            import json

            data = json.loads(result.stdout)
            self.assertEqual(1, len(data))
            self.assertIn("zh-support-paper", data[0]["triggers"])

    def test_no_gaps_returns_empty(self) -> None:
        """Test that no citation gaps returns empty list."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as f:
            f.write("This is a normal paragraph with no citation gaps.\n")
            f.flush()
            result = subprocess.run(
                ["python3", str(SCRIPTS_DIR / "extract_citation_needs.py"), f.name, "--json"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode)
            import json

            data = json.loads(result.stdout)
            self.assertEqual(0, len(data))

    def test_text_output_format(self) -> None:
        """Test plain text output format."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as f:
            f.write("This claim needs support [cite].\n")
            f.flush()
            result = subprocess.run(
                ["python3", str(SCRIPTS_DIR / "extract_citation_needs.py"), f.name],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode)
            self.assertIn("[1]", result.stdout)
            self.assertIn("claim:", result.stdout)

    def test_stdin_input(self) -> None:
        """Test reading from stdin."""
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "extract_citation_needs.py"), "-", "--json"],
            input="This claim needs support [cite].\n",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode)
        import json

        data = json.loads(result.stdout)
        self.assertEqual(1, len(data))

    def test_clean_claim_removes_marker(self) -> None:
        """Test that clean_claim removes citation marker."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as f:
            f.write("Deep learning improves performance [cite].\n")
            f.flush()
            result = subprocess.run(
                ["python3", str(SCRIPTS_DIR / "extract_citation_needs.py"), f.name, "--json"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode)
            import json

            data = json.loads(result.stdout)
            self.assertEqual(1, len(data))
            # clean_claim should not contain [cite]
            self.assertNotIn("[cite]", data[0]["clean_claim"])
            self.assertIn("Deep learning", data[0]["clean_claim"])


class ScorePapersTest(unittest.TestCase):
    """Tests for score_papers.py script."""

    def test_scores_single_record(self) -> None:
        """Test scoring a single record."""
        import json

        record = {
            "title": "Test Paper",
            "year": 2023,
            "venue": "Test Conference",
            "doi": "10.1234/test",
            "citationCount": 100,
            "ccfTier": "A",
            "source": "semantic-scholar",
            "sourceUrl": "https://semanticscholar.org/paper/123",
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump([record], f)
            f.flush()
            result = subprocess.run(
                ["python3", str(SCRIPTS_DIR / "score_papers.py"), f.name, "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode)
            data = json.loads(result.stdout)
            self.assertEqual(1, len(data))
            self.assertIn("qualityScore", data[0])
            self.assertGreater(data[0]["qualityScore"], 0)
            self.assertTrue(data[0]["eligible"])

    def test_rejects_missing_doi_without_trusted_source(self) -> None:
        """Test rejection when DOI missing and no trusted source."""
        import json

        record = {
            "title": "Test Paper",
            "year": 2023,
            "venue": "Test Conference",
            "doi": "",
            "source": "",
            "sourceUrl": "",
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump([record], f)
            f.flush()
            result = subprocess.run(
                ["python3", str(SCRIPTS_DIR / "score_papers.py"), f.name, "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode)
            data = json.loads(result.stdout)
            self.assertEqual(1, len(data))
            self.assertFalse(data[0]["eligible"])
            self.assertIn("missing-doi-and-no-trusted-bibtex-source", data[0]["rejectionReasons"])

    def test_rejects_preprint_with_formal_version(self) -> None:
        """Test rejection of preprint that has formal version."""
        import json

        record = {
            "title": "Test Paper",
            "year": 2023,
            "doi": "10.1234/test",
            "source": "arxiv",
            "sourceUrl": "https://arxiv.org/abs/1234",
            "preprint": True,
            "hasFormalVersion": True,
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump([record], f)
            f.flush()
            result = subprocess.run(
                ["python3", str(SCRIPTS_DIR / "score_papers.py"), f.name, "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode)
            data = json.loads(result.stdout)
            self.assertEqual(1, len(data))
            self.assertFalse(data[0]["eligible"])
            self.assertIn("replace-with-formal-version", data[0]["rejectionReasons"])

    def test_ccf_tier_scoring(self) -> None:
        """Test CCF tier scoring."""
        import json

        records = [
            {
                "title": "CCF A",
                "year": 2023,
                "doi": "10.1/a",
                "source": "test",
                "sourceUrl": "url",
                "ccfTier": "A",
            },
            {
                "title": "CCF B",
                "year": 2023,
                "doi": "10.1/b",
                "source": "test",
                "sourceUrl": "url",
                "ccfTier": "B",
            },
            {
                "title": "CCF C",
                "year": 2023,
                "doi": "10.1/c",
                "source": "test",
                "sourceUrl": "url",
                "ccfTier": "C",
            },
        ]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(records, f)
            f.flush()
            result = subprocess.run(
                ["python3", str(SCRIPTS_DIR / "score_papers.py"), f.name, "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode)
            data = json.loads(result.stdout)
            # CCF A should have highest venue score
            scores = {r["title"]: r["venueScore"] for r in data}
            self.assertGreater(scores["CCF A"], scores["CCF B"])
            self.assertGreater(scores["CCF B"], scores["CCF C"])

    def test_freshness_scoring(self) -> None:
        """Test freshness scoring prefers recent papers."""
        import json

        records = [
            {"title": "New", "year": 2024, "doi": "10.1/new", "source": "test", "sourceUrl": "url"},
            {"title": "Old", "year": 2018, "doi": "10.1/old", "source": "test", "sourceUrl": "url"},
        ]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(records, f)
            f.flush()
            result = subprocess.run(
                [
                    "python3",
                    str(SCRIPTS_DIR / "score_papers.py"),
                    f.name,
                    "--format",
                    "json",
                    "--current-year",
                    "2024",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode)
            data = json.loads(result.stdout)
            scores = {r["title"]: r["freshnessScore"] for r in data}
            self.assertGreater(scores["New"], scores["Old"])

    def test_tsv_output_format(self) -> None:
        """Test TSV output format."""
        import json

        record = {
            "title": "Test",
            "year": 2023,
            "doi": "10.1/t",
            "source": "test",
            "sourceUrl": "url",
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump([record], f)
            f.flush()
            result = subprocess.run(
                ["python3", str(SCRIPTS_DIR / "score_papers.py"), f.name, "--format", "tsv"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode)
            lines = result.stdout.strip().split("\n")
            self.assertEqual(2, len(lines))  # header + 1 data row
            self.assertIn("\t", lines[0])

    def test_top_n_filter(self) -> None:
        """Test --top N filter."""
        import json

        records = [
            {
                "title": "A",
                "year": 2023,
                "doi": "10.1/a",
                "source": "test",
                "sourceUrl": "url",
                "citationCount": 100,
            },
            {
                "title": "B",
                "year": 2023,
                "doi": "10.1/b",
                "source": "test",
                "sourceUrl": "url",
                "citationCount": 50,
            },
            {
                "title": "C",
                "year": 2023,
                "doi": "10.1/c",
                "source": "test",
                "sourceUrl": "url",
                "citationCount": 10,
            },
        ]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(records, f)
            f.flush()
            result = subprocess.run(
                [
                    "python3",
                    str(SCRIPTS_DIR / "score_papers.py"),
                    f.name,
                    "--format",
                    "json",
                    "--top",
                    "2",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode)
            data = json.loads(result.stdout)
            self.assertEqual(2, len(data))

    def test_jsonl_input(self) -> None:
        """Test JSONL input format."""
        import json

        lines = [
            json.dumps(
                {"title": "A", "year": 2023, "doi": "10.1/a", "source": "test", "sourceUrl": "url"}
            ),
            json.dumps(
                {"title": "B", "year": 2023, "doi": "10.1/b", "source": "test", "sourceUrl": "url"}
            ),
        ]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            f.write("\n".join(lines))
            f.flush()
            result = subprocess.run(
                ["python3", str(SCRIPTS_DIR / "score_papers.py"), f.name, "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode)
            data = json.loads(result.stdout)
            self.assertEqual(2, len(data))


class FetchVerifiedBibtexTest(unittest.TestCase):
    """Tests for fetch_verified_bibtex.py script."""

    def test_help_runs_successfully(self) -> None:
        """Test --help runs without error."""
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "fetch_verified_bibtex.py"), "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode)
        self.assertIn("Search, verify, score", result.stdout)

    def test_missing_query_returns_error(self) -> None:
        """Test missing query returns error."""
        result = subprocess.run(
            ["python3", str(SCRIPTS_DIR / "fetch_verified_bibtex.py"), "--no-key-prompt"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(0, result.returncode)

    def test_split_bibtex_entries(self) -> None:
        """Test BibTeX entry splitting."""
        # Import the module directly
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            import importlib.util

            spec = importlib.util.spec_from_file_location(
                "fetch_verified_bibtex", SCRIPTS_DIR / "fetch_verified_bibtex.py"
            )
            assert spec is not None and spec.loader is not None
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            text = r"""@article{test1,
  title = {Test Paper 1}
}

@article{test2,
  title = {Test Paper 2}
}
"""
            entries = module.split_bibtex_entries(text)
            self.assertEqual(2, len(entries))
            self.assertIn("@article{test1", entries[0])
            self.assertIn("@article{test2", entries[1])
        finally:
            sys.path.remove(str(SCRIPTS_DIR))

    def test_bibtex_entry_key(self) -> None:
        """Test BibTeX entry key extraction."""
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            import importlib.util

            spec = importlib.util.spec_from_file_location(
                "fetch_verified_bibtex", SCRIPTS_DIR / "fetch_verified_bibtex.py"
            )
            assert spec is not None and spec.loader is not None
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            entry = "@article{smith2023deep,\n  title = {Deep Learning}\n}"
            key = module.bibtex_entry_key(entry)
            self.assertEqual("smith2023deep", key)
        finally:
            sys.path.remove(str(SCRIPTS_DIR))

    def test_bibtex_field_value(self) -> None:
        """Test BibTeX field value extraction."""
        sys.path.insert(0, str(SCRIPTS_DIR))
        try:
            import importlib.util

            spec = importlib.util.spec_from_file_location(
                "fetch_verified_bibtex", SCRIPTS_DIR / "fetch_verified_bibtex.py"
            )
            assert spec is not None and spec.loader is not None
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            entry = '@article{test,\n  title = {Test Title},\n  year = "2023"\n}'
            title = module.bibtex_field_value(entry, "title")
            year = module.bibtex_field_value(entry, "year")
            self.assertEqual("Test Title", title)
            self.assertEqual("2023", year)
        finally:
            sys.path.remove(str(SCRIPTS_DIR))


if __name__ == "__main__":
    unittest.main()
