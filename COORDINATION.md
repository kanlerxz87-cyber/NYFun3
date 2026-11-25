# COORDINATION — NYFun3 Trip Planning Site

Shared task board. Read this before starting work. This file was combined by final integration after three add/add/content conflicts; no session's board or work log was discarded.

- **Repo:** `kanlerxz87-cyber/NYFun3`
- **Live site:** https://kanlerxz87-cyber.github.io/NYFun3/ (GitHub Pages, source = `main`, `/` root)
- **Board last updated:** 2026-11-25 UTC
- **Phase A:** `arena-c2e08f03`, pinned branch `arena/c2e08f03-nyfun3`
- **Phase B / source diagnostics:** `ed92e764`, pinned branch `arena/ed92e764-nyfun3`
- **Phase C / supplemental dossier:** `arena-61fbe157`, pinned branch `arena/61fbe157-nyfun3`
- **Current Arena branch:** `arena/ed92e764-nyfun3`; base `c251442d122a8d04aade3d8b5a0d57fd4e9ce37c`

## Rules in force

1. Claim a task by writing session ID + file scope here, then commit and push the claim immediately.
2. Never start a task another session has claimed.
3. Keep scopes non-overlapping; edit only claimed files.
4. Log a request in this board if a task needs a file owned by another session.
5. Small, frequent commits; `git pull --rebase` before every push.
6. Shared outputs (`data/*.json`, root navigation, Pages publishing) are changed only by the final integration session after other tasks are done.
7. Official venue, hotel-room, award, and transit facts need a primary-source link. Date-specific Booking.com rates are labeled third-party snapshots with capture date and fee/tax caveats; they are not official guaranteed totals. Unknown facts stay blank and flagged `unverified`; never infer values.
8. `needs review` means published on the **Flagged for Review** page and does not block anything.
9. Claims older than 60 minutes with no commits may be taken over; note the handoff.

## Branch-naming irregularity

The protocol asks for `session-<id>/<task>` branches. All Arena sessions are pinned to fixed `arena/<id>-nyfun3` branches and cannot create or switch branches. Resolution: non-overlapping file scopes are recorded here; each phase merged to `main` through GitHub, and the final review publishes through a pull request from the fixed branch to `main`. No session pushes directly to another branch.

## Task board

| ID | Task | Status | Owner session | File scope |
|---|---|---|---|---|
| T1 | Repo review + irregularity log | `done` | `arena-c2e08f03` | `REVIEW.md` |
| T2 | Michelin dataset, official list, star links | `done` | `arena-c2e08f03` | `data/michelin*.json`, root Michelin/Restaurants pages |
| T3 | Hotel pricing and room-fit comparison | `done` | `arena-c2e08f03` | `data/hotels.json`, root Hotels page |
| T4 | Activities with hours, exceptions, prices, review searches | `done` | `arena-c2e08f03` | `data/activities.json`, root Activities page |
| T5 | Root dashboard shell, navigation, CSS, executive summary | `done` | `arena-c2e08f03` | `index.html`, `assets/style.css`, `assets/app.js` |
| T6 | 7-night itinerary and extended-stay notes | `done` | `arena-c2e08f03` | `itinerary.html`, `data/itinerary.json` |
| T7 | Open questions and missing-information plan | `done` | `arena-c2e08f03` | `plan.html` §4 |
| T8 | Reviewable suggestions / decision paths | `done` | `arena-c2e08f03` | `plan.html` §3 |
| T9 | Line-by-line verification log | `done` | `arena-c2e08f03` | `VERIFICATION.md` |
| T10 | First Pages integration and live checks | `done` | `arena-c2e08f03` | `main` publish |
| T11 | Supplemental curated dossier with official menu arithmetic, room-fit comparisons, source/method log | `done` | `arena-61fbe157` | `pages/**`, `RESEARCH.md`, `assets/css/site.css`, `assets/js/site.js`, root dashboard dossier link |
| T12 | Official-source diagnostics and MTA/Hyatt/MICHELIN access ledger | `done` | `ed92e764` | `research/**`, `.github/workflows/research-diagnostics.yml` |
| T13 | Final integration: merge all branches, re-verify combined data, add Flagged for Review page, link/schema validation, PR to `main`, Pages build check | `in progress` | `ed92e764` | shared outputs, `review.html`, `scripts/**`, `COORDINATION.md`, `README.md`, PR to `main` |

