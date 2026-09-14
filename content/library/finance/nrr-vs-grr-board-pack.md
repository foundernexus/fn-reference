---
title: NRR vs GRR for the board pack
description: NRR asks whether existing customers grow revenue. GRR asks how much you keep with zero expansion. Put both on the board slide with cited bands. Do not mask a leaky base.
slug: nrr-vs-grr-board-pack
section: library
cluster: finance
layout: article
target_query: nrr vs grr saas
date: 2026-09-14
close: Retention is a board-visible call. If you want founders who just walked GRR and NRR through a raise or a board pack to pressure-test your cohort definitions, that conversation happens at FounderNexus.
disclaimer: not-legal-tax
draft: false
related:
- library/finance/burn-multiple-vs-rule-of-40
- tools/magic-number-cac-payback-calculator
- tools/runway-calculator
---

GRR answers how much recurring revenue you keep from a starting cohort with zero credit for expansion. NRR answers whether that same cohort’s revenue grows after expansion, contraction, and churn. Boards need both. NRR alone can hide a leaky base. Not legal, tax, or investment advice.

:::takeaways
- NRR = (Starting MRR + Expansion + Reactivation − Contraction − Churn) / Starting MRR. Can exceed 100%. Also called NDR.
- GRR = (Starting MRR − Contraction − Churn) / Starting MRR. Capped at 100%. Never counts expansion. Also called GDR.
- Same cohort only. Exclude new logos mid-period. For that cohort, NRR ≥ GRR always.
- SaaS Capital (2023, >$1M ARR): median NRR 102%, median GRR 91%. Table stakes: GRR at least ~90%. ChartMogul Dec 2025 (~3,500 software cos): median B2B SaaS NRR 82%, top quartile 97%. Different samples. Show separately.
- Put GRR, NRR, and growth on one board page (Keith Wallington). A 70% GRR with 115% NRR is a leaky base covered by expansion.
:::

## Two different board questions

:::highlight
GRR is the leak check. NRR is the expansion-plus-retention read.
:::

| Metric | Board question | Expansion? | Ceiling |
| --- | --- | --- | --- |
| GRR (gross revenue / dollar retention) | How much revenue would we keep with zero expansion? | No | 100% |
| NRR (net revenue / dollar retention) | Is revenue from existing customers growing overall? | Yes | None (can exceed 100%) |

Do not compare your GRR to someone else’s NRR. Same cohort, same period, same publisher bands.

## Formulas and a worked example

:::highlight
ChartMogul movement formulas. Same starting cohort. No new logos mid-window.
:::

