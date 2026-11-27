---
title: "Venture debt calculator: true cost, warrants, and dilution"
description: "A $5M venture loan at 12% with a 1% fee and a 5% final payment costs about 15.4% a year in cash. Add warrants and compare the dilution with equity."
slug: venture-debt-calculator
section: tools
cluster: fundraising
layout: calculator
calculator_js: venture-debt-calculator.js
target_query: venture debt cost calculator
date: 2026-11-27
close: A loan that prices well in a spreadsheet can still hurt in the quarter you miss plan. Founders who have drawn and repaid venture debt will pressure-test your draw month, warrant terms, and lender shortlist in a VEN session.
disclaimer: not-legal-tax
draft: false
related:
- library/fundraising/venture-debt
- tools/runway-calculator
- tools/burn-multiple-calculator
- tools/safe-dilution-calculator
- library/fundraising/when-runway-runs-out
- library/fundraising/term-sheet-red-flags
- library/fundraising/pre-money-vs-post-money
- library/fundraising
---

Venture debt costs more than its headline rate. You pay interest, an upfront fee, a final payment at maturity, and warrants. Take a $5M loan at 12% with 12 months interest-only, 24 months of amortization, a 1% fee, and a 5% final payment. Its cash cost is about **15.4%** a year. A 5% warrant that triples by exit lifts the all-in cost to about **18.2%**, and it takes **0.50%** of the company. Raising the same $5M as equity at a $50M pre-money takes **9.09%**. Those figures come from the calculator below on labeled hypothetical inputs. Enter your term sheet and see your payments, both annual costs, and the ownership trade. Your numbers stay in this browser tab. Not legal or tax advice.

:::takeaways
- Price the loan as cash flows. You receive the loan minus the fee, then pay interest, principal, and the final payment. The calculator solves for the annual rate that sets those to zero.
- Warrant shares = coverage × loan ÷ strike. Codexis' November 2026 loan with Trinity Capital uses that formula at **3.0%** coverage and **$1.08** a share.
- Published warrant coverage runs **2–10%** of the loan (Kruze) and **3–20%** at Hercules Capital, with the strike usually at the latest round price (Hercules 10-K).
- Kruze: warrant dilution is usually under **1%** of the cap table. An equity round dilutes **10–30%**.
- Keep peak debt service under **25%** of monthly net burn (SVB). Draw late, with about **3–6** months of runway left, if the term sheet lets you (Kruze).
:::

## What the calculator returns

:::highlight
Payments by phase, the cash cost in dollars and as an annual rate, the warrant's value and ownership, and the same money raised as equity.
:::

| Output | Formula | Source |
| --- | --- | --- |
| Interest-only payment | Loan × annual rate ÷ 12 | Arithmetic |
| Amortizing payment | Equal payments: loan × i ÷ (1 − (1 + i)^−n). Straight-line: loan ÷ n of principal plus interest on the balance | Arithmetic; Mercury's 12/36 example uses straight-line |
| Total cash cost | All payments + upfront fee + final payment − loan | Arithmetic |
| Effective annual cost, cash | (1 + monthly IRR)^12 − 1 on loan minus fee in, payments and final payment out | Arithmetic |
| Warrant shares | Coverage × loan ÷ strike | Codexis 8-K, 5 November 2026 |
| Warrant value | Shares × (exit price − strike), floored at zero, in the exit month | Our assumption; the exit price is yours |
| All-in annual cost | The cash IRR with the warrant value added as a payment in the exit month | Arithmetic |
| Ownership via warrants | Warrant shares ÷ (fully diluted shares + warrant shares) | Arithmetic |
| Ownership via equity | New money ÷ (pre-money + new money) | Arithmetic |
| Burn check | Peak monthly debt service ÷ monthly net burn, against SVB's 25% | SVB, 22 September 2023 |

The tool assumes a fixed rate, a full draw on day one, no prepayment, and a warrant fully vested at funding. Most venture loans float with prime. Hercules reported **97.9%** of its debt at floating rates or floating with a floor at the end of 2025. Rerun the calculator at a higher rate to see what a prime move costs you.

## Typical terms, by source

:::highlight
Lenders publish ranges. Banks and credit funds price differently, so read each line with its source.
:::

