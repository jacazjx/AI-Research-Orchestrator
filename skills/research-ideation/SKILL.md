---
name: airesearchorchestrator:research-ideation
agent: survey
description: Research ideation through 5-phase innovation flow using Cross-Domain Analogies, Assumption Reversal, Scale Shifting, and Interdisciplinary Fusion. Use when user says "research ideation", "research brainstorming", "研究构思", "generate research ideas", "explore research directions", or needs structured ideation before literature survey.
argument-hint: [research-context-or-topic]
allowed-tools: Bash(curl), Read, Write, Edit, Grep, Glob, WebFetch, Agent
---

# Research Ideation

## Purpose

Transform a loose research concept into a portfolio of concrete, novel research ideas through a structured 5-phase innovation flow. This skill operates **before** literature survey to help researchers explore the full solution space and identify promising directions that might be missed through conventional thinking.

## Hard Gate

Use this skill BEFORE `/research-lit` when:
- Starting a new research project without a clear direction
- Exploring alternative approaches to an existing problem
- Breaking through creative blocks in research design

## 5-Phase Innovation Flow

### Phase 1: Understanding the Context

**Objective**: Build deep understanding of the researcher's background, goals, and constraints.

#### Step 1.1: Gather Context

Read and understand:
- Researcher's domain expertise and interests
- Available resources (compute, data, time)
- Existing project materials if any
- Success criteria and constraints

#### Step 1.2: Clarify Research Intent

Ask clarifying questions one at a time:
- What problem domain are you most interested in?
- What skills and resources do you have available?
- What would "success" look like for this research?
- Are there specific constraints (time, compute, data access)?
- What approaches have you already considered or tried?

#### Step 1.3: Define Problem Space

Output a problem space definition:
- Core research question
- Key variables and their relationships
- Known constraints and assumptions
- Adjacent fields that might offer insights

### Phase 2: Divergent Exploration

**Objective**: Generate a wide variety of potential research directions using structured creativity techniques.

#### Technique 1: Cross-Domain Analogies

Apply solutions from other fields to the research problem:

```markdown
## Cross-Domain Analogy Template
- Source Domain: [e.g., biology, physics, economics]
- Mechanism: [What works there and why?]
- Analogy: [How does this map to our problem?]
- Hypothesis: [What if we applied this mechanism?]
- Test: [How would we validate this?]
```

Example prompts:
- "How does nature solve this problem?" (biomimicry)
- "What would a physicist/economist/psychologist do?"
- "How is this problem solved in a completely different industry?"

#### Technique 2: Assumption Reversal

Systematically challenge core assumptions:

```markdown
## Assumption Reversal Template
- Original Assumption: [What everyone assumes is true]
- Reversed: [What if the opposite were true?]
- Implications: [What would change?]
- Research Direction: [What new approach does this suggest?]
```

See [references/assumption_reversal.md](references/assumption_reversal.md) for detailed methodology.

#### Technique 3: Scale Shifting

Explore how the problem changes at different scales:

| Scale | Question | Potential Insight |
|-------|----------|-------------------|
| Micro | What happens at the individual/atomic level? | Fine-grained mechanisms |
| Meso | What patterns emerge at the group/system level? | Emergent behaviors |
| Macro | What are the population/societal implications? | Large-scale patterns |
| Meta | What does this problem look like abstracted? | Universal principles |

#### Technique 4: Constraint Removal/Addition

Systematically modify constraints:

**Constraint Removal:**
- "What if compute was unlimited?"
- "What if we had access to any data?"
- "What if there were no time pressure?"

**Constraint Addition:**
- "What if this must run on edge devices?"
- "What if we only have 1% of the data?"
- "What if results must be explainable?"

#### Technique 5: Interdisciplinary Fusion

Combine methods/theories from different fields:

```markdown
## Interdisciplinary Fusion Template
- Field A: [e.g., neuroscience] -> Key Concept: [e.g., attention mechanism]
- Field B: [e.g., information theory] -> Key Concept: [e.g., entropy]
- Fusion: [How do these concepts combine?]
- Novel Method: [What new approach emerges?]
```

#### Technique 6: Technology Speculation

Project future technological possibilities:

