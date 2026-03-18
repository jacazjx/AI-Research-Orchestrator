---
name: airesearchorchestrator:statistical-reporting
description: Statistical analysis guidance including test selection, assumption checking, effect sizes, power analysis, and APA reporting. Use when user says "statistical analysis", "power analysis", "effect size", "统计分析", or needs help with statistical reporting.
argument-hint: [data-description-or-analysis-goal]
allowed-tools: Bash(python, R), Read, Write, Edit, Grep, Glob
---

# Statistical Reporting

## Overview

Provide comprehensive statistical analysis guidance for research experiments, including test selection, assumption checking, effect size calculation, power analysis, and APA 7th edition reporting. This skill ensures rigorous statistical practices during the experiments phase.

## Purpose

Support researchers in making sound statistical decisions, avoiding common pitfalls, and producing reproducible, well-reported statistical analyses that meet publication standards.

## Workflow

### Step 1: Understand the Research Question

Identify the statistical analysis context:

- **Research question type**: Comparison, association, prediction, or difference
- **Variable types**: Continuous, categorical, ordinal, or count
- **Study design**: Between-subjects, within-subjects, or mixed
- **Sample characteristics**: Independent groups, paired data, or clusters

### Step 2: Select Appropriate Statistical Test

Use the test selection decision tree to identify the correct test.

Read [references/test_selection_guide.md](references/test_selection_guide.md) for detailed decision flowcharts.

#### Quick Reference by Research Question

| Question Type | Data Type | Groups | Recommended Test |
|---------------|-----------|--------|------------------|
| Compare means | Continuous | 2 independent | Independent t-test |
| Compare means | Continuous | 2 paired | Paired t-test |
| Compare means | Continuous | 3+ independent | One-way ANOVA |
| Compare means | Continuous | 3+ paired | Repeated measures ANOVA |
| Compare distributions | Ordinal/ranked | 2 independent | Mann-Whitney U |
| Compare distributions | Ordinal/ranked | 2 paired | Wilcoxon signed-rank |
| Compare distributions | Ordinal/ranked | 3+ independent | Kruskal-Wallis |
| Compare distributions | Ordinal/ranked | 3+ paired | Friedman test |
| Association | Continuous | 2 variables | Pearson correlation |
| Association | Ordinal/ranked | 2 variables | Spearman correlation |
| Association | Categorical | 2 variables | Chi-square test |
| Association | Binary outcome | Multiple predictors | Logistic regression |
| Prediction | Continuous | Multiple predictors | Linear regression |

### Step 3: Check Statistical Assumptions

Verify that the data meet the assumptions for the selected test.

#### Common Assumptions

| Test | Normality | Homogeneity of Variance | Independence | Other |
|------|-----------|------------------------|--------------|-------|
| Independent t-test | Required | Required (equal variance) | Required | - |
| Paired t-test | Required (differences) | N/A | Paired structure | - |
| ANOVA | Required | Required | Required | - |
| Mann-Whitney U | Not required | Not required | Required | Similar shapes |
| Pearson r | Required (both variables) | N/A | Required | Linearity |
| Chi-square | Not required | Not required | Required | Expected counts >= 5 |
| Linear regression | Required (residuals) | Homoscedasticity | Required | Linearity, no multicollinearity |

#### Normality Testing

```python
# Python: Test for normality
from scipy import stats
import numpy as np

# Shapiro-Wilk test (recommended for n < 50)
stat, p_value = stats.shapiro(data)
print(f"Shapiro-Wilk: W = {stat:.4f}, p = {p_value:.4f}")

# D'Agostino-Pearson test (recommended for n >= 20)
stat, p_value = stats.normaltest(data)
print(f"D'Agostino-Pearson: K2 = {stat:.4f}, p = {p_value:.4f}")

# Kolmogorov-Smirnov test (large samples)
stat, p_value = stats.kstest(data, 'norm', args=(np.mean(data), np.std(data)))
print(f"Kolmogorov-Smirnov: D = {stat:.4f}, p = {p_value:.4f}")
```

```r
# R: Test for normality
# Shapiro-Wilk test
shapiro.test(data)

# Visual inspection
par(mfrow = c(1, 2))
hist(data, main = "Histogram", xlab = "Values")
qqnorm(data)
qqline(data)
```

#### Homogeneity of Variance Testing

```python
# Python: Test for equal variances
from scipy import stats

# Levene's test (robust to non-normality)
stat, p_value = stats.levene(group1, group2, group3)
print(f"Levene's test: W = {stat:.4f}, p = {p_value:.4f}")

# Bartlett's test (sensitive to non-normality)
stat, p_value = stats.bartlett(group1, group2, group3)
print(f"Bartlett's test: T = {stat:.4f}, p = {p_value:.4f}")
```

