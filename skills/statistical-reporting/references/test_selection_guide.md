# Statistical Test Selection Guide

## Overview

This document provides comprehensive decision trees for selecting the appropriate statistical test based on research question, data type, and study design.

## Decision Framework

### Step 1: Identify Your Research Question Type

| Question Type | Description | Example |
|---------------|-------------|---------|
| **Difference** | Are groups different? | "Do treatment and control groups differ in outcome?" |
| **Association** | Are variables related? | "Is there a relationship between age and performance?" |
| **Prediction** | Can we predict an outcome? | "Can we predict success from multiple predictors?" |
| **Comparison to Standard** | Does data differ from a known value? | "Is our sample mean different from population mean?" |

### Step 2: Identify Your Variable Types

| Variable Type | Description | Examples |
|---------------|-------------|----------|
| **Continuous** | Interval/ratio scale, theoretically infinite values | Height, weight, time, temperature |
| **Ordinal** | Ordered categories | Likert scale, rankings, grade levels |
| **Nominal** | Unordered categories | Gender, treatment group, yes/no |
| **Count** | Non-negative integers | Number of events, frequency |

### Step 3: Determine Study Design

| Design | Description | Statistical Implication |
|--------|-------------|------------------------|
| **Between-subjects** | Different participants in each group | Independent tests |
| **Within-subjects** | Same participants in all conditions | Paired/repeated measures tests |
| **Mixed** | Combination of between and within | Mixed-design ANOVA |

## Decision Trees

### Decision Tree 1: Comparing Groups (Difference Questions)

```
START: Do you want to compare groups?
│
├─ YES
│   │
│   ├── How many groups?
│   │   │
│   │   ├── 2 groups
│   │   │   │
│   │   │   ├── What type of data?
│   │   │   │   │
│   │   │   │   ├── Continuous
│   │   │   │   │   │
│   │   │   │   │   ├── Study design?
│   │   │   │   │   │   ├── Between-subjects
│   │   │   │   │   │   │   ├── Normality OK?
│   │   │   │   │   │   │   │   ├── YES → Independent t-test
│   │   │   │   │   │   │   │   └── NO → Mann-Whitney U
│   │   │   │   │   │   │
│   │   │   │   │   │   └── Within-subjects
│   │   │   │   │   │       ├── Normality OK?
│   │   │   │   │   │       │   ├── YES → Paired t-test
│   │   │   │   │   │       │   └── NO → Wilcoxon signed-rank
│   │   │   │   │   │
│   │   │   │   ├── Ordinal
│   │   │   │   │   ├── Between-subjects → Mann-Whitney U
│   │   │   │   │   └── Within-subjects → Wilcoxon signed-rank
│   │   │   │   │
│   │   │   │   └── Nominal (binary/dichotomous)
│   │   │   │       ├── Between-subjects → Chi-square test
│   │   │   │       └── Within-subjects → McNemar's test
│   │   │   │
│   │   ├── 3+ groups
│   │   │   │
│   │   │   ├── What type of data?
│   │   │   │   │
│   │   │   │   ├── Continuous
│   │   │   │   │   │
│   │   │   │   │   ├── Study design?
│   │   │   │   │   │   ├── Between-subjects
│   │   │   │   │   │   │   ├── One factor? → One-way ANOVA
│   │   │   │   │   │   │   └── Two factors? → Factorial ANOVA
│   │   │   │   │   │   │
│   │   │   │   │   │   └── Within-subjects
│   │   │   │   │   │       ├── One factor? → Repeated measures ANOVA
│   │   │   │   │   │       └── Two factors? → Two-way repeated measures ANOVA
│   │   │   │   │   │
│   │   │   │   ├── Non-normality present?
│   │   │   │   │   ├── Between-subjects → Kruskal-Wallis
│   │   │   │   │   └── Within-subjects → Friedman test
│   │   │   │   │
│   │   │   │   └── Nominal
│   │   │   │       └── Chi-square test of independence
│   │   │   │
│   │   └── More complex designs
│   │       ├── Mixed (between + within) → Mixed ANOVA
│   │       ├── Covariate present? → ANCOVA
│   │       └── Hierarchical/nested → Linear mixed models
│
└─ NO → See other decision trees
```

### Decision Tree 2: Examining Relationships (Association Questions)

