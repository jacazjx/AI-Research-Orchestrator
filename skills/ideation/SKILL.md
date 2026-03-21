---
name: airesearchorchestrator:ideation
agent: survey
description: Unified research ideation skill covering brainstorming, structured innovation, filtering, novelty verification, and idea ranking. Uses a 5-phase innovation flow (context, divergent exploration, connection making, critical evaluation, synthesis) with integrated novelty checking. Use when user says "research ideation", "generate ideas", "check novelty", "头脑风暴", "研究构思", "新颖性检查", "find research ideas", or needs structured idea generation and verification.
user-invocable: false
argument-hint: [research-context-or-topic]
allowed-tools: Bash(curl, *), Read, Write, Edit, Grep, Glob, WebFetch, Agent, Skill, mcp__codex__codex
---
# Ideation

## Overview

A unified research ideation skill that covers the full spectrum from brainstorming through novelty verification. Combines structured creativity techniques with systematic filtering and novelty checking to produce a ranked portfolio of concrete, novel research ideas.

## Purpose

- Transform loose research concepts into concrete, novel research ideas
- Generate a wide solution space using structured creativity techniques
- Filter and rank ideas by novelty, feasibility, impact, and validation speed
- Verify novelty against existing literature before committing resources
- Produce actionable output for transition to literature survey or pilot design

## When to Use

- Starting a new research project without a clear direction
- Exploring alternative approaches to an existing problem
- Breaking through creative blocks in research design
- After brainstorming -- to verify selected ideas are novel
- When research intent clarification yields clarity score < 0.4

---

## 5-Phase Innovation Flow

### Phase 1: Understanding the Context

**Objective**: Build deep understanding of the researcher's background, goals, and constraints.

#### 1.1 Gather Context
- Researcher's domain expertise and interests
- Available resources (compute, data, time)
- Existing project materials
- Success criteria and constraints

#### 1.2 Clarify Research Intent
Ask clarifying questions one at a time:
- What problem domain are you most interested in?
- What skills and resources do you have available?
- What would "success" look like?
- Are there specific constraints (time, compute, data)?
- What approaches have you already considered?

#### 1.3 Define Problem Space
- Core research question
- Key variables and their relationships
- Known constraints and assumptions
- Adjacent fields that might offer insights

### Phase 2: Divergent Exploration

**Objective**: Generate a wide variety of potential research directions (aim for 10+ ideas before filtering).

#### Technique 1: Cross-Domain Analogies

Apply solutions from other fields:
```markdown
- Source Domain: [e.g., biology, physics, economics]
- Mechanism: [What works there and why?]
- Analogy: [How does this map to our problem?]
- Hypothesis: [What if we applied this mechanism?]
- Test: [How would we validate this?]
```

Prompts: "How does nature solve this?", "What would a physicist/economist do?", "How is this solved in a different industry?"

#### Technique 2: Assumption Reversal

Systematically challenge core assumptions:
```markdown
- Original Assumption: [What everyone assumes is true]
- Reversed: [What if the opposite were true?]
- Implications: [What would change?]
- Research Direction: [What new approach does this suggest?]
```

See `references/assumption_reversal.md` for detailed methodology.

#### Technique 3: Scale Shifting

| Scale | Question | Potential Insight |
|-------|----------|-------------------|
| Micro | What happens at the individual/atomic level? | Fine-grained mechanisms |
| Meso | What patterns emerge at the system level? | Emergent behaviors |
| Macro | What are the population-level implications? | Large-scale patterns |
| Meta | What does this look like abstracted? | Universal principles |

#### Technique 4: Constraint Removal/Addition

**Removal**: "What if compute was unlimited?", "What if we had any data?", "What if no time pressure?"

**Addition**: "What if this must run on edge devices?", "What if only 1% of data?", "What if results must be explainable?"

#### Technique 5: Interdisciplinary Fusion

```markdown
- Field A: [e.g., neuroscience] -> Key Concept: [e.g., attention]
- Field B: [e.g., information theory] -> Key Concept: [e.g., entropy]
- Fusion: [How do these combine?]
- Novel Method: [What new approach emerges?]
```

#### Technique 6: Technology Speculation

- What will be possible in 2-3 years?
- What current limitations might become obsolete?
- What emerging tools could change the game?

### Phase 3: Connection Making

**Objective**: Identify patterns and connections across generated ideas.

#### 3.1 Cluster Similar Ideas
Group by: underlying mechanism, required resources, risk profile, time to validate.

#### 3.2 Identify Themes
- Which techniques generated the most promising ideas?
- What common insights appear across approaches?
- What assumptions keep recurring?

#### 3.3 Map the Solution Space
- Axes: novelty vs. feasibility, theory vs. application
- Clusters of related ideas
- Gaps deserving more exploration

### Phase 4: Critical Evaluation and Novelty Check

**Objective**: Filter ideas through rigorous evaluation WITH integrated novelty verification.

#### 4.1 Evaluation Criteria

