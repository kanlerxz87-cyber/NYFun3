# Independent site-quality audit — session `b9f9777f`

**Audit date:** 27 November 2026 UTC  
**Scope:** repository state at `1823ca8` (the main branch commit this Arena branch was based on); local HTML/data/renderers, automated checks, and project documentation.  
**Purpose:** assess whether the currently published decision aids agree with one another and whether the automated checks cover the pages they claim to cover. This is a repository audit, not a fresh crawl of every hotel, restaurant, MICHELIN, MTA, or social-media page.

> **Disposition:** At the audited base, `Decide` and `Hotels` used different transit populations and methods. T82 has now aligned the live decision cockpit on this branch with the same current 69-venue route dataset used by `Hotels`, retained the older activity model as a separately labeled baseline, added consistency checks, and expanded the DOM smoke test to all 19 HTML pages. These changes are not yet deployed from this branch. OTA-rate guarantees and 2027 route/service confirmations remain open.

## Executive summary

The static site is present with category pages, a dashboard, decision cockpit, 7-day itinerary, suggestion/question registers, and a Flagged for Review page. The integration branch validators confirm 18 JSON files, 19 HTML files, 287 rendered source-linked rows, and JavaScript syntax. After installing the documented optional `jsdom` test dependency without adding a package manifest or lockfile, the recursive smoke test executed all 19 root and nested HTML pages successfully.

The most consequential audit finding is that two published transit systems answer the same hotel-selection question using different source data and rules:

- `decide.html` fetches `data/hotel_ranking.json` and `data/transit_hotels.json`; its headline and table say **65 measured starred restaurants** from a **72-restaurant 2025 selection**, using an older MTA subway+bus model.
- `hotels.html` renders `data/hotels.json`, whose captured counts are **69/69** and whose rank/median figures match `research/generated/transit_1h.json`; that generated dataset describes the **current 69-venue NYC starred directory**, uses a later subway-only GTFS run, and excludes the two out-of-city venues plus the closed Shion.

These are not necessarily arithmetic errors within their respective models: they are different populations and methodology snapshots. However, both are presented as current hotel comparisons, and the two pages do not tell the reader that their transit figures are not directly comparable. The hotel page's methodology/source note points to the newer generated file, while the decision cockpit still fetches the older data files. A single, explicitly dated, versioned method and denominator should be selected for the cross-page comparison, or both results should be labeled and kept separate.

## Findings requiring review

