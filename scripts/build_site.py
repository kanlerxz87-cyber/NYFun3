#!/usr/bin/env python3
"""Deterministic static site generator for the NYC Feb–Mar 2027 Couple Vacation Dashboard.

Reads verified JSON datasets in ./data/ and outputs clean, mobile-friendly,
GitHub Pages–compatible static HTML pages at the repository root.
"""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


def load_json(name: str) -> dict:
    with open(DATA_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)


def esc(val: object) -> str:
    return html.escape(str(val or ""), quote=True)


def render_shell(active_slug: str, title: str, body_html: str, irreg_count: int) -> str:
    nav_items = [
        ("index.html", "overview", "Overview & Summary", None),
        ("hotels.html", "hotels", "Hotels (7-Night)", "8"),
        ("michelin.html", "michelin", "MICHELIN Dining", "26"),
        ("activities.html", "activities", "Activities", "16"),
        ("questions.html", "questions", "Questions & Missing Info", "6"),
        ("suggestions.html", "suggestions", "Suggestions", "6"),
        ("review.html", "review", "Flagged Review", str(irreg_count)),
    ]
    nav_links = []
    for href, slug, label, count in nav_items:
        cls = ["nav-link"]
        if slug == active_slug:
            cls.append("active")
        if slug == "review":
            cls.append("flag-nav")
        badge = f' <span class="nav-count">{esc(count)}</span>' if count else ""
        nav_links.append(f'<a class="{" ".join(cls)}" href="./{href}">{esc(label)}{badge}</a>')

    nav_str = "\n        ".join(nav_links)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} | NYC Couple Vacation Planner (Feb–Mar 2027)</title>
  <meta name="description" content="Line-by-line verified NYC vacation analysis for two adults (Feb 15 – Mar 23, 2027): 7-night hotels ranked by MICHELIN subway reachability, MICHELIN stars vs. Guide listings, activities, and social reviews.">
  <link rel="stylesheet" href="./assets/styles.css">
</head>
<body>
  <div class="top-banner">
    <strong>2027 Verification Audit Active:</strong> Every figure verified from official primary sources (Nov 25, 2026). Unconfirmed fields are left blank &amp; logged on <a href="./review.html">Flagged Review ({irreg_count})</a>.
  </div>
  <header class="site-header">
    <div class="header-inner">
      <a class="brand" href="./index.html">
        <span class="brand-mark">NY</span>
        <span>
          NYC 2027 Couple's Planner
          <span class="brand-sub">Feb 15 – Mar 23, 2027 · Verified Primary-Source Edition</span>
        </span>
      </a>
      <nav class="site-nav" aria-label="Primary Navigation">
        {nav_str}
      </nav>
    </div>
  </header>
  <main class="container">
{body_html}
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      <div>
        <strong>NYC Couple's Vacation Analysis &amp; Verified Reference Dashboard</strong><br>
        Window: Feb 15 – Mar 23, 2027 · Party: 2 Adults (Private Bath + Queen/King Bed · Standardized 7-Night Hotel Stays · &le;60-Min MTA Transit Rule)
      </div>
      <div>
        <a href="./COORDINATION.md">COORDINATION.md</a> ·
        <a href="./review.html">14 Flagged Irregularities &amp; Unverified Log</a> ·
        <a href="./suggestions.html">Reviewable Suggestions</a>
      </div>
    </div>
  </footer>
  <script src="./assets/app.js" defer></script>
