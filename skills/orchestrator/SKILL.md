---
name: airesearchorchestrator:orchestrator
description: "Initialize and run a gated five-phase AI research project from idea through paper. Use when user says 'start research project', '帮我做一个研究', 'research workflow', '五阶段研究流程', 'research orchestrator', or needs structured AI/ML research management with Survey, Pilot, Experiments, Paper, and Reflection phases."
user-invocable: true
argument-hint: [research-topic-or-idea]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, Skill, TeamCreate, TeamDelete, TaskCreate, TaskUpdate, TaskGet, TaskList, SendMessage, mcp__codex__codex, mcp__codex__codex-reply
---
# AI Research Orchestrator

## Overview

This skill turns a loose research request into a controlled five-phase project with fixed directories, scored gate checks, visible progress artifacts, and explicit human approval between phases. It is optimized for AI/ML algorithm research that needs literature review, pilot validation, experiments, paper writing, and controlled post-project reflection without losing provenance.

## Agent Teams: Team Lead Role

The Orchestrator acts as **Team Lead** in the Agent Teams architecture. Each phase is managed as a team with direct agent-to-agent communication.

### Phase Lifecycle (Team Lead Pattern)

```
1. TeamCreate(team_name="research-<phase>", description="<phase> phase team")
2. TaskCreate for primary task (e.g., task_id="<phase>-primary")
3. TaskCreate for reviewer task with blockedBy=["<phase>-primary"]
4. Agent(..., team_name="research-<phase>") — spawn Primary
5. TaskUpdate(taskId="<phase>-primary", owner="<primary-agent-name>")
6. Agent(..., team_name="research-<phase>") — spawn Reviewer
7. TaskUpdate(taskId="<phase>-reviewer", owner="<reviewer-agent-name>")
8. Monitor with TaskGet / TaskList
9. (Phase complete) SendMessage shutdown to both agents
10. TeamDelete(team_name="research-<phase>")
```

### Team Create / Task Create / Assign Pattern

```python
# 1. Create the team for this phase
TeamCreate(team_name="research-survey", description="Survey phase: literature review and novelty check")

# 2. Create tasks with dependency chain
TaskCreate(
  taskId="survey-primary",
  title="Survey Agent: literature review and idea definition",
  description="Run define-idea, research-lit, novelty-check skills"
)
TaskCreate(
  taskId="survey-reviewer",
  title="Critic Agent: audit survey deliverables",
  description="Run audit-survey, audit-derivation skills",
  blockedBy=["survey-primary"]
)

# 3. Spawn agents with team membership
Agent(
  subagent_type="airesearchorchestrator:survey",
  name="survey",
  team_name="research-survey",
  prompt="..."
)
Agent(
  subagent_type="airesearchorchestrator:critic",
  name="critic",
  team_name="research-survey",
  prompt="..."
)

# 4. Assign tasks to agents
TaskUpdate(taskId="survey-primary", owner="survey")
TaskUpdate(taskId="survey-reviewer", owner="critic")

# 5. Monitor
TaskList(team_name="research-survey")
TaskGet(taskId="survey-primary")
```

### Phase Shutdown Sequence

Before calling TeamDelete, always send shutdown signals:

```python
SendMessage(to="survey",  message={"type": "shutdown_request", "reason": "Phase complete, gate approved"})
SendMessage(to="critic",  message={"type": "shutdown_request", "reason": "Phase complete, gate approved"})
TeamDelete(team_name="research-survey")
```

### Agent Pairs by Phase

| Phase | Primary Agent | Reviewer Agent | Team Name |
|-------|--------------|----------------|-----------|
| Survey | `survey` | `critic` | `research-survey` |
| Pilot | `coder` | `adviser` | `research-pilot` |
| Experiments | `coder` | `adviser` | `research-experiments` |
| Paper | `writer` | `reviewer` | `research-paper` |
| Reflection | `reflector` | `curator` | `research-reflection` |

### Key Benefit: Direct Agent Communication

Agents in the same team can use `SendMessage` to communicate **directly** without routing through the Orchestrator. The Orchestrator only intervenes when escalation is required (e.g., battle fails to reach consensus after 3 rounds).

---

## ⚠️ CRITICAL: Agent Invocation

**You are the orchestrator. Your PRIMARY job is to invoke and coordinate agents via the Agent Teams pattern.**

### What This Means

1. **DO NOT just run scripts** — Running `run_stage_loop.py` only updates state; it does NOT do the actual work
2. **You MUST use the Agent tool with team_name** — Spawn agents into teams so they can communicate directly
3. **Each phase has two agents** — Primary (doer) and Reviewer (auditor)

### Correct Workflow

```
1. Run script to initialize phase state
2. TeamCreate for this phase
3. TaskCreate for primary and reviewer tasks (with blockedBy dependency)
4. Spawn Primary agent with team_name; assign task via TaskUpdate
5. Primary completes work, notifies Reviewer via SendMessage
6. Spawn Reviewer agent with team_name; assign task via TaskUpdate
7. Reviewer sends audit_report to Primary via SendMessage
8. Agents battle directly if needed (up to 3 rounds via SendMessage)
9. Check gate score (TaskList / TaskGet or read deliverables)
10. If score < 3.5, loop back to Primary with feedback
11. If score >= 3.5, present gate to human for approval
12. After human approval: send shutdown_request, TeamDelete, advance phase
```

### Example Agent Invocation (Agent Teams Pattern)

