# Figure and Table Guidelines

## Table of Contents

- Overview
- Figure Standards
- Table Standards
- Statistical Reporting in Tables
- Captions and Labels
- Color and Accessibility
- Venue-Specific Requirements
- LaTeX Templates

## Overview

Figures and tables are essential for communicating results effectively. They should be self-contained, clear, and professionally formatted.

### Key Principles

1. **Self-contained**: Caption should explain the figure/table without requiring main text
2. **Consistent**: Same style throughout the paper
3. **Accessible**: Readable in grayscale, colorblind-friendly
4. **High quality**: Vector format preferred for diagrams

## Figure Standards

### Resolution and Format

| Figure Type | Format | Resolution |
|-------------|--------|------------|
| Diagrams, plots | PDF, EPS (vector) | N/A (scalable) |
| Photos, screenshots | PNG, TIFF | 300 DPI minimum |
| Line art | PDF, EPS (vector) | N/A (scalable) |

**Preferred formats**:
- PDF/EPS for all diagrams, plots, and line art (vector)
- PNG for raster images (screenshots, photos)

**Avoid**:
- JPEG for line art (compression artifacts)
- Low-resolution screenshots
- Proprietary formats (AI, PSD, etc.)

### Figure Size

Standard figure widths for academic papers:

| Width | Use Case |
|-------|----------|
| Single column | Small plots, single diagrams |
| Double column | Wide tables, multi-panel figures |
| Full page | Large diagrams (rare) |

Typical column widths:
- Single column: 3.25 inches (8.25 cm)
- Double column: 6.75 inches (17.15 cm)

### Font Size in Figures

All text in figures should be readable at printed size:

| Element | Minimum Size |
|---------|-------------|
| Axis labels | 8 pt |
| Tick labels | 7 pt |
| Legend text | 7 pt |
| Annotations | 7 pt |

**Test**: Print at actual size and verify readability.

### Figure Types

#### 1. Architecture Diagrams

**Purpose**: Show model/system architecture

**Guidelines**:
- Use consistent shapes for same components
- Include input/output arrows
- Label all components
- Show data flow direction

**Example (LaTeX with TikZ)**:
```latex
\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{figures/architecture.pdf}
\caption{Overview of our proposed architecture. The encoder processes
the input sequence, producing contextualized representations that are
passed to the decoder for generation.}
\label{fig:architecture}
\end{figure}
```

#### 2. Performance Plots

**Purpose**: Show quantitative results

**Guidelines**:
- Include error bars (standard deviation or confidence interval)
- Label axes clearly with units
- Use consistent colors/markers
- Include legend

**Types**:
- Bar charts: Compare discrete conditions
- Line plots: Show trends over continuous variable
- Scatter plots: Show correlations

**Example (bar chart with error bars)**:
```python
import matplotlib.pyplot as plt
import numpy as np

methods = ['Baseline', 'Method A', 'Ours']
means = [85.2, 88.1, 92.3]
stds = [0.5, 0.4, 0.3]

fig, ax = plt.subplots(figsize=(3.25, 2.5))
x = np.arange(len(methods))
bars = ax.bar(x, means, yerr=stds, capsize=3, color=['gray', 'lightblue', 'blue'])
ax.set_ylabel('Accuracy (%)')
ax.set_xticks(x)
ax.set_xticklabels(methods)
ax.set_ylim(80, 95)
plt.tight_layout()
plt.savefig('figures/comparison.pdf')
```

#### 3. Training Curves

**Purpose**: Show learning dynamics

**Guidelines**:
- Include both training and validation curves
- Use log scale for loss if appropriate
- Mark key points (best epoch, early stopping)
- Smooth curves if noisy (but report smoothing method)

**Example**:
```latex
\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{figures/training_curve.pdf}
\caption{Training and validation loss curves. The model converges
after approximately 50K steps, with best validation performance at
step 75K (indicated by the dashed line).}
\label{fig:training}
\end{figure}
```

#### 4. Attention/Heatmap Visualizations

**Purpose**: Show learned patterns

**Guidelines**:
- Include color bar with scale
- Label axes meaningfully
- Use perceptually uniform colormaps (viridis, not jet)
- Consider colorblind accessibility

