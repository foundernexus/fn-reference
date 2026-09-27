#!/usr/bin/env python3
"""Guard a prose rewrite: numbers, URLs, and Sources sections must not change.

Compares each content/**/*.md file in the working tree with the same file at a
git ref (default HEAD). Use it after any stop-slop edit pass on an existing page.

  python3 ops/stop-slop/facts_guard.py            # vs HEAD
  python3 ops/stop-slop/facts_guard.py origin/main
  python3 ops/stop-slop/facts_guard.py HEAD content/library/board/_hub.md

Fails (exit 1) when, for any file:
  - the multiset of numbers (digits, with % $ x suffixes) differs
  - the multiset of link URLs differs
  - the `## Sources` section text differs
  - frontmatter title or slug differs
New files are skipped (nothing to compare against).
"""
from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NUM = re.compile(r"(?<![A-Za-z])[$€£]?\d[\d,]*(?:\.\d+)?\s?(?:%|×|x\b|[kKmMbB]\b)?")
URLRE = re.compile(r"\]\(([^)\s]+)\)|https?://[^\s)\]>]+")


def sources(text: str) -> str:
    m = re.search(r"^## Sources\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def fm_field(text: str, key: str) -> str:
    m = re.search(rf"^{key}:\s*(.*)$", text, re.M)
    return m.group(1).strip() if m else ""


def nums(text: str) -> Counter:
    return Counter(n.replace(" ", "").replace(",", "") for n in NUM.findall(text))


def urls(text: str) -> Counter:
    out = Counter()
    for m in URLRE.finditer(text):
        out[m.group(1) or m.group(0)] += 1
    return out


def at_ref(ref: str, rel: str) -> str | None:
    r = subprocess.run(["git", "show", f"{ref}:{rel}"], cwd=ROOT, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    ref = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    chk = subprocess.run(["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"], cwd=ROOT, capture_output=True)
    if chk.returncode != 0:
        print(f"facts_guard: unknown git ref {ref!r}", file=sys.stderr)
        return 2
    files = [Path(a).resolve() for a in sys.argv[2:]] or sorted((ROOT / "content").rglob("*.md"))
    bad = 0
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        old = at_ref(ref, rel)
        if old is None:
            continue
        new = f.read_text(encoding="utf-8")
        probs = []
        dn = nums(old) - nums(new), nums(new) - nums(old)
        if dn[0] or dn[1]:
            probs.append(f"numbers removed={dict(dn[0])} added={dict(dn[1])}")
        du = urls(old) - urls(new), urls(new) - urls(old)
        if du[0] or du[1]:
            probs.append(f"urls removed={list(du[0])} added={list(du[1])}")
        if sources(old) != sources(new):
            probs.append("Sources section changed")
        for k in ("title", "slug"):
            if fm_field(old, k) != fm_field(new, k):
                probs.append(f"{k} changed")
        if probs:
            bad += 1
            print(f"FAIL {rel}:\n  " + "\n  ".join(probs))
    print("facts_guard:", "FAIL" if bad else "PASS", f"({len(files)} files vs {ref})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
