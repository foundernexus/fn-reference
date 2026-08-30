# Founder Decisions

Decision pages for venture-scale founders. An editorial/reference property, not a FounderNexus marketing site.

Local only. Canonical placeholder: https://founderdecisions.com. Matt McKinney (mattm@foundernexus.com) must approve anything public, any domain, and any BASE_PATH change in build.py. Do not deploy.

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

Do not use: “It’s important to note”, “in today’s landscape”, “when it comes to”, “delve”, “utilize”, “leverage”, “robust”, “unlock”, “the bottom line”, “in conclusion”, “not just X, but Y”, stacked hedges, or throat-clearing.

Do not announce that you are being careful. Just be careful. Do not say FounderNexus in the body except an optional closing paragraph. FounderNexus is one word.

Do not invent ranges. Named public sources only. Empty cell if unknown. When sources disagree, show them separately.

Legal line once, short, on finance/legal pages: “Not legal, tax, or compensation advice.”

## Daily shipping workflow

1. Add or edit a Markdown file under content/.
2. Rebuild: python3 build.py
3. Preview from dist with http.server, then stop.

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
