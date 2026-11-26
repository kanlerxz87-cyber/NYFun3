#!/usr/bin/env python3
"""Measure how long it actually takes to get from each candidate hotel to each
starred restaurant and each activity, using only official data.

Everything that is a *fact* comes from a downloaded official file:
  * MTA static GTFS feeds (https://www.mta.info/developers)
  * U.S. Census Bureau geocoder (https://geocoding.geo.census.gov/geocoder)
  * the street addresses already stored in this repo's data files

Everything that is an *assumption* is listed in ASSUMPTIONS and repeated in
the output file and on the website. The journey time is a modelled estimate
computed by this script, not an MTA-published door-to-door time.

Usage:  python3 scripts/transit/gtfs_route.py [--out data/transit_hotels.json]
"""
from __future__ import annotations

import argparse
import bisect
import csv
import datetime as dt
import io
import json
import math
import re
import sys
import urllib.parse
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "scripts" / "transit" / ".cache"

FEEDS = {
    "subway": "https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip",
    "bus_manhattan": "https://rrgtfsfeeds.s3.amazonaws.com/gtfs_m.zip",
    "bus_brooklyn": "https://rrgtfsfeeds.s3.amazonaws.com/gtfs_b.zip",
}

WALK_M_PER_MIN = 80.0          # 4.8 km/h
MAX_WALK_M = 500.0             # door -> stop, and stop -> door
TRANSFER_WALK_M = 400.0        # stop -> different stop on foot
TRANSFER_MIN = 3.0             # allowance inside one station complex
SEARCH_WINDOW_MIN = 110
REPORT_LIMIT_MIN = 60
MAX_PASSES = 4                 # walk-transfer relaxation passes
DEPARTURE_WINDOWS = ["12:00", "18:00"]

# packed-int field widths (bits): dep_time | dep_group | arr_group | arr_time | trip
W_TIME, W_GROUP, W_ARR, W_TRIP = 17, 15, 15, 18
SHIFT_TRIP = 0
SHIFT_ARRTIME = W_TRIP
SHIFT_ARRGROUP = SHIFT_ARRTIME + W_TIME
SHIFT_DEPGROUP = SHIFT_ARRGROUP + W_GROUP
SHIFT_DEPTIME = SHIFT_DEPGROUP + W_GROUP
MASK = (1 << W_TIME) - 1

ASSUMPTIONS = {
    "walk_speed_m_per_min": WALK_M_PER_MIN,
    "walk_speed_kmh": round(WALK_M_PER_MIN * 60 / 1000, 2),
    "max_walk_door_to_stop_m": MAX_WALK_M,
    "max_walk_between_stops_m": TRANSFER_WALK_M,
    "station_transfer_allowance_min": TRANSFER_MIN,
    "search_window_min": SEARCH_WINDOW_MIN,
    "report_limit_min": REPORT_LIMIT_MIN,
    "departure_windows_local_time": DEPARTURE_WINDOWS,
    "algorithm": "Connection Scan Algorithm (multi-pass, with walking transfers)",
}


def log(*a):
    print(*a, flush=True)


# --------------------------------------------------------------------- fetch
def fetch(url: str, dest: Path) -> Path:
    if dest.exists() and dest.stat().st_size > 0:
        log(f"  cached {dest.name} ({dest.stat().st_size:,} bytes)")
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "NYFun3-trip-planner/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r, open(dest, "wb") as f:
        f.write(r.read())
    log(f"  downloaded {dest.name} ({dest.stat().st_size:,} bytes)")
    return dest


def hms(text: str) -> int:
    h, m, s = text.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def haversine_m(lat1, lon1, lat2, lon2) -> float:
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def walk_minutes(meters: float) -> float:
    return meters / WALK_M_PER_MIN


