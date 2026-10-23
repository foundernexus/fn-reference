---
title: How to price AI features to cover inference cost
description: Cost sets the floor and value sets the price. Measure AI cost per unit for the typical user and the heavy cohort, include an allowance sized to typical use, and meter the rest with credits or overage priced at or above the floor.
slug: price-ai-features-inference-cost
section: library
cluster: gtm
layout: article
target_query: how to price AI features
date: 2026-10-16
close: Founders who have repriced an AI feature and kept their customers will pressure-test your allowance and overage math in a VEN session.
draft: false
related:
- library/gtm
- library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas
- library/finance/ai-gross-margin-inference-cogs
- tools/ai-gross-margin-calculator
- library/finance/usage-revenue-as-arr
- library/gtm/pilot-to-paid-contract
- library/gtm/first-customer-contract
---

Price an AI feature from the value it delivers. Set the floor from what it costs to serve. Measure AI cost per unit twice, once for the typical user and once for your heaviest cohort, and divide by one minus your target AI margin to get the floor. Then include an allowance sized for typical use and meter everything above it with credits or overage priced at or above that floor. In Kyle Poyar’s 2026 Growth Unhinged survey of 230 software companies, internal costs and margins were the top factor in pricing AI capabilities (**54%**), and the median target AI margin was about **50%**. If you have not picked the charge metric yet, start with [seat vs usage vs outcome pricing](/library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas/). This page covers the next step: making the price cover the inference bill.

:::takeaways
- Floor = AI cost per unit ÷ (1 − target AI margin). At a **50%** target the floor is **2×** cost, the same multiple Bessemer uses for its hybrid platform fee. Bessemer also warns that cost-plus pricing undercharges, so treat 2× as the floor and anchor the price to buyer value.
- A flat price breaks on heavy users. Poyar says the top **10%** of AI power users drive **70%+** of token consumption in his experience. The SaaS CFO (Murray) cites estimates that heavy users cost **50 to 100** times more than light users.
- The large vendors moved to an included allowance plus metered use. GitHub Copilot Pro (June 2026) is **$10** a month and includes **$10** of AI credits billed at published API rates. Cursor Pro (2025) includes **$20** of frontier model usage at API pricing and sells more at cost.
- Credits are spreading. **29%** of Poyar’s sample use AI credits and **33%** plan to add them within 6 to 12 months.
- Reprice with notice. Cursor apologized and refunded surprise charges after its June 2025 change. GitHub gave five weeks’ notice and a preview bill before its switch.
:::

## Pick the package before you set the number

:::highlight
Each package puts the heavy-user bill on a different party. Choose who carries it.
:::

| Package | Fits when | Who carries heavy-user cost | Public example |
| --- | --- | --- | --- |
| Bundle into a higher tier | AI use is light and even; you want adoption | You, inside a flat price | Notion: core AI in Business at **$20** per member a month since May 2025; Free and Plus get a trial |
| Paid add-on per seat | Procurement buys seats and value tracks the person | You, unless the add-on has a cap | Microsoft Copilot add-on about **$30** on top of an Office 365 license (Bessemer) |
| Included allowance plus overage | Usage per user is uneven | The heavy user, above the allowance | GitHub Copilot Pro: **$10** includes **$10** of AI credits plus a flex allotment; set a budget for more |
| Prepaid credit packs | Agents and automations run with no person in the loop | The buyer, by pack | Salesforce Flex Credits: **$500** per 100,000; one action is 20 credits (**$0.10**). Notion Custom Agents: **$10** per 1,000 credits |
| Per conversation or outcome | Success is unambiguous and you can absorb variance per task | You, per task | Salesforce Agentforce **$2** per conversation; Intercom Fin **$0.99** per resolution (Bessemer) |

Bessemer’s AI pricing playbook names usage caps, prepaid credits, hybrid models, and tiered subscriptions as the tools for balancing variable compute against predictable revenue. Poyar’s fixes for weak expansion point the same way: a premium edition priced **50–100%** above the base, add-ons that some customers value, and consumption limits that hit the top **10%** of power users. The last row is a charge-metric decision. Work it on [seat vs usage vs outcome pricing](/library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas/).

## Work out the cost floor per unit

:::highlight
Two costs per unit: the typical user and the heavy cohort. Price from the floor up.
:::

