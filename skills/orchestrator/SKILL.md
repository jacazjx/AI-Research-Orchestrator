---
name: airesearchorchestrator:orchestrator
description: "Initialize and run a gated five-phase AI research project from idea through paper. Use when user says 'start research project', '帮我做一个研究', 'research workflow', '五阶段研究流程', 'research orchestrator', or needs structured AI/ML research management with Survey, Pilot, Experiments, Paper, and Reflection phases."
argument-hint: [research-topic-or-idea]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply
---

# AI Research Orchestrator

## Overview

This skill turns a loose research request into a controlled five-phase project with fixed directories, scored gate checks, visible progress artifacts, and explicit human approval between phases. It is optimized for AI/ML algorithm research that needs literature review, pilot validation, experiments, paper writing, and controlled post-project reflection without losing provenance.

## Directory Structure

The project uses a semantic directory structure:

```
my-project/
├── .autoresearch/           # System directory (hidden)
│   ├── state/               # State files
│   │   └── research-state.yaml
│   ├── config/              # Configuration
│   │   └── orchestrator-config.yaml
│   ├── dashboard/           # Runtime dashboard
│   ├── runtime/             # Runtime registries (job, GPU, backend)
│   ├── reference-papers/    # Reference papers
│   ├── templates/           # Template cache
│   └── archive/             # Archive
├── agents/                  # Agent work directories (by role)
│   ├── survey/
│   ├── critic/
│   ├── coder/
│   ├── adviser/
│   ├── writer/
│   ├── reviewer/
│   ├── reflector/
│   └── curator/
├── paper/                   # Paper-related files
├── code/                    # Code-related files
└── docs/                    # Documentation and reports
    └── reports/
        ├── survey/
        ├── pilot/
        └── experiments/
```

## Phase Names

The project uses semantic phase names:
- `survey` — Literature survey phase
- `pilot` — Pilot validation phase
- `experiments` — Full experiments phase
- `paper` — Paper writing phase
- `reflection` — Reflection and evolution phase

> **Backward Compatibility**: Legacy numbered names (`01-survey`, `02-pilot-analysis`, etc.) are still supported, but semantic names are recommended.

## Quick Start

### Option A: Start a New Project

1. If the client supports `/init`, run it first in the target project directory. Do not rely on the generated Markdown file name.
2. Initialize the standardized workspace:

```bash
python3 scripts/init_research_project.py \
  --project-root /abs/path/to/my-project \
  --topic "Your research idea or problem statement" \
  --client-type auto
```

3. (Optional) Specify a starting phase if resuming work or skipping completed phases:

```bash
# Start at pilot analysis phase
python3 scripts/init_research_project.py \
  --project-root /abs/path/to/my-project \
  --topic "Your research idea" \
  --starting-phase pilot

# Start at paper writing phase
python3 scripts/init_research_project.py \
  --project-root /abs/path/to/my-project \
  --topic "Your research idea" \
  --starting-phase paper
```

Available starting phases: `survey`, `pilot`, `experiments`, `paper`, `reflection` (or legacy names: `01-survey`, `02-pilot-analysis`, `03-full-experiments`, `04-paper`, `05-reflection-evolution`)

### Option B: Take Over an Existing Project

If you have an existing research project that doesn't follow the orchestrator format:

1. Analyze the existing project:

```bash
python3 scripts/analyze_project.py --project-root /path/to/existing-project
```

2. Migrate to orchestrator format:

```bash
python3 scripts/migrate_project.py \
  --project-root /path/to/existing-project \
  --topic "Your research topic"
```

3. (Optional) Override the auto-detected phase:

```bash
# Force start at a specific phase
python3 scripts/migrate_project.py \
  --project-root /path/to/existing-project \
  --topic "Your research topic" \
  --starting-phase 03-full-experiments
```

4. Verify the migration:

```bash
python3 scripts/verify_system.py --project-root /path/to/existing-project
```

See [references/project-takeover-protocol.md](references/project-takeover-protocol.md) for detailed takeover procedures.

### Common Operations

Check system version:

```bash
# Show version information
python3 scripts/show_version.py

# Show only version number
python3 scripts/show_version.py --short

# JSON output
python3 scripts/show_version.py --json
```

