---
name: autoresearch:idea-creator
description: Brainstorm and filter research ideas. Generates 8-12 concrete ideas via external LLM, filters by feasibility, and runs pilot experiments on top candidates. Use when user says "generate ideas", "头脑风暴", "find research ideas", or wants to explore possible directions.
argument-hint: [research-context]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, Skill, mcp__codex__codex
---

## Purpose

Generate and filter concrete research ideas from a research landscape context.

## Workflow

### Step 1: Brainstorm (via Codex MCP)

Generate 8-12 concrete ideas with:
- Clear hypothesis
- Expected contribution
- Required compute
- Risk assessment

### Step 2: Filter

Apply filters:
- Feasibility (compute, data, skills)
- Quick novelty search
- Time to validate

### Step 3: Deep Validate Top Ideas

For top 3-5 ideas:
- Full novelty check
- Devil's advocate analysis
- Pilot experiment design

### Step 4: Run Pilots

Deploy parallel pilots on available GPUs:
- Top 2-3 ideas
- Quick validation (< 2 hours each)
- Collect empirical signal

### Step 5: Rank and Report

Output `IDEA_REPORT.md` with:
- Ranked ideas
- Pilot results
- Recommended next step

## Constants

- PILOT_MAX_HOURS = 2
- MAX_PILOT_IDEAS = 3
- MAX_TOTAL_GPU_HOURS = 8