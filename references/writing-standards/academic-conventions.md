# Academic Writing Conventions

## Overview

Academic writing follows specific conventions that distinguish it from other forms of writing. Understanding these conventions is essential for producing professional research documents.

## Core Principles

### 1. Objectivity

Academic writing presents information objectively, avoiding personal bias:

| Feature | Academic | Non-Academic |
|---------|----------|--------------|
| Voice | Third person | First/second person |
| Emotion | Neutral | Expressive |
| Opinion | Evidence-based | Personal |
| Language | Precise | Colloquial |

**Examples:**
```
❌ I think this method is really great.
✓ The proposed method demonstrates superior performance (Table 3).

❌ This is obviously the best approach.
✓ This approach achieves state-of-the-art results on three benchmarks.
```

### 2. Precision

Use precise, unambiguous language:

```
❌ The model works well.
✓ The model achieves 94.2% accuracy on the test set.

❌ We used a lot of data.
✓ We used 1.2M training examples from the ImageNet dataset.

❌ Results were pretty good.
✓ Results show a 12.3% improvement over the baseline (p < 0.01).
```

### 3. Hedging

Academic writing often uses hedging to indicate uncertainty:

| Hedge Type | Examples |
|------------|----------|
| Probability | likely, probably, possibly |
| Frequency | often, frequently, sometimes |
| Quantity | approximately, roughly, about |
| Conditionality | may, might, could, would |

**Appropriate Hedging:**
```
✓ These results suggest that the approach may generalize to other domains.
✓ The correlation is approximately linear for values below the threshold.
✓ This finding is consistent with prior work, though further investigation is warranted.
```

## Document Structure

### Title

**Characteristics:**
- Informative and specific
- Avoids abbreviations
- 10-15 words typical

**Title Patterns:**

| Type | Example |
|------|---------|
| Declarative | Deep Learning Improves Protein Structure Prediction |
| Question | Can Transformers Replace CNNs for Image Recognition? |
| Descriptive | A Study of Attention Mechanisms in Neural Networks |
| Method-Centric | EfficientNet: Rethinking Model Scaling |

### Abstract Structure

Follow the "hourglass" model:

```
Broad context (1-2 sentences)
        ↓
Specific problem (1-2 sentences)
        ↓
Method/approach (2-3 sentences)
        ↓
Key results (2-3 sentences)
        ↓
Implications (1-2 sentences)
```

**Checklist:**
- [ ] Self-contained (no citations)
- [ ] No undefined abbreviations
- [ ] Contains key results with numbers
- [ ] Under word limit (typically 150-300 words)

### Introduction Structure (Inverted Triangle)

```
General Topic
     │
     ↓
Specific Problem Area
     │
     ↓
Research Gap
     │
     ↓
Your Contribution
```

**Required Elements:**
1. **Hook:** Why should readers care?
2. **Background:** Essential context
3. **Problem:** What is unknown/unresolved?
4. **Gap:** What is missing in prior work?
5. **Contribution:** What did you do?
6. **Preview:** What follows?

### Body Organization

**Standard Sections:**

| Section | Purpose | Typical Length |
|---------|---------|----------------|
| Methods | How was it done? | 20-30% |
| Results | What was found? | 25-35% |
| Discussion | What does it mean? | 20-30% |

**Paragraph Structure (CLAIM):**
- **C**laim: Topic sentence
- **L**ead: Explanation
- **A**rgument: Evidence
- **I**nterpretation: Analysis
- **M**ake connection: Transition

### Conclusion Structure

1. Restate main contribution
2. Summarize key findings
3. Discuss limitations
4. Suggest future work
5. Broader impact (optional)

## Style Guidelines

### Sentence Construction

**Length:**
- Average 15-25 words
- Vary for rhythm
- Break sentences >35 words

**Active vs Passive Voice:**

| Situation | Preferred Voice |
|-----------|-----------------|
| Methods | Passive (common) or Active |
| Results | Active preferred |
| Attribution | Active |

```
✓ We trained the model for 100 epochs. (Active)
✓ The model was trained for 100 epochs. (Passive)
✓ Smith et al. (2020) proposed this architecture. (Active)
```

**Parallel Structure:**
```
❌ The method is efficient, accurate, and has good scalability.
✓ The method is efficient, accurate, and scalable.
```

### Paragraph Development

**Unity:** One main idea per paragraph
**Coherence:** Logical flow between sentences
**Development:** Sufficient detail and evidence

**Transitions:**

| Purpose | Transition Words |
|---------|------------------|
| Addition | furthermore, moreover, additionally |
| Contrast | however, nevertheless, conversely |
| Cause | therefore, consequently, thus |
| Example | for instance, specifically, notably |
| Sequence | first, second, subsequently |

