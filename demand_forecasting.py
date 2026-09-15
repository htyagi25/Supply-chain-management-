"""
demand_forecasting.py
======================

Week 4 Task: Predictive Analytics for Demand Forecasting
-------------------------------------------------------------
Builds a 24-month pseudo-data series for a seasonal retail product
(insulated water bottles), then fits and compares two forecasting methods:

  1. Holt-Winters Triple Exponential Smoothing (pure time-series:
     level + trend + seasonality, no external inputs)
  2. Multiple linear regression with an exogenous market-pressure index
     (a GSCPI-style supply chain pressure proxy, per the Week 1 report)

All pseudo-data is clearly synthetic, generated with a fixed random seed
for reproducibility, and is used for conceptual/illustrative purposes only
per the Week 4 task instructions.

Usage
-----
    pip install -r requirements.txt
    python demand_forecasting.py

Outputs (./output/):
    - demand_pseudo_data.csv
    - holt_winters_forecast.png
    - regression_fit.png
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error, r2_score
from statsmodels.tsa.holtwinters import ExponentialSmoothing

OUTPUT_DIR = "output"
RNG = np.random.default_rng(42)


# ---------------------------------------------------------------------------
# 1. Generate 24 months of pseudo-data (illustrative only)
# ---------------------------------------------------------------------------
def generate_pseudo_data(n_months=36):
    months = pd.period_range("2024-01", periods=n_months, freq="M")
    t = np.arange(1, n_months + 1)

    base_level = 1000
    trend = 15 * t
    seasonal_pattern = {1: 0.72, 2: 0.75, 3: 0.85, 4: 0.95, 5: 1.10, 6: 1.30,
                         7: 1.40, 8: 1.32, 9: 1.05, 10: 0.92, 11: 0.85, 12: 0.90}
    seasonal = np.array([seasonal_pattern[m.month] for m in months])
    noise = RNG.normal(0, 25, n_months)

    demand = (base_level + trend) * seasonal + noise
    demand = np.round(demand).astype(int)

    # Synthetic market-pressure index (GSCPI-style), with a deliberate spike
    # in the final 4 months that coincides with demand running below the
    # seasonal norm -- an external signal a pure time-series model misses.
    pressure = 0.3 + 0.05 * RNG.normal(size=n_months).cumsum() * 0.1
    pressure[-4:] += np.linspace(0.3, 1.4, 4)  # spike in months 21-24
    pressure = np.round(pressure, 2)
    demand[-4:] = np.round(demand[-4:] * (1 - 0.06 * pressure[-4:])).astype(int)

    df = pd.DataFrame({"month": months.astype(str), "t": t, "demand": demand,
                        "pressure_index": pressure})
    return df


# ---------------------------------------------------------------------------
# 2. Method 1: Holt-Winters Triple Exponential Smoothing
# ---------------------------------------------------------------------------
def fit_holt_winters(df, train_months=32, forecast_horizon=4):
    train = df["demand"].iloc[:train_months]
    model = ExponentialSmoothing(train, trend="add", seasonal="mul",
                                  seasonal_periods=12, initialization_method="estimated")
    # Fixed, illustrative smoothing constants (rather than optimizer-selected)
    # so the worked-calculation walkthrough in the report uses clean numbers.
    fit = model.fit(smoothing_level=0.3, smoothing_trend=0.1, smoothing_seasonal=0.2,
                     optimized=False)
    forecast = fit.forecast(forecast_horizon)

    actual_test = df["demand"].iloc[train_months:train_months + forecast_horizon].values
    mape = mean_absolute_percentage_error(actual_test, forecast) * 100

    print("=== Holt-Winters Triple Exponential Smoothing ===")
    print(f"Fitted smoothing parameters: alpha={fit.params['smoothing_level']:.3f}, "
          f"beta={fit.params['smoothing_trend']:.3f}, gamma={fit.params['smoothing_seasonal']:.3f}")
    print(f"Forecast (months {train_months+1}-{train_months+forecast_horizon}): "
          f"{[round(v) for v in forecast.values]}")
    print(f"Actual held-out demand: {list(actual_test)}")
    print(f"MAPE on held-out months: {mape:.1f}%")

    return fit, forecast, mape


# ---------------------------------------------------------------------------
# 2b. Manual walkthrough: independent hand-computable Holt-Winters steps
#     (used verbatim in the report's "worked calculation" section)
# ---------------------------------------------------------------------------
def manual_holt_winters_walkthrough(df):
    y = df["demand"].values
    alpha, beta, gamma = 0.3, 0.1, 0.2
    m = 12

    # Initialization from the first two years (simple, textbook method)
    L12 = y[0:12].mean()
    T12 = (y[12:24].mean() - y[0:12].mean()) / 12
    S = {i + 1: y[i] / L12 for i in range(12)}  # crude initial seasonal ratios, month 1-12

    print("=== Manual Holt-Winters Walkthrough (alpha=0.3, beta=0.1, gamma=0.2) ===")
    print(f"Initial level L12 (avg of months 1-12) = {L12:.1f}")
    print(f"Initial trend T12 ((avg months 13-24 - avg months 1-12) / 12) = {T12:.2f}")
    print(f"Initial seasonal index for month 1 (Jan), S1 = y1 / L12 = {y[0]} / {L12:.1f} = {S[1]:.3f}")

    L, T = L12, T12
    results = []
    for t in range(13, 16):  # walk forward months 13, 14, 15
        yt = y[t - 1]
        s_month = ((t - 1) % 12) + 1
        S_prev = S[s_month]
        L_new = alpha * (yt / S_prev) + (1 - alpha) * (L + T)
        T_new = beta * (L_new - L) + (1 - beta) * T
        S_new = gamma * (yt / L_new) + (1 - gamma) * S_prev

        print(f"\n-- Month t={t} (actual y_t = {yt}) --")
        print(f"L_t = alpha*(y_t/S_prev) + (1-alpha)*(L_prev+T_prev)")
        print(f"    = 0.3*({yt}/{S_prev:.3f}) + 0.7*({L:.1f}+{T:.2f})")
        print(f"    = 0.3*{yt / S_prev:.1f} + 0.7*{L + T:.1f} = {L_new:.1f}")
        print(f"T_t = beta*(L_t - L_prev) + (1-beta)*T_prev")
        print(f"    = 0.1*({L_new:.1f}-{L:.1f}) + 0.9*{T:.2f} = {T_new:.2f}")
        print(f"S_t = gamma*(y_t/L_t) + (1-gamma)*S_prev")
        print(f"    = 0.2*({yt}/{L_new:.1f}) + 0.8*{S_prev:.3f} = {S_new:.3f}")
        forecast_next = (L_new + T_new) * S.get(s_month % 12 + 1, S_prev)
        print(f"One-step-ahead forecast for month t+1: (L_t+T_t) * S_(next month) "
              f"= ({L_new:.1f}+{T_new:.2f}) * {S.get(s_month % 12 + 1, S_prev):.3f} "
              f"= {forecast_next:.0f}")

        results.append((t, yt, L_new, T_new, S_new))
        S[s_month] = S_new
        L, T = L_new, T_new

    return results



def fit_regression(df):
    month_num = [int(m.split("-")[1]) for m in df["month"]]
    seasonal_dummies = pd.get_dummies(month_num, prefix="m", drop_first=True).astype(float)
    X_full = np.hstack([df[["t", "pressure_index"]].values, seasonal_dummies.values])
    y = df["demand"].values

    model = LinearRegression()
    model.fit(X_full, y)
    preds = model.predict(X_full)
    r2 = r2_score(y, preds)

    print("\n=== Regression with Market-Pressure Index ===")
    print(f"Coefficient on trend (t): {model.coef_[0]:.2f} units/month")
    print(f"Coefficient on pressure_index: {model.coef_[1]:.2f} units per index point")
    print(f"Intercept: {model.intercept_:.2f}")
    print(f"R-squared (in-sample fit): {r2:.3f}")

    return model, seasonal_dummies.columns.tolist(), preds, r2


# ---------------------------------------------------------------------------
# 4. Charts
# ---------------------------------------------------------------------------
def make_hw_chart(df, fit, forecast, train_months, path):
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(df["t"], df["demand"], "o-", color="#1f4e79", label="Actual demand", markersize=4)
    ax.plot(df["t"].iloc[:train_months], fit.fittedvalues, "--", color="#7fb069",
             label="Holt-Winters fitted (training)")
    forecast_t = df["t"].iloc[train_months:train_months + len(forecast)]
    ax.plot(forecast_t, forecast.values, "s--", color="#c0392b", label="Holt-Winters forecast")
    ax.axvline(train_months + 0.5, color="grey", linestyle=":", linewidth=1)
    ax.set_xlabel("Month index (t)")
    ax.set_ylabel("Units demanded")
    ax.set_title("Holt-Winters Triple Exponential Smoothing: Fit & Forecast")
    ax.legend(fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=200, facecolor="white")
    plt.close(fig)


def make_regression_chart(df, preds, path):
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(df["t"], df["demand"], "o-", color="#1f4e79", label="Actual demand", markersize=4)
    ax.plot(df["t"], preds, "--", color="#c0392b", label="Regression fitted values")
    ax.set_xlabel("Month index (t)")
    ax.set_ylabel("Units demanded")
    ax.set_title("Regression with Trend, Seasonality & Market-Pressure Index")
    ax.legend(fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=200, facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------------------
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = generate_pseudo_data()
    df.to_csv(os.path.join(OUTPUT_DIR, "demand_pseudo_data.csv"), index=False)
    print(df.to_string(index=False))

    hw_fit, hw_forecast, hw_mape = fit_holt_winters(df)
    make_hw_chart(df, hw_fit, hw_forecast, 32, os.path.join(OUTPUT_DIR, "holt_winters_forecast.png"))
    print()
    manual_holt_winters_walkthrough(df)

    reg_model, dummy_cols, reg_preds, r2 = fit_regression(df)
    make_regression_chart(df, reg_preds, os.path.join(OUTPUT_DIR, "regression_fit.png"))

    reg_mape = mean_absolute_percentage_error(
        df["demand"].iloc[32:36].values, reg_preds[32:36]) * 100

    print(f"\nRegression MAPE on the same held-out months: {reg_mape:.1f}%")
    print(f"\nSummary: Holt-Winters MAPE = {hw_mape:.1f}% | Regression MAPE = {reg_mape:.1f}%")
    print(f"\nAll outputs written to ./{OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
