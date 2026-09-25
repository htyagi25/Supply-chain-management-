"""
dashboard_mockup.py
====================

Week 5 Task: Development of Data Dashboards and Reporting
-------------------------------------------------------------
Renders a high-fidelity dashboard mock-up (not a wireframe sketch) using
the actual KPI values, GSCPI trend, and demand-forecast results generated
in Weeks 1-4 of this coursework, so the mock-up is populated with real
worked numbers rather than placeholder data.

Usage
-----
    pip install -r requirements.txt
    python dashboard_mockup.py

Output: ./output/dashboard_mockup.png
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.gridspec as gridspec

OUTPUT_DIR = "output"

NAVY = "#1F4E79"
RED = "#C0392B"
AMBER = "#D68910"
GREEN = "#2E7D46"
GREY = "#595959"
LIGHT = "#F2F5F9"
CARDBG = "white"

# KPI cards: (label, value, delta_text, status_color, source_note)
KPIS = [
    ("On-Time In-Full", "90.0%", "\u2193 6.0 pts vs target 96%", RED, "Week 2"),
    ("Perfect Order Rate", "83.1%", "compounded from 4 sub-rates", AMBER, "Week 2"),
    ("Inventory Turnover", "6.0x", "\u2193 from 8.0x baseline", RED, "Week 2"),
    ("Fill Rate", "84%", "below 96\u201399% benchmark", AMBER, "Week 2"),
    ("Cash-to-Cash Cycle", "42 days", "target 31 days", AMBER, "Week 2"),
    ("Freight Cost / Unit", "$5.10", "\u2191 $0.90 vs last period", RED, "Week 2"),
]

# GSCPI trend (Week 1)
gscpi_months = ["Jan 2026", "Feb 2026", "Mar 2026", "Apr 2026"]
gscpi_vals = [0.41, 0.55, 0.68, 1.82]

# Demand forecast comparison (Week 4), months 33-36
fc_months = ["M33", "M34", "M35", "M36"]
actual = [1500, 1289, 1207, 1271]
hw_forecast = [1594, 1392, 1355, 1432]
reg_forecast = [1483, 1273, 1191, 1294]

# Process stage status strip (Week 3), colored by which KPI above is breached
stages = [
    ("Demand\nPlanning", GREEN), ("Procurement", AMBER), ("Inventory\nManagement", RED),
    ("Order\nFulfillment", AMBER), ("Distribution &\nTransportation", RED),
    ("Customer\nDelivery", AMBER),
]

# Exception table rows: (Lane/SKU, KPI, Value, Threshold)
exceptions = [
    ("Lane: MW\u2192NE", "OTIF", "88.2%", "< 92%"),
    ("SKU: WB-2201", "Fill Rate", "76%", "< 90%"),
    ("Lane: Import-EU", "Freight $/Unit", "$6.40", "> $5.50"),
    ("DC: Regional-3", "Inventory Turns", "5.1x", "< 6.0x"),
]


def card(ax, x, y, w, h, label, value, delta, color):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.05",
                          linewidth=1.4, edgecolor=color, facecolor=CARDBG)
    ax.add_patch(box)
    ax.add_patch(FancyBboxPatch((x, y + h - 0.06), w, 0.06, boxstyle="round,pad=0,rounding_size=0.0",
                                 linewidth=0, facecolor=color))
    ax.text(x + w / 2, y + h * 0.62, value, ha="center", va="center",
            fontsize=17, fontweight="bold", color=NAVY)
    ax.text(x + w / 2, y + h * 0.34, label, ha="center", va="center",
            fontsize=8.3, fontweight="bold", color="#333333")
    ax.text(x + w / 2, y + h * 0.14, delta, ha="center", va="center",
            fontsize=7, color=color)


def build_dashboard(path):
    fig = plt.figure(figsize=(14, 9))
    fig.patch.set_facecolor("white")
    gs = gridspec.GridSpec(4, 6, figure=fig, height_ratios=[0.9, 2.0, 1.1, 1.3],
                            hspace=0.55, wspace=0.5, left=0.04, right=0.98, top=0.90, bottom=0.04)

    # --- Header ---
    fig.text(0.04, 0.965, "Supply Chain Performance Dashboard", fontsize=18, fontweight="bold", color=NAVY)
    fig.text(0.04, 0.94, "Week ending Apr 30, 2026  |  Data sources: Weeks 1\u20134 (GSCPI, LPI, DataCo, KPI & forecast models)",
             fontsize=9, color=GREY)

    # --- KPI card row (use a dedicated axes overlay) ---
    card_ax = fig.add_axes([0.04, 0.735, 0.94, 0.16])
    card_ax.set_xlim(0, 6)
    card_ax.set_ylim(0, 1)
    card_ax.axis("off")
    cw = 0.94
    for i, (label, value, delta, color, _) in enumerate(KPIS):
        card(card_ax, i + 0.03, 0.03, cw, 0.94, label, value, delta, color)

    # --- GSCPI trend chart ---
    ax1 = fig.add_subplot(gs[1, 0:3])
    ax1.plot(gscpi_months, gscpi_vals, "o-", color=NAVY, linewidth=2.2, markersize=6)
    for x, y in zip(gscpi_months, gscpi_vals):
        ax1.annotate(f"{y:.2f}", (x, y), textcoords="offset points", xytext=(0, 8),
                     ha="center", fontsize=8, fontweight="bold", color=NAVY)
    ax1.axhline(0, color="grey", linestyle="--", linewidth=0.8)
    ax1.set_title("External Market Pressure (GSCPI) \u2014 Week 1", fontsize=10.5, fontweight="bold", loc="left")
    ax1.set_ylabel("Index", fontsize=8)
    ax1.tick_params(labelsize=8)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.grid(axis="y", linestyle=":", alpha=0.4)

    # --- Demand forecast comparison chart ---
    ax2 = fig.add_subplot(gs[1, 3:6])
    ax2.plot(fc_months, actual, "o-", color=NAVY, label="Actual", linewidth=2.2, markersize=6)
    ax2.plot(fc_months, hw_forecast, "s--", color=RED, label="Holt-Winters (9.8% MAPE)", linewidth=1.6, markersize=5)
    ax2.plot(fc_months, reg_forecast, "^--", color=GREEN, label="Regression (1.4% MAPE)", linewidth=1.6, markersize=5)
    ax2.set_title("Demand Forecast: Actual vs. Model \u2014 Week 4", fontsize=10.5, fontweight="bold", loc="left")
    ax2.set_ylabel("Units", fontsize=8)
    ax2.tick_params(labelsize=8)
    ax2.legend(fontsize=7, loc="upper right")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.grid(axis="y", linestyle=":", alpha=0.4)

    # --- Process stage status strip ---
    ax3 = fig.add_subplot(gs[2, 0:6])
    ax3.set_xlim(0, len(stages))
    ax3.set_ylim(0, 1)
    ax3.axis("off")
    ax3.text(-0.02, 1.15, "Process Health by Stage \u2014 Week 3", fontsize=10.5, fontweight="bold",
              color=NAVY, transform=ax3.transAxes)
    for i, (name, color) in enumerate(stages):
        box = FancyBboxPatch((i + 0.06, 0.15), 0.88, 0.65, boxstyle="round,pad=0.02,rounding_size=0.06",
                              linewidth=1.3, edgecolor=color, facecolor=LIGHT)
        ax3.add_patch(box)
        ax3.text(i + 0.5, 0.475, name, ha="center", va="center", fontsize=8.2, fontweight="bold", color=NAVY)
        dot_color = color
        ax3.scatter([i + 0.82], [0.68], s=60, color=dot_color, zorder=5)

    # --- Exception / alert table ---
    ax4 = fig.add_subplot(gs[3, 0:3])
    ax4.axis("off")
    ax4.text(0, 1.05, "Exception Report (below threshold)", fontsize=10.5, fontweight="bold",
              color=NAVY, transform=ax4.transAxes)
    col_labels = ["Lane / SKU / DC", "KPI", "Value", "Threshold"]
    table = ax4.table(cellText=[list(r) for r in exceptions], colLabels=col_labels,
                       loc="center", cellLoc="left", bbox=[0, 0, 1, 0.85])
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    for (r, c), cell_ in table.get_celld().items():
        cell_.set_edgecolor("#CCCCCC")
        if r == 0:
            cell_.set_facecolor(NAVY)
            cell_.set_text_props(color="white", fontweight="bold")
        else:
            cell_.set_facecolor("white" if r % 2 else LIGHT)

    # --- Perfect Order Rate compounding mini-chart ---
    ax5 = fig.add_subplot(gs[3, 3:6])
    labels = ["On-time", "In-full", "Damage-\nfree", "Accurate\ndocs", "Perfect\nOrder"]
    values = [92, 95, 97, 98, 83.1]
    colors = [NAVY] * 4 + [RED]
    bars = ax5.bar(labels, values, color=colors, width=0.6)
    for b, v in zip(bars, values):
        ax5.annotate(f"{v:.1f}", (b.get_x() + b.get_width() / 2, v), textcoords="offset points",
                     xytext=(0, 4), ha="center", fontsize=7.5, fontweight="bold")
    ax5.set_title("Perfect Order Rate Drivers \u2014 Week 2", fontsize=10.5, fontweight="bold", loc="left")
    ax5.set_ylim(0, 110)
    ax5.tick_params(labelsize=7.5)
    ax5.spines["top"].set_visible(False)
    ax5.spines["right"].set_visible(False)
    ax5.grid(axis="y", linestyle=":", alpha=0.4)

    fig.savefig(path, dpi=200, facecolor="white")
    plt.close(fig)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, "dashboard_mockup.png")
    build_dashboard(out_path)
    print(f"Dashboard mock-up saved to {out_path}")


if __name__ == "__main__":
    main()
