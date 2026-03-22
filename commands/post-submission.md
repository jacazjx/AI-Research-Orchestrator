---
name: airesearchorchestrator:post-submission
description: "Post-submission workflow: self-review, rebuttal writing, and post-acceptance materials"
allowed-tools: "Read, Write, Edit, Grep, Glob, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*), Skill"
---

# Post-Submission Workflow

Manage the post-submission lifecycle: pre-submission self-review, rebuttal writing after reviews arrive, and post-acceptance dissemination materials.

## Sub-Commands

| Sub-Command | Skill Invoked | When to Use |
|-------------|---------------|-------------|
| **self-review** | `airesearchorchestrator:self-review` | Before submitting -- run a 6-category quality checklist |
| **rebuttal** | `airesearchorchestrator:rebuttal` | After reviews arrive -- classify comments and draft responses |
| **post-acceptance** | `airesearchorchestrator:post-acceptance` | After acceptance -- generate slides, poster, and social media text |

## Steps

1. **Detect sub-command** -- determine which sub-command the user wants from their input:
   - "self review", "check before submission", "pre-submission review", "投稿自查" --> **self-review**
   - "write rebuttal", "respond to reviews", "reviewer response", "写rebuttal", "回复审稿意见" --> **rebuttal**
   - "post acceptance", "make slides", "make poster", "promote paper", "录用后", "做PPT", "做海报" --> **post-acceptance**
   - If ambiguous, ask the user which sub-command they want.

2. **Read project state** -- load `.autoresearch/state/research-state.yaml` to confirm the paper phase has been reached.

3. **Invoke the appropriate skill**:
   ```
   Skill(skill="airesearchorchestrator:self-review")
   ```
   or
   ```
   Skill(skill="airesearchorchestrator:rebuttal")
   ```
   or
   ```
   Skill(skill="airesearchorchestrator:post-acceptance")
   ```

4. **Report results** -- summarize what was produced:
   - **self-review**: X/6 categories passed, N blocking issues, recommendation
   - **rebuttal**: N reviewer responses drafted, revision changelog complete
   - **post-acceptance**: which materials were generated (slides/poster/social media)

## Usage Examples

```
/post-submission self-review
/post-submission rebuttal
/post-submission post-acceptance
/post-submission make slides
/post-submission 投稿自查
/post-submission 写rebuttal
```

## Output Locations

| Sub-Command | Output Directory | Key Files |
|-------------|------------------|-----------|
| self-review | `paper/` | `self-review-report.md` |
| rebuttal | `paper/rebuttal/` | `reviewer-N-response.md`, `revision-changelog.md`, `meta-review-summary.md` |
| post-acceptance | `paper/presentation/` | `slides-outline.md`, `poster-layout.md`, `social-media-text.md` |

## Prerequisites

- The paper phase should be reached or completed (Gate 3 approved at minimum)
- For rebuttal: reviewer comments must be provided by the user
- For post-acceptance: the paper should be accepted at a venue

**This command does NOT require agent teams -- all sub-commands run as single-agent skills.**
