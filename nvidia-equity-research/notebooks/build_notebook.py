import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

def md(t): cells.append(nbf.v4.new_markdown_cell(t))
def code(t): cells.append(nbf.v4.new_code_cell(t))

md("""# NVIDIA (NVDA) — Financial Analysis & Valuation

**Educational project — not investment advice.**

This notebook walks through the historical financial analysis and the DCF /
comparable-company valuation behind the equity research report. All data comes
from NVIDIA's 10-K filings (fiscal years ending late January). NVIDIA's FY2026
ended January 25, 2026.

Sections:
1. Load data
2. Income statement trends
3. Cash flow & FCF
4. Balance sheet strength
5. DCF valuation
6. Sensitivity analysis
7. Comparable companies
8. Valuation summary
""")

code("""import sys, os
sys.path.append(os.path.join('..', 'dashboard'))
import pandas as pd
from valuation import (load_financials, add_derived_metrics, run_dcf,
                       sensitivity_table, load_peers)

pd.set_option('display.float_format', lambda x: f'{x:,.1f}')
df = add_derived_metrics(load_financials())
df[['fiscal_year','revenue','net_income','free_cash_flow']]""")

md("""## 2. Income statement trends

Revenue, margins and EPS over five years. Note the FY2023 dip (a gaming/crypto
inventory correction) followed by the AI/data-center inflection from FY2024 on.""")

code("""df[['fiscal_year','revenue','revenue_growth_pct','gross_margin_pct',
    'operating_margin_pct','net_margin_pct','diluted_eps']]""")

md("""**Reading the trend.** Revenue was roughly flat in FY2023 (~$27B) then
grew +126% (FY2024), +114% (FY2025) and +65% (FY2026) to ~$216B, driven almost
entirely by the Data Center segment (Compute & Networking). Operating margin
expanded from ~21% in FY2023 to ~60% as high-margin data-center GPUs came to
dominate the mix. The small FY2026 gross-margin dip (75% -> 71%) reflects a
one-time $4.5B Q1 charge tied to U.S. export restrictions on H20 chips for
China; excluding that quarter, margins were still expanding.""")

md("## 3. Cash flow & free cash flow")

code("""cf = df[['fiscal_year','operating_cash_flow','capex','free_cash_flow',
         'fcf_margin_pct']].copy()
cf""")

md("""Free cash flow (operating cash flow minus capex) grew from ~$4B in FY2023
to ~$97B in FY2026, an FCF margin around 45%. Earnings are converting into cash
strongly — net income of $120B vs. FCF of $97B in FY2026. Capex stays modest
(~3% of revenue) because NVIDIA is fabless: it designs chips and outsources
manufacturing to TSMC, so it doesn't carry heavy factory spending.""")

md("## 4. Balance sheet strength")

code("""bs = df[['fiscal_year','cash_and_investments','total_debt',
         'total_assets','total_liabilities','total_equity','debt_to_equity']].copy()
bs['net_cash'] = bs['cash_and_investments'] - bs['total_debt']
bs""")

md("""NVIDIA holds far more cash and investments (~$63B) than debt (~$11B), so
it has a large net-cash position (~$51B) and a low debt-to-equity ratio (~0.09).
This is a financially strong, low-leverage balance sheet — the company could
fund growth or weather a downturn without stress.""")

md("""## 5. DCF valuation

A simple 5-year unlevered free-cash-flow DCF. We forecast revenue with a
declining growth path, apply a ~60% operating margin, tax it, add back D&A,
subtract capex and incremental working capital to get free cash flow to the
firm, discount at the WACC, and add a Gordon-growth terminal value.

**Base-case assumptions** (each explained in the report):
- Revenue growth: 45% -> 32% -> 24% -> 18% -> 12%
- Operating margin: 60%
- Tax rate: 15%   |   D&A: 2% of revenue   |   Capex: 3% of revenue
- WACC: 10%   |   Terminal growth: 3%""")

code("""base = dict(
    base_revenue=215938,
    revenue_growth=[0.45, 0.32, 0.24, 0.18, 0.12],
    operating_margin=0.60, tax_rate=0.15,
    da_pct_revenue=0.02, capex_pct_revenue=0.03, nwc_pct_revenue=0.03,
    wacc=0.10, terminal_growth=0.03,
    net_cash=51144, shares_outstanding=24500,
)
res = run_dcf(**base)
res['forecast'][['year','revenue','growth','ebit','fcf','pv_fcf']].round(0)""")

