#!/usr/bin/env python3
"""Build the mobile-friendly verified New York trip-planning dashboard.

Run `python3 tools/compile_data.py` first, then:
  python3 tools/build_site.py          # regenerate site + markdown + report
  python3 tools/build_site.py --verify-only   # re-check existing files only

The verifier refuses to publish a data row without at least one official-source
link, and checks that every internal link/anchor resolves.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"
CHECKED = "2026-11-25"

D = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(DATA.glob("*.json"))}
S = D["sources"]

NAV = [
    ("index", "Overview"),
    ("executive-summary", "Executive summary"),
    ("dates", "Dates & booking"),
    ("hotels", "Hotels"),
    ("travel", "Travel & clusters"),
    ("michelin", "MICHELIN stars"),
    ("restaurants", "Restaurants"),
    ("guide-listed", "Guide-listed"),
    ("activities", "Activities"),
    ("social", "Social reviews"),
    ("questions", "Questions"),
    ("suggestions", "Suggestions"),
    ("flagged", "Flagged for review"),
    ("sources", "Sources"),
    ("verification", "Verification"),
    ("review", "Repo review"),
]
NAV_LABEL = dict(NAV)

BLANKS: list[dict] = []
CURRENT_PAGE = "index.html"


def esc(value) -> str:
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def external(url: str, text: str, cls: str = "chip ext", small: str = "") -> str:
    tail = f"<small>{esc(small)}</small>" if small else ""
    return (f'<a class="{esc(cls)}" href="{esc(url)}" target="_blank" '
            f'rel="noopener noreferrer">{esc(text)}{tail}</a>')


def source_links(keys, extra_links=None) -> str:
    items = []
    for key in keys or []:
        s = S.get(key)
        if s:
            items.append((s["url"], s["title"], f'{s["type"]} · checked {s["checked"]}'))
    for e in extra_links or []:
        items.append((e["url"], e.get("label", "Official link"), e.get("note", "official source")))
    if not items:
        return '<span class="unverified">— unverified</span>'
    lis = []
    for url, title, small in items:
        lis.append(f'<li>{external(url, title, "chip official", small)}</li>')
    return '<ul class="source-links">' + "".join(lis) + "</ul>"


def extra_official(entry: dict) -> list[dict]:
    out = []
    for key, label, note in [
        ("official_url", "Official site", "official venue / hotel / restaurant"),
        ("michelin_url", "MICHELIN Guide page", "official guide"),
        ("booking_url", "Official booking page", "official booking engine"),
    ]:
        if entry.get(key):
            out.append({"url": entry[key], "label": label, "note": note})
    return out


def social_links(items) -> str:
    if not items:
        return ""
    lis = []
    for item in items:
        if not item.get("url"):
            continue
        label = f'{item.get("platform", "Social")}: {item.get("title", "Review")}'
        lis.append(f'<li>{external(item["url"], label, "chip social", item.get("kind", ""))}</li>')
    return '<ul class="social-list">' + "".join(lis) + "</ul>"


def flags_list(flags) -> str:
    if not flags:
        return '<span class="badge good">None</span>'
    return ('<ul class="plain-list">' + "".join(
        f'<li><span class="badge warn">Flag</span> {esc(f)}</li>' for f in flags
    ) + "</ul>")


class Row:
    def __init__(self, label: str, sources_keys=None, extra_links=None):
        self.label = label
        self.cells: list[str] = []
        self.has_unverified = False
        self.sources_keys = list(sources_keys or [])
        self.extra_links = list(extra_links or [])

    def cell(self, value, label: str, html_value: bool = False):
        if value is None or value == "" or value == [] or value == {}:
            self.has_unverified = True
            BLANKS.append({"page": CURRENT_PAGE, "row": self.label, "field": label,
                           "sources": self.sources_keys})
            content = '<span class="unverified">— unverified</span>'
        else:
            content = str(value) if html_value else esc(value)
        self.cells.append(f'<td data-label="{esc(label)}">{content}</td>')
        return self

    def social(self, items, label="Social review links"):
        return self.cell(social_links(items), label, html_value=True)

    def flags(self, items, label="Flags"):
        return self.cell(flags_list(items), label, html_value=True)

    def sources(self, label="Official sources"):
        return self.cell(source_links(self.sources_keys, self.extra_links), label, html_value=True)

    def render(self) -> str:
        cls = "data-row" + (" has-unverified" if self.has_unverified else "")
        return f'<tr class="{cls}">' + "".join(self.cells) + "</tr>"


def table(headers, rows, caption=None) -> str:
    cap = f"<caption>{esc(caption)}</caption>" if caption else ""
    head = "<tr>" + "".join(f"<th>{esc(h)}</th>" for h in headers) + "</tr>"
    body = "".join(r.render() for r in rows)
    return (f'<div class="table-wrap"><table>{cap}<thead>{head}</thead>'
            f"<tbody>{body}</tbody></table></div>")


def set_page(slug: str):
    global CURRENT_PAGE
    CURRENT_PAGE = slug + ".html"


def nav_html(active: str) -> str:
    links = "".join(
        f'<a href="{esc(slug)}.html" class="{"active" if slug == active else ""}">{esc(label)}</a>'
        for slug, label in NAV
    )
    return f'<nav class="site-nav" aria-label="Site navigation">{links}</nav>'


def page(slug: str, title: str, description: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{esc(description)}">
<title>{esc(title)} · NY 2027 Trip Research</title>
<link rel="stylesheet" href="assets/site.css">
<script src="assets/site.js" defer></script>
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <div class="brand-row">
      <a class="brand" href="index.html">NY <span>2027</span> Trip Research</a>
      <span class="checked-badge">Official sources checked {CHECKED}</span>
    </div>
    <div class="nav-scroll">{nav_html(slug)}</div>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <p>Verified from official sites only · Blank cells are intentionally unverified ·
  <a href="flagged.html">Flagged for Review</a> ·
  <a href="verification.html">Verification</a> ·
  <a href="sources.html">Sources</a></p>
</footer>
</body>
</html>
"""


def write_page(slug: str, title: str, description: str, body: str):
    set_page(slug)
    (DOCS / f"{slug}.html").write_text(page(slug, title, description, body), encoding="utf-8")


def stat(value, label) -> str:
    return f'<div class="stat"><div class="value">{esc(value)}</div><div class="label">{esc(label)}</div></div>'


