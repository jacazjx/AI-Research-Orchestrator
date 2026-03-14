# Self-Evolution

The runtime supports controlled evolution through approved overlays and reflection outputs.

Core scripts:

- `scripts/apply_overlay.py`
- `scripts/render_agent_prompt.py`

Rules:

- reflection outputs remain drafts until approved by Gate 5
- overlays are opt-in and stored in `research-state.yaml`
- approved overlays are appended during prompt rendering
- base prompts are never rewritten automatically

This preserves a system-level feedback loop without turning the Skill into an uncontrolled self-modifying system.