| Term | Published range | Source |
| --- | --- | --- |
| Interest rate | Often **8–12%** | Kruze, June 2025 |
| Interest rate | About **7–14%** across its debt book | Hercules Capital 10-K, 31 December 2025 |
| Interest rate by lender type | Light covenants: prime + **3–4%** (**10–14%**). Heavy covenants: prime + **1–3%** (**5–8%**) | Mercury, updated February 2026 |
| Term | **24–48** months | Kruze, June 2025 |
| Term | **3–5** years | Mercury, updated February 2026 |
| Term | **2–5** years; maturities typically **36–48** months | Hercules Capital 10-K, 31 December 2025 |
| Interest-only period | Often **12–18** months | Mercury, updated February 2026 |
| Interest-only period | **3–18** months or longer | Hercules Capital 10-K, 31 December 2025 |
| Upfront fee | **1.00%** of each loan funded (Codexis); **1.00%** on each future draw (Taysha) | Codexis 8-K (Trinity, November 2026); Taysha 10-Q (Trinity, 2025 loan) |
| Final payment | **5.00%** of original principal, in both examples | Same two filings |
| Warrant coverage | **2–10%** of the loan | Kruze, December 2023 |
| Warrant coverage | **3–20%** of principal; strike generally at the most recent round | Hercules Capital 10-K, 31 December 2025 |
| Warrant coverage by lender type | Light covenants **10–20%**; heavy **0–5%** | Mercury, updated February 2026 |
| Warrant life | Most often **10–12** years, up to **15** | Mercury, updated February 2026 |
| Lender yield | Weighted average effective yield **12.9%** on debt, Q4 2025 | Hercules Capital 10-K, 31 December 2025 |

There is no reliable public benchmark yet for the upfront fee and final payment. The two Trinity filings are examples, not a market median. Ask each lender for both in writing and enter them here. The Taysha loan carried no warrants, which shows the fee, final payment, and rate can carry the price on their own.

Hercules' 12.9% is the lender's side of the same math. It divides interest and fee income on its loans by the loans outstanding, and it leaves warrants out. Hold it next to the cash rate this tool shows for your offer.

## Three worked examples

:::highlight
We worked each one by hand in a separate script, then entered it here. The calculator matched to the dollar.
:::

| Example | Terms | Payments | Cash cost | Cash rate | Warrant | All-in rate |
| --- | --- | --- | --- | --- | --- | --- |
| 1. Default | $5M, 12%, 12 months interest-only + 24 amortizing, 1% fee, 5% final, 5% coverage at $2.00 | **$50,000** then **$235,367** | **$1,548,817** | **15.39%** | 125,000 shares, **0.50%**; **$500,000** at $6.00 | **18.21%** |
| 2. Trinity terms from the Codexis filing | $42.5M, 10.50%, 48 + 12, 1% fee, 5% final, 3.0% coverage at $1.08 | **$371,875** then **$3,746,316** | **$22,855,787** | **12.22%** | **1,180,556** shares; **$1,275,000** at $2.16 | **12.73%** |
| 3. Mercury's 12/36 shape | $4M, 11%, 12 + 36 straight-line, no fees, 10% coverage at $1.50 | **$36,667**, then **$147,778** falling to **$112,130** | **$1,118,333** | **11.57%** | 266,667 shares, **1.32%**; **$0** at $1.50 | **11.57%** |

Example 1 also needs 25,000,000 fully diluted shares, a $50M pre-money, exit in 5 years, and $1M of monthly net burn. Peak debt service is **23.5%** of burn, under SVB's 25%. The same $5M as equity takes **9.09%**, worth **$15,000,000** at $6.00 a share.

Example 2 takes the loan size, floor rate, fee, final payment, and warrant terms from Codexis' 8-K. The 1,180,556 shares match the filing. The 48 months of interest-only end in November 2030, with 12 months of amortization to November 2031. The filing lets interest-only run to maturity if there is no default. The exit price is ours, so the all-in rate is too.

Example 3 uses Mercury's 4-year, $4M, 12 months interest-only and 36 months amortizing structure, which gives **$111,111** of principal a month. Mercury gives no rate, so 11% is ours. With no fees and a warrant at the money, the cash rate equals (1 + 0.11 ÷ 12)^12 − 1, or 11.57%. A flat share price makes the warrant worth nothing, so the all-in rate stays the same. The warrant still takes 1.32% of the company if the price rises later.

## When to draw venture debt

:::highlight
Sign soon after an equity round. Draw as late as the term sheet lets you.
:::

SVB says your bargaining position is strongest right after an equity close. It wants at least **12** months of organic runway, and it sizes the loan to add about **6** months more. Signing and drawing are separate decisions. Every month you hold drawn cash you do not need, you pay interest on it. On the default loan that is **$50,000** a month.

Kruze's example: a lender offers venture debt to a startup with **20** months of cash and requires the draw within **6** months. That startup makes **14** payments before its cash-out date, which Kruze calls borrowing your own money. Kruze's fix is a structure that lets you draw with about **6** months of runway left. Its safest window is **3–6** months.

Warrants can follow the draw. Kruze says lenders often agree to half the coverage at signing and half at the draw. If you draw part of the facility, you issue part of the warrant. Enter only the drawn amount in the calculator to see that case.

## Cut the cost before you sign

:::highlight
Rate, fees, and warrants trade against each other. Get two term sheets and compare them here on the all-in rate.
:::

**Coverage.** Kruze says coverage can come down, in particular when you hold competing term sheets. Mercury says to collect at least two before serious negotiation.

**Interest-only.** Mercury says the interest-only length influences the rate and the warrant pricing. A longer interest-only period lowers peak debt service and helps the SVB burn check.

