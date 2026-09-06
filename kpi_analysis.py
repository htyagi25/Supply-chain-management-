"""
kpi_analysis.py
================

Week 2 Task: Supply Chain KPI Identification and Analysis
-------------------------------------------------------------
Reproduces every formula, number, and chart used in the Week 2 report
(Week2_KPI_Identification_and_Analysis.docx). Each KPI is implemented as an
independent, testable function; the __main__ block below calls each one with
the exact inputs cited in the report (either a published benchmark example
or a hypothetical scenario built on the DataCo order-level schema from
Week 1) and regenerates the two supporting charts.

This directly addresses Week 1 feedback: rather than only describing how
charts/tables were produced, this script *is* that process, runnable
end-to-end.

Usage
-----
    pip install -r requirements.txt
    python kpi_analysis.py

Outputs (written to ./output/):
    - perfect_order_rate.png
    - cash_to_cash.png
    - kpi_summary.csv
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

OUTPUT_DIR = "output"


# ---------------------------------------------------------------------------
# KPI formulas -- one small, independent function per metric
# ---------------------------------------------------------------------------
def on_time_in_full(on_time_and_in_full_orders: int, total_orders: int) -> float:
    """OTIF % = orders delivered both on-time AND in-full / total orders x 100."""
    return on_time_and_in_full_orders / total_orders * 100


def perfect_order_rate(on_time_pct, in_full_pct, damage_free_pct, accurate_docs_pct) -> float:
    """Perfect Order Rate = product of four component rates (each as a decimal, e.g. 0.92)."""
    return on_time_pct * in_full_pct * damage_free_pct * accurate_docs_pct * 100


def inventory_turnover(cogs: float, avg_inventory: float) -> float:
    """Inventory Turnover Ratio = COGS / Average Inventory Value."""
    return cogs / avg_inventory


def days_inventory_from_turnover(turnover: float, days_in_period: int = 365) -> float:
    """Convenience: convert a turnover ratio into an equivalent inventory cycle in days."""
    return days_in_period / turnover


def fill_rate(orders_fulfilled_in_full: int, total_orders_received: int) -> float:
    """Fill Rate % = orders fulfilled in full / total orders received x 100."""
    return orders_fulfilled_in_full / total_orders_received * 100


def cash_to_cash_cycle(dio: float, dso: float, dpo: float) -> float:
    """Cash-to-Cash Cycle Time (days) = DIO + DSO - DPO."""
    return dio + dso - dpo


def freight_cost_per_unit(total_freight_cost: float, total_units_shipped: int) -> float:
    """Freight Cost per Unit = total freight cost / total units shipped."""
    return total_freight_cost / total_units_shipped


# ---------------------------------------------------------------------------
# Chart generation -- built directly from the function outputs above
# ---------------------------------------------------------------------------
def make_perfect_order_chart(on_time, in_full, damage_free, accurate_docs, combined, path):
    labels = ["On-time", "In-full", "Damage-free", "Accurate docs", "Perfect\nOrder Rate"]
    values = [on_time * 100, in_full * 100, damage_free * 100, accurate_docs * 100, combined]
    colors = ["#4a7ab5"] * 4 + ["#c0392b"]

    fig, ax = plt.subplots(figsize=(7.2, 4))
    bars = ax.bar(labels, values, color=colors, width=0.6)
    for b, v in zip(bars, values):
        ax.annotate(f"{v:.1f}%", (b.get_x() + b.get_width() / 2, v),
                    textcoords="offset points", xytext=(0, 6), ha="center", fontweight="bold")
    ax.set_ylim(0, 110)
    ax.set_ylabel("Rate (%)")
    ax.set_title("Perfect Order Rate: Four Components Compound Multiplicatively")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def make_cash_to_cash_chart(dio, dso, dpo, ccc, path):
    cats = [f"DIO\n({dio:g} days)", f"DSO\n({dso:g} days)", f"DPO\n({-dpo:g} days)",
            f"Cash-to-Cash\nCycle ({ccc:g} days)"]
    vals = [dio, dso, -dpo, ccc]
    colors = ["#4a7ab5", "#4a7ab5", "#7fb069", "#c0392b"]

    fig, ax = plt.subplots(figsize=(7.2, 4))
    bars = ax.bar(cats, vals, color=colors, width=0.55)
    for b, v in zip(bars, vals):
        ax.annotate(f"{v:+.0f}", (b.get_x() + b.get_width() / 2, v),
                    textcoords="offset points", xytext=(0, 6 if v >= 0 else -16),
                    ha="center", fontweight="bold")
    ax.axhline(0, color="#888888", linewidth=1)
    ax.set_ylabel("Days")
    ax.set_title("Cash-to-Cash Cycle Time: DIO + DSO \u2212 DPO")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------------------
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    rows = []

    # --- 1. OTIF: hypothetical distributor, 10,000 orders/month ---
    otif_before = on_time_in_full(9600, 10000)
    otif_after = on_time_in_full(9000, 10000)
    print(f"OTIF before: {otif_before:.1f}% | after a lane disruption: {otif_after:.1f}%")
    rows.append(("OTIF (before)", otif_before, "%"))
    rows.append(("OTIF (after disruption)", otif_after, "%"))

    # --- 2. Perfect Order Rate: published compounding example ---
    on_time, in_full, damage_free, accurate_docs = 0.92, 0.95, 0.97, 0.98
    combined = perfect_order_rate(on_time, in_full, damage_free, accurate_docs)
    print(f"Perfect Order Rate: {combined:.1f}% (from {on_time*100:.0f}/{in_full*100:.0f}/"
          f"{damage_free*100:.0f}/{accurate_docs*100:.0f} component rates)")
    make_perfect_order_chart(on_time, in_full, damage_free, accurate_docs, combined,
                              os.path.join(OUTPUT_DIR, "perfect_order_rate.png"))
    rows.append(("Perfect Order Rate", combined, "%"))

    # --- 3. Inventory Turnover: hypothetical electronics retailer ---
    turnover_before = inventory_turnover(6_000_000, 750_000)
    turnover_after = inventory_turnover(6_000_000, 1_000_000)
    print(f"Inventory turnover: {turnover_before:.1f}x "
          f"({days_inventory_from_turnover(turnover_before):.0f}-day cycle) -> "
          f"{turnover_after:.1f}x ({days_inventory_from_turnover(turnover_after):.0f}-day cycle) "
          f"after inventory rises to $1M")
    rows.append(("Inventory Turnover (before)", turnover_before, "x/yr"))
    rows.append(("Inventory Turnover (after)", turnover_after, "x/yr"))

    # --- 4. Fill Rate: 50 orders, 42 fulfilled in full ---
    fr = fill_rate(42, 50)
    print(f"Fill rate: {fr:.0f}%")
    rows.append(("Fill Rate", fr, "%"))

    # --- 5. Cash-to-Cash Cycle Time: published DIO/DSO/DPO example ---
    dio, dso, dpo = 41, 33, 32
    ccc = cash_to_cash_cycle(dio, dso, dpo)
    print(f"Cash-to-Cash Cycle Time: {ccc:.0f} days (DIO {dio} + DSO {dso} - DPO {dpo})")
    make_cash_to_cash_chart(dio, dso, dpo, ccc, os.path.join(OUTPUT_DIR, "cash_to_cash.png"))
    rows.append(("Cash-to-Cash Cycle Time", ccc, "days"))

    # Sensitivity: what if DIO improves to 30 days?
    ccc_improved = cash_to_cash_cycle(30, dso, dpo)
    freed_cash = 15_000_000 / 365 * (ccc - ccc_improved)
    print(f"If DIO improves to 30 days: CCC falls to {ccc_improved:.0f} days, "
          f"freeing ~${freed_cash:,.0f} in working capital at $15M annual revenue")
    rows.append(("Cash-to-Cash Cycle Time (DIO improved)", ccc_improved, "days"))

    # --- 6. Freight Cost per Unit: before/after a shipping-pressure spike ---
    fcpu_before = freight_cost_per_unit(210_000, 50_000)   # $4.20/unit
    fcpu_after = freight_cost_per_unit(255_000, 50_000)    # $5.10/unit
    print(f"Freight cost per unit: ${fcpu_before:.2f} -> ${fcpu_after:.2f} "
          f"(+${(fcpu_after - fcpu_before) * 50_000:,.0f}/month total)")
    rows.append(("Freight Cost per Unit (before)", fcpu_before, "$/unit"))
    rows.append(("Freight Cost per Unit (after)", fcpu_after, "$/unit"))

    summary = pd.DataFrame(rows, columns=["kpi", "value", "unit"])
    summary.to_csv(os.path.join(OUTPUT_DIR, "kpi_summary.csv"), index=False)
    print(f"\nAll outputs written to ./{OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
