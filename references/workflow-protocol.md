# Workflow Protocol

Use this skill as a gated five-phase research runtime for one project at a time.

## Phase Order

The project uses semantic phase names:

1. `.autoresearch/`: initialize workspace, state, config, dashboard, runtime registries, idea brief, and reference drop zone.
2. `survey`: run `Survey <-> Critic` until the research-readiness package is strong enough for human review.
3. `pilot`: run `Pilot Code <-> Pilot Adviser` on problem analysis and low-cost validation before full experiments.
4. `experiments`: run `Experiment Code <-> Experiment Adviser` on the full matrix, execution provenance, and evidence package.
5. `paper`: run `Paper Writer <-> Reviewer & Editor` until the manuscript reaches top-tier submission readiness.
6. `reflection`: run `Reflector <-> Curator` to produce lessons learned, overlay drafts, and runtime improvement proposals.
7. `.autoresearch/archive/`: store superseded drafts, rejected pivots, and retired overlays without polluting live deliverables.

> **Backward Compatibility**: Legacy numbered phase names (`01-survey`, `02-pilot-analysis`, etc.) are still supported, but semantic names are recommended.

## Required Human Gates

- Gate 1: approve `docs/survey/research-readiness-report.md` before pilot analysis.
- Gate 2: approve `docs/pilot/pilot-validation-report.md` before full experiments.
- Gate 3: approve `docs/experiments/evidence-package-index.md` before paper writing.
- Gate 4: approve `paper/final-acceptance-report.md` before reflection or final handoff.
- Gate 5: approve `docs/reflection/runtime-improvement-report.md` before any overlay or runtime policy change becomes active.

When a human gate rejects the current phase:

- the orchestrator must present the allowed return phases
- the orchestrator may recommend a return phase based on the current blockers
- the user decides whether to stay in the same phase or roll back to an earlier phase
- no automatic rollback is allowed without that human decision

## Loop Policy

- `Survey` and `Critic` may iterate up to the configured `survey_critic` loop limit.
- `Code` and `Adviser` may iterate in pilot analysis up to `pilot_code_adviser`.
- `Code` and `Adviser` may iterate in full experiments up to `experiment_code_adviser`.
- `Paper Writer` and `Reviewer & Editor` may iterate up to `writer_reviewer`.
- `Reflector` and `Curator` may iterate up to `reflector_curator`.
- Once a loop reaches its limit without approval, escalate to the user instead of continuing autonomously.

## Runtime Rules

- `.autoresearch/state/research-state.yaml` is the only machine-readable truth.
- `.autoresearch/config/orchestrator-config.yaml` is the project-level runtime configuration.
- `.autoresearch/dashboard/` is the canonical place for visible progress artifacts.
- Every deliverable path referenced in the state must remain project-relative.
- Pivots may be proposed automatically, but never executed without explicit human approval.
- Paper writing must include a citation-authenticity pass before Gate 4.

**Agent Teams Update:** At the start of each phase, the Orchestrator creates a team with `TeamCreate`. When the phase ends, the Orchestrator sends a `shutdown_request` to each agent via `SendMessage`, then calls `TeamDelete` to disband the team.
