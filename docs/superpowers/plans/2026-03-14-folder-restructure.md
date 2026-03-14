# Folder Restructure Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure project folders to remove numbered naming, create per-agent directories, and establish clear main work directories with mandatory initialization check.

**Architecture:** Replace numbered phase directories with semantic structure: main work directories (`paper/`, `code/`, `docs/`), agent workspaces (`agents/<role>/`), and hidden system directory (`.autoresearch/`). All scripts must validate structure on startup.

**Tech Stack:** Python 3.10+, PyYAML, unittest

---

## File Structure

### Files to Modify

| File | Changes |
|------|---------|
| `scripts/orchestrator_common.py` | Update all constants: PHASE_DIRECTORIES → new structure, DEFAULT_DELIVERABLES paths, add ensure_project_structure() |
| `scripts/init_research_project.py` | Create new directory structure, add structure validation |
| `scripts/materialize_templates.py` | Update template path rendering |
| `scripts/generate_dashboard.py` | Update dashboard paths |
| `scripts/quality_gate.py` | Update deliverable paths |
| `scripts/validate_handoff.py` | Update phase handoff paths |
| `scripts/run_stage_loop.py` | Update phase references |
| `scripts/pivot_manager.py` | Update archive path |
| `scripts/sentinel.py` | Update runtime paths |
| `scripts/recover_stage.py` | Update phase paths |
| `scripts/run_citation_audit.py` | Update paper path |
| `scripts/phase_handoff.py` | Update phase paths |
| `scripts/render_agent_prompt.py` | Update template paths |
| `scripts/generate_statusline.py` | Update status paths |

### Files to Create

| File | Purpose |
|------|---------|
| `scripts/migrate_structure.py` | Migration script for existing projects |
| `scripts/ensure_structure.py` | Standalone structure validation utility |
| `tests/test_folder_structure.py` | Tests for new structure |

### Templates to Update

All templates in `assets/templates/` need path updates:
- `00-admin/*` → `.autoresearch/*`
- `01-survey/*` → `agents/survey/`, `docs/reports/survey/`
- `02-pilot-analysis/*` → `agents/coder/`, `docs/reports/pilot/`
- `03-full-experiments/*` → `code/`, `docs/reports/experiments/`
- `04-paper/*` → `paper/`, `agents/writer/`, `agents/reviewer/`
- `05-reflection-evolution/*` → `agents/reflector/`, `docs/reports/reflection/`
- `06-archive/*` → `.autoresearch/archive/`

---

## Chunk 1: Core Constants Update

### Task 1: Update orchestrator_common.py Constants

**Files:**
- Modify: `scripts/orchestrator_common.py:40-300`
- Test: `tests/test_folder_structure.py`

- [ ] **Step 1: Write the failing test for new constants**

```python
# tests/test_folder_structure.py
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from orchestrator_common import (
    MAIN_DIRECTORIES,
    AGENT_DIRECTORIES,
    SYSTEM_DIRECTORIES,
    REQUIRED_DIRECTORIES,
    DEFAULT_DELIVERABLES,
)


class TestNewFolderConstants(unittest.TestCase):
    def test_main_directories_exist(self):
        """Main work directories should be defined."""
        self.assertIn("paper", MAIN_DIRECTORIES)
        self.assertIn("code", MAIN_DIRECTORIES)
        self.assertIn("docs", MAIN_DIRECTORIES)
        self.assertEqual(len(MAIN_DIRECTORIES), 3)

    def test_agent_directories_exist(self):
        """Agent directories should include all roles."""
        expected_agents = ["survey", "critic", "coder", "adviser", "writer", "reviewer", "reflector", "curator"]
        for agent in expected_agents:
            self.assertIn(f"agents/{agent}", AGENT_DIRECTORIES)
        self.assertEqual(len(AGENT_DIRECTORIES), 8)

    def test_system_directories_exist(self):
        """System directories should be hidden under .autoresearch."""
        expected_system = ["state", "config", "dashboard", "runtime", "reference-papers", "templates", "archive"]
        for sys_dir in expected_system:
            self.assertIn(f".autoresearch/{sys_dir}", SYSTEM_DIRECTORIES)
        self.assertEqual(len(SYSTEM_DIRECTORIES), 7)

    def test_required_directories_combines_all(self):
        """REQUIRED_DIRECTORIES should combine main, agent, and system."""
        self.assertEqual(len(REQUIRED_DIRECTORIES), len(MAIN_DIRECTORIES) + len(AGENT_DIRECTORIES) + len(SYSTEM_DIRECTORIES))

    def test_deliverables_use_new_paths(self):
        """All deliverable paths should use new structure."""
        # State files should be under .autoresearch/state/
        self.assertTrue(DEFAULT_DELIVERABLES["research_state"].startswith(".autoresearch/state/"))
        # Paper files should be under paper/
        self.assertTrue(DEFAULT_DELIVERABLES["paper_draft"].startswith("paper/"))
        # Code files should be under code/
        self.assertTrue(DEFAULT_DELIVERABLES["experiment_spec"].startswith("code/"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /mnt/e/workspace/Autoresearch/ai-research-orchestrator && python3 -m unittest tests.test_folder_structure -v`
Expected: FAIL with "cannot import name 'MAIN_DIRECTORIES'"

- [ ] **Step 3: Update constants in orchestrator_common.py**

Replace the PHASE_DIRECTORIES and related constants:

