---
name: airesearchorchestrator:auto-review-loop
description: Autonomous multi-round research review loop. Repeatedly reviews via Codex MCP, implements fixes, and re-reviews until positive assessment or max rounds reached. Use when user says "auto review loop", "review until it passes", or wants autonomous iterative improvement.
user-invocable: true
argument-hint: [topic-or-scope]
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply
---
## Purpose

This skill implements an "Autonomous multi-round research review loop" that repeatedly: reviews via Codex MCP → implements fixes → re-reviews until the external reviewer gives a positive assessment or `MAX_ROUNDS` is reached.

## Constants

- `MAX_ROUNDS = 4`
- **Positive threshold:** score ≥ 6/10, or verdict contains "accept", "sufficient", "ready for submission"
- `REVIEW_DOC`: `AUTO_REVIEW.md` in project root (cumulative log)
- `REVIEWER_MODEL = gpt-5.4` — OpenAI model used via Codex MCP (e.g., `gpt-5.4`, `o3`, `gpt-4o`)

## State Persistence

Persist state to `REVIEW_STATE.json` after each round:

```json
{
  "round": 2,
  "threadId": "019cd392-...",
  "status": "in_progress",
  "last_score": 5.0,
  "last_verdict": "not ready",
  "pending_experiments": ["screen_name_1"],
  "timestamp": "2026-03-13T21:00:00"
}
```

Write at end of every Phase E; overwrite each time. On completion, set `"status": "completed"`.

## Workflow

### Initialization
1. Check `REVIEW_STATE.json` for recovery conditions (fresh start, resume, or stale)
2. Read project documents, memory files, prior reviews
3. Check experiment results
4. Identify weaknesses and TODOs
5. Initialize round counter (or recover from state)
6. Create/update `AUTO_REVIEW.md`

### Loop Phases (repeat ≤ MAX_ROUNDS)

**Phase A: Review**
- Send context to external reviewer via `mcp__codex__codex` (round 1) or `mcp__codex__codex-reply` (round 2+ with saved `threadId`)
- Use `config: {"model_reasoning_effort": "xhigh"}`

**Phase B: Parse Assessment**
- Save FULL raw response verbatim
- Extract: Score (1-10), Verdict, Action items
- Stop if: score ≥ 6 AND verdict contains "ready" or "almost"

**Feishu Notification** (if `~/.claude/feishu.json` exists and mode ≠ "off"):
- Send `review_scored`: "Round N: X/10 — [verdict]" with top 3 weaknesses
- Interactive mode + "almost" verdict: wait for user reply

**Phase C: Implement Fixes**
- Code changes, run experiments (SSH + screen/tmux), analysis, documentation
- Skip: excessive compute, unavailable external resources
- Prefer reframing/analysis over new experiments
- Always implement metric additions

**Phase D: Wait for Results**
- Monitor remote sessions, collect results

**Phase E: Document Round**
- Append to `AUTO_REVIEW.md` with assessment, verbatim reviewer response (in `<details>`), actions taken, results, status
- Write `REVIEW_STATE.json`
- Increment round → back to Phase A

## Termination

1. Set `REVIEW_STATE.json` `"status": "completed"`
2. Final summary to `AUTO_REVIEW.md`
3. Update project notes
4. If max rounds without positive assessment: list blockers, estimate effort, suggest next steps
5. Feishu `pipeline_done` notification with score progression table (if configured)

## Key Rules

- Always use `"model_reasoning_effort": "xhigh"`
- Save `threadId`, use `codex-reply` for subsequent rounds
- Include negative results and failures
- Don't hide weaknesses to game scores
- Implement fixes before re-reviewing
- Experiments >30 min: launch and continue with other fixes
- Document everything; update notes after each round

## Prompt Template (Round 2+)

```
[Round N update]

Since your last review, we have:
1. [Action 1]: [result]
2. [Action 2]: [result]
3. [Action 3]: [result]

Updated results table:
[paste metrics]

Please re-score and re-assess. Are the remaining concerns addressed?
Same format: Score, Verdict, Remaining Weaknesses, Minimum Fixes.
```