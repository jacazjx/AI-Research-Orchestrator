# Statistical Pitfalls

This document catalogs common statistical errors and how to identify them.

## Sample Size Issues

### Inadequate Sample Size

**Problem**: Sample too small to detect meaningful effects or draw reliable conclusions.

**Detection Signs**:
- No power analysis reported
- Wide confidence intervals
- Non-significant results with large effect sizes
- Single-digit sample sizes without justification

**Consequences**:
- False negatives (Type II errors)
- Unstable estimates
- Poor generalizability
- Wasted resources

**Remedies**:
- Conduct a priori power analysis
- Report achieved power for non-significant results
- Use appropriate effect size estimates
- Consider Bayesian approaches for small samples

### Overpowered Studies

**Problem**: Sample so large that trivial effects become statistically significant.

**Detection Signs**:
- Very large sample sizes
- Significant p-values with tiny effect sizes
- Focus on p-values rather than practical significance
- Effect sizes not reported or discussed

**Consequences**:
- Statistically significant but practically meaningless results
- Resource waste
- Over-interpretation of trivial findings

**Remedies**:
- Focus on effect sizes and confidence intervals
- Define minimum clinically important difference
- Consider practical vs. statistical significance
- Use equivalence testing when appropriate

### Power Analysis Requirements

| Analysis Type | Required Inputs |
|---------------|-----------------|
| t-test | Effect size (d), alpha, power |
| ANOVA | Effect size (f), groups, alpha, power |
| Correlation | Expected r, alpha, power |
| Regression | Effect size (f²), predictors, alpha, power |
| Chi-square | Effect size (w), df, alpha, power |

## Multiple Comparisons

### The Multiple Testing Problem

**Problem**: With multiple tests, probability of at least one false positive increases.

**Family-wise Error Rate**:

```
FWER = 1 - (1 - alpha)^k
```

Where k = number of tests and alpha = significance level.

**Example**: With 20 tests at alpha = 0.05:
- FWER = 1 - (0.95)^20 = 0.64
- 64% chance of at least one false positive

### Detection Signs

- Many statistical tests conducted
- No correction for multiple comparisons
- "Significant" results highlighted without correction
- Subgroup analyses reported without adjustment
- Multiple outcome measures treated as primary

### Correction Methods

| Method | Description | When to Use |
|--------|-------------|-------------|
| Bonferroni | alpha/k for each test | Conservative, few tests |
| Holm-Bonferroni | Sequential Bonferroni | More powerful than Bonferroni |
| Benjamini-Hochberg | Controls false discovery rate | Many tests, exploratory |
| Tukey HSD | All pairwise comparisons | ANOVA post-hoc |
| Dunnett | Comparisons to control | Multiple treatments vs. control |

### Choosing a Method

| Scenario | Recommended Method |
|----------|-------------------|
| Few pre-specified comparisons | Bonferroni or Holm |
| Many pre-specified comparisons | Holm or FDR |
| Exploratory analyses | FDR (Benjamini-Hochberg) |
| All pairwise comparisons | Tukey HSD |
| Tests vs. control | Dunnett |

## P-Value Misinterpretation

### Common Misinterpretations

| Misinterpretation | Correct Interpretation |
|-------------------|------------------------|
| "p < 0.05 means the probability the null hypothesis is true is < 5%" | p-value is the probability of data (or more extreme) given the null hypothesis, not vice versa |
| "p > 0.05 means no effect" | Failure to reject null does not prove null |
| "p < 0.05 means a large/important effect" | Statistical significance does not imply practical significance |
| "p-values can be compared across studies" | p-values depend on sample size, effect size, and study design |
| "1 - p is the probability of replication" | Replication probability is much lower |

### Detection Signs of Misuse

- p-values reported without effect sizes
- Focus on significance thresholds rather than precision
- "Marginal significance" for p > 0.05
- Selective reporting of significant p-values only
- Binary thinking (significant vs. not significant)

### Better Practices

- Report effect sizes with confidence intervals
- Consider p-values as continuous measures of evidence
- Pre-specify alpha levels
- Report exact p-values
- Interpret p-values in context of effect size and sample size

## Effect Size Issues

### Failure to Report Effect Sizes

**Problem**: p-values alone do not indicate the magnitude of effects.

**Required Effect Sizes**:

| Test | Effect Size Measure | Interpretation |
|------|---------------------|----------------|
| t-test | Cohen's d | Small = 0.2, Medium = 0.5, Large = 0.8 |
| ANOVA | eta-squared, partial eta-squared | Proportion of variance explained |
| Correlation | r | Small = 0.1, Medium = 0.3, Large = 0.5 |
| Regression | R², f² | Variance explained |
| Chi-square | Cramer's V, odds ratio | Association strength |