```python
# In orchestrator_common.py, after line 49 (after PHASE_DIRECTORIES definition)

# New folder structure constants (v2.0.0)
# Main work directories - user-facing outputs
MAIN_DIRECTORIES = ("paper", "code", "docs")

# Agent directories - per-agent workspaces
AGENT_DIRECTORIES = (
    "agents/survey",
    "agents/critic",
    "agents/coder",
    "agents/adviser",
    "agents/writer",
    "agents/reviewer",
    "agents/reflector",
    "agents/curator",
)

# System directories - hidden under .autoresearch
SYSTEM_DIRECTORIES = (
    ".autoresearch/state",
    ".autoresearch/config",
    ".autoresearch/dashboard",
    ".autoresearch/runtime",
    ".autoresearch/reference-papers",
    ".autoresearch/templates",
    ".autoresearch/archive",
)

# All required directories combined
REQUIRED_DIRECTORIES = MAIN_DIRECTORIES + AGENT_DIRECTORIES + SYSTEM_DIRECTORIES

# Legacy alias for backward compatibility during migration
PHASE_DIRECTORIES = (
    "00-admin",  # Maps to .autoresearch/
    "01-survey",  # Maps to agents/survey/ + docs/reports/survey/
    "02-pilot-analysis",  # Maps to agents/coder/ + docs/reports/pilot/
    "03-full-experiments",  # Maps to code/ + docs/reports/experiments/
    "04-paper",  # Maps to paper/
    "05-reflection-evolution",  # Maps to agents/reflector/ + docs/reports/reflection/
    "06-archive",  # Maps to .autoresearch/archive/
)

# Mapping from old paths to new paths for migration
OLD_TO_NEW_PATH_MAPPING = {
    "00-admin/": ".autoresearch/",
    "01-survey/": "agents/survey/",
    "02-pilot-analysis/": "agents/coder/",
    "03-full-experiments/": "code/",
    "04-paper/": "paper/",
    "05-reflection-evolution/": "agents/reflector/",
    "06-archive/": ".autoresearch/archive/",
}
```

- [ ] **Step 4: Update DEFAULT_DELIVERABLES paths**

Replace the entire DEFAULT_DELIVERABLES dictionary:

```python
DEFAULT_DELIVERABLES = {
    # State files
    "research_state": ".autoresearch/state/research-state.yaml",
    "review_state": ".autoresearch/state/REVIEW_STATE.json",
    "idea_state": ".autoresearch/state/IDEA_STATE.json",

    # Config
    "project_config": ".autoresearch/config/orchestrator-config.yaml",

    # Dashboard
    "dashboard_status": ".autoresearch/dashboard/status.json",
    "dashboard_progress": ".autoresearch/dashboard/progress.md",
    "dashboard_timeline": ".autoresearch/dashboard/timeline.ndjson",

    # Runtime
    "job_registry": ".autoresearch/runtime/job-registry.yaml",
    "gpu_registry": ".autoresearch/runtime/gpu-registry.yaml",
    "backend_registry": ".autoresearch/runtime/backend-registry.yaml",
    "sentinel_events": ".autoresearch/runtime/sentinel-events.ndjson",

    # Reference papers
    "reference_library_index": ".autoresearch/reference-papers/README.md",

    # Admin documents
    "idea_brief": ".autoresearch/idea-brief.md",
    "workspace_manifest": ".autoresearch/workspace-manifest.md",

    # Survey outputs
    "survey_round_log": "agents/survey/survey-round-summary.md",
    "critic_round_log": "agents/critic/critic-round-review.md",
    "readiness_report": "docs/reports/survey/research-readiness-report.md",
    "survey_scorecard": "docs/reports/survey/phase-scorecard.md",

    # Pilot outputs
    "problem_analysis": "docs/reports/pilot/problem-analysis.md",
    "pilot_plan": "docs/reports/pilot/pilot-experiment-plan.md",
    "pilot_results": "docs/reports/pilot/pilot-results.md",
    "pilot_adviser_review": "agents/adviser/pilot-review.md",
    "pilot_validation_report": "docs/reports/pilot/pilot-validation-report.md",
    "pilot_scorecard": "docs/reports/pilot/phase-scorecard.md",

    # Experiment outputs
    "experiment_spec": "code/configs/experiment-spec.yaml",
    "run_registry": "code/experiments/run-registry.md",
    "results_summary": "docs/reports/experiments/results-summary.md",
    "checkpoint_index": "code/checkpoints/checkpoint-index.md",
    "experiment_adviser_review": "agents/adviser/experiment-review.md",
    "evidence_package_index": "docs/reports/experiments/evidence-package-index.md",
    "experiment_scorecard": "docs/reports/experiments/phase-scorecard.md",

    # Paper outputs
    "paper_draft": "paper/main.tex",
    "citation_audit_report": "paper/citation-audit-report.md",
    "reviewer_report": "agents/reviewer/reviewer-report.md",
    "rebuttal_log": "paper/rebuttal-log.md",
    "final_acceptance_report": "docs/reports/paper/final-acceptance-report.md",
    "paper_scorecard": "docs/reports/paper/phase-scorecard.md",

    # Reflection outputs
    "lessons_learned": "docs/reports/reflection/lessons-learned.md",
    "overlay_draft": "agents/reflector/overlay-draft.md",
    "runtime_improvement_report": "docs/reports/reflection/runtime-improvement-report.md",
    "reflection_scorecard": "docs/reports/reflection/phase-scorecard.md",

    # Archive
    "archive_index": ".autoresearch/archive/archive-index.md",
}
```

- [ ] **Step 5: Update EXPECTED_DELIVERABLE_PREFIXES**

Replace the entire EXPECTED_DELIVERABLE_PREFIXES dictionary:

