---
title: "Default alive or default dead: the test, the math, the fix"
description: "Default alive means you reach profit on the cash you have at current growth. At 12 months of runway that takes about 6.8% monthly revenue growth."
slug: default-alive-default-dead
section: library
cluster: finance
layout: article
target_query: default alive default dead
date: 2026-11-02
close: Founders who have turned a default dead plan into a default alive one will pressure-test your growth rate, your hire dates, and your plan B in a VEN session.
disclaimer: not-legal-tax
draft: false
related:
- library/finance
- tools/runway-calculator
- library/fundraising/when-runway-runs-out
- library/finance/burn-multiple-vs-rule-of-40
- library/board/missed-plan-reforecast
- library/fundraising/when-to-raise-series-a
---

You are default alive if, with expenses held flat and revenue growing at its recent rate, you reach profitability before the cash runs out. If you don't, you are default dead (Paul Graham, 2015). Run it with three numbers: cash, monthly revenue, monthly expenses, plus your recent monthly growth rate. A company with **12** months of snapshot runway needs about **6.8%** monthly revenue growth to pass (editorial arithmetic below). Default dead is a plan problem you can fix. Cut burn, raise growth, or both, and write down the date you switch to plan B. Not legal, tax, or investment advice.

:::takeaways
- The test holds expenses flat and growth at its recent rate, then asks whether revenue covers costs before cash hits zero (Paul Graham, Oct 2015).
- Graham asks it of any startup past **8 or 9** months old, and says half the founders he talks to don't know the answer.
- Growth needed rises fast as runway shrinks. In the example below, **24** months of runway needs about **3.3%** a month and **6** months needs about **14.7%**.
- A hire plan changes the answer. Adding **$70K** a month of payroll in the same example turns a pass at **8%** growth into cash-out in month **12**.
- Plan for the gap between rounds. Carta's Q1 2026 median from seed to Series A is **2.0** years, and **2.1** years from A to B.
:::

This page covers the test itself and the math behind it. To model your own numbers with a hire ladder, use the [runway calculator](/tools/runway-calculator/). If the answer is bad and cash is short, go to [when runway runs out](/library/fundraising/when-runway-runs-out/).

## The test in one table

:::highlight
Two assumptions: expenses stay flat, and revenue keeps growing at its recent monthly rate.
:::

| Term | Definition | Source |
| --- | --- | --- |
| Default alive | On flat expenses and recent revenue growth, you reach profitability on the money you have left | Paul Graham, Oct 2015 |
| Default dead | Same assumptions; cash runs out before revenue covers expenses | Paul Graham, Oct 2015 |
| Fatal pinch | Default dead, slow growth, and not enough time to fix it | Paul Graham, Dec 2014 and Oct 2015 |
| Net burn | Cash out minus cash in each month | Kruze Consulting, Feb 2026 |
| Snapshot runway | Cash ÷ net burn. **$4.2M** ÷ **$350K** = **12** months | Kruze Consulting, Feb 2026 |

Snapshot runway ignores growth. The default alive test adds it. A company with 12 months of snapshot runway can pass or fail depending on how fast revenue grows, so you need both numbers.

## How to run the test

1. Take cash in the bank today. Leave out receivables and unsigned term sheets.
2. Take this month's revenue and this month's total expenses.
3. Take your monthly revenue growth rate over the last several months. Graham's wording is "what it has been over the last several months."
4. Grow revenue at that rate month by month, hold expenses flat, and subtract each month's loss from cash.
5. If revenue covers expenses before cash goes below zero, you are default alive. Note the month and the cash left.

A spreadsheet does this in twelve rows. Keep expenses flat only for the test. Run a second version with your real hire plan, because that is the plan you will spend against.

## Labeled example: the growth rate you need

Editorial arithmetic. Not a company and not a market rate.

You have **$3.0M** in cash. Revenue is **$100K** a month and expenses are **$350K** a month, so net burn is **$250K** and snapshot runway is **12** months.

| Monthly revenue growth | Result | When it resolves | Cash left at that point |
| --- | --- | --- | --- |
| 3% | Default dead | Cash runs out in month 14 | None |
| 5% | Default dead | Cash runs out in month 15 | None |
| About 6.8% | Break-even line | Revenue covers expenses in month 21 | Close to $0 |
| 7% | Default alive | Revenue covers expenses in month 20 | About $88K |
| 8% | Default alive | Revenue covers expenses in month 18 | About $425K |
| 10% | Default alive | Revenue covers expenses in month 15 | About $897K |

