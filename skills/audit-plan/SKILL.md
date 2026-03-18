---
name: airesearchorchestrator:audit-plan
description: Audit research execution plan for feasibility, resource adequacy, and risk coverage. Use when user says "audit plan", "review research plan", "审核研究计划", or needs to verify planning quality.
user-invocable: false
argument-hint: [research-plan-path]
allowed-tools: Read, Write, Edit, Grep, Glob
---
## Purpose

Critically review the research execution plan for feasibility and completeness.

## Workflow

### Step 1: Review Plan Document

Read `docs/reports/survey/research-readiness-report.md` focusing on planning sections.

### Step 2: Assess Feasibility

Evaluate:
- Timeline realism (include buffer?)
- Resource adequacy
- Technical feasibility
- Team capability alignment

### Step 3: Evaluate Experiment Design

Check:
- Clear variables and metrics
- Appropriate baselines
- Statistical validity
- Reproducibility provisions

### Step 4: Review Risk Management

Assess:
- Risk identification completeness
- Mitigation strategies adequacy
- Fallback plans existence
- Go/No-Go criteria clarity

### Step 5: Check Dependencies

Verify:
- External dependencies identified
- Contingency for blocked dependencies
- Critical path identified

## Output

```markdown
# Plan Audit Report

## Summary
- **Overall Assessment**: PASS / REVISE_NEEDED / MAJOR_REVISION
- **Feasibility Score**: X/10
- **Risk Coverage**: X%

## Feasibility Assessment

| Aspect | Score | Notes |
|--------|-------|-------|
| Timeline | X/10 | [Buffer included? Realistic?] |
| Resources | X/10 | [Adequate? Buffer?] |
| Technical | X/10 | [Achievable? Proven?] |
| Team | X/10 | [Skills match?] |

## Experiment Design Review

| Criterion | Status | Notes |
|-----------|--------|-------|
| Variables defined | Yes/No | |
| Metrics appropriate | Yes/No | |
| Baselines included | Yes/No | |
| Statistical validity | Yes/No | |
| Reproducibility | Yes/No | |

## Risk Management Review

| Risk | Identified? | Mitigation? | Adequate? |
|------|-------------|-------------|-----------|
| [Risk 1] | Yes/No | Yes/No | Yes/No |

**Unidentified Risks**:
- [Risk not in plan]

## Dependency Check

| Dependency | Type | Contingency | Status |
|------------|------|-------------|--------|
| [Dep 1] | Internal/External | [Plan] | OK/Risk |

## Recommendations

1. [Recommendation]
2. [Recommendation]

## Gate Decision

- [ ] PASS - Plan is sound, proceed
- [ ] PASS_WITH_FIXES - Minor adjustments needed
- [ ] REVISE - Significant gaps in planning
- [ ] BLOCK - Plan is not viable
```

## Key Rules

- Timeline without buffer is automatically flagged
- Resource estimates need 20% buffer minimum
- Missing fallback plans are critical issues
- Go/No-Go criteria must be unambiguous