```python
EXPECTED_DELIVERABLE_PREFIXES = {
    # State files
    "research_state": ".autoresearch/state/",
    "review_state": ".autoresearch/state/",
    "idea_state": ".autoresearch/state/",

    # Config
    "project_config": ".autoresearch/config/",

    # Dashboard
    "dashboard_status": ".autoresearch/dashboard/",
    "dashboard_progress": ".autoresearch/dashboard/",
    "dashboard_timeline": ".autoresearch/dashboard/",

    # Runtime
    "job_registry": ".autoresearch/runtime/",
    "gpu_registry": ".autoresearch/runtime/",
    "backend_registry": ".autoresearch/runtime/",
    "sentinel_events": ".autoresearch/runtime/",

    # Reference papers
    "reference_library_index": ".autoresearch/reference-papers/",

    # Admin
    "idea_brief": ".autoresearch/",
    "workspace_manifest": ".autoresearch/",

    # Survey
    "survey_round_log": "agents/survey/",
    "critic_round_log": "agents/critic/",
    "readiness_report": "docs/reports/survey/",
    "survey_scorecard": "docs/reports/survey/",

    # Pilot
    "problem_analysis": "docs/reports/pilot/",
    "pilot_plan": "docs/reports/pilot/",
    "pilot_results": "docs/reports/pilot/",
    "pilot_adviser_review": "agents/adviser/",
    "pilot_validation_report": "docs/reports/pilot/",
    "pilot_scorecard": "docs/reports/pilot/",

    # Experiments
    "experiment_spec": "code/configs/",
    "run_registry": "code/experiments/",
    "results_summary": "docs/reports/experiments/",
    "checkpoint_index": "code/checkpoints/",
    "experiment_adviser_review": "agents/adviser/",
    "evidence_package_index": "docs/reports/experiments/",
    "experiment_scorecard": "docs/reports/experiments/",

    # Paper
    "paper_draft": "paper/",
    "citation_audit_report": "paper/",
    "reviewer_report": "agents/reviewer/",
    "rebuttal_log": "paper/",
    "final_acceptance_report": "docs/reports/paper/",
    "paper_scorecard": "docs/reports/paper/",

    # Reflection
    "lessons_learned": "docs/reports/reflection/",
    "overlay_draft": "agents/reflector/",
    "runtime_improvement_report": "docs/reports/reflection/",
    "reflection_scorecard": "docs/reports/reflection/",

    # Archive
    "archive_index": ".autoresearch/archive/",
}
```

- [ ] **Step 6: Update HANDOFF_REQUIREMENTS next_phase values**

```python
HANDOFF_REQUIREMENTS = {
    "survey-to-pilot": {
        "statuses": (
            ("phase_reviews", "survey_critic"),
            ("approval_status", "gate_1"),
        ),
        "deliverables": ("readiness_report", "survey_scorecard"),
        "next_phase": "pilot",  # Changed from "02-pilot-analysis"
    },
    "pilot-to-experiments": {
        "statuses": (
            ("phase_reviews", "pilot_adviser"),
            ("approval_status", "gate_2"),
        ),
        "deliverables": (
            "problem_analysis",
            "pilot_plan",
            "pilot_results",
            "pilot_adviser_review",
            "pilot_validation_report",
            "pilot_scorecard",
        ),
        "next_phase": "experiments",  # Changed from "03-full-experiments"
    },
    "experiments-to-paper": {
        "statuses": (
            ("phase_reviews", "experiment_adviser"),
            ("approval_status", "gate_3"),
        ),
        "deliverables": (
            "experiment_spec",
            "run_registry",
            "results_summary",
            "checkpoint_index",
            "experiment_adviser_review",
            "evidence_package_index",
            "experiment_scorecard",
        ),
        "next_phase": "paper",  # Changed from "04-paper"
    },
    "paper-to-reflection": {
        "statuses": (
            ("phase_reviews", "paper_reviewer"),
            ("approval_status", "gate_4"),
        ),
        "deliverables": (
            "paper_draft",
            "citation_audit_report",
            "reviewer_report",
            "rebuttal_log",
            "final_acceptance_report",
            "paper_scorecard",
        ),
        "next_phase": "reflection",  # Changed from "05-reflection-evolution"
    },
    "reflection-closeout": {
        "statuses": (
            ("phase_reviews", "reflection_curator"),
            ("approval_status", "gate_5"),
        ),
        "deliverables": (
            "lessons_learned",
            "overlay_draft",
            "runtime_improvement_report",
            "reflection_scorecard",
        ),
        "next_phase": "handoff-user",
    },
}
```

- [ ] **Step 7: Update PHASE_TO_GATE and NEXT_PHASE**

```python
# New phase names (semantic, not numbered)
PHASE_TO_GATE = {
    "survey": "gate_1",
    "pilot": "gate_2",
    "experiments": "gate_3",
    "paper": "gate_4",
    "reflection": "gate_5",
}

# Legacy mapping for backward compatibility
PHASE_TO_GATE_LEGACY = {
    "01-survey": "gate_1",
    "02-pilot-analysis": "gate_2",
    "03-full-experiments": "gate_3",
    "04-paper": "gate_4",
    "05-reflection-evolution": "gate_5",
}

NEXT_PHASE = {
    "survey": "pilot",
    "pilot": "experiments",
    "experiments": "paper",
    "paper": "reflection",
    "reflection": "archive",
}

# Legacy mapping
NEXT_PHASE_LEGACY = {
    "01-survey": "02-pilot-analysis",
    "02-pilot-analysis": "03-full-experiments",
    "03-full-experiments": "04-paper",
    "04-paper": "05-reflection-evolution",
    "05-reflection-evolution": "06-archive",
}
```

