---
name: airesearchorchestrator:run-survey
description: "Run the Survey phase for literature review and research gap identification"
allowed-tools: "Read, Write, Edit, Grep, Glob, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*), Agent, Skill"
---

# Run Survey Phase

Execute the **Survey ↔ Critic** loop. No arguments needed — Orchestrator reads the project state and drives the agents directly.

## Steps

1. **Read project state** — load `.autoresearch/state/research-state.yaml` and `.autoresearch/config/orchestrator-config.yaml`.

2. **Spawn Survey agent**:
   ```
   Agent(subagent_type="airesearchorchestrator:survey", prompt="...")
   ```

3. **Spawn Critic agent** after Survey completes:
   ```
   Agent(subagent_type="airesearchorchestrator:critic", prompt="...")
   ```

4. **Evaluate gate** — read `docs/survey/phase-scorecard.md` and present Gate 1 scorecard to the user.

5. **Loop or advance** — score < 3.5: loop with Critic feedback. Score ≥ 3.5: await human approval before `/run-pilot`.

6. **Shutdown agents** — after gate evaluation completes (advance or escalate):
   ```
   SendMessage(to="survey", message={"type": "shutdown_request", "reason": "Phase complete"})
   SendMessage(to="critic", message={"type": "shutdown_request", "reason": "Phase complete"})
   TeamDelete(team_name="research-survey")
   ```

## Required deliverables

- `docs/survey/survey-round-summary.md`
- `docs/survey/critic-round-review.md`
- `docs/survey/research-readiness-report.md`
- `docs/survey/phase-scorecard.md`

## Gate 1 requirements

- Bounded scope with atomic definitions
- Literature coverage (recent 5 years + seminal works)
- Novelty argument documented
- Validation route identified

**Do NOT advance to Pilot without explicit human approval.**