```python
# Spawn Primary agent into the phase team
Agent(
  subagent_type="airesearchorchestrator:survey",
  name="survey",
  team_name="research-survey",
  prompt="""
You are the Survey agent for project at /path/to/project.

Your role: Conduct literature review...

Tasks:
1. Read the idea brief
2. Search academic APIs
3. Define atomic definitions
4. Produce research-readiness-report.md

When done, notify the Critic agent:
  SendMessage(to="critic", message={"type": "deliverables_ready", "phase": "survey", "deliverables": [...]})

Write to agents/survey/ and docs/survey/.
"""
)

# Spawn Reviewer agent into the same team
Agent(
  subagent_type="airesearchorchestrator:critic",
  name="critic",
  team_name="research-survey",
  prompt="""
You are the Critic agent for project at /path/to/project.

Wait for a deliverables_ready message from the survey agent, then audit.
Send your audit report back:
  SendMessage(to="survey", message={"type": "audit_report", "decision": "...", "issues": [...]})
"""
)
```

### Common Mistakes to Avoid

❌ **WRONG**: Just run script, then say "phase complete"
❌ **WRONG**: Do the literature search yourself without spawning survey agent
❌ **WRONG**: Update state but never invoke agents
❌ **WRONG**: Relay battle messages yourself — agents communicate directly via SendMessage
❌ **WRONG**: Call TeamDelete without sending shutdown_request first

✅ **CORRECT**: TeamCreate → TaskCreate → Spawn agents with team_name → Assign tasks → Monitor → shutdown_request → TeamDelete → Advance

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
└── docs/                    # Phase deliverables
    ├── survey/
    ├── pilot/
    ├── experiments/
    ├── paper/
    └── reflection/
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

2. **Intent Clarification** (Recommended): Use interactive mode to clarify your research intent:

```bash
python3 scripts/init_research_project.py \
  --project-root /abs/path/to/my-project \
  --interactive
```

This runs the intent clarification process:
- Assesses clarity of your research idea
- Asks targeted questions based on information gaps
- Generates `research-intent-confirmation.md`

3. **Non-Interactive Initialization** (Advanced): Skip clarification if your idea is well-formed:

```bash
python3 scripts/init_research_project.py \
  --project-root /abs/path/to/my-project \
  --topic "Your research idea or problem statement" \
  --client-type auto \
  --skip-clarification
```

4. (Optional) Specify a starting phase if resuming work or skipping completed phases:

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

**Vague Idea?** If your research idea is unclear, use `--force-brainstorm` to invoke the ideation skill:

```bash
python3 scripts/init_research_project.py \
  --project-root /abs/path/to/my-project \
  --topic "I want to do NLP research" \
  --force-brainstorm
```

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

The orchestrator includes 41 skills organized into Primary Skills (workflow execution), Audit Skills (quality verification), and Supporting Skills (workflow automation).

### Primary Skills (16)

These skills execute the research workflow phases:

| Skill | Agent | Output | Purpose |
|-------|-------|--------|---------|
| `define-idea` | Survey | `docs/survey/idea-definition.md` | Formulate research hypothesis |
| `research-plan` | Survey | `docs/survey/research-readiness-report.md` | Create research execution plan |
| `research-lit` | Survey | Working notes | Literature survey using academic APIs |
| `novelty-check` | Survey | Novelty report | Verify novelty against existing work |
| `analyze-problem` | Code | `docs/pilot/problem-analysis.md` | Analyze research problem |
| `design-pilot` | Code | `docs/pilot/pilot-design.md` | Design pilot experiment |
| `run-pilot` | Code | `docs/pilot/pilot-validation-report.md` | Execute pilot experiment |
| `design-exp` | Code | `docs/experiments/experiment-spec.md` | Design full experiment matrix |
| `run-experiment` | Code | Experiment logs | Deploy and run ML experiments |
| `monitor-experiment` | Code | Progress reports | Monitor running experiments |
| `analyze-results` | Code | Results summary | Analyze experiment results |
| `paper-plan` | Writer | `paper/PAPER_PLAN.md` | Create paper outline |
| `paper-write` | Writer | `paper/main.tex` | Write paper sections |
| `curate-citation` | Writer | `paper/citation-index.md` | Finalize and verify citations |
| `extract-lessons` | Reflector | `docs/reflection/lessons-learned.md` | Extract lessons learned |
| `propose-overlay` | Reflector | `docs/reflection/overlay-draft.md` | Propose system improvements |

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
| `paper-pipeline` | Full paper writing pipeline |
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
/autoresearch:paper-pipeline "NARRATIVE_REPORT.md"

# Sub-skills (invoked by paper-pipeline)
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
  Produce `docs/survey/research-readiness-report.md` and `docs/survey/phase-scorecard.md`, then stop for Gate 1.
- Phase 2: `Code <-> Adviser` for pilot analysis
  Produce `docs/pilot/pilot-validation-report.md` and `docs/pilot/phase-scorecard.md`, then stop for Gate 2.
- Phase 3: `Code <-> Adviser` for full experiments
  Produce `docs/experiments/evidence-package-index.md` and `docs/experiments/phase-scorecard.md`, then stop for Gate 3.
- Phase 4: `Paper Writer <-> Reviewer & Editor`
  Produce `paper/citation-audit-report.md`, `paper/final-acceptance-report.md`, and `paper/phase-scorecard.md`, then stop for Gate 4.
- Phase 5: `Reflector <-> Curator`
  Produce `docs/reflection/runtime-improvement-report.md` and `docs/reflection/phase-scorecard.md`, then stop for Gate 5 before any overlay or policy change is activated.

## Agent-Driven Architecture

### Core Principle: Orchestrator Acts as Team Lead, Never Executes

