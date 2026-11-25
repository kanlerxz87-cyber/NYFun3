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
| `T1` | Repo Baseline Audit & Prompt Irregularity Analysis | `in progress` | `fc94e0d3` | `2026-11-25T22:34:00Z` | `data/repo_audit.json` |
| `T2` | MICHELIN Guide & Starred Restaurants, Clusters, Couple Pricing, Hours & Social Reviews | `unclaimed` | — | — | `data/michelin_restaurants.json` |
| `T3` | NYC Activities, Hours, Exceptions, <=1-Hr Transit & Social Reviews | `unclaimed` | — | — | `data/activities.json` |
| `T4` | NYC Hotels (Private Bath, Queen+ Bed, Verified 7-Night Pricing Feb–Mar 2027, Best Time to Book & Michelin Transit Ranking) | `unclaimed` | — | — | `data/hotels.json` |
| `T5` | Decision Readiness (Questions & Missing Info Discovery) + Site Improvement Suggestions | `unclaimed` | — | — | `data/decision_and_suggestions.json` |
| `T6` | Final Integration, Line-by-Line Re-Verification, Dashboard Site & Subpages, Link Check & Live Preview | `unclaimed` | — | — | `index.html`, `hotels.html`, `michelin.html`, `activities.html`, `questions.html`, `suggestions.html`, `review.html`, `assets/`, `.nojekyll`, `README.md` |

---

## Coordination & Verification Log

### 2026-11-25T22:34:00Z — Session `fc94e0d3` initialized board & claimed `T1`
- Checked repository state: `COORDINATION.md` did not exist on `main` (`c251442d122a8d04aade3d8b5a0d57fd4e9ce37c`).
- Created `COORDINATION.md` and claimed `T1` (`data/repo_audit.json`).
