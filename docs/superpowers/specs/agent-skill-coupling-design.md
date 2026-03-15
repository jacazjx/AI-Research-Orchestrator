# Agent-Skill Coupling Design

## Overview

This document specifies the architecture for coupling Agents with Skills in the AI-Research-Orchestrator project. The core principle is that each phase contains multiple substeps, and each substep requires a Primary Agent to call a Skill and a Reviewer Agent to audit the result using a paired Skill. Only after passing the Reviewer's audit can the workflow proceed to the next substep.

## Design Principles

1. **Strong Constraint Relationship**: Reviewer Agents have veto power - if a substep doesn't pass review, it cannot proceed.
2. **Skill-Operation Mapping**: Each Agent operation maps to a specific Skill, eliminating redundancy.
3. **Iterative Refinement**: Agents iterate until the Reviewer approves, ensuring quality.
4. **State Tracking**: Substep completion status is tracked in `research-state.yaml`.
5. **Human Gate Preservation**: After all substeps pass, human approval is still required for phase transitions.
6. **In-Place Modification with Version Tracking**: Artifacts are modified in-place during iteration. All changes are tracked by GitMem-Skill, enabling rollback and history review.

---

## Phase 1: Survey Phase

### Substep 1.1: Literature Survey

| Role | Agent | Skill Called | Output Artifact |
|------|-------|--------------|-----------------|
| Primary | Survey | `/research-lit` | `docs/reports/survey/literature-review.md` |
| Reviewer | Critic | `/audit-survey` | `docs/reports/survey/survey-audit.md` |

**Workflow:**
1. Survey Agent invokes `/research-lit` to conduct literature search
2. Survey Agent produces `literature-review.md` using academic APIs (Semantic Scholar, arXiv, etc.)
3. Critic Agent invokes `/audit-survey` to verify:
   - Coverage completeness (no major papers missed)
   - Citation authenticity (all citations verifiable)
   - Methodology identification (baseline methods extracted)
4. **Gate**: Critic must approve before proceeding

**Approval Criteria:**
- [ ] At least 20 relevant papers cited
- [ ] All citations verified via academic database
- [ ] Research gap clearly identified
- [ ] Baseline methods documented

### Substep 1.2: Idea Definition

| Role | Agent | Skill Called | Output Artifact |
|------|-------|--------------|-----------------|
| Primary | Survey | `/define-idea` | `docs/reports/survey/idea-definition.md` |
| Reviewer | Critic | `/novelty-check` | `docs/reports/survey/novelty-report.md` |

**Workflow:**
1. Survey Agent invokes `/define-idea` to formulate research hypothesis
2. Survey Agent produces `idea-definition.md` with:
   - Problem statement
   - Proposed approach
   - Expected contributions
3. Critic Agent invokes `/novelty-check` to verify:
   - Novelty compared to existing work
   - Feasibility assessment
   - Contribution significance
4. **Gate**: Critic must approve before proceeding

**Approval Criteria:**
- [ ] Problem clearly stated with motivation
- [ ] Differentiation from at least 3 existing methods
- [ ] Feasible experimental validation plan
- [ ] Clear contribution statement

### Substep 1.3: Research Plan

| Role | Agent | Skill Called | Output Artifact |
|------|-------|--------------|-----------------|
| Primary | Survey | `/research-plan` | `docs/reports/survey/research-readiness-report.md` |
| Reviewer | Critic | `/audit-plan` | `docs/reports/survey/plan-audit.md` |

**Workflow:**
1. Survey Agent invokes `/research-plan` to create execution plan
2. Survey Agent produces `research-readiness-report.md` with:
   - Methodology overview
   - Experiment design outline
   - Resource requirements
   - Timeline estimation
3. Critic Agent invokes `/audit-plan` to verify:
   - Completeness of plan
   - Resource feasibility
   - Risk assessment
4. **Gate**: Critic must approve before phase gate

**Approval Criteria:**
- [ ] Clear methodology description
- [ ] Experiment matrix defined
- [ ] Resource requirements estimated
- [ ] Risks identified and mitigated

**Phase Gate 0**: Human approval required before proceeding to Pilot phase.

---

## Phase 2: Pilot Phase

### Substep 2.1: Problem Analysis

| Role | Agent | Skill Called | Output Artifact |
|------|-------|--------------|-----------------|
| Primary | Code | `/analyze-problem` | `docs/reports/pilot/problem-analysis.md` |
| Reviewer | Adviser | `/audit-analysis` | `docs/reports/pilot/analysis-review.md` |

