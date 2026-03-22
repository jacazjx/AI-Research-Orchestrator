# Gate Rubrics

This document defines the detailed rubrics for each gate in the five-phase research workflow.

## Gate 1: Research Readiness

### Approval Criteria

| Requirement | Description | Verification |
|-------------|-------------|--------------|
| Bounded scope | Clear problem statement with defined boundaries | Check idea-brief.md |
| Atomic definitions | Each definition is self-contained, implementable, falsifiable | Check survey-round-summary.md |
| Literature coverage | Recent (5 years) + seminal coverage | Check citation counts and dates |
| Novelty argument | Explicit differentiation from prior work | Check research-readiness-report.md |
| Validation route | Clear path to validate the hypothesis | Check proposed experiments |

### Scoring Dimensions

| Dimension | Weight | 5 (Excellent) | 3 (Acceptable) | 1 (Poor) |
|-----------|--------|---------------|----------------|----------|
| Citation Authenticity | 25% | ≥90% Grade A/B | 80-89% Grade A/B | <80% Grade A/B |
| Novelty | 25% | Clear, significant contribution | Incremental improvement | No clear novelty |
| Literature Coverage | 25% | Comprehensive, well-organized | Adequate coverage | Gaps in key areas |
| Idea Definition | 25% | Atomic, precise, implementable | Mostly clear | Vague or incomplete |

### Rejection Conditions

- Novelty claim depends on missing/weak literature
- Scope too broad to validate cheaply
- Key assumptions remain untestable
- Citation authenticity < 80% Grade A/B
- Atomic definitions incomplete

---

## Gate 2: Pilot Validation

### Approval Criteria

| Requirement | Description | Verification |
|-------------|-------------|--------------|
| Operational analysis | Hypothesis translated to testable form | Check problem-analysis.md |
| Low-cost plan | Minimal experiment design | Check pilot-experiment-plan.md |
| Pilot results | Results tied to hypothesis | Check pilot-results.md |
| Adviser review | Clear recommendation (proceed/revise/pivot) | Check pilot-adviser-review.md |
| Validation report | Explains next steps with evidence | Check pilot-validation-report.md |

### Scoring Dimensions

| Dimension | Weight | 5 (Excellent) | 3 (Acceptable) | 1 (Poor) |
|-----------|--------|---------------|----------------|----------|
| Hypothesis Clarity | 25% | Testable, bounded | Mostly clear | Ambiguous |
| Pilot Design | 25% | Can falsify hypothesis | Partially validates | Cannot validate |
| Execution Quality | 25% | Complete, documented | Mostly complete | Incomplete |
| Decision Support | 25% | Clear recommendation with evidence | Recommendation exists | No clear decision |

### Rejection Conditions

- Pilot evidence too weak for full compute
- Setup cannot falsify the main idea
- Failure modes observed but ignored
- No clear recommendation
- Hypothesis untestable

---

## Gate 3: Full Experiment Evidence Package

### Approval Criteria

| Requirement | Description | Verification |
|-------------|-------------|--------------|
| Frozen spec | Complete experiment specification | Check experiment-spec.md |
| Run provenance | All runs traceable | Check run-registry.md |
| Results tied to matrix | Results match experiment plan | Check results-summary.md |
| Checkpoint tracking | All checkpoints documented | Check checkpoint-index.md |
| Evidence index | Complete package linked | Check evidence-package-index.md |
| Statistical minimums | Runs meet minimum counts per evidence-standards.md | Check run counts vs. requirements |

### Scoring Dimensions

| Dimension | Weight | 5 (Excellent) | 3 (Acceptable) | 1 (Poor) |
|-----------|--------|---------------|----------------|----------|
| Result Traceability | 30% | All runs verified | Most verified | Unverified claims |
| Statistical Validity | 25% | Complete statistics; meets sample-size minimums | Basic statistics; most minimums met | No statistics or below minimums |
| Baseline Completeness | 25% | Fair, comprehensive | Adequate | Missing or unfair |
| Negative Handling | 20% | All documented | Some documented | Hidden |

### Rejection Conditions