- [ ] **Step 8: Run tests to verify constants pass**

Run: `cd /mnt/e/workspace/Autoresearch/ai-research-orchestrator && python3 -m unittest tests.test_folder_structure -v`
Expected: PASS

- [ ] **Step 9: Commit constants update**

```bash
git add scripts/orchestrator_common.py tests/test_folder_structure.py
git commit -m "refactor: update folder constants for new structure (v2.0.0)

- Add MAIN_DIRECTORIES, AGENT_DIRECTORIES, SYSTEM_DIRECTORIES
- Update DEFAULT_DELIVERABLES to use new paths
- Update EXPECTED_DELIVERABLE_PREFIXES
- Update HANDOFF_REQUIREMENTS, PHASE_TO_GATE, NEXT_PHASE
- Add legacy mappings for backward compatibility
- Add test for new constants"
```

---

## Chunk 2: Structure Validation Function

### Task 2: Add ensure_project_structure Function

**Files:**
- Modify: `scripts/orchestrator_common.py`
- Test: `tests/test_folder_structure.py`

- [ ] **Step 1: Add test for ensure_project_structure**

```python
# Add to tests/test_folder_structure.py

class TestEnsureProjectStructure(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_returns_true_for_valid_structure(self):
        """Should return True when all directories exist."""
        from orchestrator_common import ensure_project_structure, REQUIRED_DIRECTORIES

        # Create all required directories
        for dir_path in REQUIRED_DIRECTORIES:
            (self.project_root / dir_path).mkdir(parents=True, exist_ok=True)

        result = ensure_project_structure(self.project_root)
        self.assertTrue(result)

    def test_creates_missing_directories(self):
        """Should create missing directories when they don't exist."""
        from orchestrator_common import ensure_project_structure, REQUIRED_DIRECTORIES

        # Create only some directories
        (self.project_root / "paper").mkdir()
        (self.project_root / "code").mkdir()

        result = ensure_project_structure(self.project_root)

        self.assertTrue(result)
        for dir_path in REQUIRED_DIRECTORIES:
            self.assertTrue((self.project_root / dir_path).exists())

    def test_returns_false_for_empty_project(self):
        """Should return False for empty project without state file."""
        from orchestrator_common import ensure_project_structure

        result = ensure_project_structure(self.project_root, create_if_missing=False)
        self.assertFalse(result)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /mnt/e/workspace/Autoresearch/ai-research-orchestrator && python3 -m unittest tests.test_folder_structure.TestEnsureProjectStructure -v`
Expected: FAIL with "cannot import name 'ensure_project_structure'"

- [ ] **Step 3: Implement ensure_project_structure function**

```python
# Add to orchestrator_common.py (after the constants section)

def ensure_project_structure(project_root: Path, create_if_missing: bool = True) -> bool:
    """
    Ensure project directory structure is valid.

    This function checks and optionally creates the required directory structure.
    Every script should call this at startup to guarantee consistent structure.

    Args:
        project_root: Path to the project root directory
        create_if_missing: If True, create missing directories automatically

    Returns:
        True if structure is valid (all directories exist)
        False if structure is invalid and create_if_missing is False

    Raises:
        ValueError: If project_root is not a valid directory
    """
    project_root = Path(project_root).resolve()

    if not project_root.exists():
        if create_if_missing:
            project_root.mkdir(parents=True, exist_ok=True)
        else:
            return False

    missing_dirs = []
    for dir_path in REQUIRED_DIRECTORIES:
        full_path = project_root / dir_path
        if not full_path.exists():
            if create_if_missing:
                full_path.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Created directory: {dir_path}")
            else:
                missing_dirs.append(dir_path)

    if missing_dirs:
        logger.warning(f"Missing directories: {missing_dirs}")
        return False

    # Check state file exists
    state_path = project_root / DEFAULT_DELIVERABLES["research_state"]
    if not state_path.exists():
        logger.info(f"State file not found: {state_path}")
        # Still return True if directories exist, just log the info
        # State file will be created by init_research_project

    return True
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /mnt/e/workspace/Autoresearch/ai-research-orchestrator && python3 -m unittest tests.test_folder_structure.TestEnsureProjectStructure -v`
Expected: PASS

- [ ] **Step 5: Commit structure validation**

```bash
git add scripts/orchestrator_common.py tests/test_folder_structure.py
git commit -m "feat: add ensure_project_structure() for directory validation

- Validates all required directories exist
- Optionally creates missing directories
- Logs warnings for missing items
- To be called at startup of all scripts"
```

---

## Chunk 3: Update Initialization Script

### Task 3: Update init_research_project.py

**Files:**
- Modify: `scripts/init_research_project.py`
- Test: `tests/test_init_research_project.py`

- [ ] **Step 1: Update imports in init_research_project.py**

```python
# Update imports at the top of init_research_project.py
from orchestrator_common import (
    DEFAULT_DELIVERABLES,
    DEFAULT_LANGUAGE_POLICY,
    MAIN_DIRECTORIES,
    AGENT_DIRECTORIES,
    SYSTEM_DIRECTORIES,
    REQUIRED_DIRECTORIES,
    PHASE_TO_GATE,
    ensure_project_structure,
    build_client_instruction_text,
    build_state,
    build_template_variables,
    detect_client_profile,
    detect_client_init_artifacts,
    normalize_relative_path,
    render_template_tree,
    slugify,
    write_text_if_needed,
    write_yaml,
)
```

- [ ] **Step 2: Update VALID_PHASES constant**

