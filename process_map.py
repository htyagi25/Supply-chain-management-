"""
process_map.py
===============

Week 3 Task: Supply Chain Process Mapping and Visualization
-------------------------------------------------------------
Draws the six-stage supply chain process map used in the Week 3 report,
plus a "Data & Analytics Layer" beneath it showing which KPI (Week 2) or
public data source (Week 1) would be used to monitor each stage.

This is the actual code referenced in the report's "Tools and Methods"
section -- the diagram is generated programmatically (matplotlib), not
hand-drawn, so it can be regenerated or modified by editing the STAGES
list below.

Usage
-----
    pip install -r requirements.txt
    python process_map.py

Output: ./output/supply_chain_process_map.png
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUTPUT_DIR = "output"

NAVY = "#1F4E79"
LIGHT_BLUE = "#DCE6F1"
ACCENT = "#C0392B"
GREY = "#595959"

# Each stage: (title, one-line role, monitoring KPI/data point)
STAGES = [
    ("Demand\nPlanning", "Forecast future demand from\nhistorical sales & market signals",
     "Forecast accuracy / MAPE"),
    ("Procurement", "Source raw materials & goods\nfrom qualified suppliers",
     "Supplier on-time rate"),
    ("Inventory\nManagement", "Store, track, and replenish\nstock across warehouses",
     "Inventory Turnover"),
    ("Order\nFulfillment", "Pick, pack, and prepare\ncustomer orders",
     "Fill Rate"),
    ("Distribution &\nTransportation", "Move goods from warehouse\nto customer/retail node",
     "OTIF / Freight Cost per Unit"),
    ("Customer\nDelivery", "Final handoff and\nproof of delivery",
     "Perfect Order Rate"),
]


def draw_process_map(path):
    n = len(STAGES)
    fig, ax = plt.subplots(figsize=(13, 5.5))

    box_w, box_h = 1.85, 1.15
    gap = 0.55
    y_top = 3.4
    y_bottom = 1.1

    centers_x = []
    for i in range(n):
        x = i * (box_w + gap)
        centers_x.append(x + box_w / 2)

        # Main process box
        box = FancyBboxPatch((x, y_top), box_w, box_h,
                              boxstyle="round,pad=0.04,rounding_size=0.08",
                              linewidth=1.6, edgecolor=NAVY,
                              facecolor=LIGHT_BLUE if i % 2 == 0 else "white")
        ax.add_patch(box)
        ax.text(x + box_w / 2, y_top + box_h * 0.62, STAGES[i][0],
                ha="center", va="center", fontsize=11.5, fontweight="bold", color=NAVY)
        ax.text(x + box_w / 2, y_top + box_h * 0.24, STAGES[i][1],
                ha="center", va="center", fontsize=7.6, color="#333333")

        # Arrow to next stage
        if i < n - 1:
            arrow = FancyArrowPatch((x + box_w, y_top + box_h / 2),
                                     (x + box_w + gap, y_top + box_h / 2),
                                     arrowstyle="-|>", mutation_scale=16,
                                     linewidth=1.8, color=NAVY)
            ax.add_patch(arrow)

        # Dashed connector down to the analytics layer
        ax.plot([x + box_w / 2, x + box_w / 2], [y_top, y_bottom + 0.55],
                linestyle=":", linewidth=1.2, color=GREY)

        # Analytics layer node
        kbox = FancyBboxPatch((x, y_bottom), box_w, 0.55,
                               boxstyle="round,pad=0.03,rounding_size=0.06",
                               linewidth=1.2, edgecolor=ACCENT, facecolor="#FBEAEA")
        ax.add_patch(kbox)
        ax.text(x + box_w / 2, y_bottom + 0.275, STAGES[i][2],
                ha="center", va="center", fontsize=7.3, color=ACCENT, fontweight="bold")

    # Feedback loop arrow (Customer Delivery -> Demand Planning), routed above all boxes
    last_x = centers_x[-1]
    first_x = centers_x[0]
    y_box_top = y_top + box_h
    y_loop = y_box_top + 0.9
    ax.plot([last_x, last_x], [y_box_top + 0.08, y_loop], color="#7F7F7F", lw=1.4)
    ax.plot([first_x, first_x], [y_box_top + 0.08, y_loop], color="#7F7F7F", lw=1.4)
    ax.annotate("", xy=(first_x, y_loop), xytext=(last_x, y_loop),
                arrowprops=dict(arrowstyle="-", color="#7F7F7F", lw=1.4))
    ax.annotate("", xy=(first_x, y_box_top + 0.08), xytext=(first_x, y_loop - 0.02),
                arrowprops=dict(arrowstyle="-|>", color="#7F7F7F", lw=1.4, mutation_scale=14))
    ax.text((first_x + last_x) / 2, y_loop + 0.22, "Delivery & sales data feed back into demand planning",
            ha="center", va="center", fontsize=8.3, color="#7F7F7F", style="italic")

    # Layer labels on the left
    ax.text(-0.45, y_top + box_h / 2, "Process\nFlow", ha="right", va="center",
            fontsize=9.5, fontweight="bold", color=NAVY)
    ax.text(-0.45, y_bottom + 0.275, "Data &\nAnalytics\nLayer", ha="right", va="center",
            fontsize=9.5, fontweight="bold", color=ACCENT)

    ax.set_xlim(-1.6, centers_x[-1] + box_w / 2 + 0.3)
    ax.set_ylim(0.6, y_loop + 0.65)
    ax.axis("off")
    ax.set_title("End-to-End Supply Chain Process Map with Analytics Monitoring Layer",
                 fontsize=13, fontweight="bold", color=NAVY, pad=14)
    fig.tight_layout()
    fig.savefig(path, dpi=220, facecolor="white")
    plt.close(fig)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, "supply_chain_process_map.png")
    draw_process_map(out_path)
    print(f"Process map saved to {out_path}")


if __name__ == "__main__":
    main()
