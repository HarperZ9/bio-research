"""Pull citation contexts from the Semantic Scholar Graph API.

Saves each page of raw JSON under data/audit04/raw/<TARGET>/page_<offset>.json.
No API key. Sleeps between calls and retries on 429 and 5xx.
"""
import json
import sys
import time

import requests

from config import RAW, TARGETS

API = "https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}/citations"
FIELDS = "contexts,intents,title,year,externalIds"
LIMIT = 100
PAUSE = 3.5


def get_page(doi, offset, tries=6):
    """Fetch one page; retry with backoff. Raises after the last try."""
    params = {"fields": FIELDS, "limit": LIMIT, "offset": offset}
    for attempt in range(tries):
        resp = requests.get(API.format(doi=doi), params=params, timeout=60)
        if resp.status_code == 200:
            return resp.json()
        wait = PAUSE * (2 ** attempt)
        print(f"  HTTP {resp.status_code} at offset {offset}; retry in {wait:.0f}s",
              file=sys.stderr)
        time.sleep(wait)
    raise RuntimeError(f"failed after {tries} tries: {doi} offset {offset} "
                       f"last status {resp.status_code}: {resp.text[:200]}")


def fetch_target(name, doi):
    out = RAW / name
    out.mkdir(parents=True, exist_ok=True)
    offset, total = 0, 0
    while True:
        path = out / f"page_{offset:05d}.json"
        if path.exists():
            page = json.loads(path.read_text(encoding="utf-8"))
        else:
            page = get_page(doi, offset)
            path.write_text(json.dumps(page, ensure_ascii=False), encoding="utf-8")
            time.sleep(PAUSE)
        rows = page.get("data", [])
        total += len(rows)
        print(f"{name}: offset {offset}, {len(rows)} rows")
        nxt = page.get("next")
        if not rows or nxt is None:
            break
        offset = nxt
    return total


if __name__ == "__main__":
    for target, doi in TARGETS.items():
        n = fetch_target(target, doi)
        print(f"{target}: {n} citing records saved")
