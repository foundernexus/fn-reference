#!/usr/bin/env python3
"""Build Founder Decisions from Markdown into dist/.

Stdlib only. Drop a page in content/, run: python3 build.py

Canonical host is a placeholder. Public publish needs Matt McKinney's approval.
"""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import http.client
import shutil
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
DIST = ROOT / "dist"

# Placeholder. Matt must approve anything public, and any BASE_PATH change.
BASE_URL = "https://founderdecisions.com"
BASE_PATH = ""  # e.g. "/library" if this tree is mounted under that path

SITE_NAME = "Founder Decisions"
TAGLINE = "Decision pages for venture-scale founders."
# VEN (Venture Executive Network), formerly FounderNexus. www.foundernexus.com 301s here.
PUBLISHER_NAME = "VEN"
PUBLISHER_URL = "https://www.venexecs.com/?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library"
DISCLAIMER_LEGAL = "Not legal, tax, or compensation advice."

SECTIONS = {
    "library": {
        "title": "Library",
        "nav": "Library",
        "kicker": "Library",
        "description": "Sourced decision pages for seed to Series B founders: fundraising, equity, hiring, the board, finance, and go-to-market. One question per page.",
    },
    "tools": {
        "title": "Tools",
        "nav": "Tools",
        "kicker": "Tools",
        "description": "Calculators that turn a proposed number into something you can take to counsel, the board, or a candidate.",
    },
    "compare": {
        "title": "Comparisons",
        "nav": "Compare",
        "kicker": "Comparisons",
        "description": "Side-by-side comparisons for founders choosing a peer group or a coach, with each option's entry filters and sources.",
    },
}

NAV_ITEMS = [
    ("library", "Library", "/library/"),
    ("benchmarks", "Benchmarks", "/benchmarks/"),
    ("tools", "Tools", "/tools/"),
    ("compare", "Compare", "/compare/"),
    ("about", "About", "/about/"),
]

CLUSTERS = {
    "equity": {
        "section": "library",
        "title": "Equity & cap table",
        "description": "Size the option pool, check executive grants by stage, and plan the 409A after a priced round.",
    },
    "hiring": {
        "section": "library",
        "title": "Hiring executives",
        "description": "When to hire the first VP, which leadership seat comes first after Series A, and how to onboard them.",
    },
    "finance": {
        "section": "library",
        "title": "Finance, metrics & runway",
        "description": "Burn multiple, NRR and GRR, what counts as ARR, AI gross margin, and when to hire a CFO.",
    },
    "board": {
        "section": "library",
        "title": "Board & governance",
        "description": "Build the Series A board, run the meeting, write the monthly update, and report a missed plan.",
    },
    "gtm": {
        "section": "library",
        "title": "Go-to-market",
        "description": "Find, win, and keep your first customers: demand tests, pilots, contracts, pricing, and enterprise deals.",
    },
    "fundraising": {
        "section": "library",
        "title": "Fundraising",
        "description": "From the first angel check to the Series A data room: decks, SAFEs, term sheets, venture debt, and runway.",
    },
    "rooms": {
        "section": "library",
        "title": "Founder rooms",
        "description": "Compare peer groups, CEO forums, and executive coaching by stage, price, and who gets in.",
    },
}


def url(path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    return BASE_PATH.rstrip("/") + path


def abs_url(path: str) -> str:
    return BASE_URL.rstrip("/") + url(path)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        raise ValueError("Missing YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Unterminated YAML frontmatter")
    raw, body = parts[1], parts[2].lstrip("\n")
    data: dict = {}
    current_list = None
    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        m_list = re.match(r"^(\s*)-\s+(.*)$", line)
        if m_list and current_list is not None:
            data[current_list].append(_scalar(m_list.group(2).strip()))
            continue
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if not m:
            raise ValueError(f"Cannot parse frontmatter line: {line!r}")
        key, val = m.group(1), m.group(2)
        if val == "":
            data[key] = []
            current_list = key
        else:
            current_list = None
            data[key] = _scalar(val)
    return data, body


def _scalar(val: str):
    if val in ("true", "True", "yes"):
        return True
    if val in ("false", "False", "no"):
        return False
    if (val.startswith('"') and val.endswith('"')) or (
        val.startswith("'") and val.endswith("'")
    ):
        return val[1:-1]
    return val


def _strong(m: re.Match) -> str:
    # Short bold figure ranges ("10–20%", "$50k–$100k") get class="fig" so CSS can keep
    # them on one line in narrow table cells and In short bullets (styled in .prose only).
    t = m.group(1)
    if len(t) <= 24 and "\u2013" in t and " " not in t and re.search(r"\d", t):
        return f'<strong class="fig">{t}</strong>'
    return f"<strong>{t}</strong>"


def inline_md(text: str) -> str:
    # Capture markdown links before escape so query-string & is not double-encoded
    # into &amp;amp; inside hrefs.
    links: list[tuple[str, str]] = []

    def _park_link(m: re.Match) -> str:
        links.append((m.group(1), m.group(2)))
        return f"\x00MDLINK{len(links) - 1}\x00"

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _park_link, text)
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", _strong, text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    for i, (label, href) in enumerate(links):
        text = text.replace(
            f"\x00MDLINK{i}\x00",
            f'<a href="{html.escape(href, quote=True)}">{html.escape(label)}</a>',
        )
    return text


