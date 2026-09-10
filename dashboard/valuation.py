"""
valuation.py
------------
Core financial analysis and valuation functions for the NVIDIA equity research
project. Kept deliberately simple and readable: the notebook and the Streamlit
dashboard both import from here so the numbers can never drift apart.

All dollar figures are in $ millions unless a function says otherwise.
Data source: data/financial_data.csv (built from NVIDIA 10-K filings).
"""

import os
import pandas as pd

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_financials():
    """Load the 5-year historical financials as a DataFrame indexed by year."""
    path = os.path.join(DATA_DIR, "financial_data.csv")
    df = pd.read_csv(path)
    return df


def add_derived_metrics(df):
    """Add growth rates and margins that we didn't store raw in the CSV."""
    df = df.copy()
    df["revenue_growth_pct"] = df["revenue"].pct_change() * 100
    df["gross_margin_pct"] = df["gross_profit"] / df["revenue"] * 100
    df["operating_margin_pct"] = df["operating_income"] / df["revenue"] * 100
    df["net_margin_pct"] = df["net_income"] / df["revenue"] * 100
    df["fcf_margin_pct"] = df["free_cash_flow"] / df["revenue"] * 100
    df["current_ratio_proxy"] = None  # documented in report; not enough line items in CSV
    df["debt_to_equity"] = df["total_debt"] / df["total_equity"]
    return df


# ---------------------------------------------------------------------------
# DCF valuation
# ---------------------------------------------------------------------------

def run_dcf(
    base_revenue,              # last actual full-year revenue ($M), e.g. FY2026 = 215938
    revenue_growth,            # list of 5 annual growth rates, e.g. [0.45, 0.32, 0.24, 0.18, 0.12]
    operating_margin,          # steady-state operating margin used across forecast (e.g. 0.60)
    tax_rate,                  # effective tax rate (e.g. 0.15)
    da_pct_revenue,            # D&A as % of revenue (e.g. 0.02)
    capex_pct_revenue,         # capex as % of revenue (e.g. 0.03)
    nwc_pct_revenue,           # incremental net working capital as % of change in revenue (e.g. 0.03)
    wacc,                      # discount rate (e.g. 0.10)
    terminal_growth,           # perpetuity growth rate (e.g. 0.03)
    net_cash,                  # cash - debt ($M), added to EV to get equity value
    shares_outstanding,        # diluted shares (millions)
):
    """
    Simple 5-year unlevered free-cash-flow DCF.

    FCF (to firm) = EBIT*(1-tax) + D&A - Capex - change in NWC
    EV = sum(PV of FCF) + PV of terminal value
    Equity value = EV + net cash
    Implied price = equity value / shares

    Returns a dict with the yearly table, EV, equity value and implied price.
    """
    years = list(range(1, len(revenue_growth) + 1))
    rows = []
    prev_revenue = base_revenue

    for yr, g in zip(years, revenue_growth):
        revenue = prev_revenue * (1 + g)
        ebit = revenue * operating_margin
        nopat = ebit * (1 - tax_rate)
        da = revenue * da_pct_revenue
        capex = revenue * capex_pct_revenue
        delta_nwc = (revenue - prev_revenue) * nwc_pct_revenue
        fcf = nopat + da - capex - delta_nwc
        discount = (1 + wacc) ** yr
        pv_fcf = fcf / discount
        rows.append({
            "year": yr,
            "revenue": revenue,
            "growth": g,
            "ebit": ebit,
            "nopat": nopat,
            "da": da,
            "capex": capex,
            "delta_nwc": delta_nwc,
            "fcf": fcf,
            "pv_fcf": pv_fcf,
        })
        prev_revenue = revenue

    forecast = pd.DataFrame(rows)

    # Terminal value via Gordon growth, on the final-year FCF
    final_fcf = forecast.iloc[-1]["fcf"]
    terminal_value = final_fcf * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal_value / ((1 + wacc) ** len(years))

    pv_fcf_sum = forecast["pv_fcf"].sum()
    enterprise_value = pv_fcf_sum + pv_terminal
    equity_value = enterprise_value + net_cash
    implied_price = equity_value / shares_outstanding

    return {
        "forecast": forecast,
        "pv_fcf_sum": pv_fcf_sum,
        "terminal_value": terminal_value,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "implied_price": implied_price,
        "terminal_value_share_of_ev": pv_terminal / enterprise_value,
    }


