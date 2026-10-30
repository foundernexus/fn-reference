---
title: "SAFE dilution calculator: ownership after SAFEs convert"
description: Model post-money SAFEs converting at a priced round. Enter each cap and discount, the pool increase, and the round to see founder, SAFE, investor, and pool %.
slug: safe-dilution-calculator
section: tools
cluster: equity
layout: calculator
calculator_js: safe-dilution-calculator.js
target_query: SAFE dilution calculator
date: 2026-10-30
close: SAFE math is easy to skip until the term sheet lands. Founders who have converted a stack of SAFEs at a priced round will pressure-test your caps, pool ask, and round size in a VEN session.
disclaimer: not-legal-tax
draft: false
related:
- library/fundraising/safe-vs-priced-round
- tools/option-pool-shuffle-calculator
- library/equity/option-pool-from-hiring-plan
- library/equity/founder-vesting-83b
- library/fundraising/term-sheet-red-flags
- library/fundraising/first-angel-check
- library/equity
---

Your SAFEs convert at the priced round, and the founders pay for most of it. Each post-money SAFE takes its amount divided by its cap of the company before the new money (Y Combinator). The pool increase the lead asks for sits in the pre-money. YC's guide leaves it out of the SAFE math, so it dilutes the founders and the SAFE holders but not the new investors. Enter your cap table, each SAFE, and the round below. You get every holder's percentage before and after. Not legal or tax advice.

:::takeaways
- A post-money SAFE sells amount ÷ cap. YC's example: **$200k** at a **$4M** cap is **5%**, and **$800k** at **$8M** is **10%**, so **15%** is sold before the round.
- SAFEs do not dilute each other. The round's new money and its pool increase dilute everyone already on the table, SAFE holders included (YC).
- In YC's worked example, founders go from **92.5%** to **51.54%** after **$1M** of SAFEs and a **$5M** round at **$15M** pre with a **10%** pool.
- If the round prices below a SAFE's cap, the cap stops mattering. The SAFE converts at the round price or its discount, whichever gives more shares (YC; Carta).
- Run every SAFE you have signed before you sign the next one. Your numbers stay in this browser tab.
:::

## What the calculator returns

:::highlight
Ownership before and after for every holder, the round price, the pool increase, and how each SAFE converted.
:::

| Output | Formula | Source |
| --- | --- | --- |
| Company Capitalization (K) | Today's fully diluted shares + all SAFE conversion shares. Excludes new money and the round's pool increase | YC post-money safe user guide |
| SAFE cap price | Post-money cap ÷ K | YC |
| SAFE discount price | Round price × (1 − discount) | YC; Carta |
| SAFE conversion price | Lowest of cap price, discount price, and round price | YC; Carta |
| Pool increase | Target % × post-round shares − unissued pool today | YC worked example |
| Round price per share | Pre-money ÷ (K + pool increase) | YC worked example |
| New investor % | New money ÷ (pre-money + new money) | YC |

The tool solves for the round price and the SAFE shares together, because a discount SAFE's shares depend on the round price and the round price depends on the shares. It assumes YC post-money SAFEs, no notes, and no promised options above the unissued pool. If an investor has a pro rata side letter, put that money inside new money.

## Three worked examples

:::highlight
Each example was solved by hand and by a separate script, then run in this calculator. The first two are YC's published numbers.
:::

All three start from **10,000,000** fully diluted shares.

| Example | Inputs | Founders after | SAFE holders after | New investors | Pool |
| --- | --- | --- | --- | --- | --- |
| 1. YC, round above the caps | Founders **92.5%**, unissued pool **1%**. SAFEs **$200k** at **$4M** and **$800k** at **$8M**. **$5M** at **$15M** pre, **10%** pool | **51.54%** | **3.28%** and **6.56%** | **25.00%** | **10.00%** |
| 2. YC, round below one cap | Same SAFEs. **$2.2M** at **$8.8M** pre, **10%** pool | **55.31%** (YC rounds to 55.32%) | **3.53%** (cap) and **7.27%** (round price) | **20.00%** | **10.00%** |
| 3. Editorial, discount SAFEs | Founders **90%**, pool **10%**. **$1M** at **$20M** cap with **20%** discount and **$500k** discount-only at **20%**. **$3M** at **$12M** pre, **15%** pool | **52.50%** | **8.33%** and **4.17%** | **20.00%** | **15.00%** |

Examples 1 and 2 come from Appendix II of YC's post-money safe user guide. In example 1, YC's table shows the **$800k** investor at **9.06%** because it also buys its pro rata in the round. The **6.56%** here is its SAFE shares alone. Example 2 shows the cap turning off. The **$8M** cap works out to about **$0.68** a share, above the **$0.6577** round price, so that SAFE converts at the round price and ends up with more than the **10%** its cap implied (YC). Example 3 is not a company. The round price is **$0.875**, both SAFEs convert at **$0.70**, and the **$20M** cap never binds.

