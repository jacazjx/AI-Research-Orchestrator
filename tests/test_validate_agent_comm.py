"""Tests for scripts/validate_agent_comm.py.

Covers:
- Valid inputs for all 5 message types (dispatch, completion, challenge, response, debate)
- Missing required fields for each type
- Invalid enum values
- Empty required lists
- --json flag output
"""

from __future__ import annotations

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


VAL = load_script_module("validate_agent_comm")


def _write_yaml(tmp_dir: Path, filename: str, content: str) -> Path:
    path = tmp_dir / filename
    path.write_text(content, encoding="utf-8")
    return path


def _write_json(tmp_dir: Path, filename: str, data: dict) -> Path:
    path = tmp_dir / filename
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# dispatch
# ---------------------------------------------------------------------------

VALID_DISPATCH_YAML = """\
task_id: "task-001"
skill: "research-lit"
context:
  research_topic: "Adaptive learning rate schedules"
  current_phase: "survey"
deliverables:
  - "docs/survey/literature-review.md"
  - "docs/survey/idea-definition.md"
"""


class TestValidateDispatch(unittest.TestCase):
    def test_valid_dispatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "dispatch.yaml", VALID_DISPATCH_YAML)
            result = VAL.validate_message("dispatch", path)
            self.assertTrue(result["valid"], result["errors"])
            self.assertEqual([], result["errors"])

    def test_dispatch_missing_task_id(self) -> None:
        content = """\
skill: "research-lit"
context:
  research_topic: "Topic"
  current_phase: "survey"
deliverables:
  - "docs/survey/lit.md"
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "dispatch.yaml", content)
            result = VAL.validate_message("dispatch", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("task_id" in e for e in result["errors"]))

    def test_dispatch_missing_skill(self) -> None:
        content = """\
task_id: "t1"
context:
  research_topic: "Topic"
  current_phase: "pilot"
deliverables:
  - "docs/pilot/report.md"
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "dispatch.yaml", content)
            result = VAL.validate_message("dispatch", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("skill" in e for e in result["errors"]))

    def test_dispatch_missing_context(self) -> None:
        content = """\
task_id: "t1"
skill: "run-pilot"
deliverables:
  - "docs/pilot/report.md"
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "dispatch.yaml", content)
            result = VAL.validate_message("dispatch", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("context" in e for e in result["errors"]))

    def test_dispatch_missing_research_topic(self) -> None:
        content = """\
task_id: "t1"
skill: "run-pilot"
context:
  current_phase: "pilot"
deliverables:
  - "docs/pilot/report.md"
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "dispatch.yaml", content)
            result = VAL.validate_message("dispatch", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("research_topic" in e for e in result["errors"]))

    def test_dispatch_invalid_phase_enum(self) -> None:
        content = """\
task_id: "t1"
skill: "run-pilot"
context:
  research_topic: "Topic"
  current_phase: "kickoff"
deliverables:
  - "docs/pilot/report.md"
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "dispatch.yaml", content)
            result = VAL.validate_message("dispatch", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("current_phase" in e for e in result["errors"]))

    def test_dispatch_empty_deliverables(self) -> None:
        content = """\
task_id: "t1"
skill: "run-pilot"
context:
  research_topic: "Topic"
  current_phase: "pilot"
deliverables: []
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "dispatch.yaml", content)
            result = VAL.validate_message("dispatch", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("deliverables" in e for e in result["errors"]))

    def test_dispatch_missing_deliverables(self) -> None:
        content = """\
task_id: "t1"
skill: "run-pilot"
context:
  research_topic: "Topic"
  current_phase: "pilot"
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "dispatch.yaml", content)
            result = VAL.validate_message("dispatch", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("deliverables" in e for e in result["errors"]))

    def test_dispatch_all_valid_phases(self) -> None:
        for phase in ("survey", "pilot", "experiments", "paper", "reflection"):
            content = f"""\
task_id: "t-{phase}"
skill: "some-skill"
context:
  research_topic: "Topic"
  current_phase: "{phase}"
