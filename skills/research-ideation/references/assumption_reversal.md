# Assumption Reversal Methodology

## Overview

Assumption reversal is a systematic creativity technique that generates novel research directions by identifying and challenging the core assumptions that underlie a field or problem. By asking "what if the opposite were true?", researchers can discover approaches that the field has collectively overlooked.

## Theoretical Foundation

### Why It Works

1. **Paradigm Blindness**: Fields develop shared assumptions that become invisible
2. **Normal Science**: Most work operates within existing paradigms
3. **Revolutionary Science**: Breakthroughs often come from challenging fundamentals
4. **Cognitive Inertia**: We naturally think within established frameworks

### Historical Examples

| Original Assumption | Reversal | Resulting Innovation |
|---------------------|----------|----------------------|
| Earth is the center | Sun is the center | Heliocentric model |
| Heavier-than-air flight impossible | Heavier-than-air flight is possible | Airplane |
| Computation must be sequential | Computation can be parallel | Neural networks, distributed computing |
| Learning requires labels | Learning can happen without labels | Self-supervised learning |
| More parameters need more data | Large models can generalize with few examples | Few-shot learning in LLMs |

## Methodology

### Step 1: Assumption Excavation

Identify the implicit and explicit assumptions in your field.

#### Categories of Assumptions

**1. Data Assumptions**
- What types of data are used?
- How much data is assumed necessary?
- What data quality is assumed?
- What data sources are assumed available?

**2. Method Assumptions**
- What computational approaches are standard?
- What architectures are assumed best?
- What training procedures are standard?
- What evaluation methods are assumed appropriate?

**3. Resource Assumptions**
- What compute is assumed available?
- What time constraints are assumed?
- What human resources are assumed?
- What budget constraints are assumed?

**4. Problem Assumptions**
- What problem formulation is standard?
- What constraints are assumed necessary?
- What success criteria are assumed?
- What use cases are assumed primary?

**5. Theoretical Assumptions**
- What theoretical frameworks are used?
- What mathematical tools are standard?
- What relationships are assumed?
- What principles are taken as given?

#### Excavation Prompts

```
- "Everyone in my field assumes that..."
- "The standard approach is to..."
- "We always use X for Y because..."
- "It's well-known that..."
- "The conventional wisdom is..."
- "Nobody would consider..."
- "That's just how things are done..."
```

### Step 2: Systematic Reversal

For each identified assumption, systematically consider its opposite.

#### Reversal Matrix

| Assumption Type | Original | Reversal | Exploration |
|-----------------|----------|----------|-------------|
| Quantity | More X is better | Less X could be better | What if we used 10x less? |
| Direction | X causes Y | Y causes X | What if causality reversed? |
| Relationship | X and Y are independent | X and Y are coupled | What if they're intimately linked? |
| Status | X is necessary | X is unnecessary | What if we eliminated X entirely? |
| Sequence | X must come before Y | X could come after Y | What if we reversed the order? |
| Scope | X applies universally | X is domain-specific | What if X only works in narrow cases? |
| Necessity | X is required | X is optional | What if we made X optional? |
| Sufficiency | X is enough | X is not enough | What additional factors matter? |

### Step 3: Implication Mapping

For each reversal, map out the implications.

#### Implication Framework

```markdown
## Reversal: [Original] -> [Reversed]

### What Changes?
- [Changes in the problem]
- [Changes in the solution space]
- [Changes in evaluation]

### What Becomes Possible?
- [New approaches enabled]
- [New solutions to old problems]
- [New problem formulations]

### What Becomes Impossible?
- [What no longer works]
- [What constraints emerge]
- [What trade-offs appear]

### Research Direction
- [Specific hypothesis to test]
- [Approach to explore]
- [Validation path]
```

### Step 4: Research Direction Generation

Transform reversals into concrete research directions.

#### Quality Filters

**Strong Reversals:**
- Challenge something deeply held in the field
- Open a genuinely new solution space
- Lead to testable hypotheses
- Have clear implications if true

**Weak Reversals:**
- Challenge something already known to be false
- Lead to trivial or already-explored directions
- Cannot be tested or validated
- Have no clear implications

## Detailed Examples

### Example 1: Deep Learning

**Original Assumption**: "More training data always improves model performance."

**Reversal**: "Less data could lead to better models (under specific conditions)."

**Exploration**:
- What conditions might favor less data?
  - When data quality varies
  - When irrelevant examples dominate
  - When curriculum effects matter

**Research Directions**:
1. Data quality vs. quantity trade-offs
2. Curriculum learning: strategic data ordering
3. Coreset selection: optimal subset identification
4. Active learning: strategic data acquisition

**Validation Path**: Train models on curated subsets and compare to full dataset training.

### Example 2: Neural Network Architecture