## Why the pool increase lands on founders

:::highlight
The lead prices its shares after a full pool. The SAFEs price theirs before the increase. Founders sit under both.
:::

YC counts the unissued pool that exists before the round in the SAFE math, and leaves out the increase the round asks for. YC's reasoning: putting the Series A increase in the SAFE math would make founders bear two rounds of hiring dilution by themselves. The lead's term sheet usually puts the increase in the pre-money, so the new money does not pay for it either.

Two levers are left. Size the pool from a hiring plan, not a round number. [Size the option pool from a hiring plan](/library/equity/option-pool-from-hiring-plan/) walks the seats. Then see who pays for the top-up in the [option pool shuffle calculator](/tools/option-pool-shuffle-calculator/). Each point of pool you avoid stays with the founders and the SAFE holders.

## Cap, discount, or both

:::highlight
The SAFE holder gets the better of the two. Model both before you agree to both.
:::

YC's standard post-money SAFE has a cap and no discount. YC also posts a discount-only version and an uncapped MFN version. It pulled the cap-and-discount form on 28 August 2021, saying it had not seen cases where that form was the better choice. Carta reports that nearly a third of SAFEs still carry both. A discount only matters when the round prices close to or below the cap. Example 3 shows that case. Carta: **91%** of SAFEs on its platform were post-money as of Q2 2026. This tool does not model pre-money SAFEs or uncapped MFN SAFEs.

If you are still choosing the instrument, start with [SAFE vs priced round](/library/fundraising/safe-vs-priced-round/).

## Before you sign the next SAFE

:::steps SAFE check
1. **List every SAFE.** Amount, cap, discount, and side letters. Include the ones from friends and family.
2. **Add up amount ÷ cap.** That is the percentage you have sold before the round (YC).
3. **Pick a likely round.** Use a pre-money and raise you could defend, plus the pool size the lead will ask for.
4. **Run it here.** Read the founders' line after the round, not the SAFE line.
5. **Run a down case.** Drop the pre-money below your lowest cap and see which SAFEs switch to the round price.
6. **Check founder vesting terms.** A lead can ask you to re-vest at the same close. See [founder vesting at a priced round](/library/equity/founder-vesting-83b/).
7. **Confirm with counsel.** Bring this output and your cap table software export. Not legal or tax advice.
:::

## Mistakes

- Reading a SAFE's cap as the company's price. A cap is a ceiling. The round can price below it (YC).
- Treating SAFE ownership as final. YC: the SAFE percentage is post-SAFEs, not post-round. The round dilutes it.
- Leaving the lead's pool increase out of your model. It comes out of founders and SAFE holders.
- Adding a discount to a SAFE that already has a low cap without modeling a down round.
- Counting a pro rata purchase as SAFE ownership. It is new money in the round.

## Sources

- [Y Combinator, Post-Money Safe User Guide (PDF)](https://bookface-static.ycombinator.com/assets/ycdc/SAFE%20User%20Guide-a47c6588327d73aa2799e61ed7c2cae9f1a0ee9acfa9c43b62039dc06e715832.pdf). Version 1.2, February 2023. Ownership sold = amount ÷ post-money cap; Company Capitalization includes the existing unissued pool and converting securities and excludes the round's pool increase and new money; conversion at the better of Safe Price and round price; cap-and-discount version removed 28 August 2021; Appendix II Example 1 questions 2 and 5 (**$200k** at **$4M**, **$800k** at **$8M**; **$5M** at **$15M** pre; **$2.2M** at **$8.8M** pre; **10%** pool; founders **51.54%** and **55.32%**).
- [Y Combinator, SAFE financing documents](https://www.ycombinator.com/documents.html). Current post-money versions: cap no discount, discount no cap, uncapped MFN.
- [Carta, Understanding the SAFE](https://carta.com/learn/startups/fundraising/convertible-securities/safes/). 8 October 2026. Cap and discount definitions; the investor takes the better term; nearly a third of SAFEs carry both a cap and a discount.
- [Carta, Pre-money vs. post-money SAFEs](https://carta.com/learn/startups/fundraising/convertible-securities/pre-money-vs-post-money-safes/). 7 October 2026. Post-money SAFEs do not dilute each other; **91%** of SAFEs on Carta were post-money as of Q2 2026.
- [VEN (Venture Executive Network)](https://www.venexecs.com/?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library&utm_content=safe-dilution-calculator). Founder sessions on SAFEs, priced rounds, and founder dilution at Series A, 2026. Session topics only. No closed-session numbers.
