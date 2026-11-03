---
title: "Burn multiple calculator: net burn ÷ net new ARR"
description: "Burn multiple = net burn ÷ net new ARR. $1.8M burned for $1.0M of new ARR is 1.8×, good on Sacks' bands. Enter yours and see what each band takes."
slug: burn-multiple-calculator
section: tools
cluster: finance
layout: calculator
calculator_js: burn-multiple-calculator.js
target_query: burn multiple calculator
date: 2026-11-03
close: A burn multiple that looks fine in the pack can fall apart on one question about churn or cash. Founders who have defended theirs in a raise or a board meeting will pressure-test your numbers in a VEN session.
disclaimer: not-legal-tax
draft: false
related:
- library/finance/burn-multiple-vs-rule-of-40
- tools/runway-calculator
- library/finance/default-alive-default-dead
- library/finance/usage-revenue-as-arr
- library/finance/nrr-vs-grr-board-pack
- tools/magic-number-cac-payback-calculator
- library/finance
---

Burn multiple is net burn divided by net new ARR. Burn $1.8M in a quarter to add $1.0M of ARR and you are at 1.8×, which David Sacks rates good. Under 1× is amazing. Over 3× is bad. Enter your net burn and your ARR at the start and end of the same period below. You get the multiple, the Sacks band, and what it takes to move up a band. Your numbers stay in this browser tab. Not legal or tax advice.

:::takeaways
- Burn multiple = net burn ÷ net new ARR (David Sacks, Craft Ventures, 23 April 2020). Lower is better.
- Sacks' bands: under **1×** amazing, **1× to 1.5×** great, **1.5× to 2×** good, **2× to 3×** suspect, over **3×** bad.
- Sacks' own board example: **$2M** burned to add **$1M** is **2×**, reasonable early. **$5M** burned to add **$1M** is **5×**, and he says that company should probably cut costs immediately.
- A seed company might run about **3×**. After a Series A it might drop to about **2×** (Sacks). Bessemer says early-stage companies with negative free cash flow should aim for about **1× to 1.5×**.
- Use the same period for burn and ARR. If net new ARR is zero or negative, the multiple does not compute.
:::

## What the calculator returns

:::highlight
The multiple, its Sacks band, and the net new ARR or net burn you need to reach each band.
:::

| Output | Formula | Source |
| --- | --- | --- |
| Net new ARR | ARR at end of period − ARR at start of period | Sacks (churn nets against the denominator) |
| Burn multiple | Net burn ÷ net new ARR | Sacks, 23 April 2020 |
| Band | Sacks' rules of thumb below. Each band includes its upper edge. Amazing stops under 1× | Sacks |
| Net new ARR needed at your burn | Net burn ÷ the band's upper edge | Arithmetic on Sacks' formula |
| Net burn you can carry | Band's upper edge × your net new ARR | Arithmetic on Sacks' formula |

Net burn is cash out minus cash in for the period (Kruze). The tool does not net a funding round against it. Net new ARR is what is left after churn and contraction come out of new and expansion ARR. The tool needs a positive net new ARR and positive net burn. Otherwise it tells you why the ratio does not apply.

## Sacks' bands and where stage fits

:::highlight
Sacks published five bands for venture-stage startups. He also said the multiple should improve as you mature.
:::

| Burn multiple | Sacks label |
| --- | --- |
| Under 1× | Amazing |
| 1× to 1.5× | Great |
| 1.5× to 2× | Good |
| 2× to 3× | Suspect |
| Over 3× | Bad |

Sacks calls them rules of thumb. His table is an image in the post, so you can check it against the original. He adds that a seed company might sit at about 3 because sales are only starting, and that it might drop to about 2 after the Series A. After a Series B, when the sales team should be operating at scale, he expects efficiency to improve even more. For a company to reach profit, the multiple has to approach 0. He gives no number for later stages.

Bessemer sets a different bar. For an early-stage company with negative free cash flow, it still looks for an attractive burn multiple, ideally about 1× to 1.5× (Rule of X, 2 January 2024). Its example: next-twelve-month growth of 100% with burn of 100% of revenue is about a 2× burn multiple. Growth of 150% with burn of 200% is about 3×. Both score a 100% Rule of X at a 2× growth multiplier, and Bessemer says most companies would choose the first.

Show each source on its own line. Do not average Sacks' 3× seed note with Bessemer's 1× to 1.5× target. There is no reliable public benchmark yet for a median burn multiple by stage.

## Four worked examples

:::highlight
Each one was worked by hand, then entered here. The first two are Sacks' own board numbers.
:::

