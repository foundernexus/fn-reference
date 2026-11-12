---
title: "Pre-money vs post-money valuation: the math founders miss"
description: "Post-money is pre-money plus new money; the investor owns check ÷ post-money. A 10% pool in the pre-money cuts a $12M headline to $10.5M for existing holders."
slug: pre-money-vs-post-money
section: library
cluster: fundraising
layout: article
target_query: pre-money vs post-money valuation
date: 2026-11-12
close: Founders who have negotiated a pool increase or converted a stack of SAFEs at a priced round will pressure-test your pro forma cap table and effective valuation in a VEN session.
disclaimer: not-legal-tax
ven_playbook: concepts/pre-money-vs-post-money
ven_playbook_label: VEN playbook note on pre-money vs post-money
draft: false
related:
- library/fundraising
- tools/option-pool-shuffle-calculator
- tools/safe-dilution-calculator
- library/fundraising/safe-vs-priced-round
- library/fundraising/term-sheet-red-flags
- library/equity/option-pool-from-hiring-plan
---

Pre-money valuation is what the company is worth right before the new money arrives. Post-money is pre-money plus the new money. The investor's stake is the check divided by the post-money: **$2 million** on a **$10 million** pre-money is a **$12 million** post-money (Y Combinator), so the investor owns about **16.7%**. The formula is easy. The fight is over which shares sit inside the pre-money. Term sheets usually count the option pool increase there (Carta), and converting SAFEs too unless you negotiate otherwise (Y Combinator). Each one lowers the price you get per share. In Q2 2026 the median seed pre-money in Wilson Sonsini's deals was **$23.0 million** and the median Series A was **$80.0 million**. Not legal or tax advice.

:::takeaways
- Post-money = pre-money + new money. Investor ownership = investment ÷ post-money. Price per share = pre-money ÷ fully diluted pre-money shares.
- A pool increase counted in the pre-money dilutes only existing holders. In Venture Hacks' example, a **20%** pool turns an **$8 million** pre-money into **$6 million** of effective value.
- A post-money SAFE cap is "post" all SAFE money and the existing pool. It is not "post" the priced round or its new pool, so SAFE holders get diluted at the Series A (Y Combinator).
- **89%** of capped SAFEs in Wilson Sonsini's H1 2026 deals used a post-money cap. On Carta, **91%** of SAFEs were post-money in Q2 2026.
- Compare offers on your ownership after close and the effective pre-money. The headline number hides both.
:::

This page covers the valuation math and the terms that move it. To model a pool increase, use the [option pool shuffle calculator](/tools/option-pool-shuffle-calculator/). To model SAFEs converting, use the [SAFE dilution calculator](/tools/safe-dilution-calculator/). To choose the instrument in the first place, read [SAFE vs priced round](/library/fundraising/safe-vs-priced-round/).

## The formulas

:::highlight
The valuation math needs three numbers: the pre-money, the new money, and the fully diluted share count before the round.
:::

| You want | Formula | Source |
| --- | --- | --- |
| Post-money valuation | Pre-money + new money | Y Combinator |
| Investor ownership | Investment ÷ post-money | Y Combinator |
| Price per share | Pre-money ÷ fully diluted pre-money shares | Venture Hacks |
| New shares issued | Investment ÷ price per share | Venture Hacks |
| Ownership sold on a post-money SAFE | Investment ÷ post-money valuation cap | Y Combinator |

### Labeled example: a $3 million seed round

Editorial arithmetic. Not a company.

A lead offers **$3 million** at a **$12 million** pre-money. The post-money is **$15 million** and the lead owns **20%**. If the company has **10,000,000** fully diluted shares before the round, the price is **$1.20** a share and the lead gets **2,500,000** new shares, for **12,500,000** total.

Now read the fine print. The term sheet asks for a **10%** unallocated pool after the round, counted in the pre-money.

| Line | No pool increase | 10% pool in the pre-money |
| --- | --- | --- |
| Headline pre-money | **$12.0M** | **$12.0M** |
| New pool shares | 0 | **1,250,000** |
| Existing holders' shares | 10,000,000 | **8,750,000** |
| Effective pre-money for existing holders | **$12.0M** | **$10.5M** |
| Existing holders after close | **80%** | **70%** |
| Lead after close | **20%** | **20%** |

The lead's stake does not move. The pool comes out of the existing holders, and founders hold most of those shares. The **$1.5 million** gap is the price of the pool.

## What the pre-money includes

Ask counsel for the fully diluted pre-money share count and a list of what is in it. These are the usual lines.

| Item | In the pre-money? | Who it dilutes | Source |
| --- | --- | --- | --- |
| Founder and employee shares, granted options | Yes | All holders before the round | Venture Hacks |
| Unallocated pool and any pool increase required by the term sheet | Yes; the investor sets a target pool percentage as a pricing term | Existing holders | Carta |
| SAFEs and notes converting in the round | Yes, unless the parties agree to leave them out | Existing holders | Y Combinator |
| The new investors' money | No | No one; it creates the post-money | Y Combinator |

