# COORDINATION.md — Shared Task Board & Verification Log

## Session & Branch Coordination Protocol

- **Repository**: `kanlerxz87-cyber/NYFun3`
- **Active Session ID**: `fc94e0d3`
- **Working Branch**: `arena/fc94e0d3-nyfun3` (branched from `main` at `c251442d122a8d04aade3d8b5a0d57fd4e9ce37c`)
- **Branch Naming Note**: Arena Agent Mode fixes the active session branch to `arena/fc94e0d3-nyfun3` and prohibits creating, switching, or renaming branches. All task claims, scoped data files, verification logs, and final integration deliverables for session `fc94e0d3` are committed and pushed incrementally on `arena/fc94e0d3-nyfun3` with `git pull --rebase origin arena/fc94e0d3-nyfun3` prior to every push.
- **Verification Standard**: Every entry must be verified line-by-line against official, trusted primary sources (official venue websites, official MICHELIN Guide pages, MTA transit schedules, official hotel booking pages). If any field cannot be confirmed from an official source, it is left blank (`""` / `—`) and flagged as `Unverified` on `review.html`.

---

## Shared Task Board

| Task ID | Task Name | Status | Owning Session ID | Claimed At (UTC) | File Scope |
|---|---|---|---|---|---|
| `T1` | Repo Baseline Audit & Prompt Irregularity Analysis | `done` | `fc94e0d3` | `2026-11-25T22:34:00Z` | `data/repo_audit.json` |
| `T2` | MICHELIN Guide & Starred Restaurants, Clusters, Couple Pricing, Hours & Social Reviews | `done` | `fc94e0d3` | `2026-11-25T22:39:00Z` | `data/michelin_restaurants.json` |
| `T3` | NYC Activities, Hours, Exceptions, <=1-Hr Transit & Social Reviews | `done` | `fc94e0d3` | `2026-11-25T22:56:00Z` | `data/activities.json` |
| `T4` | NYC Hotels (Private Bath, Queen+ Bed, Verified 7-Night Pricing Feb–Mar 2027, Best Time to Book & Michelin Transit Ranking) | `in progress` | `fc94e0d3` | `2026-11-25T23:06:00Z` | `data/hotels.json` |
| `T5` | Decision Readiness (Questions & Missing Info Discovery) + Site Improvement Suggestions | `unclaimed` | — | — | `data/decision_and_suggestions.json` |
| `T6` | Final Integration, Line-by-Line Re-Verification, Dashboard Site & Subpages, Link Check & Live Preview | `unclaimed` | — | — | `index.html`, `hotels.html`, `michelin.html`, `activities.html`, `questions.html`, `suggestions.html`, `review.html`, `assets/`, `.nojekyll`, `README.md` |

---

## Coordination & Verification Log

### 2026-11-25T22:34:00Z — Session `fc94e0d3` initialized board & claimed `T1`
- Checked repository state: `COORDINATION.md` did not exist on `main` (`c251442d122a8d04aade3d8b5a0d57fd4e9ce37c`).
- Created `COORDINATION.md` and claimed `T1` (`data/repo_audit.json`).

### 2026-11-25T22:39:00Z — Session `fc94e0d3` completed `T1` & claimed `T2`
- **Verification performed**: Inspected commit `c251442d122a8d04aade3d8b5a0d57fd4e9ce37c` (`README.md`, 1 line `# NYFun3`), GitHub Pages API configuration (`main` `/`, `https://kanlerxz87-cyber.github.io/NYFun3/`), 2027 U.S. Federal Holidays (`https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/`), NYC Public Schools 2026–2027 calendar (`https://www.schools.nyc.gov/about-us/news/morning-bell/contentdetails/morning-bell/2026/04/21/2026-27-nycps-calendar-now-available`), NYC Hotel Week 2027 (`https://www.nyctourism.com/hotel-week/`), and official MICHELIN Guide NYC Star List (`https://guide.michelin.com/us/en/article/michelin-guide-ceremony/all-the-stars-in-the-michelin-guide-to-new-york-city-2025`).
- **Irregularities logged**: `IRREG-01` through `IRREG-06` saved in `data/repo_audit.json` for publication on Flagged for Review (`review.html`).
- **Next claim**: Claimed `T2` (`data/michelin_restaurants.json`).