**Colormap Recommendations**:
- Sequential data: viridis, plasma, Blues
- Diverging data: RdBu, PuOr, coolwarm
- Avoid: jet, rainbow (not perceptually uniform)

#### 5. Qualitative Examples

**Purpose**: Show illustrative examples

**Guidelines**:
- Show representative examples
- Include ground truth if applicable
- Indicate model predictions
- Explain what to observe in caption

**Example**:
```latex
\begin{figure*}[t]
\centering
\includegraphics[width=\textwidth]{figures/examples.pdf}
\caption{Qualitative comparison. Our method (bottom row) produces
more accurate predictions compared to the baseline (middle row),
especially for edge cases (columns 3-5). Ground truth is shown in
the top row.}
\label{fig:examples}
\end{figure*}
```

## Table Standards

### Table Formatting

**Basic structure**:
- Horizontal rules: top, below header, bottom
- No vertical rules
- Consistent decimal alignment
- Units in column headers

**Example (LaTeX)**:
```latex
\begin{table}[t]
\centering
\caption{Main results on benchmark datasets. Best results are in
\textbf{bold}. All results are averaged over 5 random seeds.}
\label{tab:main_results}
\begin{tabular}{lccc}
\toprule
Method & Dataset A & Dataset B & Dataset C \\
\midrule
Baseline 1 & 85.2 ± 0.5 & 82.1 ± 0.6 & 78.3 ± 0.7 \\
Baseline 2 & 87.1 ± 0.4 & 84.5 ± 0.5 & 80.2 ± 0.6 \\
Ours & \textbf{92.3 ± 0.3} & \textbf{89.7 ± 0.4} & \textbf{85.1 ± 0.5} \\
\bottomrule
\end{tabular}
\end{table}
```

### Table Types

#### 1. Comparison Tables

**Purpose**: Compare methods on metrics

**Guidelines**:
- Bold best results
- Include standard deviations
- Arrow indicating metric direction
- Statistical significance markers (*, **, ***)

**Example**:
```latex
\begin{table}[t]
\centering
\caption{Performance comparison. $\uparrow$ indicates higher is better.
Statistical significance: * p < 0.05, ** p < 0.01.}
\label{tab:comparison}
\begin{tabular}{lcccc}
\toprule
Method & Accuracy$\uparrow$ & F1$\uparrow$ & Latency (ms)$\downarrow$ \\
\midrule
Baseline & 85.2 & 0.823 & 45 \\
Method A & 87.1 & 0.845 & 52 \\
Ours & \textbf{92.3**} & \textbf{0.901**} & \textbf{38} \\
\bottomrule
\end{tabular}
\end{table}
```

#### 2. Ablation Tables

**Purpose**: Show contribution of components

**Guidelines**:
- Show incremental improvements
- Include complete model
- Explain what each row removes/adds

**Example**:
```latex
\begin{table}[t]
\centering
\caption{Ablation study on Dataset A. Each row removes one component.}
\label{tab:ablation}
\begin{tabular}{lc}
\toprule
Configuration & Accuracy \\
\midrule
Full model & \textbf{92.3} \\
\quad -- Component A & 89.5 \\
\quad -- Component B & 90.1 \\
\quad -- Component C & 88.7 \\
\bottomrule
\end{tabular}
\end{table}
```

#### 3. Hyperparameter Sensitivity Tables

**Purpose**: Show effect of hyperparameters

**Guidelines**:
- Vary one parameter at a time
- Include recommended setting
- Show sensitivity range

#### 4. Dataset Statistics Tables

**Purpose**: Describe datasets used

**Example**:
```latex
\begin{table}[t]
\centering
\caption{Dataset statistics.}
\label{tab:datasets}
\begin{tabular}{lrrr}
\toprule
Dataset & Train & Valid & Test \\
\midrule
Dataset A & 50,000 & 5,000 & 10,000 \\
Dataset B & 100,000 & 10,000 & 20,000 \\
Dataset C & 25,000 & 2,500 & 5,000 \\
\bottomrule
\end{tabular}
\end{table}
```

## Statistical Reporting in Tables

### Required Statistics

