---
title: "Should an AI startup file patents? Eligibility, cost, timing"
description: "Patent only if your edge changes how the model runs. Generic ML on new data is ineligible. File a provisional pre-pitch. Median fees: $4,500 then $12,000."
slug: ai-startup-patents-ip
section: library
cluster: gtm
layout: article
target_query: should an AI startup file patents
date: 2026-11-04
close: Founders who have decided what to patent, what to keep secret, and what to leave unprotected will pressure-test your filing plan and your IP paper in a VEN session.
disclaimer: not-legal-tax
draft: false
related:
- library/gtm
- library/gtm/data-moat-ai-startup
- library/gtm/strategic-partnership-ip
- library/fundraising/series-a-diligence-checklist
- library/fundraising/term-sheet-red-flags
- library/equity/founder-vesting-83b
---

Sometimes. File a patent only if your edge changes how the model itself runs, such as training that cuts compute or storage. The USPTO treated that as eligible in *Ex parte Desjardins* (2025). Running a known model on new data or in a new industry is not eligible (*Recentive v. Fox*, Federal Circuit, 2025). If you will pitch, publish, or share the method with a partner in the next 12 months, file a provisional first. Median attorney charges are **$4,500** for a provisional and **$12,000** for a full application on complex software (AIPLA, 2024 charges). Before any of that, get signed assignments from every founder and contractor.

:::takeaways
- Eligibility is the first test. A training or inference method that improves how the model operates can qualify. A known model applied to a new dataset or a new field does not (USPTO; Federal Circuit).
- Say the gain in technical terms: less compute, less storage, lower error. "Saves the operator time" reads as a business benefit (VEN session).
- Disclose nothing important before you file. The US allows one year after your own public disclosure, and other countries may not (USPTO).
- Budget about **$20,000** in attorney charges for a first patent, plus **$1,446** to **$3,615** in USPTO fees through issue. A provisional alone costs about **$4,630** all in at the small-entity rate (AIPLA; USPTO).
- The cheap, urgent work is ownership. Present-tense invention assignments, a log of who conceived what, and trade secret hygiene protect you whether or not you ever file.
:::

This page is for a seed to Series B team deciding whether to spend on a patent. Defensibility from data and feedback loops is on [data moat for AI startups](/library/gtm/data-moat-ai-startup/). Who owns work done with a larger partner is on [strategic partnerships and IP](/library/gtm/strategic-partnership-ip/).

## Match the edge to the protection

:::highlight
Ask what a competitor would copy, and which tool covers that.
:::

| Your edge | Best fit | Why | Source |
|---|---|---|---|
| A training or inference method that changes how the model runs | Patent | Claims that improve the model's own operation were treated as eligible | USPTO, *Desjardins* |
| A known model applied to new data or a new industry | Not a patent | A new field of use or database does not make an abstract idea eligible | Federal Circuit, *Recentive* |
| Weights, training data, prompts, eval sets | Trade secret | Protected only while you take reasonable steps to keep them secret | 18 U.S.C. § 1839 |
| Code and content your team writes | Copyright | Needs human authorship. Prompts alone do not supply it | Copyright Office, Part 2 |
| The product name | Trademark | Registered through the USPTO, separate from patents | USPTO |

Two limits on that table. A trade secret does not stop someone who works out your method on their own. Federal law says reverse engineering and independent derivation are not improper means (18 U.S.C. § 1839(6)). Weigh that before you rely on secrecy for anything customers can probe.

## What counts as eligible

The USPTO's Appeals Review Panel made *Ex parte Desjardins* precedential on 4 November 2025. The claims trained a machine-learning model so it kept performance on earlier tasks while learning new ones, with less storage and complexity. The panel treated that as an improvement to how the model works, not as abstract math.

The Federal Circuit went the other way in *Recentive Analytics v. Fox* on 18 April 2025. The claims used generic machine learning on new data to generate live-event schedules and network maps. The court held them ineligible and said a new data environment does not change that.

So the line is technical. Drafting follows the same line. A claim that describes the result ("better predictions") is weaker than one that describes the mechanism. Ask your attorney for broad independent claims with structural fallbacks underneath (VEN session).

## Timing: file before you disclose

A provisional application gives you a filing date and 12 months to file the full application. It is never examined and never becomes a patent on its own. It only covers what it describes, so a thin provisional protects little (USPTO; VEN session).

