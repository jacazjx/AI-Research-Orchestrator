# APA Statistical Reporting Templates

## Overview

This document provides templates for reporting statistical results in APA 7th edition format. Each template includes the required elements and example paragraphs.

## General APA Reporting Guidelines

### Essential Elements

1. **Descriptive statistics** (M, SD, n)
2. **Test statistic** (t, F, chi-square, etc.)
3. **Degrees of freedom**
4. **p-value** (exact to 2-3 decimals, or p < .001)
5. **Effect size** with confidence interval
6. **Direction of effect**

### Formatting Rules

- Italicize test statistics: *t*, *F*, *chi-square*, *r*, etc.
- Space around equals signs: *t*(58) = 3.72, not *t*(58)=3.72
- Use exact p-values: p = .043, not p < .05
- For p < .001, report as p < .001, not p = .000
- Use Greek letters for population parameters (beta, eta)
- Report percentages to one decimal place (45.3%)
- Report confidence intervals: 95% CI [lower, upper]
- Use brackets for confidence intervals, parentheses for degrees of freedom

### Number Formatting

| Statistic | Format | Example |
|-----------|--------|---------|
| Means | 1 decimal | 45.3 |
| Standard deviations | 1 decimal | 3.2 |
| Test statistics | 2 decimals | *t* = 3.72 |
| p-values | 2-3 decimals | p = .043 or p < .001 |
| Effect sizes | 2 decimals | d = 0.45 |
| Percentages | 1 decimal | 45.3% |

## t-Test Templates

### Independent Samples t-Test

**Template**:
> An independent-samples *t*-test was conducted to compare [DV] between [Group 1] and [Group 2]. There was a [significant/non-significant] difference in scores for [Group 1] (M = XX.X, SD = X.X) and [Group 2] (M = XX.X, SD = X.X); *t*(df) = X.XX, p = .XXX, d = X.XX, 95% CI [X.XX, X.XX].

**Example**:
> An independent-samples *t*-test was conducted to compare test scores between students who received the new teaching method and those who received the traditional method. There was a significant difference in scores for the new method group (M = 85.3, SD = 12.4) and the traditional method group (M = 72.1, SD = 15.8); *t*(58) = 3.72, p < .001, d = 0.95, 95% CI [0.42, 1.48]. The results indicate that students in the new method group scored significantly higher than those in the traditional method group.

**With Welch's Correction** (when homogeneity of variance violated):
> An independent-samples *t*-test with Welch's correction revealed a significant difference in scores for the experimental group (M = 85.3, SD = 12.4) and the control group (M = 72.1, SD = 15.8); *t*(54.3) = 3.72, p < .001, d = 0.95, 95% CI [0.42, 1.48].

### Paired Samples t-Test

**Template**:
> A paired-samples *t*-test was conducted to compare [DV] at [Time 1] and [Time 2]. There was a [significant/non-significant] difference between [Time 1] (M = XX.X, SD = X.X) and [Time 2] (M = XX.X, SD = X.X); *t*(df) = X.XX, p = .XXX, d = X.XX, 95% CI [X.XX, X.XX].

**Example**:
> A paired-samples *t*-test was conducted to compare anxiety scores before and after the intervention. There was a significant difference between pre-intervention scores (M = 42.5, SD = 8.3) and post-intervention scores (M = 35.2, SD = 7.1); *t*(29) = 5.67, p < .001, d = 1.04, 95% CI [0.60, 1.47]. Participants showed significantly lower anxiety after the intervention.

### One-Sample t-Test

**Template**:
> A one-sample *t*-test was conducted to compare [DV] to the population mean of [X.X]. The sample mean (M = XX.X, SD = X.X) was [significantly/not significantly] different from the population mean; *t*(df) = X.XX, p = .XXX, d = X.XX, 95% CI [X.XX, X.XX].

**Example**:
> A one-sample *t*-test was conducted to compare the sample's reading scores to the national average of 100. The sample mean (M = 108.5, SD = 12.3) was significantly higher than the national average; *t*(49) = 4.88, p < .001, d = 0.69, 95% CI [0.36, 1.02].

## ANOVA Templates

### One-Way ANOVA

**Template**:
> A one-way ANOVA was conducted to compare the effect of [IV] on [DV]. There was a [significant/non-significant] effect of [IV] on [DV] at the p < .05 level for the [k] conditions: *F*(df_between, df_within) = X.XX, p = .XXX, partial eta-squared = .XX.

