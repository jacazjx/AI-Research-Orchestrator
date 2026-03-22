---
name: airesearchorchestrator:rebuttal
agent: writer
description: "Write structured rebuttals responding to peer review comments. Classifies comments, drafts responses with evidence, manages revision tracking. Use when user says 'write rebuttal', '写rebuttal', 'respond to reviews', '回复审稿意见', 'reviewer response'."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*)
---
# Rebuttal Writing

## Purpose

Write structured, professional rebuttals responding to peer reviewer comments. This skill classifies each comment, drafts evidence-backed responses, tracks all manuscript revisions, and produces a meta-review summary for the editor or area chair.

## When to Use

- After receiving reviewer comments from a venue (conference or journal)
- When the user says "write rebuttal", "respond to reviews", "reviewer response", "写rebuttal", or "回复审稿意见"
- The user should provide reviewer comments as input (pasted text, uploaded file, or path to a file)

## Workflow

### Step 1: Gather Inputs

1. **Read reviewer comments** -- the user provides reviewer feedback. Accept any format:
   - Direct paste in the conversation
   - Path to a file (e.g., `paper/reviews/reviewer-1.txt`)
   - Multiple reviewers should be handled separately
2. **Read the manuscript** -- load `paper/main.tex` and all section files
3. **Read evidence package** -- load `docs/experiments/evidence-package-index.md`
4. **Read project state** -- load `.autoresearch/state/research-state.yaml` for context
5. **Create output directory** -- ensure `paper/rebuttal/` exists

### Step 2: Comment Classification

For each reviewer, parse their comments and classify each one into exactly one category:

| Category | Definition | Response Priority |
|----------|------------|-------------------|
| **Major** | Substantive concern that questions correctness, completeness, or significance. Requires new evidence, analysis, or rewriting. | Must address with evidence |
| **Minor** | Valid point about clarity, presentation, or minor gaps. Can be fixed with targeted edits. | Address with specific changes |
| **Typo** | Spelling, grammar, formatting, or reference errors. | Fix and acknowledge |
| **Misunderstanding** | Reviewer misread or misinterpreted the paper. The paper is correct but unclear. | Clarify respectfully without being defensive |

Create a classification summary at the top of each reviewer response file:

```markdown
## Comment Classification Summary

| # | Category | Topic | Section |
|---|----------|-------|---------|
| 1 | Major | Missing baseline comparison | 4.2 |
| 2 | Minor | Notation unclear | 3.1 |
| 3 | Misunderstanding | Confused loss function with regularizer | 3.3 |
| 4 | Typo | Figure 3 caption has wrong metric name | 4.1 |
```

### Step 3: Response Drafting

For each comment, draft a response with four components:

1. **Acknowledgment** -- thank the reviewer for the specific point. Be genuine, not formulaic.
2. **Action taken** -- describe what was changed in the manuscript (or explain why no change was needed)
3. **Evidence / Justification** -- provide data, citations, or reasoning that supports the response
4. **Specific changes** -- reference exact sections, paragraphs, or line numbers where edits were made

#### Response Templates by Category

**Major concern:**
```markdown
**R[N]-C[M] (Major): [Reviewer's concern summarized]**

We thank the reviewer for raising this important point.

[Action taken]: We have [added/revised/extended] [specific content] in Section X.Y.

[Evidence]: [New experimental result / additional analysis / citation]. Specifically, [quantitative evidence].

[Changes]: See Section X.Y, paragraph Z (highlighted in blue in the revised manuscript).
```

**Minor concern:**
```markdown
**R[N]-C[M] (Minor): [Reviewer's concern summarized]**

Thank you for this suggestion.

[Action]: We have [clarified/added/revised] [specific content].

[Changes]: Section X.Y, paragraph Z.
```

**Misunderstanding:**
```markdown
**R[N]-C[M] (Misunderstanding): [Reviewer's concern summarized]**

We appreciate the reviewer's careful reading. We believe this may be a misunderstanding, and we take responsibility for the lack of clarity in our original text.

[Clarification]: [Explain what the paper actually says/means, with specific references].

[Action]: To prevent this confusion, we have [rewritten/added clarification to] Section X.Y.
```

