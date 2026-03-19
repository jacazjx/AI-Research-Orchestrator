---
name: airesearchorchestrator:run-pilot
description: "Run the Pilot phase for preliminary experiment validation"
argument-hint: "[--project-root <path>] [--max-loops <number>]"
allowed-tools: "Read, Write, Edit, Grep, Glob, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*), Agent"
---

# Run Pilot Phase

Executes the Code <-> Adviser loop for pilot analysis:

- `docs/pilot/problem-analysis.md`
- `docs/pilot/pilot-experiment-plan.md`
- `docs/pilot/pilot-results.md`
- `docs/pilot/pilot-validation-report.md`
- `docs/pilot/phase-scorecard.md`

## Execution

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/run_stage_loop.py" --phase pilot $ARGUMENTS
```

## Process

1. Code does problem analysis and low-cost validation design
2. Adviser judges if pilot supports continue/revise/pivot
3. Loop until ready for Gate 2

## Gate 2 Requirements

- Operational analysis
- Low-cost plan
- Pilot results tied to hypothesis
- Clear recommendation

## Agent Invocation

**You MUST invoke subagents using the Agent tool.** Simply running the script is NOT enough.

### Agent Pair

| Role | Agent |
|------|-------|
| Primary | `code` |
| Reviewer | `adviser` |

### Workflow

1. Initialize phase state (script above)
2. Invoke Code agent with pilot experiment task
3. Invoke Adviser agent to review pilot
4. Loop if score < 3.5
5. Present Gate 2 to human for approval

**Wait for human approval before advancing to Experiments phase.**