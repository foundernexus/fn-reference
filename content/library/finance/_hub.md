---
title: Finance, metrics & runway
description: The numbers your board needs: burn multiple, Rule of 40, NRR and GRR, what counts as ARR, AI gross margin, runway, and when to hire a CFO.
slug: finance
section: library
cluster: finance
target_query: startup board financial metrics
date: 2026-09-25
close: Board metrics and runway calls are ops decisions. Founders who have walked burn, retention, and default alive through a raise or a board pack will pressure-test your pack in a VEN session.
disclaimer: not-legal-tax
draft: false
---

Early boards live on burn multiple, runway with a hiring plan, and whether you are default alive. Retention slides need GRR beside NRR so expansion cannot mask a leaky base. ARR needs one written definition: subscription fees and minimum commits in, usage above the commit on its own labeled line. AI products need gross margin with production inference in COGS, shown beside the software-only figure. Later boards add Rule of 40 with an explicit profit definition, and magic number / CAC payback when GTM efficiency is the question. At Series A you usually need CFO-level work before you need a full-time CFO. Pick the page or calculator for the decision in front of you. Not legal, tax, or investment advice.

:::group Metrics and the CFO seat
- [Burn multiple vs Rule of 40](/library/finance/burn-multiple-vs-rule-of-40/): Which efficiency number goes in the pack. Early: burn multiple trend. Later: add Rule of 40 and name the profit line.
- [NRR vs GRR for the board pack](/library/finance/nrr-vs-grr-board-pack/): Retention looks strong on NRR alone. Show GRR beside it so expansion cannot hide churn.
- [Does usage revenue count as ARR?](/library/finance/usage-revenue-as-arr/): Usage revenue in ARR. Count only up to the contract commit; put usage above it on its own line.
- [AI SaaS gross margin: inference COGS in the board pack](/library/finance/ai-gross-margin-inference-cogs/): AI costs blur gross margin. Put production inference in COGS and show margin with and without AI.
- [Customer concentration risk](/library/finance/customer-concentration/): One customer carries the revenue. Report largest and top-five share at the parent level, and grow around the account before a raise or sale.
- [Fractional vs full-time CFO](/library/finance/fractional-vs-full-time-cfo/): Hiring finance after Series A. You need CFO-level work first; a full-time CFO usually comes later.
:::

:::group Calculators
- [Runway calculator with hiring plan](/tools/runway-calculator/): Months to cash-out with your hiring plan, plus a default alive or default dead read.
- [When runway runs out](/library/fundraising/when-runway-runs-out/): Runway is short. Cut burn, bridge, or wind down in order. Pair it with the calculator above.
- [Magic number & CAC payback calculator](/tools/magic-number-cac-payback-calculator/): Is sales spend paying back? Magic number beside gross-margin CAC payback.
- [AI gross margin calculator](/tools/ai-gross-margin-calculator/): Gross margin with and without AI costs, plus the AI budget that hits your target margin.
:::

:::takeaways
- Still burning (Seed to early growth): lead with burn multiple trend (Sacks). Snapshot runway is cash ÷ net burn (Kruze). Ask default alive with the hire ladder typed in (Paul Graham).
- Retention: put GRR, NRR, and growth on one page (Wallington via ChartMogul). SaaS Capital 2023 median NRR 102% / GRR 91% is a different sample from ChartMogul Dec 2025 median NRR 82%. Show them on separate rows.
- Approaching scale: add Rule of 40 (Feld; Bessemer popularized for cloud). Early negative-FCF: Bessemer prefers burn multiple ~1×–1.5× over Rule of X theater.
- GTM efficiency: magic number (Scale long-term median 0.7) beside gross-margin CAC payback (ChartMogul; Bessemer segment targets <12 / <18 / <24 mo).
- ARR definition: count subscriptions and recurring minimum commits. Show usage above the commit as a labeled usage run-rate with its window, and use the same definition in the deck, model, and board pack.
- AI gross margin: production inference, GPU serving, and retrieval go in COGS. Training, dev/test inference, and internal tools stay in R&D. Show AI-inclusive gross margin beside software gross margin ex-AI, and do not hold it to classic SaaS bands.
- Finance seat: Series A generally fractional first (Kruze). Upgrade when interaction is constant or you hit the ARR / sequence window peers name (Bessemer; Majhi).
:::

## Which metric → when → where

