---
name: autoresearch:audit-pilot
agent: adviser
description: Audit pilot results for hypothesis validation, reproducibility, and decision support. Use when user says "audit pilot", "review pilot results", "审核 Pilot 结果", or needs to verify pilot experiment outcomes.
argument-hint: [pilot-validation-report-path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

## Purpose

Critically review pilot experiment results for hypothesis validation and reproducibility.

## Workflow

### Step 1: Review Validation Report

Read `docs/reports/pilot/pilot-validation-report.md` for results and conclusions.

### Step 2: Verify Results

Check:
- Metrics match success criteria
- Claims supported by data
- Negative results reported honestly
- Statistical validity (if applicable)

### Step 3: Assess Reproducibility

Verify:
- Code location documented
- Commands to reproduce provided
- Random seeds documented
- Environment specifications

### Step 4: Evaluate Decision

Assess:
- Go/No-Go recommendation supported by data
- Lessons learned actionable
- Next steps appropriate

### Step 5: Check Implementation

Review:
- Deviations from design explained
- Issues documented
- Root causes identified

## Output

```markdown
# Pilot Results Audit Report

## Summary
- **Overall Assessment**: PASS / REVISE_NEEDED / MAJOR_REVISION
- **Hypothesis Validated**: YES / PARTIAL / NO
- **Reproducibility Score**: X/10

## Results Verification

| Metric | Target | Reported | Verified | Status |
|--------|--------|----------|----------|--------|
| [Metric 1] | X | Y | Yes/No | Pass/Fail |

**Unverified Claims**:
- [Claim]

## Hypothesis Assessment

| Aspect | Status | Evidence |
|--------|--------|----------|
| Core hypothesis | Validated/Partial/Failed | [Evidence] |
| Success criteria met | Yes/No | [Which criteria] |

## Reproducibility Check

| Item | Documented? | Verified? |
|------|-------------|-----------|
| Code location | Yes/No | Yes/No |
| Commands | Yes/No | Yes/No |
| Seeds | Yes/No | Yes/No |
| Environment | Yes/No | Yes/No |

**Reproducibility Issues**:
- [Issue]

## Decision Review

| Aspect | Sound? | Notes |
|--------|--------|-------|
| Recommendation supported | Yes/No | |
| Lessons actionable | Yes/No | |
| Next steps appropriate | Yes/No | |

**Decision Concerns**:
- [Concern]

## Implementation Review

| Deviation | Justified? | Impact |
|-----------|------------|--------|
| [Deviation] | Yes/No | [Impact] |

## Recommendations

1. [Recommendation]
2. [Recommendation]

## Gate Decision

- [ ] PASS - Pilot validated, proceed to full experiments
- [ ] PASS_WITH_FIXES - Minor issues, address and proceed
- [ ] REVISE - Pilot needs revision or re-run
- [ ] NO_GO - Hypothesis not validated, consider pivot
```

## Key Rules

- Must verify results match reported data
- Missing reproducibility info is critical
- Negative results must be reported honestly
- Go/No-Go must be supported by data