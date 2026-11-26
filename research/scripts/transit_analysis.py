#!/usr/bin/env python3
"""Computed starred-restaurant access for each hotel, from official data only.

Method (recorded verbatim into both output files):
  1. Addresses come from data/hotels.json and data/michelin_all.json. Only
     rows whose address was already captured (33 of 72 starred restaurants)
     are geocoded; rows without a captured address are listed as excluded and
     are NOT counted. No address is inferred.
  2. Addresses are geocoded with the United States Census Bureau batch
     geocoder (https://geocoding.geo.census.gov/geocoder/locations/batch),
     benchmark Public_AR_Current. Unmatched rows are reported, never guessed.
  3. Travel times are computed on the CURRENT official MTA subway GTFS feed
     (https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip). The feed carries
     the schedule in force at capture time; it does NOT describe Feb–Mar 2027
     and is labelled as such everywhere it is published.
     Edge weight = MEDIAN scheduled stop-to-stop running time across all trips
     serving that pair (more representative than the fastest run).
  4. Walks are straight-line haversine distances multiplied by 1.3 (NYC street
     detour factor) at 75 m per minute (4.5 km/h). A 300 s first-boarding
     allowance and 480 s interchange penalty are included. No bus service is
     modelled, so these figures are a SUBWAY-ONLY, walking-included estimate:
     a conservative lower bound for the user's "by subway or bus" rule.
  5. Outputs are labelled computed, dated, and assumption-tagged. They are not
     a 2027 journey-planner guarantee.

Outputs:
  research/generated/transit_analysis.json  (full evidence, kept out of data/)
  data/transit.json                         (site-ready summary + per-row times)
"""
from __future__ import annotations

import csv
import io
import json
import math
import os
import re
import statistics
import sys
import zipfile
from datetime import datetime, timezone
from heapq import heappop, heappush
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
GEN = ROOT / "research" / "generated"
GEN.mkdir(parents=True, exist_ok=True)

GTFS_URL = "https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip"
CENSUS_BATCH = "https://geocoding.geo.census.gov/geocoder/locations/batch?benchmark=Public_AR_Current"
CENSUS_SINGLE = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"

WALK_M_PER_MIN = 75.0
CURVE = 1.3
BOARD_SECONDS = 300
TRANSFER_SECONDS = 480
EDGE_MAX_SECONDS = 3600
ORIGIN_STATION_CAP = 6
WALK_CAPTURE_M = 2500.0

GENERATED_AT = datetime.now(timezone.utc).isoformat(timespec="seconds")


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def walk_seconds(metres: float) -> float:
    return metres * CURVE / WALK_M_PER_MIN * 60.0


def parse_gtfs_time(value: str) -> int | None:
    m = re.match(r"^(\d{1,3}):(\d{2}):(\d{2})$", value.strip())
    if not m:
        return None
    h, mi, s = (int(g) for g in m.groups())
    return h * 3600 + mi * 60 + s


def split_address(addr: str):
    m = re.match(r"^(.*),\s*([A-Za-z][A-Za-z .]*),\s*([A-Z]{2})\s+(\d{5})(?:-\d{4})?\s*$", addr.strip())
    if not m:
        return None
    street, city, state, zip_ = (g.strip() for g in m.groups())
    return street, city, state, zip_


