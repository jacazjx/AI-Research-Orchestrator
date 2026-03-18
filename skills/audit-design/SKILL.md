---
name: airesearchorchestrator:audit-design
description: Audit pilot design for validity, resource efficiency, and success criteria clarity. Use when user says "audit design", "review pilot design", "审核 Pilot 设计", or needs to verify pilot experiment design.
user-invocable: false
argument-hint: [pilot-design-path]
allowed-tools: Read, Write, Edit, Grep, Glob
---
## Purpose

Critically review pilot experiment design for hypothesis validity and resource efficiency.

## Workflow

### Step 1: Review Design Document

Read `docs/reports/pilot/pilot-design.md` for scope, implementation, and criteria.

### Step 2: Assess Scope Appropriateness

Evaluate:
- Tests core hypothesis directly
- Minimal but sufficient scope
- Can complete in < 24 hours
- Success/failure determinable

### Step 3: Evaluate Implementation Plan

Check:
- Code structure reasonable
- Data pipeline defined
- Training procedure clear
- Evaluation protocol sound

### Step 4: Review Success Criteria

Assess:
- Criteria are measurable
- Go/No-Go thresholds clear
- No ambiguous success conditions
- Early stopping defined

### Step 5: Validate Resource Estimates

Verify:
- Time estimates realistic
- GPU requirements appropriate
- Debugging buffer included

## Output

```markdown
# Pilot Design Audit Report

## Summary
- **Overall Assessment**: PASS / REVISE_NEEDED / MAJOR_REVISION
- **Hypothesis Test Validity**: X/10
- **Resource Efficiency**: X/10

## Scope Appropriateness

| Criterion | Status | Notes |
|-----------|--------|-------|
| Tests core hypothesis | Yes/No | |
| Minimal scope | Yes/No | |
| Completes in < 24h | Yes/No | |
| Determinate success | Yes/No | |

**Scope Issues**:
- [Issue]

## Implementation Review

| Aspect | Status | Notes |
|--------|--------|-------|
| Code structure | Clear/Unclear | |
| Data pipeline | Defined/Missing | |
| Training procedure | Clear/Unclear | |
| Evaluation protocol | Sound/Issues | |

**Implementation Risks**:
- [Risk]

## Success Criteria Review

| Criterion | Measurable? | Threshold Clear? | Appropriate? |
|-----------|-------------|------------------|--------------|
| [Criterion 1] | Yes/No | Yes/No | Yes/No |

**Ambiguous Criteria**:
- [Criterion and issue]

## Resource Estimates

| Resource | Estimated | Auditor Estimate | Variance |
|----------|-----------|------------------|----------|
| GPU time | X hours | Y hours | +/-Z |
| Data prep | X hours | Y hours | |
| Debugging | X hours | Y hours | |

**Resource Concerns**:
- [Concern]

## Recommendations

1. [Recommendation]
2. [Recommendation]

## Gate Decision

- [ ] PASS - Design is sound, proceed to implementation
- [ ] PASS_WITH_FIXES - Minor issues, fix and proceed
- [ ] REVISE - Significant design issues
- [ ] BLOCK - Design does not validly test hypothesis
```

## Key Rules

- Pilot > 24 hours is a critical issue
- Ambiguous success criteria block approval
- Must test core hypothesis directly
- Resource estimates need debugging buffer