def card(title, body, tag="") -> str:
    tag_html = f'<span class="tag">{esc(tag)}</span>' if tag else ""
    return (f'<article class="card">{tag_html}<h3>{esc(title)}</h3>'
            f'<p>{body}</p></article>')


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def build_index():
    es = D["executive_summary"]
    vn = es["verified_numbers"]
    stats = "".join([
        stat(vn["starred_restaurants_current"], "Current starred restaurants"),
        stat(vn["detailed_starred_restaurants"], "Individually re-verified"),
        stat(vn["guide_listed_catalogued"], "Guide-listed catalogued"),
        stat(vn["activities"], "Activities"),
        stat(vn["hotels"], "Hotels"),
        stat(vn["hotels_with_7n_quotes"], "Real 7-night quotes"),
        stat(len(D["flags"]), "Flagged items"),
        stat(vn["official_sources"], "Official sources"),
    ])

    gates = []
    for g in es["decision_gates"]:
        r = Row(g["gate"], g.get("sources", ["repo"]))
        r.cell(g["gate"], "Decision gate")
        r.cell(g["status"], "Status")
        r.cell(", ".join(g["blocking"]), "Blocking questions")
        r.sources()
        gates.append(r)

    cards = [
        ("Dates & booking", "Four real 2027 date options, weekday facts, verified discounts and booking deadlines.", "dates.html", "Plan"),
        ("Hotels", "Six candidates, room requirements, two real 7-night totals and blank/flagged gaps.", "hotels.html", "Stay"),
        ("MICHELIN stars", "Current counts, the full 2025 star roster and explicit star-vs-listed status.", "michelin.html", "Eat"),
        ("Restaurants", "13 starred restaurants with per-day hours, exceptions, prices and social links.", "restaurants.html", "Eat"),
        ("Guide-listed", "2026 Selection additions and Bib Gourmand examples with no-star status.", "guide-listed.html", "Eat"),
        ("Activities", "11 museums, landmarks and parks with official links, hours and review links.", "activities.html", "Do"),
        ("Travel & clusters", "ZIP clusters, same-ZIP hotel view, price ranking and the blocked 1-hour transit analysis.", "travel.html", "Analyze"),
        ("Questions", "What is known, what is missing, answers and discovery steps for every decision.", "questions.html", "Decide"),
        ("Suggestions", "Improvement options with a path chooser; nothing implemented before review.", "suggestions.html", "Decide"),
        ("Flagged for review", "Irregularities, conflicts and every intentionally blank value.", "flagged.html", "Review"),
        ("Sources", "The complete official-source registry with check dates and direct links.", "sources.html", "Verify"),
        ("Repo review", "Line-by-line repository review and irregularities from the parallel-session board.", "review.html", "Verify"),
    ]
    card_html = "".join(
        card(title, f'{desc} <a class="card-link" href="{esc(url)}">Open →</a>', tag)
        for title, desc, url, tag in cards
    )

    highlights = "".join([
        card("Lowest verified all-in 7-night hotel total",
             f'<strong>{esc(es["verified_numbers"]["lowest_verified_all_in_7n_total"])}</strong> — '
             "Pod 51 Queen Pod, 15–22 Feb 2027, 2 adults, including taxes and fees. "
             '<a href="hotels.html">Compare hotels →</a>', "Price"),
        card("Best verified booking deadlines",
             "Arlo Hotels Cyber Exclusive Access: 40% off, book by 3 Dec 2026. "
             "Marriott CYBER SALE at citizenM: 15%/25% off, book by Tuesday 1 Dec. "
             '<a href="dates.html">See booking windows →</a>', "Booking"),
        card("MICHELIN picture",
             "69 starred NYC/surroundings restaurants (5×3★, 14×2★, 50×1★), 76 Bib Gourmand and "
             "224 Selected. Guide-listed is not starred. "
             '<a href="michelin.html">Open MICHELIN tables →</a>', "Dining"),
        card("What is deliberately blank",
             "1-hour MTA travel times, four hotel 7-night totals, many restaurant final prices and "
             "February 2027 venue hours are blank because no official source confirmed them. "
             '<a href="flagged.html">Review every flag →</a>', "Integrity"),
    ])

    body = f"""
<section class="hero">
  <div class="eyebrow">New York · 15 Feb – 23 Mar 2027 · 2 adults</div>
  <h1>Verified trip research, in one simple dashboard.</h1>
  <p>{esc(es["headline"])}</p>
  <div class="hero-meta">
    <span>Official-site source on every row</span>
    <span>Blank = unverified, never inferred</span>
    <span>Mobile-friendly tables</span>
    <span>Checked {CHECKED}</span>
  </div>
</section>
<section class="stats" aria-label="Verified data at a glance">{stats}</section>
<div class="note"><strong>How to read this site:</strong> every published table row links to at least one official source. A value that could not be confirmed is left blank, shown as <span class="unverified">— unverified</span>, and listed on the <a href="flagged.html">Flagged for Review</a> page. Social-review links sit alongside entries but never replace an official source.</div>
<h2 class="section-title">Decision gates</h2>
{table(["Decision gate", "Status", "Blocking questions", "Official sources"], gates, "What is ready and what is blocked")}
<h2 class="section-title">Verified highlights</h2>
<div class="card-grid">{highlights}</div>
<h2 class="section-title">Explore by category</h2>
<div class="card-grid">{card_html}</div>
<div class="warning"><strong>Parallel sessions:</strong> another session owns the repository-root site (<code>index.html</code>, <code>assets/</code>, <code>pages/</code>). This dashboard is self-contained in <code>docs/</code>; the other session's files are preserved and the final integration request is logged in <code>COORDINATION.md</code>.</div>
"""
    write_page("index", "Overview", "Verified New York 2027 trip research dashboard", body)


def build_executive_summary():
    es = D["executive_summary"]
    kp_rows = []
    for k in es["key_points"]:
        r = Row(k["title"], k.get("sources", ["repo"]))
        r.cell(k["title"], "Topic")
        r.cell(k["text"], "Finding")
        r.sources()
        kp_rows.append(r)

    gate_rows = []
    for g in es["decision_gates"]:
        r = Row(g["gate"], g.get("sources", ["repo"]))
        r.cell(g["gate"], "Decision gate")
        r.cell(g["status"], "Status")
        r.cell(", ".join(g["blocking"]), "Blocking questions")
        r.sources()
        gate_rows.append(r)

    number_rows = []
    for key, value in es["verified_numbers"].items():
        r = Row(key, ["repo"])
        r.cell(key.replace("_", " ").title(), "Metric")
        r.cell(value, "Verified value")
        r.sources()
        number_rows.append(r)

    body = f"""
<div class="page-head"><h1>Executive summary</h1><p>{esc(es["headline"])}</p></div>
<div class="success"><strong>Bottom line:</strong> {esc(es["headline"])}</div>
<h2 class="section-title">Important details</h2>
{table(["Topic", "Finding", "Official sources"], kp_rows, "Executive findings")}
<h2 class="section-title">Decision gates</h2>
{table(["Decision gate", "Status", "Blocking questions", "Official sources"], gate_rows, "Go / no-go view")}
<h2 class="section-title">Verified numbers</h2>
{table(["Metric", "Verified value", "Official sources"], number_rows, "Snapshot of the data corpus")}
<div class="note"><a href="index.html">← Overview</a> · <a href="questions.html">Questions →</a></div>
"""
    write_page("executive-summary", "Executive summary", "Executive summary of the verified trip research", body)


