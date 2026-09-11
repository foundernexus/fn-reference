---
title: Magic number & CAC payback calculator
description: Run the Scale-style SaaS magic number and a gross-margin CAC payback side by side. Cited bands from Scale, ChartMogul, and Bessemer. Labeled hypothetical. Not advice.
slug: magic-number-cac-payback-calculator
section: tools
cluster: finance
layout: calculator
calculator_js: magic-number-cac-payback-calculator.js
target_query: saas magic number cac payback calculator
date: 2026-09-11
close: Magic number and CAC payback are board-visible GTM calls. If you want founders who just defended those numbers in a raise or a board pack to pressure-test your S&M plan, that conversation happens at FounderNexus.
disclaimer: not-legal-tax
draft: false
related:
- library/finance/burn-multiple-vs-rule-of-40
- tools/runway-calculator
---

Enter prior and current quarter recurring revenue plus prior-quarter sales and marketing spend for the magic number. Enter CAC, monthly ARPA, and gross margin for payback months. You get both reads on one page so the board sees efficiency and cash recovery together. Not legal, tax, or investment advice.

:::takeaways
- Classic magic number = ((current-quarter recurring revenue − prior-quarter recurring revenue) × 4) ÷ prior-quarter sales & marketing spend. Scale Venture Partners popularized it; their Scale Studio long-term median is 0.7.
- ChartMogul’s cheat sheet read: above ~0.75 is commonly treated as efficient enough to invest more in GTM; below ~0.5 suggests pulling back. Scale’s 0.7 median is a different publisher’s baseline. Show them separately.
- CAC payback (months) = CAC ÷ (ARPA × gross margin %). ChartMogul: recover CAC through gross margin, not raw MRR.
- Bessemer (Scaling to $100 Million): target payback under 12 months SMB, under 18 mid-market, under 24 enterprise. Their portfolio average in the $1–10M ARR band was about 15 months.
- Use prior-quarter S&M in the magic number denominator. Same-quarter spend flatters a ramp and punishes a pipeline quarter.
:::

## What each metric answers

:::highlight
Magic number is quarterly GTM efficiency. CAC payback is months to recover acquisition cost from gross profit.
:::

| Metric | Formula used here | Best for | Source |
| --- | --- | --- | --- |
| Classic magic number | ((CQ ARR − PQ ARR) × 4) ÷ PQ S&M | Cross-company sales efficiency, GAAP-friendly | Scale Venture Partners (history + 0.7 median) |
| CAC payback (months) | CAC ÷ (monthly ARPA × gross margin %) | Unit economics / cash recovery | ChartMogul SaaS metrics cheat sheet |
| Segment payback targets | SMB <12 / mid-market <18 / enterprise <24 mo | Board targets by customer segment | Bessemer, Scaling to $100 Million |

Empty cells stay empty. Do not blend Scale’s median, ChartMogul’s invest/pull-back bands, and Bessemer’s segment targets into one “industry average.”

## Magic number

:::highlight
Annualize the quarterly net new recurring revenue, then divide by last quarter’s S&M.
:::

**Magic number = ((current-quarter recurring revenue − prior-quarter recurring revenue) × 4) ÷ prior-quarter sales & marketing spend**

Scale’s Rory O’Driscoll coined the framing while looking at Omniture: first-year revenue versus go-to-market spend. Dale Chang’s Scale Studio write-ups (2020–2021): long-term median across 1,000+ enterprise SaaS companies is **0.7**. A 0.7 means roughly $0.70 of recurring revenue per $1 of S&M on that definition. Scale also notes the private median has bounced and recently trended down in the periods they studied.

ChartMogul’s cheat sheet (separate publisher): above ~0.75 is commonly read as efficient enough to invest more; below ~0.5 suggests pulling back. That is their framing, not Scale’s median table.

| Read | Publisher | What they say |
| --- | --- | --- |
| Long-term median ~0.7 | Scale Venture Partners (Scale Studio) | Healthy baseline for growth-stage SaaS on their GAAP-based Magic Number |
| Above ~0.75 / below ~0.5 | ChartMogul cheat sheet | Invest more vs pull back (common operator read on their page) |

Optional second output in the tool multiplies the quarterly revenue change by gross margin before annualizing. That is a **gross-margin-adjusted** variant some operators use when margin profiles differ. It is not Scale’s classic Magic Number. Label it if you show it.

