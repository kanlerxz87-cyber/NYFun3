#!/usr/bin/env python3
"""Probe official pages through a read-only browser-rendering proxy.

Jina Reader is used only as a rendering/retrieval aid. Every result records the
original official URL separately. It is not treated as the authoritative source.
"""
from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
from diagnose import compact, structured_examples, visible_snippets  # noqa: E402

OUT = Path("research/generated/reader-diagnostics.json")

HYATT_PARAMS = {
    "checkinDate": "2027-02-15",
    "checkoutDate": "2027-02-22",
    "rooms": "1",
    "adults": "2",
    "kids": "0",
    "rate": "Standard",
    "accessibilityCheck": "false",
}

TARGETS = {
    "hyatt_nyczm": f"https://www.hyatt.com/shop/rooms/nyczm?{urlencode(HYATT_PARAMS)}",
    "hyatt_nyczt": f"https://www.hyatt.com/shop/rooms/nyczt?{urlencode(HYATT_PARAMS)}",
    "michelin_base": "https://guide.michelin.com/us/en/new-york-state/new-york/restaurants",
    "michelin_all_starred": "https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred",
    "michelin_le_coucou": "https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/le-coucou",
    "michelin_one_star": "https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/1-star-michelin",
}


def reader_get(target: str, respond_with: str) -> dict:
    url = "https://r.jina.ai/" + target
    headers = {
        "Accept": "text/plain",
        "X-Respond-With": respond_with,
        "X-Engine": "browser",
        "X-Timeout": "25",
        "X-Respond-Timing": "visible-content",
        "X-No-Cache": "true",
        "X-User-Agent": "diversify",
        "X-Retain-Images": "none",
        "DNT": "1",
    }
    try:
        response = requests.get(url, headers=headers, timeout=180)
        item = {
            "reader_url": url,
            "official_source": target,
            "respond_with": respond_with,
            "http_status": response.status_code,
            "bytes": len(response.content),
            "head": response.text[:1200],
            "body_excerpt": response.text[:12000],
        }
    except Exception as exc:
        return {
            "reader_url": url,
            "official_source": target,
            "respond_with": respond_with,
            "error": f"{type(exc).__name__}: {exc}",
        }
    if respond_with == "html":
        soup = BeautifulSoup(response.text, "html.parser")
        links = []
        for a in soup.select('a[href*="/restaurant/"]'):
            href = a.get("href")
            name = re.sub(r"\s+", " ", a.get_text(" ", strip=True))
            if href and not any(x["href"] == href for x in links):
                links.append({"name": name, "href": href})
        item.update({
            "title": soup.title.get_text(" ", strip=True) if soup.title else None,
            "has_avg_night": "Avg/Night" in response.text,
            "has_price_specification": "priceSpecification" in response.text,
            "structured_examples": structured_examples(response.text),
            "restaurant_links_found": len(links),
            "first_restaurant_links": links[:10],
            "rate_snippets": visible_snippets(
                response.text,
                r"Avg/Night|Standard Rate|Member Rate|Excludes tax|Includes fees|\$[0-9][0-9,.]*",
                limit=12,
            ),
        })
        marker = response.text.find("/restaurant/")
        item["restaurant_html_excerpt"] = response.text[max(0, marker - 800):marker + 1800] if marker >= 0 else None
    else:
        item["text_snippets"] = visible_snippets(
            response.text,
            r"Avg/Night|Standard Rate|Member Rate|Excludes tax|Includes fees|\$[0-9][0-9,.]*|1-48 of|restaurants",
            limit=15,
        )
    return item


def main() -> None:
    result = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "warning": "Jina Reader is a retrieval proxy. The official source is recorded in official_source; values are not authoritative until confirmed on that official page or its official structured data.",
        "requests": {},
    }
    for key, target in TARGETS.items():
        result["requests"][key] = {
            "official_source": target,
            "html": reader_get(target, "html"),
            "text": reader_get(target, "text") if key.startswith("hyatt_") else None,
        }
        print(f"Probed {key}: html {result['requests'][key]['html'].get('http_status')} / {result['requests'][key]['html'].get('bytes')} bytes")
        time.sleep(2)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
    for key in ("hyatt_nyczm", "michelin_base", "michelin_le_coucou"):
        item = result["requests"][key]["html"]
        print(f"=== {key} examples ===")
        print(json.dumps({
            "head": item.get("head"),
            "has_avg_night": item.get("has_avg_night"),
            "structured": item.get("structured_examples", [])[:3],
            "links": item.get("first_restaurant_links", [])[:5],
            "rate_snippets": item.get("rate_snippets", [])[:5],
        }, indent=2)[:10000])


if __name__ == "__main__":
    main()
