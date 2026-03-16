# Brainstorming Methods for Research Ideation

## Overview

This document provides detailed methodology for each creativity technique used in research ideation. These techniques are designed to systematically expand the solution space and generate novel research directions.

## Technique 1: Cross-Domain Analogies

### Definition

Cross-domain analogies transfer solutions, mechanisms, or insights from one field to solve problems in another. This technique leverages the fact that many problems have structural similarities across domains, even when surface features differ.

### Process

1. **Identify the core problem structure**
   - What is the fundamental challenge?
   - What makes this problem hard?
   - What are the key constraints?

2. **Search for analogous domains**
   - Where else does this structure appear?
   - What fields deal with similar constraints?
   - What industries have solved similar problems?

3. **Extract the mechanism**
   - How does the solution work in the source domain?
   - What are the key components?
   - What assumptions enable this solution?

4. **Map to target domain**
   - How does this mechanism translate?
   - What adaptations are needed?
   - What assumptions might not hold?

5. **Generate research hypothesis**
   - What if we applied this adapted mechanism?
   - What would success look like?
   - How would we test it?

### Example

**Problem**: Improving neural network robustness to adversarial attacks

**Source Domain**: Immunology
- **Mechanism**: The immune system maintains diversity (B-cell repertoire) to handle novel pathogens
- **Analogy**: Neural networks might benefit from "immune diversity" in their representations
- **Hypothesis**: Enforcing diversity in learned representations could improve robustness
- **Research Direction**: Develop a diversity-promoting regularization that mimics immune diversity

### Prompt Templates

```
- "How does [nature/physics/economics] solve [similar problem]?"
- "What would a [domain expert] do if faced with this problem?"
- "Where in the natural world do we see [constraint/phenomenon]?"
- "How is this problem solved in [completely different industry]?"
```

## Technique 2: Assumption Reversal

### Definition

Assumption reversal systematically identifies and challenges the core assumptions underlying a field or problem. By asking "what if the opposite were true?", we can discover novel research directions that others have overlooked.

### Process

See [assumption_reversal.md](assumption_reversal.md) for detailed methodology.

### Quick Reference

| Original Assumption | Reversed | Research Direction |
|---------------------|----------|-------------------|
| More data is better | What if less data could work better? | Few-shot learning, data efficiency |
| Bigger models are more capable | What if small models could be equally capable? | Model compression, efficient architectures |
| Training should be end-to-end | What if modular training could be better? | Modular networks, transfer learning |
| Humans learn from examples | What if learning from instructions is more efficient? | Instruction tuning, in-context learning |

## Technique 3: Scale Shifting

### Definition

Scale shifting explores how problems and solutions change when viewed at different scales. Many research opportunities emerge from applying methods that work at one scale to a different scale.

### Scale Dimensions

### Temporal Scale

| Scale | Focus | Example Questions |
|-------|-------|-------------------|
| Microsecond | Real-time processing | "What if this must respond in 1ms?" |
| Second | Interactive systems | "How does user behavior change response requirements?" |
| Hour | Batch processing | "What optimizations become possible with more time?" |
| Day/Week | Long-running experiments | "What longitudinal insights could emerge?" |

### Spatial/Data Scale

| Scale | Focus | Example Questions |
|-------|-------|-------------------|
| Individual | Personalization | "What if each user has a unique model?" |
| Group | Social dynamics | "How do interactions affect the system?" |
| Population | Aggregate patterns | "What statistical regularities emerge?" |
| Global | Universal patterns | "What holds across all contexts?" |

### Model Scale

| Scale | Focus | Example Questions |
|-------|-------|-------------------|
| Single neuron | Interpretability | "What does this unit compute?" |
| Layer | Feature hierarchy | "How do representations evolve?" |
| Full model | Emergent capabilities | "What behaviors emerge from scale?" |
| Ensemble | Diversity | "How do different models complement each other?" |

### Process

1. Identify the current scale of the problem
2. For each other scale, ask:
   - How does the problem change?
   - What new solutions become possible?
   - What new constraints emerge?
3. Generate hypotheses for promising scale shifts

## Technique 4: Constraint Manipulation

### Constraint Removal

Removing constraints reveals what's fundamentally possible:

| Removed Constraint | New Possibility |
|-------------------|-----------------|
| Limited compute | Full ensemble methods, massive architecture search |
| Limited data | Perfect training on all available data |
| Real-time requirements | Complex inference-time computation |
| Interpretability requirements | Black-box optimization |

### Constraint Addition

Adding constraints drives innovation:

| Added Constraint | Innovation Direction |
|-----------------|---------------------|
| Edge deployment | Model compression, quantization |
| Privacy preservation | Federated learning, differential privacy |
| Low latency | Efficient architectures, early exit |
| Explainability | Interpretable models, attention visualization |

### Process

1. List all implicit and explicit constraints
2. For each constraint:
   - Remove it: What becomes possible?
   - Strengthen it: What innovations are needed?
   - Invert it: What if the opposite constraint applied?
3. Generate research directions from each manipulation

## Technique 5: Interdisciplinary Fusion

### Definition

Interdisciplinary fusion combines concepts, methods, or theories from multiple fields to create novel approaches that neither field would develop independently.

### Common Fusion Patterns

| Field A | Field B | Successful Fusions |
|---------|---------|-------------------|
| Neuroscience | Machine Learning | Attention mechanisms, transformers |
| Physics | Deep Learning | Hamiltonian networks, equivariant architectures |
| Economics | AI | Multi-agent systems, mechanism design |
| Psychology | NLP | Theory of mind models, sentiment analysis |
| Biology | Optimization | Genetic algorithms, evolutionary strategies |
| Information Theory | ML | Information bottleneck, mutual information objectives |

### Process

1. **Identify core concepts from each field**
   - What are the fundamental building blocks?
   - What mathematical formalisms are used?

2. **Find isomorphisms**
   - Where do the concepts map to each other?
   - What's the shared structure?

3. **Design the fusion**
   - How can these concepts combine?
   - What new methods emerge?

4. **Validate the approach**
   - Does this make theoretical sense?
   - What would test this?

### Template

```markdown
## Interdisciplinary Fusion Proposal

### Source Fields
- Field A: [Name]
- Field B: [Name]

### Key Concepts
- From A: [Concept and its mathematical formulation]
- From B: [Concept and its mathematical formulation]

### Isomorphism
[How these concepts relate]

### Fusion Method
[The combined approach]

### Research Hypothesis
[What this fusion predicts or enables]

### Validation Plan
[How to test this]
```

## Technique 6: Technology Speculation

### Definition

Technology speculation projects forward to identify what will become possible as technology evolves, revealing research directions that will become relevant or that can anticipate future needs.

### Speculation Dimensions

### Hardware Evolution

| Timeline | Expected Changes | Research Implications |
|----------|-----------------|----------------------|
| 1-2 years | 2-4x compute | Scale up existing methods |
| 3-5 years | 10-100x compute | New architectures become feasible |
| 5-10 years | New paradigms | Neuromorphic, quantum, optical computing |

### Data Evolution

| Timeline | Expected Changes | Research Implications |
|----------|-----------------|----------------------|
| 1-2 years | More multimodal data | Cross-modal learning |
| 3-5 years | Synthetic data at scale | Data generation, simulation |
| 5-10 years | Universal data access | Data-efficient methods |

### Algorithm Evolution

| Timeline | Expected Changes | Research Implications |
|----------|-----------------|----------------------|
| 1-2 years | Better optimization | Faster training, better convergence |
| 3-5 years | New architectures | Beyond transformers? |
| 5-10 years | New paradigms | Embodied AI, world models |

### Process

1. Identify current technological constraints
2. Project when these constraints might relax
3. Ask: "What research would be enabled?"
4. Ask: "What research anticipates this future?"
5. Generate hypotheses for near-term validation

## Integration: Combining Techniques

The most powerful ideation comes from combining multiple techniques:

### Example Combination

1. **Cross-Domain Analogy**: Biological immune systems maintain diversity
2. **Constraint Addition**: Must work with limited compute
3. **Scale Shift**: Apply to individual models, not ensembles
4. **Result**: Efficient diversity-promoting regularization for single models

### Combination Strategies

- **Sequential**: Apply techniques one after another to refine ideas
- **Parallel**: Generate ideas with each technique, then combine
- **Iterative**: Use one technique's output as another's input

## Quality Criteria for Generated Ideas

### Strong Ideas Have:

1. **Clear hypothesis**: Testable statement about what will work
2. **Mechanistic explanation**: Why it should work, not just what to try
3. **Falsifiability**: Clear conditions under which it would fail
4. **Novel angle**: Something others haven't tried or considered
5. **Validation path**: Quick way to get initial signal

### Warning Signs:

1. **"Just try X"**: No mechanistic reasoning
2. **"Combine A and B"**: No explanation of how or why
3. **"Apply X to Y"**: No adaptation or domain-specific reasoning
4. **"It might work"**: No hypothesis about mechanism