Leaving SAFEs out of the pre-money changes who pays for them. In Y Combinator's example, a **$10 million** Series A at a **$40 million** pre-money would buy **20%**. If the parties keep **$1 million** of SAFEs at a **$10 million** post-money cap outside the pre-money, the new money gets a bit less than **20%** and the effective post-money is above **$50 million**.

## The option pool shuffle

Venture Hacks named it in 2007. A company with **6,000,000** shares takes **$2 million** on an **$8 million** pre-money. The investor asks for a **20%** pool after the round, inside the pre-money. That means **2,000,000** new options, so the price falls from **$1.33** to **$1.00** a share and the effective value of what you built is **$6 million**. Cutting the pool to **10%** from a hiring plan raised the price **17%**, to **$1.17**.

Carta gives the same mechanics with a **$10 million** pre-money and a pool going from **5%** to **15%**: the **10%** increase comes out of existing holders.

How big should the pool be? Carta cites HSBC Innovation Banking's 2026 Term Sheet Guide: most pools run **10–15%** of the company, and **10%** is the most frequent. Carta's advice is to size it from the hires you plan for the next **12–18** months. Build that list with [option pool from the hiring plan](/library/equity/option-pool-from-hiring-plan/) before you negotiate.

## SAFEs: post-money cap, pre-money round

The post-money SAFE made early ownership easy to read. Divide the check by the cap. Y Combinator's guide: to sell **15%** for **$1 million**, set a post-money cap of about **$6.7 million**.

The word "post" has limits. The cap is post all SAFE money and the pool that existed before the priced round. It is not post the Series A money or the new pool the Series A adds (Y Combinator). Post-money SAFEs do not dilute each other; pre-money SAFEs do (Carta). Both get diluted by the priced round.

In Y Combinator's worked example, SAFE investors buy **15%** for **$750,000** on a **$5 million** post-money cap. The Series A sells **25%** to new investors, plus SAFE pro rata, and adds a **10%** pool. The SAFE holders end at about **9.09%**.

| Measure | Figure | Source |
| --- | --- | --- |
| Capped SAFEs using a post-money cap, H1 2026 | **89%** (from **81%** in 2025) | Wilson Sonsini |
| SAFEs with a valuation cap, H1 2026 | **85%** (from **93%** in 2025) | Wilson Sonsini |
| Median SAFE valuation cap, H1 2026 | **$15.0M** (from **$20.0M** in 2025) | Wilson Sonsini |
| SAFEs on Carta that were post-money, Q2 2026 | **91%**, up from around **43%** at the start of the decade | Carta |

Keep a running ownership total if your cap table mixes pre-money and post-money SAFEs. The [SAFE dilution calculator](/tools/safe-dilution-calculator/) does the conversion math.

## What the market pays

| Measure | Seed | Series A | Source |
| --- | --- | --- | --- |
| Median pre-money valuation, Q2 2026 | **$23.0M** | **$80.0M** | Wilson Sonsini (its own deals) |
| Median post-money valuation, Q2 2026 | **$23.9M** | **$76.3M** | Carta Round Benchmarking Tool |
| Median round size, Q2 2026 | **$4.5M** | **$14.7M** | Carta |
| Median dilution in the round, Q2 2026 | **19.4%** | **18.7%** | Carta |
| Founding team ownership after the round | about **56%** | about **36%** | Carta Founder Ownership Report 2026 |

Read these as two datasets. Wilson Sonsini reports pre-money from deals its lawyers worked. Carta reports post-money from companies on its cap table software. Do not subtract one from the other. Carta calculates each of its medians on its own, too: **$4.5 million** ÷ **$23.9 million** is **18.8%**, while its median seed dilution is **19.4%**. Wilson Sonsini's seed median fell from **$35.0 million** in Q1 2026, which shows how much a quarter can move.

There is no reliable public benchmark yet for the effective pre-money after the pool increase and SAFE conversion at Seed to Series A. Headline medians include both.

## How to read the valuation in a term sheet

:::steps Valuation check
1. **Confirm in writing** whether the number is pre-money or post-money.
2. **Get the fully diluted pre-money share count** and the list of what it includes.
3. **Find the target pool** and whether it sits in the pre-money (Carta). Answer with a hiring plan.
4. **List every SAFE and note** with its cap, discount, and type, then model conversion.
5. **Compute the price per share**: pre-money ÷ fully diluted pre-money shares.
6. **Compute the effective pre-money**: headline pre-money minus the value of the new pool, and of any SAFE or note shares counted in it.
7. **Compare offers on founder ownership after close.** A higher headline with a bigger pool can leave you with less.
8. **Check the long-form documents** against your pro forma cap table before you sign.
:::