def render_markdown(src: str) -> str:
    src = re.sub(r"<!--.*?-->", "", src, flags=re.S)
    lines = src.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if re.match(r"^---+\s*$", line):
            out.append("<hr>")
            i += 1
            continue
        if line.strip().startswith(":::"):
            fence = line.strip()[3:].strip()
            i += 1
            if not fence:
                continue
            kind, _, label = fence.partition(" ")
            kind = kind.lower().strip()
            buf = []
            while i < len(lines) and lines[i].strip() != ":::":
                buf.append(lines[i])
                i += 1
            if i < len(lines) and lines[i].strip() == ":::":
                i += 1
            if kind == "group":
                # :::group Label … ::: with "- [Title](/path/): one line" items → a
                # scannable pick list. Consecutive groups share one grid (see end).
                lis = []
                for ln in buf:
                    m = re.match(r"^\s*[-*]\s+\[([^\]]+)\]\(([^)]+)\)\s*:?\s*(.*)$", ln)
                    if not m:
                        continue
                    lis.append(
                        f'<li><a href="{html.escape(m.group(2), quote=True)}">'
                        f'<span class="pick-title">{html.escape(m.group(1))}</span>'
                        f'<span class="pick-desc">{inline_md(m.group(3))}</span></a></li>'
                    )
                out.append(
                    f'<section class="pick-group"><h2 class="pick-label">{html.escape(label.strip())}</h2>'
                    f'<ul class="pick-list">{"".join(lis)}</ul></section>'
                )
                continue
            inner_html = render_markdown("\n".join(buf))
            if kind in ("takeaways", "takeaway"):
                label = label.strip() or "In short"
                out.append(
                    f'<aside class="takeaways"><p class="takeaways-label">{html.escape(label)}</p>{inner_html}</aside>'
                )
            elif kind in ("highlight", "note"):
                out.append(f'<aside class="highlight">{inner_html}</aside>')
            elif kind in ("steps", "step"):
                # :::steps [optional label] … :::  → numbered step/layer stack (CSS-only).
                # Prefer an ordered list inside; headings + paragraphs also work.
                label = label.strip()
                label_html = (
                    f'<p class="steps-label">{html.escape(label)}</p>' if label else ""
                )
                out.append(f'<div class="steps">{label_html}{inner_html}</div>')
            else:
                out.append(inner_html)
            continue
        if line.startswith("#"):
            m = re.match(r"^(#{1,4})\s+(.*)$", line)
            if m:
                level = len(m.group(1))
                text = m.group(2).strip()
                hid = slugify(text)
                hid_attr = html.escape(hid, quote=True)
                # Section permalink: a quiet --blue "#" that shows on hover/focus
                # (CSS generates the glyph, so heading text and SEO stay clean).
                anchor = (
                    f'<a class="h-anchor" href="#{hid_attr}" aria-label="Link to this section"></a>'
                    if level in (2, 3)
                    else ""
                )
                out.append(
                    f'<h{level} id="{hid_attr}">{inline_md(text)}{anchor}</h{level}>'
                )
                i += 1
                continue
        if line.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip("> ").rstrip())
                i += 1
            paras, cur = [], []
            for ln in buf + [""]:
                if ln:
                    cur.append(ln)
                elif cur:
                    paras.append(" ".join(cur))
                    cur = []
            inner = "".join(f"<p>{inline_md(t)}</p>" for t in paras)
            out.append(f"<blockquote>{inner}</blockquote>")
            continue
        if line.strip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(_render_table(rows))
            continue
        if re.match(r"^[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                items.append(re.sub(r"^[-*]\s+", "", lines[i]))
                i += 1
            lis = "".join(f"<li>{inline_md(it)}</li>" for it in items)
            out.append(f"<ul>{lis}</ul>")
            continue
        if re.match(r"^\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i]))
                i += 1
            lis = "".join(f"<li>{inline_md(it)}</li>" for it in items)
            out.append(f"<ol>{lis}</ol>")
            continue
        buf = [line]
        i += 1
        while (
            i < len(lines)
            and lines[i].strip()
            and not lines[i].startswith("#")
            and not lines[i].strip().startswith("|")
            and not re.match(r"^[-*]\s+", lines[i])
            and not re.match(r"^\d+\.\s+", lines[i])
            and not lines[i].startswith(">")
            and not re.match(r"^---+\s*$", lines[i])
            and not lines[i].strip().startswith(":::")
        ):
            buf.append(lines[i])
            i += 1
        out.append(f"<p>{inline_md(' '.join(buf))}</p>")
    merged: list[str] = []
    for block in out:
        if block.startswith('<section class="pick-group">'):
            if merged and merged[-1].startswith('<div class="pick-grid">'):
                merged[-1] = merged[-1][: -len("</div>")] + block + "</div>"
            else:
                merged.append(f'<div class="pick-grid">{block}</div>')
        else:
            merged.append(block)
    return "\n".join(merged)


def _looks_numeric(text: str) -> bool:
    """Mark short figure cells for nowrap. Skip prose that merely contains a year or digit."""
    plain = re.sub(r"[¹²³⁴⁵⁶⁷⁸⁹⁰*†‡]", "", text).replace("{br}", " ").strip()
    if len(plain) > 40:
        return False
    if not re.search(r"[\d$%×]|—", plain):
        return False
    letters = len(re.findall(r"[A-Za-z]", plain))
    return letters <= 8


_FIGURE_RE = re.compile(
    r"^[~≈<>≤≥]?\s*[-+]?\$?\d[\d.,]*\s*(%|x|×|[KMBkmb])?"
    r"(\s*[–-]\s*\$?\d[\d.,]*\s*(%|x|×|[KMBkmb])?)?\+?$"
)


def _is_figure(text: str) -> bool:
    """A cell that is only a figure or a figure range (bold markers ignored)."""
    plain = text.replace("**", "").strip()
    return bool(_FIGURE_RE.match(plain))


def _is_blank_cell(text: str) -> bool:
    return text.replace("**", "").strip() in ("", "—")


def _render_table(rows: list[str]) -> str:
    parsed = []
    for row in rows:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        parsed.append(cells)
    if len(parsed) >= 2 and all(re.match(r"^:?-+:?$", c or "") for c in parsed[1]):
        head, body = parsed[0], parsed[2:]
    else:
        head, body = parsed[0], parsed[1:]

    def cell_inner(c: str) -> str:
        return "<br>".join(inline_md(part) for part in c.split("{br}"))

    # Figure-only columns (after the label column) align right so digits stack.
    ncols = len(head)
    fig_cols = {
        idx
        for idx in range(1, ncols)
        if body
        and any(_is_figure(r[idx]) for r in body if idx < len(r))
        and all(_is_figure(r[idx]) or _is_blank_cell(r[idx]) for r in body if idx < len(r))
    }

    def th_html(idx: int, c: str) -> str:
        cls = ' class="num-col"' if idx in fig_cols else ""
        return f"<th{cls}>{cell_inner(c)}</th>"

    th = "".join(th_html(idx, c) for idx, c in enumerate(head))
    trs = []
    for row in body:
        tds = []
        for idx, c in enumerate(row):
            classes = []
            if _looks_numeric(c):
                classes.append("num")
            if idx in fig_cols:
                classes.append("num-col")
            # Routing cell: the whole cell is one internal link (hub "Use" columns).
            if re.fullmatch(r"\[[^\]]+\]\(/[^)\s]*\)", c):
                classes.append("route")
            cls = f' class="{" ".join(classes)}"' if classes else ""
            tds.append(f"<td{cls}>{cell_inner(c)}</td>")
        trs.append(f"<tr>{''.join(tds)}</tr>")
    return (
        '<div class="table-wrap"><table>'
        f"<thead><tr>{th}</tr></thead><tbody>{''.join(trs)}</tbody>"
        "</table></div>"
    )


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def page_path(fm: dict) -> str:
    section = fm["section"]
    slug = fm["slug"]
    cluster = fm.get("cluster")
    if section == "about":
        return "/about/"
    if section == "library" and cluster:
        return f"/library/{cluster}/{slug}/"
    return f"/{section}/{slug}/"


def load_pages() -> list[dict]:
    pages = []
    for path in sorted(CONTENT.rglob("*.md")):
        if path.name.startswith("_") and path.name != "_hub.md":
            continue
        fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        required = ["title", "description", "slug", "section", "date"]
        missing = [k for k in required if k not in fm]
        if missing:
            raise SystemExit(f"{path}: missing {missing}")
        fm["_src"] = path
        fm["_body"] = body
        fm["draft"] = bool(fm.get("draft", False))
        fm["related"] = fm.get("related") or []
        if path.name == "_hub.md":
            cluster = fm.get("cluster") or path.parent.name
            fm["cluster"] = cluster
            fm["layout"] = "hub"
            fm["path"] = f"/{fm['section']}/{cluster}/"
        else:
            fm["layout"] = fm.get("layout", "article")
            fm["path"] = page_path(fm)
        pages.append(fm)
    return pages


def published(pages: list[dict]) -> list[dict]:
    return [p for p in pages if not p["draft"]]


def content_pages(pages: list[dict]) -> list[dict]:
    return [p for p in pages if p["section"] in SECTIONS]


# ---------------------------------------------------------------------------
# HTML chrome
# ---------------------------------------------------------------------------

FN_CONTENT_REPO = "foundernexus/fn-content"
FN_RENDERS_DIR = "renders/founderdecisions"
FN_BENCHMARKS_DIR = "renders/founderdecisions-benchmarks"


_TRANSIENT_FETCH_ERRORS = (
    http.client.RemoteDisconnected,
    http.client.IncompleteRead,
    ConnectionResetError,
    TimeoutError,
    urllib.error.URLError,
)


def _urlopen_with_retries(req: urllib.request.Request, *, what: str, attempts: int = 5):
    """Open URL with retries for transient disconnects (common on Vercel→GitHub)."""
    last: BaseException | None = None
    for i in range(attempts):
        try:
            return urllib.request.urlopen(req, timeout=60)
        except urllib.error.HTTPError:
            raise
        except _TRANSIENT_FETCH_ERRORS as e:
            last = e
            if i == attempts - 1:
                break
            delay = 0.5 * (2**i)
            print(f"retry {i + 1}/{attempts - 1} after {what}: {type(e).__name__}: {e}")
            time.sleep(delay)
    raise SystemExit(f"{what} failed after {attempts} attempts: {last!r}") from last


def _github_contents(path: str) -> tuple[int, bytes]:
    token = os.environ.get("FN_CONTENT_TOKEN")
    if not token:
        raise SystemExit(
            "FN_CONTENT_TOKEN is required. Fine-grained PAT, foundernexus/fn-content, contents: read."
        )
    url = (
        f"https://api.github.com/repos/{FN_CONTENT_REPO}/contents/{path}?ref=main"
    )
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "founderdecisions-build",
        },
    )
    try:
        with _urlopen_with_retries(req, what=f"fetch {path}") as res:
            return res.status, res.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


INTERNAL_SOURCE_HOSTS = (
    "startup-bible-theta.vercel.app",
    "startup-bible",
)
PUBLIC_SESSION_SOURCE_URL = PUBLISHER_URL
PUBLIC_SESSION_SOURCE_LABEL = "VEN session"


def _is_internal_source_url(url: str) -> bool:
    u = (url or "").lower()
    return any(h in u for h in INTERNAL_SOURCE_HOSTS)


_FN_URL_RE = None


def _rebrand_fn_text(text: str) -> str:
    """fn-content still carries FounderNexus wording and foundernexus.com links.
    Render them as VEN / www.venexecs.com (UTM params kept). Fix here, never in
    generated /decisions/ or /benchmarks/ output."""
    import re
    global _FN_URL_RE
    if not text or "oundernexus" not in text.lower():
        return text
    if _FN_URL_RE is None:
        _FN_URL_RE = re.compile(r"https?://(?:www\.)?foundernexus\.com/?(?=[?#\s\"')\]]|$)", re.I)
    out = _FN_URL_RE.sub("https://www.venexecs.com/", text)
    out = out.replace(
        "FounderNexus convenes stage-matched founder groups around decisions like this one.",
        "VEN convenes small peer sessions around decisions like this one.",
    )
    out = re.sub(r"\bFounderNexus\b", "VEN", out)
    return out


