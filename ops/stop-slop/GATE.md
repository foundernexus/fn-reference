# Daily stop-slop gate (required before push)

Applies to every new or edited owned page: `content/library/**`, `content/tools/**`, `content/compare/**`, `content/about.md`, and homepage or template copy in `build.py` / `static/assets/js/*.js`. It does not apply to `/decisions/` or `/benchmarks/`, which the build generates from foundernexus/fn-content.

The gate runs locally. It is not wired into `build.py` or `vercel.json`, so a style hit can never fail a Vercel build. Do not add it there.

## Steps

1. **Mechanical check.** `python3 ops/stop-slop/check.py --changed` (or pass the file paths). Fix every HARD hit until it reports `HARD=0`. Read the soft list with `--soft` and fix what a plainer sentence fixes.
2. **Facts guard (edited existing pages).** `python3 ops/stop-slop/facts_guard.py origin/main`. It must print PASS: same numbers, same link URLs, same `## Sources` text, same title and slug as main.
3. **Manual read.** Read the page top to bottom against `ops/stop-slop/RULES.md`. Score it on the five dimensions. Below 35/50: revise.
4. **Build.** `python3 build.py` must pass (JSON-LD assert included).
5. **Record.** Put `stop-slop: pass (HARD=0, score NN/50)` in the commit message body and in the page's `ops/inventory.md` notes.

`ops/stop-slop/prepush.sh` runs steps 1, 2, and 4 in order and stops on the first failure. Step 3 stays manual.

## Optional git hook

To run the script on every `git push` from this checkout:

```
ln -sf ../../ops/stop-slop/prepush.sh .git/hooks/pre-push
```

## Report-only scans

- `python3 ops/stop-slop/check.py --dist` scans rendered owned HTML (homepage, hubs, template strings).
- `python3 ops/stop-slop/check.py --generated` scans `/decisions/` and `/benchmarks/`. Never fix those in this repo. Send findings to foundernexus/fn-content.
