---
name: airesearchorchestrator:extract-lessons
agent: reflector
description: Extract lessons learned from the research project for future improvement. Use when user says "extract lessons", "lessons learned", "经验总结", or needs to capture project insights.
argument-hint: [project-root]
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(python)
---

## Purpose

Systematically extract lessons learned from the completed research project to improve future projects. Lessons are saved both to the project directory and optionally to the user-level library for cross-project reuse.

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

### Step 6: Save to User Library (NEW)

For transferable lessons, save to user-level library:

```bash
# Save to user library using Python
python3 -c "
from user_library import save_lesson_to_library
save_lesson_to_library(
    lesson_content='''[Lesson content in markdown]''',
    category='methodology',  # or 'process' or 'tools'
    source_project='[project-name]',
    title='[Lesson Title]',
    tags=['tag1', 'tag2'],
)
"
```

Categories:
- **methodology**: Research methodology lessons (experimental design, analysis techniques)
- **process**: Process lessons (workflow, communication, coordination)
- **tools**: Tool lessons (software, hardware, infrastructure)

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
   - Saved to Library: Yes/No

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
- **Save transferable lessons to user library** for cross-project reuse

## User Library Integration

After saving to project, identify transferable lessons and save them:

```python
# Example: Saving a methodology lesson
from user_library import save_lesson_to_library

lesson_content = """
## Problem
When comparing baseline models, we initially used different random seeds for each model.

## Solution
Standardize random seeds across all models before comparison to ensure fair evaluation.

## Impact
Reduced variance in comparison results by 40%, making conclusions more reliable.
"""

save_lesson_to_library(
    lesson_content=lesson_content,
    category="methodology",
    source_project="my-research-project",
    title="Standardize Random Seeds for Fair Baseline Comparison",
    tags=["baselines", "reproducibility", "random-seeds"],
)
```

## Library Location

- Lessons are saved to `~/.autoresearch/lessons-library/`
- Organized by category: methodology, process, tools
- Indexed in `~/.autoresearch/lessons-library/index.yaml`