def rebrand_page(obj):
    if isinstance(obj, dict):
        return {k: rebrand_page(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [rebrand_page(v) for v in obj]
    if isinstance(obj, str):
        return _rebrand_fn_text(obj)
    return obj


def _scrub_internal_source_text(text: str) -> str:
    """Remove Startup Bible URLs/names from public copy. Keep VEN session framing."""
    if not text:
        return text
    import re
    out = text
    # Drop "Playbook: <bible-url>" tails
    out = re.sub(
        r"(?i)\s*Playbook:\s*https?://startup-bible-theta\.vercel\.app\S*",
        "",
        out,
    )
    out = re.sub(
        r"(?i)https?://startup-bible-theta\.vercel\.app\S*",
        PUBLIC_SESSION_SOURCE_URL,
        out,
    )
    out = re.sub(r"(?i)The Startup Bible", "a VEN session", out)
    out = re.sub(r"(?i)Startup Bible", "VEN session", out)
    return _rebrand_fn_text(out).strip()


def sanitize_decision_page(page: dict) -> dict:
    """Public pages must never show Startup Bible URLs or names. Internal-only source."""
    import copy
    page = copy.deepcopy(page)
    src = str(page.get("source_url") or "")
    if _is_internal_source_url(src):
        page["source_url"] = PUBLIC_SESSION_SOURCE_URL
        page["source_label"] = PUBLIC_SESSION_SOURCE_LABEL
    # Scrub nested strings in blocks / FAQ
    def walk(obj):
        if isinstance(obj, dict):
            return {k: walk(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [walk(v) for v in obj]
        if isinstance(obj, str):
            return _scrub_internal_source_text(obj)
        return obj
    page["blocks"] = walk(page.get("blocks") or [])
    for key in ("meta_description", "title", "stage_label"):
        if isinstance(page.get(key), str):
            page[key] = _scrub_internal_source_text(page[key])
    fn = page.get("fn_link")
    if isinstance(fn, dict):
        page["fn_link"] = walk(fn)
    return rebrand_page(page)


def fetch_json_dir(dir_path: str, *, sanitize: bool = False) -> list[dict]:
    """Load renders/<dir>/**/*.json from fn-content. 404 => no pages yet."""
    code, body = _github_contents(dir_path)
    if code == 404:
        return []
    if code != 200:
        raise SystemExit(f"fetch {dir_path} failed: {code} {body[:400]!r}")
    try:
        items = json.loads(body)
    except json.JSONDecodeError as e:
        raise SystemExit(f"invalid JSON listing {dir_path}: {e}") from e
    if not isinstance(items, list):
        raise SystemExit(f"{dir_path} is not a directory listing")
    files: list[dict] = []
    queue = list(items)
    while queue:
        item = queue.pop(0)
        if item.get("type") == "dir" and item.get("path"):
            c2, b2 = _github_contents(item["path"])
            if c2 == 404:
                continue
            if c2 != 200:
                raise SystemExit(
                    f"fetch {item['path']} failed: {c2} {b2[:400]!r}"
                )
            queue.extend(json.loads(b2))
        elif str(item.get("name", "")).endswith(".json") and item.get("path"):
            files.append(item)
    pages: list[dict] = []
    token = os.environ["FN_CONTENT_TOKEN"]
    for item in files:
        req = urllib.request.Request(
            f"https://api.github.com/repos/{FN_CONTENT_REPO}/contents/{item['path']}?ref=main",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.raw",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "founderdecisions-build",
            },
        )
        try:
            with _urlopen_with_retries(req, what=f"fetch {item['path']}") as res:
                raw = res.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            raise SystemExit(
                f"fetch {item['path']} failed: {e.code} {e.read()[:400]!r}"
            ) from e
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            raise SystemExit(f"invalid JSON {item['path']}: {e}") from e
        if not isinstance(data, dict) or not data.get("slug"):
            raise SystemExit(f"{item['path']} missing slug")
        pages.append(sanitize_decision_page(data) if sanitize else data)
    return pages


def fetch_decision_json() -> list[dict]:
    return fetch_json_dir(FN_RENDERS_DIR, sanitize=True)


def fetch_benchmark_json() -> list[dict]:
    return [rebrand_page(p) for p in fetch_json_dir(FN_BENCHMARKS_DIR)]



def ld_json_script(payload: object) -> str:
    """Serialize JSON-LD for <head>. Safe for any braces; never double-escape."""
    blob = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
    return f'<script type="application/ld+json">{blob}</script>\n'

def page_modified(p: dict) -> str:
    """Last real edit date: max(date, updated). ISO strings compare correctly."""
    return max(str(p.get("date") or ""), str(p.get("updated") or "")) or date.today().isoformat()


def newest_modified(pages: list[dict], fallback: str = "") -> str:
    dates = [page_modified(p) for p in pages if p.get("date")]
    return max(dates + ([fallback] if fallback else [])) if (dates or fallback) else date.today().isoformat()


_PUBLISHER = {"@type": "Organization", "name": SITE_NAME, "url": BASE_URL + "/"}


def breadcrumb_ld(trail: list[tuple[str, str | None]], canonical_path: str) -> dict:
    items = []
    for i, (label, href) in enumerate(trail, 1):
        if href:
            rel = href[len(BASE_PATH.rstrip("/")):] if BASE_PATH.strip("/") and href.startswith(BASE_PATH.rstrip("/")) else href
            item_url = abs_url(rel)
        else:
            item_url = abs_url(canonical_path)
        items.append({"@type": "ListItem", "position": i, "name": label, "item": item_url})
    return {"@type": "BreadcrumbList", "itemListElement": items}


def owned_json_ld(
    *,
    kind: str,
    title: str,
    description: str,
    canonical_path: str,
    trail: list[tuple[str, str | None]] | None = None,
    published: str = "",
    modified: str = "",
    section_name: str = "",
) -> str:
    """Article / CollectionPage + BreadcrumbList for owned (non fn-content) pages."""
    page_url = abs_url(canonical_path)
    node: dict = {
        "@type": kind,
        "@id": page_url + "#page" if kind != "Article" else page_url + "#article",
        "url": page_url,
        "name" if kind != "Article" else "headline": title,
        "description": description,
        "inLanguage": "en",
        "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": BASE_URL + "/"},
        "publisher": _PUBLISHER,
    }
    if kind == "Article":
        node["mainEntityOfPage"] = page_url
        node["author"] = _PUBLISHER
        if section_name:
            node["articleSection"] = section_name
    if published:
        node["datePublished"] = published
    if modified:
        node["dateModified"] = modified
    graph = [node]
    if trail:
        graph.append(breadcrumb_ld(trail, canonical_path))
    return ld_json_script({"@context": "https://schema.org", "@graph": graph})


def home_json_ld() -> str:
    return ld_json_script(
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebSite",
                    "@id": BASE_URL + "/#website",
                    "name": SITE_NAME,
                    "url": BASE_URL + "/",
                    "description": TAGLINE,
                    "inLanguage": "en",
                    "publisher": {"@id": BASE_URL + "/#org"},
                },
                {
                    "@type": "Organization",
                    "@id": BASE_URL + "/#org",
                    "name": SITE_NAME,
                    "url": BASE_URL + "/",
                    "logo": abs_url("/assets/favicon.png"),
                },
            ],
        }
    )


def json_ld_for_decision(page: dict) -> str:
    types = page.get("schema") or []
    blocks = {b.get("type"): b for b in page.get("blocks") or [] if isinstance(b, dict)}
    nodes: list[dict] = []
    if "Article" in types:
        nodes.append(
            {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": page.get("title"),
                "description": page.get("meta_description") or page.get("title"),
                "datePublished": page.get("source_date"),
                "url": abs_url(f"/decisions/{page['slug']}/"),
            }
        )
    if "FAQPage" in types:
        faq = blocks.get("faq") or {}
        items = faq.get("items") or []
        nodes.append(
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": it.get("q"),
                        "acceptedAnswer": {"@type": "Answer", "text": it.get("a")},
                    }
                    for it in items
                    if it.get("q")
                ],
            }
        )
    if not nodes:
        return ""
    payload = nodes[0] if len(nodes) == 1 else nodes
    return ld_json_script(payload)


def render_decision_json(page: dict) -> str:
    slug = page["slug"]
    blocks = page.get("blocks") or []
    parts: list[str] = []
    for b in blocks:
        kind = b.get("type")
        if kind == "situation":
            parts.append(f"<p>{html.escape(str(b.get('text') or ''))}</p>")
        elif kind == "options":
            # Map existing options JSON → choice cards (renderer only; no content invent).
            items = [str(it) for it in (b.get("items") or [])]
            n = len(items)
            cols = 3 if n == 3 or n >= 5 else 2
            cards = []
            for i, it in enumerate(items, 1):
                cards.append(
                    f'<div class="choice-card" role="listitem">'
                    f'<span class="choice-index" aria-hidden="true">{i}</span>'
                    f'<p class="choice-text">{html.escape(it)}</p>'
                    f"</div>"
                )
            parts.append(
                f'<h2 id="options">Options</h2>'
                f'<div class="choice-grid choice-grid-{cols}" role="list">'
                f'{"".join(cards)}</div>'
            )
        elif kind == "what_mattered":
            items = b.get("items") or []
            lis = "".join(f"<li>{html.escape(str(it))}</li>" for it in items)
            parts.append(f"<h2>What mattered</h2><ul>{lis}</ul>")
        elif kind == "what_was_done":
            parts.append(
                f"<h2>What was done</h2><p>{html.escape(str(b.get('text') or ''))}</p>"
            )
        elif kind == "claim":
            parts.append(
                f'<p class="claim"><span class="claim-label">Claim</span>'
                f'{html.escape(str(b.get("text") or ""))}</p>'
            )
        elif kind == "faq":
            items = b.get("items") or []
            dl = []
            for it in items:
                dl.append(
                    f"<dt>{html.escape(str(it.get('q') or ''))}</dt>"
                    f"<dd>{html.escape(str(it.get('a') or ''))}</dd>"
                )
            parts.append(f"<h2>FAQ</h2><dl>{''.join(dl)}</dl>")
    fn = page.get("fn_link") or {}
    fn_html = ""
    if fn.get("href") and fn.get("text"):
        fn_html = (
            f'<p class="article-close"><a href="{html.escape(fn["href"], quote=True)}" '
            f'data-fn-click="{html.escape(slug, quote=True)}">'
            f'{html.escape(fn["text"])}</a></p>'
        )
    source = ""
    if page.get("source_url"):
        label = page.get("source_label") or page.get("source_url")
        source = (
            f'<p class="meta">Source: <a href="{html.escape(str(page["source_url"]), quote=True)}">'
            f'{html.escape(str(label))}</a>'
            f' · {html.escape(str(page.get("source_date") or ""))}</p>'
        )
    body = f"""<main id="main">
  <article class="article-width wrap" style="padding:48px 0">
    {crumbs([("Home", url("/")), ("Decisions", url("/decisions/")), (page.get("title") or slug, None)])}
    <p class="eyebrow">{html.escape(str(page.get("stage_label") or ""))}</p>
    <h1>{html.escape(str(page.get("title") or slug))}</h1>
    {"".join(parts)}
    {fn_html}
    {source}
  </article>
</main>"""
    return base(
        title=str(page.get("title") or slug),
        description=str(page.get("meta_description") or page.get("title") or ""),
        canonical_path=f"/decisions/{slug}/",
        body=body,
        extra_head=json_ld_for_decision(page),
    )


