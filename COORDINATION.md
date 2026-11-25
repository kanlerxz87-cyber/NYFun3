# COORDINATION — NYFun3 Trip Planning Site

Shared task board. Read this before starting work.

- **Repo:** `kanlerxz87-cyber/NYFun3`
- **Live site:** https://kanlerxz87-cyber.github.io/NYFun3/ (GitHub Pages, source = `main` branch, `/` root)
- **Board last updated:** 2026-11-25 (supplemental dossier session `arena/61fbe157-nyfun3`)

## Rules in force

1. Claim a task by writing your session ID + file scope here, then commit and push the claim **immediately**.
2. Never start a task another session has claimed.
3. Keep scopes non-overlapping. Each session edits only the files in its claimed scope.
4. Need a change in someone else's file? Log a request below; do not edit it.
5. Small, frequent commits. `git pull --rebase` before every push.
6. Shared outputs (`data/*.json` combined tables, `index.html` nav, Pages publish) are changed only by the final integration session.
7. Verification standard: official venue, hotel-room, award, and transit facts need a primary source link. If a date-specific hotel rate is only available from Booking.com, label and link it as a third-party snapshot, include the capture date, and state fee/tax caveats; it is never an official rate or guaranteed total. Unknown facts remain blank and flagged; never infer values.
8. Claims older than 60 minutes with no commits may be taken over; note the handoff.

## Branch-naming irregularity (logged for review)

The repo guide asks for branches named `session-<id>/<task>`. This session is pinned by the
Arena harness to `arena/c2e08f03-nyfun3` and is not permitted to create or switch branches.
Resolution: all work stays on `arena/c2e08f03-nyfun3`; the claim records the pinned branch name.
At integration time, merge `arena/c2e08f03-nyfun3` into `main`.

## Task board

| ID | Task | Status | Owner (session) | Branch | File scope | Touches |
|----|------|--------|-----------------|--------|-----------|---------|
| T1 | Repo review + irregularity log | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `REVIEW.md` (R1–R20) | — |
| T2 | Michelin dataset (official list, stars, links) | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `data/michelin*.json`, `restaurants.html`, `michelin.html` | — |
| T3 | Hotel pricing (real 7-night totals, dates, amenities) | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `data/hotels.json`, `hotels.html` | — |
| T4 | Activities dataset + social links | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `data/activities.json`, `activities.html` | — |
| T5 | Site shell, nav, CSS, executive summary | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `index.html`, `assets/` | — |
| T6 | Itinerary (7-night + extended variants) | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `itinerary.html`, `data/itinerary.json` | — |
| T7 | Open questions + missing-information plan | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | section 4 of `plan.html` (11 items) | — |
| T8 | Suggestions / decision section | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | section 3 of `plan.html` (S1–S9) | — |
| T9 | Verification log (line-by-line) | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `VERIFICATION.md` | — |
| T10 | Integration: merge to `main`, re-verify, publish Pages | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `main` publish | — |
| T11 | Supplemental curated trip dossier and source/method log | done | arena-61fbe157 | arena/61fbe157-nyfun3 | `pages/`, `RESEARCH.md`, `assets/css/site.css`, `assets/js/site.js`, `README.md` | root dashboard dossier link; Pages integration |

## Work log

### arena-c2e08f03 — 2026-11-25

**Scope claimed:** T1–T10 (empty repo; single session did the full build).

**Environment findings**

- Initial repo contained only `README.md` (`# NYFun3`, 8 bytes) and one commit `c251442`.
- GitHub Pages already enabled: source `main`, path `/`, `public: true`, HTTPS enforced.
  Live URL: https://kanlerxz87-cyber.github.io/NYFun3/
- Sandbox shell has **no general outbound internet** (only `github.com`, `codeload.github.com`,
  `api.github.com`, `registry.npmjs.org`, `pypi.org`, `files.pythonhosted.org`).
  `curl https://www.booking.com` and `curl https://guide.michelin.com` both fail with
  `OpenSSL SSL_connect: SSL_ERROR_SYSCALL`. Consequence: no scripted crawling and no automated
  link-checker. All verification was performed page-by-page with the fetch/search tools and is
  recorded with URL + date in `VERIFICATION.md`.

**Key source decisions**

- MICHELIN stars: the **2025 New York selection (published 18 Nov 2025)** is still the current
  official selection as of 2026-11-25. The next New York/Northeast ceremony is **14 Dec 2026**
  (Michelin Media, Aug 2026) — i.e. it happens *before* the trip window but *after* this research
  snapshot. Every star cell therefore carries a "readvertised at 14 Dec 2026 ceremony" caveat.
- Prices: Booking.com quotation pages for the exact stay dates, captured with the quote timestamp.
  These are live quotes, not published rack rates — recorded as observed, with the URL that
  reproduces them.

**Requests to other sessions:** none.

**Irregularities flagged** (detail in `REVIEW.md`): empty repo; branch-name convention conflict;
Booking.com is an OTA/aggregator, not an official price publisher (used for live quotes only, with
hotel official sites used for amenities); third-party listings disagree with each other on
restaurant hours, so only first-party restaurant/venue pages were accepted.

### arena-c2e08f03 — 2026-11-25 (later pass)

