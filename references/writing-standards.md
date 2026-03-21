# Writing Standards

This document covers academic writing conventions, APA style essentials, figure and table standards, paper quality assurance, and citation formatting rules for research manuscripts.

---

## Academic Writing Conventions

### Core Principles

#### 1. Objectivity

| Feature | Academic | Non-Academic |
|---------|----------|--------------|
| Voice | Third person | First/second person |
| Emotion | Neutral | Expressive |
| Opinion | Evidence-based | Personal |
| Language | Precise | Colloquial |

#### 2. Precision

Use precise, unambiguous language:
- BAD: "The model works well."
- GOOD: "The model achieves 94.2% accuracy on the test set."

#### 3. Hedging

| Hedge Type | Examples |
|------------|----------|
| Probability | likely, probably, possibly |
| Frequency | often, frequently, sometimes |
| Quantity | approximately, roughly, about |
| Conditionality | may, might, could, would |

### Document Structure

#### Abstract (Hourglass Model)

```
Broad context (1-2 sentences)
  -> Specific problem (1-2 sentences)
    -> Method/approach (2-3 sentences)
    -> Key results (2-3 sentences)
  -> Implications (1-2 sentences)
```

**Checklist:** Self-contained (no citations), no undefined abbreviations, key results with numbers, under word limit (150-300 words).

#### Introduction (Inverted Triangle)

1. **Hook:** Why should readers care?
2. **Background:** Essential context
3. **Problem:** What is unknown/unresolved?
4. **Gap:** What is missing in prior work?
5. **Contribution:** What did you do?
6. **Preview:** What follows?

#### Section Quality Standards

| Section | Key Requirements |
|---------|-----------------|
| Abstract | 150-250 words, covers problem, approach, results, impact |
| Introduction | Clear motivation, contributions listed |
| Related Work | Comprehensive, fair, differentiated |
| Method | Complete, reproducible, well-illustrated |
| Experiments | Complete setup, all details |
| Conclusion | Summary + limitations + future work |

### Style Guidelines

#### Tense Usage

| Section | Tense | Example |
|---------|-------|---------|
| Abstract (findings) | Present | We show that... |
| Introduction (background) | Present | CNNs are widely used... |
| Methods | Past | We collected data... |
| Results | Past | The model achieved... |
| Discussion (interpretation) | Present | This suggests... |
| Conclusion | Present | We conclude that... |

#### Paragraph Structure (CLAIM)

- **C**laim: Topic sentence
- **L**ead: Explanation
- **A**rgument: Evidence
- **I**nterpretation: Analysis
- **M**ake connection: Transition

#### Transitions

| Purpose | Transition Words |
|---------|------------------|
| Addition | furthermore, moreover, additionally |
| Contrast | however, nevertheless, conversely |
| Cause | therefore, consequently, thus |
| Example | for instance, specifically, notably |
| Sequence | first, second, subsequently |

---

## Figure and Table Standards

### General Principles

Every figure and table should:
1. **Communicate** a specific finding or concept
2. **Replace** text that would be lengthy or confusing
3. **Support** the narrative of the paper
4. Be understandable without reading the main text (self-containment rule)

### Figure Types

| Type | Best For | Example |
|------|----------|---------|
| Line plot | Trends over time/epochs | Training curves |
| Bar chart | Comparing categories | Model comparison |
| Scatter plot | Relationships | Correlation analysis |
| Heatmap | Matrices/distributions | Attention weights |
| Box plot | Distributions | Performance variance |
| Violin plot | Distribution shape | Accuracy spread |

### Figure Best Practices

- **Resolution**: 300 DPI minimum
- **Format**: Vector (PDF/SVG) preferred
- **Labels**: Readable at printed size
- **Captions**: Self-contained explanation
- **Colors**: Colorblind-safe palettes (Blue & Orange, viridis). Avoid Red & Green together or rainbow colormaps.
- **Line styles**: Use different styles (solid, dashed, dotted) for B&W printing

### Table Formatting Rules

| Element | Convention |
|---------|------------|
| Title | Above table, italicized |
| Headers | Bold, title case |
| Numbers | Right-aligned, consistent decimals |
| Text | Left-aligned |
| Notes | Below table, smaller font |
| Lines | Horizontal only (top, below headers, bottom) |

### Result Tables (ML Standard)