def render_decisions_index(pages: list[dict]) -> str:
    if not pages:
        listing = '<div class="empty"><p>No decision pages yet.</p></div>'
    else:
        cards = []
        for p in pages:
            cards.append(
                f"""<a class="card" href="{url('/decisions/' + p['slug'] + '/')}">
  <div><span class="chip">Decision</span></div>
  <h3>{html.escape(str(p.get("title") or p["slug"]))}</h3>
  <p>{html.escape(str(p.get("meta_description") or ""))}</p>
</a>"""
            )
        listing = f'<div class="grid grid-2">{"".join(cards)}</div>'
    body = f"""<main id="main">
  <section class="page-hero">
    <div class="wrap">
      {crumbs([("Home", url("/")), ("Decisions", None)])}
      <h1>Decisions</h1>
      <p class="lead">Founder decisions by stage: the options, what mattered, and what founders chose.</p>
    </div>
  </section>
  <section class="section" style="padding-top:0">
    <div class="wrap">{listing}</div>
  </section>
</main>"""
    return base(
        title="Decisions",
        description="Founder decisions by stage: the options, what mattered, and what founders chose.",
        canonical_path="/decisions/",
        body=body,
    )


def json_ld_for_benchmark(page: dict) -> str:
    nodes: list[dict] = [
        {
            "@context": "https://schema.org",
            "@type": "Dataset",
            "name": page.get("title"),
            "description": page.get("meta_description") or page.get("claim") or page.get("title"),
            "url": abs_url(f"/benchmarks/{page['slug']}/"),
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": f"What is {page.get('metric') or page.get('title')}?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": page.get("how_to_read") or page.get("claim") or "",
                    },
                },
                {
                    "@type": "Question",
                    "name": "Where does this figure come from?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": (
                            f"{(page.get('source') or {}).get('name') or 'Publisher'}: "
                            f"{(page.get('source') or {}).get('url') or ''} "
                            f"({(page.get('source') or {}).get('date') or page.get('last_verified') or ''}). "
                            "Different publishers are shown separately. They are not averaged."
                        ),
                    },
                },
            ],
        },
    ]
    return ld_json_script(nodes)


def render_benchmark_json(page: dict) -> str:
    slug = page["slug"]
    src = page.get("source") if isinstance(page.get("source"), dict) else {}
    value = page.get("value")
    value_s = "Not published" if value is None or value == "" else str(value)
    unit = html.escape(str(page.get("unit") or ""))
    percentile = html.escape(str(page.get("percentile") or ""))
    segment = html.escape(str(page.get("segment") or ""))
    period = html.escape(str(page.get("period") or ""))
    metric = html.escape(str(page.get("metric") or ""))
    claim = html.escape(str(page.get("claim") or page.get("meta_description") or ""))
    how = html.escape(str(page.get("how_to_read") or ""))
    verified = html.escape(str(page.get("last_verified") or src.get("date") or ""))
    src_name = html.escape(str(src.get("name") or "Source"))
    src_url = src.get("url") or ""
    src_date = html.escape(str(src.get("date") or ""))
    if src_url:
        source_html = (
            f'<p>Source: <a href="{html.escape(src_url, quote=True)}">{src_name}</a>'
            f" · {src_date}. Cited as published. If another publisher disagrees, "
            "show both rows. Do not average them.</p>"
        )
    else:
        source_html = (
            "<p>Source not published on this row. Empty cell; do not estimate.</p>"
        )
    fn = page.get("fn_link") or {}
    fn_html = ""
    if fn.get("href") and fn.get("text"):
        fn_html = (
            f'<p class="article-close"><a href="{html.escape(fn["href"], quote=True)}" '
            f'data-fn-click="{html.escape(slug, quote=True)}">'
            f'{html.escape(fn["text"])}</a></p>'
        )
    table = f"""<div class="table-wrap"><table>
<thead><tr><th>Field</th><th>Published figure</th></tr></thead>
<tbody>
<tr><td>Metric</td><td>{metric}</td></tr>
<tr><td>Value</td><td class="num">{html.escape(value_s)} {unit}</td></tr>
<tr><td>Percentile</td><td>{percentile}</td></tr>
<tr><td>Segment</td><td>{segment}</td></tr>
<tr><td>Period</td><td>{period}</td></tr>
<tr><td>Last verified</td><td>{verified}</td></tr>
</tbody>
</table></div>"""
    how_block = f"<h2>How to read</h2><p>{how}</p>" if how else ""
    body = f"""<main id="main">
  <section class="page-hero">
    <div class="article-width">
      {crumbs([("Home", url("/")), ("Benchmarks", url("/benchmarks/")), (page.get("title") or slug, None)])}
      <p class="eyebrow">Benchmarks · {verified}</p>
      <h1>{html.escape(str(page.get("title") or slug))}</h1>
      <p class="lead">{claim}</p>
    </div>
  </section>
  <article class="prose article-width">
    <aside class="takeaways"><p class="takeaways-label">In short</p>
      <ul><li>One publisher, one figure, one date. Empty if unpublished.</li>
      <li>Different samples stay on separate rows. Never average them into a target.</li></ul>
    </aside>
    {table}
    {source_html}
    {how_block}
    {fn_html}
  </article>
</main>"""
    return base(
        title=str(page.get("title") or slug),
        description=str(page.get("meta_description") or page.get("claim") or page.get("title") or ""),
        canonical_path=f"/benchmarks/{slug}/",
        body=body,
        extra_head=json_ld_for_benchmark(page),
        og_type="article",
        active="benchmarks",
    )


def render_benchmarks_index(pages: list[dict]) -> str:
    if not pages:
        listing = '<div class="empty"><p>No benchmark pages yet.</p></div>'
    else:
        cards = []
        for p in pages:
            src = p.get("source") if isinstance(p.get("source"), dict) else {}
            cards.append(
                f"""<a class="card" href="{url('/benchmarks/' + p['slug'] + '/')}">
  <div><span class="chip">Benchmark</span></div>
  <h3>{html.escape(str(p.get("title") or p["slug"]))}</h3>
  <p>{html.escape(str(p.get("meta_description") or p.get("claim") or ""))}</p>
  <p class="meta">{html.escape(str(src.get("name") or ""))} · {html.escape(str(p.get("last_verified") or src.get("date") or ""))}</p>
</a>"""
            )
        listing = f'<div class="grid grid-2">{"".join(cards)}</div>'
    body = f"""<main id="main">
  <section class="page-hero">
    <div class="wrap">
      {crumbs([("Home", url("/")), ("Benchmarks", None)])}
      <h1>Benchmarks</h1>
      <p class="lead">Cited ranges from named publishers. Disagreements stay on separate rows. Nothing is averaged.</p>
    </div>
  </section>
  <section class="section" style="padding-top:0">
    <div class="wrap">{listing}</div>
  </section>
</main>"""
    return base(
        title="Benchmarks",
        description="Cited metric ranges for venture-scale founders. One publisher per figure.",
        canonical_path="/benchmarks/",
        body=body,
        active="benchmarks",
    )


def asset_version(rel: str) -> str:
    p = STATIC / rel
    if not p.exists():
        return ""
    h = hashlib.md5(p.read_bytes()).hexdigest()[:8]
    return f"?v={h}"


_RANGE_RE = re.compile(r"\$?\d[\d.,]*[%kKMB]?\s?(?:–|-|to)\s?\$?\d[\d.,]*(?:%|x|[kKMB])?")


def nw_ranges(escaped: str) -> str:
    """Keep numeric ranges like 0.3–0.8% on one line in already-escaped text."""
    return _RANGE_RE.sub(lambda m: f'<span class="nw">{m.group(0)}</span>', escaped)


def base(
    *,
    title: str,
    description: str,
    canonical_path: str,
    body: str,
    active: str | None = None,
    robots: str | None = None,
    extra_js: str | None = None,
    extra_head: str = "",
    og_type: str = "website",
) -> str:
    full_title = title if title.endswith(SITE_NAME) else f"{title} · {SITE_NAME}"
    if len(full_title) > 70 and not title.endswith(SITE_NAME):
        full_title = title  # long titles: keep the query words visible in search results, drop the brand suffix
    canonical = abs_url(canonical_path)
    robots_tag = (
        f'<meta name="robots" content="{html.escape(robots, quote=True)}">\n'
        if robots
        else ""
    )
    nav = []
    for key, label, href in NAV_ITEMS:
        cls = ' class="is-active"' if active == key else ""
        nav.append(f'<a href="{url(href)}"{cls}>{html.escape(label)}</a>')
    js = (
        f'<script src="{url("/assets/js/" + extra_js)}{asset_version("assets/js/" + extra_js)}" defer></script>'
        if extra_js
        else ""
    )
    css_v = asset_version("assets/css/site.css")
    # Insert extra_head/body via placeholders so JSON braces never collide
    # with f-string/format template syntax (no brace-escaping required).
    html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(description, quote=True)}">
{robots_tag}<link rel="canonical" href="{html.escape(canonical, quote=True)}">
<meta property="og:title" content="{html.escape(full_title, quote=True)}">
<meta property="og:description" content="{html.escape(description, quote=True)}">
<meta property="og:url" content="{html.escape(canonical, quote=True)}">
<meta property="og:type" content="{html.escape(og_type, quote=True)}">
<meta property="og:site_name" content="{html.escape(SITE_NAME, quote=True)}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{url('/assets/favicon.svg')}" type="image/svg+xml">
<link rel="icon" href="{url('/assets/favicon.png')}" type="image/png" sizes="32x32">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{url('/assets/css/site.css')}{css_v}">
@@EXTRA_HEAD@@</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{url('/')}">
      <span class="brand-mark" aria-hidden="true"></span>
      <span class="brand-wordmark">{html.escape(SITE_NAME)}</span>
    </a>
    <nav class="nav-links" aria-label="Sections">
      {''.join(nav)}
    </nav>
  </div>