- Metrics exist without provenance
- Baselines or datasets changed without justification
- Negative results hidden
- Statistical claims unsupported
- Run counts below minimum thresholds (single method < 3, comparison < 5 per method, ablation < 3 per config — see [Evidence Standards](evidence-standards.md#sample-size-guidelines))
- Checkpoint integrity issues

---

## Gate 4: Paper Package

### Approval Criteria

| Requirement | Description | Verification |
|-------------|-------------|--------------|
| Evidence-grounded draft | All claims from approved evidence | Cross-check with evidence package |
| Citation audit | ≥90% verified or trusted | Check citation-audit-report.md |
| Reviewer report | Structured review with scores | Check reviewer-report.md |
| Revision log | Changes tracked | Check rebuttal-log.md |
| Acceptance report | Top-tier bar met | Check final-acceptance-report.md |

### Scoring Dimensions

| Dimension | Weight | 5 (Excellent) | 3 (Acceptable) | 1 (Poor) |
|-----------|--------|---------------|----------------|----------|
| Novelty | 25% | Clear significant contribution | Incremental | Weak |
| Evidence Strength | 30% | Strong, traceable | Adequate | Unsupported |
| Theoretical Foundation | 15% | Rigorous | Reasonable | Weak |
| Result Analysis | 15% | Deep, insightful | Adequate | Shallow |
| Writing Quality | 15% | Clear, professional | Readable | Poor |

### Rejection Conditions

- Manuscript introduces unsupported claims
- Citations unverifiable or suspicious
- Reviewer findings unaddressed
- Below top-tier bar on any dimension
- Citation audit issues unresolved

---

## Gate 5: Reflection and Evolution Package

### Approval Criteria

| Requirement | Description | Verification |
|-------------|-------------|--------------|
| Lessons learned | Documented, transferable | Check lessons-learned.md |
| Overlay drafts | Marked as drafts | Check overlay-draft.md |
| Safety notes | All changes documented | Check runtime-improvement-report.md |
| Opt-in list | Changes requiring approval | Check report |
| System evaluation | Evidence-based, audited | Check system-evaluation-report.md |

### Scoring Dimensions

| Dimension | Weight | 5 (Excellent) | 3 (Acceptable) | 1 (Poor) |
|-----------|--------|---------------|----------------|----------|
| Lessons Quality | 25% | Actionable, transferable | Documented | Superficial |
| Overlay Safety | 25% | Fully documented, opt-in | Mostly documented | Undocumented |
| Runtime Improvements | 20% | Clear, prioritized | Listed | Vague |
| Documentation | 10% | Complete | Mostly complete | Incomplete |
| System Evaluation Quality | 20% | Evidence-based, audited, trend-aware | Mostly evidenced | Unsupported scores |

### Rejection Conditions

- Overlays would silently change base prompts
- Runtime changes without safety rationale
- Mixes observations with unreviewed policy changes
- Opt-in requirements not explicit

> **Note**: Gate 5 is the final gate. After approval, the project transitions to archive status. The Orchestrator moves superseded artifacts to `.autoresearch/archive/`, updates state to `completed`, and closes the project. No further phase transitions occur. To start a new project, use `/init-research`.

---

## Gate Score Thresholds

| Score Range | Decision | Action |
|-------------|----------|--------|
| 4.5 - 5.0 | Approve | Proceed to next phase |
| 3.5 - 4.4 | Advance | Minor fixes, proceed |
| 2.5 - 3.4 | Revise | Significant revision needed |
| 1.5 - 2.4 | Major Revise | Return phase for major work |
| 0.0 - 1.4 | Pivot | Consider alternative direction |

## Blocking Issues

The following issues automatically block gate approval regardless of score:

### Gate 1
- Any fabricated citation
- Novelty claim without evidence
- Untestable hypothesis

### Gate 2
- Pilot cannot validate hypothesis
- No clear recommendation
- Unaddressed failure modes

### Gate 3
- Untraceable results
- Hidden negative results
- Unverified statistical claims

### Gate 4
- Unsupported claims in manuscript
- Unverified citations
- Fabrication suspected

### Gate 5
- Silent policy changes
- Undocumented overlays
- Missing safety rationale
- Unsupported evaluation scores (no evidence)
- Systematic self-leniency unaddressed by Curator
- Omitted escalation/pivot analysis