Pick the unit you charge for: a seat, a task, a credit, or a conversation. Count the AI delivery costs that belong in COGS: production inference, production GPU, retrieval and vector serving, monitoring, AI support, and human review of customer output. Leave dev/test inference and training out. The classification table lives on [AI SaaS gross margin](/library/finance/ai-gross-margin-inference-cogs/), and the [AI gross margin calculator](/tools/ai-gross-margin-calculator/) returns cost per user and the heavy-cohort share from your monthly numbers.

Then apply the formula to both costs:

| Target AI margin | Floor as a multiple of AI cost per unit |
| --- | --- |
| 40% | 1.67× |
| 50% | 2× |
| 60% | 2.5× |
| 70% | 3.33× |

Pick the target before you see the result. Poyar’s median target is about **50%**. **12%** of his sample aim for SaaS-like AI margins of **80%+**, and a similar share aim for **20%** or lower (he names PostHog). Bessemer puts AI gross margins at **50–60%** against **80–90%** for SaaS. Murray’s published bands by product type are on the gross margin page.

The floor is the minimum price. Bessemer says most founders default to cost-plus (calculate costs, double it) and undercharge because asking for more feels awkward. Anchor the price against what the problem costs the buyer today. Keep the cost per unit of work in view so an outcome or flat price cannot invert your margin at scale ([VEN session](https://www.venexecs.com/?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library)). There is no reliable public benchmark yet for the markup AI companies charge over inference cost on credits or overage.

## A labeled example: flat bundle vs allowance plus overage

:::highlight
Editorial example with round numbers. Not a company and not a benchmark.
:::

A B2B product adds an AI assistant to **1,000** paid seats. Measured AI COGS per month: **900** typical users at **$2.50** each and **100** heavy users at **$60** each, **$8,250** in total. The heavy cohort is **73%** of the bill, close to Poyar’s **70%+** observation. The target AI margin is **50%**.

| Line | Flat bundle | Allowance plus overage |
| --- | --- | --- |
| Price design | **$16.50** seat uplift (average cost × 2) | **$10** seat uplift with **$5** of AI usage included; overage at 2× cost |
| Typical user: price vs AI cost | $16.50 vs $2.50 | $10 vs $2.50 |
| Heavy user: price vs AI cost | $16.50 vs $60 | $120 ($10 + $55 overage × 2) vs $60 |
| AI revenue vs AI COGS | $16,500 vs $8,250 | $21,000 vs $8,250 |
| AI margin | **50%** | **61%** |
| AI margin if heavy-user cost doubles | **14%** | **57%** |

The flat bundle hits the target on day one and loses **$43.50** a month on each heavy user. If agentic features double heavy-user cost, its margin falls from **50%** to **14%** and the price has not moved. The allowance plan charges typical users less, keeps each heavy user at a **50%** margin, and holds the blend near target when usage climbs. The doubling row is a stress test. GitHub and Cursor both changed pricing after agentic and long-horizon use pushed per-request costs up.

## Size the allowance and price the overage

:::highlight
Size the allowance to the typical user. Price everything above it at or above the floor.
:::

**Size the allowance from median use.** Cursor describes its Pro allowance in median terms. Its July 2025 post says that at median token usage **$20** covered about **225** Sonnet 4 requests, **550** Gemini requests, or **650** GPT 4.1 requests, and that the vast majority of Pro users do not run out. GitHub sets base credits equal to the subscription price and adds a flex allotment that it says will adapt as model pricing and efficiency change. Unused credits expire at month end. Business plans pool them across the organization so no seat strands capacity.

**Price the overage above the floor.** GitHub bills extra usage at published API rates and Cursor sells more at cost. Both earn their margin on the plan. A startup with thin plan margin cannot copy that. Price overage at the floor or above, in blocks the buyer can approve once.

**Give each credit a fixed dollar value.** GitHub fixes one AI credit at **$0.01**. Salesforce fixes one Agentforce action at **20** credits. Poyar warns that credits are great for vendors and can become a nightmare for customers who manage different credit models across dozens of vendors. A credit the finance team can convert to dollars survives procurement.

**Report overage apart from the subscription.** Usage above a commitment is not ARR. Keep it on its own line ([usage revenue as ARR](/library/finance/usage-revenue-as-arr/)).

## Guard the margin on heavy users and agents

:::highlight
Budgets, caps, and model routing keep a good price from turning into a bad month.
:::

**Give admins a budget.** GitHub lets admins set budgets at the enterprise, cost center, and user level, then choose whether to allow more usage at published rates or cap spend. Notion pauses Custom Agents when credits run out until an admin adds more.

**Price agent runs apart from human seats.** Notion keeps core AI inside the **$20** Business seat and meters Custom Agents in credits from 4 May 2026. GitHub’s stated reason for its switch: a quick chat question and a multi-hour autonomous coding session could cost the user the same amount, and the old request model was no longer sustainable. Cursor said its hardest requests cost an order of magnitude more than simple ones.

**Route work to cheaper models.** ICONIQ’s January 2026 survey, via SaaStr, found model inference rising from **20%** to **23%** of spend as products scale, and the best teams sending most tasks to smaller models. GitHub gives paid users a **10%** discount on model costs when they use auto model selection.

## Reprice without losing trust

:::highlight
Treat a pricing change like a product launch: notice, a preview, and a window for current customers.
:::

| Company | What changed | How they handled existing customers |
| --- | --- | --- |
| Cursor | 16 Jun 2025: Pro moved from **500** requests to **$20** of usage at API pricing | 4 Jul 2025 apology; refunds for unexpected usage from 16 Jun to 4 Jul |
| GitHub | Announced 27 Apr 2026; usage-based billing live 1 Jun 2026 | Base prices unchanged; preview bill in early May; Business **$30** and Enterprise **$70** in promotional credits for June to August |
| Notion | 13 May 2025: AI bundled into Business and Enterprise | New prices for new subscriptions only; existing customers moved at first renewal after 13 Aug 2025 |

Expect to do this more than once. Poyar found that three in four software companies changed pricing or packaging in the past year.

## Build the AI price in order

:::highlight
Ten steps from the cost map to the board line. Run them before launch and again at each reprice.
:::

:::steps AI feature price build
1. **Measure AI COGS per unit.** Use the COGS lines on the [gross margin page](/library/finance/ai-gross-margin-inference-cogs/). Split typical users from the heavy cohort.
2. **Write the target AI margin down.** One number, agreed with whoever owns the board pack.
3. **Compute the floor.** Cost per unit ÷ (1 − target). Do it for the typical and the heavy unit.
4. **Anchor to buyer value.** Price against what the problem costs the buyer today. Use the floor as a check on that number.
5. **Pick the package.** Bundle, add-on, allowance plus overage, credit packs, or per outcome, from the table above.
6. **Size the allowance at typical use.** Median user plus headroom. Check what share of users would exceed it.
7. **Price overage or credits at or above the floor.** Fix a dollar value per credit and sell in blocks.
8. **Add budgets, caps, and alerts.** Admin budgets, spend caps, and a usage warning before the cap.
9. **Announce with notice.** Preview bills, a date, and current customers moved at renewal.
10. **Report it monthly.** AI margin, heavy-cohort share, and overage revenue as their own lines. Reprice when AI cost per unit or tokens per task moves.
:::

## Mistakes that cost margin or trust

:::highlight
Each one shows up in the gross margin line within a quarter.
:::

**Shipping AI free inside the plan with no cap.** The heavy cohort sets your cost, and a flat price does not move with it.

**Setting the price at cost × 2.** That is the floor at a **50%** target. Bessemer calls cost-plus a trap.

**Pricing from average cost.** The example above hits **50%** on average and loses money on each heavy user.

**Selling overage at cost with no plan margin.** GitHub and Cursor can do it because the plan carries margin. Check that yours does.

**Credits with no dollar anchor.** Buyers cannot budget them and procurement slows the deal.

**Switching overnight.** Cursor’s 2025 change ended in an apology and refunds.

**Counting overage as ARR.** Report it as usage revenue next to committed ARR.

This page is operator judgment on pricing design, not legal, tax, or accounting advice.

## Sources

- [Growth Unhinged, The 2026 State of B2B SaaS and AI Monetization Report](https://www.growthunhinged.com/p/the-state-of-b2b-monetization-in-2026). Kyle Poyar, 13 May 2026. **230** B2B software and AI companies. Internal costs and margins the top factor in pricing AI (**54%**); market **36%**; productivity gains **30%**. Median target AI margin about **50%**; **12%** aim for **80%+**; a similar share **20%** or lower (PostHog). AI credits **29%** today; **33%** plan to add within 6 to 12 months; credit models grew **126%** year on year in 2025. Premium edition **50–100%** above base; consumption limits for the top **10%** of power users (top **10%** drive **70%+** of token consumption, in Poyar’s experience). Three in four companies changed pricing or packaging in the past year. Hybrid **37%**.
- [Growth Unhinged, Why everyone’s switching to AI credits](https://www.growthunhinged.com/p/ai-credit-pricing). Kyle Poyar, 3 September 2025. Credit models across Microsoft, Salesforce, Cursor, and OpenAI; credits let vendors include some AI use free and adapt to model costs.
- [Bessemer Venture Partners, The AI pricing and monetization playbook](https://www.bvp.com/atlas/the-ai-pricing-and-monetization-playbook). Atlas Editors, 10 February 2026. Pricing must account for inference costs; **50–60%** AI gross margins vs **80–90%** SaaS; cost-plus (calculate costs, double it) undercharges; platform fee at **2X** delivery costs plus outcome credits; usage caps, prepaid credits, hybrid models, and tiered subscriptions to manage variable compute; Intercom Fin **$0.99** per resolution.
- [Bessemer Venture Partners, Part III: Business model invention in the AI era](https://www.bvp.com/atlas/part-iii-business-model-invention-in-the-ai-era). 5 December 2024. Microsoft Copilot add-on about **$30** on top of Office 365 licenses.
- [The SaaS CFO, What Should Be Included in AI COGS](https://www.thesaascfo.com/what-should-be-included-in-ai-cogs/). Ben Murray, posted 5 May 2026, updated 25 September 2026. AI COGS categories; heavy users **50 to 100** times light users (citing Agicent and SaaStr).
- [GitHub Blog, GitHub Copilot is moving to usage-based billing](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/). Mario Rodriguez, 27 April 2026. Switch on 1 June 2026; credits at published API rates; Pro **$10** with **$10** of credits; Business **$19** and Enterprise **$39** per user unchanged; promotional **$30** and **$70** for June to August; preview bill in early May; pooled usage; admin budgets; quick chat and multi-hour session priced the same under the old model.
- [GitHub Docs, Usage-based billing for individuals](https://docs.github.com/en/copilot/concepts/billing/billing-for-individuals). Base credits plus flex allotment; 1 AI credit = **$0.01**; unused credits expire monthly; **10%** discount with auto model selection.
- [Cursor, Clarifying our pricing](https://cursor.com/blog/june-2025-pricing). Michael Truell, 4 July 2025. Pro: **$20** of frontier usage at API pricing, more at cost; previously **500** requests; hardest requests an order of magnitude costlier; about **225** / **550** / **650** requests at median usage; refunds for 16 June to 4 July.
- [Notion, Introducing Notion AI for Work](https://www.notion.com/blog/notion-ai-for-work). John Hurley, 13 May 2025. AI bundled into Business at **$20** per user per month; existing customers move at first renewal after 13 August 2025.
- [Notion, Pricing](https://www.notion.com/pricing) and [Notion AI](https://www.notion.com/product/ai). Checked 16 October 2026. Custom Agents **$10** per 1,000 Notion credits; credits apply from 4 May 2026; agents pause when credits run out.
- [Salesforce, Salesforce Introduces New Flexible Agentforce Pricing](https://www.salesforce.com/news/press-releases/2025/05/15/agentforce-flexible-pricing-news/). 15 May 2025. Flex Credits **$500** per 100,000; one action 20 credits (**$0.10**); conversations **$2** each.
- [SaaStr, 5 Key Takeaways from ICONIQ’s State of AI Report](https://www.saastr.com/the-execution-era-of-ai-5-key-takeaways-from-iconiqs-state-of-ai-report/). Jason Lemkin, 7 February 2026. ICONIQ January 2026, about **300** executives; inference **20%** to **23%** of spend as products scale; route most tasks to smaller models.
- [VEN (Venture Executive Network)](https://www.venexecs.com/?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library). Founder sessions, 2026. Anchor price to the buyer’s current cost of the problem; know variable cost per unit of work so outcome pricing does not invert margin. Not a survey. No closed-session numbers.

## Related

- [Go-to-market](/library/gtm/)
- [Seat vs usage vs outcome pricing for AI SaaS](/library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas/)
- [AI SaaS gross margin: inference COGS in the board pack](/library/finance/ai-gross-margin-inference-cogs/)
- [AI gross margin calculator](/tools/ai-gross-margin-calculator/)
- [Does usage revenue count as ARR?](/library/finance/usage-revenue-as-arr/)
- [How to convert a pilot to a paid contract](/library/gtm/pilot-to-paid-contract/)
- [How to negotiate your first customer contract](/library/gtm/first-customer-contract/)