</header>
@@BODY@@
<footer class="site-footer">
  <div class="wrap">
    <p class="footer-name">{html.escape(SITE_NAME)}</p>
    <p class="footer-pub">An independent library of decision pages for venture-scale founders.</p>
    <p class="footer-links">
      <a href="{url('/library/')}">Library</a>
      <a href="{url('/tools/')}">Tools</a>
      <a href="{url('/about/')}">About</a>
    </p>
  </div>
</footer>
{js}
<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments);}};</script>
<script defer src="/_vercel/insights/script.js"></script>
<script>
document.addEventListener("click", function (e) {{
  var a = e.target && e.target.closest && e.target.closest("a[href]");
  if (!a || typeof window.va !== "function") return;
  var u;
  try {{ u = new URL(a.href, location.href); }} catch (err) {{ return; }}
  if (!/(^|\.)venexecs\.com$/.test(u.hostname)) return;
  window.va("event", {{ name: "ven_click", data: {{
    page: location.pathname,
    target: u.pathname,
    type: u.pathname.indexOf("/playbooks") === 0 ? "playbook" : "homepage"
  }} }});
}});
</script>
</body>
</html>
"""
    return (
        html_out
        .replace("@@EXTRA_HEAD@@", extra_head)
        .replace("@@BODY@@", body)
    )



def crumbs(items: list[tuple[str, str | None]]) -> str:
    parts = []
    for i, (label, href) in enumerate(items):
        if i:
            parts.append('<span aria-hidden="true">/</span>')
        if href:
            parts.append(f'<a href="{html.escape(href, quote=True)}">{html.escape(label)}</a>')
        else:
            parts.append(f"<span>{html.escape(label)}</span>")
    return f'<nav class="crumbs" aria-label="Breadcrumb">{"".join(parts)}</nav>'


def page_cards(pages: list[dict]) -> str:
    cards = []
    for p in pages:
        kicker = SECTIONS.get(p["section"], {}).get("kicker") or p["section"].title()
        cluster = CLUSTERS.get(p.get("cluster") or "", {})
        chip2 = cluster.get("title")
        chips = f'<span class="chip">{html.escape(kicker)}</span>'
        if chip2:
            chips += f' <span class="chip">{html.escape(chip2)}</span>'
        cards.append(
            f"""<a class="card" href="{url(p['path'])}">
  <div>{chips}</div>
  <h3>{html.escape(p['title'])}</h3>
  <p>{html.escape(p['description'])}</p>
  <p class="meta">{html.escape(p['date'])}</p>