```r
# R: Test for equal variances
# Levene's test (from car package)
library(car)
leveneTest(values ~ group, data = df)

# Bartlett's test
bartlett.test(values ~ group, data = df)
```

#### Handling Assumption Violations

| Violation | Solution |
|-----------|----------|
| Non-normality (mild) | Proceed with parametric test; robust to mild violations |
| Non-normality (severe) | Use non-parametric alternative; transform data |
| Heterogeneity of variance | Use Welch's t-test/ANOVA; robust standard errors |
| Non-independence | Use mixed-effects models; clustered standard errors |
| Outliers | Investigate; consider robust methods or removal with justification |

### Step 4: Calculate Effect Sizes

Effect sizes quantify the magnitude of effects, independent of sample size.

Read [references/effect_size_interpretation.md](references/effect_size_interpretation.md) for interpretation guidelines.

#### Standardized Mean Differences

```python
# Python: Cohen's d and Hedges' g
import numpy as np

def cohens_d(group1, group2):
    """Calculate Cohen's d for two independent groups."""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)

    # Pooled standard deviation
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))

    d = (np.mean(group1) - np.mean(group2)) / pooled_std
    return d

def hedges_g(group1, group2):
    """Calculate Hedges' g (bias-corrected Cohen's d)."""
    d = cohens_d(group1, group2)
    n1, n2 = len(group1), len(group2)

    # Correction factor
    correction = 1 - (3 / (4 * (n1 + n2) - 9))

    return d * correction
```

```r
# R: Effect sizes using effsize package
library(effsize)

# Cohen's d
cohen.d(group1, group2)

# Hedges' g
cohen.d(group1, group2, hedge = TRUE)
```

#### Correlation Coefficients

```python
# Python: Correlation coefficients
from scipy import stats

# Pearson's r
r, p = stats.pearsonr(x, y)

# Spearman's rho
rho, p = stats.spearmanr(x, y)

# Kendall's tau
tau, p = stats.kendalltau(x, y)
```

```r
# R: Correlation coefficients
# Pearson's r
cor.test(x, y, method = "pearson")

# Spearman's rho
cor.test(x, y, method = "spearman")

# Kendall's tau
cor.test(x, y, method = "kendall")
```

#### Variance Explained

```python
# Python: Eta-squared and partial eta-squared
def eta_squared(ss_effect, ss_total):
    """Calculate eta-squared."""
    return ss_effect / ss_total

def partial_eta_squared(ss_effect, ss_error):
    """Calculate partial eta-squared."""
    return ss_effect / (ss_effect + ss_error)

# For ANOVA results
import statsmodels.api as sm
from statsmodels.formula.api import ols

model = ols('dv ~ factor', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)

# Extract SS for calculations
ss_factor = anova_table.loc['factor', 'sum_sq']
ss_residual = anova_table.loc['Residual', 'sum_sq']

eta2 = eta_squared(ss_factor, ss_factor + ss_residual)
partial_eta2 = partial_eta_squared(ss_factor, ss_residual)
```

```r
# R: Eta-squared using effectsize package
library(effectsize)

# From ANOVA model
model <- aov(dv ~ factor, data = df)
eta_squared(model)
partial_eta_squared(model)
```

#### Odds Ratios

```python
# Python: Odds ratio from 2x2 table
import numpy as np

def odds_ratio(table):
    """
    Calculate odds ratio from 2x2 contingency table.
    table = [[a, b], [c, d]]
    """
    a, b = table[0]
    c, d = table[1]

    # Add 0.5 to all cells if any cell is zero (Haldane-Anscombe correction)
    if min(a, b, c, d) == 0:
        a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5

    or_val = (a * d) / (b * c)

    # Confidence interval (Woolf method)
    se = np.sqrt(1/a + 1/b + 1/c + 1/d)
    ci_low = np.exp(np.log(or_val) - 1.96 * se)
    ci_high = np.exp(np.log(or_val) + 1.96 * se)

    return or_val, ci_low, ci_high
```

```r
# R: Odds ratio
# Using epitools package
library(epitools)
oddsratio(table)

# Using vcd package
library(vcd)
oddsratio(table, log = FALSE)
```

### Step 5: Conduct Power Analysis

Determine appropriate sample sizes or evaluate achieved power.

#### A Priori Power Analysis

Calculate required sample size before data collection.

