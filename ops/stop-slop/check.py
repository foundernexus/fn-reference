#!/usr/bin/env python3
"""stop-slop checker for Founder Decisions owned pages.

Flags the mechanical parts of the stop-slop rules (ops/stop-slop/RULES.md,
adapted from https://github.com/hardikpandya/stop-slop, MIT). It does not
replace the manual read. Stdlib only. Never imported by build.py, so it can
never fail a Vercel build.

Usage:
  python3 ops/stop-slop/check.py                 # all owned content/**/*.md (not _drafts)
  python3 ops/stop-slop/check.py FILE [FILE...]  # specific files
  python3 ops/stop-slop/check.py --changed       # md files changed vs origin/main + working tree
  python3 ops/stop-slop/check.py --soft          # also print soft warnings (judgment calls)
  python3 ops/stop-slop/check.py --dist          # rendered owned HTML in dist/ (home, hubs, templates)
  python3 ops/stop-slop/check.py --generated     # report-only scan of dist/decisions + dist/benchmarks
  python3 ops/stop-slop/check.py --summary       # counts only

Exit code: 1 if any HARD violation is found (except with --generated), else 0.

What is skipped on purpose (locked content):
  - frontmatter except `description` and `close` (titles and slugs are SEO-locked;
    title hits print as info only)
  - `## Sources` and `## Related` sections (cited titles stay verbatim)
  - link URLs, inline code, HTML comments
  - a table cell whose whole content is an em dash (empty-cell marker)
"""

from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"
DIST = ROOT / "dist"

SKIP_SECTIONS = {"sources", "related", "references"}

I = re.IGNORECASE

# ---------------------------------------------------------------- HARD rules
# (id, regex, message). Must be zero on every owned page before push.
HARD: list[tuple[str, re.Pattern, str]] = []


def hard(rid: str, pat: str, msg: str, flags: int = I) -> None:
    HARD.append((rid, re.compile(pat, flags), msg))


# Punctuation
hard("em-dash", r"\u2014", "Em dash. Use a period, comma, colon, or parentheses.", 0)
hard("double-hyphen", r"\s--\s", "Double hyphen used as a dash.", 0)
hard("spaced-en-dash", r"\s\u2013\s", "Spaced en dash used as an em dash. Ranges (6–8) are fine.", 0)

# Throat-clearing openers
hard("throat-clearing", r"\bhere(?:'s| is) (?:the thing|what|why|how|this|that|the problem|where|the catch|the kicker)\b",
     "Throat-clearing 'here's what/why/how'. State the point.")
for p in [
    r"the uncomfortable truth", r"\bit turns out\b", r"\blet me be clear\b", r"\bthe truth is\b",
    r"\bi'll say it again\b", r"\bi'm going to be honest\b", r"\bcan we talk about\b",
    r"\bthe reality is\b", r"\bthe real (?:question|answer|problem|issue|story|lesson|point) is\b",
]:
    hard("throat-clearing", p, "Throat-clearing opener. State the content directly.")

# Emphasis crutches
for p in [r"\bfull stop\b", r"(?<=[A-Za-z%)][.!?] )Period\.", r"\blet that sink in\b", r"\bthis matters because\b",
          r"\bmake no mistake\b", r"\bwhy (?:that|this) matters\b"]:
    hard("emphasis-crutch", p, "Emphasis crutch. Delete it.")

# Filler phrases
for p in [r"\bat its core\b", r"\bin today's\b", r"\b(?:it's |it is )?worth noting\b", r"\bat the end of the day\b",
          r"\bwhen it comes to\b", r"\bin a world where\b", r"\bimportant to note\b", r"\bin conclusion\b",
          r"\bthe bottom line\b"]:
    hard("filler", p, "Filler phrase. Cut it.")

# Named adverbs from the stop-slop list
hard("adverb", r"\b(?:really|just|literally|genuinely|honestly|simply|actually|deeply|truly|fundamentally|inherently|inevitably|interestingly|importantly|crucially)\b",
     "Banned adverb (stop-slop list). Delete or replace with the specific fact.")