### Detection Signs

- Only p-values reported
- No effect sizes in tables or text
- Claims of "significant" effects without magnitude
- Comparison of significance without comparing effect sizes

### Effect Size Interpretation

| Cohen's d | Interpretation | % Overlap |
|-----------|----------------|-----------|
| 0.2 | Small | 85% |
| 0.5 | Medium | 67% |
| 0.8 | Large | 53% |
| 1.2 | Very Large | 38% |

## Confidence Interval Misinterpretation

### Common Misinterpretations

| Misinterpretation | Correct Interpretation |
|-------------------|------------------------|
| "95% CI contains 95% of the data" | 95% of CIs from repeated sampling would contain the true parameter |
| "95% CI means 95% probability parameter is in interval" | CI is about procedure, not parameter (frequentist view) |
| "Wide CI means high variability" | Wide CI can result from small sample, high variability, or both |

### Detection Signs

- CIs not reported
- CIs interpreted incorrectly
- Focus on whether CI excludes zero only
- No discussion of precision

### Best Practices

- Always report CIs with effect sizes
- Interpret width as precision of estimate
- Use CIs for inference, not just significance
- Consider compatibility intervals (modern terminology)

## Assumption Violations

### Common Statistical Assumptions

| Test | Key Assumptions |
|------|-----------------|
| t-test | Normality, homogeneity of variance, independence |
| ANOVA | Normality, homogeneity of variance, independence |
| Linear regression | Linearity, normality of residuals, homoscedasticity, independence |
| Chi-square | Expected cell counts > 5, independence |
| Non-parametric | Independence |

### Detection Signs of Violations

- No assumption checks reported
- Small sample with parametric tests
- Unequal variances with standard tests
- Skewed data with t-tests/ANOVA
- Ordered categories treated as continuous

### Handling Violations

| Violation | Solution |
|-----------|----------|
| Non-normality | Transform data, use non-parametric tests, bootstrapping |
| Heterogeneity of variance | Welch's t-test, Welch's ANOVA, robust methods |
| Non-independence | Mixed models, GEE, clustered standard errors |
| Non-linearity | Polynomial terms, splines, non-linear models |

## Model Specification Issues

### Overfitting

**Problem**: Model fits noise in data, not just signal.

**Detection Signs**:
- Many predictors relative to sample size
- Perfect or near-perfect classification
- In-sample performance much better than out-of-sample
- Complex models without cross-validation

**Rule of Thumb**: At least 10-20 observations per predictor variable.

### Underfitting

**Problem**: Important variables omitted from model.

**Detection Signs**:
- Known predictors not included
- Poor model fit statistics
- Residual patterns
- Low R² without explanation

### Omitted Variable Bias

**Problem**: Excluding important confounders biases estimates.

**Detection Signs**:
- Known confounders not measured
- Coefficients change when variables added
- Large difference between adjusted and unadjusted estimates

## Missing Data Issues

### Types of Missing Data

| Type | Description | Implication |
|------|-------------|-------------|
| MCAR (Missing Completely at Random) | Missing unrelated to any variables | Unbiased, reduced power |
| MAR (Missing at Random) | Missing related to observed variables | Can be addressed with methods |
| MNAR (Missing Not at Random) | Missing related to unobserved values | Difficult to address |

### Inappropriate Handling

| Method | Problem |
|--------|---------|
| Complete case analysis | Biased if not MCAR, loses power |
| Last observation carried forward | Assumes no change, creates bias |
| Mean imputation | Underestimates variance, biases relationships |
| Single imputation | Underestimates uncertainty |

### Appropriate Methods

| Method | When to Use |
|--------|-------------|
| Multiple imputation | MAR, most situations |
| Maximum likelihood | MAR, model-based |
| Inverse probability weighting | MAR, selection model |
| Sensitivity analysis | MNAR suspected |

## Statistical Reporting Checklist

### Essential Elements

- [ ] Sample size justification (power analysis)
- [ ] Effect sizes with confidence intervals
- [ ] Exact p-values (not just < 0.05)
- [ ] Assumption checks reported
- [ ] Correction for multiple comparisons
- [ ] Handling of missing data described
- [ ] Model specification justified
- [ ] All analyses reported, not just significant ones
- [ ] Pre-registration or analysis plan referenced

### Warning Signs

- [WARNING] Only significant results reported
- [WARNING] No effect sizes with p-values
- [WARNING] Many tests without correction
- [WARNING] Assumptions not checked
- [WARNING] Sample size not justified
- [WARNING] Results seem "too good"
- [WARNING] Complex analyses without explanation