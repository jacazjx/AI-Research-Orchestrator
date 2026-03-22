# System Evaluation Rubrics

This document defines the detailed scoring rubrics for the 6-dimension system self-evaluation conducted during the Reflection phase.

## Overview

After completing a research project, the Reflector agent evaluates the orchestrator system's performance using these rubrics. The Curator agent audits the evaluation for objectivity and evidence quality.

## Scoring Scale

| Score | Meaning |
|-------|---------|
| 5 | Excellent — exceeds expectations, reference-worthy best practice |
| 4 | Good — smooth operation, only minor improvement opportunities |
| 3 | Acceptable — meets objectives, clear improvement directions exist |
| 2 | Insufficient — issues impacted research quality |
| 1 | Seriously insufficient — severely hindered research progress |
| 0 | Failed — dimension completely non-functional |

## Weighted Total to Recommendation

| Total | Recommendation |
|-------|----------------|
| 4.5 - 5.0 | System performed excellently, record best practices |
| 3.5 - 4.4 | System performed well, improvement opportunities exist |
| 2.5 - 3.4 | Targeted improvements needed |
| 1.5 - 2.4 | Major improvements needed |
| 0.0 - 1.4 | Fundamental restructuring needed |

---

## Dimension 1: Workflow Effectiveness (Weight: 20%)

Evaluates whether the five-phase structure served this project well.

| Score | Criteria |
|-------|----------|
| 5 | All phases connect naturally; outputs directly serve next-phase inputs; research type perfectly matches phase configuration |
| 3 | Phases generally effective but with transition friction (manual adaptation needed) or uneven workload distribution |
| 1 | Phase ordering caused rework; phases skipped or outputs unused; phase structure mismatched with research type |

**Evidence Sources:**
- `research-state.yaml`: research_type, phase history, current_phase progression
- Handoff files between phases
- Pivot records and phase rollback history

**Diagnostic Output:**
- Inter-phase dependency satisfaction analysis
- Per-phase iteration proportion (time/effort distribution)
- Phase regression or rollback incidents

---

## Dimension 2: Agent Collaboration Quality (Weight: 20%)

Evaluates the efficiency and quality of Primary-Reviewer agent interactions.

| Score | Criteria |
|-------|----------|
| 5 | Reviewer identifies critical issues in first round; Primary revisions directly address problems; loops used ≤ 60% of limit; disagreements resolved constructively |
| 3 | Reviewer catches major issues but misses secondary ones; 1-2 rounds with no substantive progress; converges within loop limit |
| 1 | Reviewer fails to catch critical defects (exposed in later phases); or Primary repeatedly fails to address core issues; escalate_to_user triggered |

**Evidence Sources:**
- `loop_counts` vs `loop_limits` per phase
- `phase_reviews` status transitions
- Per-phase scorecard content (review quality indicators)
- Escalation records

**Diagnostic Output:**
- Per-phase Primary-Reviewer interaction efficiency table
- Effective revision vs. wasted iteration ratio
- Issues discovered by reviewer vs. issues missed (found later)

---

## Dimension 3: Gate Accuracy (Weight: 20%)

Evaluates whether gate scores accurately reflected deliverable quality.

| Score | Criteria |
|-------|----------|
| 5 | Gate scores highly consistent with actual deliverable quality; blocking issues correctly identified; no false positives or false negatives |
| 3 | Gate direction correct but individual dimension scores deviate ≥1 point; or 1 false positive/negative not caught promptly |
| 1 | Gate scores severely misaligned with actual quality; critical issues passed through gates; or gates repeatedly blocked high-quality deliverables |

**Evidence Sources:**
- `gate_scores` (gate_1 through gate_4)
- `gate_history` records
- Per-phase scorecard content
- Whether later phases were impacted by prior-phase quality issues

**Diagnostic Output:**
- Per-gate score vs. actual quality comparison table
- False positive/negative analysis
- Blocking issue effectiveness assessment

---

## Dimension 4: Template Effectiveness (Weight: 15%)

Evaluates whether templates guided agents toward high-quality outputs.

| Score | Criteria |
|-------|----------|
| 5 | Template structure fully guides high-quality output; Agent outputs naturally fill all template sections; no need to go outside template framework |
| 3 | Templates generally useful but some sections too vague, causing inconsistent output quality; or 1-2 template fields skipped/ignored by Agent |
| 1 | Template structure mismatches Agent actual output; many fields left empty or filled with meaningless content; Agent bypasses template to self-organize output |

