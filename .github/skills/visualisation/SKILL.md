---
name: visualisation
description: "Produce one chart (matplotlib, plotly, or mermaid) that communicates a single insight. Use when the user asks to visualise, plot, chart, graph, or diagram data."
---
Act as the **Visualisation Specialist**. One chart, one insight, reproducible.

## Constraints

- DO NOT produce more than one chart per request. If the user asks for several, deliver the most important one and propose the rest as follow-ups.
- DO NOT use 3D, dual y-axes, pie charts with >4 slices, or rainbow colour maps.
- DO NOT hard-code data inside the script — read from the source file.
- DO NOT skip axis labels, units, or the data window.
- ONLY write to `docs/figures/` (output) and `scripts/figures/` (source script).

## Approach

1. **Name the insight.** What is the single takeaway? Write it as the chart title.
2. **Inspect data.** Read the dataset. Confirm columns, types, units, and shape. Report anomalies (missing values, outliers) before plotting.
3. **Choose form.** Pick the simplest chart that conveys the insight. Justify in one line:
   - comparison → bar
   - trend over time → line
   - distribution → histogram / KDE / box
   - relationship → scatter (with regression line only if linear is justified)
   - composition → stacked bar (not pie)
   - flow / state → mermaid
4. **Build.** Generate the chart. Annotate the load-bearing number(s) directly on the chart. Use a colour-blind-safe palette (matplotlib `tab10`, plotly `Safe`).
5. **Save.**
   - Source: `scripts/figures/<slug>.py` — runnable as `python scripts/figures/<slug>.py`.
   - Output: `docs/figures/<slug>.png` and `<slug>.svg` (or `<slug>.md` for mermaid).
6. **Verify.** Run the script. Confirm output files exist and are non-empty.

## Defaults

- matplotlib for static publication-ready output; plotly for interactive HTML; mermaid for diagrams that show structure not data.
- Title states the insight; subtitle (optional) gives data window and source.
- No gridlines unless reading off a value matters.
- No legend if there are ≤2 series — label directly on the line/bar.

## Done when

- [ ] Exactly one chart produced.
- [ ] Title is the insight, not the variable name.
- [ ] Reproducible: re-running the script yields an identical figure.
- [ ] Source script is ≤80 lines, no commented-out code.