def build_dates():
    t = D["trip"]
    options = []
    for o in t["options"]:
        r = Row(o["id"] + " · " + o["name"], o["sources"])
        r.cell(o["id"], "Option")
        r.cell(o["name"], "Name")
        r.cell(o["check_in"], "Check-in")
        r.cell(o["weekday_in"], "Check-in weekday")
        r.cell(o["check_out"], "Check-out")
        r.cell(o["weekday_out"], "Check-out weekday")
        r.cell(o["nights"], "Nights")
        r.cell(o["note"], "Note")
        r.sources()
        options.append(r)

    facts = []
    for i, f in enumerate(t["verified_facts"], 1):
        r = Row(f"F{i:02d}", f["sources"])
        r.cell(f["fact"], "Verified fact")
        r.sources()
        facts.append(r)

    flag_rows = []
    for i, f in enumerate(t["flags"], 1):
        r = Row(f"T{i:02d}", ["repo"])
        r.cell(f, "Trip-date flag")
        r.sources()
        flag_rows.append(r)

    cb = t["cheapest_booking_window"]
    cb_sources = source_links(cb["sources"])
    body = f"""
<div class="page-head"><h1>Dates &amp; booking</h1><p>Party: {esc(t["party"])}. Allowed window: {esc(t["window"]["start"])} to {esc(t["window"]["end"])}. {esc(t["window"]["note"])}</p></div>
<div class="warning"><strong>Window conflict:</strong> the only official city-wide hotel discount (NYC Hotel Week, 2 Jan–11 Feb 2027) ends four days before the earliest allowed check-in. See the in-window offers below.</div>
<h2 class="section-title">Date options</h2>
{table(["Option", "Name", "Check-in", "Weekday", "Check-out", "Weekday", "Nights", "Note", "Official sources"], options, "Real 2027 date options")}
<h2 class="section-title">Verified date &amp; deal facts</h2>
{table(["Verified fact", "Official sources"], facts, "Line-by-line official facts")}
<h2 class="section-title">Cheapest / best upcoming time to book</h2>
<div class="card"><h3>Verified answer</h3><p>{esc(cb["answer"])}</p>
<p><strong>Best verified deadlines:</strong> {esc(cb["best_time_to_book_for_requested_dates"])}</p>
<p class="muted">{esc(cb["note"])}</p>
<h3>Official sources</h3>{cb_sources}</div>
<h2 class="section-title">Trip-date flags</h2>
{table(["Trip-date flag", "Official sources"], flag_rows, "Needs review")}
<div class="note"><a href="index.html">← Overview</a> · <a href="hotels.html">Hotels →</a></div>
"""
    write_page("dates", "Dates & booking", "2027 trip dates, verified discounts and booking deadlines", body)


def build_hotels():
    hotels = D["hotels"]
    rows = []
    for h in hotels:
        r = Row(h["name"], h["sources"], extra_official(h))
        r.cell(h["name"], "Hotel")
        r.cell(h["area"], "Area")
        r.cell((h["address"] + (f" · ZIP {h['zip']}" if h["zip"] else "")), "Address / ZIP")
        r.cell(h["private_bath"], "Private bathroom")
        r.cell(h["bed"], "Bed")
        r.cell(h["amenities"], "Amenities")
        r.cell(h["fees"], "Fees / price basis")
        r.cell(h["transit"], "Transit")
        r.cell(h["price_7n"], "7-night total for 2 adults")
        r.cell(h["price_note"], "Price note")
        r.cell(h["exceptions"], "Exceptions")
        r.social(h.get("social", []), "Hotel social reviews")
        r.flags(h.get("flags", []), "Hotel flags")
        r.sources()
        rows.append(r)

    quotes = []
    for h in hotels:
        for q in h.get("price_quotes", []):
            r = Row(f'{h["name"]} · {q["rate"]}', [q["source"]], [{"url": S[q["source"]]["url"], "label": "Official booking quote", "note": "official dated quote"}])
            r.cell(h["name"], "Hotel")
            r.cell(q["room"], "Room")
            r.cell(q["rate"], "Rate")
            r.cell(q["total"], "Total for 7 nights")
            r.cell(q["basis"], "Official basis")
            r.sources()
            quotes.append(r)

    body = f"""
<div class="page-head"><h1>Hotels</h1><p>Six candidates, with the two mandatory room requirements shown explicitly. All 7-night totals below are real dated official quotes for 15–22 Feb 2027, 2 adults, 1 room — not estimates.</p></div>
<div class="success"><strong>Lowest verified all-in total:</strong> Pod 51 Queen Pod Pod Member Rate, $1,109 for 7 nights including taxes and fees. Arlo NoMad's $1,296 includes the urban fee but excludes taxes, so it is not like-for-like.</div>
<h2 class="section-title">Hotel comparison</h2>
{table(["Hotel", "Area", "Address / ZIP", "Private bathroom", "Bed", "Amenities", "Fees / price basis", "Transit", "7-night total", "Price note", "Exceptions", "Social reviews", "Flags", "Official sources"], rows, "Candidate hotels")}
<h2 class="section-title">Real dated 7-night quotes</h2>
{table(["Hotel", "Room", "Rate", "Total", "Official basis", "Official sources"], quotes, "Official booking-page totals")}
<div class="warning"><strong>Comparison caveat:</strong> {esc(D["analysis"]["price_comparison_caveat"])}</div>
<div class="note"><a href="dates.html">← Dates</a> · <a href="travel.html">Travel &amp; clusters →</a></div>
"""
    write_page("hotels", "Hotels", "Verified hotel comparison with real 7-night prices", body)


