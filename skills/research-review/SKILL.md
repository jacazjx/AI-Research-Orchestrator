---
name: research-review
description: External critical review of research ideas via Codex MCP. Acts as a senior reviewer (NeurIPS/ICML level) to score ideas and identify weaknesses. Use when user says "review this idea", "critique", "反馈", or wants brutal feedback on a research direction.
argument-hint: [idea-with-context]
allowed-tools: Bash(*), Read, Write, Edit, mcp__codex__codex, mcp__codex__codex-reply
---

## Purpose

Provide brutal critical feedback on a research idea, acting as a senior reviewer.

## Workflow

### Step 1: Prepare Context

Gather:
- Idea description
- Hypothesis
- Pilot results (if any)
- Literature context

### Step 2: External Review via Codex MCP

Use GPT-5.4 xhigh with prompt:

```
You are a senior reviewer for NeurIPS/ICML. Review this research idea:

[idea context]

Provide:
1. Score (1-10)
2. Verdict (accept/major revision/reject)
3. Top 3 weaknesses
4. Minimum fixes to make acceptable
5. Experimental design feedback
```

### Step 3: Parse and Report

Output:
- Score and verdict
- Key weaknesses
- Recommended improvements
- Next steps