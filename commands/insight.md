---
name: airesearchorchestrator:insight
description: "Interactive intent clarification — helps users sharpen their research idea before initialization"
allowed-tools: "Read, Write, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*), AskUserQuestion"
---

# Interactive Intent Clarification

Engages the user in a focused Q&A loop to surface and sharpen the true research intent before committing to a project. Run this **before** `/init-research`.

## Interactive Workflow

When invoked, conduct a structured Q&A session. Start by asking for the research direction, then probe each dimension.

### Step 1: Initial Research Direction

Ask: "What research direction or problem are you considering?"

Accept a free-form description. This is the starting point for deeper exploration.

### Step 2: Five-Dimension Assessment

For each dimension, ask targeted questions to assess clarity:

#### Problem (25% weight)

Ask:
- "What specific problem are you trying to solve?"
- "Why does this problem matter? Who cares about the solution?"

**Clarity indicators:**
- Clear: Specific, bounded problem statement
- Vague: "I want to do something with X"

#### Solution (25% weight)

Ask:
- "What approach or intuition do you have for solving this?"
- "What method or technique might work?"

**Clarity indicators:**
- Clear: Specific methodology or hypothesis
- Vague: "I'll figure it out"

#### Contribution (20% weight)

Ask:
- "What type of contribution will this make? (new method, new insight, new application, etc.)"
- "How will you know if the research is successful?"

**Clarity indicators:**
- Clear: Defined success criteria and contribution type
- Vague: "I want to publish something"

#### Constraints (15% weight)

Ask:
- "What time constraints do you have? (deadline, venue target)"
- "What resources are available? (GPU, data, compute budget)"

**Clarity indicators:**
- Clear: Specific deadline and resource limits
- Vague: "No constraints" or unknown

#### Novelty (15% weight)

Ask:
- "How is this different from existing work in the field?"
- "What is the key insight or angle that makes this novel?"

**Clarity indicators:**
- Clear: Specific differentiation from prior work
- Vague: "It's a new idea" without specifics

### Step 3: Calculate Clarity Score

After the Q&A session, assess each dimension:

| Score Range | Status | Recommendation |
|-------------|--------|----------------|
| >= 0.7 | Clear | Ready to proceed to `/init-research` |
| 0.4–0.7 | Needs work | Continue Q&A on weak dimensions |
| < 0.4 | Too vague | Suggest broader exploration or literature review |

### Step 4: Generate Summary

Output a structured summary:

```markdown
## Research Intent Summary

**Problem:** [summarized]
**Proposed Solution:** [summarized]
**Contribution Type:** [summarized]
**Constraints:** [summarized]
**Novelty Angle:** [summarized]

**Clarity Score:** X.XX

**Recommendation:** [proceed / needs clarification / explore further]
```

## Use Cases

- Clarify a vague or broad research direction
- Validate feasibility before initializing a full project
- Identify constraints (deadline, venue, resources) early
- Surface novelty gaps before the literature survey

## After Clarification

If score >= 0.7, suggest:
> "Your research intent is clear. Would you like to proceed with `/init-research` to create the project?"

If score < 0.7, identify weak dimensions and continue Q&A or suggest literature review.