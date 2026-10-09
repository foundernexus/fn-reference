# FounderNexus directory: keyword and IA brief
Date: 2026-08-29
Audience: venture-backed (already raised) and venture-scale (building toward $100M) founders, Seed–Series B.
CTA: Apply now → https://platform.foundernexus.com/registration
Volume: qualitative only. No Ahrefs/SEMrush dumps. Do not invent volumes.

## Page 1 (ship 2026-08-29)
Title: Executive equity grants by stage: what to offer a first VP at Seed, Series A, and Series B
Target: how much equity to give VP of sales startup
Slug: /library/equity/executive-grants-by-stage
Tool sibling: /tools/executive-equity-calculator

## Top 10 topics
1. How much equity to give a VP by stage
2. Option pool size / option pool shuffle
3. 409A cost, timing, refresh after a round
4. When to hire the first VP of Sales
5. Runway, burn, default-alive
6. NRR, magic number, CAC payback, Rule of 40
7. How to run a Series A board meeting
8. Independent director: when, who, equity
9. YPO vs EO vs Hampton vs a venture-scale room (shipped 2026-09-08 as /compare/ypo-vs-hampton-vs-venture-scale-room/)
10. Fractional vs full-time CFO (done 2026-09-17)

## IA
foundernexus.com/ → Apply product
/library/ → directory index
/library/{cluster}/ → hub
/library/{cluster}/{spoke}/ → guide
/tools/{calculator}/ → interactive
/compare/{a-vs-b}/ → commercial

## 30-day weekday queue (from Mon 2026-08-31)
1. Executive equity grants by stage
2. Executive equity calculator
3. Equity & cap table hub
4. Size option pool from hiring plan
5. Option pool shuffle calculator
6. 409A after a priced round
7. Executive hiring hub
8. When to hire first VP of Sales
9. Series A leadership hiring sequence
10. Finance, metrics & runway hub — done 2026-09-25 → /library/finance/. Query: startup board financial metrics. Orients three finance spokes + two tools; composite metric→when→spoke/tool table. Cites Sacks/Feld/Bessemer/ChartMogul/SaaS Capital/Scale/PG/Kruze/Carta; FN session stage-right pack.
11. Runway calculator with hiring plan (done 2026-09-10 → /tools/runway-calculator/)
12. Burn multiple vs Rule of 40 (done 2026-09-09 → /library/finance/burn-multiple-vs-rule-of-40/)
13. Magic number & CAC payback calculator (done 2026-09-11 → /tools/magic-number-cac-payback-calculator/)
14. NRR vs GRR for the board pack (done 2026-09-14 → /library/finance/nrr-vs-grr-board-pack/)
15. Board & governance hub — done 2026-09-27 → /library/board/. Query: Series A board structure. Orients two board spokes (agenda + independent); composite governance question→when→spoke table. Cites CRV, Lightspeed/Unusual, Feld, Carta via Walker, Boardspan; FN session updates≠decisions / drive independent shortlist. fn-content#13 covers independent equity.
16. Series A board meeting agenda (done 2026-09-15 → /library/board/series-a-board-meeting-agenda/)
17. Independent director: when, who, equity
18. Fractional vs full-time CFO (done 2026-09-17 → /library/finance/fractional-vs-full-time-cfo/)
19. Founder rooms hub — done 2026-09-28 → /library/rooms/. Query: YPO vs Hampton vs founder community. Orients two compare spokes (YPO/EO/Hampton/venture-scale + coaching vs peer group); composite room decision→when→spoke table. Cites YPO, EO, Hampton, Vistage, Powderkeg, FounderNexus filter; Manchester/ICF caveated via coaching spoke. FN quiet close. fn-content#16 covers coaching/dues.
20. YPO vs EO vs Hampton vs venture-scale room (done 2026-09-08)
21. Executive coaching vs founder peer group
22. Fundraising hub + Series A diligence checklist — diligence done 2026-09-24; hub done 2026-10-01 → /library/fundraising/. Query: Series A fundraising. See candidate #34.