**Built:** `data/activities.json` (15 rows), `data/hotels.json` (9 rows), `data/michelin_all.json`
(72 merged rows: 5/15/52), `data/itinerary.json` (7 days); pages `index.html`,
`activities.html`, `restaurants.html`, `michelin.html`, `hotels.html`, `itinerary.html`,
`plan.html`; shared `assets/style.css` + `assets/app.js`; docs `REVIEW.md` (R1–R20) and
`VERIFICATION.md`.

**Local check:** served on `0.0.0.0:8000`; all 6 pages, both assets and all 4 JSON files
return HTTP 200; each page's render logic executed against the real JSON in a Node sandbox —
activities 16 rows, restaurants 73, michelin 73 + 20 cluster rows, hotels 10 + 11 rate-tier
rows. No empty renders, no JS exceptions.

**Gaps now recorded on the site itself** (not hidden):

- The 72-row starred dataset has no comprehensive per-couple menu-cost catalogue. MICHELIN
  publishes a band and many venue sites do not expose fixed menus; root table remains blank +
  flagged. The supplemental dossier adds menu arithmetic for eight selected candidates only.
  → open question Q7 remains for the full dataset.
- No Michelin "within 1 hour" hotel ranking. Needs one measured journey per hotel ×
  restaurant pair. Column `null` + flagged. → open question Q6.
- 48 of 52 one-star rows lack hours (Guide page not yet read). Flagged per row.
- The Met and The Cloisters hours cells blank — the hours panel never rendered across four
  fetches of two URLs. Third-party hours were NOT substituted.
- Bib Gourmand (~76 venues) not yet catalogued. → suggestion S4.

**New irregularity found this pass:** Michelin's own NYC filter counts 50 one-star and 14
two-star, while its 18 Nov 2025 announcement lists 52 and 15. The extra one-star names
include La Bastide (North Salem, Westchester) and the extra two-star is Blue Hill at Stone
Barns (Tarrytown). Published as a stated discrepancy, not reconciled silently.

**T10 status:** still `needs review`. Publishing requires merging this branch to `main`,
which is the integration step, and the site still has three acknowledged data gaps. Not
marked done.

**T10 executed.** `arena/c2e08f03-nyfun3` merged into `main` (`--no-ff`, six integration
merges across the session). GitHub Pages rebuilt each time; `pages/builds/latest` reports
`built` on the newest `main` commit and the live URLs serve the new pages.

Post-publish checks run against the **live** site (not just local):

- `/` `/activities.html` `/restaurants.html` `/michelin.html` `/hotels.html`
  `/itinerary.html` `/plan.html` all render with populated tables.
- Michelin cluster table: 20 rows; the "Not yet grouped" row makes the unverified
  neighbourhoods explicit instead of misfiling them under a guessed area.
- Hotel table: ordering corrected to the cheapest captured total for each property, which is
  now Blue Angel $990 → Mayfair $1,060 → HGU $1,091.60 → citizenM $1,113 → Eurostars $1,127 →
  Hyatt $1,183 → Arlo $1,255 → Pestana $1,327 → Artezen $1,358.69. The two cheapest fail the
  queen-bed rule and carry a red verdict, so the cheapest *compliant* hotel is HGU at $1,091.60.
  Duplicated "YesYes" labels removed; run-together flag text separated.
- `plan.html` §2 corrected: it previously implied every row had an area and hours. It now
  states 20 of 72 verified neighbourhoods and 48 of 52 one-star rows still missing hours.

**Three defects were found only by looking at the published site**, not by the local render
test — worth recording as a process lesson: render tests confirmed "non-empty HTML", which is
not the same as "correct HTML". All three are fixed and re-verified live.

**Latest upstream status (25 Nov 2026):** the root dataset now reports 43 of 52 one-star
rows without verified hours and 50 of 72 rows without verified neighbourhoods; earlier counts
above describe the initial pass. Remaining gaps are no comprehensive per-couple menu costs for
all 72 starred rows (the supplemental dossier has eight selected restaurant price calculations),
no Michelin-within-1-hour hotel ranking, 43 one-star hours cells, 50 ungrouped rows, and no Bib
Gourmand tier in the all-stars dataset. Each is flagged on the site and carries a concrete
method for closing it in `plan.html` §4 or `pages/findings.html`.


### arena-61fbe157 — 2026-11-25

**Scope:** T11, a separate detailed trip dossier under `pages/` plus its source/method log. Existing root datasets, activities, restaurant/MICHELIN tables, and primary dashboard structure were preserved; the root dashboard adds a single card linking to the supplement.

**Built:** `pages/index.html`, `pages/itinerary.html`, `pages/hotels.html`, `pages/dining.html`, `pages/experiences.html`, `pages/findings.html`, `RESEARCH.md`, and separate `assets/css/site.css` / `assets/js/site.js`. The dossier makes the 3-night vs. one-week conflict, 1–2 vs. 2–4-week ambiguity, conditional hotel rate evidence, unverified MTA minutes, holiday-hours uncertainty, and 2026 MICHELIN update visible.

**Verification:** Node syntax, local HTML/file/fragment/accessibility checks, and HTTP 200 checks passed for the main pages, supplement, shared assets, research log, and `.nojekyll`.

**Integration:** The existing root dashboard and README link to the nested dossier. The changes are on the pinned active branch `arena/61fbe157-nyfun3`; pull request #2 is the GitHub Pages integration path.
