---
name: airesearchorchestrator:run-pilot
description: "Run the Pilot phase for preliminary experiment validation"
allowed-tools: "Read, Write, Edit, Grep, Glob, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*), Agent, Skill"
---

# Run Pilot Phase

Execute the **Code ↔ Adviser** loop for pilot validation. No arguments needed.

## Steps

1. **Read project state** — load `.autoresearch/state/research-state.yaml`. Confirm Gate 1 was approved.

2. **Spawn Coder agent**:
   ```
   Agent(subagent_type="airesearchorchestrator:coder", prompt="...")
   ```

3. **Spawn Adviser agent** after Coder completes:
   ```
   Agent(subagent_type="airesearchorchestrator:adviser", prompt="...")
   ```

4. **Evaluate gate** — read `docs/pilot/phase-scorecard.md` and present Gate 2 scorecard to the user.

5. **Loop or advance** — score < 3.5: loop with Adviser feedback. Score ≥ 3.5: await human approval before `/run-experiments`.

## Required deliverables

- `docs/pilot/problem-analysis.md`
- `docs/pilot/pilot-experiment-plan.md`
- `docs/pilot/pilot-results.md`
- `docs/pilot/pilot-validation-report.md`
- `docs/pilot/phase-scorecard.md`

## Gate 2 requirements

- Problem analysis complete
- Low-cost pilot executed
- Results tied to hypothesis
- Clear continue / pivot recommendation

**Do NOT advance to Experiments without explicit human approval.**
