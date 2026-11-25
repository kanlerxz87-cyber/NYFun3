# NYC Trip Planner — February/March 2027

A static, mobile-first planning dashboard for a two-adult New York City trip in the window
**15 Feb – 23 Mar 2027** (preferred start 15–18 Feb 2027).

**Live site:** https://kanlerxz87-cyber.github.io/NYFun3/

No build step, no dependencies, no framework. Plain HTML, one stylesheet, one small JS file,
and JSON data files loaded at runtime.

## Pages

| Page | What it holds |
|---|---|
| `index.html` | Dashboard: what exists, how to read the tables, known limitations. |
| `activities.html` | 15 museums, parks, landmarks and passes — weekday hours, exceptions, adult prices, review searches. |
| `restaurants.html` | Starred restaurant shortlist, filterable by area and tier. |
| `michelin.html` | All 72 starred entries (5 ★★★ / 15 ★★ / 52 ★), cluster counts, star status stated per row. |
| `hotels.html` | 9 hotels with 7-night totals for 15–22 Feb 2027, checked against private-bathroom and queen-bed requirements. |
| `itinerary.html` | 7-day plan sequenced around published closures. |
| `plan.html` | Executive summary, 9 reviewable suggestions, 11 open questions, irregularities found. |

Supporting documents: `REVIEW.md` (repo review, irregularities R1–R20) and
`VERIFICATION.md` (what was checked, against which page, and when).

## The rule this repo is built on

> Every published value must be traceable to the operator's own official page.
> If it can't be confirmed there, the cell is left blank and flagged — never inferred,
> never filled from a third-party aggregator, never estimated.

That is why several columns are visibly empty: MICHELIN publishes a price *band*, not a
price; restaurant sites are often JavaScript apps that return no menu data; and no official
source publishes subway times per hotel/restaurant pair. Each of those gaps is flagged
inline and listed as an open question rather than papered over with a plausible number.

## Data files

| File | Contents |
|---|---|
| `data/activities.json` | 15 activities, each with `source_url`. |
| `data/hotels.json` | 9 hotels, each with the exact quote URL (check-in, check-out, 2 adults). |
| `data/michelin.json` | 5 three-star + 7 two-star, full detail. |
| `data/michelin_two_star.json` | All 15 two-star records. |
| `data/michelin_one_star.json` | All 52 one-star records. |
| `data/michelin_all.json` | Merged, de-duplicated source used by the site (72 rows). |
| `data/itinerary.json` | 7-day plan, derived only from verified activity hours. |

## Preview locally

```sh
python3 -m http.server 8000
# then open http://localhost:8000/
```

Opening `index.html` directly from disk will not work: browsers block `fetch()` of local JSON
over `file://`. Any static server is fine.

## Verification status (25 November 2026)

- **Stars:** the MICHELIN 2025 selection (announced 18 Nov 2025) is current **as of this
  snapshot only**. The next New York ceremony is **14 Dec 2026** — before the trip. Re-check
  every star after that date.
- **Hotel prices:** live Booking.com rate cards, captured with their URLs. These move daily.
- **Known gaps:** 48 of 52 one-star rows lack verified hours; 52 of 72 rows lack a verified
  neighbourhood; no per-couple restaurant price has been verified; no Michelin "within 1 hour"
  hotel count has been computed. All four are flagged on the site and listed in
  `plan.html` §4.

## Contributing / parallel sessions

Read `COORDINATION.md` first. It holds the task board, the claim protocol and the file-scope
rules. Shared outputs (the combined data files, `index.html` nav, and the `main` publish) are
changed only by the integration session.