def census_batch(addresses: list[tuple[str, str]]) -> dict[str, dict]:
    """addresses: list of (id, one_line_address). Returns {id: match dict}."""
    buf = io.StringIO()
    w = csv.writer(buf)
    for ident, addr in addresses:
        parts = split_address(addr)
        if parts:
            street, city, state, zip_ = parts
        else:
            street, city, state, zip_ = addr.strip(), "", "", ""
        w.writerow([ident, street, city, state, zip_])
    files = {"addressFile": ("addresses.csv", buf.getvalue(), "text/csv")}
    try:
        resp = requests.post(CENSUS_BATCH, files=files, timeout=120)
        resp.raise_for_status()
    except Exception as e:
        print(f"census batch failed: {e}; falling back to single-address lookups", flush=True)
        return census_single(addresses)
    out = {}
    rows = list(csv.reader(io.StringIO(resp.text)))
    if not rows:
        return census_single(addresses)
    header = [h.strip().lower().replace(" ", "_") for h in rows[0]]
    def col(name):
        for i, h in enumerate(header):
            if h == name:
                return i
        for i, h in enumerate(header):
            if name in h:
                return i
        return None
    i_id, i_match = col("id"), col("match")
    i_lon, i_lat = col("longitude"), col("latitude")
    i_out = col("output_address")
    if i_id is None or i_match is None or i_lon is None or i_lat is None:
        print("census batch: unexpected columns; falling back to single-address lookups", flush=True)
        return census_single(addresses)
    for row in rows[1:]:
        if len(row) <= max(i_id, i_match, i_lon, i_lat):
            continue
        ident = row[i_id].strip()
        match = row[i_match].strip()
        rec = {"input": ident, "match": match, "output_address": row[i_out].strip() if i_out is not None else ""}
        if match.lower().startswith("match"):
            try:
                rec["lon"] = float(row[i_lon])
                rec["lat"] = float(row[i_lat])
            except ValueError:
                rec["match"] = "Match(parse error)"
        out[ident] = rec
    unmatched = [ident for ident, rec in out.items() if "lat" not in rec]
    if unmatched:
        print(f"batch unmatched {unmatched}; retrying single-address lookups", flush=True)
        retry = census_single([(ident, addr) for ident, addr in addresses if ident in set(unmatched)])
        for ident, rec in retry.items():
            if "lat" in rec:
                out[ident] = rec
    return out


def census_single(addresses: list[tuple[str, str]]) -> dict[str, dict]:
    out = {}
    for ident, addr in addresses:
        try:
            resp = requests.get(
                CENSUS_SINGLE,
                params={"address": addr, "benchmark": "Public_AR_Current", "format": "json"},
                timeout=60,
            )
            resp.raise_for_status()
            matches = resp.json().get("result", {}).get("addressMatches", [])
            if not matches:
                cleaned = addr.replace(".", "")
                if cleaned != addr:
                    resp = requests.get(
                        CENSUS_SINGLE,
                        params={"address": cleaned, "benchmark": "Public_AR_Current", "format": "json"},
                        timeout=60,
                    )
                    resp.raise_for_status()
                    matches = resp.json().get("result", {}).get("addressMatches", [])
            if matches:
                c = matches[0]["coordinates"]
                out[ident] = {
                    "input": ident,
                    "match": "Match",
                    "output_address": matches[0].get("matchedAddress", ""),
                    "lon": c["x"],
                    "lat": c["y"],
                }
            else:
                out[ident] = {"input": ident, "match": "No_Match", "output_address": ""}
        except Exception as e:
            out[ident] = {"input": ident, "match": f"error: {e}", "output_address": ""}
    return out


