---
name: paper-plan
description: Create paper outline and structure from research narrative. Builds Claims-Evidence Matrix and section plan. Use when user says "paper outline", "论文大纲", "plan paper structure".
argument-hint: [narrative-report-path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, mcp__codex__codex
---

## Purpose

Create structural outline for paper from research narrative.

## Workflow

1. Parse NARRATIVE_REPORT.md for claims, evidence, figures
2. Build Claims-Evidence Matrix
3. Design section structure (5-8 sections)
4. Plan figure/table placement
5. Scaffold citation structure
6. GPT-5.4 reviews plan for completeness

## Output

PAPER_PLAN.md with:
- Title proposal
- Section plan
- Figure plan
- Citation scaffolding