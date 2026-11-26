#!/usr/bin/env python3
"""
Compute door-to-door weekday evening (18:30 departure) transit travel times
from every hotel in data/hotels.json to every active NYC MICHELIN restaurant
in data/michelin_all.json using official U.S. Census / NYC Planning geocoders
and the live MTA GTFS Subway schedule (gtfs_subway.zip).

Outputs: research/generated/transit_1h.json
"""

import bisect
import csv
import datetime as dt
import heapq
import io
import json
import math
import re
import time
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOTELS_JSON = ROOT / "data" / "hotels.json"
MICHELIN_JSON = ROOT / "data" / "michelin_all.json"
OUT_JSON = ROOT / "research" / "generated" / "transit_1h.json"

GTFS_SUBWAY_URL = "https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip"
CENSUS_URL = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
NYC_GEOSEARCH_URL = "https://geosearch.planninglabs.nyc/v2/search"

DEPARTURE_TIME_STR = "18:30:00"
DEPARTURE_SEC = 18 * 3600 + 30 * 60
TARGET_DATE = "20270212"  # Regular Friday weekday inside active feed (20261126-20270215)
WALK_SPEED_MPS = 80.0 / 60.0  # 80 m/min (~4.8 km/h)
GRID_DETOUR = 1.25  # NYC street-grid walking factor over haversine
STATION_ENTRY_BUFFER_S = 120
TRANSFER_DEFAULT_S = 180
MAX_WALK_TO_STOP_M = 1200.0
MAX_DIRECT_WALK_M = 2400.0
MAX_TRANSFER_WALK_M = 250.0
CUTOFF_SEC = 60 * 60  # 60 minutes


