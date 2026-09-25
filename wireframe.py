"""
wireframe.py
=============

Week 5 Task: Development of Data Dashboards and Reporting
-------------------------------------------------------------
Draws the low-fidelity wireframe used in the Week 5 report's design
process (Section 4.1) -- the layout planning stage before the
high-fidelity mock-up (dashboard_mockup.py) is populated with real data.

Usage
-----
    pip install -r requirements.txt
    python wireframe.py

Output: ./output/wireframe.png
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUTPUT_DIR = "output"


fig, ax = plt.subplots(figsize=(11, 7.2))
GREY = "#888888"
DARK = "#333333"

def region(x, y, w, h, label, fontsize=10):
    ax.add_patch(Rectangle((x, y), w, h, linewidth=1.4, edgecolor=GREY,
                            facecolor="none", linestyle="--"))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=fontsize, color=DARK, wrap=True)

# Header
region(0.02, 0.92, 0.96, 0.06, "Header: Title + reporting period + data-source footnote", 9)
# KPI row
region(0.02, 0.78, 0.96, 0.12, "KPI Card Row  (6 cards: OTIF | Perfect Order | Turnover |\nFill Rate | Cash-to-Cash | Freight $/Unit)  \u2014 color-coded by status", 9.5)
# Two charts
region(0.02, 0.52, 0.47, 0.24, "Chart A:\nExternal market-pressure trend\n(line chart, time series)", 10)
region(0.51, 0.52, 0.47, 0.24, "Chart B:\nDemand forecast \u2014 actual vs. model\n(multi-line comparison)", 10)
# Process strip
region(0.02, 0.40, 0.96, 0.10, "Process Health Strip  (6 stage boxes, red/amber/green status dot)", 9.5)
# Table + chart
region(0.02, 0.06, 0.47, 0.32, "Exception / Alert Table\n(Lane \u2013 SKU \u2013 DC | KPI | Value | Threshold)\nsortable, filterable, red-highlighted rows", 10)
region(0.51, 0.06, 0.47, 0.32, "Chart C:\nKPI driver breakdown\n(bar chart, component contributions)", 10)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
ax.set_title("Dashboard Layout Plan \u2014 Low-Fidelity Wireframe (Planning Stage)",
             fontsize=13, fontweight="bold", color="#1F4E79", pad=14)
fig.tight_layout()

os.makedirs(OUTPUT_DIR, exist_ok=True)
out_path = os.path.join(OUTPUT_DIR, "wireframe.png")
fig.savefig(out_path, dpi=200, facecolor="white")
print(f"Wireframe saved to {out_path}")
