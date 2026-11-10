---
title: "Cap table waterfall calculator: who gets paid at exit"
description: "Preferred takes its preference first, then common splits the rest. Enter the sale price and each series' terms to see every holder's payout and $ per share."
slug: cap-table-waterfall
section: tools
cluster: equity
layout: calculator
calculator_js: cap-table-waterfall.js
target_query: cap table waterfall calculator
date: 2026-11-10
close: The waterfall is where a clean-looking term sheet shows its cost. Founders who have run one before a sale or a new round will pressure-test your preference stack and exit math in a VEN session.
disclaimer: not-legal-tax
draft: false
related:
- library/fundraising/term-sheet-red-flags
- tools/safe-dilution-calculator
- library/fundraising/safe-vs-priced-round
- tools/option-pool-shuffle-calculator
- library/equity/option-pool-from-hiring-plan
- library/fundraising/how-to-sell-a-startup
- library/equity/qsbs
- library/equity
---

In a sale, preferred stock gets paid first. Each series takes its liquidation preference, most often 1x what it invested, or converts to common if that pays more. Common and options split what is left. A $25M sale with a $9M Series A and a $2M Seed leaves founders with 43% of the money for 50% of the shares. Enter your sale price, your common and option shares, and each preferred series below. You get every holder's payout, $ per share, and share of the proceeds. Your numbers stay in this browser tab. Not legal or tax advice.

:::takeaways
- Non-participating preferred takes the greater of its preference or its as-converted share. Never both (Feld).
- 1x non-participating is the norm. Cooley counted a **1x** preference in **95.8%** and nonparticipating preferred in **96.4%** of its Q2 2026 deals.
- Below the conversion point, a 1x non-participating series takes its money back and common shares the rest. Above it, all holders get the same amount per share.
- Stacked preferences pay the newest series first. Wilson Sonsini saw senior preferences in **16%** of Series B and later deals in 1H 2026 and pari passu in **84%**.
- A participation cap counts the preference. A **3x** cap is 3x in total, not 3x on top (Feld).
:::

## What the calculator returns

:::highlight
Each holder's payout, $ per share, % of proceeds, % owned, and which term each series used.
:::

| Output | Formula | Source |
| --- | --- | --- |
| Preference owed | Multiple × amount invested, for each series that does not convert | Feld |
| Stacked | Newest series paid in full first, then the next newest | Feld |
| Pari passu | All series share pro rata to what each is owed | Feld |
| Residual per share | What is left ÷ shares of common, options, converted series, and participating series | Feld |
| Participation cap | Preference + participation stops at cap × amount invested. The excess goes to the others | Feld |
| Conversion | Each series takes the greater of its preference path or its as-converted share | Feld; NVCA model charter |
| Founders | Founder shares × residual per share | Arithmetic |

Conversion choices interact. When one series converts, its preference leaves the stack, and its shares join common. That changes what common is worth to the other series. The tool lets each series pick its better option given the others' picks. It repeats until no series wants to switch. It also reruns your terms at a quarter, half, double, and four times your exit, so you can see the shape of the curve.

It assumes 1:1 conversion, no dividends, and an exit value net of debt, fees, escrow, and any management carve-out. Options count as common with exercise prices ignored, which slightly overstates what option holders take.

## Five worked examples

:::highlight
We worked each one by hand, then ran it here. None is a company.
:::

Examples 1 to 3 use founders at **7,000,000** shares, **1,000,000** options, and a Series A of **2,000,000** shares that invested **$10M**. The A owns **20%**. Examples 4 and 5 use founders at **6,000,000**, **1,000,000** options, and three 1x non-participating series: Seed **2,000,000** shares for **$2M**, A **3,000,000** for **$9M**, B **2,000,000** for **$16M**.

