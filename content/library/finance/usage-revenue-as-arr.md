---
title: "Does usage revenue count as ARR? AI usage vs subscription in the board pack"
description: Subscription fees and contractual minimum commits count as ARR. Usage above the commit, pay-as-you-go consumption, pilots, and credits go on their own labeled lines. Write one definition and use it in the deck, model, board pack, and data room.
slug: usage-revenue-as-arr
section: library
cluster: finance
layout: article
target_query: is usage-based revenue ARR
date: 2026-10-12
close: Founders who have defended an ARR definition through a board pack and a raise will pressure-test your revenue lines in a FounderNexus session before the number goes in the deck.
disclaimer: not-legal-tax
draft: false
related:
- library/finance
- library/finance/nrr-vs-grr-board-pack
- library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas
- library/fundraising/series-a-diligence-checklist
- library/finance/burn-multiple-vs-rule-of-40
- library/gtm/pilot-to-paid-contract
- library/finance/ai-gross-margin-inference-cogs
---

Usage revenue counts as ARR only up to what the contract commits. Subscription fees and recurring minimum commits are ARR. Usage above the commit, pay-as-you-go consumption, pilots, credits, and services go on separate, labeled lines. Burkland’s 2026 playbook for AI startups puts it in one rule: if you cannot tie a dollar to a renewable contractual commitment, call it run-rate, bookings, services, or pipeline. Investors rebuild your ARR in diligence. If the number shifts between the deck and the data room, expect them to discount all of it. Not legal, tax, or investment advice.

:::takeaways
- ARR is subscription revenue plus recurring minimum commits. Stripe: usage-based charges without minimum commitments do not belong in committed ARR. Burkland: count usage only up to the minimum commit or a clearly renewable baseline.
- Report usage above the commit as **usage run-rate**: trailing usage annualized, labeled, with the window stated. MongoDB’s 10-K annualizes the prior **90** days of Atlas direct-sales usage and the prior **30** days for self-serve, and says so.
- ARR is not a GAAP metric, and definitions vary by company (Burkland; Stripe). Write a one-page ARR policy and use it in board decks, investor updates, and fundraising files.
- Keep pilots without renewal language, promotional credits, setup fees, and services out of ARR (Burkland; a16z; ChartMogul).
- There is no reliable public benchmark yet for usage revenue as a share of ARR in AI SaaS. Growth Unhinged’s **37%** hybrid figure counts companies by pricing model. It says nothing about revenue mix.
:::

## What counts as ARR

:::highlight
The test is the contract. A usage label on the invoice does not decide it either way.
:::

| Revenue type | Example | In ARR? | Where it goes |
| --- | --- | --- | --- |
| Subscription or platform fee | Annual seat or platform contract | Yes | ARR |
| Recurring minimum commit | Contract commits to a monthly or annual usage floor | Yes, up to the minimum | ARR |
| Usage above the commit | Tokens, API calls, or resolutions past the included amount | No | Usage run-rate |
| Pay-as-you-go consumption | Card-billed usage with no contract floor | No | Usage run-rate |
| Pilot or POC with no renewal language | Three-month pilot with an opt-out | No | Pilot line, with a conversion table |
| Promotional credits and free allowances | Launch credits, free tier | No | Track as adoption, not revenue quality |
| Outcome fees with no minimum | Per-resolution fee, no floor | No | Run-rate line |
| Setup, implementation, services | Onboarding project, custom work | No | Services and one-time |

Rows from Burkland’s AI ARR policy (Debbie Rosler, February 2026) and Stripe’s committed ARR guide (February 2026). a16z’s 16 startup metrics (2015) and ChartMogul’s ARR page both exclude one-time fees and professional services. ChartMogul defines ARR as a measure of predictable, recurring revenue from subscription contracts.

Stripe adds one exception. If the contract fixes usage above the minimum, that amount can count. Burkland’s test for any line: if the customer stopped using the product tomorrow, could you still collect what you counted? A no sends that line to run-rate.

## Why investors push back on blended ARR