## Rules
- Cite Index, Carta, Kruze, ChartMogul, Bessemer. Never imply FN proprietary comp data.
- Every URL needs a tool, original cited table, template, or labeled composite scenario.
- Not legal or tax advice on finance/legal pages.
- Brand queries stay on foundernexus.com homepage.
- Membership is offered, not sold. Apply names the decision.
- No session content scraped into the library.
- Stop-slop gate before every push (required): `python3 ops/stop-slop/check.py --changed` at HARD=0, `facts_guard.py origin/main` PASS for edited pages, and a manual read against ops/stop-slop/RULES.md at 35/50 or better. Details in ops/stop-slop/GATE.md. The /decisions/ and /benchmarks/ pages come from fn-content; report slop there, do not edit it here.
- Public copy never mentions fn-content, atoms, benchmark requests, "tracked as", or GitHub issue links (body or Sources). File the benchmark request in fn-content and keep it in this brief and ops/inventory.md. On the page, keep the named source and its figure; if no range exists, write "There is no reliable public benchmark yet for X."


## Friday 2026-09-18 Startup Bible check (internal)
Source: weekly internal scan of FounderNexus Playbooks (never link publicly). Judgment only — no closed-session numbers on FD pages. Cite as FounderNexus session → https://www.foundernexus.com?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library when earned.

### New/updated since ~2026-09-11
- Homepage now surfaces two extra pillars: Marketing & PR (4) and Building the Company (4), beyond Raising Money / Getting Customers / Equity & Legal / Reference.
- **GTM as a system** — LAST REVIEWED 2026-09; committed 2026-09-18 on fn-playbooks (Sep 2026 session). Five questions, blue-ocean lane, scatter-plot funnel, GTM hypothesis. Matches Matt's "AI + GTM" note.
- Marketing & PR cluster: DIY PR; AI-era marketing stack; marketing AI products without saying AI; GTM as a system.
- Building the Company cluster: executive team; data moats & flywheels; surviving the SaaS repricing; pricing in the AI era.
- Also since last Friday: when-runway-runs-out playbook (fn-playbooks 2026-09-15). Sessions index now spans Dec 2025 – Sep 2026.

### Pressure-test (judgment only) — no public edit today
- VP Sales / Series A sequence / executive grants: aligned with executive-team "hire for the phase / 0→10 ≠ 10→50" (already FounderNexus session on those pages).
- Fractional vs FT CFO: aligned on phase-hire; Bible has no dedicated CFO playbook — keep Kruze/Bessemer/Majhi.
- AI SDR vs human: aligned with AI-era stack (no chatbot on inbound; amplify one seller; humans close). Already cites FounderNexus session.
- Coaching vs peer group: no Bible analog — no action.

### Candidate weekday queue (do not ship Friday)
23. How to market an AI product (without leading with AI) — done 2026-09-19 → /library/gtm/market-ai-product-without-saying-ai/. Query: how to market an AI startup. Sibling to /library/gtm/ai-sdr-vs-human/. Cite Bessemer Atlas + Gartner agent washing; FounderNexus session for job-first / human close.
24. Seat vs usage vs outcome pricing for AI SaaS — done 2026-09-20 → /library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas/. Query: seat based vs usage pricing AI SaaS. Bessemer Atlas AI pricing playbook + Part III; FounderNexus session for seats-for-humans / outcomes-for-agents. fn-content#18.
25. AEO vs SEO for B2B SaaS startups — done 2026-09-21 → /library/gtm/aeo-vs-seo-b2b-saas/. Query: AEO vs SEO B2B SaaS. Google AI opt guide + GSC Gen AI reports; SparkToro/Similarweb; FN session buyers ask AI before site. fn-content#20.
26. DIY founder PR / founder narrative before launch — done 2026-09-22 → /library/gtm/diy-founder-pr-narrative/. Query: DIY PR for startups. YC Seibel + Muck Rack 2026 + First Round Carmichael/Hammerling + NextView + Everything-PR retainers; FN session narrative/founder voice. fn-content#21.
27. Data moat for AI startups — done 2026-09-23 → /library/gtm/data-moat-ai-startup/. Query: how to build a data moat startup. a16z Empty Promise + Bessemer Vertical AI Part IV + Sequoia Own Your Intelligence; FN session data-as-moat / instant feedback. fn-content#22.

