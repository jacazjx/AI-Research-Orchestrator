<p align="center">
  <img src="assets/images/logo.svg" alt="AI Research Orchestrator" width="200">
</p>

<h1 align="center">AI Research Orchestrator</h1>

<p align="center">
  <strong>Turn a research IDEA into a controlled five-phase project with explicit human gates</strong>
</p>

<p align="center">
  <a href="README.zh-CN.md">简体中文</a> | English
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-blue?logo=anthropic" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Version-1.0.0-green" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
  <img src="https://img.shields.io/badge/Python-3.9+-blue" alt="Python">
  <img src="https://img.shields.io/badge/Phase-5-orange" alt="5 Phases">
</p>

---

`AI Research Orchestrator` transforms a research idea into a structured project with state machines, deliverables, visual progress tracking, and explicit human gates between phases. Optimized for AI/ML research requiring literature review, pilot validation, experiments, and paper writing.

## Workflow Diagram

### Overall Research Pipeline

```
    ┌────────────────────────────────────────────────────────────────────────────┐
    │                         RESEARCH IDEA                                       │
    └─────────────────────────────────┬──────────────────────────────────────────┘
                                      │
                                      ▼
    ┌────────────────────────────────────────────────────────────────────────────┐
    │  PHASE 1: SURVEY                                                           │
    │  ┌───────────────┐                              ┌───────────────┐          │
    │  │    SURVEY     │ ── literature review ───────▶│    CRITIC     │          │
    │  │    (Doer)     │ ── novelty check ──────────▶│  (Auditor)    │          │
    │  │               │ ◀── revision requests ──────│               │          │
    │  └───────┬───────┘                              └───────┬───────┘          │
    │          │                                              │                  │
    │          └──────────────────┬───────────────────────────┘                  │
    │                             ▼                                              │
    │                    ┌───────────────┐                                       │
    │                    │   GATE 1 ✋   │  ← Human Approval Required            │
    │                    └───────┬───────┘                                       │
    └────────────────────────────┼───────────────────────────────────────────────┘
                                 │ Score ≥ 3.5
                                 ▼
    ┌────────────────────────────────────────────────────────────────────────────┐
    │  PHASE 2: PILOT                                                            │
    │  ┌───────────────┐                              ┌───────────────┐          │
    │  │     CODE      │ ── problem validation ─────▶│   ADVISER     │          │
    │  │    (Doer)     │ ── pilot experiment ───────▶│  (Auditor)    │          │
    │  │               │ ── preliminary results ────▶│               │          │
    │  │               │ ◀── design feedback ────────│               │          │
    │  └───────┬───────┘                              └───────┬───────┘          │
    │          │                                              │                  │
    │          └──────────────────┬───────────────────────────┘                  │
    │                             ▼                                              │
    │                    ┌───────────────┐                                       │
    │                    │   GATE 2 ✋   │  ← Go/No-Go Decision                  │
    │                    └───────┬───────┘                                       │
    └────────────────────────────┼───────────────────────────────────────────────┘
                                 │ Go decision
                                 ▼
    ┌────────────────────────────────────────────────────────────────────────────┐
    │  PHASE 3: EXPERIMENTS                                                      │
    │  ┌───────────────┐                              ┌───────────────┐          │
    │  │     CODE      │ ── full experiments ───────▶│   ADVISER     │          │
    │  │    (Doer)     │ ── evidence package ───────▶│  (Auditor)    │          │
    │  │               │ ◀── validation requests ───│               │          │
    │  └───────┬───────┘                              └───────┬───────┘          │
    │          │                                              │                  │
    │          └──────────────────┬───────────────────────────┘                  │
    │                             ▼                                              │
    │                    ┌───────────────┐                                       │
    │                    │   GATE 3 ✋   │  ← Evidence Sufficient?               │
    │                    └───────┬───────┘                                       │
    └────────────────────────────┼───────────────────────────────────────────────┘
                                 │ Evidence approved
                                 ▼
    ┌────────────────────────────────────────────────────────────────────────────┐
    │  PHASE 4: PAPER                                                            │
    │  ┌───────────────┐                              ┌───────────────┐          │
    │  │    WRITER     │ ── manuscript draft ───────▶│   REVIEWER    │          │
    │  │    (Doer)     │ ── evidence citations ─────▶│  (Auditor)    │          │
    │  │               │ ◀── revision comments ─────│               │          │
    │  └───────┬───────┘                              └───────┬───────┘          │
    │          │                                              │                  │
    │          └──────────────────┬───────────────────────────┘                  │
    │                             ▼                                              │
    │                    ┌───────────────┐                                       │
    │                    │   GATE 4 ✋   │  ← Submission Ready?                  │
    │                    └───────┬───────┘                                       │
    └────────────────────────────┼───────────────────────────────────────────────┘
                                 │ Approved
                                 ▼
    ┌────────────────────────────────────────────────────────────────────────────┐
    │  PHASE 5: REFLECTION                                                       │
    │  ┌───────────────┐                              ┌───────────────┐          │
    │  │  REFLECTOR    │ ── lessons learned ────────▶│    CURATOR    │          │
    │  │    (Doer)     │ ── improvement proposals ──▶│  (Auditor)    │          │
    │  │               │ ◀── actionable items ──────│               │          │
    │  └───────┬───────┘                              └───────┬───────┘          │
    │          │                                              │                  │
    │          └──────────────────┬───────────────────────────┘                  │
    │                             ▼                                              │
    │                    ┌───────────────┐                                       │
    │                    │   GATE 5 ✋   │  ← Archive & Close                    │
    │                    └───────┬───────┘                                       │
    └────────────────────────────┼───────────────────────────────────────────────┘
                                 │
                                 ▼
                    ┌───────────────────────┐
                    │   📁 PROJECT CLOSED   │
                    │   Lessons Archived    │
                    └───────────────────────┘
```