**Typo:**
```markdown
**R[N]-C[M] (Typo): [Error identified]**

Thank you. Fixed in the revised manuscript.
```

### Step 4: Tone Optimization

Review all drafted responses and verify:

| Principle | Check |
|-----------|-------|
| **Professional** | No informal language, no sarcasm, no passive aggression |
| **Grateful** | Each response opens with genuine acknowledgment |
| **Non-defensive** | Even when the reviewer is wrong, the response does not attack or dismiss |
| **Address the underlying concern** | If the specific criticism is incorrect, still address what confused the reviewer |
| **Concise** | Responses are focused and do not ramble or over-explain |
| **Evidence-first** | Claims in responses are backed by data, not assertions |

Common tone pitfalls to avoid:
- "The reviewer is mistaken" -- instead: "We may not have made this clear enough"
- "As clearly stated in Section X" -- instead: "We have clarified this in Section X"
- "We disagree" -- instead: "We respectfully offer an alternative perspective, supported by..."

### Step 5: Revision Tracking

Create a change log mapping every reviewer comment to its corresponding manuscript change:

```markdown
# Revision Changelog

## Overview

| Statistic | Count |
|-----------|-------|
| Total comments received | N |
| Major concerns addressed | N |
| Minor concerns addressed | N |
| Typos fixed | N |
| Misunderstandings clarified | N |
| New experiments added | N |
| Sections rewritten | N |

## Change Log

| Comment ID | Category | Manuscript Change | Location |
|------------|----------|-------------------|----------|
| R1-C1 | Major | Added baseline comparison with method X | Section 4.2, Table 3 |
| R1-C2 | Minor | Clarified notation for loss function | Section 3.1, Eq. 4 |
| R2-C1 | Misunderstanding | Rewrote paragraph on regularization | Section 3.3, para 2 |
| R2-C2 | Typo | Fixed metric name in Figure 3 caption | Figure 3 |
```

### Step 6: Meta-Review Summary

Write a one-paragraph summary for the editor or area chair that:
- Acknowledges the reviewers' efforts
- Summarizes the key changes made
- Highlights the most significant improvements
- States confidence that the concerns have been addressed

Keep this to 150-250 words.

### Step 7: Write Output Files

Save all artifacts to `paper/rebuttal/`:

| File | Content |
|------|---------|
| `reviewer-1-response.md` | Classified comments and drafted responses for Reviewer 1 |
| `reviewer-2-response.md` | Classified comments and drafted responses for Reviewer 2 |
| `reviewer-N-response.md` | (One file per reviewer) |
| `revision-changelog.md` | Complete mapping of comments to manuscript changes |
| `meta-review-summary.md` | One-paragraph summary for editor/AC |

If there is only one reviewer, still use the `reviewer-1-response.md` naming convention.

## Output Files

| File | Location | Purpose |
|------|----------|---------|
| Reviewer Responses | `paper/rebuttal/reviewer-N-response.md` | Per-reviewer classified comments and responses |
| Revision Changelog | `paper/rebuttal/revision-changelog.md` | Comment-to-change mapping |
| Meta-Review Summary | `paper/rebuttal/meta-review-summary.md` | Editor/AC summary paragraph |

## Key Rules

1. **Never be dismissive** -- every reviewer comment deserves a respectful, substantive response, even typo reports
2. **Never fabricate evidence** -- if a requested experiment was not run, say so and explain why (or offer to run it)
3. **Address the underlying concern** -- even when the specific criticism is technically incorrect, identify what confused the reviewer and fix the clarity issue
4. **Be specific about changes** -- vague responses like "we have improved the paper" are unacceptable; cite exact sections, equations, tables, or figures
5. **Do not modify the manuscript directly** -- this skill drafts responses and documents changes. Actual manuscript edits should be done separately by the writer agent or user
6. **Preserve reviewer numbering** -- use the venue's reviewer numbering (R1, R2, etc.) consistently throughout all files
7. **Separate opinion from evidence** -- when disagreeing with a reviewer, present data first, interpretation second