:::highlight
The same word covers different revenue at different companies. Investors read your definition before your number.
:::

L.E.K. Consulting (July 2025) calls ARR “a catchall label” for everything from fixed subscriptions to variable usage and AI-driven pricing. L.E.K. sees companies split contracted ARR (CARR) from variable revenue, which some annualize and others track as usage-based ARR (UARR). L.E.K. notes usage can take six to 12 months to stabilize, and NRR often looks inflated while new accounts ramp.

ChartMogul’s ARR page shows a second layer of confusion. ARR can mean Annualized Run Rate (MRR × 12) or Annual Recurring Revenue (annual and multi-year contracts only). Pick one and say which.

GTMfund’s newsletter (September 2025) names the pilot version of the problem Experimental Runrate Revenue. Its pattern: AI buyers sign three-month pilots with opt-outs, and teams book that revenue as ARR in decks. Burkland’s warning: when an ARR slide needs three minutes of verbal footnotes, many investors discount it. Services buried inside ARR often lead investors to discount the whole number.

Public consumption companies show the two approaches. Snowflake’s FY2025 10-K reports no ARR metric. It recognizes revenue on consumption, says it lacks the revenue-timing visibility of a subscription company, and reports remaining performance obligations of about **$6.9 billion**, with about **48%** expected in the next 12 months. MongoDB reports an ARR that includes annualized usage, and its 10-K states the **90**-day and **30**-day windows. Both filings state the method next to the number.

## How to present it on the board pack

:::highlight
Show the layers on one page. Put retention on the committed line.
:::

| Line | What it holds | How you annualize | What sits beside it |
| --- | --- | --- | --- |
| ARR (committed) | Subscription fees plus recurring minimum commits | Contracted recurring amount, annualized | ARR bridge; GRR and NRR on this base |
| Usage run-rate | Usage above the commit and pay-as-you-go | Trailing window annualized; state the window | Usage trend by cohort |
| Pilots | Paid pilots and POCs without renewal language | Do not annualize into ARR | Pilot-to-production conversion table |
| Services and one-time | Setup, implementation, custom work | None | Separate revenue line |
| Total revenue | Recognized revenue for the period | None | Reconciles to the ledger |

The layered view (ARR, usage run-rate, services) and the pilot conversion table come from Burkland. Burkland’s one-sentence pitch script: you define ARR as contracted recurring commitments and track usage run-rate separately as a growth signal. If you also want a combined figure, label it “ARR + usage run-rate,” show both parts beside it, and state the window. Do not call the combined figure ARR.

Run [NRR and GRR](/library/finance/nrr-vs-grr-board-pack/) on the committed line first. Usage ramps can lift NRR in early months (L.E.K.), and published retention bands come from subscription samples. Burn multiple divides net burn by net new ARR (Sacks), so your ARR definition moves that number too. See [burn multiple vs Rule of 40](/library/finance/burn-multiple-vs-rule-of-40/).

For diligence, Burkland lists five schedules investors rebuild anyway: a metrics definitions page, a customer contract schedule, an ARR bridge, a 12-month renewal calendar, and a reconciliation from contracts to billing, cash, and accounting. They slot into the room on the [Series A diligence checklist](/library/fundraising/series-a-diligence-checklist/).

## A labeled example

:::highlight
Editorial example with round numbers. Not a company and not a benchmark.
:::

An AI support product bills a platform fee, a monthly usage floor on some contracts, and per-resolution usage above the floor.

| Line | Monthly | Treatment | Annualized |
| --- | --- | --- | --- |
| Platform subscriptions | $40k | ARR | $480k |
| Recurring minimum commits | $10k | ARR | $120k |
| Usage above commits (trailing 3-month average) | $15k | Usage run-rate | $180k |
| Paid pilots, no renewal language | $5k | Pilot line | Not annualized into ARR |
| Implementation fees this month | $8k | Services | Not annualized |

Reported ARR is **$600k** ($480k + $120k). Usage run-rate is **$180k**, labeled with its three-month window. Annualize all five lines and the slide says **$936k**. In diligence that $336k gap reads as an inflated headline, and the investor then discounts the clean $600k too.

