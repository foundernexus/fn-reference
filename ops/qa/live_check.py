#!/usr/bin/env python3
"""Live QA for https://founderdecisions.com (read-only; never writes to the site).

Daily (post-deploy, ~1 min):
    python3 ops/qa/live_check.py
Friday full review (~5 min, adds external links, every page at 390/1280, search box, 404):
    python3 ops/qa/live_check.py --full

Checks
  links      every internal <a href> on every sitemap page resolves 200 (redirects reported)
  sitemap    URLs unique, lastmod ISO, not in the future, not all the same date
  freshness  homepage "New this week" lists the newest owned page, no duplicates,
             newest page is <= --max-age days old (default 1)
  hubs       every owned /library/<topic>/<slug>/ page appears exactly once on its topic page
             and is linked from /library/; no sitemap page is orphaned (no inbound link)
  topics     homepage tile "All N pages" equals the topic's real page count
  language   internal planning words (spoke, hub, cluster, target query, fn-content,
             Startup Bible, GitHub issues, foundernexus.com, "Published by") in visible
             text, meta tags, and JSON-LD; owned pages FAIL, generated /decisions/ and
             /benchmarks/ WARN (fix upstream)
  seo        one <h1>, <title> and meta description present, canonical == URL, no noindex,
             JSON-LD parses with @context/@type, VEN links carry utm_source=founderdecisions
  layout     (playwright) no horizontal overflow at 390 and 1280, no console/page errors
             daily: homepage, newest page, topic pages; --full: every sitemap page
  search     (--full) homepage finder: results, typo, empty, keyboard Enter, mobile
  external   (--full) external links (reported as WARN; many sites block bots)
  404        (--full) a missing URL returns 404 with the site template

Exit code 1 if any FAIL. Use --json PATH to save the report.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import html as htmlmod
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ops" / "stop-slop"))
try:
    from check import INTERNAL_LANGUAGE, BRAND_RULES  # one source of truth with the gate
except Exception:  # pragma: no cover
    INTERNAL_LANGUAGE, BRAND_RULES = [], []

BASE = "https://founderdecisions.com"
UA = "Mozilla/5.0 (FounderDecisions-QA; +https://founderdecisions.com)"
EXTRA_LEAKS = [
    re.compile(r"\bPublished by\b"),
    re.compile(r"\bfoundernexus\.com\b", re.I),
]
OWNED_PREFIXES = ("/library/", "/tools/", "/compare/", "/about/")
GENERATED_PREFIXES = ("/decisions/", "/benchmarks/")

results: list[dict] = []


def rec(level: str, check: str, msg: str, url: str = "") -> None:
    results.append({"level": level, "check": check, "msg": msg, "url": url})


# ---------------------------------------------------------------- fetching
def fetch(url: str, method: str = "GET", timeout: int = 20) -> tuple[int, str, str]:
    """Return (status, final_url, body). Body empty for non-HTML or HEAD."""
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = ""
            if method == "GET":
                ctype = r.headers.get("Content-Type", "")
                raw = r.read()
                if "html" in ctype or "xml" in ctype or "text" in ctype:
                    body = raw.decode("utf-8", "replace")
            return r.status, r.geturl(), body
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")
        except Exception:
            pass
        return e.code, url, body
    except Exception as e:  # network error
        return 0, url, f"{type(e).__name__}: {e}"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []  # (href, region)
        self.region_stack: list[str] = []
        self.h1 = 0
        self.title = ""
        self._in_title = False
        self.meta: dict[str, str] = {}
        self.canonical = ""
        self.ld: list[str] = []
        self._in_ld = False
        self._ld_buf = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("header", "footer", "nav", "main", "aside"):
            self.region_stack.append(tag)
        if tag == "a" and a.get("href"):
            region = next((r for r in reversed(self.region_stack) if r in ("header", "footer", "nav")), "main")
            self.links.append((a["href"], region))
        elif tag == "h1":
            self.h1 += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            k = a.get("name") or a.get("property")
            if k:
                self.meta[k.lower()] = a.get("content", "")
        elif tag == "link" and (a.get("rel") or "").lower() == "canonical":
            self.canonical = a.get("href", "")
        elif tag == "script" and (a.get("type") or "") == "application/ld+json":
            self._in_ld, self._ld_buf = True, ""

    def handle_endtag(self, tag):
        if tag in ("header", "footer", "nav", "main", "aside") and self.region_stack:
            self.region_stack.pop()
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._in_ld:
            self.ld.append(self._ld_buf)
            self._in_ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_ld:
            self._ld_buf += data


def norm(href: str, page_url: str) -> str:
    u = urllib.parse.urljoin(page_url, href)
    p = urllib.parse.urlsplit(u)
    return urllib.parse.urlunsplit((p.scheme, p.netloc, p.path, p.query, ""))


def visible_units(body: str) -> list[str]:
    raw = re.sub(r"<style\b.*?</style>|<script\b(?![^>]*application/(?:ld\+)?json)[^>]*>.*?</script>", " ", body, flags=re.S | re.I)
    attrs = " \n".join(re.findall(r'\b(?:content|alt|title|aria-label|placeholder)="([^"]*)"', raw, re.I))
    text = re.sub(r"<[^>]+>", "\n", raw)
    text = htmlmod.unescape(text + "\n" + htmlmod.unescape(attrs))
    text = re.sub(r"https?://\S+", " ", text)
    return [" ".join(u.split()) for u in text.split("\n") if u.strip()]


# ---------------------------------------------------------------- checks
def check_sitemap(today: dt.date) -> list[tuple[str, str]]:
    st, _, xml = fetch(BASE + "/sitemap.xml")
    if st != 200:
        rec("FAIL", "sitemap", f"sitemap.xml status {st}")
        return []
    entries = re.findall(r"<url>\s*<loc>([^<]+)</loc>(?:\s*<lastmod>([^<]+)</lastmod>)?", xml)
    locs = [e[0] for e in entries]
    for loc, n in Counter(locs).items():
        if n > 1:
            rec("FAIL", "sitemap", f"duplicate loc x{n}", loc)
    dates = []
    for loc, lm in entries:
        if not loc.startswith(BASE + "/"):
            rec("FAIL", "sitemap", "loc not on canonical host", loc)
        if not lm:
            rec("WARN", "sitemap", "no lastmod", loc)
            continue
        try:
            d = dt.date.fromisoformat(lm[:10])
        except ValueError:
            # W3C Datetime allows YYYY-MM; a full date is better, so warn instead of fail.
            rec("WARN" if re.fullmatch(r"\d{4}-\d{2}", lm) else "FAIL", "sitemap", f"lastmod is not a full date: {lm}", loc)
            continue
        dates.append(d)
        if d > today + dt.timedelta(days=1):
            rec("FAIL", "sitemap", f"lastmod in the future {lm}", loc)
    if dates and len(set(dates)) == 1 and len(dates) > 5:
        rec("FAIL", "sitemap", "every lastmod is the same date (build date leak?)")
    rec("INFO", "sitemap", f"{len(locs)} URLs, lastmod range {min(dates) if dates else '-'} .. {max(dates) if dates else '-'}")
    st, _, robots = fetch(BASE + "/robots.txt")
    if st != 200 or "sitemap:" not in robots.lower():
        rec("FAIL", "robots", f"robots.txt status {st} or no Sitemap line")
    if re.search(r"^Disallow:\s*/\s*$", robots, re.M):
        rec("FAIL", "robots", "robots.txt disallows /")
    return entries


def analyze_page(url: str, body: str, pages_seen: dict) -> None:
    p = PageParser()
    try:
        p.feed(body)
    except Exception as e:
        rec("FAIL", "seo", f"HTML parse error {e}", url)
        return
    path = urllib.parse.urlsplit(url).path
    owned = path == "/" or path.startswith(OWNED_PREFIXES)
    pages_seen[url] = p
    if p.h1 != 1:
        rec("FAIL", "seo", f"{p.h1} <h1> elements", url)
    t = p.title.strip()
    if not t:
        rec("FAIL", "seo", "missing <title>", url)
    elif len(t) > 70:
        rec("WARN", "seo", f"title {len(t)} chars (Google truncates ~60-65): {t}", url)
    d = p.meta.get("description", "")
    if not d:
        rec("FAIL", "seo", "missing meta description", url)
    elif len(d) > 170 or len(d) < 50:
        rec("WARN", "seo", f"meta description {len(d)} chars", url)
    if p.canonical.rstrip("/") != url.rstrip("/"):
        rec("FAIL", "seo", f"canonical {p.canonical!r} != URL", url)
    if "noindex" in p.meta.get("robots", "").lower():
        rec("FAIL", "seo", "meta robots noindex", url)
    if not p.ld and path != "/404.html":
        rec("WARN", "jsonld", "no JSON-LD", url)
    for blob in p.ld:
        try:
            data = json.loads(blob)
        except json.JSONDecodeError as e:
            rec("FAIL", "jsonld", f"invalid JSON-LD: {e}", url)
            continue
        items = data if isinstance(data, list) else data.get("@graph", [data]) if isinstance(data, dict) else []
        if isinstance(data, dict) and "@context" not in data:
            rec("FAIL", "jsonld", "JSON-LD without @context", url)
        for it in items:
            if not isinstance(it, dict) or "@type" not in it:
                rec("FAIL", "jsonld", "JSON-LD node without @type", url)
                continue
            for k in ("datePublished", "dateModified"):
                v = it.get(k)
                if v:
                    try:
                        dt.date.fromisoformat(str(v)[:10])
                    except ValueError:
                        # YYYY-MM is valid ISO 8601 and Google accepts it; a full date is better.
                        lvl = "WARN" if re.fullmatch(r"\d{4}-\d{2}", str(v)) else "FAIL"
                        rec(lvl, "jsonld", f"{k} not a full date: {v}", url)
            if it.get("@type") == "BreadcrumbList":
                for li in it.get("itemListElement", []):
                    if "name" not in li or "position" not in li:
                        rec("FAIL", "jsonld", "breadcrumb item missing name/position", url)
    # language
    units = visible_units(body)
    pats = list(INTERNAL_LANGUAGE) + EXTRA_LEAKS
    for u in units:
        for pat in pats:
            m = pat.search(u)
            if m:
                rec("FAIL" if owned else "WARN", "language", f"'{m.group(0)}' in: {u[:160]}", url)
    for rid, pat, _msg in BRAND_RULES:
        for m in pat.finditer(body):
            rec("FAIL" if owned else "WARN", "language", f"{rid}: {m.group(0)}", url)
    # VEN links
    for href, _r in p.links:
        if "venexecs.com" in href and "utm_source=founderdecisions" not in href:
            rec("FAIL", "ven", f"VEN link without FD UTM: {href}", url)


def check_links(pages: dict[str, str], full: bool) -> None:
    targets: dict[str, set[str]] = defaultdict(set)
    for url, body in pages.items():
        p = PageParser()
        p.feed(body)
        for href, _ in p.links:
            if href.startswith(("mailto:", "tel:", "javascript:", "#")):
                continue
            targets[norm(href, url)].add(url)
    internal = {t for t in targets if t.startswith(BASE)}
    external = {t for t in targets if t.startswith("http") and not t.startswith(BASE)}
    todo = [t for t in internal if t.split("?")[0] not in pages]

    def head(t):
        st, final, _ = fetch(t, "GET")
        return t, st, final

    with cf.ThreadPoolExecutor(12) as ex:
        for t, st, final in ex.map(head, todo):
            if st != 200:
                rec("FAIL", "links", f"internal link -> {st} (from {sorted(targets[t])[:3]})", t)
            elif final.rstrip("/") != t.split("?")[0].rstrip("/"):
                rec("WARN", "links", f"internal link redirects to {final}", t)
    for t in internal:
        if not urllib.parse.urlsplit(t).path.endswith("/") and "." not in urllib.parse.urlsplit(t).path.rsplit("/", 1)[-1]:
            rec("WARN", "links", "internal link without trailing slash (redirect hop)", t)
    rec("INFO", "links", f"{len(internal)} internal targets, {len(external)} external targets")
    if not full:
        return

    def ext(t):
        st, final, _ = fetch(t, "GET", timeout=25)
        return t, st

    with cf.ThreadPoolExecutor(16) as ex:
        for t, st in ex.map(ext, sorted(external)):
            if st >= 400 or st == 0:
                level = "WARN" if st in (0, 401, 403, 405, 429, 999) else "FAIL"
                if "venexecs.com" in t:
                    level = "FAIL"
                rec(level, "external", f"external link -> {st} (from {sorted(targets[t])[:2]})", t)


def check_structure(pages: dict[str, str], today: dt.date, max_age: int) -> None:
    home = pages.get(BASE + "/", "")
    owned_articles = {}
    for url, body in pages.items():
        path = urllib.parse.urlsplit(url).path
        m = re.match(r"^/library/([a-z0-9-]+)/([a-z0-9-]+)/$", path)
        if m:
            owned_articles[path] = m.group(1)
    # inbound links (excluding self, header/nav/footer)
    inbound: Counter = Counter()
    for url, body in pages.items():
        p = PageParser()
        p.feed(body)
        src = urllib.parse.urlsplit(url).path
        for href, region in p.links:
            u = norm(href, url)
            if u.startswith(BASE):
                tp = urllib.parse.urlsplit(u).path
                if tp != src and (region == "main" or re.fullmatch(r"/[a-z0-9-]+/", tp)):
                    # section index pages (/about/, /tools/, /compare/, ...) are reached from the header/footer
                    inbound[tp] += 1
    for url in pages:
        path = urllib.parse.urlsplit(url).path
        if path != "/" and inbound[path] == 0:
            rec("FAIL", "orphans", "no in-content link from any other page", url)
    # hub coverage
    lib = pages.get(BASE + "/library/", "")
    lib_links = {urllib.parse.urlsplit(norm(h, BASE + "/library/")).path for h, _ in _links(lib)}
    by_topic = defaultdict(list)
    for path, topic in owned_articles.items():
        by_topic[topic].append(path)
    for url in pages:
        m = re.match(r"^/library/([a-z0-9-]+)/$", urllib.parse.urlsplit(url).path)
        if m:
            by_topic.setdefault(m.group(1), [])
    for topic, paths in sorted(by_topic.items()):
        hub_url = f"{BASE}/library/{topic}/"
        hub = pages.get(hub_url)
        if hub is None:
            rec("FAIL", "hubs", "topic page missing from sitemap", hub_url)
            continue
        main = _main_html(hub)
        counts = Counter(urllib.parse.urlsplit(norm(h, hub_url)).path for h in re.findall(r'<a [^>]*href="([^"]+)"', main))
        # links inside the trailing Related/Sources sections don't count as placement
        for path in paths:
            c = _placement_count(main, path, hub_url)
            if c == 0:
                rec("FAIL", "hubs", f"not listed on its topic page /library/{topic}/", BASE + path)
            elif c > 1:
                rec("WARN", "hubs", f"listed {c}x in the topic page pick lists/table", BASE + path)
            if path not in lib_links:
                rec("FAIL", "hubs", "not linked from /library/", BASE + path)
        # tools and compare pages listed in the topic's pick lists belong to the topic too
        extra = {p for p in _group_paths(main, hub_url) if not p.startswith("/library/")}
        members = len(paths) + len(extra)
        m = re.search(rf'<h3><a href="/library/{topic}/">.*?All (\d+) pages?', home, re.S)
        if m and int(m.group(1)) != members:
            lvl = "FAIL" if int(m.group(1)) < len(paths) else "WARN"
            rec(lvl, "topics", f"homepage says All {m.group(1)} pages; topic page lists {members} ({len(paths)} articles + {len(extra)} tools/compare)", hub_url)
        rec("INFO", "hubs", f"{topic}: {len(paths)} articles + {len(extra)} tools/compare")
    # freshness
    m = re.search(r'class="page-list new-list">(.*?)</ul>', home, re.S)
    if not m:
        rec("FAIL", "freshness", "homepage New this week list not found")
        return
    rows = re.findall(r'href="([^"]+)".*?class="new-meta">[^<]*?(\d{4}-\d{2}-\d{2})', m.group(1), re.S)
    hrefs = [h for h, _ in rows]
    for h, n in Counter(hrefs).items():
        if n > 1:
            rec("FAIL", "freshness", "duplicate row in New this week", h)
    if not rows:
        rec("FAIL", "freshness", "New this week is empty")
        return
    newest = max(dt.date.fromisoformat(d) for _, d in rows)
    age = (today - newest).days
    rec("INFO", "freshness", f"New this week newest {newest} ({age}d old): {hrefs[0]}")
    if age > max_age:
        rec("FAIL", "freshness", f"newest page on homepage is {age} days old (max {max_age}); did today's ship deploy?")
    for h, d in rows:
        if (today - dt.date.fromisoformat(d)).days > 7:
            rec("WARN", "freshness", f"'New this week' row older than 7 days ({d})", h)
    # start-here / tiles duplicates
    tiles = re.findall(r'<ul class="topic-links">(.*?)</ul>', home, re.S)
    all_tile = [h for t in tiles for h in re.findall(r'href="([^"]+)"', t)]
    for h, n in Counter(all_tile).items():
        if n > 1:
            rec("WARN", "topics", f"homepage tile link repeated x{n}", h)


def _links(body: str):
    p = PageParser()
    p.feed(body)
    return p.links


def _main_html(body: str) -> str:
    m = re.search(r"<main\b.*?</main>", body, re.S)
    return m.group(0) if m else body


def _group_paths(main: str, base: str) -> list[str]:
    """Paths linked from the topic page's pick-list groups (link targets only, one per list item)."""
    out = []
    for sec in re.findall(r'<section class="pick-group">(.*?)</section>', main, re.S):
        for li in re.findall(r"<li\b.*?</li>", sec, re.S):
            h = re.search(r'<a [^>]*href="([^"]+)"', li)
            if h:
                out.append(urllib.parse.urlsplit(norm(h.group(1), base)).path)
    return out