Priority for next days: #23–#32 GTM spokes + GTM hub shipped (skip thin GTM-as-a-system clone). Next: pick a crisp unpublished library/tools/compare decision (hubs only when two spokes exist). Cadence: one new page every day including weekends.

28. Series A diligence checklist — done 2026-09-24 → /library/fundraising/series-a-diligence-checklist/. Query: Series A diligence checklist. First fundraising spoke (hub deferred). Cite YC Kwon/Harris checklist + Underscore staged data room + Burkland 2026 evaluation lenses; FN session room-as-ops-signal. fn-content#23.
29. Finance, metrics & runway hub — done 2026-09-25 → /library/finance/. Queue #10. Query: startup board financial metrics.


## Friday 2026-09-25 Startup Bible check (internal)
Source: weekly internal scan of FounderNexus Playbooks (never link publicly). Judgment only — no closed-session numbers on FD pages. Cite as FounderNexus session → https://www.foundernexus.com?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library when earned.

### New/updated since 2026-09-18
- **Why AI isn't making engineering 10x faster** — Building the Company (5th playbook). LAST REVIEWED 2026-09; Sep 2026 session. Amdahl’s law on delivery loop (design/code/review/test/deploy/operate); “meat proxy” tax; AI-native default; engineering sovereignty.
- New/updated concepts tied to that session: Amdahl’s law, engineering sovereignty, meat proxy, AI-native (LAST REVIEWED 2026-09).
- Sessions index still Dec 2025 – Sep 2026. Data rooms playbook present (LAST REVIEWED 2026-08; Dec 2025 session) — already used as internal lens for Series A diligence spoke.

### Pressure-test (judgment only)
- Finance hub + burn / NRR / fractional CFO: aligned with runway / SaaS-repricing framing — no edit.
- Hiring VP Sales + Series A sequence: aligned with executive-team hire-for-phase — no edit (KORE1 cite fixed this Friday).
- GTM ships (AI SDR, market-AI, pricing, AEO, DIY PR, data moat): still aligned with Marketing & PR + Building the Company cluster — no edit.
- Series A diligence checklist: aligned with data-rooms “room is the message / staged access” judgment already on page via Underscore + FN session — no edit.

### Candidate weekday queue
30. Why coding agents don’t 10x the company (Amdahl’s law on the delivery loop) — done 2026-09-26 → /library/gtm/coding-agents-dont-10x-engineering/. Query: why AI coding agents don't 10x engineering. Cite Amdahl 1967 + Atlassian (3 Apr 2026) + Faros Acceleration Whiplash (12 Apr 2026) + METR RCT (10 Jul 2025) + Meagher; FN session score-the-loop / AI-native default / policy not every gate. fn-content#25.
31. Board & governance hub — done 2026-09-27 → /library/board/. SEO-BRIEF queue #15 / Sunday. Query: Series A board structure. Two spokes already live; composite table. No new fn-content issue (#13 covers independent equity).
32. Go-to-market hub — done 2026-09-29 → /library/gtm/. Query: AI GTM for startups. Orients seven GTM spokes (AI SDR, market-AI, pricing, AEO, DIY PR, data moat, coding-agents); composite GTM decision→when→spoke table. Cites SaaStr, Bridge Group, Gartner, Bessemer Atlas, Google Search Central, YC Seibel, Muck Rack, a16z, Sequoia, Amdahl/Atlassian/Faros/METR; FN session AI-on-prep / humans-on-close. No new fn-content issue.

