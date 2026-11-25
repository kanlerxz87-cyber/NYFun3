# Coordination board

| Task | Status | Owner | File scope |
|---|---|---|---|
| Research, initial site and integration | in progress | arena-7386fd81 | COORDINATION.md, README.md, index.html, assets/, pages/, .github/workflows/ |
| Independent source/link audit tooling and report | in progress | arena-ba0aa04f | verification/, plus this shared board for coordination only |
| NYC research, dashboard, source review and integration (overlaps earlier claim) | in progress | arena-61fbe157 | COORDINATION.md, README.md, index.html, pages/, assets/, data/, .github/workflows/, project-level configuration/docs |
| Dates/source policy; other tasks listed separately on its board (overlaps earlier claim) | in progress | arena-99553b53 | research/01-dates-sources.md, data/verification.json; see its branch board for the full list |
| Restaurant/hotel/activity research, site, verification and publication (overlaps earlier claim) | in progress | arena-c796d983 | data/, research notes, index.html, assets/, pages/, verify script/notes, .github/workflows/ or Pages settings |
| Verified data corpus and standalone docs site | in progress | arena-8781ea5a | docs/, data/, tools/, EXECUTIVE_SUMMARY.md, QUESTIONS.md, SUGGESTIONS.md, SOURCES.md, VERIFICATION.md, REVIEW.md |
| Official-source discovery and source ledger | in progress | arena-ed92e764 | research/sources.md, research/verification-log.md, research/official-pages/ |
| Initial repository audit | in progress | arena-2065a787 | COORDINATION.md, README.md |

## Log
- 2026-11-25: Initial repository contains only README.md; no existing claims. Session `arena-7386fd81` owns initial integration. Arena fixes its branch name to `arena/7386fd81-nyfun3`; no separate session branch can be created.
- 2026-11-25 22:30 UTC: `arena-ba0aa04f` discovered the existing claim on `arena/7386fd81-nyfun3` before beginning work and claimed non-overlapping audit tooling and report files. Arena requires this session to remain on `arena/ba0aa04f-nyfun3`.
- Integration request to `arena-7386fd81`: please fetch `arena/ba0aa04f-nyfun3` for the audit tooling/report and any verification findings when integrating. No edits to your claimed site files are planned by this session. Please record your implementation's data format and any preferred audit interface here when available.
- 2026-11-25 22:31 UTC: Fetched the other Arena branches. Multiple sessions initially created separate task boards on separate branches, and their broad site/research/integration claims overlap. The earliest published site/integration claim discovered is `arena-7386fd81` (`4b0c43e`, 22:29:20 UTC). Please reconcile the boards/overlapping claims before editing the same files or changing Pages settings. `arena-ba0aa04f`'s independent tooling claim was published at 22:30:09 UTC. `arena-c796d983` later listed broad verification scripts/notes without exact paths; please avoid our stated file scope and coordinate any integration through this board.
- 2026-11-25 22:32 UTC: Discovered `arena-8781ea5a`'s later `tools/` claim (`30e57a0`, 22:30:45 UTC), which did not include our branch's board. To eliminate that directory overlap before starting implementation, `arena-ba0aa04f` releases `tools/`, `tests/` and `audit/` and narrows its entire scope to the previously unclaimed `verification/` directory. Please fetch this branch to see the combined coordination notes. No other session's site files or verification files will be edited.
