---
name: airesearchorchestrator:run-experiments
description: "Run the full Experiments phase for comprehensive evaluation"
allowed-tools: "Read, Write, Edit, Grep, Glob, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*), Agent, Skill"
---

# Run Experiments Phase

Execute the **Code ↔ Adviser** loop for full experiments. No arguments needed.

## Steps

1. **Read project state** — load `.autoresearch/state/research-state.yaml`. Confirm Gate 2 was approved.

2. **Spawn Coder agent**:
   ```
   Agent(subagent_type="airesearchorchestrator:coder", prompt="...")
   ```

3. **Spawn Adviser agent** after Coder completes:
   ```
   Agent(subagent_type="airesearchorchestrator:adviser", prompt="...")
   ```

4. **Evaluate gate** — read `docs/experiments/phase-scorecard.md` and present Gate 3 scorecard to the user.

5. **Loop or advance** — score < 3.5: loop with Adviser feedback. Score ≥ 3.5: await human approval before `/write-paper`.

## Required deliverables

- `docs/experiments/experiment-spec.md`
- `docs/experiments/run-registry.md`
- `docs/experiments/results-summary.md`
- `code/checkpoints/checkpoint-index.md`
- `docs/experiments/evidence-package-index.md`
- `docs/experiments/phase-scorecard.md`

## Gate 3 requirements

- Frozen experiment spec
- All runs traceable with checksums
- Results match experiment plan
- Complete evidence package

**Do NOT advance to Paper without explicit human approval.**