| Example | Terms and exit | Preferred takes | Common per share | Founders take |
| --- | --- | --- | --- | --- |
| 1. Below the conversion point | A 1x non-participating. **$30M** sale | A **$10M** preference | **$2.50** | **$17.5M** (**58.33%**) |
| 2. Above the conversion point | Same. **$80M** sale | A converts, **$16M** | **$8.00** | **$56M** (**70.00%**) |
| 3. Participating, 3x cap | A participating, capped at **3x**. **$120M** sale | A **$30M**, at the cap | **$11.25** | **$78.75M** (**65.63%**) |
| 4. Stacked, small sale | Stacked. **$20M** sale | B **$16M**, A **$4M**, Seed **$0** | **$0.00** | **$0** |
| 5. Conversions interact | Stacked. **$100M** sale | B **$16M** preference. A **$21M** and Seed **$14M** convert | **$7.00** | **$42M** (**42.00%**) |

**Example 1.** As common, the A would get 20% of **$30M**, or **$6M**. Its **$10M** preference pays more, so it keeps it. The other **$20M** goes to **8,000,000** common and option shares. The A converts once 20% of the sale beats **$10M**, so above **$50M**.

**Example 2.** At **$80M**, 20% is **$16M**, more than **$10M**. The A converts and every share gets **$8.00**.

**Example 3.** The A takes **$10M**, then shares the other **$110M** as if it held common: 20% is **$22M**, for **$32M** total. The cap stops it at **$30M**. The extra **$2M** goes to common, so **$90M** across **8,000,000** shares is **$11.25**. Converting would pay the A **$24M**, so it stays under the cap. At **$80M** the same A takes **$24M** (**$10M** plus 20% of **$70M**) and founders take **$49M**.

**Example 4.** The B goes first and takes its full **$16M** preference. The A gets the last **$4M** of its **$9M**. Seed and common get nothing. Pari passu on the same **$20M**, each series gets 20 ÷ 27 of what it is owed: B **$11.85M**, A **$6.67M**, Seed **$1.48M**. Common still gets nothing.

**Example 5.** If all three converted, each of **14,000,000** shares would get **$7.14**. That pays the B **$14.3M**, less than its **$16M** preference, so the B keeps it. The other **$84M** across **12,000,000** shares is **$7.00**. At **$7.00** the A takes **$21M** against a **$9M** preference and the Seed **$14M** against **$2M**, so both convert. The B's choice set the price the other two compared against.

## Where the market sits

:::highlight
Read each sample on its own. They count different deals over different periods.
:::

| Term | Cooley, Q2 2026 (**166** deals) | Wilson Sonsini, 1H 2026 |
| --- | --- | --- |
| 1x liquidation preference | **95.8%** | Not reported |
| Nonparticipating preferred | **96.4%** | **97%** (all rounds) |
| Participating, capped | Not reported | **1%** (all rounds) |
| Participating, no cap | Not reported | **2%** (all rounds) |
| Senior to earlier series | Not reported | **16%** (Series B and later) |
| Pari passu with earlier series | Not reported | **84%** (Series B and later) |

Carta saw participating preferred in more than **10%** of new primary rounds in Q1 2023, and less than half that rate by Q4 2024. YC's clean Series A term sheet uses 1x non-participating and calls a higher multiple or participation a dirty term. There is no reliable public benchmark yet for the size of participation caps or for the share of Seed and Series A deals that stack.

The defaults here are 1x non-participating and pari passu. Change the terms to match your charter, not the market.

## Read the stack before you sign the next round

:::highlight
The waterfall decides who gets paid in a sale. Run it at several exit values before you argue about terms.
:::

Brad Feld calls the liquidation preference the second most important economic term after price. Cooley GO's Matthew Bartus says to model the exit values you expect, so the dollar gap between preference terms shows. Two things push founders to zero faster than the headline percentage suggests.

**The stack grows with each round.** Each series adds its preference on top. In example 4, **$27M** of preferences against a **$20M** sale leaves common with nothing, though common owns half the company. When you raise, compare the total stack with the exit you can see in the next few years.

