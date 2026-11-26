# Fresh decision-readiness audit — NYC trip planner

**Audit date:** 26 November 2026 (UTC)
**Scope:** repository review, published JSON/HTML, validation scripts, live GitHub Pages URLs, and direct inspection of official MICHELIN, government tax, hotel, and MTA sources.
**Purpose:** record what the current repository supports, what was independently rechecked, and what remains unsupported. This is not a booking quote, itinerary confirmation, or substitute for rechecking each venue/rate at booking.

> **Current state:** `main` now includes 14 hotels, direct SynXis/Arlo all-in quotes and seasonality, 25 official priced MICHELIN rows, 71 / 72 Guide-hours rows, a measured current-timetable MTA GTFS ≤1 h ranking, a decision cockpit, evidence/flags registers, and nine published needs-review items. Earlier baseline counts in historical logs are superseded by this audit.

## Executive summary

The repository is a mobile-first static dashboard with category pages, a 7-day itinerary, executive summary, suggestions, questions, detailed dossier, decision cockpit, and a clearly labeled Flagged for Review page. Every published data row has a source link; unknown values stay blank and flagged. Local validators, CI, rendered-table checks, source-integrity checks, and DOM smoke tests pass. These checks prove structure, arithmetic, links, and rendering; they do not prove that a live external page still supports every captured value.

**Current evidence is strong enough to shortlist hotels and compare dining areas, but not to promise a final 2027 booking.** Direct all-in quotes now exist for several properties (Pod 51 $1,109, Pod 39 $1,138, Pod Times Square $1,195, HGU $1,200 King / $1,257 Queen, Shoreham $199/nt) and late-February seasonality is measured against March. A current-timetable GTFS model finds every hotel reaches the same 65 measured starred restaurants within 60 minutes, so the 1-hour count cannot by itself rank hotels; median door-to-door time and tie-resolution caveats are published. Still unresolved: 2027 service changes and holiday hours, star status after the 14 Dec 2026 ceremony, exact final checkout totals, a purchase-timing rule, Guide-listed/Bib Gourmand cataloguing, and menu-option comparability. No 2027 schedule, star, rate, or blank value has been inferred.

## Coverage and evidence table