### Inner Loop Detail (Per Phase)

```
                    ┌─────────────────────────────────────────┐
                    │            PHASE START                   │
                    └──────────────────┬──────────────────────┘
                                       │
                                       ▼
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    │   ┌─────────────┐                       │
                    │   │   PRIMARY   │                       │
                    │   │    AGENT    │                       │
                    │   │   (Doer)    │                       │
                    │   └──────┬──────┘                       │
                    │          │                              │
                    │          │ produces                     │
                    │          ▼                              │
                    │   ┌─────────────┐                       │
                    │   │  DELIVERABLE│                       │
                    │   │   (Draft)   │                       │
                    │   └──────┬──────┘                       │
                    │          │                              │
                    │          │ submits                      │
                    │          ▼                              │
                    │   ┌─────────────┐                       │
                    │   │   REVIEWER  │                       │
                    │   │    AGENT    │                       │
                    │   │  (Auditor)  │                       │
                    │   └──────┬──────┘                       │
                    │          │                              │
                    │          │ scores & comments            │
                    │          ▼                              │
              ┌─────┴─────────────────────────────┐           │
              │                                   │           │
              ▼                                   ▼           │
       ┌────────────┐                      ┌────────────┐     │
       │  APPROVE   │                      │  REVISE    │     │
       │  Score ≥3.5│                      │  Score <3.5│     │
       └─────┬──────┘                      └──────┬─────┘     │
             │                                    │           │
             │                                    │           │
             │        ┌───────────────────────────┘           │
             │        │                                       │
             │        │ feedback loop                          │
             │        └──────────────────────┐                │
             │                               │                │
             │                               ▼                │
             │                    ┌──────────────────┐        │
             │                    │ MAX LOOPS HIT?   │        │
             │                    └────────┬─────────┘        │
             │                             │                  │
             │              ┌──────────────┼──────────────┐    │
             │              │              │              │    │
             │              ▼              ▼              ▼    │
             │         ┌────────┐   ┌────────────┐  ┌────────┐ │
             │         │  YES   │   │    NO      │  │ ESCAL- │ │
             │         │EXIT    │   │CONTINUE    │  │  ATE   │ │
             │         │LOOP    │   │LOOP        │  │to Human│ │
             │         └────┬───┘   └────────────┘  └───┬────┘ │
             │              │                           │      │
             └──────────────┼───────────────────────────┘      │
                            │                                  │
                            ▼                                  │
                    ┌───────────────┐                          │
                    │  GATE CHECK   │◀─────────────────────────┘
                    │   ✋ HUMAN     │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
       ┌──────────┐  ┌──────────┐  ┌──────────┐
       │ APPROVE  │  │  REVISE  │  │ ROLLBACK │
       │ Continue │  │   More   │  │  Return  │
       │ to Next  │  │  Work    │  │  Back    │
       │  Phase   │  │          │  │          │
       └────┬─────┘  └──────────┘  └──────────┘
            │
            ▼
    ┌─────────────────┐
    │   NEXT PHASE    │
    └─────────────────┘
```