:::highlight
One board question per row. Do not average publishers that disagree on stage or sample.
:::

| Board question | Metric / call | When it belongs | Use |
| --- | --- | --- | --- |
| How much cash per dollar of net new ARR? | Burn multiple (net burn ÷ net new ARR) | Seed to early growth while still burning | [Burn multiple vs Rule of 40](/library/finance/burn-multiple-vs-rule-of-40/) |
| Growth + margin at scale? | Rule of 40 (say which profit); Rule of X only in late-stage valuation talk | Approaching scale / later raise narrative | [Burn multiple vs Rule of 40](/library/finance/burn-multiple-vs-rule-of-40/) |
| Is the base leaky under expansion? | GRR + NRR + growth on one page | Any recurring-revenue board with expansion stories | [NRR vs GRR for the board pack](/library/finance/nrr-vs-grr-board-pack/) |
| Does our AI usage revenue count as ARR? | Committed ARR + labeled usage run-rate + pilots + services as separate lines | Any board or raise where customers pay for usage | [Usage revenue as ARR](/library/finance/usage-revenue-as-arr/) |
| What is our gross margin once inference is counted? | AI-inclusive gross margin + software gross margin ex-AI + AI cost % of revenue + cost per user or workflow + heavy-user cohort | Any board or raise where inference is part of delivery | [AI SaaS gross margin](/library/finance/ai-gross-margin-inference-cogs/) |
| How many months of cash with this hire plan? | Snapshot runway; trajectory with hires; default alive / dead | Before a hire wave or a raise clock | [Runway calculator](/tools/runway-calculator/) |
| Is GTM spend efficient this quarter? | Magic number + CAC payback months | When S&M ramp or segment payback is the debate | [Magic number & CAC payback calculator](/tools/magic-number-cac-payback-calculator/) |
| How exposed are we to one customer? | Largest customer share + top-five share, rolled up to the parent, with trend | Before a raise, a sale, or a renewal of the big account | [Customer concentration risk](/library/finance/customer-concentration/) |
| Do we need a full-time CFO yet? | Fractional vs full-time (workload, complexity, ARR / sequence window) | Series A finance build; pre-B upgrade talk | [Fractional vs full-time CFO](/library/finance/fractional-vs-full-time-cfo/) |

