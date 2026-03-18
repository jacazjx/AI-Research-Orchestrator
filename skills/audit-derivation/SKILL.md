---
name: airesearchorchestrator:audit-derivation
description: Audit theoretical derivation for mathematical rigor, proof correctness, assumption validity, and completeness. Use when user says "audit derivation", "审核推导", "review theory", or after theoretical derivation is complete.
user-invocable: false
argument-hint: [derivation-report-path]
allowed-tools: Bash(python, sympy), Read, Write, Edit, Grep, Glob
---
# Audit Derivation

## Overview

Critically review theoretical derivations for mathematical rigor, proof correctness, assumption validity, and completeness. This skill ensures that theoretical foundations are sound before proceeding to experimental design.

## Purpose

Verify that:
- Mathematical formalization is correct and precise
- Theorems are stated accurately with all conditions
- Proofs are valid (at least in sketch form)
- Assumptions are justified and reasonable
- Complexity analysis is accurate
- Theoretical gaps are honestly acknowledged

## Workflow

### Stage 1: Formalization Review

#### Step 1.1: Mathematical Object Definitions

For each defined object, verify:

```markdown
## Object Definition Audit

| Object | Notation Clear? | Type Correct? | Properties Valid? |
|--------|-----------------|---------------|-------------------|
| [Name] | Yes/No | Yes/No | Yes/No |

**Issues Found**:
- [Issue 1]
- [Issue 2]
```

**Checklist**:
- [ ] All symbols defined before use
- [ ] Notation is standard and consistent
- [ ] Object types are mathematically valid
- [ ] Properties follow from definitions

#### Step 1.2: Problem Domain Verification

```markdown
## Problem Domain Audit

**Input/Output Spaces**:
- [ ] Input space $\mathcal{X}$ is well-defined
- [ ] Output space $\mathcal{Y}$ is well-defined
- [ ] Function class $\mathcal{F}$ is appropriate

**Assumptions Audit**:

| Assumption | Justified? | Realistic? | Necessary? |
|------------|------------|------------|------------|
| A1 | Yes/No | Yes/No | Yes/No |
| A2 | Yes/No | Yes/No | Yes/No |

**Problematic Assumptions**:
- [Assumption and why problematic]
```

### Stage 2: Theorem and Proof Review

#### Step 2.1: Theorem Statement Review

For each theorem:

```markdown
## Theorem N Audit

**Statement Precision**:
- [ ] Quantifiers (∀, ∃) are used correctly
- [ ] All variables are bound
- [ ] Conditions are clearly stated
- [ ] Conclusion is unambiguous

**Issues**:
- [Issue 1: e.g., "Missing condition on X"]

**Suggested Correction**:
[If applicable, provide corrected statement]
```

#### Step 2.2: Proof Verification

**Proof Audit Framework**:

```markdown
## Proof Audit

**Completeness**:
- [ ] All cases covered
- [ ] Edge cases addressed
- [ ] Base cases established (for induction)

**Correctness**:
- [ ] Each logical step is valid
- [ ] No circular reasoning
- [ ] References to known results are accurate

**Gap Analysis**:

| Step | Claim | Justification | Gap? |
|------|-------|---------------|------|
| 1 | [Claim] | [Reference/Reason] | Yes/No |
| 2 | [Claim] | [Reference/Reason] | Yes/No |

**Critical Gaps**:
- [Gap that undermines the proof]
```

#### Step 2.3: Lemma and Corollary Review

```markdown
## Supporting Results Audit

| Result | Correct? | Properly Used? | Issue |
|--------|----------|----------------|-------|
| Lemma 1 | Yes/No | Yes/No | [Issue if any] |
| Corollary 1 | Yes/No | Yes/No | [Issue if any] |
```

### Stage 3: Complexity Analysis Verification

#### Step 3.1: Time Complexity Check

```markdown
## Time Complexity Audit

**Verification Method**:
- [ ] Manual derivation checked
- [ ] Cross-referenced with literature
- [ ] Edge cases considered

**Per-Operation Analysis**:

| Operation | Claimed | Verified | Discrepancy |
|-----------|---------|----------|-------------|
| [Op 1] | $O(n)$ | Yes/No | [If different] |

**Overall Assessment**:
- Correct / Incorrect / Incomplete
```

#### Step 3.2: Sample Complexity Check

```markdown
## Sample Complexity Audit

**Framework Validity**:
- [ ] Correct complexity framework used
- [ ] Assumptions match framework requirements

**Bound Verification**:
- [ ] Mathematical derivation correct
- [ ] Constants are reasonable
- [ ] Comparison to known results

**Issues**:
- [Issue 1]
```

### Stage 4: Guarantee Verification

#### Step 4.1: Convergence Analysis Review

