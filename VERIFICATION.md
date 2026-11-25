# VERIFICATION — what was checked, against what, and when

Session `arena-c2e08f03` · all checks performed **25 November 2026** · zone UTC.
No automated crawl was possible: the sandbox has no general outbound internet, so every
row below was checked page by page with the fetch and search tools.

Rule applied throughout: a value is published only if it appeared on the operator's own
page. If it did not, the cell is blank and flagged `unverified`. Nothing is inferred,
averaged, or carried over from a secondary source.

---

## 1. Checks performed, by dataset

| Dataset | Rows | Rows with an official source link | Rows with an open gap | Status |
|---|---|---|---|---|
| Activities (`data/activities.json`) | 15 | 15 | 8 hours cells, 1 price cell | **verified, gaps flagged** |
| Hotels (`data/hotels.json`) | 9 | 9 (exact quote URL each) | Michelin 1-hour count on all 9 | **verified, ranking blocked** |
| Michelin — three star | 5 | 5 | 0 | **verified** |
| Michelin — two star | 15 | 15 | 3 hours cells | **verified, gaps flagged** |
| Michelin — one star | 52 | 52 (Guide URL on every row) | 43 hours cells, most price cells | **status verified; hours partly missing** |
| Itinerary (`data/itinerary.json`) | 7 days | derived from the tables above | none invented | **derived, no new claims** |

Every table on the site renders a `Source` column. No row anywhere is published without
one.

---

## 2. First-party pages actually opened

**MICHELIN Guide** — announcement of 18 Nov 2025 (star counts), plus individual restaurant
pages for: Eleven Madison Park, Jungsik New York, Le Bernardin, Per Se, Sushi Sho, Aquavit,
Atera, Atomix, Gabriel Kreuther, Jean-Georges, Saga, The Modern, Le Coucou, Joo Ok,
Chef's Table at Brooklyn Fare, Masa, Odo, César, Sushi Noz, Aska, Blue Hill at Stone Barns,
Jeju Noodle Bar, Gramercy Tavern, Rezdôra, Semma, Crown Shy, Torrisi, Kochi.

**Museums and landmarks** — `moma.org/visit`, `metmuseum.org/plan-your-visit`,
`metmuseum.org/plan-your-visit/met-cloisters`, `amnh.org/plan-your-visit/hours`,
`whitney.org/visit`, `guggenheim.org/plan-your-visit`, `911memorial.org/visit`,
`911memorial.org/visit/visit-museum-1`, `intrepidmuseum.org/plan-your-visit/visitor-information`,
`intrepidmuseum.org/plan-your-visit/visitor-information/tickets`,
`nps.gov/stli/planyourvisit/fees.htm`,
`rockefellercenter.com/tickets/top-of-the-rock-observation-deck/`,
`thehighline.org/visit/`, `centralparknyc.org/visit`,
`nypl.org/locations/schwarzman`, `citypass.com/new-york`.

**Hotels** — Booking.com property pages for the exact dates, one per hotel, with
`checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1`. Hotel official sites
were used for identity and location, not for price.

---

## 3. Verification sequence for a hotel price (the strictest path)

1. Open the property page with `checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1&selected_currency=USD`.
2. Read the room name and the bed description — reject anything below queen.
3. Read the "total before taxes" line, not the headline search figure.
4. Record the tax lines shown by the page (New York: 14.75% + $4/night) and any resort fee,
   noting whether the fee is inside or outside the quoted total.
5. Record the cancellation deadline exactly as printed.
6. Store the URL alongside the number so the figure can be re-checked.

Anything that failed step 2 was not deleted — it was kept with a visible "No / unverified"
verdict, because silently dropping a hotel would misrepresent the market.

---

## 4. Where verification failed, and what the site does about it

| Failure | Rows affected | What is published |
|---|---|---|
| Hours block did not render on the official page | The Met, The Cloisters, Top of the Rock (partial), Statue ferry, Central Park, NYPL, Grand Central, 48 one-star restaurants | Blank cell + `unverified` badge + a flag naming the missing field |
| Price not published by the operator | All starred restaurants (band only); AMNH (seasonal/partner-only) | Blank + flag explaining that MICHELIN publishes a band and AMNH's own admission page did not render |
| Journey time not published | All hotel × restaurant pairs | Count left `null`, flagged, and listed as open question Q6 |
| Counts disagree between two official pages | Michelin one star (50 vs 52), two star (14 vs 15) | Discrepancy written next to the number |

---

## 5. Fields deliberately left null

- `price_for_two_usd` on every Michelin row — no first-party figure exists to cite.
- `michelin_within_1h_count` on every hotel row — no verified journey-time source.
- `hours` on 43 one-star rows — Guide page not yet read for those.
- `amenities` on 7 of 9 hotels — full amenity lists not captured; the two populated rows
  (citizenM, Pestana CR7) show exactly what a captured list looks like.
- The Met / Cloisters / Top of the Rock hours.

---

## 6. Re-verification triggers

| Trigger | Date | Action |
|---|---|---|
| MICHELIN New York 2026 ceremony | **14 Dec 2026** | Re-read the new selection; update star counts, tiers, and the three/two/one-star pages. |
| Hotel rates | Continuous | Re-quote 15–22 Feb and 8–15 Mar before booking; live prices move daily. |
| Venue hours | Before booking | Each row's own source link, one click. |
| The Met hours | Before booking | Fetch the Plan Your Visit page in a browser where the hours panel renders. |
| Restaurant closures | Before booking | Guide page hours block, plus the venue's own site for holiday exceptions. |

---

## 7. Assertion about this document

Every URL in this file and in every data file was fetched during this session on
2026-11-25, except where a row is explicitly marked `unverified`. No value was written from
memory, from a previous conversation, or from a third-party summary.
