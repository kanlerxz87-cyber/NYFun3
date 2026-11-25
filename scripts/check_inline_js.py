#!/usr/bin/env python3
"""Syntax-check static JavaScript and every inline page script with node --check."""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(ROOT.glob("*.html")) + sorted((ROOT / "pages").glob("*.html"))
JS_FILES = sorted((ROOT / "assets").rglob("*.js")) + [ROOT / "scripts" / "check_rendered_tables.js"]
SCRIPT_RE = re.compile(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", re.S | re.I)
errors: list[str] = []
checked = 0


def node_check(label: str, code: str) -> None:
    global checked
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(code)
        temp = Path(f.name)
    try:
        result = subprocess.run(["node", "--check", str(temp)], capture_output=True, text=True)
        checked += 1
        if result.returncode:
            errors.append(f"{label}: node --check failed\n{result.stderr.strip()}")
    finally:
        temp.unlink(missing_ok=True)


for path in JS_FILES:
    node_check(str(path.relative_to(ROOT)), path.read_text())

for path in HTML_FILES:
    for i, match in enumerate(SCRIPT_RE.finditer(path.read_text()), 1):
        node_check(f"{path.relative_to(ROOT)} inline script #{i}", match.group(1))

if errors:
    print(f"JavaScript syntax check FAILED ({len(errors)}):", file=sys.stderr)
    for e in errors:
        print(" -", e, file=sys.stderr)
    sys.exit(1)
print(f"OK: node --check passed for {checked} JavaScript units ({len(JS_FILES)} files + inline page scripts)")
