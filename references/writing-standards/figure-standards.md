# Figure and Table Standards

## Overview

Figures and tables are critical for communicating research findings. This guide covers standards for creating professional, informative visualizations in academic research.

## General Principles

### Purpose

Every figure and table should:
1. **Communicate** a specific finding or concept
2. **Replace** text that would be lengthy or confusing
3. **Support** the narrative of the paper

### The Self-Containment Rule

Figures and tables should be understandable without reading the main text:
- Clear labels and captions
- All abbreviations defined
- Units specified
- Context provided

## Figure Types

### Comparison Guide

| Type | Best For | Example |
|------|----------|---------|
| Line plot | Trends over time/epochs | Training curves |
| Bar chart | Comparing categories | Model comparison |
| Scatter plot | Relationships | Correlation analysis |
| Heatmap | Matrices/distributions | Attention weights |
| Box plot | Distributions | Performance variance |
| Violin plot | Distribution shape | Accuracy spread |

### Line Plots

**Best practices:**
- Show individual data points when n < 20
- Include error bars (mean ± SD or SEM)
- Use different line styles for B&W printing
- Log scale when spanning orders of magnitude

```python
# Example: Training curve standards
plt.figure(figsize=(8, 6))
plt.plot(epochs, train_loss, 'b-', label='Train', linewidth=2)
plt.plot(epochs, val_loss, 'r--', label='Validation', linewidth=2)
plt.fill_between(epochs, mean - std, mean + std, alpha=0.2)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.yscale('log')  # If spanning orders of magnitude
plt.legend()
plt.grid(True, alpha=0.3)
```

### Bar Charts

**Best practices:**
- Start y-axis at 0 (unless showing differences)
- Group related bars
- Include error bars
- Use consistent colors across figures

**When to avoid:**
- Continuous data → Use line plot
- Many categories → Use table
- Showing distribution → Use box/violin plot

### Scatter Plots

**Best practices:**
- Show regression line if relevant
- Include correlation coefficient
- Use transparency for dense plots
- Different shapes for different groups

```python
plt.scatter(x, y, alpha=0.5, s=50)  # Transparency for overlap
plt.plot(x_fit, y_fit, 'r--', label=f'r={r:.3f}')
plt.legend()
```

### Heatmaps

**Best practices:**
- Use perceptually uniform colormaps (viridis, plasma)
- Include colorbar with label
- Annotate cells if matrix is small
- Consider diverging colormap for correlations

```python
# Good colormaps
plt.imshow(matrix, cmap='viridis')  # Sequential
plt.imshow(correlation, cmap='RdBu_r', vmin=-1, vmax=1)  # Diverging

# Avoid
plt.imshow(matrix, cmap='jet')  # Not perceptually uniform
```

### Box Plots and Violin Plots

**Box plot components:**
```
        ┌───┐
        │   │  ← Upper whisker (Q3 + 1.5*IQR)
        ├───┤
        │   │  ← Q3 (75th percentile)
    ────┤   │────
        │ - │  ← Median (Q2)
    ────┤   │────
        │   │  ← Q1 (25th percentile)
        ├───┤
        │   │  ← Lower whisker (Q1 - 1.5*IQR)
        └───┘
         ∘     ← Outlier
```

**When to use:**
- Box plot: Median and IQR important
- Violin plot: Distribution shape important

## Tables

### Table Anatomy

```
Table 1
Performance Comparison on Benchmark Datasets

┌──────────────────┬──────────┬──────────┬──────────┐
│ Method           │ Accuracy │ F1 Score │ Time (s) │
├──────────────────┼──────────┼──────────┼──────────┤
│ Baseline         │ 85.2     │ 0.841    │ 12.3     │
│ Method A         │ 87.1     │ 0.863    │ 15.7     │
│ Method B         │ 88.4     │ 0.879    │ 14.2     │
│ Ours             │ 91.3     │ 0.907    │ 11.8     │
└──────────────────┴──────────┴──────────┴──────────┘

Note. Bold indicates best result. All results averaged
over 5 runs.
```

### Formatting Rules

| Element | Convention |
|---------|------------|
| Title | Above table, italicized |
| Headers | Bold, title case |
| Numbers | Right-aligned, consistent decimals |
| Text | Left-aligned |
| Notes | Below table, smaller font |
| Lines | Horizontal only (top, below headers, bottom) |

### Number Formatting

```
✓ Good:
│ 12.34 │
│ 15.67 │
│  9.12 │  (aligned on decimal)

✗ Bad:
│ 12.3 │
│ 15.67 │
│ 9.123 │  (inconsistent decimals)
```

### Significant Figures

| Data Type | Recommended |
|-----------|-------------|
| Accuracy | 1-2 decimal places (85.2%) |
| p-values | 2-3 decimal places (p = .043) |
| Large numbers | SI prefixes (1.5M, 2.3K) |
| Very small | Scientific notation (1.2e-5) |

### Result Tables

**Standard format for ML comparisons:**

| Method | Accuracy ↑ | F1 ↑ | Time ↓ |
|--------|------------|------|--------|
| Baseline | 85.2 ± 0.3 | 0.841 | 12.3 |
| Method A | 87.1 ± 0.2 | 0.863 | 15.7 |
| **Ours** | **91.3 ± 0.2** | **0.907** | **11.8** |

**Include:**
- Arrows indicating direction of better
- Mean ± standard deviation
- Bold for best results
- Statistical significance markers (*, **, ***)

## Captions

### Caption Structure

```
[Figure/Table number]. [Title]. [Description].

Example:
Figure 3. Training curves for different optimizers. Each curve
shows mean accuracy over 5 runs, with shaded region indicating
standard deviation.
```

### Caption Length