```python
# Replace VALID_PHASES with new phase names
VALID_PHASES = ["survey", "pilot", "experiments", "paper", "reflection"]

# Legacy phases for backward compatibility
VALID_PHASES_LEGACY = ["01-survey", "02-pilot-analysis", "03-full-experiments", "04-paper", "05-reflection-evolution"]
```

- [ ] **Step 3: Update initialize_research_project function**

```python
def initialize_research_project(
    project_root: Path,
    topic: str,
    project_id: str | None = None,
    client_type: str = "auto",
    process_language: str = DEFAULT_LANGUAGE_POLICY["process_docs"],
    paper_language: str = DEFAULT_LANGUAGE_POLICY["paper_docs"],
    overwrite_templates: bool = False,
    explicit_init_paths: list[str] | None = None,
    starting_phase: str = "survey",  # Changed from "01-survey"
) -> dict[str, object]:
    project_root = project_root.resolve()
    project_root.mkdir(parents=True, exist_ok=True)

    # Ensure directory structure using new function
    ensure_project_structure(project_root, create_if_missing=True)

    # Create subdirectories for main work directories
    (project_root / "paper" / "sections").mkdir(parents=True, exist_ok=True)
    (project_root / "paper" / "figures").mkdir(parents=True, exist_ok=True)
    (project_root / "code" / "src").mkdir(parents=True, exist_ok=True)
    (project_root / "code" / "experiments").mkdir(parents=True, exist_ok=True)
    (project_root / "code" / "configs").mkdir(parents=True, exist_ok=True)
    (project_root / "code" / "checkpoints").mkdir(parents=True, exist_ok=True)
    (project_root / "docs" / "reports" / "survey").mkdir(parents=True, exist_ok=True)
    (project_root / "docs" / "reports" / "pilot").mkdir(parents=True, exist_ok=True)
    (project_root / "docs" / "reports" / "experiments").mkdir(parents=True, exist_ok=True)
    (project_root / "docs" / "reports" / "paper").mkdir(parents=True, exist_ok=True)
    (project_root / "docs" / "reports" / "reflection").mkdir(parents=True, exist_ok=True)

    # ... rest of the function stays the same ...
```

- [ ] **Step 4: Update build_parser function**

```python
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Initialize a gated AI research workspace.")
    parser.add_argument("--project-root", required=True, help="Path to the target research project root.")
    parser.add_argument("--topic", default="TODO: replace with the research idea or problem statement")
    parser.add_argument("--project-id", help="Optional stable project id. Defaults to the project directory slug.")
    parser.add_argument(
        "--client-type",
        default="auto",
        choices=("auto", "codex", "claude"),
        help="Generate the client instruction file for Codex (AGENTS.md) or Claude (CLAUDE.md).",
    )
    parser.add_argument("--process-language", default=DEFAULT_LANGUAGE_POLICY["process_docs"])
    parser.add_argument("--paper-language", default=DEFAULT_LANGUAGE_POLICY["paper_docs"])
    parser.add_argument("--overwrite-templates", action="store_true", help="Rewrite existing template files.")
    parser.add_argument(
        "--client-init-path",
        action="append",
        dest="client_init_paths",
        help="Explicit client /init artifact path relative to the project root. Repeat as needed.",
    )
    parser.add_argument(
        "--starting-phase",
        default="survey",  # Changed from "01-survey"
        choices=VALID_PHASES + VALID_PHASES_LEGACY,  # Support both new and legacy
        help="Phase to start the project at. Use for resuming work or skipping completed phases.",
    )
    parser.add_argument("--json", action="store_true", help="Print a JSON summary.")
    return parser
```

- [ ] **Step 5: Add phase name normalization**

```python
def normalize_phase_name(phase: str) -> str:
    """Convert legacy phase names to new semantic names."""
    legacy_to_new = {
        "01-survey": "survey",
        "02-pilot-analysis": "pilot",
        "03-full-experiments": "experiments",
        "04-paper": "paper",
        "05-reflection-evolution": "reflection",
    }
    return legacy_to_new.get(phase, phase)
```

- [ ] **Step 6: Update main function**

```python
def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # Normalize phase name (support legacy names)
    starting_phase = normalize_phase_name(args.starting_phase)

    result = initialize_research_project(
        project_root=Path(args.project_root),
        topic=args.topic,
        project_id=args.project_id,
        client_type=args.client_type,
        process_language=args.process_language,
        paper_language=args.paper_language,
        overwrite_templates=args.overwrite_templates,
        explicit_init_paths=args.client_init_paths,
        starting_phase=starting_phase,
    )
    # ... rest of main function ...
```

- [ ] **Step 7: Run existing tests**

Run: `cd /mnt/e/workspace/Autoresearch/ai-research-orchestrator && python3 -m unittest tests.test_init_research_project -v`
Expected: Some tests may fail, need to update them

- [ ] **Step 8: Update test_init_research_project.py**

Update any tests that reference old phase names:

```python
# Replace "01-survey" with "survey" in tests
# Replace "02-pilot-analysis" with "pilot"
# etc.
```

- [ ] **Step 9: Run tests again**

Run: `cd /mnt/e/workspace/Autoresearch/ai-research-orchestrator && python3 -m unittest tests.test_init_research_project -v`
Expected: PASS

- [ ] **Step 10: Commit init script update**

```bash
git add scripts/init_research_project.py tests/test_init_research_project.py
git commit -m "refactor: update init_research_project for new folder structure

- Use ensure_project_structure() for directory creation
- Support both new and legacy phase names
- Create subdirectories for main work areas
- Add normalize_phase_name() helper"
```

---

## Chunk 4: Update Template Structure