# Business jargon (stop-slop table + repo README voice list)
hard("jargon", r"\b(?:navigat(?:e|es|ing) (?:the |a |an |this |your )?(?:challenge|uncertaint|complexit|landscape)\w*|unpack(?:s|ing)?|lean(?:s|ing)? into|landscape|game[- ]changer|doubl(?:e|es|ing) down|deep[- ]dives?|take a step back|moving forward|circle back|(?:be|are|is|get|getting|stay|staying|keep|keeping|everyone|team) on the same page|delv(?:e|es|ing)|utiliz\w+|leverag(?:e|es|ing)|robust|unlock(?:s|ed|ing)?)\b",
     "Jargon. Use plain language.")

# Meta-commentary / performative emphasis / telling
for p in [r"\bhint:", r"\bplot twist\b", r"\bspoiler:", r"\byou already know this\b", r"\bthat's another post\b",
          r"\ba feature, not a bug\b", r"\bdressed up as\b", r"\bthe rest of this (?:essay|page|guide|post|article)\b",
          r"\blet me walk you\b", r"\bin this section,? we'll\b", r"\bas we'll see\b", r"\bi want to explore\b",
          r"\bcreeps? in\b", r"\bi promise\b", r"\bactually matters\b", r"\bthis is what [^.]{0,40}looks like\b",
          r"\bthink about it\b", r"\band that's okay\b", r"\bhere's what i mean\b"]:
    hard("meta", p, "Meta-commentary or performative emphasis. Delete it.")

# Vague declaratives
for p in [r"\bthe reasons are structural\b", r"\bthe implications are significant\b", r"\bthe stakes are high\b",
          r"\bthe consequences are real\b", r"\bthis is the deepest problem\b"]:
    hard("vague-declarative", p, "Vague declarative. Name the specific thing.")

# Binary contrasts
for p in [
    r"\bnot because\b[^.]{0,160}\bbut because\b",
    r"\bnot because\b[^.]{0,160}\.\s+because\b",
    r"\b(?:isn't|is not|aren't|are not|wasn't|was not)\b[^.;:!?]{1,80}[.;,]\s+(?:it's|it is|they're|they are|it was|that's)\b",
    r"\bnot\b[^.;:!?,]{1,60},\s+(?:it's|it is)\b",
    r"\bnot (?:just|only|merely|simply) [^.]{1,100}\bbut(?: also)?\b",
    r"\bstops? being\b",
    r"\bthe (?:question|answer|problem|issue|point|goal|job) (?:isn't|is not)\b",
    r"\bisn't the (?:problem|point|issue|question)\b",
    r"\bit feels like\b[^.]{0,80}\.\s+it's actually\b",
    r"\bdoesn't mean\b[^.]{0,80}\bbut actually\b",
    r"\b(?:isn't|is not|aren't|are not)\s+the\s+\w+\.\s+[^.]{1,40}\s(?:is|are)\.",
    r"(?:^|[.!?]\s+)(?:They|It|That|This) (?:are|is|was|were) not\.",
    r"(?:^|[.!?]\s+)(?:They|It|That|This) (?:aren't|isn't|wasn't|weren't)\.",
]:
    hard("binary-contrast", p, "Binary contrast ('not X, it's Y'). State Y directly.")

# Rhetorical setups
hard("rhetorical", r"(?:^|[.!?]\s+)What if\b", "'What if' setup. Make the point.", 0)
hard("rhetorical", r"(?:^|[.!?]\s+)Look,\s", "'Look,' opener. Remove.", 0)

# ---------------------------------------------------------------- SOFT rules
# Judgment calls. Print with --soft. Fix when the rewrite is clearer; ignore
# when the word carries a real fact (e.g. "Carta never publishes...").
SOFT: list[tuple[str, re.Pattern, str]] = []


def soft(rid: str, pat: str, msg: str, flags: int = I) -> None:
    SOFT.append((rid, re.compile(pat, flags), msg))


