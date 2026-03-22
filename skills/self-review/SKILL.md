---
name: airesearchorchestrator:self-review
agent: writer
description: "Pre-submission self-review checklist for paper quality assurance. Checks for common issues before submitting to a venue. Use when user says 'self review', '投稿自查', 'check before submission', 'pre-submission review'."
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/*:*)
---
# Pre-Submission Self-Review

## Purpose

Systematic quality assurance checklist for a manuscript before venue submission. Evaluates the paper across six categories, produces a pass/fail report with actionable fixes, and ensures nothing is submitted with avoidable defects.

## When to Use

- After the paper draft is complete and internally reviewed (Gate 4 passed)
- Before uploading to a submission system (OpenReview, CMT, EasyChair, etc.)
- When the user says "self review", "check before submission", "pre-submission review", or "投稿自查"

## Workflow

### Step 1: Gather Inputs

1. **Read the manuscript** -- locate `paper/main.tex` and all `\input` files under `paper/sections/`
2. **Read project state** -- load `.autoresearch/state/research-state.yaml` for venue info and phase context
3. **Read evidence package** -- load `docs/experiments/evidence-package-index.md`
4. **Read citation library** -- load `paper/references.bib`
5. **Read prior review reports** -- check for `paper/reviewer-report.md`, `paper/REVIEW_LOG.md`

### Step 2: Evaluate Six Categories

Run each category check sequentially. For each category, assign **Pass** or **Fail** and list specific issues found.

#### Category 1: Structural Completeness

| Check | Criteria |
|-------|----------|
| Abstract formula | Abstract follows the 5-sentence formula: (1) context/problem, (2) gap/limitation, (3) approach, (4) key result, (5) implication |
| Required sections | All IMRAD sections present: Introduction, Related Work, Method, Experiments, Conclusion |
| Page limit | Total pages (excluding references and appendix) within venue limit |
| Appendix organization | Supplementary material referenced from main text, not orphaned |
| Section balance | No section is disproportionately long or short relative to its importance |

**How to check**: Read all section files, count pages from compiled PDF if available, verify cross-references with `\ref` and `\label` matching.

#### Category 2: Evidence Integrity

| Check | Criteria |
|-------|----------|
| Claim-evidence tracing | Every claim in the paper maps to an approved entry in the evidence package |
| No unsupported statements | No sentences like "significantly improves" without a table/figure reference |
| Statistical reporting | All results include mean +/- std (or CI), sample sizes, and significance tests where applicable |
| Negative results | Any negative or null results are honestly reported, not hidden |
| Ablation coverage | Ablation study covers all major design choices mentioned in the method section |

**How to check**: Cross-reference claims in the text against `docs/experiments/evidence-package-index.md`. Search for superlatives ("significantly", "dramatically", "substantially") and verify each has a quantitative backing.

#### Category 3: Citation Quality

| Check | Criteria |
|-------|----------|
| Verification rate | >= 90% of citations are Grade A (DOI-verified) or Grade B (metadata-verified) |
| No self-generated BibTeX | Every BibTeX entry was fetched from an authoritative source (Semantic Scholar, DBLP, CrossRef), not hand-written by the agent |
| No phantom citations | Every `\cite{}` key in the text has a matching `references.bib` entry |
| No orphan entries | Every `references.bib` entry is cited at least once in the text |
| Recency check | At least 30% of citations are from the last 3 years (for non-foundational references) |

**How to check**: Run `Grep` for `\cite{` in all `.tex` files, extract keys, cross-check against `references.bib`. Read `paper/citation-audit-report.md` if available.

#### Category 4: Writing Quality

| Check | Criteria |
|-------|----------|
| LLM pattern removal | No AI-typical phrases: "delve", "pivotal", "crucial", "paramount", "It is worth noting", "In the realm of", "leveraging" |
| Consistent terminology | Key terms used consistently (e.g., not alternating between "model" and "network" for the same thing) |
| Tense consistency | Related work in present tense, own experiments in past tense, general claims in present |
| Paragraph structure | Each paragraph has a clear topic sentence and supports one main idea |
| Notation consistency | All mathematical symbols defined before first use, no symbol reuse for different meanings |

**How to check**: Search for known LLM phrases using `Grep`. Manually inspect a sample of paragraphs for tense and structure.

#### Category 5: Reproducibility

| Check | Criteria |
|-------|----------|
| Code availability | Paper includes a code/data availability statement (even if anonymous at submission) |
| Hyperparameters | All hyperparameters documented (learning rate, batch size, optimizer, schedule, etc.) |
| Random seeds | Random seeds recorded and reported for all stochastic experiments |
| Compute budget | Training hardware and wall-clock time reported |
| Environment specification | Software versions (PyTorch, CUDA, etc.) documented in appendix or supplementary |

**How to check**: Search for "hyperparameter", "seed", "GPU", "hardware" in the text. Check appendix for implementation details section.

#### Category 6: Venue Compliance

| Check | Criteria |
|-------|----------|
| Formatting | Document class and style match venue requirements (font size, margins, columns) |
| Anonymization | No author names, affiliations, or self-identifying references in the main text (for double-blind venues) |
| Supplementary format | Supplementary material follows venue guidelines (separate PDF, zip, etc.) |
| Required sections | Venue-specific required sections present (e.g., Ethics Statement, Broader Impact, Limitations) |
| File naming | Submission files named according to venue conventions |

**How to check**: Read venue CFP/style guide (from project config or user input). Check `\documentclass` and package usage. Search for author names and affiliations in the compiled text.

### Step 3: Generate Report

Write the self-review report to `paper/self-review-report.md` with the following structure:

```markdown
# Pre-Submission Self-Review Report

**Project**: <project title>
**Venue**: <target venue>
**Date**: <date>
**Overall**: X/6 categories passed

## Summary

| # | Category | Status | Issues |
|---|----------|--------|--------|
| 1 | Structural Completeness | Pass/Fail | N issues |
| 2 | Evidence Integrity | Pass/Fail | N issues |
| 3 | Citation Quality | Pass/Fail | N issues |
| 4 | Writing Quality | Pass/Fail | N issues |
| 5 | Reproducibility | Pass/Fail | N issues |
| 6 | Venue Compliance | Pass/Fail | N issues |

## Category Details

### 1. Structural Completeness -- [Pass/Fail]

- [x] Abstract follows 5-sentence formula
- [ ] **FAIL**: Page limit exceeded by 0.5 pages
  - **Fix**: Shorten Related Work by removing redundant discussion of X
...

## Actionable Fix List (Priority Order)

1. **[BLOCKING]** Fix anonymization leak in Section 3.2, line 147
2. **[HIGH]** Add missing ablation for component Y
3. **[MEDIUM]** Replace LLM phrase "delve into" in Introduction
...

## Recommendation

[ ] Ready to submit
[ ] Fix blocking issues first (N blocking issues)
[ ] Major revision needed (N high-priority issues)
```

### Step 4: Report to User

Present a summary to the user:
- Overall score (X/6 categories passed)
- Number of blocking, high, and medium issues
- Estimated effort to fix (quick fixes vs. substantial work)
- Clear recommendation: submit as-is, fix and submit, or revise further

## Output Files

| File | Location | Purpose |
|------|----------|---------|
| Self-Review Report | `paper/self-review-report.md` | Full checklist results with pass/fail per category and actionable fixes |

## Key Rules

1. **Be honest** -- do not mark a category as Pass if any check within it fails
2. **Be specific** -- every issue must include the file, line/section, and a concrete fix
3. **Prioritize** -- blocking issues (anonymization leaks, missing sections) before style issues
4. **Do not auto-fix** -- report issues only; the user or writer agent decides what to fix
5. **Check the actual files** -- do not rely on memory or assumptions; read and verify every claim
6. **Venue-specific checks** -- if no venue is configured, skip Category 6 and note it in the report
