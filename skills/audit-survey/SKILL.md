---
name: airesearchorchestrator:audit-survey
description: Audit literature survey for completeness, citation authenticity, and novelty claims. Use when user says "audit survey", "review literature", "审核文献调研", or needs to verify survey quality.
user-invocable: false
argument-hint: [survey-report-path]
allowed-tools: Bash(curl), Read, Write, Edit, Grep, Glob, WebFetch
---
## Purpose

Critically review the literature survey for completeness, citation authenticity, and novelty claims using a rigorous 7-stage review process.

## 7-Stage Review Process

### Stage 1: Initial Assessment

Evaluate the overall structure and completeness of the survey:

- [ ] Executive summary provides clear overview
- [ ] Research question/hypothesis clearly stated
- [ ] Scope and boundaries defined
- [ ] Literature search methodology documented
- [ ] Inclusion/exclusion criteria specified

### Stage 2: Detailed Section Review

Examine each section for content quality:

- [ ] Background provides sufficient context
- [ ] Related work covers major approaches
- [ ] Gap analysis is thorough and justified
- [ ] Proposed approach positioning is clear
- [ ] Conclusions follow from the analysis

### Stage 3: Methodological Rigor

Assess the rigor of the survey methodology:

- [ ] Search strategy is reproducible (databases, keywords, date range)
- [ ] Selection criteria are explicit
- [ ] Quality assessment of included studies documented
- [ ] Data extraction method described
- [ ] PRISMA guidelines followed (if systematic review)

### Stage 4: Reproducibility Check

Verify reproducibility elements:

- [ ] Search queries documented
- [ ] Database names and versions specified
- [ ] Date of search recorded
- [ ] Inclusion/exclusion criteria for papers documented
- [ ] Full list of papers reviewed provided

### Stage 5: Figure Presentation

Review figures and tables for quality:

- [ ] Tables properly formatted and readable
- [ ] Figures have clear captions
- [ ] Data visualizations are appropriate
- [ ] Comparative tables are fair and balanced

### Stage 6: Ethics Consideration

Check for ethical dimensions:

- [ ] Potential conflicts of interest disclosed
- [ ] Biases in literature selection addressed
- [ ] Limitations of the survey acknowledged
- [ ] Ethical considerations discussed (if applicable)

### Stage 7: Writing Quality

Evaluate communication quality:

- [ ] Clear and concise writing
- [ ] Logical organization
- [ ] Consistent terminology throughout
- [ ] Proper citations format
- [ ] No placeholder text

## Statistical Evaluation Criteria

When the survey includes meta-analysis or quantitative synthesis:

### Sample Size Adequacy

| Criterion | Requirement | Status |
|-----------|-------------|--------|
| Minimum studies | >= 3 studies for meta-analysis | Check |
| Total sample size | Adequate for conclusions | Check |
| Power analysis | Included if combining effect sizes | Check |

### Test Selection Appropriateness

| Test | When Required | Verified |
|------|----------------|----------|
| Heterogeneity test (I-squared) | Meta-analysis | Yes/No/N/A |
| Publication bias test | Meta-analysis with >= 10 studies | Yes/No/N/A |
| Sensitivity analysis | Meta-analysis | Yes/No/N/A |
| Subgroup analysis | When heterogeneity high | Yes/No/N/A |

### Effect Size Reporting

| Item | Required | Present |
|------|----------|---------|
| Effect size measure | Yes | Yes/No |
| Confidence intervals | Yes | Yes/No |
| P-values (if applicable) | Yes | Yes/No |
| Forest plot (meta-analysis) | Recommended | Yes/No/N/A |

## Reproducibility Standards

### Required Documentation

| Item | Required | Documented | Location |
|------|----------|------------|----------|
| Search queries | Yes | Yes/No | [Location] |
| Database list | Yes | Yes/No | [Location] |
| Search dates | Yes | Yes/No | [Location] |
| Inclusion criteria | Yes | Yes/No | [Location] |
| Exclusion criteria | Yes | Yes/No | [Location] |
| Screening log | Recommended | Yes/No | [Location] |