| Method | Accuracy (up arrow) | F1 (up arrow) | Time (down arrow) |
|--------|------------|------|--------|
| Baseline | 85.2 +/- 0.3 | 0.841 | 12.3 |
| Method A | 87.1 +/- 0.2 | 0.863 | 15.7 |
| **Ours** | **91.3 +/- 0.2** | **0.907** | **11.8** |

Include: Arrows for better direction, mean +/- std, bold for best, significance markers (*, **, ***)

### Statistical Visualization

| Error Bar Type | When to Use |
|------|-------------|
| Standard deviation (SD) | Showing data spread |
| Standard error (SEM) | Showing precision of mean |
| 95% CI | Showing confidence in estimate |

### Significance Indicators

```
ns (not significant)   p > 0.05
*                      p <= 0.05
**                     p <= 0.01
***                    p <= 0.001
****                   p <= 0.0001
```

### Sizing for Publication

```python
# Single-column width
fig, ax = plt.subplots(figsize=(3.5, 2.5))

# Two-column width
fig, ax = plt.subplots(figsize=(7, 4))

# Save at appropriate DPI
plt.savefig('figure.pdf', dpi=300, bbox_inches='tight')
```

---

## Citation Formatting

### Major Venue Style Preferences

| Venue | Style | Notes |
|-------|-------|-------|
| NeurIPS | BibTeX | LaTeX template provided |
| ICML | BibTeX | Author-year in-text |
| ICLR | BibTeX | Open review format |
| CVPR | IEEE-like | Numbered citations |
| ACL | ACL style | Custom BibTeX style |
| AAAI | AAAI style | Numbered citations |
| JMLR | MLA-like | Author-year |

### Quick Reference Card

| Element | IEEE | ACM | APA |
|---------|------|-----|-----|
| In-text | [1] | [Smith 2020] | (Smith, 2020) |
| Authors | A. Smith | Smith, A. | Smith, A. |
| Year | After title | After author | After author |
| Journal | Italic | Roman | Italic |
| Pages | 100-115 | 100-115 | 100-115 |
| DOI | Optional | DOI: | https://doi.org/ |

### BibTeX Entry Types

```bibtex
@article{smith2020,
  author    = {Smith, Adam and Jones, Beth},
  title     = {Title of the Article},
  journal   = {Journal Name},
  volume    = {10},
  number    = {2},
  pages     = {100--115},
  year      = {2020},
  doi       = {10.1000/xyz123}
}

@inproceedings{lee2021,
  author    = {Lee, Chris and Wang, David and Chen, Eric},
  title     = {Paper Title},
  booktitle = {Proceedings of the International Conference on Machine Learning},
  pages     = {1234--1245},
  year      = {2021}
}

@misc{vaswani2017,
  author    = {Vaswani, Ashish and others},
  title     = {Attention Is All You Need},
  year      = {2017},
  eprint    = {1706.03762},
  archivePrefix = {arXiv}
}
```

### Required Fields by Type

| Entry Type | Required Fields |
|------------|-----------------|
| @article | author, title, journal, year |
| @inproceedings | author, title, booktitle, year |
| @book | author, title, publisher, year |
| @misc | author, title, year |
| @phdthesis | author, title, school, year |

### APA 7th Edition Essentials

**In-Text:**
- One author: (Smith, 2020) or Smith (2020)
- Two authors: (Smith & Jones, 2020)
- Three+: (Smith et al., 2020)

**Reference List:**
- Alphabetical by surname, hanging indent, double-spaced
- DOI format: https://doi.org/xxxxx

**Statistical Reporting (APA):**
```
t-test: t(58) = 3.45, p < .001, d = 0.82
ANOVA: F(2, 57) = 12.34, p < .001, eta-squared = 0.30
Correlation: r(58) = .67, p < .001
95% CI [lower, upper]
```

### Citation Best Practices

| Cite | Don't Cite |
|------|------------|
| Direct quotes | Common knowledge |
| Paraphrased ideas | Your own prior work (unless published) |
| Methods from others | Facts in public domain |
| Data sources | General concepts |
| Code/software | Your unpublished thoughts |

### Typical Citation Counts

| Document Type | Typical Citations |
|---------------|-------------------|
| Conference paper | 20-40 |
| Journal article | 30-60 |
| Survey paper | 100+ |
| PhD thesis | 200+ |

---

## Paper Quality Assurance

### Venue Standards

#### Top-Tier Conferences

