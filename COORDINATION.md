# Coordination board

Shared task board for parallel sessions. Claim a task *before* starting it, commit and push the claim immediately, and keep file scopes non-overlapping.

Session ID for this checkout: `arena-8781ea5a` (branch `arena/8781ea5a-nyfun3`).

| Task | Status | Owner | File scope |
|---|---|---|---|
| Research, initial site and integration | in progress | arena-7386fd81 | COORDINATION.md, README.md, index.html, assets/, pages/, .github/workflows/ |
| Verified data corpus (Michelin, hotels, activities, social reviews), standalone dashboard published from `docs/`, executive summary, questions, suggestions, flagged-for-review | in progress | arena-8781ea5a | COORDINATION.md, docs/, data/, tools/, EXECUTIVE_SUMMARY.md, QUESTIONS.md, SUGGESTIONS.md, SOURCES.md, VERIFICATION.md, REVIEW.md |

## Scope separation notes
- `arena-7386fd81` owns the repository-root site (`index.html`, `assets/`, `pages/`) and `.github/workflows/`. This session does **not** edit those paths.
- This session's deliverable is self-contained under `docs/` (a GitHub Pages publishable directory), with machine-readable data in `data/` and a generator in `tools/`. No root `index.html`, `pages/`, `assets/`, or workflow file is created or modified here.
- Arena fixes each session to its own branch and forbids creating/switching/pushing other branches, so the `session-<id>/<task>` branch convention cannot be used. Branch isolation is used instead; the conflict-avoidance mechanism is the file scope table above.
- Request to the final integration session (logged, not executed here): reconcile `docs/` with the root site owned by `arena-7386fd81`, choose one navigation/index, re-verify combined tables line by line, and re-point GitHub Pages if needed.

## Log
- 2026-11-25: Initial repository contains only README.md; no existing claims. This session owns initial integration. Arena fixes the branch name to `arena/7386fd81-nyfun3`; no separate session branch can be created. (imported from `arena/7386fd81-nyfun3` COORDINATION.md)
- 2026-11-25: `arena-8781ea5a` read the board from `origin/arena/7386fd81-nyfun3`, preserved the existing claim, and claimed the verified-data-corpus task above. Fetching `origin/main` and `origin/arena/7386fd81-nyfun3` confirmed that branch contains only `COORDINATION.md` and `README.md` at this time.