**Example with Post Hoc**:
> A one-way ANOVA was conducted to compare the effect of teaching method on test scores. There was a significant effect of teaching method on test scores at the p < .05 level for the three conditions: *F*(2, 57) = 8.34, p = .001, partial eta-squared = .23, 90% CI [.07, .36]. Post hoc comparisons using Tukey's HSD indicated that the mean score for the interactive method (M = 92.1, SD = 8.3) was significantly higher than the lecture method (M = 74.5, SD = 11.2), p < .001. However, the discussion method (M = 88.3, SD = 9.1) did not significantly differ from either the interactive method (p = .23) or the lecture method (p = .07).

**Non-Significant Example**:
> A one-way ANOVA was conducted to compare the effect of treatment group on symptom severity. There was not a significant effect of treatment group at the p < .05 level for the three conditions: *F*(2, 42) = 1.23, p = .301, partial eta-squared = .06.

### Factorial ANOVA

**Template**:
> A [2 x 3] factorial ANOVA was conducted to examine the effects of [IV1] and [IV2] on [DV]. There was a [significant/non-significant] main effect of [IV1], *F*(df) = X.XX, p = .XXX, partial eta-squared = .XX. There was [also/not] a significant main effect of [IV2], *F*(df) = X.XX, p = .XXX, partial eta-squared = .XX. The interaction between [IV1] and [IV2] was [significant/non-significant], *F*(df) = X.XX, p = .XXX, partial eta-squared = .XX.

**Example**:
> A 2 (gender: male, female) x 3 (condition: control, low-intensity, high-intensity) factorial ANOVA was conducted to examine the effects on performance scores. There was a significant main effect of condition, *F*(2, 54) = 12.45, p < .001, partial eta-squared = .32. There was not a significant main effect of gender, *F*(1, 54) = 2.31, p = .134, partial eta-squared = .04. The gender x condition interaction was significant, *F*(2, 54) = 4.56, p = .015, partial eta-squared = .14, indicating that the effect of condition on performance differed by gender.

### Repeated Measures ANOVA

**Template**:
> A repeated measures ANOVA was conducted to compare [DV] across [k] time points. Mauchly's test indicated that the assumption of sphericity had been [met/violated], chi-square = X.XX, p = .XXX. [If violated: Degrees of freedom were corrected using Greenhouse-Geisser estimates of sphericity (epsilon = .XX).] There was a [significant/non-significant] effect of time, *F*(df) = X.XX, p = .XXX, partial eta-squared = .XX.

**Example**:
> A repeated measures ANOVA was conducted to compare reaction times across four testing sessions. Mauchly's test indicated that the assumption of sphericity had been violated, chi-square(5) = 18.34, p = .003. Degrees of freedom were corrected using Greenhouse-Geisser estimates of sphericity (epsilon = .72). There was a significant effect of testing session on reaction time, *F*(2.15, 47.23) = 15.67, p < .001, partial eta-squared = .42.

### Mixed ANOVA

**Example**:
> A mixed ANOVA was conducted with time (pre, post) as the within-subjects factor and group (treatment, control) as the between-subjects factor. There was a significant main effect of time, *F*(1, 38) = 24.56, p < .001, partial eta-squared = .39, indicating that scores changed from pre-test to post-test. There was not a significant main effect of group, *F*(1, 38) = 1.23, p = .275, partial eta-squared = .03. Importantly, there was a significant time x group interaction, *F*(1, 38) = 8.92, p = .005, partial eta-squared = .19. Simple effects analysis revealed that the treatment group showed significant improvement from pre (M = 45.2, SD = 8.1) to post (M = 58.3, SD = 7.4), *F*(1, 38) = 31.45, p < .001, whereas the control group did not show significant change.

## Non-Parametric Tests

### Mann-Whitney U Test

**Template**:
> A Mann-Whitney U test was conducted to compare [DV] between [Group 1] and [Group 2]. The results indicated a [significant/non-significant] difference between groups, U = XXX, p = .XXX, r = X.XX. [Group 1] had [higher/lower] ranks (Mdn = XX.X) than [Group 2] (Mdn = XX.X).

**Example**:
> A Mann-Whitney U test was conducted to compare satisfaction ratings between the two service conditions because the data violated the normality assumption. The results indicated a significant difference between groups, U = 234.5, p = .002, r = 0.42. The enhanced service group had higher satisfaction ratings (Mdn = 8.0, IQR = 2.0) than the standard service group (Mdn = 6.0, IQR = 3.0).

### Wilcoxon Signed-Rank Test

**Template**:
> A Wilcoxon signed-rank test was conducted to compare [DV] between [Time 1] and [Time 2]. The results indicated a [significant/non-significant] difference, T = XXX, p = .XXX, r = X.XX.

**Example**:
> A Wilcoxon signed-rank test was conducted to compare anxiety scores before and after the intervention. The results indicated a significant reduction in anxiety from pre-intervention (Mdn = 42.0, IQR = 12.0) to post-intervention (Mdn = 35.0, IQR = 10.0), T = 145.5, p < .001, r = 0.56.

