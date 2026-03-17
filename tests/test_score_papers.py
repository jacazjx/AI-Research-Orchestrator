"""Tests for citation/score_papers.py parsing and scoring functions."""

import importlib.util
import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def load_script_module(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / "citation" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SCORE_PAPERS = load_script_module("score_papers")


class TestParseFloat(unittest.TestCase):
    """Tests for parse_float function."""

    def test_parse_float_returns_float_value(self) -> None:
        record = {"impactFactor": 3.5}
        result = SCORE_PAPERS.parse_float(record, "impactFactor")
        self.assertEqual(3.5, result)

    def test_parse_float_returns_default_for_missing_key(self) -> None:
        record = {}
        result = SCORE_PAPERS.parse_float(record, "impactFactor")
        self.assertEqual(0.0, result)

    def test_parse_float_returns_custom_default(self) -> None:
        record = {}
        result = SCORE_PAPERS.parse_float(record, "impactFactor", default=5.0)
        self.assertEqual(5.0, result)

    def test_parse_float_handles_string_number(self) -> None:
        record = {"impactFactor": "4.2"}
        result = SCORE_PAPERS.parse_float(record, "impactFactor")
        self.assertEqual(4.2, result)

    def test_parse_float_handles_none(self) -> None:
        record = {"impactFactor": None}
        result = SCORE_PAPERS.parse_float(record, "impactFactor")
        self.assertEqual(0.0, result)

    def test_parse_float_handles_empty_string(self) -> None:
        record = {"impactFactor": ""}
        result = SCORE_PAPERS.parse_float(record, "impactFactor")
        self.assertEqual(0.0, result)

    def test_parse_float_handles_unknown_string(self) -> None:
        record = {"impactFactor": "unknown"}
        result = SCORE_PAPERS.parse_float(record, "impactFactor")
        self.assertEqual(0.0, result)

    def test_parse_float_returns_default_for_invalid_string(self) -> None:
        record = {"impactFactor": "not-a-number"}
        result = SCORE_PAPERS.parse_float(record, "impactFactor")
        self.assertEqual(0.0, result)

    def test_parse_float_handles_int(self) -> None:
        record = {"impactFactor": 5}
        result = SCORE_PAPERS.parse_float(record, "impactFactor")
        self.assertEqual(5.0, result)


class TestParseInt(unittest.TestCase):
    """Tests for parse_int function."""

    def test_parse_int_returns_int_value(self) -> None:
        record = {"citationCount": 150}
        result = SCORE_PAPERS.parse_int(record, "citationCount")
        self.assertEqual(150, result)

    def test_parse_int_returns_default_for_missing_key(self) -> None:
        record = {}
        result = SCORE_PAPERS.parse_int(record, "citationCount")
        self.assertEqual(0, result)

    def test_parse_int_returns_custom_default(self) -> None:
        record = {}
        result = SCORE_PAPERS.parse_int(record, "citationCount", default=100)
        self.assertEqual(100, result)

    def test_parse_int_handles_string_number(self) -> None:
        record = {"citationCount": "200"}
        result = SCORE_PAPERS.parse_int(record, "citationCount")
        self.assertEqual(200, result)

    def test_parse_int_handles_none(self) -> None:
        record = {"citationCount": None}
        result = SCORE_PAPERS.parse_int(record, "citationCount")
        self.assertEqual(0, result)

    def test_parse_int_handles_empty_string(self) -> None:
        record = {"citationCount": ""}
        result = SCORE_PAPERS.parse_int(record, "citationCount")
        self.assertEqual(0, result)

    def test_parse_int_handles_unknown_string(self) -> None:
        record = {"citationCount": "unknown"}
        result = SCORE_PAPERS.parse_int(record, "citationCount")
        self.assertEqual(0, result)

    def test_parse_int_returns_default_for_invalid_string(self) -> None:
        record = {"citationCount": "not-a-number"}
        result = SCORE_PAPERS.parse_int(record, "citationCount")
        self.assertEqual(0, result)

    def test_parse_int_returns_default_for_float_string(self) -> None:
        """Float strings like '150.7' raise ValueError in int()."""
        record = {"citationCount": "150.7"}
        result = SCORE_PAPERS.parse_int(record, "citationCount")
        self.assertEqual(0, result)


class TestParseBool(unittest.TestCase):
    """Tests for parse_bool function."""

    def test_parse_bool_returns_true_for_true(self) -> None:
        record = {"peerReviewed": True}
        result = SCORE_PAPERS.parse_bool(record, "peerReviewed")
        self.assertTrue(result)

    def test_parse_bool_returns_false_for_false(self) -> None:
        record = {"peerReviewed": False}
        result = SCORE_PAPERS.parse_bool(record, "peerReviewed")
        self.assertFalse(result)

    def test_parse_bool_returns_false_for_missing_key(self) -> None:
        record = {}
        result = SCORE_PAPERS.parse_bool(record, "peerReviewed")
        self.assertFalse(result)

    def test_parse_bool_handles_string_true(self) -> None:
        record = {"peerReviewed": "true"}
        result = SCORE_PAPERS.parse_bool(record, "peerReviewed")
        self.assertTrue(result)

    def test_parse_bool_handles_string_yes(self) -> None:
        record = {"peerReviewed": "yes"}
        result = SCORE_PAPERS.parse_bool(record, "peerReviewed")
        self.assertTrue(result)

    def test_parse_bool_handles_string_y(self) -> None:
        record = {"peerReviewed": "y"}
        result = SCORE_PAPERS.parse_bool(record, "peerReviewed")
        self.assertTrue(result)

    def test_parse_bool_handles_string_one(self) -> None:
        record = {"peerReviewed": "1"}
        result = SCORE_PAPERS.parse_bool(record, "peerReviewed")
        self.assertTrue(result)

    def test_parse_bool_handles_string_false(self) -> None:
        record = {"peerReviewed": "false"}
        result = SCORE_PAPERS.parse_bool(record, "peerReviewed")
        self.assertFalse(result)

    def test_parse_bool_handles_int_one(self) -> None:
        record = {"peerReviewed": 1}
        result = SCORE_PAPERS.parse_bool(record, "peerReviewed")
        self.assertTrue(result)

    def test_parse_bool_handles_int_zero(self) -> None:
        record = {"peerReviewed": 0}
        result = SCORE_PAPERS.parse_bool(record, "peerReviewed")
        self.assertFalse(result)

    def test_parse_bool_handles_float(self) -> None:
        record = {"peerReviewed": 1.5}
        result = SCORE_PAPERS.parse_bool(record, "peerReviewed")
        self.assertTrue(result)

    def test_parse_bool_handles_case_insensitive(self) -> None:
        record = {"peerReviewed": "TRUE"}
        result = SCORE_PAPERS.parse_bool(record, "peerReviewed")
        self.assertTrue(result)

    def test_parse_bool_handles_whitespace(self) -> None:
        record = {"peerReviewed": "  yes  "}
        result = SCORE_PAPERS.parse_bool(record, "peerReviewed")
        self.assertTrue(result)


class TestNormalizeCcf(unittest.TestCase):
    """Tests for normalize_ccf function."""

    def test_normalize_ccf_returns_a(self) -> None:
        result = SCORE_PAPERS.normalize_ccf("A")
        self.assertEqual("A", result)

    def test_normalize_ccf_returns_b(self) -> None:
        result = SCORE_PAPERS.normalize_ccf("B")
        self.assertEqual("B", result)

    def test_normalize_ccf_returns_c(self) -> None:
        result = SCORE_PAPERS.normalize_ccf("C")
        self.assertEqual("C", result)

    def test_normalize_ccf_handles_lowercase(self) -> None:
        result = SCORE_PAPERS.normalize_ccf("a")
        self.assertEqual("A", result)

    def test_normalize_ccf_handles_ccf_prefix_with_dash(self) -> None:
        result = SCORE_PAPERS.normalize_ccf("CCF-A")
        self.assertEqual("A", result)

    def test_normalize_ccf_handles_ccf_prefix_with_space(self) -> None:
        result = SCORE_PAPERS.normalize_ccf("CCF B")
        self.assertEqual("B", result)

    def test_normalize_ccf_handles_whitespace(self) -> None:
        result = SCORE_PAPERS.normalize_ccf("  A  ")
        self.assertEqual("A", result)

    def test_normalize_ccf_returns_none_for_invalid(self) -> None:
        result = SCORE_PAPERS.normalize_ccf("D")
        self.assertIsNone(result)

    def test_normalize_ccf_returns_none_for_none(self) -> None:
        result = SCORE_PAPERS.normalize_ccf(None)
        self.assertIsNone(result)

    def test_normalize_ccf_returns_none_for_random_string(self) -> None:
        result = SCORE_PAPERS.normalize_ccf("random")
        self.assertIsNone(result)


class TestNormalizeJcr(unittest.TestCase):
    """Tests for normalize_jcr function."""

    def test_normalize_jcr_returns_q1(self) -> None:
        result = SCORE_PAPERS.normalize_jcr("Q1")
        self.assertEqual("Q1", result)

    def test_normalize_jcr_returns_q2(self) -> None:
        result = SCORE_PAPERS.normalize_jcr("Q2")
        self.assertEqual("Q2", result)

    def test_normalize_jcr_returns_q3(self) -> None:
        result = SCORE_PAPERS.normalize_jcr("Q3")
        self.assertEqual("Q3", result)

    def test_normalize_jcr_returns_q4(self) -> None:
        result = SCORE_PAPERS.normalize_jcr("Q4")
        self.assertEqual("Q4", result)

    def test_normalize_jcr_handles_lowercase(self) -> None:
        result = SCORE_PAPERS.normalize_jcr("q1")
        self.assertEqual("Q1", result)

    def test_normalize_jcr_handles_whitespace(self) -> None:
        result = SCORE_PAPERS.normalize_jcr("  Q2  ")
        self.assertEqual("Q2", result)

    def test_normalize_jcr_returns_none_for_invalid(self) -> None:
        result = SCORE_PAPERS.normalize_jcr("Q5")
        self.assertIsNone(result)

    def test_normalize_jcr_returns_none_for_none(self) -> None:
        result = SCORE_PAPERS.normalize_jcr(None)
        self.assertIsNone(result)

    def test_normalize_jcr_returns_none_for_random_string(self) -> None:
        result = SCORE_PAPERS.normalize_jcr("random")
        self.assertIsNone(result)


class TestComputeScores(unittest.TestCase):
    """Tests for compute_scores function."""

    def test_compute_scores_returns_dict_with_scores(self) -> None:
        record = {
            "title": "Test Paper",
            "year": 2023,
            "doi": "10.1234/test",
            "source": "Test Conference",
            "sourceUrl": "https://example.com",
        }
        result = SCORE_PAPERS.compute_scores(record, current_year=2025, allow_preprint=False)

        self.assertIn("qualityScore", result)
        self.assertIn("venueScore", result)
        self.assertIn("freshnessScore", result)
        self.assertIn("citationScore", result)
        self.assertIn("impactScore", result)
        self.assertIn("relevanceScore", result)
        self.assertIn("evidenceScore", result)
        self.assertIn("publicationBonus", result)
        self.assertIn("citationsPerYear", result)
        self.assertIn("eligible", result)
        self.assertIn("rejectionReasons", result)

    def test_compute_scores_marks_eligible_for_complete_record(self) -> None:
        record = {
            "title": "Test Paper",
            "year": 2023,
            "doi": "10.1234/test",
            "source": "Test Conference",
            "sourceUrl": "https://example.com",
        }
        result = SCORE_PAPERS.compute_scores(record, current_year=2025, allow_preprint=False)

        self.assertTrue(result["eligible"])
        self.assertEqual([], result["rejectionReasons"])

    def test_compute_scores_rejects_missing_doi_without_bibtex(self) -> None:
        record = {
            "title": "Test Paper",
            "year": 2023,
            "source": "Test Conference",
            "sourceUrl": "https://example.com",
        }
        result = SCORE_PAPERS.compute_scores(record, current_year=2025, allow_preprint=False)

        self.assertFalse(result["eligible"])
        self.assertIn("missing-doi-and-no-trusted-bibtex-source", result["rejectionReasons"])

    def test_compute_scores_rejects_missing_provenance(self) -> None:
        record = {
            "title": "Test Paper",
            "year": 2023,
            "doi": "10.1234/test",
        }
        result = SCORE_PAPERS.compute_scores(record, current_year=2025, allow_preprint=False)

        self.assertFalse(result["eligible"])
        self.assertIn("missing-provenance", result["rejectionReasons"])

    def test_compute_scores_rejects_preprint_with_formal_version(self) -> None:
        record = {
            "title": "Test Paper",
            "year": 2023,
            "doi": "10.1234/test",
            "source": "arXiv",
            "sourceUrl": "https://arxiv.org/abs/1234",
            "preprint": True,
            "hasFormalVersion": True,
        }
        result = SCORE_PAPERS.compute_scores(record, current_year=2025, allow_preprint=False)

        self.assertFalse(result["eligible"])
        self.assertIn("replace-with-formal-version", result["rejectionReasons"])

    def test_compute_scores_rejects_preprint_when_not_allowed(self) -> None:
        record = {
            "title": "Test Paper",
            "year": 2023,
            "doi": "10.1234/test",
            "source": "arXiv",
            "sourceUrl": "https://arxiv.org/abs/1234",
            "preprint": True,
            "hasFormalVersion": False,
        }
        result = SCORE_PAPERS.compute_scores(record, current_year=2025, allow_preprint=False)

        self.assertFalse(result["eligible"])
        self.assertIn("preprint-not-allowed", result["rejectionReasons"])

    def test_compute_scores_accepts_preprint_when_allowed(self) -> None:
        record = {
            "title": "Test Paper",
            "year": 2023,
            "doi": "10.1234/test",
            "source": "arXiv",
            "sourceUrl": "https://arxiv.org/abs/1234",
            "preprint": True,
            "hasFormalVersion": False,
        }
        result = SCORE_PAPERS.compute_scores(record, current_year=2025, allow_preprint=True)

        self.assertTrue(result["eligible"])

    def test_compute_scores_calculates_freshness_score(self) -> None:
        record = {
            "title": "New Paper",
            "year": 2024,
            "doi": "10.1234/test",
            "source": "Test",
            "sourceUrl": "https://example.com",
        }
        result = SCORE_PAPERS.compute_scores(record, current_year=2025, allow_preprint=False)

        # Fresh paper (age 1) should have high freshness score
        self.assertGreater(result["freshnessScore"], 15.0)

    def test_compute_scores_calculates_citation_score(self) -> None:
        record = {
            "title": "Cited Paper",
            "year": 2023,
            "doi": "10.1234/test",
            "source": "Test",
            "sourceUrl": "https://example.com",
            "citationCount": 100,
        }
        result = SCORE_PAPERS.compute_scores(record, current_year=2025, allow_preprint=False)

        self.assertGreater(result["citationScore"], 0.0)

    def test_compute_scores_uses_ccf_tier_for_venue_score(self) -> None:
        record = {
            "title": "CCF-A Paper",
            "year": 2023,
            "doi": "10.1234/test",
            "source": "Test",
            "sourceUrl": "https://example.com",
            "ccfTier": "A",
        }
        result = SCORE_PAPERS.compute_scores(record, current_year=2025, allow_preprint=False)

        self.assertEqual(35.0, result["venueScore"])

    def test_compute_scores_uses_jcr_quartile_for_venue_score(self) -> None:
        record = {
            "title": "Q1 Journal Paper",
            "year": 2023,
            "doi": "10.1234/test",
            "source": "Test",
            "sourceUrl": "https://example.com",
            "jcrQuartile": "Q1",
        }
        result = SCORE_PAPERS.compute_scores(record, current_year=2025, allow_preprint=False)

        self.assertEqual(30.0, result["venueScore"])

    def test_compute_scores_uses_max_venue_score(self) -> None:
        record = {
            "title": "Paper with both CCF and JCR",
            "year": 2023,
            "doi": "10.1234/test",
            "source": "Test",
            "sourceUrl": "https://example.com",
            "ccfTier": "B",  # 28.0
            "jcrQuartile": "Q1",  # 30.0
        }
        result = SCORE_PAPERS.compute_scores(record, current_year=2025, allow_preprint=False)

        # Should use max (Q1 = 30.0)
        self.assertEqual(30.0, result["venueScore"])

    def test_compute_scores_gives_bonus_for_peer_reviewed(self) -> None:
        record_peer = {
            "title": "Peer Reviewed",
            "year": 2023,
            "doi": "10.1234/test",
            "source": "Test",
            "sourceUrl": "https://example.com",
            "peerReviewed": True,
        }
        record_not_peer = {
            "title": "Not Peer Reviewed",
            "year": 2023,
            "doi": "10.1234/test",
            "source": "Test",
            "sourceUrl": "https://example.com",
            "peerReviewed": False,
        }
        result_peer = SCORE_PAPERS.compute_scores(
            record_peer, current_year=2025, allow_preprint=False
        )
        result_not_peer = SCORE_PAPERS.compute_scores(
            record_not_peer, current_year=2025, allow_preprint=False
        )

        self.assertGreater(result_peer["venueScore"], result_not_peer["venueScore"])

    def test_compute_scores_calculates_publication_bonus(self) -> None:
        record_with_doi = {
            "title": "Paper with DOI",
            "year": 2023,
            "doi": "10.1234/test",
            "source": "Test",
            "sourceUrl": "https://example.com",
        }
        result = SCORE_PAPERS.compute_scores(
            record_with_doi, current_year=2025, allow_preprint=False
        )

        self.assertEqual(5.0, result["publicationBonus"])

    def test_compute_scores_calculates_publication_bonus_with_bibtex(self) -> None:
        record_with_bibtex = {
            "title": "Paper with Bibtex",
            "year": 2023,
            "doi": "",
            "reliableBibtexSource": "https://example.com/bib",
            "source": "Test",
            "sourceUrl": "https://example.com",
        }
        result = SCORE_PAPERS.compute_scores(
            record_with_bibtex, current_year=2025, allow_preprint=True
        )

        # Has reliable bibtex but no DOI
        self.assertEqual(3.0, result["publicationBonus"])

    def test_compute_scores_clamps_relevance_score(self) -> None:
        record = {
            "title": "Test Paper",
            "year": 2023,
            "doi": "10.1234/test",
            "source": "Test",
            "sourceUrl": "https://example.com",
            "relevanceScore": 15.0,  # Exceeds max of 10
        }
        result = SCORE_PAPERS.compute_scores(record, current_year=2025, allow_preprint=False)

        self.assertEqual(10.0, result["relevanceScore"])

    def test_compute_scores_clamps_evidence_score(self) -> None:
        record = {
            "title": "Test Paper",
            "year": 2023,
            "doi": "10.1234/test",
            "source": "Test",
            "sourceUrl": "https://example.com",
            "evidenceScore": -5.0,  # Below min of 0
        }
        result = SCORE_PAPERS.compute_scores(record, current_year=2025, allow_preprint=False)

        self.assertEqual(0.0, result["evidenceScore"])

    def test_compute_scores_preserves_original_record_fields(self) -> None:
        record = {
            "title": "Test Paper",
            "year": 2023,
            "doi": "10.1234/test",
            "source": "Test",
            "sourceUrl": "https://example.com",
            "customField": "custom value",
        }
        result = SCORE_PAPERS.compute_scores(record, current_year=2025, allow_preprint=False)

        self.assertEqual("Test Paper", result["title"])
        self.assertEqual(2023, result["year"])
        self.assertEqual("custom value", result["customField"])

    def test_compute_scores_rounds_scores(self) -> None:
        record = {
            "title": "Test Paper",
            "year": 2023,
            "doi": "10.1234/test",
            "source": "Test",
            "sourceUrl": "https://example.com",
            "impactFactor": 3.333333,
            "citationCount": 99,
        }
        result = SCORE_PAPERS.compute_scores(record, current_year=2025, allow_preprint=False)

        # All scores should have at most 2 decimal places
        for key in ["qualityScore", "venueScore", "freshnessScore", "citationScore", "impactScore"]:
            decimal_places = len(str(result[key]).split(".")[-1])
            self.assertLessEqual(decimal_places, 2)


if __name__ == "__main__":
    unittest.main()
