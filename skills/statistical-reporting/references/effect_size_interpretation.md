# Effect Size Interpretation Guide

## Overview

This document provides comprehensive guidelines for interpreting effect sizes across different statistical tests. Effect sizes quantify the magnitude of effects independent of sample size, allowing for meaningful comparisons across studies.

## Why Effect Sizes Matter

1. **Independence from sample size**: p-values conflate effect size and sample size
2. **Practical significance**: Indicate whether effects are meaningful in real-world terms
3. **Meta-analysis**: Enable combining results across studies
4. **Power analysis**: Required for sample size calculations
5. **Comparability**: Allow comparison of effects across different measures

## Standardized Mean Differences

### Cohen's d

**Definition**: Difference between two means divided by pooled standard deviation.

**Formula**:
```
d = (M1 - M2) / SDpooled

where SDpooled = sqrt(((n1-1)*SD1² + (n2-1)*SD2²) / (n1+n2-2))
```

**Interpretation Guidelines**:

| d | Interpretation | Percentile Standing | Overlap | Variance Explained (r²) |
|---|---------------|---------------------|---------|------------------------|
| 0.0 | No effect | 50th = 50th | 100% | 0% |
| 0.1 | Negligible | 54th = 50th | 96% | 0.2% |
| 0.2 | Small | 58th = 50th | 85% | 1% |
| 0.3 | Small-Medium | 62nd = 50th | 79% | 2% |
| 0.5 | Medium | 69th = 50th | 67% | 6% |
| 0.7 | Medium-Large | 76th = 50th | 56% | 11% |
| 0.8 | Large | 79th = 50th | 53% | 14% |
| 1.0 | Very Large | 84th = 50th | 45% | 20% |
| 1.2 | Very Large | 88th = 50th | 38% | 26% |
| 1.5 | Huge | 93rd = 50th | 29% | 36% |
| 2.0 | Huge | 98th = 50th | 19% | 50% |

**Context-Specific Benchmarks**:

| Field | Small | Medium | Large |
|-------|-------|--------|-------|
| Psychology (general) | 0.20 | 0.50 | 0.80 |
| Education | 0.25 | 0.50 | 0.75 |
| Medical/Health | 0.20 | 0.50 | 0.80 |
| Social sciences | 0.20 | 0.50 | 0.80 |
| Neuroscience | 0.20 | 0.50 | 0.80 |

### Hedges' g

**Definition**: Bias-corrected version of Cohen's d for small samples.

**Formula**:
```
g = d × correction factor
correction = 1 - (3 / (4×(n1+n2) - 9))
```

**When to Use**: Small samples (n < 50 total)

**Interpretation**: Same as Cohen's d

### Glass's Delta

**Definition**: Uses control group SD only.

**Formula**:
```
delta = (Mtreatment - Mcontrol) / SDcontrol
```

**When to Use**: When treatment might affect variability

## Correlation Coefficients

### Pearson's r

**Definition**: Linear association between two continuous variables.

**Interpretation Guidelines**:

| r | r² | Interpretation | Variance Explained |
|---|----|--------------|--------------------|
| .00 | .00 | No correlation | 0% |
| .10 | .01 | Small | 1% |
| .20 | .04 | Small | 4% |
| .30 | .09 | Medium | 9% |
| .40 | .16 | Medium | 16% |
| .50 | .25 | Large | 25% |
| .60 | .36 | Large | 36% |
| .70 | .49 | Very Large | 49% |
| .80 | .64 | Very Large | 64% |
| .90 | .81 | Nearly Perfect | 81% |
| 1.00 | 1.00 | Perfect | 100% |

**Field-Specific Benchmarks**:

| Field | Small | Medium | Large |
|-------|-------|--------|-------|
| Psychology | .10 | .30 | .50 |
| Education | .10 | .30 | .50 |
| Medical research | .10 | .30 | .50 |
| Personality research | .10 | .20 | .30 |
| Social psychology | .10 | .24 | .37 |
| Cognitive psychology | .17 | .34 | .51 |

### Spearman's rho

