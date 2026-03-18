import importlib.util
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


INIT = load_script_module("init_research_project")
CITATION = load_script_module("run_citation_audit")


class CitationAuditTest(unittest.TestCase):
    def test_generates_citation_audit_report_from_detected_gaps(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "citation-audit"
            INIT.initialize_research_project(project_root=project_root, topic="Citation audit")
            draft = project_root / "paper/paper-draft.md"
            draft.parent.mkdir(parents=True, exist_ok=True)
            draft.write_text("This claim needs support [cite].\n", encoding="utf-8")

            mock_claims = [
                {
                    "id": 1,
                    "start_line": 1,
                    "end_line": 1,
                    "text": "This claim needs support [cite].",
                    "clean_claim": "This claim needs support .",
                }
            ]
            with patch.object(CITATION, "_extract_claims", return_value=mock_claims):
                result = CITATION.run_citation_audit(project_root)

            self.assertEqual(1, result["detected_claims"])
            self.assertEqual("revise", result["authenticity_status"])
            report_text = (project_root / result["report_path"]).read_text(encoding="utf-8")
            self.assertIn("Detected citation gaps", report_text)
            self.assertIn("Citation authenticity status: `revise`", report_text)
            self.assertIn("citation-gaps-detected-but-not-verified", report_text)

    def test_audits_existing_bib_entries_and_emits_structured_verdict(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "citation-audit-existing-bib"
            INIT.initialize_research_project(project_root=project_root, topic="Citation audit bib")
            draft = project_root / "paper/paper-draft.md"
            draft.parent.mkdir(parents=True, exist_ok=True)
            draft.write_text(
                "FedAvg remains a baseline in FL. See \\cite{fedavg}.\n", encoding="utf-8"
            )
            bib_path = project_root / "paper" / "refs.bib"
            bib_path.write_text(
                "\n".join(
                    [
                        "@inproceedings{fedavg,",
                        "  title = {Communication-Efficient Learning of Deep Networks "
                        "from Decentralized Data},",
                        "  doi = {10.48550/arXiv.1602.05629},",
                        "  x-verification-status = {verified-doi},",
                        "  x-bib-source = {doi-content-negotiation},",
                        "}",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            with patch.object(CITATION, "_extract_claims", return_value=[]):
                result = CITATION.run_citation_audit(project_root, existing_bib="paper/refs.bib")

            self.assertEqual("approved", result["authenticity_status"])
            self.assertEqual(1, result["audited_citation_keys"])
            report_text = (project_root / result["report_path"]).read_text(encoding="utf-8")
            self.assertIn("Citation authenticity status: `approved`", report_text)
            self.assertIn("DOI-verified citations: `fedavg`", report_text)
            self.assertIn("Blocking issues: `none`", report_text)


if __name__ == "__main__":
    unittest.main()
