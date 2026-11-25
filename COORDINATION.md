# COORDINATION — NYFun3 shared task board

Last updated: 2026-11-25 UTC
Repository: `kanlerxz87-cyber/NYFun3`
Arena session ID: `ed92e764`
Fixed session branch: `arena/ed92e764-nyfun3`
Base commit: `c251442d122a8d04aade3d8b5a0d57fd4e9ce37c`

## Branch constraint / handoff note

The Arena session policy fixes all work to `arena/ed92e764-nyfun3` and prohibits creating, switching to, or pushing any other branch. Therefore this session cannot use the requested `session-<id>/<task>` branch/worktree naming. To preserve the intent of that instruction, every task below has an explicit, non-overlapping file scope, a status, an owner, and a source/verification log. Other sessions must not edit files inside an `in progress` scope. Shared outputs (`index.html`, navigation, combined table data, and the Pages workflow) are reserved for the final integration task.

## Rules of this board

- Status values: `unclaimed`, `in progress`, `done`, `needs review`.
- `needs review` means the item is published on the site's **Flagged for Review** page and does not block other work.
- Claim by adding the session ID and file scope, then commit and push the claim immediately.
- Use `git pull --rebase` before every push.
- A claim older than 60 minutes with no commits may be taken over; record the handoff in the log.
- Do not mark any value verified without checking it against an official source and recording that link.
- If a task needs a file owned by another session, log a request here instead of editing it.
- Research files may contain provisional observations; only `data/*.json` files with source URLs and verification status feed the published tables.
- Unconfirmed values are left blank and flagged as `unverified`; values are never inferred.

## Task board

| Task ID | Task | Status | Owner session | File scope | Notes |
|---|---|---|---|---|---|
| TASK-00 | Create coordination board and record branch constraint | `in progress` | `ed92e764` | `COORDINATION.md` | Initial claim; repo contained only `README.md`; Pages was configured as legacy from `main`. |
| TASK-01 | Official-source discovery, source ledger, and verification protocol | `unclaimed` |  | `research/sources.md`, `research/verification-log.md`, `research/official-pages/` | Record URLs, access date, and whether each row's source is official. |
| TASK-02 | Hotels, official pricing, Michelin Guide status, and transit evidence | `unclaimed` |  | `research/hotels/`, `research/michelin/`, `research/transit/`, `data/hotels.json`, `data/michelin.json`, `data/transit.json` | Shared combined tables are reserved for TASK-05. |
| TASK-03 | Activities/restaurants, opening days/hours/exceptions, and social-review links | `unclaimed` |  | `research/activities/`, `research/social/`, `data/activities.json`, `data/social.json` | Each factual row needs an official-site source; social links are supplementary and independently checked. |
| TASK-04 | Category subpages, executive summary, Q&A, and improvement suggestions | `unclaimed` |  | `site/pages/`, `site/assets/`, `site/styles.css`, `site/app.js` | Does not edit `index.html` or shared navigation/data. |
| TASK-05 | Final integration: shared index/navigation/data, line-by-line re-verification, link checks, GitHub Pages deployment | `unclaimed` |  | `index.html`, `site/data/`, `.github/workflows/pages.yml`, `README.md`, `COORDINATION.md` | Starts only when TASK-01–04 are done. Publishes via GitHub Actions on the fixed branch. |

## Commit / source log

| Date UTC | Task | Commit | Action | Sources | Verification | Irregularities |
|---|---|---|---|---|---|---|
| 2026-11-25 | TASK-00 | pending | Created board and claimed bootstrap task | Local `README.md`, `git log`, `gh repo view`, GitHub Pages API response | Checked repository contents, branch, remote, auth, and existing Pages configuration | Requested session branches conflict with fixed Arena branch policy; recorded above. Pages uses legacy `main` source and will need switching to GitHub Actions in final integration. |

## Cross-session requests

| Date UTC | Requesting session | Target task/file | Request | Resolution |
|---|---|---|---|---|
|  |  |  |  |  |

## Handoffs / conflicts

| Date UTC | Task | From | To | Reason | Resolution |
|---|---|---|---|---|---|
| 2026-11-25 | TASK-00 | none | `ed92e764` | Board did not exist | Created board and claimed task. |
