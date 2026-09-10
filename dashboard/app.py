"""
NVIDIA Equity Research — interactive dashboard
Run with:  streamlit run dashboard/app.py

Three tabs: Overview (financial performance), Valuation (DCF + comps),
and Sensitivity (interactive WACC / terminal-growth / growth sliders).

Note: this is a snapshot analysis. The share price and multiples are entered as
of the PRICE_DATE below (they are not pulled live from a market data feed), so
the valuation reflects that date. This is an educational project, not investment
advice.
"""

import streamlit as st
import pandas as pd

from valuation import (
    load_financials, add_derived_metrics, run_dcf,
    sensitivity_table, load_peers, comps_valuation,
)

st.set_page_config(page_title="NVIDIA Equity Research", layout="wide")

# --- constants (documented in the report; snapshot, not live) ------------
PRICE_DATE = "September 9, 2026"
CURRENT_PRICE = 224.15          # NVDA close, PRICE_DATE (stockanalysis.com)
NVDA_FWD_PE = 19.1              # NVDA forward P/E on PRICE_DATE (stockanalysis.com)
NET_CASH = 51144                # FY2026 cash & investments - total debt ($M)
SHARES = 24500                  # diluted shares (millions), FY2026
BASE_REVENUE = 215938           # FY2026 revenue ($M)

df = add_derived_metrics(load_financials())

st.title("NVIDIA (NVDA) — Equity Research & Valuation")
st.caption(f"Educational project — not investment advice. Financial data from "
           f"NVIDIA 10-K filings. Share price and peer multiples are a snapshot "
           f"as of {PRICE_DATE} (entered manually, not a live feed).")

tab1, tab2, tab3 = st.tabs(["Overview", "Valuation", "Sensitivity"])

# =========================================================================
# TAB 1 — OVERVIEW
# =========================================================================
with tab1:
    st.subheader("Financial performance (FY2022–FY2026)")

    latest = df.iloc[-1]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("FY2026 Revenue", f"${latest['revenue']/1000:.1f}B",
              f"{latest['revenue_growth_pct']:.0f}% YoY")
    c2.metric("FY2026 Net income", f"${latest['net_income']/1000:.1f}B")
    c3.metric("FY2026 Free cash flow", f"${latest['free_cash_flow']/1000:.1f}B")
    c4.metric("FY2026 Operating margin", f"{latest['operating_margin_pct']:.0f}%")

    st.markdown("**Revenue ($B)**")
    st.bar_chart(df.set_index("fiscal_year")["revenue"] / 1000)

    colA, colB = st.columns(2)
    with colA:
        st.markdown("**Net income ($B)**")
        st.bar_chart(df.set_index("fiscal_year")["net_income"] / 1000)
    with colB:
        st.markdown("**Free cash flow ($B)**")
        st.bar_chart(df.set_index("fiscal_year")["free_cash_flow"] / 1000)

    st.markdown("**Margins (%)**")
    st.line_chart(df.set_index("fiscal_year")[
        ["gross_margin_pct", "operating_margin_pct", "net_margin_pct"]])

    st.markdown("**Underlying data ($M)**")
    show = df[["fiscal_year", "revenue", "gross_profit", "operating_income",
               "net_income", "free_cash_flow", "revenue_growth_pct",
               "operating_margin_pct", "net_margin_pct"]].copy()
    st.dataframe(show.round(1), use_container_width=True, hide_index=True)