**Workflow:**
1. Code Agent invokes `/analyze-problem` to analyze the research problem
2. Code Agent produces `problem-analysis.md` with:
   - Problem decomposition
   - Technical challenges
   - Solution approach
3. Adviser Agent invokes `/audit-analysis` to verify:
   - Problem understanding correctness
   - Solution approach validity
   - Technical feasibility
4. **Gate**: Adviser must approve before proceeding

**Approval Criteria:**
- [ ] Problem correctly decomposed
- [ ] Technical challenges identified
- [ ] Solution approach aligns with literature

### Substep 2.2: Pilot Design

| Role | Agent | Skill Called | Output Artifact |
|------|-------|--------------|-----------------|
| Primary | Code | `/design-pilot` | `docs/reports/pilot/pilot-design.md` |
| Reviewer | Adviser | `/audit-design` | `docs/reports/pilot/design-review.md` |

**Workflow:**
1. Code Agent invokes `/design-pilot` to design pilot experiment
2. Code Agent produces `pilot-design.md` with:
   - Minimal implementation plan
   - Pilot experiment setup
   - Success criteria
3. Adviser Agent invokes `/audit-design` to verify:
   - Pilot scope appropriateness
   - Design correctness
   - Success criteria validity
4. **Gate**: Adviser must approve before proceeding

**Approval Criteria:**
- [ ] Pilot scope is minimal but representative
- [ ] Design follows best practices
- [ ] Success criteria are measurable

### Substep 2.3: Pilot Execution

| Role | Agent | Skill Called | Output Artifact |
|------|-------|--------------|-----------------|
| Primary | Code | `/run-pilot` | `docs/reports/pilot/pilot-validation-report.md` |
| Reviewer | Adviser | `/audit-pilot` | `docs/reports/pilot/pilot-review.md` |

**Workflow:**
1. Code Agent invokes `/run-pilot` to execute pilot experiment
2. Code Agent produces `pilot-validation-report.md` with:
   - Implementation details
   - Experiment results
   - Lessons learned
3. Adviser Agent invokes `/audit-pilot` to verify:
   - Results validity
   - Reproducibility
   - Lessons learned completeness
4. **Gate**: Adviser must approve before phase gate

**Approval Criteria:**
- [ ] Implementation complete and documented
- [ ] Results reproducible
- [ ] Go/No-Go recommendation justified

**Phase Gate 1**: Human approval required before proceeding to Experiments phase.

---

## Phase 3: Experiments Phase

### Substep 3.1: Experiment Design

| Role | Agent | Skill Called | Output Artifact |
|------|-------|--------------|-----------------|
| Primary | Code | `/design-exp` | `docs/reports/experiments/experiment-spec.md` |
| Reviewer | Adviser | `/audit-exp-design` | `docs/reports/experiments/design-review.md` |

**Workflow:**
1. Code Agent invokes `/design-exp` to design full experiment matrix
2. Code Agent produces `experiment-spec.md` with:
   - Experiment matrix
   - Hyperparameter ranges
   - Evaluation metrics
   - Statistical tests
3. Adviser Agent invokes `/audit-exp-design` to verify:
   - Experiment completeness
   - Statistical validity
   - Metric appropriateness
4. **Gate**: Adviser must approve before proceeding

**Approval Criteria:**
- [ ] All necessary baselines included
- [ ] Statistical tests properly defined
- [ ] Metrics align with research questions

### Substep 3.2: Experiment Execution

| Role | Agent | Skill Called | Output Artifact |
|------|-------|--------------|-----------------|
| Primary | Code | `/run-experiment` | `docs/reports/experiments/run-registry.md` |
| Reviewer | Adviser | `/monitor-experiment` | `docs/reports/experiments/monitoring-report.md` |

**Workflow:**
1. Code Agent invokes `/run-experiment` to execute experiments
2. Code Agent maintains `run-registry.md` with:
   - Run configurations
   - Intermediate results
   - Checkpoint index
3. Adviser Agent invokes `/monitor-experiment` to verify:
   - Run reproducibility
   - Result integrity
   - Resource utilization
4. **Gate**: Adviser must approve before proceeding

**Approval Criteria:**
- [ ] All runs fully reproducible
- [ ] Random seeds documented
- [ ] Checkpoints saved