</body>
</html>
"""


def render_social_cell(social: dict) -> str:
    chips = []
    for i, item in enumerate(social.get("youtube", []), 1):
        chips.append(
            f'<a class="chip-link chip-yt" href="{esc(item["url"])}" target="_blank" rel="noopener" title="{esc(item["label"])}">▶ YT {i}: {esc(item["label"][:34])}{"…" if len(item["label"]) > 34 else ""}</a>'
        )
    for i, item in enumerate(social.get("tiktok", []), 1):
        chips.append(
            f'<a class="chip-link chip-tt" href="{esc(item["url"])}" target="_blank" rel="noopener" title="{esc(item["label"])}">♪ TikTok {i}: {esc(item["label"][:30])}{"…" if len(item["label"]) > 30 else ""}</a>'
        )
    for i, item in enumerate(social.get("instagram", []), 1):
        chips.append(
            f'<a class="chip-link chip-ig" href="{esc(item["url"])}" target="_blank" rel="noopener" title="{esc(item["label"])}">◎ IG: {esc(item["label"][:30])}{"…" if len(item["label"]) > 30 else ""}</a>'
        )
    missing = []
    if not social.get("youtube"):
        missing.append("YT")
    if not social.get("tiktok"):
        missing.append("TikTok")
    if not social.get("instagram"):
        missing.append("IG")
    note = ""
    if missing:
        note = f'<div class="empty-cell" style="margin-top:4px;">Unconfirmed left blank: {", ".join(missing)}</div>'
    if not chips:
        return '<span class="empty-cell">— (Unverified)</span>'
    return f'<div class="link-group">{"".join(chips)}</div>{note}'


def michelin_badge(r: dict) -> str:
    st = r["michelin_status"]
    if st.startswith("3 "):
        return '<span class="badge badge-3star">★★★ 3 MICHELIN Stars</span><div class="venue-meta" style="margin-top:4px;font-weight:600;color:#991b1b;">Starred Restaurant</div>'
    if st.startswith("2 "):
        return '<span class="badge badge-2star">★★ 2 MICHELIN Stars</span><div class="venue-meta" style="margin-top:4px;font-weight:600;color:#b91c1c;">Starred Restaurant</div>'
    if st.startswith("1 "):
        extra = " + Green ★" if "Green" in st else ""
        return f'<span class="badge badge-1star">★ 1 MICHELIN Star{extra}</span><div class="venue-meta" style="margin-top:4px;font-weight:600;color:#991b1b;">Starred Restaurant</div>'
    if "Bib Gourmand" in st:
        return '<span class="badge badge-bib">Bib Gourmand (No Star)</span><div class="venue-meta" style="margin-top:4px;">Listed in MICHELIN Guide Only</div>'
    return '<span class="badge badge-selected">MICHELIN Selected (No Star)</span><div class="venue-meta" style="margin-top:4px;">Listed in MICHELIN Guide Only</div>'


def build_index(audit: dict, hotels: dict, michelin: dict, activities: dict, dec: dict) -> str:
    es = dec["executive_summary"]
    findings_li = "".join(f"<li>{esc(f)}</li>" for f in es["core_findings"])

    top3_cards = []
    for h in hotels["hotels"][:3]:
        top3_cards.append(f"""
        <div class="card">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:8px;">
            <span class="badge badge-rank">Rank #{h['rank']} · {h['michelin_starred_and_bib_60min']} MICHELIN &le;60m</span>
            <span class="badge {'badge-nofee' if h['mandatory_resort_fee_per_night'].startswith('$0 ') else 'badge-warn'}">{'$0 Resort Fee' if h['mandatory_resort_fee_per_night'].startswith('$0 ') else 'Resort Fee Applies'}</span>
          </div>
          <div class="venue-name" style="font-size:16.5px;">{esc(h['name'])}</div>
          <div class="venue-meta" style="margin-bottom:10px;">{esc(h['neighborhood'])} · {esc(h['compliant_room_type'])}</div>
          <div style="font-size:13.5px;margin-bottom:8px;"><strong>7-Night Total:</strong> {esc(h['seven_night_total_feb_preferred'])}</div>
          <div style="font-size:13px;color:var(--text-muted);margin-bottom:12px;"><strong>Walkable Starred:</strong> {esc(h['michelin_walkable_15min'])}</div>
          <div class="link-group">
            <a class="chip-link chip-official" href="{esc(h['official_url'])}" target="_blank" rel="noopener">Official Hotel Site ↗</a>
            <a class="chip-link" href="./hotels.html">Full Comparison →</a>
          </div>
        </div>""")

    return f"""
    <section class="hero">
      <div class="hero-eyebrow">★ Executive Summary · Couple Trip (2 Adults)</div>
      <h1>New York City Vacation Master Plan (Feb 15 – Mar 23, 2027)</h1>
      <p>Every hotel rate, room specification (Private Bathroom + Queen/King Bed), MTA &le;60-minute transit threshold, MICHELIN distinction, couple meal total, operating schedule, and social review link below has been verified line-by-line from official primary sources.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="./hotels.html">Compare 7-Night Hotels (#1–#8) →</a>
        <a class="btn btn-secondary" href="./michelin.html">Explore 26 MICHELIN Venues &amp; Clusters</a>
        <a class="btn btn-secondary" href="./activities.html">16 Winter-Smart Activities</a>
        <a class="btn btn-secondary" href="./questions.html">6 Pre-Booking Questions</a>
        <a class="btn btn-secondary" href="./suggestions.html">Reviewable Suggestions</a>
        <a class="btn btn-secondary" href="./review.html">14 Flagged Irregularities</a>
      </div>
    </section>

    <section class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">Sweet-Spot 7-Night Dates</div>
        <div class="kpi-value">Feb 21–28, 2027</div>
        <div class="kpi-sub">Dodges Presidents' Day + NYC School Recess (Feb 15–19) &amp; avoids +28%–57% March hotel jump</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">#1 Transit &amp; $0-Fee Hotel</div>
        <div class="kpi-value">LUMA Bryant Park</div>
        <div class="kpi-sub">70/70 NYC Starred + 78 Bib (&le;60m MTA) · Best 4★ deal: Arlo Midtown ($1,095/7n)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Active NYC MICHELIN Census</div>
        <div class="kpi-value">70 Starred + 84 Bib</div>
        <div class="kpi-sub">5 Three-Star · 14 Two-Star · 51 One-Star in NYC (Dec 14, 2026 Ceremony flagged!)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Verified MTA 7-Day Transit</div>
        <div class="kpi-value">$70.00 / Couple</div>
        <div class="kpi-sub">$3.00 OMNY fare capped at $35.00/pp per 7 days (each adult taps own card/phone)</div>
      </div>
    </section>

    <section class="section">
      <div class="card">
        <h2 class="section-title" style="margin-bottom:10px;">Executive Summary: Key Verified Findings</h2>
        <ul class="clean-list">
          {findings_li}
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="callout danger">
        <strong>Critical 2027 Schedule &amp; Prompt Irregularities Caught During Verification:</strong>
        (1) <strong>The Metropolitan Opera</strong> has ZERO performances from <strong>Jan 31 – Mar 7, 2027</strong> (reopens Mar 8);
        (2) <strong>Wollman Rink</strong> closes for the season on <strong>March 16, 2027</strong>;
        (3) <strong>Feb 15, 2027</strong> is Presidents' Day Monday (Sushi Sho, Jungsik, Jean-Georges, Dirt Candy, Aska, Morgan Library &amp; Hadestown are CLOSED Mondays) and starts NYC Schools Midwinter Recess;
        (4) Prompt mentions 3 nights (Feb 15–18), 7-night hotel baseline, and 1–4 weeks — see <a href="./questions.html">Questions &amp; Missing Info</a> and <a href="./review.html">Flagged Review</a>.
      </div>
    </section>

    <section class="section">
      <div class="section-header">
        <div>
          <h2 class="section-title">When to Go Inside Feb 15 – Mar 23, 2027: Verified Window Comparison</h2>
          <p class="section-subtitle">Comparing your preferred Feb 15–18 start against 7-night windows across February and March 2027.</p>
        </div>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Candidate Window</th>
              <th>Hotel Rate Level (7-Night Baseline)</th>
              <th>Crowd &amp; Holiday Impact</th>
              <th>Venue &amp; Seasonal Availability</th>
              <th>Verdict &amp; Official Source</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><div class="venue-name">Jan 19 – Feb 11, 2027</div><div class="venue-meta">4+ days BEFORE window</div></td>
              <td><span class="badge badge-nofee">Lowest (-25% Promo)</span></td>
              <td>Low post-holiday crowds</td>
              <td>Overlaps NYC Hotel Week (25% off), Restaurant Week &amp; 2-for-1 Broadway Week; Met Opera dark after Jan 30.</td>
              <td>Worth considering ONLY if dates are flexible · <a href="https://www.nyctourism.com/hotel-week/" target="_blank" rel="noopener">nyctourism.com ↗</a></td>
            </tr>
            <tr>
              <td><div class="venue-name">Feb 15 – Feb 22, 2027</div><div class="venue-meta">User Preferred Start (7n)</div></td>
              <td><span class="badge badge-verified">Low Feb Rates ($931–$2,680)</span></td>
              <td><span class="badge badge-warn">High Museum Crowds</span><br>Presidents' Day + NYC School Recess (Feb 15–19)</td>
              <td>Sushi Sho (open thru Feb 28 on Tock!), Broadway, Wollman Rink open; Mon Feb 15 fine-dining closures; Met Opera DARK.</td>
              <td>Strong hotel rates, but book museum timed slots early · <a href="https://www.schools.nyc.gov/calendar" target="_blank" rel="noopener">schools.nyc.gov ↗</a></td>
            </tr>
            <tr style="background:#f0fdf4;">
              <td><div class="venue-name">Feb 21 – Feb 28, 2027 ★</div><div class="venue-meta">Optimal Value &amp; Calm Week</div></td>
              <td><span class="badge badge-verified">Cheapest Window ($931–$2,350)</span></td>
              <td><span class="badge badge-nofee">Lightest Crowds</span><br>School break over; pre-spring rush</td>
              <td>Sushi Sho Tock open thru Feb 28! All museums, Broadway &amp; Wollman Rink open; Met Opera still dark.</td>
              <td><strong>#1 Recommended 7-Night Window</strong> · <a href="https://www.super.com/travel/hotels/arlo-midtown-new-york/lyD18NZW" target="_blank" rel="noopener">Verified Rate Table ↗</a></td>
            </tr>
            <tr>
              <td><div class="venue-name">Mar 8 – Mar 16, 2027</div><div class="venue-meta">Opera + Skating Overlap</div></td>
              <td><span class="badge badge-warn">+28% to +57% Higher</span><br>($1,337–$2,365+ Mar jump)</td>
              <td>Moderate early-spring crowds; Daylight Saving starts Mar 14</td>
              <td><strong>ONLY week</strong> where BOTH Met Opera (reopens Mar 8) AND Wollman Rink (closes Mar 16) are open!</td>
              <td>Best March week if Met Opera is a must-do · <a href="https://www.metopera.org/season/tickets/group-sales/extraordinary-every-night/2026-27/" target="_blank" rel="noopener">metopera.org ↗</a></td>
            </tr>
            <tr>
              <td><div class="venue-name">Mar 17 – Mar 23, 2027</div><div class="venue-meta">St. Patrick's / Early Spring</div></td>
              <td><span class="badge badge-warn">Higher Spring Rates</span></td>
              <td>St. Patrick's Parade Wed Mar 17 (5th Ave transit detours)</td>
              <td>Met Opera open (Silent Night, Aida, Manon); <strong>Wollman Rink CLOSED for season</strong> after Mar 16.</td>
              <td>Milder ~52°F highs, higher hotel spend · <a href="https://wollmanrinknyc.com/plan/" target="_blank" rel="noopener">wollmanrinknyc.com ↗</a></td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <div class="section-header">
        <div>
          <h2 class="section-title">7-Night Couple Total Budget Rollup (2 Adults, Excl. Flights)</h2>
          <p class="section-subtitle">Built strictly from verified 7-night hotel totals (taxes + mandatory resort fees included), MTA OMNY $35/pp cap, verified attraction tickets, and MICHELIN couple menus.</p>
        </div>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>7-Night Couple Budget Tier</th>
              <th>7-Night Hotel (w/ Taxes &amp; Fees)</th>
              <th>MTA Subway/Bus (7-Day OMNY Cap × 2)</th>
              <th>Activities (5–7 Iconic Sights for 2)</th>
              <th>MICHELIN &amp; NYC Dining (7 Days for 2)</th>
              <th>Estimated 7-Night Couple Total</th>
              <th>Primary Official Sources</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><div class="venue-name">Tier 1 — Smart Value Couple</div><div class="venue-meta">Hampton Inn Bklyn ($931) or Pod Queen ($980) or Arlo Midtown ($1,095)</div></td>
              <td>$931 – $1,218</td>
              <td>$70.00 exact<br><span class="venue-meta">($35/pp OMNY cap)</span></td>
              <td>$231 – $315<br><span class="venue-meta">Met $60 + MoMA $60 + Liberty $51 + SUMMIT $84 + Free High Line/Bridge/Ferry</span></td>
              <td>$950 – $1,350<br><span class="venue-meta">Cho Dang Gol $75, Katz's $80, Cote 1★ $216, Semma 1★ $190 + casual cafés</span></td>
              <td><strong>$2,182 – $2,953</strong></td>
              <td><a href="./hotels.html">Hotels</a> · <a href="https://www.mta.info/document/195636" target="_blank" rel="noopener">MTA Tariff ↗</a></td>
            </tr>
            <tr>
              <td><div class="venue-name">Tier 2 — Boutique Mid-Range</div><div class="venue-meta">Ace Medium Queen ($1,511), Hyatt Centric ($1,623), or citizenM ($1,778+)</div></td>
              <td>$1,511 – $2,051</td>
              <td>$70.00 exact</td>
              <td>$420 – $560<br><span class="venue-meta">+ Hadestown Broadway ($220), 9/11 Museum ($72), Morgan ($50), Wollman ($80)</span></td>
              <td>$1,650 – $2,250<br><span class="venue-meta">Le Bernardin 3★ Lunch ($355 all-in), Dirt Candy 1★ ($257), Le Pavillon 1★ ($374), Crown Shy 1★ ($230) + bistro meals</span></td>
              <td><strong>$3,651 – $4,931</strong></td>
              <td><a href="./michelin.html">MICHELIN</a> · <a href="./activities.html">Activities</a></td>
            </tr>
            <tr>
              <td><div class="venue-name">Tier 3 — MICHELIN Connoisseur</div><div class="venue-meta">LUMA Bryant Park ($2,265–$2,680)</div></td>
              <td>$2,265 – $2,680</td>
              <td>$70.00 OMNY<br><span class="venue-meta">(+$250–$400 late-night taxis)</span></td>
              <td>$650 – $950<br><span class="venue-meta">VIP Observatories + Orchestra Broadway/Opera + Private Museum Tours</span></td>
              <td>$3,100 – $4,900+<br><span class="venue-meta">Sushi Sho 3★ ($1,078) + Per Se 3★ ($925) + Atomix 2★ ($920) + Gabriel Kreuther 2★ ($650) + wine</span></td>
              <td><strong>$6,335 – $8,930+</strong></td>
              <td><a href="./michelin.html">26 Verified Menus →</a></td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <div class="section-header">
        <div>
          <h2 class="section-title">Top 3 Hotels by &le;60-Minute MICHELIN Subway/Bus Reachability</h2>
          <p class="section-subtitle">Preview of our 8 verified Queen/King + Private Bath properties — <a href="./hotels.html">view all 8 ranked hotels &amp; booking strategy →</a></p>
        </div>
      </div>
      <div class="grid-3">
        {"".join(top3_cards)}
      </div>
    </section>

    <section class="section">
      <div class="grid-2">
        <div class="card">
          <h3 style="margin-top:0;">Explore Category Subpages</h3>
          <ul class="clean-list">
            <li><a href="./hotels.html"><strong>Hotels &amp; 7-Night Pricing (hotels.html)</strong></a> — All 8 hotels ranked by &le;60-min MICHELIN reachability, resort-fee traps, and best time to book.</li>
            <li><a href="./michelin.html"><strong>MICHELIN Clusters &amp; 26 Restaurants (michelin.html)</strong></a> — 3★, 2★, 1★ vs. Bib Gourmand &amp; Selected (no star), couple totals, hours, and YT/TikTok/IG reviews.</li>
            <li><a href="./activities.html"><strong>16 Couple Activities (activities.html)</strong></a> — Official hours, 2027 seasonal closures, transit times, and social reviews.</li>
          </ul>
        </div>
        <div class="card">
          <h3 style="margin-top:0;">Decision Governance &amp; Review Queue</h3>
          <ul class="clean-list">
            <li><a href="./questions.html"><strong>Questions &amp; Missing Info (questions.html)</strong></a> — Knowns vs. unknowns, pre-booking questions, and how to discover missing answers.</li>
            <li><a href="./suggestions.html"><strong>Reviewable Suggestions (suggestions.html)</strong></a> — 6 high-impact proposals for site features &amp; booking strategy to review before changing.</li>
            <li><a href="./review.html"><strong>Flagged Irregularities (review.html)</strong></a> — 14 audited anomalies, room-type traps, and unverified blank fields.</li>
          </ul>
        </div>
      </div>
    </section>
    """


def build_hotels(hotels_data: dict) -> str:
    meta = hotels_data["metadata"]
    cs = meta["cheapest_upcoming_dates_summary"]
    rows = []
    for h in hotels_data["hotels"]:
        tags = ["all"]
        is_zero_fee = h["mandatory_resort_fee_per_night"].startswith("$0 ")
        if is_zero_fee:
            tags.append("nofee")
        if h["id"] in ("H03", "H06", "H07", "H08"):
            tags.append("under1400")
        if h["all_activities_within_60min"]:
            tags.append("allact60")

        fee_badge = (
            '<span class="badge badge-nofee">$0 Resort/Amenity Fee</span>'
            if is_zero_fee
            else f'<span class="badge badge-warn">{esc(h["mandatory_resort_fee_per_night"])}</span>'
        )
        act_badge = (
            f'<span class="badge badge-verified">16/16 &le;60m (Max {h["max_activity_transit_min"]}m)</span>'
            if h["all_activities_within_60min"]
            else f'<span class="badge badge-warn">15/16 &le;60m (Cloisters ~{h["max_activity_transit_min"]}m)</span>'
        )
        yt_chip = (
            f'<a class="chip-link chip-yt" href="{esc(h["review_youtube_url"])}" target="_blank" rel="noopener">▶ Room Tour YT</a>'
            if h.get("review_youtube_url")
            else ""
        )

        rows.append(f"""
            <tr data-tags="{','.join(tags)}">
              <td>
                <span class="badge badge-rank">#{h['rank']}</span>
                <div style="margin-top:6px;font-weight:800;color:var(--accent);font-size:15px;">{h['michelin_starred_and_bib_60min']} Total</div>
                <div class="venue-meta">{h['michelin_starred_60min']}/70 Starred + {h['michelin_starred_and_bib_60min'] - h['michelin_starred_60min']} Bib &le;60m</div>
              </td>
              <td>
                <div class="venue-name">{esc(h['name'])}</div>
                <div class="venue-meta">{esc(h['neighborhood'])} · {esc(h['address'])}</div>
                <div class="venue-meta" style="margin-top:4px;color:var(--emerald);font-weight:600;">{esc(h['tier'])}</div>
              </td>
              <td>
                <div><strong>{esc(h['compliant_room_type'])}</strong></div>
                <div class="venue-meta">✔ {esc(h['bed_verified'])} · ✔ {esc(h['private_bath_verified'])}</div>
                <div style="margin-top:5px;font-size:12px;color:#991b1b;background:#fef2f2;padding:4px 7px;border-radius:6px;">{esc(h['room_trap_warning'])}</div>
              </td>
              <td>
                <div style="font-weight:700;color:var(--text);">{esc(h['seven_night_total_feb_preferred'])}</div>
                <div style="margin-top:5px;font-size:12.5px;color:var(--emerald);"><strong>Cheapest Window:</strong> {esc(h['seven_night_cheapest_window'])}</div>
                <div style="margin-top:5px;">{fee_badge}</div>
                <div class="venue-meta" style="margin-top:4px;">{esc(h['pricing_source_note'])}</div>
              </td>
              <td>
                <div><strong>Walkable (&le;15m):</strong> {esc(h['michelin_walkable_15min'])}</div>
                <div style="margin-top:6px;">{act_badge}</div>
                <div class="venue-meta" style="margin-top:5px;"><strong>Subways:</strong> {esc(h['key_subways'])}</div>
              </td>
              <td>{esc(h['key_amenities'])}</td>
              <td>
                <div class="link-group">
                  <a class="chip-link chip-official" href="{esc(h['official_url'])}" target="_blank" rel="noopener">Official Site ↗</a>
                  <a class="chip-link chip-official" href="{esc(h['official_room_verify_url'])}" target="_blank" rel="noopener">Room Specs ↗</a>
                  <a class="chip-link" href="{esc(h['rate_verify_url'])}" target="_blank" rel="noopener">Rate/Fee Audit ↗</a>
                  {yt_chip}
                </div>
              </td>
            </tr>""")

    return f"""
    <section class="hero">
      <div class="hero-eyebrow">★ Task T4 · Standardized 7-Night Stay · Queen/King + Private Bath</div>
      <h1>NYC Hotels Ranked by &le;60-Minute MICHELIN Subway/Bus Reachability</h1>
      <p>All 8 hotels below are verified for two-adult occupancy with an en-suite <strong>private bathroom</strong> and a <strong>Queen or King bed</strong>, standardized to a <strong>7-night stay</strong> with NYC's 14.75% + $3.50/night tax and mandatory destination/resort fees explicitly itemized.</p>
    </section>

    <section class="section">
      <div class="grid-2">
        <div class="card">
          <h2 class="section-title" style="margin-bottom:8px;">Cheapest Upcoming Dates (Feb–Mar 2027)</h2>
          <p style="margin-top:0;"><strong>Sweet-Spot 7-Night Window: {esc(cs['cheapest_7_night_window_in_range'])}</strong></p>
          <ul class="clean-list">
            <li><strong>Why it wins:</strong> {esc(cs['why_cheapest'])}</li>
            <li><strong>Verified Feb vs. Mar price jump:</strong> Hyatt Centric jumps from <strong>$186/nt (Feb 2027)</strong> to <strong>$292/nt (Mar 2027)</strong> (+$742 on 7 nights); Arlo Midtown jumps from <strong>$113/nt</strong> to <strong>$158/nt</strong>; Hampton Inn Brooklyn jumps from <strong>$133/nt</strong> to <strong>$191/nt</strong>.</li>
            <li><strong>Adjacent Promo Note:</strong> {esc(cs['even_cheaper_adjacent_promo'])}</li>
          </ul>
        </div>
        <div class="card">
          <h2 class="section-title" style="margin-bottom:8px;">Best Time to Book &amp; Room-Spec Guardrails</h2>
          <ul class="clean-list">
            <li><strong>Two-Step Booking Strategy:</strong> {esc(cs['best_time_to_book'])}</li>
            <li><strong>NYC Tax Formula (<a href="https://legistar.council.nyc.gov/ViewReport.ashx?M=R&N=Master&GID=61&ID=6372562&GUID=B6E82CF7-D1D8-4A1A-BB26-EB1523DD819C&Extra=WithText&Title=Legislation+Details+%28With+Text%29" target="_blank" rel="noopener">NYC Local Law 2023/153 ↗</a>):</strong> 14.75% occupancy/sales/MCTD tax + $3.50/night flat unit fee ($24.50 per 7 nights), PLUS any hotel resort fee ($0 to $45.91/night).</li>
            <li><strong>Sub-Queen Room Traps Blocked:</strong> Never select Pod's <em>Full Pod</em> or <em>Bunk Pod</em>, Ace's <em>Single</em> or <em>Cozy</em>, or Arlo's <em>Twin Bunk</em> — book the exact compliant room category listed in Column 3!</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="filter-bar" data-target-table="hotels-table">
        <input class="filter-input" type="search" data-filter-search placeholder="Search hotel, neighborhood, subway line, amenity...">
        <div class="filter-pills">
          <button class="pill-btn active" type="button" data-filter-pill="all">All 8 Ranked</button>
          <button class="pill-btn" type="button" data-filter-pill="nofee">$0 Resort Fee (3)</button>
          <button class="pill-btn" type="button" data-filter-pill="under1400">Under $1,400 All-In (4)</button>
          <button class="pill-btn" type="button" data-filter-pill="allact60">100% Activities &le;60m (7)</button>
        </div>
        <div class="filter-count" data-filter-count>Showing 8 of 8 verified rows</div>
      </div>

      <div class="table-wrap">
        <table class="data-table" id="hotels-table">
          <thead>
            <tr>
              <th>MICHELIN &le;60m Rank</th>
              <th>Hotel &amp; Location</th>
              <th>Verified Queen/King + Private Bath &amp; Room Warnings</th>
              <th>Verified 7-Night Total (Feb 2027 vs. Cheapest / Mar)</th>
              <th>MICHELIN Walkability &amp; Activity Transit</th>
              <th>Key Couple Amenities</th>
              <th>Official &amp; Verification Links</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """


def build_michelin(m_data: dict) -> str:
    cluster_rows = []
    for c in m_data["clusters"]:
        notable = ", ".join(c["notable_starred"][:6]) + (
            f" (+{len(c['notable_starred']) - 6} more)" if len(c["notable_starred"]) > 6 else ""
        )
        cluster_rows.append(f"""
            <tr>
              <td><div class="venue-name">{esc(c['name'])}</div><div class="venue-meta">{esc(c['borough'])}</div></td>
              <td><strong>{c['three_star_count']}</strong></td>
              <td><strong>{c['two_star_count']}</strong></td>
              <td><strong>{c['one_star_count']}</strong></td>
              <td><span class="badge badge-2star">{c['total_starred_in_cluster']} Starred</span></td>
              <td>~{c['bib_gourmand_est_in_cluster']} Bib</td>
              <td><div class="venue-meta">{esc(c['key_subways'])}</div></td>
              <td><div style="font-size:12.5px;">{esc(notable)}</div></td>
              <td><a class="chip-link chip-michelin" href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurants" target="_blank" rel="noopener">MICHELIN Guide ↗</a></td>
            </tr>""")

    cluster_options = ['<option value="all">All 6 NYC MICHELIN Clusters</option>']
    for c in m_data["clusters"]:
        cluster_options.append(f'<option value="{esc(c["cluster_id"])}">{esc(c["name"])}</option>')

    r_rows = []
    for r in m_data["restaurants"]:
        tags = ["all"]
        st = r["michelin_status"]
        if r["has_star"]:
            tags.append("starred")
        else:
            tags.append("listed-nostar")
        if st.startswith("3 "):
            tags.append("3star")
        elif st.startswith("2 "):
            tags.append("2star")
        elif st.startswith("1 "):
            tags.append("1star")
        elif "Bib" in st:
            tags.append("bib")
        else:
            tags.append("selected")

        if "Closed Monday" not in r["days_open"] and "Closed Sunday & Monday" not in r["days_open"] and "Closed Monday & Tuesday" not in r["days_open"]:
            tags.append("monday-open")

        if r["pricing_verified"] and r["couple_total_price_display"]:
            price_cell = f"""
                <div style="font-weight:700;color:var(--text);">{esc(r['couple_total_price_display'])}</div>
                <div class="venue-meta" style="margin-top:4px;">{esc(r['couple_total_all_in_est'])}</div>
                <div style="margin-top:4px;"><span class="badge badge-verified">Verified Official Menu</span></div>"""
        else:
            price_cell = f"""
                <div class="empty-cell" style="font-weight:700;color:#b91c1c;">[Blank — Unverified on Official Site]</div>
                <div class="venue-meta" style="margin-top:4px;">{esc(r['couple_total_all_in_est'])}</div>
                <div style="margin-top:4px;"><a href="./review.html" class="badge badge-unverified">Flagged Unverified (IRREG-10)</a></div>"""

        r_rows.append(f"""
            <tr data-tags="{','.join(tags)}" data-cluster="{esc(r['cluster_id'])}">
              <td>
                <div class="venue-name">{esc(r['name'])}</div>
                <div class="venue-meta">{esc(r['neighborhood'])} · {esc(r['cuisine'])}</div>
                <div class="venue-meta">{esc(r['address'])}</div>
              </td>
              <td>{michelin_badge(r)}</td>
              <td>{price_cell}</td>
              <td>
                <div style="font-weight:600;">{esc(r['days_open'])}</div>
                <div style="font-size:12.5px;margin-top:3px;">{esc(r['hours'])}</div>
              </td>
              <td><div style="font-size:12.5px;">{esc(r['exceptions'])}</div></td>
              <td>
                <div class="link-group">
                  <a class="chip-link chip-official" href="{esc(r['official_url'])}" target="_blank" rel="noopener">Official Site ↗</a>
                  <a class="chip-link chip-official" href="{esc(r['official_verify_url'])}" target="_blank" rel="noopener">Menu/Hours Proof ↗</a>
                  <a class="chip-link chip-michelin" href="{esc(r['michelin_url'])}" target="_blank" rel="noopener">MICHELIN Page ↗</a>
                </div>
              </td>
              <td>{render_social_cell(r['social_reviews'])}</td>
            </tr>""")

    mon_open_count = sum(
        1
        for r in m_data["restaurants"]
        if "Closed Monday" not in r["days_open"]
        and "Closed Sunday & Monday" not in r["days_open"]
        and "Closed Monday & Tuesday" not in r["days_open"]
    )
    starred_count = sum(1 for r in m_data["restaurants"] if r["has_star"])
    nostar_count = sum(1 for r in m_data["restaurants"] if not r["has_star"])

    return f"""
    <section class="hero">
      <div class="hero-eyebrow">★ Task T2 · 6 Geographic Clusters · 70 NYC Starred + Bib Gourmand &amp; Selected</div>
      <h1>MICHELIN-Starred vs. MICHELIN-Listed Restaurants in NYC</h1>
      <p>Every restaurant below clearly distinguishes between venues holding <strong>1, 2, or 3 MICHELIN Stars</strong> versus venues <strong>listed in the MICHELIN Guide without a star</strong> (Bib Gourmand &amp; MICHELIN Selected), alongside verified 2-adult total pricing, hours, exceptions, official links, and social reviews.</p>
    </section>

    <section class="section">
      <div class="callout warn">
        <strong>Ceremony &amp; Boundary Note:</strong> {esc(m_data['metadata']['upcoming_ceremony_note'])}
        Official ceremony source: <a href="{esc(m_data['metadata']['primary_ceremony_source'])}" target="_blank" rel="noopener">MICHELIN Guide Official Star List ↗</a>.
      </div>
    </section>

    <section class="section">
      <div class="section-header">
        <div>
          <h2 class="section-title">NYC MICHELIN Dining Clusters (All 70 Active NYC Starred Restaurants)</h2>
          <p class="section-subtitle">Used to compute exact &le;60-minute MTA subway/bus reachability for every hotel on <a href="./hotels.html">hotels.html</a>.</p>
        </div>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Cluster &amp; Borough</th>
              <th>3★</th>
              <th>2★</th>
              <th>1★</th>
              <th>Total Starred</th>
              <th>Bib Gourmand</th>
              <th>Subway Trunks</th>
              <th>Starred Venues in Cluster</th>
              <th>Official Directory</th>
            </tr>
          </thead>
          <tbody>
            {"".join(cluster_rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <div class="section-header">
        <div>
          <h2 class="section-title">26 Line-by-Line Verified MICHELIN Restaurants (Couple Cost, Hours &amp; Social Reviews)</h2>
          <p class="section-subtitle">Includes all 5 NYC Three-Star temples, 7 Two-Star standouts, 9 One-Star icons, 2 Bib Gourmand values, and 3 MICHELIN Selected institutions.</p>
        </div>
      </div>

      <div class="filter-bar" data-target-table="michelin-table">
        <input class="filter-input" type="search" data-filter-search placeholder="Search restaurant, cuisine, neighborhood, dish...">
        <select class="filter-select" data-filter-select aria-label="Filter by MICHELIN Cluster">
          {"".join(cluster_options)}
        </select>
        <div class="filter-pills">
          <button class="pill-btn active" type="button" data-filter-pill="all">All ({len(m_data['restaurants'])})</button>
          <button class="pill-btn" type="button" data-filter-pill="starred">Has MICHELIN Star ({starred_count})</button>
          <button class="pill-btn" type="button" data-filter-pill="listed-nostar">Guide Listed Only — No Star ({nostar_count})</button>
          <button class="pill-btn" type="button" data-filter-pill="3star">3★ (5)</button>
          <button class="pill-btn" type="button" data-filter-pill="2star">2★ (7)</button>
          <button class="pill-btn" type="button" data-filter-pill="1star">1★ (9)</button>
          <button class="pill-btn" type="button" data-filter-pill="bib">Bib Gourmand (2)</button>
          <button class="pill-btn" type="button" data-filter-pill="selected">Selected (3)</button>
          <button class="pill-btn" type="button" data-filter-pill="monday-open">Open Mondays / Feb 15 ({mon_open_count})</button>
        </div>
        <div class="filter-count" data-filter-count>Showing 26 of 26 verified rows</div>
      </div>

      <div class="table-wrap">
        <table class="data-table" id="michelin-table">
          <thead>
            <tr>
              <th>Restaurant &amp; Location</th>
              <th>MICHELIN Star vs. Guide Listed</th>
              <th>Total Cost for 2 Adults (Verified)</th>
              <th>Days Open &amp; Hours</th>
              <th>Exceptions, Dress Code &amp; Booking Drops</th>
              <th>Official Sources</th>
              <th>Verified Social Media Reviews (YT / TikTok / IG)</th>
            </tr>
          </thead>
          <tbody>
            {"".join(r_rows)}
          </tbody>
        </table>
      </div>
    </section>
    """


def build_activities(a_data: dict) -> str:
    rows = []
    all_tag_lists = []
    for a in a_data["activities"]:
        tags = ["all"]
        cat = a["category"]
        if "Indoor" in cat or a["id"] == "A06":
            tags.append("indoor")
        if "$0 Free" in a["couple_total_cost"] and a["id"] in ("A12", "A15", "A16", "A08"):
            tags.append("free")
        if "Museum" in cat:
            tags.append("museum")
        if "Observation" in cat:
            tags.append("deck")
        if "Performing Arts" in cat:
            tags.append("arts")
        if "Closed Wednesdays" not in a["days_open"]:
            tags.append("wed-open")
        if "Closed Mondays" not in a["days_open"]:
            tags.append("mon-open")
        all_tag_lists.append(tags)

        t_badge = (
            f'<span class="badge badge-verified">&le;60m All Hotels ({esc(a["transit_from_midtown_min"])})</span>'
            if a["within_60_min_all_ranked_hotels"]
            else f'<span class="badge badge-warn">{esc(a["transit_from_midtown_min"])} (Cloisters &gt;60m from Bklyn)</span>'
        )

        rows.append(f"""
            <tr data-tags="{','.join(tags)}">
              <td>
                <div class="venue-name">{esc(a['name'])}</div>
                <div class="venue-meta">{esc(a['category'])} · {esc(a['neighborhood'])}</div>
                <div class="venue-meta">{esc(a['address'])}</div>
              </td>
              <td>
                <div style="font-weight:700;">{esc(a['couple_total_cost'])}</div>
              </td>
              <td>
                <div style="font-weight:600;">{esc(a['days_open'])}</div>
                <div style="font-size:12.5px;margin-top:3px;">{esc(a['hours'])}</div>
              </td>
              <td>
                <div style="font-size:12.5px;">{esc(a['exceptions'])}</div>
              </td>
              <td>
                {t_badge}
                <div class="venue-meta" style="margin-top:5px;"><strong>Subway:</strong> {esc(a['nearest_subway'])}</div>
              </td>
              <td>
                <div class="link-group">
                  <a class="chip-link chip-official" href="{esc(a['official_url'])}" target="_blank" rel="noopener">Official Site ↗</a>
                  <a class="chip-link chip-official" href="{esc(a['official_tickets_url'])}" target="_blank" rel="noopener">Tickets/Hours ↗</a>
                </div>
              </td>
              <td>{render_social_cell(a['social_reviews'])}</td>
            </tr>""")

    def tc(slug: str) -> int:
        return sum(1 for tl in all_tag_lists if slug in tl)

    return f"""
    <section class="hero">
      <div class="hero-eyebrow">★ Task T3 · 16 Couple Activities · &le;60-Min Transit Verified</div>
      <h1>NYC Couple Activities, Official Hours, 2027 Exceptions &amp; Social Reviews</h1>
      <p>{esc(a_data['metadata']['winter_weather_note'])}</p>
    </section>

    <section class="section">
      <div class="callout danger">
        <strong>3 Must-Know 2027 Seasonal Closures Verified on Official Attraction Calendars:</strong><br>
        • <strong>The Metropolitan Opera (A10):</strong> Official 2026–27 schedule has <strong>NO OPERA PERFORMANCES Jan 31 – Mar 7, 2027</strong> (reopens Mon Mar 8, 2027).<br>
        • <strong>Wollman Rink Ice Skating (A14):</strong> Official 2026–27 season <strong>CLOSES March 16, 2027</strong> (unavailable Mar 17–23; closes 2:30 PM Mon &amp; Tue).<br>
        • <strong>Weekly Museum Closures:</strong> <strong>The Met &amp; Cloisters</strong> = Closed Wednesdays · <strong>Whitney Museum</strong> = Closed Tuesdays · <strong>9/11 Museum</strong> = Closed most winter Tuesdays · <strong>Morgan Library &amp; Hadestown</strong> = Closed Mondays.
      </div>
    </section>

    <section class="section">
      <div class="filter-bar" data-target-table="activities-table">
        <input class="filter-input" type="search" data-filter-search placeholder="Search museum, observatory, Broadway, park, subway...">
        <div class="filter-pills">
          <button class="pill-btn active" type="button" data-filter-pill="all">All ({tc('all')})</button>
          <button class="pill-btn" type="button" data-filter-pill="indoor">Indoor / Winter-Proof ({tc('indoor')})</button>
          <button class="pill-btn" type="button" data-filter-pill="museum">Museums ({tc('museum')})</button>
          <button class="pill-btn" type="button" data-filter-pill="deck">Observation Decks ({tc('deck')})</button>
          <button class="pill-btn" type="button" data-filter-pill="arts">Performing Arts ({tc('arts')})</button>
          <button class="pill-btn" type="button" data-filter-pill="free">Free / $0 Options ({tc('free')})</button>
          <button class="pill-btn" type="button" data-filter-pill="mon-open">Open Mondays / Feb 15 ({tc('mon-open')})</button>
          <button class="pill-btn" type="button" data-filter-pill="wed-open">Open Wednesdays ({tc('wed-open')})</button>
        </div>
        <div class="filter-count" data-filter-count>Showing 16 of 16 verified rows</div>
      </div>

      <div class="table-wrap">
        <table class="data-table" id="activities-table">
          <thead>
            <tr>
              <th>Activity &amp; Location</th>
              <th>Couple Total (2 Adults)</th>
              <th>Days Open &amp; Hours</th>
              <th>2027 Holiday &amp; Seasonal Exceptions</th>
              <th>MTA Transit (&le;60m Check)</th>
              <th>Official Links</th>
              <th>Verified Social Media Reviews (YT / TikTok / IG)</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """


def build_questions(dec: dict) -> str:
    known_li = "".join(f"<li>{esc(k)}</li>" for k in dec["known_vs_missing"]["known_confirmed"])
    miss_li = "".join(f"<li>{esc(m)}</li>" for m in dec["known_vs_missing"]["missing_unconfirmed"])

    q_rows = []
    for q in dec["decision_questions"]:
        q_rows.append(f"""
            <tr>
              <td><span class="badge badge-rank">{esc(q['id'])}</span><div class="venue-meta" style="margin-top:5px;">{esc(q['category'])}</div></td>
              <td><div class="venue-name">{esc(q['question'])}</div></td>
              <td>{esc(q['why_it_matters'])}</td>
              <td><span class="badge badge-warn">{esc(q['answer_needed_before'])}</span></td>
              <td>{esc(q['how_to_discover'])}</td>
            </tr>""")

    return f"""
    <section class="hero">
      <div class="hero-eyebrow">★ Task T5 · Decision Readiness &amp; Information Discovery</div>
      <h1>Questions, Known vs. Missing Information &amp; How to Discover Answers</h1>
      <p>Before locking non-refundable flights, hotel rates, or prepaid Tock tasting menus, review the confirmed baseline versus open unknowns below — along with concrete steps to resolve every open question.</p>
    </section>

    <section class="section">
      <div class="grid-2">
        <div class="card" style="border-top:4px solid var(--emerald);">
          <h2 class="section-title" style="margin-bottom:8px;">✔ Known &amp; Verified Baseline</h2>
          <ul class="clean-list">
            {known_li}
          </ul>
        </div>
        <div class="card" style="border-top:4px solid var(--amber);">
          <h2 class="section-title" style="margin-bottom:8px;">? Missing Information to Confirm Together</h2>
          <ul class="clean-list">
            {miss_li}
          </ul>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-header">
        <div>
          <h2 class="section-title">6 Decisions &amp; Answers Needed Before Booking</h2>
          <p class="section-subtitle">Ordered by reservation &amp; booking deadline urgency (Dec 2026 → Jan 1, 2027 → Late Jan 2027).</p>
        </div>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID &amp; Area</th>
              <th>Question to Answer Together</th>
              <th>Why It Changes Your Plan &amp; Budget</th>
              <th>Answer Needed Before</th>
              <th>How to Discover / Verify the Answer</th>
            </tr>
          </thead>
          <tbody>
            {"".join(q_rows)}
          </tbody>
        </table>
      </div>
    </section>
    """


def build_suggestions(dec: dict) -> str:
    cards = []
    for s in dec["reviewable_suggestions"]:
        is_site = "Site" in s["category"]
        badge_cls = "badge-verified" if not is_site else "badge-bib"
        cards.append(f"""
        <div class="card">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:10px;flex-wrap:wrap;">
            <span class="badge badge-rank">{esc(s['id'])} · {esc(s['category'])}</span>
            <span class="badge {badge_cls}">Impact: {esc(s['impact'])}</span>
          </div>
          <h3 style="margin:0 0 8px;font-size:17px;">{esc(s['title'])}</h3>
          <p style="margin:0 0 10px;"><strong>Proposed Action:</strong> {esc(s['proposal'])}</p>
          <div class="callout warn" style="margin-bottom:0;padding:10px 14px;font-size:13px;">
            <strong>Trade-Off to Review Before Approving:</strong> {esc(s['tradeoff_to_review'])}
          </div>
        </div>""")

    return f"""
    <section class="hero">
      <div class="hero-eyebrow">★ Staged for Couple Review · Zero Unapproved Scope Changes</div>
      <h1>Suggestions to Improve Decision-Making &amp; This Dashboard</h1>
      <p>Per your instructions, the 6 high-leverage recommendations below are presented cleanly for your review <strong>before</strong> altering your core booking rules or adding modeled calculators on top of verified tables.</p>
    </section>

    <section class="section">
      <div class="grid-2">
        {"".join(cards)}
      </div>
    </section>
    """


def build_review(dec: dict) -> str:
    rows = []
    for ir in dec["flagged_irregularities"]:
        sev = ir["severity"]
        s_badge = (
            '<span class="badge badge-unverified">High Priority</span>'
            if sev == "High"
            else ('<span class="badge badge-warn">Medium</span>' if sev == "Medium" else '<span class="badge badge-selected">Low / Info</span>')
        )
        rows.append(f"""
            <tr>
              <td><strong>{esc(ir['id'])}</strong><div style="margin-top:4px;">{s_badge}</div></td>
              <td><span class="badge badge-selected">{esc(ir['domain'])}</span></td>
              <td><div class="venue-name">{esc(ir['item'])}</div></td>
              <td>{esc(ir['finding'])}</td>
              <td>{esc(ir['action_taken'])}</td>
              <td><a class="chip-link chip-official" href="{esc(ir['official_source'])}" target="_blank" rel="noopener">Official Source ↗</a></td>
            </tr>""")

    return f"""
    <section class="hero">
      <div class="hero-eyebrow">★ Zero-Hallucination Governance · Manual Review Log</div>
      <h1>Flagged Irregularities, Schedule Traps &amp; Unverified Blank Fields</h1>
      <p>Every prompt ambiguity, 2027 holiday/hiatus collision, hotel room-size/fee trap, and unconfirmed official value (left blank rather than guessed) is logged below with its primary verification link.</p>
    </section>

    <section class="section">
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Flag ID</th>
              <th>Domain</th>
              <th>Irregularity / Unverified Item</th>
              <th>What Official Sources Showed</th>
              <th>How We Handled It</th>
              <th>Primary Verification Link</th>
            </tr>
          </thead>
          <tbody>
            {"".join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """


def build_readme() -> str:
    return """# NYFun3 — NYC Couple's Vacation Analysis & Verified Dashboard (Feb 15 – Mar 23, 2027)

Clean, mobile-friendly static reference dashboard planning and analyzing a **New York City vacation for two adults** between **February 15, 2027 and March 23, 2027**.

## Pages Published (GitHub Pages Ready)

- **[`index.html`](./index.html)** — Executive Summary, Optimal 2027 Travel Window Matrix (`Feb 21–28, 2027` sweet spot vs. `Feb 15–22` & `Mar 8–16`), 7-Night Couple Total Cost Rollup, and Top 3 Hotels preview.
- **[`hotels.html`](./hotels.html)** — 8 NYC hotels verified for **Private Bathroom + Queen/King Bed**, standardized to a **7-night stay** (itemizing NYC 14.75% + $3.50/night tax and mandatory destination fees), and ranked strictly by **MICHELIN restaurants reachable within <=60 minutes by MTA subway/bus**.
- **[`michelin.html`](./michelin.html)** — Citywide 6-Cluster Census (**70 active NYC Starred + 84 Bib Gourmand**) and **26 line-by-line verified MICHELIN Guide restaurants** distinguishing **3★ / 2★ / 1★ Starred** from **Guide-Listed Only (Bib Gourmand & Selected)**, with 2-adult total prices, hours, exceptions, official links, and YouTube/TikTok/Instagram reviews.
- **[`activities.html`](./activities.html)** — **16 winter-smart NYC couple activities** with verified 2-adult admission totals, hours, critical 2027 closures (*Met Opera dark Jan 31–Mar 7, 2027; Wollman Rink closes Mar 16, 2027*), <=60-minute transit checks, and social media reviews.
- **[`questions.html`](./questions.html)** — Confirmed Knowns vs. Missing Information, 6 pre-booking Decision Questions, and actionable discovery steps.
- **[`suggestions.html`](./suggestions.html)** — 6 staged, reviewable suggestions to improve couple decision-making and dashboard capabilities prior to making changes.
- **[`review.html`](./review.html)** — Master audit log of **14 Flagged Irregularities & Unverified Blank Fields** (`IRREG-01` through `IRREG-14`).

## Verification & Coordination Artifacts

- [`COORDINATION.md`](./COORDINATION.md) — Task board (`T1`–`T6`), owning session log, and irregularity notes.
- [`data/`](./data/) — Structured primary-source JSON datasets (`repo_audit.json`, `hotels.json`, `michelin_restaurants.json`, `activities.json`, `decision_and_suggestions.json`).
- [`scripts/build_site.py`](./scripts/build_site.py) & [`scripts/verify_site.py`](./scripts/verify_site.py) — Deterministic static HTML builder and automated zero-hallucination / link / constraint verifier.
"""


def main() -> None:
    audit = load_json("repo_audit.json")
    hotels = load_json("hotels.json")
    michelin = load_json("michelin_restaurants.json")
    activities = load_json("activities.json")
    dec = load_json("decision_and_suggestions.json")
    irreg_count = len(dec["flagged_irregularities"])

    pages = [
        ("index.html", "overview", "Executive Summary & Overview", build_index(audit, hotels, michelin, activities, dec)),
        ("hotels.html", "hotels", "Hotels Ranked by MICHELIN Subway Reachability (7-Night Stay)", build_hotels(hotels)),
        ("michelin.html", "michelin", "MICHELIN-Starred vs. Listed Restaurants & Clusters", build_michelin(michelin)),
        ("activities.html", "activities", "NYC Couple Activities, 2027 Hours & Social Reviews", build_activities(activities)),
        ("questions.html", "questions", "Questions, Known vs. Missing Info & Discovery", build_questions(dec)),
        ("suggestions.html", "suggestions", "Reviewable Suggestions for Site & Decisions", build_suggestions(dec)),
        ("review.html", "review", "Flagged Irregularities & Unverified Fields", build_review(dec)),
    ]

    for filename, slug, title, body in pages:
        out = render_shell(slug, title, body, irreg_count)
        (ROOT / filename).write_text(out, encoding="utf-8")
        print(f"Built {filename} ({len(out):,} bytes)")

    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    (ROOT / "README.md").write_text(build_readme(), encoding="utf-8")
    print("Built .nojekyll and README.md")


if __name__ == "__main__":
    main()