The VEN session judgment lines up with steps 1 and 8: confirm pre-money or post-money in writing first, then build the pro forma cap table and check the long-form documents against it. That is session judgment, not a survey.

## Where founders get this wrong

**Reading a post-money number as pre-money.** On a **$3 million** raise, "$15 million post" and "$15 million pre" differ by **$3 million** of value and about **3.3** points of ownership.

**Treating the pool as the investor's problem.** Counted in the pre-money, the pool dilutes only existing holders (Carta).

**Assuming a post-money SAFE is immune at the Series A.** It is post the SAFE money, not the priced round or its new pool (Y Combinator).

**Anchoring on a median.** Wilson Sonsini's seed median swung from **$35.0 million** to **$23.0 million** in one quarter. Investors price your round on your numbers.

**Chasing the headline.** On a **$3 million** raise, a **$14 million** pre-money with a **15%** post-round pool leaves existing holders **67.4%**. A **$12 million** pre-money with a **10%** pool leaves them **70%**. Editorial arithmetic; model both offers.

## Pair this with

- [Option pool shuffle calculator](/tools/option-pool-shuffle-calculator/) to see who pays for a pool top-up.
- [SAFE dilution calculator](/tools/safe-dilution-calculator/) to convert a SAFE stack at the priced round.
- [Term sheet red flags](/library/fundraising/term-sheet-red-flags/) for the terms after price.
- [Option pool from the hiring plan](/library/equity/option-pool-from-hiring-plan/) to size the pool you will defend.

## Sources

- [Y Combinator, Post-Money Safe User Guide (PDF)](https://bookface-static.ycombinator.com/assets/ycdc/SAFE%20User%20Guide-a47c6588327d73aa2799e61ed7c2cae9f1a0ee9acfa9c43b62039dc06e715832.pdf). Version 1.2, February 2023. Pre-money vs post-money definitions ($2 million on $10 million pre-money = $12 million post-money); ownership sold = amount ÷ post-money cap ($1 million / 15% ≈ $6.7 million); cap is post all SAFE money and the existing pool, not post the equity financing or its new pool; worked example ($750,000 at $5 million cap = 15%; 25% new investors, 10% pool → 9.09%); footnote example ($10 million at $40 million pre-money with $1 million SAFEs left out → effective post-money above $50 million).
- [Carta, Pre-money vs. post-money SAFEs](https://carta.com/learn/startups/fundraising/convertible-securities/pre-money-vs-post-money-safes/). 7 October 2026. Post-money SAFE investors are not diluted by other SAFEs; pre-money SAFEs dilute each other; 91% of SAFEs on Carta post-money as of Q2 2026, up from around 43% at the start of the decade.
- [Carta, Option pools](https://carta.com/learn/startups/equity-management/option-pool/). 20 August 2026. Target pool percentage is a core pricing term and the increase is typically counted in the pre-money shares; $10 million pre-money with a pool going from 5% to 15%; HSBC Innovation Banking 2026 Term Sheet Guide: most pools 10–15%, 10% most frequent; size from a 12–18 month hiring plan.
- [Carta, Series A funding: How to raise your first priced round](https://carta.com/learn/startups/fundraising/series-a/). 7 October 2026. Round Benchmarking Tool, Q2 2026 medians: post-money $23.9 million (seed) and $76.3 million (Series A); round size $4.5 million and $14.7 million; dilution 19.4% and 18.7%. Founder Ownership Report 2026: founding teams about 56% after seed and about 36% after Series A.
- [Wilson Sonsini, The Entrepreneurs Report: Q2 2026 (PDF)](https://www.wsgr.com/a/web/ntbxCfmspTLoevehaAoUgh/entrepreneurs-report-q2-2026.pdf). Median pre-money valuation from Wilson Sonsini deals: seed $23.0 million (from $35.0 million in Q1 2026), Series A $80.0 million. SAFE terms, H1 2026: 85% capped (93% in 2025); median cap $15.0 million ($20.0 million in 2025); 89% of capped SAFEs post-money (81% in 2025).
- [Venture Hacks, The Option Pool Shuffle](https://venturehacks.com/option-pool-shuffle). Nivi, 10 April 2007. $2 million on $8 million pre-money, 6 million existing shares, 20% post-money pool → $6 million effective valuation and $1.00 vs $1.33 a share; 10% pool → $7 million effective and $1.17 a share (17% higher).
- [VEN (Venture Executive Network)](https://www.venexecs.com/?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library&utm_content=pre-money-vs-post-money). Session judgment on term sheets, 2026: confirm pre-money or post-money in writing first; build the pro forma cap table and check the long-form documents against it. Not a survey. No closed-session numbers.

## Related

- [Fundraising](/library/fundraising/)
