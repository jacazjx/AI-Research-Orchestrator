---
name: airesearchorchestrator:audit-system-evaluation
agent: curator
description: "Audit the system evaluation report for objectivity, evidence quality, and scoring accuracy. Use after Reflector completes system evaluation."
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Audit System Evaluation

## Purpose

Independently verify the Reflector's system evaluation report for objectivity, evidence completeness, and scoring accuracy. Detect and correct self-leniency bias.

## Prerequisites

- Reflector has sent `{"type": "system_eval_ready", "path": "..."}` message
- System evaluation report exists at `docs/reflection/system-evaluation-report.md`

## Workflow

### Step 1: Independent Evidence Review

Read the same data sources the Reflector used:

- `.autoresearch/state/research-state.yaml`
- All phase scorecards
- Core deliverables per phase

Form your own independent judgment on each dimension before reading the Reflector's scores.

### Step 2: Score Comparison

For each of the 6 dimensions:

1. Record your independent score
2. Read the Reflector's score and evidence
3. Calculate the deviation (Reflector score - your score)
4. Flag dimensions with deviation ≥ 1 point as "disputed"

### Step 3: Bias Detection

Check for systematic patterns:
- Count how many dimensions the Reflector scored higher than your assessment
- If ≥ 3 dimensions are scored ≥ 1 point higher → flag "systematic self-leniency"
- If ≥ 3 dimensions are scored ≥ 1 point lower → flag "excessive self-criticism"

### Step 4: Evidence Audit

For each dimension, verify:
- [ ] Score references specific state data or deliverable content
- [ ] No vague "as observed" statements without concrete evidence
- [ ] Quantitative metrics match actual state data
- [ ] Diagnosis identifies root causes, not just symptoms
- [ ] Recommendations are specific and actionable

### Step 5: Arithmetic Verification

- Verify weighted total calculation is correct
- Verify recommendation maps correctly to the total score

### Step 6: Registry Consistency Check

If the report includes cross-project trend data:
- Verify historical data matches the global registry
- Flag any inconsistencies

### Step 7: Issue Audit Report

Send findings to the Reflector:

```
SendMessage(to="reflector", message={
    "type": "eval_audit",
    "decision": "approve" | "revise",
    "disputes": [
        {
            "dimension": "<dimension_name>",
            "reflector_score": <score>,
            "curator_score": <score>,
            "rationale": "<why the curator disagrees>"
        }
    ],
    "bias_detected": "<none|self_leniency|excessive_criticism>",
    "evidence_issues": ["<list of evidence gaps>"],
    "arithmetic_errors": ["<list of calculation errors>"]
})
```

## Decision Criteria

- **APPROVE**: All scores within ±1 of independent assessment, evidence complete, arithmetic correct
- **REVISE**: Any disputed dimensions, evidence gaps, or calculation errors exist

## Hard Rules

1. **Independent first** — Form your own scores BEFORE reading the Reflector's report
2. **Evidence-based disagreement** — Every disputed score must cite specific counter-evidence
3. **No rubber-stamping** — Even if scores seem reasonable, verify the evidence trail
4. **Arithmetic matters** — Always recalculate the weighted total independently
5. **Do not modify the report** — Send findings via message; the Reflector makes corrections
