#!/usr/bin/env python3
"""Offline acceptance checks for the unpublished static landing bundle."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
ROBOTS = (ROOT / "robots.txt").read_text(encoding="utf-8")

class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = []
        self.links = []
        self.jsonld = []
        self._script_type = None
        self._script_text = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta": self.meta.append(attrs)
        if tag == "link": self.links.append(attrs)
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self._script_type = attrs["type"]
            self._script_text = []
    def handle_data(self, data):
        if self._script_type: self._script_text.append(data)
    def handle_endtag(self, tag):
        if tag == "script" and self._script_type:
            self.jsonld.append("".join(self._script_text))
            self._script_type = None

p = MetadataParser(); p.feed(HTML)
meta = {x.get("name"): x.get("content") for x in p.meta if x.get("name")}
props = {x.get("property"): x.get("content") for x in p.meta if x.get("property")}
links = {x.get("rel"): x.get("href") for x in p.links if x.get("rel") and x.get("href")}
checks = []
def check(ok, message):
    checks.append((ok, message))

for name in ("description", "robots", "viewport"):
    check(name in meta and meta[name], f"meta name={name}")
for prop in ("og:type", "og:title", "og:description", "og:url", "og:site_name"):
    check(prop in props and props[prop], f"Open Graph {prop}")
for name in ("twitter:card", "twitter:title", "twitter:description"):
    check(name in meta and meta[name], f"Twitter {name}")
check("canonical" in links and links["canonical"].startswith("https://"), "absolute HTTPS canonical")
check("DRAFT / UNPUBLISHED" in HTML, "explicit unpublished state")
check("https://abubakar-automation-server-01.tail1185d0.ts.net/revenue-demo/" in HTML, "customer-initiated Revenue CTA")
check("Do not submit passwords" in HTML, "sensitive-data notice")
check("$0" in HTML and "budget" in HTML.lower(), "zero-budget boundary")
check("noindex" in meta["robots"] and "Disallow: /" in ROBOTS, "draft crawler gate")
for blob in p.jsonld:
    try: data = json.loads(blob)
    except json.JSONDecodeError: data = None
    check(isinstance(data, dict) and data.get("@context") == "https://schema.org", "valid JSON-LD")
check(any(json.loads(x).get("@type") == "Organization" for x in p.jsonld), "Organization JSON-LD")
check(any(json.loads(x).get("@type") == "Service" for x in p.jsonld), "Service JSON-LD")

# Scan all shipped text, while allowing the documented CTA/canonical host only.
text = "\n".join(x.read_text(encoding="utf-8") for x in ROOT.iterdir() if x.is_file() and x.name != "test_landing.py" and x.suffix in {".html", ".css", ".js", ".txt", ".md", ".py"})
secret_patterns = [r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", r"(?:sk|pk|ghp|github_pat|xox[baprs])-[_A-Za-z0-9-]{12,}", r"(?i)(?:password|passwd|api[_-]?key|secret)\s*[:=]\s*['\"]?[^\s'\"]{8,}"]
check(not any(re.search(pattern, text) for pattern in secret_patterns), "no secret-like material")
deceptive = [r"(?i)\b(?:we|our|this)\s+(?:guarantee|guarantees|guaranteed|proven results)", r"(?i)\b\d+%\s+(?:more|increase|improvement)"]
check(not any(re.search(pattern, HTML) for pattern in deceptive), "no deceptive performance claims")
tracking = [r"google-analytics", r"googletagmanager", r"facebook\.net", r"connect\.facebook", r"tracking\s+pixel", r"plausible\.io", r"umami"]
check(not any(re.search(pattern, text, re.I) for pattern in tracking), "no external tracking")
auto_contact = [r"mailto:", r"tel:", r"navigator\.sendBeacon", r"XMLHttpRequest", r"fetch\s*\(", r"action\s*=", r"<form\b"]
check(not any(re.search(pattern, HTML, re.I) for pattern in auto_contact), "no form or automatic contact")

failed = [message for ok, message in checks if not ok]
for ok, message in checks: print(f"{'PASS' if ok else 'FAIL'}: {message}")
if failed:
    print(f"{len(failed)} check(s) failed", file=sys.stderr)
    raise SystemExit(1)
print(f"{len(checks)} checks passed")
