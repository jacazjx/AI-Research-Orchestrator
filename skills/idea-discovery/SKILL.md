---
name: autoresearch:idea-discovery
description: "Workflow 1: Full idea discovery pipeline. Orchestrates research-lit → idea-creator → novelty-check → research-review to go from a broad research direction to validated, pilot-tested ideas. Use when user says '找idea全流程', 'idea discovery pipeline', '从零开始找方向', or wants the complete idea exploration workflow."
argument-hint: [research-direction]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply
---

# Workflow 1: Idea Discovery Pipeline

Orchestrate a complete idea discovery workflow for: **$ARGUMENTS**

## Overview

This skill chains four sub-skills into a single automated pipeline:

```
/research-lit → /idea-creator → /novelty-check → /research-review
  (survey)      (brainstorm)    (verify novel)    (critical feedback)
```

## Constants

| Constant | Default | Description |
|----------|---------|-------------|
| **PILOT_MAX_HOURS** | 2 | Skip any pilot experiment estimated to take > 2 hours per GPU |
| **PILOT_TIMEOUT_HOURS** | 3 | Hard timeout for pilots |
| **MAX_PILOT_IDEAS** | 3 | Run pilots for at most 3 top ideas in parallel |
| **MAX_TOTAL_GPU_HOURS** | 8 | Total GPU budget across all pilots |
| **AUTO_PROCEED** | true | Auto-proceed with best option if user doesn't respond |
| **REVIEWER_MODEL** | `gpt-5.4` | Model used via Codex MCP |

## Pipeline

### Phase 1: Literature Survey

Invoke `/research-lit` to map the research landscape.

### Phase 2: Idea Generation + Filtering + Pilots

Invoke `/idea-creator` with the landscape context.

### Phase 3: Deep Novelty Verification

For each top idea, run `/novelty-check`.

### Phase 4: External Critical Review

For surviving ideas, run `/research-review`.

### Phase 5: Final Report

Finalize `IDEA_REPORT.md` with ranked ideas and recommendations.

## Key Rules

1. Don't skip phases
2. Checkpoint between phases
3. Kill ideas early
4. Empirical signal > theoretical appeal
5. Document everything