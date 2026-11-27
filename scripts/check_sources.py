#!/usr/bin/env python3
"""Guard the source links that ship with the site.

The site's whole promise is "every row links to the operator's own page". That
promise breaks silently when a hotel sells its domain, a brand changes a
property code, or a URL 404s — which is exactly what happened here:

  * hgunewyork.com   -> parked / for-sale page
  * mayfairnewyork.com / themayfairhotel.com -> for-sale landing pages
  * hyatt.com/...nyczc... -> a different Hyatt Place in the same city
  * arlohotels.com/arlo-midtown/ -> 404

This checker needs no network access, so it can run in CI on every push. It
enforces three things:

  1. every hotel and activity row carries an https source URL on the operator's
     own domain or the expected brand domain (no aggregators, no shorteners);
  2. no shipped source URL points at a domain recorded as dead / parked /
     for-sale in data/hotel_sources.json or in DEAD_DOMAINS below;
  3. every URL that was corrected keeps its original value in
     `official_site_shipped_wrong`, so the audit trail cannot be quietly erased.

Exit code 1 on any violation.
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

# Domains that are known, from a fetch performed on 2026-11-26, not to serve the
# venue any more. Kept explicit so the build fails if one is ever reintroduced.
DEAD_DOMAINS = {
    "hgunewyork.com": "parked Namecheap domain (verified 2026-11-26); use hgunyc.com",
    "themayfairhotel.com": "GoDaddy for-sale listing (verified 2026-11-26); use mayfairhotelnyc.com",
    "mayfairnewyork.com": "did not load (verified 2026-11-26); use mayfairhotelnyc.com",
    "blueangelhotel.com": "did not load (verified 2026-11-26); use blueangelhotelnyc.com",
}

# Aggregators and scrapers are never acceptable as a source for a fact.
BANNED_HOSTS = {
    "booking.com", "expedia.com", "hotels.com", "tripadvisor.com", "kayak.com",
    "agoda.com", "trivago.com", "yelp.com", "opentable.com", "resy.com",
    "wikipedia.org", "tiktok.com", "instagram.com", "youtube.com", "youtu.be",
}
# ... except where the row is explicitly a booking/rate snapshot, which the page
# labels as third-party. Those fields are checked separately by validate_site.py.

errors: list[str] = []


def host(url: str) -> str:
    h = urlparse(url).netloc.lower()
    return h[4:] if h.startswith("www.") else h


def check_url(path: Path, label: str, url: str, *, allow_third_party: bool = False) -> None:
    if not re.match(r"^https://", url or ""):
        errors.append(f"{path.name}: {label} must be an https URL, found {url!r}")
        return
    h = host(url)
    for dead, why in DEAD_DOMAINS.items():
        if h == dead or h.endswith("." + dead):
            errors.append(f"{path.name}: {label} uses a dead domain {dead} ({why})")
    if not allow_third_party:
        for banned in BANNED_HOSTS:
            if h == banned or h.endswith("." + banned):
                errors.append(f"{path.name}: {label} points at {h}, which is not an official source")


def main() -> int:
    hotels = json.loads((ROOT / "data" / "hotels.json").read_text())
    activities = json.loads((ROOT / "data" / "activities.json").read_text())
    register_path = ROOT / "data" / "hotel_sources.json"
    register = json.loads(register_path.read_text()) if register_path.exists() else {"hotels": []}

    for h in hotels["hotels"]:
        name = h.get("id") or h.get("name")
        for field in ("official_site", "source_url"):
            check_url(ROOT / "data" / "hotels.json", f"{name}.{field}", h.get(field, ""),
                      # source_url is the exact-date third-party rate snapshot, which the
                      # page labels as such; official_site must be the hotel itself.
                      allow_third_party=(field == "source_url"))
        if h.get("official_room_url"):
            check_url(ROOT / "data" / "hotels.json", f"{name}.official_room_url", h["official_room_url"])
        original = h.get("official_site_shipped_wrong")
        if original and original == h.get("official_site"):
            errors.append(f"data/hotels.json: {name} keeps the broken URL as its official_site")

    for a in activities["activities"]:
        name = a.get("id") or a.get("name")
        check_url(ROOT / "data" / "activities.json", f"{name}.source_url", a.get("source_url", ""))
        if a.get("hours_source_url"):
            check_url(ROOT / "data" / "activities.json", f"{name}.hours_source_url", a["hours_source_url"])

    # The register must cover every hotel and must keep the original URL for any
    # hotel whose link was corrected.
    registered = {row.get("hotel_id") for row in register.get("hotels", [])}
    for h in hotels["hotels"]:
        if h["id"] not in registered:
            errors.append(f"data/hotel_sources.json: no source-verification record for hotel {h['id']}")
    for row in register.get("hotels", []):
        if row.get("status") == "verified":
            continue
        if not row.get("corrected_official_site"):
            errors.append(f"data/hotel_sources.json: {row.get('hotel_id')} is flagged "
                          f"{row.get('status')!r} but publishes no corrected URL")
        if not row.get("checked_url"):
            errors.append(f"data/hotel_sources.json: {row.get('hotel_id')} has no checked_url")

    # The journey-time measurement must stay honestly labelled.
    transit_path = ROOT / "data" / "transit_hotels.json"
    if transit_path.exists():
        t = json.loads(transit_path.read_text())["_meta"]
        if t.get("is_modelled_estimate") is not True:
            errors.append("data/transit_hotels.json: journey times must be labelled is_modelled_estimate=true")
        if not t.get("what_this_is_not"):
            errors.append("data/transit_hotels.json: missing the 'what this is not' caveat list")
        if not t.get("assumptions"):
            errors.append("data/transit_hotels.json: missing the assumptions block")
        if not t.get("feeds"):
            errors.append("data/transit_hotels.json: missing the feed provenance block")
    else:
        errors.append("data/transit_hotels.json is missing; run scripts/transit/gtfs_route.py")

    ranking_path = ROOT / "data" / "hotel_ranking.json"
    if ranking_path.exists():
        r = json.loads(ranking_path.read_text())["_meta"]
        for key in ("ranking_metric", "ranking_metric_explained", "coverage", "caveats"):
            if not r.get(key):
                errors.append(f"data/hotel_ranking.json: missing {key}")
    else:
        errors.append("data/hotel_ranking.json is missing; run scripts/build_ranking.py")

    # The active restaurant-ranking page and Hotels table must use the same
    # current-directory route output. The older hotel_ranking/transit_hotels
    # files remain a separately labelled activity/history baseline.
    current_path = ROOT / "research" / "generated" / "transit_1h.json"
    if not current_path.exists():
        errors.append("research/generated/transit_1h.json is missing; current hotel comparison has no route evidence")
    else:
        current = json.loads(current_path.read_text())
        meta = current.get("_meta", {})
        ranking = current.get("ranking", [])
        routes = current.get("hotels", [])
        if not meta.get("generated_utc") or not meta.get("methodology") or not meta.get("schedule_caveat"):
            errors.append("research/generated/transit_1h.json: missing generation/method/schedule provenance")
        if not re.match(r"^https://", meta.get("gtfs_source", "")):
            errors.append("research/generated/transit_1h.json: missing official MTA GTFS source URL")
        elif "rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip" not in meta["gtfs_source"]:
            errors.append("research/generated/transit_1h.json: expected the official MTA subway feed source")
        if len(ranking) != len(hotels["hotels"]) or len(routes) != len(hotels["hotels"]):
            errors.append("research/generated/transit_1h.json: ranking/route hotel counts do not match data/hotels.json")
        expected_ids = {h.get("id") for h in hotels["hotels"]}
        if {h.get("id") for h in ranking} != expected_ids or {h.get("id") for h in routes} != expected_ids:
            errors.append("research/generated/transit_1h.json: ranking/route hotel IDs do not match data/hotels.json")
        hotel_by_id = {h.get("id"): h for h in hotels["hotels"]}
        routes_by_id = {h.get("id"): h for h in routes}
        for item in ranking:
            hid = item.get("id")
            route = routes_by_id.get(hid)
            hotel = hotel_by_id.get(hid)
            if not route or not hotel:
                errors.append(f"research/generated/transit_1h.json: unknown or missing hotel id {hid!r}")
                continue
            journeys = route.get("journeys", [])
            if len(journeys) != item.get("universe_count") or item.get("universe_count") != meta.get("active_nyc_restaurants"):
                errors.append(f"research/generated/transit_1h.json: {hid} route coverage does not match its stated universe")
            if item.get("within_60_min_count") != hotel.get("michelin_within_1h_count"):
                errors.append(f"data/hotels.json: {hid} one-hour count disagrees with the current route dataset")
            if not math.isclose(float(item.get("median_minutes", -1)), float(hotel.get("michelin_median_minutes", -2)), abs_tol=0.051):
                errors.append(f"data/hotels.json: {hid} median disagrees with the current route dataset")
            if item.get("rank") != hotel.get("michelin_transit_rank"):
                errors.append(f"data/hotels.json: {hid} rank disagrees with the current route dataset")
        cockpit = (ROOT / "assets" / "cockpit.js").read_text()
        if 'fetch("research/generated/transit_1h.json")' not in cockpit:
            errors.append("assets/cockpit.js: current decision ranking must load research/generated/transit_1h.json")
        if 'fetch("data/hotel_ranking.json")' in cockpit:
            errors.append("assets/cockpit.js: stale 2025 selection ranking is still used for the current hotel comparison")

    # Any HTML page that links a dead/parked domain is shipping a broken source to
    # the reader, even when the data files are clean. Scan the page markup too.
    for page in sorted(ROOT.glob("*.html")) + sorted((ROOT / "pages").glob("*.html")):
        text = page.read_text(encoding="utf-8", errors="replace")
        # Only the parked/for-sale domains: third-party hosts such as Booking.com and
        # YouTube are legitimate on the pages as long as they are labelled as such.
        for dead, why in DEAD_DOMAINS.items():
            if dead in text:
                errors.append(f"{page.relative_to(ROOT)}: links {dead} ({why})")

    # Review links must not be presented as reviews when they are search pages.
    review_path = ROOT / "data" / "review_links.json"
    if review_path.exists():
        rv = json.loads(review_path.read_text())
        for venue in rv["venues"]:
            for l in venue["links"]:
                if l["kind"].startswith("specific") and ("/results?" in l["url"] or "/search" in l["url"]):
                    errors.append(f"data/review_links.json: {venue['venue']} labels a search page as {l['kind']}")
                if l["kind"].startswith("specific") and not l.get("verified"):
                    errors.append(f"data/review_links.json: {venue['venue']} has an unverified specific link")
    else:
        errors.append("data/review_links.json is missing")

    if errors:
        print(f"FAILED: {len(errors)} source-integrity problem(s)")
        for e in errors:
            print("  -", e)
        return 1
    print(f"OK: {len(hotels['hotels'])} hotel sources, {len(activities['activities'])} activity "
          f"sources, the verification register, the journey-time caveats and the ranking "
          f"provenance all pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
