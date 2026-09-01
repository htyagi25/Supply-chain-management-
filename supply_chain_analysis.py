"""
supply_chain_analysis.py
=========================

Week 1 Task: Data Collection and Preliminary Analysis
-------------------------------------------------------
Reproduces the exploratory analysis described in the accompanying report
(Week1_Data_Collection_Preliminary_Analysis.docx) using three public
supply chain data sources:

  1. NY Fed Global Supply Chain Pressure Index (GSCPI)   -- macro time series
  2. World Bank Logistics Performance Index (LPI 2.0)    -- country panel
  3. DataCo Smart Supply Chain Dataset                   -- order-level data

No private, internal, or access-restricted data is used anywhere in this
script. Sources and access notes for each dataset are documented inline.

Usage
-----
    pip install -r requirements.txt
    python supply_chain_analysis.py

Outputs are written to ./output/:
    - gscpi_trend.png
    - lpi_components.csv
    - dataco_field_summary.csv
    - dataco_delivery_risk_summary.png   (only if a real DataCo CSV is supplied)

To run the DataCo section on the *real* dataset instead of the small
illustrative sample bundled here, download DataCoSupplyChainDataset.csv
from Kaggle or Mendeley Data (see SOURCES below) and pass its path:

    python supply_chain_analysis.py --dataco-csv path/to/DataCoSupplyChainDataset.csv
"""

import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

OUTPUT_DIR = "output"

# ---------------------------------------------------------------------------
# Data sources (see README.md / the Week 1 report for full selection criteria)
# ---------------------------------------------------------------------------
SOURCES = {
    "GSCPI": {
        "publisher": "Federal Reserve Bank of New York",
        "url": "https://www.newyorkfed.org/research/policy/gscpi",
        "access": "Public monthly XLSX/CSV download",
    },
    "LPI 2.0": {
        "publisher": "World Bank",
        "url": "https://lpi.worldbank.org/",
        "access": "Public web portal / Data360 download",
    },
    "DataCo Smart Supply Chain Dataset": {
        "publisher": "DataCo Global (research release)",
        "url": "https://data.mendeley.com/datasets/8gx2fvg2k6/3",
        "access": "Public CSV download (Kaggle mirror also available)",
    },
}


