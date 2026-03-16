# Academic Writing Style Guidelines

## Table of Contents

- Voice: Active vs Passive
- Tense Usage by Section
- Conciseness and Clarity
- Hedging and Confidence Language
- Citation Integration
- Word Choice Guidelines
- Sentence Structure
- Common Style Issues

## Voice: Active vs Passive

### When to Use Active Voice

Active voice is generally preferred for:
- Contribution statements
- Describing your actions
- Making claims

**Examples**:

| Passive | Active (Preferred) |
|---------|-------------------|
| "A new method is proposed." | "We propose a new method." |
| "Experiments were conducted." | "We conducted experiments." |
| "It was observed that..." | "We observed that..." |

### When to Use Passive Voice

Passive voice is appropriate for:
- Methods section (focus on procedure, not actor)
- Established facts
- When the actor is unknown or irrelevant

**Examples**:

```markdown
The model was trained using Adam optimizer with learning rate 1e-4.
(Passive is fine here - focus is on what was done, not who did it)

Data was collected from public repositories.
(Passive is appropriate - the source matters, not the collector)
```

### Guidelines

| Section | Preferred Voice | Reason |
|---------|----------------|--------|
| Abstract | Mix | Balance between agency and conciseness |
| Introduction | Active | Emphasize contributions |
| Related Work | Passive/Mixed | Focus on the work, not authors |
| Methods | Passive/Mixed | Focus on procedures |
| Results | Active/Mixed | "We observe/find/show" |
| Discussion | Active | Interpretation requires agency |
| Conclusion | Active | Restate contributions |

## Tense Usage by Section

### General Rules

| Section | Tense | Example |
|---------|-------|---------|
| Abstract | Present/Past | "We propose... We evaluated..." |
| Introduction | Present | "LLMs are widely used... Prior work shows..." |
| Related Work | Present/Present Perfect | "Smith et al. propose... Recent work has shown..." |
| Methods | Past | "We used... The model was trained..." |
| Results | Past | "We found... The model achieved..." |
| Discussion | Present | "This suggests... Our findings indicate..." |
| Conclusion | Present | "We propose... Future work includes..." |

### Detailed Section Guidance

#### Introduction (Present Tense)

```markdown
CORRECT: Large language models ARE transforming NLP.
CORRECT: Recent work SHOWS that attention is efficient.
INCORRECT: Recent work SHOWED that attention was efficient.
```

#### Methods (Past Tense)

```markdown
CORRECT: We USED the Adam optimizer.
CORRECT: The model WAS trained for 100 epochs.
INCORRECT: We USE the Adam optimizer.
INCORRECT: The model IS trained for 100 epochs.
```

**Exception**: Established facts remain present tense:
```markdown
The Adam optimizer [Kingma & Ba, 2015] combines momentum with
adaptive learning rates.
```

#### Results (Past Tense)

```markdown
CORRECT: Table 2 SHOWS the results. Our method ACHIEVED 92.3% accuracy.
CORRECT: We OBSERVED consistent improvements across datasets.
INCORRECT: Table 2 SHOWED the results.
```

**Note**: When referring to tables/figures in the paper, use present tense:
```markdown
CORRECT: Table 2 SHOWS the results.
```

#### Discussion (Present Tense)

```markdown
CORRECT: These results SUGGEST that our approach is effective.
CORRECT: Our findings INDICATE a strong correlation.
INCORRECT: These results SUGGESTED that our approach was effective.
```

### Tense with Citations

| Citation Context | Tense | Example |
|-----------------|-------|---------|
| Describing the paper itself | Present | "Smith et al. [1] propose a novel method." |
| Describing their findings | Present | "Their method achieves 95% accuracy." |
| Describing historical contribution | Present Perfect | "Smith et al. have pioneered this approach." |

## Conciseness and Clarity

### Eliminate Wordiness

| Wordy | Concise |
|-------|---------|
| "In order to" | "to" |
| "Due to the fact that" | "because" |
| "At this point in time" | "now" |
| "In the event that" | "if" |
| "A large number of" | "many" |
| "The majority of" | "most" |
| "It is possible that" | "may" |
| "Has the ability to" | "can" |
| "In close proximity to" | "near" |
| "On a daily basis" | "daily" |

### Avoid Redundancy

| Redundant | Correct |
|-----------|---------|
| "past history" | "history" |
| "future plans" | "plans" |
| "advance planning" | "planning" |
| "basic fundamentals" | "fundamentals" |
| "completely eliminate" | "eliminate" |
| "reason why" | "reason" |
| "consensus of opinion" | "consensus" |
| "each and every" | "each" |
| "first and foremost" | "first" |

### Use Concrete Language

