---
description: "Run the full Experiments phase for comprehensive evaluation"
argument-hint: "[--project-root <path>] [--max-loops <number>]"
allowed-tools: "Read, Write, Edit, Grep, Glob, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*), Agent"
---

# Run Experiments Phase

Executes the Code <-> Adviser loop for full experiments:

- `docs/reports/experiments/experiment-spec.md`
- `docs/reports/experiments/run-registry.md`
- `docs/reports/experiments/results-summary.md`
- `code/checkpoints/checkpoint-index.md`
- `docs/reports/experiments/evidence-package-index.md`
- `docs/reports/experiments/phase-scorecard.md`

## Execution

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/run_stage_loop.py" --phase experiments $ARGUMENTS
```

## Process

1. Code finalizes experiment matrix and runs experiments
2. Adviser reviews evidence strength
3. Loop until ready for Gate 3

## Gate 3 Requirements

- Frozen experiment spec
- All runs traceable
- Results match experiment plan
- Checkpoints documented
- Complete evidence package

## Agent Invocation

**You MUST invoke subagents using the Agent tool.** Simply running the script is NOT enough.

### Agent Pair

| Role | Agent |
|------|-------|
| Primary | `code` |
| Reviewer | `adviser` |

### Workflow

1. Initialize phase state (script above)
2. Invoke Code agent with experiment execution task
3. Invoke Adviser agent to verify experiment integrity
4. Loop if score < 3.5
5. Present Gate 3 to human for approval

**Wait for human approval before advancing to Paper phase.**