**The Orchestrator is the Team Lead, not an executor.** The Orchestrator NEVER directly performs research tasks. All research work is delegated to specialized agents spawned into phase teams, where they communicate directly with each other.

```
CORRECT Architecture (Agent Teams):
┌─────────────────────────────────────────────────────────────────┐
│              Orchestrator (Team Lead / Main Session)             │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  Team Lead Responsibilities:                                │ │
│  │  • TeamCreate / TeamDelete per phase                        │ │
│  │  • TaskCreate / TaskUpdate (assign, monitor)                │ │
│  │  • Spawn agents with team_name                              │ │
│  │  • Send shutdown_request before TeamDelete                  │ │
│  │  • Coordinate phase transitions                             │ │
│  │  • Present gates to human for decision                      │ │
│  │  • Maintain state file                                      │ │
│  │  • Handle human interaction                                 │ │
│  │  • Arbitrate only when battle escalates (blocked task)      │ │
│  └─────────────────────────────────────────────────────────────┘ │
│         │ spawn+assign             │ spawn+assign               │
│         ▼                          ▼                            │
│  ┌─────────────┐     SendMessage  ┌─────────────┐              │
│  │ Survey Agent│ ◀──────────────▶ │ Critic Agent│              │
│  │  (Primary)  │  (direct, no     │  (Reviewer) │              │
│  │team_name=.. │   relay needed)  │team_name=.. │              │
│  └─────────────┘                  └─────────────┘              │
│         │                               │                       │
│         ▼                               ▼                       │
│  research-lit skill            audit-survey skill               │
└─────────────────────────────────────────────────────────────────┘

WRONG Architecture (DO NOT DO THIS):
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestrator (Main Session)                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  ❌ Directly executing research-lit                          │ │
│  │  ❌ Directly writing survey reports                         │ │
│  │  ❌ Directly running experiments                            │ │
│  │  ❌ Directly writing paper sections                          │ │
│  │  ❌ Relaying battle messages between agents                  │ │
│  │  ❌ Calling TeamDelete without shutdown_request first        │ │
│  │  ❌ Spawning agents without team_name                        │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Dispatch Pattern (Agent Teams)

Each phase follows a **Primary Agent + Reviewer Agent** pattern, spawned into a named team. Agents communicate directly via SendMessage.

**Spawn pattern:**
```python
Agent(
  subagent_type="airesearchorchestrator:<role>",
  name="<role>",
  team_name="research-<phase>",
  prompt="..."
)
```

| Phase | Primary Agent | Reviewer Agent | Team Name | Primary Skill | Reviewer Skill |
|-------|---------------|----------------|-----------|---------------|----------------|
| Survey | Survey Agent | Critic Agent | `research-survey` | `define-idea`, `theoretical-derivation`, `research-lit`, `novelty-check` | `audit-derivation`, `audit-survey` |
| Pilot | Code Agent | Adviser Agent | `research-pilot` | `analyze-problem`, `design-pilot`, `run-pilot` | `audit-analysis`, `audit-design`, `audit-pilot` |
| Experiments | Code Agent | Adviser Agent | `research-experiments` | `design-exp`, `run-experiment`, `analyze-results` | `audit-exp-design`, `audit-results` |
| Paper | Writer Agent | Reviewer Agent | `research-paper` | `paper-plan`, `paper-write`, `curate-citation` | `audit-paper-plan`, `audit-paper`, `audit-citation` |
| Reflection | Reflector Agent | Curator Agent | `research-reflection` | `extract-lessons`, `propose-overlay` | `audit-lessons`, `audit-overlay` |

### Survey Phase Workflow (Updated with Theoretical Derivation)

The Survey Phase now includes theoretical derivation:

```
define-idea → theoretical-derivation → audit-derivation → [BATTLE] → research-lit → audit-survey → [BATTLE] → Gate 1
                    ↑                         │
                    └─────────────────────────┘
                          May iterate based on battle outcome
```

### Task State Management

Subagent tasks follow a strict state machine:

```
                    ┌──────────────┐
                    │   PENDING    │  Task created, waiting to be assigned
                    └──────┬───────┘
                           │ spawn subagent
                           ▼
                    ┌──────────────┐
           ┌───────│  IN_PROGRESS │  Subagent actively working
           │       └──────┬───────┘
           │              │
    timeout/         success│           │failure
    retry_limit             ▼           ▼
           │       ┌──────────────┐  ┌──────────────┐
           └──────▶│  COMPLETED   │  │   FAILED     │
                   └──────────────┘  └──────┬───────┘
                                             │ retry? │
                                             ▼       │
                                      ┌──────────────┐
                                      │   RETRYING   │
                                      └──────┬───────┘
                                             │ respawn
                                             ▼
                                      ┌──────────────┐
                                      │  IN_PROGRESS │
                                      └──────────────┘
```

**State Definitions:**

| State | Description | Orchestrator Action |
|-------|-------------|---------------------|
| `PENDING` | Task queued, no agent assigned | Spawn subagent with task |
| `IN_PROGRESS` | Subagent actively working | Monitor progress, collect results |
| `COMPLETED` | Task finished successfully | Record results, dismiss subagent |
| `FAILED` | Task failed with error | Log error, decide retry or escalate |
| `RETRYING` | Failed task being retried | Respawn subagent with same task |

**Task State Transitions:**

```yaml
# Example state tracking in research-state.yaml
current_phase: survey
phase_status:
  survey:
    state: in_progress
    tasks:
      - task_id: survey-001
        skill: research-lit
        agent: survey-agent
        state: completed
        result_path: docs/survey/literature-review.md
      - task_id: survey-002
        skill: audit-survey
        agent: critic-agent
        state: in_progress
        started_at: "2024-01-15T10:30:00Z"
