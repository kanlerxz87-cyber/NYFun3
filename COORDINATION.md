# Coordination Board — NYFun3

Shared task board for parallel agent sessions. **Read this before starting any task.**

## Session and branch constraint

This session ID is `arena/99553b53-nyfun3` and the only branch permitted by the
runtime is `arena/99553b53-nyfun3` (the branch named in the session note).
The request asks each session to use a branch named `session-<id>/<task>`;
that is not possible here because the runtime forbids switching or creating
branches. Consequently **this session holds all claims** and acts as its own
final integration session. Other sessions: please do not edit files marked as
claimed below; log requests here instead.

## Task board

| Task ID | Task | Status | Owner session | File scope |
| --- | --- | --- | --- | --- |
| T01 | Create coordination board and claim tasks | done | arena/99553b53-nyfun3 | COORDINATION.md |
| T02 | Verify NYC trip dates, sources and official-source policy | done | arena/99553b53-nyfun3 | research/01-dates-sources.md |
| T03 | Research Michelin Guide NYC starred/selected restaurants and menu prices | done | arena/99553b53-nyfun3 | data/michelin.json, research/02-michelin.md |
| T04 | Research hotels with official rates for Feb 2027 dates | done (pricing unavailable — flagged) | arena/99553b53-nyfun3 | data/hotels.json, research/03-hotels.md |
| T05 | Research activities and social-media review links | done | arena/99553b53-nyfun3 | data/activities.json, research/04-activities.md |
| T06 | Build GitHub Pages dashboard site (landing + subpages) | done | arena/99553b53-nyfun3 | index.html, assets/, pages/ |
| T07 | Write executive summary, suggestions, open questions, flagged items | done | arena/99553b53-nyfun3 | pages/executive-summary.html, pages/suggestions.html, pages/questions.html, pages/flagged-for-review.html |
| T08 | Line-by-line verification, link check, publish to GitHub Pages | in progress (publish pending Pages settings) | arena/99553b53-nyfun3 | scripts/, research/05-verification.md, Pages settings |

## Claim protocol

1. Change a task's status to `in progress`, set owner session ID and exact file scope.
2. Commit and push that claim before editing any scoped file.
3. Work only in your scope. Need another scope? Add a request to the log below.
4. Small, frequent commits; `git pull --rebase` before every push.
5. On merge conflict: stop, resolve without discarding other work, log it here.
6. When done: record sources, verification performed and irregularities below, set `done`.
7. `needs review` means the item is published on the Flagged for Review page and blocks nothing.

## Source / verification rules

- Official sources only for factual table values (Michelin Guide, hotel/brand or
  restaurant/activity own sites, NYC government, MTA, etc.).
- A value that cannot be confirmed on an official page is left blank and
  flagged as unverified. No inference, no estimates presented as facts.
- Every table row carries at least one source link.
- Social links count as verified only when linked from the subject's own
  official site or official Michelin page.

## Log

- 2026-11-25 — Session `arena/99553b53-nyfun3` created board, claimed all tasks
  because the runtime fixes it to one branch. No other session claims present.
- 2026-11-25 — T02/T03/T04/T05 complete. Sources: official Michelin Guide NYC
  restaurant list + 19 detail pages; official hotel pages (Hyatt, Marriott,
  Hilton-indexed content); NPS, MoMA, The Met, 9/11 Memorial, High Line, NYC
  Parks, ESB, Statue City Cruises; YouTube/Instagram pages opened directly.
  Verification: every Michelin row transcribed from its own Michelin page;
  every activity row from its operator/government page. Irregularities: Feb 2027
  dated hotel rates unavailable; Michelin booking window limited to 31 days;
  Met hours differ between indexed official versions; Saga page shows
  millesime=2025; Hilton pages blocked direct fetch; one Atomix YouTube video
  returned 401; a guessed Joo Ok slug failed and was replaced with verified slug
  `joo-ok-1214822`; TikTok links not verifiable; no official subway/bus travel
  times for Feb 2027; 17 of 50 one-star restaurants not captured. All such
  values are blank or flagged on the Flagged for Review page.
- 2026-11-25 — T06/T07 complete. Built mobile dashboard from committed JSON via
  `scripts/build_site.py`: landing page, executive summary, hotels, Michelin,
  activities, itinerary, questions, suggestions, flagged-for-review and sources.
  Tables carry official source links; unverified cells are blank. Correction:
  all 50 one-star names were captured from official pages 1 and 2 (previously 33).
- 2026-11-25 — T08 verification: `scripts/verify_site.py` passes with 0 hard
  problems and 0 warnings; 81 unique external URLs extracted. The sandbox proxy
  blocks direct TLS checks (curl error 35 / EOF), so HTTP status could not be
  confirmed here; representative official pages were re-opened with the page
  fetcher instead, and blocked pages remain flagged. Report:
  `research/05-verification.md`. Remaining step: enable GitHub Pages for this
  branch in repository settings (outside the branch file scope).
- 2026-11-25 — T08 publish attempt: GitHub Pages is already enabled at
  `https://kanlerxz87-cyber.github.io/NYFun3/` but its source is `main`. Changing
  the source to this branch via `gh api PUT /repos/kanlerxz87-cyber/NYFun3/pages`
  returned HTTP 403 (Resource not accessible by integration). No permission to
  change repository settings with this token; branch-side files are complete.
  Local static preview served all pages/assets with HTTP 200.
