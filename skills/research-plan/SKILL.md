---
name: airesearchorchestrator:research-plan
description: Create comprehensive research execution plan with methodology overview, experiment design outline, resource requirements, and timeline. Use when user says "research plan", "create plan", "研究计划", or needs to structure research execution.
argument-hint: [idea-definition-path]
allowed-tools: Read, Write, Edit, Grep, Glob
---

## Purpose

Transform an idea definition into a detailed research execution plan with methodology, experiments, resources, and timeline.

## Workflow

### Step 1: Review Idea Definition

Read `docs/reports/survey/idea-definition.md` to understand:
- Research hypothesis
- Proposed approach
- Expected contributions

### Step 2: Design Methodology

Structure as:
- Overall approach overview
- Key methodological choices
- Data requirements
- Evaluation criteria

### Step 3: Outline Experiment Design

Create experiment matrix with:
- Experiment categories (main, ablation, baseline)
- Variables to test
- Datasets to use
- Metrics to report

### Step 4: Estimate Resources

Document:
- Compute requirements (GPU hours)
- Data requirements (storage, sources)
- Software dependencies
- Human effort estimates

### Step 5: Create Timeline

Build phase-based timeline:
- Literature review completion
- Pilot experiment
- Full experiments
- Analysis
- Paper writing

### Step 6: Risk Mitigation Plan

Identify:
- Technical risks
- Resource risks
- Timeline risks
- Mitigation strategies

## Output

Save to `docs/reports/survey/research-readiness-report.md`:

```markdown
# Research Readiness Report

## Executive Summary
[One paragraph overview of the research plan]

## Methodology Overview
[High-level approach and key technical decisions]

## Experiment Design Outline
| Experiment | Purpose | Variables | Metrics | Priority |
|------------|---------|-----------|---------|----------|
| ...        | ...     | ...       | ...     | ...      |

## Resource Requirements
- Compute: [GPU hours, memory requirements]
- Data: [sources, storage needs]
- Software: [key dependencies]
- Time: [estimated person-hours]

## Timeline
| Phase | Duration | Milestones |
|-------|----------|------------|
| Survey | X weeks | ... |
| Pilot | X weeks | ... |
| Experiments | X weeks | ... |
| Paper | X weeks | ... |

## Risk Assessment
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| ...  | ...         | ...    | ...        |

## Go/No-Go Criteria
[Conditions that would trigger stopping or pivoting]
```

## Key Rules

- Timeline must be realistic with buffer
- Resource estimates must include 20% buffer
- Must include fallback plans for key risks
- Experiments must directly test the hypothesis