# =========================================================================
# TAB 2 — VALUATION
# =========================================================================
with tab2:
    # ---- Investment summary box (recruiter sees the answer immediately) ----
    st.markdown(
        f"""
        <div style="background:#f4f8ee;border-left:6px solid #76b900;
        padding:14px 18px;border-radius:6px;margin-bottom:8px;">
        <span style="font-size:20px;font-weight:700;">Investment View: HOLD / Neutral</span><br>
        <span style="color:#333;">
        <b>Current price ${CURRENT_PRICE:,.0f}</b> &nbsp;·&nbsp;
        DCF base case ~$165 &nbsp;·&nbsp;
        Comps ~$277–$500 &nbsp;·&nbsp;
        Valuation range ~$131–$257 (DCF)
        </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Why Hold? (the one-paragraph thesis)", expanded=True):
        st.markdown(
            "- **Exceptional business**: ~65% revenue growth, ~60% operating "
            "margin, ~45% FCF margin, net-cash balance sheet.\n"
            "- **DCF says modestly expensive**: base case ~$165, about 26% below "
            "the market price on my cash-flow assumptions.\n"
            "- **Comps say the opposite**: NVIDIA trades *below* every AI-chip "
            "peer on P/E and EV/EBITDA despite better growth and margins — likely "
            "the market pricing in some normalization of its growth, but still "
            "reasonably valued on a relative basis.\n"
            "- **The catch**: the DCF is assumption-heavy (terminal value ~77% of "
            "value) and the comps rely on peers with sky-high growth expectations. "
            "Neither method is decisive.\n"
            "- **Conclusion**: a great company at a full-but-not-crazy price — "
            "**Hold**, with limited margin of safety for a new buyer."
        )

    st.divider()
    st.subheader("DCF valuation (base case)")

    base_kwargs = dict(
        base_revenue=BASE_REVENUE,
        revenue_growth=[0.45, 0.32, 0.24, 0.18, 0.12],
        operating_margin=0.60,
        tax_rate=0.15,
        da_pct_revenue=0.02,
        capex_pct_revenue=0.03,
        nwc_pct_revenue=0.03,
        wacc=0.10,
        terminal_growth=0.03,
        net_cash=NET_CASH,
        shares_outstanding=SHARES,
    )
    res = run_dcf(**base_kwargs)
    dcf_price = res["implied_price"]

    # Real comps: peer-median forward P/E applied to NVIDIA forward EPS.
    nvda_fwd_eps = CURRENT_PRICE / NVDA_FWD_PE
    comps = comps_valuation(nvda_fwd_eps=nvda_fwd_eps)
    comps_price = comps["headline_price"]

    c1, c2, c3 = st.columns(3)
    c1.metric("DCF implied price", f"${dcf_price:,.0f}")
    c2.metric("Comps implied price", f"${comps_price:,.0f}",
              help="NVIDIA forward EPS x cheapest peer forward P/E (~23.6x). "
                   "Peer median would imply ~$500 but is inflated by peers' "
                   "high growth expectations, so we anchor conservatively.")
    c3.metric("Current market price", f"${CURRENT_PRICE:,.0f}")

    upside_dcf = (dcf_price / CURRENT_PRICE - 1) * 100
    st.markdown(
        f"Base-case DCF implies **{upside_dcf:+.0f}%** vs. the current price. "
        f"The terminal value is **{res['terminal_value_share_of_ev']:.0%}** of "
        f"enterprise value — a reminder that most of the value sits in "
        f"long-run assumptions."
    )

    st.markdown("**5-year forecast ($M)**")
    f = res["forecast"].copy()
    f["growth"] = (f["growth"] * 100).round(0)
    st.dataframe(
        f[["year", "revenue", "growth", "ebit", "fcf", "pv_fcf"]]
        .round(0).rename(columns={"growth": "growth_%"}),
        use_container_width=True, hide_index=True,
    )

    # ---- Real comparable-company table -------------------------------------
    st.markdown("**Comparable companies — valuation multiples**")
    peers = load_peers()
    st.dataframe(
        peers[["company", "ticker", "ttm_pe", "forward_pe", "ev_ebitda",
               "revenue_growth_pct", "operating_margin_pct"]]
        .rename(columns={
            "ttm_pe": "Trailing P/E", "forward_pe": "Forward P/E",
            "ev_ebitda": "EV/EBITDA", "revenue_growth_pct": "Rev growth %",
            "operating_margin_pct": "Op margin %"}),
        use_container_width=True, hide_index=True,
    )
    st.caption(
        f"Source: stockanalysis.com / S&P Global, snapshot as of {PRICE_DATE}. "
        f"NVIDIA has the **highest growth and margins yet the lowest multiples** "
        f"of the group. Peer median forward P/E ≈ {comps['fwd_pe_median']:.0f}x; "
        f"cheapest peer ≈ {comps['fwd_pe_low']:.0f}x. Applied to NVIDIA's forward "
        f"EPS (~${nvda_fwd_eps:.2f}), comps imply roughly "
        f"${comps['price_low']:,.0f}–${comps['price_median']:,.0f}. "
        f"We anchor near the low end because NVIDIA has already realised much of "
        f"the growth its peers are still only promising."
    )

# =========================================================================
# TAB 3 — SENSITIVITY
# =========================================================================
with tab3:
    st.subheader("How much do the assumptions matter?")

    col1, col2 = st.columns(2)
    with col1:
        wacc = st.slider("WACC (discount rate)", 8.0, 12.0, 10.0, 0.5) / 100
        tg = st.slider("Terminal growth rate", 1.5, 4.0, 3.0, 0.5) / 100
    with col2:
        yr1_growth = st.slider("Year-1 revenue growth", 20, 60, 45, 5) / 100
        op_margin = st.slider("Operating margin", 50, 65, 60, 1) / 100

    # taper the chosen year-1 growth down over 5 years
    growth_path = [yr1_growth,
                   yr1_growth * 0.72,
                   yr1_growth * 0.53,
                   yr1_growth * 0.40,
                   yr1_growth * 0.27]

    user_kwargs = dict(
        base_revenue=BASE_REVENUE,
        revenue_growth=growth_path,
        operating_margin=op_margin,
        tax_rate=0.15,
        da_pct_revenue=0.02,
        capex_pct_revenue=0.03,
        nwc_pct_revenue=0.03,
        wacc=wacc,
        terminal_growth=tg,
        net_cash=NET_CASH,
        shares_outstanding=SHARES,
    )
    user_result = run_dcf(**user_kwargs)
    user_price = user_result["implied_price"]
    upside = (user_price / CURRENT_PRICE - 1) * 100

    c1, c2 = st.columns(2)
    c1.metric("Implied price (your assumptions)", f"${user_price:,.0f}")
    c2.metric("Upside / downside vs. market", f"{upside:+.0f}%")

    st.markdown("**Sensitivity grid — implied price by WACC × terminal growth**")
    st.caption("(Uses your growth and margin sliders; base case WACC/TG grid below.)")
    grid = sensitivity_table(
        user_kwargs,
        wacc_range=[0.08, 0.09, 0.10, 0.11],
        tg_range=[0.02, 0.025, 0.03, 0.035],
    )
    # highlight cells above/below current price
    def color(v):
        return "background-color: #d6f5d6" if v >= CURRENT_PRICE else "background-color: #f9d6d6"
    st.dataframe(grid.round(0).style.map(color), use_container_width=True)
    st.caption("Green = implied price above current market price (undervalued); "
               "red = below (overvalued). Small assumption changes flip the call — "
               "which is the honest takeaway for a stock like NVIDIA.")
