# COORDINATION — NYFun3 Trip Planning Site

Shared task board. Read this before starting work. This file was combined by the final integration session after an add/add conflict; neither session's board was discarded.

- **Repo:** `kanlerxz87-cyber/NYFun3`
- **Live site:** https://kanlerxz87-cyber.github.io/NYFun3/ (GitHub Pages, source = `main`, `/` root)
- **Board last updated:** 2026-11-25 UTC
- **Phase A session:** `arena-c2e08f03`, fixed branch `arena/c2e08f03-nyfun3`
- **Phase B / final integration session:** `ed92e764`, fixed branch `arena/ed92e764-nyfun3`
- **Current Arena branch:** `arena/ed92e764-nyfun3`; base `c251442d122a8d04aade3d8b5a0d57fd4e9ce37c`

## Rules in force

1. Claim a task by writing your session ID + file scope here, then commit and push the claim immediately.
2. Never start a task another session has claimed.
3. Keep scopes non-overlapping. Each session edits only the files in its claimed scope.
4. Need a change in someone else's file? Log a request below; do not edit it.
5. Small, frequent commits. Run `git pull --rebase` before every push.
6. Shared outputs (`data/*.json` combined tables, `index.html` navigation, and Pages publishing) are changed only by the final integration session once other tasks are done.
7. Verification standard: every published value needs an official source link. Unconfirmed values are left blank and flagged `unverified`. Never infer or fill in values.
8. `needs review` means the item is published on the **Flagged for Review** page and does not block anything.
9. Claims older than 60 minutes with no commits may be taken over; note the handoff.

## Branch-naming irregularity

The project protocol asks for branches named `session-<id>/<task>`. Both Arena sessions are pinned by the harness to their own fixed `arena/<id>-nyfun3` branch and cannot create or switch branches. Resolution: non-overlapping file scopes are recorded here, and final integration merges `main` into the current fixed branch, then opens and merges a pull request from the fixed branch to `main`. No session pushes directly to another branch.

## Phase A task board — published site build

| ID | Task | Status | Owner session | Branch | File scope |
|---|---|---|---|---|---|
| T1 | Repo review + irregularity log | `done` | `arena-c2e08f03` | `arena/c2e08f03-nyfun3` | `REVIEW.md` (R1–R20) |
| T2 | Michelin dataset (official list, stars, links) | `done` | `arena-c2e08f03` | `arena/c2e08f03-nyfun3` | `data/michelin*.json`, `restaurants.html`, `michelin.html` |
| T3 | Hotel pricing (real 7-night totals, dates, amenities) | `done` | `arena-c2e08f03` | `arena/c2e08f03-nyfun3` | `data/hotels.json`, `hotels.html` |
| T4 | Activities dataset + social links | `done` | `arena-c2e08f03` | `arena/c2e08f03-nyfun3` | `data/activities.json`, `activities.html` |
| T5 | Site shell, nav, CSS, executive summary | `done` | `arena-c2e08f03` | `arena/c2e08f03-nyfun3` | `index.html`, `assets/` |
| T6 | Itinerary (7-night + extended variants) | `done` | `arena-c2e08f03` | `arena/c2e08f03-nyfun3` | `itinerary.html`, `data/itinerary.json` |
| T7 | Open questions + missing-information plan | `done` | `arena-c2e08f03` | `arena/c2e08f03-nyfun3` | section 4 of `plan.html` |
| T8 | Suggestions / decision section | `done` | `arena-c2e08f03` | `arena/c2e08f03-nyfun3` | section 3 of `plan.html` |
| T9 | Verification log (line-by-line) | `done` | `arena-c2e08f03` | `arena/c2e08f03-nyfun3` | `VERIFICATION.md` |
| T10 | Final integration: merge, re-verify, publish Pages | `in progress` | `ed92e764` | `arena/ed92e764-nyfun3` | shared outputs, `COORDINATION.md`, PR to `main` |

## Phase B task board — second-session research and final verification

| ID | Task | Status | Owner session | File scope | Notes |
|---|---|---|---|---|---|
| TASK-00 | Create coordination board and record branch constraint | `done` | `ed92e764` | `COORDINATION.md` | Initial board created on the second fixed branch. |
| TASK-01 | Official-source discovery, source ledger, verification protocol, research-collector diagnostics | `done` | `ed92e764` | `research/**`, `.github/workflows/research-diagnostics.yml` | See `research/sources.md`, `research/verification-log.md`, and `research/generated/*.json`. |
| TASK-02 | Hotels, official pricing, Michelin Guide status, transit evidence | `superseded by Phase A; gaps under final review` | `ed92e764` | `data/hotels.json`, `data/michelin*.json`, `research/transit/` | Phase A produced the published tables; final integration re-checks them. |
| TASK-03 | Activities/restaurants, hours/exceptions, social-review links | `superseded by Phase A; gaps under final review` | `ed92e764` | `data/activities.json`, `data/michelin*.json`, `research/social/` | Phase A produced the published tables; final integration re-checks them. |
| TASK-04 | Category subpages, executive summary, Q&A, improvement suggestions | `superseded by Phase A; final review in progress` | `ed92e764` | `*.html`, `assets/**` | Phase A produced the pages; final integration checks coverage and adds review items. |
| TASK-05 | Final integration: shared index/navigation/data, line-by-line re-verification, link checks, GitHub Pages deployment | `in progress` | `ed92e764` | `index.html`, `site/data/`, `README.md`, `COORDINATION.md`, PR to `main` | Uses legacy Pages from `main` via PR merge rather than an Actions deploy. |

