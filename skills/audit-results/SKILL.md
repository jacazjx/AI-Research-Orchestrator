---
name: autoresearch:audit-results
agent: adviser
description: Audit experiment results for traceability, statistical validity, and negative result handling. Use when user says "audit results", "review experiment results", "审核实验结果", or needs to verify experiment outcomes.
argument-hint: [results-path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

## Purpose

Critically review experiment results for traceability, statistical validity, and complete reporting.

## Workflow

### Step 1: Review Results Summary

Read `docs/reports/experiments/results-summary.md` and evidence package.

### Step 2: Verify Traceability

Check:
- All results have run IDs
- Configs logged and reproducible
- Checkpoints exist where claimed
- Logs accessible

### Step 3: Assess Statistical Validity

Evaluate:
- Error bars reported
- Significance tests performed
- Confidence intervals included
- Outliers handled appropriately

### Step 4: Check Baseline Comparisons

Verify:
- Baselines properly implemented
- Fair comparison conditions
- Reported accurately

### Step 5: Review Negative Results

Ensure:
- All experiments reported
- Negative results not hidden
- Failure analysis included

## Output

```markdown
# Results Audit Report

## Summary
- **Overall Assessment**: PASS / REVISE_NEEDED / MAJOR_REVISION
- **Traceability Score**: X/10
- **Statistical Validity**: X/10

## Traceability Check

| Result | Run ID | Config | Checkpoint | Logs |
|--------|--------|--------|------------|------|
| [Result 1] | Yes/No | Yes/No | Yes/No | Yes/No |

**Untraceable Results**:
- [Result without proper documentation]

## Statistical Validity

| Metric | Error Bars | Significance Test | CI | Status |
|--------|------------|-------------------|-----|--------|
| [Metric 1] | Yes/No | Yes/No | Yes/No | Pass/Fail |

**Statistical Issues**:
- [Issue]

## Baseline Comparisons

| Baseline | Implementation | Fair? | Reported Accurately? |
|----------|----------------|-------|---------------------|
| [Baseline 1] | Verified/Unverified | Yes/No | Yes/No |

**Baseline Concerns**:
- [Concern]

## Negative Results Review

| Experiment | Reported? | Analysis? | Status |
|------------|-----------|-----------|--------|
| [Exp 1] | Yes/No | Yes/No | [Status] |

**Unreported Experiments**:
- [Experiment not in report]

## Claims Verification

| Claim | Supported By | Verified? | Notes |
|-------|--------------|-----------|-------|
| [Claim 1] | [Result ref] | Yes/No | |

**Unsupported Claims**:
- [Claim without support]

## Recommendations

1. [Recommendation]
2. [Recommendation]

## Gate Decision

- [ ] PASS - Results are traceable and valid
- [ ] PASS_WITH_FIXES - Minor issues, address and proceed
- [ ] REVISE - Significant gaps in results
- [ ] BLOCK - Critical traceability or validity issues
```

## Key Rules

- Untraceable results are critical issues
- Hidden negative results are blockers
- Statistical claims must have evidence
- All experiments must be reported