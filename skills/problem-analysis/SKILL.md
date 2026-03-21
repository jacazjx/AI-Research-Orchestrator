---
name: airesearchorchestrator:problem-analysis
agent: coder
description: Unified problem definition, decomposition analysis, and significance validation skill. Covers transforming loose research concepts into well-defined hypotheses, decomposing problems into sub-problems, validating problem existence and significance, and assessing feasibility. The agent decides which aspects to focus on based on current phase and context. Use when user says "define idea", "analyze problem", "validate problem", "formulate hypothesis", "明确研究想法", "问题分析", "问题验证", or needs any level of problem work.
user-invocable: false
argument-hint: [research-topic-or-problem-statement]
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(curl), WebFetch
---
# Problem Analysis

## Overview

A unified skill that covers the full spectrum of problem work: defining and structuring research ideas, decomposing problems into manageable components, validating problem existence and significance, and assessing feasibility. The agent adapts its focus based on the current phase and what the deliverable needs.

## Purpose

- Transform loose research concepts into well-defined, testable hypotheses
- Decompose complex research problems into sub-problems with dependencies
- Validate that problems truly exist, are significant, and haven't been solved
- Assess technical, resource, and timeline feasibility
- Produce deliverables that support quality gate evaluation

## When to Focus on What

| Context | Primary Focus |
|---------|---------------|
| Starting a new project, idea is unstructured | Problem Definition (Step 1) |
| Idea is defined but needs detailed breakdown | Decomposition Analysis (Step 2) |
| Need to verify problem is worth pursuing | Significance Validation (Step 3) |
| Preparing for pilot phase | All three steps, ending with feasibility |
| Reviewing an existing problem statement | Validation only (Step 3) |

---

## Step 1: Problem Definition

Transform a loose research concept into a well-defined hypothesis.

### 1.1 Gather Context

Read existing materials:
- Project description and research intent clarification
- Any existing literature notes
- Researcher's domain expertise and constraints

### 1.2 Define Problem Statement

Structure as:
- **Background and motivation**: Why does this problem matter?
- **Specific problem**: What exactly needs to be solved?
- **Significance**: What's the impact of a solution?
- **Scope and boundaries**: What's in and out of scope?

### 1.3 Formulate Hypothesis

Create a testable hypothesis with:
- Clear independent variables
- Expected relationships
- Measurable outcomes
- Falsifiability criteria

### 1.4 Propose Approach

Outline:
- High-level methodology
- Key technical components
- Required resources
- Risk assessment

### 1.5 Define Contributions

List expected contributions:
- Novel algorithms/methods
- Theoretical insights
- Empirical findings
- Practical applications

### Problem Definition Output

Save to `docs/survey/idea-definition.md`:

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

## Risk Assessment
- Technical risks and mitigations
- Resource constraints
- Alternative approaches

## Success Criteria
[Measurable outcomes that would validate the hypothesis]
```

---

## Step 2: Decomposition Analysis

Break down the problem into manageable components.

### 2.1 Problem Decomposition

- **Core challenge identification**: The fundamental problem being addressed
- **Sub-problems**: All component problems with dependencies mapped
- **Assumptions**: What is being taken as given?
- **Boundary conditions**: Where does the approach apply and not apply?

### 2.2 Technical Challenge Analysis

For each sub-problem:
- Why is it hard?
- What approaches exist and their limitations?
- What makes our approach different?

Must identify at least 3 technical challenges.

### 2.3 Solution Approach Design

- High-level architecture
- Key algorithms/components
- Data flow
- Integration points

The solution approach must address ALL identified challenges.

### 2.4 Feasibility Assessment

| Aspect | Assessment | Notes |
|--------|------------|-------|
| Technical | Ready/Blocked | Can it be done with current technology? |
| Resources | Available/Needed | Compute, data, time available? |
| Timeline | Realistic/Tight | Can it be completed in time? |

### 2.5 Success Metrics

| Metric | Target | Baseline |
|--------|--------|----------|
| [Primary metric] | [Target value] | [Current best] |
| [Secondary metric] | [Target value] | [Current best] |

### Decomposition Output

Save to `docs/pilot/problem-analysis.md`:

```markdown
# Problem Analysis

## Problem Decomposition

### Core Challenge
[The fundamental problem]

### Sub-problems
1. [Sub-problem 1]
   - Dependencies: ...
   - Complexity: Low/Medium/High
2. [Sub-problem 2]
   ...

### Assumptions
- [Assumption 1]

## Technical Challenges

| Challenge | Difficulty | Existing Solutions | Our Approach |
|-----------|------------|-------------------|--------------|
| [Challenge] | [Rating] | [What exists] | [Our approach] |

## Solution Approach

### Architecture
[High-level design]

### Key Components
1. [Component]: [Purpose and implementation sketch]

### Data Flow
[How data moves through the system]

## Feasibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Technical | Ready/Blocked | ... |
| Resources | Available/Needed | ... |
| Timeline | Realistic/Tight | ... |

## Success Metrics

| Metric | Target | Baseline |
|--------|--------|----------|
| ... | ... | ... |

