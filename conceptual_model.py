"""
conceptual_model.py
====================

Week 4 Task: Predictive Analytics for Demand Forecasting
-------------------------------------------------------------
Draws the conceptual demand-forecasting model diagram used in the Week 4
report: three input categories feeding a two-method forecasting engine,
producing a blended forecast that drives three supply chain planning
functions, with a feedback loop back to historical data.

Usage
-----
    pip install -r requirements.txt
    python conceptual_model.py

Output: ./output/conceptual_model.png
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
ACCENT_BG = "#FBEAEA"
GREEN = "#3C7A4B"
GREEN_BG = "#E7F3EA"

fig, ax = plt.subplots(figsize=(12.5, 6.8))

def box(x, y, w, h, text, edge, face, fontsize=10, fontweight="bold", textcolor=None):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.08",
                        linewidth=1.6, edgecolor=edge, facecolor=face)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, fontweight=fontweight, color=textcolor or edge, linespacing=1.3)
    return (x + w / 2, y, x + w / 2, y + h)  # (cx, bottom, cx, top)

def arrow(p1, p2, color="#444444", style="-|>", lw=1.6):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=15, linewidth=lw, color=color)
    ax.add_patch(a)

# --- Inputs (left column, 3 stacked) ---
in_w, in_h = 2.6, 0.85
x_in = 0.3
cx1, _, _, top1 = box(x_in, 5.3, in_w, in_h, "Historical Demand\nData (internal)", NAVY, LIGHT_BLUE, 9.5)
cx2, _, _, top2 = box(x_in, 4.15, in_w, in_h, "Seasonal & Trend\nPatterns", NAVY, LIGHT_BLUE, 9.5)
cx3, _, _, top3 = box(x_in, 3.0, in_w, in_h, "Market Indicators\n(e.g., GSCPI, LPI)", NAVY, LIGHT_BLUE, 9.5)

# --- Forecasting engine (center) ---
eng_x, eng_w, eng_h = 4.0, 3.0, 2.9
eng_y = 3.15
box(eng_x, eng_y, eng_w, eng_h, "", NAVY, "white", 1)  # outer container border
ax.text(eng_x + eng_w / 2, eng_y + eng_h - 0.3, "Forecasting Engine", ha="center",
        fontsize=11.5, fontweight="bold", color=NAVY)
m1cx, m1b, _, m1t = box(eng_x + 0.25, eng_y + 1.55, eng_w - 0.5, 0.85,
                          "Method 1:\nHolt-Winters Smoothing", GREEN, GREEN_BG, 9)
m2cx, m2b, _, m2t = box(eng_x + 0.25, eng_y + 0.35, eng_w - 0.5, 0.85,
                          "Method 2:\nRegression + Market Index", ACCENT, ACCENT_BG, 9)

for cx, top in [(cx1, top1), (cx2, top2), (cx3, top3)]:
    arrow((x_in + in_w, (top + top - 0.85) / 2), (eng_x, eng_y + eng_h / 2), lw=1.3)

# --- Blended forecast output ---
out_x, out_w, out_h = 8.1, 2.1, 1.1
out_y = eng_y + eng_h / 2 - out_h / 2
ocx, ob, _, ot = box(out_x, out_y, out_w, out_h, "Blended Demand\nForecast", ACCENT, "white", 10)
arrow((eng_x + eng_w, eng_y + eng_h / 2), (out_x, out_y + out_h / 2), lw=1.8)

# --- Planning outputs (right column, 3 stacked) ---
pl_x, pl_w, pl_h = 10.7, 2.3, 0.85
p1cx, p1b, _, p1t = box(pl_x, 5.3, pl_w, pl_h, "Inventory &\nSafety Stock Plans", NAVY, LIGHT_BLUE, 9)
p2cx, p2b, _, p2t = box(pl_x, 4.15, pl_w, pl_h, "Procurement &\nSupplier Orders", NAVY, LIGHT_BLUE, 9)
p3cx, p3b, _, p3t = box(pl_x, 3.0, pl_w, pl_h, "Workforce &\nCapacity Planning", NAVY, LIGHT_BLUE, 9)

for cx, b, t in [(p1cx, p1b, p1t), (p2cx, p2b, p2t), (p3cx, p3b, p3t)]:
    arrow((out_x + out_w, out_y + out_h / 2), (pl_x, (b + t) / 2), lw=1.3)

# --- Feedback loop ---
ax.annotate("", xy=(x_in + in_w / 2, 5.3 + in_h), xytext=(pl_x + pl_w / 2, 5.3 + pl_h),
            arrowprops=dict(arrowstyle="-", color="#888888", lw=1.3,
                             connectionstyle="arc3,rad=0.18"))
ax.annotate("", xy=(x_in + in_w / 2 + 0.05, 5.3 + in_h + 0.02),
            xytext=(x_in + in_w / 2, 5.3 + in_h + 0.55),
            arrowprops=dict(arrowstyle="-|>", color="#888888", lw=1.3))
ax.plot([x_in + in_w / 2, x_in + in_w / 2], [5.3 + in_h, 5.3 + in_h + 0.55], color="#888888", lw=1.3)
ax.plot([pl_x + pl_w / 2, pl_x + pl_w / 2], [5.3 + pl_h, 5.3 + pl_h + 0.55], color="#888888", lw=1.3)
ax.plot([x_in + in_w / 2, pl_x + pl_w / 2], [5.3 + in_h + 0.55, 5.3 + pl_h + 0.55], color="#888888", lw=1.3)
ax.text((x_in + in_w / 2 + pl_x + pl_w / 2) / 2, 5.3 + in_h + 0.7,
        "Actual outcomes feed back into next cycle's historical data", ha="center",
        fontsize=8.3, color="#888888", style="italic")

ax.set_xlim(-0.3, 13.3)
ax.set_ylim(2.7, 6.9)
ax.axis("off")
ax.set_title("Conceptual Model: Predictive Demand Forecasting for Supply Chain Planning",
             fontsize=13.5, fontweight="bold", color=NAVY, pad=16)
fig.tight_layout()

os.makedirs(OUTPUT_DIR, exist_ok=True)
out_path = os.path.join(OUTPUT_DIR, "conceptual_model.png")
fig.savefig(out_path, dpi=220, facecolor="white")
print(f"Conceptual model diagram saved to {out_path}")