LY_ALLOW = {
    "only", "early", "family", "supply", "apply", "reply", "rally", "italy", "july", "monthly", "weekly",
    "daily", "quarterly", "yearly", "hourly", "likely", "unlikely", "fly", "belly", "ally", "holy", "ugly",
    "silly", "friendly", "costly", "lonely", "lovely", "elderly", "assembly", "anomaly", "multiply", "comply",
    "rely", "imply", "jelly", "bully", "curly", "orderly", "timely", "nightly", "biweekly", "semiannually",
    "annually", "reply", "firstly", "poly", "ply", "doily", "bubbly", "anomaly", "kelly", "sully", "wholly",
    "lily", "emily", "molly", "billy", "sally", "reilly", "apply", "resupply", "underbelly", "burly", "surly",
    "homely", "manly", "deadly", "worldly", "scholarly", "neighborly", "fatherly", "motherly", "only-",
    "fully-diluted", "ly",
}
soft("ly-adverb", r"\b[a-z]{3,}ly\b", "-ly adverb. Cut unless it carries a fact.")
soft("lazy-extreme", r"\b(?:every|always|never|everyone|everybody|nobody|no one)\b",
     "Lazy extreme. Keep only if literally true and specific.")
soft("passive", r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?(?:\w+ed|built|made|done|given|taken|shown|known|seen|written|paid|held|kept|left|sold|told|found|brought|drawn|grown|run|set|cut|spent|won|lost|priced|thrown)\b",
     "Possible passive voice. Name the actor if it hides one.")
soft("false-agency", r"\bthe (?:data|numbers|market|culture|conversation|decision|pack|room)\s+(?:tells?|says|shows|rewards|punishes|shifts|moves|emerges|decides|wants|asks)\b",
     "False agency. Name the person.")
soft("false-agency", r"\bemerges?\b", "'emerges'. Someone decides or builds it.")
soft("so-opener", r"^So[, ]", "Paragraph starts with 'So'.", 0)
soft("negative-listing", r"(?:^|[.!?]\s+)Not [^.]{1,50}\.\s+Not [^.]{1,50}\.", "Negative listing / staccato 'Not X. Not Y.'", 0)
soft("wh-starter", r"(?:^|[.!?]\s+)(?:What|When|Where|Which|Who|Why|How)\b(?![^.?!]*\?)(?!:)", "Sentence starts with a Wh- word. Lead with the subject.", 0)

# ---------------------------------------------------------------- text prep

LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
CODE = re.compile(r"`[^`]*`")
COMMENT = re.compile(r"<!--.*?-->", re.S)
URL = re.compile(r"https?://\S+")


def norm(s: str) -> str:
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = COMMENT.sub(" ", s)
    s = LINK.sub(r"\1", s)
    s = CODE.sub(" ", s)
    s = URL.sub(" ", s)
    return s


def split_frontmatter(text: str) -> tuple[dict, str, int]:
    if not text.startswith("---"):
        return {}, text, 0
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text, 0
    fm_raw = text[3:end]
    fm = {}
    for line in fm_raw.splitlines():
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = (m.group(2).strip().strip('"').strip("'"), line)
    body_start = end + len("\n---")
    return fm, text[body_start:], text[:body_start].count("\n")


def md_units(path: Path):
    """Yield (line_no, kind, text) prose units from a markdown source file."""
    text = path.read_text(encoding="utf-8")
    fm, body, offset = split_frontmatter(text)
    lines = text.splitlines()
    for key in ("description", "close"):
        if key in fm:
            val, raw = fm[key]
            ln = next((i + 1 for i, l in enumerate(lines) if l == raw), 1)
            yield ln, f"fm:{key}", val
    if "title" in fm:
        val, raw = fm["title"]
        ln = next((i + 1 for i, l in enumerate(lines) if l == raw), 1)
        yield ln, "fm:title", val
    skipping = False
    for i, line in enumerate(body.splitlines()):
        ln = offset + i + 1
        s = line.strip()
        if s.startswith("## "):
            skipping = s[3:].strip().lower() in SKIP_SECTIONS
            if not skipping:
                yield ln, "heading", s.lstrip("#").strip()
            continue
        if skipping or not s:
            continue
        if s.startswith(":::"):
            label = s.lstrip(":").split(None, 1)
            if len(label) == 2:
                yield ln, "fence-label", label[1]
            continue
        if s.startswith("#"):
            yield ln, "heading", s.lstrip("#").strip()
            continue
        if s.startswith("|"):
            if re.match(r"^\|[\s:|-]+\|?$", s):
                continue
            cells = [c.strip() for c in s.strip("|").split("|")]
            cells = [c for c in cells if c not in ("—", "-", "")]
            yield ln, "table", " | ".join(cells)
            continue
        item = re.sub(r"^(?:[-*+]|\d+\.)\s+", "", s)
        # A list item that opens with a link is a page title (SEO-locked): skip Wh- checks on it.
        yield ln, ("link-item" if item.startswith("[") else "prose"), item


