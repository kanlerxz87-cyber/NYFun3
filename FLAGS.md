# FLAGS — irregular, conflicting and unverifiable findings

Published alongside the site. Every item below was found by opening the page named, and every item names
the next check that would clear it. Nothing here blocks the dashboard: a fact that could not be confirmed
stays blank in its table and is listed here.

Two companions: `EVIDENCE_AUDIT.md` (how good the evidence behind each table is) and
`CURRENT_AUDIT.md` (what is still missing before a booking decision). This file is the list of *defects*.

Verification date: **26 November 2026**. Travel window: 15 February – 23 March 2027, preferred 15–18 February.

---

## 1. Hotel source links that did not reach the hotel

Eight of the hotel websites shipped in `data/hotels.json` did not reach the property when checked (the
comparison set has since grown to 14 hotels as other sessions added rows). Each was opened;
each replacement was opened and checked for the hotel's own address or room names.

| Hotel | Link that failed | What it actually served | Verified replacement |
|---|---|---|---|
| Hotel Giraffe Union Square (HGU) | `hgunewyork.com` | parked / for-sale domain, no hotel content | <https://www.hgunyc.com/> — Queen Standard page shows "NYC pre-war style bathroom" |
| The Mayfair Hotel | `themayfairhotel.com` | GoDaddy for-sale page (US$9,995) | <https://www.mayfairhotelnyc.com/rooms> — 242 W 49th St, 1 Queen / 1 King, max 2 |
| Hyatt Place Chelsea | `hyatt.com/…/nyczc-…` | wrong property code | `lgazc` property code for Hyatt Place New York/Chelsea |
| Arlo Midtown | `arlohotels.com/arlo-midtown/` | 404 | <https://arlohotels.com/midtown/rooms/king-city/> — King City 170–190 sq ft, sleeps 2 |
| citizenM Times Square | `citizenm.com/…` | redirects to a brand page | <https://www.marriott.com/en-us/hotels/nyczt-citizenm-new-york-times-square/rooms/> — every room XL king, max occupancy 2 |
| Pestana CR7 Times Square | `pestana.com/…/pestana-cr7-new-york` | 404 slug | <https://www.pestana.com/en/hotel/pestana-cr7-times-square> |
| Blue Angel Hotel | `blueangelhotel.com` | dead domain | <https://www.blueangelhotelnyc.com/rooms> |
| Eurostars Wall Street | — reached the hotel, but only the Spanish locale rendered | 56 rooms, breakfast 07:00–10:30 weekdays, 15:00 / 12:00 | kept as-is |

**Do not cite:** `hgunewyork.com`, `themayfairhotel.com`, `mayfairnewyork.com`, `blueangelhotel.com`.
`scripts/check_sources.py` now fails the build if one of these re-enters a data file.

**Still wrong on the Flagged for Review page:** NR-02 still links the parked `hgunewyork.com` domain and
NR-03 links a Booking.com page for that property. The link is public and points at a parked domain; the
correct first-party starting point is `hgunyc.com`. Logged as a request rather than silently rewritten,
because the surrounding NR rows are another session's evidence statements.

## 2. Blue Angel Hotel — the street address disagrees

The shipped record says **1234 Broadway, 10001**. The hotel's own site says **152 East 55th Street, 10022**
(rooms page, plus the phone number 212-752-0600). Those are different neighbourhoods, and the difference
changes every journey time from that door.

Resolved in the model only: `scripts/transit/gtfs_route.py` carries `ADDRESS_OVERRIDES["Blue Angel Hotel"]`
so measurements run from 152 E 55th St, and each hotel row now carries `address_used`. `data/hotels.json`
records both values with `address_flag: official address differs from the shipped address`.
The Hotels page text still shows the old address — owner's call, not edited here.

## 3. Pestana CR7 — the fee arithmetic on the Hotels page does not match the hotel

`hotels.html` describes a **$26/night resort fee already included**. The hotel's own page states
**US$26.14 per room per night, plus 14.75% tax, plus US$3.50 per night local tax**. Three consequences:
the fee is not $26, the tax is charged on the fee as well, and the total for 7 nights is not derivable by
multiplication alone. The verified figures are stored in `data/hotels.json` as `fees_official` with the
source URL; the page arithmetic needs its owner to re-derive it. Left in place and flagged rather than
silently edited while another session owns the page.

## 4. Star counts: three different totals for the same city

- The shipped dataset has **72** starred restaurants (5 three-star, 15 two-star, 52 one-star).
- The current official all-starred directory displays **3 / 14 / 50 = 67** while its own result line says
  "1–48 of 69".
- The 2025 selection announcement is the source of the 72.

Published as NR-01. Effect on this work: the ranking counts starred restaurants from the local dataset, so
its "65 within 60 minutes" is a count against **72**, not against the Guide's current 67/69. The next
MICHELIN ceremony is **14 December 2026** — before the trip — so any tier can change before February.

## 5. Review links: search pages were labelled as reviews

All **261** social links in `data/michelin_all.json` and `data/activities.json` (72 restaurants × 3 and
15 activities × 3) are search or hashtag URLs: `youtube_search`, `tiktok_search`, `instagram_search`.
Not one is a specific post. A search page is not a review — it can show any venue, and its content changes.

What has been verified instead is recorded in **`data/review_links.json`**: for 8 restaurants and 1 museum, the specific video that was actually opened
(26 posts in all: 25 name the venue in their own title, one — a Sushi Sho documentary — films it without naming it)
, with its title, uploader, length, view count and URL as shown.
A link is only marked `specific-*` when the title or description names the venue. Everything else stays
labelled `search`. The remaining 78 venues still have no verified specific link.