def build_michelin():
    m = D["michelin"]
    c = m["counts_current"]
    count_rows = []
    for label, key in [
        ("3 MICHELIN Stars", "three_star"), ("2 MICHELIN Stars", "two_star"),
        ("1 MICHELIN Star", "one_star"), ("Starred total", "starred_total"),
        ("Bib Gourmand", "bib_gourmand"), ("Selected restaurants (no star)", "selected_restaurants"),
        ("NYC Guide total", "nyc_total"),
    ]:
        r = Row(label, c["sources"])
        r.cell(label, "Distinction")
        r.cell(c[key], "Count")
        r.sources()
        count_rows.append(r)
    for day, count in c["days_open_aggregate"].items():
        r = Row("Open on " + day, c["sources"])
        r.cell("Starred restaurants open on " + day, "Day")
        r.cell(count, "Count")
        r.sources()
        count_rows.append(r)

    roster = []
    for r0 in m["roster"]:
        r = Row(r0["name"], r0["sources"], [{"url": r0["michelin_url"], "label": "MICHELIN Guide page", "note": "official guide"}])
        r.cell(r0["name"], "Restaurant")
        r.cell(r0["stars_2025"], "2025 star level")
        r.cell(r0["cuisine"], "Cuisine")
        r.cell(r0["current_star_verified"], "Current star verified")
        r.cell(external(r0["michelin_url"], "Official MICHELIN page", "chip official"), "MICHELIN link", html_value=True)
        r.flags(r0.get("flags", []), "Roster flags")
        r.sources()
        roster.append(r)

    green = "".join(f'<span class="chip">{esc(x)}</span>' for x in m["green_stars_2025"])
    body = f"""
<div class="page-head"><h1>MICHELIN stars</h1><p>{esc(m["status_note"])}</p></div>
<div class="note"><strong>Status rule:</strong> “Starred” means 1–3 MICHELIN Stars. “Listed / Selected”, “Bib Gourmand” and Green Star are Guide distinctions without a Star. The <a href="guide-listed.html">Guide-listed page</a> catalogues the 2026 Selection additions separately.</div>
<h2 class="section-title">Current official counts</h2>
<p class="muted">{esc(c["note"])}</p>
{table(["Distinction / day", "Count", "Official sources"], count_rows, "MICHELIN Guide NYC selection counts")}
<h2 class="section-title">2025 Green Stars</h2>
<div class="card"><p>{green}</p><p class="muted small">Green Stars are sustainability distinctions, not additional Michelin Stars. Source: <a href="{esc(S["michelin_stars_2025"]["url"])}" target="_blank" rel="noopener noreferrer">official 2025 star article</a>.</p></div>
<h2 class="section-title">Full 2025 star roster</h2>
{table(["Restaurant", "2025 stars", "Cuisine", "Current star verified", "MICHELIN link", "Flags", "Official sources"], roster, "2025 official star article roster (72 names)")}
<div class="note"><a href="restaurants.html">Detailed starred restaurants →</a> · <a href="guide-listed.html">Guide-listed →</a></div>
"""
    write_page("michelin", "MICHELIN stars", "Official MICHELIN star counts and full 2025 star roster", body)


def build_restaurants():
    rows = []
    for r0 in D["michelin"]["detailed"]:
        r = Row(r0["name"], r0["sources"], extra_official(r0))
        r.cell(r0["name"], "Restaurant")
        r.cell(r0["status"], "Star status")
        r.cell(r0["stars"], "Stars")
        r.cell(r0["cuisine"], "Cuisine")
        r.cell((r0["address"] + (f" · ZIP {r0['zip']}" if r0["zip"] else "")), "Address / ZIP")
        r.cell(r0["days_open"], "Days open")
        r.cell(r0["hours"], "Hours")
        r.cell(r0["exceptions"], "Exceptions")
        r.cell(r0["price_two"], "Cost for 2 adults")
        r.cell(r0["price_basis"], "Price basis")
        r.cell(r0["price_note"], "Price note")
        r.cell(external(r0["official_url"], "Official site", "chip official") if r0["official_url"] else "", "Official site", html_value=bool(r0["official_url"]))
        r.cell(external(r0["michelin_url"], "MICHELIN page", "chip official"), "MICHELIN link", html_value=True)
        r.social(r0.get("social", []))
        r.flags(r0.get("flags", []))
        r.sources()
        rows.append(r)

    body = f"""
<div class="page-head"><h1>Starred restaurants — detailed</h1><p>13 restaurants whose current official MICHELIN pages were fetched line by line. Cost figures labelled “subtotal” are pure arithmetic from official per-person menu prices, not a final check total.</p></div>
{table(["Restaurant", "Star status", "Stars", "Cuisine", "Address / ZIP", "Days open", "Hours", "Exceptions", "Cost for 2", "Price basis", "Price note", "Official site", "MICHELIN link", "Social reviews", "Flags", "Official sources"], rows, "Starred restaurants with hours, prices and social links")}
<div class="note"><a href="michelin.html">← MICHELIN roster</a> · <a href="guide-listed.html">Guide-listed →</a></div>
"""
    write_page("restaurants", "Starred restaurants", "Detailed starred restaurants with official hours, prices and review links", body)


def build_guide_listed():
    rows = []
    for g in D["michelin"]["guide_listed"]:
        r = Row(g["name"], g["sources"], extra_official(g))
        r.cell(g["name"], "Restaurant")
        r.cell(g["status"], "Status")
        r.cell(g["added"], "Added")
        r.cell(g["cuisine"], "Cuisine")
        r.cell(g["area"], "Area")
        r.cell((g["address"] + (f" · ZIP {g['zip']}" if g["zip"] else "")), "Address / ZIP")
        r.cell(g["days_open"], "Days open")
        r.cell(g["hours"], "Hours")
        r.cell(g["exceptions"], "Exceptions")
        r.cell(g["price_two"], "Cost for 2 adults")
        r.cell(g["price_note"], "Price note")
        r.cell(external(g["michelin_url"], "MICHELIN page", "chip official"), "MICHELIN link", html_value=True)
        r.cell(external(g["official_url"], "Official site", "chip official") if g["official_url"] else "", "Official site", html_value=bool(g["official_url"]))
        r.social(g.get("social", []))
        r.flags(g.get("flags", []))
        r.sources()
        rows.append(r)

    body = f"""
<div class="page-head"><h1>Guide-listed / Selected (no star)</h1><p>These entries are in the MICHELIN Guide but do not have a confirmed Michelin Star. Blank cells are intentional: the official new-additions article does not publish hours, exact prices or social links for most of them.</p></div>
<div class="warning"><strong>Not starred:</strong> the official article states Stars and Bib Gourmands are revealed only at the annual ceremony; new restaurants are added to the Selection twice a year and marked “New”. Bib Gourmand is also a Guide distinction, not a Star.</div>
{table(["Restaurant", "Status", "Added", "Cuisine", "Area", "Address / ZIP", "Days open", "Hours", "Exceptions", "Cost for 2", "Price note", "MICHELIN link", "Official site", "Social reviews", "Flags", "Official sources"], rows, "Guide-listed / Selected restaurants")}
<div class="note"><a href="restaurants.html">← Starred restaurants</a> · <a href="activities.html">Activities →</a></div>
"""
    write_page("guide-listed", "Guide-listed restaurants", "MICHELIN Guide-listed and Selected restaurants without stars", body)


