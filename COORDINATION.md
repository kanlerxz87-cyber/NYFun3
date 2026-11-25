# COORDINATION.md — Shared Task Board & Verification Log

**Repository:** `kanlerxz87-cyber/NYFun3`  
**Active Session Branch:** `arena/2065a787-nyfun3` (Session ID: `2065a787`)  
**Last Updated:** 2026-11-25 (UTC)

---

## Coordination Protocol
1. Check task status before starting (`unclaimed`, `in progress`, `done`, `needs review`).
2. `needs review` items are published on the **Flagged for Review** page (`flagged.html`) and do not block execution.
3. Every table row in the published dataset and site must have a verified official source URL. Any value that cannot be confirmed from an official source must be left blank and flagged as `unverified`.
4. Commit and push claims and completed milestones with `git pull --rebase origin arena/2065a787-nyfun3` (when remote branch exists) before pushing.

---

## Task Board

| Task ID | Task Name | Status | Owning Session ID | Branch | File Scope | Notes |
|---|---|---|---|---|---|---|
| T-01 | Repository Audit & Initial Baseline Verification | `done` | `2065a787` | `arena/2065a787-nyfun3` | `COORDINATION.md`, `README.md` | Baseline `README.md` audited (`# NYFun3`, 1 line, commit `c251442`). Prompt date/duration irregularities flagged for `flagged.html`. |
| T-02 | Michelin Guide NYC Restaurants & Cluster Verification + Social Reviews | `done` | `2065a787` | `arena/2065a787-nyfun3` | `data/restaurants.json` | Verified 362 NYC Michelin Guide listings (69 Starred, 78 Bib Gourmand, 215 Selected) + 20 flagship rows with official URLs, hours, 2-adult totals & YT/TT/IG links. Flagged Torrisi (no online numeric prices), Four Horsemen (daily rotating à la carte), and Dec 14, 2026 Michelin ceremony. |
| T-03 | NYC Activities Verification, Hours, Pricing & Social Reviews | `done` | `2065a787` | `arena/2065a787-nyfun3` | `data/activities.json` | Verified 12 flagship NYC activities from official domains with 2027 seasonal hours/cutoffs (Wollman Rink closes Mar 16, 2027; High Line 8 PM winter close; Met closed Wed; 9/11 Museum closed most Tue), 2-adult totals, and YT/TT/IG links. |
| T-04 | Hotel Selection, 7-Night Real Pricing (Feb 15–Mar 23, 2027), Booking Window & <=1h Transit / Michelin Ranking | `done` | `2065a787` | `arena/2065a787-nyfun3` | `data/hotels.json` | Verified 9 Queen/King + private-bath hotels ranked #1–#9 by Michelin reach <=60m (355 down to 338 of 362; 69/69 Starred), real verified Feb/Mar 7-night totals + NYC 14.75%+$3.50/nt tax math, sweet-spot dates (Feb 21–28, 2027), and <=36m transit to all 12 activities. Flagged Club Quarters & Boro Hotel unstated official-site resort fees. |
| T-05 | Decision Questions, Missing Information & Site Improvement Suggestions | `in progress` | `2065a787` | `arena/2065a787-nyfun3` | `data/analysis.json` | Compiling known vs. missing information, pre-booking questions, discovery steps, flagged irregularities, and reviewable site/decision improvement proposals. |
| T-06 | GitHub Pages Dashboard Site, Subpages, Line-by-Line Audit & Flagged Review Page | `unclaimed` | — | — | `index.html`, `hotels.html`, `restaurants.html`, `activities.html`, `questions.html`, `suggestions.html`, `flagged.html`, `assets/styles.css`, `assets/app.js` | Mobile-friendly clean dashboard + subpages, search/filter tables, all official & social links verified, zero broken links. |

---

## Session Log

- **2026-11-25 — Session `2065a787` (`arena/2065a787-nyfun3`):**
  - Audited repository at commit `c251442d122a8d04aade3d8b5a0d57fd4e9ce37c`. Found single file `README.md` (`# NYFun3`, 8 bytes) and legacy GitHub Pages configured on `main` (`/`).
  - Created `COORDINATION.md` and claimed `T-01` to establish baseline and coordination tracking.