### Substep 3.3: Results Analysis

| Role | Agent | Skill Called | Output Artifact |
|------|-------|--------------|-----------------|
| Primary | Code | `/analyze-results` | `docs/reports/experiments/results-summary.md` |
| Reviewer | Adviser | `/audit-results` | `docs/reports/experiments/evidence-package-index.md` |

**Workflow:**
1. Code Agent invokes `/analyze-results` to analyze experiment results
2. Code Agent produces `results-summary.md` with:
   - Statistical analysis
   - Comparison tables
   - Key findings
3. Adviser Agent invokes `/audit-results` to verify:
   - Statistical correctness
   - Evidence strength
   - Claim support
4. **Gate**: Adviser must approve before phase gate

**Approval Criteria:**
- [ ] Statistical tests correctly applied
- [ ] All claims supported by evidence
- [ ] Evidence package complete

**Phase Gate 2**: Human approval required before proceeding to Paper phase.

---

## Phase 4: Paper Phase

### Substep 4.1: Paper Planning

| Role | Agent | Skill Called | Output Artifact |
|------|-------|--------------|-----------------|
| Primary | Writer | `/paper-plan` | `paper/paper-outline.md` |
| Reviewer | Reviewer | `/audit-paper-plan` | `paper/outline-review.md` |

**Workflow:**
1. Writer Agent invokes `/paper-plan` to create paper structure
2. Writer Agent produces `paper-outline.md` with:
   - Section outline
   - Key arguments per section
   - Figure/table plan
3. Reviewer Agent invokes `/audit-paper-plan` to verify:
   - Logical flow
   - Argument completeness
   - Figure/table appropriateness
4. **Gate**: Reviewer must approve before proceeding

**Approval Criteria:**
- [ ] Logical flow clear
- [ ] All key results covered
- [ ] Target venue format followed

### Substep 4.2: Paper Writing

| Role | Agent | Skill Called | Output Artifact |
|------|-------|--------------|-----------------|
| Primary | Writer | `/paper-write` | `paper/paper-draft.md` |
| Reviewer | Reviewer | `/audit-paper` | `paper/reviewer-report.md` |

**Workflow:**
1. Writer Agent invokes `/paper-write` to write paper sections
2. Writer Agent produces `paper-draft.md` following top-tier standards
3. Reviewer Agent invokes `/audit-paper` to review:
   - Clarity and correctness
   - Evidence grounding
   - Contribution framing
4. **Gate**: Reviewer must approve before proceeding

**Approval Criteria:**
- [ ] All sections complete
- [ ] Evidence-grounded claims only
- [ ] Top-tier writing quality

### Substep 4.3: Citation Curation

| Role | Agent | Skill Called | Output Artifact |
|------|-------|--------------|-----------------|
| Primary | Writer | `/curate-citation` | `paper/citation-index.md` |
| Reviewer | Reviewer | `/audit-citation` | `paper/citation-audit-report.md` |

**Workflow:**
1. Writer Agent invokes `/curate-citation` to finalize citations
2. Writer Agent produces `citation-index.md` with all references
3. Reviewer Agent invokes `/audit-citation` to verify:
   - Citation authenticity (>=90% verified)
   - Attribution correctness
   - Reference formatting
4. **Gate**: Reviewer must approve before phase gate

**Approval Criteria:**
- [ ] >=90% citations verified in academic databases
- [ ] No misattribution
- [ ] Correct reference format

**Phase Gate 3**: Human approval required before proceeding to Reflection phase.

---

## Phase 5: Reflection Phase

### Substep 5.1: Lessons Extraction

| Role | Agent | Skill Called | Output Artifact |
|------|-------|--------------|-----------------|
| Primary | Reflector | `/extract-lessons` | `docs/reports/reflection/lessons-learned.md` |
| Reviewer | Curator | `/audit-lessons` | `docs/reports/reflection/lessons-review.md` |

**Workflow:**
1. Reflector Agent invokes `/extract-lessons` to document lessons
2. Reflector Agent produces `lessons-learned.md` with:
   - What worked well
   - What didn't work
   - Process improvements
3. Curator Agent invokes `/audit-lessons` to verify:
   - Lesson transferability
   - Actionability
   - Completeness
4. **Gate**: Curator must approve before proceeding

**Approval Criteria:**
- [ ] Lessons are transferable to future projects
- [ ] Actionable recommendations provided
- [ ] Both positive and negative lessons documented

