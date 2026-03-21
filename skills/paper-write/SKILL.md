---
name: airesearchorchestrator:paper-write
agent: writer
description: "Plan paper structure and generate LaTeX sections following IMRAD structure. Covers outlining (Claims-Evidence Matrix, section plan) and drafting. Use when user says \"write paper\", \"写论文\", \"generate LaTeX\", \"draft manuscript\", \"paper outline\", \"论文大纲\"."
user-invocable: false
argument-hint: [paper-plan-path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, mcp__codex__codex
---
## Purpose

Plan paper structure and generate LaTeX sections following IMRAD structure. This skill covers both outlining (Claims-Evidence Matrix, section planning) and section-by-section drafting.

## Workflow

### Phase 0: Paper Planning

Before writing, create the structural outline. If `paper/paper-plan.md` does not exist, create it.

1. **Parse research narrative** from experiment evidence package and prior phase deliverables
2. **Build Claims-Evidence Matrix** -- map each claim to its supporting evidence
3. **Design section structure** (5-8 sections following IMRAD)
4. **Plan figure/table placement** -- assign figures and tables to sections
5. **Scaffold citation structure** -- identify where key citations belong

Save to `paper/paper-plan.md`:
- Title proposal
- Section plan with key points per section
- Claims-Evidence Matrix
- Figure/table placement plan
- Citation scaffolding

### Phase 1: Preparation

1. **Read paper plan** from `paper/paper-plan.md`
2. **Review evidence package** from `docs/experiments/evidence-package-index.md`
3. **Check citation library** from `paper/references.bib`
4. **Review figures and tables** from `paper/figures/` and `paper/tables/`

### Phase 2: Section-by-Section Writing

Follow IMRAD structure. See `references/imrad_structure.md` for detailed section guidelines.

### Phase 3: LaTeX Compilation and Polish

1. **Clean stale files**: Remove old .aux, .log, .bbl files
2. **Compile**: pdflatex/bibtex cycle (3x for references)
3. **De-AI Polish**: Remove AI-typical phrases:
   - "delve", "pivotal", "crucial", "paramount"
   - "It is worth noting that..."
   - "In order to..." (use "to...")
4. **Check venue compliance**: Format, length, required sections

## LaTeX Templates

### Main Document Structure

```latex
\documentclass{article}  % or venue-specific class
\input{math_commands.tex}

\title{...}
\author{...}

\begin{document}
\maketitle
\begin{abstract} ... \end{abstract}

\input{sections/introduction}
\input{sections/related_work}
\input{sections/method}
\input{sections/experiments}
\input{sections/conclusion}

\bibliographystyle{plain}  % venue-specific
\bibliography{references}
\end{document}
```

### Algorithm Environment

```latex
\usepackage{algorithm}
\usepackage{algorithmic}

\begin{algorithm}[t]
\caption{Algorithm Name}
\label{alg:name}
\begin{algorithmic}[1]
\REQUIRE Input description
\ENSURE Output description
\STATE Step 1
\FOR{$i = 1$ to $N$}
  \STATE Step in loop
\ENDFOR
\RETURN result
\end{algorithmic}
\end{algorithm}
```

### Results Table

```latex
\begin{table}[t]
\centering
\caption{Main results. Best in \textbf{bold}. $\uparrow$ = higher is better.}
\label{tab:main}
\begin{tabular}{lcc}
\toprule
Method & Metric 1 $\uparrow$ & Metric 2 $\uparrow$ \\
\midrule
Baseline A & 85.2 $\pm$ 0.3 & 72.1 $\pm$ 0.5 \\
Baseline B & 87.4 $\pm$ 0.4 & 74.3 $\pm$ 0.6 \\
\textbf{Ours} & \textbf{92.3 $\pm$ 0.4} & \textbf{78.9 $\pm$ 0.3} \\
\bottomrule
\end{tabular}
\end{table}
```

### Figure Environment

```latex
\begin{figure}[t]
\centering
\includegraphics[width=\linewidth]{figures/figure_name.pdf}
\caption{Self-contained caption describing the figure.}
\label{fig:name}
\end{figure}
```

## Output Files

| File | Location | Purpose |
|------|----------|---------|
| Paper Plan | `paper/paper-plan.md` | Structure and Claims-Evidence Matrix |
| Main Document | `paper/main.tex` | Document root |
| Sections | `paper/sections/*.tex` | Individual sections |
| References | `paper/references.bib` | Bibliography |
| Math Commands | `paper/math_commands.tex` | Custom math macros |
| Figures | `paper/figures/*.pdf` | Vector figures |
| Tables | `paper/tables/*.tex` | Table source files |

## Key Rules

1. **IMRAD Structure**: Follow Introduction, Methods, Results, Discussion structure
2. **Citation Authenticity**: All citations must be verified (see `references/citation-standards.md`)
3. **Evidence Traceability**: All claims mapped to evidence package
4. **Statistical Rigor**: Report means, standard deviations, and significance
5. **Reproducibility**: Methods must be detailed enough for replication
6. **De-AI Polish**: Remove AI-typical phrases before final output
7. **Venue Compliance**: Match specific venue requirements

## References

- `references/imrad_structure.md` - Detailed IMRAD section guidelines
- `references/academic_writing_style.md` - Writing style guidelines
- `references/figure_table_guidelines.md` - Visualization standards
- `references/citation-standards.md` - Citation verification