Re-materialize templates after state updates or missing files:

```bash
python3 scripts/materialize_templates.py --project-root /abs/path/to/my-project
```

View current project status with agent activity:

```bash
# Full statusline display
python3 scripts/generate_statusline.py --project-root /abs/path/to/my-project

# Compact single-line status
python3 scripts/generate_statusline.py --project-root /abs/path/to/my-project --compact

# JSON output for programmatic use
python3 scripts/generate_statusline.py --project-root /abs/path/to/my-project --json
```

Render a role prompt, then let the user-facing orchestrator adjust it for the current task:

```bash
python3 scripts/render_agent_prompt.py \
  --project-root /abs/path/to/my-project \
  --role survey \
  --task-summary "Expand the idea into atomic academic definitions and recent literature" \
  --current-objective "Prepare the first survey round before critic review"
```

Generate dashboard artifacts and inspect runtime status:

```bash
python3 scripts/generate_dashboard.py --project-root /abs/path/to/my-project
```

Validate a gate or loop before advancing:

```bash
python3 scripts/validate_handoff.py --project-root /abs/path/to/my-project --target survey-to-pilot
python3 scripts/quality_gate.py --project-root /abs/path/to/my-project --phase survey
```

Manage phase handoff summaries:

```bash
# Save a handoff summary
python3 scripts/phase_handoff.py --project-root /abs/path/to/my-project \
  --action save --phase survey --agent survey \
  --summary '{"key_findings": ["Finding 1"], "decisions_made": ["Decision 1"]}'

# Load a handoff summary
python3 scripts/phase_handoff.py --project-root /abs/path/to/my-project \
  --action load --phase survey --agent survey

# List all summaries
python3 scripts/phase_handoff.py --project-root /abs/path/to/my-project --action list
```

## Literature Search (IMPORTANT)

**CRITICAL: Use academic database APIs, NOT web search.**

When searching for literature, use these APIs:

| API | Use Case | Example |
|-----|----------|---------|
| Semantic Scholar | AI/ML papers | `api.semanticscholar.org/graph/v1/paper/search?query=transformer` |
| arXiv | Preprints | `export.arxiv.org/api/query?search_query=all:attention` |
| CrossRef | DOI verification | `api.crossref.org/works?query.title=paper+title` |
| DBLP | Computer Science | `dblp.org/search/publ/api?q=transformer&format=json` |
| OpenAlex | Comprehensive | `api.openalex.org/works?search=vision+transformer` |

See [references/literature-verification.md](references/literature-verification.md) for detailed API usage.

## Skills Registry

The orchestrator includes 40 skills organized into Primary Skills (workflow execution) and Audit Skills (quality verification).

### Primary Skills (16)

These skills execute the research workflow phases:

| Skill | Agent | Output | Purpose |
|-------|-------|--------|---------|
| `define-idea` | Survey | `docs/reports/survey/idea-definition.md` | Formulate research hypothesis |
| `research-plan` | Survey | `docs/reports/survey/research-readiness-report.md` | Create research execution plan |
| `research-lit` | Survey | Working notes | Literature survey using academic APIs |
| `novelty-check` | Survey | Novelty report | Verify novelty against existing work |
| `analyze-problem` | Code | `docs/reports/pilot/problem-analysis.md` | Analyze research problem |
| `design-pilot` | Code | `docs/reports/pilot/pilot-design.md` | Design pilot experiment |
| `run-pilot` | Code | `docs/reports/pilot/pilot-validation-report.md` | Execute pilot experiment |
| `design-exp` | Code | `docs/reports/experiments/experiment-spec.md` | Design full experiment matrix |
| `run-experiment` | Code | Experiment logs | Deploy and run ML experiments |
| `monitor-experiment` | Code | Progress reports | Monitor running experiments |
| `analyze-results` | Code | Results summary | Analyze experiment results |
| `paper-plan` | Writer | `paper/PAPER_PLAN.md` | Create paper outline |
| `paper-write` | Writer | `paper/main.tex` | Write paper sections |
| `curate-citation` | Writer | `paper/citation-index.md` | Finalize and verify citations |
| `extract-lessons` | Reflector | `docs/reports/reflection/lessons-learned.md` | Extract lessons learned |
| `propose-overlay` | Reflector | `docs/reports/reflection/overlay-draft.md` | Propose system improvements |

