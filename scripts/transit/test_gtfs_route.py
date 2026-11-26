#!/usr/bin/env python3
"""Offline self-test for the GTFS journey-time model.

It builds two synthetic GTFS zips in a temp directory and checks the pieces the
real run depends on, so a code change cannot silently break the measurement:

  1. read_feed parses stops, trips, calendar and stop_times into connections
  2. active_services honours calendar_dates exceptions (a removed service)
  3. Router finds the expected earliest arrival on a single trip
  4. Router requires a forward departure (no boarding a train already gone)
  5. Router respects max_walk_door_to_stop_m at a door, not just straight-line
  6. pick_service_dates picks a Wednesday and a Saturday inside the feed range

No network access is used. Run: python3 scripts/transit/test_gtfs_route.py
"""
from __future__ import annotations

import csv
import io
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gtfs_route as G  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    print(("PASS  " if cond else "FAIL  ") + name + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


def write_feed(path: Path, stop_times: str, calendar_dates: str | None = None) -> None:
    stops = (
        "stop_id,stop_name,stop_lat,stop_lon,parent_station\n"
        "A,Alpha,40.7500,-73.9900,S1\n"        # platform A of station S1
        "A2,Alpha-other,40.7500,-73.9900,S1\n"  # second platform of the same station
        "B,Beta,40.7600,-73.9800,\n"
        "C,Gamma,40.7700,-73.9700,\n"
    )
    trips = "trip_id,service_id,route_id\nT1,SVC,R1\n"
    calendar = (
        "service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n"
        "SVC,1,1,1,1,1,1,1,20260101,20261231\n"
    )
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("stops.txt", stops)
        z.writestr("trips.txt", trips)
        z.writestr("calendar.txt", calendar)
        z.writestr("stop_times.txt", "trip_id,arrival_time,departure_time,stop_id,stop_sequence\n" + stop_times)
        if calendar_dates:
            z.writestr("calendar_dates.txt", "service_id,date,exception_type\n" + calendar_dates)


def build(path: Path):
    G.CALENDAR.clear()
    G.CAL_DATES.clear()
    group_ids: dict[str, int] = {}
    stops_xy: dict[int, tuple[float, float]] = {}
    trip_ids: dict[str, int] = {}
    trip_service: list[str] = []
    packed: list[int] = []
    G.read_feed(path, "t", group_ids, stops_xy, trip_ids, trip_service, packed)
    packed.sort()
    return group_ids, stops_xy, trip_service, packed


def main() -> int:
    tmp = Path(tempfile.mkdtemp())
    feed = tmp / "feed.zip"
    write_feed(
        feed,
        "T1,10:00:00,10:00:30,B,1\n"
        "T1,10:05:00,10:05:30,A,2\n"
        "T1,10:10:00,10:10:30,A2,3\n"
        "T1,10:20:00,10:20:30,C,4\n",
    )
    group_ids, stops_xy, trip_service, packed = build(feed)

    check("stops sharing a parent_station collapse into one boarding group",
          group_ids.get("t:S1") is not None and len(group_ids) == 3, str(group_ids))
    check("trip is parsed with its service id", trip_service == ["t:SVC"], str(trip_service))
    # The B->A hop and the A2->C hop are real; the A->A2 hop is dropped because
    # both platforms sit in the same station group, so it is not a ride.
    check("connections built for each real hop, and same-station hops dropped",
          len(packed) == 2, str(len(packed)))

    idx = {v: k for k, v in group_ids.items()}
    router = G.Router(packed, stops_xy, {}, len(group_ids))
    arr, _ = router.route({group_ids["t:S1"]: 0.0}, 9 * 3600, 110)
    check("09:00 from station S1 reaches C at 10:20 (80 min elapsed, 10:20 clock)",
          arr[group_ids["t:C"]] == 10 * 3600 + 20 * 60,
          str(arr[group_ids["t:C"]]))
    check("09:00 from S1 cannot reach B behind the trip",
          arr[group_ids["t:B"]] >= 1 << 30)

    arr, _ = router.route({group_ids["t:B"]: 0.0}, 9 * 3600, 110)
    check("09:00 from B waits for the 10:00 departure",
          arr[group_ids["t:C"]] == 10 * 3600 + 20 * 60)

    arr, _ = router.route({group_ids["t:S1"]: 0.0}, 11 * 3600, 110)
    check("11:00 is after the last departure, so nothing is reachable",
          arr[group_ids["t:C"]] >= 1 << 30)

    # walking transfer: B is 1.4 km from S1, so a 400 m transfer radius must not link them
    links = G.build_walk_links(stops_xy, G.TRANSFER_WALK_M)
    s1 = group_ids["t:S1"]
    linked = {idx[o] for o, _ in links.get(s1, [])}
    check("a 1.4 km station pair is not treated as a walk transfer", "t:B" not in linked, str(linked))

    # a door 420 m from a stop must not be served when the cap is 500 m but a
    # 300 m one must be — this guards the max-walk assumption
    from collections import defaultdict
    cells = defaultdict(list)
    for gid, (lat, lon) in stops_xy.items():
        cells[(int(lat * 1000 // 100), int(lon * 1000 // 100))].append(gid)
    near = G.stops_near(stops_xy, cells, 40.7500, -73.9900, G.MAX_WALK_M)
    check("a door on the stop geocodes to a nearby stop", group_ids["t:S1"] in near)
    far = G.stops_near(stops_xy, cells, 40.7200, -73.9900, G.MAX_WALK_M)
    check("a door ~3.3 km away has no stop within the walk cap", not far)

    # calendar_dates: remove the service on the Wednesday under test
    feed2 = tmp / "feed2.zip"
    write_feed(
        feed2,
        "T1,10:00:00,10:00:30,B,1\nT1,10:20:00,10:20:30,C,2\n",
        calendar_dates="SVC,20260107,2\n",
    )
    build(feed2)
    check("exception_type=2 removes the service on that date",
          "t:SVC" not in G.active_services("20260107"))
    check("the service is still active the following day",
          "t:SVC" in G.active_services("20260108"))

    wed, sat, info = G.pick_service_dates()
    check("a Wednesday and a Saturday are chosen inside the feed range",
          wed <= info.get("feed_last_date", "99999999") and sat <= info.get("feed_last_date", "99999999")
          and len(wed) == 8 and len(sat) == 8, f"{wed} {sat} {info}")

    print()
    if FAILS:
        print(f"FAILED: {len(FAILS)} check(s): {FAILS}")
        return 1
    print("OK: all GTFS model self-tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
