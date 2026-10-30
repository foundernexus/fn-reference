---
title: "AI gross margin calculator: inference COGS and cost per user"
description: Enter monthly revenue, classic COGS, and each AI delivery cost. Get AI-inclusive gross margin beside software margin ex-AI, AI cost per user, a heavy-user cohort read, the R&D misclassification swing, and the AI budget that hits your target. Bands cited by source. Not advice.
slug: ai-gross-margin-calculator
section: tools
cluster: finance
layout: calculator
calculator_js: ai-gross-margin-calculator.js
target_query: AI gross margin calculator
date: 2026-10-15
updated: 2026-10-30
close: Founders who have walked a low AI margin and a credible path up through a raise will pressure-test your COGS map and target in a VEN session.
disclaimer: not-legal-tax
draft: false
related:
- library/finance/ai-gross-margin-inference-cogs
- tools/magic-number-cac-payback-calculator
- library/finance/usage-revenue-as-arr
- library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas
- library/gtm/price-ai-features-inference-cost
- library/finance/burn-multiple-vs-rule-of-40
---

Type one month of revenue, your classic COGS, and each AI delivery cost. The calculator returns your AI-inclusive gross margin with software gross margin ex-AI beside it, AI cost as a share of revenue, AI cost per active user or per workflow, and whether your heaviest users pay for their own inference. It also shows how far the margin moves if you book AI spend to the wrong bucket. Then set a target margin and it tells you the AI budget, the cost per user, and the revenue lift that hit it. Read the result against the band for your product type from The SaaS CFO. Not legal, tax, or investment advice. Confirm classification with your CPA or auditor.

:::takeaways
- AI-inclusive gross margin = (revenue − classic COGS − AI delivery COGS) ÷ revenue. AI delivery COGS covers production inference, production GPU serving, the AI infrastructure layer, AI monitoring, and AI support (Murray), plus human review of customer outputs (a16z).
- Pick the band for your product type. Ben Murray (The SaaS CFO, 2026): AI-native **50–65%** at maturity, early-stage AI-native often **25–30%**, AI-enabled SaaS **72–85%**, traditional SaaS **70–80%**.
- The gap between ex-AI and AI-inclusive margin equals AI cost as a share of revenue. Mavvrik and Benchmarkit (2025, N=**372**): **84%** report more than **6** points of erosion, and **26%** report **16** or more.
- There is no reliable public benchmark yet for AI cost per active user or per workflow. Use the calculator to set your own budget per unit and track the trend.
:::

## What the calculator returns

:::highlight
The first six rows describe this month. The last two solve for your target.
:::

| Output | Formula | Read it against |
| --- | --- | --- |
| AI-inclusive gross margin | (revenue − classic COGS − AI COGS) ÷ revenue | Murray’s band for your product type |
| Software gross margin ex-AI | (revenue − classic COGS) ÷ revenue | Classic SaaS bands |
| AI delivery cost % of revenue | AI COGS ÷ revenue | Mavvrik and Benchmarkit erosion shares |
| AI COGS per user or workflow | AI COGS ÷ units this month | Your own trend |
| Heavy cohort AI share | Cohort AI COGS ÷ cohort revenue | 100% means the cohort loses money before classic COGS |
| Margin with dev/test in COGS | AI-inclusive margin minus test inference ÷ revenue | Shows what a shared API account does to the slide |
| AI budget at target | revenue × (1 − target) − classic COGS | Your current AI COGS |
| Revenue lift to hit target | total COGS ÷ (1 − target) ÷ revenue − 1 | Your pricing plan, with costs held flat |

The cost lines map to the COGS table on [AI SaaS gross margin: inference COGS in the board pack](/library/finance/ai-gross-margin-inference-cogs/). Training, fine-tuning, dev/test inference, and staff AI tools stay out of the AI COGS fields. They belong in R&D or the department that uses them (Murray).

## Which band to read against

:::highlight
Choose one product type and say why. Publishers that disagree stay on separate rows.
:::

The calculator reads your margin against one publisher’s bands so the verdict stays consistent.

| Product type (Murray) | Gross margin band |
| --- | --- |
| AI-native, at maturity | **50–65%** |
| AI-native, early stage | Often **25–30%** |
| AI-enabled SaaS | **72–85%** |
| Traditional SaaS | **70–80%** |

Murray defines AI-native as a product where inference is core to value delivery and each interaction carries a compute cost. AI-enabled means traditional SaaS with AI features added. Your spot inside the AI-enabled band depends on AI intensity and whether you charge for AI usage.

Other publishers measured different samples. Quote them by name and keep them out of the verdict.

| Publisher | Figure |
| --- | --- |
| a16z, 2020 (founder interviews) | AI often **50–60%** vs **60–80%+** for comparable SaaS |
| Bessemer State of AI, 2025 (20 startups) | Shooting Stars **~60%**; Supernovas **~25%**, often negative |
| ICONIQ via SaaStr, 2026 (about **300** executives) | AI product average **41%** in 2024, **52%** projected for 2026 |

## The example behind the defaults

:::highlight
Editorial example with round numbers. Not a company and not a benchmark.
:::

An AI support product books **$500k** of revenue in a month. Classic COGS is **$75k**. AI delivery costs are **$80k** inference, **$15k** vector database and retrieval, **$5k** monitoring, and **$10k** AI-tagged support, for **$110k**. It has **10,000** active users. Its heaviest **1,000** users bring in **$60k** and drive **$50k** of AI COGS. Engineers run **$30k** of test inference on the production account.

| Read | Result |
| --- | --- |
| Software gross margin ex-AI | **85%** |
| AI-inclusive gross margin | **63%**, inside Murray’s AI-native band |
| AI delivery cost % of revenue | **22%**, in Mavvrik’s 16-points-or-more group |
| AI COGS per active user | **$11.00** per month |
| Heavy cohort AI share | **83.3%** of cohort revenue |
| Margin with dev/test in COGS | **57%** |