deliverables:
  - "docs/{phase}/file.md"
"""
            with tempfile.TemporaryDirectory() as tmp:
                path = _write_yaml(Path(tmp), "dispatch.yaml", content)
                result = VAL.validate_message("dispatch", path)
                self.assertTrue(result["valid"], f"Phase {phase} failed: {result['errors']}")


# ---------------------------------------------------------------------------
# completion
# ---------------------------------------------------------------------------

VALID_COMPLETION_YAML = """\
task_id: "task-001"
status: "completed"
deliverables:
  - path: "docs/survey/literature-review.md"
    status: "created"
    summary: "Comprehensive literature review covering 50 papers."
errors: []
"""


class TestValidateCompletion(unittest.TestCase):
    def test_valid_completion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "completion.yaml", VALID_COMPLETION_YAML)
            result = VAL.validate_message("completion", path)
            self.assertTrue(result["valid"], result["errors"])

    def test_valid_completion_with_errors(self) -> None:
        content = """\
task_id: "task-002"
status: "failed"
deliverables: []
errors:
  - "Could not connect to API"
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "completion.yaml", content)
            result = VAL.validate_message("completion", path)
            self.assertTrue(result["valid"], result["errors"])

    def test_completion_missing_task_id(self) -> None:
        content = """\
status: "completed"
deliverables: []
errors: []
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "completion.yaml", content)
            result = VAL.validate_message("completion", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("task_id" in e for e in result["errors"]))

    def test_completion_invalid_status_enum(self) -> None:
        content = """\
task_id: "t1"
status: "done"
deliverables: []
errors: []
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "completion.yaml", content)
            result = VAL.validate_message("completion", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("status" in e for e in result["errors"]))

    def test_completion_deliverable_invalid_status(self) -> None:
        content = """\
task_id: "t1"
status: "completed"
deliverables:
  - path: "docs/survey/lit.md"
    status: "generated"
    summary: "A summary."
errors: []
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "completion.yaml", content)
            result = VAL.validate_message("completion", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("status" in e for e in result["errors"]))

    def test_completion_deliverable_missing_path(self) -> None:
        content = """\
task_id: "t1"
status: "completed"
deliverables:
  - status: "created"
    summary: "A summary."
errors: []
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "completion.yaml", content)
            result = VAL.validate_message("completion", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("path" in e for e in result["errors"]))

    def test_completion_deliverable_missing_summary(self) -> None:
        content = """\
task_id: "t1"
status: "completed"
deliverables:
  - path: "docs/file.md"
    status: "created"
errors: []
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "completion.yaml", content)
            result = VAL.validate_message("completion", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("summary" in e for e in result["errors"]))

    def test_completion_missing_errors_field(self) -> None:
        content = """\
task_id: "t1"
status: "completed"
deliverables: []
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "completion.yaml", content)
            result = VAL.validate_message("completion", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("errors" in e for e in result["errors"]))

    def test_completion_all_valid_statuses(self) -> None:
        for status in ("completed", "failed", "in_progress"):
            content = f"""\
task_id: "t-{status}"
status: "{status}"
deliverables: []
errors: []
"""
            with tempfile.TemporaryDirectory() as tmp:
                path = _write_yaml(Path(tmp), "completion.yaml", content)
                result = VAL.validate_message("completion", path)
                self.assertTrue(result["valid"], f"Status {status} failed: {result['errors']}")


# ---------------------------------------------------------------------------
# challenge
# ---------------------------------------------------------------------------

VALID_CHALLENGE_YAML = """\
challenge_type: "derivation_audit"
disputed_points:
  - point_id: "pt-001"
    original_claim: "The loss function converges in O(n log n)."
    challenge_reason: "The proof skips the case where gradient is zero."
    proposed_alternative: "Convergence is O(n^2) under the given assumptions."
"""


