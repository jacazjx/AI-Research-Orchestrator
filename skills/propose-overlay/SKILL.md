---
name: autoresearch:propose-overlay
agent: reflector
description: Propose system improvements through prompt modifications and workflow changes. Use when user says "propose overlay", "system improvement", "系统改进", or needs to suggest orchestrator enhancements.
argument-hint: [lessons-learned-path]
allowed-tools: Read, Write, Edit, Grep, Glob
---

## Purpose

Propose concrete improvements to the orchestrator system based on lessons learned, with safety assessment.

## Workflow

### Step 1: Review Lessons Learned

Read `docs/reports/reflection/lessons-learned.md` for:
- Systemic issues
- Process improvements
- Tool limitations

### Step 2: Identify Improvement Areas

Map lessons to potential changes:
- Prompt improvements
- Workflow modifications
- Tool integrations
- Documentation updates

### Step 3: Draft Proposals

For each improvement:
- Current state
- Proposed change
- Expected benefit
- Implementation approach

### Step 4: Assess Risks

Evaluate each proposal:
- Safety implications
- Backward compatibility
- Edge cases
- Rollback plan

### Step 5: Prioritize

Rank by:
- Impact potential
- Implementation effort
- Risk level
- Dependencies

## Output

Save to `docs/reports/reflection/overlay-draft.md`:

```markdown
# Overlay Draft

## Overview
[Summary of proposed system improvements]

## Proposed Changes

### Change 1: [Title]

**Type**: Prompt / Workflow / Tool / Documentation

**Current State**:
[Description of how things work now]

**Proposed Change**:
[Description of the proposed improvement]

**Rationale**:
[Why this change, based on lessons learned]

**Expected Benefit**:
[Quantified or qualitative expected improvement]

**Implementation**:
```yaml
# Configuration or prompt change
type: prompt_modification
target: agents/survey/PROMPT.md
action: append
content: |
  [New prompt content]
```

**Risk Assessment**:
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk] | Low/Medium/High | Low/Medium/High | [Mitigation] |

**Rollback Plan**:
[How to revert if problems occur]

---

### Change 2: [Title]
[Same structure as Change 1]

---

## Safety Checklist

Before activation, verify:

- [ ] All changes have rollback procedures
- [ ] No changes bypass human gates
- [ ] Changes are additive, not destructive
- [ ] Edge cases considered
- [ ] Documentation updated

## Testing Plan

| Test | Method | Expected Result |
|------|--------|-----------------|
| [Test] | [Method] | [Expected] |

## Activation Sequence

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Monitoring

Post-activation metrics to track:
- [Metric 1]
- [Metric 2]

## Approval Request

**Proposed by**: [Agent role]
**Date**: [Date]
**Review required**: Yes/No
**Risk level**: Low/Medium/High

### Decision (to be filled by Curator)

- [ ] APPROVE - Safe to activate
- [ ] APPROVE WITH MODIFICATIONS - See notes
- [ ] REJECT - See notes
- [ ] DEFER - Requires more analysis

**Notes**:
[Curator's notes]

## Appendix: Full Diff

```diff
[Complete diff of all changes]
```
```

## Key Rules

- NEVER propose changes that bypass human gates
- MUST include rollback plan for every change
- MUST assess safety implications
- Changes must be reviewed by Curator before activation