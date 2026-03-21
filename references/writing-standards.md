# Writing Standards

Academic writing conventions, manuscript structure, common pitfalls, figure/table standards, citation formatting, and paper quality assurance for research manuscripts.

---

## Academic Writing Conventions

### Core Principles

| Principle | Academic Standard | Avoid |
|-----------|-------------------|-------|
| Objectivity | Third person, neutral, evidence-based, precise | First/second person, emotional, opinion-based, colloquial |
| Precision | "The model achieves 94.2% accuracy on the test set." | "The model works well." |
| Hedging | "may", "suggests", "likely" for speculative claims | Over-hedging: "could potentially suggest that results might possibly indicate..." |

### Document Structure

#### Abstract (Hourglass Model)

```
Broad context (1-2 sentences)
  -> Specific problem (1-2 sentences)
    -> Method/approach (2-3 sentences)
    -> Key results (2-3 sentences)
  -> Implications (1-2 sentences)
```

**Checklist:** Self-contained (no citations), no undefined abbreviations, key results with numbers, under word limit (150-300 words). Write last.

#### Introduction (Inverted Triangle)

1. **Hook:** Why should readers care?
2. **Background:** Essential context
3. **Problem:** What is unknown/unresolved?
4. **Gap:** What is missing in prior work?
5. **Contribution:** What did you do?
6. **Preview:** Paper structure overview

#### Section Quality Standards

| Section | Key Requirements |
|---------|-----------------|
| Abstract | 150-250 words, covers problem, approach, results, impact |
| Introduction | Clear motivation, contributions listed, funnel structure |
| Related Work | Comprehensive, fair, organized by approach, ends with gap identification |
| Method | Complete, reproducible, well-illustrated, notation defined upfront |
| Experiments | Complete setup, all details, ablation studies |
| Results | Objective presentation with statistics, all figures/tables referenced |
| Discussion | Interprets results, compares with related work, limitations acknowledged |
| Conclusion | Summary + limitations + future work |

### Tense Usage

| Section | Tense | Example |
|---------|-------|---------|
| Abstract (findings) | Present | We show that... |
| Introduction (background) | Present | CNNs are widely used... |
| Methods | Past | We collected data... |
| Results | Past | The model achieved... |
| Discussion (interpretation) | Present | This suggests... |
| Conclusion | Present | We conclude that... |

---

## Paragraph Structure

### The MEAL Plan

| Component | Purpose | Example |
|-----------|---------|---------|
| **M**ain Idea | Topic sentence | "Our approach improves efficiency through a novel caching mechanism." |
| **E**vidence | Supporting data or citation | "Experiments show 40% speedup (Table 3)." |
| **A**nalysis | Interpretation | "This improvement stems from reduced redundant computation." |
| **L**ink | Connect to next paragraph | "Having established efficiency gains, we now examine accuracy." |

### Paragraph Length

| Context | Recommended Length |
|---------|-------------------|
| Introduction | 4-8 sentences |
| Methods | 4-6 sentences |
| Results | 3-5 sentences per finding |
| Discussion | 5-8 sentences |

Warning signs: single-sentence paragraphs (merge), over 10 sentences (split), no clear topic sentence.

### Transitions

| Purpose | Phrases |
|---------|---------|
| Addition | furthermore, moreover, additionally, similarly |
| Contrast | however, nevertheless, conversely, in contrast |
| Cause | therefore, consequently, thus, hence |
| Example | for instance, specifically, notably |
| Sequence | first, second, subsequently, finally |

### Signposting

Guide readers through complex arguments:
- "To address this, we propose..."
- "Building on this observation..."
- "As shown in Figure 3..."
- "This section is organized as follows..."

---

## Common Mistakes to Avoid

### Weak Openings

| Avoid | Use Instead |
|-------|-------------|
| "It is important to note that..." | Direct statement |
| "It should be mentioned that..." | State the point directly |
| "In terms of..." | Use specific preposition |

### AI-Typical Language

| AI Phrase | Natural Alternative |
|-----------|-------------------|
| "delve into" | "examine", "explore" |
| "pivotal", "crucial", "paramount" | "key", "important", "primary" |
| "It is worth noting that" | Remove entirely |
| "In order to" | "to" |
| "underscores" | "highlights", "emphasizes" |
| "tapestry", "landscape" | Remove or use "field", "area" |

### Other Pitfalls

- **Ambiguous pronouns**: "This demonstrates its effectiveness" -- unclear referent. Be explicit.
- **Passive voice overuse**: "We conducted experiments" is clearer than "Experiments were conducted." Use passive only when the actor is irrelevant.
- **Redundancy**: "past history", "basic fundamentals", "reason why" -- drop the redundant word.
- **Run-on sentences**: Break sentences over 30 words.
- **Dangling modifiers**: "Using this approach, the results improved" -- who used it? Fix: "Using this approach, we improved the results."
- **Excessive hedging**: Quantify when you can. "X% better" beats "somewhat better."

