---
name: paper-compile
description: Compile LaTeX paper to PDF. Handles multi-pass compilation and auto-fixes common errors. Use when user says "compile paper", "编译论文", "build PDF".
argument-hint: [paper-directory]
allowed-tools: Bash(*), Read, Write, Edit
---

## Purpose

Build PDF from LaTeX source.

## Workflow

1. Run latexmk -pdf
2. Auto-fix common errors (missing packages, undefined refs)
3. Up to 3 compilation attempts
4. Post-compilation checks
5. Precise page verification

## Output

paper/main.pdf

## Checks

- Undefined references: 0
- Undefined citations: 0
- Page count vs venue limit
- Font embedding