# Independent site-quality audit — session `b9f9777f`

**Audit date:** 27 November 2026 UTC  
**Scope:** repository state at `1823ca8` (the main branch commit this Arena branch was based on); local HTML/data/renderers, automated checks, and project documentation.  
**Purpose:** assess whether the currently published decision aids agree with one another and whether the automated checks cover the pages they claim to cover. This is a repository audit, not a fresh crawl of every hotel, restaurant, MICHELIN, MTA, or social-media page.

> **Disposition:** Site build and data-shape checks pass. A material split remains between the hotel transit results displayed on `Decide` and the more recently generated 69-venue results used on `Hotels`. This audit does not silently choose or overwrite either dataset. Resolve the source-of-truth question in an integration task before using cross-page transit results to choose a hotel.

## Executive summary

The static site is present with category pages, a dashboard, decision cockpit, 7-day itinerary, suggestion/question registers, and a Flagged for Review page. Validators confirm 18 JSON files, 19 HTML files, 203 rendered table rows with source links, and JavaScript syntax. After installing the repository's documented optional `jsdom` test dependency without adding a package manifest or lockfile, the DOM smoke test executed all 13 root-level HTML pages successfully.

The most consequential audit finding is that two published transit systems answer the same hotel-selection question using different source data and rules:

- `decide.html` fetches `data/hotel_ranking.json` and `data/transit_hotels.json`; its headline and table say **65 measured starred restaurants** from a **72-restaurant 2025 selection**, using an older MTA subway+bus model.
- `hotels.html` renders `data/hotels.json`, whose captured counts are **69/69** and whose rank/median figures match `research/generated/transit_1h.json`; that generated dataset describes the **current 69-venue NYC starred directory**, uses a later subway-only GTFS run, and excludes the two out-of-city venues plus the closed Shion.

These are not necessarily arithmetic errors within their respective models: they are different populations and methodology snapshots. However, both are presented as current hotel comparisons, and the two pages do not tell the reader that their transit figures are not directly comparable. The hotel page's methodology/source note points to the newer generated file, while the decision cockpit still fetches the older data files. A single, explicitly dated, versioned method and denominator should be selected for the cross-page comparison, or both results should be labeled and kept separate.

## Findings requiring review