### Task 4: Reorganize Template Directory

**Files:**
- Create: `assets/templates/.autoresearch/*`
- Create: `assets/templates/paper/*`
- Create: `assets/templates/code/*`
- Create: `assets/templates/docs/*`
- Create: `assets/templates/agents/*`
- Delete: `assets/templates/00-admin/*` (after migration)
- Delete: `assets/templates/01-survey/*` (after migration)
- etc.

- [ ] **Step 1: Create new template directory structure**

```bash
cd /mnt/e/workspace/Autoresearch/ai-research-orchestrator/assets/templates
mkdir -p .autoresearch/state .autoresearch/config .autoresearch/dashboard .autoresearch/runtime .autoresearch/reference-papers .autoresearch/archive
mkdir -p paper/sections paper/figures
mkdir -p code/src code/experiments code/configs code/checkpoints
mkdir -p docs/reports/survey docs/reports/pilot docs/reports/experiments docs/reports/paper docs/reports/reflection
mkdir -p agents/survey agents/critic agents/coder agents/adviser agents/writer agents/reviewer agents/reflector agents/curator
```

- [ ] **Step 2: Move admin templates to .autoresearch**

```bash
# Move templates from 00-admin to .autoresearch
mv 00-admin/*.tmpl .autoresearch/ 2>/dev/null || true
mv 00-admin/dashboard/*.tmpl .autoresearch/dashboard/ 2>/dev/null || true
mv 00-admin/runtime/*.tmpl .autoresearch/runtime/ 2>/dev/null || true
mv 00-admin/reference-papers/*.tmpl .autoresearch/reference-papers/ 2>/dev/null || true
```

- [ ] **Step 3: Move phase templates to appropriate locations**

```bash
# Survey templates
mv 01-survey/*.tmpl docs/reports/survey/ 2>/dev/null || true

# Pilot templates
mv 02-pilot-analysis/*.tmpl docs/reports/pilot/ 2>/dev/null || true

# Experiment templates
mv 03-full-experiments/*.tmpl docs/reports/experiments/ 2>/dev/null || true
mv 03-full-experiments/checkpoints/*.tmpl code/checkpoints/ 2>/dev/null || true

# Paper templates
mv 04-paper/*.tmpl paper/ 2>/dev/null || true

# Reflection templates
mv 05-reflection-evolution/*.tmpl docs/reports/reflection/ 2>/dev/null || true

# Archive templates
mv 06-archive/*.tmpl .autoresearch/archive/ 2>/dev/null || true
```

- [ ] **Step 4: Remove old template directories**

```bash
rm -rf 00-admin 01-survey 02-pilot-analysis 03-full-experiments 04-paper 05-reflection-evolution 06-archive
```

- [ ] **Step 5: Update template paths in scripts**

Update `materialize_templates.py` to use new template paths:

```python
# Update TEMPLATE_ROOT structure references
# The template directory structure now mirrors the project structure
```

- [ ] **Step 6: Commit template reorganization**

```bash
git add assets/templates/
git commit -m "refactor: reorganize templates to match new folder structure

- Move admin templates to .autoresearch/
- Move phase templates to docs/reports/<phase>/
- Move paper templates to paper/
- Move experiment templates to code/
- Remove old numbered directories"
```

---

## Chunk 5: Update Supporting Scripts

### Task 5: Update quality_gate.py

**Files:**
- Modify: `scripts/quality_gate.py`
- Test: `tests/test_quality_gate.py`

- [ ] **Step 1: Update imports**

```python
from orchestrator_common import (
    DEFAULT_DELIVERABLES,
    EXPECTED_DELIVERABLE_PREFIXES,
    PHASE_REQUIRED_DELIVERABLES,
    PHASE_TO_GATE,
    load_state,
    save_state,
    ensure_project_structure,  # Add this
)
```

- [ ] **Step 2: Add ensure_project_structure call**

```python
def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()

    # Ensure project structure before proceeding
    ensure_project_structure(project_root, create_if_missing=False)

    # ... rest of function
```

- [ ] **Step 3: Update phase names in PHASE_REQUIRED_DELIVERABLES**

```python
# Update this constant in orchestrator_common.py
PHASE_REQUIRED_DELIVERABLES = {
    "survey": ["readiness_report", "survey_scorecard"],
    "pilot": ["problem_analysis", "pilot_plan", "pilot_validation_report", "pilot_scorecard"],
    "experiments": ["experiment_spec", "results_summary", "evidence_package_index", "experiment_scorecard"],
    "paper": ["paper_draft", "citation_audit_report", "final_acceptance_report", "paper_scorecard"],
    "reflection": ["lessons_learned", "runtime_improvement_report", "reflection_scorecard"],
}
```

- [ ] **Step 4: Commit changes**

```bash
git add scripts/quality_gate.py scripts/orchestrator_common.py
git commit -m "refactor: update quality_gate.py for new folder structure"
```

### Task 6: Update validate_handoff.py

**Files:**
- Modify: `scripts/validate_handoff.py`

- [ ] **Step 1: Add ensure_project_structure call**

```python
def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()

    # Ensure project structure
    ensure_project_structure(project_root, create_if_missing=False)

    # ... rest of function
```

- [ ] **Step 2: Update handoff target names**

The HANDOFF_REQUIREMENTS constant already has updated next_phase values from Chunk 1.

- [ ] **Step 3: Commit changes**

```bash
git add scripts/validate_handoff.py
git commit -m "refactor: update validate_handoff.py for new folder structure"
```

### Task 7: Update Other Scripts

For each remaining script, add the ensure_project_structure call at the start of main():

