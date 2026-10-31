---
title: "Startup pricing and packaging: tiers, anchors, first increase"
description: "Price from buyer value: YC suggests 25–50% of it. Ship two or three tiers, a premium 50–100% above base, discounts that expire, and raise at renewal."
slug: startup-pricing-packaging
section: library
cluster: gtm
layout: article
target_query: startup pricing and packaging
date: 2026-10-31
updated: 2026-10-31
close: Founders who have set a first price list and raised it on live customers will pressure-test your tiers, discounts, and increase plan in a VEN session.
draft: false
related:
- library/gtm
- library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas
- library/gtm/price-ai-features-inference-cost
- library/gtm/first-customer-contract
- library/gtm/pilot-to-paid-contract
- library/gtm/landing-page-that-converts
- tools/ai-gross-margin-calculator
---

Set the price from the value your buyer gets, then package it as two or three tiers the buyer can sort themselves into. Tom Blomfield's Y Combinator talk puts the number at **25–50%** of the value you deliver, so the customer keeps about two-thirds. Use your cost as the floor and aim for software margins of **80–90%**. Put the enterprise features (single sign-on, audit logs, compliance reports) in the top tier and price it well above the rest. Kyle Poyar's 2026 survey of more than **230** software companies puts a premium edition at **50–100%** above base. Show discounts as a dated line that expires. Plan the first price increase before you need it: McKinsey found that a **1%** price rise, at steady volume, lifts operating profit about **8%** for an average S&P 1500 company.

:::takeaways
- Start from a value equation the buyer's champion agrees with. YC: charge **25–50%** of it; cost only sets the floor.
- Two or three tiers cover most needs. In Toolradar's May 2026 count of **2,526** paid tools with public prices, **34.9%** used three tiers and **19.0%** used one.
- Gate enterprise needs in the top tier. YC: SSO, SOC 2 reports, and audit logs can justify up to **10×** the price of a small-team plan.
- Discount on a dated line and trade it for something. McKinsey: standard discounts on a new product cut its reference price; free trials and samples do not.
- Raise prices for new customers first, then for existing ones at renewal with notice. PostHog grandfathers live customers for about **2** months on a GA price change.
:::

This page covers the price list: the number, the tiers, the discount rules, and the first increase. If you have not picked what you charge for (seats, usage, or outcomes), start with [seat vs usage vs outcome pricing](/library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas/). For AI cost floors and overage, use [how to price AI features](/library/gtm/price-ai-features-inference-cost/). For the order form itself, use [how to negotiate your first customer contract](/library/gtm/first-customer-contract/).

## Set the number from a value equation

:::highlight
Write down the dollars you save or earn for one buyer, get their champion to agree with it, and price at a share of that number.
:::

Blomfield's method has three inputs. Value comes first: time saved, cost removed, or revenue added, in the buyer's own numbers. Cost comes second and only sets a floor. Competition comes third, and his advice is to differentiate rather than match a lower price.

| Input | What to write down | Rule of thumb | Source |
| --- | --- | --- | --- |
| Value to the buyer | Annual dollars saved or earned, agreed with the champion | Charge **25–50%** of it; the buyer keeps about two-thirds | YC, Blomfield 2024 |
| Your cost to serve | Model, cloud, and support cost per customer per year | A floor only; aim for **80–90%** gross margin | YC, Blomfield 2024 |
| Competitors | What they charge and what they leave out | Differentiate on function; a price war takes the margin out | YC, Blomfield 2024 |
| Unknown value | Prices of other software this buyer already pays for | Start there and raise **50%** with each new pitch until you lose more than **25%** of deals on price alone | YC, Blomfield 2024 |

Worked example from Blomfield's talk, illustrative and not data from any company:

| Line | Amount |
| --- | --- |
| Support team cost for the buyer | $10M a year |
| Share of time your tool removes (agreed in the pilot) | 20% |
| Value to the buyer | $2M a year |
| Your price at about a third | $700k a year |
| Your cost to serve | $200k a year |

