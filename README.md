# NYC Trip Planner — February/March 2027

A static, mobile-first planning dashboard for a two-adult New York City trip in the window
**15 Feb – 23 Mar 2027** (preferred start 15–18 Feb 2027).

**Live site:** https://kanlerxz87-cyber.github.io/NYFun3/

No build step, dependencies, or framework. The primary dashboard is plain HTML with JSON data loaded at runtime; the supplemental dossier has a separate stylesheet and small progressive-enhancement script.

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
| `pages/index.html` | Supplemental curated dossier: itinerary, hotel snapshots, dining/menu arithmetic, attraction hours, and research notes. |

Supporting documents: `REVIEW.md` (repo review, irregularities R1–R20),
`VERIFICATION.md` (what was checked, against which page, and when), and `RESEARCH.md`
(the supplemental dossier source/method log). The nested `pages/` dossier complements the
data-driven root site; it does not replace the existing JSON datasets or star/activity tables.
The root `.nojekyll` file keeps the linked Markdown research log available to GitHub Pages as-is.

## The rule this repo is built on

> Official venue, hotel-room, museum, award, and transit facts need a linked primary source.
> Unknown official facts remain blank and flagged — never inferred or estimated.

For live hotel availability, the dashboard can show date-specific Booking.com observations;
those are explicitly marked as **third-party snapshots**, linked to their query, and are not
represented as official hotel quotes or guaranteed all-in prices. The supplemental `pages/`
dossier also includes selected published restaurant-menu arithmetic and creator-review leads;
menu estimates are not final bills, and social links are not treated as factual authorities.

Several gaps remain visible: the primary MICHELIN table is not a complete per-couple menu-cost
catalogue, restaurant sites may not expose menu data, and no official source publishes subway
times per hotel/restaurant pair. Each gap is listed rather than papered over with a plausible
number.

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
python3 -m http.server 8000 --bind 0.0.0.0
# then open http://localhost:8000/
```

Opening `index.html` directly from disk will not work: browsers block `fetch()` of local JSON
over `file://`. Any static server is fine.

## Verification status (25 November 2026)

- **Stars:** the MICHELIN 2025 selection (announced 18 Nov 2025) is current **as of this
  snapshot only**. The next New York ceremony is **14 Dec 2026** — before the trip. Re-check
  every star after that date.
- **Hotel prices:** live Booking.com rate cards, captured with their URLs. These move daily.
- **Known gaps:** 43 of 52 one-star rows lack verified hours; 50 of 72 rows lack a verified
  neighbourhood; the primary 72-row MICHELIN dataset has no complete per-couple cost catalogue
  (the supplement contains menu arithmetic for eight selected candidates); no Michelin "within
  1 hour" hotel count has been computed. These gaps are flagged on the site and listed in
  `plan.html` §4 / `pages/findings.html`.

## Contributing / parallel sessions

Read `COORDINATION.md` first. It holds the task board, the claim protocol and the file-scope
rules. Shared outputs (the combined data files, `index.html` nav, and the `main` publish) are
changed only by the integration session.
