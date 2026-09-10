"""
make_charts.py
--------------
Generates the five core charts for the report and README, saved to charts/.
Run from the repo root:  python notebooks/make_charts.py
"""

import os
import sys
import matplotlib.pyplot as plt

# allow importing the shared valuation module
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "dashboard"))
from valuation import load_financials, add_derived_metrics  # noqa: E402

CHART_DIR = os.path.join(os.path.dirname(__file__), "..", "charts")
os.makedirs(CHART_DIR, exist_ok=True)

# NVIDIA-ish green, kept simple
GREEN = "#76b900"
GREY = "#4d4d4d"

df = add_derived_metrics(load_financials())
years = df["fiscal_year"]


def save(fig, name):
    path = os.path.join(CHART_DIR, name)
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("saved", path)


# 1. Revenue over time ($B)
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(years, df["revenue"] / 1000, color=GREEN)
ax.set_title("NVIDIA Revenue by Fiscal Year")
ax.set_ylabel("Revenue ($ billions)")
for x, v in zip(years, df["revenue"] / 1000):
    ax.text(x, v + 3, f"${v:.0f}B", ha="center", fontsize=9)
ax.margins(y=0.15)
save(fig, "01_revenue.png")

# 2. Net income over time ($B)
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(years, df["net_income"] / 1000, color=GREY)
ax.set_title("NVIDIA Net Income by Fiscal Year")
ax.set_ylabel("Net income ($ billions)")
for x, v in zip(years, df["net_income"] / 1000):
    ax.text(x, v + 2, f"${v:.0f}B", ha="center", fontsize=9)
ax.margins(y=0.15)
save(fig, "02_net_income.png")

# 3. Margins over time (%)
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(years, df["gross_margin_pct"], marker="o", label="Gross margin", color=GREEN)
ax.plot(years, df["operating_margin_pct"], marker="s", label="Operating margin", color=GREY)
ax.plot(years, df["net_margin_pct"], marker="^", label="Net margin", color="#b0b0b0")
ax.set_title("NVIDIA Margins by Fiscal Year")
ax.set_ylabel("Margin (%)")
ax.set_ylim(0, 100)
ax.legend()
save(fig, "03_margins.png")

# 4. Free cash flow over time ($B)
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(years, df["free_cash_flow"] / 1000, color=GREEN)
ax.set_title("NVIDIA Free Cash Flow by Fiscal Year")
ax.set_ylabel("Free cash flow ($ billions)")
for x, v in zip(years, df["free_cash_flow"] / 1000):
    ax.text(x, v + 2, f"${v:.0f}B", ha="center", fontsize=9)
ax.margins(y=0.15)
save(fig, "04_fcf.png")

# 5. Revenue growth %
fig, ax = plt.subplots(figsize=(7, 4))
growth = df["revenue_growth_pct"].fillna(0)
ax.bar(years, growth, color=GREY)
ax.set_title("NVIDIA Revenue Growth (% YoY)")
ax.set_ylabel("Growth (%)")
for x, v in zip(years, growth):
    if v > 0:
        ax.text(x, v + 3, f"{v:.0f}%", ha="center", fontsize=9)
ax.margins(y=0.15)
save(fig, "05_revenue_growth.png")

print("All charts generated.")
