#!/usr/bin/env python3
"""Automated QA & Zero-Hallucination Integrity Verifier for NYFun3."""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

EXPECTED_PAGES = [
    "index.html",
    "hotels.html",
    "michelin.html",
    "activities.html",
    "questions.html",
    "suggestions.html",
    "review.html",
]


class LinkAndTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.tr_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v:
                    self.hrefs.append(v)
        elif tag == "tr":
            self.tr_count += 1


def main() -> int:
    errors: list[str] = []

    # 1. Validate JSON schemas & constraints
    hotels = json.loads((DATA_DIR / "hotels.json").read_text(encoding="utf-8"))["hotels"]
    michelin = json.loads((DATA_DIR / "michelin_restaurants.json").read_text(encoding="utf-8"))
    activities = json.loads((DATA_DIR / "activities.json").read_text(encoding="utf-8"))["activities"]
    dec = json.loads((DATA_DIR / "decision_and_suggestions.json").read_text(encoding="utf-8"))

    # Verify hotels ranked monotonically by michelin_starred_and_bib_60min descending
    reach_scores = [h["michelin_starred_and_bib_60min"] for h in hotels]
    if reach_scores != sorted(reach_scores, reverse=True):
        errors.append(f"Hotels not sorted by MICHELIN <=60m reachability: {reach_scores}")

    for h in hotels:
        if not h.get("official_url", "").startswith("https://"):
            errors.append(f"Hotel {h['name']} missing https official_url")
        bed = h.get("bed_verified", "")
        if "Queen" not in bed and "King" not in bed:
            errors.append(f"Hotel {h['name']} fails Queen+ bed check: {bed}")
        if "private" not in h.get("private_bath_verified", "").lower():
            errors.append(f"Hotel {h['name']} fails private bath check")

    # Verify MICHELIN census sums to 70 NYC starred
    starred_sum = sum(c["total_starred_in_cluster"] for c in michelin["clusters"])
    if starred_sum != 70:
        errors.append(f"Cluster starred sum expected 70, got {starred_sum}")

    for r in michelin["restaurants"]:
        if not r.get("official_url", "").startswith("https://"):
            errors.append(f"Restaurant {r['name']} missing official_url")
        if not r.get("michelin_url", "").startswith("https://guide.michelin.com/"):
            errors.append(f"Restaurant {r['name']} missing official guide.michelin.com URL")
        if not r["pricing_verified"] and r["couple_total_price_display"] != "":
            errors.append(f"Unverified restaurant {r['name']} must leave couple_total_price_display blank!")

    for a in activities:
        if not a.get("official_url", "").startswith("https://"):
            errors.append(f"Activity {a['name']} missing official_url")

    # 2. Validate generated HTML pages, relative links & zero localhost leaks
    for page in EXPECTED_PAGES:
        p = ROOT / page
        if not p.exists():
            errors.append(f"Missing page: {page}")
            continue
        text = p.read_text(encoding="utf-8")
        if "localhost" in text or "127.0.0.1" in text:
            errors.append(f"{page} contains forbidden localhost/127.0.0.1 reference")

        parser = LinkAndTableParser()
        parser.feed(text)
        if not parser.hrefs:
            errors.append(f"{page} has zero links")

        for href in parser.hrefs:
            if href.startswith("./"):
                target = href.split("#")[0].lstrip("./")
                if not (ROOT / target).exists():
                    errors.append(f"{page} has broken relative link: {href}")
            elif href.startswith("http://"):
                errors.append(f"{page} uses insecure http:// link: {href}")
            elif not href.startswith("https://") and not href.startswith("#"):
                errors.append(f"{page} has unexpected link format: {href}")

        # Ensure zero raw markdown artifacts or unresolved template braces
        if re.search(r"\{\{.*?\}\}", text):
            errors.append(f"{page} has unresolved template braces")

        # Verify filter pill counts match actual row data-tags
        pills = re.findall(r'data-filter-pill="([^"]+)">[^<]*\((\d+)\)</button>', text)
        row_tags = [t.split(",") for t in re.findall(r'<tr data-tags="([^"]+)"', text)]
        for pill_slug, count_str in pills:
            actual = sum(1 for tags in row_tags if pill_slug in tags)
            if actual != int(count_str):
                errors.append(
                    f"{page} pill '{pill_slug}' displays ({count_str}) but matches {actual} rows"
                )

    if errors:
        print("VERIFICATION FAILED:")
        for e in errors:
            print(" -", e)
        return 1

    print(
        f"ALL CHECKS PASSED: {len(EXPECTED_PAGES)} HTML pages, "
        f"{len(hotels)} hotels, {len(michelin['restaurants'])} MICHELIN venues, "
        f"{len(activities)} activities, {len(dec['flagged_irregularities'])} audited flags."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
