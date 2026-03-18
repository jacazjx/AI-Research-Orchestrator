---
name: airesearchorchestrator:paper-writing-guide
description: Comprehensive manuscript writing guide covering paragraph structure, transitions, common mistakes, and peer review criteria. Use as reference for writing high-quality academic manuscripts.
argument-hint: [section-type]
allowed-tools: Read, Grep, Glob
---

## Purpose

Provide comprehensive guidance for academic manuscript writing, including paragraph structure, transition phrases, common mistakes to avoid, and peer review criteria awareness. Use this skill as a reference during paper writing.

## Paragraph Structure

### The Topic Sentence

Every paragraph should begin with a clear topic sentence that:
- States the main point of the paragraph
- Connects to the previous paragraph (via transition)
- Sets expectations for what follows

**Example - Good**:
```
Recent advances in transformer architectures have significantly improved
performance on natural language understanding tasks.
```

**Example - Poor** (no clear topic):
```
There are many approaches to NLP. Some use transformers. Others use
RNNs. The field has changed a lot.
```

### The MEAL Plan

Structure paragraphs using MEAL:

| Component | Purpose | Example |
|-----------|---------|---------|
| **M**ain Idea | Topic sentence | "Our approach improves efficiency through a novel caching mechanism." |
| **E**vidence | Supporting data or citation | "Experiments show 40% speedup (Table 3)." |
| **A**nalysis | Interpretation | "This improvement stems from reduced redundant computation." |
| **L**ink | Connect to next paragraph | "Having established efficiency gains, we now examine accuracy." |

### Paragraph Length Guidelines

| Context | Recommended Length |
|---------|-------------------|
| Introduction | 4-8 sentences |
| Methods | 4-6 sentences typical |
| Results | 3-5 sentences per finding |
| Discussion | 5-8 sentences |

**Warning Signs**:
- Single-sentence paragraphs (usually need merging)
- Paragraphs over 10 sentences (consider splitting)
- Paragraphs without clear topic sentence

## Transition Phrases and Signposting

### Types of Transitions

#### 1. Additive Transitions (Adding Information)

| Phrase | Usage |
|--------|-------|
| Additionally | Formal addition |
| Furthermore | Builds on previous point |
| Moreover | Emphasizes addition |
| Similarly | Parallel point |
| Likewise | Similar to previous |
| In the same vein | Academic parallel |

**Example**:
```
Our method improves accuracy on dataset A. Similarly, on dataset B,
we observe a 5% improvement over baselines.
```

#### 2. Adversative Transitions (Contrast)

| Phrase | Usage |
|--------|-------|
| However | Direct contrast |
| Nevertheless | Despite previous |
| In contrast | Highlighting difference |
| Conversely | Opposite relationship |
| On the other hand | Alternative perspective |
| Despite this | Acknowledging limitation |

**Example**:
```
Prior work focuses on accuracy. However, our approach also considers
computational efficiency.
```

#### 3. Causal Transitions (Cause-Effect)

| Phrase | Usage |
|--------|-------|
| Therefore | Logical consequence |
| Consequently | Result of previous |
| As a result | Outcome |
| Thus | Summary/conclusion |
| Hence | Deduction |
| For this reason | Explanation |

**Example**:
```
The model struggles with rare classes. Consequently, we employ
class-balanced sampling during training.
```

#### 4. Sequential Transitions (Order)

| Phrase | Usage |
|--------|-------|
| First, Second, Third | Explicit ordering |
| Initially | Beginning of process |
| Subsequently | Following step |
| Finally | Last item |
| Next | Immediate next |

**Example**:
```
First, we preprocess the data. Second, we extract features using
our proposed encoder. Finally, we train the classifier.
```

### Signposting

Use signposts to guide readers through complex arguments:

```markdown
This section is organized as follows. Section 3.1 describes our
model architecture. Section 3.2 presents the training procedure.
Section 3.3 provides theoretical analysis.
```