```python
# Python: Power analysis using statsmodels
from statsmodels.stats.power import TTestPower, TTestIndPower, FTestAnovaPower

# Independent t-test
power_analysis = TTestIndPower()
sample_size = power_analysis.solve_power(
    effect_size=0.5,  # Cohen's d (medium)
    power=0.80,       # Desired power
    alpha=0.05,       # Significance level
    ratio=1.0         # n2/n1 ratio
)
print(f"Required sample size per group: {np.ceil(sample_size)}")

# One-way ANOVA
anova_power = FTestAnovaPower()
sample_size = anova_power.solve_power(
    effect_size=0.25,  # f (medium)
    power=0.80,
    alpha=0.05,
    k_groups=3
)
print(f"Required total sample size: {np.ceil(sample_size)}")
```

```r
# R: Power analysis using pwr package
library(pwr)

# Independent t-test
pwr.t.test(
    d = 0.5,      # Cohen's d
    power = 0.80,
    sig.level = 0.05,
    type = "two.sample"
)

# One-way ANOVA
pwr.anova.test(
    k = 3,        # Number of groups
    f = 0.25,     # Effect size f
    power = 0.80,
    sig.level = 0.05
)

# Correlation
pwr.r.test(
    r = 0.30,     # Expected correlation
    power = 0.80,
    sig.level = 0.05
)
```

#### Post Hoc Power Analysis

Calculate achieved power given sample size and observed effect.

```python
# Python: Post hoc power
from statsmodels.stats.power import TTestIndPower

power_analysis = TTestIndPower()
achieved_power = power_analysis.solve_power(
    effect_size=0.4,  # Observed Cohen's d
    nobs1=50,         # Sample size per group
    alpha=0.05,
    ratio=1.0
)
print(f"Achieved power: {achieved_power:.3f}")
```

```r
# R: Post hoc power
library(pwr)

pwr.t.test(
    d = 0.4,
    n = 50,
    sig.level = 0.05,
    type = "two.sample"
)
```

#### Sensitivity Analysis

Determine minimum detectable effect size.

```python
# Python: Sensitivity analysis
from statsmodels.stats.power import TTestIndPower

power_analysis = TTestIndPower()
min_effect = power_analysis.solve_power(
    power=0.80,
    nobs1=100,
    alpha=0.05,
    ratio=1.0
)
print(f"Minimum detectable effect size (d): {min_effect:.3f}")
```

```r
# R: Sensitivity analysis
library(pwr)

pwr.t.test(
    n = 100,
    power = 0.80,
    sig.level = 0.05,
    type = "two.sample"
)
```

#### Power Analysis Parameters by Test

| Test | Effect Size | Python | R |
|------|-------------|--------|---|
| t-test | Cohen's d | TTestIndPower | pwr.t.test |
| ANOVA | Cohen's f | FTestAnovaPower | pwr.anova.test |
| Correlation | r | - | pwr.r.test |
| Chi-square | w | GofChisquarePower | pwr.chisq.test |
| Regression | f2 | - | pwr.f2.test |

### Step 6: Report Results in APA Format

Follow APA 7th edition guidelines for reporting statistical results.

Read [references/apa_reporting_templates.md](references/apa_reporting_templates.md) for complete templates.

#### Key Reporting Elements

1. **Descriptive statistics**: Mean, SD (or median, IQR for non-normal data)
2. **Test statistic**: t, F, chi-square, etc.
3. **Degrees of freedom**
4. **p-value**: Exact value, or p < .001 for very small values
5. **Effect size**: With confidence interval when possible
6. **Direction of effect**: Which group was higher/lower

#### APA Format Rules

- Italicize test statistics (t, F, chi-square, r, etc.)
- Use exact p-values to two or three decimal places (p = .043)
- Report p < .001 for values below .001
- Do NOT report p = .000
- Include effect sizes with confidence intervals
- Use metric units for descriptive statistics
- Space around operators (M = 10.5, SD = 2.3)

#### Example Reports

**Independent t-test:**
> An independent-samples t-test revealed a significant difference in scores between the experimental group (M = 85.3, SD = 12.4) and the control group (M = 72.1, SD = 15.8), t(58) = 3.72, p < .001, d = 0.95, 95% CI [0.42, 1.48].

**One-way ANOVA:**
> A one-way ANOVA showed a significant effect of treatment condition on performance, F(2, 57) = 8.34, p = .001, partial eta-squared = .23, 90% CI [.07, .36]. Post hoc comparisons using Tukey's HSD indicated that the high-dose group (M = 92.1, SD = 8.3) scored significantly higher than the control group (M = 74.5, SD = 11.2), p < .001.