def haversine_m(lat1, lon1, lat2, lon2):
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def clean_address(addr: str) -> str:
    s = re.sub(r"\s*\([^)]*\)", "", addr).strip()
    # Strip building/hotel prefixes before comma when followed by a street address
    s = re.sub(r"^(?:Trump International Hotel & Tower|11 Howard Hotel),\s*", "", s)
    s = re.sub(r",\s*(?:Ste\.?|Suite|Fl\.?|Floor)\s*[^,]+", "", s, flags=re.I)
    s = re.sub(r",\s*\d+(?:st|nd|rd|th)\s+Fl\.?", "", s, flags=re.I)
    s = re.sub(r"\s+#\S+", "", s)
    s = s.replace("Long Island City, Queens, NY", "Long Island City, NY")
    s = s.replace("Ninth Ave.", "9th Ave").replace("Ninth Ave", "9th Ave")
    s = s.replace("Tenth Ave.", "10th Ave").replace("Tenth Ave", "10th Ave")
    s = s.replace("Eighth Ave.", "8th Ave").replace("Seventh Ave.", "7th Ave")
    s = s.replace("Fifth Ave.", "5th Ave").replace("Sixth Ave.", "6th Ave")
    s = re.sub(r"\b(St|Ave|Pl|Sq|Rd|Blvd)\.", r"\1", s)
    s = re.sub(r"\b([NSEW])\.\s+", r"\1 ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def fetch_json(url: str, timeout: int = 20):
    req = urllib.request.Request(url, headers={"User-Agent": "NYFun3-TransitBot/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def in_nyc_bbox(lat: float, lon: float) -> bool:
    return 40.48 <= lat <= 40.95 and -74.26 <= lon <= -73.70


def geocode_address(raw_addr: str):
    cleaned = clean_address(raw_addr)
    # 1. NYC Department of City Planning GeoSearch (fast, authoritative NYC addresses)
    for candidate in (cleaned, raw_addr):
        qs = urllib.parse.urlencode({"text": candidate, "size": 1})
        try:
            data = fetch_json(f"{NYC_GEOSEARCH_URL}?{qs}", timeout=15)
            feats = data.get("features", [])
            if feats:
                lon, lat = feats[0]["geometry"]["coordinates"][:2]
                lat, lon = float(lat), float(lon)
                if in_nyc_bbox(lat, lon):
                    return {
                        "lat": round(lat, 6),
                        "lon": round(lon, 6),
                        "matched_address": feats[0].get("properties", {}).get("label", ""),
                        "geocoder": "NYC Planning GeoSearch",
                    }
        except Exception as exc:
            print(f"GeoSearch warn ({candidate}): {exc}", flush=True)

    # 2. U.S. Census Geocoder fallback
    for candidate in (cleaned, raw_addr):
        qs = urllib.parse.urlencode({
            "address": candidate,
            "benchmark": "Public_AR_Current",
            "format": "json",
        })
        try:
            data = fetch_json(f"{CENSUS_URL}?{qs}", timeout=20)
            matches = data.get("result", {}).get("addressMatches", [])
            if matches:
                c = matches[0]["coordinates"]
                lat, lon = float(c["y"]), float(c["x"])
                if in_nyc_bbox(lat, lon):
                    return {
                        "lat": round(lat, 6),
                        "lon": round(lon, 6),
                        "matched_address": matches[0].get("matchedAddress", ""),
                        "geocoder": "US Census Geocoder",
                    }
        except Exception as exc:
            print(f"Census warn ({candidate}): {exc}", flush=True)
    return None


def parse_gtfs_time(t: str) -> int:
    h, m, s = map(int, t.strip().split(":"))
    return h * 3600 + m * 60 + s


def pick_active_services(zf: zipfile.ZipFile, yyyymmdd: str):
    d = dt.datetime.strptime(yyyymmdd, "%Y%m%d").date()
    dow_col = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"][d.weekday()]
    active = set()
    feed_min, feed_max = None, None
    with zf.open("calendar.txt") as f:
        for row in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            s_d, e_d = row["start_date"].strip(), row["end_date"].strip()
            feed_min = s_d if feed_min is None else min(feed_min, s_d)
            feed_max = e_d if feed_max is None else max(feed_max, e_d)
            if s_d <= yyyymmdd <= e_d and row[dow_col].strip() == "1":
                active.add(row["service_id"].strip())
    if "calendar_dates.txt" in zf.namelist():
        with zf.open("calendar_dates.txt") as f:
            for row in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
                if row["date"].strip() == yyyymmdd:
                    sid = row["service_id"].strip()
                    if row["exception_type"].strip() == "1":
                        active.add(sid)
                    elif row["exception_type"].strip() == "2":
                        active.discard(sid)
    return active, feed_min, feed_max


def build_gtfs_graph(gtfs_bytes: bytes):
    zf = zipfile.ZipFile(io.BytesIO(gtfs_bytes))
    active_services, feed_min, feed_max = pick_active_services(zf, TARGET_DATE)

    stops = {}
    parent_children = {}
    with zf.open("stops.txt") as f:
        for row in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            sid = row["stop_id"].strip()
            lat = float(row["stop_lat"])
            lon = float(row["stop_lon"])
            ps = (row.get("parent_station") or "").strip()
            stops[sid] = {
                "id": sid,
                "name": row["stop_name"].strip(),
                "lat": lat,
                "lon": lon,
                "parent": ps,
                "loc_type": (row.get("location_type") or "0").strip(),
            }
            if ps:
                parent_children.setdefault(ps, []).append(sid)

    routes = {}
    with zf.open("routes.txt") as f:
        for row in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            routes[row["route_id"].strip()] = (
                row.get("route_short_name") or row.get("route_id")
            ).strip()

    trips = {}
    with zf.open("trips.txt") as f:
        for row in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            if row["service_id"].strip() in active_services:
                trips[row["trip_id"].strip()] = routes.get(row["route_id"].strip(), row["route_id"].strip())

    # Collect stop_times in evening window [DEPARTURE_SEC - 300, DEPARTURE_SEC + 5400]
    win_start = DEPARTURE_SEC - 300
    win_end = DEPARTURE_SEC + 5400
    trip_stops = {}
    with zf.open("stop_times.txt") as f:
        for row in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            tid = row["trip_id"].strip()
            if tid not in trips:
                continue
            arr = parse_gtfs_time(row["arrival_time"])
            dep = parse_gtfs_time(row["departure_time"])
            if dep < win_start or arr > win_end:
                continue
            trip_stops.setdefault(tid, []).append((int(row["stop_sequence"]), row["stop_id"].strip(), arr, dep))

    # Build ride edges: stop_id -> list of (dep_sec, arr_sec, to_stop_id, route_name)
    # Keep sorted by dep_sec per stop_id
    ride_edges = {}
    for tid, seq_list in trip_stops.items():
        seq_list.sort(key=lambda x: x[0])
        rname = trips[tid]
        for i in range(len(seq_list) - 1):
            _, s1, _, dep1 = seq_list[i]
            _, s2, arr2, _ = seq_list[i + 1]
            if arr2 >= dep1:
                ride_edges.setdefault(s1, []).append((dep1, arr2, s2, rname))

    for sid in ride_edges:
        ride_edges[sid].sort(key=lambda e: e[0])

    # Build transfer / walking edges between platform stops
    boardable_stops = [sid for sid in stops if sid in ride_edges or any(stops[sid]["loc_type"] != "1" for _ in [0])]
    # Restrict to stops actually used in trips or having parent_station
    used_stops = set(ride_edges.keys())
    for edges in ride_edges.values():
        for _, _, to_s, _ in edges:
            used_stops.add(to_s)

    walk_edges = {sid: {} for sid in used_stops}

    def add_walk(u, v, sec):
        if u in walk_edges and v in walk_edges and u != v:
            cur = walk_edges[u].get(v)
            if cur is None or sec < cur:
                walk_edges[u][v] = sec

    # Sibling stops in same parent station
    for ps, kids in parent_children.items():
        for u in kids:
            for v in kids:
                add_walk(u, v, 120)

    # GTFS transfers.txt (mapping parent_station to children if needed)
    if "transfers.txt" in zf.namelist():
        with zf.open("transfers.txt") as f:
            for row in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
                fs = row["from_stop_id"].strip()
                ts = row["to_stop_id"].strip()
                if row.get("transfer_type", "").strip() == "3":
                    continue
                mt = int(row["min_transfer_time"]) if (row.get("min_transfer_time") or "").strip().isdigit() else TRANSFER_DEFAULT_S
                mt = max(120, mt)
                f_nodes = parent_children.get(fs, [fs])
                t_nodes = parent_children.get(ts, [ts])
                for u in f_nodes:
                    for v in t_nodes:
                        add_walk(u, v, mt)

    # Nearby walking transfers (<= 250 m between distinct stations)
    used_list = sorted(used_stops)
    for i, u in enumerate(used_list):
        su = stops[u]
        for j in range(i + 1, len(used_list)):
            v = used_list[j]
            sv = stops[v]
            if abs(su["lat"] - sv["lat"]) > 0.0028 or abs(su["lon"] - sv["lon"]) > 0.0035:
                continue
            d_m = haversine_m(su["lat"], su["lon"], sv["lat"], sv["lon"])
            if d_m <= MAX_TRANSFER_WALK_M:
                w_sec = int(round((d_m * GRID_DETOUR) / WALK_SPEED_MPS)) + 120
                add_walk(u, v, w_sec)
                add_walk(v, u, w_sec)

    # Convert ride_edges to dep_keys + lists for fast bisect
    ride_deps = {sid: [e[0] for e in edges] for sid, edges in ride_edges.items()}

    return {
        "stops": stops,
        "used_stops": used_list,
        "ride_edges": ride_edges,
        "ride_deps": ride_deps,
        "walk_edges": walk_edges,
        "active_services": sorted(active_services),
        "feed_min": feed_min,
        "feed_max": feed_max,
    }


def dijkstra_from_origin(graph, origin_lat, origin_lon):
    stops = graph["stops"]
    ride_edges = graph["ride_edges"]
    ride_deps = graph["ride_deps"]
    walk_edges = graph["walk_edges"]

    best = {}
    prev = {}  # node -> (prev_node, mode, route_or_min)
    pq = []

    for sid in graph["used_stops"]:
        st = stops[sid]
        d_m = haversine_m(origin_lat, origin_lon, st["lat"], st["lon"])
        if d_m <= MAX_WALK_TO_STOP_M:
            walk_s = int(round((d_m * GRID_DETOUR) / WALK_SPEED_MPS)) + STATION_ENTRY_BUFFER_S
            arr = DEPARTURE_SEC + walk_s
            if arr < best.get(sid, 10**9):
                best[sid] = arr
                prev[sid] = (None, "walk_in", round(walk_s / 60.0, 1), st["name"])
                heapq.heappush(pq, (arr, sid))

    max_arr = DEPARTURE_SEC + CUTOFF_SEC + 600
    while pq:
        t, u = heapq.heappop(pq)
        if t > best.get(u, 10**9) or t > max_arr:
            continue

        # 1. Walk/transfer edges
        for v, w_sec in walk_edges.get(u, {}).items():
            nt = t + w_sec
            if nt < best.get(v, 10**9) and nt <= max_arr:
                best[v] = nt
                prev[v] = (u, "transfer", round(w_sec / 60.0, 1), stops[v]["name"])
                heapq.heappush(pq, (nt, v))

        # 2. Scheduled subway departures >= t (keep earliest arrival per destination stop & route)
        if u in ride_edges:
            deps = ride_deps[u]
            edges = ride_edges[u]
            idx = bisect.bisect_left(deps, t)
            seen_to = set()
            for k in range(idx, len(edges)):
                dep, arr, v, rname = edges[k]
                if dep > t + 1500:  # ignore waits >25 min on a single segment
                    break
                if arr > max_arr:
                    continue
                if (v, rname) in seen_to:
                    continue
                seen_to.add((v, rname))
                if arr < best.get(v, 10**9):
                    best[v] = arr
                    prev[v] = (u, "subway", rname, stops[v]["name"])
                    heapq.heappush(pq, (arr, v))
    return best, prev


def summarize_route(prev, end_stop, stops):
    chain = []
    cur = end_stop
    while cur is not None and cur in prev:
        p, mode, info, sname = prev[cur]
        chain.append((cur, mode, info, sname))
        cur = p
    chain.reverse()
    lines = []
    board_station = None
    last_station = None
    for sid, mode, info, sname in chain:
        if mode == "walk_in":
            board_station = sname
        elif mode == "subway":
            if not lines or lines[-1] != info:
                lines.append(info)
            last_station = sname
        elif mode == "transfer":
            last_station = sname
    if not lines:
        return "walk"
    return f"{'/'.join(lines)} ({board_station} -> {last_station})"


def main():
    hotels_data = json.loads(HOTELS_JSON.read_text())
    michelin_data = json.loads(MICHELIN_JSON.read_text())

    # Filter active NYC MICHELIN venues
    active_restaurants = []
    excluded = []
    for r in michelin_data["restaurants"]:
        name = r["name"]
        addr = r.get("address", "")
        if "Shion 69 Leonard" in name or "CLOSED" in addr:
            excluded.append({"name": name, "reason": "Closed indefinitely (Dec 27, 2025 fire); omitted from live MICHELIN NYC Guide."})
            continue
        if "Tarrytown" in addr or "North Salem" in addr:
            excluded.append({"name": name, "reason": f"Outside NYC subway transit boundary ({addr})."})
            continue
        active_restaurants.append(r)

    print(f"Geocoding {len(hotels_data['hotels'])} hotels and {len(active_restaurants)} active NYC restaurants...")
    from concurrent.futures import ThreadPoolExecutor

    def _geo_hotel(h):
        return h["id"], geocode_address(h["address"]), h

    def _geo_rest(r):
        return r["name"], geocode_address(r["address"]), r

    with ThreadPoolExecutor(max_workers=6) as pool:
        hotel_coords = {}
        for hid, g, h in pool.map(_geo_hotel, hotels_data["hotels"]):
            if not g:
                raise RuntimeError(f"Failed to geocode hotel {h['name']}: {h['address']}")
            hotel_coords[hid] = g

        rest_coords = {}
        for rname, g, r in pool.map(_geo_rest, active_restaurants):
            if not g:
                raise RuntimeError(f"Failed to geocode restaurant {r['name']}: {r['address']}")
            rest_coords[rname] = g

    print(f"Downloading MTA GTFS Subway feed from {GTFS_SUBWAY_URL}...")
    req = urllib.request.Request(GTFS_SUBWAY_URL, headers={"User-Agent": "NYFun3-TransitBot/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        gtfs_bytes = resp.read()

    graph = build_gtfs_graph(gtfs_bytes)
    stops = graph["stops"]
    print(f"Loaded {len(graph['used_stops'])} active subway platform stops; feed dates {graph['feed_min']}..{graph['feed_max']}")

    hotel_results = []
    for h in hotels_data["hotels"]:
        hc = hotel_coords[h["id"]]
        best_arr, prev = dijkstra_from_origin(graph, hc["lat"], hc["lon"])
        journeys = []
        within_60 = 0
        within_45 = 0
        within_30 = 0
        all_mins = []

        for r in active_restaurants:
            rc = rest_coords[r["name"]]
            best_min = None
            best_desc = None

            # Direct walk check
            direct_m = haversine_m(hc["lat"], hc["lon"], rc["lat"], rc["lon"])
            if direct_m <= MAX_DIRECT_WALK_M:
                w_min = round((direct_m * GRID_DETOUR) / WALK_SPEED_MPS / 60.0, 1)
                best_min = w_min
                best_desc = f"Direct walk (~{int(round(direct_m * GRID_DETOUR))} m)"

            # Subway + walk egress check
            for sid, arr in best_arr.items():
                st = stops[sid]
                eg_m = haversine_m(st["lat"], st["lon"], rc["lat"], rc["lon"])
                if eg_m <= MAX_WALK_TO_STOP_M:
                    eg_s = int(round((eg_m * GRID_DETOUR) / WALK_SPEED_MPS))
                    tot_min = round((arr + eg_s - DEPARTURE_SEC) / 60.0, 1)
                    if best_min is None or tot_min < best_min:
                        best_min = tot_min
                        best_desc = summarize_route(prev, sid, stops)

            in_1h = best_min is not None and best_min <= 60.0
            if in_1h:
                within_60 += 1
            if best_min is not None and best_min <= 45.0:
                within_45 += 1
            if best_min is not None and best_min <= 30.0:
                within_30 += 1
            if best_min is not None:
                all_mins.append(best_min)

            journeys.append({
                "restaurant": r["name"],
                "stars": r["stars"],
                "minutes": best_min,
                "within_60_min": in_1h,
                "route": best_desc or ">70 min / unreachable in cutoff window",
            })

        all_mins_sorted = sorted(all_mins)
        median_min = all_mins_sorted[len(all_mins_sorted) // 2] if all_mins_sorted else None
        hotel_results.append({
            "id": h["id"],
            "name": h["name"],
            "address": h["address"],
            "geocoded": hc,
            "within_60_min_count": within_60,
            "within_45_min_count": within_45,
            "within_30_min_count": within_30,
            "universe_count": len(active_restaurants),
            "median_minutes": median_min,
            "journeys": sorted(journeys, key=lambda x: (999 if x["minutes"] is None else x["minutes"], x["restaurant"])),
        })

    hotel_results.sort(key=lambda x: (-x["within_60_min_count"], -x["within_45_min_count"], x["median_minutes"] or 999))

    out = {
        "_meta": {
            "generated_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "methodology": (
                "Door-to-door weekday evening departure (18:30 local) using live MTA GTFS Subway timetable "
                f"(feed {graph['feed_min']}–{graph['feed_max']}, service date {TARGET_DATE}) and official "
                "U.S. Census Geocoder / NYC Planning GeoSearch coordinates. Walking uses 80 m/min (~4.8 km/h) "
                f"with {GRID_DETOUR}× street-grid detour factor, {STATION_ENTRY_BUFFER_S}s station-entry buffer, "
                "and GTFS transfers + <=250 m station-complex walks."
            ),
            "schedule_caveat": (
                f"Published MTA subway GTFS covers {graph['feed_min']}–{graph['feed_max']} (extending through arrival day Feb 15, 2027); "
                "bus feeds expired 2027-01-01 so subway+walk is modeled here. Presidents' Day (Feb 15) and post-Feb 15 subway schedules should be rechecked closer to travel."
            ),
            "gtfs_source": GTFS_SUBWAY_URL,
            "active_nyc_restaurants": len(active_restaurants),
            "excluded_from_nyc_transit": excluded,
        },
        "ranking": [
            {
                "rank": idx + 1,
                "id": h["id"],
                "name": h["name"],
                "within_60_min_count": h["within_60_min_count"],
                "within_45_min_count": h["within_45_min_count"],
                "within_30_min_count": h["within_30_min_count"],
                "universe_count": h["universe_count"],
                "median_minutes": h["median_minutes"],
            }
            for idx, h in enumerate(hotel_results)
        ],
        "hotels": hotel_results,
        "restaurants_geocoded": [
            {"name": r["name"], "stars": r["stars"], "address": r["address"], **rest_coords[r["name"]]}
            for r in active_restaurants
        ],
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {OUT_JSON}")
    for row in out["ranking"]:
        print(f"  #{row['rank']} {row['name']}: {row['within_60_min_count']}/{row['universe_count']} <=60m, {row['within_45_min_count']} <=45m, {row['within_30_min_count']} <=30m (median {row['median_minutes']}m)")


if __name__ == "__main__":
    main()
PY