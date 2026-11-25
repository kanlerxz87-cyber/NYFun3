# Verification and link-check report (2026-11-25)

This is the final integration verification pass for branch `arena/99553b53-nyfun3`.
It describes checks actually performed, not assumptions.

## 1. Line-by-line data checks

`python3 scripts/verify_site.py` parses every generated HTML file:

- All 10 pages exist and contain `<main id="main">`, `<title>` and a viewport meta tag.
- All internal links resolve to an existing file (no broken navigation or asset links).
- Every factual table row in the Michelin, hotel, activities and flagged-review tables contains at least one external source link. The `sources.html` table is itself the source index and is exempted from this rule.
- Every Michelin record has the required keys, an official `guide.michelin.com` URL, https social links, a blank official `priceFor2` and non-empty hours.
- Every hotel has an official https source and blank (unverified) dated price fields.
- Every activity has an official https source and a blank (unverified) travel-time field.

Result at final run: **0 hard problems, 0 warnings**.

## 2. Source and link checks

- All 81 unique external URLs rendered by the site were extracted and checked programmatically. The sandbox outbound proxy closes TLS connections for direct `curl`/`urllib` requests to external hosts (error 35 / EOF), so HTTP status codes could **not** be verified in this environment. No URL was silently marked valid on the basis of that failed check.
- Instead, representative official pages were re-opened with the browser-style page fetcher during this session:
  - MICHELIN NYC 1-star list, page 1 (chunks 0–7) and page 2 — returned the published counts (5/14/50/76/224), the complete list of 48 + 2 names, and restaurant detail links.
  - NYC 3-star and 2-star lists and all 19 detail pages were opened earlier in the session when the data files were built.
  - Hotel, activity and social links were opened with the same tool when their rows were created; blocked or unavailable pages are listed on the Flagged for Review page.
- The site itself was built from the committed JSON files by `scripts/build_site.py`; no table value was hand-copied into HTML except the static narrative pages, whose claims link to official sources inline.
- Local preview check: `python3 -m http.server` served `index.html` and all subpages; paths were also checked by the script above.

## 3. Corrections made during verification

1. `scripts/build_site.py` initially produced a relative-path error: the Overview nav link on subpages pointed at `index.html` inside `pages/`. Fixed to `../index.html`; static link checker passed afterwards.
2. One missing closing parenthesis in `activities_table()` prevented the build; fixed before generation.
3. all 50 one-star restaurant names were completed from official page 2, replacing the earlier partial 33-name capture. The Flagged for Review item was updated to `resolved`.
4. The sources table is a source index rather than a factual data table; the checker now exempts it from the "every row has an external source link" rule while still checking its internal links.

## 4. Irregularities that remain open

See `pages/flagged-for-review.html` for the full list. The material ones are:

- No official dated February 2027 hotel rate, so seven-night totals and cheapest booking date are blank.
- No official subway/bus itinerary, so the ≤1-hour constraint is not claimed as verified.
- Broadway/Times Square hours and cost were unavailable from an official page; blank.
- Met hours differ between indexed official versions; Hilton direct fetch was blocked; TikTok links could not be verified.
- Official prices for two are not published for the starred restaurants; reviewer prices are stored separately and labelled third-party.

## 5. Publish checklist

- [x] Data files committed and sourced
- [x] Site generated from data files
- [x] Internal + source-link static verification passes
- [x] Flagged items published on their own page
- [x] Coordination board updated
- [ ] GitHub Pages enabled on the branch (see `COORDINATION.md` T06/T08 and repository settings)
