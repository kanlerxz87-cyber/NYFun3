# Coordination board

Shared task board for parallel sessions. Claim a task *before* starting it, commit and push the claim immediately, and keep file scopes non-overlapping.

Session ID for this checkout: `arena-8781ea5a` (branch `arena/8781ea5a-nyfun3`).

| Task | Status | Owner | File scope |
|---|---|---|---|
| Research, initial site and integration | needs review | arena-7386fd81 | COORDINATION.md, README.md, index.html, assets/, pages/, .github/workflows/ |
| Verified data corpus (Michelin, hotels, activities, social reviews), standalone dashboard published from `docs/`, executive summary, questions, suggestions, flagged-for-review | needs review | arena-8781ea5a | COORDINATION.md, docs/, data/, tools/, EXECUTIVE_SUMMARY.md, QUESTIONS.md, SUGGESTIONS.md, SOURCES.md, VERIFICATION.md, REVIEW.md |

## Scope separation notes
- `arena-7386fd81` owns the repository-root site (`index.html`, `assets/`, `pages/`) and `.github/workflows/`. This session does **not** edit those paths.
- The other session's fetched board at `origin/arena/7386fd81-nyfun3` commit `dd6cbd6` marks its root-site task **needs review**, reports no comparable hotel prices or routes and a Met Thursday source conflict, notes incomplete coverage on Flagged for Review, and makes no future-availability or comprehensive-ranking claim. That claim and wording are preserved here; no root `index.html`, `pages/`, `assets/`, or workflow file was created or modified by this session.
- This session's deliverable is self-contained under `docs/` (a GitHub Pages publishable directory), with machine-readable data in `data/`, deterministic generators in `tools/`, and root-level Markdown summaries. The `docs/.nojekyll` marker is included.
- Arena fixes each session to its own branch and forbids creating/switching/pushing other branches, so the `session-<id>/<task>` branch convention cannot be used. Branch isolation is used instead; the conflict-avoidance mechanism is the file scope table above.
- Request to the final integration session (logged, not executed here): reconcile `docs/` with the root site owned by `arena-7386fd81`, choose one navigation/index, re-verify combined tables line by line, and re-point GitHub Pages if needed.

## Sources
- `SOURCES.md` and `docs/sources.html` contain the complete official-source registry: 77 official / government / venue / hotel / platform source IDs, each with a direct URL, type and check date `2026-11-25`.
- `data/sources.json` is the machine-readable registry. Every published data-table row links to at least one official source; social-platform links are supplementary and never replace an official source.
- Newly re-fetched or revalidated source groups: MICHELIN 2025 star article, current MICHELIN all-starred / NYC listing pages, the 18 November 2026 new-additions article (chunks 0–5), current Noury / Mūje / Nyonya / Jungsik New York pages, official restaurant websites, Pod 51 and Arlo NoMad dated booking engines, Arlo and Marriott cyber-sale pages, Marriott citizenM property/rooms pages, Met homepage/visit, NYC Hotel Week pages, and MTA maps / Trip Planner help.
- External URLs were not re-fetched by the build verifier; they were fetched during research. `tools/check_links.py` prints the external URL review list and checks every local link.

## Verification
- Run `python3 tools/compile_data.py`, then `python3 tools/build_site.py`; use `python3 tools/verify.py` and `python3 tools/check_links.py` to re-check the generated site without rebuilding.
- `docs/verification-report.txt` records the latest automated result: **PASS**, 16 generated HTML pages, 406 internal links checked, 0 broken internal links/anchors, 891 data-table rows, 0 rows missing an official-source link, 1,867 official-source links rendered, 384 intentionally blank / unverified fields, 16 flagged irregularities, 77 official sources, 0 sources missing a URL.
- `VERIFICATION.md`, `docs/verification.html`, and `REVIEW.md` / `docs/review.html` provide the line-by-line rule log and repository review. `docs/flagged.html` lists every irregularity and every blank field with official source links.
- Weekday values were computed with Python `datetime`, not estimated. Blank values are rendered as `— unverified`; no value was inferred, filled in, or taken from a third-party travel blog.

