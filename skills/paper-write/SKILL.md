---
name: airesearchorchestrator:paper-write
description: Generate LaTeX sections for paper following IMRAD structure with proper academic writing style. Writes section-by-section with detailed guidance for each section. Use when user says "write paper", "写论文", "generate LaTeX", "draft manuscript".
user-invocable: false
argument-hint: [paper-plan-path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, mcp__codex__codex
---
## Purpose

Generate LaTeX sections for paper from plan following IMRAD (Introduction, Methods, Results, And Discussion) structure with proper academic writing style, citation integration, and figure/table formatting.

## Workflow

### Phase 1: Preparation

1. **Read paper plan** from `paper/paper-plan.md`
2. **Review evidence package** from `docs/experiments/evidence-package-index.md`
3. **Check citation library** from `paper/references.bib`
4. **Review figures and tables** from `paper/figures/` and `paper/tables/`

### Phase 2: Section-by-Section Writing

Follow IMRAD structure with section-specific guidance. See `references/imrad_structure.md` for detailed guidelines.

#### 2.1 Abstract Writing

**Structure** (150-250 words):
1. **Context** (1-2 sentences): Background and problem importance
2. **Objective** (1 sentence): What this paper addresses
3. **Method** (1-2 sentences): Approach overview
4. **Results** (2-3 sentences): Key quantitative findings
5. **Conclusion** (1 sentence): Impact and implications

**Key Rules**:
- No citations in abstract
- No undefined abbreviations
- Self-contained (readable without paper)
- Match venue word limits exactly

#### 2.2 Introduction Writing (Funnel Structure)

**Paragraph Flow**:
1. **Broad Context** (1-2 paragraphs): Establish field importance
2. **Specific Problem** (1-2 paragraphs): Narrow to the gap
3. **Related Work Limitations** (1 paragraph): What existing work cannot do
4. **Contribution Statement** (1 paragraph): What this paper does
5. **Paper Organization** (optional): How paper is structured

**Key Elements**:

```markdown
## Contribution Statement Template

Our contributions are as follows:
1. We propose [method name], a novel approach to [problem] that [key innovation].
2. We provide theoretical analysis showing [key theoretical result].
3. We conduct comprehensive experiments on [datasets] demonstrating [quantitative improvement].
```

**Citation Integration**:
- Supportive: "Recent work has shown that X improves Y [1, 2]."
- Contrastive: "While method A achieves X, it fails to address Y [3]."
- Attribution: "The concept of X was first introduced by Smith et al. [4]."

See `references/academic_writing_style.md` for citation best practices.

#### 2.3 Related Work Writing

**Organization Strategies**:
- By approach type (recommended for ML papers)
- Chronological (for historical context)
- By research question (for survey-style)

**Structure per Topic**:

```markdown
### [Topic Name]

[Overview paragraph establishing importance]

[Detailed discussion of key papers]
- Paper A [cite]: contribution
- Paper B [cite]: builds on A
- Paper C [cite]: addresses limitation of B

[Gap identification leading to this work]
```

**Citation Density**:
- 3-5 citations per paragraph typical
- Group related citations: "[1, 2, 3]" not "[1], [2], [3]"
- Primary sources preferred over secondary

#### 2.4 Methods Writing

**Structure**:

```markdown
## [N]. Method

### [N].1 Problem Formulation
[Define notation, objective, constraints]

### [N].2 [Method Component 1]
[Detailed description with equations]

### [N].3 [Method Component 2]
[Continue with remaining components]

### [N].4 [Theoretical Analysis] (if applicable)
[Proofs, complexity analysis]

### [N].5 Implementation Details
[Practical considerations]
```

**Key Requirements**:
- All variables defined before use
- Consistent notation throughout
- Reproducibility: enough detail to replicate
- Algorithm pseudocode in float environment
- Figure for architecture/system diagram

#### 2.5 Experiments Writing

**Structure**:

```markdown
## [N]. Experiments

### [N].1 Experimental Setup
- Datasets
- Baselines
- Evaluation metrics
- Implementation details

### [N].2 Main Results
[Primary comparison tables/figures]

### [N].3 Ablation Studies
[Component analysis]

### [N].4 Analysis
[Deeper investigation of results]
```

**Statistical Reporting** (see `references/figure_table_guidelines.md`):

```latex
% Correct format
Our method achieves 92.3 +/- 0.4% accuracy, compared to 88.1 +/- 0.5%
for the best baseline (p < 0.001, paired t-test).
```

**Table Guidelines**:
- Best results in bold
- Include standard deviations
- Arrow indicators for metric direction (higher/lower is better)
- Self-contained captions

#### 2.6 Results Writing

**Structure**:
- Objective presentation without interpretation
- Reference all figures and tables
- Statistical significance for comparisons

**Writing Pattern**:

```markdown
Table [N] shows the main results. Our method outperforms all baselines
on [dataset] by [X]% (p < 0.01). Figure [N] visualizes the learned
representations, showing clear cluster separation.
```

**Key Rules**:
- Present, do not interpret (interpretation belongs in Discussion)
- Include confidence intervals and significance tests
- Acknowledge negative results honestly

#### 2.7 Discussion Writing

**Structure**:

```markdown
## [N]. Discussion

### [N].1 Interpretation of Results
[What the results mean]

### [N].2 Comparison with Prior Work
[How findings relate to existing literature]

### [N].3 Limitations
[Honest assessment of scope and weaknesses]

### [N].4 Future Work
[Promising directions]

### [N].5 Broader Impact (if required)
[Societal implications]
```

**Limitations Section Template**:

```markdown
### Limitations

Our work has several limitations:
1. **[Limitation 1]**: [Description and impact]
2. **[Limitation 2]**: [Description and impact]

We believe these limitations provide opportunities for future research.
```

#### 2.8 Conclusion Writing

**Structure** (1-2 paragraphs):
1. Summary of contributions
2. Key results recap
3. Future directions (1 sentence)

**Key Rules**:
- No new information
- No citations typically
- Match introduction's contribution statement

### Phase 3: Figure and Table Integration

See `references/figure_table_guidelines.md` for detailed standards.

**Figure Checklist**:
- [ ] 300 DPI minimum for raster images
- [ ] Vector format (PDF/EPS) preferred for diagrams
- [ ] Readable labels at printed size
- [ ] Self-contained captions
- [ ] Consistent style across all figures

**Table Checklist**:
- [ ] Consistent formatting throughout paper
- [ ] Units specified for all numerical values
- [ ] Appropriate significant figures (2-3)
- [ ] Self-contained captions
- [ ] Best results bolded

### Phase 4: Reference Management

1. **Build references.bib** from:
   - `docs/survey/references.bib`
   - `paper/citation-audit-report.md` (verified citations)

2. **Citation Quality Check**:
   - All citations have DOI (preferred) or arXiv ID
   - Primary sources used for key claims
   - No broken or placeholder citations

3. **Citation Style**: Use venue-specific style (e.g., `\bibliographystyle{plain}` for NeurIPS)

### Phase 5: LaTeX Compilation and Polish

1. **Clean stale files**: Remove old .aux, .log, .bbl files
2. **Compile**: pdflatex/bibtex cycle (3x for references)
3. **De-AI Polish**: Remove AI-typical phrases:
   - "delve", "pivotal", "crucial", "paramount"
   - "It is worth noting that..."
   - "In order to..." (use "to...")
   - Excessive hedging: "somewhat", "rather", "quite"

4. **Section Review**: Each section reviewed for:
   - Grammar and spelling
   - Consistent terminology
   - Logical flow
   - Proper citations

### Phase 6: Quality Assurance

1. **Run citation audit**: Verify all citations are authentic
2. **Check venue compliance**: Format, length, required sections
3. **Verify evidence mapping**: All claims traceable to evidence package

## Academic Style Guidelines

See `references/academic_writing_style.md` for comprehensive guidelines on:

- Active vs passive voice usage
- Tense by section (Introduction: present; Methods: past; Results: past; Discussion: present)
- Conciseness and clarity
- Hedging and confidence language
- Paragraph structure and transitions

## Key Rules

1. **IMRAD Structure**: Follow Introduction, Methods, Results, Discussion structure
2. **Citation Authenticity**: All citations must be verified (see `references/citation-standards.md`)
3. **Evidence Traceability**: All claims mapped to evidence package
4. **Statistical Rigor**: Report means, standard deviations, and significance
5. **Reproducibility**: Methods must be detailed enough for replication
6. **De-AI Polish**: Remove AI-typical phrases before final output
7. **Venue Compliance**: Match specific venue requirements

## Output Files

| File | Location | Purpose |
|------|----------|---------|
| Main Document | `paper/main.tex` | Document root |
| Sections | `paper/sections/*.tex` | Individual sections |
| References | `paper/references.bib` | Bibliography |
| Math Commands | `paper/math_commands.tex` | Custom math macros |
| Figures | `paper/figures/*.pdf` | Vector figures |
| Tables | `paper/tables/*.tex` | Table source files |

## Integration with Research Pipeline

This skill integrates with:
- **paper-plan**: Receives section structure and key points
- **paper-figure**: Receives figure specifications
- **audit-paper**: Quality gate for paper quality
- **latex-citation-curator**: Verified citation library

## References

- `references/imrad_structure.md` - Detailed IMRAD section guidelines
- `references/academic_writing_style.md` - Writing style guidelines
- `references/figure_table_guidelines.md` - Visualization standards
- `/home/jacazjx/Workspaces/AI-Research-Develop/AI-Research-Orchestrator/references/writing-standards.md` - Quality standards
- `/home/jacazjx/Workspaces/AI-Research-Develop/AI-Research-Orchestrator/references/citation-standards.md` - Citation verification