```

### Gate Decision Workflow (with Battle Phase)

Gates are **human decision points** after collecting subagent results. The workflow now includes a **Battle Phase** where the Primary Agent can challenge the Reviewer's findings.

```
Phase Execution                    Battle Phase              Gate Decision
────────────────────────────────────────────────────────────────────────────────

┌─────────────┐    spawn    ┌─────────────┐
│ Orchestrator│────────────▶│ Primary     │
│             │             │ Agent       │
└─────────────┘             └──────┬──────┘
      │                            │ complete
      │                            ▼
      │                     ┌─────────────┐
      │                     │ Primary     │
      │                     │ Results     │
      │                     └──────┬──────┘
      │                            │ collect
      │                            ▼
      │    spawn            ┌─────────────┐
      ├───────────────────▶│ Reviewer    │
      │                    │ Agent       │
      │                    └──────┬──────┘
      │                            │ complete
      │                            ▼
      │                     ┌─────────────┐
      │                     │ Reviewer    │
      │                     │ Results     │
      │                     └──────┬──────┘
      │                            │
      │                            ▼
      │                     ┌─────────────┐
      │    notify           │   BATTLE    │◀── NEW: Challenge Phase
      ├───────────────────▶│   PHASE     │
      │                    └──────┬──────┘
      │                           │
      │            ┌──────────────┼──────────────┐
      │            │              │              │
      │            ▼              ▼              ▼
      │     ┌──────────┐   ┌──────────┐   ┌──────────┐
      │     │ Consensus│   │ Primary  │   │ Reviewer │
      │     │ Reached  │   │ Defends  │   │ Replies  │
      │     └────┬─────┘   └────┬─────┘   └────┬─────┘
      │          │              │              │
      │          │              └──────┬───────┘
      │          │                     │
      │          ▼                     ▼
      │   ┌─────────────┐       ┌─────────────┐
      │   │ Aggregate   │       │ Orchestrator│
      │   │ Results     │       │ Arbitrates  │
      │   └──────┬──────┘       └──────┬──────┘
      │          │                     │
      │          │              ┌──────┴──────┐
      │          │              │             │
      │          │              ▼             ▼
      │          │       ┌──────────┐  ┌──────────┐
      │          │       │ Decision │  │  Escalate│
      │          │       │  Made    │  │ to Human │
      │          │       └────┬─────┘  └────┬─────┘
      │          │            │             │
      │          ▼            ▼             ▼
      │   ┌─────────────┐                     │
      └──▶│   GATE      │◀────────────────────┘
          │  Decision   │
          └──────┬──────┘
                 │
                  ┌──────────────┼──────────────┐
                  │              │              │
                  ▼              ▼              ▼
            ┌──────────┐  ┌──────────┐  ┌──────────┐
            │ APPROVE  │  │  REVISE  │  │  PIVOT   │
            │ (next)   │  │  (retry) │  │ (back)   │
            └──────────┘  └──────────┘  └──────────┘
```

### Battle Resolution Protocol

After the Reviewer Agent produces an audit report, the workflow enters the **Battle Phase**:

#### Step 1: Present Review to Primary Agent

The Orchestrator sends the Reviewer's findings to the Primary Agent:

```yaml
# Battle notification to Primary Agent
battle_phase:
  type: "review_presentation"
  reviewer_findings:
    critical_issues: [...]
    major_issues: [...]
    gate_decision: "REVISE"
  options:
    - "ACCEPT: Accept all findings and revise"
    - "CHALLENGE: Contest specific findings"
```

#### Step 2: Primary Agent Response

The Primary Agent can choose:

| Response | Description | Next Step |
|----------|-------------|-----------|
| `ACCEPT_ALL` | Accept all reviewer findings | Proceed to revision |
| `ACCEPT_PARTIAL` | Accept some, note disagreements | Document disagreements, proceed |
| `CHALLENGE` | Formally challenge findings | Enter formal debate |

**Challenge Format:**

```yaml
challenge:
  type: "formal_challenge"
  issues_contested:
    - point_id: "critical-1"
      primary_position: "This is not actually a critical issue because..."
      evidence: "[Supporting argument]"
    - point_id: "major-2"
      primary_position: "The reviewer misunderstood the approach..."
      evidence: "[Clarification]"
  max_rounds: 3  # Maximum debate rounds
```

#### Step 3: Reviewer Response to Challenge

The Reviewer Agent responds to each contested issue:

```yaml
challenge_response:
  type: "reviewer_rebuttal"
  responses:
    - point_id: "critical-1"
      reviewer_position: "I maintain this is critical because..."
      counter_evidence: "[Counter-argument]"
      stance: "UPHELD" | "MODIFIED" | "WITHDRAWN"
    - point_id: "major-2"
      reviewer_position: "I acknowledge the clarification, but..."
      stance: "MODIFIED"
      revised_severity: "minor"
```

#### Step 4: Consensus Check

After each round, check for consensus:

```yaml
consensus_check:
  round: 1
  agreed_issues: [issue-1, issue-3]
  disputed_issues: [issue-2, issue-4]
  consensus_reached: false
  next_action: "continue_debate" | "arbitrate" | "escalate"
```

#### Step 5: Orchestrator Arbitration

If consensus is NOT reached after max rounds (default: 3), the Orchestrator arbitrates:

```yaml
arbitration:
  type: "orchestrator_decision"
  disputed_issues:
    - point_id: "issue-2"
      primary_argument: "..."
      reviewer_argument: "..."
  orchestrator_ruling:
    - point_id: "issue-2"
      decision: "UPHOLD_REVIEWER" | "UPHOLD_PRIMARY" | "COMPROMISE"
      reasoning: "..."
      final_severity: "critical" | "major" | "minor" | "dismissed"
