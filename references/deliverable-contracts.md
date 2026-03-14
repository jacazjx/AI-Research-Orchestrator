# Deliverable Contracts

## `.autoresearch/state/research-state.yaml`

- Store project id, topic, current phase, gate state, phase-review state, loop counts, loop limits, language policy, progress, runtime registry paths, and canonical deliverable paths.
- Keep all deliverable paths project-relative.

## `.autoresearch/config/orchestrator-config.yaml`

- Store project-level runtime defaults such as stale job threshold, loop limits, language policy, and enabled backends.
- Act as the human-editable configuration source for runtime scripts that should not hard-code policy.

## `.autoresearch/dashboard/*`

- `status.json` is the machine-readable dashboard snapshot.
- `progress.md` is the human-readable progress board.
- `timeline.ndjson` is the append-only event stream.

## `docs/reports/survey/research-readiness-report.md`

- Include background, scope, problem definition, theory analysis, recent work, risk register, novelty argument, and minimum viable validation path.
- End with an explicit Gate 1 recommendation.

## `docs/reports/pilot/pilot-validation-report.md`

- Explain whether the idea deserves full experiments, revision, or pivot.
- Link problem analysis, pilot plan, pilot results, and adviser review.

## `docs/reports/experiments/evidence-package-index.md`

- Act as the table of contents for experiment artifacts, run provenance, checkpoints, tables, and figures.
- Point to the final set of evidence used for Gate 3.

## `paper/final-acceptance-report.md`

- State whether the package has reached top-tier venue submission quality for user review.
- Explicitly note unresolved risks and out-of-scope checks.

## `paper/citation-audit-report.md`

- Record citation gaps, verification attempts, DOI-verified or trusted-source outcomes, preprint replacement issues, and remaining citation risks.
- Serve as the paper-phase evidence source for citation authenticity review.

## `docs/reports/reflection/runtime-improvement-report.md`

- Separate observations, recommendations, and overlay drafts.
- State which changes are safe to consider and which still require additional human judgment.