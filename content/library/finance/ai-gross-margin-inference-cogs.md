---
title: "AI SaaS gross margin: inference COGS in the board pack"
description: Classic SaaS gross margin bands assume delivery is almost free. Put production inference, GPU serving, retrieval, AI monitoring, and AI support in COGS. Keep training, dev/test inference, and internal AI tools in R&D or OpEx. Show AI gross margin as its own board line with one written definition.
slug: ai-gross-margin-inference-cogs
section: library
cluster: finance
layout: article
target_query: AI SaaS gross margin
date: 2026-10-13
close: Founders who have defended an AI gross margin line through a board pack and a raise will pressure-test your COGS map in a FounderNexus session.
disclaimer: not-legal-tax
draft: false
related:
- library/finance
- library/finance/usage-revenue-as-arr
- library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas
- library/finance/burn-multiple-vs-rule-of-40
- library/finance/nrr-vs-grr-board-pack
- library/fundraising/series-a-diligence-checklist
- tools/magic-number-cac-payback-calculator
---

If inference is core to how you deliver the product, the classic SaaS gross margin benchmark does not apply to you. Ben Murray (The SaaS CFO, 2026) says his 70% to 80% benchmark is for traditional SaaS and does not apply to AI-native or heavily AI-featured products. Put production inference, GPU serving for production, vector databases and retrieval serving customer queries, AI monitoring, AI support, and human review of customer outputs in COGS. Training, fine-tuning, dev/test inference, and internal AI tools go to R&D or the department that uses them. Then show AI gross margin as its own line in the board pack and write the definition down once. Not legal, tax, or investment advice. Confirm classification with your CPA or auditor.

:::takeaways
- The COGS rule has not changed: costs to deliver the product go to COGS, costs to build it go to R&D (Murray). Split production and development AI accounts first. Murray: if engineers test models in the production account, you cannot split the costs.
- Published AI bands sit below classic SaaS and disagree with each other. a16z (2020): often **50–60%** vs **60–80%+** for comparable SaaS. Bessemer (2025): Shooting Stars **~60%**, Supernovas **~25%**, often negative. ICONIQ via SaaStr (2026): average AI product gross margin **41%** in 2024, **52%** projected for 2026. Show each on its own row.
- Mavvrik and Benchmarkit (2025, N=**372**): **84%** of companies report AI delivery costs cutting product gross margin by more than **6** points. **26%** see **16** points or more.
- Board pack: AI-inclusive gross margin as the headline, software gross margin ex-AI beside it, AI delivery cost as a share of revenue, cost per active user or per workflow, and a heavy-user cohort line.
- There is no reliable public benchmark yet for AI cost per active user or per workflow. Track your own trend and label the unit.
:::

## What goes in AI COGS and what stays in R&D

:::highlight
Classify by purpose. The same OpenAI or Anthropic invoice can land in both buckets.
:::

| Cost | Where it goes | What it covers |
| --- | --- | --- |
| Production inference (customer-facing) | COGS | Model API calls that answer customers: OpenAI, Anthropic, Gemini, Azure OpenAI, Bedrock |
| GPU compute for production serving | COGS | Self-hosted or fine-tuned models served to customers |
| AI infrastructure layer serving customers | COGS | Vector databases, embeddings, RAG pipelines, orchestration, caching, AI-driven data platform use, egress to model providers |
| AI monitoring and observability | COGS | Tracing, evals, guardrails, cost attribution on production traffic |
| AI-related support | COGS | Incremental support hours on AI-tagged tickets |
| Human review of customer outputs | COGS | People who check or correct AI output before the customer gets it |
| Dev/test inference | R&D | Engineering exploration and prompt testing |
| Model training and fine-tuning | R&D, or capitalized under ASC 350-40 | Training runs and the GPU time behind them; ask your auditor |
| Internal AI tools | The department that uses them | Copilot, ChatGPT, and similar seats for your own staff |

Rows from The SaaS CFO (Ben Murray, posted 5 May 2026, updated 25 September 2026), except human review, which follows a16z’s description of humans in the loop as a gross margin cost. Murray’s classification test: under U.S. GAAP it depends on the nature and purpose of the activity. Training generally falls under ASC 730 (expensed R&D) or ASC 350-40 (internal-use software, potentially capitalizable). He flags FASB’s ASU 2025-06, which modernizes ASC 350-40 for fiscal years beginning after 15 December 2027.

