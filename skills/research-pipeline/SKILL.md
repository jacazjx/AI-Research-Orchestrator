---
name: airesearchorchestrator:research-pipeline
description: "Full research pipeline: Workflow 1 (idea discovery) → implementation → Workflow 2 (auto review loop). Goes from a broad research direction all the way to a submission-ready paper. Use when user says '全流程', 'full pipeline', '从找idea到投稿', 'end-to-end research', or wants the complete autonomous research lifecycle."
argument-hint: [research-direction]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply
---

# Full Research Pipeline: Idea → Experiments → Submission

End-to-end autonomous research workflow for: **$ARGUMENTS**

## Overview

This skill chains the entire research lifecycle into a single pipeline:

```
/idea-discovery → implement → /run-experiment → /auto-review-loop → submission-ready
├── Workflow 1 ──┤            ├────────── Workflow 2 ──────────────┤
```

## Pipeline

### Stage 1: Idea Discovery (Workflow 1)

Invoke `/idea-discovery "$ARGUMENTS"`

**🚦 Gate 1 — Human Checkpoint:**

After `IDEA_REPORT.md` is generated, pause and present top ideas to user. Wait for user confirmation before continuing.

### Stage 2: Implementation

Implement full experiment based on approved idea.

### Stage 3: Deploy Experiments

Deploy with `/run-experiment` and monitor with `/monitor-experiment`.

### Stage 4: Auto Review Loop

Run `/auto-review-loop` for iterative improvement.

### Stage 5: Final Summary

Write final status report.

## Key Rules

- Human checkpoint after Stage 1 is MANDATORY
- Stages 2-4 can run autonomously after user confirms idea
- If Stage 4 ends at round 4 without positive assessment, stop and report
- Track total GPU-hours across pipeline

## Typical Timeline

| Stage | Duration | Can sleep? |
|-------|----------|------------|
| 1. Idea Discovery | 30-60 min | No |
| 2. Implementation | 15-60 min | No |
| 3. Deploy | 5 min + experiment time | Yes |
| 4. Auto Review | 1-4 hours | Yes |