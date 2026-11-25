# COORDINATION.md — Shared Task Board

Project: NYC Trip Planning (branch `arena/c796d983-nyfun3`)
Rules: claim a task by writing your session ID + file scope here, commit & push the claim BEFORE starting work.
`needs review` = published on the Flagged for Review page; does not block other tasks.
If a session crashes or its claim is >60 min old with no commits, another session may take over and note the handoff here.
Last updated: 2026-11-25 (UTC)

## Repo Review (initial)
- Repo contains only `README.md` ("# NYFun3") + `.git`. No site, no data, no CI. Initialized fresh.
- Irregularities: none beyond emptiness. No existing content to migrate or conflict with.

## Task Board

| Task | Status | Owner (session) | Files / scope | Notes |
|------|--------|-----------------|---------------|-------|
| T1 — Repo review & irregularity flags | done | arena-c796d983 | repo root review | Repo is a near-empty skeleton; nothing else present. Logged below. |
| T2 — Michelin restaurant research (stars, addresses, hours, prices, socials, sources) | in progress | arena-c796d983 | data/restaurants.*, research notes | Sources: Michelin Guide articles, official restaurant sites, happy-hour.nyc (Nov 2026 check) cross-referenced. Every row must carry a source link or be flagged unverified. |
| T3 — Hotel research (price, location, amenities, 7-night totals, Michelin proximity ranking) | in progress | arena-c796d983 | data/hotels.* | Feb 15–22 2027 7-night window; preferred short trip Feb 15–18 2027. Real verified pricing only; otherwise blank + flagged. |
| T4 — Activities research (hours, days open, socials, ticket info, sources) | in progress | arena-c796d983 | data/activities.* | YouTube / TikTok / Instagram links per activity where verifiable. |
| T5 — Itinerary + Executive summary (Feb 15–18 2027 pref.; 7-night base; up to 2–4 wk option) | in progress | arena-c796d983 | data/itinerary.md, site exec summary | Built from T2–T4 after they land. |
| T6 — Site creation (landing dashboard + subpages, mobile-friendly) | in progress | arena-c796d983 | index.html, assets/, pages/*.html | Plain static HTML/CSS/JS, GitHub Pages compatible. |
| T7 — Verification pass + Flagged for Review page + Suggestions page + Q&A gaps page | in progress | arena-c796d983 | verify script/notes, flagged page | Every row source-linked; unverifiable values left blank & flagged. |
| T8 — Publish GitHub Pages + final integration check | in progress | arena-c796d983 | .github/workflows or Pages settings | Enable Pages from this branch via gh api; confirm site serves. |

## Log

- 2026-11-25 — arena-c796d983: Initialized board. Repo reviewed: skeleton only (README.md one line). Claimed T1–T8 (single-session run). No other sessions present at claim time. Will push this claim first, then research, then build site, then verify, then publish.