code("""print(f"Sum of PV of FCF:        ${res['pv_fcf_sum']:,.0f}M")
print(f"PV of terminal value:    ${res['pv_terminal']:,.0f}M")
print(f"Enterprise value:        ${res['enterprise_value']:,.0f}M")
print(f"+ Net cash:              ${51144:,.0f}M")
print(f"Equity value:            ${res['equity_value']:,.0f}M")
print(f"/ Shares (M):             {24500:,.0f}")
print(f"= Implied price:         ${res['implied_price']:,.2f}")
print(f"\\nCurrent price (Sep 9 2026): $224.15")
print(f"Terminal value = {res['terminal_value_share_of_ev']:.0%} of EV")""")

md("""The base case implies roughly **$165**, about 26% below the ~$224 market
price. But notice the terminal value is ~77% of enterprise value: the answer is
dominated by long-run assumptions, so the base case alone shouldn't drive the
call. That's what the sensitivity analysis is for.""")

md("## 6. Sensitivity analysis")

code("""grid = sensitivity_table(base,
        wacc_range=[0.08,0.09,0.10,0.11],
        tg_range=[0.02,0.025,0.03,0.035])
grid.round(0)""")

md("""The implied price ranges from about **$131 to $257** across reasonable
WACC and terminal-growth combinations — straddling the current price. At an 8%
WACC the stock looks roughly fair to cheap; at 10–11% it looks expensive. The
valuation is genuinely assumption-dependent.""")

md("""## 7. Comparable companies

Three AI-chip peers, compared on the multiples investors actually use. Data:
stockanalysis.com / S&P Global, snapshot as of early September 2026.""")

code("""peers = load_peers()
peers[['company','ticker','ttm_pe','forward_pe','ev_ebitda',
       'revenue_growth_pct','operating_margin_pct']]""")

md("""**The key finding:** NVIDIA has the highest growth and margins of the group,
yet trades at the *lowest* multiple on every measure — forward P/E ~19x versus a
peer median of ~43x. So on a relative basis NVIDIA looks cheap, not expensive.

A caution on trailing P/E: peers like AMD (121x) and Marvell (79x) trade at huge
trailing multiples because their current earnings are small relative to expected
AI growth. NVIDIA already earns at scale, so applying peers' trailing multiples to
its large earnings would give a nonsense number. Forward P/E is the fair
comparison.""")

code("""from valuation import comps_valuation
nvda_fwd_eps = 224.15 / 19.1   # NVDA forward EPS implied by its own forward P/E
comps = comps_valuation(nvda_fwd_eps=nvda_fwd_eps)
print(f"NVIDIA forward EPS:        ${nvda_fwd_eps:.2f}")
print(f"Cheapest peer fwd P/E:      {comps['fwd_pe_low']:.1f}x  -> ${comps['price_low']:,.0f}")
print(f"Peer median fwd P/E:        {comps['fwd_pe_median']:.1f}x  -> ${comps['price_median']:,.0f}")
print(f"\\nConservative comps anchor: ~${comps['headline_price']:,.0f} (cheapest peer)")
print("Current price:             $224.15")""")

md("""I anchor toward the conservative low end (~$277, the cheapest peer's
multiple) because NVIDIA has already realised much of the growth its peers are
still only promising. Even that conservative figure is above the current price and
well above the DCF.""")

md("## 8. Valuation summary")

code("""summary = pd.DataFrame({
    'Method': ['DCF (base case)', 'DCF range (sensitivity)',
               'Comps (conservative, cheapest peer)',
               'Comps (peer median)', 'Current market price'],
    'Implied share price': ['~$165', '~$131 – $257', '~$277', '~$500', '$224'],
})
summary""")

md("""**Takeaway.** NVIDIA is an exceptional business — enormous growth, ~60%
operating margins, ~45% FCF margins, a net-cash balance sheet. The two valuation
methods disagree, and that's the real signal: the DCF base case (~$165) says
modestly expensive, while comps (~$277+) say NVIDIA is actually cheap relative to
its AI-chip peers. The DCF is assumption-heavy (77% terminal value) and the comps
depend on peers priced for years of future growth, so neither is decisive. The
honest conclusion is **Hold / Neutral**: a great company at a full-but-defensible
price, with limited margin of safety for a new buyer and an outcome that hinges on
assumptions (AI demand durability, competition, export policy) that could break
either way.

*This is an educational project and not professional investment advice.*""")

nb['cells'] = cells
with open('financial_analysis.ipynb', 'w') as f:
    nbf.write(nb, f)
print("notebook written")