### 2026-11-25T22:56:00Z — Session `fc94e0d3` completed `T2` & claimed `T3`
- **Verification performed**: Mapped all 70 active NYC MICHELIN-starred restaurants across 6 geographic clusters via `guide.michelin.com`, and verified 26 showcase MICHELIN Guide restaurants (5 Three-Star, 7 Two-Star, 9 One-Star, 2 Bib Gourmand, 3 MICHELIN Selected) line-by-line against official restaurant websites, Tock/menu PDFs (`DR-112026.pdf`, `chef-s-tasting-11.5.pdf`, `viacarota.com/text`, etc.), and `guide.michelin.com` pages, plus verified YouTube/TikTok/Instagram links.
- **Irregularities logged**:
  - `I Sodi` (`R25`): Official site (`https://www.isodinyc.com/`) publishes no menu item prices; couple total left blank and flagged `Unverified` (MICHELIN lists `$$$`).
  - `Manhatta` (`R26`): Official site (`https://www.manhattarestaurant.com/chefs-counter/`) states the $275/pp Chef's Counter is paused; Bar/à la carte verified.
  - `Joo Ok` (`R11`), `Gramercy Tavern` (`R15`), `Torrisi` (`R17`), `Oxomoco` (`R21`), `Cho Dang Gol` (`R22`), `Via Carota` (`R24`), `I Sodi` (`R25`), `Manhatta` (`R26`): Individual platform cells without confirmed video/profile matches left empty (`[]`) rather than inferred.
- **Next claim**: Claimed `T3` (`data/activities.json`).

### 2026-11-25T23:06:00Z — Session `fc94e0d3` completed `T3` & claimed `T4`
- **Verification performed**: Verified 16 NYC couple activities line-by-line against official attraction websites (`metmuseum.org`, `moma.org`, `amnh.org`, `summitov.com`, `rockefellercenter.com`, `esbnyc.com`, `nps.gov/stli`, `911memorial.org`, `hadestown.com/tickets`, `metopera.org`, `whitney.org`, `thehighline.org`, `themorgan.org`, `wollmanrinknyc.com`, `brooklynbridgepark.org`, `siferry.com`) plus verified YouTube/TikTok/Instagram review links.
- **Critical 2027 schedule irregularities caught & logged**:
  - `IRREG-07` (**The Metropolitan Opera Winter Hiatus**): Per `https://www.metopera.org/season/tickets/group-sales/extraordinary-every-night/2026-27/`, the Met Opera has **NO PERFORMANCES FROM JAN 31 TO MAR 7, 2027**, reopening Monday, March 8, 2027 (`Silent Night`, `Aida`, `Manon`). Completely unavailable during the preferred Feb 15–18 window!
  - `IRREG-08` (**Wollman Rink 2026–27 Season End Date**): Per `https://wollmanrinknyc.com/plan/`, the rink closes for the season on **March 16, 2027** (unavailable March 17–23, 2027), and closes early at **2:30 PM** on Mondays & Tuesdays.
  - `IRREG-09` (**9/11 Memorial Museum 2027 Tuesday Closures**): Closed on select winter Tuesdays (`Feb 24, Mar 3, Mar 10, Mar 17` schedule pattern) while open during school-break Tuesday.
  - `IRREG-10` (**The Met Cloisters Transit Threshold**): Reachable in 38–48 min via `A` express from Midtown/UWS hotels, but 55–62 min from Brooklyn/FiDi hotels — flagged as borderline on the `<= 60 min` rule.
- **Next claim**: Claimed `T4` (`data/hotels.json`).