```

#### Step 6: Escalation to Human

If the Orchestrator CANNOT make a confident ruling:

```yaml
escalation:
  type: "human_escalation"
  reason: "Unable to determine technical validity without domain expertise"
  summary:
    - issue: "..."
      primary_position: "..."
      reviewer_position: "..."
      orchestrator_assessment: "Both positions have merit"
  questions_for_human:
    - "Is assumption A realistic for our use case?"
    - "Does the proof sketch adequately cover the edge case?"
```

### Battle State Machine

```
                    ┌──────────────────┐
                    │ Review Complete  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Present to       │
                    │ Primary Agent    │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
       ┌────────────┐ ┌────────────┐ ┌────────────┐
       │ ACCEPT_ALL │ │ ACCEPT_    │ │  CHALLENGE │
       │            │ │ PARTIAL    │ │            │
       └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
             │              │              │
             │              │              ▼
             │              │      ┌───────────────┐
             │              │      │ Debate Round  │
             │              │      │ (max 3)       │
             │              │      └───────┬───────┘
             │              │              │
             │              │       ┌──────┴──────┐
             │              │       │             │
             │              │       ▼             ▼
             │              │ ┌───────────┐ ┌───────────┐
             │              │ │ Consensus │ │ Disputed  │
             │              │ │ Reached   │ │ Issues    │
             │              │ └─────┬─────┘ └─────┬─────┘
             │              │       │             │
             │              │       │      ┌──────┴──────┐
             │              │       │      │             │
             │              │       │      ▼             ▼
             │              │       │ ┌──────────┐ ┌──────────┐
             │              │       │ │Arbitrate │ │ Escalate │
             │              │       │ │          │ │ to Human │
             │              │       │ └────┬─────┘ └────┬─────┘
             │              │       │      │           │
             └──────────────┴───────┴──────┴───────────┘
                                         │
                                         ▼
                                  ┌─────────────┐
                                  │   GATE      │
                                  │  Decision   │
                                  └─────────────┘
```

### Battle Communication Protocol

> **Agent Teams Architecture**: Agents battle **directly** via SendMessage. The Orchestrator does NOT relay messages during battle. Orchestrator only intervenes when `status="blocked"` is set (escalation after 3 rounds).

**Primary Agent → Reviewer Agent (Challenge):**
```python
SendMessage(
  to="<reviewer>",
  message={
    "type": "battle_challenge",
    "disputed_points": [
      {"point_id": "crit-1", "position": "This finding is incorrect because...", "evidence": "[Supporting details]"},
    ]
  }
)
```

**Reviewer Agent → Primary Agent (Battle Response):**
```python
SendMessage(
  to="<primary>",
  message={
    "type": "battle_response",
    "responses": [
      {"point_id": "crit-1", "stance": "upheld" | "modified" | "withdrawn",
       "reasoning": "[Why upheld/modified/withdrawn]", "revised_severity": "major"}
    ]
  }
)
```

**Agent → Orchestrator (Escalation after max rounds):**
```python
# Either agent sets task to blocked when battle fails to converge
TaskUpdate(taskId="<phase>-reviewer", status="blocked", reason="No consensus after 3 battle rounds")
```

**Orchestrator → Both Agents (Arbitration — only after escalation):**
```python
SendMessage(
  to="<primary>",
  message={
    "type": "arbitration_ruling",
    "disputed_issues": [
      {"point_id": "...", "ruling": "uphold_reviewer" | "uphold_primary" | "compromise",
       "reasoning": "[Technical justification]", "final_severity": "..."}
    ],
    "mandatory": True
  }
)
SendMessage(to="<reviewer>", message={"type": "arbitration_ruling", ...})  # same ruling
```

**Orchestrator → Human (Escalation when Orchestrator cannot rule):**
```yaml
message_type: "human_escalation"
escalation_id: "esc-001"
phase: "survey"
summary: "[Summary of the dispute]"
positions:
  primary: "[Primary Agent's position]"
  reviewer: "[Reviewer Agent's position]"
questions:
  - "[Question for human to decide]"
decision_options:
  - "uphold_reviewer"
  - "uphold_primary"
  - "compromise"
  - "request_more_analysis"