## Next Steps
[What needs to happen before pilot implementation]
```

---

## Step 3: Significance Validation

Validate that the research problem truly exists and is worth investigating.

### 3.1 Problem Insight Analysis

#### Origin Analysis
- **Literature Gap**: Discovered through literature review
- **Practical Need**: Observed in real-world applications
- **Theoretical Question**: Arising from theoretical considerations
- **Industry Demand**: Driven by industry requirements

#### Motivation Assessment
- Academic importance, practical impact, social value, economic relevance

#### Scope Definition
- Boundary conditions, constraints, explicit exclusions

#### Stakeholder Identification
- Primary beneficiaries, secondary affected parties, potential skeptics

### 3.2 Evidence Gathering

Collect evidence from at least 2 different source types:

**Literature Evidence**: Existing discussions, papers that mention but don't solve, surveys highlighting as open challenge, recent CFPs.

**Data Evidence** (if applicable): Dataset patterns, performance gaps in benchmarks, failure modes, error logs.

**Practical Evidence**: Industry reports, forum discussions, GitHub issues, expert consultations.

### 3.3 Significance Assessment

| Dimension | Criteria | Score (1-5) |
|-----------|----------|-------------|
| Academic | Novelty, theoretical contribution | 5 = groundbreaking, 1 = incremental |
| Practical | Real-world impact, adoption potential | 5 = critical need, 1 = nice-to-have |
| Timeliness | Current relevance, trending interest | 5 = urgent, 1 = outdated |
| Feasibility | Within current technical capabilities | 5 = achievable, 1 = speculative |

**Decision thresholds**:

| Total Score | Recommended Action |
|-------------|-------------------|
| 16-20 | Validated -- proceed confidently |
| 12-15 | Validated -- proceed with caution |
| 8-11 | Reformulate -- refine problem statement |
| 4-7 | Defer/Pivot -- consider alternatives |

### 3.4 Gap Analysis

1. **Previous Attempts**: What has been tried?
2. **Why They Fell Short**: Limitations of existing approaches
3. **The Gap**: What remains unsolved?
4. **Our Angle**: How will we approach it differently?

### 3.5 Validation Verdict

| Verdict | Meaning | Next Step |
|---------|---------|-----------|
| **Validated** | Problem is real, significant, research-worthy | Proceed to analysis/pilot |
| **Reformulate** | Problem exists but needs refinement | Revise problem statement, re-validate |
| **Defer** | Valid but not currently feasible | Document blockers, revisit conditions |
| **Pivot** | Not worth pursuing as stated | Explore related alternatives |

### Validation Output

Save to `docs/pilot/problem-validation-report.md`:

```markdown
# Problem Validation Report

## Problem Statement
[Clear, concise statement]

## Problem Insight Analysis

### Origin
- **Source**: [Literature/Practical/Theoretical/Industry]
- **Discovery Context**: [How identified]

### Motivation
| Stakeholder | Why They Care | Impact Level |
|-------------|---------------|--------------|
| [Group] | [Reason] | High/Medium/Low |

### Scope
- **Boundaries**: [Where applicable]
- **Constraints**: [Limitations]
- **Exclusions**: [Out of scope]

## Evidence Summary

### Literature Evidence
| Source | What It Shows | Relevance |
|--------|---------------|-----------|
| [Citation] | [Finding] | [Support] |

### Data Evidence
| Source | Finding | Implication |
|--------|---------|-------------|
| [Source] | [Observation] | [Suggestion] |

### Practical Evidence
| Type | Finding | Source |
|------|---------|--------|
| [Type] | [Finding] | [Link] |

## Significance Assessment

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Academic | X/5 | [Why] |
| Practical | X/5 | [Why] |
| Timeliness | X/5 | [Why] |
| Feasibility | X/5 | [Why] |
| **Total** | **XX/20** | |

## Gap Analysis

### Previous Attempts
1. [Approach]: [What tried, limitations]

### The Gap
[What remains unsolved]

### Our Angle
[How we approach differently]

## Validation Verdict

**Status**: [Validated / Reformulate / Defer / Pivot]

### Rationale
[Clear justification]

## Next Steps
- [ ] [Action item 1]
- [ ] [Action item 2]
```

---

## Integration with Pilot Phase

This skill provides the first substeps of the Pilot phase:

```
Pilot Phase:
1. problem_validation (Step 3) <-- ENTRY POINT
2. problem_analysis (Step 2)
3. pilot_design
4. pilot_execution
```

If validation fails (Reformulate/Defer/Pivot), do NOT proceed to decomposition analysis.

## Key Rules

1. **Hypothesis must be testable and falsifiable**
2. **Problem statement must be specific, not vague**
3. **Contributions must be differentiated from existing work**
4. **Include at least one "what if this fails" contingency**
5. **Must identify at least 3 technical challenges** in decomposition
6. **Solution approach must address ALL identified challenges**
7. **Feasibility must be an honest assessment** -- not optimistic handwaving
8. **Must gather evidence from at least 2 different source types** for validation
9. **Significance scores must be justified** with specific evidence
10. **Verdict must be supported by the analysis**, not personal preference
11. **If verdict is not "Validated"**, must provide a clear path forward
12. **This is a gate**: problem analysis cannot proceed without validation