**Original Assumption**: "Deeper networks learn more complex functions."

**Reversal**: "Shallow networks could match deep networks with appropriate modifications."

**Exploration**:
- What enables shallow networks?
  - Wider layers
  - Better optimization
  - Different activation functions
  - External memory

**Research Directions**:
1. Wide networks vs. deep networks
2. Knowledge distillation to shallow networks
3. Non-deep architectures (e.g., state space models)
4. Computationally efficient shallow alternatives

**Validation Path**: Train wide shallow networks and compare to deep counterparts on standard benchmarks.

### Example 3: Machine Learning Methodology

**Original Assumption**: "Training should minimize a single loss function."

**Reversal**: "Training should optimize multiple objectives simultaneously."

**Exploration**:
- What does multi-objective training enable?
  - Better generalization
  - Robustness to distribution shift
  - Alignment with multiple constraints
  - Disentangled representations

**Research Directions**:
1. Multi-task learning architectures
2. Gradient surgery for conflicting objectives
3. Pareto-optimal training
4. Constrained optimization in ML

**Validation Path**: Train with auxiliary objectives and measure primary task performance and robustness.

### Example 4: AI Safety

**Original Assumption**: "We should align AI with human values."

**Reversal**: "We should design AI that operates without relying on value alignment."

**Exploration**:
- What if alignment is impossible or unstable?
  - Constitutional AI approaches
  - Bounded optimization
  - Corrigibility without value loading
  - Tripwires and shutdown mechanisms

**Research Directions**:
1. Mechanistic interpretability as alternative to alignment
2. Bounded optimization for safety
3. Sandboxing and containment strategies
4. Formal verification of properties

**Validation Path**: Design systems that remain safe without assuming value alignment.

## Practice Exercises

### Exercise 1: Identify Hidden Assumptions

For your research area, complete:

```markdown
1. "The standard approach in my field is to..."
   - Hidden assumption: ________

2. "Everyone agrees that..."
   - Hidden assumption: ________

3. "The problem requires..."
   - Hidden assumption: ________

4. "We can't do X because..."
   - Hidden assumption: ________
```

### Exercise 2: Generate Reversals

For each assumption above:

```markdown
## Assumption: [From Exercise 1]

**Reversal**: [The opposite]

**What if true?**:
- Implication 1: ________
- Implication 2: ________
- Implication 3: ________

**Research Direction**: ________

**Quick Test**: [How to validate in <1 week]
```

### Exercise 3: Find the Strongest Reversal

From your generated reversals:

1. Which reversal is most surprising?
2. Which has the clearest testable hypothesis?
3. Which opens the largest new solution space?
4. Which, if true, would have the biggest impact?

## Integration with Other Techniques

### With Cross-Domain Analogies

1. Find an assumption in your field
2. Reverse it
3. Ask: "Where does the reversed version already work?"
4. Import methods from that domain

### With Scale Shifting

1. Find a scale-dependent assumption
2. Reverse it for different scales
3. Generate multi-scale research directions

### With Constraint Manipulation

1. Identify constraint-related assumptions
2. Reverse the constraint relationship
3. Explore new solution spaces

## Common Pitfalls

### Pitfall 1: Reversing Truisms

**Bad**: "The sky is blue" -> "The sky is not blue"
**Better**: "Color is essential for vision" -> "Color is dispensable for vision"

### Pitfall 2: Reversing Without Exploring

**Bad**: "More data is better" -> "Less data is better" (end of thought)
**Better**: "Less data could be better when data quality varies, which suggests research into..."

### Pitfall 3: Ignoring Context

**Bad**: Applying reversals that have already been explored extensively
**Better**: Focus on assumptions that remain largely unchallenged

### Pitfall 4: Not Generating Research Directions

**Bad**: List of reversals without next steps
**Better**: Each reversal leads to specific, testable research hypotheses

## Reference Sheet

### Quick Reference: Assumption Categories

1. **Data assumptions**: Type, quantity, quality, source
2. **Method assumptions**: Architecture, training, evaluation
3. **Resource assumptions**: Compute, time, budget, expertise
4. **Problem assumptions**: Formulation, constraints, success criteria
5. **Theoretical assumptions**: Frameworks, tools, relationships, principles

### Quick Reference: Reversal Types

1. **Quantity**: More <-> Less
2. **Direction**: X causes Y <-> Y causes X
3. **Relationship**: Independent <-> Coupled
4. **Status**: Necessary <-> Unnecessary
5. **Sequence**: Before <-> After
6. **Scope**: Universal <-> Specific
7. **Necessity**: Required <-> Optional
8. **Sufficiency**: Enough <-> Not enough

### Quick Reference: Quality Criteria

Good reversals:
- Challenge deeply held beliefs
- Open new solution spaces
- Lead to testable hypotheses
- Have clear implications