def build_activities():
    rows = []
    for a in D["activities"]:
        r = Row(a["name"], a["sources"], extra_official(a))
        r.cell(a["name"], "Activity")
        r.cell(a["category"], "Category")
        r.cell(a["days_open"], "Days open")
        r.cell(a["hours"], "Hours")
        r.cell(a["exceptions"], "Exceptions")
        r.cell(a["price_two"], "Cost for 2 adults")
        r.cell(a["price_note"], "Price note")
        r.cell(external(a["official_url"], "Official site", "chip official"), "Official link", html_value=True)
        r.social(a.get("social", []))
        r.flags(a.get("flags", []))
        r.sources()
        rows.append(r)

    body = f"""
<div class="page-head"><h1>Activities</h1><p>11 museums, landmarks, observation decks and parks. Every row has an official link; days, hours and exceptions are transcribed from official venue or government pages.</p></div>
{table(["Activity", "Category", "Days open", "Hours", "Exceptions", "Cost for 2", "Price note", "Official link", "Social reviews", "Flags", "Official sources"], rows, "Activities with official schedules and review links")}
<div class="note"><a href="guide-listed.html">← Guide-listed</a> · <a href="social.html">Social reviews →</a></div>
"""
    write_page("activities", "Activities", "Official activity schedules, prices and social review links", body)


def build_travel():
    a = D["analysis"]
    zrows = []
    for z in a["zip_clusters"]:
        r = Row("ZIP " + z["zip"], z.get("sources", ["michelin_all_starred"]))
        r.cell(z["zip"], "ZIP")
        r.cell(z["count"], "Starred restaurants in sample")
        r.cell("".join(external(x["michelin_url"], f'{x["name"]} ({x["stars"]}★)', "chip official") for x in z["restaurants"]), "Restaurants", html_value=True)
        r.sources()
        zrows.append(r)

    hzip = []
    for h in a["hotel_zip_clusters"]:
        r = Row(h["hotel"], h["sources"])
        r.cell(h["hotel"], "Hotel")
        r.cell(h["zip"], "ZIP")
        r.cell(h["same_zip_count"], "Same-ZIP count")
        r.cell(", ".join(h["restaurants"]), "Restaurants")
        r.cell(h["note"], "Note")
        r.sources()
        hzip.append(r)

    prows = []
    for q in a["price_rank"]:
        r = Row(f'{q["hotel"]} · {q["rate"]}', [q["source"]], [{"url": S[q["source"]]["url"], "label": "Official quote", "note": "official dated quote"}])
        r.cell(q["hotel"], "Hotel")
        r.cell(q["room"], "Room")
        r.cell(q["rate"], "Rate")
        r.cell(q["total"], "Total for 7 nights")
        r.cell("Yes" if q["taxes_included"] else "No", "Taxes & fees included")
        r.cell(q["basis"], "Basis")
        r.sources()
        prows.append(r)

    vrows = []
    for v in a["verified_attribute_ranking"]:
        r = Row(v["hotel"], v["sources"])
        r.cell(v["hotel"], "Hotel")
        r.cell(v["score"], "Verified fields")
        r.cell(", ".join(v["fields"]), "Fields")
        r.sources()
        vrows.append(r)

    tt = a["travel_time"]
    body = f"""
<div class="page-head"><h1>Travel &amp; MICHELIN clusters</h1><p>{esc(a["method"])}</p></div>
<div class="warning"><strong>Blocked ranking:</strong> {esc(tt["why"])} The requested “number of Michelin restaurants within 1 hour by subway/bus” and the resulting hotel ranking are <span class="unverified">— unverified</span> and intentionally blank.</div>
<h2 class="section-title">Starred restaurants by ZIP (verified sample)</h2>
<p class="muted">{esc(a["cluster_scope"])} {esc(a["same_zip_note"])}</p>
{table(["ZIP", "Count", "Restaurants", "Official sources"], zrows, "Clusters from official MICHELIN street addresses")}
<h2 class="section-title">Hotels matched to same-ZIP clusters</h2>
{table(["Hotel", "ZIP", "Same-ZIP count", "Restaurants", "Note", "Official sources"], hzip, "Static same-ZIP view — not travel time")}
<h2 class="section-title">Real dated price ranking</h2>
<div class="success"><strong>{esc(a["best_price_verified"])}</strong></div>
{table(["Hotel", "Room", "Rate", "Total", "Taxes & fees included", "Basis", "Official sources"], prows, "Official 7-night quotes, sorted by displayed total")}
<h2 class="section-title">Verified-attribute ranking</h2>
<p class="muted">{esc(a["verified_attribute_rule"])}</p>
{table(["Hotel", "Verified fields", "Fields", "Official sources"], vrows, "Count of confirmed requirement fields")}
<h2 class="section-title">Travel-time status</h2>
<div class="card"><h3>1-hour transit count</h3><p><span class="unverified">— unverified</span> {esc(tt["why"])}</p>{source_links(tt["sources"])}</div>
<div class="card"><h3>MICHELIN-density hotel ranking</h3><p><span class="unverified">— unverified</span> {esc(a["michelin_density_ranking_status"])}. No count was inferred from distance, ZIP or a map.</p>{source_links(["mta_trip", "mta_maps"])}</div>
<div class="note"><a href="hotels.html">← Hotels</a> · <a href="questions.html">Questions →</a></div>
"""
    write_page("travel", "Travel & clusters", "MICHELIN ZIP clusters, verified price ranking and blocked 1-hour transit analysis", body)


def build_questions():
    rows = []
    for q in D["questions"]:
        r = Row(q["id"] + " · " + q["question"], q["sources"])
        r.cell(q["id"], "ID")
        r.cell(q["question"], "Question / information needed")
        r.cell(q["have"], "What we have")
        r.cell(q["answer"], "Answer")
        r.cell(q["missing"], "Still missing")
        r.cell(q["discover"], "How to discover missing info")
        r.cell("Yes" if q["blocks_decision"] else "No", "Blocks decision")
        r.sources()
        rows.append(r)
    blocking = [q for q in D["questions"] if q["blocks_decision"]]
    body = f"""
<div class="page-head"><h1>Questions, information &amp; answers</h1><p>A clear list of what must be addressed before a reasonable decision can be made, based on what is already known and what is still missing. {len(blocking)} of {len(D["questions"])} questions currently block a decision.</p></div>
<div class="warning"><strong>Blocking now:</strong> {", ".join(q["id"] for q in blocking)}. None were filled with guesses; each has a discovery step.</div>
{table(["ID", "Question / information needed", "What we have", "Answer", "Still missing", "How to discover", "Blocks decision", "Official sources"], rows, "Decision questions")}
<div class="note"><a href="travel.html">← Travel &amp; clusters</a> · <a href="suggestions.html">Suggestions →</a></div>
"""
    write_page("questions", "Questions & answers", "Known information, unanswered questions and discovery steps", body)


