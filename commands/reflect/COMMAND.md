---
name: airesearchorchestrator:reflect
description: "Run the Reflection phase with Reflector and Curator agents. Use when user says 'reflect', 'reflection', '反思', '总结'."
triggers:
  - "reflect"
  - "reflection"
  - "反思"
  - "总结"
  - "lessons learned"
---

# Reflection Phase

Executes the Reflector <-> Curator loop for project closure:

- `docs/reports/reflection/lessons-learned.md`
- `docs/reports/reflection/overlay-draft.md`
- `docs/reports/reflection/runtime-improvement-report.md`
- `docs/reports/reflection/phase-scorecard.md`
- `.autoresearch/archive/archive-index.md`

## Process

1. Reflector extracts lessons and improvement suggestions
2. Curator judges which suggestions are reusable
3. User decides on overlay activation

## Gate 5 Requirements

- Lessons documented and transferable
- Overlay drafts marked as drafts
- All changes documented
- Opt-in list for changes requiring approval

## Final Decisions

- Overlay activation (yes/no)
- If yes: `python3 scripts/apply_overlay.py --project-root <path>`
- Project status set to `completed`