Growth stretches runway past the snapshot figure even when you fail. At 3% a month this company still lasts into month 14, two months past the 12-month snapshot.

Now hold the same revenue and costs, and change only the cash. The break-even growth rate moves like this:

| Snapshot runway | Cash at $250K net burn | Monthly growth needed to pass | Same rate per year |
| --- | --- | --- | --- |
| 6 months | $1.5M | About 14.7% | About 5.2× |
| 9 months | $2.25M | About 9.3% | About 2.9× |
| 12 months | $3.0M | About 6.8% | About 2.2× |
| 18 months | $4.5M | About 4.4% | About 1.7× |
| 24 months | $6.0M | About 3.3% | About 1.5× |

Graham writes that steep revenue growth, "say over 5x a year," lets you start to count on investor interest even while unprofitable. In this example, 5× a year is about what a company with six months of cash needs to pass the test on its own.

## What a hire plan does to the answer

Graham calls hiring too fast "by far the biggest killer of startups that raise money." The example shows the mechanism.

| Case (same $3.0M cash, $100K revenue) | Expenses | Growth | Result |
| --- | --- | --- | --- |
| Base | $350K | 8% | Default alive in month 18, about $425K left |
| Add **$70K** a month of payroll now | $420K | 8% | Default dead, cash runs out in month 12 |
| Same hires, growth needed to pass | $420K | About 10.5% | Break-even line |
| Cut expenses by **$50K** a month | $300K | 5% | Default alive in month 24, about $243K left |

Four hires at about $17.5K a month each, fully loaded, would add that $70K. If the hires don't raise growth from 8% to about 10.5% a month, they move the company from alive to dead. Put the hire start dates in the model before you call the company default alive.

The cut row shows the other lever. At 5% growth the base company fails. Taking $50K a month out of expenses makes it pass, with about two years to profitability.

## Why the gap between rounds matters

Default dead is safe only if investors save you, and Graham warns that you can never treat fundraising as more than plan A. The time between rounds sets how long plan A has to work.

| Measure | Figure | Source |
| --- | --- | --- |
| Median time, seed to Series A | **2.0** years, Q1 2026 | Carta, State of Private Markets Q1 2026 |
| Median time, Series A to Series B | **2.1** years, Q1 2026 | Carta, State of Private Markets Q1 2026 |
| Median time, Series B to Series C | **2.4** years, Q1 2026 | Carta, State of Private Markets Q1 2026 |
| Median wait before a Series A, Q4 2024 | **774** days, about 2.1 years | Carta, fundraising guide |
| Runway Carta tells founders to plan for | At least **24 to 30** months, against a common **12 to 18** month target | Carta, fundraising guide |

Carta calls the Q1 2026 intervals "historically elevated" and notes that early-stage gaps are starting to shorten. The planning advice stays the same. If you are default dead with 18 months of cash and the median gap to your next round is two years, your plan A needs better than median timing.

There is no reliable public benchmark yet for the share of Seed to Series B companies that are default alive, or for the monthly growth rate they run at. Use your own numbers and the arithmetic above.

## What to do with the answer

| Your result | Next move | Source |
| --- | --- | --- |
| Default alive with room to spare | Talk about ambitious new things you could do with the cash | Paul Graham, Oct 2015 |
| Default alive only with the current team | Keep hiring tied to growth. Rerun the test before each hire | Paul Graham, Oct 2015 |
| Default dead, more than 8 months of cash | Cut burn, raise growth, or both, now. Write plan B and the switch date | Paul Graham, Oct 2015; YC, Caldwell |
| Default dead, **8** months of runway or less | Try to raise the money right now so you learn the answer while you can still act | Paul Graham, Dec 2014 |
| Under **3** months of cash | Face the shutdown scenario. Caldwell writes that under **2** months is often the point of no return | YC, Caldwell, Jan 2015 |

Dalton Caldwell's YC post tells a default dead founder to grow revenue, cut costs, or both, right away. He lists PR, marketing, and perks as the first spend to cut.

The VEN session judgment lines up with Graham. Founders who run the test every month, with the hire dates in the model, catch a default dead plan while there is still time to change it.