def build_suggestions():
    rows = []
    for s in D["suggestions"]:
        r = Row(s["id"] + " · " + s["title"], s.get("sources", ["repo"]))
        r.cell(s["id"], "ID")
        r.cell(s["title"], "Suggestion")
        r.cell(s["problem"], "Problem")
        r.cell(s["proposal"], "Proposed improvement")
        r.cell(s["decision_needed"], "Decision needed before implementation")
        r.cell(s["effort"], "Effort")
        r.cell(s["priority"], "Priority")
        r.cell(s["status"], "Status")
        r.sources()
        rows.append(r)
    path_cards = "".join(
        f'''<div class="path-card"><h3>{esc(s["id"])} · {esc(s["title"])}</h3>
        <p>{esc(s["proposal"])}</p>
        <div class="path-options">
          <label><input type="radio" name="path-{esc(s["id"])}" value="approve">Approve</label>
          <label><input type="radio" name="path-{esc(s["id"])}" value="defer">Defer</label>
          <label><input type="radio" name="path-{esc(s["id"])}" value="reject">Reject</label>
        </div></div>'''
        for s in D["suggestions"]
    )
    body = f"""
<div class="page-head"><h1>Suggestions</h1><p>Dedicated review section. These are improvement options only — no suggestion has been implemented before a path is chosen. The chooser below is a static review aid; it does not submit data.</p></div>
<div class="warning"><strong>Choose before implementing:</strong> each suggestion lists the decision that must be made first. The site intentionally leaves blocked values blank instead of adopting a change that would require unverified data.</div>
{table(["ID", "Suggestion", "Problem", "Proposed improvement", "Decision needed", "Effort", "Priority", "Status", "Official sources"], rows, "Improvement options")}
<h2 class="section-title">Path chooser</h2>
<div class="path-grid">{path_cards}</div>
<div class="note"><a href="questions.html">← Questions</a> · <a href="flagged.html">Flagged for review →</a></div>
"""
    write_page("suggestions", "Suggestions", "Review improvement options and choose a path before implementation", body)


def build_flagged():
    rows = []
    for f in D["flags"]:
        r = Row(f["id"] + " · " + f["title"], f["sources"])
        r.cell(f["id"], "ID")
        r.cell(f["severity"], "Severity")
        r.cell(f["title"], "Flag")
        r.cell(f["detail"], "Detail")
        r.cell(f'<a href="{esc(f["page"])}">{esc(f["page"])}</a>', "Related page", html_value=True)
        r.sources()
        rows.append(r)

    blank_rows = []
    for b in BLANKS:
        r = Row(b["row"] + " · " + b["field"], b["sources"])
        r.cell(b["page"], "Page")
        r.cell(b["row"], "Row")
        r.cell(b["field"], "Blank field")
        r.sources()
        blank_rows.append(r)

    body = f"""
<div class="page-head"><h1>Flagged for review</h1><p>Needs-review treatment: a flag does not block the rest of the site. It records an irregularity, conflict or intentionally unverified value with its official sources.</p></div>
<div class="warning"><strong>{len(D["flags"])} irregularities / conflicts</strong> and <strong>{len(BLANKS)} blank fields</strong> are listed below. Blank cells are never filled with estimates.</div>
<h2 class="section-title">Irregularities &amp; conflicts</h2>
{table(["ID", "Severity", "Flag", "Detail", "Related page", "Official sources"], rows, "Flagged items")}
<h2 class="section-title">Every intentionally blank / unverified value</h2>
{table(["Page", "Row", "Blank field", "Official sources"], blank_rows, "Blank-value inventory")}
<div class="note"><a href="suggestions.html">← Suggestions</a> · <a href="sources.html">Sources →</a></div>
"""
    write_page("flagged", "Flagged for review", "Irregularities, conflicts and every unverified blank value", body)


def build_social():
    rows = []
    gaps = []
    for group_name, entries in [
        ("Detailed starred restaurant", D["michelin"]["detailed"]),
        ("Guide-listed restaurant", D["michelin"]["guide_listed"]),
        ("Activity", D["activities"]),
        ("Hotel", D["hotels"]),
    ]:
        for e in entries:
            socials = e.get("social", [])
            if not socials:
                r = Row(e["name"], e.get("sources", ["repo"]))
                r.cell(group_name, "Entry type")
                r.cell(e["name"], "Entry")
                r.cell("No verified social review link", "Gap")
                r.sources()
                gaps.append(r)
            for s in socials:
                if not s.get("url"):
                    continue
                r = Row(e["name"] + " · " + s.get("platform", ""), e.get("sources", ["repo"]))
                r.cell(group_name, "Entry type")
                r.cell(e["name"], "Entry")
                r.cell(s.get("platform", ""), "Platform")
                r.cell(s.get("title", ""), "Review / post")
                r.cell(s.get("kind", ""), "Type")
                r.cell(external(s["url"], "Open on platform", "chip social"), "Platform link", html_value=True)
                r.sources()
                rows.append(r)

    body = f"""
<div class="page-head"><h1>Social reviews</h1><p>YouTube, TikTok and Instagram links sit alongside entries. They are platform links, <strong>not</strong> official sources: every published row still carries an official source link in the last column.</p></div>
<div class="note"><strong>Verification rule:</strong> social URLs were obtained by fetching a platform page directly or via a site-restricted search of that platform's domain. Where no platform page could be confirmed, the cell is blank and flagged.</div>
<h2 class="section-title">Verified social links</h2>
{table(["Entry type", "Entry", "Platform", "Review / post", "Type", "Platform link", "Official sources"], rows, "All verified social review links")}
<h2 class="section-title">Coverage gaps</h2>
{table(["Entry type", "Entry", "Gap", "Official sources"], gaps, "Entries with no verified social review link")}
<div class="note"><a href="activities.html">← Activities</a> · <a href="sources.html">Sources →</a></div>
"""
    write_page("social", "Social reviews", "YouTube, TikTok and Instagram review links alongside official sources", body)


def build_sources():
    rows = []
    for key, s in sorted(S.items()):
        r = Row(key, [key], [{"url": s["url"], "label": "Open official source", "note": s["type"]}])
        r.cell(f'<a id="source-{esc(key)}" href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(key)}</a>', "ID", html_value=True)
        r.cell(s["title"], "Source")
        r.cell(s["type"], "Type")
        r.cell(s["checked"], "Checked")
        r.cell(external(s["url"], "Open official page", "chip official"), "URL", html_value=True)
        r.sources()
        rows.append(r)
    body = f"""
<div class="page-head"><h1>Official source registry</h1><p>{len(S)} official / government / venue / platform sources, each fetched or site-restricted-searched and checked on {CHECKED}. This is the manual-review link index for the whole deliverable.</p></div>
{table(["ID", "Source", "Type", "Checked", "URL", "Official sources"], rows, "All sources used by the site")}
<div class="note"><a href="flagged.html">← Flagged</a> · <a href="verification.html">Verification →</a></div>
"""
    write_page("sources", "Sources", "Complete official source registry for manual review", body)


