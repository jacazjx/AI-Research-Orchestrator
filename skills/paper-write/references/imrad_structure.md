# IMRAD Structure Guidelines

## Table of Contents

- Overview
- Introduction Section
- Methods Section
- Results Section
- Discussion Section
- Additional Sections
- Venue-Specific Variations
- Templates

## Overview

IMRAD (Introduction, Methods, Results, And Discussion) is the standard structure for scientific papers. Each section serves a distinct purpose:

| Section | Purpose | Key Question Answered |
|---------|---------|----------------------|
| Introduction | Why this research? | What is the problem and why does it matter? |
| Methods | How was it done? | How can others replicate this work? |
| Results | What was found? | What are the objective findings? |
| Discussion | What does it mean? | How do findings relate to existing knowledge? |

### Information Flow

```
Introduction → Methods → Results → Discussion
     ↓            ↓          ↓          ↓
   "Why"       "How"     "What"     "So What"
```

## Introduction Section

### Purpose

Establish the research context, identify the gap, and state contributions.

### Funnel Structure

The Introduction follows a "funnel" shape - starting broad and narrowing to your specific contribution:

```
┌─────────────────────────────────────────────────────┐
│                 Broad Context                        │
│         (Why is this field important?)               │
├─────────────────────────────────────────────────────┤
│              Specific Problem                        │
│     (What specific problem do we address?)           │
├─────────────────────────────────────────────────────┤
│              Existing Limitations                    │
│      (What can't current approaches do?)             │
├─────────────────────────────────────────────────────┤
│              Contribution Statement                  │
│        (What do we do in this paper?)                │
└─────────────────────────────────────────────────────┘
```

### Paragraph-by-Paragraph Guide

#### Paragraph 1-2: Broad Context

**Purpose**: Establish importance and relevance.

**Content**:
- Why is this research area important?
- What is the broader impact?
- Who cares about this problem?

**Example**:
```markdown
Large language models (LLMs) have revolutionized natural language
processing, achieving unprecedented performance on tasks ranging
from question answering to code generation. These models are now
deployed in production systems serving millions of users daily,
making their efficiency and reliability crucial for real-world
applications.
```

#### Paragraph 2-3: Specific Problem

**Purpose**: Narrow to the specific research gap.

**Content**:
- What specific challenge does this field face?
- Why is current performance insufficient?
- What is the core technical difficulty?

**Example**:
```markdown
Despite their success, LLMs suffer from a critical limitation:
their computational cost scales quadratically with sequence length
due to the self-attention mechanism. This restricts their
applicability to long documents, where many real-world use cases
lie. Processing a 100K token document requires prohibitive memory
and computation, even on high-end hardware.
```

#### Paragraph 3-4: Existing Limitations

**Purpose**: Show what prior work cannot achieve.

**Content**:
- What have others tried?
- Why are existing solutions insufficient?
- What is missing?

**Example**:
```markdown
Several approaches have been proposed to address this limitation.
Sparse attention patterns reduce complexity but sacrifice model
quality [1, 2]. Linear attention variants maintain efficiency but
underperform on tasks requiring precise token interactions [3, 4].
Recurrent approaches process sequences efficiently but struggle
with long-range dependencies [5]. None of these solutions achieves
both efficiency and quality on par with standard attention.
```

#### Paragraph 4-5: Contribution Statement

**Purpose**: Clearly state what this paper contributes.

**Content**:
- What does this paper propose?
- What are the specific contributions?
- What are the key results?

**Template**:
```markdown
In this paper, we propose [method name], a novel approach to
[problem] that [key innovation]. Our contributions are as follows:

1. We introduce [contribution 1], which [what it enables].
2. We provide [contribution 2], demonstrating [key result].
3. We conduct [contribution 3], showing [quantitative improvement].

Our experiments on [datasets/benchmarks] demonstrate that [method]
achieves [quantitative result], outperforming [baseline] by [X]%
while reducing computational cost by [Y]%.
```