## Mistakes that cost trust

:::highlight
Each mistake below moves the definition, and investors catch the move in diligence.
:::

**Annualizing a first-month spike.** Onboarding bursts and one-off migrations make a fragile headline (Burkland). Use a stated trailing window.

**Counting pilots as ARR.** A three-month pilot with an opt-out is a trial (GTMfund). Show it with a conversion table. Converting pilots is its own job: [pilot to paid contract](/library/gtm/pilot-to-paid-contract/).

**Changing the definition mid-raise.** Burkland’s policy exists to stop the definition drifting as pricing changes or fundraising pressure rises. If you change it, restate past periods on the new rule and tell the board first.

**Comparing blended ARR to peers’ subscription ARR.** Your blended number and a peer’s contract-only number describe different revenue. Compare committed ARR to committed ARR.

**Treating credits as paid usage.** Credits drive adoption. Burkland: separate free usage from contracted usage.

**Mixing customer definitions.** Workspace in one sheet and enterprise logo in another breaks retention and ARPA math (Burkland).

## Lock the definition before the board meeting or the raise

:::highlight
Burkland’s 30-day plan fits the month before a raise. Run it before the first investor sees the number.
:::

:::steps ARR definition lock
1. **Pull every contract.** Order forms, pilot agreements, and amendments in one contract log (Burkland week 1).
2. **Tag each line.** ARR, usage run-rate, pilot, or services, with the clause that supports the tag (Burkland).
3. **Write the one-page policy.** Definitions, inclusion and exclusion rules, and the annualization window (Burkland; Stripe for minimum commits).
4. **Restate the trend.** Rebuild past months on the new rule so the board sees one consistent line.
5. **Build the schedules.** Contract schedule, ARR bridge, renewal calendar, and reconciliation (Burkland weeks 2 to 3).
6. **Use one definitions page everywhere.** Deck, model, board pack, and data room (Burkland; FounderNexus session).
7. **Dry-run diligence.** Have someone outside the build trace headline ARR to contracts and invoices (Burkland week 4).
:::

## Pricing model context

:::highlight
The pricing model sets how much of your revenue sits outside ARR.
:::

Bessemer’s AI pricing playbook (February 2026) describes hybrid pricing as a base subscription for predictability with usage tiers for upside, and calls it the middle ground for early-stage startups. Under the table above, the base lands in ARR and the tiers above any commit land in usage run-rate. Picking the charge metric is a separate decision: [seat vs usage vs outcome pricing](/library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas/).

Growth Unhinged’s 2026 survey (Kyle Poyar, **230** companies, April to May 2026) found **37%** on hybrid pricing, up from **25%** twelve months earlier. Usage- and outcome-priced companies said their revenue is hard to forecast. Those are shares of companies by pricing model. There is no reliable public benchmark yet for usage revenue share of ARR in AI SaaS, so do not quote a “normal” mix to your board.

