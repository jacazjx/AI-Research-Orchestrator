---
name: airesearchorchestrator:define-idea
agent: survey
description: Formulate research hypothesis with clear problem statement, proposed approach, and expected contributions. Use when user says "define idea", "formulate hypothesis", "明确研究想法", or needs to structure a research concept.
argument-hint: [research-topic-or-idea]
allowed-tools: Bash(curl), Read, Write, Edit, Grep, Glob, WebFetch
---

## Purpose

Transform a loose research concept into a well-defined hypothesis with problem statement, proposed approach, and expected contributions.

## Workflow

### Step 1: Gather Context

Read existing materials:
- Project CLAUDE.md for context
- Any existing literature notes
- User's research intent clarification

### Step 2: Define Problem Statement

Structure as:
- Background and motivation
- Specific problem to address
- Why it matters (significance)
- Scope and boundaries

### Step 3: Formulate Hypothesis

Create testable hypothesis with:
- Clear independent variables
- Expected relationships
- Measurable outcomes
- Falsifiability criteria

### Step 4: Propose Approach

Outline:
- High-level methodology
- Key technical components
- Required resources
- Risk assessment

### Step 5: Define Contributions

List expected contributions:
- Novel algorithms/methods
- Theoretical insights
- Empirical findings
- Practical applications

## Output

Save to `docs/reports/survey/idea-definition.md`:

```markdown
# Idea Definition

## Problem Statement
[Background, specific problem, significance]

## Research Hypothesis
[Testable hypothesis with variables and expected outcomes]

## Proposed Approach
[High-level methodology and technical components]

## Expected Contributions
1. [Contribution 1]
2. [Contribution 2]
...

## Risk Assessment
- Technical risks and mitigations
- Resource constraints
- Alternative approaches

## Success Criteria
[Measurable outcomes that would validate the hypothesis]
```

## Key Rules

- Hypothesis must be testable and falsifiable
- Problem statement must be specific, not vague
- Contributions must be clearly differentiated from existing work
- Include at least one "what if this fails" contingency