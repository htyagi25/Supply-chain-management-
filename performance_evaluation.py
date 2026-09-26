"""
performance_evaluation.py
===========================

Week 6 Task: Performance Evaluation and Improvement Recommendations
-------------------------------------------------------------------
Builds the two supporting charts for the Week 6 capstone report:
  1. A KPI scorecard (current vs. target, all six Week 2 KPIs, normalized
     to a 0-100 "percent of target achieved" scale so metrics with very
     different units can be compared on one axis)
  2. An Impact vs. Effort matrix for the six strategic recommendations

Also reproduces the worked capstone calculations quoted in the report
(Perfect Order Rate improvement, safety-stock savings, freight cost
impact), all built on figures already established in Weeks 2 and 4.

Usage
-----
    pip install -r requirements.txt
    python performance_evaluation.py

Output: ./output/kpi_scorecard.png, ./output/impact_effort_matrix.png
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUTPUT_DIR = "output"
NAVY = "#1F4E79"
RED = "#C0392B"
AMBER = "#D68910"
GREEN = "#2E7D46"


# ---------------------------------------------------------------------------
# Worked capstone calculations (reusing Week 2 / Week 4 figures)
# ---------------------------------------------------------------------------
def worked_calculations():
    current_por = 0.90 * 0.95 * 0.97 * 0.98 * 100
    target_por = 0.96 * 0.95 * 0.97 * 0.98 * 100
    print(f"Perfect Order Rate, current on-time=90%: {current_por:.1f}%")
    print(f"Perfect Order Rate, target on-time=96%:  {target_por:.1f}%  "
          f"(+{target_por - current_por:.1f} points)")

    safety_stock_savings_per_sku = 22.7 * 2  # units * $/unit/month, from Week 4
    print(f"Safety-stock savings per SKU/month: ${safety_stock_savings_per_sku:.1f}")
    print(f"Across 50 SKUs: ${safety_stock_savings_per_sku * 50:,.0f}/month "
          f"(${safety_stock_savings_per_sku * 50 * 12:,.0f}/year)")

    freight_excess = (5.10 - 4.20) * 50_000
    print(f"Freight cost excess: ${freight_excess:,.0f}/month "
          f"(${freight_excess * 12:,.0f}/year if sustained)")


# ---------------------------------------------------------------------------
# Chart 1: KPI scorecard (percent of target achieved)
# ---------------------------------------------------------------------------
def make_scorecard(path):
    # (KPI, current, target, "higher is better"?)
    rows = [
        ("OTIF", 90.0, 96.0, True),
        ("Perfect Order Rate", 83.1, 90.0, True),
        ("Inventory Turnover", 6.0, 8.0, True),
        ("Fill Rate", 84.0, 97.0, True),
        ("Cash-to-Cash Cycle", 42, 31, False),   # lower is better
        ("Freight Cost/Unit", 5.10, 4.20, False),  # lower is better
    ]
    labels, pct_achieved, colors = [], [], []
    for name, cur, tgt, higher_better in rows:
        pct = (cur / tgt * 100) if higher_better else (tgt / cur * 100)
        pct = min(pct, 100)
        labels.append(name)
        pct_achieved.append(pct)
        colors.append(GREEN if pct >= 95 else AMBER if pct >= 80 else RED)

    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    bars = ax.barh(labels, pct_achieved, color=colors)
    for b, p in zip(bars, pct_achieved):
        ax.annotate(f"{p:.0f}%", (p, b.get_y() + b.get_height() / 2), textcoords="offset points",
                    xytext=(5, 0), va="center", fontsize=9, fontweight="bold")
    ax.axvline(95, color="grey", linestyle="--", linewidth=1)
    ax.text(95, len(labels) - 0.3, " 95% = healthy", fontsize=7.5, color="grey")
    ax.set_xlim(0, 115)
    ax.set_xlabel("% of target achieved")
    ax.set_title("KPI Scorecard: Current Performance vs. Target (Week 2 definitions)",
                 fontsize=11, fontweight="bold", loc="left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(path, dpi=200, facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Chart 2: Impact vs. Effort matrix for recommendations
# ---------------------------------------------------------------------------
def make_impact_effort_matrix(path):
    # (short label, effort 1-10, impact 1-10, annualized $ impact, color)
    recs = [
        ("R1: Adopt regression forecasting\n($27K/yr)", 2, 8.5, GREEN),
        ("R2: Fix on-time delivery process\n(POR +5.4 pts)", 7.5, 9.2, RED),
        ("R3: Renegotiate freight contracts\n($540K/yr)", 4.3, 6.8, RED),
        ("R4: Inventory cycle-count program\n(Turns 6\u21928x)", 6.3, 4.8, AMBER),
        ("R5: External-indicator early warning\n(leading signal)", 2, 5), 
        ("R6: Carrier scorecarding\n(OTIF support)", 8.5, 6.5, AMBER),
    ]
    recs[4] = recs[4] + (GREEN,)
    fig, ax = plt.subplots(figsize=(9.5, 6.8))
    ax.axvspan(0, 5, 0, 0.5, color="#FBEAEA", alpha=0.5)
    ax.axvspan(5, 10, 0.5, 1, color="#E7F3EA", alpha=0.5)
    ax.axvspan(0, 5, 0.5, 1, color="#E7F3EA", alpha=0.8)
    ax.axvspan(5, 10, 0, 0.5, color="#FDF3E3", alpha=0.5)

    for label, effort, impact, color in recs:
        ax.scatter([effort], [impact], s=420, color=color, edgecolor="white", linewidth=1.5, zorder=5)
        ax.annotate(label, (effort, impact), textcoords="offset points", xytext=(0, 18),
                    ha="center", fontsize=8, fontweight="bold")

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10.6)
    ax.set_xlabel("Effort to implement \u2192")
    ax.set_ylabel("Impact on supply chain performance \u2192")
    ax.set_title("Strategic Recommendations: Impact vs. Effort", fontsize=12, fontweight="bold", loc="left")
    ax.text(0.2, 10.15, "QUICK WINS", fontsize=9, fontweight="bold", color=GREEN)
    ax.text(8.6, 10.15, "MAJOR", fontsize=9, fontweight="bold", color=AMBER, ha="center")
    ax.text(1.2, 0.6, "FILL-IN", fontsize=9, fontweight="bold", color="#888888")
    ax.text(6.8, 0.6, "RECONSIDER", fontsize=9, fontweight="bold", color=RED)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=200, facecolor="white")
    plt.close(fig)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    worked_calculations()
    make_scorecard(os.path.join(OUTPUT_DIR, "kpi_scorecard.png"))
    make_impact_effort_matrix(os.path.join(OUTPUT_DIR, "impact_effort_matrix.png"))
    print(f"\nCharts written to ./{OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
