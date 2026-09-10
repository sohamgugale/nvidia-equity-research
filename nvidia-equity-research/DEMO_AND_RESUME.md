# Recruiter demo & resume materials

Keep this file out of the recruiter's view — it's your prep sheet. (It's fine to
leave it in the repo; recruiters won't dig for it, and if they do, a candidate
who prepared a demo script reads as organized, not unprepared.)

---

## 2–3 minute live demo script

### Short version — the paragraph to memorize

If you only memorize one thing, memorize this. It's a natural spoken walk-through
you can deliver while clicking through the dashboard:

> "I built this project to evaluate whether NVIDIA's current valuation is supported
> by its financial performance and growth outlook. I started by analyzing five years
> of NVIDIA's financial statements — revenue, profitability, free cash flow, and
> balance-sheet strength. The big story is the growth after the AI boom: revenue
> went from about $27 billion to more than $215 billion, with operating margins
> expanding sharply. I then built two valuation approaches — a five-year DCF and a
> comparable-company analysis using NVIDIA, AMD, Broadcom, and Marvell. The DCF gives
> a more conservative valuation, while the comps give a higher one because NVIDIA
> trades at a lower forward P/E than several peers. I also built a sensitivity
> analysis so I can change assumptions like WACC and terminal growth and see how the
> implied price moves. Based on the strong fundamentals, the gap between the two
> valuation methods, and how sensitive the DCF is to assumptions, my conclusion is
> Hold. The main takeaway for me was that valuation isn't just about whether a
> company is performing well — it's about whether the price already reflects that
> performance."

### Detailed version — beat by beat

The single most important rule: **don't explain the code.** Show the story. The
whole point is that you can form and defend an investment view.

### 0:00–0:20 — Open GitHub, set up the question
> "I built an equity research and valuation project on NVIDIA to answer one
> question: is it fairly valued given its financials and growth? I valued it two
> ways — a DCF and a comparable-company analysis — and the interesting part is
> that the two methods disagree."

### 0:20–0:50 — Overview tab
Point to Revenue → Net income → Free cash flow → Margins.
> "I started with five years of financials from the 10-Ks. Revenue went from about
> $27B to $216B in three years, operating margins are around 60%, and free cash
> flow is roughly $97B. So the business quality isn't in question — it's
> exceptional."

### 0:50–1:25 — Valuation tab
Read the green summary box, then the two numbers.
> "My DCF base case comes out around $165 — that's about 26% *below* the current
> price, so on its own cash flows the stock looks slightly expensive. But look at
> the comps: NVIDIA actually trades at the *lowest* multiple of any AI-chip peer —
> a forward P/E around 19x versus 24 to 50x for AMD, Broadcom and Marvell — even
> though it has the best growth and margins. On a relative basis it looks cheap.
> So one method says expensive, the other says cheap."

*(This contrast is your best moment. Let it land.)*

### 1:25–1:55 — Sensitivity tab
Move WACC from 10% → 11%, then nudge terminal growth.
> "This is the part I think matters most. The terminal value is about 77% of the
> DCF, so the answer is really sensitive to two assumptions. Watch — moving the
> discount rate one point swings the fair value by tens of dollars. That's exactly
> why I don't treat the DCF as a precise price target. The honest read is a range,
> not a number."

### 1:55–2:15 — Land the conclusion
> "So my call is Hold. It's a great business, the relative valuation is actually
> reasonable, but the DCF says there's limited margin of safety and the whole thing
> hinges on AI demand staying strong. I wouldn't force a Buy or a Sell when the two
> methods genuinely point in different directions — I'd rather be honest about the
> uncertainty."

### If they push back (good — engage)
- **"Why is your DCF below the market?"** → "Mostly the discount rate and the
  declining growth path. At an 8% WACC instead of 10% it's roughly fair. The model
  is assumption-driven, which is the point of the sensitivity table."
- **"Why not just use the peer median for comps?"** → "The peer median forward P/E
  would imply about $500, but that's misleading — peers trade at high multiples
  because their current earnings are small relative to expected growth. NVIDIA
  already earns at scale, so I anchored at the cheapest peer's multiple, around
  $277, which is more conservative."
- **"Is this your own opinion or the model's?"** → "The model gives me the range;
  the Hold is my judgment call weighing the business quality, the relative
  valuation, and the risks together."

---

## Resume bullets (use these two)

Deliberately plain — no buzzwords, true to the repo, and not claiming professional
experience. The first is the finance/investment-analysis side; the second is the
technical/data side. Together they say: financial statements + valuation +
investment thinking + Python + dashboard.

> Analyzed NVIDIA's five-year financial performance — revenue growth, margins, free
> cash flow and balance-sheet strength — and built a DCF and peer-based valuation to
> assess its investment outlook.

> Built an interactive Python/Streamlit valuation dashboard with DCF assumptions,
> comparable-company multiples and sensitivity analysis to evaluate how changes in
> key assumptions affect implied share price.

Put this project relatively high on the resume (not buried under a generic
"Projects" heading) for Investment Analyst / Financial Analyst / Equity Research /
Corporate Finance applications.

**Alternate bullets** (if you want to swap emphasis):

> Reached a Hold recommendation by reconciling a DCF (~$165) against peer multiples
> implying ~$277–$500, concluding the stock was fairly valued despite a ~26%
> DCF-to-market gap.

> Wrote a 7-page equity research report on NVIDIA, flagging that ~77% of the DCF
> value sat in the terminal value — i.e. the valuation rests heavily on long-run
> assumptions.
