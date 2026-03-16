---
name: airesearchorchestrator:audit-survey
agent: critic
description: Audit literature survey for completeness, citation authenticity, and novelty claims. Use when user says "audit survey", "review literature", "审核文献调研", or needs to verify survey quality.
argument-hint: [survey-report-path]
allowed-tools: Bash(curl), Read, Write, Edit, Grep, Glob, WebFetch
---

## Purpose

Critically review the literature survey for completeness, citation authenticity, and novelty claims.

## Workflow

### Step 1: Review Survey Report

Read `docs/reports/survey/research-readiness-report.md` and related materials.

### Step 2: Verify Citation Authenticity

For each cited paper:
- Verify via academic APIs (Semantic Scholar, arXiv, CrossRef)
- Check DOI validity
- Flag potential fabrications

### Step 3: Assess Literature Coverage

Evaluate:
- Number of papers reviewed (minimum 10)
- Recency (last 2-3 years priority)
- Seminal papers included
- Competing approaches covered

### Step 4: Evaluate Novelty Claims

For each novelty claim:
- Is it supported by gap analysis?
- Are similar/concurrent works acknowledged?
- Is differentiation clear?

### Step 5: Check Problem Definition

Assess:
- Is hypothesis testable?
- Are success criteria clear?
- Is scope appropriate?

## Output

Save audit report with verdict:

```markdown
# Survey Audit Report

## Summary
- **Overall Assessment**: PASS / REVISE_NEEDED / MAJOR_REVISION
- **Critical Issues**: X
- **Warnings**: Y

## Citation Authenticity

| Citation | Status | Source | Notes |
|----------|--------|--------|-------|
| author2023 | VERIFIED | Semantic Scholar | |
| unknown2022 | UNVERIFIED | - | NOT FOUND |

**Fabrication Risk**: LOW / MEDIUM / HIGH

## Literature Coverage

| Aspect | Status | Notes |
|--------|--------|-------|
| Paper count | Sufficient/Insufficient | X papers reviewed |
| Recency | Good/Poor | X% from last 3 years |
| Seminal papers | Included/Missing | |
| Competing approaches | Covered/Missing | |

## Novelty Assessment

| Claim | Supported? | Evidence | Issues |
|-------|------------|----------|--------|
| [Claim 1] | Yes/No | [Evidence] | [Issues] |

## Problem Definition

| Aspect | Clear? | Notes |
|--------|--------|-------|
| Hypothesis | Yes/No | |
| Success criteria | Yes/No | |
| Scope | Yes/No | |

## Recommendations

1. [Recommendation]
2. [Recommendation]

## Gate Decision

- [ ] PASS - Proceed to pilot phase
- [ ] PASS_WITH_FIXES - Minor issues, fix and proceed
- [ ] REVISE - Significant revision required
- [ ] BLOCK - Critical issues, do not proceed
```

## Key Rules

- Must verify EVERY citation via academic APIs
- Must flag any potential fabrications
- Novelty claims must have supporting evidence
- Use academic APIs, NOT web search