| Event | Rule | Source |
|---|---|---|
| Your own public disclosure, in the US | One-year grace period to file | USPTO |
| Your own public disclosure, abroad | May bar a foreign patent | USPTO |
| Provisional filed | 12 months to file the full application | USPTO |
| Pitch, paper, demo, or partner sharing the method | Treat as the trigger to file first | VEN session |

If a demo day, a conference talk, or a design partner is on your calendar, file before it. An NDA helps with the partner and does nothing for a conference audience.

## What it costs

Attorney charges are the larger bill. These are medians for services rendered in 2024.

| Item | Median attorney charge | USPTO fee, large / small entity | Source |
|---|---|---|---|
| Provisional application | $4,500 | $325 / $130 | AIPLA; USPTO |
| Full application, complex electrical or computer | $12,000 | $2,000 / $800 | AIPLA; USPTO |
| Response to one examiner rejection, same field | $3,500 | none | AIPLA |
| Issue fee | included above | $1,290 / $516 | USPTO |
| Novelty search, optional | $2,500 | none | AIPLA |

The USPTO full-application fee adds three parts: filing ($350 / $140), search ($770 / $308), and examination ($880 / $352). Small entity status has limits on company size and on licensing to larger companies, so confirm it with your attorney. Micro entity is lower again.

**Labeled example.** One provisional, one full application, one rejection response, grant. Attorney charges: $4,500 + $12,000 + $3,500 = **$20,000**. USPTO fees at the small-entity rate: $130 + $800 + $516 = **$1,446**. At the large-entity rate: $325 + $2,000 + $1,290 = **$3,615**. Total about **$21,400** to **$23,600**. This is arithmetic on the medians above, not a quote. One rejection is an assumption, and the first maintenance fee at 3.5 years is another $860 small-entity or $2,150 large.

Does it pay? One study of US startups found that those drawing a lenient examiner had on average 55% higher employment growth and 80% higher sales growth five years later (Farre-Mensa, Hegde and Ljungqvist, 2020). That is evidence that a first grant helps young companies. It covers all US startups, not AI teams, and it does not say a patent beats shipping. There is no reliable public benchmark yet for how many AI startups hold a patent at seed or Series A.

## Ownership comes first

Patent rights start with the inventor, not the company. The Supreme Court said in 2011 that rights in an invention belong to the inventor, and an inventor must expressly grant them to an employer (*Stanford v. Roche*). In that case a researcher's earlier promise to "agree to assign" lost to a later "will assign and do hereby assign". The Federal Circuit drew that distinction. The Supreme Court did not rule on it, but affirmed.

For you, that means three things.

**Use present-tense assignment language.** Every founder, employee, and contractor signs "hereby assigns", not "agrees to assign". Fix old forms. Series A counsel will ask for them (see the [Series A diligence checklist](/library/fundraising/series-a-diligence-checklist/)).

**Keep a record of who conceived each idea.** Inventors must be people. The USPTO's November 2025 guidance says AI is a tool and applies the ordinary conception test to the human using it. Dated notes on who came up with each technical idea answer that test later.

**Read the AI tools' terms.** Check who owns the output and whether your inputs train the provider's models. A free tool can put a trade secret at risk (VEN session).

## Do this

:::steps File or not
1. **Write the edge in one sentence.** Name the mechanism and the gain: compute, storage, or error rate.
2. **Sort it.** Method that changes the model: patent candidate. Data, prompts, weights: trade secret. New field only: no patent.
3. **List disclosures in the next 12 months.** Pitches, papers, demos, partner calls.
4. **If one is coming, file a provisional first.** Have the attorney draft it as if it were the full application.
5. **Sign present-tense assignments.** Founders, employees, contractors, advisors who build.
6. **Log inventorship.** Date and name the human who conceived each method.
7. **Protect the secrets.** Access limits, NDAs, and written rules for AI tool use.
8. **Decide on the full application by month 10.** Budget about $15,500 in attorney charges for the full application and one rejection.
:::

## Mistakes that cost the claim

**Patenting a business result.** "Saves the operator time" is not a technical gain. Say what the system does differently.

**Pitching first, filing later.** The US gives you a year, but a foreign patent may be gone the day you talk.

**Filing a thin provisional to claim a date.** It protects only what it describes.

**Relying on an NDA at a conference.** It binds the person who signed it.