A [FounderNexus](https://www.foundernexus.com?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library) session landed on the same rule: keep AI usage revenue out of ARR, and use one metric definition across the deck, the model, and the board pack. That is operator judgment, not a survey.

## Sources

- [Burkland Associates, AI ARR You Can Defend: A Seed-to-Series A Playbook for Metrics and Diligence](https://burklandassociates.com/2026/02/24/ai-arr-you-can-defend/) — Debbie Rosler, 23 February 2026. ARR not a GAAP metric; ARR only for revenue tied to renewable contractual commitments; usage without a minimum commit excluded and shown as usage run-rate; exclusions (pilots without renewal language, setup and implementation, promotional credits, outcome-only fees with no minimum); layered view; one-page policy across board decks, investor updates, and fundraising materials; stop-using test; three minutes of verbal footnotes; five diligence schedules plus optional pilot conversion table; gotchas (usage spike, pilots, services, credits, customer definitions); 30-day plan.
- [Stripe, Committed annual recurring revenue explained](https://stripe.com/resources/more/committed-annual-recurring-revenue-explained) — updated 18 February 2026. Usage-based charges without minimum commitments, one-time fees, and services do not belong in committed ARR; recurring minimum commitments can count; usage above the minimum excluded unless contractually fixed; committed ARR not standardized across companies.
- [ChartMogul, ARR: Annual Recurring Revenue vs Annualized Run Rate](https://chartmogul.com/saas-metrics/arr/) — updated 8 September 2026. Two meanings (MRR × 12 vs annual and multi-year contracts only); ARR excludes one-time payments and professional services; predictable, recurring revenue from subscription contracts.
- [Andreessen Horowitz, 16 Startup Metrics](https://a16z.com/16-startup-metrics/) — Jeff Jordan, Anu Hariharan, Frank Chen, and Preethi Kasireddy, 21 August 2015. ARR excludes one-time fees and professional service fees; common mistake of multiplying all-in bookings by 12.
- [L.E.K. Consulting, How AI Is Redefining SaaS Metrics and Forecasting](https://www.lek.com/insights/technology/how-ai-redefining-saas-metrics-and-forecasting) — 24 July 2025. ARR as a catchall label; CARR vs UARR; usage can take six to 12 months to stabilize; NRR often inflated during ramp.
- [GTMnow (GTMfund), ARR vs. ERR: Why every dollar isn’t equal](https://gtmnow.com/arr-vs-err-why-every-dollar-isnt-equal/) — 5 September 2025. Three-month pilots with opt-outs; pilot revenue booked as ARR in decks; Experimental Runrate Revenue.
- [Snowflake Inc., Form 10-K for fiscal year ended 31 January 2025 (SEC)](https://www.sec.gov/Archives/edgar/data/1640147/000164014725000052/snow-20250131.htm) — filed 21 March 2025. Consumption-based model; revenue generally recognized on consumption; less revenue-timing visibility than a subscription company; remaining performance obligations about **$6.9 billion**, about **48%** expected in the next 12 months; no ARR metric reported.
- [MongoDB, Inc., Form 10-K for fiscal year ended 31 January 2026 (SEC)](https://www.sec.gov/Archives/edgar/data/1441816/000162828026016799/mdb-20260131.htm) — filed 11 March 2026. ARR includes contractual commitments plus annualized prior **90** days of Atlas direct-sales usage and prior **30** days of self-serve usage; excludes professional services.
- [Bessemer Venture Partners, The AI pricing and monetization playbook](https://www.bvp.com/atlas/the-ai-pricing-and-monetization-playbook) — Atlas Editors, 10 February 2026. Hybrid pricing: base subscription for predictability, usage tiers for upside; middle ground for early-stage startups.
- [Growth Unhinged, The state of B2B monetization in 2026](https://www.growthunhinged.com/p/the-state-of-b2b-monetization-in-2026) — Kyle Poyar, 13 May 2026. **230** B2B software and AI companies surveyed April to May 2026; **37%** hybrid pricing, up from **25%** twelve months earlier; usage- and outcome-based companies say revenue is hard to forecast.
- [David Sacks, The Burn Multiple (Craft Ventures / Medium)](https://medium.com/craft-ventures/the-burn-multiple-51a7e43cb200) — 23 April 2020. Burn multiple = net burn ÷ net new ARR.
- [FounderNexus session](https://www.foundernexus.com?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library) — Operator judgment from live finance and data-room sessions: keep AI usage revenue out of ARR; one metric definition across deck, model, and board pack. Not a survey.

## Related

- [Finance, metrics & runway](/library/finance/)
- [NRR vs GRR for the board pack](/library/finance/nrr-vs-grr-board-pack/)
- [Seat vs usage vs outcome pricing for AI SaaS](/library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas/)
- [Series A diligence checklist](/library/fundraising/series-a-diligence-checklist/)
- [Burn multiple vs Rule of 40](/library/finance/burn-multiple-vs-rule-of-40/)
- [Pilot to paid contract](/library/gtm/pilot-to-paid-contract/)
