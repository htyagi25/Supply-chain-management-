# Week 1: Supply Chain Data Collection & Preliminary Analysis

Reproducible companion code for the Week 1 supply chain analytics report.
Explores three public data sources and produces the charts/tables used in
the write-up.

## Data sources

| Source | Publisher | Access |
|---|---|---|
| [GSCPI](https://www.newyorkfed.org/research/policy/gscpi) | Federal Reserve Bank of New York | Public monthly XLSX/CSV |
| [LPI 2.0](https://lpi.worldbank.org/) | World Bank | Public web portal / Data360 |
| [DataCo Smart Supply Chain Dataset](https://data.mendeley.com/datasets/8gx2fvg2k6/3) | DataCo Global | Public CSV (Kaggle mirror also available) |

No private, internal, or access-restricted data is used anywhere in this repo.

## Setup

```bash
pip install -r requirements.txt
python supply_chain_analysis.py
```

To run the delivery-risk breakdown on the **real** DataCo dataset instead of
the small bundled illustrative sample, download `DataCoSupplyChainDataset.csv`
from the link above and run:

```bash
python supply_chain_analysis.py --dataco-csv path/to/DataCoSupplyChainDataset.csv
```

## Outputs

Written to `./output/`:

- `gscpi_trend.png` — GSCPI monthly trend, Jan–Apr 2026
- `lpi_components.csv` — the six LPI components and what each measures
- `dataco_field_summary.csv` — DataCo dataset field groups
- `dataco_delivery_risk_summary.png` — late-delivery risk by shipping mode

## Repo structure

```
.
├── supply_chain_analysis.py
├── requirements.txt
├── README.md
└── output/          (generated on run)
```