def main() -> int:
    hotels = json.loads((DATA / "hotels.json").read_text())["hotels"]
    restaurants = json.loads((DATA / "michelin_all.json").read_text())["restaurants"]

    targets = []  # (id, kind, name, address)
    for h in hotels:
        targets.append((f"hotel:{h['id']}", "hotel", h["name"], h["address"]))
    excluded_restaurants = []
    for i, r in enumerate(restaurants):
        addr = (r.get("address") or "").strip()
        if addr:
            targets.append((f"rest:{i}", "restaurant", r["name"], addr))
        else:
            excluded_restaurants.append({"name": r["name"], "stars": r["stars"], "reason": "address not captured in data/michelin_all.json"})

    print(f"geocoding {len(targets)} addresses ({len(excluded_restaurants)} restaurants excluded: no captured address)", flush=True)
    geo = census_batch([(t[0], t[3]) for t in targets])

    print(f"downloading GTFS from {GTFS_URL}", flush=True)
    gtfs_bytes = requests.get(GTFS_URL, timeout=180).content
    print(f"gtfs bytes: {len(gtfs_bytes)}", flush=True)

    with zipfile.ZipFile(io.BytesIO(gtfs_bytes)) as zf:
        names = set(zf.namelist())
        needed = {"stops.txt", "trips.txt", "stop_times.txt"}
        missing = needed - names
        if missing:
            print(f"GTFS missing {missing}", file=sys.stderr)
            return 2
        with zf.open("stops.txt") as fh:
            raw_stops = list(csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8-sig")))
        with zf.open("trips.txt") as fh:
            raw_trips = list(csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8-sig")))
        with zf.open("stop_times.txt") as fh:
            raw_times = list(csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8-sig")))

    station_of: dict[str, str] = {}
    stations: dict[str, dict] = {}
    for row in raw_stops:
        sid = (row.get("stop_id") or "").strip()
        parent = (row.get("parent_station") or "").strip()
        station_of[sid] = parent if parent else sid
        if (row.get("location_type") or "").strip() == "1":
            try:
                stations[sid] = {
                    "name": (row.get("stop_name") or "").strip(),
                    "lat": float(row["stop_lat"]),
                    "lon": float(row["stop_lon"]),
                }
            except (ValueError, KeyError):
                pass
    # Ensure every referenced station exists (fall back to child coords).
    for row in raw_stops:
        sid = (row.get("stop_id") or "").strip()
        st = station_of[sid]
        if st not in stations:
            try:
                stations[st] = {
                    "name": (row.get("stop_name") or "").strip(),
                    "lat": float(row["stop_lat"]),
                    "lon": float(row["stop_lon"]),
                }
            except (ValueError, KeyError):
                pass

    trip_route = {(t.get("trip_id") or "").strip(): (t.get("route_id") or "").strip() for t in raw_trips}

    per_trip: dict[str, list[tuple[int, str, int]]] = {}
    for row in raw_times:
        trip = (row.get("trip_id") or "").strip()
        try:
            seq = int(row.get("stop_sequence") or 0)
        except ValueError:
            continue
        station = station_of.get((row.get("stop_id") or "").strip())
        dep = parse_gtfs_time(row.get("departure_time") or row.get("arrival_time") or "")
        if station is None or dep is None:
            continue
        per_trip.setdefault(trip, []).append((seq, station, dep))

    edge_samples: dict[tuple[str, str, str], list[int]] = {}
    for trip, rows in per_trip.items():
        route = trip_route.get(trip)
        if not route:
            continue
        rows.sort(key=lambda r: r[0])
        for (s0, st0, t0), (s1, st1, t1) in zip(rows, rows[1:]):
            delta = t1 - t0
            if 0 < delta <= EDGE_MAX_SECONDS and st0 != st1:
                edge_samples.setdefault((st0, st1, route), []).append(delta)

    edge_median = {(u, v, r): statistics.median(samples) for (u, v, r), samples in edge_samples.items()}
    adj: dict[str, list[tuple[str, float, str]]] = {}
    routes_at_station: dict[str, set[str]] = {}
    for (u, v, r), w in edge_median.items():
        adj.setdefault(u, []).append((v, w, r))
        routes_at_station.setdefault(u, set()).add(r)
        routes_at_station.setdefault(v, set()).add(r)
    print(f"stations={len(stations)} trips={len(per_trip)} directed edges={len(edge_median)}", flush=True)

    def nearest_stations(lat: float, lon: float, cap: int = ORIGIN_STATION_CAP):
        arr = []
        for sid, s in stations.items():
            d = haversine_m(lat, lon, s["lat"], s["lon"])
            if d <= WALK_CAPTURE_M:
                arr.append((d, sid))
        arr.sort(key=lambda x: x[0])
        return arr[:cap]

    def route_from(hotel_lat: float, hotel_lon: float):
        origins = nearest_stations(hotel_lat, hotel_lon)
        dist: dict[tuple[str, str | None], float] = {}
        heap: list[tuple[float, str, str | None]] = []
        for d, sid in origins:
            key = (sid, None)
            dist[key] = walk_seconds(d)
            heappush(heap, (dist[key], sid, None))
        while heap:
            cost, station, route = heappop(heap)
            if cost > dist.get((station, route), float("inf")):
                continue
            for v, w, route2 in adj.get(station, ()):
                if route is None:
                    nroute, ncost = route2, cost + BOARD_SECONDS + w
                elif route2 == route:
                    nroute, ncost = route2, cost + w
                else:
                    continue
                key = (v, nroute)
                if ncost < dist.get(key, float("inf")):
                    dist[key] = ncost
                    heappush(heap, (ncost, v, nroute))
            if route is not None:
                for r2 in routes_at_station.get(station, ()):
                    if r2 == route:
                        continue
                    key = (station, r2)
                    ncost = cost + TRANSFER_SECONDS
                    if ncost < dist.get(key, float("inf")):
                        dist[key] = ncost
                        heappush(heap, (ncost, station, r2))
        best: dict[str, float] = {}
        for (station, route), cost in dist.items():
            if station not in best or cost < best[station]:
                best[station] = cost
        return best

    geo_rows = geo
    def coords_for(ident):
        rec = geo_rows.get(ident) or {}
        if "lat" in rec:
            return rec["lat"], rec["lon"], rec
        return None, None, rec

    hotel_reports = []
    for h in hotels:
        ident = f"hotel:{h['id']}"
        lat, lon, rec = coords_for(ident)
        if lat is None:
            hotel_reports.append({"id": h["id"], "name": h["name"], "address": h["address"], "geocode": rec, "error": "geocode failed", "entries": [], "counts": None})
            continue
        best = route_from(lat, lon)
        entries = []
        for i, r in enumerate(restaurants):
            rid = f"rest:{i}"
            addr = (r.get("address") or "").strip()
            if not addr:
                entries.append({"name": r["name"], "stars": r["stars"], "reachable": None, "reason": "address not captured", "michelin_url": r.get("michelin_url", "")})
                continue
            rlat, rlon, rrec = coords_for(rid)
            if rlat is None:
                entries.append({"name": r["name"], "stars": r["stars"], "reachable": None, "reason": f"geocode {rrec.get('match', 'failed')}", "michelin_url": r.get("michelin_url", "")})
                continue
            straight = haversine_m(lat, lon, rlat, rlon)
            if straight > 25000:
                entries.append({
                    "name": r["name"], "stars": r["stars"], "cluster": r.get("cluster") or "",
                    "straight_line_km": round(straight / 1000.0, 2),
                    "reachable": False, "minutes": None,
                    "reason": "beyond subway service area (straight-line > 25 km); Metro-North or drive required, not modelled",
                    "michelin_url": r.get("michelin_url", ""), "official_site": r.get("official_site", ""),
                })
                continue
            best_total, best_station, best_walk = None, None, None
            for sid, s in stations.items():
                arr = best.get(sid)
                if arr is None:
                    continue
                wsec = walk_seconds(haversine_m(rlat, rlon, s["lat"], s["lon"]))
                total = arr + wsec
                if best_total is None or total < best_total:
                    best_total, best_station, best_walk = total, sid, wsec
            entry = {
                "name": r["name"],
                "stars": r["stars"],
                "cluster": r.get("cluster") or "",
                "straight_line_km": round(straight / 1000.0, 2),
                "michelin_url": r.get("michelin_url", ""),
                "official_site": r.get("official_site", ""),
            }
            if best_total is None:
                entry.update({"reachable": False, "minutes": None, "reason": "no connected subway path found (feed/geometry) or beyond walk capture"})
            else:
                entry.update({
                    "reachable": True,
                    "minutes": round(best_total / 60.0, 1),
                    "entry_station": stations[best_station]["name"],
                    "egress_walk_minutes": round(best_walk / 60.0, 1),
                })
            entries.append(entry)
        counts = {}
        for label, cap in (("reachable_60", 3600.0), ("reachable_45", 2700.0), ("reachable_30", 1800.0)):
            c = {"three_star": 0, "two_star": 0, "one_star": 0, "total": 0}
            for e in entries:
                if e.get("reachable") and e.get("minutes") is not None and e["minutes"] <= cap / 60.0:
                    key = {3: "three_star", 2: "two_star", 1: "one_star"}[e["stars"]]
                    c[key] += 1
                    c["total"] += 1
            counts[label] = c
        hotel_reports.append({
            "id": h["id"],
            "name": h["name"],
            "address": h["address"],
            "lat": lat,
            "lon": lon,
            "geocode": rec,
            "entries": entries,
            "counts": counts,
            "counts_60_address_known_denominator": sum(1 for e in entries if e.get("reachable") is not None),
        })
        print(f"{h['name']}: 60-min starred reach = {counts['reachable_60']}", flush=True)

    ranked = [r for r in hotel_reports if r.get("counts")]
    ranked.sort(key=lambda r: (-r["counts"]["reachable_60"]["total"], -r["counts"]["reachable_45"]["total"], -r["counts"]["reachable_30"]["total"], r["id"]))
    for i, r in enumerate(ranked, 1):
        r["rank"] = i

    method = {
        "gtfs_url": GTFS_URL,
        "census_batch_url": CENSUS_BATCH,
        "edge_weight": "median scheduled stop-to-stop running time across trips in the current GTFS feed",
        "walk_model": f"haversine x {CURVE} street-detour factor at {int(WALK_M_PER_MIN)} m/min",
        "first_boarding_seconds": BOARD_SECONDS,
        "interchange_penalty_seconds": TRANSFER_SECONDS,
        "bus_included": False,
        "calendar_note": "GTFS in force at capture time; it does NOT describe Feb-Mar 2027 and must not be read as a 2027 timetable.",
        "excluded": "starred restaurants whose street address was not captured in data/michelin_all.json (see excluded_restaurants); no address was inferred",
    }

    full = {
        "generated_at_utc": GENERATED_AT,
        "method": method,
        "excluded_restaurants": excluded_restaurants,
        "geocodes": {k: v for k, v in geo_rows.items()},
        "stations": len(stations),
        "directed_edges": len(edge_median),
        "hotels": hotel_reports,
    }
    (GEN / "transit_analysis.json").write_text(json.dumps(full, indent=1, ensure_ascii=False))

    site = {
        "_meta": {
            "generated": GENERATED_AT[:10],
            "generated_at_utc": GENERATED_AT,
            "title": "Computed subway access to starred restaurants",
            "method": method,
            "caveat": "Computed from the CURRENT MTA subway GTFS feed (median scheduled running times, walking included). This is not a Feb-Mar 2027 timetable, includes no bus service, and covers only the starred restaurants whose street address was captured. Treat as a comparative ranking, not a journey promise.",
            "sources": [
                {"label": "MTA subway GTFS feed (official, current)", "url": GTFS_URL},
                {"label": "MTA developer resources / GTFS", "url": "https://www.mta.info/developers"},
                {"label": "US Census Bureau batch geocoder (benchmark Public_AR_Current)", "url": CENSUS_BATCH},
                {"label": "Full evidence and geocode ledger", "url": "research/generated/transit_analysis.json"},
            ],
            "address_coverage": f"{len(restaurants) - len(excluded_restaurants)} of {len(restaurants)} starred restaurants have a captured street address and are included; {len(excluded_restaurants)} do not and are excluded rather than guessed.",
        },
        "excluded_restaurants": excluded_restaurants,
        "hotels": [
            {
                "id": r["id"],
                "name": r["name"],
                "address": r["address"],
                "rank": r.get("rank"),
                "counts": r.get("counts"),
                "counts_60_address_known_denominator": r.get("counts_60_address_known_denominator"),
                "entries": [
                    {k: e.get(k) for k in ("name", "stars", "cluster", "minutes", "entry_station", "egress_walk_minutes", "straight_line_km", "michelin_url", "official_site", "reachable", "reason")}
                    for e in r["entries"]
                ],
            }
            for r in sorted(hotel_reports, key=lambda r: (r.get("rank") or 99))
        ],
    }
    (DATA / "transit.json").write_text(json.dumps(site, indent=1, ensure_ascii=False))
    print(f"wrote research/generated/transit_analysis.json and data/transit.json", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
