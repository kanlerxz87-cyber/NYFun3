# COORDINATION — NYFun3 Trip Planning Site

Shared task board. Read this before starting work. This file was combined by final integration after three add/add/content conflicts; no session's board or work log was discarded.

- **Repo:** `kanlerxz87-cyber/NYFun3`
- **Live site:** https://kanlerxz87-cyber.github.io/NYFun3/ (GitHub Pages, source = `main`, `/` root)
- **Board last updated:** 2026-11-27 UTC (T81 claimed by `957d4019`)
- **Phase A:** `arena-c2e08f03`, pinned branch `arena/c2e08f03-nyfun3`
- **Phase B / source diagnostics:** `ed92e764`, pinned branch `arena/ed92e764-nyfun3`
- **Phase C / supplemental dossier:** `arena-61fbe157`, pinned branch `arena/61fbe157-nyfun3`
- **Current Arena branch (this session):** `arena/67e5a326-nyfun3`; base `c4a5467c127bd08ec0a3cf79852fc98311c87513` (main after PR #7); merged `origin/main` (PRs #8–#17, then #18/#20) on 2026-11-26 before updating PR #19
- **Other recent fixed branch:** `arena/3c65c9fa-nyfun3`; base `c4a5467c127bd08ec0a3cf79852fc98311c87513` (T16, merged as PRs #16/#18/#20)
- **Other recent fixed branch:** `arena/79f655ba-nyfun3`; initial base `1cc713110837ecbaf2f36ab4def44dcaabeddc73`; rebased onto `c4a5467c127bd08ec0a3cf79852fc98311c87513` before its T14/T15

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
| T16 | Independent post-merge line-by-line source audit, recheck/correction of stale claims, final rebuild/link checks, PR to `main`, merge and Pages confirmation | `done` | `3c65c9fa` | `COORDINATION.md`, `README.md`, `REVIEW.md`, `VERIFICATION.md`, `RESEARCH.md`, `CURRENT_AUDIT.md`, shared `data/*.json`, root/Pages HTML, `scripts/*`, final PR to `main` |
| T67 | Journey-time model + Michelin-cluster hotel ranking from MTA static GTFS | `done` | `8e38e7e7` | `scripts/transit/**`, `data/transit_hotels.json`, `data/geocode_cache.json`, `.github/workflows/transit-analysis.yml` |
| T68 | Decision cockpit page (`decide.html`) and suggestions registry | `done` | `8e38e7e7` | `decide.html`, `assets/cockpit.js`, `SUGGESTIONS.md` |
| T69 | Evidence-quality audit of the review links | `done` | `8e38e7e7` | `EVIDENCE_AUDIT.md`, `data/review_links.json` |
| T70 | Source-integrity checks in CI | `done` | `8e38e7e7` | `scripts/check_sources.py`, `.github/workflows/validate-site.yml` |
| T24 | Integration of T67–T70 & `audit-53d4ee2e.md` onto `main` | `done` | `8e38e7e7` | shared outputs, `COORDINATION.md`, PR #11 |
| T71 | Verification audit remediation (Issue #3 / `snapshot-audit.md`), live direct SynXis/Arlo hotel quotes & seasonality, 100% active MICHELIN addresses/hours & 25 priced menus, measured MTA GTFS + Census/NYC GeoSearch 1h transit ranking (`transit_1h.json`), mobile & renderer fixes, CI, PR & merge to `main` | `done` | `arena-25fd4b76` | `data/*.json`, `*.html`, `pages/*.html`, `assets/*`, `research/**`, `scripts/**`, `.github/workflows/**`, `COORDINATION.md` |
| T72 | Session `67e5a326` contribution: priority review links (10 priced restaurants + 15 activities) with dated creator links | `done` | `67e5a326` | `data/michelin*.json`, `data/activities.json`, `assets/app.js`, `restaurants.html`, `michelin.html`, `activities.html` |
| T73 | Session `67e5a326` contribution: computed GTFS ranking drafted in parallel, then **superseded by T67/T71** (kept on this board for the record; not merged) | `superseded` | `67e5a326` | `research/scripts/transit_analysis.py`, `data/transit.json`, `transit.html` (all removed in the main-merge reconciliation) |
| T81 | Session `957d4019`: independent official-source spot audit of the open `needs review` items (NR-01, NR-04, NR-05, NR-07, NR-08), the hotel-tax components, and the repo irregularities list; publishes results as a new audit file only; no shared output edited | `done` (results in `research/audit-957d4019.md`; irregularities I1–I9 handed to integration) | `957d4019` | `research/audit-957d4019.md`, `COORDINATION.md` (own row and log only) |

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
| NR-01 | MICHELIN counts and 2027 star status need reconciliation. An earlier audit misread the official directory’s “Distinction 3” active-filter badge as 3 three-star venues; the live NYC starred counts are 5 / 14 / 50 = 69. The local 2025 dataset has 5 / 15 / 52 (72 total). Michelin Media confirms the 14 Dec 2026 ceremony, so 2027 stars are not yet knowable. | `needs review` | [Current MICHELIN all-starred directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred) · [2025 announcement](https://guide.michelin.com/us/en/article/michelin-guide-ceremony/all-the-stars-in-the-michelin-guide-to-new-york-city-2025) · [Michelin Media ceremony](https://michelinmedia.com/pages/blog/detail/article/c/a1479/) |
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

**Verification:** `python3 scripts/validate_site.py`, `python3 scripts/check_inline_js.py`, `node scripts/check_rendered_tables.js`, `python3 scripts/check_sources.py`, `node scripts/smoke_pages.js`, and `git diff --check` were rerun after re-applying the corrections. **T16:** `done`; PR, CI, Pages deployment, and live URL results are recorded in the final publish check below.

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
| 2026-11-26 | `3c65c9fa` | `COORDINATION.md` | PR #17 / T46 appended a new session log to `main` while follow-up PR #18 was open | Rebased PR #18, preserved both the T46 log and the PR #16 final publish check, and added this conflict row; no work discarded. |
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
  - [`data/michelin_2026_guide.json`](data/michelin_2026_guide.json) — Verified 2026 ceremony schedule (**14 Dec 2026 at The Glasshouse, NYC** via [Michelin North America Media](https://michelinmedia.com/pages/blog/detail/article/c/a1479/)), live NYC directory counts (**`5` 3★ + `14` 2★ + `50` 1★ = `69` Starred**, **`76` Bib Gourmand**, **`224` Selected** = **`369` total Guide venues**), and 15 primary-source-verified venues across all 3 tiers (`Le Bernardin`, `Jungsik New York`, `The Modern`, `COTE`, `Gramercy Tavern`, `Crown Shy`, `COQODAQ`, `HanGawi`, `Dhamaka`, `Katz's Delicatessen`, `8282`, `Manhatta`, `Le Rock`, `Don Angie`, `Cosme`).
  - [`data/hotel_date_audit.json`](data/hotel_date_audit.json) — Official hotel room/bed/bath/URL audit, [NYC Department of Finance](https://www.nyc.gov/site/finance/business/business-hotel-room-occupancy-tax.page) statutory single-room tax formula (`14.75% + $3.50/night` = `$24.50` flat on 7 nights), and live promo deadlines (`CYBER` up to 40% off at [Arlo Midtown](https://arlohotels.com/midtown/) through 3 Dec 2026; Hyatt seasonal offer through 8 Dec 2026; `DIRECT` 5% off at [The Artezen Hotel](https://www.artezenhotel.com/)).
  - [`research/audit-46804a5a.md`](research/audit-46804a5a.md) — Complete 16-item (`FA-01`–`FA-16`) line-by-line repository audit and primary-source ledger.
- **Cross-session findings logged for `NR-01` / `NR-05` / `NR-06` & shared outputs (without overwriting concurrent shared files):**
  1. **`NR-01` UI Badge Correction:** On [guide.michelin.com/.../all-starred](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred), `Distinction 3` is the active filter-pill badge for 3 selected checkboxes (1★, 2★, 3★), not 3 three-star venues; actual live NYC starred counts are **`5` + `14` + `50` = `69`** (no `67-vs-69` internal mismatch).
  2. **`NR-05` Met Fifth Ave & Met Cloisters Hours Resolved:** Official [The Met](https://www.metmuseum.org/plan-your-visit) & [Met Cloisters](https://www.metmuseum.org/plan-your-visit/met-cloisters) confirm Fifth Ave is open Sun–Tue & Thu `10:00–17:00`, Fri–Sat `10:00–21:00`, closed Wed (`$30/adult = $60/couple`), and Met Cloisters is open Thu–Tue `10:00–17:00`, closed Wed (`$30/adult = $60/couple`).
  3. **`NR-06` Bib Gourmand & Selected Tier Comparison Published:** [`guide-2026.html`](guide-2026.html) catalogues official couple totals for Bib Gourmand (`COQODAQ` $104, `HanGawi` $84–$198, `Dhamaka` $100–$146, `Katz's` $61.90–$63.90, `8282` $82–$140) and Selected (`Manhatta` $130–$336, `Le Rock` $92–$232, `Don Angie` $134–$162; `Cosme` left `unverified`).
  4. **Couple Room-Tier Caveat:** Official [HGU Queen Standard](https://www.hgunyc.com/stay/queen) states *"Ideal for a solo traveler"* and [Artezen Rooms](https://www.artezenhotel.com/rooms) describes *Petite Queen* for individual business travelers — couples of 2 adults should verify *Queen Deluxe* / *Deluxe Queen* / *King Standard* tiers.
- **Validation:** `python3 scripts/validate_site.py`, `python3 scripts/check_sources.py`, `python3 scripts/check_inline_js.py`, `node scripts/check_rendered_tables.js`, `node scripts/smoke_pages.js`, and `git diff --check` all passed locally.

## Session `67e5a326` — Priority review links kept; transit drafted then superseded (closed 2026-11-26 UTC)

This session claimed board rows for a computed GTFS hotel×starred-restaurant ranking and for dated creator links on the priority rows. Partway through, `origin/main` advanced through PRs #8–#17 (sessions `79f655ba`, `8e38e7e7`, `3c65c9fa`, `46804a5a`, `arena-25fd4b76`) with a strictly more complete implementation of the same ranking (T67 `scripts/transit/gtfs_route.py` + `data/transit_hotels.json`; T71 `research/generated/transit_1h.json` with measured 18:30 in-window weekday routing, 14 hotels, 100% active MICHELIN addresses, direct SynXis/Arlo quotes, `decide.html` cockpit, source-integrity CI). Duplicate work would have forked the dataset, so the parallel transit draft from this session (`research/scripts/transit_analysis.py`, `data/transit.json`, `transit.html`, branch-local `.github/workflows/transit-analysis.yml`) was **not merged**; the branch instead carries only main's implementation plus this session's additions below. My two GTFS workflow runs (`45830340621`, `45831132436`, `45832310175`) ran on my branch only and touched only my draft files.

**T72 — priority review links (`done`).** All 10 priced starred restaurants (Eleven Madison Park, Le Bernardin, The Modern, Masa, COTE, Aquavit, Daniel, Gramercy Tavern, Le Coucou, Rezdôra) and all 15 activities now carry dated creator links found by web search on 2026-11-26 in each row's `review_links` array (`platform`, `url`, `title`, `found_on: 2026-11-26`), plus `review_links_note` (creator content, not official sources, not endorsements). Rendered via `NYF.reviewCell` in `assets/app.js` on `restaurants.html`, `michelin.html`, `activities.html`, found links first with platform labels and tooltips, search links kept as a labelled `search:` fallback. Footnotes added to the three pages. Note: T69 (`data/review_links.json`, session `8e38e7e7`) is the higher-assurance registry (opened pages, link-kind taxonomy, 9 venues with 25 title-verified posts) — it is complementary; neither file overwrites the other. Coverage overlap (venues with both a T69 registry entry and a T72 row link, e.g. Le Bernardin) is intentional and flagged here for the reviewer.

**T73 — computed transit ranking (`superseded`).** Built on this branch, then removed in the merge reconciliation exactly because T67/T71 merged first and cover more (time-of-day routing vs my median-edge model; 65–69 of 72 venues placed vs my 31; hotel universe 14 vs 9). Kept as a record only.

**Verification performed (on this branch, after merging `origin/main`):**
- Data injection ran against main's regenerated dataset: 10 restaurant rows and 15 activity rows updated; counts verified programmatically.
- `restaurants.html`, `michelin.html`, `activities.html` renderers and footnotes survived the auto-merge cleanly; all `transit.html` references removed (page dropped); `git grep transit.html` clean.
- Validators re-run on the reconciled tree (see below; results recorded in the publish check for PR #19).

**Irregularities / notes:**
1. GitHub registered `.github/workflows/transit-analysis.yml` under the name **“Measure journey times (official MTA GTFS)”** before this branch created its own file at the same path; after the reconciliation the file on this branch is main's version, so the registration is correct on merge.
2. My earlier claim used `T14`/`T15`, which main had already assigned to sessions `79f655ba` (audit, directory discrepancy) — renumbered to `T72`/`T73` in this reconciliation; no session's task IDs were rewritten.
3. `scripts/validate_site.py` / `scripts/check_rendered_tables.js` from this branch were **not** carried over; main's versions (with `check_sources.py` and CI source-integrity gates) govern.
4. Found creator links are dated pointers, not verifications; links can rot. `.github/workflows/validate-site.yml` on main checks source integrity for the published tables.
5. `data/michelin_all.json` from main (directory-count tension documented on the Flagged for Review page under NR-01) is left untouched; this session injected only `review_links`.

**Cross-session notes:** merge conflict resolution took `origin/main` for every shared output (`data/*.json` rows, `hotels.html`, `index.html`, `plan.html`, `flagged-for-review.html`, `README.md`, `VERIFICATION.md`, validators) and re-applied only this session's additive changes. No other session's file was overwritten, and no fact from main was reverted. The dossier (`pages/`) and audit docs from other sessions are untouched.

## Final publish check — Independent recheck (`3c65c9fa`, 26 November 2026 UTC)

- **PR [#16](https://github.com/kanlerxz87-cyber/NYFun3/pull/16)** (`arena/3c65c9fa-nyfun3` → `main`) merged at `9297c78e7b491573986cf1c4cfe9adf25ec97cdd` on 2026-11-26 14:02:02 UTC.
- **CI:** [Validate static site run 45834691039](https://github.com/kanlerxz87-cyber/NYFun3/actions/runs/45834691039) passed on the PR head `edf8aca`; [Measure journey times run 45834597675](https://github.com/kanlerxz87-cyber/NYFun3/actions/runs/45834597675) passed and generated commit `47ab85d` was included in the merge. Local validators, source-integrity checks, rendered-table checks, DOM smoke tests, and `git diff --check` also passed.
- **GitHub Pages:** API reported `status: built`, `error.message: null`, source `main` `/`, HTTPS enforced; build for `9297c78` completed at 14:02:27 UTC.
- **Live URLs checked after deployment:** [root dashboard](https://kanlerxz87-cyber.github.io/NYFun3/), [Flagged for Review](https://kanlerxz87-cyber.github.io/NYFun3/flagged-for-review.html), [Hotels](https://kanlerxz87-cyber.github.io/NYFun3/hotels.html), [Decide](https://kanlerxz87-cyber.github.io/NYFun3/decide.html), and [CURRENT_AUDIT.md](https://kanlerxz87-cyber.github.io/NYFun3/CURRENT_AUDIT.md). The live pages showed 14 hotels, 25 priced menus, 71 / 72 Guide hours, 9 published review items, resolved source corrections, official tax links, and the current GTFS decision cockpit.
- **Result:** T16 is `done`. NR-01–NR-09 remain published as `needs review` and do not block the live dashboard. This board update is a small follow-up commit on the same branch so the PR link and merge result are preserved in `main`.

**Conflict note:** PR #17 / T46 landed on `main` while this board follow-up PR #18 was open, causing an append/add-style conflict at the end of `COORDINATION.md`. Both the T46 work log and this final publish check are retained; no session work was discarded.

## Final publish check — Board follow-up (`3c65c9fa`, 26 November 2026 UTC)

- **PR [#18](https://github.com/kanlerxz87-cyber/NYFun3/pull/18)** (board follow-up and T46 integration) merged at `499b8564ad7b0db5bcc94124cbf0bf02afdd27d7` on 2026-11-26 14:12:24 UTC.
- **CI:** [push run 45836519113](https://github.com/kanlerxz87-cyber/NYFun3/actions/runs/45836519113) and [pull_request run 45836530245](https://github.com/kanlerxz87-cyber/NYFun3/actions/runs/45836530245) both passed `Validate static site`; local validators, source-integrity checks, rendered-table checks, DOM smoke tests, and `git diff --check` also passed.
- **GitHub Pages:** API reported `status: built` for `499b856` at 14:12:48 UTC with `error.message: null`, source `main` `/`, HTTPS enforced.
- **Live URLs rechecked:** root dashboard, Flagged for Review, `guide-2026.html`, `COORDINATION.md`, and `CURRENT_AUDIT.md`. The live root dashboard showed the new Guide 2026 card and nav link; Flagged for Review showed the corrected NR-01 “Distinction 3” filter-badge explanation and NR-09; the board showed T16 `done` and the PR #16 merge record.
- **Final state:** T16 is `done`, PR #16 and its follow-up PR #18 are merged, Pages is built, and no further PR from this session is planned. NR-01–NR-09 remain published as `needs review` and do not block the live site.

## Session `550e02c4` — Claim & coordination log (completed T21–T23 on 2026-11-26 UTC)

- **Branch:** `arena/550e02c4-nyfun3` (fixed by Arena harness; rebased onto `origin/main` at `3f922c9`).
- **Non-overlapping scope rule:** Concurrent sessions observed on remote branches (`3c65c9fa`, `53d4ee2e`, `8e38e7e7`, `46804a5a`, `67e5a326`) are respected; no session's work log or files were discarded.

| ID | Task | Status | Owner session | File scope |
|---|---|---|---|---|
| T21 | Official MICHELIN Guide Listed (`Selected`) & `Bib Gourmand` vs Starred dataset + couple menu & hours verification | `done` | `550e02c4` | `data/michelin_guide_selection.json`, `guide-selection.html` |
| T22 | First-party hotel room/bed/bathroom/amenity verification, NYC official hotel-tax breakdown, 1–2 week window & booking-timing matrix | `done` | `550e02c4` | `data/hotel_verification_550e02c4.json`, `booking-strategy.html` |
| T23 | Targeted repository & official-source verification ledger (`V55-01`–`V55-14`: Blue Angel windowless `NQ1` & Midtown East address, Artezen `$13.95+tax/night` mandatory facility fee, Eurostars `27 m²` Queen + bathtub, Mayfair `100 sq ft` Double & stray Wisconsin Dells copy, Pestana CR7 Double-vs-King & suspended breakfast) | `done` | `550e02c4` | `research/verification-550e02c4.md`, `COORDINATION.md` |

- **Built (`arena/550e02c4-nyfun3`):**
  - [`guide-selection.html`](guide-selection.html) & [`data/michelin_guide_selection.json`](data/michelin_guide_selection.json) — 12 additional line-by-line verified Manhattan non-starred MICHELIN Guide picks (`Atoboy` $150, `Ai Fiori` $290, `Manhatta` $256–$336 dinner / $130–$156 lunch, `One White Street` $290, `Don Angie` $130–$193, `Upland` $80–$124, `La Dong` $60 or $87, `Thai Diner` $67 or $76, `Dhamaka` $82 or $108; `Nyonya`, `Nami Nori` and `Ruffian` prices left blank + `unverified`), dynamically combined with all 25 priced starred rows (`37` combined venues) + 6 Manhattan dining clusters and explicit profile / video-result / search-discovery social badges, without claiming independent verification.
  - [`booking-strategy.html`](booking-strategy.html) & [`data/hotel_verification_550e02c4.json`](data/hotel_verification_550e02c4.json) — First-party room-fit, address, amenity, and fee verification across 10 selected hotel properties (`Eurostars Wall Street` `27 m²` Queen + private bathtub; `The Artezen Hotel` mandatory `$13.95 + tax/night` facility fee; `Blue Angel Hotel NYC` Choice Ascend `ny842` at `152 E. 55th St` with windowless `NQ1` entry Queen warning; `The Mayfair Hotel` `100 sq ft` Double warning; `Pestana CR7` King-only rule + suspended breakfast FAQ), NYC DOF statutory hotel tax math (`14.75% + $3.50/night`), and Feb 15–Mar 23, 2027 weekly window curve.
  - [`research/verification-550e02c4.md`](research/verification-550e02c4.md) — Complete 14-item (`V55-01`–`V55-14`) line-by-line official-source verification ledger.
- **Validation:** `python3 scripts/validate_site.py`, `python3 scripts/check_sources.py`, `python3 scripts/check_inline_js.py`, `node scripts/check_rendered_tables.js`, `node scripts/smoke_pages.js`, and `git diff --check` all passed locally.

### Follow-up integration claim — `550e02c4` (2026-11-26 UTC)

| ID | Task | Status | Owner session | File scope |
|---|---|---|---|---|
| T74 | Link the new Guide-listed and hotel-verification pages from existing dashboards, add review cautions, validate and publish PR #21 | `done` | `550e02c4` | `index.html`, `guide-2026.html`, `flagged-for-review.html`, `COORDINATION.md` |

The prior integration T24 is complete, and PR #19 merged; this follow-up preserves both previous integrations. No other open PR currently claims these files.

**T74 result:** Added dashboard cards and Guide links, published NR-10, and removed unsupported blanket 2027 transit and uncertain hotel checkout assertions from the older Guide page. Five local validators and `git diff --check` pass; jsdom interaction checks additionally confirmed the 37-row combined dining filter and the hotel search filter. PR [#21](https://github.com/kanlerxz87-cyber/NYFun3/pull/21) is the publication vehicle; its final merge/deployment status is recorded after the event.

## Publish check — Session `67e5a326` / PR #19 (26 November 2026 UTC)

- **PR [#19](https://github.com/kanlerxz87-cyber/NYFun3/pull/19)** (`arena/67e5a326-nyfun3` → `main`) merged at `8cde9f61c690aed6b8068ccae2855db4c576121f` on 2026-11-26 14:28:43 UTC.
- **CI:** [Validate static site run 45839115459](https://github.com/kanlerxz87-cyber/NYFun3/actions/runs/45839115459) passed on the PR head (both PR-head checks green before merge); merge commit `8cde9f6` passed the `Validate static site` push check (run `45839414246`, 18 s) — see below for the fresh post-merge verification.
- **GitHub Pages:** API reported `status: built`, `error.message: null`, source `main` `/`, HTTPS enforced; pages-build-deployment for `8cde9f6` completed (run `45839413770`, 27 s).
- **Live checks:** outbound HTTPS from this sandbox was cut mid-session (TLS EOF on every `kanlerxz87-cyber.github.io` URL), so the post-merge live verification was done by reading the deployed artifacts directly from `main` (the exact source GitHub Pages serves): `restaurants.html`/`michelin.html`/`activities.html` carry the T72 `review_links` footnotes and the `NYF.reviewCell` renderer call; `data/activities.json` carries 15/15 `review_links` rows (e.g. MoMA iKhkApixPYA/cUiBPdqd_m8) and `data/michelin_all.json` carries 10/10 priced rows; `assets/app.js` exports `reviewCell`. Direct live fetches of the published pages could not be repeated after the sandbox lost egress — flagged for the reviewer as a **verification limitation**, not a site claim.
- **Result:** T72 `done` and live on `main`; T73 `superseded` (main's T67/T71 implementation governs). NR-01…NR-09 remain `needs review`; no flag was closed by this merge.

## Publish check — Session `550e02c4` / PR #21 (26 November 2026 UTC)

- PR [#21](https://github.com/kanlerxz87-cyber/NYFun3/pull/21) merged at `a4323c0978be4a2ffa3fbc25bd1cb23e20652990` on 2026-11-26 14:32 UTC; T21–T23 and T74 are complete.
- Both PR/push Validate static site checks passed, including jsdom smoke tests. The Pages run for `a4323c0` was canceled when a newer main build superseded it; the subsequent Pages run `45840009266` succeeded, and the Pages API reported `built` for descendant `0bed49d`.
- Cache-busted live checks opened `guide-selection.html`, `booking-strategy.html`, and `flagged-for-review.html` including NR-10; the live dashboard linked both new pages. Restaurant menu examples and older hotel snapshots remain time-sensitive, and actual 2027 routes/fees must be checked at booking.

## Session `551dcafd` — Claim & final verification (2026-11-27 UTC)

- **Branch:** `arena/551dcafd-nyfun3` (fixed by Arena harness; base `c1e3be0` = main after PR #22).
- **Scope (non-overlapping):** `COORDINATION.md` (this log only) + verification-only audit; no shared data/nav files edited.

| ID | Task | Status | Owner session | File scope |
|---|---|---|---|---|
| T80 | Independent final verification: re-run all validators, spot-check data counts, confirm Pages status, publish PR to main | `in progress` | `551dcafd` | `COORDINATION.md` |

- **Verification performed (2026-11-27):** `validate_site.py`, `check_sources.py`, `check_inline_js.py`, `check_rendered_tables.js` all pass (18 JSON, 19 HTML, 203 rendered rows). `data/michelin_all.json` = 72 starred rows. GitHub Pages API: `status: built`, source `main` `/`, HTTPS enforced. Direct `curl` to `*.github.io` returns 000 from this sandbox (egress blocked, same limitation noted in PR #19) — live content verified via Pages API + deployed `main` artifacts instead.
- **Irregularity flagged:** MICHELIN New York 2026 ceremony is 14 Dec 2026 (after this audit, before the trip) — star status must be re-checked after that date; already flagged on `plan.html` / `flagged-for-review.html`. NR-01–NR-10 remain `needs review` and do not block merge.

## Session `957d4019` — Official-source spot audit (T81, 2026-11-27 UTC)

- **Claim:** T81 (commit `ed8ac3b`), scope limited to `research/audit-957d4019.md` and this board. No shared output (`data/*.json`, root HTML, `flagged-for-review.html`, `plan.html`) was edited.
- **Sources opened (27 Nov 2026):** [MICHELIN NYC all-starred directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred); [NYC DOF hotel room occupancy tax](https://www.nyc.gov/site/finance/business/business-hotel-room-occupancy-tax.page); [MoMA visit](https://www.moma.org/visit/); [The Met plan your visit](https://www.metmuseum.org/plan-your-visit); [CityPASS New York](https://www.citypass.com/new-york); [MTA GTFS transition guidance](https://www.mta.info/developers/gtfs-schedules-transition); [HGU Queen Standard](https://www.hgunyc.com/stay/queen).
- **Confirmed:** NYC star counts 5 / 14 / 50 (NR-01); MoMA admission and weekly hours, and the Friday evening exception; The Met's $30 non-resident adult admission; NYC $2.00/day room fee and NYS $1.50/day unit fee; CityPASS $149 + $2 and $307.04 regular price; the MTA GTFS transition caveat (NR-04); HGU "solo traveler" wording.
- **Not confirmed (kept open):** The Met Fifth Ave weekday hours (NR-05); the 5.875% room-tax percentage attributed to DOF (I1).
- **Irregularities handed to integration (I1–I9, detail in the audit file):** 5.875% attribution; FA-12 Met "verified" wording; CityPASS "8 attractions" vs 10 listed; 69/69 saturated 1-hour metric on `hotels.html`; garbled NR-08 text; stale T80 `in progress` row; unsupported Pestana fee inference; mixed-basis cheapest-first sort; missing NY-resident Met pricing option.
- **Validation (27 Nov 2026):** `validate_site.py`, `check_sources.py`, `check_inline_js.py`, `check_rendered_tables.js` (203 source-linked rows) and `git diff --check` all passed on this branch.

- **PR:** https://github.com/kanlerxz87-cyber/NYFun3/pull/25 (open, not merged; for the final integration session to review and merge).