| Statistic | When Required | Format |
|-----------|--------------|--------|
| Mean | Always | X.XX |
| Standard deviation | Always | X.XX ± X.XX |
| Confidence interval | Recommended | X.XX (CI: X.XX-X.XX) |
| p-value | For comparisons | p < 0.05 |
| Effect size | Recommended | d = X.XX |

### Reporting Format

**Standard deviation**:
```latex
92.3 ± 0.4
```

**Confidence interval**:
```latex
92.3 (95\% CI: 91.5--93.1)
```

**Statistical significance**:
```latex
92.3**  % ** indicates p < 0.01
```

**Full statistical reporting**:
```latex
Our method achieves 92.3 ± 0.4\% accuracy compared to 88.1 ± 0.5\%
for the baseline (p < 0.001, paired t-test, n=5).
```

### Significance Stars

| Symbol | p-value | Meaning |
|--------|---------|---------|
| * | p < 0.05 | Significant |
| ** | p < 0.01 | Highly significant |
| *** | p < 0.001 | Very highly significant |

**Note**: Always explain the meaning of stars in the caption.

### Significant Figures

- Report 2-3 significant figures typically
- Match precision to measurement precision
- Don't report more precision than meaningful

| Incorrect | Correct |
|-----------|---------|
| 92.3456% | 92.3% |
| 0.001234 seconds | 1.2 ms |

## Captions and Labels

### Caption Guidelines

**Principles**:
1. Self-contained (understandable without text)
2. Explain what is shown
3. Highlight key observations
4. Define abbreviations

**Structure**:
```markdown
[What]: Brief description of content
[Key observation]: What to notice
[Details]: Additional context if needed
```

**Figure Caption Example**:
```latex
\caption{Training loss curves for different learning rates. The
default learning rate (1e-4) achieves fastest convergence, while
higher rates (1e-3) cause instability. All models were trained for
100K steps on the same dataset.}
```

**Table Caption Example**:
```latex
\caption{Comparison with state-of-the-art methods on GLUE benchmark.
Best results in \textbf{bold}. Our method outperforms all baselines
on 5 out of 9 tasks. Results averaged over 5 random seeds.}
```

### Labels and References

**Naming convention**:
- Figures: `fig:description`
- Tables: `tab:description`
- Equations: `eq:description`

**Example**:
```latex
\label{fig:attention_heatmap}
\label{tab:ablation_results}
\label{eq:loss_function}
```

**Referencing**:
```latex
Figure~\ref{fig:attention_heatmap} shows...
As shown in Table~\ref{tab:ablation_results}...
```

**Note**: Use non-breaking space (`~`) between Figure/Table and the number.

## Color and Accessibility

### Colorblind-Friendly Palettes

Approximately 8% of men have color vision deficiency. Use colorblind-friendly palettes:

**Recommended palettes**:
- ColorBrewer: Set1, Set2, Dark2
- Wong palette: Blue, Orange, Sky Blue, Red, Vermillion, Bluish Green

**Python (matplotlib)**:
```python
# Wong palette (colorblind-friendly)
colors = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#F0E442', '#56B4E9']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
```

### Testing for Accessibility

1. **Grayscale test**: Print in grayscale, verify readability
2. **Colorblind simulation**: Use tools like Coblis or Color Oracle
3. **Pattern differentiation**: Use different markers/line styles in addition to color

### Safe Color Combinations

| Good | Problematic |
|------|-------------|
| Blue + Orange | Red + Green |
| Blue + Red | Green + Red |
| Yellow + Blue | Yellow + Green |

## Venue-Specific Requirements

### Conference Formats

| Venue | Column Width | Figure Width | Font |
|-------|-------------|--------------|------|
| NeurIPS | 5.5 in | Single or double | Times |
| ICML | 6.75 in | Single or double | Times |
| ICLR | 6.75 in | Single or double | Times |
| CVPR | 3.25/6.875 in | Single or double | Times |
| ACL | 6.875 in | Single or double | Times |

### Journal Formats

| Venue | Typical Width | Resolution |
|-------|--------------|------------|
| TPAMI | 7.5 in | 300 DPI |
| JMLR | 6.5 in | Vector preferred |
| Nature | 3.5/7.0 in | 300 DPI |

