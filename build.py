#!/usr/bin/env python3
"""Build Founder Decisions from Markdown into dist/.

Stdlib only. Drop a page in content/, run: python3 build.py

Canonical host is a placeholder. Public publish needs Matt McKinney's approval.
"""

from __future__ import annotations

import hashlib
import html
import re
import shutil
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
    ("tools", "Tools", "/tools/"),
    ("about", "About", "/about/"),
]

CLUSTERS = {
    "equity": {
        "section": "library",
        "title": "Equity",
        "description": "How you grant, vest, and explain ownership at the executive layer.",
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
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>',
        text,
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
        ):
            buf.append(lines[i])
            i += 1
        out.append(f"<p>{inline_md(' '.join(buf))}</p>")
    return "\n".join(out)


def _looks_numeric(text: str) -> bool:
    stripped = re.sub(r"[¹²³⁴⁵⁶⁷⁸⁹⁰*†‡\s]", "", text)
    stripped = stripped.replace("{br}", "")
    return bool(re.search(r"[\d$%]|—", stripped))


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
        fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        required = ["title", "description", "slug", "section", "date"]
        missing = [k for k in required if k not in fm]
        if missing:
            raise SystemExit(f"{path}: missing {missing}")
        fm["_src"] = path
        fm["_body"] = body
        fm["draft"] = bool(fm.get("draft", False))
        fm["layout"] = fm.get("layout", "article")
        fm["path"] = page_path(fm)
        fm["related"] = fm.get("related") or []
        pages.append(fm)
    return pages


def published(pages: list[dict]) -> list[dict]:
    return [p for p in pages if not p["draft"]]


def content_pages(pages: list[dict]) -> list[dict]:
    return [p for p in pages if p["section"] in SECTIONS]


# ---------------------------------------------------------------------------
# HTML chrome
# ---------------------------------------------------------------------------

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
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
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
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{url('/')}">
      <span class="brand-wordmark">{html.escape(SITE_NAME)}</span>
    </a>
    <nav class="nav-links" aria-label="Sections">
      {''.join(nav)}
    </nav>
  </div>
</header>
{body}
<footer class="site-footer">
  <div class="wrap">
    <p class="footer-name">{html.escape(SITE_NAME)}</p>
    <p class="footer-pub">Published by {html.escape(PUBLISHER_NAME)}</p>
    <p class="footer-links">
      <a href="{url('/library/')}">Library</a>
      <a href="{url('/tools/')}">Tools</a>
      <a href="{url('/about/')}">About</a>
    </p>
    <p class="footer-tiny"><a href="{html.escape(PUBLISHER_URL, quote=True)}">{html.escape(PUBLISHER_NAME)}</a></p>
  </div>
</footer>
{js}
</body>
</html>
"""


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
        '<section class="section related-section">'
        '<div class="wrap article-width">'
        f"<h2>Related</h2><ul class=\"page-list\">{lis}</ul>"
        "</div></section>"
    )


def article_close(sentence: str) -> str:
    if not sentence:
        return ""
    escaped = html.escape(sentence)
    linked = escaped.replace(
        PUBLISHER_NAME,
        f'<a href="{html.escape(PUBLISHER_URL, quote=True)}">{html.escape(PUBLISHER_NAME)}</a>',
        1,
    )
    return f'<p class="article-close">{linked}</p>'


CALCULATOR_FORM = """
<div id="equity-calculator" class="calc-mount"></div>
<p class="small muted" style="margin-top:16px">Series D+ is not in this form. Cited sources on the companion page do not publish a VP band for that stage.</p>
"""


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
  <section class="page-hero">
    <div class="wrap">
      <h1>{html.escape(TAGLINE.rstrip('.'))}</h1>
      <p class="lead">Public ranges, tables, and calculators for the grants and hires you write. One challenge at a time.</p>
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


def render_cluster(cid: str, pages: list[dict]) -> str:
    cl = CLUSTERS[cid]
    sec = SECTIONS[cl["section"]]
    subset = [p for p in pages if p.get("cluster") == cid]
    listing = (
        page_cards(subset)
        if subset
        else '<div class="empty"><p>No pages in this cluster yet.</p></div>'
    )
    path = f"/{cl['section']}/{cid}/"
    body = f"""<main id="main">
  <section class="page-hero">
    <div class="wrap">
      {crumbs([("Home", url("/")), (sec["title"], url("/" + cl["section"] + "/")), (cl["title"], None)])}
      <h1>{html.escape(cl["title"])}</h1>
      <p class="lead">{html.escape(cl["description"])}</p>
    </div>
  </section>
  <section class="section" style="padding-top:0">
    <div class="wrap">{listing}</div>
  </section>
</main>"""
    return base(
        title=cl["title"],
        description=cl["description"],
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
    extra = CALCULATOR_FORM if page["layout"] == "calculator" else ""
    sentence = page.get("close") or page.get("cta_sentence") or ""
    close_html = article_close(sentence)
    related = related_block(page, by_key)
    eyebrow = ""
    if kicker:
        eyebrow = f'<p class="eyebrow">{html.escape(kicker)} · {html.escape(page["date"])}</p>'
    body = f"""<main id="main">
  <section class="page-hero">
    <div class="wrap">
      {crumbs(trail)}
      {eyebrow}
      <h1>{html.escape(page['title'])}</h1>
      <p class="lead">{html.escape(page['description'])}</p>
    </div>
  </section>
  <article class="wrap prose article-width">
    {render_markdown(page['_body'])}
    {extra}
    {close_html}
  </article>
  {related}
</main>"""
    extra_js = "equity-calculator.js" if page["layout"] == "calculator" else None
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


def write_robots() -> None:
    write(
        DIST / "robots.txt",
        f"User-agent: *\nAllow: /\nSitemap: {abs_url('/sitemap.xml')}\n",
    )


def write_sitemap(pages: list[dict]) -> None:
    urls = [("/", date.today().isoformat(), "1.0")]
    for key in SECTIONS:
        urls.append((f"/{key}/", date.today().isoformat(), "0.8"))
    urls.append(("/about/", date.today().isoformat(), "0.6"))
    for cid, cl in CLUSTERS.items():
        urls.append((f"/{cl['section']}/{cid}/", date.today().isoformat(), "0.7"))
    for p in pages:
        if p["path"] == "/about/":
            continue
        urls.append((p["path"], p["date"], "0.9"))
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
        rel = p["path"].strip("/") + "/index.html"
        write(DIST / rel, render_article(p, by_key))
    write(DIST / "404.html", render_404())
    write_robots()
    write_sitemap(pages)
    write(DIST / "CNAME", "founderdecisions.com\n")

    print(f"Built {len(pages)} published page(s), skipped {len(drafts)} draft(s).")
    print(f"Output: {DIST}")
    for p in pages:
        print(f"  {p['path']}")
    for d in drafts:
        print(f"  (draft, not built) {d['_src'].relative_to(ROOT)}")


if __name__ == "__main__":
    build()
