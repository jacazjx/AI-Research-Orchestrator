---
name: airesearchorchestrator:reflect
description: "Run the Reflection phase for lessons learned and system improvement"
allowed-tools: "Read, Write, Edit, Grep, Glob, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*), Agent, Skill"
---

# Reflection Phase

Execute the **Reflector ↔ Curator** loop for project closure. No arguments needed.

## Steps

1. **Read project state** — load `.autoresearch/state/research-state.yaml`. Confirm Gate 4 was approved.

2. **Spawn Reflector agent**:
   ```
   Agent(subagent_type="airesearchorchestrator:reflector", prompt="...")
   ```

3. **Spawn Curator agent** after Reflector completes:
   ```
   Agent(subagent_type="airesearchorchestrator:curator", prompt="...")
   ```

4. **Evaluate gate** — read `docs/reflection/phase-scorecard.md` and present Gate 5 scorecard to the user.

5. **Present decisions** — ask user:
   - Approve the lessons-learned report?
   - Activate any overlay proposals? (requires explicit opt-in per overlay)

6. **Shutdown agents** — after gate evaluation completes:
   ```
   SendMessage(to="reflector", message={"type": "shutdown_request", "reason": "Phase complete"})
   SendMessage(to="curator", message={"type": "shutdown_request", "reason": "Phase complete"})
   TeamDelete(team_name="research-reflection")
   ```

7. **Project closure validation** — after user approves Gate 5, run closure validation:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_handoff.py \
     --project-root <project_root> --target reflection-closeout --json
   ```
   If validation fails, report issues to user before marking project complete.
   If validation passes, update state: `current_phase: "archive"`, `progress.completion_percent: 100`.

## Required deliverables

- `docs/reflection/lessons-learned.md`
- `docs/reflection/overlay-draft.md`
- `docs/reflection/runtime-improvement-report.md`
- `docs/reflection/phase-scorecard.md`
- `docs/reflection/system-evaluation-report.md`

## Gate 5 requirements

- Lessons documented and transferable
- Overlay proposals clearly marked as drafts
- Safe vs. human-judgment changes separated
- System evaluation report evidence-based and Curator-audited

**Overlays are NEVER applied automatically — each requires explicit user approval.**