**Example**:
```markdown
In this paper, we propose FlashAttention, an IO-aware exact
attention algorithm that computes attention in linear memory.
Our contributions are as follows:

1. We introduce a tiling strategy that exploits the memory
   hierarchy of GPUs, reducing HBM accesses by 2-4x.
2. We provide a theoretical analysis showing our algorithm is
   IO-optimal for the attention computation.
3. We conduct comprehensive experiments showing FlashAttention
   achieves 2-4x speedup while maintaining exact attention.

Our experiments on language modeling and long-document tasks
demonstrate that FlashAttention enables training on sequences
4x longer than standard attention with comparable quality.
```

### Gap Identification

A strong gap identification is essential for a compelling Introduction.

**Weak Gap Statement**:
```
"Little work has been done on X."
```
(Vague, may not be true, doesn't explain why it matters)

**Strong Gap Statement**:
```
"While approaches A and B address X and Y respectively, no existing
method simultaneously handles both. This gap is significant because
real-world applications require both capabilities simultaneously,
as demonstrated by [citation]."
```
(Specific, explains limitation, justifies importance)

### Contribution Statement Templates

#### Single Contribution

```markdown
Our main contribution is [method/approach/insight], which [what it does].
We demonstrate that [quantitative result].
```

#### Multiple Contributions

```markdown
Our contributions are as follows:

1. **[Contribution Type]**: We [specific contribution]. This enables
   [capability not possible before].
2. **[Contribution Type]**: We [specific contribution]. Our analysis
   shows [key finding].
3. **[Contribution Type]**: We [specific contribution]. Results on
   [benchmark] demonstrate [quantitative improvement].
```

#### Contribution Types

| Type | Template |
|------|----------|
| New Method | "We propose/introduce/present [method name], a novel approach to [problem]" |
| New Dataset | "We release [dataset name], a new benchmark for [task]" |
| New Insight | "We provide theoretical analysis showing [key result]" |
| New Baseline | "We establish strong baselines for [task] using [approaches]" |
| Negative Result | "We investigate [hypothesis] and find that [surprising result]" |

## Methods Section

### Purpose

Provide enough detail for others to replicate the work.

### Structure

```markdown
## [N]. Methods

### [N].1 Problem Formulation
[Define the problem mathematically]

### [N].2 Overview
[High-level description of the approach]

### [N].3 [Component 1 Name]
[Detailed description]

### [N].4 [Component 2 Name]
[Detailed description]

...

### [N].[K] Implementation Details
[Practical considerations, hyperparameters]
```

### Problem Formulation

**Requirements**:
- Define all notation before use
- State objective function explicitly
- Specify constraints if any

**Template**:
```markdown
### Problem Formulation

Let X denote [input space] and Y denote [output space]. Given a
dataset D = {(x_i, y_i)}_{i=1}^N, our goal is to learn a function
f: X → Y that minimizes the expected loss:

    L(f) = E_{(x,y)~P(X,Y)} [l(f(x), y)]

where l(·,·) is [loss function]. We make the following assumptions:
1. [Assumption 1]
2. [Assumption 2]
```

### Notation Table

For complex methods, include a notation table:

```markdown
| Symbol | Description |
|--------|-------------|
| X | Input space |
| x ∈ X | Input sample |
| N | Number of samples |
| d | Hidden dimension |
| L | Number of layers |
| θ | Model parameters |
```

### Algorithm Description

**Guidelines**:
1. Start with high-level overview
2. Break into logical components
3. Provide pseudocode for complex procedures
4. Explain design choices

**Pseudocode Template** (LaTeX):
```latex
\begin{algorithm}[t]
\caption{[Algorithm Name]}
\label{alg:[label]}
\begin{algorithmic}[1]
\REQUIRE Input: [input description]
\ENSURE Output: [output description]
\STATE [Step 1]
\STATE [Step 2]
\FOR{[condition]}
    \STATE [Loop body]
\ENDFOR
\RETURN [result]
\end{algorithmic}
\end{algorithm}
```

### Implementation Details

Include practical details for reproducibility:

```markdown
### Implementation Details

**Hyperparameters**: We use learning rate of 1e-4 with AdamW optimizer
[32], weight decay 0.01, and batch size 64. We train for 100K steps
with linear warmup for the first 10K steps.

**Hardware**: All experiments run on 8x A100 80GB GPUs with mixed
precision training (bfloat16).

**Code**: Our implementation is based on PyTorch 2.0 [33] and will
be released upon publication.
```

### Theoretical Analysis (if applicable)

Include when:
- Method has theoretical guarantees
- Complexity analysis is relevant
- Convergence proofs exist

**Template**:
```markdown
### Theoretical Analysis

**Theorem 1**. [Statement of theorem]

*Proof sketch*. [Brief proof or reference to appendix for full proof].

**Corollary 1**. [Implication of theorem for practical use].

The complexity of our algorithm is O(n log n) compared to O(n^2)
for the baseline, as shown in Table 2.
```

## Results Section

### Purpose

Present findings objectively without interpretation.

### Structure

```markdown
## [N]. Experiments

### [N].1 Experimental Setup
- Datasets
- Baselines
- Metrics
- Implementation

### [N].2 Main Results
[Primary comparison]

### [N].3 Ablation Studies
[Component analysis]

### [N].4 Analysis
[Deeper investigation]
```

### Experimental Setup

**Datasets**:
```markdown
**Datasets**: We evaluate on four benchmark datasets:
- **Dataset A**: [description, size, split]
- **Dataset B**: [description, size, split]
All datasets are publicly available under [license].
```

**Baselines**:
```markdown
**Baselines**: We compare against:
- **Baseline 1** [cite]: [brief description]
- **Baseline 2** [cite]: [brief description]
For fair comparison, we use official implementations and recommended
hyperparameters for all baselines.
```

**Metrics**:
```markdown
**Metrics**: We report:
- **Accuracy**: Percentage of correct predictions
- **F1 Score**: Harmonic mean of precision and recall
- **AUC-ROC**: Area under the receiver operating characteristic curve
For statistical significance, we report 95% confidence intervals
over 5 random seeds.
```

### Presenting Results

**Table Presentation**:
```
Table 2 shows main results on benchmark datasets. Our method
outperforms all baselines on Dataset A by 3.2% (p < 0.01) and on
Dataset B by 2.1% (p < 0.05). The improvement is most pronounced
on the more challenging Dataset A, where the gap to the strongest
baseline is 5.8%.
```

**Figure Presentation**:
```
Figure 3 visualizes the learned embeddings using t-SNE. Our method
produces clearly separated clusters corresponding to class labels,
while the baseline shows significant overlap between classes.
```

### Statistical Reporting

**Required**:
- Mean and standard deviation (mean ± std)
- Number of runs (n=5 random seeds)
- Statistical significance (p-value)

**Format**:
```latex
Our method achieves 92.3 ± 0.4\% accuracy compared to 88.1 ± 0.5\%
for the best baseline (p < 0.001, two-tailed paired t-test, n=5).
```

### Ablation Studies

**Purpose**: Validate design choices.

**Template**:
```markdown
### Ablation Studies

To understand the contribution of each component, we conduct
ablation experiments (Table 3). Removing component A decreases
accuracy by 2.3%, demonstrating its importance for [reason].
Component B contributes 1.8% improvement through [mechanism].
```

## Discussion Section

### Purpose

Interpret results, relate to prior work, acknowledge limitations.

### Structure

```markdown
## [N]. Discussion

### [N].1 Interpretation
[What do results mean?]

### [N].2 Comparison with Prior Work
[How do findings relate to literature?]

### [N].3 Limitations
[Honest assessment]

### [N].4 Future Work
[Promising directions]

### [N].5 Broader Impact (optional)
[Societal implications]
```

### Interpretation

Move beyond restating results:

```
WEAK: "Our method achieved 92.3% accuracy."
GOOD: "Our method achieved 92.3% accuracy, indicating that [insight].
The improvement is most pronounced on [condition], suggesting that
[mechanism] is particularly effective when [circumstance]."
```

### Limitations Section

**Guidelines**:
- Be honest and specific
- Explain impact, not just list
- Suggest mitigations or future work

**Template**:
```markdown
### Limitations

Our work has several limitations:

1. **Scalability**: Our method requires O(n) memory, which may be
   prohibitive for extremely long sequences (>1M tokens). Future
   work could explore memory-efficient variants.

2. **Generalization**: We evaluate on English text; performance on
   other languages remains to be verified. Multilingual extension
   would require additional investigation.

3. **Hyperparameter Sensitivity**: Performance varies with learning
   rate selection (see Appendix D). We recommend the provided
   default hyperparameters as a starting point.

Despite these limitations, our approach provides a strong foundation
for [application domain].
```

### Future Work

Be specific rather than generic:

```
WEAK: "Future work could explore other applications."
GOOD: "Future work could explore applying this approach to video
understanding, where temporal dependencies span thousands of frames
[ref], or to scientific document analysis, where papers routinely
exceed 10K tokens [ref]."
```

## Additional Sections

### Abstract

**Structure** (150-250 words):
1. Context (1-2 sentences)
2. Objective (1 sentence)
3. Method (1-2 sentences)
4. Results (2-3 sentences)
5. Conclusion (1 sentence)

**Template**:
```markdown
[Context: Why this matters] [Objective: What we address] We propose
[method name], a novel approach that [key innovation]. [Method details]
Our method [brief technical description]. [Results] Experiments on
[datasets] demonstrate that [method] achieves [quantitative result],
outperforming [baseline] by [X]%. [Conclusion] This enables [new
capability], with implications for [application domain].
```

### Related Work

**Structure Options**:

1. **By Approach** (recommended for ML papers):
   - Group papers by methodology
   - End each group with gap identification

2. **By Research Question**:
   - Group by what problem they solve
   - Useful for survey-style papers

3. **Chronological**:
   - Order by publication date
   - Useful for historical context

**Template per Subsection**:
```markdown
### [Approach Category]

[Overview of this category of methods]

[Specific papers and contributions]
Author et al. [1] propose [method], which achieves [result] but
suffers from [limitation]. Building on this, Author et al. [2]
introduce [improvement], addressing [limitation] at the cost of
[new limitation].

[Gap identification]
However, none of these approaches addresses [gap], which our work
targets by [approach].
```

### Conclusion

**Structure** (1-2 paragraphs):
1. Recap main contributions
2. Summarize key results
3. State broader impact or future direction (1 sentence)

**Template**:
```markdown
We presented [method], a novel approach to [problem] that achieves
[quantitative result]. Our key contributions include [contribution 1],
[contribution 2], and [contribution 3]. Experiments demonstrate
[summary of main findings]. Future work includes [specific direction].
```

## Venue-Specific Variations

### Conference Papers (NeurIPS, ICML, ICLR)

| Aspect | Typical Requirements |
|--------|---------------------|
| Length | 8 pages main + unlimited appendix |
| Abstract | 150-250 words |
| Related Work | Often merged with Introduction |
| Broader Impact | Required (NeurIPS) |
| Checklist | Required (varies by conference) |

### Journal Papers (TPAMI, JMLR)

| Aspect | Typical Requirements |
|--------|---------------------|
| Length | No strict limit (typically 20+ pages) |
| Abstract | 150-300 words |
| Related Work | Separate, comprehensive section |
| Proofs | Full proofs in main text or appendix |
| Reproducibility | Detailed implementation section |

### Workshop Papers

| Aspect | Typical Requirements |
|--------|---------------------|
| Length | 4-8 pages |
| Abstract | 100-200 words |
| Related Work | Brief, often merged |
| Experiments | May be preliminary |

## Templates

### Full Paper Outline

```markdown
# [Title]

## Abstract
[150-250 words]

## 1. Introduction
- Paragraph 1-2: Broad context
- Paragraph 2-3: Specific problem
- Paragraph 3-4: Existing limitations
- Paragraph 4-5: Contributions

## 2. Related Work
### 2.1 [Category 1]
### 2.2 [Category 2]
### 2.3 [Category 3]

## 3. Preliminaries / Problem Formulation
[Background and notation]

## 4. Method
### 4.1 Overview
### 4.2 [Component 1]
### 4.3 [Component 2]
### 4.4 Theoretical Analysis

## 5. Experiments
### 5.1 Experimental Setup
### 5.2 Main Results
### 5.3 Ablation Studies
### 5.4 Analysis

## 6. Discussion
### 6.1 Interpretation
### 6.2 Limitations
### 6.3 Future Work

## 7. Conclusion

## References

## Appendix
```

## References

- CONSORT Statement: Guidelines for reporting randomized trials
- PRISMA Statement: Guidelines for systematic reviews
- STROBE Statement: Guidelines for observational studies
- ARRIVE Guidelines: Guidelines for animal experiments