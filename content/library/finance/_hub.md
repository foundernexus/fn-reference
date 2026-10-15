---
title: Finance, metrics & runway
description: Put the right efficiency, retention, and runway reads in front of the board. Orient burn multiple, Rule of 40, NRR/GRR, magic number, the ARR definition, AI gross margin, and the CFO seat.
slug: finance
section: library
cluster: finance
target_query: startup board financial metrics
date: 2026-09-25
close: Board metrics and runway calls are ops decisions. Founders who have walked burn, retention, and default alive through a raise or a board pack will pressure-test your pack in a FounderNexus session.
disclaimer: not-legal-tax
draft: false
---

Early boards live on burn multiple, runway with a hiring plan, and whether you are default alive. Retention slides need GRR beside NRR so expansion cannot mask a leaky base. ARR needs one written definition: subscription fees and minimum commits in, usage above the commit on its own labeled line. AI products need gross margin with production inference in COGS, shown beside the software-only figure. Later boards add Rule of 40 with an explicit profit definition, and magic number / CAC payback when GTM efficiency is the question. At Series A you usually need CFO-level work before you need a full-time CFO. Pick the spoke or tool for the decision in front of you. Not legal, tax, or investment advice.

:::takeaways
- Still burning (Seed to early growth): lead with burn multiple trend (Sacks). Snapshot runway is cash ÷ net burn (Kruze). Ask default alive with the hire ladder typed in (Paul Graham).
- Retention: put GRR, NRR, and growth on one page (Wallington via ChartMogul). SaaS Capital 2023 median NRR 102% / GRR 91% is a different sample from ChartMogul Dec 2025 median NRR 82%. Show them on separate rows.
- Approaching scale: add Rule of 40 (Feld; Bessemer popularized for cloud). Early negative-FCF: Bessemer prefers burn multiple ~1×–1.5× over Rule of X theater.
- GTM efficiency: magic number (Scale long-term median 0.7) beside gross-margin CAC payback (ChartMogul; Bessemer segment targets <12 / <18 / <24 mo).
- ARR definition: count subscriptions and recurring minimum commits. Show usage above the commit as a labeled usage run-rate with its window, and use the same definition in the deck, model, and board pack.
- AI gross margin: production inference, GPU serving, and retrieval go in COGS. Training, dev/test inference, and internal tools stay in R&D. Show AI-inclusive gross margin beside software gross margin ex-AI, and do not hold it to classic SaaS bands.
- Finance seat: Series A generally fractional first (Kruze). Upgrade when interaction is constant or you hit the ARR / sequence window peers name (Bessemer; Majhi).
:::

## Spokes in this cluster

:::highlight
This cluster covers five decisions: how to balance efficiency against scale, how to report retention without masking churn, what counts as ARR when customers pay for usage, how to report gross margin when inference is part of delivery, and when to hire a full-time CFO.
:::

- [Burn multiple vs Rule of 40](/library/finance/burn-multiple-vs-rule-of-40/): Burn multiple = net burn ÷ net new ARR (Sacks / Craft, April 2020). Rule of 40 = growth % + profit % (Feld, February 2015). Early pack: burn trend. Later: add Rule of 40 and say which profit. Bessemer’s Rule of X is a late-stage valuation frame, not a Seed slide.
- [NRR vs GRR for the board pack](/library/finance/nrr-vs-grr-board-pack/): GRR is the leak check (capped at 100%). NRR includes expansion and can exceed 100%. ChartMogul formulas; SaaS Capital and Bessemer bands stay on separate rows. If GRR is 70% and NRR looks strong, expansion is hiding churn.
- [Does usage revenue count as ARR?](/library/finance/usage-revenue-as-arr/): only up to the contract’s commit. Subscription fees and recurring minimum commits are ARR. Usage above the commit, pay-as-you-go, pilots, credits, and services go on separate lines. Write a one-page ARR policy and state the annualization window.
- [AI SaaS gross margin: inference COGS in the board pack](/library/finance/ai-gross-margin-inference-cogs/): production inference, production GPU serving, retrieval serving customers, AI monitoring, AI support, and human review go in COGS. Training, fine-tuning, dev/test inference, and internal AI tools stay in R&D or the department that uses them. Split production and development AI accounts first (The SaaS CFO). Show AI-inclusive gross margin, software gross margin ex-AI, AI cost as a share of revenue, and a heavy-user cohort. Andreessen Horowitz, Bessemer, and ICONIQ bands stay on separate rows.
- [Fractional vs full-time CFO](/library/finance/fractional-vs-full-time-cfo/): at Series A you need the model, board pack, and raise prep. Kruze: usually not a full-time CFO yet. Bessemer community: many CFOs land at $10M–$25M ARR. Majhi B2B SaaS: often months 12–24 after A, or pre-B.

