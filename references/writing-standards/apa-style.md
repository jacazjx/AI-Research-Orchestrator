# APA Style Guide

## Overview

APA (American Psychological Association) style is the most common citation and formatting style in social sciences, psychology, and increasingly in other fields. This guide covers APA 7th edition.

## General Formatting

### Document Setup

| Element | Setting |
|---------|---------|
| Font | 12-point Times New Roman or sans-serif equivalent |
| Margins | 1 inch on all sides |
| Line spacing | Double-spaced throughout |
| Paragraph indentation | First line: 0.5 inches |
| Alignment | Left-aligned (ragged right) |
| Page numbers | Top right corner |

### Title Page Elements

```markdown
Running head: SHORT TITLE  (professional papers only)

Title
Subtitle (if any)

Author Name
Affiliation
Course (if applicable)
Instructor (if applicable)
Date
```

## Headings

### Heading Hierarchy

```markdown
# Level 1: Centered, Bold, Title Case
Text begins on new line.

## Level 2: Left-Aligned, Bold, Title Case
Text begins on new line.

### Level 3: Left-Aligned, Bold Italic, Title Case
Text begins on new line.

#### Level 4: Indented, Bold, Title Case, Period.
Text continues on same line.

##### Level 5: Indented, Bold Italic, Title Case, Period.
Text continues on same line.
```

### Heading Selection

| Number of Levels | Use |
|------------------|-----|
| 1 level | Level 1 |
| 2 levels | Levels 1, 2 |
| 3 levels | Levels 1, 2, 3 |
| 4 levels | Levels 1, 2, 3, 4 |
| 5 levels | Levels 1, 2, 3, 4, 5 |

## In-Text Citations

### Author-Date Format

**One author:**
```markdown
(Smith, 2020) or Smith (2020) found that...
```

**Two authors:**
```markdown
(Smith & Jones, 2020) or Smith and Jones (2020) found...
```

**Three or more authors:**
```markdown
(Smith et al., 2020) or Smith et al. (2020) found...
```

**Group author:**
```markdown
(National Institute of Health [NIH], 2020)
First citation: (National Institute of Health [NIH], 2020)
Subsequent: (NIH, 2020)
```

### Multiple Works

**Same author, different years:**
```markdown
(Smith, 2018, 2020, 2022)
```

**Same author, same year:**
```markdown
(Smith, 2020a, 2020b)
```

**Different authors:**
```markdown
(Smith, 2020; Jones, 2019; Lee, 2021)
(Alphabetical order by author surname)
```

### Direct Quotations

**Short quotes (< 40 words):**
```markdown
Smith (2020) found that "the effect was significant across all conditions" (p. 45).
```

**Long quotes (≥ 40 words):**
```markdown
Smith (2020) concluded:

The findings suggest that the intervention had a robust effect
across all demographic groups, with particularly strong effects
among younger participants. This pattern is consistent with
theoretical predictions. (p. 45)
```

### Secondary Sources

```markdown
Original source: Freud (1900)
Source you read: Smith (2020)

Citation: Freud (1900, as cited in Smith, 2020)
Reference list: Include Smith (2020) only
```

## Reference List

### General Format

- Alphabetical order by author surname
- Hanging indent (0.5 inches)
- Double-spaced
- DOI format: https://doi.org/xxxxx

### Journal Article

```markdown
Author, A. A., & Author, B. B. (Year). Title of article.
Title of Periodical, volume(issue), page–page.
https://doi.org/xxxxx

Example:
Smith, J. D., & Jones, M. K. (2020). The effect of sleep on memory.
Journal of Experimental Psychology, 45(2), 123–145.
https://doi.org/10.1037/0000000
```

### Book

```markdown
Author, A. A. (Year). Title of work: Capital letter for subtitle.
Publisher.

Example:
Kahneman, D. (2011). Thinking, fast and slow. Farrar, Straus and Giroux.
```

### Edited Book Chapter

```markdown
Author, A. A. (Year). Title of chapter. In E. E. Editor (Ed.),
Title of book (pp. xx–xx). Publisher.

Example:
Nisbett, R. E. (2020). Human inference. In D. Kahneman (Ed.),
Judgment under uncertainty (pp. 45–67). Cambridge University Press.
```

