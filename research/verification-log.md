# Verification log

Last updated: 2026-11-25 UTC

## Protocol

1. Discover an official URL with a web search or an official site link.
2. Open the official URL directly. Record the status, access date, and source ID.
3. Read only the value shown on that official page. Do not infer a missing value.
4. If a value is absent, publish an empty cell with `unverified` and a Flagged for Review entry.
5. For prices, record dates, occupancy, room/rate name, currency, tax wording, and access timestamp.
6. For arithmetic totals (for example, two tasting menus), show the official per-person price, the formula, and a `calculated` label.
7. For transit, use official MTA GTFS schedule data and record the feed URL, calendar range, and the fact that it is not a 2027 service guarantee.
8. For every published table row, include at least one clickable official source link.
9. Before publishing, run a link checker and a data-shape checker. Fail the build on missing source URLs or broken internal links.

## Line-by-line checks performed

| Check | Source / command | Result | Status |
|---|---|---|---|
| Repository contained only `README.md` | `find`, `git show --stat HEAD`, `git log` | Initial commit `c251442` had one file | Verified |
| Current branch and base | `git status --short --branch`, branch note | `arena/ed92e764-nyfun3`, base `c251442` | Verified |
| GitHub authentication and admin permission | `gh auth status`, `gh repo view` | Authenticated as repository admin | Verified |
| Existing Pages configuration | `gh api repos/kanlerxz87-cyber/NYFun3/pages` | `https://kanlerxz87-cyber.github.io/NYFun3/`, `build_type=legacy`, source `main` | Verified |
| MICHELIN Guide NYC directory reachable | `fetch_page` of official directory | Page opened; 369 restaurants; 5 three-star, 14 two-star, 50 one-star, 76 Bib Gourmand, 224 Selected | Verified as 2026-11-25 snapshot |
| MICHELIN Guide all-starred directory reachable | `fetch_page` of official all-starred page | Page opened; 69 starred restaurants, two pages | Verified as 2026-11-25 snapshot |
| MTA official site reachable | `fetch_page` of https://www.mta.info/ | Page opened | Verified |
| MTA official apps describe subway/bus trip planning | `fetch_page` of https://www.mta.info/guides/apps | Page opened | Verified |
| MTA developer static GTFS feed list | `fetch_page` of https://www.mta.info/developers | Official subway and six borough bus feed URLs listed | Verified |
| MTA schedule-transition limitation | `fetch_page` of https://www.mta.info/developers/gtfs-schedules-transition | Official page says current feeds are replaced about a week before a schedule change | Verified |
| Official Hyatt hotel pages reachable | `fetch_page` of dated shop pages | Pages opened; dates and 2 guests were displayed | Verified |
| Dynamic Hyatt price fields visible to the page fetcher | `fetch_page` of dated shop pages | Price cards were not exposed in extracted markdown | `unverified`; research collector needed |
| Hilton dated room page | `fetch_page` of official reservation URL | Official site returned an error page through the fetcher | `unverified`; no price recorded |
| Marriott dated search page | `fetch_page` of official search URL | Search results remained loading; no rate captured | `unverified`; no price recorded |
| IHG dated rooms page | `fetch_page` of official rooms URL | Room details loaded; no dated price captured | `unverified`; no price recorded |
| Old MTA Trip Planner widget | `fetch_page` of http://tripplanner.mta.info/widget/ | Direct fetch failed | Flagged for review; use official MTA app/GTFS instead |

## Irregularities flagged for review

1. The user's parallel-session instruction asks for `session-<id>/<task>` branches, but the Arena session policy fixes this session to `arena/ed92e764-nyfun3` and prohibits other branches. Mitigation: non-overlapping file scopes on the shared task board.
2. GitHub Pages was configured as legacy publishing from `main`; work is on the fixed branch. Final integration must switch Pages to GitHub Actions so the fixed branch publishes the site without pushing another branch.
3. MICHELIN Guide counts and star/status values are dynamic and can change before February 2027.
4. MTA GTFS static feeds are current schedules, not a guarantee for February–March 2027.
5. Hotel rates are dynamic and booking engines sometimes block non-browser fetchers. No price will be published unless the official dated page yields a rate and its tax wording.
6. Old `tripplanner.mta.info` links are HTTP and did not open directly; the current official MTA app and Developer Resources are used instead.
