# Founder Decisions

Decision pages for venture-scale founders. An editorial/reference property, not a FounderNexus marketing site.

Canonical host: https://founderdecisions.com. Built by `python3 build.py` (output `dist/`). Hosted on Vercel. `FN_CONTENT_TOKEN` is required at build.

FounderNexus is named once as publisher, in the footer, like First Round Review. It is how some readers go deeper on a live decision. It is not the product of the page.

## No-marketing rule

Do not turn this into a landing page.

- Header wordmark is the text **Founder Decisions** (Plus Jakarta Sans 700, navy #01052A). No FounderNexus lockup or mark in the header or favicon.
- No “Apply now” in global nav. No membership pitch, conversion column, or second navy band.
- No “community” language. No “the room is the product.”
- On an article, a contextual close is optional: one short paragraph plus a text link to FounderNexus as a next step, not as publisher. No CTA card, no header button, no “Published by FounderNexus.” Do not put this on the homepage. Do not link The Startup Bible; it is an internal check only.
- `cta` in frontmatter is optional. The build does not fail if a page has none.

## Voice

Write like a sharp operator explaining it to another founder over coffee. Mature, precise, useful. Sentence-case headings. You = the founder making the decision.

Short sentences. Vary length. Default to periods, not em dashes.

Stop-slop is required. Every new or edited owned page follows `ops/stop-slop/RULES.md` (adapted from [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop), MIT) and passes the gate in `ops/stop-slop/GATE.md` before push: no em dashes, no named adverbs or jargon, no binary contrasts, active voice with a named actor. Numbers, citations, and `## Sources` stay exactly as written.

Do not use: “It’s important to note”, “in today’s landscape”, “when it comes to”, “delve”, “utilize”, “leverage”, “robust”, “unlock”, “the bottom line”, “in conclusion”, “not just X, but Y”, stacked hedges, or throat-clearing.

Do not announce that you are being careful. Just be careful. Do not say FounderNexus in the body except an optional closing paragraph. FounderNexus is one word.

Do not invent ranges. Named public sources only. Empty cell if unknown. When sources disagree, show them separately.

Legal line once, short, on finance/legal pages: “Not legal, tax, or compensation advice.”

## Markdown fences (library articles)

Supported in `render_markdown` (library/compare/about bodies only; not fn-content JSON):

- `:::takeaways` / `:::takeaway` — In short box (optional label after the fence name).
- `:::highlight` / `:::note` — thin blue left rule.
- `:::steps` / `:::step` — numbered step/layer stack (CSS-only). Prefer an ordered list inside; optional label after the fence name.

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

FounderNexus links fire a Vercel Web Analytics custom event `fn_click` with the page slug.

Vercel: `vercel.json` runs `python3 build.py` and serves `dist/`. Set `FN_CONTENT_TOKEN` on the project (fine-grained PAT, foundernexus/fn-content, contents: read).

## Daily shipping workflow

1. Add or edit a Markdown file under content/.
2. Stop-slop gate (required, see ops/stop-slop/GATE.md):
   - `python3 ops/stop-slop/check.py --changed` must report `HARD=0`. Fix every HARD hit; read `--soft` and fix what a plainer sentence fixes.
   - When you edited an existing page: `python3 ops/stop-slop/facts_guard.py origin/main` must print PASS (same numbers, URLs, Sources, title, slug).
   - Read the page against ops/stop-slop/RULES.md and score it (Directness, Rhythm, Trust, Authenticity, Density). Below 35/50: revise.
   - Record `stop-slop: pass (HARD=0, score NN/50)` in the commit body and the ops/inventory.md row.
   - `ops/stop-slop/prepush.sh` runs the two scripts plus the build in one step. Never add the check to build.py or vercel.json; style must not fail a Vercel build.
3. Rebuild: python3 build.py
4. Preview from dist with http.server, then stop.

Stdlib only. Draft pages are skipped. Do not git. Do not deploy. Do not leave a server running.

## How to add a page

Create a .md file in content/library/<cluster>/, content/tools/, or content/compare/.

Required frontmatter: title, description, slug, section, date.
Library pages also need cluster.
Optional: close (one-sentence contextual close; FounderNexus in that sentence becomes a text link), disclaimer: not-legal-tax, related (list of page keys), layout: calculator, draft: true.

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

Favicon is a typographic FR mark, not the FounderNexus mark.

## Do not

Clone GitHub, use CloudAgent, or deploy.
Invent search-volume numbers or compensation ranges.
Publish pricing, eligibility, speakers, or partners.