### Audit Skills (12)

These skills verify quality and provide phase gate assessments:

| Skill | Agent | Purpose |
|-------|-------|---------|
| `audit-survey` | Critic | Audit literature completeness and citation authenticity |
| `audit-plan` | Critic | Audit research plan feasibility and risk coverage |
| `audit-analysis` | Adviser | Audit problem analysis completeness |
| `audit-design` | Adviser | Audit pilot design validity and efficiency |
| `audit-pilot` | Adviser | Audit pilot results and hypothesis validation |
| `audit-exp-design` | Adviser | Audit experiment design statistical validity |
| `audit-results` | Adviser | Audit results traceability and negative result handling |
| `audit-paper-plan` | Reviewer | Audit paper outline claim-evidence alignment |
| `audit-paper` | Reviewer | Review paper draft for rigor and quality |
| `audit-citation` | Reviewer | Audit citation authenticity in detail |
| `audit-lessons` | Curator | Audit lessons transferability and actionability |
| `audit-overlay` | Curator | Audit proposed system improvements for safety |

### Supporting Skills (12)

Additional workflow automation skills:

| Skill | Purpose |
|-------|---------|
| `idea-discovery` | Full idea discovery pipeline |
| `idea-creator` | Generate research ideas |
| `research-review` | Review research progress |
| `research-pipeline` | End-to-end research pipeline |
| `paper-writing` | Full paper writing pipeline |
| `paper-figure` | Generate paper figures |
| `paper-compile` | Compile paper to PDF |
| `auto-review-loop` | Multi-round autonomous review |
| `auto-paper-improvement-loop` | Iterative paper improvement |
| `latex-citation-curator` | Curate LaTeX citations |
| `feishu-notify` | Send Feishu notifications |
| `gitmem` | Git memory and commit tracking |

## ARIS Integration: Standalone Entry Points

This skill now includes ARIS (Auto-Research-In-Sleep) capabilities. You can invoke these workflows independently:

### Workflow 1: Idea Discovery

```bash
# Full idea discovery pipeline
/autoresearch:idea-discovery "transformer efficiency optimization"

# Sub-skills (invoked by idea-discovery)
/autoresearch:research-lit "attention mechanisms"
/autoresearch:idea-creator "multi-modal reasoning"
/autoresearch:novelty-check "proposed idea description"
/autoresearch:research-review "idea with pilot results"
```

### Workflow 2: Auto Review Loop

```bash
# Multi-round autonomous review
/autoresearch:auto-review-loop "experiment results"

# Supporting skills
/autoresearch:run-experiment "python train.py --config config.yaml"
/autoresearch:monitor-experiment "gpu-server-1"
/autoresearch:analyze-results "results/"
```

### Workflow 3: Paper Writing

```bash
# Full paper writing pipeline
/autoresearch:paper-writing "NARRATIVE_REPORT.md"

# Sub-skills (invoked by paper-writing)
/autoresearch:paper-plan "results/"
/autoresearch:paper-figure "data/"
/autoresearch:paper-write "PAPER_PLAN.md"
/autoresearch:paper-compile "paper/"
```

### Full Pipeline

```bash
# End-to-end: idea → experiments → submission
/autoresearch:research-pipeline "multi-modal reasoning"
```

### Configuration

Enable cross-model review in `.autoresearch/config/orchestrator-config.yaml`:

```yaml
aris:
  auto_proceed: false
  reviewer:
    enabled: true
    model: gpt-5.4
```

To enable Codex MCP for cross-model review, configure it in your Claude Code environment.

## Workflow

### 1. Initialize the workspace

