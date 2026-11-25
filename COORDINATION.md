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
| T02 | Verify NYC trip dates, sources and official-source policy | in progress | arena/99553b53-nyfun3 | research/01-dates-sources.md, data/verification.json |
| T03 | Research Michelin Guide NYC starred/selected restaurants and menu prices | unclaimed | — | data/michelin.json, research/02-michelin.md |
| T04 | Research hotels with official rates for Feb 2027 dates | unclaimed | — | data/hotels.json, research/03-hotels.md |
| T05 | Research activities and social-media review links | unclaimed | — | data/activities.json, research/04-activities.md |
| T06 | Build GitHub Pages dashboard site (landing + subpages) | unclaimed | — | index.html, assets/, pages/ |
| T07 | Write executive summary, suggestions, open questions, flagged items | unclaimed | — | pages/executive-summary.html, pages/suggestions.html, pages/questions.html, pages/flagged-for-review.html |
| T08 | Line-by-line verification, link check, publish to GitHub Pages | unclaimed | — | scripts/, Pages settings |

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