**Skipping the assignment because everyone is a friend.** The right to the invention starts with the person, so the paper has to say otherwise.

Not legal advice. Talk to a patent attorney before you disclose or file, and have counsel review your assignment forms.

## Sources

- [USPTO, Revised inventorship guidance for AI-assisted inventions](https://www.federalregister.gov/documents/2025/11/28/2025-21457/revised-inventorship-guidance-for-ai-assisted-inventions). Federal Register, 28 November 2025. Replaces the February 2024 guidance. AI is a tool. The ordinary conception test applies to the human inventor.
- [USPTO, Appeals Review Panel decision designated precedential (*Ex parte Desjardins*)](https://www.uspto.gov/subscription-center/2025/ptab-designates-precedential-appeals-review-panel-decision). Appeal 2024-000567, designated 4 November 2025. Training claims that improve how the model operates were eligible under 35 U.S.C. § 101.
- [Federal Circuit, *Recentive Analytics, Inc. v. Fox Corp.*, No. 23-2437](https://www.cafc.uscourts.gov/opinions-orders/23-2437.OPINION.4-18-2025_2500790.pdf). 18 April 2025. Generic machine learning applied to new data environments is ineligible.
- [USPTO, Provisional application for patent](https://www.uspto.gov/patents/basics/apply/provisional-application). Twelve months to file the nonprovisional. Not examined. One-year US grace period after your own disclosure. A prior disclosure may preclude foreign patenting.
- [USPTO fee schedule](https://www.uspto.gov/learning-and-resources/fees-and-payment/uspto-fee-schedule). Provisional $325 / $130 / $65. Utility filing $350 / $140 / $70, search $770 / $308 / $154, examination $880 / $352 / $176, issue $1,290 / $516 / $258. Maintenance at 3.5 years $2,150 / $860 / $430. Large / small / micro entity.
- [AIPLA, 2025 Report of the Economic Survey](https://www.aipla.org/docs/default-source/adr-neutrals/aipla-2025_report_protected_updated-address.pdf). Median charges, 2024: provisional $4,500; complex electrical or computer application $12,000; amendment or argument, complex electrical or computer, $3,500; novelty search $2,500. Excludes USPTO fees.
- [Farre-Mensa, Hegde and Ljungqvist, What Is a Patent Worth? Evidence from the U.S. Patent "Lottery"](https://doi.org/10.1111/jofi.12867). Journal of Finance, 2020. Startups whose first application drew a lenient examiner had 55% higher employment growth and 80% higher sales growth after five years.
- [Board of Trustees of Leland Stanford Junior University v. Roche Molecular Systems](https://supreme.justia.com/cases/federal/us/563/776/). 563 U.S. 776, 6 June 2011. Rights in an invention belong to the inventor. Footnote 2 leaves the Federal Circuit's reading of the assignment wording undecided.
- [Porter Hedges, Are your IP assignments effective?](https://www.porterhedges.com/newsroom-publications-IP_Alert_Are_Your_IP_Assignments_Effective). 13 January 2016. "Will assign and do hereby assign" conveys title in the present. "Agree to assign" is a promise for later.
- [18 U.S.C. § 1839, Definitions (trade secret)](https://www.law.cornell.edu/uscode/text/18/1839). Reasonable measures to keep the information secret are required. Reverse engineering and independent derivation are not improper means.
- [U.S. Copyright Office, Copyright and Artificial Intelligence, Part 2: Copyrightability](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf). January 2025. Purely AI-generated material is not protected. Prompts alone do not give enough control. Human-authored expression, selection, and arrangement can be.
- [VEN (Venture Executive Network)](https://www.venexecs.com/?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library&utm_content=ai-startup-patents-ip). Founder session with patent attorneys, 2026. State the technical gain, file before a pitch or partner collaboration, layer claims from broad to structural, and read free AI tools' terms. Not a survey. No closed-session numbers.

## Related

- [Go-to-market](/library/gtm/)
- [Data moat for AI startups](/library/gtm/data-moat-ai-startup/)
- [Strategic partnerships and IP: what to settle before you sign](/library/gtm/strategic-partnership-ip/)
- [Series A diligence checklist](/library/fundraising/series-a-diligence-checklist/)
- [Term sheet red flags](/library/fundraising/term-sheet-red-flags/)
- [Founder vesting at a priced round](/library/equity/founder-vesting-83b/)