**Correlation:**
> Pearson correlation analysis revealed a strong positive relationship between study time and exam scores, r(98) = .72, p < .001, 95% CI [.61, .80].

## Multiple Comparisons Correction

When conducting multiple statistical tests, apply appropriate corrections.

### Correction Methods

| Method | Description | When to Use |
|--------|-------------|-------------|
| Bonferroni | alpha / number of tests | Conservative, few tests |
| Holm-Bonferroni | Sequential Bonferroni | More powerful than Bonferroni |
| Benjamini-Hochberg | Controls false discovery rate | Many tests, exploratory |
| Tukey HSD | All pairwise comparisons | ANOVA post-hoc |
| Dunnett | Comparisons to control | Multiple treatments vs. control |

```python
# Python: Multiple comparison corrections
from statsmodels.stats.multitest import multipletests

p_values = [0.01, 0.03, 0.04, 0.12, 0.23, 0.04]

# Bonferroni correction
reject, p_corrected, _, _ = multipletests(p_values, method='bonferroni')

# Benjamini-Hochberg (FDR)
reject, p_corrected, _, _ = multipletests(p_values, method='fdr_bh')

# Holm-Bonferroni
reject, p_corrected, _, _ = multipletests(p_values, method='holm')
```

```r
# R: Multiple comparison corrections
p_values <- c(0.01, 0.03, 0.04, 0.12, 0.23, 0.04)

# Bonferroni correction
p.adjust(p_values, method = "bonferroni")

# Benjamini-Hochberg (FDR)
p.adjust(p_values, method = "BH")

# Holm-Bonferroni
p.adjust(p_values, method = "holm")
```

## Common Statistical Errors to Avoid

1. **p-hacking**: Running multiple analyses and reporting only significant results
2. **HARKing**: Hypothesizing After Results are Known
3. **Ignoring assumptions**: Not checking test assumptions
4. **Over-reliance on p-values**: Not reporting effect sizes
5. **Multiple comparisons**: Not correcting for multiple tests
6. **Small sample sizes**: Insufficient power to detect effects
7. **Data dredging**: Exploratory analyses presented as confirmatory

## Output

Generate a Statistical Analysis Report:

```markdown
# Statistical Analysis Report

## Research Question
[State the research question and hypotheses]

## Data Description
- **Sample Size**: N = [n]
- **Variables**: [List IV(s) and DV(s)]
- **Data Type**: [Continuous/Categorical/Ordinal]
- **Missing Data**: [Amount and handling method]

## Test Selection
- **Selected Test**: [Test name]
- **Justification**: [Why this test is appropriate]

## Assumption Checks

| Assumption | Test | Result | Status |
|------------|------|--------|--------|
| Normality | Shapiro-Wilk | W = X.XX, p = .XX | Met/Violated |
| Homogeneity | Levene's | F = X.XX, p = .XX | Met/Violated |

## Results

### Descriptive Statistics

| Group | n | M | SD | 95% CI |
|-------|---|---|----|----|
| Group 1 | XX | XX.XX | X.XX | [XX.XX, XX.XX] |
| Group 2 | XX | XX.XX | X.XX | [XX.XX, XX.XX] |

### Inferential Statistics

[Test statistic], [df], p = [value], [effect size] = [value], 95% CI [lower, upper].

### Effect Size Interpretation
[Interpret the effect size magnitude]

## Power Analysis

- **Achieved Power**: XX% (post hoc)
- **Minimum Detectable Effect**: d = X.XX (sensitivity)

## APA-Formatted Report

[Complete APA-style paragraph reporting the results]

## Interpretation

[What do these results mean in context of the research question?]

## Limitations

[List any limitations of the statistical analysis]
```

## Key Rules

1. **Always check assumptions** before running parametric tests
2. **Report effect sizes** alongside p-values
3. **Use confidence intervals** to convey precision
4. **Correct for multiple comparisons** when appropriate
5. **Follow APA format** for reporting
6. **Interpret practical significance** not just statistical significance
7. **Document all decisions** about test selection and assumptions
8. **Consider power** when interpreting non-significant results
9. **Be transparent** about exploratory vs. confirmatory analyses
10. **Use appropriate visualizations** to support statistical findings

## References

- [Test Selection Guide](references/test_selection_guide.md) - Detailed decision trees for test selection
- [Effect Size Interpretation](references/effect_size_interpretation.md) - Interpretation tables and guidelines
- [APA Reporting Templates](references/apa_reporting_templates.md) - Complete APA format templates by test type