### Substep 5.2: Overlay Proposal

| Role | Agent | Skill Called | Output Artifact |
|------|-------|--------------|-----------------|
| Primary | Reflector | `/propose-overlay` | `docs/reports/reflection/overlay-draft.md` |
| Reviewer | Curator | `/audit-overlay` | `docs/reports/reflection/runtime-improvement-report.md` |

**Workflow:**
1. Reflector Agent invokes `/propose-overlay` to propose system improvements
2. Reflector Agent produces `overlay-draft.md` with:
   - Proposed prompt improvements
   - Proposed workflow changes
   - Risk assessment
3. Curator Agent invokes `/audit-overlay` to verify:
   - Proposed changes are safe
   - Changes are reversible
   - Changes align with project goals
4. **Gate**: Curator must approve before phase gate

**Approval Criteria:**
- [ ] Changes are clearly documented
- [ ] Changes are reversible
- [ ] User opt-in list provided

**Phase Gate 4**: Human approval required for overlay activation and project completion.

---

## GitMem-Skill Integration

GitMem-Skill provides version tracking for agent edits, enabling iterative refinement without creating v1, v2, v3 copies. All changes are tracked in a separate `.gitmem` repository, keeping the main project history clean.

### Initialization

When `/init-research` creates a new project, GitMem is automatically initialized:

```bash
# In init_research_project.py
gitmem init --project-root /path/to/project
```

This creates:
- `.gitmem/` directory with a separate git repository
- Tracks all files in `docs/reports/`, `paper/`, `code/`, `agents/`

### Iteration Workflow with GitMem

Each substep iteration follows this pattern:

```
Primary Agent                    GitMem                    Reviewer Agent
     │                             │                             │
     ├─ Edit artifact ────────────►│                             │
     │                             ├─ auto-commit (gitmem watch) │
     │                             │                             │
     ├─ Submit for review ─────────────────────────────────────►│
     │                             │                             │
     │                             │◄── Review: needs revision ──┤
     │                             │                             │
     ├─ Edit artifact (in-place) ─►│                             │
     │                             ├─ auto-commit                │
     │                             │                             │
     ├─ Submit again ──────────────────────────────────────────►│
     │                             │                             │
     │                             │◄── Review: APPROVED ────────┤
     │                             │                             │
     │                             ├─ gitmem checkpoint ─────────┤
     │                             │  "substep-X.X-approved"     │
     ▼                             ▼                             ▼
```

### Checkpoint Strategy

Checkpoints mark stable states for easy rollback:

| Checkpoint Name | When Created |
|-----------------|--------------|
| `init-complete` | After project initialization |
| `survey-1.1-approved` | After Literature Survey substep passes |
| `survey-1.2-approved` | After Idea Definition substep passes |
| `survey-complete` | After Survey phase gate approval |
| `pilot-2.1-approved` | After Problem Analysis substep passes |
| ... | ... |
| `phase-gate-N-approved` | After each human gate approval |

### Loop Guard

GitMem's loop guard prevents infinite edit cycles:

- **Warning**: If a file appears in 5+ consecutive commits without a checkpoint
- **Action**: Orchestrator is notified to investigate potential stuck state
- **Resolution**: Either create checkpoint or escalate to human

### GitMem Commands in Orchestrator

```python
# In orchestrator_common.py

def gitmem_init(project_root: str) -> None:
    """Initialize GitMem for a new project."""
    subprocess.run(["gitmem", "init", "--project-root", project_root])

def gitmem_commit(project_root: str, file_path: str, message: str) -> None:
    """Commit a file change to GitMem history."""
    subprocess.run([
        "gitmem", "commit",
        "--project-root", project_root,
        "--file", file_path,
        "--message", message
    ])

def gitmem_checkpoint(project_root: str, name: str) -> None:
    """Create a checkpoint after substep approval."""
    subprocess.run([
        "gitmem", "checkpoint",
        "--project-root", project_root,
        "--name", name
    ])

def gitmem_check_loop(project_root: str, file_path: str) -> bool:
    """Check if a file is in an edit loop (5+ changes without checkpoint)."""
    result = subprocess.run([
        "gitmem", "check-loop",
        "--project-root", project_root,
        "--file", file_path
    ], capture_output=True)
    return "LOOP DETECTED" in result.stdout.decode()
```

### Version History Access

Users can view and rollback changes at any time:

