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

## Session log — arena-c796d983 (2026-11-25, UTC)

### Completed (T1–T7) — all claims kept, no other sessions detected
- **T1 Repo review**: skeleton repo (1-line README), commit c251442, branch arena/c796d983-nyfun3. No other files, no CI, no data. No secrets. Irregularities: README context-free; no license; no build/publish automation (decided: Pages legacy source = main, no workflow).
- **T2 Michelin research**: verified against official Guide pages (fetched 2026-11-25): Le Bernardin 3★ (155 W 51st; hours Mon–Fri 12–14:30/17–22:30 Fri→23:00, Sat dinner only, Sun closed) · Per Se 3★ (10 Columbus Circle; daily 16:30–21:00) · Eleven Madison Park 3★ (11 Madison Ave; $$$$; hours not rendered in fetched chunk → Flag #J2) · Jungsik NY 3★ (2 Harrison St; hours not rendered → Flag #J1) · Masa 2★ (10 Columbus Circle St 401; Tue–Sat 12–14:30 & 17:30–22; Sun/Mon closed — conflicts with 2026 media listing 3★ → Flag #R2) · Jean-Georges 2★ (1 Central Park West; Tue–Sat 12–2 & 17–21:30; Sun/Mon closed) · The Modern 2★ (9 W 53rd; daily lunch 12–14:30; dinner 17–21 Fri/Sat→21:30). Selection counts verified on official selection page: 5×★★★ / 14×★★ / 50×★ / 76 Bib Gourmand. Sushi Sho NY (3 E 41st) reported 3★ by 4 independent 2026 sources; NYC Guide slug unresolvable → Flag #R3. One-star examples (Gramercy Tavern, Cote, Semma, Jeju Noodle Bar) = secondary-sourced, flagged. Dinner-for-2 estimates from 2026 press (EMP ≈$770/pp×2? no: $385pp×2=$770; Per Se $850; Le Bernardin $700/lunch $436; Jungsik $670; Sushi Sho ≈$990 incl 10% admin; Atomix $770; Aska $750; Aquavit $160–190 lunch; Jeju ≈$50–120) — all unverified for Feb 2027, marked as such.
- **T3 Hotels**: 8 shortlisted; reported-rate snapshots only (no Feb-2027 public quotes exist): citizenM NY Times Square from $151 typical $219–310 (7N ≈$1,533–2,170) · Arlo Nomad $152–378 (7N ≈$1,064–2,646) · Mandarin Oriental $948–2,394+fees (7N ≈$6,636–16,758+) · Gramercy Park Hotel from $99 teaser (7N ≈$700–1,500, Flag #H4) · Hyatt Grand Central $519+ (7N ≈$3,633+) · Trump Intl/Essex House/Peninsula = blank, unverified. All have advertised private baths; Gramercy Park Hotel unconfirmed → flagged. All reach the 19 starred restaurants ≤1h subway/walk; density tie broken by walk-time and price (see Analysis page). Cheapest booking: March floor (KAYAK ≈$99) vs Oct peak (≈$780); book refundable now + re-check at T−90/60/30/14.
- **T4 Activities**: NPS Statue of Liberty hours verified (daily 9:00–16:30; ferry only; last entry 15:30; closed Thanksgiving & Christmas; page updated Apr 2026). MoMA verified (Mon–Sun 10:30–17:30, Fri→20:30; closed Thanksgiving & Christmas; $30). Met: price verified ($30) but hours unverified (official page renders none; sources conflict) → Flag #A3. Top of the Rock (8:00 vs 9:00 open; $42–60 dynamic) → #A4. 12 more attractions flagged individually (#A5–#A16). Broadway/TKTS, Summit, Edge = link-only. Social links = platform search URLs, handles unverified → Flag #S1.
- **T5 Itinerary/Exec summary**: 3-night (Feb 15–18), 7-night (Feb 15–22), 2/3/4-week variants. Feb 15 2027 = Monday = Presidents Day (crowd warning). Met closed Wed → MoMA/Statue on Wed. Budget bands value/comfort/luxury. Booking order: refundable hotel now → watch Dec-2026 ceremony → Jan-2027 reservations (Resy/Tock) → 48h checks.
- **T6 Site**: static HTML/CSS/JS, mobile-friendly (responsive nav + table scroll), 12 pages, internal links validated by script (all OK), print CSS included. Live preview on port 8080.
- **T7 Verification**: every row carries official link or flag; ≈50 items on Flagged page w/ official manual-check links; unverifiable = blank + flag (never guessed).

### T8 Publish — BLOCKED (needs repo admin)
- GitHub Pages currently serves **main** (root). `gh api PUT .../pages` → 403 "Resource not accessible by integration". Session rules forbid pushing to main.
- Resolution: **PR #1 opened** (arena/c796d983-nyfun3 → main): https://github.com/kanlerxz87-cyber/NYFun3/pull/1 . Merging it publishes https://kanlerxz87-cyber.github.io/NYFun3/ . Until merge, Pages still serves main (one-line README).
- Until merge, the site is previewable at the sandbox preview URL for port 8080.

### Irregularities flagged for review (headline)
R1 ceremony mid-Dec-2026 (reported) · R2 Masa 2★ vs media 3★ · R3 Sushi Sho NY official listing unresolvable · R4–R14 restaurant prices/addresses secondary · J1/J2 hours not rendered · H1–H8 hotel Feb-2027 quotes nonexistent · A1/A3–A16 activity hours/prices unverified · S1 social handles unverified · REPO1 repo was 1-line README (fixed) · P1 Presidents Day premium unverified.

### Next actions
1. Owner merges PR #1 → Pages live. 2. On 2026-12-16 re-diff Michelin stars; update site. 3. Traveler answers Q1–Q6,Q10,Q11,Q16 → lock Path A/B/C → book refundable rates + reservations. 4. Re-check flags at T−90/60/30/14.
