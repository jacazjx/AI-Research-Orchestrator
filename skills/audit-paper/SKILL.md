---
name: airesearchorchestrator:audit-paper
agent: reviewer
description: Review paper draft for scientific rigor, writing quality, and citation authenticity. Use when user says "audit paper", "review paper", "审核论文", or needs to verify manuscript quality.
argument-hint: [paper-directory]
allowed-tools: Bash(curl), Read, Write, Edit, Grep, Glob, WebFetch
---

## Purpose

Critically review the paper manuscript for scientific quality, writing, and authenticity.

## Workflow

### Step 1: Review Manuscript

Read `paper/main.tex` or equivalent for content and structure.

### Step 2: Verify Claims and Evidence

Check:
- Claims supported by experiments
- Numbers match results
- Figures accurate and clear
- Tables formatted correctly

### Step 3: Assess Writing Quality

Evaluate:
- Clarity and readability
- Logical flow
- Consistent terminology
- No placeholder text

### Step 4: Verify Citations

For all citations:
- Verify authenticity via academic APIs
- Check DOI validity
- Flag potential fabrications
- Ensure proper attribution

### Step 5: Check Reproducibility

Verify:
- Code availability statement
- Data availability statement
- Hyperparameters documented
- Seeds documented

## Output

```markdown
# Paper Audit Report

## Summary
- **Overall Assessment**: PASS / REVISE_NEEDED / MAJOR_REVISION
- **Scientific Rigor**: X/10
- **Writing Quality**: X/10
- **Citation Authenticity**: X/10

## Claims and Evidence

| Claim | Page | Evidence | Accurate? | Notes |
|-------|------|----------|-----------|-------|
| [Claim 1] | X | [Reference] | Yes/No | |

**Unsupported Claims**:
- [Claim without evidence]

**Inaccurate Claims**:
- [Claim with wrong numbers]

## Writing Quality

| Aspect | Score | Notes |
|--------|-------|-------|
| Clarity | X/10 | |
| Flow | X/10 | |
| Terminology | X/10 | |
| Grammar | X/10 | |

**Placeholders Found**:
- [Location]: [Placeholder text]

## Citation Verification

| Citation | Verified? | Source | Issue |
|----------|-----------|--------|-------|
| [Key] | Yes/No | [API] | [Issue if any] |

**Potential Fabrications**:
- [Citation and concern]

**Verification Rate**: X% (Y/Z citations)

## Figure and Table Review

| Item | Page | Accurate? | Clear? | Issues |
|------|------|-----------|--------|--------|
| Fig 1 | X | Yes/No | Yes/No | |

## Reproducibility Check

| Aspect | Documented? | Location |
|--------|-------------|----------|
| Code | Yes/No | [URL/path] |
| Data | Yes/No | [URL/path] |
| Hyperparameters | Yes/No | Section X |
| Seeds | Yes/No | Section X |

## Recommendations

1. [Recommendation]
2. [Recommendation]

## Gate Decision

- [ ] PASS - Paper ready for submission
- [ ] PASS_WITH_FIXES - Minor revisions needed
- [ ] REVISE - Significant revisions required
- [ ] BLOCK - Critical issues (fabrication, unsupported claims)
```

## Key Rules

- Citation verification rate must be >90%
- Any fabrication is a blocker
- Placeholders must be removed
- Claims must match experimental results