**Senior new money moves the risk onto older investors and common.** Stacked seniority does not change who converts at a high price. It changes who gets paid at a low one. If a term sheet asks for seniority, run the low case both ways. [Term sheet red flags](/library/fundraising/term-sheet-red-flags/) walks the clean term for each line.

Your SAFEs also join this table once they convert. Run the [SAFE dilution calculator](/tools/safe-dilution-calculator/) first, then enter the new share counts here. If the pool top-up is still open, the [option pool shuffle calculator](/tools/option-pool-shuffle-calculator/) shows who pays for it. If a sale is the real question, [how to sell a startup](/library/fundraising/how-to-sell-a-startup/) covers the process.

## Before you sign a term sheet or an LOI

:::steps Waterfall check
1. **Pull the charter terms.** For each series: shares, amount invested, preference multiple, participation, cap, and seniority. Your charter is the source, not your memory of the term sheet.
2. **Enter the cap table.** Founder shares, other common, granted options, and each series oldest first.
3. **Pick three exit values.** A low case near the total stack, the price you hope for, and a high case.
4. **Read the founders' line.** Compare % of proceeds with % owned. The gap is what the preferences cost you at that price.
5. **Run the new term both ways.** Participating versus not, stacked versus pari passu, at the low case.
6. **Net the exit value.** Take out debt, fees, escrow, and any carve-out before you enter it.
7. **Confirm with counsel.** Bring this output and your cap table export. Not legal or tax advice.
:::

## Mistakes

- Reading ownership as payout. Below the conversion point, common takes less than its percentage.
- Counting a 3x cap as 3x on top of the preference. It is 3x in total (Feld).
- Assuming every series converts together. Each series makes its own call, and the calls depend on each other.
- Entering the headline price. Debt, fees, and escrow come out first.
- Modeling one exit value. The waterfall bends, so run several.
- Counting the unissued pool. Unissued options get nothing in a sale.

## Sources

- [Brad Feld, Term Sheet: Liquidation Preference (Feld Thoughts)](https://feld.com/archives/2005/01/term-sheet-liquidation-preference/). 4 January 2005. Second most important economic term after price; full, capped, and non-participating; a cap counts the preference (a 3x cap is an additional 2x after a 1x preference); stacked vs pari passu; investors take the preference or the as-converted amount, not both.
- [Cooley, Q2 2026 Venture Financing Report](https://www.cooley.com/news/insight/2026/2026-08-17-q2-2026-venture-financing-report). 17 August 2026. **166** financings; **95.8%** 1x liquidation preference; **96.4%** nonparticipating.
- [Wilson Sonsini, The Entrepreneurs Report: Q2 2026](https://www.wsgr.com/a/web/ntbxCfmspTLoevehaAoUgh/entrepreneurs-report-q2-2026.pdf). Deal-terms appendix, 1H 2026. All rounds: non-participating **97%**, participating capped **1%**, uncapped **2%**. Series B and later: senior **16%**, pari passu **84%**.
- [Carta, State of Private Markets: Q4 and 2024 in review](https://carta.com/data/state-of-private-markets-q4-2024/). 12 February 2025. Participating preferred in more than **10%** of new primary rounds in Q1 2023; less than half that rate by Q4 2024.
- [Y Combinator, A Standard and Clean Series A Term Sheet](https://www.ycombinator.com/series_a_term_sheet). 1x non-participating preference; a higher multiple and participation listed as dirty terms.
- [Cooley GO, Negotiating Term Sheets: Focus on What's Important](https://www.cooleygo.com/negotiating-term-sheets/). Matthew Bartus. Model expected exit values to see the dollar gap between preference terms.
- [NVCA, Model Legal Documents](https://nvca.org/model-legal-documents/). Model charter: liquidation preference, participation, and deemed liquidation event language.
- [VEN (Venture Executive Network)](https://www.venexecs.com/?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library&utm_content=cap-table-waterfall). Founder sessions on term sheets, preferred stock, and liquidation preferences, 2026. Session topics only. No closed-session numbers.
