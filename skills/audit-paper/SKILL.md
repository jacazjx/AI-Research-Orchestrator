---
name: airesearchorchestrator:audit-paper
agent: reviewer
description: Review paper draft for scientific rigor, writing quality, and citation authenticity. Use when user says "audit paper", "review paper", "审核论文", or needs to verify manuscript quality.
argument-hint: [paper-directory]
allowed-tools: Bash(curl), Read, Write, Edit, Grep, Glob, WebFetch
---

## Purpose

Critically review the paper manuscript for scientific quality, writing, and authenticity using a rigorous 7-stage review process.

## 7-Stage Review Process

### Stage 1: Initial Assessment

Evaluate the overall structure and completeness:

- [ ] Title clearly describes the work
- [ ] Abstract contains all required elements (background, methods, results, conclusion)
- [ ] Keywords/index terms provided
- [ ] Main sections present (Introduction, Methods, Results, Discussion)
- [ ] References section complete
- [ ] Acknowledgments and funding included

### Stage 2: Detailed Section Review

Examine each section systematically:

#### Introduction
- [ ] Background provides sufficient context
- [ ] Gap in knowledge clearly identified
- [ ] Research question/hypothesis stated
- [ ] Contribution summarized
- [ ] Paper structure outlined (if field standard)

#### Methods
- [ ] Study design described
- [ ] Participants/data source detailed
- [ ] Sample size justified
- [ ] Variables defined
- [ ] Procedures described for replication
- [ ] Statistical methods specified

#### Results
- [ ] Results address all research questions
- [ ] Data presented in logical order
- [ ] Tables and figures referenced in text
- [ ] Statistical results properly reported
- [ ] Negative results included

#### Discussion
- [ ] Main findings summarized
- [ ] Findings interpreted in context
- [ ] Comparison with prior work
- [ ] Limitations acknowledged
- [ ] Implications stated
- [ ] Future directions outlined

### Stage 3: Methodological Rigor

Assess the rigor of the methodology:

- [ ] Methods sufficient for replication
- [ ] Study design appropriate for question
- [ ] Sample size/power calculation documented
- [ ] Control/comparison groups justified
- [ ] Outcome measures validated
- [ ] Statistical approach appropriate
- [ ] Assumptions checked and reported
- [ ] Limitations addressed

### Stage 4: Reproducibility Check

Verify all reproducibility elements:

| Item | Required | Present | Location |
|------|----------|---------|----------|
| Code availability statement | Yes | Yes/No | |
| Data availability statement | Yes | Yes/No | |
| Repository URL | Recommended | Yes/No | |
| DOI/version | Recommended | Yes/No | |
| Hyperparameters documented | Yes | Yes/No | |
| Random seeds documented | Yes | Yes/No | |
| Environment specified | Recommended | Yes/No | |
| Pre-registration | Field-dependent | Yes/No | |

### Stage 5: Figure and Table Presentation

Review all figures and tables:

- [ ] Each figure has caption
- [ ] Figure legends explain all elements
- [ ] Tables have column headers
- [ ] Table notes explain abbreviations
- [ ] Error bars described (SD, SEM, CI)
- [ ] Statistical significance indicated
- [ ] Resolution sufficient for print
- [ ] Color choices accessible (colorblind-friendly)

### Stage 6: Ethics Consideration

Check for ethical dimensions:

- [ ] IRB/Ethics approval stated (if human subjects)
- [ ] Informed consent mentioned (if required)
- [ ] Animal welfare statement (if applicable)
- [ ] Data privacy addressed
- [ ] Conflicts of interest disclosed
- [ ] Funding sources declared
- [ ] Author contributions stated

### Stage 7: Writing Quality

Evaluate writing quality:

- [ ] Clear and concise language
- [ ] Logical flow between sections
- [ ] Consistent terminology throughout
- [ ] Appropriate for target audience
- [ ] Grammar and spelling correct
- [ ] No placeholder text (TODO, FIXME, etc.)
- [ ] Word count within limits
- [ ] Citation format consistent

## Statistical Evaluation Criteria

### Sample Size Adequacy

| Aspect | Requirement | Met? | Location in Paper |
|--------|-------------|------|-------------------|
| Power analysis | Documented | Yes/No | Section X |
| Sample size justification | Required | Yes/No | Section X |
| Effect size for power | Stated | Yes/No | Section X |
| Alpha level | Stated (typically 0.05) | Yes/No | Section X |

### Test Selection Appropriateness

Verify statistical tests match data characteristics:

| Data Characteristic | Check | Appropriate Test |
|--------------------|-------|-------------------|
| Normal distribution | Tested? | Parametric vs non-parametric |
| Independence | Assumed? | Paired vs independent tests |
| Equal variances | Tested? | Standard vs Welch's correction |
| Sample size | Adequate? | Normal approximation valid |

### Multiple Comparisons Handling

| Scenario | Required | Present |
|----------|----------|---------|
| Multiple primary outcomes | Pre-specification or correction | Yes/No/N/A |
| Subgroup analyses | Correction or exploratory label | Yes/No/N/A |
| Post-hoc tests | Correction method stated | Yes/No/N/A |
| Interim analyses | Pre-specified stopping rules | Yes/No/N/A |

### Effect Size Reporting

| Result | Effect Size Reported | CI Reported | P-value Format |
|--------|---------------------|-------------|----------------|
| [Result 1] | Yes/No | Yes/No | Exact/Threshold/N/A |

**Required Format:**
- Effect size with CI: "The treatment reduced symptoms (d = 0.65, 95% CI [0.32, 0.98])"
- P-value: Exact value preferred (p = 0.03) over threshold (p < 0.05)

## Reproducibility Standards

### Code Availability

| Item | Status | Location | Notes |
|------|--------|----------|-------|
| Availability statement | Present/Missing | | |
| Repository URL | Present/Missing | | |
| License specified | Yes/No | | |
| Documentation | Adequate/Inadequate | | |

### Data Availability

| Item | Status | Location | Notes |
|------|--------|----------|-------|
| Availability statement | Present/Missing | | |
| Access method | Public/Upon request/Not available | | |
| Data description | Adequate/Inadequate | | |
| License/restrictions | Stated/Not stated | | |

### Methods Reproducibility

| Item | Present | Location | Notes |
|------|---------|----------|-------|
| Hyperparameters | Yes/No | | |
| Random seeds | Yes/No | | |
| Software versions | Yes/No | | |
| Hardware specs | Yes/No | | |
| Preprocessing steps | Yes/No | | |
| Train/val/test splits | Yes/No | | |

### Reproducibility Score

```
Score = (Items Present / Total Required Items) * 10

Required: Code statement, Data statement, Hyperparameters, Seeds
Recommended: Repository URL, Software versions, Hardware specs
```

## Reporting Standards Reference

Apply relevant standards based on paper type:

| Paper Type | Primary Standard | Checklist Items | Key Requirements |
|------------|------------------|-----------------|------------------|
| RCT | CONSORT | 25 items | Flow diagram, ITT, registration |
| Systematic Review | PRISMA | 27 items | Flow diagram, search strategy |
| Cohort Study | STROBE | 22 items | Follow-up, losses to follow-up |
| Case-Control | STROBE | 22 items | Matching, selection criteria |
| Cross-Sectional | STROBE | 22 items | Sampling method |
| Animal Study | ARRIVE | Essential 10 | Sample size, randomization, blinding |
| ML/AI Paper | CLAIM | Key items | Data splits, baselines, metrics |

### Standard-Specific Checks

#### For CONSORT (RCT)
- [ ] Title identifies as randomized
- [ ] Flow diagram shows participant progression
- [ ] Randomization method described
- [ ] Allocation concealment described
- [ ] Blinding described (who was blinded)
- [ ] All pre-specified outcomes reported
- [ ] Harms/adverse events reported
- [ ] Trial registration number

#### For PRISMA (Systematic Review)
- [ ] Title identifies as systematic review
- [ ] Abstract structured with required elements
- [ ] PRISMA flow diagram included
- [ ] Search strategy fully documented
- [ ] Risk of bias assessment included
- [ ] Publication bias assessed (if meta-analysis)
- [ ] Registration number provided

#### For STROBE (Observational)
- [ ] Study design stated in title/abstract
- [ ] Setting and participants described
- [ ] All variables defined
- [ ] Potential sources of bias addressed
- [ ] Sample size justification
- [ ] Handling of missing data described
- [ ] Sensitivity analyses described

#### For ARRIVE (Animal Studies)
- [ ] Sample size justified
- [ ] Inclusion/exclusion criteria stated
- [ ] Randomization described
- [ ] Blinding described
- [ ] Primary/secondary outcomes defined
- [ ] Housing conditions described
- [ ] Ethical approval stated

For detailed checklists, see: `references/reporting_standards.md`

## Citation Verification

### Verification Process

For each citation:
1. Verify via academic APIs (Semantic Scholar, CrossRef, arXiv)
2. Check DOI validity
3. Confirm publication details match
4. Flag potential fabrications
5. Verify content claims match cited work

### Verification Standards