The pilot's job is to confirm the 20%. If it comes in at 15% or 25%, adjust the price to match.

McKinsey's partners wrote in 2003 that 80 to 90 percent of the poorly chosen prices they saw were too low. They also warned that the release price, minus discounts, sets the market's reference point for what the product is worth. A low first price is harder to fix than a high one.

## Package two or three tiers

:::highlight
Build tiers around how buyers differ, then gate the features only larger customers need in the top tier.
:::

| Tier | Who it serves | What goes in | Price logic |
| --- | --- | --- | --- |
| Starter or team | A small team proving the product | Core workflow, limited seats or usage | Low enough for a manager to buy without a long approval |
| Growth or pro | The buyer you sell to most | Full workflow, integrations, higher limits | The tier you expect most to choose; the anchor for the others |
| Enterprise | Security and procurement-led buyers | SSO, audit logs, SOC 2 reports, data residency, admin controls | Contact sales or a high published floor; YC says up to **10×** |

Toolradar counted the tiers on **2,526** paid tools with public prices in May 2026. Three tiers was the most common shape at **34.9%**, one tier was next at **19.0%**, and only **10.8%** published five or more. Its count excludes products with no public price, so it underweights enterprise software. There is no reliable public benchmark yet for tier structure or price-increase size at Seed to Series A.

Middle options gain share. Itamar Simonson's 1989 experiments found that a product's share was on average **17.5%** larger when it sat as the middle option between two others, with significant differences in **9** of **11** cases. Use that by making the tier you want most buyers on the middle one, with a real top tier above it.

Poyar's 2026 survey found a premium edition usually priced **50–100%** above the base edition, and named weak expansion revenue as the top monetization problem. A top tier with clear extras gives a growing customer a place to go. Early-stage companies under **$5M** ARR in the same survey leaned most toward flat fees, at **37%** adoption.

The VEN session framing was to package the product in a unit the buyer already counts, such as a team, a location, or a block of usage, and to make overage cost a little more than buying the next block.

## Discount on a dated line

:::highlight
Show the full list price, show the discount as its own line with an end date, and write what the customer gives in return.
:::

McKinsey's advice for a new product was to protect the reference price. Free trials, samples, and early access for well-known customers let buyers try the product without lowering the price. Standard discounts and rebates do lower it, and buyers start to doubt the product.

| Discount | What you get in return | When it ends |
| --- | --- | --- |
| Design partner rate | Weekly feedback, a case study, a reference call | At the first renewal |
| Annual prepay | Cash up front, a 12-month term | Renews at the list rate |
| Multi-year | A longer term | Stated on the order form |
| Pilot price | A short test with a written success metric | At conversion to the annual plan |

Blomfield prefers an annual contract with a 30-day or 60-day money-back guarantee over a long free pilot. Keep any pilot to two to four weeks with clear success criteria. The [pilot to paid contract](/library/gtm/pilot-to-paid-contract/) page covers the conversion terms.

## Publish the price or ask buyers to talk to sales

:::highlight
Publish the lower tiers so small buyers can self-serve. Put the enterprise tier behind a conversation when value differs a lot from one buyer to the next.
:::

Blomfield's case for "contact sales" on the top tier: enterprise value varies by customer, so one public number overprices some buyers and underprices others. Publish the starter and team prices so a buyer can compare without a call. The [landing page](/library/gtm/landing-page-that-converts/) page covers where the price goes on the site.

Check that the price can pay for the way you sell. Blomfield's rule of thumb is about **5:1** between new ARR a seller closes in a year and that seller's total pay. At a **$100k** total pay, a seller needs about **$500k** of new ARR. At **$1,000** a year per customer, that is about **42** deals a month for one seller, a pace that fits an inside sales team.

## Plan the first price increase

:::highlight
Raise the list price for new customers first, watch conversion, then move existing customers at renewal with written notice.
:::

