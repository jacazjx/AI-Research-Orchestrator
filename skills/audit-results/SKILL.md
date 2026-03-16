---
name: airesearchorchestrator:audit-results
agent: adviser
description: Audit experiment results for traceability, statistical validity, and negative result handling. Use when user says "audit results", "review experiment results", "审核实验结果", or needs to verify experiment outcomes.
argument-hint: [results-path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

## Purpose

Critically review experiment results for traceability, statistical validity, and complete reporting using a rigorous 7-stage review process.

## 7-Stage Review Process

### Stage 1: Initial Assessment

Evaluate the overall completeness of the results:

- [ ] Executive summary of key findings
- [ ] Research questions/hypotheses restated
- [ ] Success criteria referenced
- [ ] All planned experiments reported
- [ ] Results organized by research question

### Stage 2: Detailed Section Review

Examine each component of the results:

- [ ] Primary outcomes reported first
- [ ] Secondary outcomes clearly labeled
- [ ] Exploratory analyses distinguished
- [ ] Each result linked to hypothesis
- [ ] Negative/null results included

### Stage 3: Methodological Rigor

Assess the rigor of the experimental methodology:

- [ ] Experimental design matches protocol
- [ ] Sample size justified
- [ ] Randomization documented (if applicable)
- [ ] Blinding documented (if applicable)
- [ ] Outcomes defined a priori
- [ ] Analysis plan followed or deviations explained

### Stage 4: Reproducibility Check

Verify all reproducibility elements:

| Item | Required | Documented | Verified |
|------|----------|------------|----------|
| Code repository | Yes | Yes/No | Yes/No |
| Code version (commit/tag) | Yes | Yes/No | Yes/No |
| Data repository | Yes | Yes/No | Yes/No |
| Random seeds | Yes | Yes/No | Yes/No |
| Hyperparameters | Yes | Yes/No | Yes/No |
| Environment spec | Yes | Yes/No | Yes/No |
| Run logs | Recommended | Yes/No | Yes/No |
| Config files | Recommended | Yes/No | Yes/No |

### Stage 5: Figure and Table Presentation

Review all figures and tables:

- [ ] All figures have captions
- [ ] Error bars shown with description (SD, SEM, CI)
- [ ] Tables properly formatted
- [ ] Significant differences clearly marked
- [ ] Raw data available for verification
- [ ] Figure quality sufficient for publication

### Stage 6: Ethics Consideration

Check for ethical dimensions:

- [ ] Data usage rights documented
- [ ] IRB/Ethics approval noted (if human subjects)
- [ ] Privacy protections described
- [ ] Potential harms identified
- [ ] Conflicts of interest disclosed

### Stage 7: Writing Quality

Evaluate documentation quality:

- [ ] Clear and concise writing
- [ ] Logical organization
- [ ] Consistent terminology
- [ ] All claims supported by evidence
- [ ] Limitations acknowledged

## Statistical Evaluation Criteria

### Sample Size Adequacy

| Aspect | Requirement | Met? | Notes |
|--------|-------------|------|-------|
| Power analysis | Documented | Yes/No/N/A | |
| Minimum sample | Appropriate for effect | Yes/No | |
| Multiple runs | >= 3 for variance | Yes/No/N/A | |
| Effect size detection | Justified | Yes/No | |

### Test Selection Appropriateness

| Data Type | Test | Verify |
|-----------|------|--------|
| Continuous, 2 groups | t-test / Mann-Whitney | Correct assumption check |
| Continuous, >2 groups | ANOVA / Kruskal-Wallis | Post-hoc with correction |
| Categorical | Chi-square / Fisher | Expected counts > 5 |
| Paired data | Paired t-test / Wilcoxon | Paired structure maintained |
| Survival | Log-rank / Cox | Censoring handled |
| Correlation | Pearson / Spearman | Appropriate for distribution |
| Regression | Linear / Logistic | Assumptions checked |

### Multiple Comparisons Handling

| Scenario | Required Correction | Verified |
|----------|---------------------|----------|
| Multiple primary outcomes | Pre-specified hierarchy or adjustment | Yes/No |
| Multiple time points | Adjustment or pre-specified | Yes/No |
| Subgroup analyses | Adjustment or exploratory label | Yes/No |
| Post-hoc analyses | Labeled as exploratory | Yes/No |

**Multiple Comparison Methods:**
- Bonferroni correction (conservative)
- Holm-Bonferroni (less conservative)
- Benjamini-Hochberg FDR (for many tests)
- Pre-registration of primary outcomes (preferred)

### Effect Size Reporting

| Item | Requirement | Present | Correct |
|------|-------------|---------|---------|
| Effect size | Required | Yes/No | Yes/No |
| Confidence interval | Required | Yes/No | Yes/No |
| Standard error | Optional | Yes/No | - |
| P-value | Required if testing | Yes/No | Yes/No |
| Effect size interpretation | Recommended | Yes/No | - |

**Effect Size Measures by Test:**

| Test | Effect Size Measure |
|------|---------------------|
| t-test | Cohen's d |
| ANOVA | eta-squared, partial eta-squared |
| Correlation | r, r-squared |
| Chi-square | Cramer's V, phi |
| Regression | standardized beta, R-squared |
| Logistic regression | odds ratio, Cohen's f |

## Reproducibility Standards

### Traceability Requirements

| Result | Run ID | Config | Checkpoint | Logs | Status |
|--------|--------|--------|------------|------|--------|
| [Result 1] | Yes/No | Yes/No | Yes/No | Yes/No | Traceable/Not Traceable |

### Code Availability Standards

| Item | Status | Location | Notes |
|------|--------|----------|-------|
| Repository URL | Documented/Missing | | |
| Commit hash | Documented/Missing | | |
| Branch/tag | Documented/Missing | | |
| Dependencies | Documented/Missing | | |
| Setup script | Documented/Missing | | |

### Data Availability Standards

| Item | Status | Location | Notes |
|------|--------|----------|-------|
| Raw data | Available/Unavailable | | |
| Processed data | Available/Unavailable | | |
| Data dictionary | Available/Unavailable | | |
| Access instructions | Available/Unavailable | | |

### Reproducibility Score Calculation

```
Score = (Items Documented & Verified / Total Required Items) * 10

Required Items:
- Code repository and version
- Data location
- Random seeds
- Hyperparameters
- Environment spec
- Run ID for each result

Recommended Items:
- Run logs
- Config files
- Checkpoints
- Hardware details
```

## Reporting Standards Reference

Apply relevant standards based on research type:

| Research Type | Primary Standard | Key Items |
|---------------|------------------|-----------|
| Clinical Trial | CONSORT | Flow diagram, ITT analysis, adverse events |
| Systematic Review | PRISMA | Flow diagram, risk of bias, study selection |
| Observational Study | STROBE | Confounders, missing data, sensitivity analysis |
| Animal Experiment | ARRIVE | Sample size, randomization, blinding |
| ML/Computational | CLAIM | Data splits, hyperparameters, baselines |

For detailed checklists, see: `references/reporting_standards.md`

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
- Multiple comparisons corrected

### Step 4: Check Baseline Comparisons

Verify:
- Baselines properly implemented
- Fair comparison conditions
- Reported accurately
- Statistical tests applied

### Step 5: Review Negative Results

Ensure:
- All experiments reported
- Negative results not hidden
- Failure analysis included

### Step 6: Apply Statistical Criteria

Work through statistical evaluation criteria systematically.

### Step 7: Complete 7-Stage Review

Document findings for each stage.

## Output

```markdown
# Results Audit Report

## Summary
- **Overall Assessment**: PASS / REVISE_NEEDED / MAJOR_REVISION
- **Traceability Score**: X/10
- **Statistical Validity**: X/10
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

## Traceability Check

| Result | Run ID | Config | Checkpoint | Logs |
|--------|--------|--------|------------|------|
| [Result 1] | Yes/No | Yes/No | Yes/No | Yes/No |

**Untraceable Results**:
- [Result without proper documentation]

## Statistical Validity

### Sample Size and Power

| Metric | Adequate? | Notes |
|--------|-----------|-------|
| Power analysis | Yes/No/N/A | |
| Sample size | Yes/No | |
| Multiple runs | Yes/No/N/A | |

### Test Selection

| Analysis | Test Used | Appropriate? | Assumptions Met? |
|----------|-----------|--------------|------------------|
| [Analysis 1] | [Test] | Yes/No | Yes/No |

### Multiple Comparisons

| Analysis | Tests Run | Correction Applied? | Method |
|----------|-----------|---------------------|--------|
| [Analysis 1] | X | Yes/No | [Method] |

### Effect Size Reporting

| Result | Effect Size | CI | P-value | Interpretation |
|--------|-------------|-----|---------|----------------|
| [Result 1] | [Value] | [CI] | [p] | [Small/Medium/Large] |

**Statistical Issues**:
- [Issue]

## Baseline Comparisons

| Baseline | Implementation | Fair? | Reported Accurately? | Statistical Test |
|----------|----------------|-------|---------------------|-------------------|
| [Baseline 1] | Verified/Unverified | Yes/No | Yes/No | [Test] |

**Baseline Concerns**:
- [Concern]

## Negative Results Review

| Experiment | Reported? | Analysis? | Status |
|------------|-----------|-----------|--------|
| [Exp 1] | Yes/No | Yes/No | [Status] |

**Unreported Experiments**:
- [Experiment not in report]

## Reproducibility Check

### Code and Data

| Item | Documented | Verified | Location |
|------|------------|----------|----------|
| Code repo | Yes/No | Yes/No | |
| Code version | Yes/No | Yes/No | |
| Data location | Yes/No | Yes/No | |
| Seeds | Yes/No | Yes/No | |
| Hyperparameters | Yes/No | Yes/No | |
| Environment | Yes/No | Yes/No | |

### Reproducibility Score Breakdown

| Category | Score | Weight |
|----------|-------|--------|
| Code availability | X/10 | 30% |
| Data availability | X/10 | 30% |
| Hyperparameters | X/10 | 20% |
| Seeds | X/10 | 10% |
| Environment | X/10 | 10% |
| **Total** | X/10 | 100% |

## Claims Verification

| Claim | Supported By | Verified? | Notes |
|-------|--------------|-----------|-------|
| [Claim 1] | [Result ref] | Yes/No | |

**Unsupported Claims**:
- [Claim without support]

## Reporting Standards Compliance

| Standard | Applicable | Compliance | Missing Items |
|----------|-----------|------------|---------------|
| CONSORT | Yes/No | X% | [List] |
| STROBE | Yes/No | X% | [List] |
| ARRIVE | Yes/No | X% | [List] |

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
- 7-stage review is mandatory
- Statistical tests must be appropriate
- Multiple comparisons must be corrected
- Effect sizes and CIs required for all comparisons
- Reproducibility score must be >= 7/10 to pass