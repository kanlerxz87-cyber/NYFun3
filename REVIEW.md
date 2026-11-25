# REVIEW — repo line-by-line against official sources

Session `arena-c2e08f03` · branch `arena/c2e08f03-nyfun3` · checked 2026-11-25.

Scope of this review: every file in the repository, plus every value published on the site,
checked against the official page named in its row. Third-party blogs, aggregators, listicles
and price-scraper sites were not accepted as sources at any point.

---

## 1. Repository inventory at review time

| Path | What it is | Verdict |
|---|---|---|
| `README.md` | Original stub: `# NYFun3` | **Irregularity R1** — no purpose, no run instructions, no source policy. Left untouched on purpose (shared file, not in this session's scope to rewrite without asking). |
| `.git` | Single initial commit `c251442` before this session | Clean; no unexpected history, no large objects, no committed secrets, no `.env`. |
| GitHub Pages | Source `main`, path `/`, HTTPS enforced | Correct for a static site. |
| `.gitignore` | Absent | **Irregularity R2** — nothing to ignore yet (no build step, no dependencies), but the absence should be deliberate rather than accidental. |
| Tests / CI | Absent | **Irregularity R3** — a site whose entire value is "every row has a source" has no automated check that links resolve. Recorded here, fixed only if approved (see `plan.html` suggestion S3). |

Files added by this session, each reviewed line by line:

`COORDINATION.md`, `data/michelin.json`, `data/michelin_two_star.json`,
`data/michelin_one_star.json`, `data/michelin_all.json`, `data/hotels.json`,
`data/activities.json`, `data/itinerary.json`, `assets/style.css`, `assets/app.js`,
`index.html`, `activities.html`, `restaurants.html`, `michelin.html`, `hotels.html`,
`itinerary.html`, `plan.html`, `REVIEW.md`, `VERIFICATION.md`.

---

## 2. Irregularities found

### R1 — README is a bare stub
`README.md` contains eight bytes of content and states nothing about the project, the
verification standard, or how to preview the site. Anyone picking this repo up cold cannot
tell what it is. **Not fixed** in this pass because `README.md` predates the session and
rewriting shared documentation without approval would violate the coordination rules.

### R2 — No `.gitignore`
No build artefacts exist today, so nothing is currently leaking into Git. If a bundler or
`node_modules` is ever introduced this becomes a real problem.

### R3 — Nothing verifies the verification
The central promise of the site is "every row has an official source link". There is no
link checker and no schema check. A stale Michelin URL would be invisible.

### R4 — Branch-name convention conflict
The repo protocol asks for `session-<id>/<task>` branches. The session is pinned by the
harness to `arena/c2e08f03-nyfun3` and cannot create or switch branches. Logged in
`COORDINATION.md`; the resolution is to merge that branch into `main` at integration.

### R5 — Michelin one-star count does not reconcile
MICHELIN's own New York filter reports **50** one-star restaurants in NYC. Its 18 November
2025 announcement lists **52** one-star names, two of which are outside the NYC filter
(La Bastide by Andrea Calstier is in North Salem, Westchester). The site publishes the
announcement's 52 and states the discrepancy next to the number rather than quietly
choosing one.

### R6 — Michelin two-star count does not reconcile either
The NYC filter says **14**; the announcement names **15**. The fifteenth is Blue Hill at
Stone Barns in Tarrytown — a 40-minute Metro-North ride, not a subway trip. Published with
the same explicit note.

### R7 — The stars will be out of date before the trip
The 2025 selection is current as of 25 Nov 2026. The next New York ceremony is
**14 December 2026**, five weeks before the preferred travel window. Every page carries the
caveat; the star cells are not claimed as final.

### R8 — Michelin publishes no price, only a band
`$`–`$$$$` is a band, not a number. A "cost per couple" figure cannot be derived from it
without inventing a number. The column is therefore blank and flagged. This is the single
biggest gap against the original brief.

### R9 — Starred restaurant sites are JavaScript apps
`le-bernardin.com` and `jean-georges.com` return no menu prices to a text fetch. Several
others gate menus behind a reservation flow. This is *why* R8 stands rather than being
worked around.

### R10 — Third-party price sites contradict each other
Menu-price aggregators disagreed with one another on the same dish at the same restaurant,
and disagreed with the restaurants' own descriptions. They are excluded as sources; no
number on this site comes from one.

### R11 — Booking.com is an OTA, not a price publisher
The hotel totals are live rate cards, not published rack rates. They are recorded with the
exact URL (check-in, check-out, `group_adults=2`) and a capture date so any figure can be
reproduced or refuted. This is a methodological caveat, not a data error.

### R12 — Cheapest-search-card price ≠ cheapest compliant room
Two hotels looked cheap on the search card because the cheapest tier is a full/double bed
(The Mayfair, Blue Angel) — both fail the queen-or-larger requirement. One "Pod Bunk" twin
product at roughly $700 was excluded for the same reason. The cheapest figure and the
cheapest *compliant* figure are shown as different things.

### R13 — One hotel's cheapest king is the ADA room
Pestana CR7's lowest king rate card is the ADA-accessible Superior King. If accessibility
features are not needed, that specific card must not be booked. Flagged inline on the row.

### R14 — The Met's hours block would not render
The hours panel on `metmuseum.org/plan-your-visit` did not appear in the fetched page text
across four attempts on two URLs. The Met and The Cloisters hours cells are blank and
flagged rather than copied from a third party.

### R15 — The Cloisters breaks the 1-hour rule
The Met's own directions page states the M4 bus from Fifth Avenue to The Cloisters takes
about **1 h 25 min**. It is therefore listed as a half-day excursion and marked as failing
the ≤1 hour constraint — a constraint that is otherwise applied to every activity.

### R16 — "Michelin within 1 hour" cannot be computed from any verified source
The ranking you asked for (hotels ranked by count of Michelin restaurants within ~1 hour)
needs a journey time per hotel × restaurant pair. No official page publishes those, and
estimating them would violate the "never infer" rule. The column is blank, flagged, and
listed as open question Q6 with a concrete method to fill it (MTA trip planner, one query
per pair, timestamped).

### R17 — NPS fee page vs. operator page
`nps.gov/stli/planyourvisit/fees.htm` publishes the ferry prices and states plainly that NPS
charges no entrance fee and that Statue City Cruises is the only authorised operator. It
also warns that unauthorised ticket sellers at The Battery are a known scam. Both facts are
surfaced on the activity row.

### R18 — 9/11 Museum is not open seven days
It is open Wednesday–Monday plus *select* Tuesdays, with a last entry of 17:30 and
mandatory advance timed tickets. The itinerary places it on a Wednesday for this reason.
The outdoor Memorial is free and daily 08:00–20:00 — a genuinely free alternative.

### R19 — Winter hours change the plan
The High Line runs 07:00–20:00 from 1 Dec to 31 Mar, so the whole trip window is on winter
hours. The Intrepid is on fall/winter hours (10:00–17:00, last entry 16:00) until 31 March.
Both are recorded as seasonal notes rather than as a single weekday cell.

### R20 — No indoor fallback exists yet for weather-exposed days
Central Park, the High Line and the Statue ferry have no verified indoor substitute on the
site. For a February trip that is a real planning hole; it is open question Q11.

---

## 3. What was *not* reviewed, and why

- **Bib Gourmand and "listed but not starred" Michelin venues.** The 2025 selection includes
  ~76 Bib Gourmand entries. Not catalogued yet; proposed as suggestion S4.
- **Broadway / Off-Broadway, The Edge, Circle Line, Chelsea Market, Brooklyn Bridge walk.**
  Plausible additions, but no first-party price or hours page was verified for them in this
  pass, so they were left out rather than listed without a source.
- **Airline, airport transfer and MetroCard/OMNY fares.** Out of the stated scope; also not
  verified.
- **Restaurant reservation windows.** Not captured; proposed as suggestion S8.

---

## 4. Per-file notes

| File | Note |
|---|---|
| `data/michelin.json` | 5 three-star + 7 two-star with full hours from Guide pages. Validates as JSON, 12 records. |
| `data/michelin_two_star.json` | All 15 two-star records; 7 overlap the file above and were merged by name in `michelin_all.json`, not duplicated at render time. |
| `data/michelin_one_star.json` | 52 one-star rows. Where the Guide page was not fetched, hours and website are blank with an explicit flag — 48 of 52 rows still need their hours captured. **This is the largest known gap.** |
| `data/michelin_all.json` | Merged, de-duplicated, filterable source for the Michelin and Restaurants pages. 72 rows. |
| `data/hotels.json` | 9 hotels, all with the exact quote URL. Michelin-proximity count deliberately null. |
| `data/activities.json` | 15 activities; 1 row carries an unverified price (AMNH), 8 rows carry an unverified or seasonal hours cell (2 of those are seasonal-by-design: the High Line and the Statue ferry). |
| `data/itinerary.json` | Derived only from verified activity hours; no invented travel times. |
| `index.html`, `assets/` | Static, no build step, no external JS. Renders on GitHub Pages as-is. |
| `assets/app.js` | All rendering escapes text before insertion; no `innerHTML` of raw remote data. |

---

## 5. Honest summary

The repository is in good shape structurally: static, dependency-free, mobile-first, and
every published value traces to an official page. The three things that genuinely limit the
deliverable are (a) no verified per-couple restaurant prices, (b) no computed Michelin
proximity ranking, and (c) 48 one-star rows whose hours have not yet been read off their
Guide pages. All three are stated on the site rather than papered over.