:::steps Default alive check for this month's board pack
1. **Pull three numbers.** Cash today, this month's revenue, this month's total expenses.
2. **Set the growth rate.** Average monthly revenue growth over the last several months. Write down the window you used.
3. **Run flat expenses first.** Grow revenue, hold costs, subtract monthly losses until revenue covers costs or cash hits zero.
4. **Run the hire plan second.** Add each planned hire on its start date and rerun.
5. **Find your break-even growth rate.** Lower the growth rate until the plan fails. That number goes on the board slide.
6. **Write plan B.** The cuts you would make, their monthly savings, and the date you switch if the raise isn't working (Paul Graham).
7. **Rerun it every month.** Use the [runway calculator](/tools/runway-calculator/) or your own sheet, and keep the same definitions each time.
:::

## Mistakes founders make with the test

**Using last month's growth spike.** One strong month inflates the rate. Graham's test uses the last several months.

**Leaving out the hire plan.** The test holds expenses flat. Your plan doesn't. A pass on flat expenses can fail once the hires land.

**Counting the next round as revenue.** Graham's fix is to say it out loud: "We're default dead, but we're counting on investors to save us."

**Asking too late.** Graham's advice is to start asking too early. Worrying early costs little. Worrying late leads to the fatal pinch.

**Treating gross burn as net burn.** Runway divides cash by net burn, cash out minus cash in (Kruze).

## Pair this with

- [Runway calculator with hiring plan](/tools/runway-calculator/) to run the test with your own hire ladder.
- [When runway runs out](/library/fundraising/when-runway-runs-out/) for the cut, bridge, and wind-down paths.
- [Burn multiple vs Rule of 40](/library/finance/burn-multiple-vs-rule-of-40/) for the efficiency number beside the runway slide.
- [How to tell the board you missed the plan](/library/board/missed-plan-reforecast/) when the test fails mid-year.

## Sources

- [Paul Graham, Default Alive or Default Dead?](https://paulgraham.com/aord.html). October 2015. Definition of default alive and default dead on constant expenses and recent revenue growth; asked of startups operating more than 8 or 9 months; half of founders don't know; steep revenue growth "say over 5x a year"; never treat fundraising as more than plan A; write down plan B and when to switch; hiring too fast is by far the biggest killer of startups that raise money; start asking too early.
- [Paul Graham, The Fatal Pinch](https://paulgraham.com/pinch.html). December 2014. Default dead with slow growth and little time; with 8 months of runway or less, try to get the money right now.
- [Y Combinator, Advice for Companies With Less Than 1 Year of Runway](https://www.ycombinator.com/blog/advice-startups-running-out-of-money). Dalton Caldwell, 22 January 2015. Default dead founders must grow revenue, cut costs, or both, right away; PR, marketing, and perks as first cuts; under 3 months of cash, account for shutdown; under 2 months often the point of no return.
- [Kruze Consulting, Build a Rolling Cash Forecast to Maximize Startup Runway](https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/). 22 February 2026. Net burn is cash out minus cash in; runway is cash ÷ net burn; $4.2M ÷ $350K = 12 months.
- [Carta, State of Private Markets Q1 2026 (full report)](https://carta.com/data/state-of-private-markets-q1-2026-full-report/). Data as of May 2026. Median time between primary rounds: seed to Series A 2.0 years, Series A to B 2.1 years, Series B to C 2.4 years; historically elevated; early-stage intervals beginning to compress.
- [Carta, Startup funding: a guide to raising startup capital](https://carta.com/learn/startups/fundraising/). Median Series A in Q4 2024 waited 774 days (about 2.1 years) since the prior round; 12 to 18 months of runway is a common target; plan for at least 24 to 30 months.
- [VEN (Venture Executive Network)](https://www.venexecs.com/?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library&utm_content=default-alive-default-dead). Founder sessions on runway and the board, 2026. Run the test monthly with hire dates in the model. Not a survey. No closed-session numbers.

## Related

- [Finance, metrics & runway](/library/finance/)
- [Runway calculator with hiring plan](/tools/runway-calculator/)
- [When runway runs out](/library/fundraising/when-runway-runs-out/)
- [Burn multiple vs Rule of 40](/library/finance/burn-multiple-vs-rule-of-40/)
- [How to tell the board you missed the plan](/library/board/missed-plan-reforecast/)
- [When to raise a Series A](/library/fundraising/when-to-raise-series-a/)