One line needs a written call. a16z found many AI companies spend up to **10–15%** of revenue capturing and labeling new data to keep models accurate after launch. Murray puts training in R&D. a16z tells founders to measure their real variable costs and not let them hide in R&D. If your labeling or retraining scales with customer volume, decide which bucket it belongs in, write the reason down, and tell the board which way you went.

## Why AI gross margins sit below classic SaaS

:::highlight
Each request costs compute, and heavy users cost more. Read each published band against its own sample.
:::

| Source | Date | Sample | AI gross margin | Classic SaaS comparison |
| --- | --- | --- | --- | --- |
| a16z (Casado and Bornstein) | 16 Feb 2020 | Interviews with AI startup founders | Often **50–60%** | **60–80%+** for comparable SaaS |
| Bessemer State of AI 2025 | 13 Aug 2025 | 20 high-growth AI startups | Shooting Stars **~60%**; Supernovas **~25%**, often negative | Shooting Stars slightly below SaaS peers |
| Bessemer AI pricing playbook | 10 Feb 2026 | Atlas editors | **50–60%** | **80–90%** for SaaS |
| ICONIQ State of AI, via SaaStr | Jan 2026 report; SaaStr 7 Feb 2026 | About **300** executives at software companies building AI products | Average AI product gross margin **41%** in 2024, **52%** projected for 2026 | Not stated |
| The SaaS CFO (Murray) | Updated 25 Sep 2026 | Practitioner framework citing SaaStr and KnowledgeLib | AI-native **50–65%** at maturity; early-stage AI-native often **25–30%**; AI-enabled SaaS **72–85%** | **70–80%** for traditional SaaS |

Do not average these rows. a16z’s AI figure comes from founder interviews in 2020. Bessemer’s Supernovas are ten companies that reached about **$40M** ARR in their first year of commercialization, and Bessemer says many trade margin for distribution. ICONIQ reports averages from a survey, and SaaStr adds that companies combining model and product work reported **53%** while pure application-layer companies reported **45%**.

a16z put cloud spend at **25%** of revenue or more for many AI companies. Murray cites estimates that heavy users can cost **50 to 100** times more than light users, and that reasoning models and agentic workflows generate **10 to 100** times more tokens per task than 2023-era completions. Net cost per task can rise while token prices fall. In the Mavvrik and Benchmarkit survey, data platform usage (**56%**) and network access to models (**52%**) were the top sources of unexpected AI costs. LLM token costs ranked fifth at **37%**. If you map only the model API bill, your COGS is short.

## How to present it in the board pack

:::highlight
Lead with the AI-inclusive number. Put the ex-AI number beside it so the board can see what AI costs you.
:::

| Line | Definition | Why the board needs it |
| --- | --- | --- |
| AI-inclusive gross margin | Revenue minus all COGS, including the AI delivery lines in the table above | The number investors rebuild in diligence |
| Software gross margin (ex-AI) | Revenue minus classic COGS only: hosting, support, success, DevOps | Shows the base business against classic SaaS bands |
| AI delivery cost as % of revenue | Inference, production GPU, AI infrastructure layer, monitoring, and AI support over revenue | The trend line for model routing and pricing work |
| Cost per active user or per workflow | AI COGS over active users or completed workflows; name the unit | Unit economics you can price against |
| Heavy-user cohort | AI COGS and revenue for your heaviest users, with the cohort cut written down | Shows whether the top of the usage curve loses money |

The layering follows Murray: AI lines go on top of your existing COGS stack, and he lists cost per active user, cost per request, and whether your heaviest users are still profitable as the checks to run. There is no reliable public benchmark yet for cost per active user or per workflow in AI SaaS, so show your own trend and do not quote a peer band.

If customers pay for usage, the margin read and the [ARR read](/library/finance/usage-revenue-as-arr/) belong on the same page. Usage priced above cost lifts revenue and AI COGS together. Usage you absorb inside a flat subscription shows up only as margin erosion.

## A labeled example

:::highlight
Editorial example with round numbers. Not a company and not a benchmark.
:::