### Rollback & Pivot Flow

```
    Current Phase
         │
         │ Gate Rejected (Score < 2.5)
         │
         ▼
    ┌─────────────────────────────────────────────────────┐
    │                  ROLLBACK OPTIONS                    │
    │                                                      │
    │   ┌──────────┐   ┌──────────┐   ┌──────────┐        │
    │   │  REVISE  │   │ ROLLBACK │   │  PIVOT   │        │
    │   │  (Stay)  │   │  (Back)  │   │ (Change) │        │
    │   └────┬─────┘   └────┬─────┘   └────┬─────┘        │
    │        │              │              │               │
    │        ▼              ▼              ▼               │
    │   Continue       Return to       Change             │
    │   current        earlier         research           │
    │   phase          phase           direction          │
    │                                                      │
    └─────────────────────────────────────────────────────┘
         │
         │ Orchestrator suggests:
         │ "Based on issues found, recommend rollback to Phase X"
         │
         ▼
    ┌─────────────────┐
    │  HUMAN DECIDES  │
    │  Which option?  │
    └────────┬────────┘
             │
             ▼
    Resumed at chosen phase
    with context preserved
```

## Five Phases

| Phase | Agents | Key Deliverable | Gate |
|-------|--------|-----------------|------|
| **Survey** | Survey ↔ Critic | `research-readiness-report.md` | Gate 1 |
| **Pilot** | Code ↔ Adviser | `pilot-validation-report.md` | Gate 2 |
| **Experiments** | Code ↔ Adviser | `evidence-package-index.md` | Gate 3 |
| **Paper** | Writer ↔ Reviewer | `final-acceptance-report.md` | Gate 4 |
| **Reflection** | Reflector ↔ Curator | `runtime-improvement-report.md` | Gate 5 |

## Agent Roles

### Primary Agents (Doers)

| Agent | Phase | Responsibilities |
|--------|-------|------------------|
| **Survey** | Survey | Literature review using academic APIs, define atomic academic definitions, identify research gaps |
| **Code** | Pilot, Experiments | Design experiments, implement code, run experiments, analyze results |
| **Writer** | Paper | Write manuscript based only on approved evidence, structure arguments |
| **Reflector** | Reflection | Extract lessons learned, propose system improvements (overlays) |

### Reviewer Agents (Auditors)

| Agent | Phase | Responsibilities |
|--------|-------|------------------|
| **Critic** | Survey | Audit novelty, feasibility, theory risk, citation authenticity |
| **Adviser** | Pilot, Experiments | Review experimental design, validate results, judge evidence strength |
| **Reviewer** | Paper | Review manuscript per top-tier standards, audit citations |
| **Curator** | Reflection | Judge which improvements are reusable, safe, and actionable |

## Gate Mechanism

### Gate Scoring

| Score | Decision | Action |
|-------|----------|--------|
| 4.5-5.0 | ✅ Approve | Proceed immediately |
| 3.5-4.4 | 🔶 Advance | Minor fixes, then proceed |
| 2.5-3.4 | 🔄 Revise | Significant revision required |
| 1.5-2.4 | 🔙 Major Revise | Return to earlier phase |
| 0.0-1.4 | ⚠️ Pivot | Consider alternative or termination |

### Gate Checklist

**Gate 1 (Survey → Pilot):**
- [ ] Literature review (min 10 papers, academic APIs only)
- [ ] Novelty argument with evidence
- [ ] All citations verified authentic
- [ ] Research questions clearly defined

**Gate 2 (Pilot → Experiments):**
- [ ] Pilot code runs without errors
- [ ] Preliminary results support hypothesis
- [ ] Clear go/no-go recommendation

**Gate 3 (Experiments → Paper):**
- [ ] All experiments traceable with run IDs
- [ ] Statistical analysis complete
- [ ] No hidden negative results

**Gate 4 (Paper → Reflection):**
- [ ] Manuscript compiles to PDF
- [ ] All citations verified (≥90%)
- [ ] No placeholder text

**Gate 5 (Reflection → Close):**
- [ ] Lessons documented
- [ ] Overlay decisions made
- [ ] Project archived

## Installation

### Option 1: From GitHub Marketplace (Recommended)

```bash
# Add the marketplace
/plugin marketplace add jacazjx/AI-Research-Orchestrator

# Install the plugin
/plugin install airesearchorchestrator@airesearchorchestrator
```

### Option 2: Configure settings.json

