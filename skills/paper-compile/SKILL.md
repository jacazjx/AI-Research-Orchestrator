---
name: airesearchorchestrator:paper-compile
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

## Key Rules

1. Check LaTeX syntax before compilation
2. Compile PDF with latexmk -pdf (up to 3 attempts)
3. Report errors with line numbers and suggested fixes

## Checks

- Undefined references: 0
- Undefined citations: 0
- Page count vs venue limit
- Font embedding