**Common Signpost Phrases**:
- "To address this, we propose..."
- "Building on this observation..."
- "As shown in Figure 3..."
- "Table 2 presents the results..."
- "We now turn to..."

## Common Mistakes to Avoid

### 1. Weak Openings

**Mistake**: Starting paragraphs with weak or filler phrases.

| Avoid | Use Instead |
|-------|-------------|
| "It is important to note that..." | Direct statement |
| "It should be mentioned that..." | State the point directly |
| "There are several reasons why..." | State the reasons directly |
| "In terms of..." | Use specific preposition |

**Example**:
```
WEAK: "It is important to note that our method achieves state-of-the-art results."
BETTER: "Our method achieves state-of-the-art results."
```

### 2. AI-Typical Language

These phrases often indicate AI-generated content. Replace with more natural alternatives:

| AI Phrase | Natural Alternative |
|-----------|-------------------|
| "delve into" | "examine", "explore" |
| "pivotal" | "key", "important" |
| "crucial" | "important", "critical" |
| "paramount" | "primary", "most important" |
| "It is worth noting that" | Remove entirely |
| "In order to" | "to" |
| "plays a vital role" | "is important" |
| "underscores" | "highlights", "emphasizes" |
| "tapestry" | Remove (overused metaphor) |
| "landscape" | "field", "area" (when overused) |

### 3. Excessive Hedging

While some hedging is appropriate in academic writing, excessive hedging weakens arguments.

| Over-Hedged | Appropriately Hedged |
|-------------|---------------------|
| "It could potentially suggest that results might possibly indicate..." | "Our results suggest that..." |
| "It seems to appear that..." | "Our analysis shows..." |
| "somewhat better" | "X% better" (quantify) |

**Appropriate Hedging**:
- "may" for speculative claims
- "suggests" for interpreted results
- "appears to" for observations
- "likely" for probable conclusions

**When NOT to Hedge**:
- Direct measurements (report exactly)
- Established facts (cite confidently)
- Your own contributions (state clearly)

### 4. Ambiguous Pronoun References

**Mistake**: Unclear what "it", "this", "they" refers to.

```
AMBIGUOUS: "The model outperforms the baseline. This demonstrates its effectiveness."
CLEAR: "The model outperforms the baseline, demonstrating the effectiveness of our approach."
```

### 5. Passive Voice Overuse

While passive voice has its place, excessive use obscures agency.

| Passive (Often Weaker) | Active (Often Clearer) |
|------------------------|----------------------|
| "Experiments were conducted..." | "We conducted experiments..." |
| "It was observed that..." | "We observed that..." |
| "The data was collected..." | "We collected data from..." |

**When Passive IS Appropriate**:
- Methods section (emphasize procedure over actor)
- When the actor is unknown or irrelevant
- To maintain focus on the object

### 6. Redundancy

| Redundant | Concise |
|-----------|---------|
| "past history" | "history" |
| "future plans" | "plans" |
| "advance planning" | "planning" |
| "completely eliminate" | "eliminate" |
| "basic fundamentals" | "fundamentals" |
| "reason why" | "reason" |

### 7. Sentence Structure Issues

**Run-on Sentences**: Break long sentences (>30 words) into shorter ones.

```
RUN-ON: "We propose a new method that uses attention mechanisms and achieves
state-of-the-art results on multiple benchmarks which demonstrates its
effectiveness and generalizability across different domains."

BETTER: "We propose a new method using attention mechanisms. It achieves
state-of-the-art results on multiple benchmarks, demonstrating effectiveness
and generalizability across different domains."
```

**Dangling Modifiers**:

```
WRONG: "Using this approach, the results improved significantly."
RIGHT: "Using this approach, we improved the results significantly."
```

## Peer Review Criteria Awareness

Understanding how reviewers evaluate papers helps write better submissions.

### Common Review Criteria

