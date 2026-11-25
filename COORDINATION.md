# COORDINATION — NYFun3 Trip Planning Site

Shared task board. Read this before starting work.

- **Repo:** `kanlerxz87-cyber/NYFun3`
- **Live site:** https://kanlerxz87-cyber.github.io/NYFun3/ (GitHub Pages, source = `main` branch, `/` root)
- **Board last updated:** 2026-11-25 (session `arena-c2e08f03`)

## Rules in force

1. Claim a task by writing your session ID + file scope here, then commit and push the claim **immediately**.
2. Never start a task another session has claimed.
3. Keep scopes non-overlapping. Each session edits only the files in its claimed scope.
4. Need a change in someone else's file? Log a request below; do not edit it.
5. Small, frequent commits. `git pull --rebase` before every push.
6. Shared outputs (`data/*.json` combined tables, `index.html` nav, Pages publish) are changed only by the final integration session.
7. Verification standard: every published value needs an official source link. Unconfirmed values are left blank and flagged. Never infer or fill in values.
8. Claims older than 60 minutes with no commits may be taken over; note the handoff.

## Branch-naming irregularity (logged for review)

The repo guide asks for branches named `session-<id>/<task>`. This session is pinned by the
Arena harness to `arena/c2e08f03-nyfun3` and is not permitted to create or switch branches.
Resolution: all work stays on `arena/c2e08f03-nyfun3`; the claim records the pinned branch name.
At integration time, merge `arena/c2e08f03-nyfun3` into `main`.

## Task board

| ID | Task | Status | Owner (session) | Branch | File scope | Touches |
|----|------|--------|-----------------|--------|-----------|---------|
| T1 | Repo review + irregularity log | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `REVIEW.md`, `review.html` | — |
| T2 | Michelin dataset (official list, stars, links) | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `data/michelin.json`, `restaurants.html` | — |
| T3 | Hotel pricing (real 7-night totals, dates, amenities) | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `data/hotels.json`, `hotels.html` | — |
| T4 | Activities dataset + social links | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `data/activities.json`, `activities.html` | — |
| T5 | Site shell, nav, CSS, executive summary | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `index.html`, `assets/` | — |
| T6 | Itinerary (7-night + extended variants) | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `itinerary.html`, `data/itinerary.json` | — |
| T7 | Open questions + missing-information plan | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `questions.html` | — |
| T8 | Suggestions / decision section | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `suggestions.html` | — |
| T9 | Verification log (line-by-line) | done | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `VERIFICATION.md`, `verification.html` | — |
| T10 | Integration: merge to `main`, re-verify, publish Pages | needs review | arena-c2e08f03 | arena/c2e08f03-nyfun3 | `main` publish | — |

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