Period is one quarter in every row.

| Example | Net burn | ARR start → end | Net new ARR | Burn multiple | Sacks band |
| --- | --- | --- | --- | --- | --- |
| 1. Sacks, reasonable | **$2.0M** | $4.0M → $5.0M | **$1.0M** | **2.00×** | Good (top edge) |
| 2. Sacks, terrible | **$5.0M** | $4.0M → $5.0M | **$1.0M** | **5.00×** | Bad |
| 3. Editorial, efficient | **$900k** | $2.0M → $2.75M | **$750k** | **1.20×** | Great |
| 4. Editorial, with churn | **$2.4M** | $6.0M → $7.5M | **$1.5M** | **1.60×** | Good |

Examples 1 and 2 use Sacks' burn and net new ARR from his Q1 board meeting. He gives no starting ARR, so $4.0M is ours. Neither example is a company. Example 4 shows the netting: **$1.8M** new plus **$0.4M** expansion, minus **$0.5M** churn and **$0.2M** contraction, is **$1.5M** net new. The ARR you started with is irrelevant to the ratio. Only the change counts.

Take example 4 to the "what it takes" table. At **$2.4M** of burn, moving to great (1.5×) needs **$1.6M** of net new ARR. At **$1.5M** of net new ARR, it needs net burn at or under **$2.25M**. Both are plain arithmetic on Sacks' formula.

## Get the two inputs right

:::highlight
Burn comes from the cash statement. Net new ARR comes from the ARR you would show a board.
:::

**Net burn.** Use cash, not the P&L (Kruze). Take the same months as the ARR change. A quarter of burn against a month of ARR change gives a number three times too high.

**Net new ARR.** Count new and expansion ARR, then take out churn and contraction. Usage above a commit and pilots belong on their own lines. [Does usage revenue count as ARR?](/library/finance/usage-revenue-as-arr/) walks the definition.

**What moves it.** Sacks calls the multiple a catch-all. A gross margin problem, weak sales efficiency, churn, stalled growth, and loose spending all show up in it. Read the two halves before you read the ratio. If net burn rose, look at costs. If net new ARR fell, look at churn and pipeline. Pair it with the [magic number and CAC payback calculator](/tools/magic-number-cac-payback-calculator/) when sales spend is the question.

If you are still deciding which efficiency number belongs in the pack, see [Burn multiple vs Rule of 40](/library/finance/burn-multiple-vs-rule-of-40/). If the cash itself is the worry, use the [runway calculator](/tools/runway-calculator/).

## Before you put it in the board pack

:::steps Burn multiple check
1. **Pick the period.** Use the quarter your board reviews. Run the prior quarters the same way.
2. **Pull net burn from cash.** Cash out minus cash in for those months. Leave financing out.
3. **Pull ARR at both ends.** Use one written ARR definition.
4. **Run it here.** Read the band, then read both halves.
5. **Show the trend.** Sacks says the multiple should improve as you mature. A rising multiple while headline growth rises is a warning.
6. **Show the inputs.** Put net burn and net new ARR on separate lines beside the ratio.
:::

## Mistakes

- Mixing periods. Quarterly burn against annual ARR change gives a wrong ratio.
- Netting a funding round against burn. That hides the real cash cost of growth.
- Counting gross new ARR as net new. Churn comes out of the denominator (Sacks).
- Quoting the multiple with zero net new ARR. It does not compute.
- Averaging Sacks' bands with another publisher's target. Show each by source.
- Reading one quarter as the trend. Show at least three.

## Sources

- [David Sacks, The Burn Multiple (Craft Ventures / Medium)](https://medium.com/craft-ventures/the-burn-multiple-51a7e43cb200). 23 April 2020. Formula; five-band table (under 1× amazing, 1× to 1.5× great, 1.5× to 2× good, 2× to 3× suspect, over 3× bad); **$2M** / **$1M** = **2×** and **$5M** / **$1M** = **5×** board examples; seed about 3, after Series A about 2; churn nets against the denominator; pre-revenue does not compute. The band table is an image in the post.
- [Bessemer Venture Partners, The Rule of X](https://www.bvp.com/atlas/the-rule-of-x). 2 January 2024. Early-stage venture and growth with negative free cash flow: attractive burn multiple, ideally about 1× to 1.5×. Company A about 2× and Company B about 3× on the same Rule of X.
- [Kruze Consulting, Build a Rolling Cash Forecast to Maximize Startup Runway](https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/). 22 February 2026. Net burn is cash out minus cash in; cash over P&L.