| Criterion | What Reviewers Look For |
|-----------|------------------------|
| **Novelty** | What's new? Is it significant? |
| **Soundness** | Is the methodology correct? |
| **Significance** | Does it matter? Impact? |
| **Clarity** | Is the writing clear? |
| **Reproducibility** | Can others replicate this? |
| **Comparison** | Fair baselines? Honest comparison? |

### Addressing Common Reviewer Concerns

#### Novelty Concerns

**Reviewer Question**: "How is this different from prior work?"

**How to Address**:
- Clear contribution statement in Introduction
- Explicit differentiation in Related Work
- Quantitative comparison where possible

```markdown
Our approach differs from Smith et al. [1] in three ways:
(1) We use a different attention mechanism,
(2) Our training procedure is more efficient,
(3) We handle out-of-distribution samples explicitly.
```

#### Methodology Concerns

**Reviewer Question**: "Is the evaluation methodology sound?"

**How to Address**:
- Clear hyperparameter settings
- Multiple runs with variance
- Statistical significance tests
- Ablation studies
- Baseline implementation details

#### Significance Concerns

**Reviewer Question**: "Who cares? What's the impact?"

**How to Address**:
- Motivate the problem clearly
- Show practical applications
- Quantify improvements meaningfully
- Discuss broader implications

#### Clarity Concerns

**Reviewer Question**: "I couldn't follow the method description."

**How to Address**:
- Use figures to illustrate complex concepts
- Define all notation before use
- Provide algorithm pseudocode
- Include running examples

### Self-Review Checklist

Before submission, check:

**Introduction**:
- [ ] Problem clearly motivated?
- [ ] Gap in literature identified?
- [ ] Contributions explicitly listed?

**Related Work**:
- [ ] Comprehensive coverage?
- [ ] Clear differentiation from this work?
- [ ] Recent papers included?

**Methods**:
- [ ] Reproducible with given details?
- [ ] All variables defined?
- [ ] Notation consistent?

**Experiments**:
- [ ] Fair baselines?
- [ ] Statistical significance reported?
- [ ] Ablation studies included?

**Discussion**:
- [ ] Limitations acknowledged?
- [ ] Results interpreted (not just restated)?
- [ ] Future directions outlined?

**Writing**:
- [ ] No AI-typical phrases?
- [ ] Transitions smooth?
- [ ] Consistent terminology?
- [ ] No grammatical errors?

## Section-Specific Writing Tips

### Abstract Tips

1. Write last (after all sections complete)
2. Include: context, objective, method, results, conclusion
3. No citations or undefined abbreviations
4. Match venue word limit exactly
5. Make first sentence compelling

### Introduction Tips

1. Use funnel structure (broad to specific)
2. End with clear contribution statement
3. Avoid literature review in Introduction (use Related Work)
4. Preview paper structure for long papers

### Related Work Tips

1. Organize by approach, not chronologically
2. End each subsection with gap identification
3. Be fair to prior work (don't straw-man)
4. Cite primary sources

### Methods Tips

1. Define notation upfront
2. Use consistent terminology throughout
3. Include pseudocode for algorithms
4. Explain design choices

### Results Tips

1. Present objectively, without interpretation
2. Reference all figures and tables
3. Report statistics (mean, std, significance)
4. Acknowledge limitations honestly

### Discussion Tips

1. Interpret results, don't repeat them
2. Compare with Related Work
3. Acknowledge limitations explicitly
4. Suggest concrete future directions

## Integration with Paper Writing Workflow

This guide supports:
- **paper-write**: Reference during section writing
- **audit-paper**: Quality criteria for review
- **auto-review-loop**: Self-improvement criteria

## References

- See `/home/jacazjx/Workspaces/AI-Research-Develop/AI-Research-Orchestrator/skills/paper-write/references/imrad_structure.md` for section-specific guidance
- See `/home/jacazjx/Workspaces/AI-Research-Develop/AI-Research-Orchestrator/skills/paper-write/references/academic_writing_style.md` for style guidelines
- See `/home/jacazjx/Workspaces/AI-Research-Develop/AI-Research-Orchestrator/references/paper-quality-assurance.md` for quality standards