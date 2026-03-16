# Meta-Analysis Methods

## Overview

Meta-analysis is a statistical technique for combining results from multiple studies to derive more precise and reliable conclusions. It is essential for evidence synthesis in AI/ML research where many similar experiments are conducted.

## When to Use Meta-Analysis

### Appropriate Scenarios

| Scenario | Example |
|----------|---------|
| Multiple RCTs on same intervention | Comparing training methods across papers |
| Similar outcome measures | Accuracy improvements across datasets |
| Need for precision | Estimating true effect size |
| Inconsistent results | Resolving conflicting findings |
| Subgroup analysis | Effect modifiers identification |

### Prerequisites

- [ ] At least 2-3 studies addressing the same question
- [ ] Similar enough to combine (conceptual homogeneity)
- [ ] Comparable outcome measures
- [ ] Sufficient reported statistics
- [ ] Access to necessary data (means, SDs, sample sizes)

## Effect Size Calculation

### Common Effect Size Measures

#### Standardized Mean Difference (Cohen's d)

For comparing means between two groups:

$$
d = \frac{\bar{X}_1 - \bar{X}_2}{s_{pooled}}
$$

Where:
$$
s_{pooled} = \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2}}
$$

**Interpretation:**
| d value | Interpretation |
|---------|----------------|
| 0.2 | Small effect |
| 0.5 | Medium effect |
| 0.8 | Large effect |

#### Hedges' g (Bias-corrected)

For small sample sizes:

$$
g = d \times \left(1 - \frac{3}{4(n_1 + n_2) - 9}\right)
$$

#### Odds Ratio

For binary outcomes:

$$
OR = \frac{a/c}{b/d} = \frac{ad}{bc}
$$

**Log transformation for meta-analysis:**
$$
\ln(OR) \pm SE
$$

#### Correlation Coefficient (r)

For relationship studies:

$$
r = \frac{t}{\sqrt{t^2 + df}}
$$

### Effect Size Extraction from Different Statistics

| Reported Statistic | Conversion Formula |
|-------------------|-------------------|
| t-statistic | $d = \frac{2t}{\sqrt{df}}$ |
| F-statistic (1 df) | $d = \sqrt{\frac{F(n_1+n_2)}{n_1 n_2}}$ |
| $\chi^2$ (1 df) | $d = \sqrt{\frac{\chi^2}{N}}$ |
| p-value only | Use conservative estimates or contact authors |

## Fixed-Effect vs Random-Effects Models

### Fixed-Effect Model

**Assumption:** All studies share a single true effect size.

$$
\hat{\theta}_{FE} = \frac{\sum w_i \hat{\theta}_i}{\sum w_i}
$$

Where $w_i = 1/v_i$ (inverse variance weight).

**When to use:**
- Studies are functionally identical
- Same population, intervention, outcome
- Interest is in this specific set of studies

### Random-Effects Model

**Assumption:** True effect sizes vary across studies.

$$
\hat{\theta}_{RE} = \frac{\sum w_i^* \hat{\theta}_i}{\sum w_i^*}
$$

Where $w_i^* = 1/(v_i + \tau^2)$ and $\tau^2$ is between-study variance.

**When to use:**
- Studies differ in populations/methods
- Generalizing beyond these specific studies
- Heterogeneity is expected

### Model Selection Decision Tree

```
                    ┌─────────────────┐
                    │ Are studies     │
                    │ identical?      │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
       ┌────────────┐               ┌────────────┐
       │    YES     │               │     NO     │
       └─────┬──────┘               └─────┬──────┘
             │                             │
             ▼                             ▼
      Fixed-Effect                 ┌─────────────┐
                                   │ Is there    │
                                   │ significant │
                                   │ heterogeneity?│
                                   └──────┬──────┘
                                          │
                           ┌──────────────┴──────────────┐
                           │                             │
                           ▼                             ▼
                    Random-Effects              Fixed-Effect
                    (recommended)               (if I² < 25%)
```

## Heterogeneity Assessment

### Q-Statistic

$$
Q = \sum w_i (\hat{\theta}_i - \hat{\theta}_{FE})^2
$$

- Under null (homogeneity): $Q \sim \chi^2_{k-1}$
- Significant Q indicates heterogeneity

### I² Statistic

Percentage of total variation due to heterogeneity:

$$
I^2 = \frac{Q - df}{Q} \times 100\%
$$

**Interpretation:**
| I² Value | Interpretation |
|----------|----------------|
| 0-25% | Low heterogeneity |
| 25-50% | Moderate heterogeneity |
| 50-75% | Substantial heterogeneity |
| 75-100% | Considerable heterogeneity |

### Prediction Interval

The range where 95% of true effect sizes lie:

$$
\hat{\theta} \pm t_{df, 0.975} \times \sqrt{\tau^2 + v_{\hat{\theta}}}
$$

## Publication Bias Assessment

### Funnel Plot

Visual assessment of asymmetry:

```
         Effect Size
    ←─────────────────────→
           │
           │      *
           │    *   *
      SE   │   *     *
           │  *   *   *
           │ *    *    *
           │*  *  *  *  *
           └─────────────
```