| Criterion | Weight | Questions |
|-----------|--------|-----------|
| **Novelty** | 25% | Is this meaningfully different from existing work? |
| **Feasibility** | 25% | Can this be done with available resources? |
| **Impact** | 20% | If successful, how important would this be? |
| **Validation Speed** | 15% | How quickly can we test the core hypothesis? |
| **Risk Profile** | 15% | What's the downside? Is it asymmetric? |

#### 4.2 Novelty Verification

For each promising idea (top 3-5), perform a systematic novelty check:

**Multi-source search**:
- Search for exact or near-exact matches in academic databases
- Check for similar approaches using Semantic Scholar, arXiv, DBLP, OpenAlex
- Look for concurrent work (last 3-6 months)
- Use academic APIs, NOT web search

**Closest work identification**:
For each similar paper found:
- Summarize its contribution
- Identify overlap with proposed idea
- Note differentiation points

**Novelty status determination**:

| Status | Meaning | Action |
|--------|---------|--------|
| CONFIRMED | No close matches found | Proceed with confidence |
| PARTIAL | Similar work exists but differentiation is clear | Sharpen the differentiators |
| NOT_NOVEL | Idea already published or very similar work exists | Pivot to alternative or find new angle |

#### 4.3 Devil's Advocate Analysis

For each promising idea:
- What's the strongest argument against this?
- Under what conditions would this fail?
- What would a skeptical reviewer say?

#### 4.4 Kill Criteria

Eliminate ideas that:
- Require unavailable resources or data
- Have been thoroughly explored (NOT_NOVEL status)
- Cannot be validated within the project timeline
- Have asymmetric downside with limited upside

### Phase 5: Synthesis and Next Steps

**Objective**: Produce actionable output and transition to literature survey or pilot.

#### 5.1 Rank and Prioritize

Output 3-5 research ideas ranked by composite score:
- Clear hypothesis statement
- Key technical approach
- Resource requirements
- Risk assessment
- Quick validation path
- Novelty status with closest papers

#### 5.2 Quick Pilot Validation (Optional)

For top 2-3 ideas, if resources allow:
- Deploy parallel quick pilots (< 2 hours each, max 3 ideas, max 8 total GPU hours)
- Collect empirical signal
- Update rankings based on pilot results

#### 5.3 Define Next Steps

For each top idea:
- Key papers to search for in literature survey
- Preliminary experiments or proofs of concept
- Open questions to resolve

#### 5.4 Handoff to Literature Survey

Prepare for the `literature` skill:
- Search terms and key concepts
- Expected related work areas
- Gaps to look for

---

## Output

Save to `docs/survey/ideation-report.md`:

```markdown
# Research Ideation Report

## Context Summary
[Researcher background, goals, constraints]

## Generated Ideas

### Idea 1: [Title]
- **Hypothesis**: [Clear testable statement]
- **Approach**: [Key technical method]
- **Novelty Status**: CONFIRMED / PARTIAL / NOT_NOVEL
- **Closest Work**: [Paper reference and differentiation]
- **Feasibility**: [Resources required]
- **Risk**: [Key risks and mitigations]
- **Validation Path**: [How to test quickly]
- **Composite Score**: X/100

### Idea 2: [Title]
...

## Novelty Verification Summary

| Idea | Status | Closest Paper | Differentiation |
|------|--------|---------------|-----------------|
| Idea 1 | CONFIRMED | [ref] | [How it differs] |
| Idea 2 | PARTIAL | [ref] | [Sharpen these] |

## Pilot Results (if applicable)

| Idea | Pilot Duration | Key Signal | Outcome |
|------|----------------|------------|---------|
| Idea 1 | X hours | [Metric] | Promising/Inconclusive/Negative |

## Synthesis

### Themes Identified
[Patterns across ideas]

### Recommended Direction
[Top choice with reasoning]

### Next Steps
1. Literature survey focus areas and search terms
2. Preliminary experiments to run
3. Open questions to resolve

## Appendix: Full Idea List
[All generated ideas, including rejected ones, for reference]
```

---

## Key Rules

1. **Generate before filtering**: Produce many ideas (10+) before evaluating any
2. **One technique at a time**: Apply each creativity technique systematically
3. **No premature criticism**: Keep divergent and convergent phases separate
4. **Document everything**: Save all ideas, even rejected ones
5. **Stay grounded**: Novelty must be meaningful, not just different
6. **Verify novelty systematically**: Use academic APIs for every promising idea
7. **Transition explicitly**: Hand off to literature survey with clear search terms
8. **Empirical signal > theoretical appeal**: Prefer ideas with quick validation paths
9. **Kill ideas early**: Don't invest in ideas that fail novelty or feasibility checks

## Common Mistakes

| Mistake | Correction |
|---------|------------|
| Evaluating too early | Complete all divergent techniques before filtering |
| Ignoring constraints | Check feasibility after each generation round |
| Too few ideas | Aim for 10+ before filtering |
| Generic ideas | Use specific techniques (analogies, reversal) |
| Skipping novelty check | Always verify top ideas against literature |
| Skipping phases | Each phase builds on the previous one |

## References

- `references/brainstorming_methods.md` - Detailed methodology for creativity techniques
- `references/assumption_reversal.md` - Assumption reversal methodology