class TestValidateChallenge(unittest.TestCase):
    def test_valid_challenge(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "challenge.yaml", VALID_CHALLENGE_YAML)
            result = VAL.validate_message("challenge", path)
            self.assertTrue(result["valid"], result["errors"])

    def test_challenge_missing_challenge_type(self) -> None:
        content = """\
disputed_points:
  - point_id: "pt-001"
    original_claim: "Claim."
    challenge_reason: "Reason."
    proposed_alternative: "Alternative."
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "challenge.yaml", content)
            result = VAL.validate_message("challenge", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("challenge_type" in e for e in result["errors"]))

    def test_challenge_invalid_challenge_type_enum(self) -> None:
        content = """\
challenge_type: "math_audit"
disputed_points:
  - point_id: "pt-001"
    original_claim: "Claim."
    challenge_reason: "Reason."
    proposed_alternative: "Alternative."
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "challenge.yaml", content)
            result = VAL.validate_message("challenge", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("challenge_type" in e for e in result["errors"]))

    def test_challenge_empty_disputed_points(self) -> None:
        content = """\
challenge_type: "survey_audit"
disputed_points: []
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "challenge.yaml", content)
            result = VAL.validate_message("challenge", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("disputed_points" in e for e in result["errors"]))

    def test_challenge_missing_disputed_points(self) -> None:
        content = """\
challenge_type: "survey_audit"
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "challenge.yaml", content)
            result = VAL.validate_message("challenge", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("disputed_points" in e for e in result["errors"]))

    def test_challenge_point_missing_point_id(self) -> None:
        content = """\
challenge_type: "derivation_audit"
disputed_points:
  - original_claim: "Claim."
    challenge_reason: "Reason."
    proposed_alternative: "Alternative."
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "challenge.yaml", content)
            result = VAL.validate_message("challenge", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("point_id" in e for e in result["errors"]))

    def test_challenge_point_missing_proposed_alternative(self) -> None:
        content = """\
challenge_type: "derivation_audit"
disputed_points:
  - point_id: "pt-001"
    original_claim: "Claim."
    challenge_reason: "Reason."
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "challenge.yaml", content)
            result = VAL.validate_message("challenge", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("proposed_alternative" in e for e in result["errors"]))

    def test_challenge_all_valid_types(self) -> None:
        for ctype in ("derivation_audit", "survey_audit"):
            content = f"""\
challenge_type: "{ctype}"
disputed_points:
  - point_id: "pt-001"
    original_claim: "Claim."
    challenge_reason: "Reason."
    proposed_alternative: "Alternative."
"""
            with tempfile.TemporaryDirectory() as tmp:
                path = _write_yaml(Path(tmp), "challenge.yaml", content)
                result = VAL.validate_message("challenge", path)
                self.assertTrue(result["valid"], f"Type {ctype} failed: {result['errors']}")


# ---------------------------------------------------------------------------
# response
# ---------------------------------------------------------------------------

VALID_RESPONSE_YAML = """\
response_type: "partial"
point_responses:
  - point_id: "pt-001"
    action: "accept"
    reason: "The analysis is sound and well-supported."
  - point_id: "pt-002"
    action: "modify"
    reason: "The original position needs refinement."
    modified_position: "Convergence requires an additional Lipschitz condition."
  - point_id: "pt-003"
    action: "reject"
    reason: "The proposed alternative contradicts established theory."
"""


class TestValidateResponse(unittest.TestCase):
    def test_valid_response(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "response.yaml", VALID_RESPONSE_YAML)
            result = VAL.validate_message("response", path)
            self.assertTrue(result["valid"], result["errors"])

    def test_response_missing_response_type(self) -> None:
        content = """\
point_responses:
  - point_id: "pt-001"
    action: "accept"
    reason: "Reason."
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "response.yaml", content)
            result = VAL.validate_message("response", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("response_type" in e for e in result["errors"]))

    def test_response_invalid_response_type_enum(self) -> None:
        content = """\