Set a **65%** target, the top of Murray’s AI-native maturity band. The AI budget becomes **$100k**, so this company is **$10k** over. That is **$10.00** of AI COGS per user instead of **$11.00**. Holding costs flat, revenue would need to rise **5.7%**.

## Reading a low number

:::highlight
Explain the variable cost and show the path up before the board asks.
:::

Founders in a [VEN](https://www.venexecs.com/?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library) session agreed on one rule: investors accept a low AI-native margin when you can explain the variable cost and show a credible path up. That is session judgment, not a survey.

Murray names two levers. Pricing discipline: companies that package and charge for AI usage have better margins than those that absorb it into the base subscription. Model routing: send most tasks to smaller, cheaper models and escalate only the hard cases to frontier models. Bessemer’s pricing playbook adds a third. Each AI query has a real compute cost, so track true costs from day one and price to cover them.

The calculator gives you the numbers for each lever. The heavy-cohort line tells you where usage pricing or caps would land. The per-user budget at target is the ceiling for routing work. The revenue lift tells you how far a price change has to go if costs stay put. The [seat vs usage vs outcome pricing](/library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas/) page compares the pricing models. To turn the per-user budget into a price, an allowance, and an overage rate, use [how to price AI features to cover inference cost](/library/gtm/price-ai-features-inference-cost/).

## Before you put the number in the board pack

:::steps Board-pack check
1. **Split the accounts.** Separate production and development AI accounts. Murray: without the split, every later step is unreliable. Then set the dev/test field to zero.
2. **Fill all six AI lines.** Include the infrastructure layer. Mavvrik and Benchmarkit found data platform usage (**56%**) and network access to models (**52%**) ahead of LLM tokens (**37%**) as sources of unexpected AI cost.
3. **Write the cohort cut.** Pick the heavy-user definition once and keep it month to month.
4. **Name the unit.** Active user or completed workflow. Use the same unit in the deck, model, and board pack.
5. **Pick the band and say why.** AI-native or AI-enabled, with one sentence on how much of delivery runs on inference.
6. **Show both margins.** AI-inclusive as the headline, ex-AI beside it, AI cost share under them.
7. **Rerun the downstream metrics.** Put the AI-inclusive margin into the [magic number and CAC payback calculator](/tools/magic-number-cac-payback-calculator/) and recheck [burn multiple](/library/finance/burn-multiple-vs-rule-of-40/).
:::

## Mistakes

- Typing training or fine-tuning runs into the inference field. Murray puts them in R&D or capitalizes them under ASC 350-40 with your auditor.
- Leaving the AI infrastructure layer at zero because only the model API bill reached finance.
- Comparing an AI-native product to the **70–80%** traditional SaaS benchmark.
- Averaging Bessemer’s Supernova **~25%** with ICONIQ’s **52%** into one target.
- Quoting a per-user AI cost against a peer. There is no reliable public benchmark yet. Compare against your own last six months.
- Solving for the target by moving costs to R&D. Restate past months on the new rule and tell the board first.

## Sources

- [The SaaS CFO, What Should Be Included in AI COGS](https://www.thesaascfo.com/what-should-be-included-in-ai-cogs/). Ben Murray, posted 5 May 2026, updated 25 September 2026. Five AI COGS categories; production vs development account split; training under ASC 730 or ASC 350-40; heavy users **50 to 100** times light users (citing Agicent); AI-native **50–65%** at maturity, early-stage AI-native often **25–30%**, AI-enabled **72–85%** (citing SaaStr and KnowledgeLib); traditional SaaS **70–80%**; pricing discipline and model routing levers.
- [Andreessen Horowitz, The New Business of AI (and How It’s Different From Traditional Software)](https://a16z.com/the-new-business-of-ai-and-how-its-different-from-traditional-software/). Martin Casado and Matt Bornstein, 16 February 2020. AI gross margins often **50–60%** vs **60–80%+** for comparable SaaS; humans in the loop lower gross margin.
- [Bessemer Venture Partners, The State of AI 2025](https://www.bvp.com/atlas/the-state-of-ai-2025). 13 August 2025. **20** high-growth AI startups; Supernovas **~25%** average gross margin, often negative; Shooting Stars **~60%**.
- [Bessemer Venture Partners, The AI pricing and monetization playbook](https://www.bvp.com/atlas/the-ai-pricing-and-monetization-playbook). Atlas Editors, 10 February 2026. Every AI query incurs real compute costs; track true costs from day one and price to cover compute.
- [SaaStr, AI Gross Margins Are Up, R&D Spend Is Way Up, AI Pricing is a Mess: 5 Key Takeaways from ICONIQ’s State of AI Report](https://www.saastr.com/the-execution-era-of-ai-5-key-takeaways-from-iconiqs-state-of-ai-report/). Jason Lemkin, 7 February 2026. ICONIQ State of AI (January 2026), about **300** executives; average AI product gross margin **41%** in 2024, **52%** projected for 2026.
- [Mavvrik and Benchmarkit, 2025 State of AI Cost Governance (PDF)](https://www.mavvrik.ai/wp-content/uploads/State-of-AI-Cost-Governance-2025_FINAL.pdf). 2025. N=**372**; **84%** report more than **6** points of gross margin erosion from AI delivery costs, **26%** report **16** points or more; data platform usage **56%**, network access to models **52%**, LLM tokens **37%** as unexpected AI costs.
- [VEN (Venture Executive Network)](https://www.venexecs.com/?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library). Founder session. A low AI-native margin is acceptable when the variable-cost story is clear and the path up is credible. Session judgment, not a survey.
