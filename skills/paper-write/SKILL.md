---
name: airesearchorchestrator:paper-write
agent: writer
description: Generate LaTeX sections for paper. Writes section-by-section with proper formatting. Use when user says "write paper", "写论文", "generate LaTeX".
argument-hint: [paper-plan-path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, mcp__codex__codex
---

## Purpose

Generate LaTeX sections for paper from plan.

## Workflow

1. Write each section following plan
2. Insert figure/table references
3. Build references.bib
4. Clean stale files
5. Automated bib cleaning
6. De-AI polish (remove "delve", "pivotal", etc.)
7. GPT-5.4 reviews each section

## Output

paper/ directory with:
- main.tex
- sections/*.tex
- references.bib
- math_commands.tex