Poyar's 2026 survey found three in four companies changed pricing or packaging in the past year, so your buyers have seen price changes before. McKinsey's arithmetic is the reason to do it with care: for an average S&P 1500 company, a **1%** price rise at steady volume lifts operating profit about **8%**, and a **5%** price cut needs about **18.7%** more volume to break even.

| Step | What to do | Source |
| --- | --- | --- |
| Model it per account | Old bill, new bill, plan, and owner for each customer, plus revenue at risk | PostHog handbook |
| Grandfather live customers | About **2** months on a GA price change; about **1** month from beta to GA | PostHog handbook |
| Allow lead time | About six weeks from first draft to launch day | PostHog handbook |
| State the increase | If the price goes up, the email says so; managed accounts get a conversation | PostHog handbook |
| Use the renewal date | A dated discount brings a customer back to list; escalator clauses now appear in **13%** of contracts, down from **23%** in 2024 | Common Paper 2026 |

Large vendors still raise on a schedule. Vendr reports Salesforce's standard annual uplift at **9%**, negotiable to **5–7%**. A startup gets further by pairing an increase with shipped value, such as a new module, a higher limit, or a new tier.

Not legal advice. Notice periods and renewal terms depend on your contracts; have counsel check price-change clauses before you send notices.

:::steps Set and raise your price
1. **Write the value equation.** Dollars saved or earned for one buyer, agreed with their champion.
2. **Price at a share of it.** Start at **25–50%** of value and check that cost leaves **80–90%** margin.
3. **Pick two or three tiers.** Starter, the main tier most buyers choose, and enterprise.
4. **Gate enterprise needs.** SSO, audit logs, compliance reports, and data residency go in the top tier.
5. **Price the premium.** A top edition **50–100%** above base gives growing customers somewhere to go.
6. **Choose a unit buyers count.** Teams, locations, or usage blocks, with overage priced a little above the next block.
7. **Date each discount.** List, discount, and net on separate lines, with what the discount buys and when it ends.
8. **Test the number on new pitches.** Raise it until you lose more than **25%** of deals on price alone.
9. **Check the sales math.** About **5:1** new ARR to seller pay sets which sales motion the price supports.
10. **Raise at renewal.** New customers first, then existing ones with notice and a grandfather window.
:::

## Mistakes that cost revenue

**Cost-plus pricing.** Blomfield says it always ends with underpricing. Cost is the floor.

**A launch price set to win share.** McKinsey found most poorly chosen prices were too low, and the first price becomes the market's reference.

**Too many tiers.** Toolradar found **10.8%** of paid tools publish five or more tiers. A buyer who cannot tell tiers apart asks for a call or leaves.

**Discounts with no end date.** An open-ended discount becomes the price at renewal. Common Paper's data shows buyers strike automatic increases more often, so the dated line does the work.

**Matching a cheaper competitor.** Blomfield's example is the airline industry at **2.7%** net margin. Differentiate on function, a niche, or integrations.

**Raising on all customers at once with no notice.** PostHog grandfathers live customers and models revenue at risk per account first.

Pair this page with the [first customer contract](/library/gtm/first-customer-contract/) for the order form and the [AI gross margin calculator](/tools/ai-gross-margin-calculator/) for the cost floor.

## Sources