## CAC payback

:::highlight
Gross margin belongs in the denominator. Ignoring it understates months to recover.
:::

**CAC payback (months) = CAC ÷ (ARPA × gross margin %)**

ChartMogul: payback is the average time to recoup CAC through gross margin. CAC is period sales and marketing (and related acquisition) spend divided by new customers in that period. ARPA here is average monthly recurring revenue per account.

Bessemer’s Scaling to $100 Million (cloud portfolio, 2010–1H21): they evaluate CAC payback on **gross-margin-adjusted** ARR. Average payback in the **$1–10M ARR** bucket was about **15 months**, rising somewhat as companies mature. Segment targets they publish:

| Segment | Bessemer target |
| --- | --- |
| SMB-focused | Under 12 months |
| Mid-market | Under 18 months |
| Enterprise | Under 24 months |

Bessemer: invest when CLTV / CAC is about 3× or better; if much under that, keep experimenting before pouring into acquisition. ChartMogul’s LTV:CAC note on the same cheat sheet is the familiar 3:1 rule of thumb. Different pages, same order of magnitude.

Bessemer State of the Cloud 2023 also published a Good / Better / Best CAC payback ladder for that year’s fundraising context: 12–18 months good, 6–12 better, 0–6 best. That is a third framing. Put it next to the segment targets; do not average them.

## Labeled hypothetical

Not a company. Numbers chosen so both metrics are readable.

Prior-quarter ARR $2.0M. Current-quarter ARR $2.4M. Prior-quarter S&M $2.0M → classic magic number **0.80**. At 75% gross margin, a GM-adjusted variant on the same delta is **0.60**. CAC $12,000. Monthly ARPA $1,000. Gross margin 75% → payback **16.0 months** (inside Bessemer’s mid-market under-18 target; above their SMB under-12 target). Load those defaults, then replace every field with your board numbers.

## Board uses

:::highlight
Show formula, period, and which publisher’s band you are comparing against.
:::

Put magic number and payback on the same slide with the lag (prior-quarter S&M). State whether ARR is net new (includes churn) or new-logo only. State gross margin definition. If you sell mixed SMB and enterprise, show payback by segment against Bessemer’s three buckets rather than one blended number. Tie capital-efficiency context to burn multiple / Rule of 40 on the sibling page. Do not claim a single “good” magic number when Scale’s median and ChartMogul’s invest band disagree on the label.

## Mistakes

- Using current-quarter S&M in the magic number denominator during a hiring ramp.
- Skipping gross margin in payback, then comparing to Bessemer’s GM-adjusted targets.
- Averaging Scale’s 0.7 median with ChartMogul’s 0.75 invest line into one fake threshold.
- Calling payback “on plan” against the SMB under-12 target when the book of business is enterprise.
- Mixing bookings, billings, and recognized ARR in the same magic number without saying so.

## Sources

- [Scale Venture Partners, SaaS Metrics: A History of the Magic Number](https://www.scalevp.com/blog/saas-metrics-a-history-of-the-magic-number). Dale Chang, 11 September 2020. Origin story (O’Driscoll / Omniture); 0.7× as healthy baseline; long-term median ~0.7×.
- [Scale Venture Partners, From $0 to $1M: The Magic of 0.7](https://www.scalevp.com/blog/from-0-to-1m-the-magic-of-07). Dale Chang, 17 September 2021. Scale Studio 1,000+ enterprise SaaS; long-term median Magic Number 0.7; $0.70 recurring revenue per $1 S&M.
- [ChartMogul, SaaS metrics cheat sheet](https://chartmogul.com/saas-metrics/cheat-sheet/). Magic Number invest/pull-back framing (~0.75 / ~0.5); CAC; payback through gross margin; LTV:CAC ~3:1 rule of thumb.
- [Bessemer Venture Partners, Scaling to $100 Million](https://www.bvp.com/atlas/scaling-to-100-million). CAC payback on GM-adjusted ARR; ~15 months average at $1–10M ARR; SMB <12 / mid-market <18 / enterprise <24; CLTV/CAC ~3×+ invest guidance. Portfolio data 2010–1H21.
- [Bessemer Venture Partners, State of the Cloud 2023](https://www.bvp.com/atlas/state-of-the-cloud-2023). Good / Better / Best CAC payback: 12–18 / 6–12 / 0–6 months in that year’s fundraising benchmarks.
