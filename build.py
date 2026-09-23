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
PUBLISHER_NAME = "FounderNexus"
PUBLISHER_URL = "https://www.foundernexus.com?utm_source=founderdecisions&utm_medium=referral&utm_campaign=library"
DISCLAIMER_LEGAL = "Not legal, tax, or compensation advice."

SECTIONS = {
    "library": {
        "title": "Library",
        "nav": "Library",
        "kicker": "Library",
        "description": "Decision pages for one challenge at a time.",
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
        "description": "Side-by-side pages when a comparison is worth the time. Nothing ships here without a sourced reason to exist.",
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
        "description": "Option pool size, executive grants as pool draws, and pre-money dilution through the next round.",
    },
    "hiring": {
        "section": "library",
        "title": "Hiring executives",
        "description": "When the first VP is actually a VP, and when it is still a founder-led motion.",
    },
    "finance": {
        "section": "library",
        "title": "Finance, metrics & runway",
        "description": "Runway with a hiring plan, burn multiple, Rule of 40, and the efficiency metrics boards ask for.",
    },
    "board": {
        "section": "library",
        "title": "Board & governance",
        "description": "Series A board cadence, decision-first agendas, packs, and closed-session norms.",
    },
    "gtm": {
        "section": "library",
        "title": "Go-to-market",
        "description": "Where AI sits in the sales motion, and the human SDR numbers to score it against.",
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
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
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
            inner_html = render_markdown("\n".join(buf))
            if kind in ("takeaways", "takeaway"):
                label = label.strip() or "In short"
                out.append(
                    f'<aside class="takeaways"><p class="takeaways-label">{html.escape(label)}</p>{inner_html}</aside>'
                )
            elif kind in ("highlight", "note"):
                out.append(f'<aside class="highlight">{inner_html}</aside>')
            else:
                out.append(inner_html)
            continue
        if line.startswith("#"):
            m = re.match(r"^(#{1,4})\s+(.*)$", line)
            if m:
                level = len(m.group(1))
                text = m.group(2).strip()
                hid = slugify(text)
                out.append(
                    f'<h{level} id="{html.escape(hid, quote=True)}">{inline_md(text)}</h{level}>'
                )
                i += 1
                continue
        if line.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip("> ").rstrip())
                i += 1
            out.append(f"<blockquote><p>{inline_md(' '.join(buf))}</p></blockquote>")
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
    return "\n".join(out)


def _looks_numeric(text: str) -> bool:
    """Mark short figure cells for nowrap. Skip prose that merely contains a year or digit."""
    plain = re.sub(r"[¹²³⁴⁵⁶⁷⁸⁹⁰*†‡]", "", text).replace("{br}", " ").strip()
    if len(plain) > 40:
        return False
    if not re.search(r"[\d$%×]|—", plain):
        return False
    letters = len(re.findall(r"[A-Za-z]", plain))
    return letters <= 8


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

    th = "".join(f"<th>{cell_inner(c)}</th>" for c in head)
    trs = []
    for row in body:
        tds = []
        for idx, c in enumerate(row):
            cls = ' class="num"' if _looks_numeric(c) else ""
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
PUBLIC_SESSION_SOURCE_LABEL = "FounderNexus session"


def _is_internal_source_url(url: str) -> bool:
    u = (url or "").lower()
    return any(h in u for h in INTERNAL_SOURCE_HOSTS)


def _scrub_internal_source_text(text: str) -> str:
    """Remove Startup Bible URLs/names from public copy. Keep FounderNexus session framing."""
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
    out = re.sub(r"(?i)The Startup Bible", "a FounderNexus session", out)
    out = re.sub(r"(?i)Startup Bible", "FounderNexus session", out)
    return out.strip()


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
    return page


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
    return fetch_json_dir(FN_BENCHMARKS_DIR)



def ld_json_script(payload: object) -> str:
    """Serialize JSON-LD for <head>. Safe for any braces; never double-escape."""
    blob = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
    return f'<script type="application/ld+json">{blob}</script>\n'

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
            items = b.get("items") or []
            lis = "".join(f"<li>{html.escape(str(it))}</li>" for it in items)
            parts.append(f"<h2>Options</h2><ul>{lis}</ul>")
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
                f'<p class="claim">{html.escape(str(b.get("text") or ""))}</p>'
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
        listing = '<div class="empty"><p>No decision pages from fn-content yet.</p></div>'
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
      <p class="lead">Pages rendered from foundernexus/fn-content. One JSON file, one route.</p>
    </div>
  </section>
  <section class="section" style="padding-top:0">
    <div class="wrap">{listing}</div>
  </section>
</main>"""
    return base(
        title="Decisions",
        description="Decision pages rendered from fn-content.",
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
        listing = '<div class="empty"><p>No benchmark pages from fn-content yet.</p></div>'
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
<script defer src="https://va.vercel-scripts.com/v1/script.js"></script>
<script>
document.addEventListener("click", function (e) {{
  var a = e.target && e.target.closest && e.target.closest("a[data-fn-click]");
  if (!a || typeof window.va !== "function") return;
  window.va("event", {{ name: "fn_click", data: {{ slug: a.getAttribute("data-fn-click") }} }});
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
    linked = escaped.replace(
        PUBLISHER_NAME,
        f'<a href="{html.escape(PUBLISHER_URL, quote=True)}" data-fn-click="close">{html.escape(PUBLISHER_NAME)}</a>',
        1,
    )
    return f'<p class="article-close">{linked}</p>'


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


def render_home(pages: list[dict]) -> str:
    latest = sorted(content_pages(pages), key=lambda p: p["date"], reverse=True)
    cluster_cards = []
    for cid, cl in CLUSTERS.items():
        n = sum(1 for p in pages if p.get("cluster") == cid)
        cluster_cards.append(
            f"""<a class="card" href="{url('/' + cl['section'] + '/' + cid + '/')}">
  <div><span class="chip">{html.escape(SECTIONS[cl['section']]['kicker'])}</span></div>
  <h3>{html.escape(cl['title'])}</h3>
  <p>{html.escape(cl['description'])}</p>
  <p class="meta">{n} {'page' if n == 1 else 'pages'}</p>
</a>"""
        )
    body = f"""<main id="main">
  <section class="page-hero home-hero">
    <div class="wrap">
      <p class="eyebrow">{html.escape(SITE_NAME)}</p>
      <h1>{html.escape(TAGLINE.rstrip('.'))}</h1>
      <p class="lead">Public ranges, tables, and calculators for the grants and hires you write. One challenge at a time.</p>
    </div>
  </section>
  <section class="how-strip" aria-label="How these pages work">
    <div class="wrap">
      <p class="how-strip-label">How these pages work</p>
      <ul class="how-strip-list">
        <li><strong>One challenge</strong> Each page covers a single decision, not a curriculum.</li>
        <li><strong>Cited ranges</strong> Tables and bands stay attributed to the source that published them.</li>
        <li><strong>Disagreements shown</strong> When sources conflict, the page shows the split instead of averaging it away.</li>
      </ul>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <h2 class="section-title">Latest pages</h2>
      {page_cards(latest)}
    </div>
  </section>
  <section class="section section-alt">
    <div class="wrap">
      <h2 class="section-title">Topics</h2>
      <div class="grid grid-2">{''.join(cluster_cards)}</div>
    </div>
  </section>
</main>"""
    return base(
        title=TAGLINE.rstrip("."),
        description="Public ranges, tables, and calculators for venture-scale founders. Clustered by challenge.",
        canonical_path="/",
        body=body,
        active=None,
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
        else '<div class="empty"><p>No pages in this cluster yet.</p></div>'
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
        editorial = (
            f'<article class="prose article-width">'
            f'{render_markdown(hub["_body"])}'
            f'{article_close(hub.get("close") or "")}'
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
  <section class="section">
    <div class="wrap">
      <h2 class="section-title">In this topic</h2>
      {listing}
    </div>
  </section>
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
    sentence = page.get("close") or page.get("cta_sentence") or ""
    close_html = article_close(sentence)
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
    {render_markdown(page['_body'])}
    {extra}
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


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
    urls = [("/", date.today().isoformat(), "1.0")]
    for key in SECTIONS:
        urls.append((f"/{key}/", date.today().isoformat(), "0.8"))
    urls.append(("/about/", date.today().isoformat(), "0.6"))
    urls.append(("/decisions/", date.today().isoformat(), "0.8"))
    urls.append(("/benchmarks/", date.today().isoformat(), "0.8"))
    for cid, cl in CLUSTERS.items():
        urls.append((f"/{cl['section']}/{cid}/", date.today().isoformat(), "0.7"))
    for p in pages:
        if p["path"] == "/about/" or p.get("layout") == "hub":
            continue
        urls.append((p["path"], p["date"], "0.9"))
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
