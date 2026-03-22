---
name: airesearchorchestrator:post-acceptance
agent: writer
description: "Generate post-acceptance materials: conference presentation slides outline, academic poster layout, and social media promotion text. Use when user says 'post acceptance', '录用后', 'make slides', 'make poster', 'promote paper', '做PPT', '做海报'."
allowed-tools: Read, Write, Edit, Grep, Glob
---
# Post-Acceptance Materials

## Purpose

Generate dissemination materials after a paper is accepted: a presentation slides outline with speaker notes, an academic poster layout, and social media promotion text. These materials help maximize the impact of accepted work.

## When to Use

- After a paper has been accepted at a venue
- When the user says "post acceptance", "make slides", "make poster", "promote paper", "录用后", "做PPT", or "做海报"
- Can also be used selectively (e.g., only slides, only poster) based on user request

## Workflow

### Step 1: Gather Inputs

1. **Read the manuscript** -- load `paper/main.tex` and all section files
2. **Read the evidence package** -- load `docs/experiments/evidence-package-index.md` for key results
3. **Read project state** -- load `.autoresearch/state/research-state.yaml` for venue info and project metadata
4. **Read figures** -- identify key figures in `paper/figures/` for reuse in slides and poster
5. **Create output directory** -- ensure `paper/presentation/` exists
6. **Determine scope** -- check user request: all three outputs, or a specific subset

### Step 2: Presentation Slides Outline

Design a 15-20 slide outline suitable for a conference oral or spotlight talk.

#### Slide Structure

| Slide # | Section | Content | Time (15min oral) | Time (5min spotlight) |
|---------|---------|---------|--------------------|-----------------------|
| 1 | Title | Title, authors, affiliations, venue, date | 0:00-0:30 | 0:00-0:15 |
| 2 | Motivation | Why this problem matters (real-world example or striking statistic) | 0:30-1:30 | 0:15-0:45 |
| 3 | Problem | Formal problem statement, key challenge | 1:30-2:30 | 0:45-1:15 |
| 4 | Prior Work | 2-3 key prior approaches and their limitations (one slide, not exhaustive) | 2:30-3:30 | -- |
| 5 | Key Idea | One-sentence insight that drives the method (the "aha" moment) | 3:30-4:30 | 1:15-1:45 |
| 6-8 | Method | Method overview (architecture diagram), then 1-2 slides on key technical details | 4:30-7:00 | 1:45-2:30 |
| 9 | Experimental Setup | Datasets, baselines, metrics (brief) | 7:00-7:30 | 2:30-2:45 |
| 10-12 | Results | Main results table, key comparison plots, ablation highlights | 7:30-10:30 | 2:45-3:45 |
| 13 | Analysis | Qualitative examples, visualizations, or case studies | 10:30-11:30 | 3:45-4:15 |
| 14 | Limitations | Honest limitations and future directions | 11:30-12:00 | -- |
| 15 | Conclusion | Summary of contributions (3 bullet points max) | 12:00-12:30 | 4:15-4:30 |
| 16 | Q&A | "Thank you" slide with contact info, paper link, code link | 12:30-15:00 | 4:30-5:00 |

#### Speaker Notes

For each slide, include:
- **Key message**: The one thing the audience should take away from this slide
- **Talking points**: 2-4 bullet points of what to say (not a script, but guidance)
- **Transition**: How to connect to the next slide
- **Backup notes**: Anticipated questions and prepared answers (for key slides)

#### Presentation Principles

- **One idea per slide** -- never overload a slide with multiple concepts
- **Figures over text** -- prefer diagrams, plots, and examples over bullet points
- **Build complexity gradually** -- start simple, add details incrementally
- **Highlight key results** -- use color, bold, or animation cues to draw attention to the main finding
- **Rehearsal timing** -- include timing markers for both 15-minute oral and 5-minute spotlight formats

### Step 3: Academic Poster Layout

Design a poster layout for A0 (841 x 1189 mm) or A1 (594 x 841 mm) landscape format.

#### Layout Grid

```
+------------------------------------------------------------------+
|                         TITLE BAR                                |
|  Title | Authors | Affiliations | Venue | Logo(s) | QR Code     |
+----------+----------+----------+----------+----------+-----------+
|          |          |          |          |          |           |
| 1.       | 2.       | 3.       | 4.       | 5.       | 6.       |
| Motiv-   | Problem  | Method   | Method   | Results  | Results  |
| ation    | State-   | Overview | Detail   | (Main    | (Ablation|
| & Gap    | ment     | (Diagram)| (Key     | Table)   | or       |
|          |          |          | Equation)|          | Analysis)|
|          |          |          |          |          |           |
+----------+----------+----------+----------+----------+-----------+
|                    |                      |                      |
| 7. Qualitative     | 8. Conclusion &      | 9. References &      |
|    Examples /      |    Key Takeaways     |    Acknowledgments   |
|    Visualizations  |    (3 bullet points) |    QR: paper + code  |
|                    |                      |                      |
+--------------------+----------------------+----------------------+
```

