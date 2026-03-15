---
name: autoresearch:paper-figure
description: Generate data-driven plots and tables for paper. Creates matplotlib/seaborn plots from JSON/CSV data. Use when user says "generate figures", "画图", "create plots".
argument-hint: [paper-plan-path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent
---

## Purpose

Generate figures and tables for paper from data.

## Workflow

1. Read figure plan from PAPER_PLAN.md
2. Generate matplotlib/seaborn plots from JSON/CSV
3. Generate LaTeX comparison tables
4. Create figures/latex_includes.tex
5. GPT-5.4 reviews figure quality

## Output

figures/ directory with:
- PDF figures
- Generation scripts
- latex_includes.tex

## Scope

Auto-generates ~60% of figures. Architecture diagrams and qualitative results need manual creation.