An AI support product books **$500k** of revenue in a month. Classic COGS (hosting, support, customer success) is **$75k**. AI delivery costs are **$80k** inference, **$15k** vector database and retrieval, **$5k** monitoring, and **$10k** AI-tagged support, for **$110k** total.

| Line | Amount | Result |
| --- | --- | --- |
| Software gross margin (ex-AI) | $500k − $75k | **85%** |
| AI-inclusive gross margin | $500k − $75k − $110k | **63%** |
| AI delivery cost as % of revenue | $110k ÷ $500k | **22%** |
| AI COGS per active user (10,000 users) | $110k ÷ 10,000 | **$11** per month |
| Heavy-user cohort (1,000 users) | $50k of the inference bill against $60k of cohort revenue | Inference alone takes **83%** of that cohort’s revenue |

Book all AI spend in R&D and the slide says **85%**. Put **$30k** of engineering test inference in the same API account and book it to COGS, and the slide says **57%**. The **63%** describes the business, and it is the number a diligence team will reach.

## Mistakes that cost trust

:::highlight
Each mistake below moves the margin, and diligence teams catch the move.
:::

**Hiding inference in R&D.** a16z’s advice to AI founders: track down your real variable costs and do not let them hide in R&D.

**Running dev and production on one API account.** Murray calls this the first fix. Without the split, you cannot classify the rest.

**Comparing yourself to an 80% SaaS band.** Murray says a 70% gross margin for an AI-enabled product may be excellent, but only if AI costs are mapped to COGS.

**Averaging publishers.** Bessemer’s Supernova **~25%** and ICONIQ’s **52%** describe different samples. Quote each with its source.

**Showing one blended margin.** Heavy users can cost far more than light users (Murray). Without a cohort line, the board cannot see whether growth in your top accounts helps or hurts.

**Forecasting on token price alone.** Murray: token prices keep falling while tokens per task rise. Model cost per task.

**Reclassifying mid-raise.** If you move a cost between COGS and R&D, restate past periods on the new rule and tell the board before an investor sees the change.

## Lock the definition before the board meeting or the raise

:::highlight
Murray’s action list, in order, with the board steps added at the end.
:::

:::steps AI gross margin definition lock
1. **Split production and development AI accounts.** Separate API keys, projects, and GPU clusters for customer traffic and engineering work (Murray).
2. **Separate internal AI use from product AI use.** Staff tools go to the department that uses them (Murray).
3. **Open the GL accounts.** Inference, model hosting, AI infrastructure layer, AI monitoring, and AI support, tagged to DevOps or an AI COGS cost center (Murray).
4. **Classify each line.** Use the table above. Write your training and labeling position, and agree any capitalization with your auditor.
5. **Segment heavy users.** Calculate AI cost per user and per workflow, split average users from power users (Murray).
6. **Price or absorb.** Decide whether you charge for AI usage. Murray: companies that package and charge for AI usage have better margins than those that absorb it. See [seat vs usage vs outcome pricing](/library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas/).
7. **Write one policy.** One page: which costs sit in COGS, the cohort cut, the per-unit denominator. Use it in the deck, model, board pack, and data room.
8. **Restate the trend.** Rebuild prior months on the new rule so the board sees one consistent line.
9. **Dry-run with the board.** Walk one board member or an outside finance lead from the headline margin to the GL accounts before the meeting.
:::

## How gross margin moves your other board metrics

:::highlight
A gross margin change shows up in burn, payback, and the ARR story.
:::

Gross margin sits upstream of burn. Burn multiple divides net burn by net new ARR (Sacks), and margin you lose to inference adds to net burn. See [burn multiple vs Rule of 40](/library/finance/burn-multiple-vs-rule-of-40/). CAC payback measured on gross margin stretches when margin drops, so run the [magic number and CAC payback calculator](/tools/magic-number-cac-payback-calculator/) on the AI-inclusive figure.

Pricing sets how much of the cost you pass through. Bessemer’s pricing playbook says every AI query incurs real compute costs and tells founders to track true costs from day one and price to cover compute. Your ARR definition decides which of that usage revenue counts as ARR ([usage revenue as ARR](/library/finance/usage-revenue-as-arr/)). Retention slides stay on committed revenue ([NRR vs GRR](/library/finance/nrr-vs-grr-board-pack/)).

