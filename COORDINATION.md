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
| T-02 | Michelin Guide NYC Restaurants & Cluster Verification + Social Reviews | `in progress` | `2065a787` | `arena/2065a787-nyfun3` | `data/restaurants.json` | Verifying official Michelin status (Stars / Bib Gourmand / Selected), official sites, hours/days/exceptions, 2-adult total cost, and YouTube/TikTok/Instagram review URLs. |
| T-03 | NYC Activities Verification, Hours, Pricing & Social Reviews | `unclaimed` | — | — | `data/activities.json` | Verify official site, open days/hours/exceptions for Feb–Mar 2027, 2-adult cost, transit hubs, and YouTube/TikTok/Instagram review URLs. |
| T-04 | Hotel Selection, 7-Night Real Pricing (Feb 15–Mar 23, 2027), Booking Window & <=1h Transit / Michelin Ranking | `unclaimed` | — | — | `data/hotels.json` | Verify Queen/King bed + private bath for 2 adults, real 7-night total pricing on actual dates, cheapest window, Michelin count within <=60 min MTA subway/bus, and activity <=60 min transit matrix. |
| T-05 | Decision Questions, Missing Information & Site Improvement Suggestions | `unclaimed` | — | — | `data/analysis.json` | Compile known vs. missing info, pre-booking questions, discovery methods, and reviewable site improvement options. |
| T-06 | GitHub Pages Dashboard Site, Subpages, Line-by-Line Audit & Flagged Review Page | `unclaimed` | — | — | `index.html`, `hotels.html`, `restaurants.html`, `activities.html`, `questions.html`, `suggestions.html`, `flagged.html`, `assets/styles.css`, `assets/app.js` | Mobile-friendly clean dashboard + subpages, search/filter tables, all official & social links verified, zero broken links. |

---

## Session Log

- **2026-11-25 — Session `2065a787` (`arena/2065a787-nyfun3`):**
  - Audited repository at commit `c251442d122a8d04aade3d8b5a0d57fd4e9ce37c`. Found single file `README.md` (`# NYFun3`, 8 bytes) and legacy GitHub Pages configured on `main` (`/`).
  - Created `COORDINATION.md` and claimed `T-01` to establish baseline and coordination tracking.
