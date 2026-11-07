"""Reads Stuxedo Web Status (the web hosting status page) and saves its overall state to data/web-status.json,
which status.stuxedo.com's Web Status button shows as a live badge.

The web hosting status page is rendered on its server and can't be read cross-site from a browser, so this
runs in the "Web status" workflow every 5 minutes instead. It only rewrites the file when the state or headline changes,
so it doesn't commit every run.

Usage: python3 scripts/web-status.py   (prints "changed" or "unchanged"; exits 1 if no source answered)
"""
import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

SOURCES = ["https://status.stuxedo.dev/"]
OUT = Path(__file__).resolve().parent.parent / "data" / "web-status.json"
# The page's top alert: alert-success / -info when all is well, -warning when degraded, -danger for outages.
STATES = {"success": "up", "info": "up", "warning": "degraded", "danger": "down"}
ALERT = re.compile(r'<div class="alert alert-(success|info|warning|danger)[^"]*"[^>]*>\s*<h4[^>]*>(.*?)</h4>', re.S)


def read(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Stuxedo-Status-web-status-check"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "replace")


def main():
    for url in SOURCES:
        try:
            m = ALERT.search(read(url))
        except Exception as e:  # noqa: BLE001 - any failure means "try the next source"
            print(f"{url}: {e}", file=sys.stderr)
            continue
        if not m:
            print(f"{url}: no status alert found", file=sys.stderr)
            continue
        state = STATES[m.group(1)]
        headline = html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
        old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
        if old.get("status") == state and old.get("headline") == headline and old.get("source") == url:
            print("unchanged")
            return 0
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps({"status": state, "headline": headline, "source": url,
                                   "updated": int(time.time())}, indent=1) + "\n", encoding="utf-8")
        print("changed")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