| ID | Severity | Finding and direct repository evidence | Recommended action |
|---|---|---|---|
| QA-01 | **High — decision integrity** | Transit datasets are split. `decide.html` loads `data/hotel_ranking.json` and `data/transit_hotels.json` via `assets/cockpit.js` (see its fetch calls around lines 294–302). The cockpit labels the result 65 measured restaurants; `data/hotel_ranking.json` records coverage 65/72 and names seven unmeasured 2025-selection entries. By contrast, `hotels.html` renders `data/hotels.json`; all 14 rows report 69/69 and their ranks/medians match `research/generated/transit_1h.json` exactly. The latter metadata says the live 69-venue NYC directory was used, with Blue Hill at Stone Barns, La Bastide, and Shion excluded; it specifies subway-only GTFS. The older ranking metadata describes the 72-row 2025 set and a different subway+bus model. | **T82 resolution on this branch:** the current `Decide` ranking, one-hour answer and restaurant matrix now use `research/generated/transit_1h.json`, the same current route output summarized by `Hotels`; the older 65/72 files are explicitly separated as an activity-route baseline. The source-integrity check asserts route counts, ranks and medians match `data/hotels.json`. Both source datasets are preserved. Actual 2027 service remains a review item. Official starting points: [MTA GTFS developer page](https://www.mta.info/developers), [official MICHELIN all-starred directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred), [U.S. Census Geocoder](https://geocoding.geo.census.gov/geocoder/). Local evidence: [cockpit](../decide.html), [ranking JSON](../data/hotel_ranking.json), [older route measurements](../data/transit_hotels.json), [hotel table data](../data/hotels.json), [latest generated route summary](generated/transit_1h.json). |
| QA-02 | **Medium — requirements coverage** | Hotel rate figures in `data/hotels.json` include Booking.com snapshots, while the request requires official sources for every row and verified real totals. Existing metadata and page copy disclose that Booking.com is third-party and that some amounts exclude taxes; the offer totals are not equivalent to direct hotel quotes. This is correctly caveated, but it remains an unmet requirement for those entries. | Keep OTA rows visibly marked third-party and not confirmed; prefer official hotel-engine checkout totals with room name, occupancy, cancellation rule, taxes/fees, timestamp, and exact dates. If no official quote is available, leave the verified-total field blank and retain a separate comparison snapshot only if useful. Official hotel links are already present in the hotel dataset; government tax links are listed in `hotels.html`. |
| QA-03 | **Low — verification coverage** | `scripts/smoke_pages.js` searches only the repository root (`readdirSync(ROOT)`), so it runs 13 pages and does not execute the six nested `pages/*.html` dossier pages, although `validate_site.py` reports 19 total HTML documents. Its header comment also says “all 10 root pages,” which no longer matches the 13-page run. | **T82 resolution on this branch:** `scripts/smoke_pages.js` recursively discovers HTML pages, resolves nested-page script paths relative to the page, and asserts source links for every dynamic host; the CI job installs jsdom and exercises all 19 HTML pages. |
| QA-04 | **Low — documentation freshness** | `README.md` still labels its verification status 25 November 2026; the data and page copy contain later 26 November captures, and the current audit is dated 26 November. | **T82 resolution on this branch:** README and CURRENT_AUDIT now use the 27 November audit date, while source-specific capture dates and the no-live-crawl limitation remain explicit. |

### Important distinctions

- The **69** value is not a verified 2027 service guarantee. `research/generated/transit_1h.json` records a current feed/model snapshot and warns that service changes and the Presidents' Day schedule require a closer-to-travel check.
- The **65 of 72** value is also tied to its own older coverage definition. It must not be presented as if it used the same current-city universe as the 69/69 table.
- The code-level source/link checks establish that a source URL is present and structurally valid; they do not re-prove every external page's content, rate availability, hotel-room fit, or future opening hours.
- No star status, hotel rate, restaurant price, or future schedule was changed by this audit.

## Reproducible checks performed

| Check | Result |
|---|---|
| `python3 scripts/validate_site.py` | PASS — 18 JSON files, 19 HTML pages, 14 Markdown docs; 15 activities, 14 hotels, 72 starred restaurant rows, and seven itinerary days. Schemas, price arithmetic, source-link coverage, local links/anchors, navigation, table source columns, and correction guards passed. |
| `python3 scripts/check_sources.py` | PASS — hotel/activity sources, hotel verification register, journey caveats, and ranking provenance checks passed. |
| `python3 scripts/check_inline_js.py` | PASS — 12 JavaScript units across four files and inline page scripts. |
| `node scripts/check_rendered_tables.js` | PASS — six dynamic renderers generated 287 source-linked rows, including 50 priced rows. |
| `node scripts/smoke_pages.js` without jsdom | SKIP by design (optional dependency absent). |
| `npm install --no-save --no-package-lock --no-audit --no-fund jsdom && node scripts/smoke_pages.js` | PASS — 19 root and nested HTML pages executed; every dynamic host rendered content and a source link. The dependency installation was ignored under `node_modules/`; no manifest or lockfile was added. |
| `git diff --check` | PASS after resolving the concurrent README/coordination rebase changes; run again before publication. |

These checks are local structural/rendering checks, not a fresh live crawl of official sites. The official URLs in QA-01 are the authoritative starting points for a future re-verification; the internal dataset discrepancies above are confirmed directly from the checked-out files.

## Integration status and remaining limitations

T83 is a completed read-only audit; T82 carries the narrowly scoped remediation on this branch. QA-01 is reconciled in the decision cockpit and in the test suite; the earlier 65/72 model is still retained but is labeled separately for activity-route context. QA-03 is resolved by recursive browser-DOM coverage of all 19 HTML pages. The Flagged for Review page records both as resolved corrections and retains the genuine MTA schedule warning under NR-04.

This audit did not independently fetch every operator page or guarantee availability. Hotel OTA snapshots remain third-party, some room/amenity fields are blank or conditional, and actual 2027 opening hours, MICHELIN status, hotel checkout totals, and transit service must be rechecked. Those outstanding limitations remain documented in the site's review queue and the original data records.