| Vague | Concrete |
|-------|----------|
| "significantly better" | "5.3% better (p < 0.01)" |
| "substantial improvement" | "40% faster inference" |
| "many applications" | "applications in healthcare, finance, and education" |
| "recently" | "in the past two years" |
| "some experiments" | "experiments on 5 benchmark datasets" |

### Sentence Length

- Target: 15-25 words average
- Maximum: Avoid sentences over 35 words
- Minimum: One-word sentences rarely appropriate in academic writing

**Example of overly long sentence**:
```
We propose a new method that uses a novel attention mechanism which
achieves state-of-the-art results on multiple benchmarks including
GLUE, SuperGLUE, and SQuAD, demonstrating the effectiveness of our
approach across a wide range of natural language understanding tasks.
```

**Improved**:
```
We propose a new method using a novel attention mechanism. It achieves
state-of-the-art results on GLUE, SuperGLUE, and SQuAD, demonstrating
effectiveness across diverse NLU tasks.
```

## Hedging and Confidence Language

### When to Hedge

Hedge when:
- Making claims beyond direct evidence
- Suggesting interpretations
- Discussing future implications

**Appropriate Hedging Words**:

| Hedge | Strength | Example |
|-------|----------|---------|
| "may", "might" | Weak | "This may indicate..." |
| "could" | Weak | "This could suggest..." |
| "suggests" | Moderate | "Our results suggest..." |
| "indicates" | Moderate | "The data indicates..." |
| "appears to" | Moderate | "The model appears to..." |
| "likely" | Strong | "This is likely due to..." |
| "probably" | Strong | "This probably reflects..." |

### When NOT to Hedge

Do NOT hedge when:
- Reporting direct measurements
- Stating established facts
- Describing your contributions

**Inappropriate Hedging**:

| Over-Hedged | Appropriate |
|-------------|-------------|
| "It might appear that our method somewhat achieves better results." | "Our method achieves 92.3% accuracy." |
| "We somewhat improved performance." | "We improved performance by 5.3%." |
| "Our method could possibly be useful." | "Our method is applicable to [specific domains]." |

### Hedging by Section

| Section | Hedging Level | Reason |
|---------|--------------|--------|
| Introduction | Low | Confidently state contributions |
| Methods | None | Describe procedures factually |
| Results | Low | Report findings factually |
| Discussion | Moderate | Interpret findings carefully |

## Citation Integration

### Citation Types

#### 1. Supportive Citations

Support a claim with prior evidence.

```markdown
Recent work has shown that pre-training improves downstream
performance [1, 2, 3].
```

**Format**: Claim + [citations]

#### 2. Contrastive Citations

Highlight differences from prior work.

```markdown
While Smith et al. [1] achieve 85% accuracy, their approach requires
substantial computational resources.
```

**Format**: "While [author] [cite] [claim], [limitation]"

#### 3. Attribution Citations

Credit the originator of an idea or method.

```markdown
The transformer architecture was introduced by Vaswani et al. [1].
```

**Format**: "[Method/idea] was [introduced/proposed] by [author] [cite]."

#### 4. Method Citations

Reference implementation details.

```markdown
We use the Adam optimizer [1] with default hyperparameters.
```

**Format**: "We use [method] [cite]..."

### Citation Placement

| Placement | Example | Use Case |
|-----------|---------|----------|
| End of claim | "...shown in prior work [1]." | Default position |
| After author name | "Smith et al. [1] showed..." | When emphasizing author |
| Multiple citations | "...improved results [1, 2, 3]." | Multiple supporting works |
| Narrative | "Smith et al. [1] and Jones [2] both..." | Discussing multiple works |

### Citation Density

| Section | Typical Density |
|---------|----------------|
| Introduction | 1-2 per paragraph |
| Related Work | 3-5 per paragraph |
| Methods | 1-3 per paragraph (for existing methods) |
| Results | 0-1 per paragraph (for baselines) |
| Discussion | 1-2 per paragraph |

### Citation Quality

| Source Type | Quality | When to Use |
|-------------|---------|-------------|
| Peer-reviewed journal/conference | Highest | Default choice |
| arXiv preprint | Good | For very recent work |
| Workshop paper | Moderate | When no better source |
| Blog post | Low | Only for non-academic claims |
| Wikipedia | Avoid | Find primary source instead |

### Primary vs Secondary Sources

**Primary**: The original source of a claim or method
**Secondary**: A paper that cites the primary source

**Rule**: Always cite primary sources when possible.

```markdown
INCORRECT: Transformers use self-attention [Smith 2023].
CORRECT: Transformers use self-attention [Vaswani et al. 2017].
```

### Self-Citation Guidelines

**Appropriate self-citation**:
- Your prior work is directly relevant
- Building on your previous methods
- Comparing to your own baselines

**Excessive self-citation warning signs**:
- More than 15-20% self-citations
- Citing tangentially related work
- Citing to inflate citation counts

