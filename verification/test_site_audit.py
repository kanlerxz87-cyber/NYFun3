#!/usr/bin/env python3
"""Regression tests for site_audit.py. Uses only the Python standard library."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from urllib.error import HTTPError, URLError

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_audit import (  # noqa: E402
    PublicRedirectHandler,
    audit_site,
    check_external_url,
    concrete_social_video,
    is_public_url,
    load_hosts,
)


PAGE_START = '<!doctype html><html lang="en"><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>Trip</title></head><body>'
PAGE_END = '</body></html>'


class SiteAuditTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def write(self, name: str, content: str):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def page(self, name: str, body: str):
        return self.write(name, PAGE_START + body + PAGE_END)

    def codes(self, report):
        return [item["code"] for item in report["issues"]]

    def test_static_site_validates_relative_links_and_row_host(self):
        self.page("index.html", '''
          <a href="pages/activities.html#museum">Activities</a>
          <link rel="stylesheet" href="assets/style.css">
          <table><thead><tr><th>Name</th><th>Source</th></tr></thead><tbody>
          <tr><td>Park</td><td><a href="https://www.nps.gov/example">Official source</a></td></tr>
          </tbody></table>''')
        self.page("pages/activities.html", '<h1 id="museum">Museum</h1><a href="../index.html">Back</a>')
        self.write("assets/style.css", "body { color: black }")
        report = audit_site(self.root, {"www.nps.gov"})
        self.assertEqual(report["summary"]["html_files"], 2)
        self.assertEqual(report["summary"]["data_rows"], 1)
        self.assertEqual(report["summary"]["rows_with_operator_reviewed_host"], 1)
        self.assertEqual(report["summary"]["errors"], 0)
        self.assertEqual(report["summary"]["warnings"], 0)
        self.assertEqual(report["summary"]["network_mode"], "not checked")
        self.assertIn("does not verify factual claims", report["summary"]["limitation"])

    def test_missing_source_empty_cell_and_fragment_are_reported(self):
        self.page("index.html", '''
          <a href="other.html#missing">Go</a><img src="missing.png">
          <table><tr><td>No evidence</td><td></td></tr></table>''')
        self.page("other.html", '<h1 id="there">Other</h1>')
        report = audit_site(self.root)
        codes = self.codes(report)
        self.assertIn("ROW_NO_SOURCE_LINK", codes)
        self.assertIn("ROW_EMPTY_NOT_FLAGGED", codes)
        self.assertIn("FRAGMENT_MISSING", codes)
        self.assertIn("LOCAL_TARGET_MISSING", codes)
        self.assertIn("IMAGE_ALT_MISSING", codes)

    def test_blank_value_is_not_silently_filled_and_flag_counts(self):
        self.page("index.html", '''<table><tr><td>Hours</td><td>—</td>
          <td>Unverified</td><td><a href="https://www.nps.gov/">Official</a></td></tr></table>''')
        report = audit_site(self.root, {"www.nps.gov"})
        self.assertNotIn("ROW_EMPTY_NOT_FLAGGED", self.codes(report))
        self.assertIn("ROW_EMPTY_FLAG_ELSEWHERE", self.codes(report))
        self.assertEqual(report["summary"]["errors"], 0)

    def test_price_flag_does_not_hide_a_separate_blank_hours_cell(self):
        self.page("index.html", '''<table><tr><td>Jungsik</td><td></td>
          <td>Price unverified</td><td><a href="https://www.nps.gov/">Source</a></td></tr>
          <tr><td>Another</td><td>Hours unverified</td><td>— not verified</td>
          <td><a href="https://www.nps.gov/">Source</a></td></tr></table>''')
        report = audit_site(self.root, {"www.nps.gov"})
        warnings = [issue for issue in report["issues"] if issue["code"] == "ROW_EMPTY_FLAG_ELSEWHERE"]
        self.assertEqual(len(warnings), 1)
        self.assertIn("Jungsik", warnings[0]["message"])
        self.assertIn("cell(s) 2", warnings[0]["message"])
        self.assertNotIn("ROW_EMPTY_NOT_FLAGGED", self.codes(report))

    def test_reviewed_hosts_are_exact_and_social_is_not_official(self):
        self.page("index.html", '''<table>
          <tr><td>A</td><td><a href="https://guide.michelin.com.evil.example/a">source</a></td></tr>
          <tr><td>B</td><td><a href="https://www.youtube.com/watch?v=abc">video</a></td></tr>
          <tr><td>C</td><td><a href="https://guide.michelin.com/g">source</a></td></tr>
        </table>''')
        report = audit_site(self.root, {"guide.michelin.com"})
        self.assertEqual(report["summary"]["data_rows"], 3)
        self.assertEqual(report["summary"]["rows_with_operator_reviewed_host"], 1)
        self.assertEqual(self.codes(report).count("ROW_SOURCE_AUTHORITY_UNREVIEWED"), 1)
        self.assertEqual(self.codes(report).count("ROW_NO_SOURCE_LINK"), 1)

    def test_social_search_and_profile_are_not_specific_posts(self):
        yes = ["https://www.youtube.com/watch?v=abc", "https://youtu.be/abc",
               "https://www.youtube.com/shorts/abc", "https://www.instagram.com/reel/abc/",
               "https://www.instagram.com/p/abc/", "https://www.tiktok.com/@person/video/123"]
        no = ["https://www.youtube.com/results?search_query=nyc", "https://instagram.com/restaurant/",
              "https://tiktok.com/@person", "https://youtube.com/watch", "http://youtu.be/abc"]
        for url in yes:
            self.assertTrue(concrete_social_video(url), url)
        for url in no:
            self.assertFalse(concrete_social_video(url), url)
        self.page("restaurants.html", '''<table>
          <tr><td>A</td><td><a href="https://www.nps.gov/">Official</a></td>
          <td><a href="https://www.youtube.com/results?search_query=a">Search</a></td></tr>
          <tr><td>B</td><td><a href="https://www.nps.gov/">Official</a></td>
          <td><a href="https://youtu.be/abc">Video</a></td></tr></table>''')
        report = audit_site(self.root, {"www.nps.gov"}, review_patterns=["restaurants.html"])
        self.assertEqual(self.codes(report).count("SOCIAL_REVIEW_NOT_FOUND"), 1)
        self.assertEqual(self.codes(report).count("SOCIAL_REVIEW_CONTENT_UNCHECKED"), 1)

    def test_table_marker_can_require_review_without_cli_pattern(self):
        self.page("index.html", '''<table data-audit-reviews><tr><td>Park</td>
          <td><a href="https://www.nps.gov">Official</a></td></tr></table>''')
        self.assertIn("SOCIAL_REVIEW_NOT_FOUND", self.codes(audit_site(self.root, {"www.nps.gov"})))

    def test_project_base_path_and_absolute_site_links(self):
        self.page("index.html", '''
          <a href="/NYFun3/pages/hotels.html#hotel">Within project</a>
          <a href="https://example.github.io/NYFun3/pages/hotels.html">Absolute same site</a>
          <a href="/pages/hotels.html">Incorrect site-root path</a>
          <a href="/NYFun3/../outside.html">Path escape</a>''')
        self.page("pages/hotels.html", '<div id="hotel">Hotel</div>')
        report = audit_site(self.root, base_path="/NYFun3/", site_url="https://example.github.io/NYFun3/")
        self.assertEqual(report["summary"]["local_references_checked"], 2)
        self.assertIn("OUTSIDE_BASE_PATH", self.codes(report))
        self.assertIn("PATH_ESCAPES_ROOT", self.codes(report))
        self.assertEqual(report["summary"]["distinct_external_urls"], 0)

    def test_dynamic_html_and_non_https_links_are_flagged(self):
        self.page("index.html", '''<script src="app.js"></script><base href="/">
          <img src="photo.jpg" alt="" srcset="photo.jpg 1x, photo2.jpg 2x">
          <a href="http://example.com/">Insecure</a><a href="//example.com/">Protocol-relative</a>''')
        self.write("app.js", "document.body.innerHTML += '<p>dynamic</p>'; ")
        self.write("photo.jpg", "a fixture")
        report = audit_site(self.root)
        for code in ("DYNAMIC_CONTENT_NOT_CHECKED", "BASE_ELEMENT_NOT_APPLIED", "SRCSET_NOT_CHECKED",
                     "INSECURE_EXTERNAL_URL", "PROTOCOL_RELATIVE_URL"):
            self.assertIn(code, self.codes(report))

    def test_duplicate_ids_warn_and_local_top_fragment_is_permitted(self):
        self.page("index.html", '<h1 id="x">A</h1><h2 id="x">B</h2><a href="#top">Top</a>')
        report = audit_site(self.root)
        self.assertIn("DUPLICATE_ID", self.codes(report))
        self.assertNotIn("FRAGMENT_MISSING", self.codes(report))

    def test_extra_nested_cells_are_not_mistaken_for_well_formed_table(self):
        self.page("index.html", '''<table><thead><tr><th>Hotel</th><th>Room</th><th>Source</th></tr></thead>
        <tbody><tr><td>Hotel</td><td><td>King bed</td></td>
        <td><a href="https://www.nps.gov/">Source</a></td></tr></tbody></table>''')
        report = audit_site(self.root, {"www.nps.gov"})
        self.assertIn("CELL_START_BEFORE_PREVIOUS_END", self.codes(report))
        self.assertEqual(report["summary"]["errors"], 1)
        self.assertEqual(report["summary"]["data_rows"], 1)

    def test_network_results_distinguish_broken_blocked_and_reachable(self):
        class Response:
            def __init__(self, code, url):
                self.code, self.url = code, url
            def __enter__(self): return self
            def __exit__(self, *_args): return False
            def getcode(self): return self.code
            def geturl(self): return self.url
        calls = []
        def fake_opener(request, timeout):
            url, method = request.full_url, request.get_method()
            calls.append((url, method))
            if "missing" in url:
                raise HTTPError(url, 404, "Not found", {}, None)
            if "blocked" in url:
                raise HTTPError(url, 403, "Blocked", {}, None)
            if "fallback" in url and method == "HEAD":
                raise HTTPError(url, 405, "Method not allowed", {}, None)
            return Response(200, url)
        self.page("index.html", '''<a href="https://example.com/missing">missing</a>
          <a href="https://example.com/blocked">blocked</a>
          <a href="https://example.com/fallback">fallback</a>
          <a href="https://example.com/fallback#again">duplicate</a>''')
        report = audit_site(self.root, network=True, opener=fake_opener)
        self.assertEqual(report["summary"]["external_urls_checked"], 3)
        self.assertEqual(report["summary"]["external_urls_reachable"], 1)
        self.assertEqual(self.codes(report).count("EXTERNAL_BROKEN"), 1)
        self.assertEqual(self.codes(report).count("EXTERNAL_UNVERIFIED"), 1)
        self.assertIn(("https://example.com/fallback", "GET"), calls)
        self.assertIn(("https://example.com/blocked", "GET"), calls)

    def test_network_error_and_obvious_local_addresses_are_unverified(self):
        def fail(request, timeout):
            raise URLError("No network")
        self.assertEqual(check_external_url("https://example.com", 1, fail)[0], "unverified")
        self.assertEqual(check_external_url("http://127.0.0.1/secret", 1, fail)[0], "unverified")
        self.assertFalse(is_public_url("https://[::1]/"))
        self.assertFalse(is_public_url("https://something.local/"))
        self.assertTrue(is_public_url("https://www.nps.gov/"))
        handler = PublicRedirectHandler()
        with self.assertRaises(URLError):
            handler.redirect_request(None, None, 302, "", {}, "http://127.0.0.1/secret")

    def test_manifest_validation_and_cli_json_exit_status(self):
        manifest = self.write("hosts.json", json.dumps({"hosts": [{"host": "www.nps.gov",
            "organization": "NPS", "evidence": "https://www.nps.gov/"}]}))
        self.assertEqual(load_hosts(manifest), {"www.nps.gov"})
        bad = self.write("bad-hosts.json", json.dumps({"hosts": [{"host": "youtube.com",
            "organization": "Bad", "evidence": "https://youtube.com/"}]}))
        with self.assertRaises(ValueError):
            load_hosts(bad)
        self.page("index.html", '<table><tr><td>Missing source</td></tr></table>')
        script = Path(__file__).with_name("site_audit.py")
        result = subprocess.run([sys.executable, str(script), str(self.root), "--host-manifest", str(manifest), "--json"],
                                text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("ROW_NO_SOURCE_LINK", [i["code"] for i in json.loads(result.stdout)["issues"]])

    def test_no_html_is_an_error(self):
        report = audit_site(self.root)
        self.assertIn("NO_HTML_FILES", self.codes(report))
        self.assertEqual(report["summary"]["errors"], 1)


if __name__ == "__main__":
    unittest.main()