def _placement_count(main: str, path: str, base: str) -> int:
    """How many times path is placed on the topic page: pick-list groups plus the More list.
    Topic pages without groups fall back to every link before Related / Sources."""
    more = re.search(r'(More in this topic|In this topic)</h2>(.*?)</ul>', main, re.S)
    more_paths = [urllib.parse.urlsplit(norm(h, base)).path for h in re.findall(r'<a [^>]*href="([^"]+)"', more.group(2))] if more else []
    groups = _group_paths(main, base)
    if groups:
        return groups.count(path) + more_paths.count(path)
    cut = re.split(r'<h2[^>]*>\s*(?:Related|Sources)\b', main, maxsplit=1)[0]
    # also count the "More in this topic" list which comes after the article
    more = re.search(r'(More in this topic|In this topic)</h2>(.*?)</ul>', main, re.S)
    scope = cut + (more.group(2) if more else "")
    n = 0
    for h in re.findall(r'<a [^>]*href="([^"]+)"', scope):
        if urllib.parse.urlsplit(norm(h, base)).path == path:
            n += 1
    return n


# ---------------------------------------------------------------- browser
def browser_checks(urls: list[str], full: bool, shots: Path | None) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        rec("WARN", "layout", "playwright not installed; pip install playwright && python3 -m playwright install chromium")
        return
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for width, height, mobile in ((390, 844, True), (1280, 900, False)):
            ctx = b.new_context(viewport={"width": width, "height": height}, is_mobile=mobile, has_touch=mobile,
                                device_scale_factor=2 if mobile else 1, user_agent=UA)
            page = ctx.new_page()
            errs: list[str] = []
            page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
            page.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
            for u in urls:
                errs.clear()
                try:
                    page.goto(u, wait_until="networkidle", timeout=30000)
                except Exception as e:
                    rec("FAIL", "layout", f"{width}px load failed: {e}", u)
                    continue
                info = page.evaluate("""() => {
                  const vw = document.documentElement.clientWidth;
                  const sw = document.documentElement.scrollWidth;
                  const bad = [];
                  for (const el of document.querySelectorAll('body *')) {
                    const r = el.getBoundingClientRect();
                    if (r.width === 0 || r.right <= vw + 1) continue;
                    let p = el.parentElement, clipped = false;
                    while (p && p !== document.body) {
                      const s = getComputedStyle(p);
                      if (/(auto|scroll|hidden|clip)/.test(s.overflowX)) { clipped = true; break; }
                      p = p.parentElement;
                    }
                    if (!clipped) bad.push(el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : '') + ' right=' + Math.round(r.right));
                    if (bad.length > 4) break;
                  }
                  return {vw, sw, bad};
                }""")
                if info["sw"] > info["vw"] + 1 or info["bad"]:
                    rec("FAIL", "layout", f"{width}px horizontal overflow scrollWidth={info['sw']} vw={info['vw']} {info['bad'][:3]}", u)
                for e in errs:
                    if "_vercel/insights" in e or "va.vercel-scripts" in e:
                        continue
                    rec("FAIL", "console", f"{width}px {e[:200]}", u)
                if shots is not None and (u.rstrip("/") == BASE or full is False):
                    shots.mkdir(parents=True, exist_ok=True)
                    name = (urllib.parse.urlsplit(u).path.strip("/").replace("/", "_") or "home") + f"-{width}.png"
                    page.screenshot(path=str(shots / name), full_page=True)
            if full:
                search_checks(page, width)
            ctx.close()
        b.close()