| Citation Type | Required Verification |
|---------------|----------------------|
| Journal article | DOI verification via CrossRef |
| arXiv preprint | arXiv ID verification |
| Conference paper | DBLP/Semantic Scholar verification |
| Book | ISBN verification |
| Website | URL accessibility check |

### Citation Quality Checks

| Issue | Severity | Action |
|-------|----------|--------|
| Fabricated citation | CRITICAL | Flag immediately |
| Wrong claims attributed | HIGH | Note discrepancy |
| Retracted source | HIGH | Flag and verify |
| Preprint without version | MEDIUM | Request version |
| Incomplete citation | LOW | Request full details |

## Workflow

### Step 1: Review Manuscript

Read `paper/main.tex` or equivalent for content and structure.

### Step 2: Apply 7-Stage Review

Work through each stage systematically.

### Step 3: Verify Claims and Evidence

Check:
- Claims supported by experiments
- Numbers match results
- Figures accurate and clear
- Tables formatted correctly

### Step 4: Evaluate Statistical Rigor

Apply statistical evaluation criteria.

### Step 5: Assess Reproducibility

Verify:
- Code availability statement
- Data availability statement
- Hyperparameters documented
- Seeds documented
- Methods sufficient for replication

### Step 6: Verify Citations

For all citations:
- Verify authenticity via academic APIs
- Check DOI validity
- Flag potential fabrications
- Ensure proper attribution

### Step 7: Check Reporting Standards

Apply appropriate standard based on paper type.

## Output

```markdown
# Paper Audit Report

## Summary
- **Overall Assessment**: PASS / REVISE_NEEDED / MAJOR_REVISION
- **Scientific Rigor**: X/10
- **Writing Quality**: X/10
- **Citation Authenticity**: X/10
- **Reproducibility Score**: X/10
- **7-Stage Score**: X/7 stages passed

## 7-Stage Review

| Stage | Passed | Issues |
|-------|--------|--------|
| Initial Assessment | Yes/No | [Issues] |
| Detailed Section Review | Yes/No | [Issues] |
| Methodological Rigor | Yes/No | [Issues] |
| Reproducibility Check | Yes/No | [Issues] |
| Figure and Table Presentation | Yes/No | [Issues] |
| Ethics Consideration | Yes/No | [Issues] |
| Writing Quality | Yes/No | [Issues] |

## Claims and Evidence

| Claim | Page | Evidence | Accurate? | Notes |
|-------|------|----------|-----------|-------|
| [Claim 1] | X | [Reference] | Yes/No | |

**Unsupported Claims**:
- [Claim without evidence]

**Inaccurate Claims**:
- [Claim with wrong numbers]

## Statistical Evaluation

### Sample Size and Power

| Aspect | Documented | Adequate | Notes |
|--------|------------|----------|-------|
| Power analysis | Yes/No | Yes/No | |
| Sample size justification | Yes/No | Yes/No | |

### Test Appropriateness

| Analysis | Test | Appropriate | Assumptions Met |
|----------|------|-------------|-----------------|
| [Analysis 1] | [Test] | Yes/No | Yes/No |

### Multiple Comparisons

| Analysis | Tests | Correction | Method |
|----------|-------|------------|--------|
| [Analysis 1] | X | Yes/No | [Method] |

### Effect Sizes

| Result | Effect Size | CI | P-value |
|--------|-------------|-----|---------|
| [Result 1] | [Value] | [CI] | [p] |

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
| Code availability | Yes/No | [URL/path] |
| Data availability | Yes/No | [URL/path] |
| Hyperparameters | Yes/No | Section X |
| Seeds | Yes/No | Section X |
| Software versions | Yes/No | Section X |
| Hardware specs | Yes/No | Section X |

**Reproducibility Issues**:
- [Issue]

## Reporting Standards Compliance

| Standard | Applicable | Compliance | Missing Items |
|----------|-----------|------------|---------------|
| CONSORT | Yes/No | X% | [List] |
| PRISMA | Yes/No | X% | [List] |
| STROBE | Yes/No | X% | [List] |
| ARRIVE | Yes/No | X% | [List] |

**Critical Missing Items**:
- [Item 1]
- [Item 2]

## Ethics and Integrity

| Item | Present | Notes |
|------|---------|-------|
| IRB/Ethics approval | Yes/No/N/A | |
| Informed consent | Yes/No/N/A | |
| Conflicts of interest | Yes/No | |
| Funding statement | Yes/No | |
| Author contributions | Yes/No | |

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
- 7-stage review is mandatory
- Statistical rigor required for all quantitative work
- Reproducibility score must be >= 7/10 to pass
- Reporting standards compliance required
- Ethics statements required for human/animal research