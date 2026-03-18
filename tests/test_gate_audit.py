"""Tests for gate decision audit logging in save_state."""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, SKILL_DIR / "scripts" / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


COMMON = _load("orchestrator_common")
INIT = _load("init_research_project")


class GateAuditTest(unittest.TestCase):
    def _init_project(self, tmp_dir: str) -> Path:
        project_root = Path(tmp_dir)
        INIT.initialize_research_project(
            project_root=project_root,
            topic="audit test",
            client_type="vscode",
        )
        return project_root

    def test_save_state_without_previous_creates_no_sentinel_events(self) -> None:
        """Calling save_state without previous_state should not write gate events."""
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self._init_project(tmp)
            state = COMMON.load_state(project_root)
            sentinel_path = project_root / COMMON.DEFAULT_DELIVERABLES["sentinel_events"]
            # record initial line count
            initial_lines = (
                sentinel_path.read_text().strip().splitlines() if sentinel_path.exists() else []
            )
            initial_gate_events = [line for line in initial_lines if '"gate_decision"' in line]
            COMMON.save_state(project_root, state)
            new_lines = (
                sentinel_path.read_text().strip().splitlines() if sentinel_path.exists() else []
            )
            new_gate_events = [line for line in new_lines if '"gate_decision"' in line]
            self.assertEqual(
                len(initial_gate_events),
                len(new_gate_events),
                "No gate events should be added without previous_state",
            )

    def test_save_state_logs_gate_approval_event(self) -> None:
        """save_state with previous_state should log when approval_status changes."""
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self._init_project(tmp)
            old_state = COMMON.load_state(project_root)
            new_state = COMMON.load_state(project_root)
            new_state["approval_status"]["gate_1"] = "approved"

            COMMON.save_state(project_root, new_state, previous_state=old_state)

            sentinel_path = project_root / COMMON.DEFAULT_DELIVERABLES["sentinel_events"]
            self.assertTrue(sentinel_path.exists(), "sentinel_events.ndjson should exist")
            events = [
                json.loads(line) for line in sentinel_path.read_text().splitlines() if line.strip()
            ]
            gate_events = [e for e in events if e.get("type") == "gate_decision"]
            self.assertGreater(len(gate_events), 0, "Should have at least one gate_decision event")
            last_event = gate_events[-1]
            self.assertEqual("gate_1", last_event.get("gate"))
            self.assertEqual("approved", last_event.get("status"))
            self.assertIn("timestamp", last_event)

    def test_save_state_no_log_when_gate_unchanged(self) -> None:
        """No gate event should be logged when approval_status doesn't change."""
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self._init_project(tmp)
            state = COMMON.load_state(project_root)
            sentinel_path = project_root / COMMON.DEFAULT_DELIVERABLES["sentinel_events"]
            initial_events = (
                [
                    line
                    for line in sentinel_path.read_text().splitlines()
                    if '"gate_decision"' in line
                ]
                if sentinel_path.exists()
                else []
            )
            COMMON.save_state(project_root, state, previous_state=state)
            new_events = (
                [
                    line
                    for line in sentinel_path.read_text().splitlines()
                    if '"gate_decision"' in line
                ]
                if sentinel_path.exists()
                else []
            )
            self.assertEqual(
                len(initial_events), len(new_events), "No gate events when status unchanged"
            )

    def test_gate_event_has_iso_timestamp(self) -> None:
        """Gate events should have valid ISO 8601 timestamp."""
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self._init_project(tmp)
            old_state = COMMON.load_state(project_root)
            new_state = COMMON.load_state(project_root)
            new_state["approval_status"]["gate_2"] = "approved"
            COMMON.save_state(project_root, new_state, previous_state=old_state)

            sentinel_path = project_root / COMMON.DEFAULT_DELIVERABLES["sentinel_events"]
            events = [
                json.loads(line) for line in sentinel_path.read_text().splitlines() if line.strip()
            ]
            gate_events = [e for e in events if e.get("type") == "gate_decision"]
            self.assertGreater(len(gate_events), 0)
            ts = gate_events[-1]["timestamp"]
            # Basic ISO 8601 check
            self.assertIn("T", ts, f"Timestamp should be ISO 8601: {ts}")


if __name__ == "__main__":
    unittest.main()