33. When to raise Series A (readiness signals) — done 2026-09-30 → /library/fundraising/when-to-raise-series-a/. Query: when to raise Series A. Second fundraising spoke (hub deferred). Cite Burkland 2026 readiness lenses + Carta seed→A timing (Q2 2025 616 days; Walker Q4 2025 1.9 years) + Bessemer SotC 2023 fundability; Sacks/Craft burn multiple via sibling; FN session six-lens score before outreach. fn-content#30.

34. Fundraising hub — done 2026-10-01 → /library/fundraising/. SEO-BRIEF queue #22 / Thursday. Query: Series A fundraising. Two spokes already live (when-to-raise + diligence); composite raise decision→when→spoke table. Cites Burkland 2026, Carta seed→A timing, Bessemer SotC 2023, YC Kwon/Harris, Underscore, Sacks/Craft via sibling; FN session machine-score / cash-to-negotiate / room-as-ops-signal. No new fn-content issue (#23/#30 cover siblings).

35. SAFE vs priced round (Seed instrument) — done 2026-10-02 → /library/fundraising/safe-vs-priced-round/. Query: SAFE vs priced round. Third fundraising spoke. Cite YC post-money SAFE + SAFE vs note vs priced; Carta Q3 2024 seed mix (64/27/10) + size bands + Q1 2026 pre-seed 93% SAFE; Carta SAFE learn + State of Pre-Seed Q2 2025 under-$4M convertibles; Cooley GO discounts; CRV priced vs SAFE cost/timeline; FN session mid-Seed modeling / one-instrument stack. Hub orient + inbound related on siblings. fn-content#32.

## Friday 2026-10-02 Startup Bible check (internal)
Source: weekly internal scan of FounderNexus Playbooks (never link publicly). Judgment only — no closed-session numbers on FD pages. Cite as FounderNexus session → https://www.foundernexus.com?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library when earned. Preview host https://startup-bible-theta.vercel.app 308→ https://www.foundernexus.com/playbooks.

### New/updated since 2026-09-25
- **No new playbook pages** since last Friday. Counts unchanged: raising-money 11, getting-customers 8, building-the-company 5, marketing-pr 4, equity-legal 4; ~40 concepts; sitemap ~77 URLs (no lastmod stamps on playbooks sitemap-0).
- Sessions index still **LAST REVIEWED 2026-09** / transcript batches **Dec 2025 – Sep 2026** (unchanged vs 2026-09-25).
- Home copy polish only: headline/lede “Playbooks from live sessions, not a content mill.” — no section-count change. AI-engineering-10x + GTM-as-a-system remain the newest substantive playbooks (already reflected in FD coding-agents spoke + GTM hub).
- Raising-money cluster still lists unpublished-for-FD topics that earn search queries: first angel check, when runway runs out, venture debt, term-sheet red flags, how seed VCs decide; Getting Customers still has pilots that convert.

### Pressure-test (judgment only)
- SAFE vs priced (`/library/fundraising/safe-vs-priced-round/`): aligns with Bible `raising-money/safes-notes-priced-rounds`. Public cites YC/Carta/Cooley/CRV + FN session; no Bible URL on live page — no edit.
- When to raise Series A + Fundraising hub: aligned with running-the-raise / readiness framing already on pages via Burkland/Carta/Bessemer + FN session — no edit.
- Series A diligence checklist: still aligned with data-rooms staged-access judgment — no edit.
- Equity hub / GTM hub: still aligned with options-pools + Marketing & PR / Building the Company clusters — no edit.

