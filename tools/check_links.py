#!/usr/bin/env python3
"""Check local links and manually review external official URLs.

Run `python3 tools/build_site.py` first. This script validates every local file
and anchor link in the generated Markdown/HTML, then prints every external URL
with its source ID so a human can open and check it. External links are not
fetched here because the sandbox is restricted; line-by-line source research
was performed separately with official pages.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
S = json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8"))


def collect_files():
    paths = []
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".html", ".md", ".txt"}:
            if any(part in {".git", "data", "tools", "__pycache__", "node_modules"} for part in p.parts):
                continue
            paths.append(p)
    return sorted(paths)


HREF = re.compile(r'href="([^"]+)"', re.I)
MD = re.compile(r'\[[^\]]+\]\(([^)]+)\)')
ID = re.compile(r'id="([^"]+)"', re.I)


def main():
    files = collect_files()
    ids_by_file = {p.resolve(): set(ID.findall(p.read_text(encoding="utf-8", errors="ignore"))) for p in files}
    broken = []
    local_links = 0
    external = set()

    for p in files:
        text = p.read_text(encoding="utf-8", errors="ignore")
        links = HREF.findall(text) + (MD.findall(text) if p.suffix.lower() == ".md" else [])
        for link in links:
            link = html.unescape(link.strip())
            if link.startswith("#"):
                if link[1:] not in ids_by_file[p.resolve()]:
                    broken.append(f"{p.relative_to(ROOT)}: missing anchor {link}")
                continue
            if link.startswith(("http://", "https://", "mailto:", "//")):
                external.add(link)
                continue
            local_links += 1
            path_part, _, anchor = link.partition("#")
            target = (p.parent / path_part).resolve() if path_part else p.resolve()
            if not target.exists():
                broken.append(f"{p.relative_to(ROOT)}: missing local target {link}")
                continue
            if anchor:
                ids = ids_by_file.get(target) or set(ID.findall(target.read_text(encoding="utf-8", errors="ignore")))
                if anchor not in ids:
                    broken.append(f"{p.relative_to(ROOT)}: missing anchor {link}")

    print(f"Local links checked: {local_links}")
    print(f"Broken local links: {len(broken)}")
    for x in broken:
        print("  BROKEN", x)
    print(f"External URLs in generated content: {len(external)}")
    print(f"Official source registry URLs: {len(S)}")
    print("\nOfficial source review list:")
    for key, s in sorted(S.items()):
        print(f"  {key:28s} {s['checked']}  {s['url']}")
    return 1 if broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
