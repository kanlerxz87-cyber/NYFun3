#!/usr/bin/env python3
"""Static verification pass: internal links, table source links, data integrity.

Run: python3 scripts/verify_site.py
Exits non-zero if a hard check fails. Warnings are printed for review.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = [ROOT / 'index.html'] + sorted((ROOT / 'pages').glob('*.html'))
problems = []
warnings = []


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.in_tbody = False
        self.rows = []
        self.row_has_source = False
        self.buffer = []
        self.in_table = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
            if self.in_tbody and (a['href'].startswith('https://') or a['href'].startswith('http://')):
                self.row_has_source = True
        if tag == 'table':
            self.in_table = True
        if tag == 'tbody':
            self.in_tbody = True
        if tag == 'tr' and self.in_tbody:
            self.row_has_source = False
            self.buffer = []

    def handle_endtag(self, tag):
        if tag == 'tr' and self.in_tbody:
            self.rows.append(self.row_has_source)
        if tag == 'tbody':
            self.in_tbody = False
        if tag == 'table':
            self.in_table = False

    def handle_data(self, data):
        if self.in_tbody:
            self.buffer.append(data)


for f in HTML_FILES:
    text = f.read_text()
    p = LinkParser()
    p.feed(text)
    for href in p.links:
        if href.startswith(('http://', 'https://', '#', 'mailto:', 'tel:')):
            continue
        target = (f.parent / href.split('#')[0]).resolve()
        if not target.exists():
            problems.append('{}: broken local link {}'.format(f.relative_to(ROOT), href))
    if '<main id="main">' not in text or '<title>' not in text:
        problems.append('{}: missing main/title'.format(f.relative_to(ROOT)))
    if '<meta name="viewport"' not in text:
        problems.append('{}: missing viewport meta'.format(f.relative_to(ROOT)))
    if p.rows and not all(p.rows) and f.name != 'sources.html':
        # sources.html is itself the source index; some rows point to internal pages.
        missing = len(p.rows) - sum(p.rows)
        problems.append('{}: {} table row(s) without any external source link'.format(f.relative_to(ROOT), missing))
    print('{:<38} links={:<4} table_rows={:<4}'.format(str(f.relative_to(ROOT)), len(p.links), len(p.rows)))

# Data integrity checks.
m = json.loads((ROOT / 'data/michelin.json').read_text())
required = {'name', 'distinction', 'cuisine', 'address', 'band', 'hours', 'michelinUrl', 'officialUrl',
            'social', 'priceFor2', 'thirdPartyPrice', 'thirdPartyPriceSource', 'flags'}
for r in m['restaurants']:
    missing = required - set(r)
    if missing:
        problems.append('michelin {}: missing keys {}'.format(r['name'], sorted(missing)))
    if not r['michelinUrl'].startswith('https://guide.michelin.com/'):
        problems.append('michelin {}: non-official source URL'.format(r['name']))
    if not r['hours']:
        warnings.append('michelin {}: hours blank'.format(r['name']))
    if r['priceFor2']:
        problems.append('michelin {}: official price unexpectedly filled'.format(r['name']))
    for s in r['social']:
        if not s['url'].startswith('https://'):
            problems.append('michelin {}: bad social URL'.format(r['name']))

h = json.loads((ROOT / 'data/hotels.json').read_text())
for x in h['hotels']:
    if not x['officialUrl'].startswith('https://'):
        problems.append('hotel {}: missing official URL'.format(x['name']))
    if x['sevenNightTotal'] or x['nightlyRate']:
        problems.append('hotel {}: unverified price unexpectedly filled'.format(x['name']))
    if not x['room']:
        warnings.append('hotel {}: room blank'.format(x['name']))

a = json.loads((ROOT / 'data/activities.json').read_text())
for x in a['activities']:
    if not x['source'].startswith('https://'):
        problems.append('activity {}: missing source'.format(x['name']))
    if x['travelTime']:
        problems.append('activity {}: unverified travel time unexpectedly filled'.format(x['name']))

print('\nWarnings ({}):'.format(len(warnings)))
for w in warnings:
    print(' -', w)
print('\nHard problems ({}):'.format(len(problems)))
for p in problems:
    print(' -', p)
sys.exit(1 if problems else 0)
