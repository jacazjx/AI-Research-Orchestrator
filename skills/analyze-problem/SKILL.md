---
name: airesearchorchestrator:analyze-problem
agent: code
description: Analyze research problem with decomposition, technical challenges, and solution approach. Use when user says "analyze problem", "problem analysis", "问题分析", or needs to break down a research challenge.
argument-hint: [problem-description]
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(curl), WebFetch
---

## Purpose

Decompose a research problem into manageable components, identify technical challenges, and propose solution approaches.

## Workflow

### Step 1: Problem Decomposition

Break down the problem:
- Core challenge identification
- Sub-problems and dependencies
- Assumptions and constraints
- Boundary conditions

### Step 2: Technical Challenge Analysis

For each sub-problem:
- Why is it hard?
- What approaches exist?
- What are their limitations?
- What makes our approach different?

### Step 3: Solution Approach Design

Outline proposed solution:
- High-level architecture
- Key algorithms/components
- Data flow
- Integration points

### Step 4: Feasibility Assessment

Evaluate:
- Technical feasibility
- Resource feasibility
- Time feasibility
- Risk factors

### Step 5: Success Metrics

Define:
- Quantitative metrics
- Qualitative criteria
- Comparison baselines

## Output

Save to `docs/reports/pilot/problem-analysis.md`:

```markdown
# Problem Analysis

## Problem Decomposition

### Core Challenge
[The fundamental problem being addressed]

### Sub-problems
1. [Sub-problem 1]
   - Dependencies: ...
   - Complexity: Low/Medium/High
2. [Sub-problem 2]
   ...

### Assumptions
- [Assumption 1]
- [Assumption 2]

## Technical Challenges

| Challenge | Difficulty | Existing Solutions | Our Approach |
|-----------|------------|-------------------|--------------|
| ...       | ...        | ...               | ...          |

## Solution Approach

### Architecture
[High-level design diagram or description]

### Key Components
1. [Component 1]: [Purpose and implementation sketch]
2. [Component 2]: [Purpose and implementation sketch]

### Data Flow
[How data moves through the system]

## Feasibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Technical | Ready/Blocked | ... |
| Resources | Available/Needed | ... |
| Timeline | Realistic/Tight | ... |

## Success Metrics

| Metric | Target | Baseline |
|--------|--------|----------|
| ...    | ...    | ...      |

## Next Steps
[What needs to happen before pilot implementation]
```

## Key Rules

- Decomposition must reveal all sub-problems
- Must identify at least 3 technical challenges
- Solution approach must address all challenges
- Feasibility must be honest assessment