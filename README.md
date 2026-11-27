<a id="trip-brief"></a>
# NYC Trip Planner — February/March 2027

A static, mobile-first planning dashboard for a two-adult New York City trip in the window
**15 Feb – 23 Mar 2027** (preferred start 15–18 Feb 2027).

**Live site:** https://kanlerxz87-cyber.github.io/NYFun3/

No build step, dependencies, or framework. The primary dashboard is plain HTML with JSON data loaded at runtime; the supplemental dossier has a separate stylesheet and small progressive-enhancement script.

## Pages

| Page | What it holds |
|---|---|
| `index.html` | Dashboard: what exists, how to read the tables, known limitations. |
| `activities.html` | 15 museums, parks, landmarks and passes — weekday hours, exceptions, adult prices, review searches. |
| `restaurants.html` | Starred restaurant shortlist, filterable by area and tier. |
| `michelin.html` | The 72-row 2025 MICHELIN Guide release dataset (5 ★★★ / 15 ★★ / 52 ★), with per-row status labels and cluster counts. This is a preserved release snapshot, not the current NYC directory: the official directory showed 69 (5 / 14 / 50) on 27 Nov 2026; see the explicit scope caveat and review queue. |
| `guide-2026.html` | Current starred vs Bib Gourmand vs Guide-listed tiers, 15 verified venues, clusters, hotel audit, and official 2-adult totals. |
| `hotels.html` | 14 properties with 7-night direct/third-party totals for 15–22 Feb 2027, private-bathroom and queen-bed checks, seasonality, and current-timetable GTFS reach. |
| `itinerary.html` | 7-day plan sequenced around published closures. |
| `plan.html` | Executive summary, reviewable suggestions, open questions, and irregularities found. |
| `decide.html` | Current 69-venue MICHELIN transit comparison, restaurant route matrix, separate activity-route baseline, open questions, and reviewable suggestions. |
| `flagged-for-review.html` | Published NR-01–NR-10 `needs review` queue, resolved source corrections, official starting sources, and next checks. |
| `pages/index.html` | Supplemental curated dossier: itinerary, hotel snapshots, dining/menu arithmetic, attraction hours, and research notes. |

Supporting documents: `REVIEW.md` (repo review, irregularities R1–R25, with final-integration resolutions), `EVIDENCE_AUDIT.md`, `FLAGS.md`,
`VERIFICATION.md` (what was checked, against which page, and when), `RESEARCH.md`
(the supplemental dossier source/method log), and `CURRENT_AUDIT.md` (27 Nov 2026 decision-readiness
audit and independent source corrections). The nested `pages/` dossier complements the
data-driven root site; it does not replace the existing JSON datasets or star/activity tables.
The root `.nojekyll` file keeps the linked Markdown research log available to GitHub Pages as-is.

## The rule this repo is built on

> Official venue, hotel-room, museum, award, and transit facts need a linked primary source.
> Unknown official facts remain blank and flagged — never inferred or estimated.

For live hotel availability, the dashboard can show date-specific Booking.com observations;
those are explicitly marked as **third-party snapshots**, linked to their query, and are not
represented as official hotel quotes or guaranteed all-in prices. The supplemental `pages/`
dossier also includes selected published restaurant-menu arithmetic and creator-review leads;
menu estimates are not final bills, and social links are not treated as factual authorities.

Several gaps remain visible: the primary MICHELIN table is only a partial per-couple menu-cost
catalogue (25 selected rows have explicit `2 × official per-person price` arithmetic; 47 remain
blank + `unverified`), restaurant sites may not expose menu data, and no official source publishes
subway times per hotel/restaurant pair. The figures that are published are paired with
menu/FAQ/PDF links and an exclusions caveat; they are not quoted all-in totals or 2027 price
guarantees. Each gap is listed rather than papered over with a plausible number. The
review queue on `flagged-for-review.html` currently covers NR-01–NR-10; earlier notes may still
refer to the prior NR-01–NR-09 count.