Add to `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "airesearchorchestrator": {
      "source": {
        "source": "github",
        "repo": "jacazjx/AI-Research-Orchestrator"
      }
    }
  },
  "enabledPlugins": {
    "airesearchorchestrator@airesearchorchestrator": true
  }
}
```

### Option 3: Local Development

```bash
cc --plugin-dir /path/to/AI-Research-Orchestrator
```

## Quick Start

```bash
# Step 0 (recommended): Clarify your research idea before committing to a project
/airesearchorchestrator:insight

# Step 1: Initialize a new research project
/airesearchorchestrator:init-research

# Steps 2–6: Run each phase in sequence
/airesearchorchestrator:run-survey      # Phase 1 — literature review
/airesearchorchestrator:run-pilot       # Phase 2 — pilot experiment
/airesearchorchestrator:run-experiments # Phase 3 — full experiments
/airesearchorchestrator:write-paper     # Phase 4 — manuscript
/airesearchorchestrator:reflect         # Phase 5 — lessons learned
```

> **Resuming an existing project?** Start every new Claude Code session with `/airesearchorchestrator:reload` to restore project context before continuing.

## Directory Structure

```
my-project/
├── .autoresearch/           # System directory
│   ├── state/               # research-state.yaml (single source of truth)
│   ├── config/              # orchestrator-config.yaml
│   ├── dashboard/           # Visual progress tracking
│   └── runtime/             # Job/GPU/Backend registries
├── agents/                  # Agent work directories
│   ├── survey/              # Survey agent workspace
│   ├── critic/              # Critic agent workspace
│   ├── coder/               # Code agent workspace
│   ├── adviser/             # Adviser agent workspace
│   ├── writer/              # Writer agent workspace
│   ├── reviewer/            # Reviewer agent workspace
│   ├── reflector/           # Reflector agent workspace
│   └── curator/             # Curator agent workspace
├── paper/                   # Paper-related files
├── code/                    # Code and experiments
└── docs/reports/            # Phase deliverables
    ├── survey/
    ├── pilot/
    ├── experiments/
    └── reflection/
```

## Commands

| Command | Description | Triggers |
|---------|-------------|----------|
| `/airesearchorchestrator:insight` | Clarify research intent | "insight", "clarify intent" |
| `/airesearchorchestrator:init-research` | Initialize new project | "init research", "start research project" |
| `/airesearchorchestrator:run-survey` | Run Survey phase | "run survey", "literature review" |
| `/airesearchorchestrator:run-pilot` | Run Pilot phase | "run pilot", "pilot experiment" |
| `/airesearchorchestrator:run-experiments` | Run full experiments | "run experiments", "full experiments" |
| `/airesearchorchestrator:write-paper` | Write paper | "write paper", "draft paper" |
| `/airesearchorchestrator:reflect` | Run reflection | "reflect", "lessons learned" |
| `/airesearchorchestrator:reload` | Restore session context | "reload", "continue research" |
| `/airesearchorchestrator:configure` | Configure project settings | "configure", "config" |

## Hard Rules

1. **Two agents per phase** - Only the primary and reviewer agents are active
2. **No web search for literature** - Use academic APIs (Semantic Scholar, arXiv, CrossRef, DBLP, OpenAlex)
3. **No fabrication** - Never fabricate citations, experiments, or results
4. **Human gates mandatory** - No automatic phase advancement without approval
5. **State persistence** - All state saved to `research-state.yaml`

## Literature Search APIs

| API | Use Case | Example |
|-----|----------|---------|
| Semantic Scholar | AI/ML papers | `api.semanticscholar.org/graph/v1/paper/search?query=transformer` |
| arXiv | Preprints | `export.arxiv.org/api/query?search_query=all:attention` |
| CrossRef | DOI verification | `api.crossref.org/works?query.title=paper+title` |
| DBLP | Computer Science | `dblp.org/search/publ/api?q=transformer&format=json` |
| OpenAlex | Comprehensive | `api.openalex.org/works?search=vision+transformer` |

## Documentation

- [Workflow Protocol](references/workflow-protocol.md) - Phase order and requirements
- [Gate Rubrics](references/gate-rubrics.md) - Detailed scoring criteria
- [System Architecture](references/system-architecture.md) - Inner/outer loop design
- [Phase Execution Details](references/phase-execution-details.md) - Substeps per phase

## Testing

```bash
python3 -m pytest tests/ -v
```

## License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  Made with ❤️ for AI Researchers
</p>