### Reproducibility Score Calculation

```
Score = (Items Documented / Total Required Items) * 10

Required Items: Search queries, Database list, Search dates, Inclusion criteria, Exclusion criteria
Recommended Items: Screening log, Quality assessment form
```

## Reporting Standards Reference

Apply relevant standards based on survey type:

| Survey Type | Primary Standard | Checklist Items |
|-------------|------------------|-----------------|
| Systematic Review | PRISMA | 27 items |
| Literature Survey | PRISMA (adapted) | Core items |
| Scoping Review | PRISMA-ScR | 22 items |

For detailed checklists, see: `references/reporting_standards.md`

## Workflow

### Step 1: Review Survey Report

Read `docs/survey/research-readiness-report.md` and related materials.

### Step 2: Verify Citation Authenticity

For each cited paper:
- Verify via academic APIs (Semantic Scholar, arXiv, CrossRef)
- Check DOI validity
- Flag potential fabrications
- Verify claims match cited content

### Step 3: Assess Literature Coverage

Evaluate:
- Number of papers reviewed (minimum 10)
- Recency (last 2-3 years priority)
- Seminal papers included
- Competing approaches covered
- Geographic/institutional diversity

### Step 4: Evaluate Novelty Claims

For each novelty claim:
- Is it supported by gap analysis?
- Are similar/concurrent works acknowledged?
- Is differentiation clear?
- Is the contribution size appropriate?

### Step 5: Check Problem Definition

Assess:
- Is hypothesis testable?
- Are success criteria clear?
- Is scope appropriate?
- Are assumptions explicit?

### Step 6: Apply 7-Stage Review

Work through each stage systematically, documenting findings.

### Step 7: Evaluate Statistical Rigor (if applicable)

Apply statistical evaluation criteria for any quantitative synthesis.

## Output

Save audit report with verdict:

```markdown
# Survey Audit Report

## Summary
- **Overall Assessment**: PASS / REVISE_NEEDED / MAJOR_REVISION
- **Critical Issues**: X
- **Warnings**: Y
- **7-Stage Score**: X/7 stages passed
- **Reproducibility Score**: X/10

## 7-Stage Review

| Stage | Passed | Issues |
|-------|--------|--------|
| Initial Assessment | Yes/No | [Issues] |
| Detailed Section Review | Yes/No | [Issues] |
| Methodological Rigor | Yes/No | [Issues] |
| Reproducibility Check | Yes/No | [Issues] |
| Figure Presentation | Yes/No | [Issues] |
| Ethics Consideration | Yes/No | [Issues] |
| Writing Quality | Yes/No | [Issues] |

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
| Geographic diversity | Good/Poor | |

## Statistical Evaluation (if applicable)

| Criterion | Met? | Notes |
|-----------|------|-------|
| Sample size adequacy | Yes/No/N/A | |
| Heterogeneity assessed | Yes/No/N/A | |
| Publication bias tested | Yes/No/N/A | |
| Effect sizes reported | Yes/No/N/A | |
| Confidence intervals | Yes/No/N/A | |

## Reproducibility Check

| Item | Documented? | Location |
|------|-------------|----------|
| Search queries | Yes/No | |
| Databases | Yes/No | |
| Search dates | Yes/No | |
| Inclusion criteria | Yes/No | |
| Exclusion criteria | Yes/No | |

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
| Assumptions | Yes/No | |

## Reporting Standards Compliance

| Standard | Applicable | Key Items Missing |
|----------|-----------|-------------------|
| PRISMA | Yes/No | [List missing items] |

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
- 7-stage review is mandatory for all audits
- Statistical rigor required if meta-analysis included
- Reproducibility score must be >= 7/10 to pass