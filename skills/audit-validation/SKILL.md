---
name: airesearchorchestrator:audit-validation
description: Audit problem validation for evidence quality, significance assessment accuracy, and verdict justification. Use when user says "audit validation", "review problem validation", "审核问题验证", or needs to verify a validation report.
argument-hint: [project-root]
allowed-tools: Read, Grep, Glob
---

## Purpose

Critically review a problem validation report to ensure the evidence is sound, the significance assessment is justified, and the verdict follows logically from the analysis.

## Workflow

### Step 1: Read Validation Report

Read the problem validation report at `docs/reports/pilot/problem-validation-report.md`.

### Step 2: Evidence Quality Check

Evaluate each piece of evidence:

#### Literature Evidence Review
- Is the citation authentic? (verify if possible)
- Does it actually support the problem existence claim?
- Is it recent enough to be relevant?
- Are counter-evidence papers ignored?

#### Data Evidence Review
- Is the data source credible?
- Is the observation statistically significant?
- Could the observation have alternative explanations?

#### Practical Evidence Review
- Are sources verifiable?
- Is there selection bias in evidence gathering?
- Do multiple sources converge on the same conclusion?

### Step 3: Significance Assessment Review

For each dimension:

| Dimension | Check |
|-----------|-------|
| Academic | Is novelty claim justified? Does literature support novelty? |
| Practical | Is real-world impact documented? Any use cases? |
| Timeliness | Is this problem currently relevant? Any recent publications? |
| Feasibility | Are technical capabilities assessed realistically? |

### Step 4: Gap Analysis Review

Verify the gap is real and valuable:

- Is the gap clearly articulated?
- Are previous attempts accurately characterized?
- Is the "our angle" actually different?
- Is the gap worth filling?

### Step 5: Verdict Justification Check

Ensure verdict follows from analysis:

| Verdict | Must Show |
|---------|-----------|
| Validated | Strong evidence + high significance + clear gap |
| Reformulate | Problem is real but poorly scoped |
| Defer | Real problem but currently blocked |
| Pivot | Weak evidence OR low significance OR already solved |

## Output

Provide an audit report as markdown:

```markdown
# Problem Validation Audit Report

## Summary

**Verdict**: [Approved / Needs Revision / Rejected]
**Confidence**: [High / Medium / Low]

## Evidence Quality Assessment

### Literature Evidence
| Citation | Authenticity | Relevance | Quality |
|----------|--------------|-----------|---------|
| [Citation] | Verified/Unverified | Relevant/Weak | Good/Issues |

**Issues Found**:
- [Issue 1]
- [Issue 2]

### Data Evidence
| Source | Credibility | Significance | Quality |
|--------|-------------|--------------|---------|
| [Source] | High/Medium/Low | Yes/No | Good/Issues |

**Issues Found**:
- [Issue 1]

### Practical Evidence
| Source | Verifiable | Supports Claim | Quality |
|--------|------------|----------------|---------|
| [Source] | Yes/No | Yes/Partially/No | Good/Issues |

**Issues Found**:
- [Issue 1]

## Significance Assessment Review

| Dimension | Score Given | Score Justified? | Notes |
|-----------|-------------|------------------|-------|
| Academic | X/5 | Yes/No | [Reason] |
| Practical | X/5 | Yes/No | [Reason] |
| Timeliness | X/5 | Yes/No | [Reason] |
| Feasibility | X/5 | Yes/No | [Reason] |

**Adjustments Needed**:
- [Adjustment 1]

## Gap Analysis Review

- **Gap Clarity**: Clear / Needs Work / Missing
- **Previous Attempts Coverage**: Comprehensive / Partial / Missing
- **Differentiation**: Strong / Weak / Unclear

**Issues Found**:
- [Issue 1]

## Verdict Justification

- **Logical Consistency**: Does verdict follow from evidence? Yes/No
- **Supporting Evidence**: Strong / Moderate / Weak
- **Alternative Verdicts Considered**: Yes/No

## Recommendations

### Must Fix (blocks approval)
1. [Critical issue]

### Should Fix (improves quality)
1. [Important issue]

### Nice to Have
1. [Minor issue]

## Final Assessment

**Approval Status**: [Approved / Approved with Minor Revisions / Needs Major Revision / Rejected]

**Rationale**:
[Summary of why this verdict was reached]

**Next Steps**:
- [Action for researcher]
```

## Key Rules

- MUST verify at least 50% of cited literature if feasible
- MUST challenge weak evidence even if verdict seems correct
- MUST suggest specific improvements if revisions needed
- If evidence is insufficient, recommend appropriate verdict change

## Audit Checklist

- [ ] Problem statement is clear and testable
- [ ] Evidence comes from multiple source types
- [ ] Literature citations are relevant and recent
- [ ] Significance scores are justified
- [ ] Gap is clearly articulated
- [ ] Verdict logically follows from analysis
- [ ] If not validated, clear path forward is provided