**Best practice**: 5-10% self-citations is typical and appropriate.

## Word Choice Guidelines

### Technical Terms

| Informal | Formal |
|----------|--------|
| "use" | "employ", "utilize" |
| "try" | "attempt", "investigate" |
| "big" | "large-scale", "substantial" |
| "good" | "effective", "performant" |
| "bad" | "suboptimal", "limited" |
| "show" | "demonstrate", "illustrate" |
| "look at" | "examine", "investigate" |
| "figure out" | "determine", "identify" |

### Avoid AI-Typical Phrases

These phrases often signal AI-generated content:

| AI Phrase | Natural Alternative |
|-----------|-------------------|
| "delve into" | "examine", "investigate" |
| "pivotal" | "key", "critical" |
| "crucial" | "important" |
| "paramount" | "most important" |
| "It is worth noting that" | Remove entirely |
| "In order to" | "to" |
| "plays a vital role" | "is important" |
| "underscores" | "demonstrates", "highlights" |
| "tapestry" | Remove metaphor |
| "landscape" | "field" (when overused) |
| "robust" | Use only with empirical validation |
| "seamless" | "integrated" |
| "leverage" | "use" (when "use" works) |

### Preferred Terms in ML/AI

| Less Preferred | Preferred |
|---------------|-----------|
| "our algorithm" | "our method" / "our approach" |
| "the data" | "the dataset" (when specific) |
| "training the model" | "training" (when clear) |
| "the model learns" | "the model captures" (models don't "learn" like humans) |

## Sentence Structure

### Parallel Structure

Maintain parallel structure in lists and comparisons.

```markdown
CORRECT: We evaluate accuracy, efficiency, and robustness.
INCORRECT: We evaluate accuracy, how efficient it is, and robustness.

CORRECT: The model achieves high accuracy, runs efficiently, and
generalizes well.
INCORRECT: The model achieves high accuracy, is efficient to run,
and generalizes well.
```

### Avoiding Dangling Modifiers

```markdown
INCORRECT: Using this approach, the results improved significantly.
(WHO used the approach?)

CORRECT: Using this approach, we improved results significantly.

CORRECT: By using this approach, results improved significantly.
```

### Subject-Verb Agreement

```markdown
INCORRECT: The list of experiments are shown in Table 1.
(subject: "list", not "experiments")

CORRECT: The list of experiments is shown in Table 1.
```

### Common Grammar Issues

| Incorrect | Correct | Rule |
|-----------|---------|------|
| "The data shows" | "The data show" | "Data" is plural |
| "The criteria is" | "The criteria are" | "Criteria" is plural |
| "Less experiments" | "Fewer experiments" | Countable vs uncountable |
| "Amount of samples" | "Number of samples" | Countable vs uncountable |

## Common Style Issues

### Overuse of "Respectively"

```markdown
INCORRECT: We evaluate on datasets A and B, achieving 90% and 85%
accuracy, respectively.
(redundant - order is clear)

CORRECT: We evaluate on datasets A and B, achieving 90% and 85%
accuracy.
```

Use "respectively" only when order might be ambiguous:
```markdown
CORRECT: Models A and B achieve 90% and 85% F1 score on dataset X
and 88% and 82% on dataset Y, respectively.
```

### Starting Sentences with Numbers

```markdown
INCORRECT: 100 samples were collected.
CORRECT: We collected 100 samples.
CORRECT: One hundred samples were collected.
```

### Excessive Acronym Use

```markdown
INCORRECT: We use LSTM, GRU, and BiRNN with BPE tokenization on
WMT14 EN-DE with BLEU evaluation.
TOO MANY ACRONYMS

CORRECT: We use long short-term memory (LSTM) networks with byte-pair
encoding (BPE) tokenization on the WMT14 English-German dataset,
evaluated using BLEU score.
```

**Guideline**: Define acronyms on first use, then use consistently.

### "That" vs "Which"

- "That" introduces essential clauses (no commas)
- "Which" introduces non-essential clauses (with commas)

```markdown
ESSENTIAL: The model that we trained achieved 92% accuracy.
(Identifies which model - essential info)

NON-ESSENTIAL: Our model, which was trained on 1M examples,
achieved 92% accuracy.
(Additional info - not essential to identify the model)
```

## Style Checklist

Before submission, verify:

- [ ] Active voice used for contributions
- [ ] Consistent tense per section
- [ ] No AI-typical phrases ("delve", "pivotal", etc.)
- [ ] Concrete quantitative claims (not vague "significant")
- [ ] Primary sources cited
- [ ] No excessive hedging
- [ ] Parallel structure maintained
- [ ] No dangling modifiers
- [ ] Subject-verb agreement correct
- [ ] Acronyms defined on first use