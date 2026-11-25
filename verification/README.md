# Independent site audit

This folder belongs to session `arena-ba0aa04f` and is deliberately separate from the site integration session's files. It contains a conservative static triage tool, tests, a short list of reviewed source-host identities, and a snapshot-specific handoff report. It does **not** certify a site or its facts.

## Run

Python 3.10+ is the only requirement; no third-party packages are needed.

```sh
python3 -m unittest -v verification/test_site_audit.py
python3 verification/site_audit.py . \
  --host-manifest verification/official-hosts.json \
  --base-path /NYFun3/ \
  --site-url https://kanlerxz87-cyber.github.io/NYFun3/ \
  --review-page 'pages/dining.html' \
  --review-page 'pages/activities.html'
```

Use the actual published site directory instead of `.` when the site is built into a subdirectory. Use `--review-page` with the actual restaurant/activity page paths (repeat the option as needed); alternatively, put `data-audit-reviews` on the relevant tables. The script also accepts `--json` for machine-readable results and `--fail-on-warnings` for stricter CI. It exits 1 for errors (and, optionally, warnings), 0 otherwise, or 2 for invalid arguments. An absence of errors is **not** a verification of claims or of the live site.

## What it checks

- Local HTML pages, links and selected asset references, missing local targets, HTML fragment IDs, duplicate IDs, and paths unsafe for the configured GitHub Pages project base path. A table header with only `th` cells is not treated as a data row; each row with `td` cells is. Cells started before an earlier cell closes (including nested `<td><td>`) are flagged because browsers may insert extra cells or shift columns. HTML permits some omitted end tags, so inspect any such result rather than assuming the exact rendered layout.
- Each data row has at least an HTTPS, non-social **candidate** source link. A row with none is an error. Social links alone do not satisfy the requested official-source requirement.
- Exact source hosts are checked against `official-hosts.json`, a small manually reviewed *identity* list. An unknown host is a review warning, not proof that the source is unofficial. A known host is not proof that its contents support a particular row or value. The source page and its relationship to the claim still need independent examination.
- Blank/placeholder cells without an `unverified` or `not verified` label in the same row are warned about. This is a heuristic: it does not determine whether a nonempty value is true or whether every unknown value is correctly flagged.
- Rows on specified review pages are checked for a recognizable *individual* YouTube video, Instagram post/reel, or TikTok video URL. A search-results page or profile is not counted. A recognized URL is still flagged for content/relevance review; a URL shape alone does not establish that a review exists.
- Missing document language, viewport metadata, title and image alt attributes are flagged, but this is not a comprehensive accessibility or mobile test.

## External links and safety

Network checks are **off by default**. `--network` optionally attempts HEAD requests with a GET fallback for certain servers. HTTP 404/410 is reported as missing; access blocks, rate limits, server errors and network failures are **unverified**, not automatically broken. A successful response establishes reachability only; it does not establish truth, authority, current hours or rate, or the relevance of a video. In this sandbox, outbound network access is restricted and most external hosts cannot be checked by this script; use an appropriate network-enabled environment and verify content separately. The checker blocks obvious loopback/private literal addresses and local redirects, but does not protect against all DNS rebinding. Run `--network` only on trusted site content, not untrusted arbitrary HTML.

## Limitations and handoff

The tool does not execute JavaScript, follow every CSS URL, inspect `srcset`, calculate routes, evaluate all accessibility concerns, or test mobile layouts. It flags JavaScript and `<base>` use for manual rendered-site inspection. It does not validate future-dated availability, booking costs, cancellation rules, restaurant awards, opening exceptions, meal totals, or the content of social videos. Those require direct inspection of the official subject-specific source, with an access date and separate assessment of every field. Do not turn blank values into guesses or present a reachability result as fact verification.

[GitHub Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site) describes project publishing sources and the requirement that the entry file be at the root of the published source. Check the actual deployment and live links after publication as well as the local build.
