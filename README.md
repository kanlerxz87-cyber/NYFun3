# NYFun3 — New York 2027 trip dossier

A static, responsive GitHub Pages site for researching a New York City trip for two adults. It organizes a date-aware itinerary, hotel comparisons, MICHELIN dining, attractions, and an evidence/open-questions log.

## Browse the site

- [`index.html`](index.html) — overview and key planning decisions
- [`pages/itinerary.html`](pages/itinerary.html) — Feb 15–18 three-night mini-plan, Feb 15–22 seven-night core, and optional second week
- [`pages/hotels.html`](pages/hotels.html) — official room-fit evidence and clearly labeled third-party price snapshots
- [`pages/dining.html`](pages/dining.html) — year-stamped MICHELIN status, official hours/menu arithmetic, and creator review leads
- [`pages/experiences.html`](pages/experiences.html) — attraction hours, admission sources, and review videos
- [`pages/findings.html`](pages/findings.html) — unresolved questions, method, and data-quality caveats
- [`RESEARCH.md`](RESEARCH.md) — source inventory and research details

## Preview locally

No build step, package install, or JavaScript framework is required. From the repository root:

```bash
python3 -m http.server 4173 --bind 0.0.0.0
```

Then open <http://localhost:4173>. The JavaScript is an optional progressive enhancement for filtering hotel rows and restaurant cards; all core content remains available without it.

## Evidence and date caveats

- Research snapshot: **November 25, 2026**.
- Feb 15–18, 2027 is three nights and conflicts with the separate one-week minimum. The site keeps that conflict visible; Feb 15–22 is a separate seven-night comparison window.
- The trip duration is also described as both 1–2 weeks and up to 2–4 weeks. The itinerary shows a seven-night core and an optional second week, not an assumed four-week stay.
- Official exact-date hotel totals were not verified. Numeric room rates are dated Booking.com snapshots, not official quotes or guaranteed all-in totals. Taxes, city tax, resort-fee inclusion, cancellation terms, and breakfast must be checked at checkout.
- The latest awarded NYC MICHELIN list found for this snapshot is 2025; the 2026 ceremony is scheduled after the research date. All award claims are labeled by year.
- MTA route minutes, 2027 holiday schedules, and some attraction/menu prices remain unverified and are explicitly flagged rather than guessed.

The project is configured for GitHub Pages from the repository root on `main`. Changes on an Arena working branch will publish after they are merged into that configured source branch.