response_type: "maybe"
point_responses:
  - point_id: "pt-001"
    action: "accept"
    reason: "Reason."
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "response.yaml", content)
            result = VAL.validate_message("response", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("response_type" in e for e in result["errors"]))

    def test_response_empty_point_responses(self) -> None:
        content = """\
response_type: "accept"
point_responses: []
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "response.yaml", content)
            result = VAL.validate_message("response", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("point_responses" in e for e in result["errors"]))

    def test_response_invalid_action_enum(self) -> None:
        content = """\
response_type: "accept"
point_responses:
  - point_id: "pt-001"
    action: "ignore"
    reason: "Reason."
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "response.yaml", content)
            result = VAL.validate_message("response", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("action" in e for e in result["errors"]))

    def test_response_modify_requires_modified_position(self) -> None:
        content = """\
response_type: "partial"
point_responses:
  - point_id: "pt-001"
    action: "modify"
    reason: "Needs change."
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "response.yaml", content)
            result = VAL.validate_message("response", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("modified_position" in e for e in result["errors"]))

    def test_response_modify_with_modified_position(self) -> None:
        content = """\
response_type: "partial"
point_responses:
  - point_id: "pt-001"
    action: "modify"
    reason: "Needs change."
    modified_position: "Revised claim here."
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "response.yaml", content)
            result = VAL.validate_message("response", path)
            self.assertTrue(result["valid"], result["errors"])

    def test_response_missing_point_id(self) -> None:
        content = """\
response_type: "accept"
point_responses:
  - action: "accept"
    reason: "Reason."
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "response.yaml", content)
            result = VAL.validate_message("response", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("point_id" in e for e in result["errors"]))

    def test_response_missing_reason(self) -> None:
        content = """\
response_type: "accept"
point_responses:
  - point_id: "pt-001"
    action: "accept"
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "response.yaml", content)
            result = VAL.validate_message("response", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("reason" in e for e in result["errors"]))

    def test_response_all_valid_types(self) -> None:
        for rtype in ("accept", "reject", "partial"):
            content = f"""\
response_type: "{rtype}"
point_responses:
  - point_id: "pt-001"
    action: "accept"
    reason: "Reason."
"""
            with tempfile.TemporaryDirectory() as tmp:
                path = _write_yaml(Path(tmp), "response.yaml", content)
                result = VAL.validate_message("response", path)
                self.assertTrue(result["valid"], f"Type {rtype} failed: {result['errors']}")


# ---------------------------------------------------------------------------
# debate
# ---------------------------------------------------------------------------

VALID_DEBATE_DEBATING = {
    "round": 1,
    "phase": "survey",
    "primary_agent": "survey-agent",
    "reviewer_agent": "critic-agent",
    "status": "debating",
    "turns": [],
    "resolved_issues": [],
    "unresolved_issues": ["convergence proof"],
}

VALID_DEBATE_COMPLETED = {
    "round": 2,
    "phase": "pilot",
    "primary_agent": "code-agent",
    "reviewer_agent": "adviser-agent",
    "status": "completed",
    "turns": [{"turn": 1, "speaker": "code-agent", "content": "Initial claim."}],
    "resolved_issues": ["baseline comparison"],
    "unresolved_issues": [],
    "verdict": {
        "decision": "approve",
        "verdict_by": "adviser-agent",
        "scores": {"technical": 4.5, "novelty": 4.0},
        "required_actions": [],
    },
}