- `run_stage_loop.py`
- `pivot_manager.py`
- `sentinel.py`
- `recover_stage.py`
- `run_citation_audit.py`
- `phase_handoff.py`
- `render_agent_prompt.py`
- `generate_statusline.py`
- `generate_dashboard.py`
- `materialize_templates.py`

- [ ] **Step 1: Update all scripts with ensure_project_structure call**

Pattern for each script:

```python
def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()

    # Ensure project structure
    ensure_project_structure(project_root, create_if_missing=False)

    # ... rest of function
```

- [ ] **Step 2: Commit changes**

```bash
git add scripts/*.py
git commit -m "refactor: add ensure_project_structure call to all scripts

Ensures directory structure is valid before any operation"
```

---

## Chunk 6: Create Migration Script

### Task 8: Create migrate_structure.py

**Files:**
- Create: `scripts/migrate_structure.py`
- Test: `tests/test_folder_structure.py`

- [ ] **Step 1: Write migration script**

```python
#!/usr/bin/env python3
"""Migrate existing project from old numbered structure to new semantic structure.

Usage:
    python3 scripts/migrate_structure.py --project-root /path/to/project [--dry-run]
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

# Add scripts directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

from orchestrator_common import (
    OLD_TO_NEW_PATH_MAPPING,
    DEFAULT_DELIVERABLES,
    REQUIRED_DIRECTORIES,
    ensure_project_structure,
    load_state,
    save_state,
)


def migrate_project(project_root: Path, dry_run: bool = False, backup: bool = True) -> dict:
    """
    Migrate a project from old numbered structure to new semantic structure.

    Args:
        project_root: Path to the project root
        dry_run: If True, only print what would be done without making changes
        backup: If True, create a backup of old directories before migration

    Returns:
        Dictionary with migration results
    """
    project_root = project_root.resolve()
    results = {
        "project_root": str(project_root),
        "dry_run": dry_run,
        "migrated_files": [],
        "migrated_dirs": [],
        "errors": [],
    }

    # Check if project has old structure
    has_old_structure = any(
        (project_root / old_dir).exists()
        for old_dir in ["00-admin", "01-survey", "02-pilot-analysis", "03-full-experiments", "04-paper", "05-reflection-evolution", "06-archive"]
    )

    if not has_old_structure:
        results["message"] = "No old structure detected, project may already be migrated"
        return results

    # Create backup if requested
    if backup and not dry_run:
        backup_dir = project_root / ".autoresearch" / "migration_backup"
        backup_dir.mkdir(parents=True, exist_ok=True)
        for old_dir in ["00-admin", "01-survey", "02-pilot-analysis", "03-full-experiments", "04-paper", "05-reflection-evolution", "06-archive"]:
            old_path = project_root / old_dir
            if old_path.exists():
                shutil.copytree(old_path, backup_dir / old_dir, dirs_exist_ok=True)
        results["backup_path"] = str(backup_dir)

    # Create new directory structure
    if not dry_run:
        ensure_project_structure(project_root, create_if_missing=True)

    # Migrate files
    file_mappings = [
        # State files
        ("00-admin/research-state.yaml", ".autoresearch/state/research-state.yaml"),
        ("00-admin/orchestrator-config.yaml", ".autoresearch/config/orchestrator-config.yaml"),
        ("00-admin/idea-brief.md", ".autoresearch/idea-brief.md"),
        ("00-admin/workspace-manifest.md", ".autoresearch/workspace-manifest.md"),
        # Dashboard files
        ("00-admin/dashboard/status.json", ".autoresearch/dashboard/status.json"),
        ("00-admin/dashboard/progress.md", ".autoresearch/dashboard/progress.md"),
        ("00-admin/dashboard/timeline.ndjson", ".autoresearch/dashboard/timeline.ndjson"),
        # Runtime files
        ("00-admin/runtime/job-registry.yaml", ".autoresearch/runtime/job-registry.yaml"),
        ("00-admin/runtime/gpu-registry.yaml", ".autoresearch/runtime/gpu-registry.yaml"),
        ("00-admin/runtime/backend-registry.yaml", ".autoresearch/runtime/backend-registry.yaml"),
        ("00-admin/runtime/sentinel-events.ndjson", ".autoresearch/runtime/sentinel-events.ndjson"),
        # Reference papers
        ("00-admin/reference-papers/", ".autoresearch/reference-papers/"),
        # Survey files
        ("01-survey/", "docs/reports/survey/"),
        # Pilot files
        ("02-pilot-analysis/", "docs/reports/pilot/"),
        # Experiment files
        ("03-full-experiments/", "docs/reports/experiments/"),
        # Paper files
        ("04-paper/", "paper/"),
        # Reflection files
        ("05-reflection-evolution/", "docs/reports/reflection/"),
        # Archive
        ("06-archive/", ".autoresearch/archive/"),
    ]

    for old_path, new_path in file_mappings:
        src = project_root / old_path
        dst = project_root / new_path

        if src.exists():
            if dry_run:
                print(f"Would migrate: {old_path} -> {new_path}")
                results["migrated_files"].append((old_path, new_path))
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                if src.is_dir():
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                    results["migrated_dirs"].append((old_path, new_path))
                else:
                    shutil.copy2(src, dst)
                    results["migrated_files"].append((old_path, new_path))

    # Update state file with new paths
    if not dry_run:
        state_path = project_root / ".autoresearch/state/research-state.yaml"
        if state_path.exists():
            state = load_state(project_root)
            # Update current_phase if it uses old format
            if state.get("current_phase", "").startswith("0"):
                old_phase = state["current_phase"]
                new_phase = old_phase.split("-", 1)[-1] if "-" in old_phase else old_phase
                if new_phase == "pilot-analysis":
                    new_phase = "pilot"
                elif new_phase == "full-experiments":
                    new_phase = "experiments"
                elif new_phase == "reflection-evolution":
                    new_phase = "reflection"
                state["current_phase"] = new_phase
                save_state(project_root, state)
                results["state_updated"] = True

    # Remove old directories if not dry run
    if not dry_run:
        for old_dir in ["00-admin", "01-survey", "02-pilot-analysis", "03-full-experiments", "04-paper", "05-reflection-evolution", "06-archive"]:
            old_path = project_root / old_dir
            if old_path.exists():
                shutil.rmtree(old_path)
                results["removed_dirs"].append(old_dir)

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate project to new folder structure.")
    parser.add_argument("--project-root", required=True, help="Path to project root")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--no-backup", action="store_true", help="Skip creating backup before migration")
    args = parser.parse_args()

    results = migrate_project(
        Path(args.project_root),
        dry_run=args.dry_run,
        backup=not args.no_backup,
    )

    print(f"Migration results for: {results['project_root']}")
    if results.get("message"):
        print(f"  {results['message']}")
    else:
        print(f"  Files migrated: {len(results['migrated_files'])}")
        print(f"  Directories migrated: {len(results['migrated_dirs'])}")
        if results.get("backup_path"):
            print(f"  Backup created: {results['backup_path']}")
        if results.get("errors"):
            print(f"  Errors: {results['errors']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Add test for migration script**

```python
# Add to tests/test_folder_structure.py

