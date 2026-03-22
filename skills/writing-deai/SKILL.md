---
name: airesearchorchestrator:writing-deai
agent: writer
description: "Detect and remove LLM writing patterns from paper drafts. Scores text for AI-likeness and suggests human-sounding alternatives. Use when user says 'check AI writing', '去AI痕迹', 'deAI', 'remove AI patterns', 'humanize writing', 'anti-AI check'."
allowed-tools: Read, Write, Edit, Grep, Glob
---
# Writing De-AI

## Purpose

Scan paper drafts for telltale signs of LLM-generated text and provide specific, actionable rewrites. The goal is not to hide AI assistance but to ensure the writing reflects the researcher's authentic voice and meets the quality bar of human-written academic prose.

## When to Use

- After drafting any paper section with AI assistance
- Before submission, as a complement to the self-review skill
- When the user says "check AI writing", "deAI", "remove AI patterns", "humanize writing", "anti-AI check", or "去AI痕迹"

## Detection Categories (10 categories, 5 points each = 50 total)

### 1. Hedging Overuse (5 pts)

- Excessive "it is worth noting", "it should be noted", "importantly"
- Redundant qualifiers: "quite", "rather", "somewhat", "arguably"
- Score: 5 = no issues, 0 = pervasive hedging

**Detection keywords**: "it is worth noting", "it should be noted", "importantly", "notably", "interestingly", "quite", "rather", "somewhat", "arguably", "it bears mentioning"

### 2. Formulaic Transitions (5 pts)

- "Furthermore", "Moreover", "Additionally" used as paragraph openers
- "In conclusion", "To summarize", "In summary" without adding value
- Mechanistic paragraph structure (topic sentence, 3 support sentences, wrap-up)
- Score: 5 = natural flow, 0 = every paragraph follows formula

**Detection keywords**: paragraph-initial "Furthermore,", "Moreover,", "Additionally,", "In conclusion,", "To summarize,", "In summary,", "It is important to note that"

### 3. Superlative Claims (5 pts)

- "groundbreaking", "novel", "revolutionary", "state-of-the-art" without evidence
- "significantly outperforms" without statistical significance test
- "first to" claims without thorough literature check
- Score: 5 = appropriately qualified, 0 = unreasonable claims

**Detection keywords**: "groundbreaking", "novel", "revolutionary", "state-of-the-art", "cutting-edge", "unprecedented", "significantly outperforms", "dramatically improves", "first to"

### 4. Passive Voice Excess (5 pts)

- Overuse of "is shown", "was performed", "has been demonstrated"
- Guidelines: passive OK for methods, active preferred for contributions
- Score: 5 = balanced, 0 = entirely passive

**Detection pattern**: Count sentences with passive constructions ("is/was/are/were/has been/have been" + past participle) outside the Methods section. Flag if passive ratio exceeds 60% in Introduction, Discussion, or Conclusion.

### 5. Generic Filler (5 pts)

- "In recent years, X has gained significant attention"
- "With the rapid development of deep learning"
- "plays a crucial/pivotal/vital role"
- "has shown great/remarkable/promising results"
- Score: 5 = specific openings, 0 = generic filler throughout

**Detection keywords**: "in recent years", "has gained significant attention", "with the rapid development of", "plays a crucial role", "plays a pivotal role", "plays a vital role", "has shown great promise", "has shown remarkable results", "has attracted considerable interest", "has emerged as a promising", "in the realm of", "in the landscape of", "leveraging the power of"

### 6. Uniform Sentence Length (5 pts)

- Every sentence approximately the same length (15-25 words)
- No short punchy sentences, no complex multi-clause sentences
- Natural writing varies: 5-40 word range
- Score: 5 = varied rhythm, 0 = monotonous length

**Detection method**: Compute sentence word counts per paragraph. If the standard deviation of sentence length within a paragraph is below 4 words for 3+ consecutive paragraphs, flag it. Check for absence of any sentence under 8 words or over 35 words in extended sections.

### 7. Over-Enumeration (5 pts)

- Excessive use of "(1)... (2)... (3)..." or "first... second... third..."
- Bullet points where prose would be more natural
- Numbered lists in discussion/conclusion sections
- Score: 5 = appropriate structure, 0 = everything is a list

**Detection method**: Count enumeration markers per section. Flag if Discussion or Conclusion sections contain numbered lists. Flag if more than 30% of paragraphs in the paper use enumeration.

### 8. Vocabulary Uniformity (5 pts)

- Same word/phrase repeated instead of natural variation
- Or: suspiciously perfect synonym rotation (also an AI tell)
- Technical terms should be consistent; non-technical language should vary naturally
- Score: 5 = natural vocabulary, 0 = robotic repetition or rotation

**Detection method**: For non-technical adjectives and adverbs, check whether the same word appears more than 5 times per 1000 words. Also check for mechanical synonym cycling (e.g., "effective"/"efficient"/"efficacious" in strict alternation).

### 9. Missing Personality (5 pts)

- No opinions, no voice, no perspective
- Everything reads as "balanced" with no clear stance
- Compare: good human writing takes positions and defends them
- Score: 5 = clear authorial voice, 0 = anonymous encyclopedic tone

