# NVIDIA (NVDA) — Equity Research & Valuation

A beginner-to-intermediate equity research project analyzing NVIDIA's financial
performance and estimating its fair value using a DCF model and comparable-company
analysis. Built as a personal project to practice financial statement analysis,
valuation, and investment reasoning.

**Question this project answers:**
> Is NVIDIA fairly valued based on its financial performance, growth outlook, and
> valuation compared with similar companies?

> ⚠️ **This is an educational project and not professional investment advice.**

## Key Takeaways

- Revenue grew from about **$27B (FY2022) to $216B (FY2026)**, driven almost
  entirely by the Data Center / AI segment.
- FY2026 operating margin was approximately **60%**; free cash flow was about **$97B**.
- The DCF base case (~**$165**) sits **below** the current share price (~**$224**),
  implying the market already prices in years of continued strong execution.
- Relative valuation suggests NVIDIA is **more reasonably valued than its AI-chip
  peers** — it trades at a lower forward P/E despite higher growth and margins.
- The resulting investment view is **Hold** — strong fundamentals offset by
  meaningful valuation uncertainty.

---

## Project overview

The project pulls five years of NVIDIA financials (FY2022–FY2026) from the
company's 10-K filings, analyzes the trends, and then values the company two ways:

- A **5-year discounted cash flow (DCF)** model
- A **comparable-company** analysis against AMD, Broadcom and Marvell, comparing
  trailing P/E, forward P/E and EV/EBITDA and applying peer multiples to NVIDIA

It includes a short written report, an Excel model with live formulas, a Jupyter
notebook, and an interactive Streamlit dashboard.

> Note: this is a **snapshot** analysis. The share price ($224.15) and peer
> multiples are entered as of September 9, 2026 — they are not pulled from a live
> market-data feed, so the valuation reflects that date.

## Analysis included

- Income statement analysis (revenue, margins, EPS, growth)
- Cash flow analysis (operating cash flow, capex, free cash flow)
- Balance sheet analysis (cash, debt, net cash, leverage)
- DCF valuation with clearly stated assumptions
- Sensitivity analysis (WACC × terminal growth)
- Comparable-company context
- Investment thesis (bull case, bear case, catalysts, risks)
- Final Buy / Hold / Sell view

## Tools used

- **Python** — pandas, matplotlib, numpy
- **Streamlit** — interactive dashboard
- **Excel** (openpyxl) — DCF model with live formulas
- **Jupyter** — analysis notebook
- Financial modeling (DCF, comparable companies, sensitivity)

## Key findings

- NVIDIA's revenue grew from ~$27B (FY2023) to ~$216B (FY2026), driven almost
  entirely by the Data Center segment and the AI compute buildout.
- Profitability is exceptional: ~60% operating margin and ~45% free-cash-flow
  margin in FY2026, with net income of ~$120B.
- The balance sheet is strong — roughly $63B cash & investments vs. ~$11B debt
  (net cash ~$51B), so leverage is very low.
- The base-case DCF implies roughly **$165/share**, about 26% below the ~$224
  market price (as of Sep 9, 2026) — but the terminal value is ~77% of enterprise
  value, so the answer is very assumption-sensitive.
- Across reasonable WACC/terminal-growth combinations the implied price ranges
  from about **$131 to $257**, straddling the market price.
- On comparable multiples, NVIDIA trades at the **lowest multiple in the AI-chip
  peer group** — a forward P/E of ~19x versus 24–50x for AMD, Broadcom and Marvell —
  despite having the highest growth and margins. Applying peer forward multiples
  implies a range of roughly **$277 (cheapest peer) to $500 (peer median)**, *above*
  both the market price and the DCF. The low multiple likely reflects the market
  pricing in some normalization of NVIDIA's growth.
- The DCF and comps **disagree** (DCF says modestly expensive, comps say reasonably
  valued vs. peers), which is the real analytical takeaway: the valuation is
  genuinely uncertain and assumption-dependent.
- **Overall view: Hold / Neutral** — an excellent business at a full-but-defensible
  price, with limited margin of safety for a new buyer.

## Repository structure

```
nvidia-equity-research/
├── README.md
├── requirements.txt
├── report/
│   └── NVIDIA_Equity_Research_Report.pdf   # the written report
├── model/
│   ├── NVIDIA_Valuation_Model.xlsx         # DCF with live formulas
│   └── build_model.py                      # script that builds the xlsx
├── data/
│   ├── financial_data.csv                  # 5-year financials (from 10-Ks)
│   └── peer_data.csv                       # peer context data
├── dashboard/
│   ├── app.py                              # Streamlit dashboard
│   └── valuation.py                        # shared DCF / comps / ratio functions
├── notebooks/
│   ├── financial_analysis.ipynb            # analysis walkthrough
│   ├── build_notebook.py                   # script that builds the notebook
│   └── make_charts.py                      # generates the charts
└── charts/
    └── *.png                               # revenue, net income, margins, FCF, growth
```

## How to run

```bash
# 1. clone and enter the repo
git clone https://github.com/<your-username>/nvidia-equity-research.git
cd nvidia-equity-research

# 2. install dependencies
pip install -r requirements.txt

# 3. (optional) regenerate the charts
python notebooks/make_charts.py

# 4. run the interactive dashboard
streamlit run dashboard/app.py
```

The dashboard opens in your browser with three tabs: **Overview** (financial
performance), **Valuation** (DCF + comps), and **Sensitivity** (move the WACC,
terminal-growth, revenue-growth and margin sliders and watch the implied price
change).

## Data sources

- NVIDIA Form 10-K filings, FY2022–FY2026 (SEC EDGAR)
- NVIDIA quarterly earnings press releases / CFO commentary (investor.nvidia.com)
- StockAnalysis.com (aggregated 10-K figures, current share price)
- Peer figures from AMD, Broadcom and Marvell public filings/earnings

All financial figures trace back to company filings. The current share price
($224.15) is as of September 9, 2026.

## Disclaimer

This project was created for educational and portfolio purposes to demonstrate
financial analysis and valuation skills. It is **not** investment advice, not a
recommendation to buy or sell any security, and should not be relied on for any
investment decision. Valuation assumptions are my own and are inherently
uncertain.