### Kruskal-Wallis Test

**Template**:
> A Kruskal-Wallis test was conducted to compare [DV] across [k] groups. The results indicated a [significant/non-significant] difference, H(df) = X.XX, p = .XXX, eta-squared = .XX. Pairwise comparisons [using Dunn's test with Bonferroni correction] revealed that [specific comparisons].

**Example**:
> A Kruskal-Wallis test was conducted to compare pain scores across three treatment groups. The results indicated a significant difference, H(2) = 12.45, p = .002, eta-squared = .18. Pairwise comparisons using Dunn's test with Bonferroni correction revealed that the high-dose group (Mdn = 3.0) had significantly lower pain scores than the placebo group (Mdn = 6.0), p = .002, but the low-dose group (Mdn = 5.0) did not significantly differ from either group.

### Friedman Test

**Template**:
> A Friedman test was conducted to compare [DV] across [k] conditions. The results indicated a [significant/non-significant] difference, chi-square(df) = X.XX, p = .XXX, W = X.XX.

**Example**:
> A Friedman test was conducted to compare preference ratings across three different product designs. The results indicated a significant difference in preferences, chi-square(2) = 18.67, p < .001, Kendall's W = 0.42. Post hoc pairwise comparisons with Bonferroni correction indicated that Design A was preferred over Design C (p = .003), but there were no significant differences between Design A and B or Design B and C.

## Chi-Square Templates

### Chi-Square Test of Independence

**Template**:
> A chi-square test of independence was conducted to examine the relation between [Variable 1] and [Variable 2]. The relation between these variables was [significant/non-significant], chi-square(df, N = XXX) = X.XX, p = .XXX, Cramer's V = .XX.

**Example**:
> A chi-square test of independence was conducted to examine the relation between treatment group and recovery status. The relation between these variables was significant, chi-square(1, N = 120) = 8.45, p = .004, Cramer's V = 0.27. Patients in the treatment group were more likely to recover (70%) compared to those in the control group (45%).

**Expected Frequencies Note**:
> Note. Expected frequencies in all cells were greater than 5, satisfying the assumptions of the chi-square test.

**Fisher's Exact Test** (when expected frequencies < 5):
> A Fisher's exact test was conducted because expected frequencies in some cells were less than 5. The relation between [Variable 1] and [Variable 2] was [significant/non-significant], p = .XXX, odds ratio = X.XX, 95% CI [X.XX, X.XX].

### Chi-Square Goodness of Fit

**Template**:
> A chi-square goodness-of-fit test was conducted to determine whether the observed frequencies of [Variable] differed from expected frequencies. The observed frequencies [did/did not] differ significantly from expected, chi-square(df, N = XXX) = X.XX, p = .XXX.

**Example**:
> A chi-square goodness-of-fit test was conducted to determine whether preferences for the four product colors differed from equal distribution. The observed frequencies differed significantly from expected, chi-square(3, N = 200) = 15.80, p = .001. Blue was preferred more frequently (35%) than expected (25%), while yellow was preferred less frequently (12%) than expected (25%).

## Correlation Templates

### Pearson Correlation

**Template**:
> A Pearson correlation coefficient was computed to assess the linear relationship between [Variable 1] and [Variable 2]. There was a [positive/negative] [small/medium/large] correlation between the two variables, r(df) = .XX, p = .XXX, 95% CI [.XX, .XX].

**Example**:
> A Pearson correlation coefficient was computed to assess the linear relationship between study hours and exam scores. There was a positive, large correlation between the two variables, r(98) = .72, p < .001, 95% CI [.61, .80], indicating that more study hours were associated with higher exam scores.

**Non-Significant Example**:
> A Pearson correlation coefficient was computed to assess the linear relationship between age and job satisfaction. There was not a significant correlation between the two variables, r(78) = .08, p = .493, 95% CI [-.14, .29].

### Spearman Correlation

**Template**:
> A Spearman rank-order correlation was conducted to assess the relationship between [Variable 1] and [Variable 2]. There was a [positive/negative] [weak/moderate/strong] correlation, rs = .XX, p = .XXX.

**Example**:
> A Spearman rank-order correlation was conducted to assess the relationship between years of experience and performance ranking because the performance data were ordinal. There was a positive, moderate correlation, rs = .45, p < .001, indicating that more experienced employees tended to have higher performance rankings.

### Partial Correlation

**Template**:
> A partial correlation was conducted to assess the relationship between [Variable 1] and [Variable 2] while controlling for [Control Variable]. After controlling for [Control Variable], there was a [significant/non-significant] [positive/negative] correlation, r(df) = .XX, p = .XXX.

**Example**:
> A partial correlation was conducted to assess the relationship between education level and income while controlling for years of work experience. After controlling for experience, there was a significant positive correlation, r(97) = .32, p = .001, indicating that education level was associated with income even when experience was held constant.

## Regression Templates

### Simple Linear Regression

**Template**:
> A simple linear regression was conducted to predict [DV] from [IV]. The regression equation was: [DV] = [intercept] + [slope] x [IV]. The model explained XX% of the variance in [DV], R² = .XX, *F*(1, df) = X.XX, p = .XXX. [IV] significantly predicted [DV], beta = X.XX, t(df) = X.XX, p = .XXX, 95% CI [X.XX, X.XX].

**Example**:
> A simple linear regression was conducted to predict sales from advertising expenditure. The regression equation was: Sales = 12,500 + 3.2 x Advertising. The model explained 64% of the variance in sales, R² = .64, *F*(1, 48) = 85.3, p < .001. Advertising expenditure significantly predicted sales, beta = 0.80, t(48) = 9.24, p < .001, 95% CI [2.52, 3.88].

### Multiple Linear Regression

**Template**:
> A multiple linear regression was conducted to predict [DV] from [IV1], [IV2], and [IV3]. The overall model explained XX% of the variance in [DV], R² = .XX, *F*(df1, df2) = X.XX, p = .XXX. [Adjusted R² = .XX.] [Individual predictors: table or text]

**Example**:
> A multiple linear regression was conducted to predict job performance from cognitive ability, personality, and motivation. The overall model explained 45% of the variance in job performance, R² = .45, *F*(3, 96) = 26.2, p < .001, adjusted R² = .43. As shown in Table 1, cognitive ability (beta = .42, p < .001) and motivation (beta = .31, p = .002) were significant predictors, whereas personality was not (beta = .12, p = .198).

**Table Example**:
```
Table 1
Multiple Regression Results Predicting Job Performance

Predictor        B      SE B    Beta     t      p      95% CI
----------------------------------------------------------------
Constant      12.45    3.21            3.88   <.001  [6.08, 18.82]
Cognitive      0.42    0.08    .42     5.25   <.001  [0.26, 0.58]
Personality    0.15    0.12    .12     1.25   .198   [-0.09, 0.39]
Motivation     0.31    0.10    .31     3.10   .002   [0.11, 0.51]
----------------------------------------------------------------
Note. R² = .45, adjusted R² = .43, F(3, 96) = 26.2, p < .001.
```

### Logistic Regression

**Template**:
> A logistic regression was conducted to predict [binary DV] from [predictor(s)]. The model [was/was not] significant, chi-square(df) = X.XX, p = .XXX. [Nagelkerke R² = .XX.] The model correctly classified XX% of cases. [Predictor name] was a [significant/non-significant] predictor, OR = X.XX, 95% CI [X.XX, X.XX], Wald = X.XX, p = .XXX.

**Example**:
> A logistic regression was conducted to predict student retention from GPA, financial aid status, and first-generation status. The model was significant, chi-square(3) = 42.5, p < .001, Nagelkerke R² = .38. The model correctly classified 78% of cases. GPA was a significant predictor, OR = 2.45, 95% CI [1.78, 3.37], Wald = 28.9, p < .001, indicating that each unit increase in GPA was associated with 2.45 times higher odds of retention. First-generation status was also significant, OR = 0.52, 95% CI [0.31, 0.87], Wald = 6.2, p = .013, indicating lower odds of retention for first-generation students.

## Effect Size Reporting Quick Reference

| Test | Effect Size | Format |
|------|-------------|--------|
| t-test | Cohen's d | d = 0.50, 95% CI [0.20, 0.80] |
| ANOVA | Partial eta-squared | partial eta-squared = .23, 90% CI [.07, .36] |
| Correlation | Pearson's r | r(98) = .72, 95% CI [.61, .80] |
| Chi-square | Cramer's V | Cramer's V = 0.27 |
| Regression | R² | R² = .45, adjusted R² = .43 |
| Logistic regression | Odds ratio | OR = 2.45, 95% CI [1.78, 3.37] |

## Common Mistakes to Avoid

1. **Reporting p = .000**: Report p < .001 instead
2. **Omitting effect sizes**: Always include effect sizes
3. **Missing confidence intervals**: Include CIs when possible
4. **Not italicizing test statistics**: *t*, *F*, *r*, etc. should be italicized
5. **Using p < .05**: Report exact p-values (p = .043)
6. **Omitting degrees of freedom**: Always include df
7. **Not reporting direction**: Specify which group was higher/lower
8. **Missing descriptive statistics**: Report M and SD for each group
9. **Incorrect CI format**: Use brackets [lower, upper]
10. **Not interpreting results**: Provide interpretation of findings