**Definition**: Rank-based correlation for monotonic relationships.

**Interpretation**: Similar to Pearson's r

**When to Use**: Ordinal data, non-linear monotonic relationships, presence of outliers

### Kendall's tau

**Definition**: Another rank-based correlation, more robust.

**Interpretation**:

| tau | Interpretation |
|-----|---------------|
| < .10 | Negligible |
| .10 - .19 | Weak |
| .20 - .29 | Moderate |
| .30+ | Strong |

**When to Use**: Small samples, many tied ranks

## Variance Explained Measures

### Eta-Squared (eta²)

**Definition**: Proportion of total variance explained by an effect.

**Formula**:
```
eta² = SS_effect / SS_total
```

**Interpretation**:

| eta² | Interpretation |
|------|---------------|
| .01 | Small |
| .06 | Medium |
| .14 | Large |

### Partial Eta-Squared (partial eta²)

**Definition**: Proportion of variance explained by an effect, partialling out other effects.

**Formula**:
```
partial eta² = SS_effect / (SS_effect + SS_error)
```

**Interpretation**: Same as eta²

**When to Use**: Factorial designs, ANOVA with multiple factors

### Omega-Squared (omega²)

**Definition**: Unbiased estimate of variance explained.

**Formula**:
```
omega² = (SS_effect - df_effect × MS_error) / (SS_total + MS_error)
```

**Interpretation**: Same as eta², but less biased for small samples

**When to Use**: Small samples, reporting population effect

### Cohen's f

**Definition**: Effect size for ANOVA.

**Formula**:
```
f = sqrt(eta² / (1 - eta²))
```

**Interpretation**:

| f | eta² | Interpretation |
|---|------|---------------|
| 0.10 | .01 | Small |
| 0.25 | .06 | Medium |
| 0.40 | .14 | Large |

## Odds Ratios and Risk Ratios

### Odds Ratio (OR)

**Definition**: Ratio of odds of an event in two groups.

**Interpretation**:

| OR | Interpretation |
|----|---------------|
| 1.0 | No effect |
| 1.5 | Small |
| 2.0 | Small-Medium |
| 2.5 | Medium |
| 3.0 | Medium |
| 4.0 | Medium-Large |
| 5.0+ | Large |

**Clinical Context**:

| OR | Clinical Significance |
|----|----------------------|
| 1.0 - 1.5 | Likely not clinically meaningful |
| 1.5 - 3.0 | Moderate clinical significance |
| 3.0+ | Strong clinical significance |

**Note**: For rare events, OR approximates Risk Ratio

### Risk Ratio (Relative Risk, RR)

**Definition**: Ratio of probabilities of an event in two groups.

**Interpretation**:

| RR | Interpretation |
|----|---------------|
| 1.0 | No effect |
| 1.5 | Small increase in risk |
| 2.0 | Moderate increase in risk |
| 3.0+ | Substantial increase in risk |
| 0.67 | Small protective effect |
| 0.50 | Moderate protective effect |
| 0.33 | Strong protective effect |

### Risk Difference (Absolute Risk Reduction)

**Definition**: Difference in event rates between groups.

**Interpretation**:
- 0% = No effect
- Small effects: < 5%
- Moderate effects: 5-10%
- Large effects: > 10%

**Number Needed to Treat (NNT)**:
```
NNT = 1 / Risk Difference
```

## Regression Effect Sizes

### R² (Coefficient of Determination)

**Definition**: Proportion of variance explained by regression model.

**Interpretation**:

| R² | Interpretation |
|----|---------------|
| .02 | Small (2% variance explained) |
| .13 | Medium (13% variance explained) |
| .26 | Large (26% variance explained) |

### Cohen's f²

**Definition**: Effect size for R².

**Formula**:
```
f² = R² / (1 - R²)
```

**Interpretation**:

| f² | R² | Interpretation |
|----|----| --------------|
| 0.02 | .02 | Small |
| 0.15 | .13 | Medium |
| 0.35 | .26 | Large |

### Semi-Partial (Part) Correlation

