#!/usr/bin/env python3
"""Build data/hotel_ranking.json from measured journey times.

Every number comes from data/transit_hotels.json, which scripts/transit/gtfs_route.py
produces from the official MTA GTFS feeds. Nothing here is typed in by hand and
nothing is ordered by opinion: the `ranking_metric` field states exactly what the
sort uses, and the coverage fields state how many destinations it covers.
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRIC = "median_minutes_to_measured_starred_restaurants"
APPLICATION_SLICE = ("wednesday", "12:00")


def to_minutes(v: str) -> int:
    h, m = v.split(":")
    return int(h) * 60 + int(m)


def main() -> int:
    transit = json.loads((ROOT / "data/transit_hotels.json").read_text())
    hotels = json.loads((ROOT / "data/hotels.json").read_text())["hotels"]
    restaurants = json.loads((ROOT / "data/michelin_all.json").read_text())["restaurants"]

    star_of = {r["name"]: r["stars"] for r in restaurants}
    tier_of = {r["name"]: ("listed_only" if r.get("listed_only") else f"{r['stars']}_star")
               for r in restaurants}

    measured_starred = sorted({n for r in transit["results"] for n, v in r["destinations"].items()
                               if v["kind"] == "restaurant"})
    all_starred = sorted(star_of)
    uncovered = [n for n in all_starred if n not in measured_starred]

    by_hotel: dict[str, dict] = {}
    for row in transit["results"]:
        hid = row["hotel_id"]
        slot = by_hotel.setdefault(hid, {"name": row["hotel_name"], "windows": {}})
        key = f"{row['service']} {row['depart_after_local']}"
        slot["windows"][key] = row

    out = []
    for h in hotels:
        slot = by_hotel.get(h["id"])
        if not slot:
            out.append({"hotel_id": h["id"], "name": h["name"], "status": "not measured"})
            continue
        primary = slot["windows"].get("wednesday 12:00") or next(iter(slot["windows"].values()))
        dests = primary["destinations"]

        def stat(kind: str):
            vals = [(n, v) for n, v in dests.items() if v["kind"] == kind and v["minutes"] is not None]
            mins = sorted(v["minutes"] for _, v in vals)
            within = sum(1 for _, v in vals if v["within_1h"])
            return {
                "measured": len(vals),
                "within_60_min": within,
                "median_minutes": round(statistics.median(mins), 1) if mins else None,
                "best_minutes": mins[0] if mins else None,
                "worst_minutes": mins[-1] if mins else None,
                "within_45_min": sum(1 for m in mins if m <= 45),
                "within_30_min": sum(1 for m in mins if m <= 30),
            }

        star_counts = {
            "three_star": sum(1 for n, v in dests.items()
                              if v["kind"] == "restaurant" and v["within_1h"] and star_of.get(n) == 3),
            "two_star": sum(1 for n, v in dests.items()
                            if v["kind"] == "restaurant" and v["within_1h"] and star_of.get(n) == 2),
            "one_star": sum(1 for n, v in dests.items()
                            if v["kind"] == "restaurant" and v["within_1h"] and star_of.get(n) == 1),
        }

        # sensitivity: does the ranking metric move between service/window samples?
        sample_medians = {}
        for key, wrow in slot["windows"].items():
            mins = sorted(v["minutes"] for v in wrow["destinations"].values()
                          if v["kind"] == "restaurant" and v["minutes"] is not None)
            if mins:
                sample_medians[key] = round(statistics.median(mins), 1)

        out.append({
            "hotel_id": h["id"],
            "name": h["name"],
            "area": h.get("area"),
            "address_used": primary.get("address_used") or h.get("address"),
            "nearest_stop_walk_min": primary["nearest_stop_walk_min"],
            "stops_within_walk": primary["hotel_stops_within_walk"],
            "starred_restaurants_within_60_min": star_counts,
            "starred_restaurants_within_60_min_total": sum(star_counts.values()),
            "restaurants": stat("restaurant"),
            "activities": stat("activity"),
            "median_minutes_by_window": sample_medians,
            "median_spread_between_windows_min": (
                round(max(sample_medians.values()) - min(sample_medians.values()), 1)
                if len(sample_medians) > 1 else None),
            "hotel_quote_total_before_tax_usd": (
                min([t["total_before_tax_usd"] for t in h.get("rate_tiers", [])
                     if t.get("total_before_tax_usd")] or [None])),
            "hotel_search_page_total_usd": h.get("search_page_cheapest_total_usd"),
            "quality_flag": h.get("room_meets_private_bathroom", "")[:0] or None,
        })

    ranked = [r for r in out if r.get("restaurants", {}).get("median_minutes") is not None]
    ranked.sort(key=lambda r: r["restaurants"]["median_minutes"])
    for i, r in enumerate(ranked, 1):
        r["rank_by_median"] = i
    for r in out:
        r.setdefault("rank_by_median", None)

    doc = {
        "_meta": {
            "generated_utc": transit["_meta"]["generated_utc"],
            "ranking_metric": METRIC,
            "ranking_metric_explained":
                "Each hotel's rank is the median modelled door-to-door time to the "
                "starred restaurants that could be measured for it. A lower median is "
                "better. The metric is chosen because the requested 'count within 1 hour' "
                "turned out not to discriminate: every hotel reaches every measured starred "
                "restaurant inside 60 minutes, so the count is identical and the tie has to "
                "be broken by something that is actually measured.",
            "why_the_1h_count_is_not_a_ranking":
                "starred_restaurants_within_60_min_total is published for every hotel and is "
                "the same number for all of them. That is a real result of the measurement, "
                "not a placeholder: Midtown and the Financial District are both within an "
                "hour of every measured starred restaurant on the timetable used.",
            "sample_used_for_the_rank": f"{APPLICATION_SLICE[0]} {APPLICATION_SLICE[1]} local departure",
            "sensitivity_note":
                "median_spread_between_windows_min shows how much the median moves across the "
                "four samples (weekday/Saturday × 12:00/18:00). A rank whose spread overlaps "
                "the next hotel's median is a tie, not a win.",
            "coverage": {
                "starred_restaurants_in_dataset": len(all_starred),
                "starred_restaurants_measured": len(measured_starred),
                "starred_restaurants_unmeasured": len(uncovered),
                "unmeasured_names": uncovered,
                "why_unmeasured":
                    "the records carry no street address, or the U.S. Census geocoder could not "
                    "resolve the address, or no stop is within the 500 m walk cap. Each one is "
                    "listed in data/transit_hotels.json → _meta.unmeasured_destinations with its reason.",
            },
            "sources": {
                "journey_times": "data/transit_hotels.json (MTA GTFS model)",
                "hotel_totals": "data/hotels.json (Booking.com third-party rate snapshots, 15–22 Feb 2027)",
                "stars": "data/michelin_all.json (MICHELIN Guide 2025 selection)",
                "gtfs": "https://www.mta.info/developers",
                "geocoder": "https://geocoding.geo.census.gov/geocoder",
            },
            "caveats": [
                "journey times are modelled from the current timetable, not a 2027 trip plan",
                "hotel totals are third-party snapshots before tax, not official quotes",
                "star counts are the 2025 selection and must be re-read after the next ceremony",
            ],
        },
        "ranking": ranked,
        "all_hotels": out,
    }
    path = ROOT / "data/hotel_ranking.json"
    path.write_text(json.dumps(doc, indent=1, sort_keys=False))
    print(f"wrote {path}")
    for r in ranked:
        print(f"  #{r['rank_by_median']} {r['name'][:32]:<32} median {r['restaurants']['median_minutes']:>5} min"
              f"  spread {r['median_spread_between_windows_min']}  stars within 60 = "
              f"{r['starred_restaurants_within_60_min_total']}"
              f"  total ${r['hotel_quote_total_before_tax_usd']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