```

## Agent Teams Communication Protocol

When Agent Teams is enabled (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), agents operate as
teammates that communicate **directly** via SendMessage. The Orchestrator does NOT relay messages
between agents; it only intervenes when escalation is required.

### Team Setup per Phase

At phase start, the Orchestrator (as Team Lead):
1. `TeamCreate(team_name="research-<phase>", description="...")` — create the phase team
2. `TaskCreate(taskId="<phase>-primary", ...)` — primary task
3. `TaskCreate(taskId="<phase>-reviewer", ..., blockedBy=["<phase>-primary"])` — reviewer task, blocked until primary done
4. `Agent(subagent_type="airesearchorchestrator:<role>", name="<role>", team_name="research-<phase>", prompt="...")` — spawn Primary
5. `TaskUpdate(taskId="<phase>-primary", owner="<role>")` — assign task to Primary
6. `Agent(subagent_type="airesearchorchestrator:<reviewer>", name="<reviewer>", team_name="research-<phase>", prompt="...")` — spawn Reviewer
7. `TaskUpdate(taskId="<phase>-reviewer", owner="<reviewer>")` — assign task to Reviewer

### Direct Agent-to-Agent Communication

Agents in the same team communicate directly — the Orchestrator does NOT relay these messages:

**Primary → Reviewer (deliverables ready):**
```python
SendMessage(
  to="<reviewer>",
  message={"type": "deliverables_ready", "phase": "<phase>", "deliverables": [...], "summary": "..."}
)
```

**Reviewer → Primary (audit report):**
```python
SendMessage(
  to="<primary>",
  message={"type": "audit_report", "decision": "approve" | "revise" | "reject", "issues": [...]}
)
```

**Primary → Reviewer (battle challenge):**
```python
SendMessage(
  to="<reviewer>",
  message={"type": "battle_challenge", "disputed_points": [
    {"point_id": "...", "position": "...", "evidence": "..."}
  ]}
)
```

**Reviewer → Primary (battle response):**
```python
SendMessage(
  to="<primary>",
  message={"type": "battle_response", "responses": [
    {"point_id": "...", "stance": "upheld" | "modified" | "withdrawn", "reasoning": "..."}
  ]}
)
```

**Agent escalates to Orchestrator (battle unresolved after 3 rounds):**
```python
TaskUpdate(taskId="<phase>-reviewer", status="blocked", reason="Battle unresolved after 3 rounds")
```
The Orchestrator detects the blocked status and performs arbitration or human escalation.

### Orchestrator Role During Battle

- **Orchestrator does NOT relay messages** between Primary and Reviewer during battle
- Agents battle directly via SendMessage (up to 3 rounds)
- Orchestrator only intervenes when:
  - A task is marked `status="blocked"` (battle escalation)
  - No consensus after 3 rounds (Orchestrator arbitrates)
  - Orchestrator cannot arbitrate confidently (escalate to human)

### Phase Shutdown Sequence

After gate approval, before TeamDelete:
```python
SendMessage(to="<primary>",  message={"type": "shutdown_request", "reason": "Phase complete, gate approved"})
SendMessage(to="<reviewer>", message={"type": "shutdown_request", "reason": "Phase complete, gate approved"})
TeamDelete(team_name="research-<phase>")
```

### Battle Rules

1. **Max Rounds**: Maximum 3 debate rounds before arbitration
2. **Evidence Required**: Each challenge must include supporting evidence
3. **Good Faith**: Agents must argue in good faith, not just defend ego
4. **Orchestrator Neutral**: Orchestrator arbitrates based on technical merit
5. **Human Supreme**: Human escalation overrides all agent decisions
6. **Document Everything**: All battle exchanges are logged in state file

### Battle Record in State File

```yaml
battle_history:
  phase: survey
  started_at: "2024-01-15T14:00:00Z"
  rounds:
    - round: 1
      primary_challenges:
        - point_id: "crit-1"
          position: "..."
          evidence: "..."
      reviewer_responses:
        - point_id: "crit-1"
          stance: "upheld"
          reasoning: "..."
    - round: 2
      ...
  outcome:
    type: "arbitrated" | "consensus" | "escalated"
    final_issues:
      - point_id: "crit-1"
        final_severity: "major"  # Reduced from critical
        resolution: "compromise"
  resolution_at: "2024-01-15T15:30:00Z"
```

### Orchestrator Prohibitions

The Orchestrator MUST NOT:

| Prohibition | Reason | Correct Approach |
|-------------|--------|------------------|
| ❌ Execute `research-lit` directly | Survey work requires domain expertise | Spawn Survey Agent with team_name |
| ❌ Execute `audit-survey` directly | Review requires independent perspective | Spawn Critic Agent with team_name |
| ❌ Write survey reports directly | Research synthesis needs focused agent | Delegate to Survey Agent |
| ❌ Run experiments directly | Experiment execution needs isolation | Spawn Code Agent with team_name |
| ❌ Write paper sections directly | Writing requires dedicated focus | Spawn Writer Agent with team_name |
| ❌ Make gate decisions autonomously | Human oversight is mandatory | Present options, await human input |
| ❌ Skip phase gates | Quality control requires checkpoints | Always pause at gates |
| ❌ Spawn helper/explore agents | Only 2 agents per phase allowed | Stick to Primary + Reviewer pattern |
| ❌ Auto-proceed without human approval | Research direction requires human judgment | Wait for explicit approval |
| ❌ Relay battle messages between agents | Agents communicate directly in a team | Let agents use SendMessage directly |
| ❌ Call TeamDelete without shutdown_request | Agents need graceful shutdown signal | Send shutdown_request to both agents first |
| ❌ Spawn agents without team_name | Agents must be in a team to use SendMessage | Always pass `team_name="research-<phase>"` |

### Agent Communication Protocol

When dispatching a subagent, the Orchestrator provides:

```yaml
# Subagent dispatch context
dispatch:
  task_id: "survey-001"
  skill: "research-lit"
  role: "survey"
  context:
    research_topic: "..."
    current_phase: "survey"
    handoff_summary: "..." # if resuming
  deliverables:
    - "docs/survey/literature-review.md"
    - "docs/survey/novelty-report.md"
  constraints:
    max_iterations: 5
    timeout_minutes: 60
    required_apis:
      - "semantic-scholar"
      - "arxiv"
```

When a subagent completes, it returns:

```yaml
# Subagent completion report
completion:
  task_id: "survey-001"
  status: "completed"  # or "failed"
  deliverables:
    - path: "docs/survey/literature-review.md"
      status: "created"
      summary: "Reviewed 15 papers on attention mechanisms"
  errors: []  # populated if failed
  recommendations:
    - "Consider expanding to transformer variants"