## Irregularities / needs review
- NYC Hotel Week press release says 148 hotels while the page says 152 results; Hotel Week ends 11 February 2027, before the requested 15 February–23 March 2027 window. The Jan 6 10am ET reservation time applies to Restaurant / Broadway / Must-See Week, while Hotel Week reservations opened 17 November 2026.
- Arlo official Cyber Exclusive Access page says NYC stays through 31 October 2027 while the official booking rate description says through December 2027; both are cited, neither corrected. Arlo 7-night totals include the urban fee but exclude taxes; Pod 51 totals include taxes and fees. No tax amount was published for Arlo, so the figures are not like-for-like.
- Pod 51 official FAQ lists a $29.84 incl-tax facility fee per room per night, but the dated booking total says only "Including taxes and fees" without itemizing that fee. No manual adjustment was made.
- Met weekly hours are from an official-domain site-restricted search extract; "closed Wednesdays" and $30 admission were also confirmed by direct homepage / visit fetches. The static `plan-your-visit` chunks fetched later contained exhibitions, not the weekly hours table.
- The official 2025 star article lists 72 names (5 three-star, 15 two-star, 52 one-star, including Westchester / Brooklyn / Queens), while the current official all-starred listing shows 69 (5 / 14 / 50). Per-name current status was verified only for 13 restaurants; the 2025 article may be superseded by a later ceremony before the 2027 trip.
- 11 Howard homepage says 207 rooms while its MICHELIN hotel page says 213. A malformed `https://www.https//11howard.oncehospitality.com/...` link and stale 2025 SynXis dates were observed. The official booking root returned only a default 25–26 November 2026 search form, not a 2027 quote.
- COTE search snippet said closed Sundays while the MICHELIN / official Flatiron pages say open 7 days; ESB hours contain a "10 AM = 10 PM" typo and no February 2027 table; Top of the Rock direct page says 8 AM–12 AM while an older official blog says 9 AM–midnight; EMP FAQ gives a $255 bar tasting and later "begin at $225"; The Modern mixes holiday / NYE prices with regular menus; Le Bernardin PDFs have multiple dated versions and prices.
- No official subway / bus travel-time matrix or dated Trip Planner results were captured, so the requested "number of Michelin restaurants within 1 hour" and the resulting hotel ranking are blank. No official source proves a market-wide cheapest booking date. Four hotel 7-night totals, Mūje hours, many restaurant final prices, ESB February 2027 hours, and Central Park hours remain blank.
- During line-by-line cleanup, the unrelated Statue of Liberty Instagram placeholder was removed from MoMA, the 2025 roster alias `Jungsik` was mapped to the current official page `Jungsik New York`, and all November / July / April 2026 MICHELIN new-addition slugs were revalidated against the fetched article. Noury, Mūje and Nyonya current MICHELIN pages and official websites were fetched; Nyonya hours / address / cash-only note were filled, Mūje hours remain blank.

## Log
- 2026-11-25: Initial repository contains only README.md; no existing claims. This session owns initial integration. Arena fixes the branch name to `arena/7386fd81-nyfun3`; no separate session branch can be created. (imported from `arena/7386fd81-nyfun3` COORDINATION.md)
- 2026-11-25: `arena-8781ea5a` read the board from `origin/arena/7386fd81-nyfun3`, preserved the existing claim, and claimed the verified-data-corpus task above. Fetching `origin/main` and `origin/arena/7386fd81-nyfun3` confirmed that branch contained only `COORDINATION.md` and `README.md` at that time.
- 2026-11-25: Claim committed as `30e57a0` and pushed to `origin/arena/8781ea5a-nyfun3`; the remote branch and tracking were created. Later fetches of `origin/arena/7386fd81-nyfun3` showed `dd6cbd6 Build sourced New York trip planning dashboard` with the root-site files and a needs-review board.
- 2026-11-25: Built the self-contained `docs/` dashboard (16 mobile-friendly pages), `data/` corpus (13 JSON files including `blank_fields.json`), root Markdown summaries, source registry, deterministic generators, verification scripts, and an automated report. Re-ran all generators and checks; `python3 tools/verify.py` and `python3 tools/check_links.py` both report 0 broken local links / anchors. No manual user input was requested.
- 2026-11-25: Marked this session's corpus / dashboard task **needs review** and recorded sources, verification, irregularities and scope separation above for the final integration session.
