# Stop-slop rules for Founder Decisions

Source: [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) by Hardik Pandya, read at commit `8da1f03` (2026-09-27). MIT License, reproduced at the bottom of this file. Sections 1 to 4 are a condensed copy of the upstream `SKILL.md` and `references/*.md`. Section 5 is our adaptation for this site. When upstream changes, re-read it and update this file.

Every new or edited owned page (library, hubs, tools, compare, about, homepage and template copy) must pass this gate before push. See `ops/stop-slop/GATE.md`.

## 1. Core rules (upstream SKILL.md)

1. **Cut filler phrases.** Remove throat-clearing openers, emphasis crutches, and adverbs.
2. **Break formulaic structures.** No binary contrasts, negative listings, dramatic fragmentation, rhetorical setups, or false agency.
3. **Use active voice.** Every sentence needs a subject doing something. Inanimate things do not perform human actions ("the complaint becomes a fix").
4. **Be specific.** No vague declaratives ("The reasons are structural"). Name the thing. No lazy extremes ("every", "always", "never") doing vague work.
5. **Put the reader in the room.** "You" beats "people". Specifics beat abstractions. No narrator-from-a-distance voice.
6. **Vary rhythm.** Mix sentence lengths. Two items beat three. End paragraphs differently. No em dashes.
7. **Trust readers.** State facts directly. Skip softening, justification, and hand-holding.
8. **Cut quotables.** If a line sounds like a pull-quote, rewrite it.

## 2. Phrases to remove (upstream references/phrases.md)

- **Throat-clearing:** "Here's the thing", "Here's what/why/this/that…", "The uncomfortable truth is", "It turns out", "The real X is", "Let me be clear", "The truth is", "I'm going to be honest", "Can we talk about".
- **Emphasis crutches:** "Full stop.", "Period.", "Let that sink in.", "This matters because", "Make no mistake", "Here's why that matters".
- **Business jargon → plain word:** navigate → handle; unpack → explain; lean into → accept; landscape → situation, field; game-changer → significant; double down → commit, increase; deep dive → analysis; take a step back → reconsider; moving forward → next; circle back → revisit; on the same page → aligned.
- **Adverbs:** cut them. Named offenders: really, just, literally, genuinely, honestly, simply, actually, deeply, truly, fundamentally, inherently, inevitably, interestingly, importantly, crucially.
- **Filler:** "At its core", "In today's X", "It's worth noting", "At the end of the day", "When it comes to", "In a world where", "The reality is".
- **Meta-commentary:** "Hint:", "Plot twist:", "Spoiler:", "You already know this, but", "X is a feature, not a bug", "Dressed up as", "The rest of this essay explains…", "Let me walk you through…", "In this section, we'll…", "As we'll see…", "I want to explore…".
- **Performative emphasis:** "creeps in", "I promise".
- **Telling instead of showing:** "This is genuinely hard", "This is what X actually looks like", "actually matters".
- **Vague declaratives:** "The implications are significant", "The stakes are high", "The consequences are real", "This is the deepest problem".

## 3. Structures to avoid (upstream references/structures.md)

- **Binary contrasts:** "Not because X. Because Y.", "X isn't the problem. Y is.", "The answer/question isn't X. It's Y.", "It feels like X. It's actually Y.", "not X, it's Y", "stops being X and starts being Y", "not just X but also Y". State Y directly.
- **Negative listing:** "Not a X. Not a Y. A Z." State Z.
- **Dramatic fragmentation:** "[Noun]. That's it.", "X. And Y. And Z." Write full sentences.
- **Rhetorical setups:** "What if…?", "Here's what I mean:", "Think about it:", "And that's okay."
- **Formulaic constructions:** "By the time X, I was Y."; "X that isn't Y".
- **False agency:** "the decision emerges", "the data tells us", "the market rewards". Name the person who acts, or use "you".
- **Narrator from a distance:** "Nobody designed this.", "This happens because…", "People tend to…".
- **Passive voice:** "X was created", "It is believed that". Find the actor and put them first.
- **Sentence starters:** avoid What/When/Where/Which/Who/Why/How openers, paragraphs opening with "So", and "Look,".
- **Rhythm:** avoid reflexive three-item lists, questions answered right away, a punchy one-liner at the end of every paragraph, stacked short fragments, "Not always. Not perfectly." hedges, and em dashes.

## 4. Scoring (upstream)

Rate each dimension 1 to 10. Below 35/50: revise.

| Dimension | Question |
|-----------|----------|
| Directness | Statements or announcements? |
| Rhythm | Varied or metronomic? |
| Trust | Respects reader intelligence? |
| Authenticity | Sounds human? |
| Density | Anything cuttable? |

## 5. Founder Decisions adaptation

The locked site rules in `README.md` and `SEO-BRIEF.md` win over any style rule.

- **Numbers and sources are locked.** Never add, remove, or change a number, range, date, or citation to fix style. Keep `## Sources` exactly as written. `ops/stop-slop/facts_guard.py` checks this on edited pages.
- **Source hedges stay.** "Typically", "often", "about", "roughly", or "~" attached to a cited figure is the source's precision, not a softener. Keep it.
- **Quoted text stays verbatim.** Text in curly quotes (source titles, quoted lines) and `## Sources` / `## Related` sections are exempt.
- **Titles, slugs, and URLs are SEO-locked.** Do not change them for style. You may tighten a meta `description` or an H1 only when it is plainly slop.
- **Keep the chrome.** `:::takeaways`, `:::steps`, `:::highlight`, choice cards, and decision tables stay. An em dash as an empty table cell ("—") is allowed.
- **Close line.** One sentence. FounderNexus appears once, as the quiet link the renderer creates. Name the decision. No "If you want founders who just…" formula.
- **Never name or link The Startup Bible** or its site. Never write "Published by FounderNexus".
- **Hard vs judgment.** `check.py` fails (HARD) on em dashes, spaced en dashes, double hyphens, throat-clearing, emphasis crutches, filler, the named adverbs, jargon, meta-commentary, vague declaratives, binary contrasts, and "What if" / "Look," openers. It warns (soft) on other -ly adverbs, lazy extremes, passive voice, false agency, "So" openers, negative listing, and Wh- starters. Fix soft hits when a better sentence exists. A soft hit that carries a cited fact ("Bessemer is widely used…", "never" quoted from a source) can stay.
- **Plain English wins over the letter of a rule.** Do not twist a sentence to dodge a pattern. If the fix reads worse, restate the fact more plainly.

---

MIT License

Copyright (c) 2025 Hardik Pandya

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