# ---------------------------------------------------------------- parse feeds
def read_feed(zip_path: Path, tag: str, group_ids: dict[str, int], stops_xy: dict[int, tuple[float, float]],
              trip_ids: dict[str, int], trip_service: list[str], packed: list[int]):
    """Stream one GTFS zip into the shared, compact structures."""
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
        stop_group: dict[str, int] = {}
        with zf.open("stops.txt") as fh:
            for row in csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8-sig", newline="")):
                try:
                    lat, lon = float(row["stop_lat"]), float(row["stop_lon"])
                except (KeyError, ValueError):
                    continue
                # Group platforms that share a parent station: a passenger can
                # walk between them without leaving the paid area.
                parent = (row.get("parent_station") or "").strip()
                key = f"{tag}:{parent}" if parent else f"{tag}:{row['stop_id']}"
                gid = group_ids.get(key)
                if gid is None:
                    gid = len(group_ids)
                    group_ids[key] = gid
                    stops_xy[gid] = (lat, lon)
                stop_group[row["stop_id"]] = gid
        with zf.open("trips.txt") as fh:
            for row in csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8-sig", newline="")):
                key = f"{tag}:{row['trip_id']}"
                if key not in trip_ids:
                    trip_ids[key] = len(trip_service)
                    trip_service.append(f"{tag}:{row.get('service_id', '')}")
        if "calendar.txt" in names:
            with zf.open("calendar.txt") as fh:
                for row in csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8-sig", newline="")):
                    CALENDAR[f"{tag}:{row['service_id']}"] = row
        if "calendar_dates.txt" in names:
            with zf.open("calendar_dates.txt") as fh:
                for row in csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8-sig", newline="")):
                    CAL_DATES[f"{tag}:{row['service_id']}"].append(
                        (row.get("date", ""), row.get("exception_type", "")))

        rows = 0
        prev_trip = None
        prev_group = None
        prev_arr = 0
        backwards = 0
        with zf.open("stop_times.txt") as fh:
            for row in csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8-sig", newline="")):
                rows += 1
                trip = row["trip_id"]
                try:
                    arr = hms(row["arrival_time"])
                    dep = hms(row["departure_time"])
                except (KeyError, ValueError):
                    arr = dep = None
                gid = stop_group.get(row["stop_id"])
                if gid is None or arr is None:
                    continue
                if trip != prev_trip:
                    prev_trip, prev_group, prev_arr = trip, gid, arr
                    continue
                # stops within one trip can repeat a group (loop routes); a
                # repeated group with no forward movement is not a boarding
                # opportunity, so it is skipped rather than counted.
                if gid == prev_group:
                    prev_arr = arr
                    continue
                if arr < prev_arr:
                    backwards += 1
                    prev_group, prev_arr = gid, arr
                    continue
                ti = trip_ids[f"{tag}:{trip}"]
                packed.append(
                    ((((prev_arr << W_GROUP) | prev_group) << W_GROUP | gid)
                     << W_TIME | arr) << W_TRIP | ti)
                prev_group, prev_arr = gid, arr
    log(f"  {tag}: {rows:,} stop_times rows, {len(stop_group):,} stops, "
        f"{len([t for t in trip_ids if t.startswith(tag + ':')]):,} trips, "
        f"{backwards} out-of-order rows skipped")


CALENDAR: dict[str, dict] = {}
CAL_DATES: dict[str, list] = defaultdict(list)


def active_services(date_str: str) -> set[str]:
    d = dt.datetime.strptime(date_str, "%Y%m%d").date()
    flags = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    active = set()
    for sid, row in CALENDAR.items():
        try:
            if row["start_date"] <= date_str <= row["end_date"] and row.get(flags[d.weekday()]) == "1":
                active.add(sid)
        except KeyError:
            continue
    for sid, exceptions in CAL_DATES.items():
        for date, kind in exceptions:
            if date == date_str:
                if kind == "1":
                    active.add(sid)
                elif kind == "2":
                    active.discard(sid)
    return active


def pick_service_dates() -> tuple[str, str, dict]:
    """First Wednesday and first Saturday inside the subway feed's range."""
    best = None
    for sid, row in CALENDAR.items():
        if not sid.startswith("subway:"):
            continue
        try:
            start = dt.datetime.strptime(row["start_date"], "%Y%m%d").date()
            end = dt.datetime.strptime(row["end_date"], "%Y%m%d").date()
        except (KeyError, ValueError):
            continue
        if best is None or start < best[0]:
            best = (start, end)
    if not best:
        today = dt.date.today()
        return "20260101", "20260103", {}
    start, end = best
    wed = start + dt.timedelta(days=(2 - start.weekday()) % 7)
    sat = start + dt.timedelta(days=(5 - start.weekday()) % 7)
    if wed > end:
        wed = end
    if sat > end:
        sat = end
    info = {"feed_first_date": start.isoformat(), "feed_last_date": end.isoformat()}
    return wed.strftime("%Y%m%d"), sat.strftime("%Y%m%d"), info