class TestValidateDebate(unittest.TestCase):
    def test_valid_debate_debating_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_json(Path(tmp), "debate.json", VALID_DEBATE_DEBATING)
            result = VAL.validate_message("debate", path)
            self.assertTrue(result["valid"], result["errors"])

    def test_valid_debate_completed_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_json(Path(tmp), "debate.json", VALID_DEBATE_COMPLETED)
            result = VAL.validate_message("debate", path)
            self.assertTrue(result["valid"], result["errors"])

    def test_valid_debate_as_yaml(self) -> None:
        content = """\
round: 1
phase: "survey"
primary_agent: "survey-agent"
reviewer_agent: "critic-agent"
status: "debating"
turns: []
resolved_issues: []
unresolved_issues: []
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "debate.yaml", content)
            result = VAL.validate_message("debate", path)
            self.assertTrue(result["valid"], result["errors"])

    def test_debate_missing_round(self) -> None:
        data = dict(VALID_DEBATE_DEBATING)
        del data["round"]
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_json(Path(tmp), "debate.json", data)
            result = VAL.validate_message("debate", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("round" in e for e in result["errors"]))

    def test_debate_round_zero(self) -> None:
        data = dict(VALID_DEBATE_DEBATING)
        data["round"] = 0
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_json(Path(tmp), "debate.json", data)
            result = VAL.validate_message("debate", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("round" in e for e in result["errors"]))

    def test_debate_missing_phase(self) -> None:
        data = dict(VALID_DEBATE_DEBATING)
        del data["phase"]
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_json(Path(tmp), "debate.json", data)
            result = VAL.validate_message("debate", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("phase" in e for e in result["errors"]))

    def test_debate_invalid_status_enum(self) -> None:
        data = dict(VALID_DEBATE_DEBATING)
        data["status"] = "ongoing"
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_json(Path(tmp), "debate.json", data)
            result = VAL.validate_message("debate", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("status" in e for e in result["errors"]))

    def test_debate_missing_turns(self) -> None:
        data = dict(VALID_DEBATE_DEBATING)
        del data["turns"]
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_json(Path(tmp), "debate.json", data)
            result = VAL.validate_message("debate", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("turns" in e for e in result["errors"]))

    def test_debate_completed_missing_verdict(self) -> None:
        data = dict(VALID_DEBATE_COMPLETED)
        data = {k: v for k, v in data.items() if k != "verdict"}
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_json(Path(tmp), "debate.json", data)
            result = VAL.validate_message("debate", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("verdict" in e for e in result["errors"]))

    def test_debate_verdict_invalid_decision(self) -> None:
        data = {
            **VALID_DEBATE_COMPLETED,
            "verdict": {
                "decision": "postpone",
                "verdict_by": "adviser-agent",
                "scores": {},
                "required_actions": [],
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_json(Path(tmp), "debate.json", data)
            result = VAL.validate_message("debate", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("decision" in e for e in result["errors"]))

    def test_debate_verdict_missing_verdict_by(self) -> None:
        data = {
            **VALID_DEBATE_COMPLETED,
            "verdict": {
                "decision": "approve",
                "scores": {},
                "required_actions": [],
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_json(Path(tmp), "debate.json", data)
            result = VAL.validate_message("debate", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("verdict_by" in e for e in result["errors"]))

    def test_debate_verdict_all_valid_decisions(self) -> None:
        for decision in ("approve", "revise", "reject"):
            data = {
                **VALID_DEBATE_COMPLETED,
                "verdict": {
                    "decision": decision,
                    "verdict_by": "adviser-agent",
                    "scores": {},
                    "required_actions": [],
                },
            }
            with tempfile.TemporaryDirectory() as tmp:
                path = _write_json(Path(tmp), "debate.json", data)
                result = VAL.validate_message("debate", path)
                self.assertTrue(
                    result["valid"], f"Decision '{decision}' failed: {result['errors']}"
                )

    def test_debate_missing_resolved_issues(self) -> None:
        data = dict(VALID_DEBATE_DEBATING)
        del data["resolved_issues"]
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_json(Path(tmp), "debate.json", data)
            result = VAL.validate_message("debate", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("resolved_issues" in e for e in result["errors"]))


# ---------------------------------------------------------------------------
# File loading edge cases
# ---------------------------------------------------------------------------


class TestFileHandling(unittest.TestCase):
    def test_file_not_found(self) -> None:
        result = VAL.validate_message("dispatch", Path("/nonexistent/path/msg.yaml"))
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("not found" in e.lower() or "File not found" in e for e in result["errors"])
        )

    def test_invalid_yaml_syntax(self) -> None:
        content = "task_id: [unclosed bracket\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "bad.yaml", content)
            result = VAL.validate_message("dispatch", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("parse" in e.lower() for e in result["errors"]))

    def test_invalid_json_syntax(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text("{invalid json", encoding="utf-8")
            result = VAL.validate_message("debate", path)
            self.assertFalse(result["valid"])
            self.assertTrue(any("parse" in e.lower() for e in result["errors"]))

    def test_non_mapping_yaml(self) -> None:
        content = "- item1\n- item2\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "list.yaml", content)
            result = VAL.validate_message("dispatch", path)
            self.assertFalse(result["valid"])
            self.assertTrue(
                any("object" in e.lower() or "mapping" in e.lower() for e in result["errors"])
            )


# ---------------------------------------------------------------------------
# --json flag output
# ---------------------------------------------------------------------------


class TestJsonFlagOutput(unittest.TestCase):
    def test_json_flag_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "dispatch.yaml", VALID_DISPATCH_YAML)
            args = ["--type", "dispatch", "--file", str(path), "--json"]
            with patch("sys.argv", ["validate_agent_comm.py"] + args):
                with patch("builtins.print") as mock_print:
                    VAL.main()
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertIn("valid", parsed)
                    self.assertIn("errors", parsed)
                    self.assertTrue(parsed["valid"])
                    self.assertEqual([], parsed["errors"])

    def test_json_flag_invalid(self) -> None:
        content = """\