```

### Agent Lifecycle Management

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Lifecycle                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. SPAWN                                                    │
│     │                                                        │
│     │  Orchestrator:                                         │
│     │  - Generate task_id                                   │
│     │  - Select appropriate skill                           │
│     │  - Provide context and deliverables                    │
│     │  - Record PENDING state                               │
│     │                                                        │
│     ▼                                                        │
│  2. MONITOR                                                  │
│     │                                                        │
│     │  Orchestrator:                                         │
│     │  - Track progress via state file                      │
│     │  - Check for timeout                                   │
│     │  - Collect intermediate results                        │
│     │                                                        │
│     ▼                                                        │
│  3. COLLECT                                                  │
│     │                                                        │
│     │  Orchestrator:                                         │
│     │  - Gather deliverables                                 │
│     │  - Record completion status                            │
│     │  - Save handoff summary if dismissing                  │
│     │                                                        │
│     ▼                                                        │
│  4. DISMISS                                                  │
│     │                                                        │
│     │  Orchestrator:                                         │
│     │  - Clear agent context                                 │
│     │  - Update state file                                   │
│     │  - Prepare for next phase or retry                    │
│     │                                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Gate Score Presentation Protocol

When `quality_gate.py` returns results, the Orchestrator MUST follow this 4-step procedure before asking the researcher what to do next. Never skip directly to asking "what do you want to do?" — always show the score card first.

### Step 1: Display the Score Card

Present the gate result as a formatted score card. Map `decision` to an interpretation using the table below.

```
Gate [N] Score Card
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase        : [phase]       Gate: [gate]
Loop count   : [loop_count] / [loop_limit]

Evidence completeness : [evidence_completeness]%
Review readiness      : [review_readiness]%
Human gate            : [human_gate]%

Overall decision: [DECISION_LABEL]
```

Decision label mapping:

| `decision` value | Label to display |
|-----------------|-----------------|
| `advance` | ✅ ADVANCE — all criteria met, ready to proceed |
| `revise` | 🔄 REVISE — work is incomplete, continue this phase |
| `pivot` | ⚠️  PIVOT — reviewer flagged fundamental problems |
| `escalate_to_user` | 🔔 ESCALATE — loop limit reached, your decision required |

### Step 2: Explain Each Blocker in Plain Language

For each entry in the `blockers` list, show a human-readable explanation:

| Blocker key | Plain-language explanation |
|-------------|---------------------------|
| `required_deliverables_missing` | "The following required files have not been created yet: [list missing_deliverables]" |
| `deliverables_still_template` | "The following files still contain placeholder text and need real content: [list placeholder_deliverables]" |
| `structured_gate_signals_invalid` | "The phase scorecard contains invalid or missing structured signals" |
| `phase_review_pending` | "The reviewer agent has not submitted an approval yet" |
| `phase_review_revise` | "The reviewer agent has requested revisions" |
| `user_gate_pending` | "This gate is waiting for your explicit approval" |
| `loop_limit_reached` | "This phase has used all [loop_limit] allowed loops without approval" |

If `blockers` is empty: say "No blockers — all quality criteria are satisfied."

### Step 3: Present Three Named Options

Always present exactly these three options, but grey out any that are not applicable given the current `decision`:

```
What would you like to do next?

  A) CONTINUE  — accept the current result and move to the next phase
     [Show only if decision == "advance". Otherwise: "⛔ Not available until all blockers are resolved"]

  B) REVISE    — stay in this phase and address the blockers
     [Always available]
     Suggested focus areas: [derived from blockers, e.g. "complete pilot-validation-report.md"]
     Loops remaining: [loop_limit - loop_count]

  C) PIVOT     — change research direction or roll back to an earlier phase
     [Always available]
     Allowed rollback targets: [allowed_return_phases from state, or survey/pilot as defaults]

