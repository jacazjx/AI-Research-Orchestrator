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
  <img src="https://img.shields.io/badge/Version-1.3.0-green" alt="Version">
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

## Time Expectations

Each research phase has different time requirements based on complexity and scope:

| Phase | Duration | Key Activities |
|-------|----------|----------------|
| **Survey** | 2-5 days | Literature search via academic APIs, novelty analysis, citation verification |
| **Pilot** | 1-3 days | Code implementation, small-scale experiment, preliminary validation |
| **Experiments** | 3-14 days | Full experiment runs, statistical analysis, evidence collection (varies by complexity) |
| **Paper** | 3-7 days | Manuscript writing, internal review, revision cycles |
| **Reflection** | 1 day | Lessons learned extraction, improvement proposals |

**Total project duration:** 10-30 days typical, depending on experiment complexity and revision cycles.

**Tips for faster completion:**
- Provide clear, specific research ideas during initialization
- Respond promptly to gate decisions
- Use GPU resources efficiently for experiments
- Keep literature search focused on key papers

## Frequently Asked Questions

### Q: How do I resume an interrupted research project?

Use the reload command at the start of any new Claude Code session:
```bash
/airesearchorchestrator:reload
```
This restores the full project context from `research-state.yaml`, including:
- Current phase and status
- Gate scores and feedback
- Agent handoff summaries
- Blockers and pending decisions

### Q: What if my gate score is too low?

Gate scores below 3.5 require revision. The reviewer agent provides specific feedback:

| Score Range | Action Required |
|-------------|-----------------|
| 2.5-3.4 | Significant revision needed; address feedback and resubmit |
| 1.5-2.4 | Major issues; may need to return to earlier phase |
| 0.0-1.4 | Fundamental problems; consider pivoting research direction |

The orchestrator will suggest specific remediation steps based on the reviewer's feedback.

### Q: How do I use my own GPU server?

1. Register your GPU in `~/.autoresearch/gpu-registry.yaml`:
```yaml
devices:
  - id: "my-gpu-01"
    name: "RTX 4090"
    host: "192.168.1.100"
    ssh_key: "~/.ssh/id_rsa"
```

2. Configure the project to use it:
```bash
/airesearchorchestrator:configure
```

3. Select your GPU during configuration when prompted.

### Q: What if citation verification fails?

Citation verification failures indicate potential authenticity issues:

1. **Check the source:** Verify the paper exists using DOI lookup or academic APIs
2. **Replace fabricated citations:** Use Semantic Scholar or arXiv to find real papers
3. **Re-run verification:** The Critic agent will re-verify after corrections

Common causes:
- Typos in paper titles or author names
- Citing papers that don't exist (AI hallucination)
- Using web search results instead of academic API sources

### Q: Can I skip phases?

**No.** The five-phase pipeline is designed to ensure research quality:

- Each phase builds on the previous phase's deliverables
- Gate checks validate readiness for the next phase
- Skipping phases would compromise research integrity

**However, you can:**
- Request "advance with minor fixes" if gate score is 3.5-4.4
- Use the `/airesearchorchestrator:configure` command to adjust parameters
- Manually approve early advancement in exceptional cases (not recommended)

## Troubleshooting Guide

### Initialization Failure

**Symptoms:** `/init-research` fails or creates incomplete project structure.

**Solutions:**
1. Verify Python 3.9+ is installed: `python3 --version`
2. Check write permissions for target directory
3. Ensure sufficient disk space (minimum 500MB recommended)
4. Try with absolute path: `--project-root /absolute/path/to/project`

### Agent Not Responding

**Symptoms:** Agent appears stuck, no progress for extended time.

**Solutions:**
1. Check for blocker messages in the dashboard
2. Run `/airesearchorchestrator:status` to see current state
3. Try reloading the project: `/airesearchorchestrator:reload`
4. If truly stuck, you can dismiss and re-spawn the agent
5. Check `agents/<role>/` for error logs

### Gate Review Failure

**Symptoms:** Consistently receiving low gate scores despite revisions.

**Solutions:**
1. Read the reviewer feedback carefully - it contains specific issues
2. Address ALL points mentioned in the feedback
3. Check that deliverables match the expected format
4. Verify citations are from academic APIs, not web search
5. Consider requesting a rollback to an earlier phase if issues are fundamental

### Citation Problems

**Symptoms:** "Citation verification failed" or "Fabricated citation detected".

**Solutions:**
1. **Verify the citation exists:**
   ```bash
   # Check via DOI
   curl "https://api.crossref.org/works?query.title=YOUR_PAPER_TITLE"

   # Check via Semantic Scholar
   curl "https://api.semanticscholar.org/graph/v1/paper/search?query=YOUR_QUERY"
   ```

2. **Replace problematic citations** with verified papers from academic APIs

3. **Re-run the citation audit** through the reviewer agent

4. **Avoid web search** for literature - always use academic APIs

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `State file not found` | Project not initialized | Run `/airesearchorchestrator:init-research` |
| `Invalid phase transition` | Skipping phases | Complete previous phase first |
| `Gate score insufficient` | Score < 3.5 | Address reviewer feedback |
| `Agent timeout` | Long-running task | Wait or check logs |
| `Citation not found` | Fabricated or typo | Verify and replace citation |

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
└── docs/                    # Phase deliverables
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
| `/airesearchorchestrator:status` | Show project status | "status", "查看状态", "项目状态" |
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

- [Workflow Protocol](references/workflow.md) - Phase order and requirements
- [Gate Rubrics](references/gate-rubrics.md) - Detailed scoring criteria
- [System Architecture](references/system-architecture.md) - Inner/outer loop design
- [Phase Execution Details](references/workflow.md) - Substeps per phase

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