**Evidence Sources:**
- Compare template files (`assets/templates/`) with actual deliverable content
- Placeholder detection results from `validate_deliverable_content`
- Deliverable completion metrics

**Diagnostic Output:**
- Per-template field fill rate table
- List of skipped/ignored fields
- Content that agents added beyond template structure

---

## Dimension 5: Resource Efficiency (Weight: 15%)

Evaluates whether loops, iterations, and escalations were used efficiently.

| Score | Criteria |
|-------|----------|
| 5 | All phases loop count ≤ 60% of limit; no unnecessary pivots; escalation only triggered when genuinely needed |
| 3 | Most phases efficient but 1-2 phases approach loop limit; 1 avoidable escalation or ineffective pivot |
| 1 | Multiple phases hit loop limit; frequent escalations; pivots fail to resolve core issues |

**Evidence Sources:**
- `loop_counts` vs `loop_limits` per phase
- `pivot_candidates` list
- `human_decisions` records
- Escalation frequency and outcomes

**Diagnostic Output:**
- Per-phase efficiency ratio table (actual loops / limit)
- Resource waste hotspot identification
- Pivot/escalation outcome analysis

---

## Dimension 6: User Experience (Weight: 10%)

Evaluates the quality of interaction between the orchestrator and the researcher.

| Score | Criteria |
|-------|----------|
| 5 | Decision points clearly presented; status information accurate and timely; gate results easily understood; no repeated user inquiries needed |
| 3 | Main information delivered but some decision points lack sufficient context; or status updates delayed |
| 1 | User frequently confused; critical decisions lack information support; status information inaccurate or lagging |

**Evidence Sources:**
- `human_decisions` (frequency, type, context quality)
- Dashboard content accuracy
- Escalation context quality (was enough information provided?)

**Diagnostic Output:**
- User intervention frequency analysis
- Information delivery quality assessment
- Decision point context completeness

---

## Blocking Issues (Automatic Rejection in Gate 5)

The following issues automatically block Gate 5 approval for the system evaluation component:

- **Unsupported scores**: Any dimension scored without corresponding factual evidence
- **Systematic self-leniency**: Curator finds ≥3 dimensions scored ≥1 point too high and Reflector refuses correction
- **Omitted critical events**: Project escalations or pivots not analyzed in evaluation
- **Fabricated trends**: Cross-project comparison data inconsistent with registry records

## Curator Independent Scoring Protocol

Before reviewing the Reflector's scores, the Curator MUST produce independent scores using this protocol:

### Step 1: Independent Assessment

For each of the 6 dimensions, the Curator:
1. Reads ONLY the evidence sources listed in that dimension's rubric (not the Reflector's report)
2. Applies the scoring criteria from the rubric above
3. Records a score (0-5) with a 1-sentence justification citing specific evidence

### Step 2: Comparison

After completing all 6 independent scores:
1. Read the Reflector's scores and justifications
2. For each dimension, compute `delta = |Curator_score - Reflector_score|`

### Step 3: Dispute Resolution

| Delta | Action |
|-------|--------|
| 0 | Agreement — accept score as-is |
| 1 | Minor disagreement — Curator notes the difference, accepts Reflector's score with caveat |
| ≥ 2 | Major disagreement — flag as "disputed", require Reflector to provide additional evidence or revise score. If unresolved after 1 round, use the LOWER of the two scores |

### Step 4: Final Score

The final reported score for each dimension is:
- The agreed score (if delta ≤ 1)
- The lower score (if delta ≥ 2 and unresolved)
- Weighted total recalculated from final dimension scores

## Curator Audit Checklist

### Evidence Completeness
- [ ] Each dimension's score references specific state data or deliverable content
- [ ] No vague "as observed" statements substituting for concrete evidence
- [ ] Quantitative metrics (loop counts, fill rates) consistent with state data

### Scoring Objectivity
- [ ] Per-dimension independent assessment completed
- [ ] Deviations ≥1 point flagged as "disputed"
- [ ] Systematic bias check (too lenient or too harsh)
- [ ] Arithmetic verification of weighted total

### Diagnostic Quality
- [ ] Each issue has root cause analysis, not just symptom description
- [ ] Recommendations are specific and actionable
- [ ] Top Issues priority ordering is reasonable

### Registry Consistency
- [ ] Data written to global registry matches report content
- [ ] Cross-project trend analysis based on real historical data