In diligence, the gross margin bridge goes in the financials folder next to the ARR schedules on the [Series A diligence checklist](/library/fundraising/series-a-diligence-checklist/). Bring the COGS map, the account split, and the restated trend.

## Sources

- [The SaaS CFO, What Should Be Included in AI COGS](https://www.thesaascfo.com/what-should-be-included-in-ai-cogs/). Ben Murray, posted 5 May 2026, updated 25 September 2026. COGS vs OpEx table (production inference, dev/test inference, training and fine-tuning, production vs training GPU, vector DB, internal AI tools); separate production and development AI accounts; ASC 730 and ASC 350-40; ASU 2025-06 for fiscal years beginning after 15 December 2027; five AI COGS categories and GL accounts; heavy users **50 to 100** times light users and **10 to 100** times more tokens per task (citing Agicent and SaaStr); 70% to 80% traditional SaaS benchmark does not apply to AI-native products; AI-native **50–65%** at maturity, early-stage **25–30%**, AI-enabled **72–85%** (citing SaaStr and KnowledgeLib); pricing discipline; action list.
- [Andreessen Horowitz, The New Business of AI (and How It’s Different From Traditional Software)](https://a16z.com/the-new-business-of-ai-and-how-its-different-from-traditional-software/). Martin Casado and Matt Bornstein, 16 February 2020. AI gross margins often **50–60%** vs **60–80%+** for comparable SaaS; cloud **25%** of revenue or more; up to **10–15%** of revenue on data labeling for model maintenance; humans in the loop lower gross margin; do not let variable costs hide in R&D. AI estimates from founder interviews; software estimates from publiccomps.com.
- [Bessemer Venture Partners, The State of AI 2025](https://www.bvp.com/atlas/the-state-of-ai-2025). Kent Bennett, Talia Goldberg, Janelle Teng Wade, and others, 13 August 2025. **20** high-growth AI startups; ten Supernovas at **~$40M** first-year ARR with **~25%** average gross margin, often negative; Shooting Stars **~60%** average gross margin, slightly lower than SaaS peers.
- [Bessemer Venture Partners, The AI pricing and monetization playbook](https://www.bvp.com/atlas/the-ai-pricing-and-monetization-playbook). Atlas Editors, 10 February 2026. Every AI query incurs real compute costs; **50–60%** gross margins vs **80–90%** for SaaS; track true costs from day one and price to cover compute.
- [SaaStr, AI Gross Margins Are Up, R&D Spend Is Way Up, AI Pricing is a Mess: 5 Key Takeaways from ICONIQ’s State of AI Report](https://www.saastr.com/the-execution-era-of-ai-5-key-takeaways-from-iconiqs-state-of-ai-report/). Jason Lemkin, 7 February 2026. ICONIQ State of AI: Bi-Annual Snapshot (January 2026), about **300** executives; average AI product gross margin **41%** in 2024, **52%** projected for 2026; balanced differentiation **53%**, application layer **45%**.
- [Mavvrik and Benchmarkit, 2025 State of AI Cost Governance (PDF)](https://www.mavvrik.ai/wp-content/uploads/State-of-AI-Cost-Governance-2025_FINAL.pdf). 2025. N=**372**; **84%** report AI delivery costs cutting product gross margin by more than **6** points, **26%** by **16** points or more; data platform usage **56%** and network access to models **52%** top unexpected AI costs, LLM tokens fifth at **37%**.
- [David Sacks, The Burn Multiple (Craft Ventures / Medium)](https://medium.com/craft-ventures/the-burn-multiple-51a7e43cb200). 23 April 2020. Burn multiple = net burn ÷ net new ARR.

## Related

- [Finance, metrics & runway](/library/finance/)
- [Does usage revenue count as ARR?](/library/finance/usage-revenue-as-arr/)
- [Seat vs usage vs outcome pricing for AI SaaS](/library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas/)
- [Burn multiple vs Rule of 40](/library/finance/burn-multiple-vs-rule-of-40/)
- [NRR vs GRR for the board pack](/library/finance/nrr-vs-grr-board-pack/)
- [Series A diligence checklist](/library/fundraising/series-a-diligence-checklist/)
- [Magic number & CAC payback calculator](/tools/magic-number-cac-payback-calculator/)
