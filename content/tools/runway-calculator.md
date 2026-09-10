---
title: Runway calculator with hiring plan
description: Turn cash, burn, revenue growth, and a hire ladder into snapshot runway, months to cash-out, and a Paul Graham–style default alive or default dead read. Labeled hypothetical. Not advice.
slug: runway-calculator
section: tools
cluster: finance
layout: calculator
calculator_js: runway-calculator.js
target_query: startup runway calculator hiring plan
date: 2026-09-10
close: Runway and default-alive calls are board-visible. If you want founders who just lived that conversation to pressure-test your hiring plan against the cash left, that conversation happens at FounderNexus.
disclaimer: not-legal-tax
draft: false
related:
- library/finance/burn-multiple-vs-rule-of-40
- tools/option-pool-shuffle-calculator
---

Enter cash, current revenue and expenses, a growth rate, and a planned hire ladder. You get snapshot runway (ignore hiring and growth), months to cash-out with the plan, and whether this model is default alive or default dead before cash hits zero. Not legal, tax, or investment advice.

:::takeaways
- Snapshot runway = cash ÷ monthly net burn (Kruze). Net burn = cash out − cash in. If net burn ≤ 0 at today’s run-rate, you are not burning.
- A forecast without the hire ladder is a guess. Kruze: headcount is often 60–80% of burn.
- Paul Graham (2015): default alive means, if expenses stay constant and recent revenue growth continues, you reach profitability on the cash you have. Default dead means you do not. Hiring too fast is by far the biggest killer of startups that raise money.
- Carta Q1 2024: median Seed→A was 766 days; A→B was 824 days. Longer waits mean more runway required.
- Use cash, not only P&L. Average net burn over the last 3–6 months when you set the starting point (Kruze).
:::

## What it models

:::highlight
Constant base expenses plus an explicit hire ladder, with revenue compounding monthly.
:::

Month zero is cash on hand, current monthly revenue, and current monthly expenses before planned hires. Each later month grows revenue by your growth %, adds fully loaded cost for every hire whose start month has arrived, holds other expenses flat, and updates cash by revenue minus expenses.

That matches Paul Graham’s “expenses remain constant” test, with the hiring plan as the one expense path you choose to change. It is not Trevor Blackwell’s calculator that PG points to. It is a browser tool for the same question with your hire dates typed in.

## Snapshot runway vs trajectory

:::highlight
Snapshot is a static ratio. Trajectory asks whether you cross to profitable before cash runs out.
:::

| Term | Definition | Source |
| --- | --- | --- |
| Gross burn | Cash out for the period | Kruze Consulting, 22 Feb 2026 |
| Net burn | Cash out − cash in | Kruze Consulting, 22 Feb 2026 |
| Runway (months) | Cash ÷ monthly net burn | Kruze Consulting, 22 Feb 2026 |
| Default alive | On constant expenses and recent revenue growth, reach profitability before cash runs out | Paul Graham, Oct 2015 |
| Default dead | Same assumptions; you do not reach profitability on the cash left | Paul Graham, Oct 2015 |

Kruze’s worked example: $4.2M cash ÷ $350k net burn = 12 months; at $280k burn → 15 months. Snapshot runway in this tool is that ratio with hiring and growth turned off.

Paul Graham’s question is different. Assume expenses stay constant and revenue keeps growing as it has in recent months. Do you hit profitability on the cash you have? If yes, default alive. If no, default dead. The fatal pinch is default dead plus slow growth plus not enough time to fix it. He also notes Airbnb waited four months after raising at the end of YC before the first employee.

Carta’s State of Private Markets Q1 2024: median time between rounds lengthened (Seed→A 766 days; A→B 824 days in that quarter). Their piece frames a longer A→B wait versus an earlier cycle as needing more runway (on the order of three more months in their comparison). Longer fundraising clocks raise the bar on how much cash you need under either read.

## Hiring plan as burn plan

:::highlight
Most burn is people. Model start dates, not hope dates.
:::

Kruze: headcount often runs 60–80% of total burn. A rolling 18-month cash forecast without the hire plan is not a forecast. They cite a US SBA rule of thumb for fully loaded cost of about 1.25–1.4× base salary. Build that into the monthly cost per hire field. Assume future hires start a month or two later than the date on the slide.

Spacing matters. Three hires in month two is a different cash path than one hire every other month. PG’s warning that hiring too fast is the biggest killer of startups that raise money is the same problem in operator language.

## Labeled hypothetical

Not a company. Scaled to Kruze’s $4.2M / ~$350k example.

Cash $4.2M. Revenue $80k. Expenses before planned hires $430k (so starting net burn $350k). Monthly revenue growth 8%. Three hires at $18k fully loaded per month each. First starts in month 2, then one per month. Horizon 18 months. Load those defaults. Read snapshot versus plan, then whether revenue covers expenses before cash hits zero. Replace every input with your numbers before you take anything to a board.

## Board uses

:::highlight
Put both the static months and the alive/dead call in the pack with the hire dates.
:::

Show snapshot runway so everyone shares the same cash ÷ net burn starting point. Show the hire ladder and the month cash would hit zero if the plan runs. Show whether this model crosses to revenue ≥ expenses before that month. If Carta-style round timing is stretching, say how many months of buffer you are buying. Tie efficiency reads (burn multiple, Rule of 40) to a sibling page. Do not present a single “runway” number when the hire plan is still open.

## Mistakes

- Treating snapshot runway as the plan when three hires are already verbal-offered.
- Using P&L burn and ignoring cash timing (Kruze: use cash; average the last 3–6 months of net burn when you set the start).
- Booking hire starts on the recruiting slide date instead of a month or two later.
- Calling the company default alive because last month’s growth looked fine while the hire plan doubles expenses before revenue catches up.
- Inventing round-timing benchmarks. Cite Carta’s published medians or leave the cell empty.

## Sources

- [Paul Graham, Default Alive or Default Dead?](http://paulgraham.com/aord.html). October 2015. Default alive vs default dead; hiring too fast; Airbnb’s four-month wait; fatal pinch; points to Trevor Blackwell’s calculator.
- [Kruze Consulting, Build a Rolling Cash Forecast to Maximize Startup Runway](https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/). 22 February 2026. Gross vs net burn; runway = cash ÷ monthly net burn; $4.2M / $350k example; headcount 60–80% of burn; rolling 18-month forecast; SBA fully loaded 1.25–1.4×; recruiting slips; cash over P&L.
- [Carta, State of Private Markets Q1 2024](https://carta.com/sg/en/data/state-of-private-markets-q1-2024/). Median Seed→A 766 days; A→B 824 days; longer waits imply more runway required.