PUNCT_RULES = {"em-dash", "double-hyphen", "spaced-en-dash"}
QUOTED = re.compile(r"\u201c[^\u201d]{0,200}\u201d")


def scan_units(units, include_soft: bool):
    hits = []
    for ln, kind, raw in units:
        t = norm(raw)
        # Text inside curly quotes is someone else's words (a cited title or a quoted
        # source line). It stays verbatim, so HARD rules skip it.
        t_unquoted = QUOTED.sub(" ", t)
        for rid, pat, msg in HARD:
            for m in pat.finditer(t_unquoted):
                level = "info" if kind == "fm:title" else "HARD"
                hits.append((ln, level, rid, m.group(0), t, msg, kind))
        if include_soft and kind not in ("fm:title",):
            for rid, pat, msg in SOFT:
                if rid == "wh-starter" and kind != "prose":
                    continue
                for m in pat.finditer(t):
                    w = m.group(0).lower()
                    if rid == "ly-adverb" and (w in LY_ALLOW or w.endswith("ply") and len(w) <= 6):
                        continue
                    if rid == "ly-adverb" and w == "fully" and re.match(r"\s*[- ]diluted", t[m.end():], I):
                        continue
                    hits.append((ln, "soft", rid, m.group(0), t, msg, kind))
    return hits


# ---------------------------------------------------------------- dist mode

class TextExtractor(HTMLParser):
    SKIP_TAGS = {"script", "style", "nav", "header", "footer", "noscript", "svg"}
    BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "td", "th", "div", "section", "blockquote", "summary", "dd", "dt"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_main = False
        self.skip_depth = 0
        self.card_depth = 0
        self.section_skip = False
        self.cur_h2 = None
        self.buf: list[str] = []
        self.units: list[str] = []

    def flush(self):
        t = " ".join("".join(self.buf).split())
        if t:
            self.units.append(t)
        self.buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main":
            self.in_main = True
        if not self.in_main:
            return
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
        if tag == "a" and "card" in (a.get("class") or "").split():
            self.card_depth += 1
        if tag == "h2":
            self.flush()
            self.cur_h2 = []
        if tag in self.BLOCK:
            self.flush()

    def handle_endtag(self, tag):
        if not self.in_main:
            return
        if tag == "main":
            self.flush()
            self.in_main = False
        if tag in self.SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
        if tag == "a" and self.card_depth:
            self.card_depth -= 1
            self.buf = []
        if tag == "h2" and self.cur_h2 is not None:
            name = "".join(self.cur_h2).strip().lower()
            self.section_skip = name in SKIP_SECTIONS
            self.cur_h2 = None
        if tag in ("article",):
            self.section_skip = False
        if tag in self.BLOCK:
            self.flush()

    def handle_data(self, data):
        if not self.in_main or self.skip_depth or self.card_depth:
            return
        if self.cur_h2 is not None:
            self.cur_h2.append(data)
        if self.section_skip and self.cur_h2 is None:
            return
        self.buf.append(data)


def dist_units(path: Path):
    p = TextExtractor()
    p.feed(path.read_text(encoding="utf-8"))
    p.flush()
    for i, u in enumerate(p.units):
        if u.strip() in ("—",):
            continue
        yield i + 1, "html", u


