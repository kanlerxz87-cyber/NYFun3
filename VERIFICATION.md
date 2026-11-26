# VERIFICATION — what was checked, against what, and when

Session `arena-c2e08f03` · all checks performed **25 November 2026** · zone UTC.
Final integration by `ed92e764` on the same date merged the supplemental dossier and
official-source diagnostics, refreshed selected first-party facts, and added automated
validation. This log records the original manual checks; the final-integration notes below
update claims that changed.

No automated crawl was possible during the original review: the sandbox had no general
outbound internet, so every row below was checked page by page with the fetch and search
tools. The later diagnostics workflow added read-only direct fetches, while the final site
validator checks schema/link/anchor/source-column consistency offline.

Rule applied throughout: a value is published only if it appeared on the operator's own
page. If it did not, the cell is blank and flagged `unverified`. Nothing is inferred,
averaged, or carried over from a secondary source.

---

## 1. Checks performed, by dataset

| Dataset | Rows | Rows with an official source link | Rows with an open gap | Status |
|---|---|---|---|---|
| Activities (`data/activities.json`) | 15 | 15 primary + separate official-hours links | 5 hours cells, 1 price cell in final integration | **verified, gaps flagged** |
| Hotels (`data/hotels.json`) | 9 | 9 (exact quote URL each) | Michelin 1-hour count on all 9 | **verified, ranking blocked** |
| Michelin — three star | 5 | 5 | 0 | **verified** |
| Michelin — two star | 15 | 15 | 3 hours cells | **verified, gaps flagged** |
| Michelin — one star | 52 | 52 (Guide URL on every row) | 43 hours cells; 48 blank price cells, 4 selected menu-price rows | **status verified; hours partly missing** |
| Itinerary (`data/itinerary.json`) | 7 days | derived from the tables above | none invented | **derived, no new claims** |

Final integration now enforces the original claim as a checked invariant: every static and
dynamically rendered table has a `Source` column and every body row has at least one link.
`scripts/validate_site.py` fails CI when a static body row has no link, when a dynamic
renderer loses its source logic, or when a local link/anchor is broken;
`scripts/check_rendered_tables.js` executes the five root renderers against the current JSON
and checks every generated body row for a source link, priced-row menu link, and exclusions
caveat. Header-only rows are not data rows. `flagged-for-review.html` publishes all eight `needs review` items with source
links.

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
`nypl.org/locations/schwarzman`, `citypass.com/new-york`, `nps.gov/stli/planyourvisit/hours.htm`,
`grandcentralterminal.com/visit/`, `centralparknyc.org/visit`, `centralparknyc.org/alerts`.

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
| Hours block did not render on the official page | Final integration: The Met, The Cloisters, Top of the Rock (partial), NYPL, 43 one-star restaurants | Blank cell + `unverified` badge + a flag naming the missing field |
| Official baseline captured but not a 2027 calendar | NPS Statue/Liberty Island park, High Line winter hours, Central Park, Grand Central, AMNH, MoMA, Whitney, Guggenheim, Intrepid, 9/11 | Baseline hours cell + explicit "not a 2027 calendar confirmation" note + official hours link |
| Venue publishes a first-party menu/FAQ/PDF price | 10 selected starred restaurants | `2 × official per-person price` arithmetic, menu/FAQ/PDF link, exclusions caveat, and "not a quoted all-in total or 2027 price" flag |
| Price not published by the operator | 62 starred restaurants (band only); AMNH (seasonal/partner-only) | Blank + flag explaining that MICHELIN publishes a band and AMNH's own admission page did not render |
| Journey time not published | All hotel × restaurant pairs | Count left `null`, flagged, and listed as open question Q6 |
| Counts disagree between two official pages | Michelin one star (50 vs 52), two star (14 vs 15) | Discrepancy written next to the number |

---

## 5. Fields deliberately left null

- `price_for_two_usd` on 62 of 72 Michelin rows — no first-party figure exists to cite. The
  10 populated rows are simple arithmetic from a linked official per-person menu price, not an
  all-in quote.
- `michelin_within_1h_count` on every hotel row — no verified journey-time source.
- `hours` on 43 one-star rows — Guide page not yet read for those; 45 of 72 Michelin rows
  still lack a full hours dict.
- `amenities` on 7 of 9 hotels — full amenity lists not captured; the two populated rows
  (citizenM, Pestana CR7) show exactly what a captured list looks like.
- The Met / Cloisters / Top of the Rock / NYPL full building hours.
- 2027 holiday exceptions and date-specific transit schedules.

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

Every URL used for a published value in the original data files was fetched during this
session on 2026-11-25, except where a row is explicitly marked `unverified`. Final
integration additionally fetched the official menu/FAQ/PDF and hours pages named in `RESEARCH.md`
and `research/sources.md`; no value was written from memory, from a previous conversation,
or from a third-party summary. The offline validator does not re-fetch the web: it enforces
that a source URL, schema field, local target, and anchor remain present and syntactically valid.