```bash
# View history of a specific artifact
gitmem history docs/reports/survey/literature-review.md

# Compare versions
gitmem diff docs/reports/survey/literature-review.md

# Rollback to previous version
gitmem rollback docs/reports/survey/literature-review.md

# View all checkpoints
gitmem checkpoint list
```

---

## Configuration Changes

### orchestrator-config.yaml

```yaml
phases:
  survey:
    agents:
      primary: survey
      reviewer: critic
    substeps:
      - name: literature_survey
        primary_skill: research-lit
        reviewer_skill: audit-survey
        required_artifacts:
          - docs/reports/survey/literature-review.md
      - name: idea_definition
        primary_skill: define-idea
        reviewer_skill: novelty-check
        required_artifacts:
          - docs/reports/survey/idea-definition.md
      - name: research_plan
        primary_skill: research-plan
        reviewer_skill: audit-plan
        required_artifacts:
          - docs/reports/survey/research-readiness-report.md

  pilot:
    agents:
      primary: code
      reviewer: adviser
    substeps:
      - name: problem_analysis
        primary_skill: analyze-problem
        reviewer_skill: audit-analysis
        required_artifacts:
          - docs/reports/pilot/problem-analysis.md
      - name: pilot_design
        primary_skill: design-pilot
        reviewer_skill: audit-design
        required_artifacts:
          - docs/reports/pilot/pilot-design.md
      - name: pilot_execution
        primary_skill: run-pilot
        reviewer_skill: audit-pilot
        required_artifacts:
          - docs/reports/pilot/pilot-validation-report.md

  experiments:
    agents:
      primary: code
      reviewer: adviser
    substeps:
      - name: experiment_design
        primary_skill: design-exp
        reviewer_skill: audit-exp-design
        required_artifacts:
          - docs/reports/experiments/experiment-spec.md
      - name: experiment_execution
        primary_skill: run-experiment
        reviewer_skill: monitor-experiment
        required_artifacts:
          - docs/reports/experiments/run-registry.md
      - name: results_analysis
        primary_skill: analyze-results
        reviewer_skill: audit-results
        required_artifacts:
          - docs/reports/experiments/evidence-package-index.md

  paper:
    agents:
      primary: writer
      reviewer: reviewer
    substeps:
      - name: paper_planning
        primary_skill: paper-plan
        reviewer_skill: audit-paper-plan
        required_artifacts:
          - paper/paper-outline.md
      - name: paper_writing
        primary_skill: paper-write
        reviewer_skill: audit-paper
        required_artifacts:
          - paper/paper-draft.md
      - name: citation_curation
        primary_skill: curate-citation
        reviewer_skill: audit-citation
        required_artifacts:
          - paper/citation-audit-report.md

  reflection:
    agents:
      primary: reflector
      reviewer: curator
    substeps:
      - name: lessons_extraction
        primary_skill: extract-lessons
        reviewer_skill: audit-lessons
        required_artifacts:
          - docs/reports/reflection/lessons-learned.md
      - name: overlay_proposal
        primary_skill: propose-overlay
        reviewer_skill: audit-overlay
        required_artifacts:
          - docs/reports/reflection/runtime-improvement-report.md
```

### research-state.yaml Structure Update

```yaml
status: in_progress
current_phase: survey
current_substep: literature_survey

substep_status:
  survey:
    literature_survey:
      status: in_progress
      attempts: 1
      last_agent: survey
      review_result: pending
    idea_definition:
      status: pending
    research_plan:
      status: pending
  pilot:
    problem_analysis:
      status: pending
    pilot_design:
      status: pending
    pilot_execution:
      status: pending
  # ... other phases
```

---

## Skill Specifications

### Primary Skills (14 total)

| Skill | Purpose | Agent |
|-------|---------|-------|
| `/research-lit` | Literature search using academic APIs | Survey |
| `/define-idea` | Formulate research hypothesis | Survey |
| `/research-plan` | Create research execution plan | Survey |
| `/analyze-problem` | Analyze research problem | Code |
| `/design-pilot` | Design pilot experiment | Code |
| `/run-pilot` | Execute pilot experiment | Code |
| `/design-exp` | Design full experiment matrix | Code |
| `/run-experiment` | Execute experiments | Code |
| `/analyze-results` | Analyze experiment results | Code |
| `/paper-plan` | Create paper outline | Writer |
| `/paper-write` | Write paper sections | Writer |
| `/curate-citation` | Finalize citations | Writer |
| `/extract-lessons` | Extract lessons learned | Reflector |
| `/propose-overlay` | Propose system improvements | Reflector |