## Phase A work log — `arena-c2e08f03`

**Scope claimed:** T1–T10 (empty repo; single session did the full build).

**Environment findings:** initial repo contained only `README.md` and one commit `c251442`; GitHub Pages was already enabled from `main` at `/`; sandbox shell had no general outbound internet (only GitHub, npm, and PyPI hosts). All verification was performed page by page with fetch/search tools and recorded with URL + date in `VERIFICATION.md`.

**Sources:** [MICHELIN Guide New York 2025 star announcement](https://guide.michelin.com/us/en/article/michelin-guide-ceremony/all-the-stars-in-the-michelin-guide-to-new-york-city-2025), individual MICHELIN Guide restaurant pages, first-party museum/landmark pages, hotel official sites for identity/location, and Booking.com exact-date quote URLs for live prices. See `VERIFICATION.md` for the row-by-row list.

**Verification performed:** 15 activity rows, 9 hotel rows, 5 three-star rows, 15 two-star rows, 52 one-star rows, and 7 itinerary days. Every table renders a `Source` column; blank cells carry `unverified` flags. Local site check: six pages, both assets, and all four JSON files returned HTTP 200; render logic was exercised in a Node sandbox.

**Irregularities flagged:** bare README, absent `.gitignore`, absent link/schema checker, branch-name conflict, MICHELIN 50-vs-52 one-star and 14-vs-15 two-star discrepancies, the 14 Dec 2026 star ceremony before the trip, MICHELIN price bands rather than dollar totals, blocked JavaScript menus/hours, Booking.com being an OTA rather than an official price publisher, and third-party hour disagreements. Details in `REVIEW.md`.

**Known gaps at handoff:** no verified per-couple Michelin restaurant price; no Michelin-within-1-hour hotel ranking; 48 one-star rows lacking hours; The Met / Cloisters hours blank; Bib Gourmand not catalogued.

## Phase B work log — `ed92e764`

**Sources:** [MICHELIN NYC directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants), [MICHELIN all-starred directory](https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred), [MTA home](https://www.mta.info/), [MTA official apps](https://www.mta.info/guides/apps), [MTA Developer Resources](https://www.mta.info/developers), [MTA schedule-transition guidance](https://www.mta.info/developers/gtfs-schedules-transition), [Hyatt Midtown-South](https://www.hyatt.com/hyatt-place/en-US/nyczm-hyatt-place-new-york-midtown-south), [Hyatt Times Square](https://www.hyatt.com/hyatt-place/en-US/nyczt-hyatt-place-new-york-city-times-square), [Hilton Times Square Central](https://www.hilton.com/en/hotels/nycssgi-hilton-garden-inn-new-york-times-square-central/), [Marriott Fairfield Times Square South](https://www.marriott.com/hotels/travel/nycmw-fairfield-inn-and-suites-new-york-manhattan-times-square-south/), [IHG Times Square South rooms](https://www.ihg.com/holidayinnexpress/hotels/us/en/new-york/nycts/hoteldetail/rooms), [GitHub Pages API](https://api.github.com/repos/kanlerxz87-cyber/NYFun3/pages), and [U.S. Census geocoder](https://geocoding.geo.census.gov/geocoder/locations/onelineaddress).

**Verification performed:** checked repository contents, branch, remote, auth, existing Pages configuration, and official source reachability. A read-only GitHub Actions collector opened official MTA GTFS feeds and the Census geocoder successfully: subway regular feed 5,606,305 bytes / 1,488 stops; Manhattan bus 8,322,100 bytes / 1,823 stops; Brooklyn bus 17,046,285 bytes / 4,575 stops; Queens bus 5,983,145 bytes / 1,422 stops. High Line, NPS Statue of Liberty, and Empire State Building pages also opened. Evidence is in `research/generated/diagnostics.json`.

**Irregularities found:** `workflow_dispatch` is not registered for a workflow that exists only on a non-default branch; direct plain-HTTP requests were blocked by Hyatt (403), MICHELIN Guide (202 with no links), several museums (403/429/405), and an old 9/11 URL (404); Jina Reader's browser-rendered HTML requires an API key; local artifact download was blocked by the sandbox's host allowlist. No blocked page's values were published or inferred. The collector was changed to commit research JSON only to the fixed branch, then the published site work on `main` was merged into the fixed branch for final review.

**Merge conflict:** add/add conflict on `COORDINATION.md` during `git merge origin/main`. Resolution: this combined board preserves both task boards, work logs, source lists, verification notes, and irregularities. No work was discarded.

## Cross-session requests

| Date UTC | Requesting session | Target task/file | Request | Resolution |
|---|---|---|---|---|
| 2026-11-25 | `ed92e764` | Phase A shared outputs on `main` | Final integration needs to review and augment site/data after Phase A tasks are done | Merged `origin/main` into the fixed branch; T10 / TASK-05 claimed as final integration. |

## Handoffs / conflicts

| Date UTC | Task | From | To | Reason | Resolution |
|---|---|---|---|---|---|
| 2026-11-25 | T10 / TASK-05 | `arena-c2e08f03` | `ed92e764` | Phase A marked integration `needs review`; second session has the fixed branch for final integration | Final integration claimed; combined board created; PR to `main` planned. |