### What proofreading the live page changed

Reading the deployed page rather than the local files found four defects that all checks had passed:

| Defect | Why the checks missed it | Fix |
|---|---|---|
| Every "hotel row" link pointed at `hotels.html#arlo-midtown`, but `hotels.html` renders its rows from JSON and has no row anchors — all nine links landed on the top of the page | `validate_site.py` checks that a local target exists, and `hotels.html` does; an anchor into a JS-rendered table does not, and nothing checked for that | links now go to `hotels.html`, and the client check no longer follows a fragment into a rendered table |
| The matrix header rendered **"The"** as a hotel, because the header took the first word of "The Mayfair Hotel" | no check reads a column header | leading article stripped, full name kept in the `title` attribute |
| The ranking said *"top four hotels sit within 0.8 minutes"* while the data shows **five** hotels within 0.8 (18.5→19.3) | the number was written in prose, not derived | the table now groups hotels whose medians are within the model's own resolution and labels them `tied #1–#5`, `tied #7–#8`, so the claim cannot drift from the data again |
| The 1-hour section still called the top order "close calls" on a 0.8-min threshold when the *stability* figure (spread across four departures) was 1.5–3.4 min | two different thresholds were conflated | ties now come from the ranking gap; instability gets its own flag, `moves N min by time of day` |

A fifth, cosmetic-but-confusing defect surfaced only after the second merge: the two status pills ran together
in the rendered cell (`tied #1–#5moves 2.7 min by time of day`) and the spread was printed twice, once in
the pill and once underneath. The cell now prints the spread once.

Also: the Sushi Sho documentary is labelled `venue not in the title`, because it films the restaurant without
naming it — the earlier wording implied every listed post named its venue.

## 5b. The ranking is a moving target, and the prose must move with it

The journey model and hotel list are shared files: between two of this branch's merges, another session grew
the input from 9 hotels and 29 measured restaurants to **14 hotels and 65 of 72**. The rendered table followed
the data; three pieces of hand-written prose did not, and the live page briefly said "ranks 1–5" while the
table showed fourteen hotels. Two of its own claims were then wrong in a way no validator can see:

- the tie sentence said "one tied group" when the real situation is a **chain**: with 14 hotels, no
  *neighbouring* pair is separable (each step is under 0.8 min) but the chain spans 1.9 min end to end. Saying
  "all tied" would have been the opposite error.
- the headline cards printed a hotel count and a restaurant count that came from the data.

The tie sentence is now computed from the ranking itself, and `scripts/check_rendered_tables.js` compares the
four headline numbers on `decide.html` against `data/hotel_ranking.json`, `data/blockers.json` and
`data/suggestions.json` (demonstrated by feeding it a wrong count, which it rejected).

## 6. Restaurant rows: what is still empty

| Gap | Count | Why it is still blank |
|---|---|---|
| Starred restaurants with no measured journey time | 7 of 72 (65 measured) | the record has no usable address, the Census geocoder could not resolve it, or no stop is inside the 500 m walk cap; guessing an address would fabricate a number |
| Starred restaurants with unverified opening hours | 45 of 72 | the Guide's hours panel did not render for these rows |
| Starred restaurants with no price for two | 62 of 72 | only the venue's own menu or booking engine publishes it |
| Hotel amenity lists not captured first-hand | 11 of 14 | the room pages were read; the amenity pages were not |
| Activity opening hours blank | 5 of 15 | same rendering problem on the operator's own page |

## 7. Prices are snapshots, not quotes

The 7-night totals are Booking.com rate snapshots captured on a stated date, before New York's 14.75%
hotel tax and the $4/night city tax. Five hotels have a captured tier (HGU $1,091.60 · Eurostars $1,127 ·
Hyatt Place $1,183 · Arlo $1,255 · Pestana $1,327); four have none and render `unverified` rather than a
guess. **Cheapest time to book** and **best time to book** cannot be established from a single snapshot —
a booking-timing claim would need a price history, which no official source publishes.

## 8. The journey model is a model

`data/transit_hotels.json` carries `_meta.is_modelled_estimate: true`. It runs the official MTA static GTFS
through a connection-scan algorithm at one sample departure (weekday 12:00), with fixed walk speeds and a
fixed transfer penalty. It is not a trip plan and not a 2027 timetable. One geocoding defect was found and
fixed: "46th St & 12th Ave" resolved to **Brooklyn 11219**, sending the Intrepid to 81 minutes; addresses
are now rejected when they land in the wrong borough.

## 9. A page could load every check and still not render

The suite validated data, links and generated rows, but nothing executed a page in a browser. A renderer
that throws, or a `fetch` path that no longer matches a file name, leaves the reader a permanent
"Loading…" panel with every check green. `scripts/smoke_pages.js` now loads all 10 root pages in a DOM,
runs their scripts in document order, serves the local JSON to `fetch`, fires `DOMContentLoaded` and fails
if any host still shows a placeholder or renders no source link. While wiring this up, section 3 of the
Decide page was found to be the one panel with no link at all; it now cites
`data/transit_hotels.json`, `data/hotel_ranking.json` and the method section.

## 10. Items awaiting another owner

- Hotels page: Pestana fee arithmetic (§3) and the Blue Angel address (§2).
- Flagged for Review page: the parked HGU domain in NR-02/NR-03 (§1).
- Restaurant and activity data: the 261 search links (§5) — replacement values are supplied in
  `data/review_links.json`, not written into files this session does not own.