## 8. Final publish check (25 November 2026, session `ed92e764`)

PR #4 merged the final integration into `main` as `0a2eafe` after the `Validate static site` workflow succeeded (run `45722618504`; all seven job steps passed). PR #5 merged the final page-copy reconciliation as `0b9ec96`, with its validation check also passing. GitHub Pages reported `status: built` with no error for both commits; the latest build completed 23:39:31 UTC. The published root dashboard, Flagged for Review page, executive summary, dossier findings, Restaurants, Michelin, and Itinerary pages were fetched from `https://kanlerxz87-cyber.github.io/NYFun3/` and showed the expected Source columns, review queue, official-menu arithmetic, and itinerary source links. A cache-busted refetch after the second build confirmed the reconciled Restaurants introduction. No factual value changed in PR #5.

## 9. Computed subway access (26 November 2026, session `67e5a326`)

**T14 — hotel × starred-restaurant subway access.** Method: (1) addresses taken as captured in
`data/hotels.json` and `data/michelin_all.json` (no address was invented; 39 starred rows have no
captured address and are listed as excluded in `data/transit.json` and `research/generated/transit_analysis.json`);
(2) geocoded with the US Census Bureau batch geocoder, benchmark `Public_AR_Current`, with a
single-address retry pass (periods stripped, then street abbreviations expanded — deterministic string
normalisation only; no coordinates were guessed). Two rows return Census `No_Match` and stay excluded:
Blue Hill at Stone Barns (630 Bedford Rd., Tarrytown, NY 10591) and Le Pavillon (1 Vanderbilt Ave., New York, NY 10017);
(3) travel time computed on the **current** official MTA subway GTFS feed (`https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip`),
edge weight = **median** scheduled stop-to-stop running time per serving trip, transfer penalty 480 s,
first-boarding allowance 300 s; (4) walking model: haversine × 1.3 detour factor at 75 m/min from the hotel to
the six nearest stations within 2.5 km and from the arrival station to each restaurant; (5) Blue Hill at Stone Barns
is additionally excluded from the time model because straight-line distance exceeds 25 km (beyond subway
service area; Metro-North required, not modelled).

Outputs: `data/transit.json` (site-ready), `research/generated/transit_analysis.json` (full evidence: 81 geocodes,
station graph stats, per-hotel per-restaurant minutes). Generator: `research/scripts/transit_analysis.py`, run by
`.github/workflows/transit-analysis.yml` on GitHub Actions (runs `45830340621`, `45831132436`,
`45832310175` — all concluded success; results committed by the runner as `a8ca418`, `faab030`, `e8b4085`).

**Result:** Artezen Hotel, Hyatt Place Chelsea, Blue Angel Hotel, citizenM Times Square, The Mayfair Hotel and
HGU New York reach 31/31 geocoded starred venues within 60 minutes; Arlo Midtown and Pestana CR7 Times Square reach
30/31 (Aska, 47 S. 5th St. Brooklyn, is >60 min for both under the model); Eurostars Wall Street reaches 31/31 but
only 19 within 30 minutes. Per-hotel ≤30/≤45/≤60 tier splits are in `data/transit.json` and on `transit.html`.

**Honesty scope, restated:** current GTFS is **not** a Feb–Mar 2027 timetable; no bus service is modelled (the result
is therefore a lower bound for the user's "subway or bus" rule); competitor claims about exact 2027 journey times were
not made anywhere on the site. `hotels.json` now carries `michelin_within_1h_count` (int), `michelin_count_denominator`,
`michelin_count_detail`, `michelin_count_method`, `michelin_count_flag` — the CI validator enforces that a non-null
count carries a GTFS method note. NR-04 remains `needs review` on the Flagged for Review page with the computed
caveat folded in.

## 10. Review links on priority rows (26 November 2026, session `67e5a326`)

**T15.** 25 priority rows (10 priced starred restaurants — Eleven Madison Park, Le Bernardin, The Modern, Masa, COTE,
Aquavit, Daniel, Gramercy Tavern, Le Coucou, Rezdôra — and all 15 activities) now carry dated, found-by-search creator
links (YouTube; TikTok where the search surfaced one) recorded in each row's `review_links` array with `found_on:
2026-11-26` and a `review_links_note` stating these are creator content, not official sources and not endorsements.
Every row keeps the pre-existing YouTube/TikTok/Instagram **search** links as a fallback. Creator links were gathered
with the web search tool on 2026-11-26; they are not fetched or endorsed by this repo, and no star/hours/price row
changed as a result. Full link list: `data/michelin*.json` and `data/activities.json` (`review_links` per row).

Files changed: `assets/app.js` (new `NYF.reviewCell`), `restaurants.html`, `michelin.html`, `activities.html`
(found links rendered first, search links labelled "search:"), plus a visible footnote on all three pages.
