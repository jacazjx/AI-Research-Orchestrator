---
name: airesearchorchestrator:ideation
agent: survey
description: "Research ideation: generate ideas, filter by feasibility and novelty, verify against literature. Use when user says \"research ideation\", \"generate ideas\", \"check novelty\", \"头脑风暴\", \"研究构思\", \"新颖性检查\"."
user-invocable: false
argument-hint: [research-context-or-topic]
allowed-tools: Bash(curl, *), Read, Write, Edit, Grep, Glob, WebFetch, Agent, Skill, mcp__codex__codex
---
# Ideation

## Purpose

Generate concrete, novel research ideas from a research context. Follows a three-stage pattern: generate broadly, filter rigorously, verify novelty against literature.

## Core Pattern: Generate -> Filter -> Verify

### 1. Generate

Produce many candidate ideas (aim for 10+) before evaluating any. Use whatever creativity techniques fit the problem -- cross-domain analogies, assumption reversal, constraint removal/addition, interdisciplinary fusion, scale shifting. The specific techniques matter less than producing a wide, diverse set.

### 2. Filter

Evaluate candidates against these criteria:

| Criterion | Weight | Key Question |
|-----------|--------|--------------|
| Novelty | 25% | Is this meaningfully different from existing work? |
| Feasibility | 25% | Can this be done with available resources? |
| Impact | 20% | If successful, how important would this be? |
| Validation Speed | 15% | How quickly can we test the core hypothesis? |
| Risk Profile | 15% | What is the downside? Is it asymmetric? |

Kill ideas that: require unavailable resources, cannot be validated within the project timeline, or have asymmetric downside with limited upside.

### 3. Verify Novelty

For each promising idea (top 3-5), perform a systematic novelty check:

**Multi-source search** using academic APIs (Semantic Scholar, arXiv, DBLP, OpenAlex -- NOT web search):
- Search for exact or near-exact matches
- Check for similar approaches and concurrent work (last 3-6 months)
- Identify closest existing papers and differentiation points

**Novelty status**:

| Status | Meaning | Action |
|--------|---------|--------|
| CONFIRMED | No close matches found | Proceed with confidence |
| PARTIAL | Similar work exists but differentiation is clear | Sharpen the differentiators |
| NOT_NOVEL | Already published or very similar work exists | Pivot or find new angle |

## Output

Save to `docs/survey/ideation-report.md`:

```markdown
# Research Ideation Report

## Context Summary
[Researcher background, goals, constraints]

## Top Ideas (Ranked)

### Idea 1: [Title]
- **Hypothesis**: [Clear testable statement]
- **Approach**: [Key technical method]
- **Novelty Status**: CONFIRMED / PARTIAL / NOT_NOVEL
- **Closest Work**: [Paper reference and differentiation]
- **Feasibility**: [Resources required]
- **Validation Path**: [How to test quickly]
- **Composite Score**: X/100

### Idea 2: [Title]
...

## Novelty Verification Summary

| Idea | Status | Closest Paper | Differentiation |
|------|--------|---------------|-----------------|
| ... | ... | ... | ... |

## Next Steps
1. Literature survey focus areas and search terms
2. Preliminary experiments to run
3. Open questions to resolve

## Appendix: Full Idea List
[All generated ideas, including rejected ones, for reference]
```

## Key Rules

1. **Generate before filtering** -- produce many ideas before evaluating any
2. **Use academic APIs for novelty checks** -- Semantic Scholar, arXiv, DBLP, OpenAlex (NOT web search)
3. **Empirical signal > theoretical appeal** -- prefer ideas with quick validation paths
4. **Kill ideas early** -- do not invest in ideas that fail novelty or feasibility checks
5. **Document everything** -- save all ideas including rejected ones for reference
