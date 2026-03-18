---
name: airesearchorchestrator:insight
description: "Interactive intent clarification — helps users sharpen their research idea before initialization"
argument-hint: "[--idea <string>] [--project-root <path>] [--interactive] [--max-rounds <number>] [--json]"
allowed-tools: "Read, Write, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*)"
---

# Interactive Intent Clarification

Engages the user in a focused Q&A loop to surface and sharpen the true research intent before committing to a project. Run this **before** `/init-research`.

## Execution

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/run_insight.py" $ARGUMENTS
```

## Usage

```bash
# Interactive clarification (default)
python3 scripts/run_insight.py

# Provide an initial idea
python3 scripts/run_insight.py --idea "I want to study time-series forecasting"

# Point at an existing project
python3 scripts/run_insight.py --project-root /abs/path/to/project

# Non-interactive assessment only (outputs JSON)
python3 scripts/run_insight.py --idea "research idea" --interactive false --json
```

## Use Cases

- Clarify a vague or broad research direction
- Validate feasibility before initializing a full project
- Identify constraints (deadline, venue, resources) early
- Surface novelty gaps before the literature survey

## Five-Dimension Assessment

| Dimension | Weight | Key question |
|-----------|--------|--------------|
| Problem | 25% | What specific problem are you solving, and why does it matter? |
| Solution | 25% | What approach or intuition do you have in mind? |
| Contribution | 20% | What type of contribution? What is the success criterion? |
| Constraints | 15% | What time, resource, or venue constraints apply? |
| Novelty | 15% | How is this different from existing work? What is the key insight? |

## Clarity Thresholds

| Score | Status | Recommendation |
|-------|--------|----------------|
| >= 0.7 | Clear | Proceed to `/init-research` |
| 0.4–0.7 | Needs work | Continue Q&A rounds |
| < 0.4 | Too vague | Brainstorm before proceeding |