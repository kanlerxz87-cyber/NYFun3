# Repository review

Checked 2026-11-25. Baseline commit `c251442d122a8d04aade3d8b5a0d57fd4e9ce37c`. Full review page: [`docs/review.html`](docs/review.html).

| Item | Verified | Irregularity | Source |
| --- | --- | --- | --- |
| README.md | Yes — fetched from the repository at c251442; contains only the single line '# NYFun3'. | The repository had no site, no data files, no COORDINATION.md and no CI/GitHub Pages configuration at the start of this session. | local git show c251442:README.md |
| COORDINATION.md | Yes — created in this session; imported the existing board from origin/arena/7386fd81-nyfun3. | The existing claim on the other session branch covers COORDINATION.md, README.md, index.html, assets/, pages/ and .github/workflows/. This session therefore keeps its entire deliverable in docs/, data/ and tools/. | git show FETCH_HEAD:COORDINATION.md (origin/arena/7386fd81-nyfun3) |
| Branch model | Yes — git branch / git ls-remote origin. | Arena fixes this session to arena/8781ea5a-nyfun3 and forbids creating or pushing other branches; the requested session-<id>/<task> branch convention cannot be used. Logged in COORDINATION.md. | local git status / git ls-remote origin |
| Existing verification | Yes — no data tables, no sources, no tests existed to review line by line. | All verification in this session is new work against official external sources; no prior claims were carried over. | git ls-tree -r c251442 |
| origin/arena/7386fd81-nyfun3 root site | Yes — git fetch / git ls-tree / git show FETCH_HEAD:COORDINATION.md on 2026-11-25. | That branch now contains index.html, assets/style.css and pages/*.html and marks its task 'needs review'. It reports no comparable hotel prices or routes and a Met Thursday source conflict. This session does not edit those files; the final integration request is logged in COORDINATION.md. | git show FETCH_HEAD:COORDINATION.md (origin/arena/7386fd81-nyfun3) |

## Flagged for review

| ID | Severity | Title | Detail |
| --- | --- | --- | --- |
| F01 | medium | Four of six hotel 7-night totals remain unverified | Real dated official 7-night quotes were captured for Pod 51 and Arlo NoMad. 11 Howard, citizenM New York Times Square, AC Hotel New York Times Square and The Westin New York at Times Square still have blank totals; no estimate was substituted. Arlo's displayed total also excludes taxes. |
| F02 | high | Cheapest official booking window falls outside the trip window | NYC Hotel Week 2027 discount applies 2 Jan–11 Feb 2027. The requested window starts 15 Feb 2027. The verified discount cannot be used for the requested dates. |
| F03 | high | Michelin-density hotel ranking blocked | The ≤1-hour subway/bus criterion needs dated MTA Trip Planner results. No static official value exists, so counts and ranking are blank rather than inferred. |
| F04 | medium | 2025 star roster vs current official count mismatch | The official 2025 ceremony article lists 5 three-star, 15 two-star and 52 one-star restaurants (72 names, including Westchester, Brooklyn and Queens entries). The current official all-starred listing shows 69 starred (5/14/50). Per-name current status was verified only for 13 restaurants; the remaining names are flagged unverified. |
| F05 | medium | Reported December 2026 MICHELIN ceremony is not an official source | A third-party page reports the next New York star announcement for 14 Dec 2026. No official MICHELIN announcement was fetched, so this is logged as a question, not a fact. |
| F06 | medium | 11 Howard room-count conflict | Official hotel website: 207 guest rooms and suites. MICHELIN Guide hotel page: 213 rooms. Both are cited; neither was corrected. |
| F07 | medium | Empire State Building February 2027 hours not published | The official hours page states it is open 365 days and lists near-term Nov–Dec 2026 hours only; no February 2027 hours are published. Hours cell is blank. |
| F08 | low | Instagram review coverage incomplete; MoMA placeholder removed | Instagram site-restricted searches returned official accounts/location pages rather than third-party reviews. Such links are labeled 'official account' and are not presented as reviews. An unrelated Statue of Liberty Instagram location placeholder accidentally attached to MoMA was removed; no verified Instagram review link for MoMA remains. |
| F09 | low | Central Park hours not published on official page | NYC Parks Central Park page lists location, facilities and ZIP codes but no opening hours. Days/hours left blank. |
| F10 | low | Some official pages could not be fetched directly | Hilton, Hyatt and Arlo booking/rooms pages redirected to generic booking shells or failed to return content. Those hotels were kept only where an official NYC Tourism listing or another official page supplied verified facts; all unverified fields are blank. |
| F11 | low | Trip starts on a U.S. federal holiday | Monday 15 February 2027 is Washington's Birthday (OPM). Impact on rates, crowds and venue hours is not verified. |
| F12 | low | Parallel-session scope separation | Another session owns the repository-root site and .github/workflows/. This session's site is self-contained in docs/. Arena fixes the branch name, so the requested session-<id>/<task> branches could not be created; branch isolation plus file-scope claims are used instead. |
| F13 | medium | Arlo Cyber Sale stay-date end conflict | Official Arlo Cyber Exclusive Access page: 40% off, sale ends 3 Dec 2026, NYC stay dates through 31 Oct 2027. Official Arlo booking page rate description: 'Book by December 3 ... stay dates through December 2027'. Both cited; neither corrected. |
| F14 | medium | Hotel 7-night totals are not like-for-like | Pod 51 Queen Pod $1,109 states 'Including taxes and fees'. Arlo NoMad Queen $1,296 states 'Including the urban fee, excluding taxes'. No official Arlo tax amount was published on the fetched page, so the final Arlo total and the true cheapest hotel cannot be confirmed. |
| F15 | low | No market-wide cheapest booking time is officially verified | Arlo 40% off (book by 3 Dec 2026) and Marriott 15%/25% off (book by Tuesday 1 Dec) are the highest verified in-window discounts among the offers checked. No official source compares all NYC hotels or publishes a single best time to book; the claim is qualified, not presented as market-wide proof. |
| F16 | low | Pod 51 facility fee not itemized in booking total | Official FAQ lists a $29.84 incl-tax facility fee per room per night. The 7-night booking page says totals include taxes and fees but does not itemize that facility fee; no amount was added or subtracted manually. |

See [`docs/flagged.html`](docs/flagged.html) for official source links and the complete blank-value inventory.