### Candidate weekday queue (do not ship from this check)
36. First angel check — done 2026-10-03 → /library/fundraising/first-angel-check/. Query: how to find angel investors (primary) / first angel check. Fourth fundraising spoke. Cites YC seed guide + Seibel email + SAFE pages, Paul Graham How to Raise Money, a16z Angels vs VCs, Cooley GO angel finder + SAFE, Carta Q3 2024 seed mix + Q1 2026 pre-seed 93% (reuse). FN session active-writer filter / niche insider / lead-wait soft-no. Hub spokes+composite updated; inbound related on safe-vs-priced, when-to-raise, diligence. No new fn-content issue (reused Carta/YC bands; no new benchmark atom).
37. When runway runs out — done 2026-10-04 → /library/fundraising/when-runway-runs-out/. Query: what to do when startup runway runs out (secondary: when runway runs out startup / default alive default dead). Fifth fundraising spoke (hub already live). Diagnose snapshot vs PG default alive/dead; cut / bridge-angel / revenue extend / orderly wind-down; :::steps measure→choose→communicate→execute→re-measure. Cites PG aord + Fatal Pinch, YC Caldwell <1yr runway, Kruze, Carta Q1 2024 + Q2 2025 (reuse), Burkland runway-at-process, Sacks via sibling; FN session score-machine / cut-before-desperation / board-with-options. Hub spokes+composite+stage sketch updated (no new hub cite numbers in Sources); inbound related on when-to-raise, first-angel, safe-vs-priced, diligence, runway-calculator, burn-multiple, finance hub. No new fn-content issue (reused PG/Kruze/Carta/Burkland/Sacks).
38. Venture debt when it fits — done 2026-10-05 → /library/fundraising/venture-debt/. Query: venture debt for startups. Sixth fundraising spoke (hub already live). Fit table (right after equity close / milestone extension / capex / undrawn insurance / late-stage bridge vs short runway, down-round dodge, angel-only seed); sizing table; cost table; terms-to-fight table (draw window, MAC + funding MAC, investor abandonment, covenants, litigation threshold, debt overhang); :::steps equity close → first draw. Cites SVB/First Citizens (sizing 20–40% / 6–8% / ≤10% EV / <25% debt service / 6+12 months; $4M+ qualifier; FAQ), Kruze (insights, warrants 2–10%, don't borrow your own money, downround, MAC, events of default, sample term sheet), Mercury term sheet guide, Orrick/Hellman default provisions, Fred Wilson AVC 2011, PitchBook 2025 $62.4B / 943 deals; FN session accelerant-not-rescue / raise-when-you-don't-need-it / lender-by-behavior / reference-check. Hub spokes+composite+stage sketch+takeaway updated (no new hub cite numbers; Sources unchanged); when-runway venture-debt row now links the spoke; inbound related on when-runway, safe-vs-priced, when-to-raise, runway-calculator. fn-content#34.
39. Pilots that convert — done 2026-10-06 → /library/gtm/pilot-to-paid-contract/. Query: how to convert a pilot to a paid contract. Eighth GTM spoke (hub already live). Motion table (opt-out contract / paid pilot / paid POC / demo on their data / free pilot); conversion clauses before kickoff; buying-group map; :::steps scope → metrics → paper the conversion → run → readout → sign; stall table. Cites SaaStr (polls 74% paid / 42% free; Lemkin 70%+ / ~60–90%+ / 60-day opt-out; charge-for-pilots; big paid pilot 2–3 metrics + 60/30-day example; why enterprises insist), a16z Need for Speed in AI Sales (70% / 57% / 11%), Gartner GenAI POC abandonment ≥30% (forecast), Gartner B2B Buying Report 2023 (5–11 stakeholders). FN session PO-is-the-goal / price-before-proof / cut-scope-before-price (no session numbers). Hub spokes+composite+stage sketch updated; inbound related on ai-sdr, seat-vs-usage, market-ai. fn-content#35. Bible check 2026-10-06: no new playbook pages (counts unchanged).
40. Term sheet red flags — done 2026-10-08 → /library/fundraising/term-sheet-red-flags/. Query: term sheet red flags. Seventh fundraising spoke (hub already live); shipped Thursday after the 10/7 run failed. Clean-vs-red-flag table (preference, participation, dividends, anti-dilution, seniority, board, operating approvals, protective provisions, pool, redemption, pay-to-play, warrants, exclusivity); prevalence table; option pool shuffle; board and vetoes; exclusivity and re-trading; :::steps price basis → economics → board/vetoes → waterfall → ~3 issues → close. Cites Cooley Q2 2026 Venture Financing Report (166 deals; 95.8% 1x; 96.4% nonparticipating; redemption 5.4%; accruing dividends 3%; pay-to-play 8.4%; down 12.1%), Wilson Sonsini Entrepreneurs Report Q2 2026 (1H 2026 terms appendix + 2025 down rounds), Carta State of Private Markets Q4 2024 (participating preferred), YC clean Series A term sheet, Cooley GO Bartus negotiating term sheets, Feld liquidation preference + protective provisions, Venture Hacks option pool shuffle, NVCA model docs. FN session pre-vs-post in writing / pro forma vs long-form / re-vest with vested floor / board over dilution (no session numbers). Hub spokes+composite+stage sketch+takeaway updated; inbound related on safe-vs-priced, venture-debt, diligence, when-to-raise. fn-content#37 (reused). Bible check 2026-10-08: no new playbook pages (sitemap 77 URLs; raising-money 11, getting-customers 8, building-the-company 5, marketing-pr 4, equity-legal 4, concepts 39; unchanged). Remaining raising-money candidate: how seed VCs decide.
41. How seed VCs decide — done 2026-10-09 → /library/fundraising/how-seed-vcs-decide/. Query: how do seed VCs decide to invest (secondary: what seed investors look for). Eighth fundraising spoke (hub already live). Selection-factor table (team / product / business model / market / fit / valuation / value-add, early vs late); funnel-per-closed-deal table; pricing from check + target ownership; labeled composite fund-lens table (team / defensibility / traction / category-leader bet, no thresholds); :::steps fund list → convince yourself → team → market path → lens evidence → milestone ask → first meeting for the second → reference-check lead; mistakes. Cites Gompers, Gornall, Kaplan & Strebulaev JFE 2020 (885 VCs / 681 firms; survey Nov 2015–Mar 2016; team 95% / 47%; early 96% / 53% vs late 39%; early valuation 0% most important; fit 13%; funnel 119 / 34 / 11 / 4.6 / 1.5 vs all 101 / 28 / 10 / 4.8 / 1.7; 73 vs 106 days, 81 vs 184 hours, 8 vs 13 references; desired ownership 75%, 63% set valuation from check + ownership, 20% target stake), Bernstein/Korteweg/Laws JF 2017 (AngelList ~4,500 investors / ~17,000 emails; team moves average investor, traction and leads do not), Paul Graham How to Convince Investors (2013), YC Ralston seed guide (10%/week; 12–18 months; up to 20% dilution, avoid >25%; first meeting → next meeting; no detailed financials), Carta State of Pre-Seed Q2 2026 ($3.19B / 11,500+ vs $3.22B / 14,825; $276K avg, +27%; AI 49% H1). FN session know-the-fund's-lens / qualify thesis-check-deployment / reference-check lead / friendly-no-next-step = no (no session numbers). Hub lede+takeaway+spokes+composite (2 rows)+stage sketch+close+Related updated (no new hub cite numbers; Sources unchanged); inbound related on first-angel-check, safe-vs-priced, when-to-raise, term-sheet-red-flags. fn-content#38 (new: seed VC deal funnel and selection factors). Bible check 2026-10-09: no new playbook pages (sitemap 77 URLs; raising-money 11, getting-customers 8, building-the-company 5, marketing-pr 4, equity-legal 4, concepts 39; unchanged). Lastmod bumps only: how-seed-vcs-decide, pitch-deck, running-the-raise, sessions (2026-10-06); how-seed-vcs-decide now adds category-leader, capital-fit, and founder-commitment lenses (used as judgment only). Raising-money playbooks not yet on FD: pitch deck, running the raise, exit process, exits and M&A.