- [Y Combinator, How To Price For B2B (Startup School)](https://www.youtube.com/watch?v=4hjiRmgmHiU). Tom Blomfield, 25 July 2024. Value equation with the champion; charge **25–50%** of value so the customer keeps about two-thirds; worked example of **$10M** support cost, **20%** saved, **$2M** value, about **$700k** price, **$200k** cost; cost only as a floor; target **80–90%** software margins; airline industry **2.7%** net margin; enterprise gating of SSO, SOC 2 reports, audit logs, compliance reports, data residency, sometimes up to **10×**; about **5:1** new ARR to seller total compensation, **$1,000** a year is about **42** deals a month; pilots of a couple of weeks to four weeks, or annual contracts with a **30**- or **60**-day money-back guarantee; when unsure, start near similar software and raise **50%** per pitch until more than **25%** of deals are lost on price.
- [McKinsey, The power of pricing](https://www.mckinsey.com/capabilities/growth-marketing-and-sales/our-insights/the-power-of-pricing). Michael V. Marn, Eric V. Roegner, Craig C. Zawada, 1 February 2003. Average S&P 1500 income statement: a **1%** price rise at stable volume gives about **8%** more operating profit; a **5%** price cut needs **18.7%** more volume to offset.
- [McKinsey, Pricing new products](https://www.mckinsey.com/capabilities/growth-marketing-and-sales/our-insights/pricing-new-products). Marn, Roegner, Zawada, 1 August 2003. **80 to 90 percent** of poorly chosen prices are too low; the release price minus discounts sets the reference point; free samples and trials preserve it, standard discounts and rebates cut it.
- [Growth Unhinged, The 2026 State of B2B SaaS and AI Monetization Report](https://www.growthunhinged.com/p/the-state-of-b2b-monetization-in-2026). Kyle Poyar, 13 May 2026. **230+** companies, survey April–May 2026. Premium edition usually **50–100%** above base; not enough expansion revenue the top challenge; three in four changed pricing or packaging in the past year; companies under **$5M** ARR leaned most to flat fees (**37%**); hybrid **37%**.
- [Toolradar, SaaS Pricing Models 2026](https://toolradar.com/reports/saas-pricing-models-2026). Louis Corneloup, published 15 May 2026, updated 2 July 2026. **2,526** paid tools with parsed public pricing tiers: one tier **19.0%**, two **16.5%**, three **34.9%**, four **16.7%**, five **3.4%**, six or more **7.4%**. Tools without a public pricing page excluded.
- [Itamar Simonson, Choice Based on Reasons: The Case of Attraction and Compromise Effects](https://doi.org/10.1086/209205). Journal of Consumer Research 16(2), September 1989, pp. 158–174. Lab choice experiments across product categories; shares on average **17.5%** larger as the compromise option, significant in **9** of **11** cases.
- [PostHog Handbook, Shipping a pricing change](https://posthog.com/handbook/growth/shipping-a-pricing-change). Read 31 October 2026. Model old and new bills per account and revenue at risk; grandfather existing customers about **1** month beta to GA and about **2** months for GA price changes; budget about six weeks from first draft to launch; say an increase plainly; managed accounts get a conversation.
- [Common Paper, 2026 SaaS Contract Benchmark Report](https://commonpaper.com/resources/2026-saas-contract-benchmark-report/). Published 15 July 2026, updated 16 October 2026. **16,140** signed agreements; automatic fee increases **13%** (**23%** in 2024).
- [Vendr, The Pricing Intelligence Report](https://www.vendr.com/resources/trends-report). 2025 full year and Q1 2026. Salesforce profile: standard annual uplift **9%**, negotiable to **5–7%**.
- [VEN (Venture Executive Network)](https://www.venexecs.com/?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library&utm_content=startup-pricing-packaging). Founder sessions on pricing and packaging, 2026. Start above free; anchor the premium number first and discount visibly and for a set time; each discount buys time, feedback, or proof and expires; package in a unit the buyer already counts; overage a little worse than the next block. Not a survey. No closed-session numbers.

## Related

- [Go-to-market](/library/gtm/)
- [Seat vs usage vs outcome pricing for AI SaaS](/library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas/)
- [How to price AI features to cover inference cost](/library/gtm/price-ai-features-inference-cost/)
- [How to negotiate your first customer contract](/library/gtm/first-customer-contract/)
- [How to convert a pilot to a paid contract](/library/gtm/pilot-to-paid-contract/)
- [How to write a startup landing page that converts](/library/gtm/landing-page-that-converts/)
- [AI gross margin calculator](/tools/ai-gross-margin-calculator/)