### Conference Paper

```markdown
Author, A. A. (Year, Month). Title of paper. In E. Editor (Ed.),
Proceedings of Conference Name (pp. xx–xx). Publisher.

Example:
Vaswani, A., et al. (2017, December). Attention is all you need.
In Advances in Neural Information Processing Systems (pp. 5998–6008).
```

### Website

```markdown
Author, A. A. (Year, Month Day). Title of page.
Site Name. https://www.example.com/page

Example:
World Health Organization. (2020, March 11). Coronavirus disease 2019.
https://www.who.int/emergencies/diseases/novel-coronavirus-2019
```

### Preprint (arXiv)

```markdown
Author, A. A. (Year). Title of paper. arXiv.
https://arxiv.org/abs/xxxxx

Example:
Brown, T. B., et al. (2020). Language models are few-shot learners.
arXiv. https://arxiv.org/abs/2005.14165
```

## Numbers and Statistics

### When to Use Numerals

- Numbers 10 and above
- Numbers that represent time, dates, ages, scores
- Numbers in abstracts
- Statistical results
- Decimal fractions

### When to Use Words

- Numbers zero through nine
- Any number beginning a sentence
- Common fractions (one half)

### Statistical Reporting

```markdown
t-test: t(df) = value, p = value, d = value
t(58) = 3.45, p < .001, d = 0.82

ANOVA: F(dfbetween, dfwithin) = value, p = value, η² = value
F(2, 57) = 12.34, p < .001, η² = 0.30

Correlation: r(df) = value, p = value
r(58) = .67, p < .001

Chi-square: χ²(df, N = n) = value, p = value
χ²(2, N = 100) = 15.67, p < .001

Regression: R² = value, F(df1, df2) = value, p = value
R² = .45, F(3, 96) = 23.45, p < .001
```

### Confidence Intervals

```markdown
95% CI [lower, upper]
The mean difference was 5.2 points (95% CI [3.1, 7.3]).
```

### P-value Formatting

| P-value | Format |
|---------|--------|
| p < .001 | p < .001 |
| .001 ≤ p < .01 | p = .003 |
| .01 ≤ p < 1.00 | p = .042 |
| p = 1.00 | p > .99 |

Note: Report exact p-values to two or three decimal places. Use p < .001 for values below .001.

## Tables

### Table Format

```markdown
Table 1
Comparison of Groups on Primary Outcomes

| Variable | Control (n = 50) | Treatment (n = 50) | t    | p     |
|----------|------------------|--------------------|------|-------|
| Score    | 75.2 (12.3)      | 82.1 (10.5)        | 3.02 | .003  |
| Time     | 45.6 (8.2)       | 38.9 (7.5)         | 4.21 | <.001 |

Note. Values are M (SD). Time measured in seconds.
```

### Table Guidelines

1. Number tables consecutively (Table 1, Table 2)
2. Brief but descriptive title (italicized)
3. Column headers (bold)
4. Horizontal lines only (top, below headers, bottom)
5. Note section for explanations

## Figures

### Figure Format

```markdown
Figure 1
Scatterplot showing the relationship between study time and test scores.

[Figure appears here]

Note. Each point represents one participant (N = 100).
The correlation was r = .67, p < .001.
```

### Figure Guidelines

1. Number figures consecutively (Figure 1, Figure 2)
2. Brief but descriptive title (italicized)
3. Clear axis labels with units
4. Legend if needed
5. Note section below figure

## Common Mistakes to Avoid

### Citation Errors

| Mistake | Correction |
|---------|------------|
| et al. for 2 authors | Use & for 2 authors in parentheses |
| et. al. | et al. (no period after "et") |
| (Smith, 2020, p. 5) for paraphrase | Page number only for direct quotes |
| Not citing paraphrased ideas | Always cite, even when paraphrasing |

### Format Errors

| Mistake | Correction |
|---------|------------|
| Single spacing | Double-space throughout |
| Right justification | Left-align text |
| Bold headings in wrong places | Follow heading hierarchy |
| Inconsistent capitalization | Use title case for titles in references |

## References

- American Psychological Association. (2020). Publication manual of the American Psychological Association (7th ed.)
- APA Style website: https://apastyle.apa.org/