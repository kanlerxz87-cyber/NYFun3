# COORDINATION — NYFun3 Trip Planning Site

Shared task board. Read this before starting work. This file was combined by final integration after three add/add/content conflicts; no session's board or work log was discarded.

- **Repo:** `kanlerxz87-cyber/NYFun3`
- **Live site:** https://kanlerxz87-cyber.github.io/NYFun3/ (GitHub Pages, source = `main`, `/` root)
- **Board last updated:** 2026-11-26 UTC
- **Phase A:** `arena-c2e08f03`, pinned branch `arena/c2e08f03-nyfun3`
- **Phase B / source diagnostics:** `ed92e764`, pinned branch `arena/ed92e764-nyfun3`
- **Phase C / supplemental dossier:** `arena-61fbe157`, pinned branch `arena/61fbe157-nyfun3`
- **Current Arena branch:** `arena/79f655ba-nyfun3`; initial base `1cc713110837ecbaf2f36ab4def44dcaabeddc73`; rebased onto `c4a5467c127bd08ec0a3cf79852fc98311c87513` before T14/T15

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

<a id="task-board"></a>
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
| T13 | Final integration: merge all branches, re-verify combined data, add Flagged for Review page, link/schema validation, PR to `main`, Pages build check | `done` | `ed92e764` | shared outputs, `flagged-for-review.html`, `review.html`, `scripts/**`, `.github/workflows/validate-site.yml`, `COORDINATION.md`, `README.md`, PR to `main` |
| T14 | Fresh post-integration audit of requirements coverage, site integrity, data provenance gaps, and actionable decision readiness | `done` | `arena/79f655ba-nyfun3` | `CURRENT_AUDIT.md`, `COORDINATION.md` |
| T15 | Publish newly verified MICHELIN directory discrepancy on the Flagged for Review page | `done` | `arena/79f655ba-nyfun3` | `flagged-for-review.html`, `COORDINATION.md` |
| T16 | Independent post-merge line-by-line source audit, recheck/correction of stale claims, final rebuild/link checks, PR to `main`, merge and Pages confirmation | `in progress` | `3c65c9fa` | `COORDINATION.md`, `README.md`, `REVIEW.md`, `VERIFICATION.md`, `RESEARCH.md`, `CURRENT_AUDIT.md`, shared `data/*.json`, root/Pages HTML, `scripts/*`, final PR to `main` |
| T67 | Journey-time model + Michelin-cluster hotel ranking from MTA static GTFS | `done` | `8e38e7e7` | `scripts/transit/**`, `data/transit_hotels.json`, `data/geocode_cache.json`, `.github/workflows/transit-analysis.yml` |
| T68 | Decision cockpit page (`decide.html`) and suggestions registry | `done` | `8e38e7e7` | `decide.html`, `assets/cockpit.js`, `SUGGESTIONS.md` |
| T69 | Evidence-quality audit of the review links | `done` | `8e38e7e7` | `EVIDENCE_AUDIT.md`, `data/review_links.json` |
| T70 | Source-integrity checks in CI | `done` | `8e38e7e7` | `scripts/check_sources.py`, `.github/workflows/validate-site.yml` |
| T24 | Integration of T67–T70 & `audit-53d4ee2e.md` onto `main` | `done` | `8e38e7e7` | shared outputs, `COORDINATION.md`, PR #11 |
| T71 | Verification audit remediation (Issue #3 / `snapshot-audit.md`), live direct SynXis/Arlo hotel quotes & seasonality, 100% active MICHELIN addresses/hours & 25 priced menus, measured MTA GTFS + Census/NYC GeoSearch 1h transit ranking (`transit_1h.json`), mobile & renderer fixes, CI, PR & merge to `main` | `done` | `arena-25fd4b76` | `data/*.json`, `*.html`, `pages/*.html`, `assets/*`, `research/**`, `scripts/**`, `.github/workflows/**`, `COORDINATION.md` |

**T24 post-merge proofread (26 Nov 2026):** the merged page was read on the live site, not just validated
locally. Four defects that every check passed were fixed on this branch in a follow-up commit: nine
`hotels.html#<id>` links pointing at anchors that do not exist because that table is rendered from JSON;
a matrix column headed "The" instead of "Mayfair"; a prose claim of "four hotels within 0.8 minutes" when
the data shows five; and "close call" conflating a ranking gap with a stability spread. Details in
`FLAGS.md` §5.

**T24 — dataset moved under the prose (26 Nov 2026):** PR #12 (`25fd4b76`) expanded the shared input from
9 hotels / 29 measured restaurants to **14 hotels / 65 of 72** between this branch's merges. The rendered
table followed the data; three hand-written sentences did not, and the live page briefly read "ranks 1–5"
above a fourteen-row table. Fixed here: the tie sentence is now computed from `data/hotel_ranking.json`
(and correctly describes a *chain*, not one tie), the two headline counts are checked against the data by
`check_rendered_tables.js`, and the coverage figures in `FLAGS.md` / `EVIDENCE_AUDIT.md` are updated.
This is the standing risk with shared data files: a value written into prose rots silently.

## `needs review` items — published on Flagged for Review page

| ID | Item | Status | Official source link |
|---|---|---|---|
| NR-01 | MICHELIN counts and 2027 star status need reconciliation. One 26 Nov 2026 directory fetch displayed 3 / 14 / 50 and an independent recheck displayed 5 / 14 / 50 (sum 69); the local 2025 dataset has 5 / 15 / 52 (72 total). Michelin Media confirms the 14 Dec 2026 ceremony, so 2027 stars are not yet knowable. | `needs review` | [Current MICHELIN all-starred directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred) · [2025 announcement](https://guide.michelin.com/us/en/article/michelin-guide-ceremony/all-the-stars-in-the-michelin-guide-to-new-york-city-2025) · [Michelin Media ceremony](https://michelinmedia.com/pages/blog/detail/article/c/a1479/) |
| NR-02 | Hotel rates are Booking.com third-party snapshots, not official hotel quotes | `needs review` | [GitHub Pages API](https://api.github.com/repos/kanlerxz87-cyber/NYFun3/pages) · [HGU official site](https://www.hgunyc.com/) |
| NR-03 | Cheapest upcoming time to book / best time to book remain unverified | `needs review` | [HGU exact-date quote](https://www.booking.com/hotel/us/hgu-new-york.html?checkin=2027-02-15&checkout=2027-02-22&group_adults=2&no_rooms=1&group_children=0&selected_currency=USD) |
| NR-04 | 2027 one-hour transit counts are unverified; current GTFS cannot be extended | `needs review` | [MTA schedule-transition guidance](https://www.mta.info/developers/gtfs-schedules-transition) |
| NR-05 | 71 / 72 Michelin rows have verified Guide hours; one closed venue remains blank/flagged. Met/Cloisters weekly hours panels and Blue Hill at Stone Barns Wed–Fri hours still need browser confirmation. | `needs review` | [MICHELIN NYC directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants) · [The Met visit page](https://www.metmuseum.org/plan-your-visit) · [NYPL location](https://www.nypl.org/locations/schwarzman) |
| NR-06 | Bib Gourmand and merely Guide-listed venues are not fully catalogued | `needs review` | [MICHELIN NYC directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants) |
| NR-07 | 2–4-week hotel pricing and 2027 date-specific admission totals are not captured | `needs review` | [Hyatt Midtown-South official site](https://www.hyatt.com/hyatt-place/en-US/nyczm-hyatt-place-new-york-midtown-south) |
| NR-08 | Direct official hotel APIs/pages did not expose exact-date totals; diagnostics recorded blocks | `needs review` | [Hyatt Midtown-South official site](https://www.hyatt.com/hyatt-place/en-US/nyczm-hyatt-place-new-york-midtown-south) |
| NR-09 | First-party menu pages publish multiple differently priced options on the same page; the 25 priced rows use explicit official per-person options and are not like-for-like all-in bills | `needs review` | [EMP FAQ](https://www.elevenmadisonpark.com/faq) · [Gramercy Tavern menu](https://www.gramercytavern.com/dining-room-menu/) · [Le Coucou menus](https://lecoucou.com/) · [Local priced rows](data/michelin_all.json) |

## Independent recheck work log — `3c65c9fa` (26 November 2026, after PR #11 / #12 / #13)

**Sources directly inspected:** [official MICHELIN NYC all-starred directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred), [2025 NYC star announcement](https://guide.michelin.com/us/en/article/michelin-guide-ceremony/all-the-stars-in-the-michelin-guide-to-new-york-city-2025), [Michelin Media 2026 ceremony announcement](https://michelinmedia.com/pages/blog/detail/article/c/a1479/), individual Guide pages for the contradictory hours rows, [HGU official site](https://www.hgunyc.com/) and [contact](https://www.hgunyc.com/more/contact), [Marriott citizenM property page](https://www.marriott.com/en-us/hotels/nyczt-citizenm-new-york-times-square/overview/), [NYC DOF hotel tax](https://www.nyc.gov/site/finance/business/business-hotel-room-occupancy-tax.page), [NYS ST-101.5](https://www.tax.ny.gov/pdf/current_forms/st/st101_5.pdf), [NYC Council tax report](https://legistar.council.nyc.gov/View.ashx?GUID=4547DD67-B740-4FED-A1E3-596960BC0E98&ID=12994382&M=F), and the first-party menu/FAQ pages indexed in `RESEARCH.md`.

**Conflict resolution:** while this session was working, PR #11 / #12 / #13 merged 14-hotel direct quotes, seasonality, 25 priced menus, 71 / 72 Guide hours, measured GTFS 1-hour counts, evidence audits, and CI source checks into `main`. Rebasing produced overlapping edits in `COORDINATION.md`, shared JSON, root/Pages HTML, and `scripts/validate_site.py`. The branch was reset to the latest `origin/main` and the independent source corrections were re-applied semantically so no other session’s work was discarded. Historical `official_site_shipped_wrong` fields and audit documents that deliberately cite old URLs are preserved as evidence, not active links.

**Verified corrections retained:** active HGU and citizenM links now use verified official property pages; the unsupported $4/night tax claim and `$3.50–$4/night` range were replaced with current official NYC/State components and source links; ceremony links were normalized to the fetched official Michelin Media article; four populated Guide-hours rows with contradictory UNVERIFIED flags were cleared; 71 / 72 hours metadata now matches the row-level count; NR-09 publishes first-party menu-option ambiguity; resolved corrections are published on the Flagged for Review page. Unknown 2027 holiday hours, future star status, and exact-date checkout totals remain blank/flagged rather than inferred.

**Verification:** `python3 scripts/validate_site.py`, `python3 scripts/check_inline_js.py`, `node scripts/check_rendered_tables.js`, `python3 scripts/check_sources.py`, `node scripts/smoke_pages.js`, and `git diff --check` were rerun after re-applying the corrections. T16 remains `in progress` until the PR, merge, CI, Pages deployment, and live URL checks are recorded below.

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
| 2026-11-26 | `3c65c9fa` | shared JSON, root/Pages HTML, `COORDINATION.md`, `scripts/validate_site.py` | PR #11 / #12 / #13 landed while the independent recheck was in progress, causing broad overlapping edits on the same shared outputs | Reset the branch to latest `origin/main`, re-applied only evidence-based semantic corrections, preserved all new direct-quote/GTFS/pricing work and historical audit evidence, and recorded the handoff above; no work discarded. |
| 2026-11-25 | `ed92e764` | shared `data/*.json`, `*.html`, `pages/**` | Re-verify combined data and publish final integration | PR #4 merged at `0a2eafe`; final copy reconciliation merged in PR #5 at `0b9ec96`; both Pages builds and live checks passed. |

## Work log — Final integration (`ed92e764`)

**Built:** `flagged-for-review.html` publishes NR-01–NR-08 with an official starting source and a concrete next check; `review.html` redirects to it; root and dossier navigation now include the review page and Itinerary; every static/dynamic published data row has a Source cell/link. `scripts/validate_site.py` checks JSON schemas, `2 × official per-person` arithmetic, source-link coverage, local links/anchors, and navigation; `scripts/check_inline_js.py` checks all JavaScript; `scripts/check_rendered_tables.js` executes the five root renderers and checks 175 generated rows; `.github/workflows/validate-site.yml` runs all three on pushes and PRs.

**Data refreshed:** 10 selected starred rows now carry linked first-party menu/FAQ/PDF prices as `2 × official per-person price` with an exclusions caveat; 62 rows remain blank + `unverified`. Four official activity hour baselines were added for NPS/Liberty Island, the High Line, Central Park, and Grand Central, with explicit "not a 2027 calendar" notes; Met/Cloisters/NYPL/Top of the Rock remain blank/partial. `data/itinerary.json` exposes consolidated official source links. No 2027 Michelin, transit, holiday, or hotel-price inference was made.

**Docs reconciled:** `README.md`, `REVIEW.md`, and `VERIFICATION.md` now describe the combined pages, exact final coverage, CI validators, and Flagged for Review semantics; stale R1/R2/R3 and "no row has a source" defects are explicitly resolved. The Phase A/B/C logs and conflict history are preserved above.

**Checks:** `python scripts/validate_site.py`, `python scripts/check_inline_js.py`, and `node scripts/check_rendered_tables.js` passed locally after the integration edits. PR, CI, and Pages rebuild checks are pending at the time of this log entry.

## Final publish check (`ed92e764`, 2026-11-25 UTC)

- **PR #4** (`arena/ed92e764-nyfun3` → `main`) merged as `0a2eafe` after the `Validate static site` check succeeded. CI run `45722618504` passed all seven job steps, including the DOM-stub rendered-table check.
- **PR #5** merged the final copy reconciliation as `0b9ec96`; its `Validate static site` check passed.
- **GitHub Pages** reported `status: built`, `error: null` for both `0a2eafe` and `0b9ec96`. The latest build completed 23:39:31 UTC. Legacy source remains `main` `/`.
- **Live URLs checked:** root dashboard, `flagged-for-review.html`, `plan.html`, `pages/findings.html`, `restaurants.html`, `michelin.html`, and `itinerary.html`. The new review queue, Source columns, `2 × official per-person price` cells, and consolidated itinerary sources rendered on the published site. The Restaurants and Michelin introductions were rechecked with a cache-busting query after the second build.
- **T13:** `done`. All substantive integration, CI, PR, Pages, and live checks are complete; no 2027 inference or unverified value was introduced.

## Work log — Fresh audit (`arena/79f655ba-nyfun3`, 2026-11-26)

**T14 result:** Added `CURRENT_AUDIT.md`, a decision-readiness crosswalk covering the travel window, holiday, hotel quote limitations, missing transit counts, current MICHELIN status discrepancy, hours/prices coverage, social-link semantics, open questions, and recommended next steps. No hotel, transit, 2027 hours, or MICHELIN row values were inferred or changed.

**Sources directly inspected:** [official MICHELIN NYC all-starred directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred) (displayed 3 three-star / 14 two-star / 50 one-star counts and a 69-restaurant heading; the visible counts sum to 67; this differs from the repository's 2025-tagged 72-row dataset), and [official OPM 2027 federal holiday schedule](https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/) (Washington's Birthday is Monday 15 February 2027). Local data, pages, and validators were inspected; see `CURRENT_AUDIT.md` for exact coverage and caveats.

**Verification:** `python scripts/validate_site.py`, `python scripts/check_inline_js.py`, `node scripts/check_rendered_tables.js`, and `git diff --check` all passed after rebasing this branch onto `origin/main`. Automated checks establish structure/source-link coverage, not truth or live availability.

**Irregularities:** the current official MICHELIN page aggregate differs from local 2025 data and its own visible tier counts (67) differ from the displayed result total (69); 9/9 hotel ≤1-hour counts remain null; hotel quote totals are third-party and only one date range; 7/9 amenity fields and 5/15 activity hours tables are blank; 45/72 Michelin hours and 62/72 couple price totals are blank; social links are discovery searches, not verified specific content. Detailed flags and sources are in `CURRENT_AUDIT.md`.

**T15:** final integration follow-up claimed to add the MICHELIN count discrepancy to `flagged-for-review.html`; it will not overwrite dataset values until individual official records can be reconciled.

**T15 result:** Updated NR-01 on `flagged-for-review.html` and this board with the current official-directory count discrepancy, individual-entry recheck guidance, and links to the current Guide, historical 2025 announcement, and local dataset. Corrected the previously stated future ceremony date claim instead of retaining an unsupported date. Added the fresh audit link and updated the verification date to 26 November 2026. No restaurant tier data was changed.

**Verification:** the three site validators and `git diff --check` passed after the review-page edit. The review entry is published and remains `needs review` until line-by-line individual Guide reconciliation is completed.

## Final publish check — Fresh audit follow-up (`arena/79f655ba-nyfun3`, 2026-11-26 UTC)

- **PR #8** (this branch → `main`) merged at `e41d259af151a3ca6799bfbc79dd03b68eabe9e4` on 2026-11-26 13:20 UTC: https://github.com/kanlerxz87-cyber/NYFun3/pull/8
- The `Validate static site` check passed for the PR head and merge commit. Pages deployment run `45828218510` completed successfully. GitHub Pages API reported `status: built`, `error: null`, source `main` `/`, commit `e41d259af151a3ca6799bfbc79dd03b68eabe9e4`.
- Live post-deploy checks: [Flagged for Review](https://kanlerxz87-cyber.github.io/NYFun3/flagged-for-review.html) displayed updated NR-01 and the current-audit link; [CURRENT_AUDIT.md](https://kanlerxz87-cyber.github.io/NYFun3/CURRENT_AUDIT.md) rendered with the full decision-readiness tables. No data-tier changes were made.
- **Publish result:** PR #8 merged; static site checks passed; GitHub Pages build succeeded and the updated review queue/audit were verified live.

## Session `46804a5a` — Official-source line-by-line verification, 2026 MICHELIN Guide + Guide-listed/Bib Gourmand catalogue & multi-window audit (completed 2026-11-26 UTC)

| ID | Task | Status | Owner session | File scope |
|---|---|---|---|---|
| T46 | Line-by-line official-source verification of 2026 MICHELIN Guide NYC ceremony/selection vs 2025, Guide-listed & Bib Gourmand entries, missing museum/venue hours & prices, hotel property/address/date-window audit, and social review links | `done` | `46804a5a` | `research/audit-46804a5a.md`, `data/michelin_2026_guide.json`, `data/hotel_date_audit.json`, `guide-2026.html`, `COORDINATION.md` (own claim and log) |

- **Built (`arena/46804a5a-nyfun3`):**
  - [`guide-2026.html`](guide-2026.html) — Mobile-friendly interactive dashboard comparing **Currently MICHELIN-Starred (`3★`/`2★`/`1★`)** vs. **Bib Gourmand (Guide-listed, no star)** vs. **Selected (just listed in the MICHELIN Guide, no star)** NYC venues, 5 Manhattan MICHELIN clusters, line-by-line hotel bed/bath/URL/tax audit, and newly verified museum/landmark schedules.
  - [`data/michelin_2026_guide.json`](data/michelin_2026_guide.json) — Verified 2026 ceremony schedule (**14 Dec 2026 at The Glasshouse, NYC** via [Michelin North America Media](https://michelinmedia.com/pages/blog/detail/article/c0/a1479)), live NYC directory counts (**`5` 3★ + `14` 2★ + `50` 1★ = `69` Starred**, **`76` Bib Gourmand**, **`224` Selected** = **`369` total Guide venues**), and 15 primary-source-verified venues across all 3 tiers (`Le Bernardin`, `Jungsik New York`, `The Modern`, `COTE`, `Gramercy Tavern`, `Crown Shy`, `COQODAQ`, `HanGawi`, `Dhamaka`, `Katz's Delicatessen`, `8282`, `Manhatta`, `Le Rock`, `Don Angie`, `Cosme`).
  - [`data/hotel_date_audit.json`](data/hotel_date_audit.json) — Official hotel room/bed/bath/URL audit, [NYC Department of Finance](https://www.nyc.gov/site/finance/business/business-hotel-room-occupancy-tax.page) statutory single-room tax formula (`14.75% + $3.50/night` = `$24.50` flat on 7 nights), and live promo deadlines (`CYBER` up to 40% off at [Arlo Midtown](https://arlohotels.com/midtown/) through 3 Dec 2026; Hyatt seasonal offer through 8 Dec 2026; `DIRECT` 5% off at [The Artezen Hotel](https://www.artezenhotel.com/)).
  - [`research/audit-46804a5a.md`](research/audit-46804a5a.md) — Complete 16-item (`FA-01`–`FA-16`) line-by-line repository audit and primary-source ledger.
- **Cross-session findings logged for `NR-01` / `NR-05` / `NR-06` & shared outputs (without overwriting concurrent shared files):**
  1. **`NR-01` UI Badge Correction:** On [guide.michelin.com/.../all-starred](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred), `Distinction 3` is the active filter-pill badge for 3 selected checkboxes (1★, 2★, 3★), not 3 three-star venues; actual live NYC starred counts are **`5` + `14` + `50` = `69`** (no `67-vs-69` internal mismatch).
  2. **`NR-05` Met Fifth Ave & Met Cloisters Hours Resolved:** Official [The Met](https://www.metmuseum.org/plan-your-visit) & [Met Cloisters](https://www.metmuseum.org/plan-your-visit/met-cloisters) confirm Fifth Ave is open Sun–Tue & Thu `10:00–17:00`, Fri–Sat `10:00–21:00`, closed Wed (`$30/adult = $60/couple`), and Met Cloisters is open Thu–Tue `10:00–17:00`, closed Wed (`$30/adult = $60/couple`).
  3. **`NR-06` Bib Gourmand & Selected Tier Comparison Published:** [`guide-2026.html`](guide-2026.html) catalogues official couple totals for Bib Gourmand (`COQODAQ` $104, `HanGawi` $84–$198, `Dhamaka` $100–$146, `Katz's` $61.90–$63.90, `8282` $82–$140) and Selected (`Manhatta` $130–$336, `Le Rock` $92–$232, `Don Angie` $134–$162; `Cosme` left `unverified`).
  4. **Couple Room-Tier Caveat:** Official [HGU Queen Standard](https://www.hgunyc.com/stay/queen) states *"Ideal for a solo traveler"* and [Artezen Rooms](https://www.artezenhotel.com/rooms) describes *Petite Queen* for individual business travelers — couples of 2 adults should verify *Queen Deluxe* / *Deluxe Queen* / *King Standard* tiers.
- **Validation:** `python3 scripts/validate_site.py`, `python3 scripts/check_sources.py`, `python3 scripts/check_inline_js.py`, `node scripts/check_rendered_tables.js`, `node scripts/smoke_pages.js`, and `git diff --check` all passed locally.