| Requirement / finding | What the repository currently contains | Audit status and limitation | Source / next check |
|---|---|---|---|
| Travel window and length | 7-day plan begins Mon 15 Feb 2027; 7-night hotel quotes cover 15–22 Feb; 14-night quotes cover 15 Feb–1 Mar; three second-week suggestions are present. | **Partial.** The 15 Feb–23 Mar choice window is not exhaustively priced, and no dated 14-day itinerary is supplied. | [Itinerary data](data/itinerary.json) · [Hotel data](data/hotels.json) |
| Preferred dates / holiday exception | The itinerary starts 15 Feb 2027. | **Confirmed calendar exception.** OPM lists Monday 15 February 2027 as Washington’s Birthday. Venue-by-venue 2027 holiday hours still need official confirmation. | [OPM 2027 federal holiday schedule](https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/) · [Itinerary data](data/itinerary.json) |
| Hotel comparisons | 14 properties; direct SynXis/Arlo all-in or pre-tax quotes where available; clearly labeled Booking.com snapshots; exact room/bed/bath notes; Feb–Mar seasonality. | **Useful but not a 2027 guarantee.** Direct all-in quotes resolve several earlier gaps, but cancellation, room category, fee inclusion, and final checkout terms still need rechecking. Some amenity fields remain blank/flagged. | [Hotel data](data/hotels.json) · [Pod 51 direct quote](https://be.synxis.com/?hotel=41155&arrive=2027-02-15&depart=2027-02-22&adult=2&child=0) · [HGU official site](https://www.hgunyc.com/) |
| Cheapest dates / best time to book | Direct Pod 51 quotes show Feb 15–22 ($1,109) and Feb 22–Mar 1 ($1,138) are ~30–45% cheaper than Mar 1–8 ($1,628) and Mar 15–22 ($2,004); 14-night Feb 15–Mar 1 is $2,246. | **Partially resolved for tested travel dates.** A universal best date to purchase is still unsupported; repeated dated quotes under identical conditions would be needed. | [Pod 51 Feb quote](https://be.synxis.com/?hotel=41155&arrive=2027-02-15&depart=2027-02-22&adult=2&child=0) · [Pod 51 Mar quote](https://be.synxis.com/?hotel=41155&arrive=2027-03-15&depart=2027-03-22&adult=2&child=0) · [NR-03](flagged-for-review.html#NR-03) |
| Hotel ranking by MICHELIN venues within ≤1 hour | 14 hotels have measured current-timetable GTFS counts; every hotel reaches the same 65 measured starred restaurants inside 60 minutes; 7 of 72 rows are unmeasured because addresses/geocodes were unavailable. The cockpit ranks by median door-to-door time and publishes tie-resolution caveats. | **Measured, not a 2027 guarantee.** Subway feed covers the current published timetable; bus feeds expire 2027-01-01, and Presidents’ Day/weekend work must be rechecked near travel. | [Transit data](data/transit_hotels.json) · [Ranking](data/hotel_ranking.json) · [MTA guidance](https://www.mta.info/developers/gtfs-schedules-transition) · [Decide](decide.html) |
| Current MICHELIN star status | Dataset retains the official 2025 announcement’s 72 rows (5 / 15 / 52). The current NYC all-starred directory reports 69 active NYC restaurants (5 / 14 / 50) and adds four new names while omitting fire-damaged Shion 69 Leonard Street. | **Needs reconciliation after the 14 Dec 2026 ceremony.** Two same-day directory fetches displayed different three-star counts (3 and 5); the dynamic aggregate is flagged, not silently reconciled. | [Official all-starred directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred) · [2025 announcement](https://guide.michelin.com/us/en/article/michelin-guide-ceremony/all-the-stars-in-the-michelin-guide-to-new-york-city-2025) · [Michelin Media ceremony](https://michelinmedia.com/pages/blog/detail/article/c/a1479/) |
| Guide-listed (non-starred) vs starred venues | 72 starred rows; Bib Gourmand / merely Guide-listed venues are not fully catalogued. Some named Guide-listed examples appear in evidence notes. | **Partial.** Star tiers are explicit, but broader Guide coverage is incomplete. | [MICHELIN NYC directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants) · [NR-06](flagged-for-review.html#NR-06) |
| Restaurant hours and couple costs | 71 / 72 rows have Guide hours; one closed venue is blank/flagged. 25 rows have official per-person menu/Tock/PDF arithmetic; 47 remain blank. | **Partial, deliberately blank where unsupported.** Published totals are menu subtotals, not all-in bills or 2027 prices; multiple options on one first-party page are not like-for-like. | [Combined restaurant data](data/michelin_all.json) · [MICHELIN directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants) · [NR-09](flagged-for-review.html#NR-09) |
| Activities, dates, hours, and admission | 15 activities; some hours/admission cells remain blank or partial where official pages did not render. | **Partial.** Baseline hours and exceptions are linked, but 2027 holiday/day-specific calendars are not confirmed. | [Activities data](data/activities.json) · [OPM holiday calendar](https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/) |
| Social links | Activity and restaurant rows carry YouTube/TikTok/Instagram discovery links. | **Lead-only.** Search/hashtag links are not verified venue-specific creator posts and are not factual sources. | [Activities data](data/activities.json) · [Review-link audit](data/review_links.json) |
| Questions, suggestions, and flags | `plan.html` has an executive summary, reviewable suggestions, and open questions; `decide.html` has a decision cockpit; `flagged-for-review.html` publishes NR-01–NR-09 and resolved corrections. | **Present.** These support decision-making but do not replace missing 2027 confirmations. | [Plan](plan.html) · [Decide](decide.html) · [Flagged for Review](flagged-for-review.html) |

## Decision checklist — what must be settled before a reasonable booking decision

| Question to resolve | Current answer from repository | Evidence needed to answer it | Source / starting point |
|---|---|---|---|
| Exact check-in/check-out and 7 vs 14 nights? | No final user choice; 7-night and 14-night examples are priced for Feb 2027. | Confirm the exact dates and stay length, then re-quote every finalist for that span. | [Hotel quote matrix](data/hotels.json) · [NR-07](flagged-for-review.html#NR-07) |
| Does “cheapest upcoming time to book” mean cheapest travel dates or best purchase date? | Travel-date seasonality is measured for tested dates; purchase timing is not established. | Treat as separate analyses; preserve dated repeated quotes under identical room/cancellation conditions. | [NR-03](flagged-for-review.html#NR-03) |
| Which room options definitely satisfy private bathroom and queen-or-larger? | Several direct quotes and official room pages now document fit; some low-cost snapshots remain conditional. | Capture room name, exact bed/bath wording, occupancy, cancellation, total incl. taxes/fees, and quote timestamp from the actual offer. | [Hotel data](data/hotels.json) · [NR-02](flagged-for-review.html#NR-02) |
| Which hotel is best for MICHELIN dining within one hour? | All 14 hotels reach the same 65 measured starred restaurants within 60 minutes; median time and tie caveats are published. | Choose on price/room/area rather than the tied count; re-run date/time-specific MTA journeys near travel. | [Decide](decide.html) · [Ranking](data/hotel_ranking.json) · [NR-04](flagged-for-review.html#NR-04) |
| Which star status and Guide-only venues should be used? | Static 2025 list plus flagged current-directory differences; 2027 status is unknowable before the ceremony. | Reconcile individual Guide pages after 14 Dec 2026 and add a `checked_on` date for each venue. | [Official directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred) · [NR-01](flagged-for-review.html#NR-01) |
| Which hours apply on the chosen 2027 dates? | Current baselines and some exceptions only; one closed restaurant and several activity panels remain partial. | Recheck each official 2027 calendar, including 15 Feb holiday hours and reservation availability. | [Activities data](data/activities.json) · [NR-05](flagged-for-review.html#NR-05) |
| What dinner budget should be used? | 25 menu subtotals are published; 47 are blank, and multiple first-party menu options are not like-for-like. | Decide tasting-menu/lunch/dinner scope and state exclusions separately from any all-in bill. | [Restaurant data](data/michelin_all.json) · [NR-09](flagged-for-review.html#NR-09) |

## Reviewable recommendations

1. **Do not promise a final 2027 “best hotel” or all-in total.** Use the direct quotes to shortlist, then re-check the exact room, date, cancellation, and checkout breakdown before paying.
2. **Reconcile MICHELIN status after the ceremony.** The 69-active-NYC directory and 72-row 2025 announcement differ; two same-day fetches also displayed different three-star counts. Preserve both observations as a dynamic-page irregularity.
3. **Keep the one-hour definition auditable.** Count only date/time-specific door-to-door results at ≤60 minutes, list unmeasured destinations, and recheck post-Feb 2027 schedules.
4. **Date-check holiday operations.** 15 Feb 2027 is a federal holiday; preserve baseline and holiday exceptions as distinct fields.
5. **Separate source authority.** Direct hotel pages/engines support hotel facts; OTAs are labeled snapshots. MICHELIN and venue pages remain the authority for stars, hours, and menu wording; government pages support tax components.
6. **Keep social links as discovery only.** Do not treat search/hashtag links as evidence for price, hours, access, or award status.

## Repository checks performed

After rebasing onto current `main` and re-applying the independent source corrections:

```text
python3 scripts/validate_site.py
python3 scripts/check_inline_js.py
node scripts/check_rendered_tables.js
python3 scripts/check_sources.py
node scripts/smoke_pages.js
git diff --check
```

All passed. The rendered-table check produced 203 source-linked rows across 6 dynamic renderers, including 50 priced rows; the DOM smoke test executed 10 pages. These automated passes establish internal consistency, link coverage, and rendering only. They do not independently verify live external pages, hotel availability, future transit journeys, or the correctness of every captured fact.

## Official sources directly inspected

- [MICHELIN NYC all-starred directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred) — one 26 Nov 2026 fetch showed 3 / 14 / 50 and an independent recheck showed 5 / 14 / 50 (sum 69) against a 69-result heading.
- [2025 NYC star announcement](https://guide.michelin.com/us/en/article/michelin-guide-ceremony/all-the-stars-in-the-michelin-guide-to-new-york-city-2025) and [Michelin Media 2026 ceremony announcement](https://michelinmedia.com/pages/blog/detail/article/c/a1479/).
- [HGU New York](https://www.hgunyc.com/) and [contact](https://www.hgunyc.com/more/contact); [Marriott citizenM New York Times Square](https://www.marriott.com/en-us/hotels/nyczt-citizenm-new-york-times-square/overview/).
- [NYC DOF hotel-room occupancy tax](https://www.nyc.gov/site/finance/business/business-hotel-room-occupancy-tax.page), [NYS ST-101.5](https://www.tax.ny.gov/pdf/current_forms/st/st101_5.pdf), and [NYC Council aggregate report](https://legistar.council.nyc.gov/View.ashx?GUID=4547DD67-B740-4FED-A1E3-596960BC0E98&ID=12994382&M=F).
- [U.S. OPM Federal Holidays](https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/) and [MTA schedule-transition guidance](https://www.mta.info/developers/gtfs-schedules-transition).
- First-party menu pages including [EMP FAQ](https://www.elevenmadisonpark.com/faq), [Gramercy Tavern](https://www.gramercytavern.com/dining-room-menu/), and [Le Coucou](https://lecoucou.com/).

## Independent recheck corrections (`3c65c9fa`, 26 November 2026)

| Check | Official source | Correction / status |
|---|---|---|
| 2026 ceremony date | [Michelin Media](https://michelinmedia.com/pages/blog/detail/article/c/a1479/) | The 14 Dec 2026 Northeast Cities ceremony is officially supported; 2027 stars still cannot be inferred. |
| MICHELIN aggregate | [Official NYC all-starred directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred) | An independent recheck displayed 5 / 14 / 50 (69), while an earlier same-day fetch displayed 3 / 14 / 50. Both are flagged as a dynamic-page irregularity; no individual star row was overwritten. |
| HGU official domain | [HGU New York](https://www.hgunyc.com/) · [HGU contact](https://www.hgunyc.com/more/contact) | `hgunewyork.com` resolved to a Namecheap parking page. Active links now use `hgunyc.com`; old values remain only as audit evidence. |
| citizenM property URL | [Marriott property page](https://www.marriott.com/en-us/hotels/nyczt-citizenm-new-york-times-square/overview/) | The old citizenM URL resolved to a generic brand page. Active links now use the official Marriott property page. |
| Hotel tax components | [NYC DOF](https://www.nyc.gov/site/finance/business/business-hotel-room-occupancy-tax.page) · [NYS ST-101.5](https://www.tax.ny.gov/pdf/current_forms/st/st101_5.pdf) · [NYC Council](https://legistar.council.nyc.gov/View.ashx?GUID=4547DD67-B740-4FED-A1E3-596960BC0E98&ID=12994382&M=F) | Unsupported `$4/night` and `$3.50–$4/night` wording was removed. Current components are 14.75% plus $2.00/day NYC occupancy tax for rent ≥$40 and $1.50/day NYS unit fee, not a 2027 quote. |
| Guide hours flags | [Official MICHELIN NYC directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred) | Four populated rows with contradictory UNVERIFIED flags were cleared; combined/tier datasets now agree on 71 / 72 populated Guide-hours rows and one closed blank/flagged venue. |
| Menu-option ambiguity | [EMP FAQ](https://www.elevenmadisonpark.com/faq) · [Gramercy Tavern](https://www.gramercytavern.com/dining-room-menu/) · [Le Coucou](https://lecoucou.com/) | Official pages expose multiple differently priced options; NR-09 asks for a service-scope decision before any like-for-like ranking. |

Unresolved checks remain on [Flagged for Review](flagged-for-review.html). No 2027 hotel quote, transit duration, star status, holiday hour, or activity calendar was inferred.
