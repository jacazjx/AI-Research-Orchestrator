---
name: airesearchorchestrator:validate-problem
agent: code
description: Validate research problem existence and significance before committing resources. Use when user says "validate problem", "problem validation", "问题验证", or needs to verify a research problem is worth investigating.
argument-hint: [problem-statement]
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(curl), WebFetch
---

## Purpose

Validate that a research problem truly exists, is significant enough to warrant investigation, and has not already been adequately solved. This step precedes problem analysis to prevent wasted effort on non-existent or insignificant problems.

## Workflow

### Step 1: Problem Insight Analysis

Analyze the problem's origin and motivation:

#### Origin Analysis
- **Literature Gap**: Problem discovered through literature review
- **Practical Need**: Problem observed in real-world applications
- **Theoretical Question**: Problem arising from theoretical considerations
- **Industry Demand**: Problem driven by industry requirements

#### Motivation Assessment
- **Academic Importance**: Advances scientific knowledge
- **Practical Impact**: Solves real-world challenges
- **Social Value**: Benefits society or community
- **Economic Relevance**: Has commercial potential

#### Scope Definition
- **Boundary Conditions**: Where does the problem apply?
- **Constraints**: Technical, resource, or time limitations
- **Exclusions**: What is explicitly out of scope?

#### Stakeholder Identification
- **Primary**: Who directly benefits from solving this?
- **Secondary**: Who else is affected?
- **Skeptics**: Who might question the problem's validity?

### Step 2: Evidence Gathering

Collect evidence that the problem exists and matters:

#### Literature Evidence
- Search for existing discussions of the problem
- Identify papers that mention but don't solve it
- Find related surveys that highlight this as an open challenge
- Check recent conference/workshop calls for papers

#### Data Evidence (if applicable)
- Examine datasets for patterns suggesting the problem
- Look for performance gaps in benchmarks
- Identify failure modes in existing systems
- Review error logs or user feedback

#### Practical Evidence
- Industry reports mentioning the challenge
- Forum discussions (Stack Overflow, Reddit, etc.)
- GitHub issues related to the problem
- Expert consultations or interviews

### Step 3: Significance Assessment

Evaluate the problem's importance across dimensions:

| Dimension | Criteria | Scoring (1-5) |
|-----------|----------|---------------|
| Academic | Novelty, theoretical contribution potential | 5 = groundbreaking, 1 = incremental |
| Practical | Real-world impact, adoption potential | 5 = critical need, 1 = nice-to-have |
| Timeliness | Current relevance, trending interest | 5 = urgent, 1 = outdated |
| Feasibility | Within current technical capabilities | 5 = achievable, 1 = speculative |

### Step 4: Gap Analysis

Identify the precise gap this research fills:

1. **Previous Attempts**: What has been tried?
2. **Why They Fell Short**: Limitations of existing approaches
3. **The Gap**: What remains unsolved?
4. **Our Angle**: How will we approach it differently?

### Step 5: Validation Verdict

Based on the analysis, reach one of four conclusions:

#### Validated
The problem is real, significant, and research-worthy.
- Proceed to problem analysis
- Document evidence for future reference

#### Reformulate
The problem exists but needs refinement.
- What aspect needs reformulation?
- Suggested improved problem statement
- Re-validate after reformulation

#### Defer
The problem is valid but not currently feasible.
- What makes it infeasible now?
- What needs to change?
- When should we revisit?

#### Pivot
The problem is not worth pursuing as stated.
- Why is it not worth pursuing?
- Are there related problems that might be better?
- Should we abandon this research direction?

## Output

Save to `docs/reports/pilot/problem-validation-report.md`:

```markdown
# Problem Validation Report

## Problem Statement

[Clear, concise statement of the problem being validated]

## Problem Insight Analysis

### Origin
- **Source**: [Literature/Practical/Theoretical/Industry]
- **Discovery Context**: [How was this problem identified?]

### Motivation
| Stakeholder | Why They Care | Impact Level |
|-------------|---------------|--------------|
| [Group] | [Reason] | High/Medium/Low |

### Scope
- **Boundaries**: [Where the problem applies]
- **Constraints**: [Limitations]
- **Exclusions**: [What's out of scope]

## Evidence Summary

### Literature Evidence
| Source | What It Shows | Relevance |
|--------|---------------|-----------|
| [Citation] | [Finding] | [How it supports problem existence] |

### Data Evidence
| Dataset/Source | Finding | Implication |
|----------------|---------|-------------|
| [Source] | [Observation] | [What it suggests] |

### Practical Evidence
| Evidence Type | Finding | Source |
|---------------|---------|--------|
| [Industry report/Forum/GitHub] | [Finding] | [Link] |

## Significance Assessment

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Academic | X/5 | [Why this score] |
| Practical | X/5 | [Why this score] |
| Timeliness | X/5 | [Why this score] |
| Feasibility | X/5 | [Why this score] |
| **Total** | **XX/20** | |

## Gap Analysis

### Previous Attempts
1. [Approach 1]: [What was tried, limitations]
2. [Approach 2]: [What was tried, limitations]

### The Gap
[What remains unsolved that this research addresses]

### Our Angle
[How we will approach this differently]

## Validation Verdict

**Status**: [Validated / Reformulate / Defer / Pivot]

### Rationale
[Clear justification for the verdict]

### If Reformulate
- **Issue**: [What needs reformulation]
- **Suggested Statement**: [Improved problem statement]

### If Defer
- **Blocker**: [What prevents proceeding]
- **Conditions to Revisit**: [What needs to change]

### If Pivot
- **Reason**: [Why not worth pursuing]
- **Alternative Directions**: [Other problems to consider]

## Next Steps

- [ ] [Action item 1]
- [ ] [Action item 2]
- [ ] [Action item 3]

## References

1. [Reference 1]
2. [Reference 2]
```

## Key Rules

- MUST gather evidence from at least 2 different sources (literature + practical/data)
- Significance scores must be justified with specific evidence
- Verdict must be supported by the analysis, not personal preference
- If verdict is not "Validated", must provide clear path forward
- This report is a gate: problem analysis cannot proceed without validation

## Decision Thresholds

| Total Score | Recommended Action |
|-------------|-------------------|
| 16-20 | Validated - proceed confidently |
| 12-15 | Validated - proceed with caution |
| 8-11 | Reformulate - refine problem statement |
| 4-7 | Defer/Pivot - consider alternatives |

## Integration with Pilot Phase

This is the **first substep** of the Pilot phase:

```
Pilot Phase:
1. problem_validation (this skill) ← ENTRY POINT
2. problem_analysis
3. pilot_design
4. pilot_execution
```

If validation fails (Reformulate/Defer/Pivot), do NOT proceed to problem_analysis.