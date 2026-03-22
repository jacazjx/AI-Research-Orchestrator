---
name: airesearchorchestrator:system-evaluation
agent: reflector
description: "Evaluate the orchestrator system's performance across 6 dimensions during the Reflection phase. Produces a scored diagnostic report with evidence-based analysis. Use after completing lessons extraction and overlay proposal."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/system_eval_registry.py:*)
---

# System Evaluation

## Purpose

Evaluate how well the orchestrator system performed during this research project. Produce a scored diagnostic report across 6 dimensions, grounded in project evidence from state data and deliverable content analysis.

## Prerequisites

- Task 1 (Extract Lessons) and Task 2 (Propose Overlays) must be completed
- Access to `.autoresearch/state/research-state.yaml`
- Access to all phase deliverables and scorecards

## Workflow

### Step 1: Gather Evidence

Read and analyze the following data sources:

**State data:**
- `.autoresearch/state/research-state.yaml` — Extract: `loop_counts`, `loop_limits`, `gate_scores`, `gate_history`, `human_decisions`, `pivot_candidates`, `phase_reviews`, `research_type`

**Phase scorecards:**
- `docs/survey/phase-scorecard.md`
- `docs/pilot/phase-scorecard.md`
- `docs/experiments/phase-scorecard.md`
- `docs/paper/phase-scorecard.md`

**Core deliverables** (read content for quality assessment):
- `docs/survey/research-readiness-report.md`
- `docs/pilot/pilot-validation-report.md`
- `docs/experiments/evidence-package-index.md`
- `paper/paper-draft.md`

**Templates** (compare against actual deliverables):
- Read template files from `${CLAUDE_PLUGIN_ROOT}/assets/templates/` and compare structure against actual deliverable content

### Step 2: Per-Dimension Evaluation

Consult `${CLAUDE_PLUGIN_ROOT}/references/system-evaluation-rubrics.md` for detailed scoring criteria.

For each of the 6 dimensions:
1. List the specific evidence found (cite file paths and data values)
2. Score the dimension (0-5) based on the rubric criteria
3. Write a diagnosis identifying root causes of any issues
4. Propose specific, actionable recommendations

**Dimensions and weights:**
| Dimension | Weight |
|-----------|--------|
| Workflow Effectiveness | 20% |
| Agent Collaboration Quality | 20% |
| Gate Accuracy | 20% |
| Template Effectiveness | 15% |
| Resource Efficiency | 15% |
| User Experience | 10% |

### Step 3: Calculate Weighted Total

```
total = (workflow * 0.20) + (collaboration * 0.20) + (gate * 0.20)
      + (template * 0.15) + (efficiency * 0.15) + (ux * 0.10)
```

Map total to recommendation:
- 4.5 - 5.0: System performed excellently, record best practices
- 3.5 - 4.4: System performed well, improvement opportunities exist
- 2.5 - 3.4: Targeted improvements needed
- 1.5 - 2.4: Major improvements needed
- 0.0 - 1.4: Fundamental restructuring needed

### Step 4: Generate Report

Fill the template at `docs/reflection/system-evaluation-report.md` with all findings. Ensure every score has corresponding evidence in the Evidence section.

### Step 5: Write to Global Registry

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/system_eval_registry.py \
  --action record \
  --project-root <project_root> \
  --scores '<JSON scores>' \
  --weighted-total <total> \
  --recommendation "<recommendation>" \
  --top-issues '<JSON issues>'
```

### Step 6: Check Cross-Project Trends (if available)

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/system_eval_registry.py \
  --action trend --last 10
```

If historical data exists, add a trend comparison to the "Cross-Project Trend" section of the report.

### Step 7: Notify Curator

```
SendMessage(to="curator", message={"type": "system_eval_ready", "path": "docs/reflection/system-evaluation-report.md"})
```

## Hard Rules

1. **Every score must have evidence** — No dimension may be scored without citing specific state data, file content, or metrics
2. **No self-leniency** — Apply rubrics strictly; when in doubt, round down
3. **Root cause required** — Do not just describe symptoms; identify why issues occurred
4. **Quantitative where possible** — Use loop ratios, fill rates, and score deltas, not vague qualifiers
5. **Acknowledge limitations** — If evidence is insufficient to score a dimension accurately, state this explicitly

## Output

- `docs/reflection/system-evaluation-report.md` — Filled evaluation report
- Global registry entry at `~/.autoresearch/system-eval-history.yaml`