#### Poster Content Guidelines

| Section | Content | Design Notes |
|---------|---------|--------------|
| Title bar | Full title, all authors, affiliations, venue name and year | Largest font; include lab/university logos |
| Motivation | Why this matters (1-2 sentences + a motivating figure) | Eye-catching; draw visitors in |
| Problem | Formal statement, input/output definition | Keep concise |
| Method overview | Architecture or pipeline diagram | The visual centerpiece of the poster |
| Method detail | Key equation or algorithm (just the core insight) | Do not reproduce the entire method |
| Main results | Primary comparison table or plot | Highlight best results in bold/color |
| Analysis | Ablation, qualitative examples, or visualizations | Select 2-3 most compelling |
| Conclusion | 3 key takeaways as bullet points | Memorable and self-contained |
| References | 5-8 most important references only | Small font is acceptable |
| QR codes | Links to: (1) paper PDF, (2) code repository | Place in bottom-right and title bar |

#### Figure Selection

Identify the top 3-5 figures from the paper for poster inclusion:
1. **Method diagram** -- the main architecture or pipeline figure (required)
2. **Main results** -- the primary comparison table or plot (required)
3. **Qualitative examples** -- visual examples showing the method in action (if applicable)
4. **Ablation plot** -- showing contribution of key components (if space permits)

### Step 4: Social Media Promotion Text

Generate promotion materials for three platforms:

#### Twitter/X Thread (5-7 tweets)

```markdown
Tweet 1 (Hook):
[Exciting result or surprising finding in plain language]
Our paper "[Title]" is accepted at [Venue]!
A thread on what we found: [1/N]

Tweet 2 (Problem):
[What problem does this solve? Why should anyone care?]
[2/N]

Tweet 3 (Key idea):
[One-sentence explanation of the approach, accessible to a broad ML audience]
[Include method figure if possible]
[3/N]

Tweet 4 (Results):
[Headline result with numbers]
[Include results figure or table screenshot]
[4/N]

Tweet 5 (Insight):
[The most surprising or interesting finding from the paper]
[5/N]

Tweet 6 (Links):
Paper: [link]
Code: [link]
[6/N]

Tweet 7 (Acknowledgments):
Joint work with [co-authors tagged]. Thanks to [acknowledgments].
[7/N]
```

**Thread principles:**
- First tweet must hook -- lead with the result, not the method name
- Use plain language -- avoid jargon; a PhD student outside the subfield should understand
- Include visually appealing figures (method diagram + results plot)
- Keep each tweet under 280 characters
- Tag co-authors and relevant accounts

#### LinkedIn Post

A single professional post (150-300 words):
- Opening: announce the acceptance with venue name
- Body: describe the problem, approach, and key result in accessible language
- Closing: link to paper and code, tag co-authors
- Tone: professional but enthusiastic, not overly promotional

#### Lab Website Abstract

A one-paragraph summary (100-150 words) suitable for a lab or personal website project page:
- Self-contained (no assumed context)
- Includes: problem, approach, key result, venue
- Written for a general technical audience
- Ends with links to paper, code, and any supplementary materials

### Step 5: Write Output Files

Save all artifacts to `paper/presentation/`:

| File | Content |
|------|---------|
| `slides-outline.md` | Full slide-by-slide outline with speaker notes and timing |
| `poster-layout.md` | Poster layout grid, section content, and figure selection |
| `social-media-text.md` | Twitter thread, LinkedIn post, and website abstract |

## Output Files

| File | Location | Purpose |
|------|----------|---------|
| Slides Outline | `paper/presentation/slides-outline.md` | 15-20 slide structure with speaker notes and timing guidance |
| Poster Layout | `paper/presentation/poster-layout.md` | A0/A1 landscape layout with section placement and figure selection |
| Social Media Text | `paper/presentation/social-media-text.md` | Twitter/X thread, LinkedIn post, and lab website abstract |

## Key Rules

1. **Read the actual paper** -- all materials must be derived from the manuscript content, not generated from imagination
2. **Accuracy first** -- never overstate results in promotion materials; use the same qualifications as the paper
3. **Audience-appropriate language** -- slides for experts, social media for broad technical audience, poster in between
4. **Reuse existing figures** -- reference figures already in `paper/figures/` rather than describing new ones
5. **Respect authorship** -- include all co-authors in all materials; do not omit anyone
6. **No fabricated links** -- use placeholder `[link]` for URLs the user will fill in; do not invent URLs
7. **Selective, not exhaustive** -- poster and slides should highlight 3-5 key points, not compress the entire paper