| ID | Severity | Finding and direct repository evidence | Recommended action |
|---|---|---|---|
| QA-01 | **High — decision integrity** | Transit datasets are split. `decide.html` loads `data/hotel_ranking.json` and `data/transit_hotels.json` via `assets/cockpit.js` (see its fetch calls around lines 294–302). The cockpit labels the result 65 measured restaurants; `data/hotel_ranking.json` records coverage 65/72 and names seven unmeasured 2025-selection entries. By contrast, `hotels.html` renders `data/hotels.json`; all 14 rows report 69/69 and their ranks/medians match `research/generated/transit_1h.json` exactly. The latter metadata says the live 69-venue NYC directory was used, with Blue Hill at Stone Barns, La Bastide, and Shion excluded; it specifies subway-only GTFS. The older ranking metadata describes the 72-row 2025 set and a different subway+bus model. | Integration owner: choose one authoritative comparison for the current trip, or clearly label these as separate historical/current scenarios; make each page identify its denominator, service date/feed, transit modes, exclusions, and capture date; add a consistency test preventing uncaveated conflicting summaries. Preserve both source datasets if they remain useful; do not overwrite a dataset without re-verification. Official starting points: [MTA GTFS developer page](https://www.mta.info/developers), [official MICHELIN all-starred directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred), [U.S. Census Geocoder](https://geocoding.geo.census.gov/geocoder/). Local evidence: [cockpit](../decide.html), [ranking JSON](../data/hotel_ranking.json), [older route measurements](../data/transit_hotels.json), [hotel table data](../data/hotels.json), [latest generated route summary](generated/transit_1h.json). |
| QA-02 | **Medium — requirements coverage** | Hotel rate figures in `data/hotels.json` include Booking.com snapshots, while the request requires official sources for every row and verified real totals. Existing metadata and page copy disclose that Booking.com is third-party and that some amounts exclude taxes; the offer totals are not equivalent to direct hotel quotes. This is correctly caveated, but it remains an unmet requirement for those entries. | Keep OTA rows visibly marked third-party and not confirmed; prefer official hotel-engine checkout totals with room name, occupancy, cancellation rule, taxes/fees, timestamp, and exact dates. If no official quote is available, leave the verified-total field blank and retain a separate comparison snapshot only if useful. Official hotel links are already present in the hotel dataset; government tax links are listed in `hotels.html`. |
| QA-03 | **Low — verification coverage** | `scripts/smoke_pages.js` searches only the repository root (`readdirSync(ROOT)`), so it runs 13 pages and does not execute the six nested `pages/*.html` dossier pages, although `validate_site.py` reports 19 total HTML documents. Its header comment also says “all 10 root pages,” which no longer matches the 13-page run. | Update the smoke test to recursively discover HTML pages (or explicitly list tested exclusions), and revise the stale count comment. Run rendered-host assertions on any nested pages that use dynamic data. |
| QA-04 | **Low — documentation freshness** | `README.md` still labels its verification status 25 November 2026; the data and page copy contain later 26 November captures, and the current audit is dated 26 November. | On the next documentation integration, update the README status date and distinguish source-capture dates from the audit date. Avoid implying that every live source was freshly re-opened today. |

### Important distinctions

- The **69** value is not a verified 2027 service guarantee. `research/generated/transit_1h.json` records a current feed/model snapshot and warns that service changes and the Presidents' Day schedule require a closer-to-travel check.
- The **65 of 72** value is also tied to its own older coverage definition. It must not be presented as if it used the same current-city universe as the 69/69 table.
- The code-level source/link checks establish that a source URL is present and structurally valid; they do not re-prove every external page's content, rate availability, hotel-room fit, or future opening hours.
- No star status, hotel rate, restaurant price, or future schedule was changed by this audit.

## Reproducible checks performed

| Check | Result |
|---|---|
| `python3 scripts/validate_site.py` | PASS — 18 JSON files, 19 HTML pages, 13 Markdown docs; 15 activities, 14 hotels, 72 starred restaurant rows, and seven itinerary days. Schemas, price arithmetic, source-link coverage, local links/anchors, navigation, table source columns, and correction guards passed. |
| `python3 scripts/check_sources.py` | PASS — hotel/activity sources, hotel verification register, journey caveats, and ranking provenance checks passed. |
| `python3 scripts/check_inline_js.py` | PASS — 12 JavaScript units across four files and inline page scripts. |
| `node scripts/check_rendered_tables.js` | PASS — six dynamic renderers generated 203 source-linked rows, including 50 priced rows. |
| `node scripts/smoke_pages.js` without jsdom | SKIP by design (optional dependency absent). |
| `npm install --no-save --no-package-lock --no-audit --no-fund jsdom && node scripts/smoke_pages.js` | PASS — 13 root-level HTML pages executed; dynamic hosts rendered content and source links. The dependency installation was ignored under `node_modules/`; no manifest or lockfile was added. |
| `git diff --check` | PASS at audit start; run again before publication. |

These checks are local structural/rendering checks, not a fresh live crawl of official sites. The official URLs in QA-01 are the authoritative starting points for a future re-verification; the internal dataset discrepancies above are confirmed directly from the checked-out files.

## Coordination request

`T80` is separately marked in progress by session `551dcafd` with `COORDINATION.md` in its scope. QA-01 and QA-03 should be handed to the final integration owner rather than this audit changing shared datasets, dashboard scripts, or the Flagged for Review page. Please add a corresponding review item to the shared review queue when the integration owner takes up QA-01; keep the cross-page discrepancy visible until its chosen denominator and method are verified. No code or published data was silently rewritten in this audit.
