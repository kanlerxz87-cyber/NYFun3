#!/usr/bin/env python3
"""Read official public pages and record structured diagnostics.

This script never invents data. It records HTTP status, parsed structured data,
and short excerpts so a later collector can be written against the real shape
of each official source.
"""
from __future__ import annotations

import csv
import io
import json
import re
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

OUT = Path("research/generated/diagnostics.json")
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def fetch(url: str, params: dict | None = None) -> tuple[int, str, str]:
    try:
        r = SESSION.get(url, params=params, timeout=45)
        return r.status_code, r.text, r.url
    except Exception as exc:  # pragma: no cover - diagnostic output only
        return -1, f"ERROR: {type(exc).__name__}: {exc}", url


def compact(value, limit: int = 1600):
    text = json.dumps(value, ensure_ascii=False, default=str)
    return text if len(text) <= limit else text[:limit] + "…"


def walk_dicts(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_dicts(child)


def jsonld_blocks(html: str) -> tuple[list, list]:
    soup = BeautifulSoup(html, "html.parser")
    parsed, snippets = [], []
    for script in soup.find_all("script"):
        script_type = (script.get("type") or "").lower()
        raw = script.string or script.get_text()
        if not raw or not raw.strip():
            continue
        if "ld+json" in script_type or ('"@context"' in raw and '"@type"' in raw):
            snippets.append(raw.strip()[:4000])
            try:
                parsed.append(json.loads(raw))
            except Exception:
                pass
    return parsed, snippets


def structured_examples(html: str, max_items: int = 12) -> list:
    examples = []
    blocks, snippets = jsonld_blocks(html)
    for block in blocks:
        for obj in walk_dicts(block):
            keys = set(obj)
            if keys & {"offers", "priceSpecification", "openingHoursSpecification", "geo", "starRating"}:
                examples.append(compact(obj))
            elif obj.get("@type") in {"Restaurant", "Hotel", "HotelRoom", "Place", "LodgingBusiness"}:
                examples.append(compact(obj))
            if len(examples) >= max_items:
                return examples
    # If nothing parsed, return raw snippets so the shape can be inspected.
    return [compact({"unparsed_jsonld_snippet": s}) for s in snippets[:max_items]]


def visible_snippets(html: str, pattern: str, window: int = 180, limit: int = 8) -> list:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
    out = []
    for match in re.finditer(pattern, text, flags=re.I):
        start = max(0, match.start() - window // 2)
        end = min(len(text), match.end() + window // 2)
        out.append(text[start:end])
        if len(out) >= limit:
            break
    return out


def hyatt_diagnostics() -> dict:
    base = "https://www.hyatt.com/shop/rooms/{code}"
    params = {
        "checkinDate": "2027-02-15",
        "checkoutDate": "2027-02-22",
        "rooms": "1",
        "adults": "2",
        "kids": "0",
        "rate": "Standard",
        "accessibilityCheck": "false",
    }
    result = {}
    for code in ("nyczm", "nyczt"):
        url = base.format(code=code) + "?" + urlencode(params)
        status, html, final = fetch(url)
        result[code] = {
            "source": final,
            "status": status,
            "bytes": len(html),
            "has_avg_night": "Avg/Night" in html,
            "has_price_specification": "priceSpecification" in html,
            "structured_examples": structured_examples(html),
            "visible_rate_snippets": visible_snippets(
                html, r"Avg/Night|Standard Rate|Member Rate|Excludes tax|Includes fees"
            ),
        }
        time.sleep(1)
    search_url = "https://www.hyatt.com/search/hotels/en-US/New%20York?" + urlencode(params | {"location": "New York"})
    status, html, final = fetch(search_url)
    codes = sorted(set(re.findall(r"/shop/rooms/([A-Za-z0-9_-]+)", html)))
    spirit_codes = sorted(set(re.findall(r'"spiritCode"\s*:\s*"([A-Za-z0-9_-]+)"', html)))
    result["search"] = {
        "source": final,
        "status": status,
        "bytes": len(html),
        "shop_room_codes": codes[:100],
        "spirit_codes": spirit_codes[:100],
    }
    return result


def michelin_diagnostics() -> dict:
    result = {}
    list_urls = {
        "base": "https://guide.michelin.com/us/en/new-york-state/new-york/restaurants",
        "all_starred": "https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred",
        "three_star": "https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/3-stars-michelin",
        "two_star": "https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/2-stars-michelin",
        "one_star": "https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/1-star-michelin",
        "bib_gourmand": "https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/bib-gourmand",
        "selected": "https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/selected-restaurants",
    }
    for key, url in list_urls.items():
        status, html, final = fetch(url)
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for a in soup.select('a[href*="/restaurant/"]'):
            name = re.sub(r"\s+", " ", a.get_text(" ", strip=True))
            href = a.get("href")
            if name and href and (name, href) not in [(x["name"], x["href"]) for x in links]:
                links.append({"name": name, "href": href})
        cards = []
        for a in soup.select('a[href*="/restaurant/"]')[:3]:
            parent = a.find_parent(["article", "li", "div"])
            cards.append({
                "tag": parent.name if parent else None,
                "classes": parent.get("class") if parent else None,
                "data_attrs": parent.attrs if parent else None,
                "html_excerpt": str(parent)[:1800] if parent else str(a)[:1800],
            })
        result[key] = {
            "source": final,
            "status": status,
            "bytes": len(html),
            "restaurant_links_found": len(links),
            "first_links": links[:8],
            "card_examples": cards,
            "page_label": visible_snippets(html, r"1-48 of|1-[0-9]+ of|restaurants", limit=3),
        }
        time.sleep(0.7)
    restaurant_urls = {
        "le_coucou": "https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/le-coucou",
        "sushi_sho": "https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/sushi-sho-1213976",
    }
    result["individual_pages"] = {}
    for key, url in restaurant_urls.items():
        status, html, final = fetch(url)
        result["individual_pages"][key] = {
            "source": final,
            "status": status,
            "bytes": len(html),
            "structured_examples": structured_examples(html),
            "visible_detail_snippets": visible_snippets(
                html, r"MICHELIN Guide|Opening hours|Hours|Address|Price|\\$|reservation", limit=10
            ),
        }
        time.sleep(0.7)
    return result


def gtfs_diagnostics() -> dict:
    feeds = {
        "subway_regular": "https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip",
        "bus_manhattan": "https://rrgtfsfeeds.s3.amazonaws.com/gtfs_m.zip",
        "bus_brooklyn": "https://rrgtfsfeeds.s3.amazonaws.com/gtfs_b.zip",
        "bus_queens": "https://rrgtfsfeeds.s3.amazonaws.com/gtfs_q.zip",
    }
    result = {}
    for key, url in feeds.items():
        try:
            r = SESSION.get(url, timeout=60)
            item = {"source": url, "status": r.status_code, "bytes": len(r.content)}
            if r.status_code == 200 and r.content[:2] == b"PK":
                with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
                    names = zf.namelist()
                    item["files"] = names
                    for filename in ("stops.txt", "routes.txt", "calendar.txt", "calendar_dates.txt"):
                        if filename in names:
                            text = zf.read(filename).decode("utf-8-sig", errors="replace")
                            rows = list(csv.DictReader(io.StringIO(text)))
                            item[filename] = {
                                "rows": len(rows),
                                "header": list(rows[0].keys()) if rows else [],
                                "sample": rows[:2],
                            }
                            if filename.startswith("calendar"):
                                dates = [row.get("start_date") or row.get("date") for row in rows if row.get("start_date") or row.get("date")]
                                item["date_min"] = min(dates) if dates else None
                                item["date_max"] = max(dates) if dates else None
                    if "stop_times.txt" in names:
                        sample = zf.read("stop_times.txt")[:800].decode("utf-8-sig", errors="replace")
                        item["stop_times_sample"] = sample
            result[key] = item
        except Exception as exc:
            result[key] = {"source": url, "error": f"{type(exc).__name__}: {exc}"}
        time.sleep(0.5)
    return result


def census_diagnostics() -> dict:
    url = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
    params = {
        "address": "52 West 36th Street, New York, NY 10018",
        "benchmark": "Public_AR_Current",
        "format": "json",
    }
    status, text, final = fetch(url, params)
    item = {"source": final, "status": status, "bytes": len(text)}
    try:
        item["parsed"] = json.loads(text)
    except Exception:
        item["excerpt"] = text[:1600]
    return item


def activity_diagnostics() -> dict:
    urls = {
        "met": "https://www.metmuseum.org/visit/plan-your-visit",
        "moma": "https://www.moma.org/visit",
        "amnh": "https://www.amnh.org/visit",
        "central_park": "https://www.nycgovparks.org/parks/central-park",
        "high_line": "https://www.thehighline.org/visit/",
        "statue_liberty": "https://www.nps.gov/stli/planyourvisit/hours.htm",
        "911_memorial": "https://www.911memorial.org/visit/memorial-and-museum/hours",
        "empire_state": "https://www.esbnyc.com/buy-tickets",
    }
    result = {}
    for key, url in urls.items():
        status, html, final = fetch(url)
        soup = BeautifulSoup(html, "html.parser")
        result[key] = {
            "source": final,
            "status": status,
            "bytes": len(html),
            "title": soup.title.get_text(" ", strip=True) if soup.title else None,
            "snippets": visible_snippets(
                html, r"hours|open daily|closed|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|6 a\.m\.|a\.m\.|p\.m\.", limit=8
            ),
        }
        time.sleep(0.5)
    return result


def main() -> None:
    diagnostics = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "method": "Direct HTTPS GET to official public URLs from a GitHub Actions runner; no values inferred.",
        "hyatt": hyatt_diagnostics(),
        "michelin": michelin_diagnostics(),
        "mta_gtfs": gtfs_diagnostics(),
        "census_geocoder": census_diagnostics(),
        "activities": activity_diagnostics(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(diagnostics, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
    print("=== SUMMARY ===")
    print(json.dumps({
        "hyatt": {k: {"status": v.get("status"), "bytes": v.get("bytes"), "rates": len(v.get("structured_examples", []))} for k, v in diagnostics["hyatt"].items()},
        "michelin": {k: {"status": v.get("status"), "links": v.get("restaurant_links_found")} for k, v in diagnostics["michelin"].items() if k != "individual_pages"},
        "mta_gtfs": {k: {"status": v.get("status"), "bytes": v.get("bytes"), "files": len(v.get("files", []))} for k, v in diagnostics["mta_gtfs"].items()},
    }, indent=2))
    print("=== HYATT STRUCTURED EXAMPLES ===")
    print(json.dumps(diagnostics["hyatt"]["nyczm"]["structured_examples"][:4], indent=2)[:12000])
    print("=== MICHELIN INDIVIDUAL EXAMPLES ===")
    print(json.dumps(diagnostics["michelin"]["individual_pages"]["le_coucou"]["structured_examples"][:4], indent=2)[:12000])
    print("=== MICHELIN CARD EXAMPLE ===")
    print(json.dumps(diagnostics["michelin"]["all_starred"]["card_examples"][:1], indent=2)[:8000])


if __name__ == "__main__":
    main()