- Create a project root with `.autoresearch/` (state, config, dashboard, runtime), `agents/` (per-role directories), `paper/`, `code/`, and `docs/`.
- Create `.autoresearch/reference-papers/` for user-provided reference PDFs, notes, or BibTeX exports.
- Generate `AGENTS.md` or `CLAUDE.md` at the project root according to the detected or requested client type.
- **Ask the researcher about compute configuration** (local/remote, GPU specs, existing codebases).
- Maintain `.autoresearch/state/research-state.yaml` as the only machine-readable state.
- Maintain `.autoresearch/config/orchestrator-config.yaml` as project-level runtime configuration.
- Maintain `.autoresearch/dashboard/` as the visible runtime dashboard.
- Record any pre-existing client `/init` artifacts, but never treat their file names as protocol.
- **The Orchestrator is the only agent that talks directly to the researcher.** Before any phase begins, the Orchestrator confirms the research intent through iterative clarification.

### 2. Run the five-phase loop

**IMPORTANT: Each phase has EXACTLY 2 active agents (primary + reviewer). Do NOT spawn explore agents or other helpers.**

When transitioning between phases:
1. Save handoff summaries from both agents
2. Dismiss previous phase agents
3. Spawn new phase agents (2 only)
4. Pass handoff summaries if resuming from rollback

- Phase 1: `Survey <-> Critic`
  Produce `docs/reports/survey/research-readiness-report.md` and `docs/reports/survey/phase-scorecard.md`, then stop for Gate 1.
- Phase 2: `Code <-> Adviser` for pilot analysis
  Produce `docs/reports/pilot/pilot-validation-report.md` and `docs/reports/pilot/phase-scorecard.md`, then stop for Gate 2.
- Phase 3: `Code <-> Adviser` for full experiments
  Produce `docs/reports/experiments/evidence-package-index.md` and `docs/reports/experiments/phase-scorecard.md`, then stop for Gate 3.
- Phase 4: `Paper Writer <-> Reviewer & Editor`
  Produce `paper/citation-audit-report.md`, `paper/final-acceptance-report.md`, and `paper/phase-scorecard.md`, then stop for Gate 4.
- Phase 5: `Reflector <-> Curator`
  Produce `docs/reports/reflection/runtime-improvement-report.md` and `docs/reports/reflection/phase-scorecard.md`, then stop for Gate 5 before any overlay or policy change is activated.

## Phase Gate Checklist

Before advancing to the next phase, ALL items in the corresponding gate checklist must be verified.

### Gate 0: Initialization Check

- [ ] `.autoresearch/state/research-state.yaml` exists and is valid
- [ ] `.autoresearch/config/orchestrator-config.yaml` exists
- [ ] Required directories created (`paper/`, `code/`, `docs/`, `agents/`)
- [ ] `AGENTS.md` or `CLAUDE.md` generated at project root
- [ ] Research topic clarified and recorded

### Gate 1: Survey → Pilot

**Required Deliverables:**
- [ ] `docs/reports/survey/research-readiness-report.md` exists and contains:
  - [ ] Problem statement with clear research questions
  - [ ] Literature review summary (min 10 papers)
  - [ ] Gap analysis with proposed contribution
  - [ ] Recommended method/approach
- [ ] `docs/reports/survey/phase-scorecard.md` exists
- [ ] Phase score ≥ 3.5 (on 5-point scale)

**Quality Checks:**
- [ ] All cited papers verified via academic APIs (Semantic Scholar/arXiv/CrossRef)
- [ ] No fabricated citations
- [ ] User approval recorded in state file

### Gate 2: Pilot → Experiments

**Required Deliverables:**
- [ ] `docs/reports/pilot/pilot-validation-report.md` exists and contains:
  - [ ] Pilot experiment design
  - [ ] Implementation details
  - [ ] Preliminary results with error bars
  - [ ] Go/No-Go recommendation
- [ ] `docs/reports/pilot/phase-scorecard.md` exists
- [ ] Phase score ≥ 3.5

**Quality Checks:**
- [ ] Code runs without errors
- [ ] Pilot results are reproducible
- [ ] Method validated on pilot dataset
- [ ] User approval recorded in state file

### Gate 3: Experiments → Paper

**Required Deliverables:**
- [ ] `docs/reports/experiments/evidence-package-index.md` exists and contains:
  - [ ] Complete experiment configurations
  - [ ] All results with statistical analysis
  - [ ] Figures and tables for paper
  - [ ] Ablation studies (if applicable)