## Data files

| File | Contents |
|---|---|
| `data/activities.json` | 15 activities, each with `source_url`. |
| `data/hotels.json` | 14 hotels, each with official/first-party and exact-date quote links where available. |
| `data/michelin.json` | 5 three-star + 7 two-star, full detail. |
| `data/michelin_two_star.json` | All 15 two-star records. |
| `data/michelin_one_star.json` | All 52 one-star records. |
| `data/michelin_all.json` | Merged, de-duplicated source used by the site (72 rows). |
| `data/itinerary.json` | 7-day plan plus 3 second-week suggestions, derived from source-linked activity data. |

## Preview and validation

```sh
python3 -m http.server 8000 --bind 0.0.0.0
# then open http://localhost:8000/ in your own browser (local preview only)
python scripts/validate_site.py
python scripts/check_sources.py
python scripts/check_inline_js.py
node scripts/check_rendered_tables.js
npm install --no-save --no-package-lock --no-audit --no-fund jsdom
node scripts/smoke_pages.js
```

Opening `index.html` directly from disk will not work: browsers block `fetch()` of local JSON
over `file://`. Any static server is fine. The validators check JSON schemas, official source links, local links/anchors, navigation,
table Source columns, and `2 × official per-person` arithmetic; `check_sources.py` also compares
the current transit ranking against the hotel-page values. The JavaScript checker runs
`node --check` on every script; the rendered-table harness executes each data renderer with a
minimal DOM stub and checks every generated row for a source link. The recursive jsdom smoke test
executes root and nested HTML pages, including the dossier. CI installs jsdom and runs the full suite
on pushes and pull requests.

## Verification status (27 November 2026)

- **Star scope:** the official MICHELIN NYC-and-surroundings all-starred directory currently displays 5 three-star, 14 two-star, and 50 one-star entries (69 total; checked 27 Nov 2026). The separate [18 Nov 2025 New York selection release](https://guide.michelin.com/us/en/article/michelin-guide-ceremony/all-the-stars-in-the-michelin-guide-to-new-york-city-2025) is preserved as a 72-row dataset (5 / 15 / 52). These are different source snapshots/scopes; the repository does not silently reconcile them. The [officially announced 2026 New York ceremony](https://michelinmedia.com/pages/blog/detail/article/c/a1479/) is scheduled for **14 Dec 2026**, before the trip, so re-check every restaurant's current status after that date. See the [live starred directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred), [Guide comparison](guide-2026.html), and [Flagged for Review](flagged-for-review.html).
- **Hotel prices:** date-specific direct quotes and Booking.com observations are captured with links and capture dates. OTA observations are third-party snapshots, not guaranteed totals; rates, availability, room tier, cancellation rules, taxes, and fees can change. Recheck the actual dates and selected room at checkout.
- **Transit comparison:** the current hotel ranking uses the 69-venue active NYC directory snapshot and current MTA Subway GTFS route model. Every hotel reaches 69/69 venues within 60 minutes in that model, so compare median travel time only as a secondary factor to price and room fit. The older 65/72 2025-selection dataset is separately labeled as an activity-route baseline. Neither result guarantees Feb/Mar 2027 operations; verify Presidents’ Day and planned service near travel using the [MTA schedule guidance](https://www.mta.info/developers/gtfs-schedules-transition).
- **Other data gaps:** 71 of 72 2025-release rows have current MICHELIN Guide weekday hours; one closed venue remains blank/flagged. These are not a promise of Feb/Mar 2027 opening. The 72-row dataset has 25 first-party menu subtotals for two and 47 blank/unverified price rows. Hotel rates and some room/amenity facts still need exact-checkout confirmation. The [review queue](flagged-for-review.html) lists these gaps.

## Contributing / parallel sessions

Read `COORDINATION.md` first. It holds the task board, the claim protocol and the file-scope
rules. Shared outputs (the combined data files, `index.html` nav, and the `main` publish) are
changed only by the integration session.