def build_verification():
    v = D["verification"]
    rules = "".join(f"<li>{esc(r)}</li>" for r in v["rules"])
    rows = []
    for i, c in enumerate(v["checks"], 1):
        r = Row(f"V{i:02d}", c.get("sources", ["repo"]))
        r.cell(c["check"], "Verification check")
        r.cell(c["result"], "Result")
        r.sources()
        rows.append(r)
    body = f"""
<div class="page-head"><h1>Verification</h1><p>Line-by-line verification rules and checks performed on {esc(v["checked"])}.</p></div>
<div class="card"><h2>Verification rules</h2><ol>{rules}</ol></div>
<h2 class="section-title">Checks performed</h2>
{table(["Verification check", "Result", "Official sources"], rows, "Verification log")}
<div class="success"><strong>Automated build check:</strong> <a href="verification-report.txt">verification-report.txt</a> records internal-link resolution, official-source coverage on every data row, blank-value inventory and build status.</div>
<div class="note"><a href="sources.html">← Sources</a> · <a href="review.html">Repo review →</a></div>
"""
    write_page("verification", "Verification", "Line-by-line verification log and automated build report", body)


def build_review():
    rr = D["repo_review"]
    rows = []
    for i, f in enumerate(rr["findings"], 1):
        r = Row(f"R{i:02d}", f.get("sources", ["repo"]))
        r.cell(f["item"], "Item")
        r.cell(f["verified"], "Verified")
        r.cell(f["irregularity"], "Irregularity / finding")
        r.cell(f["source"], "Review source")
        r.sources()
        rows.append(r)
    body = f"""
<div class="page-head"><h1>Repository review</h1><p>Line-by-line review of the repository and parallel-session coordination, with irregularities flagged for manual review. Baseline commit: <code>{esc(rr["baseline_commit"])}</code>.</p></div>
<div class="warning"><strong>No hallucinations:</strong> prior repository claims were not carried over. All factual rows on this site were rebuilt against the official sources in the <a href="sources.html">source registry</a>.</div>
{table(["Item", "Verified", "Irregularity / finding", "Review source", "Official sources"], rows, "Repo review findings")}
<div class="card"><h2>Manual review links</h2><ul class="plain-list">
<li><a href="sources.html">Official source registry</a> — direct links for every row</li>
<li><a href="verification.html">Verification log</a> — rules and checks</li>
<li><a href="flagged.html">Flagged for review</a> — irregularities and every blank value</li>
<li><a href="verification-report.txt">Automated build report</a></li>
</ul></div>
<div class="note"><a href="verification.html">← Verification</a> · <a href="index.html">Overview →</a></div>
"""
    write_page("review", "Repo review", "Line-by-line repository review and irregularities", body)


