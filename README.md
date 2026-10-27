# Founder Decisions

Decision pages for venture-scale founders. An editorial/reference property, not a VEN marketing site.

Canonical host: https://founderdecisions.com. Built by `python3 build.py` (output `dist/`). Hosted on Vercel. `FN_CONTENT_TOKEN` is required at build.

VEN (Venture Executive Network, https://www.venexecs.com, formerly FounderNexus) is the publisher behind the library. It is how some readers go deeper on a live decision. It is not the product of the page. Public pages never link foundernexus.com.

## No-marketing rule

Do not turn this into a landing page.

- Header wordmark is the text **Founder Decisions** (Plus Jakarta Sans 700, navy #01052A). No VEN or FounderNexus lockup or mark in the header or favicon.
- No “Apply now” in global nav. No membership pitch, conversion column, or second navy band.
- No “community” language. No “the room is the product.”
- On an article, a contextual close is optional: one short paragraph plus a text link to VEN as a next step, not as publisher. Under it the build may add one quiet “Go deeper: VEN playbook on …” link from `VEN_PLAYBOOKS` in build.py (genuine topic match only; see SEO-BRIEF). No CTA card, no header button, no “Published by VEN.” The homepage carries one quiet VEN text line at the bottom (`HOME_VEN_URL`, utm_campaign=home); no other VEN element on the homepage. Never name The Startup Bible; playbook pages are linked only through the `VEN_PLAYBOOKS` mapping and never copied.
- `cta` in frontmatter is optional. The build does not fail if a page has none.

## Voice

Write like a sharp operator explaining it to another founder over coffee. Mature, precise, useful. Sentence-case headings. You = the founder making the decision.

Short sentences. Vary length. Default to periods, not em dashes.

Stop-slop is required. Every new or edited owned page follows `ops/stop-slop/RULES.md` (adapted from [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop), MIT) and passes the gate in `ops/stop-slop/GATE.md` before push: no em dashes, no named adverbs or jargon, no binary contrasts, active voice with a named actor. Numbers, citations, and `## Sources` stay exactly as written.

Do not use: “It’s important to note”, “in today’s landscape”, “when it comes to”, “delve”, “utilize”, “leverage”, “robust”, “unlock”, “the bottom line”, “in conclusion”, “not just X, but Y”, stacked hedges, or throat-clearing.

Internal words stay internal. Never write spoke, hub, cluster, pillar, target query, money page, SEO-BRIEF, inventory, or an “Orient…” / “this hub collects…” note in anything a reader sees: body, tables, Sources, `description`, `close`, `title`, link text. Say “page”, “topic”, or the topic name (“finance, metrics & runway”). Frontmatter keys such as `cluster:` and `target_query:` are fine; they never render. `check.py` fails these as HARD `internal-language`.

Do not announce that you are being careful. Just be careful. Name VEN in the body only as a “VEN session” cite or in the closing paragraph. The first visible mention renders as “VEN (Venture Executive Network)” automatically.

Do not invent ranges. Named public sources only. Empty cell if unknown. When sources disagree, show them separately.

Legal line once, short, on finance/legal pages: “Not legal, tax, or compensation advice.”

## Markdown fences (library articles)

Supported in `render_markdown` (library/compare/about bodies only; not fn-content JSON):

- `:::takeaways` / `:::takeaway` — In short box (optional label after the fence name).
- `:::highlight` / `:::note` — thin blue left rule.
- `:::steps` / `:::step` — numbered step/layer stack (CSS-only). Prefer an ordered list inside; optional label after the fence name.
- `:::group <Question label>` — topic-page pick list. Each line `- [Page title](/path/): one-line answer`. Consecutive groups render as one two-column grid. Topic pages (`_hub.md`) lead with these, grouped by the question a founder asks, before any long table.

```md
:::steps How to run it
1. Name the hypothesis
2. Run ten discovery calls
3. Kill or keep the profile
:::
```

## fn-content decision pages


At build, `build.py` fetches `renders/founderdecisions/*.json` → `/decisions/<slug>/` and `renders/founderdecisions-benchmarks/*.json` → `/benchmarks/<slug>/` from `foundernexus/fn-content` using `FN_CONTENT_TOKEN` (JSON-LD from `schema`, one `fn_link`). A 404 on a directory means zero pages, not a failed build. Other errors exit non-zero.

```bash
export FN_CONTENT_TOKEN=...   # fine-grained PAT, foundernexus/fn-content, contents: read
python3 build.py
```

Vercel Web Analytics loads from `/_vercel/insights/script.js`. Any venexecs.com link click fires custom event `ven_click` {page, target, type: homepage|playbook} (custom events need Vercel Pro; Hobby records pageviews only).

Vercel: `vercel.json` runs `python3 build.py` and serves `dist/`. Set `FN_CONTENT_TOKEN` on the project (fine-grained PAT, foundernexus/fn-content, contents: read).

## Daily shipping workflow

1. Add or edit a Markdown file under content/.
2. Stop-slop gate (required, see ops/stop-slop/GATE.md):
   - `python3 ops/stop-slop/check.py --changed` must report `HARD=0`. After the build, `python3 ops/stop-slop/check.py --dist` must also report `HARD=0` (catches internal words in meta tags, JSON-LD, and template strings). Fix every HARD hit; read `--soft` and fix what a plainer sentence fixes.
   - When you edited an existing page: `python3 ops/stop-slop/facts_guard.py origin/main` must print PASS (same numbers, URLs, Sources, title, slug).
   - Read the page against ops/stop-slop/RULES.md and score it (Directness, Rhythm, Trust, Authenticity, Density). Below 35/50: revise.
   - Record `stop-slop: pass (HARD=0, score NN/50)` in the commit body and the ops/inventory.md row.
   - `ops/stop-slop/prepush.sh` runs the two scripts plus the build in one step. Never add the check to build.py or vercel.json; style must not fail a Vercel build.
3. Rebuild: python3 build.py
4. Preview from dist with http.server, then stop.
5. After the push deploys, run the live check against founderdecisions.com:
   - Daily ship: `python3 ops/qa/live_check.py --quiet`. Exit code 1 means a FAIL; fix it before calling the ship done. It checks the sitemap, canonicals, robots, JSON-LD, internal links, orphans, topic-page placement, homepage counts, New this week freshness, internal language, VEN UTMs, and (with Playwright) overflow, console errors, and search at 390px and 1280px.
   - Friday review: `python3 ops/qa/live_check.py --full --json ops/qa/last-full.json` adds every external link and full-page screenshots. External 401/403/429 are WARN (sites that block bots); report them, do not delete the citation.
   - One-time setup: `pip install playwright && python3 -m playwright install chromium`. `--no-browser` skips the browser checks.

Stdlib only. Draft pages are skipped. Do not git. Do not deploy. Do not leave a server running.

## How to add a page

Create a .md file in content/library/<cluster>/, content/tools/, or content/compare/.

Required frontmatter: title, description, slug, section, date.
Library pages also need cluster.
Optional: close (one-sentence contextual close; VEN in that sentence becomes a text link), disclaimer: not-legal-tax, related (list of page keys), layout: calculator, draft: true.

Then rebuild. HTML is written to dist/.

URLs:

- / index
- /library/ /tools/ /compare/ section hubs
- /library/<cluster>/ cluster hub
- /library/<cluster>/<slug>/ guide
- /tools/<slug>/ calculator
- /compare/<slug>/ comparison
- /about/

## Current pages

- Page 1: /library/equity/executive-grants-by-stage/
- Calculator: /tools/executive-equity-calculator/
- About: /about/
- Unpublished sample: content/_drafts/how-to-run-a-board-meeting.md (draft: true)

## Brand tokens (type and color only)

Keep Plus Jakarta Sans 400/500/600/700. Navy #01052A. Blue #0072BA (links/actions, hover #0059A8). Page white / #F9F9F9. Buttons 8px radius if any remain.

Do not introduce purple, emoji, Title Case headlines, or a second typeface.

Favicon is a typographic FR mark, not the VEN mark.

## Do not

Clone GitHub, use CloudAgent, or deploy.
Invent search-volume numbers or compensation ranges.
Publish pricing, eligibility, speakers, or partners.