Please reply with A, B, or C.
```

### Step 4: Execute the Chosen Action

| Choice | Action |
|--------|--------|
| **A — CONTINUE** | Run: `python3 scripts/run_stage_loop.py --project-root [root] --gate-status approved` then transition to the next phase |
| **B — REVISE** | Run: `python3 scripts/run_stage_loop.py --project-root [root] --review-status revise` then present the specific revision targets from the blockers list |
| **C — PIVOT** | Ask: "Which phase do you want to return to? [list allowed targets]" then run: `python3 scripts/run_stage_loop.py --project-root [root] --gate-status rejected --return-phase [chosen]` |

### Critical Integrity Rules

1. **Never present option A as available when `decision != "advance"`**. Allowing premature advancement corrupts the research record.
2. **Never skip Steps 1–3 and jump straight to action**. The researcher must see the full picture before deciding.
3. **Never make the decision autonomously**. Even when `decision == "advance"`, wait for the researcher to type "A" or equivalent confirmation.
4. **Document the decision**: After the researcher chooses, confirm: "Recorded: [choice] for [gate]. [Description of what happens next]."

---

## Phase Gate Checklist

Before advancing to the next phase, ALL items in the corresponding gate checklist must be verified.

### Gate 0: Initialization Check

#### Mandatory Requirements
- [ ] `.autoresearch/state/research-state.yaml` exists and is valid
- [ ] `.autoresearch/config/orchestrator-config.yaml` exists
- [ ] Required directories created (`paper/`, `code/`, `docs/`, `agents/`)
- [ ] `AGENTS.md` or `CLAUDE.md` generated at project root

#### Intent Confirmation (One Required)
- [ ] **Option A:** `.autoresearch/research-intent-confirmation.md` exists with confirmed intent
- [ ] **Option B:** `--skip-clarification` flag used with explicit acknowledgment

#### Intent Clarification Process

Before initialization, the research intent is clarified through:

1. **Clarity Assessment** - Evaluate idea across five dimensions:
   - Problem Definition (25%)
   - Solution Direction (25%)
   - Contribution Type (20%)
   - Constraints (15%)
   - Novelty Claim (15%)

2. **Action by Score:**
   - Score < 0.4: Invoke `research-ideation` skill for brainstorming
   - Score 0.4-0.7: Run clarification loop (max 5 rounds)
   - Score ≥ 0.7: Proceed to confirmation

3. **Documentation** - Generate `research-intent-confirmation.md` with:
   - Clarified research idea
   - Key parameters (venue, timeline, resources)
   - Success criteria
   - Q&A history

> See [skills/research-intent-clarification/SKILL.md](../research-intent-clarification/SKILL.md) and [references/intent-clarification-protocol.md](references/intent-clarification-protocol.md) for details.

### Gate 1: Survey → Pilot

**Required Deliverables:**
- [ ] `docs/survey/research-readiness-report.md` exists and contains:
  - [ ] Problem statement with clear research questions
  - [ ] Literature review summary (min 10 papers)
  - [ ] Gap analysis with proposed contribution
  - [ ] Recommended method/approach
- [ ] `docs/survey/phase-scorecard.md` exists
- [ ] Phase score ≥ 3.5 (on 5-point scale)

**Quality Checks:**
- [ ] All cited papers verified via academic APIs (Semantic Scholar/arXiv/CrossRef)
- [ ] No fabricated citations
- [ ] User approval recorded in state file

### Gate 2: Pilot → Experiments

**Required Deliverables:**
- [ ] `docs/pilot/pilot-validation-report.md` exists and contains:
  - [ ] Pilot experiment design
  - [ ] Implementation details
  - [ ] Preliminary results with error bars
  - [ ] Go/No-Go recommendation
- [ ] `docs/pilot/phase-scorecard.md` exists
- [ ] Phase score ≥ 3.5

**Quality Checks:**
- [ ] Code runs without errors
- [ ] Pilot results are reproducible
- [ ] Method validated on pilot dataset
- [ ] User approval recorded in state file

### Gate 3: Experiments → Paper

**Required Deliverables:**
- [ ] `docs/experiments/evidence-package-index.md` exists and contains:
  - [ ] Complete experiment configurations
  - [ ] All results with statistical analysis
  - [ ] Figures and tables for paper
  - [ ] Ablation studies (if applicable)
- [ ] `docs/experiments/results-summary.md` exists
- [ ] `docs/experiments/phase-scorecard.md` exists
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
- [ ] `docs/paper/final-acceptance-report.md` exists
- [ ] Phase score ≥ 3.5

**Quality Checks:**
- [ ] All figures readable and referenced
- [ ] No placeholder text (e.g., "TODO", "[insert figure]")
- [ ] Paper compiles to PDF successfully
- [ ] Citation audit passed (no fake papers)
- [ ] User approval recorded in state file

### Gate 5: Reflection → Close

**Required Deliverables:**
- [ ] `docs/reflection/lessons-learned.md` exists and contains:
  - [ ] What worked well
  - [ ] What could be improved
  - [ ] Recommendations for future projects
- [ ] `docs/reflection/runtime-improvement-report.md` exists
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

### Agent Execution Rules (Agent Teams)

- **Orchestrator NEVER executes research tasks directly.** All research work must be delegated to specialized agents via the Agent tool.
- **Each phase has EXACTLY 2 active agents** (primary + reviewer). Do NOT spawn explore agents or other helper agents.
- **Spawn agents with `team_name`** so they join the phase team and can communicate directly via SendMessage.
- **Use `TeamCreate` before spawning agents** and `TeamDelete` (after shutdown_request) when the phase ends.
- **Use `TaskCreate` + `TaskUpdate`** to create and assign tasks with dependency chains (reviewer blocked by primary).
- **Do NOT relay battle messages** — agents communicate directly during battle; Orchestrator only intervenes on escalation.
- **Always send `shutdown_request`** to both agents before calling `TeamDelete`.

### Literature Search Rules

- **Do NOT use websearch for literature.** Use academic database APIs (Semantic Scholar, arXiv, CrossRef, DBLP, OpenAlex).
- All cited papers must be verified via academic APIs before inclusion in any report.

### Language and Documentation Rules

- Keep process documents in Chinese by default and manuscript-facing documents in English by default unless the user overrides this.
- Do not claim plagiarism checks, AI-detection checks, or formal proof verification in v1.

### Integrity Rules

- Do not fabricate experiments, citations, datasets, checkpoints, or reviewer conclusions.
- All results must be traceable to actual runs with logged configurations.
- All citations must be verifiable through academic APIs.

### Gate and Transition Rules

- **Human gates are mandatory between phases.** The Orchestrator presents options but NEVER makes the decision autonomously.
- Do not pivot or advance phases without explicit human approval at the phase boundary.
- When a human gate rejects the current phase, present the allowed return phases and a suggested return phase; do not roll back automatically without that human choice.
- Do not advance phases when `validate_handoff.py` or `quality_gate.py` reports failure or escalation.
- Escalate back to the user when a phase loop reaches its configured limit without approval.

### State Management Rules

- **Save handoff summaries when dismissing agents.** Read them when resuming a phase.
- The Orchestrator maintains the single source of truth in `.autoresearch/state/research-state.yaml`.
- Task states must be updated in real-time as subagents progress through PENDING → IN_PROGRESS → COMPLETED/FAILED.

### Human Interaction Rules

- **The Orchestrator is the only agent that talks directly to the researcher.** Subagents do not interact with users.
- All questions, clarifications, and decisions must flow through the Orchestrator to the human.

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