---

## Figure and Table Standards

### General Principles

Every figure and table should: (1) communicate a specific finding, (2) be understandable without the main text, (3) support the narrative.

### Figure Best Practices

- **Resolution**: 300 DPI minimum; vector (PDF/SVG) preferred
- **Labels**: Readable at printed size
- **Captions**: Self-contained explanation
- **Colors**: Colorblind-safe palettes (Blue & Orange, viridis). Avoid Red & Green or rainbow.
- **Line styles**: Use different styles (solid, dashed, dotted) for B&W printing

### Figure Types

| Type | Best For |
|------|----------|
| Line plot | Trends over time/epochs |
| Bar chart | Comparing categories |
| Scatter plot | Relationships/correlation |
| Heatmap | Matrices/distributions |
| Box/Violin plot | Distribution shape and variance |

### Table Formatting

| Element | Convention |
|---------|------------|
| Title | Above table, italicized |
| Headers | Bold, title case |
| Numbers | Right-aligned, consistent decimals |
| Lines | Horizontal only (top, below headers, bottom) |
| Best result | **Bold**, with significance markers (*, **, ***) |

Include: arrows for direction (higher/lower is better), mean +/- std, significance tests.

### Error Bars and Significance

| Type | When to Use |
|------|-------------|
| Standard deviation (SD) | Showing data spread |
| Standard error (SEM) | Showing precision of mean |
| 95% CI | Showing confidence in estimate |

```
ns (not significant)   p > 0.05
*                      p <= 0.05
**                     p <= 0.01
***                    p <= 0.001
```

### Sizing for Publication

```python
fig, ax = plt.subplots(figsize=(3.5, 2.5))   # Single-column
fig, ax = plt.subplots(figsize=(7, 4))         # Two-column
plt.savefig('figure.pdf', dpi=300, bbox_inches='tight')
```

---

## Citation Formatting

### Venue Style Preferences

| Venue | Style | Notes |
|-------|-------|-------|
| NeurIPS/ICML/ICLR | BibTeX | LaTeX template provided |
| CVPR | IEEE-like | Numbered citations |
| ACL | ACL style | Custom BibTeX style |
| AAAI | AAAI style | Numbered citations |

### BibTeX Entry Types

| Entry Type | Required Fields |
|------------|-----------------|
| @article | author, title, journal, year |
| @inproceedings | author, title, booktitle, year |
| @book | author, title, publisher, year |
| @misc | author, title, year |

### APA 7th Edition Essentials

- One author: (Smith, 2020); Two: (Smith & Jones, 2020); Three+: (Smith et al., 2020)
- Reference list: alphabetical, hanging indent, DOI as https://doi.org/xxxxx

### Citation Best Practices

Cite: direct quotes, paraphrased ideas, methods from others, data sources, code/software.
Do not cite: common knowledge, public domain facts, general concepts.

---

## Paper Quality Assurance

### Peer Review Criteria

| Criterion | What Reviewers Look For |
|-----------|------------------------|
| Novelty | What's new? Is it significant? |
| Soundness | Is the methodology correct? |
| Significance | Does it matter? Impact? |
| Clarity | Is the writing clear? |
| Reproducibility | Can others replicate this? |
| Comparison | Fair baselines? Honest comparison? |

### Addressing Common Reviewer Concerns

- **Novelty**: Clear contribution statement, explicit differentiation in Related Work, quantitative comparison.
- **Methodology**: Hyperparameter settings, multiple runs with variance, significance tests, ablation studies.
- **Significance**: Motivate clearly, show practical applications, quantify improvements.
- **Clarity**: Figures for complex concepts, all notation defined, pseudocode for algorithms.

### Review Dimensions

| Dimension | Weight | Focus Areas |
|-----------|--------|-------------|
| Novelty | 25% | Problem, method, theory, empirical |
| Evidence | 30% | Rigor, statistics, baselines, reproducibility |
| Theory | 15% | Grounding, correctness, limitations |
| Analysis | 15% | Depth, discussion, future work |
| Writing | 15% | Clarity, structure, presentation |

### Content Authenticity

For each claim in the manuscript, map to evidence source, verify against experiment logs. Red flags: numbers not in logs, citations to non-existent papers, perfect results, missing experiments.

### Pre-Submission Checklist

- [ ] Title informative and concise
- [ ] Abstract self-contained, under word limit
- [ ] Introduction has clear motivation and contributions
- [ ] Methods reproducible
- [ ] Results with statistics, all figures/tables referenced
- [ ] Discussion addresses limitations
- [ ] All claims supported by evidence
- [ ] Citations complete, correct, DOI-verified
- [ ] Language precise and objective, no AI-typical phrases
- [ ] Figures high-resolution and colorblind-safe
- [ ] Tables consistently formatted
- [ ] Venue formatting guidelines followed
