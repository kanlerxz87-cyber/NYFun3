#!/usr/bin/env python3
"""Validate NYFun3 JSON schemas, source links, local links, and table source columns.

This is deliberately dependency-free: GitHub Pages serves the static site as-is,
so the validation must run with the Python standard library on any runner.
"""
from __future__ import annotations

import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(ROOT.glob("*.html")) + sorted((ROOT / "pages").glob("*.html"))
MARKDOWN_FILES = sorted(ROOT.glob("*.md")) + sorted((ROOT / "research").glob("*.md"))
JSON_FILES = sorted((ROOT / "data").glob("*.json"))
WEEKDAYS = {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}
EXPECTED_ROOT_NAV = [
    "index.html", "decide.html", "activities.html", "restaurants.html", "michelin.html",
    "hotels.html", "itinerary.html", "plan.html", "flagged-for-review.html",
    "pages/index.html",
]
EXPECTED_DOSSIER_NAV = [
    "index.html", "itinerary.html", "hotels.html", "dining.html",
    "experiences.html", "findings.html", "../flagged-for-review.html",
]
errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def valid_http_url(url: str) -> bool:
    p = urlparse(url)
    return p.scheme in {"http", "https"} and bool(p.netloc) and " " not in url


def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception as e:  # pragma: no cover - surfaced as validation error
        err(f"{path.relative_to(ROOT)}: invalid JSON: {e}")
        return None