### Tense Usage

| Section | Tense | Example |
|---------|-------|---------|
| Abstract (findings) | Present | We show that... |
| Introduction (background) | Present | CNNs are widely used... |
| Introduction (prior work) | Present/Past | Smith (2020) proposes... / Smith (2020) proposed... |
| Methods | Past | We collected data... |
| Results | Past | The model achieved... |
| Discussion (interpretation) | Present | This suggests... |
| Conclusion | Present | We conclude that... |

## Academic Vocabulary

### Reporting Verbs

**Neutral:**
- states, notes, observes, reports, describes

**Strong Agreement:**
- demonstrates, proves, establishes, confirms

**Weak Agreement:**
- suggests, indicates, implies, points to

**Disagreement:**
- challenges, contradicts, disputes, questions

### Noun Phrases

Academic writing uses complex noun phrases:

```
Simple: the method
Expanded: the proposed method for image classification
Complex: the novel attention-based method proposed in this work for multi-label image classification
```

**Warning:** Avoid over-nominalization that obscures meaning.

### Signaling Words

| Function | Words |
|----------|-------|
| Importance | notably, significantly, importantly |
| Clarification | specifically, in other words, that is |
| Emphasis | indeed, in fact, crucially |
| Concession | admittedly, granted, while it is true |

## Common Problems and Solutions

### Wordiness

```
❌ In order to achieve better results, we made the decision to...
✓ To improve results, we...
```

### Redundancy

```
❌ The results were surprising and unexpected.
✓ The results were unexpected.
```

### Vague Language

```
❌ There are many factors that affect performance.
✓ Three primary factors affect performance: learning rate, batch size, and model depth.
```

### Anthropomorphism

```
❌ The algorithm knows when to stop.
✓ The algorithm terminates when the convergence criterion is met.
```

### Informal Language

| Informal | Formal |
|----------|--------|
| a lot of | numerous, substantial |
| big | substantial, significant |
| get | obtain, acquire |
| look into | investigate |
| thing | factor, element, aspect |

## Citation Integration

### Quoting

**Short quotes (<40 words):**
```
As Smith (2020) argues, "deep learning has fundamentally changed
natural language processing" (p. 15).
```

**Long quotes (≥40 words):**
```
Smith (2020) elaborates:

    Deep learning has fundamentally changed natural language processing.
    The introduction of transformer architectures enabled unprecedented
    improvements in machine translation, summarization, and question
    answering. (p. 15)
```

### Paraphrasing

```
❌ Deep learning has completely transformed NLP (Smith, 2020).
✓ The field of NLP experienced a paradigm shift with the adoption of
deep learning methods (Smith, 2020).
```

### Synthesizing Multiple Sources

```
Several studies have demonstrated the effectiveness of attention
mechanisms (Vaswani et al., 2017; Devlin et al., 2019; Brown et al., 2020).
However, recent work questions their necessity for certain tasks
(Merrill et al., 2022; Tay et al., 2023).
```

## Formatting Conventions

### Numbers

| Rule | Example |
|------|---------|
| 0-9 as words | three experiments, five datasets |
| 10+ as numerals | 15 participants, 100 epochs |
| Start sentence with words | Twenty participants completed... |
| Units always numerals | 3 ms, 5 MB |
| Statistics always numerals | p < .05, r = .67 |

### Abbreviations

```
First use: convolutional neural network (CNN)
Subsequent: CNN

Standard abbreviations (no definition needed):
- AI, ML, NLP, API, URL
- etc., e.g., i.e., vs.
```

### Lists

**Run-in list:**
```
The three main contributions are: (1) a novel architecture,
(2) improved efficiency, and (3) extensive evaluation.
```

**Vertical list:**
```
The main contributions are:
1. A novel architecture that...
2. Improved training efficiency that...
3. Extensive evaluation across...
```

## Quality Checklist

### Before Submission

- [ ] Title is informative and concise
- [ ] Abstract is self-contained
- [ ] Introduction has clear motivation and contribution
- [ ] Methods are reproducible
- [ ] Results are clearly presented
- [ ] Discussion addresses limitations
- [ ] Conclusion summarizes contributions
- [ ] All claims are supported by evidence
- [ ] Citations are complete and correct
- [ ] Language is precise and objective
- [ ] Transitions provide logical flow
- [ ] Formatting follows guidelines

## References

- Strunk, W., & White, E. B. (2000). The Elements of Style
- Williams, J. M., & Bizup, J. (2016). Style: Lessons in Clarity and Grace
- Day, R. A., & Gastel, B. (2016). How to Write and Publish a Scientific Paper