# ---------------------------------------------------------------------------
# 1. GSCPI -- macro supply chain pressure trend
# ---------------------------------------------------------------------------
def analyze_gscpi():
    """Plot the GSCPI's early-2026 trend.

    Values below are the published monthly readings (source: Federal Reserve
    Bank of New York / Trading Economics). Replace `data` with the full
    series pulled from the GSCPI's own XLSX download for a longer-run
    analysis (available back to 1997).
    """
    data = {
        "2026-01": 0.41,
        "2026-02": 0.55,
        "2026-03": 0.68,
        "2026-04": 1.82,
    }
    series = pd.Series(data)
    series.index = pd.PeriodIndex(series.index, freq="M")

    print("\n=== GSCPI: Global Supply Chain Pressure Index ===")
    print(series.to_string())
    print(f"Change Jan->Apr 2026: {series.iloc[-1] - series.iloc[0]:+.2f}")

    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.plot(series.index.astype(str), series.values, marker="o",
            linewidth=2.5, markersize=8, color="#1f4e79")
    for x, y in zip(series.index.astype(str), series.values):
        ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points",
                    xytext=(0, 10), ha="center", fontweight="bold", color="#1f4e79")
    ax.axhline(0, color="#888888", linestyle="--", linewidth=1)
    ax.set_title("NY Fed Global Supply Chain Pressure Index (GSCPI), Jan\u2013Apr 2026")
    ax.set_ylabel("Index value (std. deviations from average)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "gscpi_trend.png"), dpi=200)
    plt.close(fig)
    return series


# ---------------------------------------------------------------------------
# 2. LPI -- structural cross-country logistics performance
# ---------------------------------------------------------------------------
def analyze_lpi():
    """Summarize the six LPI components as a reference table.

    For country-level scores, download the indicator series from
    World Bank Data360 (WB_LPI_20) and merge on `country_code`.
    """
    components = pd.DataFrame([
        ("Customs", "Efficiency of the clearance process (speed, simplicity, predictability)"),
        ("Infrastructure", "Quality of trade- and transport-related infrastructure"),
        ("International shipments", "Ease of arranging competitively priced international shipments"),
        ("Logistics quality & competence", "Competence and quality of logistics services"),
        ("Tracking & tracing", "Ability to track and trace consignments in transit"),
        ("Timeliness", "Frequency with which shipments arrive within the scheduled time"),
    ], columns=["component", "description"])

    print("\n=== LPI 2.0: Six Components ===")
    print(components.to_string(index=False))

    components.to_csv(os.path.join(OUTPUT_DIR, "lpi_components.csv"), index=False)
    return components


# ---------------------------------------------------------------------------
# 3. DataCo -- order-level operational data
# ---------------------------------------------------------------------------
FIELD_GROUPS = pd.DataFrame([
    ("Order & customer", "Order ID/date, customer segment, market, region, order status"),
    ("Product & category", "Product name, category, department, unit price"),
    ("Shipping & delivery", "Shipping mode, scheduled vs. actual shipping days, late-delivery-risk flag"),
    ("Financial", "Sales, discount, profit ratio per order line"),
    ("Geography", "Order/customer city, state, country, latitude/longitude"),
], columns=["field_group", "representative_columns"])


def _load_illustrative_sample():
    """A tiny, hand-built sample with the DataCo schema, used only when no
    real CSV is supplied, so the script runs end-to-end out of the box.
    This is NOT the real dataset and should not be used for conclusions --
    swap in the actual file via --dataco-csv for real analysis.
    """
    return pd.DataFrame({
        "Shipping Mode": ["Standard Class", "First Class", "Second Class",
                           "Standard Class", "Same Day", "First Class"],
        "Order Region": ["West", "East", "West", "Central", "East", "West"],
        "Days for shipping (scheduled)": [4, 2, 3, 4, 1, 2],
        "Days for shipping (real)": [6, 2, 5, 4, 1, 3],
        "Late_delivery_risk": [1, 0, 1, 0, 0, 1],
    })


def analyze_dataco(csv_path: str | None):
    """Summarize the DataCo dataset's schema and, if a real file is given,
    compute a simple late-delivery-risk breakdown by shipping mode.
    """
    print("\n=== DataCo Smart Supply Chain Dataset: Field Groups ===")
    print(FIELD_GROUPS.to_string(index=False))
    FIELD_GROUPS.to_csv(os.path.join(OUTPUT_DIR, "dataco_field_summary.csv"), index=False)

    if csv_path:
        df = pd.read_csv(csv_path, encoding="latin1")
        print(f"\nLoaded real DataCo dataset: {df.shape[0]:,} rows, {df.shape[1]} columns")
    else:
        df = _load_illustrative_sample()
        print("\nNo --dataco-csv supplied; using a small illustrative sample "
              "(schema only, not representative of real volumes).")

    if "Shipping Mode" in df.columns and "Late_delivery_risk" in df.columns:
        risk_by_mode = (
            df.groupby("Shipping Mode")["Late_delivery_risk"]
            .mean()
            .sort_values(ascending=False)
        )
        print("\nLate-delivery risk rate by shipping mode:")
        print(risk_by_mode.to_string())

        fig, ax = plt.subplots(figsize=(6, 4))
        risk_by_mode.plot(kind="bar", ax=ax, color="#1f4e79")
        ax.set_ylabel("Share of orders flagged late-delivery risk")
        ax.set_title("Late-Delivery Risk by Shipping Mode")
        ax.set_xlabel("")
        plt.xticks(rotation=30, ha="right")
        fig.tight_layout()
        fig.savefig(os.path.join(OUTPUT_DIR, "dataco_delivery_risk_summary.png"), dpi=200)
        plt.close(fig)

    return df


# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataco-csv", default=None,
                         help="Path to a downloaded DataCoSupplyChainDataset.csv")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Sources used (all public, no internal/private data):")
    for name, info in SOURCES.items():
        print(f"  - {name}: {info['publisher']} ({info['url']})")

    analyze_gscpi()
    analyze_lpi()
    analyze_dataco(args.dataco_csv)

    print(f"\nAll outputs written to ./{OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