- [ ] `docs/reports/experiments/results-summary.md` exists
- [ ] `docs/reports/experiments/phase-scorecard.md` exists
- [ ] Phase score ≥ 3.5

**Quality Checks:**
- [ ] All claimed experiments actually run
- [ ] Results are reproducible with logged configs
- [ ] Checkpoints/saved models exist where claimed
- [ ] User approval recorded in state file

### Gate 4: Paper → Reflection

**Required Deliverables:**
- [ ] `paper/main.tex` exists and compiles without errors
- [ ] `paper/references.bib` exists with all citations
- [ ] `paper/citation-audit-report.md` exists with:
  - [ ] All citations verified authentic
  - [ ] No fabricated references
- [ ] `docs/reports/paper/final-acceptance-report.md` exists
- [ ] Phase score ≥ 3.5

**Quality Checks:**
- [ ] All figures readable and referenced
- [ ] No placeholder text (e.g., "TODO", "[insert figure]")
- [ ] Paper compiles to PDF successfully
- [ ] Citation audit passed (no fake papers)
- [ ] User approval recorded in state file

### Gate 5: Reflection → Close

**Required Deliverables:**
- [ ] `docs/reports/reflection/lessons-learned.md` exists and contains:
  - [ ] What worked well
  - [ ] What could be improved
  - [ ] Recommendations for future projects
- [ ] `docs/reports/reflection/runtime-improvement-report.md` exists
- [ ] `.autoresearch/archive/archive-index.md` exists

**Final Decisions:**
- [ ] Overlay activation decision made (yes/no)
- [ ] If yes: `python3 scripts/apply_overlay.py --project-root <path>`
- [ ] Project status set to `completed` in state file

### Gate Score Interpretation

| Score | Decision | Action |
|-------|----------|--------|
| 4.5-5.0 | Approve | Proceed to next phase immediately |
| 3.5-4.4 | Advance | Minor fixes needed, proceed after fix |
| 2.5-3.4 | Revise | Significant revision required, retry phase |
| 1.5-2.4 | Major Revise | Return to earlier phase, may need pivot |
| 0.0-1.4 | Pivot | Consider alternative approach or termination |

### Automatic Blockers

The following issues **automatically block gate approval** regardless of score:

**Gate 1 Blockers:**
- [ ] Any fabricated citation detected
- [ ] Novelty claim without supporting evidence
- [ ] Untestable hypothesis

**Gate 2 Blockers:**
- [ ] Pilot cannot validate hypothesis
- [ ] No clear recommendation from adviser
- [ ] Unaddressed failure modes

**Gate 3 Blockers:**
- [ ] Untraceable results (missing run IDs)
- [ ] Hidden negative results
- [ ] Unverified statistical claims

**Gate 4 Blockers:**
- [ ] Unsupported claims in manuscript
- [ ] Unverified citations (<90% verified)
- [ ] Suspected fabrication

**Gate 5 Blockers:**
- [ ] Silent policy changes proposed
- [ ] Undocumented overlays
- [ ] Missing safety rationale

### Scoring Dimensions Reference

Each gate is scored on these dimensions (see `references/gate-rubrics.md` for details):

| Gate | Dimension 1 (25%) | Dimension 2 (25%) | Dimension 3 (25%) | Dimension 4 (25%) |
|------|-------------------|-------------------|-------------------|-------------------|
| 1 | Citation Authenticity | Novelty | Literature Coverage | Idea Definition |
| 2 | Hypothesis Clarity | Pilot Design | Execution Quality | Decision Support |
| 3 | Result Traceability | Statistical Validity | Baseline Completeness | Negative Handling |
| 4 | Novelty | Evidence Strength | Theoretical Foundation | Writing Quality |
| 5 | Lessons Quality | Overlay Safety | Runtime Improvements | Documentation |

## Hard Rules