| Venue | Acceptance Criteria | Typical Bar |
|-------|---------------------|-------------|
| CVPR | Novelty + Visual Evidence | Top 25% |
| NeurIPS | Novelty + Theory/Empirical | Top 20% |
| ICLR | Novelty + Reproducibility | Top 30% |
| ACL | Novelty + Linguistic Insight | Top 25% |

#### Top-Tier Journals

| Venue | Acceptance Criteria | Typical Bar |
|-------|---------------------|-------------|
| TPAMI | Depth + Impact | ~15% |
| JMLR | Theory + Rigor | ~20% |
| Nature/Science | Impact + Broad Interest | <10% |

### Quality Dimensions

#### 1. Novelty Assessment

| Type | Description | Evidence Required |
|------|-------------|-------------------|
| Problem Novelty | New problem formulation | Problem not addressed before |
| Method Novelty | New algorithm/architecture | Technical innovation |
| Theoretical Novelty | New insight/proposition | Mathematical contribution |
| Empirical Novelty | New experimental findings | Novel results |

#### 2. Evidence Strength

**Experimental Rigor Checklist:**
- [ ] Clear hypothesis stated
- [ ] Appropriate evaluation metrics
- [ ] Statistical significance reported
- [ ] Multiple runs for variance
- [ ] Ablation studies included
- [ ] Baselines properly implemented

#### 3. Theoretical Foundation

**Correctness Checks:**
- All variables defined, notation consistent, derivations correct
- Assumptions clearly stated and justified
- Claims precisely worded, scope limited to evidence

#### 4. Limitations Section Template

```markdown
## Limitations

1. **[Limitation 1]**: [Description]
   - Impact: [How this affects applicability]
   - Mitigation: [Possible future solutions]
```

### Content Authenticity

#### Evidence-to-Claim Mapping

For each claim in the manuscript:
```markdown
### Claim: "[exact quote from paper]"

**Evidence Source:**
- Document: [filename]
- Section: [section]
- Data: [specific numbers]

**Verification Status:** [Verified/Partial/Unsupported]
```

#### Fabrication Prevention

| Red Flag | Detection Method |
|----------|-----------------|
| Numbers not in logs | Cross-check with evidence package |
| Citations to non-existent papers | DOI/Scholar verification |
| Perfect results | Statistical plausibility check |
| Missing experiments | Compare to experiment plan |

### Review Protocol

#### Review Dimensions

| Dimension | Weight | Focus Areas |
|-----------|--------|-------------|
| Novelty | 25% | Problem, method, theory, empirical |
| Evidence | 30% | Rigor, statistics, baselines, reproducibility |
| Theory | 15% | Grounding, correctness, limitations |
| Analysis | 15% | Depth, discussion, future work |
| Writing | 15% | Clarity, structure, presentation |

#### Review Template

```markdown
# Manuscript Review

## Decision: [Accept / Minor Revision / Major Revision / Reject]

## Summary
[Brief overall assessment]

## Strengths
1. [Specific strength]

## Weaknesses
1. [Specific weakness with location]

## Detailed Scores

| Dimension | Score | Comments |
|-----------|-------|----------|
| Novelty | [1-5] | [comments] |
| Evidence | [1-5] | [comments] |
| Theory | [1-5] | [comments] |
| Analysis | [1-5] | [comments] |
| Writing | [1-5] | [comments] |

## Blocking Issues
[List issues that prevent acceptance]

## Recommendations
[List specific, actionable recommendations]
```

### Gate 4 Requirements

| Requirement | Status |
|-------------|--------|
| Manuscript complete | [ ] |
| Citation audit passed | [ ] |
| Content authenticity verified | [ ] |
| Venue formatting compliant | [ ] |
| Score >= 4.0 average | [ ] |
| No blocking issues | [ ] |

### Pre-Submission Quality Checklist

- [ ] Title is informative and concise
- [ ] Abstract is self-contained
- [ ] Introduction has clear motivation and contribution
- [ ] Methods are reproducible
- [ ] Results are clearly presented with statistics
- [ ] Discussion addresses limitations
- [ ] Conclusion summarizes contributions
- [ ] All claims are supported by evidence
- [ ] Citations are complete and correct
- [ ] Language is precise and objective
- [ ] Figures are high-resolution and colorblind-safe
- [ ] Tables have consistent formatting
- [ ] Formatting follows venue guidelines
