---
name: airesearchorchestrator:paper-pipeline
description: "Workflow 3: Full paper writing pipeline. Orchestrates paper-plan → paper-figure → paper-write → paper-compile → auto-paper-improvement-loop to go from a narrative report to a polished, submission-ready PDF. Use when user says '写论文全流程', 'write paper pipeline', '从报告到PDF', 'paper pipeline', or wants the complete paper generation workflow."
user-invocable: true
argument-hint: [narrative-report-path-or-topic]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply
---
# Workflow 3: Paper Writing Pipeline

Orchestrate a complete paper writing workflow for: **$ARGUMENTS**

## Overview

This skill chains five sub-skills into a single automated pipeline:

```
/paper-plan → /paper-figure → /paper-write → /paper-compile → /auto-paper-improvement-loop
  (outline)     (plots)        (LaTeX)        (build PDF)       (review & polish ×2)
```

## Constants

| Constant | Default | Description |
|----------|---------|-------------|
| VENUE | ICLR | Target venue (ICLR/NeurIPS/ICML) |
| MAX_IMPROVEMENT_ROUNDS | 2 | Review→fix→recompile rounds |
| REVIEWER_MODEL | gpt-5.4 | Model via Codex MCP |
| AUTO_PROCEED | true | Auto-continue between phases |

## Pipeline

### Phase 1: Paper Plan
- Parse narrative for claims, evidence, figures
- Build Claims-Evidence Matrix
- Design section structure
- GPT-5.4 reviews plan

### Phase 2: Figure Generation
- Generate matplotlib/seaborn plots
- Create LaTeX comparison tables
- ~60% auto-generated, rest manual

### Phase 3: LaTeX Writing
- Write each section
- Build references.bib
- De-AI polish

### Phase 4: Compilation
- latexmk -pdf
- Auto-fix common errors
- Verify page count

### Phase 5: Auto Improvement (2 rounds)
- GPT-5.4 xhigh reviews
- Implement fixes
- Save round PDFs

## Output

- paper/main.pdf (final)
- paper/main_round0_original.pdf
- paper/main_round1.pdf
- paper/main_round2.pdf
- PAPER_IMPROVEMENT_LOG.md