| Type | Length |
|------|--------|
| Simple figure | 1 sentence |
| Complex figure | 2-4 sentences |
| Table | 1-2 sentences + notes |

### What to Include

**Figures:**
- What is plotted
- Key takeaways
- Sample sizes / runs

**Tables:**
- What is compared
- Key observations
- Statistical tests used

## Color Guidelines

### Colorblind-Friendly Palettes

```
✓ Good (colorblind-safe):
- Blue & Orange
- Blue & Red
- Viridis palette

✗ Avoid (problematic):
- Red & Green together
- Rainbow colormaps
```

### Color Roles

| Use | Recommendation |
|-----|----------------|
| Categories | Distinct, named colors |
| Continuous | Sequential palette |
| Diverging | Diverging palette with white center |
| Highlight | Single accent color |

### Line Styles for B&W

When color may not be available:
```
plt.plot(x, y1, 'b-', label='Method A')   # Solid
plt.plot(x, y2, 'r--', label='Method B')  # Dashed
plt.plot(x, y3, 'g:', label='Method C')   # Dotted
plt.plot(x, y4, 'm-.', label='Method D')  # Dash-dot
```

## Font and Sizing

### Font Recommendations

| Element | Size | Font |
|---------|------|------|
| Title | 12-14pt | Bold |
| Axis labels | 10-12pt | Regular |
| Tick labels | 8-10pt | Regular |
| Legend | 8-10pt | Regular |
| Annotations | 8-10pt | Regular |

### Sizing for Publication

```
# Typical single-column width
fig, ax = plt.subplots(figsize=(3.5, 2.5))  # inches

# Two-column width
fig, ax = plt.subplots(figsize=(7, 4))

# Save at appropriate DPI
plt.savefig('figure.pdf', dpi=300, bbox_inches='tight')
```

### LaTeX Integration

```latex
% In document preamble
\usepackage{graphicx}

% Figure with caption
\begin{figure}[t]
  \centering
  \includegraphics[width=\columnwidth]{figure.pdf}
  \caption{Description of figure.}
  \label{fig:example}
\end{figure}

% Reference in text
As shown in Figure~\ref{fig:example}, ...
```

## Common Mistakes

### Data Visualization Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Truncated y-axis | Exaggerates differences | Start at 0 for bar charts |
| Dual y-axes | Misleading comparison | Use separate panels |
| 3D charts | Distorts perception | Use 2D alternatives |
| Pie charts | Hard to compare angles | Use bar charts |
| Too many categories | Cluttered | Group or filter |

### Table Mistakes

| Mistake | Solution |
|---------|----------|
| Too many digits | Round to significant figures |
| Missing units | Add to column headers |
| Inconsistent formatting | Standardize across columns |
| Vertical lines | Remove (use horizontal only) |
| No notes | Add necessary explanations |

## Statistical Visualization

### Error Bars

| Type | When to Use |
|------|-------------|
| Standard deviation (SD) | Showing data spread |
| Standard error (SEM) | Showing precision of mean |
| 95% CI | Showing confidence in estimate |

```python
# Standard deviation
plt.errorbar(x, y, yerr=std, fmt='o', capsize=5)

# 95% CI (assuming normal distribution)
ci = 1.96 * std / np.sqrt(n)
plt.errorbar(x, y, yerr=ci, fmt='o', capsize=5)
```

### Significance Indicators

```
ns (not significant)   p > 0.05
*                      p ≤ 0.05
**                     p ≤ 0.01
***                    p ≤ 0.001
****                   p ≤ 0.0001
```

### Statistical Tables

```
Table 3
Statistical Tests for Model Comparison

┌──────────────┬────────┬────────┬──────────┬──────────┐
│ Comparison   │ t-stat │ df     │ p-value  │ Cohen's d│
├──────────────┼────────┼────────┼──────────┼──────────┤
│ Ours vs. A   │ 3.42   │ 58     │ .001**   │ 0.89     │
│ Ours vs. B   │ 2.15   │ 58     │ .035*    │ 0.56     │
│ Ours vs. C   │ 0.92   │ 58     │ .362 ns  │ 0.24     │
└──────────────┴────────┴────────┴──────────┴──────────┘

Note. *p < .05, **p < .01, ***p < .001.
```

## ML-Specific Figures

### Training Curves

```python
def plot_training_curves(history):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Loss
    axes[0].plot(history['train_loss'], label='Train')
    axes[0].plot(history['val_loss'], label='Validation')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Accuracy
    axes[1].plot(history['train_acc'], label='Train')
    axes[1].plot(history['val_acc'], label='Validation')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
```

### Attention Visualization

```python
def plot_attention(attention_weights, tokens):
    plt.figure(figsize=(8, 8))
    sns.heatmap(attention_weights,
                xticklabels=tokens,
                yticklabels=tokens,
                cmap='viridis',
                square=True)
    plt.xlabel('Key')
    plt.ylabel('Query')
```

### Model Architecture

Use tools like:
- TensorBoard graph visualization
- Netron for saved models
- draw.io for conceptual diagrams

## Checklist

### Before Submission

**Figures:**
- [ ] Resolution at least 300 DPI
- [ ] Vector format (PDF, SVG) preferred
- [ ] All text readable at printed size
- [ ] Colorblind-safe palette used
- [ ] Consistent style across figures
- [ ] Captions are informative
- [ ] Referenced in main text

**Tables:**
- [ ] Title above table
- [ ] Horizontal lines only
- [ ] Numbers right-aligned
- [ ] Decimals consistent
- [ ] Units specified
- [ ] Notes included
- [ ] Referenced in main text

## References

- Tufte, E. R. (2001). The Visual Display of Quantitative Information
- Few, S. (2012). Show Me the Numbers
- Wilke, C. O. (2019). Fundamentals of Data Visualization
- Nature Methods Points of View column