class HtmlInfo(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids: set[str] = set()
        self.links: list[tuple[str, dict[str, str | None]]] = []
        self.assets: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = {k: v for k, v in attrs}
        if "id" in a and a["id"]:
            if a["id"] in self.ids:
                err(f"{self.path.relative_to(ROOT)}: duplicate id {a['id']!r}")
            self.ids.add(a["id"])
        if tag == "a" and a.get("href") is not None:
            self.links.append((a["href"], a))
        if tag in {"script", "img"} and a.get("src"):
            self.assets.append(a["src"])
        if tag == "link" and a.get("href"):
            self.assets.append(a["href"])


HTML_INFO: dict[Path, HtmlInfo] = {}
for path in HTML_FILES:
    info = HtmlInfo(path)
    info.feed(path.read_text())
    HTML_INFO[path] = info


def slugify(heading: str) -> str:
    h = heading.strip().lower()
    h = re.sub(r"[`*_\[\](){}#.,!?:;/\"']", "", h)
    h = re.sub(r"[^a-z0-9]+", "-", h)
    return h.strip("-")


def markdown_anchor_ok(path: Path, fragment: str) -> bool:
    text = path.read_text()
    if f'id="{fragment}"' in text:
        return True
    for line in text.splitlines():
        if line.startswith("#"):
            if slugify(line.lstrip("# ")) == fragment:
                return True
    return False


def check_local_target(source: Path, href: str) -> None:
    parsed = urlparse(href)
    frag = parsed.fragment
    rel_path = unquote(parsed.path) or source.name
    target = (source.parent / rel_path).resolve()
    if not target.is_relative_to(ROOT.resolve()):
        err(f"{source.relative_to(ROOT)}: link escapes workspace: {href}")
        return
    if not target.exists():
        err(f"{source.relative_to(ROOT)}: broken local link: {href}")
        return
    if frag:
        if target.suffix == ".html":
            info = HTML_INFO.get(target)
            if info is None:
                info = HtmlInfo(target)
                info.feed(target.read_text())
                HTML_INFO[target] = info
            if frag not in info.ids:
                err(f"{source.relative_to(ROOT)}: broken anchor {href} (id {frag!r} not found)")
        elif target.suffix == ".md" and not markdown_anchor_ok(target, frag):
            err(f"{source.relative_to(ROOT)}: broken markdown anchor {href}")


def check_url(source: Path, url: str, *, context: str = "link") -> None:
    if not url:
        return
    if url.startswith("#"):
        check_local_target(source, url)
        return
    if url.startswith(("mailto:", "tel:", "data:", "javascript:")):
        if url.startswith("javascript:"):
            err(f"{source.relative_to(ROOT)}: javascript: URL is not allowed")
        return
    parsed = urlparse(url)
    if parsed.scheme:
        if not valid_http_url(url):
            err(f"{source.relative_to(ROOT)}: invalid external {context}: {url}")
        elif parsed.scheme == "http":
            warn(f"{source.relative_to(ROOT)}: external {context} uses http, not https: {url}")
        return
    if url.startswith("//"):
        err(f"{source.relative_to(ROOT)}: protocol-relative {context} is not allowed: {url}")
        return
    check_local_target(source, url)


# HTML links, assets, and external-link hygiene.
for path, info in HTML_INFO.items():
    for href, attrs in info.links:
        check_url(path, href)
        if attrs.get("target") == "_blank":
            rel = attrs.get("rel") or ""
            if "noopener" not in rel or "noreferrer" not in rel:
                err(f"{path.relative_to(ROOT)}: target=_blank without rel=noopener noreferrer: {href}")
    for asset in info.assets:
        check_url(path, asset, context="asset")
    text = path.read_text()
    if "localhost" in text or "127.0.0.1" in text:
        err(f"{path.relative_to(ROOT)}: browser-facing HTML must not call localhost/127.0.0.1")
    # Check JSON paths referenced by inline render scripts.
    for rel in re.findall(r'(?:NYF\.load|fetch)\(\s*["\']([^"\']+)["\']', text):
        check_url(path, rel, context="data load")

# Markdown links.
for path in MARKDOWN_FILES:
    text = path.read_text()
    for href in re.findall(r"\[[^\]]+\]\(([^)\s]+)\)", text):
        check_url(path, html.unescape(href), context="markdown link")

# Meta-refresh redirect in review.html.
review = ROOT / "review.html"
if review.exists():
    for target in re.findall(r'url=([^"\']+)', review.read_text()):
        check_url(review, target.strip(), context="redirect")

# Every static table body row needs a source link, and the header must say Source.
for path in HTML_FILES:
    text = re.sub(r"<script.*?</script>", "", path.read_text(), flags=re.S)
    for table in re.findall(r"<table.*?</table>", text, flags=re.S):
        header_match = re.search(r"<thead.*?</thead>", table, flags=re.S)
        header = header_match.group(0) if header_match else ""
        if not header:
            first_tr = re.search(r"<tr.*?</tr>", table, flags=re.S)
            if first_tr and "<th" in first_tr.group(0):
                header = first_tr.group(0)
        body = re.sub(r"<thead.*?</thead>", "", table, flags=re.S) if header_match else table
        body_rows = [r for r in re.findall(r"<tr.*?</tr>", body, flags=re.S) if "<td" in r]
        if not body_rows:
            continue
        if "source" not in re.sub(r"<[^>]+>", " ", header).lower():
            err(f"{path.relative_to(ROOT)}: table has body rows but no Source header")
        for i, row in enumerate(body_rows, 1):
            if "<a " not in row or "href=" not in row:
                err(f"{path.relative_to(ROOT)}: static table body row {i} has no source link")

# Dynamic renderer strings must expose source links too.
renderer_requirements = {
    ROOT / "assets/app.js": ["priceForTwo", "sourceCell", "2 × "],
    ROOT / "activities.html": ["<th>Source</th>", "NYF.srcLink(a.source_url", "hours_source_url"],
    ROOT / "restaurants.html": ["<th>Source</th>", "NYF.priceForTwo(r)", "NYF.sourceCell(r)", "function clusterKey"],
    ROOT / "michelin.html": ["<th>Source</th>", "NYF.priceForTwo(r)", "NYF.sourceCell(r)", "DATA._meta.official_list_url", "by[k].urls"],
    ROOT / "hotels.html": ["<th>Source</th>", "NYF.srcLink(h.official_site, \"official hotel\")", "rate snapshot"],
    ROOT / "itinerary.html": ["<th>Source</th>", "rowSources(d)", "NYF.srcLink(a.source_url"],
}
for path, needles in renderer_requirements.items():
    text = path.read_text()
    for needle in needles:
        if needle not in text:
            err(f"{path.relative_to(ROOT)}: renderer missing required source/price logic: {needle}")

# Navigation consistency.
for path in ROOT.glob("*.html"):
    m = re.search(r'<nav class="main".*?</nav>', path.read_text(), flags=re.S)
    if not m:
        continue
    for href in EXPECTED_ROOT_NAV:
        if f'href="{href}"' not in m.group(0):
            err(f"{path.relative_to(ROOT)}: root nav missing {href}")
for path in sorted((ROOT / "pages").glob("*.html")):
    m = re.search(r'<nav class="primary-nav".*?</nav>', path.read_text(), flags=re.S)
    if not m:
        err(f"{path.relative_to(ROOT)}: dossier primary nav missing")
        continue
    for href in EXPECTED_DOSSIER_NAV:
        if f'href="{href}"' not in m.group(0):
            err(f"{path.relative_to(ROOT)}: dossier nav missing {href}")

# JSON schema / arithmetic / source checks.
data: dict[str, object] = {}
for path in JSON_FILES:
    d = load_json(path)
    if d is not None:
        data[path.name] = d
        for url in re.findall(r'https?://[^\s"<>]+', path.read_text()):
            clean = url.rstrip(",.);]")
            if not valid_http_url(clean):
                err(f"{path.relative_to(ROOT)}: malformed URL in JSON: {clean}")

expected_counts = {
    "activities.json": (15, "activities"),
    "hotels.json": (14, "hotels"),
    "itinerary.json": None,
    "michelin.json": (12, "restaurants"),
    "michelin_two_star.json": (15, "restaurants"),
    "michelin_one_star.json": (52, "restaurants"),
    "michelin_all.json": (72, "restaurants"),
}
for name, expected in expected_counts.items():
    if name not in data or not isinstance(data[name], dict):
        err(f"data/{name}: missing or not an object")
        continue
    if expected:
        n, key = expected
        rows = data[name].get(key)
        if not isinstance(rows, list) or len(rows) != n:
            err(f"data/{name}: expected {n} {key}, found {len(rows) if isinstance(rows, list) else 'non-list'}")

activities = data.get("activities.json", {}).get("activities", [])
hotels = data.get("hotels.json", {}).get("hotels", [])
michelin_all = data.get("michelin_all.json", {}).get("restaurants", [])

for a in activities:
    if not all(k in a for k in ("id", "name", "source_url", "hours_table", "hours_flag")):
        err(f"activities: row missing required key: {a.get('name', '<unnamed>')}")
    if not valid_http_url(str(a.get("source_url", ""))):
        err(f"activities: invalid source_url for {a.get('name')}")
    ht = a.get("hours_table", {})
    if not isinstance(ht, dict) or set(ht) - WEEKDAYS:
        err(f"activities: invalid hours_table for {a.get('name')}")
    if ht and (a.get("hours_verified_on") not in ("2026-11-25", "2026-11-26") or not a.get("hours_baseline_note")):
        err(f"activities: populated hours missing capture metadata for {a.get('name')}")
    if not ht and not str(a.get("hours_flag", "")).startswith(("UNVERIFIED", "PARTIAL", "SEASONAL", "N/A", "CURRENT")):
        err(f"activities: blank hours missing flag for {a.get('name')}")
    if a.get("price_adult_usd") is None and not str(a.get("price_note", "")).startswith("UNVERIFIED"):
        err(f"activities: blank price must carry UNVERIFIED note for {a.get('name')}")

for h in hotels:
    for k in ("name", "official_site", "booking_url", "source_url", "rate_tiers"):
        if k not in h:
            err(f"hotels: missing {k} for {h.get('name', '<unnamed>')}")
    for k in ("official_site", "booking_url", "source_url"):
        if h.get(k) and not valid_http_url(str(h[k])):
            err(f"hotels: invalid {k} for {h.get('name')}")
    cnt = h.get("michelin_within_1h_count")
    if not isinstance(cnt, int) or cnt < 0:
        err(f"hotels: michelin_within_1h_count must be a measured non-negative integer for {h.get('name')}")
    for t in h.get("rate_tiers", []):
        if "room" not in t or not isinstance(t.get("total_before_tax_usd"), (int, float)):
            err(f"hotels: malformed rate tier for {h.get('name')}")

PRICE_CAVEAT = "excludes beverages, tax, and gratuity"
for name in ("michelin.json", "michelin_two_star.json", "michelin_one_star.json", "michelin_all.json"):
    d = data.get(name)
    if not isinstance(d, dict):
        continue
    for r in d.get("restaurants", []):
        nm = r.get("name", "<unnamed>")
        if not valid_http_url(str(r.get("michelin_url", ""))):
            err(f"{name}: invalid michelin_url for {nm}")
        opts = r.get("price_options", [])
        pair = r.get("price_for_two_usd")
        if opts:
            if not isinstance(pair, (int, float)) or not r.get("price_source_url") or not r.get("price_sources"):
                err(f"{name}: priced row {nm} missing price_for_two_usd/source metadata")
            if r.get("price_basis") != "2 × official per-person price":
                err(f"{name}: priced row {nm} missing 2 × official per-person basis")
            if PRICE_CAVEAT not in str(r.get("price_caveat", "")):
                err(f"{name}: priced row {nm} missing standard exclusions caveat")
            if not str(r.get("price_flag", "")).startswith("VERIFIED"):
                err(f"{name}: priced row {nm} price_flag should start VERIFIED")
            for o in opts:
                if o.get("for_two_usd") != 2 * o.get("per_person_usd"):
                    err(f"{name}: bad couple arithmetic for {nm}: {o}")
                if not valid_http_url(str(o.get("source_url", ""))):
                    err(f"{name}: price option for {nm} missing official source URL")
        else:
            if pair not in ("", None):
                err(f"{name}: unpriced row {nm} has price_for_two_usd={pair!r}")
            if not str(r.get("price_flag", "")).startswith("UNVERIFIED"):
                err(f"{name}: unpriced row {nm} price_flag should start UNVERIFIED")

if michelin_all:
    meta = data["michelin_all.json"].get("_meta", {})
    counts = meta.get("counts", {})
    if counts != {"three_star": 5, "two_star": 15, "one_star": 52, "total": 72}:
        err("michelin_all.json: unexpected star counts")
    if meta.get("ungrouped_count") != sum((not r.get("cluster")) or bool(r.get("cluster_flag")) for r in michelin_all):
        err("michelin_all.json: ungrouped_count does not match flagged/blank clusters")
    priced = sum(bool(r.get("price_options")) for r in michelin_all)
    if priced != 25:
        err(f"michelin_all.json: expected 25 priced rows, found {priced}")
    if "14 DECEMBER 2026" not in str(meta.get("star_caveat", "")).upper():
        err("michelin_all.json: 2026 ceremony caveat missing")

itinerary = data.get("itinerary.json", {})
if itinerary:
    days = itinerary.get("days", [])
    if len(days) != 7 or len(itinerary.get("second_week_suggestions", [])) != 3:
        err("itinerary.json: expected 7 days and 3 second-week suggestions")
    if not itinerary.get("_meta", {}).get("source_links"):
        err("itinerary.json: source_links metadata missing")
    activity_ids = {a.get("id") for a in activities}
    for d in days:
        for slot in ("morning", "afternoon", "evening"):
            for s in d.get(slot, []):
                if isinstance(s, dict) and s.get("activity") not in activity_ids:
                    err(f"itinerary.json: unknown activity id {s.get('activity')}")

# Report.
print(f"Validated {len(JSON_FILES)} JSON files, {len(HTML_FILES)} HTML pages, {len(MARKDOWN_FILES)} markdown docs")
print(f"Rows: {len(activities)} activities, {len(hotels)} hotels, {len(michelin_all)} starred restaurants, {len(itinerary.get('days', []))} itinerary days")
for w in warnings:
    print("WARNING:", w)
if errors:
    print(f"FAILED with {len(errors)} error(s):", file=sys.stderr)
    for e in errors:
        print(" -", e, file=sys.stderr)
    sys.exit(1)
print("OK: schemas, price arithmetic, source links, local links, anchors, navigation, and table Source columns pass")
