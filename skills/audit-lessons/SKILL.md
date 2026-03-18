---
name: airesearchorchestrator:audit-lessons
description: Audit lessons learned for transferability and actionability. Use when user says "audit lessons", "review lessons learned", "审核经验总结", or needs to verify lessons quality.
argument-hint: [lessons-learned-path]
allowed-tools: Read, Write, Edit, Grep, Glob
---

## Purpose

Critically review lessons learned for transferability and practical applicability.

## Workflow

### Step 1: Review Lessons Document

Read `docs/reports/reflection/lessons-learned.md` for content and structure.

### Step 2: Assess What Worked

Evaluate:
- Successes accurately captured
- Root causes identified
- Replicable factors clear

### Step 3: Assess What Didn't Work

Check:
- Issues honestly reported
- Root causes identified
- Not just surface-level observations

### Step 4: Evaluate Transferability

For each lesson:
- Is it project-specific or general?
- What conditions make it applicable?
- How can it be transferred?

### Step 5: Assess Actionability

Check:
- Recommendations are concrete
- Owners/roles identified
- Effort estimates provided

## Output

```markdown
# Lessons Learned Audit Report

## Summary
- **Overall Assessment**: PASS / REVISE_NEEDED / MAJOR_REVISION
- **Honesty Score**: X/10
- **Transferability Score**: X/10
- **Actionability Score**: X/10

## What Worked Review

| Success | Root Cause Identified? | Transferable? | Notes |
|---------|------------------------|---------------|-------|
| [Success 1] | Yes/No | Yes/No | |

**Missing Successes**:
- [Success not documented]

## What Didn't Work Review

| Issue | Honestly Reported? | Root Cause? | Systemic? |
|-------|--------------------| ------------|-----------|
| [Issue 1] | Yes/No | Yes/No | Yes/No |

**Missing Issues**:
- [Issue not documented]

## Transferability Assessment

### Highly Transferable Lessons

1. **[Lesson]**
   - Context: [When applicable]
   - Transfer method: [How to apply elsewhere]
   - Confidence: HIGH/MEDIUM/LOW

### Project-Specific Lessons

1. **[Lesson]**
   - Why specific: [Context]
   - Value as reference: [What can be learned]

### Lessons Needing More Context

1. **[Lesson]**
   - Issue: [What's missing]
   - Need: [What to add]

## Actionability Assessment

| Recommendation | Concrete? | Owner? | Effort? | Status |
|----------------|-----------|--------|---------|--------|
| [Rec 1] | Yes/No | Yes/No | Yes/No | Actionable/Vague |

**Vague Recommendations**:
- [Recommendation needing clarification]

## Metrics Completeness

| Metric | Documented? | Accurate? |
|--------|-------------|-----------|
| Duration | Yes/No | Yes/No |
| Resources | Yes/No | Yes/No |
| Experiments | Yes/No | Yes/No |
| Gate passes | Yes/No | Yes/No |

## Recommendations

1. [Recommendation to improve lessons document]
2. [Recommendation]

## Gate Decision

- [ ] PASS - Lessons are comprehensive and actionable
- [ ] PASS_WITH_FIXES - Minor gaps, address and proceed
- [ ] REVISE - Significant gaps in lessons
- [ ] BLOCK - Lessons not honest or not actionable
```

## Key Rules

- Must include both successes and failures
- Root causes must be identified
- Must distinguish transferable vs specific
- Recommendations must be actionable