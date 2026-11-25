#!/usr/bin/env python3
"""Conservative, dependency-free audit of a static GitHub Pages site.

This is a triage tool, not a fact checker. See verification/README.md.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
import fnmatch
from html.parser import HTMLParser
import ipaddress
import json
from pathlib import Path
import re
import sys
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, unquote, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


SOCIAL_HOSTS = frozenset({
    "youtube.com", "youtu.be", "instagram.com", "tiktok.com", "facebook.com",
    "twitter.com", "x.com", "pinterest.com", "threads.net",
})
IGNORED_DIRECTORIES = frozenset({
    ".git", ".next", ".arena", ".cache", "node_modules", "__pycache__", ".venv",
})
EMPTY_MARKERS = frozenset({"", "-", "–", "—", "?", "tbd", "unknown", "n/a"})
UNVERIFIED_RE = re.compile(r"\b(?:unverified|not verified)\b", re.I)


@dataclass
class Issue:
    severity: str
    code: str
    file: str
    line: int
    message: str
    url: str = ""


@dataclass
class Link:
    line: int
    tag: str
    attribute: str
    url: str


@dataclass
class Cell:
    text: list[str] = field(default_factory=list)


@dataclass
class Row:
    line: int
    cells: list[Cell] = field(default_factory=list)
    text: list[str] = field(default_factory=list)
    links: list[Link] = field(default_factory=list)
    current_cell: Cell | None = None
    review_required: bool = False


class Document(HTMLParser):
    def __init__(self, relative_path: str):
        super().__init__(convert_charrefs=True)
        self.path = relative_path
        self.links: list[Link] = []
        self.rows: list[Row] = []
        self.ids: dict[str, int] = {}
        self.issues: list[Issue] = []
        self.active_rows: list[Row] = []
        self.table_review: list[bool] = []
        self.lang = False
        self.viewport = False
        self.title = False
        self.in_title = False
        self.ignored_text_depth = 0
        self.has_script = False
        self.has_base = False

    def issue(self, severity: str, code: str, message: str, url: str = "") -> None:
        self.issues.append(Issue(severity, code, self.path, self.getpos()[0], message, url))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        line = self.getpos()[0]
        if tag == "html":
            self.lang = bool((attr.get("lang") or "").strip())
        if tag == "meta" and (attr.get("name") or "").lower() == "viewport":
            self.viewport = bool((attr.get("content") or "").strip())
        if tag == "title":
            self.in_title = True
        if tag == "base" and attr.get("href"):
            self.has_base = True
        if tag in ("script", "style"):
            self.ignored_text_depth += 1
            if tag == "script":
                self.has_script = True
        identifier = attr.get("id")
        if identifier:
            if identifier in self.ids:
                self.issue("warning", "DUPLICATE_ID", f"Duplicate id {identifier!r}; first seen on line {self.ids[identifier]}.")
            else:
                self.ids[identifier] = line
        if tag == "a" and attr.get("name"):
            self.ids.setdefault(attr["name"], line)
        if tag == "img" and "alt" not in attr:
            self.issue("warning", "IMAGE_ALT_MISSING", "Image has no alt attribute; use alt=\"\" for decorative images.")
        if tag == "table":
            self.table_review.append("data-audit-reviews" in attr)
        if tag == "tr":
            if self.active_rows:
                self.issue("warning", "NESTED_TABLE", "Nested table row: manually inspect row and source coverage.")
            self.active_rows.append(Row(line=line, review_required=any(self.table_review)))
        if tag == "td" and self.active_rows:
            cell = Cell()
            self.active_rows[-1].cells.append(cell)
            self.active_rows[-1].current_cell = cell
        if tag == "img" and self.active_rows and self.active_rows[-1].current_cell and attr.get("alt"):
            self.active_rows[-1].current_cell.text.append(attr["alt"] or "")
        for attribute in ("href", "src", "poster"):
            if attribute not in attr:
                continue
            if attribute == "href" and tag not in ("a", "area", "link"):
                continue
            if attribute in ("src", "poster") and tag not in ("img", "script", "iframe", "source", "video", "audio", "embed"):
                continue
            url = attr.get(attribute) or ""
            link = Link(line, tag, attribute, url)
            self.links.append(link)
            if tag in ("a", "area") and self.active_rows:
                self.active_rows[-1].links.append(link)
        if "srcset" in attr:
            self.issue("warning", "SRCSET_NOT_CHECKED", "srcset candidates are not parsed; inspect those image URLs manually.")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        if tag in ("script", "style") and self.ignored_text_depth:
            self.ignored_text_depth -= 1
        if tag == "td" and self.active_rows:
            self.active_rows[-1].current_cell = None
        if tag == "tr" and self.active_rows:
            row = self.active_rows.pop()
            if row.cells:
                self.rows.append(row)
        if tag == "table" and self.table_review:
            self.table_review.pop()

    def handle_data(self, data: str) -> None:
        if self.in_title and data.strip():
            self.title = True
        if self.ignored_text_depth or not self.active_rows:
            return
        row = self.active_rows[-1]
        row.text.append(data)
        if row.current_cell is not None:
            row.current_cell.text.append(data)


def normalize_text(parts: list[str]) -> str:
    return " ".join(" ".join(parts).split())


def belongs_to(host: str, domain: str) -> bool:
    return host == domain or host.endswith("." + domain)


def social_host(host: str) -> bool:
    return any(belongs_to(host, item) for item in SOCIAL_HOSTS)


def parse_url(url: str):
    try:
        parsed = urlsplit(url)
        # Accessing port raises for malformed bracketed/port URLs.
        _ = parsed.port
        return parsed
    except ValueError:
        return None


def concrete_social_video(url: str) -> bool:
    """Recognize video/post URL shapes, not whether their contents are reviews."""
    parts = parse_url(url)
    if not parts or parts.scheme.lower() != "https" or not parts.hostname:
        return False
    host, path = parts.hostname.lower(), parts.path.strip("/")
    chunks = path.split("/") if path else []
    if belongs_to(host, "youtu.be"):
        return bool(chunks and chunks[0])
    if belongs_to(host, "youtube.com"):
        return (path == "watch" and bool(parse_qs(parts.query).get("v"))) or (
            len(chunks) >= 2 and chunks[0] in {"shorts", "live"} and bool(chunks[1])
        )
    if belongs_to(host, "instagram.com"):
        return len(chunks) >= 2 and chunks[0] in {"p", "reel", "reels", "tv"} and bool(chunks[1])
    if belongs_to(host, "tiktok.com"):
        return ("video" in chunks and chunks.index("video") + 1 < len(chunks)) or (
            host in {"vm.tiktok.com", "vt.tiktok.com"} and bool(path)
        )
    return False


def load_hosts(path: Path | None) -> set[str]:
    if path is None:
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("hosts"), list):
        raise ValueError("Host manifest must be an object containing a 'hosts' array.")
    result = set()
    for entry in data["hosts"]:
        if not isinstance(entry, dict):
            raise ValueError("Each host entry must be an object.")
        host = entry.get("host", "")
        evidence = parse_url(entry.get("evidence", "")) if isinstance(entry.get("evidence"), str) else None
        if not isinstance(host, str) or not re.fullmatch(r"[a-z0-9.-]+", host) or host.startswith(".") or host.endswith("."):
            raise ValueError(f"Invalid exact hostname in manifest: {host!r}")
        if not entry.get("organization") or not evidence or evidence.scheme != "https" or not evidence.hostname:
            raise ValueError(f"Host {host!r} needs an organization and an HTTPS evidence URL.")
        if social_host(host):
            raise ValueError(f"Social host {host!r} cannot serve as a trip row's official-source host.")
        result.add(host)
    return result


def iter_html_files(root: Path):
    # Do not follow symlinked files or directories outside the site root.
    import os
    for current, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIRECTORIES and not (Path(current) / d).is_symlink())
        for name in sorted(files):
            path = Path(current) / name
            if path.suffix.lower() in {".html", ".htm"} and not path.is_symlink():
                yield path


def resolve_local(
    root: Path, page: Path, url: str, base_path: str, site_url: str | None
) -> tuple[Path | None, str, str | None, bool]:
    """Return target, fragment, problem code, and whether URL is external."""
    parts = parse_url(url)
    if parts is None:
        return None, "", "INVALID_URL", False
    scheme = parts.scheme.lower()
    if scheme in {"mailto", "tel", "sms", "data"}:
        return None, "", None, False
    if scheme and scheme not in {"http", "https"}:
        return None, "", "UNSUPPORTED_SCHEME", False
    if parts.netloc and not scheme:
        return None, "", "PROTOCOL_RELATIVE_URL", False
    if scheme and not parts.hostname:
        return None, "", "INVALID_URL", False
    if any(character.isspace() for character in url):
        return None, "", "URL_WHITESPACE", False
    if scheme:
        configured = parse_url(site_url) if site_url else None
        same_site = configured is not None and parts.netloc.lower() == configured.netloc.lower()
        if not same_site:
            return None, "", None, True
    path = unquote(parts.path)
    if path.startswith("/"):
        bare_base = base_path.rstrip("/")
        if base_path != "/" and path != bare_base and not path.startswith(base_path):
            return None, "", "OUTSIDE_BASE_PATH", False
        local_path = path[len(bare_base):].lstrip("/") if bare_base else path.lstrip("/")
        target = root / local_path
    else:
        target = page.parent / path if path else page
    target = target.resolve()
    try:
        target.relative_to(root)
    except ValueError:
        return None, "", "PATH_ESCAPES_ROOT", False
    if target.is_dir():
        target = target / "index.html"
    return target, unquote(parts.fragment), None, False


def is_public_url(url: str) -> bool:
    """Avoid obvious local targets in the opt-in network checker."""
    parts = parse_url(url)
    if not parts or parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
        return False
    host = parts.hostname.lower().rstrip(".")
    if host == "localhost" or host.endswith((".localhost", ".local")):
        return False
    try:
        return ipaddress.ip_address(host).is_global
    except ValueError:
        return True


class PublicRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not is_public_url(newurl):
            raise URLError("Redirect to a local or invalid target was blocked.")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def check_external_url(url: str, timeout: float, opener: Callable | None = None) -> tuple[str, str]:
    """Return reachable, broken or unverified. Never equate reachability with truth."""
    if not is_public_url(url):
        return "unverified", "Local or invalid target skipped for safety."
    if opener is None:
        opener = build_opener(PublicRedirectHandler()).open

    def request(method: str):
        req = Request(url, method=method, headers={"User-Agent": "NYFun3-LinkAudit/1.0", "Range": "bytes=0-0"})
        try:
            with opener(req, timeout=timeout) as response:
                return response.getcode(), response.geturl()
        except HTTPError as exc:
            return exc.code, exc.geturl()

    try:
        code, final = request("HEAD")
        if code in (403, 405, 501):
            code, final = request("GET")
        if not is_public_url(final):
            return "unverified", "Redirected to a local or invalid target; inspect manually."
        if 200 <= code < 400:
            if urlsplit(final).scheme.lower() != "https":
                return "unverified", f"Responded HTTP {code} but final URL is not HTTPS: {final}"
            return "reachable", f"HTTP {code}; content and source authority not checked."
        if code in (404, 410):
            return "broken", f"HTTP {code}; the server reports the resource missing."
        return "unverified", f"HTTP {code}; access, rate limiting or a server issue may prevent verification."
    except (URLError, OSError, TimeoutError, ValueError) as exc:
        return "unverified", f"Could not check: {type(exc).__name__}: {exc}"


def audit_site(
    root: Path, approved_hosts: set[str] | None = None, base_path: str = "/",
    site_url: str | None = None, review_patterns: list[str] | None = None,
    network: bool = False, timeout: float = 10.0, workers: int = 4,
    opener: Callable | None = None,
) -> dict:
    root = root.resolve()
    approved_hosts = approved_hosts or set()
    review_patterns = review_patterns or []
    if not root.is_dir():
        raise ValueError(f"Site root is not a directory: {root}")
    if not base_path.startswith("/") or "?" in base_path or "#" in base_path:
        raise ValueError("Base path must be an absolute URL path, such as /NYFun3/.")
    base_path = "/" + base_path.strip("/") + "/" if base_path != "/" else "/"
    if site_url:
        parsed = parse_url(site_url)
        if not parsed or parsed.scheme != "https" or not parsed.hostname or parsed.query or parsed.fragment:
            raise ValueError("Site URL must be an HTTPS URL with no query or fragment.")
    issues: list[Issue] = []
    documents: dict[Path, Document] = {}
    for path in iter_html_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
            doc = Document(rel)
            doc.feed(text)
            doc.close()
            documents[path.resolve()] = doc
            issues.extend(doc.issues)
        except (OSError, UnicodeError, ValueError) as exc:
            issues.append(Issue("error", "HTML_READ_FAILED", rel, 1, f"Could not parse UTF-8 HTML: {exc}"))
    if not documents:
        issues.append(Issue("error", "NO_HTML_FILES", ".", 1, "No readable HTML files found under the site root."))

    rows = candidate_rows = approved_rows = 0
    external_refs: dict[str, list[tuple[str, int]]] = {}
    local_links = 0
    for page, doc in documents.items():
        if not doc.lang:
            issues.append(Issue("warning", "LANG_MISSING", doc.path, 1, "Document has no html lang attribute."))
        if not doc.viewport:
            issues.append(Issue("warning", "VIEWPORT_MISSING", doc.path, 1, "Document has no viewport meta tag; inspect mobile rendering."))
        if not doc.title:
            issues.append(Issue("warning", "TITLE_MISSING", doc.path, 1, "Document has no non-empty title."))
        if doc.has_script:
            issues.append(Issue("warning", "DYNAMIC_CONTENT_NOT_CHECKED", doc.path, 1,
                                "JavaScript is not executed; inspect rendered rows, generated links and interactions separately."))
        if doc.has_base:
            issues.append(Issue("warning", "BASE_ELEMENT_NOT_APPLIED", doc.path, 1,
                                "A base element changes browser URL resolution; this static check does not apply it."))
        for row in doc.rows:
            rows += 1
            row_text = normalize_text(row.text)
            label = normalize_text(row.cells[0].text)[:100] or "(first cell blank)"
            row_prefix = f"Row {label!r}: "
            candidates = []
            for link in row.links:
                parts = parse_url(link.url)
                if parts and parts.scheme.lower() == "https" and parts.hostname and not social_host(parts.hostname.lower()):
                    candidates.append(parts.hostname.lower().rstrip("."))
            if not candidates:
                issues.append(Issue("error", "ROW_NO_SOURCE_LINK", doc.path, row.line,
                                    row_prefix + "no HTTPS non-social source link; add an official source. A review flag does not replace the link."))
            else:
                candidate_rows += 1
                if any(host in approved_hosts for host in candidates):
                    approved_rows += 1
                else:
                    issues.append(Issue("warning", "ROW_SOURCE_AUTHORITY_UNREVIEWED", doc.path, row.line,
                                        row_prefix + f"candidate host(s) {', '.join(sorted(set(candidates)))} not in reviewed manifest; check manually. This does not mean unofficial."))
            missing = sum(1 for cell in row.cells if normalize_text(cell.text).casefold() in EMPTY_MARKERS)
            if missing and not UNVERIFIED_RE.search(row_text):
                issues.append(Issue("warning", "ROW_EMPTY_NOT_FLAGGED", doc.path, row.line,
                                    row_prefix + f"{missing} blank/placeholder cell(s), but the row does not say 'unverified' or 'not verified'."))
            if row.review_required or any(fnmatch.fnmatch(doc.path, pattern) for pattern in review_patterns):
                if not any(concrete_social_video(link.url) for link in row.links):
                    issues.append(Issue("warning", "SOCIAL_REVIEW_NOT_FOUND", doc.path, row.line,
                                        row_prefix + "no recognizable individual social post/video URL; a search, channel, or profile is not a verified review."))
                else:
                    issues.append(Issue("warning", "SOCIAL_REVIEW_CONTENT_UNCHECKED", doc.path, row.line,
                                        row_prefix + "a social post/video URL exists, but its content and relevance still require manual review."))
        for link in doc.links:
            target, fragment, problem, external = resolve_local(root, page, link.url, base_path, site_url)
            if problem:
                issues.append(Issue("error", problem, doc.path, link.line,
                                    "URL cannot be resolved safely for this deployment; inspect it manually.", link.url))
                continue
            if external:
                parts = parse_url(link.url)
                assert parts is not None
                if parts.scheme.lower() != "https":
                    issues.append(Issue("warning", "INSECURE_EXTERNAL_URL", doc.path, link.line,
                                        "External URL is not HTTPS.", link.url))
                # HTTP fragments are not sent to servers and should not create duplicate checks.
                key = urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ""))
                external_refs.setdefault(key, []).append((doc.path, link.line))
                continue
            if target is None:
                continue
            local_links += 1
            if not target.is_file():
                issues.append(Issue("error", "LOCAL_TARGET_MISSING", doc.path, link.line,
                                    "Local page or asset does not exist.", link.url))
            elif fragment and target.suffix.lower() in {".html", ".htm"}:
                target_doc = documents.get(target.resolve())
                if target_doc is None:
                    issues.append(Issue("warning", "FRAGMENT_NOT_CHECKED", doc.path, link.line,
                                        "Target HTML could not be parsed; fragment not checked.", link.url))
                elif fragment not in target_doc.ids and fragment.lower() != "top":
                    issues.append(Issue("error", "FRAGMENT_MISSING", doc.path, link.line,
                                        "Target page does not contain the referenced id/name.", link.url))

    checked = reachable = 0
    if network:
        urls = sorted(external_refs)
        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(lambda url: check_external_url(url, timeout, opener), urls))
        for url, (state, detail) in zip(urls, results):
            checked += 1
            if state == "reachable":
                reachable += 1
                continue
            path, line = external_refs[url][0]
            issues.append(Issue("error" if state == "broken" else "warning",
                                "EXTERNAL_BROKEN" if state == "broken" else "EXTERNAL_UNVERIFIED",
                                path, line, detail, url))

    issues.sort(key=lambda item: (item.file, item.line, item.code, item.url))
    summary = {
        "html_files": len(documents), "data_rows": rows,
        "rows_with_candidate_non_social_https_source": candidate_rows,
        "rows_with_operator_reviewed_host": approved_rows,
        "local_references_checked": local_links, "distinct_external_urls": len(external_refs),
        "network_mode": "checked" if network else "not checked",
        "external_urls_checked": checked, "external_urls_reachable": reachable,
        "errors": sum(i.severity == "error" for i in issues),
        "warnings": sum(i.severity == "warning" for i in issues),
        "limitation": "This static audit does not verify factual claims, official authority for a specific row, future rates/hours, route times, social review content, rendered JavaScript, CSS URLs, accessibility, or redirects' destination contents.",
    }
    return {"summary": summary, "issues": [asdict(issue) for issue in issues]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site_root", type=Path, help="Directory containing the deployed site's index.html")
    parser.add_argument("--host-manifest", type=Path, help="JSON list of manually reviewed exact hostnames")
    parser.add_argument("--base-path", default="/", help="Deployment path, e.g. /NYFun3/ (default: /)")
    parser.add_argument("--site-url", help="Published HTTPS site URL, for validating its absolute links locally")
    parser.add_argument("--review-page", action="append", default=[], metavar="GLOB",
                        help="Require individual social post/video links on rows of matching pages; repeatable")
    parser.add_argument("--network", action="store_true", help="Opt in to checking external HTTP response statuses")
    parser.add_argument("--timeout", type=float, default=10.0, help="Per-request network timeout in seconds")
    parser.add_argument("--workers", type=int, default=4, help="Maximum parallel network checks (1–16)")
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable report")
    parser.add_argument("--fail-on-warnings", action="store_true", help="Exit 1 for warnings as well as errors")
    args = parser.parse_args(argv)
    if not 1 <= args.workers <= 16 or args.timeout <= 0:
        parser.error("workers must be 1–16 and timeout must be positive")
    try:
        hosts = load_hosts(args.host_manifest)
        report = audit_site(args.site_root, hosts, args.base_path, args.site_url, args.review_page,
                            args.network, args.timeout, args.workers)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        summary = report["summary"]
        print(f"Scanned {summary['html_files']} HTML file(s), {summary['data_rows']} data row(s), "
              f"{summary['local_references_checked']} local reference(s), {summary['distinct_external_urls']} external URL(s).")
        print(f"Row source links: {summary['rows_with_candidate_non_social_https_source']}/{summary['data_rows']} candidates; "
              f"{summary['rows_with_operator_reviewed_host']}/{summary['data_rows']} have a host in the supplied manifest.")
        print(f"External network status: {summary['network_mode']} ({summary['external_urls_reachable']}/{summary['external_urls_checked']} reachable).")
        print("IMPORTANT: " + summary["limitation"])
        for issue in report["issues"]:
            suffix = f" — {issue['url']}" if issue["url"] else ""
            print(f"{issue['severity'].upper():7} {issue['file']}:{issue['line']} {issue['code']}: {issue['message']}{suffix}")
        print(f"Result: {summary['errors']} error(s), {summary['warnings']} warning(s).")
    return int(bool(report["summary"]["errors"] or (args.fail_on_warnings and report["summary"]["warnings"])))


if __name__ == "__main__":
    sys.exit(main())