```
START: Do you want to examine relationships between variables?
│
├─ YES
│   │
│   ├── How many variables?
│   │   │
│   │   ├── 2 variables
│   │   │   │
│   │   │   ├── What types?
│   │   │   │   │
│   │   │   │   ├── Both Continuous
│   │   │   │   │   ├── Linear relationship?
│   │   │   │   │   │   ├── YES, normal → Pearson correlation
│   │   │   │   │   │   ├── NO (monotonic) → Spearman correlation
│   │   │   │   │   │   └── NO (non-monotonic) → Consider regression
│   │   │   │   │   │
│   │   │   │   ├── Both Ordinal
│   │   │   │   │   └── Spearman correlation / Kendall's tau
│   │   │   │   │
│   │   │   │   ├── One Continuous, One Categorical
│   │   │   │   │   └── Point-biserial correlation (if binary) / Eta (if nominal)
│   │   │   │   │
│   │   │   │   └── Both Categorical
│   │   │   │       ├── 2x2 table → Chi-square test / Fisher's exact
│   │   │   │       └── Larger tables → Chi-square test
│   │   │   │
│   │   ├── Multiple variables
│   │   │   │
│   │   │   ├── Predicting a continuous outcome?
│   │   │   │   ├── Simple (1 predictor) → Simple linear regression
│   │   │   │   ├── Multiple predictors → Multiple linear regression
│   │   │   │   ├── Hierarchical structure → Mixed-effects model
│   │   │   │   └── Non-linear relationship → Polynomial/non-linear regression
│   │   │   │
│   │   │   ├── Predicting a categorical outcome?
│   │   │   │   ├── Binary outcome → Logistic regression
│   │   │   │   ├── 3+ unordered categories → Multinomial logistic regression
│   │   │   │   └── 3+ ordered categories → Ordinal logistic regression
│   │   │   │
│   │   │   └── Predicting a count outcome?
│   │   │       ├── Poisson regression
│   │   │       └── If overdispersion → Negative binomial regression
│   │   │
│   │   └── Many variables (exploratory)
│   │       ├── Reduce dimensions → Factor analysis / PCA
│   │       ├── Cluster observations → Cluster analysis
│   │       └── Identify groups → Discriminant analysis
│
└─ NO → See other decision trees
```

### Decision Tree 3: Comparing to a Standard

```
START: Do you want to compare your data to a known value or distribution?
│
├─ YES
│   │
│   ├── What type of comparison?
│   │   │
│   │   ├── Compare mean to a known value
│   │   │   ├── One sample t-test (if normality holds)
│   │   │   └── Wilcoxon signed-rank test (if non-normal)
│   │   │
│   │   ├── Compare proportion to a known value
│   │   │   └── One-sample z-test for proportions / Binomial test
│   │   │
│   │   ├── Compare variance to a known value
│   │   │   └── Chi-square test for variance
│   │   │
│   │   ├── Compare distribution to a known distribution
│   │   │   ├── Kolmogorov-Smirnov test
│   │   │   └── Anderson-Darling test (more sensitive to tails)
│   │   │
│   │   └── Compare to multiple standards
│   │       └── goodness-of-fit chi-square
│
└─ NO → Revisit Decision Tree 1 or 2
```

## Test Summary Tables

### Parametric vs Non-Parametric Equivalents

| Research Design | Parametric Test | Non-Parametric Alternative |
|-----------------|-----------------|---------------------------|
| Two independent groups | Independent t-test | Mann-Whitney U test |
| Two paired groups | Paired t-test | Wilcoxon signed-rank test |
| 3+ independent groups | One-way ANOVA | Kruskal-Wallis test |
| 3+ paired groups | Repeated measures ANOVA | Friedman test |
| Correlation | Pearson r | Spearman rho / Kendall tau |
| Compare to value | One-sample t-test | Wilcoxon signed-rank |

### ANOVA Family Decision Table

| Factors | Between/Within | Covariates | Recommended Test |
|---------|---------------|------------|------------------|
| 1 | Between | No | One-way ANOVA |
| 1 | Between | Yes | One-way ANCOVA |
| 2+ | Between | No | Factorial ANOVA |
| 2+ | Between | Yes | Factorial ANCOVA |
| 1 | Within | No | Repeated measures ANOVA |
| 2+ | Within | No | Repeated measures ANOVA |
| Mixed | Mixed | No | Mixed ANOVA |
| Mixed | Mixed | Yes | Mixed ANCOVA |
| Hierarchical | Any | Any | Linear mixed model |

### Regression Family Decision Table

| Outcome Type | Predictors | Special Conditions | Recommended Model |
|--------------|------------|-------------------|-------------------|
| Continuous | 1 | Linear relationship | Simple linear regression |
| Continuous | 2+ | Linear, independent errors | Multiple linear regression |
| Continuous | 2+ | Correlated errors | Mixed-effects regression |
| Binary | 1+ | - | Logistic regression |
| Ordinal | 1+ | - | Ordinal logistic regression |
| Nominal (3+) | 1+ | Unordered | Multinomial logistic regression |
| Count | 1+ | Poisson distribution | Poisson regression |
| Count | 1+ | Overdispersion | Negative binomial regression |
| Time-to-event | 1+ | Censored data | Cox proportional hazards |

## Assumption Requirements by Test

### t-Tests

| Test | Normality | Homogeneity of Variance | Independence |
|------|-----------|------------------------|--------------|
| Independent t-test | Groups approximately normal | Levene's p > .05 | Groups independent |
| Paired t-test | Differences approximately normal | N/A | Pairs matched |
| Welch's t-test | Groups approximately normal | Not required | Groups independent |