# -------------------------------------------------------------- walk network
def build_walk_links(stops_xy: dict[int, tuple[float, float]], radius_m: float):
    cells = defaultdict(list)
    for gid, (lat, lon) in stops_xy.items():
        cells[(int(lat * 1000 // 100), int(lon * 1000 // 100))].append(gid)
    links: dict[int, list[tuple[int, float]]] = {}
    for gid, (lat, lon) in stops_xy.items():
        cy, cx = int(lat * 1000 // 100), int(lon * 1000 // 100)
        out = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                for other in cells.get((cy + dy, cx + dx), ()):
                    if other == gid:
                        continue
                    o = stops_xy[other]
                    d = haversine_m(lat, lon, o[0], o[1])
                    if d <= radius_m:
                        out.append((other, walk_minutes(d)))
        if out:
            links[gid] = out
    return links


def stops_near(stops_xy, cells, lat, lon, max_m):
    out = {}
    cy, cx = int(lat * 1000 // 100), int(lon * 1000 // 100)
    for dy in (-2, -1, 0, 1, 2):
        for dx in (-2, -1, 0, 1, 2):
            for gid in cells.get((cy + dy, cx + dx), ()):
                o = stops_xy[gid]
                d = haversine_m(lat, lon, o[0], o[1])
                if d <= max_m:
                    out[gid] = walk_minutes(d)
    return out


# ------------------------------------------------------------------- routing
class Router:
    def __init__(self, packed: list[int], stops_xy, walk_links, n_groups: int):
        self.packed = packed
        self.stops_xy = stops_xy
        self.walk_links = walk_links
        self.n = n_groups
        self.dep_times = [p >> (W_TIME + W_GROUP + W_GROUP + W_TRIP) for p in packed]

    def route(self, origin_walks: dict[int, float], start_sec: int, limit_min: int):
        INF = 1 << 30
        ready = [INF] * self.n
        arrival = [INF] * self.n
        for gid, minutes in origin_walks.items():
            t = start_sec + int(round(minutes * 60))
            if t < ready[gid]:
                ready[gid] = t
                arrival[gid] = t
        deadline = start_sec + limit_min * 60
        start_idx = bisect.bisect_left(self.dep_times, start_sec)
        transfer = int(TRANSFER_MIN * 60)
        packed = self.packed
        for _pass in range(MAX_PASSES):
            improved = False
            onboard_trip = -1
            onboard_stop = -1
            onboard_arr = INF
            for idx in range(start_idx, len(packed)):
                p = packed[idx]
                dep_time = p >> (W_TIME + W_GROUP + W_GROUP + W_TRIP)
                if dep_time > deadline:
                    break
                dep_group = (p >> (W_GROUP + W_TIME + W_TRIP)) & ((1 << W_GROUP) - 1)
                arr_group = (p >> (W_TIME + W_TRIP)) & ((1 << W_GROUP) - 1)
                arr_time = (p >> W_TRIP) & MASK
                trip = p & ((1 << W_TRIP) - 1)
                boarded = False
                if trip == onboard_trip and onboard_stop == dep_group and onboard_arr <= dep_time:
                    boarded = True
                elif ready[dep_group] <= dep_time:
                    boarded = True
                elif _pass > 0:
                    # walking transfer into this stop during a later pass
                    if ready[dep_group] <= dep_time:
                        boarded = True
                if not boarded:
                    continue
                onboard_trip, onboard_stop, onboard_arr = trip, arr_group, arr_time
                if arr_time < arrival[arr_group]:
                    arrival[arr_group] = arr_time
                    improved = True
                cand = arr_time + transfer
                if cand < ready[arr_group]:
                    ready[arr_group] = cand
                    improved = True
                start_idx = max(start_idx, bisect.bisect_left(self.dep_times, start_sec))
            # relax walking transfers between nearby stops/stations
            walk_changed = False
            for gid, links in self.walk_links.items():
                if arrival[gid] >= INF:
                    continue
                for other, minutes in links:
                    cand = arrival[gid] + int(round(minutes * 60))
                    if cand < ready[other] and cand < arrival[other]:
                        ready[other] = cand
                        arrival[other] = cand
                        walk_changed = True
            if not improved and not walk_changed:
                break
        return arrival, deadline


# ---------------------------------------------------------------- geocoding
GEOCODE_CACHE = ROOT / "data" / "geocode_cache.json"


def load_cache() -> dict:
    return json.loads(GEOCODE_CACHE.read_text()) if GEOCODE_CACHE.exists() else {}


def save_cache(cache: dict) -> None:
    GEOCODE_CACHE.parent.mkdir(parents=True, exist_ok=True)
    GEOCODE_CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True))


def geocode(address: str, cache: dict) -> dict | None:
    if address in cache:
        return cache[address]
    q = urllib.parse.urlencode({"address": address, "benchmark": "Public_AR_Current", "format": "json"})
    url = f"https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?{q}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "NYFun3-trip-planner/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        m = data["result"]["addressMatches"]
        if not m:
            cache[address] = {"lat": None, "lon": None, "matched": None, "source": url,
                              "status": "no match returned by the Census geocoder"}
            return cache[address]
        matched = m[0]["matchedAddress"]
        # The geocoder usually returns several candidates; a first result whose
        # street name or number disagrees with what we asked for is recorded as
        # "partial" so it can be flagged instead of quietly trusted.
        asked_number = re.match(r"\s*(\d+)", address)
        got_number = re.match(r"\s*(\d+)", matched or "")
        street_word = re.search(r"\d+\s+(?:[NSEW]\.?\s+)?([A-Za-z0-9.]+)", address)
        same_number = bool(asked_number and got_number and asked_number.group(1) == got_number.group(1))
        same_street = bool(street_word and street_word.group(1).lower() in (matched or "").lower())
        status = "exact number and street" if same_number and same_street else "partial match"
        cache[address] = {"lat": m[0]["coordinates"]["y"], "lon": m[0]["coordinates"]["x"],
                          "matched": matched, "source": url, "status": status,
                          "candidates": len(m)}
        return cache[address]
    except Exception as exc:  # noqa: BLE001
        log(f"  ! geocode failed for {address!r}: {exc}")
        return None


def street_address(text: str) -> str | None:
    """Take the first '123 Something St' style address out of a longer string."""
    if not text:
        return None
    m = re.search(r"(\d+[^,]*),?\s*(New York|Brooklyn|Queens|Bronx),?\s*NY", text)
    return m.group(0) if m else None


# ---------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/transit_hotels.json")
    ap.add_argument("--skip-buses", action="store_true")
    args = ap.parse_args()

    hotels = json.loads((ROOT / "data/hotels.json").read_text())["hotels"]
    restaurants = json.loads((ROOT / "data/michelin_all.json").read_text())["restaurants"]
    activities = json.loads((ROOT / "data/activities.json").read_text())["activities"]

    group_ids: dict[str, int] = {}
    stops_xy: dict[int, tuple[float, float]] = {}
    trip_ids: dict[str, int] = {}
    trip_service: list[str] = []
    packed: list[int] = []
    feed_meta = {}

    log("Downloading and parsing official MTA GTFS feeds…")
    for tag, url in FEEDS.items():
        if args.skip_buses and tag.startswith("bus"):
            continue
        path = fetch(url, CACHE / f"{tag}.zip")
        before = len(packed)
        read_feed(path, tag, group_ids, stops_xy, trip_ids, trip_service, packed)
        feed_meta[tag] = {"url": url, "connections": len(packed) - before}

    log(f"Sorting {len(packed):,} connections by departure time…")
    packed.sort()
    n_groups = len(group_ids)
    log(f"{n_groups:,} boarding groups, {len(trip_service):,} trips")

    weekday, saturday, feed_range = pick_service_dates()
    log(f"service dates chosen from the feed: weekday={weekday} saturday={saturday} {feed_range}")

    log("Building walking-transfer links between nearby stops…")
    walk_links = build_walk_links(stops_xy, TRANSFER_WALK_M)
    log(f"  {sum(len(v) for v in walk_links.values()):,} walking links")

    cache = load_cache()
    doors = []
    for h in hotels:
        doors.append({"kind": "hotel", "row": h, "addr": h.get("address")})
    for r in restaurants:
        doors.append({"kind": "restaurant", "row": r, "addr": street_address(r.get("address")) or r.get("address")})
    for a in activities:
        addr = a.get("address") or ""
        if "Digital ticket" in addr:
            continue
        doors.append({"kind": "activity", "row": a, "addr": street_address(addr) or addr})
    for d in doors:
        d["geo"] = geocode(d["addr"], cache) if d.get("addr") else None
    save_cache(cache)
    missing = [d for d in doors if not d["geo"] or not d["geo"].get("lat")]
    log(f"geocoded {len(doors) - len(missing)}/{len(doors)} doors; missing: {[d['row'].get('name') for d in missing]}")

    cells = defaultdict(list)
    for gid, (lat, lon) in stops_xy.items():
        cells[(int(lat * 1000 // 100), int(lon * 1000 // 100))].append(gid)

    destinations = [d for d in doors if d["kind"] != "hotel" and d["geo"] and d["geo"].get("lat")]
    unmeasured = []
    for d in list(destinations):
        d["stops"] = stops_near(stops_xy, cells, d["geo"]["lat"], d["geo"]["lon"], MAX_WALK_M)
        if not d["stops"]:
            unmeasured.append({"name": d["row"].get("name"), "kind": d["kind"],
                               "address": d["addr"], "reason": "no subway or bus stop within the 500 m walk cap"})
            destinations.remove(d)
    for d in doors:
        if d["kind"] == "hotel":
            continue
        if not d.get("addr"):
            unmeasured.append({"name": d["row"].get("name"), "kind": d["kind"], "address": None,
                               "reason": "no street address published in data/activities.json"})
        elif not d["geo"] or not d["geo"].get("lat"):
            unmeasured.append({"name": d["row"].get("name"), "kind": d["kind"], "address": d["addr"],
                               "reason": "the U.S. Census geocoder returned no match for this address"})

    results = []
    for svc_date, label in ((weekday, "wednesday"), (saturday, "saturday")):
        services = active_services(svc_date)
        active_trips = {i for i, sid in enumerate(trip_service) if sid in services}
        log(f"{label} {svc_date}: {len(services)} service ids, {len(active_trips):,} trips")
        keep = [p for p in packed if (p & ((1 << W_TRIP) - 1)) in active_trips]
        log(f"  {len(keep):,} connections active that day")
        router = Router(keep, stops_xy, walk_links, n_groups)

        for h in hotels:
            geo = next((d["geo"] for d in doors if d["kind"] == "hotel" and d["row"] is h), None)
            if not geo:
                continue
            origins = stops_near(stops_xy, cells, geo["lat"], geo["lon"], MAX_WALK_M)
            if not origins:
                continue
            for window in DEPARTURE_WINDOWS:
                hh, mm = window.split(":")
                start = int(hh) * 3600 + int(mm) * 60
                log(f"  routing {h['name']} · {label} · depart {window} "
                    f"({len(origins)} nearby stops)")
                arrival, deadline = router.route(origins, start, SEARCH_WINDOW_MIN)
                row = {
                    "hotel_id": h["id"],
                    "hotel_name": h["name"],
                    "service": label,
                    "service_date": svc_date,
                    "depart_after_local": window,
                    "hotel_stops_within_walk": len(origins),
                    "nearest_stop_walk_min": round(min(origins.values()), 1),
                    "destinations": {},
                }
                for d in destinations:
                    best = None
                    for gid, wmin in d["stops"].items():
                        if arrival[gid] >= (1 << 30):
                            continue
                        total = (arrival[gid] - start) / 60.0 + wmin
                        if best is None or total < best:
                            best = total
                    name = d["row"].get("name") or d["row"].get("id")
                    row["destinations"][name] = {
                        "minutes": round(best, 1) if best is not None else None,
                        "within_1h": (best is not None and round(best, 1) <= REPORT_LIMIT_MIN),
                        "kind": d["kind"],
                        "stops_within_walk": len(d["stops"]),
                    }
                results.append(row)

    within = [r for r in results]
    out = {
        "_meta": {
            "generated_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "what_this_is": "A modelled door-to-door journey time for every hotel x destination pair, "
                            "computed by this script from the official MTA static GTFS timetable.",
            "what_this_is_not": [
                "not an MTA-published door-to-door time",
                "not a 2027 trip plan — the static feed carries the current timetable and omits most "
                "temporary service changes",
                "not a live disruption, elevator or weather check",
            ],
            "assumptions": ASSUMPTIONS,
            "feeds": feed_meta,
            "feed_index_url": "https://www.mta.info/developers",
            "service_dates": {"wednesday": weekday, "saturday": saturday, **feed_range},
            "geocoder": {
                "name": "U.S. Census Bureau geocoder",
                "benchmark": "Public_AR_Current",
                "url": "https://geocoding.geo.census.gov/geocoder",
            },
            "null_meaning": "minutes = null means no journey of 110 minutes or less was found, or the "
                            "address could not be geocoded. It never means zero.",
            "geocode_register": {d["addr"]: d["geo"] for d in doors if d.get("addr") and d.get("geo")},
            "unmeasured_destinations": sorted(unmeasured, key=lambda x: (x["kind"], str(x["name"]))),
            "rows": len(within),
        },
        "results": results,
    }
    outpath = ROOT / args.out
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_text(json.dumps(out, indent=1, sort_keys=True))
    log(f"wrote {outpath} ({len(results)} hotel x service x window rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
