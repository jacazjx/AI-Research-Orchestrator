---
name: airesearchorchestrator:extract-lessons
agent: reflector
description: Extract lessons learned from the research project for future improvement. Use when user says "extract lessons", "lessons learned", "经验总结", or needs to capture project insights.
argument-hint: [project-root]
allowed-tools: Read, Write, Edit, Grep, Glob
---

## Purpose

Systematically extract lessons learned from the completed research project to improve future projects.

## Workflow

### Step 1: Review Project Artifacts

Read key documents:
- Research state file
- Phase scorecards
- Gate decisions
- Communication logs

### Step 2: Identify What Worked

Catalog successful approaches:
- Methodology wins
- Process improvements
- Tool effectiveness
- Communication patterns

### Step 3: Identify What Didn't Work

Document issues:
- Methodology problems
- Process bottlenecks
- Tool limitations
- Communication gaps

### Step 4: Analyze Root Causes

For each issue:
- Why did it happen?
- What could have prevented it?
- Is it systemic or specific?

### Step 5: Generate Recommendations

Create actionable improvements:
- Process changes
- Tool improvements
- Training needs
- Resource adjustments

## Output

Save to `docs/reports/reflection/lessons-learned.md`:

```markdown
# Lessons Learned

## Executive Summary
[Top 3 lessons for quick reference]

## What Worked Well

### Methodology Successes

| Approach | Outcome | Evidence |
|----------|---------|----------|
| [Approach] | [Outcome] | [Evidence] |

### Process Wins

| Process | Benefit | Replication Tips |
|---------|---------|------------------|
| [Process] | [Benefit] | [Tips] |

### Tool Effectiveness

| Tool | Use Case | Value |
|------|----------|-------|
| [Tool] | [Use Case] | [Value] |

## What Didn't Work Well

### Methodology Issues

| Issue | Impact | Root Cause |
|-------|--------|------------|
| [Issue] | [Impact] | [Cause] |

### Process Problems

| Problem | Effect | Frequency |
|---------|--------|-----------|
| [Problem] | [Effect] | [Frequency] |

### Tool Limitations

| Tool | Limitation | Workaround |
|------|------------|------------|
| [Tool] | [Limitation] | [Workaround] |

## Root Cause Analysis

### Systemic Issues
1. [Issue and pattern]
2. [Issue and pattern]

### Project-Specific Issues
1. [Issue and context]

## Recommendations

### High Priority

| Recommendation | Impact | Effort | Owner |
|----------------|--------|--------|-------|
| [Recommendation] | High/Medium/Low | High/Medium/Low | [Role] |

### Medium Priority

| Recommendation | Impact | Effort |
|----------------|--------|--------|
| [Recommendation] | Medium | Low |

## Transferability Assessment

### Lessons Applicable to Other Projects

1. **[Lesson Category]**
   - Context: [When this applies]
   - Lesson: [The actual lesson]
   - Application: [How to apply]

### Lessons Specific to This Project

1. **[Lesson]**
   - Why specific: [Context]
   - Value: [Still useful as reference]

## Metrics Summary

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total duration | X weeks | Y weeks | +/-Z |
| GPU hours used | X | Y | +/-Z |
| Experiments run | X | Y | +/-Z |
| Gate passes first try | X/Y | Y | +/-Z |

## Action Items

- [ ] [Action item 1]
- [ ] [Action item 2]
- [ ] [Action item 3]
```

## Key Rules

- Must include both positive and negative lessons
- Recommendations must be actionable
- Distinguish systemic vs project-specific issues
- Include metrics for objective assessment