### ANOVA Tests

| Test | Normality | Homogeneity | Independence | Sphericity |
|------|-----------|-------------|--------------|------------|
| One-way ANOVA | Residuals normal | Levene's p > .05 | Groups independent | N/A |
| Factorial ANOVA | Residuals normal | Levene's p > .05 | Groups independent | N/A |
| Repeated measures ANOVA | Residuals normal | N/A | Within-subjects | Mauchly's p > .05 |
| Mixed ANOVA | Residuals normal | Between-subjects homogeneity | Mixed | Mauchly's p > .05 |

### Non-Parametric Tests

| Test | Required Assumptions |
|------|---------------------|
| Mann-Whitney U | Independent groups, similar distributions |
| Wilcoxon signed-rank | Paired observations, symmetric differences |
| Kruskal-Wallis | Independent groups, similar distributions |
| Friedman | Related samples, similar distributions |
| Chi-square | Expected frequencies >= 5, independence |

## Sample Size Considerations

### Minimum Sample Size Guidelines

| Test | Minimum per Group | Recommended |
|------|------------------|-------------|
| t-test | 15-20 | 30+ |
| ANOVA | 15-20 | 30+ |
| Correlation | 25 | 50+ |
| Simple regression | 10 per predictor | 20+ per predictor |
| Multiple regression | 10-20 per predictor | 30+ per predictor |
| Chi-square | Expected count >= 5 | 20+ total |

### Power Analysis Quick Reference

| Test | Small Effect | Medium Effect | Large Effect |
|------|-------------|---------------|--------------|
| t-test (d) | d = 0.2 | d = 0.5 | d = 0.8 |
| ANOVA (f) | f = 0.1 | f = 0.25 | f = 0.4 |
| Correlation (r) | r = 0.1 | r = 0.3 | r = 0.5 |
| Regression (f²) | f² = 0.02 | f² = 0.15 | f² = 0.35 |

**Sample sizes needed for 80% power at alpha = .05:**

| Test | Small Effect | Medium Effect | Large Effect |
|------|-------------|---------------|--------------|
| t-test (2 groups) | 394 per group | 64 per group | 26 per group |
| One-way ANOVA (3 groups) | 322 total | 159 total | 66 total |
| Correlation | 783 total | 85 total | 28 total |

## Special Situations

### Small Samples (n < 30)

- Prefer exact tests (e.g., exact Wilcoxon)
- Use bootstrap methods for confidence intervals
- Consider Bayesian approaches
- Report effect sizes with caution

### Large Samples (n > 500)

- Very small effects become significant
- Focus on effect sizes and practical significance
- Use effect size confidence intervals
- Consider equivalence testing

### Violated Assumptions

| Violation | Solution |
|-----------|----------|
| Non-normality | Use non-parametric test; transform data; use bootstrap |
| Heterogeneity | Use Welch's correction; robust methods |
| Non-sphericity | Use Greenhouse-Geisser or Huynh-Feldt correction |
| Small expected frequencies | Use Fisher's exact test; combine categories |

### Missing Data

| Pattern | Recommendation |
|---------|---------------|
| MCAR (Missing Completely at Random) | Complete case analysis acceptable |
| MAR (Missing at Random) | Multiple imputation |
| MNAR (Missing Not at Random) | Sensitivity analysis; pattern-mixture models |

## Decision Checklist

Before selecting a test, confirm:

- [ ] Research question clearly stated
- [ ] Variable types identified (continuous, ordinal, nominal)
- [ ] Study design identified (between, within, mixed)
- [ ] Number of groups/factors determined
- [ ] Sample size appropriate for planned analysis
- [ ] Distribution properties assessed (normality)
- [ ] Variance properties assessed (homogeneity)
- [ ] Any special conditions (paired data, repeated measures)

## Quick Reference Card

```
QUESTION: What statistical test should I use?

1. What is your outcome variable?
   ├── Continuous → Go to 2
   ├── Ordinal → Go to 3
   └── Categorical → Go to 4

2. Continuous outcome:
   ├── Comparing groups?
   │   ├── 2 groups → t-test (or Mann-Whitney if non-normal)
   │   └── 3+ groups → ANOVA (or Kruskal-Wallis if non-normal)
   └── Examining relationships?
       ├── 1 predictor → Linear regression
       └── Multiple predictors → Multiple regression

3. Ordinal outcome:
   ├── Comparing groups?
   │   ├── 2 groups → Mann-Whitney U
   │   └── 3+ groups → Kruskal-Wallis
   └── Examining relationships?
       └── Spearman correlation / Ordinal regression

4. Categorical outcome:
   ├── Binary outcome → Logistic regression
   ├── Comparing proportions → Chi-square test
   └── Multiple categories → Multinomial logistic regression
```