def owned_dist_files() -> list[Path]:
    out = []
    for f in sorted(DIST.rglob("index.html")):
        rel = f.relative_to(DIST).as_posix()
        if rel.startswith(("decisions/", "benchmarks/")):
            continue
        out.append(f)
    return out


def generated_dist_files() -> list[Path]:
    return sorted(
        f for f in DIST.rglob("index.html")
        if f.relative_to(DIST).as_posix().startswith(("decisions/", "benchmarks/"))
    )


# ---------------------------------------------------------------- main

def owned_md_files() -> list[Path]:
    return sorted(p for p in CONTENT.rglob("*.md") if "_drafts" not in p.parts)


def changed_md_files() -> list[Path]:
    names: set[str] = set()
    cmds = [
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        ["git", "diff", "--name-only"],
        ["git", "diff", "--name-only", "--cached"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    for c in cmds:
        try:
            out = subprocess.run(c, cwd=ROOT, capture_output=True, text=True, check=False).stdout
        except OSError:
            continue
        names.update(n.strip() for n in out.splitlines() if n.strip())
    files = []
    for n in sorted(names):
        p = ROOT / n
        if n.startswith("content/") and n.endswith(".md") and "_drafts/" not in n and p.exists():
            files.append(p)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--soft", action="store_true", help="also print soft warnings")
    ap.add_argument("--dist", action="store_true", help="scan rendered owned HTML in dist/")
    ap.add_argument("--generated", action="store_true", help="report-only scan of dist/decisions and dist/benchmarks")
    ap.add_argument("--changed", action="store_true", help="only md files changed vs origin/main")
    ap.add_argument("--summary", action="store_true", help="counts only")
    args = ap.parse_args()

    if args.generated:
        targets = [(f, dist_units(f)) for f in generated_dist_files()]
    elif args.dist:
        targets = [(f, dist_units(f)) for f in owned_dist_files()]
    else:
        if args.files:
            files = [Path(f).resolve() for f in args.files]
        elif args.changed:
            files = changed_md_files()
        else:
            files = owned_md_files()
        targets = [(f, md_units(f)) for f in files]

    total_hard = total_soft = total_info = 0
    by_rule: dict[str, int] = {}
    per_file: list[tuple[str, int, int]] = []
    for f, units in targets:
        hits = scan_units(units, args.soft)
        rel = f.relative_to(ROOT).as_posix() if f.is_relative_to(ROOT) else str(f)
        h = sum(1 for x in hits if x[1] == "HARD")
        s = sum(1 for x in hits if x[1] == "soft")
        total_hard += h
        total_soft += s
        total_info += sum(1 for x in hits if x[1] == "info")
        per_file.append((rel, h, s))
        for x in hits:
            if x[1] != "info":
                key = f"{x[1]}:{x[2]}"
                by_rule[key] = by_rule.get(key, 0) + 1
        if not args.summary:
            for ln, level, rid, match, text, msg, kind in hits:
                ctx = text if len(text) <= 160 else text[max(0, text.lower().find(match.lower()) - 70):][:160]
                print(f"{rel}:{ln}: {level} [{rid}] {match!r} ({kind}) {msg}\n    … {ctx}")

    print("\n== stop-slop summary ==")
    for rel, h, s in per_file:
        if h or s:
            print(f"  {rel}: hard={h}" + (f" soft={s}" if args.soft else ""))
    for k in sorted(by_rule, key=lambda k: (-by_rule[k], k)):
        print(f"  {k}: {by_rule[k]}")
    print(f"files={len(per_file)} HARD={total_hard}" + (f" soft={total_soft}" if args.soft else "")
          + (f" info(title, locked)={total_info}" if total_info else ""))
    if args.generated:
        print("(report only: /decisions/ and /benchmarks/ come from foundernexus/fn-content; do not edit here)")
        return 0
    if total_hard:
        print("FAIL: fix every HARD hit, then do the manual read against ops/stop-slop/RULES.md.")
        return 1
    print("PASS (mechanical). Still required: manual read against ops/stop-slop/RULES.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