**Final payment and prepayment.** Mercury says prepayment fees can step down near maturity. The Trinity filings step down **3%**, **2%**, then **1%** by year. If you expect to repay early from a round or a sale, model the final payment plus the prepayment fee.

**Strike.** Hercules sets the strike at the latest round price in most deals. A strike below that round gives the lender more value per share.

For the clauses that hurt more than price, like the draw window, MAC, and covenants, read [venture debt for startups](/library/fundraising/venture-debt/). Then put the payment schedule into the [runway calculator](/tools/runway-calculator/).

## Mistakes

- Comparing offers on the headline rate. In example 1 the fee, final payment, and warrant add more than six points a year.
- Using a nominal rate. The calculator reports the effective annual rate, compounded monthly.
- Drawing on signing with 20 months of cash. You pay interest on money you would have spent anyway (Kruze).
- Valuing the warrant at zero. It costs nothing only if the share price stays at or below the strike.
- Forgetting amortization in the burn plan. SVB's example: $250K of monthly burn with a $5M facility amortizing over 30 months raises burn more than 50%.
- Counting dilution without the equity comparison. Show the board both percentages.

Check what the loan does to your efficiency numbers with the [burn multiple calculator](/tools/burn-multiple-calculator/). If SAFEs convert at the next round, run the [SAFE dilution calculator](/tools/safe-dilution-calculator/) with the warrant shares in the fully diluted count.

## Sources

- [Kruze Consulting, Key Insights into Venture Debt for Startups](https://kruzeconsulting.com/blog/insights-into-venture-debt/). Bryan Long, 12 June 2025. Terms **24–48** months; interest often **8–12%**; warrant dilution usually under **1%** of the cap table; equity rounds **10–30%** dilution.
- [Kruze Consulting, Warrant Coverage in Venture Loans Explained](https://kruzeconsulting.com/blog/warrant-coverage-venture-loans/). 19 December 2023, updated 1 August 2024. Coverage **2–10%** of the loan; negotiate with competing term sheets; half at commitment and half at draw; shares, strike, expiry.
- [Kruze Consulting, Don't borrow your own money](https://kruzeconsulting.com/blog/dont-borrow-your-own-money/). 5 June 2022, updated 1 August 2024. **20** months of cash, draw within **6** months, **14** payments before cash-out; draw with **6** months of runway left; safest **3–6** months.
- [Mercury, How to read a typical venture debt term sheet](https://mercury.com/blog/the-venture-debt-term-sheet). 3 January 2023, updated 3 February 2026. Duration **3–5** years; interest-only typically **12–18** months; $4M 12/36 example with about **$111,111** of monthly principal; final payments as a share of the loan; prepayment fees can step down; warrant life **10–12** years, up to **15**; light vs heavy covenant rate and warrant bands; collect at least two term sheets.
- [Hercules Capital, Form 10-K for 2025](https://www.sec.gov/Archives/edgar/data/1280784/000128078426000009/htgc-20251231.htm). Filed 12 February 2026. Warrant coverage **3–20%** of principal, strike generally at the most recent equity round; rates about **7–14%**; term **2–5** years; maturities typically **36–48** months; interest-only **3–18** months or longer; **97.9%** floating or floating with a floor; weighted average effective yield **12.9%** in Q4 2025.
- [Codexis, Form 8-K](https://www.sec.gov/Archives/edgar/data/1200375/000119312526454447/d187712d8k.htm). Event 5 November 2026, filed 10 November 2026. Trinity Capital loan: **$42.5M** Tranche A; greater of **10.50%** or prime (capped at 8.00%) + **3.75%**; **1.00%** commitment fee; interest-only to 1 November 2030 and maturity 1 November 2031; **5.00%** end-of-term payment; prepayment **3%** / **2%** / **1%**; warrants at **3.0%** of funded principal ÷ **$1.08**, **1,180,556** shares vested on Tranche A.
- [Taysha Gene Therapies, Form 10-Q, note 7 (term loans)](https://www.sec.gov/Archives/edgar/data/1806310/000119312526456949/R17.htm). Quarter to 30 September 2026. 2025 Trinity Capital loan: **$50.0M**; greater of prime + **4.00%** or **11.50%**; **1.00%** commitment fee on future draws; **5.00%** end-of-term payment; prepayment **3%** / **2%** / **1%**; no warrants.
- [Silicon Valley Bank (First Citizens), Venture Debt Amount: How Much Should Startups Raise?](https://www.svb.com/business-growth/access-to-capital/right-amount-of-venture-debt/). 22 September 2023. Debt service under **25%** of net burn; about **6** months added on top of **12+** months of organic runway; **$250K** burn and a **$5M** facility amortizing over **30** months raises burn more than **50%**.
- [Silicon Valley Bank, What is venture debt? Answering startups' common questions](https://www.svb.com/startup-insights/venture-debt/what-is-venture-debt/). Pricing has three parts: interest, an origination fee, and warrants; bargaining leverage is highest right after an equity close.
