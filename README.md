# NYFun3 — NYC Couple's Vacation Analysis & Verified Dashboard (Feb 15 – Mar 23, 2027)

Clean, mobile-friendly static reference dashboard planning and analyzing a **New York City vacation for two adults** between **February 15, 2027 and March 23, 2027**.

## Pages Published (GitHub Pages Ready)

- **[`index.html`](./index.html)** — Executive Summary, Optimal 2027 Travel Window Matrix (`Feb 21–28, 2027` sweet spot vs. `Feb 15–22` & `Mar 8–16`), 7-Night Couple Total Cost Rollup, and Top 3 Hotels preview.
- **[`hotels.html`](./hotels.html)** — 8 NYC hotels verified for **Private Bathroom + Queen/King Bed**, standardized to a **7-night stay** (itemizing NYC 14.75% + $3.50/night tax and mandatory destination fees), and ranked strictly by **MICHELIN restaurants reachable within <=60 minutes by MTA subway/bus**.
- **[`michelin.html`](./michelin.html)** — Citywide 6-Cluster Census (**70 active NYC Starred + 84 Bib Gourmand**) and **26 line-by-line verified MICHELIN Guide restaurants** distinguishing **3★ / 2★ / 1★ Starred** from **Guide-Listed Only (Bib Gourmand & Selected)**, with 2-adult total prices, hours, exceptions, official links, and YouTube/TikTok/Instagram reviews.
- **[`activities.html`](./activities.html)** — **16 winter-smart NYC couple activities** with verified 2-adult admission totals, hours, critical 2027 closures (*Met Opera dark Jan 31–Mar 7, 2027; Wollman Rink closes Mar 16, 2027*), <=60-minute transit checks, and social media reviews.
- **[`questions.html`](./questions.html)** — Confirmed Knowns vs. Missing Information, 6 pre-booking Decision Questions, and actionable discovery steps.
- **[`suggestions.html`](./suggestions.html)** — 6 staged, reviewable suggestions to improve couple decision-making and dashboard capabilities prior to making changes.
- **[`review.html`](./review.html)** — Master audit log of **14 Flagged Irregularities & Unverified Blank Fields** (`IRREG-01` through `IRREG-14`).

## Verification & Coordination Artifacts

- [`COORDINATION.md`](./COORDINATION.md) — Task board (`T1`–`T6`), owning session log, and irregularity notes.
- [`data/`](./data/) — Structured primary-source JSON datasets (`repo_audit.json`, `hotels.json`, `michelin_restaurants.json`, `activities.json`, `decision_and_suggestions.json`).
- [`scripts/build_site.py`](./scripts/build_site.py) & [`scripts/verify_site.py`](./scripts/verify_site.py) — Deterministic static HTML builder and automated zero-hallucination / link / constraint verifier.