# ---------------------------------------------------------------------------
# Root Markdown deliverables
# ---------------------------------------------------------------------------
def md_escape(value) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(headers, rows) -> str:
    head = "| " + " | ".join(md_escape(h) for h in headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = "\n".join("| " + " | ".join(md_escape(c) for c in row) + " |" for row in rows)
    return head + "\n" + sep + "\n" + body + "\n"


def build_markdown():
    es = D["executive_summary"]
    (ROOT / "EXECUTIVE_SUMMARY.md").write_text(
        "# Executive summary\n\n"
        f"Checked {CHECKED}. {md_escape(es['headline'])}\n\n"
        "Full dashboard: [`docs/index.html`](docs/index.html).\n\n"
        "## Important details\n\n"
        + md_table(["Topic", "Finding", "Sources"],
                   [[k["title"], k["text"], ", ".join(k.get("sources", []))] for k in es["key_points"]])
        + "\n## Decision gates\n\n"
        + md_table(["Gate", "Status", "Blocking"],
                   [[g["gate"], g["status"], ", ".join(g["blocking"])] for g in es["decision_gates"]])
        + "\n## Verified numbers\n\n"
        + md_table(["Metric", "Value"],
                   [[k.replace("_", " ").title(), v] for k, v in es["verified_numbers"].items()])
        + "\nSee [`docs/executive-summary.html`](docs/executive-summary.html) for source links on every row.\n",
        encoding="utf-8",
    )

    (ROOT / "QUESTIONS.md").write_text(
        "# Questions, information and answers\n\n"
        f"Checked {CHECKED}. Full dashboard: [`docs/questions.html`](docs/questions.html).\n\n"
        + md_table(["ID", "Question", "Answer", "Missing", "Discover", "Blocks", "Sources"],
                   [[q["id"], q["question"], q["answer"], q["missing"], q["discover"],
                     "Yes" if q["blocks_decision"] else "No", ", ".join(q["sources"])] for q in D["questions"]])
        + "\nNo unanswered value was filled with an estimate.\n",
        encoding="utf-8",
    )

    (ROOT / "SUGGESTIONS.md").write_text(
        "# Suggestions — review before implementation\n\n"
        f"Checked {CHECKED}. Full dashboard with path chooser: [`docs/suggestions.html`](docs/suggestions.html).\n\n"
        + md_table(["ID", "Suggestion", "Problem", "Proposal", "Decision needed", "Effort", "Priority", "Status"],
                   [[s["id"], s["title"], s["problem"], s["proposal"], s["decision_needed"],
                     s["effort"], s["priority"], s["status"]] for s in D["suggestions"]])
        + "\nThese are proposals only; no path has been implemented before review.\n",
        encoding="utf-8",
    )

    (ROOT / "SOURCES.md").write_text(
        "# Official source registry\n\n"
        f"Checked {CHECKED}. Full linked registry: [`docs/sources.html`](docs/sources.html).\n\n"
        + md_table(["ID", "Title", "Type", "Checked", "URL"],
                   [[k, s["title"], s["type"], s["checked"], s["url"]] for k, s in sorted(S.items())])
        + "\nSocial-platform links are catalogued separately on [`docs/social.html`](docs/social.html); they never replace an official source.\n",
        encoding="utf-8",
    )

    v = D["verification"]
    (ROOT / "VERIFICATION.md").write_text(
        "# Verification\n\n"
        f"Checked {CHECKED}. Full verification page: [`docs/verification.html`](docs/verification.html). "
        "Automated report: [`docs/verification-report.txt`](docs/verification-report.txt).\n\n"
        "## Rules\n\n" + "".join(f"- {md_escape(r)}\n" for r in v["rules"])
        + "\n## Checks\n\n"
        + md_table(["Check", "Result", "Sources"],
                   [[c["check"], c["result"], ", ".join(c.get("sources", []))] for c in v["checks"]])
        + "\nEvery table row on the site carries at least one official source link; blank values are rendered as unverified and listed on the Flagged for Review page.\n",
        encoding="utf-8",
    )

    rr = D["repo_review"]
    (ROOT / "REVIEW.md").write_text(
        "# Repository review\n\n"
        f"Checked {CHECKED}. Baseline commit `{rr['baseline_commit']}`. "
        "Full review page: [`docs/review.html`](docs/review.html).\n\n"
        + md_table(["Item", "Verified", "Irregularity", "Source"],
                   [[f["item"], f["verified"], f["irregularity"], f["source"]] for f in rr["findings"]])
        + "\n## Flagged for review\n\n"
        + md_table(["ID", "Severity", "Title", "Detail"],
                   [[f["id"], f["severity"], f["title"], f["detail"]] for f in D["flags"]])
        + "\nSee [`docs/flagged.html`](docs/flagged.html) for official source links and the complete blank-value inventory.\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------
HREF_RE = re.compile(r'href="([^"]+)"', re.I)
ID_RE = re.compile(r'id="([^"]+)"', re.I)
ROW_RE = re.compile(r'<tr class="data-row[^"]*".*?</tr>', re.I | re.S)
OFFICIAL_RE = re.compile(r'class="[^"]*\bofficial\b', re.I)


def collect_html_files():
    files = []
    for p in ROOT.rglob("*.html"):
        if any(part in {".git", "data", "tools", "__pycache__", "node_modules"} for part in p.parts):
            continue
        files.append(p)
    return sorted(files)


def verify_site() -> int:
    files = collect_html_files()
    report_path = DOCS / "verification-report.txt"
    blank_inventory = DATA / "blank_fields.json"
    if blank_inventory.exists():
        saved = json.loads(blank_inventory.read_text(encoding="utf-8"))
        blank_count = len(saved.get("fields", []))
        blank_source = "saved build inventory"
    else:
        blank_count = len(BLANKS)
        blank_source = "current build inventory"
    ids_by_file = {}
    for p in files:
        text = p.read_text(encoding="utf-8")
        ids_by_file[p.resolve()] = set(ID_RE.findall(text))

    broken = []
    checked_links = 0
    for p in files:
        text = p.read_text(encoding="utf-8")
        local_ids = ids_by_file[p.resolve()]
        for href in HREF_RE.findall(text):
            href = html.unescape(href)
            if not href or href.startswith("#"):
                if href and href[1:] not in local_ids:
                    broken.append(f"{p.relative_to(ROOT)}: missing anchor {href}")
                continue
            if href.startswith(("http://", "https://", "mailto:", "tel:", "//", "javascript:", "data:")):
                continue
            if href.startswith("/"):
                continue  # absolute site-root links are intentionally left to the Pages host
            checked_links += 1
            path_part, _, anchor = href.partition("#")
            target = (p.parent / path_part).resolve() if path_part else p.resolve()
            if not target.exists():
                broken.append(f"{p.relative_to(ROOT)}: missing file {href}")
                continue
            if anchor:
                target_ids = ids_by_file.get(target, set(ID_RE.findall(target.read_text(encoding="utf-8"))))
                if anchor not in target_ids:
                    broken.append(f"{p.relative_to(ROOT)}: missing anchor {href}")

    missing_official = []
    data_rows = 0
    official_links = 0
    for p in files:
        text = p.read_text(encoding="utf-8")
        official_links += len(re.findall(r'class="[^"]*\bofficial\b', text))
        for i, block in enumerate(ROW_RE.findall(text), 1):
            data_rows += 1
            if not OFFICIAL_RE.search(block):
                missing_official.append(f"{p.relative_to(ROOT)}: data row {i}")

    missing_sources = []
    for key in sorted(S):
        if not S[key].get("url"):
            missing_sources.append(key)

    status = "PASS" if not (broken or missing_official or missing_sources) else "FAIL"
    report = f"""NY 2027 trip dashboard — automated verification report
Checked: {CHECKED}
Status: {status}

Generated HTML files: {len(files)}
Internal links checked: {checked_links}
Broken internal links / anchors: {len(broken)}
Data table rows: {data_rows}
Rows missing an official-source link: {len(missing_official)}
Official source links rendered: {official_links}
Intentionally blank / unverified fields: {blank_count} ({blank_source})
Flagged irregularities: {len(D["flags"])}
Official sources in registry: {len(S)}
Sources missing a URL: {len(missing_sources)}

Rules enforced:
- Every table row has at least one official-source link.
- Blank values are rendered as "— unverified" and inventoried on Flagged for Review.
- No value is inferred, estimated, or taken from a third-party travel blog.
- Social links are platform links and never replace an official source.
- Weekday values are computed with Python datetime, not estimated.
- External official links are not HTTP-checked here; they were fetched during research.

"""
    if broken:
        report += "Broken internal links:\n" + "\n".join("  - " + x for x in broken) + "\n\n"
    if missing_official:
        report += "Rows missing official source:\n" + "\n".join("  - " + x for x in missing_official) + "\n\n"
    if missing_sources:
        report += "Sources missing URL:\n" + "\n".join("  - " + x for x in missing_sources) + "\n\n"
    report += "Generated pages:\n" + "\n".join("  - " + str(p.relative_to(ROOT)) for p in files) + "\n"

    report_path.write_text(report, encoding="utf-8")
    print(report)
    return 0 if status == "PASS" else 1


def build():
    DOCS.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    if not (ASSETS / "site.css").exists() or not (ASSETS / "site.js").exists():
        raise SystemExit("docs/assets/site.css and docs/assets/site.js must exist")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    BLANKS.clear()
    build_index()
    build_executive_summary()
    build_dates()
    build_hotels()
    build_michelin()
    build_restaurants()
    build_guide_listed()
    build_activities()
    build_travel()
    build_questions()
    build_suggestions()
    build_flagged()
    build_social()
    build_sources()
    build_verification()
    build_review()
    build_markdown()
    (DATA / "blank_fields.json").write_text(
        json.dumps({"checked": CHECKED, "fields": BLANKS}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Built {len(NAV)} pages, {len(BLANKS)} blank-field records, {len(S)} sources.")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true", help="only verify existing files")
    args = parser.parse_args(argv)
    if not args.verify_only:
        build()
    return verify_site()


if __name__ == "__main__":
    sys.exit(main())