- What will be possible in 2-3 years?
- What assumptions about current limitations might become obsolete?
- What new tools or techniques are emerging that could change the game?

### Phase 3: Connection Making

**Objective**: Identify patterns and connections across the generated ideas.

#### Step 3.1: Cluster Similar Ideas

Group ideas by:
- Underlying mechanism
- Required resources
- Risk profile
- Time to validate

#### Step 3.2: Identify Themes

Look for recurring patterns:
- Which techniques generated the most promising ideas?
- Are there common insights across different approaches?
- What assumptions keep appearing?

#### Step 3.3: Map the Solution Space

Create a visual or structured map:
- Axes: novelty vs feasibility, theory vs application
- Clusters of related ideas
- Gaps that deserve more exploration

### Phase 4: Critical Evaluation

**Objective**: Filter ideas through a rigorous evaluation process while maintaining creative momentum.

#### Evaluation Criteria

| Criterion | Weight | Questions |
|-----------|--------|-----------|
| **Novelty** | 25% | Is this meaningfully different from existing work? |
| **Feasibility** | 25% | Can this be done with available resources? |
| **Impact** | 20% | If successful, how important would this be? |
| **Validation Speed** | 15% | How quickly can we test the core hypothesis? |
| **Risk Profile** | 15% | What's the downside? Is it asymmetric? |

#### Devil's Advocate Analysis

For each promising idea, ask:
- What's the strongest argument against this?
- Under what conditions would this fail?
- What would a skeptical reviewer say?

#### Kill Criteria

Eliminate ideas that:
- Require unavailable resources or data
- Have been thoroughly explored in existing literature
- Cannot be validated within the project timeline
- Have asymmetric downside with limited upside

### Phase 5: Synthesis and Next Steps

**Objective**: Produce actionable output and transition to literature survey.

#### Step 5.1: Rank and Prioritize

Output a ranked list of 3-5 research ideas with:
- Clear hypothesis statement
- Key technical approach
- Resource requirements
- Risk assessment
- Quick validation path

#### Step 5.2: Define Next Steps

For each top idea, outline:
- Key papers to search for in literature survey
- Preliminary experiments or proofs of concept
- Open questions to resolve

#### Step 5.3: Handoff to Literature Survey

Prepare materials for `/research-lit`:
- Search terms and key concepts
- Expected related work areas
- Gaps to look for

## Output

Save to `docs/reports/survey/ideation-report.md`:

```markdown
# Research Ideation Report

## Context Summary
[Researcher background, goals, constraints]

## Generated Ideas

### Idea 1: [Title]
- **Hypothesis**: [Clear testable statement]
- **Approach**: [Key technical method]
- **Novelty**: [What's new]
- **Feasibility**: [Resources required]
- **Risk**: [Key risks and mitigations]
- **Validation Path**: [How to test quickly]

### Idea 2: [Title]
...

## Synthesis

### Themes Identified
[Patterns across ideas]

### Recommended Direction
[Top choice with reasoning]

### Next Steps
1. Literature survey focus areas
2. Preliminary experiments to run
3. Open questions to resolve

## Appendix: Full Idea List
[All generated ideas for reference]
```

## Key Rules

1. **Generate before filtering**: Produce many ideas before evaluating any
2. **One technique at a time**: Apply each creativity technique systematically
3. **No premature criticism**: Keep divergent and convergent phases separate
4. **Document everything**: Save all ideas, even rejected ones
5. **Stay grounded**: Novelty must be meaningful, not just different
6. **Transition explicitly**: Hand off to `/research-lit` with clear search terms

## Common Mistakes

| Mistake | Correction |
|---------|------------|
| Evaluating too early | Complete all divergent techniques before filtering |
| Ignoring constraints | Check feasibility after each idea generation round |
| Too few ideas | Aim for 10+ ideas before filtering |
| Generic ideas | Use specific techniques (analogies, reversal) |
| Skipping phases | Each phase builds on the previous one |

## References

- [references/brainstorming_methods.md](references/brainstorming_methods.md) - Detailed methodology for each creativity technique
- [references/assumption_reversal.md](references/assumption_reversal.md) - Deep dive on assumption reversal methodology