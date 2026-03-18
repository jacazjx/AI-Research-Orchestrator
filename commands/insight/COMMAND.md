---
name: airesearchorchestrator:insight
description: "Interactive intent clarification — helps users sharpen their research idea before initialization"
script: scripts/run_insight.py
triggers:
  - "insight"
  - "澄清意图"
  - "明确想法"
  - "clarify intent"
  - "研究想法"
phase: init
agents: []
arguments:
  required: []
  optional:
    - name: project-root
      description: Absolute path to research project root (auto-detected if omitted)
      type: path
    - name: idea
      description: Initial research idea
      type: string
    - name: interactive
      description: Enable interactive Q&A mode
      type: boolean
      default: true
    - name: max-rounds
      description: Maximum clarification rounds
      type: int
      default: 5
    - name: json
      description: Output JSON format
      type: boolean
      default: false
---

# Interactive Intent Clarification

Engages the user in a focused Q&A loop to surface and sharpen the true research intent before committing to a project. Run this **before** `/init-research`.

## Use Cases

- Clarify a vague or broad research direction
- Validate feasibility before initializing a full project
- Identify constraints (deadline, venue, resources) early
- Surface novelty gaps before the literature survey

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

## Execution Flow

```
/insight
    │
    ├─→ 1. Detect existing project
    │       ├─→ Found: continue clarifying the existing idea
    │       └─→ Not found: collect idea from scratch
    │
    ├─→ 2. Clarity assessment (five dimensions)
    │       ├── Problem (25%)
    │       ├── Solution (25%)
    │       ├── Contribution (20%)
    │       ├── Constraints (15%)
    │       └── Novelty (15%)
    │
    ├─→ 3. Generate targeted questions
    │       └─→ Focus on lowest-scoring dimensions
    │
    ├─→ 4. Interactive Q&A loop
    │       └─→ Until clarity >= 0.7 or max rounds reached
    │
    ├─→ 5. Recommend next step
    │       └─→ clarity < 0.4: suggest /idea-brainstorm
    │
    └─→ 6. Output clarification result
            ├── Sharpened idea statement
            ├── Clarity score
            ├── Per-dimension scores
            └── Recommended next action
```

## Five-Dimension Assessment

| Dimension | Weight | Key question |
|-----------|--------|--------------|
| Problem | 25% | What specific problem are you solving, and why does it matter? |
| Solution | 25% | What approach or intuition do you have in mind? |
| Contribution | 20% | What type of contribution? What is the success criterion? |
| Constraints | 15% | What time, resource, or venue constraints apply? |
| Novelty | 15% | How is this different from existing work? What is the key insight? |

## Output Example

```
💡 Intent Clarification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current idea:
"I want to study optimization methods for time-series forecasting"

Clarity: 0.35/1.0 (needs further clarification)

Dimension scores:
  Problem:      0.3 ████████░░░░░░░░░░░░
  Solution:     0.2 ██████░░░░░░░░░░░░░░
  Contribution: 0.4 ████████████░░░░░░░░
  Constraints:  0.3 ████████░░░░░░░░░░░░
  Novelty:      0.5 ███████████████░░░░░

Question 1: What specific failure mode are you targeting?
  (e.g. accuracy degrades on long horizons? high compute cost? poor generalization?)

> Accuracy degrades badly when the forecast horizon exceeds 100 steps

...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sharpened idea:
"Improve long-horizon time-series forecasting (>100 steps) accuracy by
proposing an enhanced attention mechanism that better captures long-range
dependencies. Target venue: ICML 2026 (deadline: May 2026)."

Clarity: 0.78/1.0 ✅

Recommended next step:
  Run /init-research to initialize the project with this idea.
```

## Clarity Thresholds

| Score | Status | Recommendation |
|-------|--------|----------------|
| >= 0.7 | Clear | Proceed to `/init-research` |
| 0.4–0.7 | Needs work | Continue Q&A rounds |
| < 0.4 | Too vague | Brainstorm before proceeding |

## Relationship to Other Commands

- **`/init-research`** — run after `/insight`; internally also calls insight if no idea is provided
- **`/configure`** — can update the idea after initialization