class TestMigrationScript(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_migrate_from_old_structure(self):
        """Should migrate old numbered structure to new semantic structure."""
        # Create old structure
        (self.project_root / "00-admin").mkdir()
        (self.project_root / "01-survey").mkdir()
        (self.project_root / "04-paper").mkdir()

        # Create a test file
        (self.project_root / "00-admin" / "test.txt").write_text("test content")

        # Run migration (dry run first)
        from orchestrator_common import ensure_project_structure
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

        # Now run actual migration
        import migrate_structure
        results = migrate_structure.migrate_project(self.project_root, dry_run=True)

        self.assertIn("migrated_files", results)
```

- [ ] **Step 3: Run tests**

Run: `cd /mnt/e/workspace/Autoresearch/ai-research-orchestrator && python3 -m unittest tests.test_folder_structure -v`
Expected: PASS

- [ ] **Step 4: Commit migration script**

```bash
git add scripts/migrate_structure.py tests/test_folder_structure.py
git commit -m "feat: add migration script for folder restructure

- Supports dry-run mode
- Creates backup by default
- Updates state file phase names
- Removes old directories after migration"
```

---

## Chunk 7: Update Documentation

### Task 9: Update SKILL.md and References

**Files:**
- Modify: `SKILL.md`
- Modify: `references/workflow-protocol.md`
- Modify: `references/phase-execution-details.md`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Update SKILL.md Quick Start section**

Update the directory references in SKILL.md to use new structure.

- [ ] **Step 2: Update workflow-protocol.md**

Update phase names from numbered to semantic.

- [ ] **Step 3: Update CLAUDE.md**

Update the core architecture section with new directory structure.

- [ ] **Step 4: Commit documentation updates**

```bash
git add SKILL.md references/*.md CLAUDE.md
git commit -m "docs: update documentation for new folder structure"
```

---

## Chunk 8: Final Verification

### Task 10: Run All Tests and Verify

- [ ] **Step 1: Run all tests**

Run: `cd /mnt/e/workspace/Autoresearch/ai-research-orchestrator && python3 -m unittest discover -s tests`
Expected: All tests PASS

- [ ] **Step 2: Test migration on sample project**

```bash
# Create a test project with old structure
mkdir -p /tmp/test-old-project/00-admin /tmp/test-old-project/01-survey

# Run migration
cd /mnt/e/workspace/Autoresearch/ai-research-orchestrator
python3 scripts/migrate_structure.py --project-root /tmp/test-old-project --dry-run

# Run actual migration
python3 scripts/migrate_structure.py --project-root /tmp/test-old-project

# Verify new structure exists
ls -la /tmp/test-old-project/
```

- [ ] **Step 3: Test new project initialization**

```bash
python3 scripts/init_research_project.py \
  --project-root /tmp/test-new-project \
  --topic "Test research topic" \
  --json

# Verify structure
ls -la /tmp/test-new-project/
```

- [ ] **Step 4: Update version number**

Update SYSTEM_VERSION to "2.0.0" in orchestrator_common.py and add version history entry.

- [ ] **Step 5: Final commit**

```bash
git add scripts/orchestrator_common.py CHANGELOG.md
git commit -m "release: v2.0.0 - new folder structure

Breaking change: Restructured project directories

- Removed numbered phase directories
- Added main work directories: paper/, code/, docs/
- Added per-agent directories: agents/<role>/
- Added hidden system directory: .autoresearch/
- Added mandatory structure validation
- Added migration script for existing projects"
```

---

## Summary

This plan restructures the project from numbered phase directories to a semantic, agent-centric structure. Key changes:

1. **Constants**: New `MAIN_DIRECTORIES`, `AGENT_DIRECTORIES`, `SYSTEM_DIRECTORIES`
2. **Validation**: `ensure_project_structure()` called at startup
3. **Paths**: All deliverables use new paths
4. **Migration**: `migrate_structure.py` for existing projects
5. **Backward Compatibility**: Legacy phase names supported via `normalize_phase_name()`