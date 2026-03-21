---
name: airesearchorchestrator:insight
agent: orchestrator
description: "Interactive intent clarification -- helps users sharpen their research idea before initialization. Use when user says 'insight', '澄清意图', '明确想法', 'clarify intent', '研究想法'. Run this BEFORE /init-research for vague ideas."
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Interactive Intent Clarification

Engages the user in a focused Q&A loop to surface and sharpen the true research intent before committing to a project. Run this **before** `/init-research`.

## When to Use

- Clarify a vague or broad research direction
- Validate feasibility before initializing a full project
- Identify constraints (deadline, venue, resources) early
- Surface novelty gaps before the literature survey

## Workflow

1. **Detect context** -- Check if an existing project has a topic to refine, or start from scratch
2. **Assess clarity** across five dimensions (see below)
3. **Ask targeted questions** focused on the lowest-scoring dimensions
4. **Iterate** until clarity >= 0.7 or max rounds reached
5. **Output** the sharpened idea statement with scores and recommended next step

## Five-Dimension Assessment

| Dimension | Weight | Key Question |
|-----------|--------|--------------|
| **Problem** | 25% | What specific problem are you solving, and why does it matter? |
| **Solution** | 25% | What approach or intuition do you have in mind? |
| **Contribution** | 20% | What type of contribution? What is the success criterion? |
| **Constraints** | 15% | What time, resource, or venue constraints apply? |
| **Novelty** | 15% | How is this different from existing work? What is the key insight? |

Compute overall clarity as the weighted sum of per-dimension scores (each 0.0-1.0).

## Clarity Thresholds

| Score | Status | Recommendation |
|-------|--------|----------------|
| >= 0.7 | Clear | Proceed to `/init-research` |
| 0.4-0.7 | Needs work | Continue Q&A rounds |
| < 0.4 | Too vague | Browse `${CLAUDE_PLUGIN_ROOT}/skills/` for ideation tools (e.g., the `ideation` skill) to help brainstorm |

## Conducting Each Round

In each Q&A round:

1. Score all five dimensions based on what is known so far (0.0-1.0 each)
2. Compute the weighted clarity score
3. Identify the 1-2 lowest-scoring dimensions
4. Ask 1-2 focused questions targeting those dimensions
5. After the user responds, re-score and check thresholds

Keep questions concrete and specific. Avoid abstract meta-questions. Good: "What specific metric would you use to measure success?" Bad: "Can you tell me more about your idea?"

## Output

After clarification completes, provide:

- Sharpened idea statement (1-3 sentences)
- Overall clarity score
- Per-dimension scores with brief justification
- Recommended next action (proceed to `/init-research`, continue clarifying, or brainstorm with `ideation`)
- Summary of key decisions made during clarification

## Hard Rules

1. **Never skip for low clarity** -- if score < 0.4, recommend brainstorming with the `ideation` skill
2. **Max 5 rounds** -- do not loop endlessly; escalate if still unclear after 5 rounds
3. **Document everything** -- all Q&A exchanges must be recorded for the project record
4. **Confirm before proceeding** -- get explicit user confirmation on the sharpened idea
5. **Use first-principles thinking** -- start from fundamentals, not assumptions

## Related Skills

- `orchestrator` -- Initialize and run the full project after clarification
- `ideation` -- Brainstorm and develop research ideas when the direction is too vague
