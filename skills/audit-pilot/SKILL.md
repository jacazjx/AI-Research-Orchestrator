---
name: airesearchorchestrator:audit-pilot
agent: adviser
description: Audit pilot results for hypothesis validation, reproducibility, and decision support. Use when user says "audit pilot", "review pilot results", "审核 Pilot 结果", or needs to verify pilot experiment outcomes.
argument-hint: [pilot-validation-report-path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

## Purpose

Critically review pilot experiment results for hypothesis validation and reproducibility using a rigorous 7-stage review process.

## 7-Stage Review Process

### Stage 1: Initial Assessment

Evaluate the overall completeness of the pilot study:

- [ ] Pilot objectives clearly stated
- [ ] Success criteria defined before experiments
- [ ] Hypothesis to validate is explicit
- [ ] Scope and limitations acknowledged
- [ ] Timeline and resources documented

### Stage 2: Detailed Section Review

Examine each component of the pilot report:

- [ ] Experimental design is sound
- [ ] Data collection methodology documented
- [ ] Results presented clearly and accurately
- [ ] Analysis methods appropriate for data type
- [ ] Conclusions follow from results

### Stage 3: Methodological Rigor

Assess the rigor of experimental methodology:

- [ ] Control experiments included
- [ ] Baselines properly defined
- [ ] Random seeds documented
- [ ] Hyperparameters recorded
- [ ] Environment specifications complete
- [ ] Appropriate sample size justified

### Stage 4: Reproducibility Check

Verify all reproducibility elements:

| Item | Required | Documented | Location |
|------|----------|------------|----------|
| Code location | Yes | Yes/No | |
| Code version/commit | Yes | Yes/No | |
| Data location | Yes | Yes/No | |
| Environment spec | Yes | Yes/No | |
| Commands to run | Yes | Yes/No | |
| Random seeds | Yes | Yes/No | |
| Hyperparameters | Yes | Yes/No | |
| Hardware spec | Recommended | Yes/No | |

### Stage 5: Figure and Data Presentation

Review figures and data presentations:

- [ ] Figures have clear labels and captions
- [ ] Error bars shown where appropriate
- [ ] Raw data accessible
- [ ] Tables formatted correctly
- [ ] Visualizations match the data

### Stage 6: Ethics Consideration

Check for ethical and responsible research:

- [ ] Data usage rights verified
- [ ] Privacy considerations addressed (if applicable)
- [ ] Potential harms identified
- [ ] Bias considerations addressed
- [ ] Limitations honestly reported

### Stage 7: Writing Quality

Evaluate documentation quality:

- [ ] Clear and concise language
- [ ] Logical flow
- [ ] Consistent terminology
- [ ] All claims supported by data
- [ ] No placeholder text

## Statistical Evaluation Criteria

### Sample Size Adequacy

| Aspect | Requirement | Met? |
|--------|-------------|------|
| Minimum runs | >= 3 runs for variance estimation | Yes/No/N/A |
| Sample size justification | Documented rationale | Yes/No |
| Statistical power | Considered (if applicable) | Yes/No/N/A |

### Test Selection Appropriateness

| Scenario | Recommended Test | Verified |
|----------|-------------------|----------|
| Comparing two groups | t-test or non-parametric equivalent | Yes/No/N/A |
| Multiple comparisons | ANOVA + post-hoc with correction | Yes/No/N/A |
| Proportion comparisons | Chi-square or Fisher's exact | Yes/No/N/A |
| Correlation analysis | Pearson/Spearman with CI | Yes/No/N/A |

### Multiple Comparisons Handling

| Item | Required When | Status |
|------|---------------|--------|
| Bonferroni correction | Multiple hypotheses tested | Yes/No/N/A |
| FDR control | Many comparisons | Yes/No/N/A |
| Pre-registration of tests | Hypothesis testing | Yes/No/N/A |

### Effect Size Reporting

| Item | Required | Reported |
|------|----------|----------|
| Effect size measure | Yes | Yes/No |
| Confidence intervals | Yes | Yes/No |
| Standard errors | Yes | Yes/No |
| Practical significance | Recommended | Yes/No |

## Reproducibility Standards

### Code Availability

| Item | Status | Notes |
|------|--------|-------|
| Repository URL | Documented/Missing | |
| Commit hash | Documented/Missing | |
| Branch/tag | Documented/Missing | |
| Setup instructions | Documented/Missing | |
| Dependencies listed | Documented/Missing | |

### Data Availability

| Item | Status | Notes |
|------|--------|-------|
| Data location | Documented/Missing | |
| Data format | Documented/Missing | |
| Access instructions | Documented/Missing | |
| Data license | Documented/Missing | |

### Environment Documentation

| Item | Required | Documented |
|------|----------|------------|
| Python/R version | Yes | Yes/No |
| Package versions | Yes | Yes/No |
| OS version | Yes | Yes/No |
| GPU model (if used) | Yes | Yes/No |
| CUDA version (if used) | Yes | Yes/No |

### Hyperparameters and Seeds

| Item | Required | Documented |
|------|----------|------------|
| Learning rate | Yes | Yes/No |
| Batch size | Yes | Yes/No |
| Epochs/iterations | Yes | Yes/No |
| Random seed | Yes | Yes/No |
| Cross-validation folds | Yes | Yes/No |
| Train/val/test split | Yes | Yes/No |

### Reproducibility Score Calculation

```
Score = (Items Documented / Total Required Items) * 10

Required Items: Code location, Data location, Commands, Seeds, Hyperparameters, Environment spec
Recommended Items: Hardware spec, Exact versions, Step-by-step instructions
```

## Reporting Standards Reference

Apply relevant standards based on research type:

| Research Type | Applicable Standards |
|---------------|---------------------|
| ML Experiment | CLAIM, internal standards |
| Clinical Pilot | CONSORT pilot extension |
| Animal Study | ARRIVE |
| Observational | STROBE |

For detailed checklists, see: `references/reporting_standards.md`

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
- Hyperparameters recorded

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

### Step 6: Apply Statistical Evaluation

Run through statistical criteria if quantitative results present.

### Step 7: Complete 7-Stage Review

Document findings for each stage.

## Output

```markdown
# Pilot Results Audit Report

## Summary
- **Overall Assessment**: PASS / REVISE_NEEDED / MAJOR_REVISION
- **Hypothesis Validated**: YES / PARTIAL / NO
- **Reproducibility Score**: X/10
- **7-Stage Score**: X/7 stages passed

## 7-Stage Review

| Stage | Passed | Issues |
|-------|--------|--------|
| Initial Assessment | Yes/No | [Issues] |
| Detailed Section Review | Yes/No | [Issues] |
| Methodological Rigor | Yes/No | [Issues] |
| Reproducibility Check | Yes/No | [Issues] |
| Figure and Data Presentation | Yes/No | [Issues] |
| Ethics Consideration | Yes/No | [Issues] |
| Writing Quality | Yes/No | [Issues] |

## Results Verification

| Metric | Target | Reported | Verified | Status |
|--------|--------|----------|----------|--------|
| [Metric 1] | X | Y | Yes/No | Pass/Fail |

**Unverified Claims**:
- [Claim]

## Statistical Evaluation

| Criterion | Met? | Notes |
|-----------|------|-------|
| Sample size adequacy | Yes/No/N/A | |
| Correct test selection | Yes/No/N/A | |
| Multiple comparison correction | Yes/No/N/A | |
| Effect size reported | Yes/No/N/A | |
| Confidence intervals | Yes/No/N/A | |

**Statistical Issues**:
- [Issue]

## Hypothesis Assessment

| Aspect | Status | Evidence |
|--------|--------|----------|
| Core hypothesis | Validated/Partial/Failed | [Evidence] |
| Success criteria met | Yes/No | [Which criteria] |

## Reproducibility Check

### Code Availability
| Item | Documented? | Verified? |
|------|-------------|-----------|
| Code location | Yes/No | Yes/No |
| Commit hash | Yes/No | Yes/No |
| Setup instructions | Yes/No | Yes/No |

### Data Availability
| Item | Documented? | Verified? |
|------|-------------|-----------|
| Data location | Yes/No | Yes/No |
| Data format | Yes/No | Yes/No |
| Access instructions | Yes/No | Yes/No |

### Environment
| Item | Documented? | Verified? |
|------|-------------|-----------|
| Language version | Yes/No | Yes/No |
| Package versions | Yes/No | Yes/No |
| Hardware spec | Yes/No | Yes/No |

### Hyperparameters and Seeds
| Item | Documented? | Value |
|------|-------------|-------|
| Learning rate | Yes/No | [Value] |
| Batch size | Yes/No | [Value] |
| Random seed | Yes/No | [Value] |
| Train/val/test split | Yes/No | [Value] |

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
- 7-stage review is mandatory
- Statistical claims require evidence
- Reproducibility score must be >= 7/10 to pass
- All hyperparameters must be documented