**Interpretation:**
- Symmetric: No publication bias
- Asymmetric: Possible publication bias (missing small studies)

### Statistical Tests

#### Egger's Test

Regression-based test for funnel plot asymmetry:

$$
\frac{\hat{\theta}_i}{SE_i} = \alpha + \beta \times \frac{1}{SE_i} + \epsilon_i
$$

- Significant β indicates asymmetry

#### Begg's Rank Correlation

Kendall's tau between effect size and variance:

- Significant correlation indicates bias

### Trim and Fill Method

1. Estimate number of missing studies
2. "Trim" extreme studies
3. "Fill" missing studies symmetrically
4. Recalculate effect size

## Meta-Analysis for AI/ML Research

### Common Applications

| Research Question | Effect Size | Example |
|-------------------|-------------|---------|
| Method comparison | d, OR | Novel optimizer vs SGD |
| Architecture impact | d | Transformer vs RNN accuracy |
| Hyperparameter effect | r | Learning rate vs convergence |
| Dataset effect | d | Performance across datasets |

### ML-Specific Considerations

#### Cross-Dataset Synthesis

```python
# Pseudocode for ML meta-analysis
studies = [
    {"dataset": "ImageNet", "method": "Ours", "acc": 0.85, "std": 0.02, "n": 50000},
    {"dataset": "CIFAR-100", "method": "Ours", "acc": 0.78, "std": 0.03, "n": 10000},
    {"dataset": "ImageNet", "method": "Baseline", "acc": 0.82, "std": 0.02, "n": 50000},
    # ...
]

# Calculate effect sizes per dataset
# Apply random-effects model
# Report pooled improvement with CI
```

#### Handling Multiple Comparisons

When papers report many metrics:
1. Pre-specify primary outcomes
2. Apply Bonferroni or FDR correction
3. Report all analyses transparently

#### Reproducibility Standards

- [ ] Report inclusion/exclusion criteria
- [ ] List all studies considered
- [ ] Provide extracted data table
- [ ] Share analysis code
- [ ] Register protocol (PROSPERO for health, OSF for ML)

## Reporting Standards (PRISMA)

### Flow Diagram Elements

```
Identification → Screening → Eligibility → Included

Records identified (n)
    ↓
Duplicates removed (n)
    ↓
Records screened (n)
    ↓
Records excluded (n)
    ↓
Full-text assessed (n)
    ↓
Full-text excluded (n)
    ↓
Studies included (n)
```

### Required Elements in Meta-Analysis Report

1. **Background**
   - Rationale for synthesis
   - Objective and hypotheses

2. **Methods**
   - Eligibility criteria
   - Information sources
   - Search strategy
   - Study selection process
   - Data extraction methods
   - Effect size calculations
   - Statistical model choice
   - Heterogeneity assessment
   - Publication bias assessment

3. **Results**
   - Study selection flow
   - Study characteristics table
   - Risk of bias assessment
   - Forest plot
   - Heterogeneity statistics
   - Publication bias assessment
   - Sensitivity analyses

4. **Discussion**
   - Summary of findings
   - Limitations
   - Conclusions

## Forest Plot Interpretation

```
Study           Effect Size    Weight
─────────────────────────────────────
Study A    ───────●───────        25%
Study B    ────●──────────        15%
Study C    ─────────●─────        30%
Study D    ─────●─────────        20%
Study E    ───────●───────        10%
─────────────────────────────────────
Overall    ◆                      100%
           │←─────── CI ───────→│
         -1.0   0   +1.0
```

**Elements:**
- Squares: Individual study effects (size = weight)
- Horizontal lines: Confidence intervals
- Diamond: Pooled effect (width = CI)
- Vertical line: Null effect (d = 0, OR = 1)

## Sensitivity Analyses

### Leave-One-Out Analysis

Remove each study sequentially:
- Checks if results driven by single study
- Reports range of pooled effects

### Subgroup Analysis

```markdown
| Subgroup | k | Effect | 95% CI | I² |
|----------|---|--------|--------|-----|
| CNN      | 5 | 0.45   | [0.32, 0.58] | 30% |
| RNN      | 3 | 0.62   | [0.41, 0.83] | 45% |
| Transformer | 4 | 0.78 | [0.55, 1.01] | 25% |
```

### Meta-Regression

For continuous moderators:

$$
\hat{\theta}_i = \beta_0 + \beta_1 X_{1i} + \beta_2 X_{2i} + \epsilon_i
$$

Examples:
- Year of publication → Time trend
- Sample size → Power effect
- Model parameters → Complexity effect

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Garbage in, garbage out | Assess study quality first |
| Inappropriate combination | Check conceptual homogeneity |
| Ignoring heterogeneity | Report and explain I² |
| Overinterpreting small samples | Use caution with few studies |
| Ignoring dependencies | Use multilevel models for clustered data |
| Selective outcome reporting | Contact authors, use imputation |

## References

- Borenstein, M., et al. (2009). Introduction to Meta-Analysis
- Higgins, J. P. T., et al. (2019). Cochrane Handbook
- PRISMA Statement: www.prisma-statement.org