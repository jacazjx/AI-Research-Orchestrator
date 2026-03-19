---
name: airesearchorchestrator:reflect
description: "Run the Reflection phase for lessons learned and system improvement"
argument-hint: ""
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

## Required deliverables

- `docs/reflection/lessons-learned.md`
- `docs/reflection/overlay-draft.md`
- `docs/reflection/runtime-improvement-report.md`
- `docs/reflection/phase-scorecard.md`

## Gate 5 requirements

- Lessons documented and transferable
- Overlay proposals clearly marked as drafts
- Safe vs. human-judgment changes separated

**Overlays are NEVER applied automatically — each requires explicit user approval.**
