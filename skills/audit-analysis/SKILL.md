---
name: airesearchorchestrator:audit-analysis
agent: adviser
description: Audit problem analysis for completeness, challenge identification, and solution feasibility. Use when user says "audit analysis", "review problem analysis", "审核问题分析", or needs to verify analysis quality.
argument-hint: [problem-analysis-path]
allowed-tools: Read, Write, Edit, Grep, Glob
---

## Purpose

Critically review the problem analysis for thoroughness and solution approach viability.

## Workflow

### Step 1: Review Analysis Document

Read `docs/reports/pilot/problem-analysis.md` for decomposition and approach.

### Step 2: Assess Decomposition

Evaluate:
- All sub-problems identified
- Dependencies mapped
- Assumptions reasonable
- Boundaries clear

### Step 3: Evaluate Challenge Analysis

Check:
- Challenges accurately identified
- Difficulty assessment reasonable
- Existing solutions properly evaluated
- Differentiation clear

### Step 4: Review Solution Approach

Assess:
- Addresses all challenges
- Technically sound
- Implementation feasible
- Integration points clear

### Step 5: Validate Feasibility

Verify:
- Technical feasibility assessment
- Resource feasibility
- Risk factors identified

## Output

```markdown
# Problem Analysis Audit Report

## Summary
- **Overall Assessment**: PASS / REVISE_NEEDED / MAJOR_REVISION
- **Completeness Score**: X/10
- **Solution Viability**: X/10

## Decomposition Review

| Aspect | Status | Notes |
|--------|--------|-------|
| Sub-problems complete | Yes/No | X identified |
| Dependencies mapped | Yes/No | |
| Assumptions reasonable | Yes/No | |
| Boundaries clear | Yes/No | |

**Missing Sub-problems**:
- [Problem not identified]

## Challenge Analysis Review

| Challenge | Accurate? | Difficulty Fair? | Differentiation Clear? |
|-----------|-----------|------------------|----------------------|
| [Challenge 1] | Yes/No | Yes/No | Yes/No |

**Missing Challenges**:
- [Challenge not identified]

## Solution Approach Review

| Criterion | Status | Notes |
|-----------|--------|-------|
| Addresses all challenges | Yes/No | |
| Technically sound | Yes/No | |
| Implementation feasible | Yes/No | |
| Integration points clear | Yes/No | |

**Gaps in Approach**:
- [Gap]

## Feasibility Assessment

| Aspect | Assessment | Auditor Opinion |
|--------|------------|-----------------|
| Technical | [Rating] | [Agree/Disagree because...] |
| Resources | [Rating] | |

## Recommendations

1. [Recommendation]
2. [Recommendation]

## Gate Decision

- [ ] PASS - Analysis is thorough, proceed
- [ ] PASS_WITH_FIXES - Minor gaps, address and proceed
- [ ] REVISE - Significant gaps in analysis
- [ ] BLOCK - Analysis inadequate for pilot
```

## Key Rules

- Must identify at least 3 technical challenges
- Solution must address all identified challenges
- Feasibility must be honestly assessed
- Missing sub-problems are critical issues