## `needs review` items — published on Flagged for Review page

| ID | Item | Status | Official source link |
|---|---|---|---|
| NR-01 | 2027 MICHELIN star status is not yet knowable; re-check after the 14 Dec 2026 ceremony | `needs review` | [MICHELIN 2025 announcement](https://guide.michelin.com/us/en/article/michelin-guide-ceremony/all-the-stars-in-the-michelin-guide-to-new-york-city-2025) |
| NR-02 | Hotel rates are Booking.com third-party snapshots, not official hotel quotes | `needs review` | [GitHub Pages API](https://api.github.com/repos/kanlerxz87-cyber/NYFun3/pages) · [HGU official site](https://www.hgunewyork.com/) |
| NR-03 | Cheapest upcoming time to book / best time to book remain unverified | `needs review` | [HGU exact-date quote](https://www.booking.com/hotel/us/hgu-new-york.html?checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1&group_children=0&selected_currency=USD) |
| NR-04 | 2027 one-hour transit counts are unverified; current GTFS cannot be extended | `needs review` | [MTA schedule-transition guidance](https://www.mta.info/developers/gtfs-schedules-transition) |
| NR-05 | 48 one-star hours cells, Met/Cloisters/NYPL building hours remain blank where official hours did not render | `needs review` | [MICHELIN NYC directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants) · [The Met visit page](https://www.metmuseum.org/plan-your-visit) |
| NR-06 | Bib Gourmand and merely Guide-listed venues are not fully catalogued | `needs review` | [MICHELIN NYC directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants) |
| NR-07 | 2–4-week hotel pricing and 2027 date-specific admission totals are not captured | `needs review` | [Hyatt Midtown-South official site](https://www.hyatt.com/hyatt-place/en-US/nyczm-hyatt-place-new-york-midtown-south) |
| NR-08 | Direct official hotel APIs/pages did not expose exact-date totals; diagnostics recorded blocks | `needs review` | [Hyatt Midtown-South official site](https://www.hyatt.com/hyatt-place/en-US/nyczm-hyatt-place-new-york-midtown-south) |

## Work log — Phase A (`arena-c2e08f03`)

**Built:** root dashboard (`index.html`), category pages, `assets/style.css`, `assets/app.js`, `data/activities.json` (15), `data/hotels.json` (9), `data/michelin*.json` (72 starred rows), `data/itinerary.json` (7 days), `plan.html`, `REVIEW.md`, `VERIFICATION.md`, and `README.md`. Live Pages build was checked; all seven root pages rendered with populated tables. Hotel ordering and cluster honesty fixes were applied after live inspection.

**Sources:** [MICHELIN 2025 New York star announcement](https://guide.michelin.com/us/en/article/michelin-guide-ceremony/all-the-stars-in-the-michelin-guide-to-new-york-city-2025), individual Guide pages, first-party museum/landmark pages, hotel official sites, and Booking.com exact-date quote URLs. See `VERIFICATION.md` for row-by-row links.

**Irregularities:** bare README (later replaced), no `.gitignore` (later added), no automated link checker, branch naming conflict, MICHELIN 50-vs-52 and 14-vs-15 count discrepancies, 14 Dec 2026 ceremony before trip, price bands vs dollar totals, blocked JavaScript menus, Booking.com OTA status, third-party hour disagreements. Details in `REVIEW.md`.

## Work log — Phase B (`ed92e764`)

**Built:** `research/sources.md`, `research/verification-log.md`, `research/scripts/diagnose.py`, `research/scripts/diagnose_reader.py`, `.github/workflows/research-diagnostics.yml`, and committed `research/generated/*.json` diagnostics.

**Sources:** [MICHELIN NYC directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants), [MICHELIN all-starred directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred), [MTA Developer Resources](https://www.mta.info/developers), [MTA schedule-transition guidance](https://www.mta.info/developers/gtfs-schedules-transition), [Hyatt Midtown-South](https://www.hyatt.com/hyatt-place/en-US/nyczm-hyatt-place-new-york-midtown-south), [Hyatt Times Square](https://www.hyatt.com/hyatt-place/en-US/nyczt-hyatt-place-new-york-city-times-square), [Hilton Times Square Central](https://www.hilton.com/en/hotels/nycssgi-hilton-garden-inn-new-york-times-square-central/), [Marriott Fairfield Times Square South](https://www.marriott.com/hotels/travel/nycmw-fairfield-inn-and-suites-new-york-manhattan-times-square-south/), [IHG Times Square South rooms](https://www.ihg.com/holidayinnexpress/hotels/us/en/new-york/nycts/hoteldetail/rooms), [GitHub Pages API](https://api.github.com/repos/kanlerxz87-cyber/NYFun3/pages), and [U.S. Census geocoder](https://geocoding.geo.census.gov/geocoder/locations/onelineaddress).

**Verification performed:** a read-only GitHub Actions collector opened official MTA GTFS feeds and Census geocoder successfully: subway 5,606,305 bytes / 1,488 stops; Manhattan bus 8,322,100 / 1,823; Brooklyn bus 17,046,285 / 4,575; Queens bus 5,983,145 / 1,422. High Line, NPS, and Empire State Building pages also opened. Evidence is in `research/generated/diagnostics.json`.

**Irregularities:** `workflow_dispatch` 404 on non-default branch; Hyatt 403; MICHELIN list 202 with zero links; museum bot checks 403/429/405; Jina Reader browser HTML 401; artifact download blocked by sandbox host allowlist. No blocked page's values were published or inferred.

## Work log — Phase C (`arena-61fbe157`)

**Built:** a mobile-friendly supplemental dossier under `pages/` (`index`, `itinerary`, `hotels`, `dining`, `experiences`, `findings`), `assets/css/site.css`, `assets/js/site.js`, `RESEARCH.md`, and a link from the root dashboard. It adds curated restaurant hours/menu arithmetic for eight selected candidates, hotel room-fit comparisons, direct TikTok review samples, attraction/hour findings, and a source/method log.

**Sources:** official menu/hours pages for [Le Bernardin](https://www.le-bernardin.com/content/pdfs/dinner-1.2.pdf), [The Modern](https://www.themodernnyc.com/the-modern/), [COTE](https://www.cotekoreansteakhouse.com/nycdinnermenu), [Rezdôra](https://www.rezdora.nyc/menus/), [Gramercy Tavern](https://www.gramercytavern.com/dining-room-menu/), [Crown Shy](https://www.crownshy.nyc/menus/), plus [Ruffian](https://ruffiannyc.com/) and [Sushi Akira](https://sushiakiranyc.com/about), [MTA app guidance](https://new.mta.info/guides/apps), and official attraction pages. See `RESEARCH.md` for the complete list.

**Irregularities:** preferred 15–18 Feb is only three nights while the priced test stay is seven nights; The Met and MoMA hours were captured from official pages but need 2027 confirmation; SUMMIT opening-time discrepancy; Sushi Akira homepage/About hours conflict; High Line live homepage vs winter visitor-page hours; official hotel pages did not expose exact-date totals; Booking.com remains third-party. Details in `RESEARCH.md` and `pages/findings.html`.

## Cross-session requests and conflicts

| Date UTC | From | To / file | Request / conflict | Resolution |
|---|---|---|---|---|
| 2026-11-25 | `ed92e764` | Phase A shared outputs on `main` | Final review needs the root dashboard and data | Merged `origin/main` into fixed branch. |
| 2026-11-25 | `ed92e764` | `COORDINATION.md` | Add/add and content conflicts because three sessions created/updated the board | Combined board preserves all task boards, work logs, source lists, verification notes, and irregularities. |
| 2026-11-25 | `arena-61fbe157` | root `index.html` | Add dossier link | Link present in root dashboard; retained in final integration. |
| 2026-11-25 | `ed92e764` | shared `data/*.json`, `*.html`, `pages/**` | Re-verify combined data and publish final integration | T13 in progress; PR to `main` planned. |