| | NRR | GRR |
| --- | --- | --- |
| Formula | (Starting MRR + Expansion + Reactivation − Contraction − Churn) / Starting MRR | (Starting MRR − Contraction − Churn) / Starting MRR |
| Counts expansion / reactivation | Yes | No |
| Can exceed 100% | Yes | No |
| Source | [ChartMogul NRR](https://chartmogul.com/saas-metrics/nrr/) · updated 8 Sep 2026 | [ChartMogul GRR](https://chartmogul.com/saas-metrics/grr/) · updated 8 Sep 2026 |

**Labeled ChartMogul-style example (not your company).** Start with $770 MRR from four paying customers. Later, the same cohort is at $800 MRR after expansion, churn, and contraction → **NRR = 800 / 770 = 103.9%**. Excluding expansion, remaining MRR from that cohort is $630 → **GRR = 630 / 770 = 81.8%**. Same cohort. NRR sits above GRR because expansion only ever adds.

## Why boards need both

:::highlight
Strong NRR with weak GRR is a masking story, not a retention win.
:::

Keith Wallington (quoted on ChartMogul’s GRR page): chart GRR, NRR, and growth on one page for a board meeting. That frame forces the full customer journey. New business. Retention. Upsell.

ChartMogul’s masking warning: **70% GRR with 115% NRR** means a leaky base covered by expansion. Diligence cares about that. So should your board. Fix GRR leaks before you celebrate NRR.

Bessemer’s Atlas churn piece: net dollar retention should be 100%+. Customer success North Star is net retention. That is the NRR bar. It does not replace the GRR leak check.

## Cited benchmarks (do not average)

:::highlight
Three publishers. Different samples and years. Keep the rows separate.
:::

### SaaS Capital Research Brief 28 (2023)

Survey of private B2B SaaS; retention cuts exclude companies with less than $1M ARR unless noted.

| Cut | Median NRR | Median GRR |
| --- | --- | --- |
| All surveyed SaaS (>$1M ARR) | 102% (unchanged vs 2022) | 91% (unchanged vs 2022) |
| ACV <$12k | ~100% | ~90% |
| ACV $12–25k | ~102% | ~90% |
| ACV $25–50k | ~103% | ~92% |
| ACV $50–100k | ~105% | ~93% |
| ACV $100–250k | ~107% | ~93% |
| ACV >$250k | ~110% | ~93% |

Source: [SaaS Capital, Research Brief 28 — 2023 B2B SaaS Retention Benchmarks](https://www.saas-capital.com/wp-content/uploads/2023/05/RB28WS1-2023-B2B-SaaS-Retention-Benchmarks.pdf) (Figure 1 and conclusions).

Other SaaS Capital lines from the same brief:

- Table stakes: GRR must be at least ~90% for a shot at peer parity.
- ACV >$25k: median GRR ~93%. Below $25k: ~90%.
- Top-quartile ACV >$100k: NRR 118–120%.
- Population median growth (>$1M ARR): **34%**. Companies with NRR ≥110% grew above that median; companies with NRR below 100% grew below it.
- Benchmark to target for that median growth rate of 34%: **NRR of at least 100%** (their words). Median NRR in the survey is already 102%.
- Moving NRR from the 90–100% band to the 100–110% band improves growth ~9 percentage points. Highest-NRR cohort median growth is about double the population median (~34%).

### Bessemer segment aims (State of the Cloud 2019)

Aims by customer segment, not a survey median table.

| Segment | ACV | GRR aim | NRR aim |
| --- | --- | --- | --- |
| SMB | <$12k | 70–80% | 80–100% |
| Mid-market | $12–50k | 80–90% | 90–120% |
| Enterprise | $50k+ | >90% | >100% |

Source: [Bessemer, State of the Cloud 2019](https://www.bvp.com/atlas/state-of-the-cloud-2019) (6 Feb 2019).

Bessemer *Scaling to $100 Million*: strong retention often cited as ~85%+ gross and ~120%+ net across lifetimes. Net retention ranges they publish include ~105–145% at $1–10M ARR and ~105–125% at $100M+; middle 50% still >100%. Average net ~140% at $1–10M then ~120% at $10–100M+. Mindbody IPO ~109% NRR on ~$2k ACV vs Okta 123% on $50k+ ACV. Different framing from SaaS Capital’s 2023 medians. Show both; do not blend.

### ChartMogul Dec 2025 (separate sample)

| Cut | NRR |
| --- | --- |
| Median B2B SaaS (~3,500 software companies analysis) | 82% |
| Top quartile B2B SaaS | 97% |

Source: [ChartMogul NRR page](https://chartmogul.com/saas-metrics/nrr/) (updated 8 Sep 2026; cites Dec 2025 analysis). This is a different sample than SaaS Capital’s private B2B survey. Do not average 82% with 102%.

**Best-in-class GRR (ChartMogul):** over 86% at any stage (lose ~14% gross revenue per year). From the [ChartMogul GRR page](https://chartmogul.com/saas-metrics/grr/) / guide. SaaS Capital’s peer-parity floor (~90%) is a different publisher’s bar. Label which one you mean on the slide.

## What to put on the board slide

:::highlight
Period, cohort definition, GRR + NRR + growth. No blended publisher averages.
:::

1. **Period.** Usually trailing 12 months. If you use a quarter, say so and keep it consistent.
2. **Cohort.** Starting customers only. No new logos mid-period. Say whether you use MRR or ARR.
3. **GRR and NRR side by side** for that cohort, plus **growth** (Wallington).
4. **Trend.** Last 4–8 quarters if you have them. One heroic month is noise.
5. **ACV or segment label** so the board picks the right Bessemer / SaaS Capital band.
6. **Publisher footnotes.** “SaaS Capital 2023 median” is not “ChartMogul Dec 2025 median.” Never average them into one target.

## Labeled board sketches

:::highlight
Round numbers so the arithmetic is visible. Not a company.
:::

**Sketch A — healthy mid-market.** Starting cohort MRR $1,000k. Contraction $40k, churn $50k, expansion $120k, reactivation $0. GRR = (1000 − 40 − 50) / 1000 = **91%**. NRR = (1000 + 120 − 40 − 50) / 1000 = **103%**. Near SaaS Capital’s overall medians. Board talk: hold GRR above ~90% and push expansion without buying it with discounts that later contract.

**Sketch B — masked leak.** Starting $1,000k. Contraction $80k, churn $220k, expansion $350k. GRR = **70%**. NRR = **105%**. Looks “fine” on net. ChartMogul’s 70% / 115%-style warning applies. Board talk: stop celebrating NRR until GRR recovers.

**Sketch C — enterprise expansion engine.** Starting $1,000k. Contraction $30k, churn $40k, expansion $200k. GRR = **93%**. NRR = **113%**. Sits near SaaS Capital’s higher-ACV medians and above Bessemer’s enterprise NRR floor (>100%). Board talk: protect GRR while expansion compounds.

## Mistakes that waste a board meeting

:::highlight
Wrong cohort, mixed acronyms, and averaged publishers are the usual failures.
:::

**Showing only NRR.** Expansion can paper over churn. Bring GRR.

**Mixing GRR and NRR labels.** GDR/NDR are the same metrics under dollar names. Compare like with like.

**Including new logos in the retention cohort.** That inflates both numbers and is not retention.

**Averaging SaaS Capital 102% with ChartMogul 82% into “aim for 92%.”** Different samples. Pick the band that matches your ACV and say which source.

**Treating Bessemer 2019 segment aims as 2023 survey medians.** Aims ≠ medians.

**Declaring victory at 100% NRR while GRR sits at 75%.** Wallington’s three-line slide (GRR, NRR, growth) surfaces that faster than a single vanity net number.

## Sources

- [ChartMogul, Net Revenue Retention (NRR)](https://chartmogul.com/saas-metrics/nrr/) — updated 8 Sep 2026. Movement formula; $770 → $800 = 103.9% example; NRR ≥ GRR; NDR alias; Dec 2025 median B2B SaaS NRR 82% / top quartile 97%.
- [ChartMogul, Gross Revenue Retention (GRR)](https://chartmogul.com/saas-metrics/grr/) — updated 8 Sep 2026. Movement formula; $770 → $630 excl. expansion = 81.8%; 100% cap; 70% GRR / 115% NRR masking example; best-in-class GRR >86%; Keith Wallington board-page quote.
- [SaaS Capital, Research Brief 28: 2023 B2B SaaS Retention Benchmarks (PDF)](https://www.saas-capital.com/wp-content/uploads/2023/05/RB28WS1-2023-B2B-SaaS-Retention-Benchmarks.pdf) — 2023. Overall medians 102% NRR / 91% GRR; ACV table; ≥90% GRR table stakes; growth vs NRR bands; target NRR ≥100% for median 34% growth.
- [Bessemer Venture Partners, State of the Cloud 2019](https://www.bvp.com/atlas/state-of-the-cloud-2019) — 6 Feb 2019. SMB / mid-market / enterprise GRR and NRR aims by ACV.
- [Bessemer Venture Partners, Scaling to $100 Million](https://www.bvp.com/atlas/scaling-to-100-million) — Strong retention ~85%+ gross / ~120%+ net framing; net retention ranges by ARR band; Mindbody vs Okta ACV contrast.
- [Bessemer Venture Partners, Understanding churn](https://www.bvp.com/atlas/understanding-churn-and-building-an-action-plan-to-fix-the-proverbial-leaky-bucket) — Net dollar retention should be 100%+; CS North Star is net retention.

## Related

- [Burn multiple vs Rule of 40](/library/finance/burn-multiple-vs-rule-of-40/)
- [Magic number & CAC payback calculator](/tools/magic-number-cac-payback-calculator/)
- [Runway calculator with hiring plan](/tools/runway-calculator/)