def sensitivity_table(base_kwargs, wacc_range, tg_range):
    """
    Build a WACC x terminal-growth grid of implied share prices.
    base_kwargs is the dict of arguments to run_dcf (wacc/terminal_growth are overwritten).
    Returns a DataFrame indexed by WACC, columns = terminal growth.
    """
    grid = {}
    for tg in tg_range:
        col = []
        for w in wacc_range:
            kwargs = dict(base_kwargs)
            kwargs["wacc"] = w
            kwargs["terminal_growth"] = tg
            col.append(run_dcf(**kwargs)["implied_price"])
        grid[f"{tg:.1%}"] = col
    df = pd.DataFrame(grid, index=[f"{w:.1%}" for w in wacc_range])
    df.index.name = "WACC"
    return df


# ---------------------------------------------------------------------------
# Comparable companies
# ---------------------------------------------------------------------------

def load_peers():
    path = os.path.join(DATA_DIR, "peer_data.csv")
    return pd.read_csv(path)


def comps_valuation(nvda_fwd_eps, net_cash=None, shares_outstanding=None,
                    nvda_ebitda=None):
    """
    Comparable-company valuation for NVIDIA, using peer multiples.

    An important judgment call is baked in here, and it's worth understanding:

    NVIDIA's peers (AMD, Broadcom, Marvell) trade at very high *trailing*
    multiples (e.g. AMD ~121x trailing P/E) because their current earnings are
    small relative to the AI growth investors expect. NVIDIA, by contrast,
    already earns at enormous scale. Mechanically multiplying NVIDIA's large
    earnings by peers' inflated trailing multiples produces a nonsense number
    (>$600/share). So trailing multiples are shown for context but are NOT used
    to anchor value.

    Instead we lead with **forward P/E**, which is the least distorted multiple
    because it puts every company on next-year earnings. We report a range:
      - Low anchor  = cheapest peer forward P/E (Broadcom, ~23.6x)
      - Mid anchor  = peer median forward P/E
    applied to NVIDIA's forward EPS.

    Returns the peer forward-P/E stats and the implied price range.
    """
    peers = load_peers()
    others = peers[peers["ticker"] != "NVDA"]

    fwd_pe_low = others["forward_pe"].min()      # cheapest peer (AVGO ~23.6x)
    fwd_pe_median = others["forward_pe"].median()  # ~42.6x

    price_low = fwd_pe_low * nvda_fwd_eps
    price_median = fwd_pe_median * nvda_fwd_eps

    return {
        "nvda_fwd_eps": nvda_fwd_eps,
        "fwd_pe_low": fwd_pe_low,
        "fwd_pe_median": fwd_pe_median,
        "price_low": price_low,
        "price_median": price_median,
        # A single "headline" comps number: we anchor conservatively toward the
        # low end (cheapest peer) because NVIDIA's growth is already partly
        # realised, so it shouldn't command the full peer-median premium.
        "headline_price": price_low,
    }


if __name__ == "__main__":
    # Quick self-check when run directly
    df = add_derived_metrics(load_financials())
    print(df[["fiscal_year", "revenue", "revenue_growth_pct",
              "gross_margin_pct", "operating_margin_pct", "net_margin_pct",
              "fcf_margin_pct"]].to_string(index=False))

    base = dict(
        base_revenue=215938,
        revenue_growth=[0.45, 0.32, 0.24, 0.18, 0.12],
        operating_margin=0.60,
        tax_rate=0.15,
        da_pct_revenue=0.02,
        capex_pct_revenue=0.03,
        nwc_pct_revenue=0.03,
        wacc=0.10,
        terminal_growth=0.03,
        net_cash=51144,
        shares_outstanding=24500,
    )
    res = run_dcf(**base)
    print(f"\nBase-case implied price: ${res['implied_price']:.2f}")
    print(f"Terminal value = {res['terminal_value_share_of_ev']:.0%} of EV")