def search_checks(page, width: int) -> None:
    page.goto(BASE + "/", wait_until="networkidle")
    q = page.locator("#home-q")
    if q.count() == 0:
        rec("FAIL", "search", "homepage search box missing")
        return
    cases = {"vp equity": True, "safe": True, "runway": True, "pilot": True, "board": True,
             "equty": None, "seriesa": None, "409a": True, "zzzzqqq": False}
    for text, expect in cases.items():
        q.fill("")
        q.type(text, delay=10)
        page.wait_for_timeout(250)
        res = page.locator("#home-results")
        visible = res.is_visible()
        n = page.locator("#home-results a").count()
        body = res.inner_text() if visible else ""
        if expect is True and n == 0:
            rec("FAIL", "search", f"{width}px '{text}' returned no results")
        if expect is False and n > 0:
            rec("WARN", "search", f"{width}px nonsense '{text}' returned {n} results")
        if expect is False and visible and "no" not in body.lower():
            rec("WARN", "search", f"{width}px no-match state for '{text}' shows no message")
        if expect is None and n == 0:
            rec("WARN", "search", f"{width}px typo '{text}' returned no results")
    q.fill("")
    page.wait_for_timeout(150)
    if page.locator("#home-results a").count() and page.locator("#home-results").is_visible():
        rec("WARN", "search", f"{width}px empty query still shows results")
    q.fill("runway")
    page.wait_for_timeout(250)
    q.press("ArrowDown")
    q.press("Enter")
    page.wait_for_load_state("networkidle")
    if page.url.rstrip("/") == BASE:
        rec("FAIL", "search", f"{width}px keyboard ArrowDown+Enter did not open a result")
    page.goto(BASE + "/", wait_until="networkidle")
    q = page.locator("#home-q")
    q.fill("runway")
    q.press("Enter")
    page.wait_for_load_state("networkidle")
    if page.url.rstrip("/") == BASE:
        rec("FAIL", "search", f"{width}px Enter on a typed query went nowhere")


