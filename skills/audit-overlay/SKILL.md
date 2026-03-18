---
name: airesearchorchestrator:audit-overlay
description: Audit proposed system improvements for safety, backward compatibility, and rollback capability. Use when user says "audit overlay", "review overlay", "审核系统改进", or needs to verify overlay safety.
argument-hint: [overlay-draft-path]
allowed-tools: Read, Write, Edit, Grep, Glob
---

## Purpose

Critically review proposed system improvements for safety and proper procedure.

## Workflow

### Step 1: Review Overlay Draft

Read `docs/reports/reflection/overlay-draft.md` for proposed changes.

### Step 2: Assess Safety

Evaluate each change:
- Could it bypass human gates?
- Could it cause data loss?
- Could it affect existing projects?
- Are edge cases considered?

### Step 3: Check Backward Compatibility

Verify:
- Existing projects will still work
- No breaking changes to interfaces
- Migration path if needed

### Step 4: Review Rollback Plan

Ensure:
- Rollback procedure documented
- Rollback tested or verified
- No irreversible changes

### Step 5: Validate Testing Plan

Check:
- Test coverage adequate
- Edge cases tested
- Monitoring defined

## Output

```markdown
# Overlay Audit Report

## Summary
- **Overall Assessment**: APPROVE / APPROVE_WITH_MODIFICATIONS / REJECT / DEFER
- **Safety Score**: X/10
- **Backward Compatibility**: YES / PARTIAL / NO
- **Rollback Capability**: YES / PARTIAL / NO

## Safety Assessment

### Change-by-Change Analysis

| Change | Bypasses Gates? | Data Risk? | Edge Cases? | Safety |
|--------|-----------------|------------|-------------|--------|
| [Change 1] | Yes/No | Low/High | Yes/No | SAFE/UNSAFE |

### Safety Concerns

| Change | Concern | Severity | Mitigation |
|--------|---------|----------|------------|
| [Change] | [Concern] | HIGH/MEDIUM/LOW | [Suggested mitigation] |

## Backward Compatibility

| Aspect | Compatible? | Notes |
|--------|-------------|-------|
| Existing projects | Yes/No | |
| Interfaces | Yes/No | |
| Configs | Yes/No | |

**Breaking Changes**:
- [Change and impact]

**Migration Required**:
- [What needs migration]

## Rollback Assessment

| Change | Rollback Plan | Tested? | Recovery Time |
|--------|---------------|---------|---------------|
| [Change 1] | [Plan] | Yes/No | [Time] |

**Irreversible Changes**:
- [Change that cannot be rolled back]

## Testing Plan Review

| Test | Adequate? | Edge Cases? | Notes |
|------|-----------|-------------|-------|
| [Test 1] | Yes/No | Yes/No | |

**Missing Tests**:
- [Test that should be added]

## Monitoring Plan

| Metric | Defined? | Threshold? | Alert? |
|--------|----------|------------|--------|
| [Metric] | Yes/No | Yes/No | Yes/No |

## Gate Bypass Check

- [ ] No changes bypass human gates
- [ ] No changes auto-approve phase transitions
- [ ] No changes modify state without logging
- [ ] No changes suppress audit skills

## Recommendations

1. [Modification or concern]
2. [Modification or concern]

## Final Decision

- [ ] APPROVE - Safe to activate as proposed
- [ ] APPROVE_WITH_MODIFICATIONS - See recommendations
- [ ] REJECT - Unsafe changes, do not activate
- [ ] DEFER - Needs more analysis

**Curator Notes**:
[Detailed notes on decision]

## Activation Conditions

If approved, activate only when:
1. [Condition 1]
2. [Condition 2]

## Post-Activation Monitoring

Must monitor for:
- [Metric or behavior]
- [Metric or behavior]
```

## Key Rules

- MUST NOT approve changes that bypass human gates
- MUST NOT approve irreversible changes without justification
- Rollback plan must be documented and verified
- All safety concerns must be addressed