- Keep every phase as a two-agent loop under the user-facing orchestrator.
- **Do NOT spawn explore agents or other helper agents. Only the 2 designated phase agents.**
- **Do NOT use websearch for literature. Use academic database APIs (Semantic Scholar, arXiv, CrossRef, DBLP, OpenAlex).**
- Keep process documents in Chinese by default and manuscript-facing documents in English by default unless the user overrides this.
- Do not claim plagiarism checks, AI-detection checks, or formal proof verification in v1.
- Do not fabricate experiments, citations, datasets, checkpoints, or reviewer conclusions.
- Do not pivot or advance phases without explicit human approval at the phase boundary.
- When a human gate rejects the current phase, present the allowed return phases and a suggested return phase; do not roll back automatically without that human choice.
- Do not advance phases when `validate_handoff.py` or `quality_gate.py` reports failure or escalation.
- Escalate back to the user when a phase loop reaches its configured limit without approval.
- **Save handoff summaries when dismissing agents. Read them when resuming a phase.**

## Resource Map

- Read [references/workflow-protocol.md](references/workflow-protocol.md) for the end-to-end phase order.
- Read [references/system-architecture.md](references/system-architecture.md) for the inner-loop and outer-loop design.
- Read [references/orchestrator-protocol.md](references/orchestrator-protocol.md) for the Orchestrator's interaction protocols with researchers.
- Read [references/project-takeover-protocol.md](references/project-takeover-protocol.md) before taking over an existing project.
- Read [references/pivot-policy.md](references/pivot-policy.md) before proposing pivots.
- Read [references/progress-visualization.md](references/progress-visualization.md) before generating dashboards or runtime summaries.
- Read [references/remote-execution.md](references/remote-execution.md) before scheduling or running backend jobs.
- Read [references/self-healing.md](references/self-healing.md) before using sentinel or recovery actions.
- Read [references/self-evolution.md](references/self-evolution.md) before activating overlays.
- Read [references/phase-execution-details.md](references/phase-execution-details.md) for detailed substeps inside each phase.
- Read [references/citation-authenticity.md](references/citation-authenticity.md) before approving or revising paper-phase citations.
- Read [references/literature-verification.md](references/literature-verification.md) for survey-phase citation verification standards.
- Read [references/experiment-integrity.md](references/experiment-integrity.md) for experiment-phase integrity and logging standards.
- Read [references/paper-quality-assurance.md](references/paper-quality-assurance.md) for paper-phase quality and authenticity standards.
- Read [references/ai-researcher-agent-mapping.md](references/ai-researcher-agent-mapping.md) before assigning responsibilities to local roles.
- Read [references/prompt-customization.md](references/prompt-customization.md) before rendering or adjusting role prompts.
- Read [references/role-protocols.md](references/role-protocols.md) when role behavior needs to be strict.
- Read [references/gate-rubrics.md](references/gate-rubrics.md) before approving or rejecting a phase.
- Read [references/deliverable-contracts.md](references/deliverable-contracts.md) when deciding what each file must contain.
- Read [references/evidence-rules.md](references/evidence-rules.md) before using citations, codebases, datasets, logs, or figures as evidence.
- Use `assets/templates/` as the canonical source of workspace document skeletons.
- Use `assets/prompts/` as the canonical source of fixed role prompt templates.

## Cross-Session Feedback Channel

The skill supports cross-session collaboration via a shared feedback file located at a stable path that survives skill re-installations.

### Feedback File Location

- **Feedback**: `~/.claude/shared/ai-research-orchestrator-feedback.md`
- **Metadata**: `~/.claude/shared/ai-research-orchestrator-metadata.json`

### Report Feedback

```markdown
### [FEEDBACK-XXX] Issue Title
- **时间**: YYYY-MM-DD HH:MM
- **Session**: your-session-id
- **类型**: BUG / IMPROVEMENT / QUESTION
- **阶段**: current phase (e.g., 01-survey)
- **状态**: OPEN
- **描述**: detailed description
- **复现步骤**: steps to reproduce (if BUG)
- **期望行为**: expected behavior
- **实际行为**: actual behavior
```

### Check for Feedback

Periodically read `~/.claude/shared/ai-research-orchestrator-feedback.md` to see if other sessions have reported issues. Update status when working on or resolving feedback:

- `OPEN` → `IN_PROGRESS` (when starting work)
- `IN_PROGRESS` → `RESOLVED` (when fixed)
- `IN_PROGRESS` → `WONTFIX` (if not addressable)

This enables iterative improvement across multiple concurrent sessions without losing feedback on skill re-installation.