def check_404() -> None:
    st, _, body = fetch(BASE + "/qa-missing-page-xyz/")
    if st != 404:
        rec("FAIL", "404", f"missing page returns {st}, want 404")
    elif "Founder Decisions" not in body:
        rec("FAIL", "404", "404 body is not the site template")


# ---------------------------------------------------------------- main
def main() -> int:
    global BASE
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--full", action="store_true", help="Friday review: external links, all pages in browser, search, 404")
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--max-age", type=int, default=1, help="max days since the newest homepage page (default 1)")
    ap.add_argument("--no-browser", action="store_true")
    ap.add_argument("--screens", help="directory for 390/1280 screenshots")
    ap.add_argument("--json", help="write the report as JSON")
    ap.add_argument("--quiet", action="store_true", help="print WARN/FAIL only")
    args = ap.parse_args()
    BASE = args.base.rstrip("/")
    today = dt.date.today()

    entries = check_sitemap(today)
    urls = [BASE + "/"] + [e[0].replace("https://founderdecisions.com", BASE) for e in entries if e[0].rstrip("/") != BASE]
    pages: dict[str, str] = {}
    pages_seen: dict = {}

    def get(u):
        return u, fetch(u)

    with cf.ThreadPoolExecutor(12) as ex:
        for u, (st, final, body) in ex.map(get, urls):
            if st != 200:
                rec("FAIL", "links", f"sitemap page status {st}", u)
                continue
            pages[u] = body
    for u, body in pages.items():
        analyze_page(u, body, pages_seen)
    check_links(pages, args.full)
    check_structure(pages, today, args.max_age)
    if args.full:
        check_404()
    if not args.no_browser:
        if args.full:
            burls = sorted(pages)
        else:
            newest = re.search(r'class="page-list new-list">\s*<li><a href="([^"]+)"', pages.get(BASE + "/", ""))
            burls = [BASE + "/"] + ([norm(newest.group(1), BASE + "/")] if newest else [])
            burls += sorted(u for u in pages if re.match(re.escape(BASE) + r"/(library|tools|compare)/[a-z0-9-]*/?$", u))
        browser_checks(burls, args.full, Path(args.screens) if args.screens else None)

    order = {"FAIL": 0, "WARN": 1, "INFO": 2}
    fails = sum(r["level"] == "FAIL" for r in results)
    warns = sum(r["level"] == "WARN" for r in results)
    for r in sorted(results, key=lambda r: (order[r["level"]], r["check"], r["url"])):
        if args.quiet and r["level"] == "INFO":
            continue
        print(f"{r['level']:4} [{r['check']}] {r['msg']}" + (f"  <{r['url']}>" if r["url"] else ""))
    print(f"\n== live QA {'full' if args.full else 'daily'}: pages={len(pages)} FAIL={fails} WARN={warns} ==")
    if args.json:
        Path(args.json).write_text(json.dumps({"date": str(today), "full": args.full, "fail": fails, "warn": warns, "results": results}, indent=1))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
