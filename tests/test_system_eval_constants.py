import importlib.util
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from constants.phases import DEFAULT_DELIVERABLES, HANDOFF_REQUIREMENTS
from constants.paths import EXPECTED_DELIVERABLE_PREFIXES
from state.builder import _build_default_substep_status


def test_system_evaluation_report_in_default_deliverables():
    assert "system_evaluation_report" in DEFAULT_DELIVERABLES
    assert DEFAULT_DELIVERABLES["system_evaluation_report"] == "docs/reflection/system-evaluation-report.md"


def test_system_evaluation_report_in_expected_prefixes():
    assert "system_evaluation_report" in EXPECTED_DELIVERABLE_PREFIXES
    assert EXPECTED_DELIVERABLE_PREFIXES["system_evaluation_report"] == "docs/"


def test_reflection_closeout_includes_system_evaluation():
    req = HANDOFF_REQUIREMENTS["reflection-closeout"]
    assert "system_evaluation_report" in req["deliverables"]


def test_reflection_substep_includes_system_evaluation():
    substep_status = _build_default_substep_status()
    assert "system_evaluation" in substep_status["reflection"]
    se = substep_status["reflection"]["system_evaluation"]
    assert se["status"] == "pending"
    assert se["review_result"] == "pending"
    assert se["attempts"] == 0
    assert se["last_agent"] is None