### Common Requirements

- **EPS/PDF preferred** for LaTeX submissions
- **TIFF/PNG at 300 DPI** for some journals
- **No embedded fonts** issues (embed all fonts)
- **RGB color** for online, sometimes CMYK for print

## LaTeX Templates

### Basic Figure

```latex
\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{figures/example.pdf}
\caption{Description of the figure. Key observation about what
the figure shows.}
\label{fig:example}
\end{figure}
```

### Multi-Panel Figure

```latex
\begin{figure*}[t]
\centering
\begin{subfigure}{0.32\textwidth}
    \centering
    \includegraphics[width=\textwidth]{figures/panel_a.pdf}
    \caption{Panel A description}
    \label{fig:example_a}
\end{subfigure}
\hfill
\begin{subfigure}{0.32\textwidth}
    \centering
    \includegraphics[width=\textwidth]{figures/panel_b.pdf}
    \caption{Panel B description}
    \label{fig:example_b}
\end{subfigure}
\hfill
\begin{subfigure}{0.32\textwidth}
    \centering
    \includegraphics[width=\textwidth]{figures/panel_c.pdf}
    \caption{Panel C description}
    \label{fig:example_c}
\end{subfigure}
\caption{Overall caption describing the three panels. Panel (a)
shows X, panel (b) shows Y, and panel (c) shows Z.}
\label{fig:example_multipanel}
\end{figure*}
```

### Professional Table

```latex
\usepackage{booktabs}

\begin{table}[t]
\centering
\caption{Main results. Best results in \textbf{bold}.}
\label{tab:results}
\begin{tabular}{@{}lcccc@{}}
\toprule
Method & Metric 1 & Metric 2 & Metric 3 \\
\midrule
Baseline & 85.2 & 0.823 & 45.1 \\
Method A & 87.5 & 0.845 & 52.3 \\
Ours & \textbf{92.3} & \textbf{0.901} & \textbf{38.2} \\
\bottomrule
\end{tabular}
\end{table}
```

### Table with Spanning Columns

```latex
\begin{table*}[t]
\centering
\caption{Comprehensive results across all datasets.}
\label{tab:full_results}
\begin{tabular}{@{}l*{4}{c}@{}}
\toprule
& \multicolumn{2}{c}{Dataset A} & \multicolumn{2}{c}{Dataset B} \\
\cmidrule(l){2-3} \cmidrule(l){4-5}
Method & Acc & F1 & Acc & F1 \\
\midrule
Baseline & 85.2 & 0.823 & 82.1 & 0.798 \\
Ours & \textbf{92.3} & \textbf{0.901} & \textbf{89.7} & \textbf{0.876} \\
\bottomrule
\end{tabular}
\end{table*}
```

### Algorithm Pseudocode

```latex
\usepackage{algorithm}
\usepackage{algorithmic}

\begin{algorithm}[t]
\caption{Training procedure}
\label{alg:training}
\begin{algorithmic}[1]
\REQUIRE Dataset $\mathcal{D}$, learning rate $\eta$
\STATE Initialize model parameters $\theta$
\FOR{epoch $= 1$ to $E$}
    \FOR{batch $(x, y) \in \mathcal{D}$}
        \STATE Compute loss $\mathcal{L} = \ell(f_\theta(x), y)$
        \STATE Update $\theta \leftarrow \theta - \eta \nabla_\theta \mathcal{L}$
    \ENDFOR
\ENDFOR
\RETURN Trained model $f_\theta$
\end{algorithmic}
\end{algorithm}
```

## Quality Checklist

### Figures

- [ ] Vector format (PDF/EPS) for diagrams
- [ ] 300+ DPI for raster images
- [ ] Readable labels at printed size
- [ ] Self-contained captions
- [ ] Colorblind-friendly colors
- [ ] Consistent style across figures
- [ ] Proper file naming (descriptive names)

### Tables

- [ ] Consistent formatting
- [ ] Units specified
- [ ] Best results highlighted
- [ ] Standard deviations included
- [ ] Self-contained captions
- [ ] Proper decimal alignment
- [ ] No vertical rules