Empty cells stay empty. Each row comes from a different publisher and answers a different board question. A [VEN](https://www.venexecs.com/?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library) session pushed on the same three things: stage-right metrics, GRR beside NRR, and default alive with the hire dates written down. That is session judgment, not a survey.

## Stage sketch for the pack

:::highlight
Early: show the cash cost of growth and the cash left. Later: add margin balance and GTM recovery. At each stage: show retention without masking.
:::

**Seed to early Series A (still burning).** Lead with burn multiple trend (Sacks bands: under 1× amazing through over 3× bad; seed may sit near 3×, post-A toward ~2×). Show net burn and net new ARR as separate lines. Put snapshot runway and the hire ladder on one page with the [runway calculator](/tools/runway-calculator/). If net new ARR is zero, burn multiple does not compute (Sacks). Keep burn low and get to first revenue.

**Growth / later raise prep.** Keep burn multiple while you are still cash-negative. Add Rule of 40 with an explicit profit definition (Feld prefers EBITDA; Bessemer often uses FCF margin in Rule of X). Bessemer: early negative-FCF companies should prefer an attractive burn multiple (~1×–1.5×); Rule of X is less relevant there.

**Any recurring-revenue board.** Show GRR and NRR for the same cohort and period. SaaS Capital (2023, >$1M ARR): median NRR 102%, median GRR 91%; table stakes GRR at least ~90%. Label Bessemer SotC 2019 segment aims and ChartMogul Dec 2025 medians by source. Do not average 102% with 82%. If customers pay for usage, run retention on committed ARR and show usage run-rate on its own line ([usage revenue as ARR](/library/finance/usage-revenue-as-arr/)).

**AI product on the P&L.** Put production inference and the AI infrastructure layer in COGS, and show AI-inclusive gross margin beside software gross margin ex-AI. Compare it to AI bands by source, not to classic SaaS bands. Lower margin raises net burn and stretches gross-margin CAC payback, so rerun both on the AI-inclusive figure ([AI SaaS gross margin](/library/finance/ai-gross-margin-inference-cogs/)).

**GTM debate on the table.** Magic number with prior-quarter S&M in the denominator. CAC payback on gross margin. Show Scale’s 0.7 median and ChartMogul’s ~0.75 / ~0.5 bands as separate rows.

**Finance org.** Put a bookkeeper and controller under the strategy seat. Buy fractional help for the model and pack until you hit an upgrade trigger ([fractional vs full-time CFO](/library/finance/fractional-vs-full-time-cfo/)). Pair with the [Series A leadership hiring sequence](/library/hiring/series-a-leadership-hiring-sequence/) when the board asks which exec seat comes first.

## Sources

- [David Sacks, The Burn Multiple (Craft Ventures / Medium)](https://medium.com/craft-ventures/the-burn-multiple-51a7e43cb200) — 23 April 2020. Formula; tier chart; stage guidance.
- [Brad Feld, The Rule of 40% For a Healthy SaaS Company](https://feld.com/archives/2015/02/rule-40-healthy-saas-company/) — 25 February 2015. Growth + profit ≥ 40; scale caveat.
- [Bessemer Venture Partners, The Rule of X](https://www.bvp.com/atlas/the-rule-of-x) — Rule of 40 restated; early-stage prefer burn multiple ~1×–1.5×.
- [ChartMogul, NRR](https://chartmogul.com/saas-metrics/nrr/) and [GRR](https://chartmogul.com/saas-metrics/grr/) — movement formulas; masking warning; Dec 2025 sample.
- [SaaS Capital, Research Brief 28: 2023 B2B SaaS Retention Benchmarks (PDF)](https://www.saas-capital.com/wp-content/uploads/2023/05/RB28WS1-2023-B2B-SaaS-Retention-Benchmarks.pdf) — median NRR 102% / GRR 91%; ≥90% GRR table stakes.
- [Bessemer Venture Partners, State of the Cloud 2019](https://www.bvp.com/atlas/state-of-the-cloud-2019) and [Scaling to $100 Million](https://www.bvp.com/atlas/scaling-to-100-million) — segment GRR/NRR aims; CAC payback targets by segment.
- [Scale Venture Partners, From $0 to $1M: The Magic of 0.7](https://www.scalevp.com/blog/from-0-to-1m-the-magic-of-07) — Dale Chang, 17 Sep 2021. Scale Studio long-term median magic number 0.7. See also [SaaS Metrics: A History of the Magic Number](https://www.scalevp.com/blog/saas-metrics-a-history-of-the-magic-number).
- [ChartMogul, SaaS metrics cheat sheet](https://chartmogul.com/saas-metrics/cheat-sheet/) — magic number invest/pull-back framing; CAC payback through gross margin.
- [Paul Graham, Default Alive or Default Dead?](https://paulgraham.com/aord.html) — October 2015. Alive/dead test; hiring too fast as the biggest killer after a raise.
- [Kruze Consulting, rolling cash forecast / runway](https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/) — cash ÷ net burn; headcount 60–80% of burn. [When a startup needs a CFO](https://kruzeconsulting.com/startup-need-cfo/) — Series A generally fractional first.
- [Carta, State of Private Markets Q1 2024](https://carta.com/sg/en/data/state-of-private-markets-q1-2024/) — median Seed→A 766 days; A→B 824 days.
- [VEN (Venture Executive Network)](https://www.venexecs.com/?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library) — founder session. Stage-right board metrics; GRR beside NRR; default alive with hire dates. Not a survey.

## Related

- [Burn multiple vs Rule of 40](/library/finance/burn-multiple-vs-rule-of-40/)
- [NRR vs GRR for the board pack](/library/finance/nrr-vs-grr-board-pack/)
- [Does usage revenue count as ARR?](/library/finance/usage-revenue-as-arr/)
- [AI SaaS gross margin: inference COGS in the board pack](/library/finance/ai-gross-margin-inference-cogs/)
- [Customer concentration risk](/library/finance/customer-concentration/)
- [Fractional vs full-time CFO](/library/finance/fractional-vs-full-time-cfo/)
- [Runway calculator with hiring plan](/tools/runway-calculator/)
- [Magic number & CAC payback calculator](/tools/magic-number-cac-payback-calculator/)
- [AI gross margin calculator](/tools/ai-gross-margin-calculator/)
- [Series A leadership hiring sequence](/library/hiring/series-a-leadership-hiring-sequence/)
- [Hiring executives](/library/hiring/)
- [Monthly investor update template](/library/board/monthly-investor-update/)