**Detection method**: Check for first-person plural usage ("we argue", "we believe", "our key insight"). Check for evaluative language that takes a position ("the main limitation of X is", "this approach fails to account for", "a more natural choice is"). Absence of both signals missing personality.

### 10. Citation Integration (5 pts)

- Citations only appear at end of sentences: "... [1]."
- No inline discussion: "As Smith et al. showed in their seminal work on X..."
- No critical engagement: just listing, never analyzing
- Score: 5 = citations woven into argument, 0 = perfunctory citation dumps

**Detection method**: Count citations that appear only as terminal references (sentence-final `\cite{}`). Flag if more than 80% of citations are terminal. Check for presence of critical phrases near citations ("however, X fails to", "unlike Y, which assumes", "building on the insight of Z").

## Workflow

### Step 1: Gather Inputs

1. **Read the manuscript** -- locate `paper/main.tex` and all `\input` files under `paper/sections/`. Also check for Markdown drafts under `paper/`.
2. **Read project state** -- load `.autoresearch/state/research-state.yaml` for phase context.

### Step 2: Scan and Score

For each section of the paper, evaluate all 10 detection categories:

1. **Hedging Overuse** -- search for hedging phrases, count occurrences per 1000 words.
2. **Formulaic Transitions** -- check paragraph openers, look for mechanical structure.
3. **Superlative Claims** -- search for unsupported superlatives, check if evidence is nearby.
4. **Passive Voice Excess** -- estimate passive vs. active ratio per section.
5. **Generic Filler** -- search for stock phrases, especially in Introduction and Related Work.
6. **Uniform Sentence Length** -- compute sentence length variance per paragraph.
7. **Over-Enumeration** -- count enumeration patterns, flag inappropriate list usage.
8. **Vocabulary Uniformity** -- check repetition frequency and synonym rotation.
9. **Missing Personality** -- check for authorial voice markers.
10. **Citation Integration** -- analyze citation placement patterns.

Assign a score of 0-5 for each category. Record specific sentences/paragraphs that triggered each detection.

### Step 3: Identify Top Issues

Rank all detected issues by severity. Select the 5 worst offenders -- the specific passages that most strongly signal AI-generated text.

### Step 4: Generate Rewrites

For each of the top 5 issues, provide:
- The original text (exact quote)
- Which category it violates and why
- A concrete suggested rewrite that preserves the technical meaning

### Step 5: Write Report

Output the full report to `paper/writing-deai-report.md`.

## Scoring Guide

- **40-50**: Minimal AI patterns -- ready for submission
- **30-39**: Some patterns detected -- targeted edits recommended
- **20-29**: Significant AI patterns -- substantial revision needed
- **0-19**: Heavy AI patterns -- consider rewriting key sections

## Output Format

Write the report to `paper/writing-deai-report.md`:

```markdown
# Writing De-AI Report

**Project**: <project title>
**Date**: <date>
**Files scanned**: <list of files>

## Overall Score: XX/50

## Category Scores

| # | Category | Score | Issues Found |
|---|----------|-------|--------------|
| 1 | Hedging Overuse | X/5 | N instances |
| 2 | Formulaic Transitions | X/5 | N instances |
| 3 | Superlative Claims | X/5 | N instances |
| 4 | Passive Voice Excess | X/5 | N instances |
| 5 | Generic Filler | X/5 | N instances |
| 6 | Uniform Sentence Length | X/5 | N sections |
| 7 | Over-Enumeration | X/5 | N instances |
| 8 | Vocabulary Uniformity | X/5 | N instances |
| 9 | Missing Personality | X/5 | N sections |
| 10 | Citation Integration | X/5 | N instances |

## Assessment

<Overall assessment paragraph based on scoring guide.>

## Top Issues (with suggested rewrites)

### Issue 1: [Category] in [Section]

**Original:** "..."
**Problem:** <why this reads as AI-generated>
**Suggested rewrite:** "..."

### Issue 2: [Category] in [Section]

**Original:** "..."
**Problem:** <why this reads as AI-generated>
**Suggested rewrite:** "..."

(... up to 5 issues ...)

## Full Issue Log

### Hedging Overuse
- File: `paper/sections/intro.tex`, paragraph 3: "It is worth noting that..."
- ...

### Formulaic Transitions
- ...

(... all categories with specific locations ...)
```

## Output Files

| File | Location | Purpose |
|------|----------|---------|
| De-AI Report | `paper/writing-deai-report.md` | Full scoring, issue log, and suggested rewrites |

## Hard Rules

1. **NEVER change technical content or factual claims** -- rewrites must preserve meaning exactly.
2. **NEVER remove citations or evidence references** -- rewording must keep all references intact.
3. **Suggest rewrites, do not auto-apply** -- the human researcher decides which changes to accept.
4. **Focus on the 5 worst issues, not every minor pattern** -- the report should be actionable, not exhausting.
5. **Academic writing IS different from casual writing** -- do not over-correct toward informal tone. Formal is fine; robotic is not.
6. **Technical terms must remain consistent** -- do not suggest varying technical terminology for the sake of variety. Vocabulary uniformity checks apply to non-technical language only.
7. **Context matters** -- passive voice in Methods is standard practice, not an AI tell. Score relative to section norms.