## Tools in this cluster

:::highlight
Run the hire ladder, the GTM efficiency pair, and the AI margin check before the meeting.
:::

- [Runway calculator with hiring plan](/tools/runway-calculator/): snapshot runway (Kruze) plus months to cash-out with hires, plus a Paul Graham–style default alive / default dead read. Headcount often 60–80% of burn (Kruze). With Carta’s Q1 2024 medians of 766 days Seed→A and 824 days A→B, you need a bigger buffer.
- [When runway runs out](/library/fundraising/when-runway-runs-out/): diagnose short runway, cut burn, bridge or angel capital, or orderly wind-down. Pair with the calculator above.
- [Magic number & CAC payback calculator](/tools/magic-number-cac-payback-calculator/): Scale-style magic number next to gross-margin CAC payback. Scale Studio long-term median 0.7. ChartMogul’s invest/pull-back bands (~0.75 / ~0.5) come from a different publisher. Bessemer payback targets by segment.
- [AI gross margin calculator](/tools/ai-gross-margin-calculator/): AI-inclusive gross margin beside software margin ex-AI, AI cost per user or workflow, a heavy-user cohort read, and the AI budget that hits your target margin. Reads against The SaaS CFO’s bands by product type.

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
| Do we need a full-time CFO yet? | Fractional vs full-time (workload, complexity, ARR / sequence window) | Series A finance build; pre-B upgrade talk | [Fractional vs full-time CFO](/library/finance/fractional-vs-full-time-cfo/) |

Empty cells stay empty. Each row comes from a different publisher and answers a different board question. A [FounderNexus](https://www.foundernexus.com?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library) session pushed on the same three things: stage-right metrics, GRR beside NRR, and default alive with the hire dates written down. That is session judgment, not a survey.

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
- [Paul Graham, Default Alive or Default Dead?](http://www.paulgraham.com/aord.html) — October 2015. Alive/dead test; hiring too fast as the biggest killer after a raise.
- [Kruze Consulting, rolling cash forecast / runway](https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/) — cash ÷ net burn; headcount 60–80% of burn. [When a startup needs a CFO](https://kruzeconsulting.com/startup-need-cfo/) — Series A generally fractional first.
- [Carta, State of Private Markets Q1 2024](https://carta.com/sg/en/data/state-of-private-markets-q1-2024/) — median Seed→A 766 days; A→B 824 days.
- [FounderNexus](https://www.foundernexus.com?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library) — founder session. Stage-right board metrics; GRR beside NRR; default alive with hire dates. Not a survey.

## Related

- [Burn multiple vs Rule of 40](/library/finance/burn-multiple-vs-rule-of-40/)
- [NRR vs GRR for the board pack](/library/finance/nrr-vs-grr-board-pack/)
- [Does usage revenue count as ARR?](/library/finance/usage-revenue-as-arr/)
- [AI SaaS gross margin: inference COGS in the board pack](/library/finance/ai-gross-margin-inference-cogs/)
- [Fractional vs full-time CFO](/library/finance/fractional-vs-full-time-cfo/)
- [Runway calculator with hiring plan](/tools/runway-calculator/)
- [Magic number & CAC payback calculator](/tools/magic-number-cac-payback-calculator/)
- [AI gross margin calculator](/tools/ai-gross-margin-calculator/)
- [Series A leadership hiring sequence](/library/hiring/series-a-leadership-hiring-sequence/)
- [Hiring executives](/library/hiring/)
- [Monthly investor update template](/library/board/monthly-investor-update/)