**Definition**: Unique variance explained by a predictor.

**Interpretation**: Same as Pearson's r

### Standardized Regression Coefficients (Beta)

**Definition**: Change in SD units of Y per SD change in X.

**Interpretation**: Similar to Cohen's d for continuous predictors

## Confidence Intervals for Effect Sizes

### Why Report Confidence Intervals

1. Indicate precision of effect size estimate
2. Enable meta-analysis
3. Show range of plausible values
4. Support null hypothesis significance testing

### Common Methods

| Effect Size | Method |
|-------------|--------|
| Cohen's d | Noncentral t-distribution |
| Pearson's r | Fisher's z-transformation |
| Odds Ratio | Woolf (log) method |
| R² | Bootstrap or F-distribution |

### Interpretation of CIs

- **Wide CI**: Imprecise estimate, may need larger sample
- **CI excludes null value**: Significant effect (at corresponding alpha)
- **CI includes null value**: Non-significant, but examine CI bounds for practical significance

## Converting Between Effect Sizes

### d to r

```
r = d / sqrt(d² + 4)
```

### r to d

```
d = 2r / sqrt(1 - r²)
```

### OR to d

```
d = ln(OR) × (sqrt(3) / pi) ≈ ln(OR) / 1.81
```

### d to OR

```
OR = exp(d × pi / sqrt(3)) ≈ exp(d × 1.81)
```

### f to eta²

```
eta² = f² / (1 + f²)
```

### eta² to f

```
f = sqrt(eta² / (1 - eta²))
```

## Effect Size Reporting Checklist

- [ ] Report appropriate effect size for each statistical test
- [ ] Include confidence interval for effect size
- [ ] Interpret effect size magnitude using established benchmarks
- [ ] Consider field-specific benchmarks
- [ ] Discuss practical significance, not just statistical significance
- [ ] Report consistent effect size measures across analyses
- [ ] Consider meta-analytic context when relevant

## Effect Size Calculator Reference

### Python

```python
import numpy as np
from scipy import stats

# Cohen's d
def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_sd = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_sd

# CI for Cohen's d
def ci_cohens_d(d, n1, n2, confidence=0.95):
    se = np.sqrt((n1+n2)/(n1*n2) + d**2/(2*(n1+n2)))
    z = stats.norm.ppf((1 + confidence) / 2)
    return (d - z*se, d + z*se)

# CI for Pearson's r
def ci_pearson_r(r, n, confidence=0.95):
    z = np.arctanh(r)  # Fisher's z
    se = 1 / np.sqrt(n - 3)
    z_crit = stats.norm.ppf((1 + confidence) / 2)
    z_low, z_high = z - z_crit*se, z + z_crit*se
    return np.tanh(z_low), np.tanh(z_high)

# Eta-squared from ANOVA
def eta_squared(ss_effect, ss_total):
    return ss_effect / ss_total

# Partial eta-squared
def partial_eta_squared(ss_effect, ss_error):
    return ss_effect / (ss_effect + ss_error)

# Cohen's f from eta-squared
def cohens_f(eta_squared):
    return np.sqrt(eta_squared / (1 - eta_squared))
```

### R

```r
# Using the effsize package
library(effsize)

# Cohen's d with CI
cohen.d(group1, group2, conf.level = 0.95)

# Using the effectsize package
library(effectsize)

# Standardized differences
cohens_d(group1, group2)
hedges_g(group1, group2)

# Variance explained
eta_squared(model)
omega_squared(model)

# Correlation CI
cor.test(x, y, conf.level = 0.95)
```

## Common Mistakes to Avoid

1. **Using p-values as effect sizes**: p-values depend on sample size
2. **Reporting only statistical significance**: Always report effect sizes
3. **Ignoring confidence intervals**: CIs show precision of estimates
4. **Misapplying Cohen's benchmarks**: Consider field-specific context
5. **Comparing effect sizes across different measures**: Use standardized measures
6. **Reporting unstandardized effects only**: Standardized effects enable comparison
7. **Forgetting to interpret magnitude**: Effect sizes need interpretation