```markdown
## Convergence Audit

**Setting Appropriateness**:
- [ ] Assumptions match optimization setting
- [ ] Rate type is correctly identified

**Bound Verification**:
- [ ] Proof sketch covers key steps
- [ ] Rate matches known results where applicable
- [ ] No missing conditions

**Comparison Audit**:
| Method | Claimed Rate | Literature Rate | Match? |
|--------|--------------|-----------------|--------|
| Proposed | $O(1/T)$ | [Check papers] | Yes/No |
```

#### Step 4.2: Generalization Bound Review

```markdown
## Generalization Audit

**Framework Check**:
- [ ] Appropriate framework for problem type
- [ ] All framework assumptions satisfied

**Mathematical Correctness**:
- [ ] Derivation follows from framework
- [ ] Constants and terms are meaningful

**Practical Relevance**:
- [ ] Bound provides useful insight
- [ ] Not vacuous for typical problem sizes
```

### Stage 5: Gap Assessment

```markdown
## Gap Assessment

**Conjectures Audit**:

| Conjecture | Plausible? | Evidence Strong? | Risk |
|------------|------------|------------------|------|
| C1 | Yes/No | Yes/No | High/Med/Low |

**Open Questions Assessment**:
- [ ] Gaps are honestly acknowledged
- [ ] Importance correctly assessed
- [ ] Not hiding critical missing pieces

**Risk to Research**:
- [Risk from unproven conjectures]
- [Risk from simplifying assumptions]
```

### Stage 6: Experiment Mapping Review

```markdown
## Experiment Mapping Audit

**Predictions Audit**:

| Prediction | Testable? | Correct Test? | Metric Appropriate? |
|------------|-----------|---------------|---------------------|
| P1 | Yes/No | Yes/No | Yes/No |

**Critical Experiments Assessment**:
- [ ] Assumptions can be tested
- [ ] Boundary conditions covered
- [ ] Comparative predictions fair

**Missing Experiments**:
- [Experiment that should test theory but isn't listed]
```

## Output

Generate audit report:

```markdown
# Theoretical Derivation Audit Report

## Summary
- **Overall Assessment**: PASS / PASS_WITH_REVISIONS / MAJOR_REVISION / BLOCKED
- **Mathematical Rigor**: X/10
- **Proof Correctness**: X/10
- **Assumption Validity**: X/10
- **Completeness**: X/10

## Critical Issues (Must Fix)

1. **[Issue Title]**
   - Location: [Theorem/Section]
   - Problem: [What's wrong]
   - Severity: Critical
   - Suggestion: [How to fix]

## Major Issues (Should Fix)

1. **[Issue Title]**
   - Location: [Where]
   - Problem: [What's wrong]
   - Suggestion: [How to fix]

## Minor Issues (Consider Fixing)

1. **[Issue Title]**
   - Location: [Where]
   - Suggestion: [Fix]

## Dimension Scores

### Mathematical Rigor (X/10)

**Strengths**:
- [Strength 1]

**Weaknesses**:
- [Weakness 1]

### Proof Correctness (X/10)

**Verified**:
- [Theorem 1]: Sketch verified
- [Lemma 1]: Correct

**Gaps Found**:
- [Gap 1]

### Assumption Validity (X/10)

| Assumption | Realistic? | Justified? | Issue |
|------------|------------|------------|-------|
| A1 | Yes | Yes | None |
| A2 | Questionable | Weak | [Issue] |

### Completeness (X/10)

**Covered**:
- [Area 1]

**Missing**:
- [Area 1] - needed because [reason]

## Gate Decision

- [ ] **PASS** - Derivation is sound, proceed to literature survey
- [ ] **PASS_WITH_REVISIONS** - Minor fixes needed, address and proceed
- [ ] **MAJOR_REVISION** - Significant theoretical issues, revise before proceeding
- [ ] **BLOCKED** - Critical errors in formalization or proofs, do not proceed

## Recommendations

1. [Recommendation 1]
2. [Recommendation 2]
```

## Key Rules

1. **Be Rigorous**: Every claim in the derivation must be verified
2. **Be Specific**: Point to exact locations of issues
3. **Be Constructive**: Provide suggestions for fixes, not just complaints
4. **Be Fair**: Acknowledge good work, not just problems
5. **Know Limits**: If uncertain about a proof step, flag for expert review

## Blocking Conditions

Automatically BLOCK when:
- Main theorem statement is imprecise or ambiguous
- Critical proof gap undermines the result
- Assumptions are clearly unrealistic without justification
- Fundamental mathematical errors detected

## Integration

This skill is part of the Survey Phase workflow:

```
define-idea → theoretical-derivation → audit-derivation → research-lit
```

The audit ensures theoretical foundations are sound before extensive literature survey and experimental design.