</a>"""
        )
    return f'<div class="grid grid-2">{"".join(cards)}</div>'


def related_block(page: dict, by_key: dict[str, dict]) -> str:
    keys = page.get("related") or []
    items = []
    for k in keys:
        other = by_key.get(k)
        if other and not other["draft"]:
            items.append(other)
    if not items:
        return ""
    lis = "".join(
        f'<li><a href="{url(o["path"])}"><span class="list-title">{html.escape(o["title"])}</span>'
        f'<p class="list-desc">{html.escape(o["description"])}</p></a></li>'
        for o in items
    )
    return (
        '<section class="section related-section" aria-label="Related">'
        '<div class="article-width">'
        f'<h2 class="related-heading">Related</h2>'
        f'<ul class="page-list">{lis}</ul>'
        "</div></section>"
    )


def article_close(sentence: str) -> str:
    if not sentence:
        return ""
    escaped = html.escape(sentence)
    import re
    linked = re.sub(
        rf"\b{re.escape(PUBLISHER_NAME)}\b",
        f'<a href="{html.escape(PUBLISHER_URL, quote=True)}" data-fn-click="close">{html.escape(PUBLISHER_NAME)}</a>',
        escaped,
        count=1,
    )
    return f'<p class="article-close">{linked}</p>'


VEN_PLAYBOOK_BASE = "https://www.venexecs.com/playbooks/"
VEN_PLAYBOOK_UTM = "utm_source=founderdecisions&utm_medium=referral&utm_campaign=playbook&utm_content={slug}"
# Owned page key (content path, no slashes at ends) -> (playbook path under /playbooks/, anchor text).
# One quiet "Go deeper" link per page, only on a genuine topic match (venexecs.com/sitemap.xml).
# Pages not listed keep only the homepage UTM link. Frontmatter `ven_playbook: <path>` and
# `ven_playbook_label: <anchor>` override or add an entry for new daily pages.
# Link out only; never copy playbook text onto Founder Decisions.
VEN_PLAYBOOKS: dict[str, tuple[str, str]] = {
    "library/board": ("guides/capital-runway-and-the-board", "VEN guide to capital, runway and the board"),
    "library/board/monthly-investor-update": ("concepts/material-change-update", "VEN playbook note on material-change investor updates"),
    "library/board/missed-plan-reforecast": ("guides/running-against-the-plan", "VEN guide to running against the plan"),
    "library/board/series-a-board-meeting-agenda": ("guides/capital-runway-and-the-board", "VEN guide to capital, runway and the board"),
    "library/equity": ("equity-legal/options-pools-advisor-equity", "VEN playbook on options, pools and advisor equity"),
    "library/equity/409a-after-priced-round": ("concepts/409a-valuation", "VEN playbook note on 409A valuations"),
    "library/equity/founder-vesting-83b": ("equity-legal/founder-stock-vesting-83b", "VEN playbook on founder stock, vesting and 83(b)"),
    "library/equity/executive-grants-by-stage": ("equity-legal/options-pools-advisor-equity", "VEN playbook on options, pools and advisor equity"),
    "library/equity/option-pool-from-hiring-plan": ("equity-legal/options-pools-advisor-equity", "VEN playbook on options, pools and advisor equity"),
    "library/finance": ("guides/capital-runway-and-the-board", "VEN guide to capital, runway and the board"),
    "library/finance/ai-gross-margin-inference-cogs": ("building-the-company/pricing-in-the-ai-era", "VEN playbook on pricing and margins in the AI era"),
    "library/finance/customer-concentration": ("concepts/customer-concentration", "VEN playbook note on customer concentration"),
    "library/finance/burn-multiple-vs-rule-of-40": ("guides/capital-runway-and-the-board", "VEN guide to capital, runway and the board"),
    "library/finance/nrr-vs-grr-board-pack": ("guides/customer-retention-and-expansion", "VEN guide to customer retention and expansion"),
    "library/finance/usage-revenue-as-arr": ("building-the-company/pricing-in-the-ai-era", "VEN playbook on pricing in the AI era"),
    "library/fundraising": ("raising-money/running-the-raise", "VEN playbook on running the raise"),
    "library/fundraising/first-angel-check": ("raising-money/first-angel-check", "VEN playbook on finding your first angel"),
    "library/fundraising/how-seed-vcs-decide": ("raising-money/how-seed-vcs-decide", "VEN playbook on how seed investors evaluate startups"),
    "library/fundraising/safe-vs-priced-round": ("raising-money/safes-notes-priced-rounds", "VEN playbook on SAFEs, notes and priced rounds"),
    "library/fundraising/seed-fundraising-process": ("raising-money/running-the-raise", "VEN playbook on running the raise"),
    "library/fundraising/seed-pitch-deck": ("raising-money/pitch-deck", "VEN playbook on the pitch deck"),
    "library/fundraising/series-a-diligence-checklist": ("raising-money/data-rooms", "VEN playbook on data rooms for due diligence"),
    "library/fundraising/term-sheet-red-flags": ("raising-money/term-sheets-red-flags", "VEN playbook on term sheets and red flags"),
    "library/fundraising/venture-debt": ("raising-money/venture-debt", "VEN playbook on venture debt"),
    "library/fundraising/when-runway-runs-out": ("raising-money/when-runway-runs-out", "VEN playbook on running out of runway"),
    "library/fundraising/when-to-raise-series-a": ("raising-money/running-the-raise", "VEN playbook on round size, outreach and timing"),
    "library/gtm": ("marketing-pr/gtm-as-a-system", "VEN playbook on GTM as a system"),
    "library/gtm/aeo-vs-seo-b2b-saas": ("marketing-pr/ai-era-marketing-stack", "VEN playbook on the AI-era marketing stack"),
    "library/gtm/ai-sdr-vs-human": ("getting-customers/repeatable-sales-motion", "VEN playbook on building a repeatable sales motion"),
    "library/gtm/coding-agents-dont-10x-engineering": ("building-the-company/ai-engineering-10x", "VEN playbook on why AI isn't making engineering 10x faster"),
    "library/gtm/conference-to-customers": ("getting-customers/conferences-to-customers", "VEN playbook on conference lead generation"),
    "library/gtm/customer-development-sales-funnel": ("getting-customers/customer-development-funnel", "VEN playbook on customer development as a sales funnel"),
    "library/gtm/data-moat-ai-startup": ("building-the-company/data-moats-flywheels", "VEN playbook on data moats and AI defensibility"),
    "library/gtm/diy-founder-pr-narrative": ("marketing-pr/diy-pr", "VEN playbook on DIY PR and the founder narrative"),
    "library/gtm/early-customer-retention": ("getting-customers/customer-feedback-and-retention", "VEN playbook on customer feedback and early retention"),
    "library/gtm/first-customer-contract": ("getting-customers/first-customer-contracts", "VEN playbook on first customer contracts"),
    "library/gtm/landing-page-that-converts": ("getting-customers/landing-pages", "VEN playbook on landing pages that convert"),
    "library/gtm/market-ai-product-without-saying-ai": ("marketing-pr/marketing-ai-products", "VEN playbook on marketing an AI product"),
    "library/gtm/pilot-to-paid-contract": ("getting-customers/pilots-that-convert", "VEN playbook on turning a pilot into a paid contract"),
    "library/gtm/price-ai-features-inference-cost": ("building-the-company/pricing-in-the-ai-era", "VEN playbook on pricing in the AI era"),
    "library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas": ("building-the-company/pricing-in-the-ai-era", "VEN playbook on pricing in the AI era"),
    "library/gtm/repeatable-sales-process": ("getting-customers/repeatable-sales-motion", "VEN playbook on building a repeatable sales motion"),
    "library/gtm/sell-to-enterprise": ("getting-customers/selling-to-the-enterprise", "VEN playbook on selling to the enterprise"),
    "library/gtm/strategic-partnership-ip": ("equity-legal/strategic-partnerships-and-ip", "VEN playbook on strategic partnerships and IP"),
    "library/gtm/validate-demand-before-you-build": ("getting-customers/validate-before-you-build", "VEN playbook on validating demand before you build"),
    "library/hiring": ("building-the-company/executive-team", "VEN playbook on building your executive team"),
    "library/hiring/onboard-first-executive": ("building-the-company/executive-team", "VEN playbook on building your executive team"),
    "library/hiring/series-a-leadership-hiring-sequence": ("building-the-company/executive-team", "VEN playbook on building your executive team"),
    "library/hiring/when-to-hire-first-vp-sales": ("getting-customers/repeatable-sales-motion", "VEN playbook on building a repeatable sales motion"),
    "tools/ai-gross-margin-calculator": ("building-the-company/pricing-in-the-ai-era", "VEN playbook on pricing and margins in the AI era"),
    "tools/executive-equity-calculator": ("equity-legal/options-pools-advisor-equity", "VEN playbook on options, pools and advisor equity"),
    "tools/magic-number-cac-payback-calculator": ("concepts/ltv-cac", "VEN playbook note on LTV:CAC"),
    "tools/option-pool-shuffle-calculator": ("equity-legal/options-pools-advisor-equity", "VEN playbook on options, pools and advisor equity"),
    "tools/runway-calculator": ("guides/capital-runway-and-the-board", "VEN guide to capital, runway and the board"),
}


def ven_playbook_line(key: str, page: dict | None = None) -> str:
    page = page or {}
    entry = VEN_PLAYBOOKS.get(key)
    if page.get("ven_playbook"):
        entry = (str(page["ven_playbook"]).strip("/"), str(page.get("ven_playbook_label") or (entry[1] if entry else "VEN playbook")))
    if not entry:
        return ""
    path, label = entry
    slug = key.rstrip("/").split("/")[-1] or "home"
    href = f"{VEN_PLAYBOOK_BASE}{path}?{VEN_PLAYBOOK_UTM.format(slug=slug)}"
    return (
        f'<p class="article-more">Go deeper: '
        f'<a href="{html.escape(href, quote=True)}">{html.escape(label)}</a></p>'
    )


# Default mount/JS for calculator pages that omit calculator_js.
# Per-page override: frontmatter calculator_js (and optional calculator_mount, calculator_note).
CALCULATOR_DEFAULT_JS = "equity-calculator.js"
CALCULATOR_DEFAULT_MOUNT = "equity-calculator"
CALCULATOR_DEFAULT_NOTE = (
    "Series D+ is not in this form. Cited sources on the companion page do not "
    "publish a VP band for that stage."
)


def calculator_mount_and_js(page: dict) -> tuple[str, str | None]:
    """Return (mount HTML, js filename) for a page. Empty mount and None js if not a calculator."""
    if page.get("layout") != "calculator":
        return "", None
    js = (page.get("calculator_js") or CALCULATOR_DEFAULT_JS).strip()
    if not js.endswith(".js"):
        js = js + ".js"
    mount = (page.get("calculator_mount") or "").strip()
    if not mount:
        if page.get("calculator_js"):
            mount = js[:-3]  # option-pool-shuffle-calculator.js -> id
        else:
            mount = CALCULATOR_DEFAULT_MOUNT
    if "calculator_note" in page:
        note = (page.get("calculator_note") or "").strip()
    elif page.get("calculator_js"):
        note = ""
    else:
        note = CALCULATOR_DEFAULT_NOTE
    note_html = (
        f'<p class="small muted" style="margin-top:16px">{html.escape(note)}</p>'
        if note
        else ""
    )
    mount_html = (
        f'<div id="{html.escape(mount, quote=True)}" class="calc-mount"></div>'
        f"{note_html}"
    )
    return mount_html, js


def calculator_prose(body_md: str, mount_html: str) -> str:
    """Render page prose. On calculator pages, put the tool right after the lede and
    In short block (before the first ## section) so it sits on the first scroll
    instead of below Sources. Pages without a ## heading keep the tool at the end."""
    if not mount_html:
        return render_markdown(body_md)
    m = re.search(r"(?m)^## ", body_md)
    if not m:
        return render_markdown(body_md) + "\n" + mount_html
    return (
        render_markdown(body_md[: m.start()])
        + "\n"
        + mount_html
        + "\n"
        + render_markdown(body_md[m.start() :])
    )


# Homepage curation. Picks come from Search Console page impressions (W44 readout,
# 18-24 Oct 2026: executive grants by stage leads, then pilot to paid, venture debt,
# seed deck, validate demand, usage revenue). Refresh at the weekly review.
HOME_START_HERE: list[tuple[str, str]] = [
    ("library/equity/executive-grants-by-stage", "Seed, Series A, and Series B equity bands for VP and C-level offers."),
    ("library/gtm/pilot-to-paid-contract", "Charge for the pilot and write the conversion terms before kickoff."),
    ("library/fundraising/venture-debt", "When a venture loan fits after a round, how much, and which terms to fight."),
    ("library/fundraising/seed-pitch-deck", "What each slide must answer and where investors spend their time."),
    ("library/gtm/validate-demand-before-you-build", "Write the demand bet as a number and ask for money before code."),
    ("library/finance/usage-revenue-as-arr", "Which usage and AI revenue counts as ARR, and how to show it to the board."),
]
HOME_TOPIC_ORDER = ["fundraising", "equity", "hiring", "board", "finance", "gtm", "rooms"]
# Three links per topic tile, most useful first. Missing keys fall back to the newest pages.
HOME_TOPIC_TOP: dict[str, list[str]] = {
    "fundraising": ["library/fundraising/when-to-raise-series-a", "library/fundraising/safe-vs-priced-round", "library/fundraising/seed-fundraising-process"],
    "equity": ["library/equity/executive-grants-by-stage", "library/equity/option-pool-from-hiring-plan", "library/equity/409a-after-priced-round"],
    "hiring": ["library/hiring/when-to-hire-first-vp-sales", "library/hiring/series-a-leadership-hiring-sequence", "library/hiring/onboard-first-executive"],
    "board": ["library/board/monthly-investor-update", "library/board/when-to-add-independent-director", "library/board/series-a-board-meeting-agenda"],
    "finance": ["library/finance/burn-multiple-vs-rule-of-40", "library/finance/nrr-vs-grr-board-pack", "library/finance/ai-gross-margin-inference-cogs"],
    "gtm": ["library/gtm/first-customer-contract", "library/gtm/seat-vs-usage-vs-outcome-pricing-ai-saas", "library/gtm/sell-to-enterprise"],
    "rooms": ["compare/executive-coaching-vs-founder-peer-group", "compare/ypo-vs-hampton-vs-venture-scale-room"],
}
HOME_TOOL_LINES: dict[str, str] = {
    "tools/executive-equity-calculator": "Check a VP grant against cited bands and your pool.",
    "tools/runway-calculator": "Months to cash-out with your hiring plan in it.",
    "tools/option-pool-shuffle-calculator": "Who pays for a pre-money pool top-up.",
    "tools/magic-number-cac-payback-calculator": "Magic number and CAC payback side by side.",
    "tools/ai-gross-margin-calculator": "Gross margin with inference cost counted.",
}
HOME_POPULAR: list[tuple[str, str]] = [
    ("VP equity by stage", "/library/equity/executive-grants-by-stage/"),
    ("When to raise Series A", "/library/fundraising/when-to-raise-series-a/"),
    ("SAFE or priced round", "/library/fundraising/safe-vs-priced-round/"),
    ("Runway calculator", "/tools/runway-calculator/"),
]
HOME_VEN_URL = "https://www.venexecs.com/?utm_source=founderdecisions&utm_medium=referral&utm_campaign=home&utm_content=home"


def _topic_label(p: dict) -> str:
    cl = CLUSTERS.get(p.get("cluster") or "")
    if cl:
        return cl["title"]
    return SECTIONS.get(p["section"], {}).get("kicker") or p["section"].title()


def home_search_index(pages: list[dict]) -> str:
    """Small inline JSON index (title, line, topic, url) for the homepage finder."""
    items = []
    for p in pages:
        if p["section"] not in SECTIONS and p.get("layout") != "hub":
            continue
        items.append({
            "t": p["title"],
            "d": p["description"],
            "k": _topic_label(p) if p.get("layout") != "hub" else "Topic",
            "u": url(p["path"]),
        })
    raw = json.dumps(items, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/json" id="fd-index">{raw}</script>'


def render_home(pages: list[dict]) -> str:
    owned = [p for p in content_pages(pages) if p.get("layout") != "hub"]
    by_key = {page_key(p): p for p in owned}
    latest = sorted(owned, key=lambda p: (p["date"], p["title"]), reverse=True)
    esc = html.escape

    # Start here
    start_cards = []
    for key, line in HOME_START_HERE:
        p = by_key.get(key)
        if not p:
            continue
        start_cards.append(
            f'<a class="card card-compact" href="{url(p["path"])}">'
            f'<span class="card-topic">{esc(_topic_label(p))}</span>'
            f'<h3>{nw_ranges(esc(p["title"]))}</h3><p>{nw_ranges(esc(line))}</p></a>'
        )

    # Topic tiles
    tiles = []
    for cid in HOME_TOPIC_ORDER:
        cl = CLUSTERS[cid]
        in_topic = [p for p in owned if p.get("cluster") == cid]
        n = len(in_topic)
        picks = [by_key[k] for k in HOME_TOPIC_TOP.get(cid, []) if k in by_key]
        for p in sorted(in_topic, key=lambda p: p["date"], reverse=True):
            if len(picks) >= 3:
                break
            if p not in picks:
                picks.append(p)
        hub = url(f"/{cl['section']}/{cid}/")
        lis = "".join(f'<li><a href="{url(p["path"])}">{nw_ranges(esc(p["title"]))}</a></li>' for p in picks[:3])
        tiles.append(
            f'<div class="topic-tile">'
            f'<h3><a href="{hub}">{esc(cl["title"])}</a></h3>'
            f'<p class="topic-desc">{esc(cl["description"])}</p>'
            f'<ul class="topic-links">{lis}</ul>'
            f'<a class="topic-all" href="{hub}">All {n} {"page" if n == 1 else "pages"}<span aria-hidden="true"> →</span></a>'
            f"</div>"
        )

    # Tools
    tools = sorted((p for p in owned if p["section"] == "tools"), key=lambda p: list(HOME_TOOL_LINES).index(page_key(p)) if page_key(p) in HOME_TOOL_LINES else 99)
    tool_cards = "".join(
        f'<a class="tool-card" href="{url(p["path"])}"><span class="tool-title">{esc(p["title"].split(":")[0])}</span>'
        f'<span class="tool-line">{esc(HOME_TOOL_LINES.get(page_key(p), ""))}</span></a>'
        for p in tools
    )

    # Newest
    new_rows = "".join(
        f'<li><a href="{url(p["path"])}"><span class="list-title">{nw_ranges(esc(p["title"]))}</span>'
        f'<span class="new-meta">{esc(_topic_label(p))} · {esc(p["date"])}</span></a></li>'
        for p in latest[:4]
    )
    popular = "".join(f'<a href="{url(h)}">{esc(t)}</a>' for t, h in HOME_POPULAR)

    body = f"""<main id="main">
  <section class="home-hero">
    <div class="wrap">
      <h1>{esc(TAGLINE.rstrip('.')).replace("venture-scale", '<span class="nw">venture-scale</span>')}</h1>
      <p class="lead">Cited ranges, tables, and calculators for the calls between seed and Series B: the raise, the grant, the first VP, the board, and your first customers.</p>
      <form class="home-search" action="{url('/library/')}" method="get" role="search">
        <label class="home-search-label" for="home-q">What decision are you facing?</label>
        <input id="home-q" name="q" type="search" placeholder="Try VP equity, SAFE, or runway" autocomplete="off" aria-controls="home-results">
        <ul id="home-results" class="home-results" hidden></ul>
      </form>
      <p class="home-popular"><span>Popular</span>{popular}</p>
      <p class="home-trust">Every number links to its source. When sources disagree, the page shows both.</p>
    </div>
  </section>
  <section class="section home-block">
    <div class="wrap">
      <div class="home-head"><h2 class="section-title">Start here</h2><p class="home-sub">The questions founders search for most</p></div>
      <div class="grid grid-3">{''.join(start_cards)}</div>
    </div>
  </section>
  <section class="section section-alt home-block">
    <div class="wrap">
      <div class="home-head"><h2 class="section-title">Browse by topic</h2><a class="home-more" href="{url('/library/')}">Full library: {len([p for p in owned if p['section'] == 'library'])} pages<span aria-hidden="true"> →</span></a></div>
      <div class="topic-grid">{''.join(tiles)}</div>
    </div>
  </section>
  <section class="section home-block">
    <div class="wrap">
      <div class="home-head"><h2 class="section-title">Calculators</h2><a class="home-more" href="{url('/tools/')}">All tools<span aria-hidden="true"> →</span></a></div>
      <div class="tool-row">{tool_cards}</div>
    </div>
  </section>
  <section class="section section-alt home-block">
    <div class="wrap">
      <div class="home-head"><h2 class="section-title">New this week</h2><p class="home-sub">One new decision page every day</p></div>
      <ul class="page-list new-list">{new_rows}</ul>
    </div>
  </section>
  <section class="home-ven">
    <div class="wrap">
      <p>Working through one of these calls right now? <a href="{esc(HOME_VEN_URL, quote=True)}" data-fn-click="home">VEN</a> runs small sessions where founders who have made it pressure-test yours.</p>
    </div>
  </section>
  {home_search_index(pages)}
</main>"""
    return base(
        title=TAGLINE.rstrip("."),
        description="Cited ranges, tables, and calculators for venture-scale founders: fundraising, equity, executive hiring, the board, finance, and go-to-market.",
        canonical_path="/",
        body=body,
        active=None,
        extra_js="home-search.js",
        extra_head=home_json_ld(),
    )


def render_section(key: str, pages: list[dict]) -> str:
    sec = SECTIONS[key]
    subset = [p for p in pages if p["section"] == key]
    clusters_here = [
        (cid, cl) for cid, cl in CLUSTERS.items() if cl["section"] == key
    ]
    cluster_html = ""
    if clusters_here:
        cards = []
        for cid, cl in clusters_here:
            n = sum(1 for p in subset if p.get("cluster") == cid)
            cards.append(
                f"""<a class="card" href="{url('/' + key + '/' + cid + '/')}">
  <h3>{html.escape(cl['title'])}</h3>
  <p>{html.escape(cl['description'])}</p>
  <p class="meta">{n} {'page' if n == 1 else 'pages'}</p>
</a>"""
            )
        cluster_html = (
            f'<h2 class="section-title">Topics</h2>'
            f'<div class="grid grid-2">{"".join(cards)}</div>'
        )
    listing = (
        page_cards(subset)
        if subset
        else '<div class="empty"><p>No pages in this section yet.</p></div>'
    )
    body = f"""<main id="main">
  <section class="page-hero">
    <div class="wrap">
      {crumbs([("Home", url("/")), (sec["title"], None)])}
      <h1>{html.escape(sec["title"])}</h1>
      <p class="lead">{html.escape(sec["description"])}</p>
    </div>
  </section>
  <section class="section" style="padding-top:0">
    <div class="wrap">
      {cluster_html}
      <h2 class="section-title">Pages</h2>
      {listing}
    </div>
  </section>
</main>"""
    return base(
        title=sec["title"],
        description=sec["description"],
        canonical_path=f"/{key}/",
        body=body,
        active=key,
        extra_head=owned_json_ld(
            kind="CollectionPage",
            title=sec["title"],
            description=sec["description"],
            canonical_path=f"/{key}/",
            trail=[("Home", url("/")), (sec["title"], None)],
            modified=newest_modified(subset),
        ),
    )


def load_hub(cid: str) -> dict | None:
    """Optional editorial hub: content/{section}/{cid}/_hub.md"""
    cl = CLUSTERS[cid]
    hub_path = CONTENT / cl["section"] / cid / "_hub.md"
    if not hub_path.exists():
        return None
    fm, body = parse_frontmatter(hub_path.read_text(encoding="utf-8"))
    fm["_body"] = body
    fm["_src"] = hub_path
    return fm


def render_cluster(cid: str, pages: list[dict]) -> str:
    cl = CLUSTERS[cid]
    sec = SECTIONS[cl["section"]]
    subset = [p for p in pages if p.get("cluster") == cid and p.get("layout") != "hub"]
    hub = load_hub(cid)
    title = (hub.get("title") if hub else None) or cl["title"]
    description = (hub.get("description") if hub else None) or cl["description"]
    listing = (
        page_cards(subset)
        if subset
        else '<div class="empty"><p>No pages in this topic yet.</p></div>'
    )
    path = f"/{cl['section']}/{cid}/"
    trail = [
        ("Home", url("/")),
        (sec["title"], url("/" + cl["section"] + "/")),
        (title, None),
    ]

    if hub:
        date = hub.get("date") or ""
        eyebrow = (
            f'<p class="eyebrow">{html.escape(sec["kicker"])} · {html.escape(date)}</p>'
            if date
            else f'<p class="eyebrow">{html.escape(sec["kicker"])}</p>'
        )
        # Pages already listed in the hub's own pick lists are not repeated as cards.
        linked = set(re.findall(r"\]\((/[^)#]+)\)", hub["_body"]))
        rest = [p for p in subset if p["path"] not in linked]
        more_section = ""
        if rest or not subset:
            rows = "".join(
                f'<li><a href="{url(p["path"])}"><span class="list-title">{html.escape(p["title"])}</span>'
                f'<span class="list-desc">{html.escape(p["description"])}</span></a></li>'
                for p in sorted(rest, key=lambda p: p["date"], reverse=True)
            )
            inner = f'<ul class="page-list">{rows}</ul>' if rest else listing
            label = "More in this topic" if linked & {p["path"] for p in subset} else "In this topic"
            more_section = f"""<section class="section">
    <div class="wrap">
      <h2 class="section-title">{label}</h2>
      {inner}
    </div>
  </section>"""
        editorial = (
            f'<article class="prose article-width">'
            f'{render_markdown(hub["_body"])}'
            f'{article_close(hub.get("close") or "")}'
            f'{ven_playbook_line(cl["section"] + "/" + cid, hub)}'
            f"</article>"
        )
        body = f"""<main id="main">
  <section class="page-hero">
    <div class="article-width">
      {crumbs(trail)}
      {eyebrow}
      <h1>{html.escape(title)}</h1>
      <p class="lead">{html.escape(description)}</p>
    </div>
  </section>
  {editorial}
  {more_section}
</main>"""
    else:
        body = f"""<main id="main">
  <section class="page-hero">
    <div class="wrap">
      {crumbs(trail)}
      <h1>{html.escape(title)}</h1>
      <p class="lead">{html.escape(description)}</p>
    </div>
  </section>
  <section class="section" style="padding-top:0">
    <div class="wrap">{listing}</div>
  </section>
</main>"""
    return base(
        title=title,
        description=description,
        canonical_path=path,
        body=body,
        active=cl["section"],
        extra_head=owned_json_ld(
            kind="CollectionPage",
            title=title,
            description=description,
            canonical_path=path,
            trail=trail,
            published=(hub.get("date") or "") if hub else "",
            modified=newest_modified(subset, page_modified(hub) if hub and hub.get("date") else ""),
        ),
    )


def render_article(page: dict, by_key: dict[str, dict]) -> str:
    section = page["section"]
    if section == "about":
        trail = [("Home", url("/")), ("About", None)]
        kicker = None
        active = "about"
    else:
        sec = SECTIONS[section]
        cluster = CLUSTERS.get(page.get("cluster") or "")
        trail = [("Home", url("/")), (sec["title"], url("/" + section + "/"))]
        if cluster:
            trail.append(
                (
                    cluster["title"],
                    url(f"/{cluster['section']}/{page['cluster']}/"),
                )
            )
        trail.append((page["title"], None))
        kicker = cluster["title"] if cluster else sec["kicker"]
        active = section
    extra, extra_js = calculator_mount_and_js(page)
    prose_html = calculator_prose(page["_body"], extra)
    sentence = page.get("close") or page.get("cta_sentence") or ""
    close_html = article_close(sentence) + ven_playbook_line(page_key(page), page)
    related = related_block(page, by_key)
    eyebrow = ""
    if kicker:
        eyebrow = f'<p class="eyebrow">{html.escape(kicker)} · {html.escape(page["date"])}</p>'
    body = f"""<main id="main">
  <section class="page-hero">
    <div class="article-width">
      {crumbs(trail)}
      {eyebrow}
      <h1>{html.escape(page['title'])}</h1>
      <p class="lead">{html.escape(page['description'])}</p>
    </div>
  </section>
  <article class="prose article-width">
    {prose_html}
    {close_html}
  </article>
  {related}
</main>"""
    return base(
        title=page["title"],
        description=page["description"],
        canonical_path=page["path"],
        body=body,
        active=active,
        extra_js=extra_js,
        og_type="article",
        extra_head=owned_json_ld(
            kind="Article" if section != "about" else "AboutPage",
            title=page["title"],
            description=page["description"],
            canonical_path=page["path"],
            trail=trail,
            published=str(page.get("date") or ""),
            modified=page_modified(page),
            section_name=(kicker or ""),
        ),
    )


def render_404() -> str:
    body = f"""<main id="main">
  <section class="page-hero">
    <div class="wrap">
      <h1>This page is not here</h1>
      <p class="lead">The URL does not match a page in Founder Decisions.</p>
      <p><a href="{url('/')}">Back to the index</a></p>
    </div>
  </section>
</main>"""
    return base(
        title="This page is not here",
        description="This URL is not a Founder Decisions page.",
        canonical_path="/404.html",
        body=body,
        robots="noindex",
    )


_VEN_FULL = "VEN (Venture Executive Network)"


def expand_first_ven(page_html: str) -> str:
    """First visible mention of VEN in <body> reads "VEN (Venture Executive Network)"; later ones stay "VEN"."""
    if not page_html.lstrip().startswith("<!") or "<body" not in page_html:
        return page_html
    head, sep, body = page_html.partition("<body")
    parts = re.split(r"(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)", body, flags=re.S)
    for i, part in enumerate(parts):
        if not part or part.startswith("<"):
            continue
        m = re.search(r"\bVEN\b", part)
        if not m:
            continue
        if part[m.end():].startswith(" (Venture Executive Network)"):
            return page_html
        parts[i] = part[: m.start()] + _VEN_FULL + part[m.end():]
        return head + sep + "".join(parts)
    return page_html


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".html":
        text = expand_first_ven(text)
    path.write_text(text, encoding="utf-8")


def copy_static() -> None:
    dest = DIST / "assets"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(STATIC / "assets", dest)
    media_src = ROOT / "media"
    if media_src.exists():
        media_dest = DIST / "media"
        if media_dest.exists():
            shutil.rmtree(media_dest)
        shutil.copytree(media_src, media_dest)


def write_robots() -> None:
    write(
        DIST / "robots.txt",
        f"User-agent: *\nAllow: /\nSitemap: {abs_url('/sitemap.xml')}\n",
    )


def write_sitemap(
    pages: list[dict],
    decision_pages: list[dict] | None = None,
    benchmark_pages: list[dict] | None = None,
) -> None:
    content = [p for p in pages if p["path"] != "/about/" and p.get("layout") != "hub"]
    dec_dates = [str(d.get("source_date")) for d in decision_pages or [] if d.get("source_date")]
    bench_dates = []
    for b in benchmark_pages or []:
        src = b.get("source") if isinstance(b.get("source"), dict) else {}
        v = b.get("last_verified") or src.get("date")
        if v:
            bench_dates.append(str(v))
    site_newest = max([newest_modified(content)] + dec_dates + bench_dates)
    urls = [("/", site_newest, "1.0")]
    for key in SECTIONS:
        urls.append((f"/{key}/", newest_modified([p for p in content if p["section"] == key], ""), "0.8"))
    about = next((p for p in pages if p["path"] == "/about/"), None)
    urls.append(("/about/", page_modified(about) if about and about.get("date") else site_newest, "0.6"))
    urls.append(("/decisions/", max(dec_dates) if dec_dates else site_newest, "0.8"))
    urls.append(("/benchmarks/", max(bench_dates) if bench_dates else site_newest, "0.8"))
    for cid, cl in CLUSTERS.items():
        hub = load_hub(cid)
        hub_date = page_modified(hub) if hub and hub.get("date") else ""
        urls.append(
            (
                f"/{cl['section']}/{cid}/",
                newest_modified([p for p in content if p.get("cluster") == cid], hub_date),
                "0.7",
            )
        )
    for p in content:
        urls.append((p["path"], page_modified(p), "0.9"))
    for d in decision_pages or []:
        urls.append(
            (
                f"/decisions/{d['slug']}/",
                str(d.get("source_date") or date.today().isoformat()),
                "0.9",
            )
        )
    for b in benchmark_pages or []:
        src = b.get("source") if isinstance(b.get("source"), dict) else {}
        urls.append(
            (
                f"/benchmarks/{b['slug']}/",
                str(b.get("last_verified") or src.get("date") or date.today().isoformat()),
                "0.9",
            )
        )
    items = []
    for path, lastmod, prio in urls:
        items.append(
            "  <url>\n"
            f"    <loc>{html.escape(abs_url(path))}</loc>\n"
            f"    <lastmod>{html.escape(lastmod)}</lastmod>\n"
            f"    <priority>{prio}</priority>\n"
            "  </url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(items)
        + "\n</urlset>\n"
    )
    write(DIST / "sitemap.xml", xml)


def page_key(p: dict) -> str:
    path = p["path"].strip("/")
    return path


_LD_JSON_RE = re.compile(
    r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',
    re.I | re.S,
)


def assert_json_ld_parses(dist: Path) -> None:
    """Fail the build if any emitted application/ld+json block is not valid JSON."""
    failures: list[str] = []
    for html_path in sorted(dist.rglob("*.html")):
        html_text = html_path.read_text(encoding="utf-8")
        for i, m in enumerate(_LD_JSON_RE.finditer(html_text), 1):
            raw = m.group(1).strip()
            try:
                json.loads(raw)
            except json.JSONDecodeError as e:
                rel = html_path.relative_to(dist)
                failures.append(f"{rel} script#{i}: {e}")
    if failures:
        raise SystemExit(
            "Invalid application/ld+json (must parse via json.loads):\n  "
            + "\n  ".join(failures)
        )



def build() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    copy_static()

    all_pages = load_pages()
    drafts = [p for p in all_pages if p["draft"]]
    pages = published(all_pages)
    by_key = {page_key(p): p for p in all_pages}

    write(DIST / "index.html", render_home(pages))
    for key in SECTIONS:
        write(DIST / key / "index.html", render_section(key, pages))
    for cid in CLUSTERS:
        cl = CLUSTERS[cid]
        write(DIST / cl["section"] / cid / "index.html", render_cluster(cid, pages))
    for p in pages:
        if p.get("layout") == "hub":
            continue
        rel = p["path"].strip("/") + "/index.html"
        write(DIST / rel, render_article(p, by_key))
    write(DIST / "404.html", render_404())

    decision_pages = fetch_decision_json()
    write(DIST / "decisions" / "index.html", render_decisions_index(decision_pages))
    for d in decision_pages:
        write(
            DIST / "decisions" / d["slug"] / "index.html",
            render_decision_json(d),
        )

    benchmark_pages = fetch_benchmark_json()
    write(DIST / "benchmarks" / "index.html", render_benchmarks_index(benchmark_pages))
    for b in benchmark_pages:
        write(
            DIST / "benchmarks" / b["slug"] / "index.html",
            render_benchmark_json(b),
        )

    write_robots()
    write_sitemap(pages, decision_pages, benchmark_pages)
    write(DIST / "CNAME", "founderdecisions.com\n")

    assert_json_ld_parses(DIST)

    print(f"Built {len(pages)} published page(s), skipped {len(drafts)} draft(s).")
    print(f"Fetched {len(decision_pages)} fn-content decision page(s).")
    print(f"Fetched {len(benchmark_pages)} fn-content benchmark page(s).")
    print(f"Output: {DIST}")
    for p in pages:
        print(f"  {p['path']}")
    for d in drafts:
        print(f"  (draft, not built) {d['_src'].relative_to(ROOT)}")


if __name__ == "__main__":
    build()
