---
name: airesearchorchestrator:write-paper
description: "Run the Paper phase for manuscript writing and review"
allowed-tools: "Read, Write, Edit, Grep, Glob, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*), Agent, Skill"
---

# Write Paper Phase

Execute the **Writer ↔ Reviewer** loop for manuscript development. No arguments needed.

## Steps

1. **Read project state** — load `.autoresearch/state/research-state.yaml`. Confirm Gate 3 was approved.

2. **Spawn Writer agent**:
   ```
   Agent(subagent_type="airesearchorchestrator:writer", prompt="...")
   ```

3. **Spawn Reviewer agent** after Writer completes:
   ```
   Agent(subagent_type="airesearchorchestrator:reviewer", prompt="...")
   ```

4. **Evaluate gate** — read `paper/phase-scorecard.md` and present Gate 4 scorecard to the user.

5. **Loop or advance** — score < 3.5: loop with Reviewer feedback. Score ≥ 3.5: await human approval before `/reflect`.

## Required deliverables

- `paper/paper-draft.md`
- `paper/citation-audit-report.md`
- `paper/reviewer-report.md`
- `paper/rebuttal-log.md`
- `paper/final-acceptance-report.md`
- `paper/phase-scorecard.md`

## Gate 4 requirements

- Evidence-grounded draft (no unsupported claims)
- Citation audit ≥ 90% verified
- Reviewer report with scores
- Revision log complete
- Top-tier submission bar met

**Do NOT advance to Reflection without explicit human approval.**
