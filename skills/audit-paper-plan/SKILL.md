---
name: airesearchorchestrator:audit-paper-plan
agent: reviewer
description: Audit paper outline for claim-evidence alignment, structure completeness, and citation scaffolding. Use when user says "audit paper plan", "review paper outline", "审核论文大纲", or needs to verify paper planning.
argument-hint: [paper-plan-path]
allowed-tools: Read, Write, Edit, Grep, Glob
---

## Purpose

Critically review paper outline for structural soundness and claim-evidence alignment.

## Workflow

### Step 1: Review Paper Plan

Read `paper/PAPER_PLAN.md` for structure, claims, and figure plan.

### Step 2: Assess Claim-Evidence Matrix

Evaluate:
- All claims have supporting evidence
- Evidence mapped to experiments
- Gaps in evidence identified

### Step 3: Review Section Structure

Check:
- Logical flow
- Standard paper sections
- Appropriate length distribution

### Step 4: Evaluate Figure/Table Plan

Assess:
- Key figures identified
- Tables for main results
- Supporting materials adequate

### Step 5: Check Citation Scaffolding

Verify:
- Key citations identified
- Missing citations noted
- Citation categories clear

## Output

```markdown
# Paper Plan Audit Report

## Summary
- **Overall Assessment**: PASS / REVISE_NEEDED / MAJOR_REVISION
- **Claim-Evidence Alignment**: X/10
- **Structure Completeness**: X/10

## Claim-Evidence Matrix Review

| Claim | Evidence | Experiment | Status |
|-------|----------|------------|--------|
| [Claim 1] | [Evidence] | [Exp ID] | Supported/Gap |

**Unsupported Claims**:
- [Claim without evidence]

**Evidence Gaps**:
- [Missing evidence for claim]

## Section Structure Review

| Section | Planned | Appropriate? | Notes |
|---------|---------|--------------|-------|
| Abstract | Yes/No | Yes/No | |
| Introduction | Yes/No | Yes/No | |
| Related Work | Yes/No | Yes/No | |
| Method | Yes/No | Yes/No | |
| Experiments | Yes/No | Yes/No | |
| Conclusion | Yes/No | Yes/No | |

**Missing Sections**:
- [Section]

## Figure/Table Plan Review

| Item | Type | Purpose | Adequate? |
|------|------|---------|-----------|
| Fig 1 | Diagram/Plot | [Purpose] | Yes/No |

**Missing Figures**:
- [Figure that should be included]

## Citation Scaffolding

| Category | Count | Key Papers | Missing? |
|----------|-------|------------|----------|
| Foundation | X | [Papers] | Yes/No |
| Related Work | X | [Papers] | Yes/No |
| Baselines | X | [Papers] | Yes/No |

**Missing Citations**:
- [Paper that should be cited]

## Recommendations

1. [Recommendation]
2. [Recommendation]

## Gate Decision

- [ ] PASS - Plan is sound, proceed to writing
- [ ] PASS_WITH_FIXES - Minor gaps, address and proceed
- [ ] REVISE - Significant structural issues
- [ ] BLOCK - Claims not supported by evidence
```

## Key Rules

- Every claim must have supporting evidence
- Missing standard sections are critical
- Figure plan must cover all key results
- Citations must be scaffolding for related work