### Reviewer/Audit Skills (14 total)

| Skill | Purpose | Agent |
|-------|---------|-------|
| `/audit-survey` | Audit literature completeness | Critic |
| `/novelty-check` | Verify idea novelty | Critic |
| `/audit-plan` | Audit research plan | Critic |
| `/audit-analysis` | Audit problem analysis | Adviser |
| `/audit-design` | Audit pilot design | Adviser |
| `/audit-pilot` | Audit pilot results | Adviser |
| `/audit-exp-design` | Audit experiment design | Adviser |
| `/monitor-experiment` | Monitor experiment execution | Adviser |
| `/audit-results` | Audit results analysis | Adviser |
| `/audit-paper-plan` | Audit paper outline | Reviewer |
| `/audit-paper` | Review paper draft | Reviewer |
| `/audit-citation` | Audit citation authenticity | Reviewer |
| `/audit-lessons` | Audit lessons transferability | Curator |
| `/audit-overlay` | Audit overlay safety | Curator |

---

## Strong Constraint Implementation

### Substep Gate Logic

```python
def advance_substep(project_root: str, current_phase: str, current_substep: str) -> bool:
    """
    Check if workflow can advance to next substep.
    Returns True only if reviewer approved.
    """
    state = load_research_state(project_root)

    # Get current substep status
    substep_data = state['substep_status'][current_phase][current_substep]

    # Must have reviewer approval
    if substep_data['review_result'] != 'approved':
        return False

    # Must have required artifacts
    config = load_orchestrator_config(project_root)
    phase_config = config['phases'][current_phase]
    substep_config = next(s for s in phase_config['substeps'] if s['name'] == current_substep)

    for artifact in substep_config['required_artifacts']:
        if not os.path.exists(os.path.join(project_root, artifact)):
            return False

    return True
```

### Agent Prompt Template Updates

Each agent prompt must include skill invocation instructions:

```markdown
## Your Role

You are the {AGENT_NAME} agent. Your responsibility is to {RESPONSIBILITY}.

## Available Skills

You have access to the following skill:
- `/{SKILL_NAME}`: {SKILL_DESCRIPTION}

## Workflow

1. Invoke your skill using the Skill tool
2. Produce the required artifact (modify in-place, GitMem tracks versions)
3. Wait for reviewer feedback
4. Iterate until approved

## Version Tracking

All your edits are automatically tracked by GitMem-Skill:
- **DO NOT** create v1, v2, v3 versions of files
- **DO** modify files in-place
- GitMem preserves all previous versions
- Users can rollback via `gitmem rollback <file>`

## Constraints

- You MUST use your assigned skill for this substep
- You CANNOT proceed to the next substep without reviewer approval
- You MUST address all reviewer feedback
```

---

## Implementation Checklist

### Phase 0: GitMem Integration
- [ ] Add GitMem-Skill as a dependency/embedded skill
- [ ] Update `init_research_project.py` to call `gitmem init`
- [ ] Add GitMem functions to `orchestrator_common.py`
- [ ] Implement checkpoint creation after each substep approval
- [ ] Add loop guard monitoring to `run_stage_loop.py`

### Phase 1: Create Skills
- [ ] Create 14 primary skill files in `skills/`
- [ ] Create 14 audit skill files in `skills/`
- [ ] Update SKILL.md with skill registry (28 skills total)

### Phase 2: Update Configuration
- [ ] Update `orchestrator-config.yaml` with substeps
- [ ] Update `research-state.yaml` schema
- [ ] Create substep validation script

### Phase 3: Update Agent Prompts
- [ ] Update all agent prompt templates
- [ ] Add skill invocation instructions
- [ ] Add reviewer constraint documentation
- [ ] Add GitMem usage notes (in-place editing with auto-tracking)

### Phase 4: Update Orchestrator Script
- [ ] Modify `run_stage_loop.py` to handle substeps
- [ ] Implement substep gate checking
- [ ] Implement substep state tracking
- [ ] Integrate GitMem checkpoint on approval

### Phase 5: Testing
- [ ] Unit tests for substep validation
- [ ] Unit tests for GitMem integration
- [ ] Integration tests for substep flow
- [ ] End-to-end test for complete workflow