skill: "research-lit"
context:
  research_topic: "Topic"
  current_phase: "survey"
deliverables:
  - "docs/file.md"
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "dispatch.yaml", content)
            args = ["--type", "dispatch", "--file", str(path), "--json"]
            with patch("sys.argv", ["validate_agent_comm.py"] + args):
                with patch("builtins.print") as mock_print:
                    VAL.main()
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertFalse(parsed["valid"])
                    self.assertGreater(len(parsed["errors"]), 0)

    def test_json_flag_completion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "completion.yaml", VALID_COMPLETION_YAML)
            args = ["--type", "completion", "--file", str(path), "--json"]
            with patch("sys.argv", ["validate_agent_comm.py"] + args):
                with patch("builtins.print") as mock_print:
                    VAL.main()
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertTrue(parsed["valid"])

    def test_json_flag_debate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_json(Path(tmp), "debate.json", VALID_DEBATE_COMPLETED)
            args = ["--type", "debate", "--file", str(path), "--json"]
            with patch("sys.argv", ["validate_agent_comm.py"] + args):
                with patch("builtins.print") as mock_print:
                    VAL.main()
                    call_args = mock_print.call_args[0][0]
                    parsed = json.loads(call_args)
                    self.assertTrue(parsed["valid"])


# ---------------------------------------------------------------------------
# Exit codes
# ---------------------------------------------------------------------------


class TestExitCodes(unittest.TestCase):
    def test_exit_zero_on_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "dispatch.yaml", VALID_DISPATCH_YAML)
            args = ["--type", "dispatch", "--file", str(path)]
            with patch("sys.argv", ["validate_agent_comm.py"] + args):
                with patch("builtins.print"):
                    code = VAL.main()
                    self.assertEqual(0, code)

    def test_exit_one_on_invalid(self) -> None:
        content = "skill: only-skill\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_yaml(Path(tmp), "dispatch.yaml", content)
            args = ["--type", "dispatch", "--file", str(path)]
            with patch("sys.argv", ["validate_agent_comm.py"] + args):
                with patch("builtins.print"), patch("sys.stderr"):
                    code = VAL.main()
                    self.assertEqual(1, code)

    def test_build_parser_accepts_all_types(self) -> None:
        parser = VAL.build_parser()
        for msg_type in ("dispatch", "completion", "challenge", "response", "debate"):
            args = parser.parse_args(["--type", msg_type, "--file", "/tmp/test.yaml"])
            self.assertEqual(msg_type, args.msg_type)


if __name__ == "__main__":
    unittest.main()
