---
name: airesearchorchestrator:external-review
agent: orchestrator
description: "External review of any research deliverable via Codex MCP. Supports single-shot critique and multi-round review-fix loops for research ideas, experiment results, papers, or any artifact. The agent decides scope and number of rounds based on context. Use when user says \"review\", \"critique\", \"improve paper\", \"auto review\", \"反馈\", \"改论文\", \"论文润色循环\"."
user-invocable: true
argument-hint: [deliverable-path-or-description]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply
---
# External Review

## Purpose

Provide external critical review of any research deliverable via Codex MCP. This skill unifies single-shot reviews and multi-round improvement loops into one flexible workflow. The agent decides whether to do a one-off review or iterate based on the deliverable type, current quality, and project context.

## Modes

| Mode | When to Use | Typical Rounds |
|------|-------------|----------------|
| **Single-shot** | Quick feedback on an idea, plan, or early draft | 1 |
| **Multi-round** | Iterative improvement of a mature deliverable (paper, experiment results) | Agent decides based on progress |

The agent should stop iterating when: (a) the reviewer gives a positive assessment (score >= 6/10 and verdict contains "accept", "ready", or "sufficient"), (b) successive rounds show diminishing returns (score improvement < 0.5), or (c) remaining issues require work outside the scope of this skill (e.g., new experiments, fundamental redesign).

## Workflow

### Step 1: Assess the Deliverable

Read the target deliverable and determine:
- **Type**: research idea, experiment results, paper draft, or other artifact
- **Maturity**: early draft vs. near-final
- **Review goal**: brutal feedback, specific improvement, or submission readiness check

### Step 2: Prepare Review Context

Gather supporting materials:
- Project state and phase context
- Relevant prior reviews (if any)
- Evidence package, pilot results, or literature notes as appropriate
- Prior review thread ID (if resuming a multi-round loop)

### Step 3: Send to External Reviewer

Use Codex MCP with reasoning effort `xhigh`:

```
mcp__codex__codex (first round):
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    You are a senior reviewer for [VENUE]. Review this [deliverable type]:

    [deliverable content]

    Provide:
    1. Score (1-10)
    2. Verdict (accept / major revision / reject)
    3. Strengths (ranked)
    4. Weaknesses (ranked: CRITICAL > MAJOR > MINOR)
    5. For each CRITICAL/MAJOR weakness: a specific, actionable fix
    6. Missing references (if any)
```

Save the `threadId` from the response.

### Step 4: Parse and Record Assessment

- Save the FULL raw response verbatim (in a `<details>` block in the log)
- Extract: score, verdict, action items by severity
- Record in the review log file

### Step 5: Decide Whether to Iterate

If single-shot mode or positive assessment: stop and report.

If iterating:
1. Implement fixes by severity (CRITICAL first, then MAJOR)
2. For papers: recompile LaTeX after fixes, verify 0 errors
3. Send update to reviewer via `mcp__codex__codex-reply` with saved `threadId`:

```
mcp__codex__codex-reply:
  threadId: [saved]
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    [Round N update]

    Since your last review, we have:
    1. [Action 1]: [result]
    2. [Action 2]: [result]

    Please re-score and re-assess. Same format:
    Score, Verdict, Strengths, Weaknesses, Actionable fixes.
```

4. Repeat from Step 4.

### Step 6: Document Results

Save review log to the appropriate location based on deliverable type:
- Research ideas/plans: `docs/<phase>/review-log.md`
- Papers: `paper/REVIEW_LOG.md`

Include:
- Score progression table (if multi-round)
- Full verbatim reviewer responses in `<details>` blocks
- Actions taken per round
- Final status and remaining issues

## State Persistence

For multi-round loops, persist state to `REVIEW_STATE.json` next to the review log:

```json
{
  "round": 2,
  "threadId": "019cd392-...",
  "status": "in_progress",
  "last_score": 5.0,
  "last_verdict": "not ready",
  "deliverable_type": "paper",
  "timestamp": "2026-03-13T21:00:00"
}
```

On startup, check for existing state to support session recovery. Set `"status": "completed"` when done.

## Paper-Specific Guidance

When reviewing papers, after each round of fixes:
1. Recompile: `cd paper && latexmk -C && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`
2. Verify: 0 undefined references, 0 undefined citations
3. Preserve PDF versions: `cp main.pdf main_roundN.pdf`
4. Run format check (page count, overfull hbox warnings) after the final round

Common paper fix patterns:

| Issue | Fix Pattern |
|-------|-------------|
| Assumption-model mismatch | Rewrite assumption to match model, add bridging proposition |
| Overclaims | Soften language: "validate" -> "demonstrate practical relevance" |
| Missing metrics | Add quantitative table with honest parameter counts |
| Notation confusion | Rename conflicting symbols globally, add Notation paragraph |
| Theory-practice gap | Frame theory as idealized; add synthetic validation subsection |

## Feishu Notification

If `~/.claude/feishu.json` exists and mode is not `"off"`:
- After each round: send `review_scored` with score and top weaknesses
- After completion: send `pipeline_done` with score progression table

## Key Rules

1. Always use `"model_reasoning_effort": "xhigh"` for Codex MCP calls
2. Save `threadId` and use `codex-reply` for subsequent rounds in the same thread
3. Save FULL raw review text verbatim -- do not summarize or truncate
4. Verify citation authenticity (no fake references)
5. Include negative results and failures honestly -- do not hide weaknesses to game scores
6. Implement fixes before re-reviewing
7. For experiments > 30 min: launch asynchronously and continue with other fixes
8. Do not fabricate experimental results
