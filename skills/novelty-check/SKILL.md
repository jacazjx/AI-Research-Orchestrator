---
name: airesearchorchestrator:novelty-check
agent: critic
description: Verify novelty of a research idea against existing literature. Use when user says "check novelty", "新颖性检查", "is this novel", or needs to verify an idea is not already published.
argument-hint: [idea-description]
allowed-tools: Bash(curl), Read, Write, Edit, Grep, Glob, WebFetch, mcp__codex__codex
---

## Purpose

Verify that a research idea is novel and identify closest existing work.

## Workflow

### Step 1: Multi-source Search

Search for:
- Exact or near-exact matches
- Similar approaches
- Concurrent work (last 3-6 months)

### Step 2: Identify Closest Work

For each similar paper:
- Summarize contribution
- Identify overlap with proposed idea
- Note differentiation points

### Step 3: Cross-verify with LLM

Use GPT-5.4 xhigh to:
- Compare idea vs existing work
- Identify unique contributions
- Suggest differentiation angles

### Step 4: Report

Output:
- NOVELTY_STATUS: CONFIRMED | PARTIAL | NOT_NOVEL
- Closest papers with DOI
- Differentiation points (if CONFIRMED or PARTIAL)
- Recommended pivot (if NOT_NOVEL)

## Output

- `docs/reports/survey/novelty-report.md` - Novelty verification report with closest papers and differentiation points