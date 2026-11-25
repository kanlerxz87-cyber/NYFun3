#!/usr/bin/env python3
"""Build the static GitHub Pages dashboard from verified JSON data.

Every generated data row includes its source link. Blank values stay blank.
Run: python3 scripts/build_site.py
"""
import html
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
PAGES = ROOT / 'pages'
PAGES.mkdir(exist_ok=True)

MICHELIN = json.loads((DATA / 'michelin.json').read_text())
HOTELS = json.loads((DATA / 'hotels.json').read_text())
ACTIVITIES = json.loads((DATA / 'activities.json').read_text())

NAV = [
    ('index.html', 'Overview'),
    ('pages/executive-summary.html', 'Executive summary'),
    ('pages/hotels.html', 'Hotels'),
    ('pages/michelin.html', 'Michelin dining'),
    ('pages/activities.html', 'Activities + social'),
    ('pages/itinerary.html', 'Itinerary'),
    ('pages/questions.html', 'Questions'),
    ('pages/suggestions.html', 'Suggestions'),
    ('pages/flagged-for-review.html', 'Flagged for review'),
    ('pages/sources.html', 'Sources'),
]


def e(value):
    return html.escape(str(value if value is not None else ''), quote=True)


def cell(value, css=''):
    if value is None or value == '':
        return '<td class="blank">— <span class="sr-only">unverified / blank</span></td>'
    return '<td{}>{}</td>'.format(' class="%s"' % css if css else '', value)


def link(url, label='Source', cls=''):
    if not url:
        return '<span class="blank">—</span>'
    return '<a href="{}" target="_blank" rel="noopener noreferrer"{}>{}</a>'.format(
        e(url), ' class="%s"' % cls if cls else '', e(label))


def badge(text, kind='verified'):
    return '<span class="badge {}">{}</span>'.format(kind, e(text))


def header(active):
    items = []
    for href, label in NAV:
        cls = ' class="active" aria-current="page"' if href == active else ''
        items.append('<a href="{}"{}>{}</a>'.format(
            e(href if href.startswith('pages/') else href), cls, e(label)))
    # Resolve relative paths for subpages.
    if active.startswith('pages/'):
        resolved = []
        for href, label in NAV:
            target = href if href.startswith('pages/') else href
            target = target.replace('pages/', '', 1)
            if target == 'index.html':
                target = '../index.html'
            cls = ' class="active" aria-current="page"' if href == active else ''
            resolved.append('<a href="{}"{}>{}</a>'.format(e(target), cls, e(label)))
        items = resolved
    return '''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{home}">NYFun3 <span>New York trip planning dashboard</span></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main navigation">
{nav}
    </nav>
  </div>
</header>'''.format(home='index.html' if not active.startswith('pages/') else '../index.html', nav='\n'.join(items))


def footer():
    return '''<footer class="site-footer">
  Data captured 2026-11-25 from official sources. Blank values are unverified, not estimated.
  &nbsp;·&nbsp; <a href="https://github.com/kanlerxz87-cyber/NYFun3/blob/arena/99553b53-nyfun3/COORDINATION.md" target="_blank" rel="noopener noreferrer">Coordination board</a>
</footer>'''


def page(title, active, body, description=''):
    return '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{desc}">
  <title>{title} · NYFun3</title>
  <link rel="stylesheet" href="{css}">
</head>
<body>
{header}
<main id="main">
{body}
</main>
{footer}
<script src="{js}"></script>
</body>
</html>
'''.format(
        desc=e(description or title), title=e(title),
        css='assets/style.css' if not active.startswith('pages/') else '../assets/style.css',
        js='assets/app.js' if not active.startswith('pages/') else '../assets/app.js',
        header=header(active), body=body, footer=footer())


def write(path, content):
    (ROOT / path).write_text(content)
    print('wrote', path)


def filters(kind):
    if kind == 'michelin':
        buttons = [('all', 'All 19'), ('3 Stars', '3 stars (5)'), ('2 Stars', '2 stars (14)')]
    else:
        buttons = [('all', 'All')]
    html_buttons = ''.join(
        '<button type="button" data-filter-value="{}" class="{}">{}</button>'.format(
            e(v), 'active' if i == 0 else '', e(label)) for i, (v, label) in enumerate(buttons))
    return '<div class="filters">{}<input id="table-search" type="search" placeholder="Filter rows by text" aria-label="Filter rows by text"></div><div class="count" id="visible-count"></div>'.format(html_buttons)


# ------------------------------- Michelin ---------------------------------
def social_links(items):
    if not items:
        return '<span class="blank">Not verified</span>'
    out = []
    for s in items:
        kind = 'badge verified' if 'Official' in s['kind'] else 'badge third-party'
        out.append('<a href="{}" target="_blank" rel="noopener noreferrer">{}</a> <span class="{}">{}</span>'.format(
            e(s['url']), e(s['platform']), kind, e(s['kind'])))
    return '<div class="socials">{}</div>'.format('<br>'.join(out))


def michelin_table():
    rows = []
    for r in MICHELIN['restaurants']:
        tags = r['distinction'].lower().replace(' ', '-')
        third = ''
        if r.get('thirdPartyPrice'):
            third = '{} <span class="sub">{} — <a href="{}" target="_blank" rel="noopener noreferrer">review video</a>, not an official price</span>'.format(
                e(r['thirdPartyPrice']), e(r['thirdPartyPriceNote']), e(r['thirdPartyPriceSource']))
        rows.append('''<tr data-tags="{}">
  <td><strong>{}</strong><span class="sub">{}</span></td>
  <td><span class="badge star">{}</span></td>
  <td>{}</td>
  <td>{}{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}{}</td>
  <td><a href="{}" target="_blank" rel="noopener noreferrer">MICHELIN Guide</a></td>
</tr>'''.format(
            e(tags), e(r['name']), e(r['address']), e(r['distinction']), e(r['cuisine']),
            cell(r['address']),
            ('<span class="sub">Official site: {}</span>'.format(link(r['officialUrl'], 'Website')) if r['officialUrl'] else ''),
            cell(r['hours']), cell(r['exceptions']), cell(r['band']),
            '<span class="blank">Not verified</span>',
            cell(third), social_links(r['social']),
            ('<span class="sub">{}</span>'.format(e(r['flags'][0])) if r.get('flags') else ''),
            e(r['michelinUrl'])))
    head = ['Restaurant / address', 'Distinction', 'Cuisine', 'Address', 'Days + hours (Michelin)',
            'Exceptions', 'Michelin price band', 'Price for 2 (official)', 'Third-party reported price',
            'Social review links', 'Source (official)']
    return '<div class="table-wrap"><table data-filterable><thead><tr>{}</tr></thead><tbody>{}</tbody></table></div>'.format(
        ''.join('<th>{}</th>'.format(e(h)) for h in head), '\n'.join(rows))


def one_star_names_table():
    rows = []
    for i, name in enumerate(MICHELIN['oneStarNames'], 1):
        source = MICHELIN['oneStarNamesPage2'] if i >= 49 else MICHELIN['oneStarNamesSource']
        rows.append('<tr><td>#{}</td><td>{}</td><td>1 Star (awarded)</td><td><a href="{}" target="_blank" rel="noopener noreferrer">Official 1-star list</a></td></tr>'.format(
            i, e(name), e(source)))
    return '<div class="table-wrap"><table><thead><tr><th>#</th><th>Restaurant</th><th>Guide distinction</th><th>Source (official)</th></tr></thead><tbody>{}</tbody></table></div>'.format(''.join(rows))


# ------------------------------- Hotels -----------------------------------
def hotels_table():
    rows = []
    for h in HOTELS['hotels']:
        rows.append('''<tr data-tags="hotel">
  <td><strong>#{}</strong></td>
  <td><strong>{}</strong><span class="sub">{}</span></td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{} <span class="sub">same count for all Midtown candidates; not a door-to-door result</span></td>
  <td>{}</td>
  <td>{}{}</td>
  <td><a href="{}" target="_blank" rel="noopener noreferrer">Official site</a></td>
</tr>'''.format(
            e(h['rank']), e(h['name']), e(h['area']), cell(h['area']),
            cell(h['room']), cell(h['bathroom']), cell(h['amenities']),
            '<span class="blank">Not verified — dated Feb 2027 rate unavailable</span>',
            e(h['michelinCluster']),
            '<span class="blank">Not verified</span>',
            cell(h['promotion']),
            ('<span class="sub"><a href="{}" target="_blank" rel="noopener noreferrer">Offer terms</a>: {}</span>'.format(
                e(h['promotionUrl']), e(h['flags'][0])) if h.get('promotionUrl') and h.get('flags') else
             ('<span class="sub">{}</span>'.format(e(h['flags'][0])) if h.get('flags') else '')),
            e(h['officialUrl'])))
    head = ['Rank', 'Hotel', 'Area', 'Room / bed (verified)', 'Bathroom', 'Amenities',
            'Total for 7 nights (15–22 Feb 2027)', 'Michelin-starred addresses in Midtown band',
            'Travel ≤1 hour', 'Verified booking window / promotion', 'Source (official)']
    return '<div class="table-wrap"><table data-filterable><thead><tr>{}</tr></thead><tbody>{}</tbody></table></div>'.format(
        ''.join('<th>{}</th>'.format(e(x)) for x in head), '\n'.join(rows))


# ------------------------------ Activities --------------------------------
def activities_table():
    rows = []
    for a in ACTIVITIES['activities']:
        social = []
        for s in a['social']:
            social.append('<a href="{}" target="_blank" rel="noopener noreferrer">{}</a> <span class="badge {}">{}</span>'.format(
                e(s['url']), e(s['platform']),
                'verified' if 'Official' in s['kind'] else 'third-party', e(s['kind'])))
        rows.append('''<tr data-tags="activity">
  <td><strong>{}</strong></td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td>{}</td>
  <td><a href="{}" target="_blank" rel="noopener noreferrer">{}</a></td>
</tr>'''.format(
            e(a['name']), cell(a['area']), cell(a['daysHours']), cell(a['exceptions']),
            cell(a['costForTwo']), '<br>'.join(social) if social else '<span class="blank">Not verified</span>',
            ('<a href="{}" target="_blank" rel="noopener noreferrer">Booking</a>'.format(e(a['booking'])) if a['booking'] else '<span class="blank">—</span>'),
            '<span class="blank">Not verified</span>', e(a['source']),
            e(a['source'].split('/')[2])))
    head = ['Activity', 'Area', 'Days + hours', 'Exceptions', 'Cost for 2', 'Social links',
            'Booking', 'Travel ≤1 hour', 'Source (official)']
    return '<div class="table-wrap"><table data-filterable><thead><tr>{}</tr></thead><tbody>{}</tbody></table></div>'.format(
        ''.join('<th>{}</th>'.format(e(x)) for x in head), '\n'.join(rows))


# ------------------------------- Pages ------------------------------------
index_body = '''
<section class="hero">
  <span class="pill ok">Verified-source research dashboard</span>
  <h1>New York trip plan — two adults</h1>
  <p>Preferred dates: <strong>Monday 15 February 2027 to Thursday 18 February 2027</strong>, inside the
  requested 15 February – 23 March 2027 window. A seven-night comparison stay is
  <strong>15–22 February 2027</strong>. Built for a couple who wants Michelin dining, walkable Midtown
  bases, social-media context and source links on every row.</p>
  <p><a href="pages/executive-summary.html">Read the executive summary →</a></p>
</section>
<div class="cards">
  <div class="card"><h3>Starred restaurants</h3><div class="big">19</div><div class="small">5 three-star + 14 two-star, each with an official Michelin source link</div></div>
  <div class="card"><h3>Midtown dining cluster</h3><div class="big">12</div><div class="small">Starred addresses in the roughly 30th–60th St band (not a transit-time result)</div></div>
  <div class="card"><h3>Hotels compared</h3><div class="big">5</div><div class="small">Room/bath details verified; dated rates unavailable</div></div>
  <div class="card"><h3>Unverified items</h3><div class="big">Flagged</div><div class="small">No dated Feb 2027 hotel prices, transit times or TikTok links were invented</div></div>
</div>
<div class="grid-2">
  <section class="panel">
    <h2>Start here</h2>
    <ul>
      <li><a href="pages/hotels.html">Hotel ranking + booking windows</a></li>
      <li><a href="pages/michelin.html">Michelin stars, hours, prices and social reviews</a></li>
      <li><a href="pages/activities.html">Activities, opening days and social links</a></li>
      <li><a href="pages/itinerary.html">Four-day and seven-day outlines</a></li>
    </ul>
  </section>
  <section class="panel">
    <h2>Decision gates</h2>
    <ul>
      <li><a href="pages/questions.html">Questions that must be answered first</a></li>
      <li><a href="pages/suggestions.html">Improvement options — choose a path before implementing</a></li>
      <li><a href="pages/flagged-for-review.html">Flagged irregularities and missing values</a></li>
      <li><a href="pages/sources.html">Full official source list</a></li>
    </ul>
  </section>
</div>
<div class="note warn"><strong>Verification policy:</strong> every factual table row has an official source link.
If an official page did not confirm a value, the cell is blank and the item is flagged on the
<a href="pages/flagged-for-review.html">Flagged for Review</a> page. Third-party prices and reviews are labelled as such.</div>
'''
write('index.html', page('Overview', 'index.html', index_body,
                         'Verified-source New York trip planning dashboard for February 2027.'))

summary_body = '''
<h1>Executive summary</h1>
<p class="small">Prepared 2026-11-25. All dates and values below come from the linked official pages; gaps are flagged rather than filled.</p>

<section class="panel">
<h2>1. Trip frame</h2>
<ul>
  <li><strong>Preferred trip:</strong> Mon 15 Feb 2027 – Thu 18 Feb 2027 (3 nights). This is inside the requested window and avoids a Sunday/Monday-heavy restaurant schedule for the main evenings.</li>
  <li><strong>Seven-night comparison:</strong> Mon 15 Feb – Mon 22 Feb 2027, used because the request asks for hotel costs as a seven-night total.</li>
  <li><strong>Widest allowed window:</strong> 15 Feb – 23 Mar 2027 (1–4 weeks). No dated pricing for any of these dates was available from official booking pages at capture time.</li>
</ul>
</section>

<section class="panel">
<h2>2. Michelin dining picture</h2>
<ul>
  <li>The official Michelin Guide filter panel for New York City shows <strong>5 three-star, 14 two-star, 50 one-star, 76 Bib Gourmand and 224 selected restaurants</strong> (<a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/3-stars-michelin" target="_blank" rel="noopener noreferrer">source</a>).</li>
  <li>All <strong>19 starred restaurants</strong> are listed on the <a href="michelin.html">Michelin dining page</a> with distinction, address, days/hours, price band, social links and a direct Michelin source link.</li>
  <li><strong>12 of the 19</strong> have verified street addresses in Manhattan's roughly 30th–60th Street band, which is the densest cluster for a Midtown base. This is an address-based count, not a verified one-hour travel-time calculation.</li>
  <li>All <strong>50 one-star names</strong> were captured from pages 1 and 2 of the official listing; names only, no unverified details were added.</li>
</ul>
</section>

<section class="panel">
<h2>3. Hotels and money</h2>
<ul>
  <li>Five Midtown candidates were checked against their own brand pages for room size/bed, bathroom and amenities; see <a href="hotels.html">Hotels</a>.</li>
  <li><strong>No official dated rate for February 2027 could be verified.</strong> Nightly rates and seven-night totals are therefore blank on the site. The cheapest date cannot be named without dated rates.</li>
  <li>The Michelin Guide hotel booking interface states bookings cannot be made more than 31 days ahead; 15 Feb 2027 was 82 days away at capture.</li>
  <li>Two verified booking windows are worth watching: <a href="https://www.hyatt.com/hyatt-centric/en-US/nycts-hyatt-centric-times-square/offers" target="_blank" rel="noopener noreferrer">World of Hyatt members save up to 25%</a> for qualifying stays 31 Oct 2026–30 Apr 2027, book by 8 Dec 2026; and a <a href="https://www.marriott.com/en-us/hotels/nycts-towneplace-suites-new-york-manhattan-times-square/overview/" target="_blank" rel="noopener noreferrer">Marriott Cyber Sale</a> for 25% off stays 29 Nov 2026–2 May 2027 (terms apply to both).</li>
</ul>
</section>

<section class="panel">
<h2>4. Activities and social context</h2>
<ul>
  <li>Eight activities are listed with operator/government hours and exception notes on <a href="activities.html">Activities + social</a>.</li>
  <li>Six restaurants and two activities have at least one directly verified Instagram or YouTube link. Several links are clearly marked as third-party reviews, not official commentary.</li>
  <li>No TikTok review link could be verified with available search tools, so none is listed.</li>
  <li>The one-hour travel constraint is <strong>not yet verified</strong>: no official subway/bus itinerary for February 2027 was obtained. MTA planning links are provided per activity; check close to travel.</li>
</ul>
</section>

<section class="panel">
<h2>5. Recommended path (pending the decision gates)</h2>
<ol>
  <li>Keep 15–18 Feb 2027 as the target; hold off on non-refundable booking until dated rates are visible.</li>
  <li>Check Hyatt/Marriott offer terms and dated rates as soon as the booking window opens; compare seven-night totals on one date range.</li>
  <li>Choose one Midtown hotel with a king or queen bed and private bath, then run each restaurant/activity through the MTA trip planner to confirm the one-hour rule.</li>
  <li>Book only one or two starred dinners in advance; the rest can be scheduled after confirming opening days for those dates.</li>
</ol>
<p>See <a href="questions.html">Questions</a> for what is still unknown and <a href="suggestions.html">Suggestions</a> for optional site and research upgrades.</p>
</section>
'''
write('pages/executive-summary.html', page('Executive summary', 'pages/executive-summary.html', summary_body))

michelin_body = '''
<h1>Michelin dining</h1>
<p>All 19 starred restaurants in the current official New York City 3-star and 2-star lists.
Days, hours and addresses are transcribed from each restaurant's own Michelin Guide detail page.
"Michelin price band" is Michelin's own cost symbol ($$$$) and is <strong>not</strong> a menu price.</p>
<div class="note warn"><strong>Price for 2 (official) is blank on every row.</strong> No restaurant's own site published a fixed
price for two on the capture date. The "third-party reported price" column quotes what a reviewer said
in a video description and must not be treated as a current booked price.</div>
{filters}
{table}
<p class="small">Counts and distinction: <a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/3-stars-michelin" target="_blank" rel="noopener noreferrer">official 3-star list</a>,
<a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/2-stars-michelin" target="_blank" rel="noopener noreferrer">official 2-star list</a>,
<a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/1-star-michelin" target="_blank" rel="noopener noreferrer">official 1-star list</a>.</p>
<h2>Guide vs star distinction</h2>
<p>A Michelin star (one, two or three) is an award. "Selected restaurants" and "Bib Gourmand" are
MICHELIN Guide recommendations without stars. Every restaurant in the table above currently holds
stars per the official list. All 50 one-star names are listed below from the official list; only the
19 three-/two-star entries were transcribed to full detail rows.</p>
<h2>All 50 one-star restaurants (names only)</h2>
{one_star_table}
'''.format(filters=filters('michelin'), table=michelin_table(), one_star_table=one_star_names_table())
write('pages/michelin.html', page('Michelin dining', 'pages/michelin.html', michelin_body))

hotels_body = '''
<h1>Hotels</h1>
<p>Candidates are ranked by verified room/bath/amenity fit and location for a two-adult stay.
<strong>Price ranking is deliberately not shown</strong> because no dated February 2027 rate was available
from an official booking page on the capture date.</p>
<div class="note warn"><strong>7-night totals and one-hour transit times are blank.</strong> The Michelin Guide
hotels page states bookings cannot be made more than 31 days ahead; the preferred stay was 82 days away.
Blank cells are unverified, not zero.</div>
<h2>How the Michelin cluster number is defined</h2>
<p>12 of the 19 verified starred restaurants have Michelin-listed addresses in Manhattan's roughly
30th–60th Street band. All five candidate hotels are in or next to that band, so the number is the same
for each. It is <strong>not</strong> a verified count of restaurants reachable within one hour by subway
or bus; that requires actual itineraries and is flagged as unverified.</p>
{filters}
{table}
<h2>Booking timing — what is actually verified</h2>
<ul>
  <li>Hyatt promotion window: qualifying stays 31 Oct 2026–30 Apr 2027, book by 8 Dec 2026, up to 25% for World of Hyatt members (terms apply). <a href="https://www.hyatt.com/hyatt-centric/en-US/nycts-hyatt-centric-times-square/offers" target="_blank" rel="noopener noreferrer">Official offer page</a>.</li>
  <li>Marriott Cyber Sale: members save 25%, stays 29 Nov 2026–2 May 2027; also a "Planning Ahead Pays Off" offer with stays 1 Nov 2026–30 Jun 2027. <a href="https://www.marriott.com/en-us/hotels/nycts-towneplace-suites-new-york-manhattan-times-square/overview/" target="_blank" rel="noopener noreferrer">Official hotel page</a>.</li>
  <li>Neither promotion confirms a price for 15–22 Feb 2027. Compare total price including taxes and mandatory fees on the same dates before deciding.</li>
</ul>
<p class="small">MTA trip planning: <a href="https://new.mta.info/" target="_blank" rel="noopener noreferrer">new.mta.info</a>.
Hotel ranking is provisional and may change once verified rates arrive.</p>
'''.format(filters=filters('hotels'), table=hotels_table())
write('pages/hotels.html', page('Hotels', 'pages/hotels.html', hotels_body))

activities_body = '''
<h1>Activities + social links</h1>
<p>Opening days, hours and exceptions are taken only from each operator or government page.
Social links were opened and checked where possible; third-party videos are labelled as such.</p>
<div class="note"><strong>Travel ≤1 hour:</strong> this is a planning target, not a verified result.
No official subway/bus itinerary for February 2027 was obtained, so travel-time cells are blank.
Check routes with the <a href="https://new.mta.info/" target="_blank" rel="noopener noreferrer">official MTA site</a>.</div>
{filters}
{table}
<h2>Social coverage gaps</h2>
<ul>
  <li>TikTok: no review link could be verified; none is listed.</li>
  <li>The Met, MoMA, High Line, ESB and 9/11 Museum: no official social link was captured from the fetched official pages.</li>
  <li>Social links marked "third-party" are reviews by creators, not statements from the venue.</li>
</ul>
'''.format(filters=filters('activities'), table=activities_table())
write('pages/activities.html', page('Activities + social', 'pages/activities.html', activities_body))

itinerary_body = '''
<h1>Itinerary outlines</h1>
<p>Day-by-day structure uses only opening days confirmed on official pages. Exact start times,
travel times and admission costs are left out when not verified.</p>
<div class="note warn">Restaurant evenings were chosen against the Michelin-listed weekly closures.
Holiday and private-event exceptions for February 2027 are not published; recheck before booking.</div>
<h2>Preferred four nights — 15–18 February 2027</h2>
<ul class="timeline">
  <li><span class="day">Mon 15 Feb · arrival</span><h3>Central Park + MoMA + downtown dinner</h3>
    Central Park (NYC Parks general hours), <a href="https://www.moma.org/visit/" target="_blank" rel="noopener noreferrer">MoMA</a> open Mon 10:30–17:30.
    Dinner: <a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/cesar" target="_blank" rel="noopener noreferrer">César</a> (Mon 6–11 PM) or <a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/atera" target="_blank" rel="noopener noreferrer">Atera</a> (Mon 7–10 PM). Jungsik is closed Monday.</li>
  <li><span class="day">Tue 16 Feb</span><h3>Statue of Liberty / Ellis Island + High Line + Korean fine dining</h3>
    <a href="https://www.nps.gov/stli/planyourvisit/hours.htm" target="_blank" rel="noopener noreferrer">NPS park hours 9:00–16:30</a>; ferry times must be checked with the official operator.
    <a href="https://www.thehighline.org/visit/" target="_blank" rel="noopener noreferrer">High Line</a> 7 AM–8 PM in February.
    Dinner: <a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/jungsik-new-york" target="_blank" rel="noopener noreferrer">Jungsik</a> or <a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/atomix" target="_blank" rel="noopener noreferrer">Atomix</a> (both open Tue).</li>
  <li><span class="day">Wed 17 Feb</span><h3>Empire State Building + The Modern / Per Se</h3>
    <a href="https://www.esbnyc.com/hours-directions" target="_blank" rel="noopener noreferrer">ESB</a> currently 10 AM–10 PM; February 2027 hours not published. The Met is closed Wednesday.
    Dinner: <a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/per-se" target="_blank" rel="noopener noreferrer">Per Se</a> (Wed 4:30–9 PM) or <a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/the-modern" target="_blank" rel="noopener noreferrer">The Modern</a> (Wed 5–9 PM).</li>
  <li><span class="day">Thu 18 Feb · departure</span><h3>MoMA late + Eleven Madison Park</h3>
    MoMA open until 8:30 PM on Friday, 5:30 PM Thursday.
    Farewell dinner: <a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/eleven-madison-park" target="_blank" rel="noopener noreferrer">Eleven Madison Park</a> (Thu 5:30–10 PM).</li>
</ul>
<h2>Seven-night extension — 19–22 February 2027</h2>
<ul class="timeline">
  <li><span class="day">Fri 19 Feb</span><h3>The Met late + Aquavit / Gabriel Kreuther</h3>
    <a href="https://www.metmuseum.org/plan-your-visit" target="_blank" rel="noopener noreferrer">The Met</a> Fri 10 AM–9 PM (official hours; one indexed version shows different days — recheck).
    Dinner: Aquavit or Gabriel Kreuther, both open Friday.</li>
  <li><span class="day">Sat 20 Feb</span><h3>Broadway / Times Square + a three-star lunch or dinner</h3>
    Le Bernardin is open Saturday for dinner (5–11 PM); Per Se and Jungsik are also open.</li>
  <li><span class="day">Sun 21 Feb</span><h3>9/11 Memorial + slower day</h3>
    <a href="https://www.911memorial.org/visit" target="_blank" rel="noopener noreferrer">Memorial</a> daily 8 AM–8 PM; Museum Wed–Mon 9 AM–7 PM, last entry 5:30 PM.
    Per Se, Sushi Sho and Chef's Table at Brooklyn Fare are open Sunday.</li>
  <li><span class="day">Mon 22 Feb</span><h3>Departure day</h3>
    MoMA and The Met are open Monday; many starred restaurants close Monday — verify before planning a final dinner.</li>
</ul>
<p class="small">Detailed hours and source links are on the <a href="michelin.html">Michelin dining</a> and
<a href="activities.html">Activities</a> pages.</p>
'''
write('pages/itinerary.html', page('Itinerary', 'pages/itinerary.html', itinerary_body))

questions_body = '''
<h1>Questions to answer before a decision</h1>
<p>These are the gaps that currently prevent a fully evidenced booking decision. Each question is
paired with what is known, what is missing and how to discover it.</p>

<div class="qa">
<h3>Q1. What is the actual total price for seven nights?</h3>
<dl><dt>Known</dt><dd>Room/bath/amenity details for five hotels; nationwide promotion windows.</dd>
<dt>Missing</dt><dd>Dated per-night rate, taxes, mandatory fees and seven-night total for 15–22 Feb 2027.</dd>
<dt>How to find</dt><dd>Open each official booking link with those exact dates, two adults, one room; record the all-in total.</dd>
<dt>Decision</dt><dd>Determines cheapest hotel and whether the trip stays in budget.</dd></dl>
</div>
<div class="qa">
<h3>Q2. Which date range is cheapest inside 15 Feb – 23 Mar 2027?</h3>
<dl><dt>Known</dt><dd>Preferred dates and the booking-window promotions.</dd>
<dt>Missing</dt><dd>A dated rate calendar for every candidate weekend/weekday combination.</dd>
<dt>How to find</dt><dd>Check official rate calendars on the same room type for several date ranges; record totals side by side.</dd>
<dt>Decision</dt><dd>Whether to move away from the preferred 15–18 Feb dates.</dd></dl>
</div>
<div class="qa">
<h3>Q3. When is the booking window open for February 2027?</h3>
<dl><dt>Known</dt><dd>Michelin Guide hotel search says no more than 31 days ahead; Hyatt and Marriott promotions cover Feb 2027 stays.</dd>
<dt>Missing</dt><dd>Exact date when each brand exposes 15–22 Feb 2027 inventory.</dd>
<dt>How to find</dt><dd>Check brand booking calendar periodically; set a reminder before the Hyatt 8 Dec 2026 offer deadline.</dd>
<dt>Decision</dt><dd>Booking timeline and rate-lock strategy.</dd></dl>
</div>
<div class="qa">
<h3>Q4. Does each hotel meet the private-bath and queen-or-bigger requirement on the booked rate?</h3>
<dl><dt>Known</dt><dd>Hyatt and Hilton list queen/king rooms; Marriott pages list queen/studio options.</dd>
<dt>Missing</dt><dd>Confirmation for the exact room category available on the chosen dates; bathroom details for several hotels.</dd>
<dt>How to find</dt><dd>Read the room description on the dated booking result; contact hotel if the page is silent.</dd>
<dt>Decision</dt><dd>Eliminates hotels that fail hard requirements.</dd></dl>
</div>
<div class="qa">
<h3>Q5. Is every chosen activity within one hour by subway/bus from the hotel?</h3>
<dl><dt>Known</dt><dd>Official addresses and MTA planning site.</dd>
<dt>Missing</dt><dd>Actual origin-to-destination itineraries for a specific hotel and date/time, including walking and transfers.</dd>
<dt>How to find</dt><dd>Run each address through the MTA trip planner for midday and evening; record the longest trip.</dd>
<dt>Decision</dt><dd>Whether the Midtown base satisfies the travel constraint.</dd></dl>
</div>
<div class="qa">
<h3>Q6. Will the chosen restaurants be open on the exact dates?</h3>
<dl><dt>Known</dt><dd>Weekly hours from Michelin detail pages; several Monday/Sunday closures.</dd>
<dt>Missing</dt><dd>February 2027 holiday, private-event and seasonal closures.</dd>
<dt>How to find</dt><dd>Confirm on the restaurant's own reservation page or by phone closer to the date.</dd>
<dt>Decision</dt><dd>Which dinners can be booked with confidence.</dd></dl>
</div>
<div class="qa">
<h3>Q7. What will a meal for two actually cost?</h3>
<dl><dt>Known</dt><dd>Michelin's $$$$ band; three reviewer-stated per-person prices on YouTube.</dd>
<dt>Missing</dt><dd>Current official menu prices, service charges, taxes, wine and tip.</dd>
<dt>How to find</dt><dd>Read the menu on each restaurant's own site or the official reservation deposit page.</dd>
<dt>Decision</dt><dd>Whether the dining budget is realistic.</dd></dl>
</div>
<div class="qa">
<h3>Q8. How far in advance are starred tables released?</h3>
<dl><dt>Known</dt><dd>Michelin pages link to Resy/Tock/OpenTable booking pages.</dd>
<dt>Missing</dt><dd>Release windows, deposit rules and cancellation terms per restaurant.</dd>
<dt>How to find</dt><dd>Open each official booking link and read the reservation terms.</dd>
<dt>Decision</dt><dd>When to book the must-do dinners.</dd></dl>
</div>
<div class="qa">
<h3>Q9. Which social reviews should be trusted?</h3>
<dl><dt>Known</dt><dd>Six restaurant and two activity links opened directly; some official accounts carry verified badges.</dd>
<dt>Missing</dt><dd>Current, date-matched reviews for every venue; TikTok links; creator disclosure of sponsored meals.</dd>
<dt>How to find</dt><dd>Search each platform for recent posts and check whether the account is official or discloses sponsorship.</dd>
<dt>Decision</dt><dd>Which reviews influence the shortlist.</dd></dl>
</div>
<div class="qa">
<h3>Q10. What do the conflicting official hours mean?</h3>
<dl><dt>Known</dt><dd>The Met's indexed official pages disagreed about one or more weekdays on 2026-11-25; Saga's Michelin page carried a 2025 edition breadcrumb.</dd>
<dt>Missing</dt><dd>Which displayed version is current for February 2027.</dd>
<dt>How to find</dt><dd>Recheck the live official pages closer to travel and record the retrieval date.</dd>
<dt>Decision</dt><dd>Itinerary sequencing for those venues.</dd></dl>
</div>
<div class="qa">
<h3>Q11. Are there better hotels outside the shortlist?</h3>
<dl><dt>Known</dt><dd>Five Midtown candidates with partial amenity verification.</dd>
<dt>Missing</dt><dd>Systematic comparison of all qualifying hotels in the allowed area, with dated rates.</dd>
<dt>How to find</dt><dd>Define the search radius, filter for queen/king + private bath, then compare dated all-in totals.</dd>
<dt>Decision</dt><dd>Whether the current ranking is complete.</dd></dl>
</div>
<div class="qa">
<h3>Q12. Is a 4-night, 7-night or longer stay best?</h3>
<dl><dt>Known</dt><dd>User preference 15–18 Feb; seven-night pricing request; allowed stay up to four weeks.</dd>
<dt>Missing</dt><dd>Preferences on pace, budget and number of starred meals; dated weekly rates.</dd>
<dt>How to find</dt><dd>Compare nightly totals across 3, 7 and 14 nights once rates are visible; decide with the traveller.</dd>
<dt>Decision</dt><dd>Final length of stay.</dd></dl>
</div>
'''
write('pages/questions.html', page('Questions', 'pages/questions.html', questions_body))

suggestions_body = '''
<h1>Suggestions — choose a path before implementing</h1>
<p>None of the items below has been applied to the data or the site. They are options for review.
Each has a benefit, cost in effort and the missing information it would resolve.</p>

<div class="panel">
<h2>A. Decision-focused options</h2>
<div class="idea"><h3>A1. Wait for dated rates, then rebuild the hotel ranking</h3>
<p><span class="badge verified">Highest value</span> Benefit: turns the blank price columns into a real cheapest-stay answer.
Effort: low once booking windows open. Needs: dated all-in totals for five hotels. Resolves Q1–Q3.</p></div>
<div class="idea"><h3>A2. Add a verified transit-time column using MTA itineraries</h3>
<p><span class="badge third-party">Research task</span> Benefit: makes the one-hour rule testable.
Effort: medium (one itinerary per restaurant/activity at evening travel time). Needs: origin hotel and date/time. Resolves Q5.</p></div>
<div class="idea"><h3>A3. Collect official menu prices for two</h3>
<p><span class="badge third-party">Research task</span> Benefit: replaces reviewer-reported prices with official figures.
Effort: medium; some restaurants publish only a deposit. Needs: official menu or booking deposit pages. Resolves Q7.</p></div>
<div class="idea"><h3>A4. Fix a hard decision date and booking calendar</h3>
<p><span class="badge verified">Recommended</span> Benefit: avoids missing the Hyatt 8 Dec 2026 deadline and similar offers.
Effort: low. Needs: traveller confirmation of preferred dates. Resolves Q2–Q3.</p></div>
</div>

<div class="panel">
<h2>B. Site and structure options</h2>
<div class="idea"><h3>B1. Add sorting and CSV download to every table</h3>
<p>Benefit: quick comparison on a phone. Effort: small JavaScript change. Needs: no new data. Does not change any verified value.</p></div>
<div class="idea"><h3>B2. Split "verified", "third-party" and "unverified" into separate visual columns</h3>
<p>Benefit: even clearer audit trail. Effort: small layout change. Needs: no new data.</p></div>
<div class="idea"><h3>B3. Add a map view with official MTA links</h3>
<p>Benefit: makes the cluster and travel constraint visual. Effort: medium. Needs: verified coordinates and transit itineraries; otherwise map would imply unverified travel times.</p></div>
<div class="idea"><h3>B4. Add a "changes since last check" log</h3>
<p>Benefit: catches Michelin award changes and hour edits. Effort: low. Needs: repeat captures with dates.</p></div>
</div>

<div class="panel">
<h2>C. Research-expansion options</h2>
<div class="idea"><h3>C1. Transcribe full detail for the 50 one-star restaurants</h3>
<p>Benefit: complete starred table with hours, addresses and social links. Effort: high. Needs: 50 official Michelin detail pages; names are already captured.</p></div>
<div class="idea"><h3>C2. Add Bib Gourmand and selected restaurants as a value-focused shortlist</h3>
<p>Benefit: cheaper alternatives near the hotel. Effort: medium. Needs: official Michelin list pages and price confirmation.</p></div>
<div class="idea"><h3>C3. Expand social coverage to every listed venue</h3>
<p>Benefit: more review context. Effort: high. Needs: verified official or clearly-labelled third-party links; TikTok access may remain blocked.</p></div>
<div class="idea"><h3>C4. Add Broadway show times and ticket prices for the exact dates</h3>
<p>Benefit: completes the evening plan. Effort: medium. Needs: official Broadway league/show pages with Feb 2027 schedules.</p></div>
</div>

<div class="note warn"><strong>No change has been implemented.</strong> Review the options, choose a path, then update
<code>COORDINATION.md</code> with a new task before work begins.</div>
'''
write('pages/suggestions.html', page('Suggestions', 'pages/suggestions.html', suggestions_body))

flagged_body = '''
<h1>Flagged for review</h1>
<p>Items below are published for review and do not block anything. Values that could not be confirmed
on an official source remain blank in the tables.</p>
<div class="table-wrap"><table>
<thead><tr><th>#</th><th>Irregularity / gap</th><th>Where it appears</th><th>What was done</th><th>Source or verification link</th><th>Status</th></tr></thead>
<tbody>
<tr><td>1</td><td>No dated February 2027 hotel rate on any official page</td><td>Hotels, executive summary</td><td>Nightly and 7-night totals left blank</td><td><a href="https://guide.michelin.com/us/en/hotels" target="_blank" rel="noopener noreferrer">Michelin hotels (31-day booking limit)</a></td><td><span class="badge flagged">needs review</span></td></tr>
<tr><td>2</td><td>Cheapest booking date cannot be calculated</td><td>Hotels, questions</td><td>Left unanswered; booking windows listed instead</td><td><a href="https://www.hyatt.com/hyatt-centric/en-US/nycts-hyatt-centric-times-square/offers" target="_blank" rel="noopener noreferrer">Hyatt offers</a></td><td><span class="badge flagged">needs review</span></td></tr>
<tr><td>3</td><td>One-hour subway/bus travel time not verified for any venue</td><td>Hotels, activities, itinerary</td><td>Travel cells blank; MTA link supplied</td><td><a href="https://new.mta.info/" target="_blank" rel="noopener noreferrer">MTA</a></td><td><span class="badge flagged">needs review</span></td></tr>
<tr><td>4</td><td>Met hours conflict between indexed official versions</td><td>Activities, itinerary</td><td>Used the version shown on the official site listing; flagged</td><td><a href="https://www.metmuseum.org/plan-your-visit" target="_blank" rel="noopener noreferrer">The Met</a></td><td><span class="badge flagged">needs review</span></td></tr>
<tr><td>5</td><td>Saga Michelin page breadcrumb showed millesime=2025</td><td>Michelin dining</td><td>2-star status confirmed on current 2-star list; page noted</td><td><a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/saga" target="_blank" rel="noopener noreferrer">Michelin Saga</a></td><td><span class="badge flagged">needs review</span></td></tr>
<tr><td>6</td><td>Hilton pages blocked direct fetch in this session</td><td>Hotels</td><td>Used Hilton-indexed official page content; flagged for manual recheck</td><td><a href="https://www.hilton.com/en/hotels/nycnhhh-new-york-hilton-midtown/rooms/" target="_blank" rel="noopener noreferrer">Hilton rooms</a></td><td><span class="badge flagged">needs review</span></td></tr>
<tr><td>7</td><td>One Atomix YouTube video returned HTTP 401 (private/unavailable)</td><td>Michelin dining</td><td>Link marked search-result-only</td><td><a href="https://www.youtube.com/watch?v=_XCQ1sooD2o" target="_blank" rel="noopener noreferrer">YouTube result</a></td><td><span class="badge flagged">needs review</span></td></tr>
<tr><td>8</td><td>Joo Ok slug first tried did not resolve</td><td>Michelin dining</td><td>Replaced with verified slug from official page; detail recorded</td><td><a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/joo-ok-1214822" target="_blank" rel="noopener noreferrer">Michelin Joo Ok</a></td><td><span class="badge verified">resolved</span></td></tr>
<tr><td>9</td><td>TikTok review links could not be verified</td><td>Michelin dining, activities</td><td>No TikTok links listed</td><td><a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/3-stars-michelin" target="_blank" rel="noopener noreferrer">Michelin list (source policy)</a></td><td><span class="badge flagged">needs review</span></td></tr>
<tr><td>10</td><td>17 of 50 one-star names initially not captured</td><td>Michelin dining</td><td>All 50 names now captured from official page 2; names only, no inferred detail</td><td><a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/1-star-michelin/page/2" target="_blank" rel="noopener noreferrer">Official 1-star list, page 2</a></td><td><span class="badge verified">resolved</span></td></tr>
<tr><td>11</td><td>Restaurant prices for two not published officially</td><td>Michelin dining</td><td>Official price column blank; reviewer prices clearly separated</td><td><a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/eleven-madison-park" target="_blank" rel="noopener noreferrer">Example Michelin page (price band only)</a></td><td><span class="badge flagged">needs review</span></td></tr>
<tr><td>12</td><td>February 2027 holiday/event exceptions not published</td><td>Activities, itinerary</td><td>Left blank or noted as not published</td><td><a href="https://www.nps.gov/stli/planyourvisit/hours.htm" target="_blank" rel="noopener noreferrer">NPS hours</a></td><td><span class="badge flagged">needs review</span></td></tr>
<tr><td>13</td><td>Broadway/times-square row has no verified hours or price</td><td>Activities</td><td>All value cells blank rather than inferred</td><td><a href="https://www.timessquarenyc.org/" target="_blank" rel="noopener noreferrer">Times Square Alliance</a></td><td><span class="badge flagged">needs review</span></td></tr>
<tr><td>14</td><td>Hotel rank is not price-based</td><td>Hotels</td><td>Stated explicitly; promotion windows shown instead of a price rank</td><td><a href="https://www.marriott.com/en-us/hotels/nycts-towneplace-suites-new-york-manhattan-times-square/overview/" target="_blank" rel="noopener noreferrer">Marriott offers page</a></td><td><span class="badge flagged">needs review</span></td></tr>
</tbody></table></div>
'''
write('pages/flagged-for-review.html', page('Flagged for review', 'pages/flagged-for-review.html', flagged_body))

sources_body = '''
<h1>Official sources</h1>
<p>Every data table row links to one of these sources directly. Social links are separate and labelled
official or third-party.</p>
<div class="table-wrap"><table>
<thead><tr><th>Source</th><th>Used for</th><th>Verification method</th><th>Link</th></tr></thead>
<tbody>
<tr><td>MICHELIN Guide — NYC 3-star list</td><td>Counts, five 3-star restaurants</td><td>Page opened and read 2026-11-25</td><td><a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/3-stars-michelin" target="_blank" rel="noopener noreferrer">Open</a></td></tr>
<tr><td>MICHELIN Guide — NYC 2-star list</td><td>14 two-star restaurants</td><td>Page opened and read 2026-11-25</td><td><a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/2-stars-michelin" target="_blank" rel="noopener noreferrer">Open</a></td></tr>
<tr><td>MICHELIN Guide — NYC 1-star list</td><td>First 33 names; status counts</td><td>Page opened and read 2026-11-25</td><td><a href="https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/1-star-michelin" target="_blank" rel="noopener noreferrer">Open</a></td></tr>
<tr><td>19 individual MICHELIN Guide detail pages</td><td>Address, cuisine, band, days and hours</td><td>Each page opened; values transcribed</td><td><a href="michelin.html">See Michelin dining page</a></td></tr>
<tr><td>Hyatt Centric Times Square</td><td>Rooms, beds, bathroom, offer window</td><td>Official rooms/overview/offers pages opened</td><td><a href="https://www.hyatt.com/hyatt-centric/en-US/nycts-hyatt-centric-times-square/rooms" target="_blank" rel="noopener noreferrer">Open</a></td></tr>
<tr><td>Marriott (Marquis, TownePlace, Essex House)</td><td>Rooms, amenities, offer windows</td><td>Official Marriott pages opened</td><td><a href="https://www.marriott.com/en-us/hotels/nycmq-new-york-marriott-marquis/rooms/" target="_blank" rel="noopener noreferrer">Open</a></td></tr>
<tr><td>Hilton New York Midtown</td><td>Queen room, address, mandatory fee note</td><td>Official page content via search index; direct fetch blocked</td><td><a href="https://www.hilton.com/en/hotels/nycnhhh-new-york-hilton-midtown/rooms/" target="_blank" rel="noopener noreferrer">Open</a></td></tr>
<tr><td>National Park Service — Statue of Liberty</td><td>Park hours, closures, exceptions</td><td>Official page opened</td><td><a href="https://www.nps.gov/stli/planyourvisit/hours.htm" target="_blank" rel="noopener noreferrer">Open</a></td></tr>
<tr><td>Statue City Cruises</td><td>Authorized ferry, ticket inclusions</td><td>Official ticket page opened</td><td><a href="https://statuecitycruises.com/tickets" target="_blank" rel="noopener noreferrer">Open</a></td></tr>
<tr><td>The Metropolitan Museum of Art</td><td>Hours, holidays, admission</td><td>Official pages opened/indexed</td><td><a href="https://www.metmuseum.org/plan-your-visit" target="_blank" rel="noopener noreferrer">Open</a></td></tr>
<tr><td>MoMA</td><td>Hours, holidays, admission</td><td>Official visit page opened</td><td><a href="https://www.moma.org/visit/" target="_blank" rel="noopener noreferrer">Open</a></td></tr>
<tr><td>9/11 Memorial & Museum</td><td>Memorial/museum hours, ticket note</td><td>Official visit page opened</td><td><a href="https://www.911memorial.org/visit" target="_blank" rel="noopener noreferrer">Open</a></td></tr>
<tr><td>Friends of the High Line</td><td>Seasonal hours, Rail Yard exception</td><td>Official visitor page opened</td><td><a href="https://www.thehighline.org/visit/" target="_blank" rel="noopener noreferrer">Open</a></td></tr>
<tr><td>NYC Parks</td><td>Central Park location, general park hours, official social links</td><td>Official pages opened</td><td><a href="https://www.nycgovparks.org/about" target="_blank" rel="noopener noreferrer">Open</a></td></tr>
<tr><td>Empire State Building</td><td>Current hours, ticket prices, directions</td><td>Official hours/ticket pages opened</td><td><a href="https://www.esbnyc.com/hours-directions" target="_blank" rel="noopener noreferrer">Open</a></td></tr>
<tr><td>MTA</td><td>Trip planning link (no itinerary values claimed)</td><td>Official site linked for user verification</td><td><a href="https://new.mta.info/" target="_blank" rel="noopener noreferrer">Open</a></td></tr>
<tr><td>YouTube / Instagram venue and reviewer pages</td><td>Social review links</td><td>Each linked page opened directly unless marked search-only</td><td><a href="michelin.html">See Michelin dining page</a></td></tr>
</tbody></table></div>
'''
write('pages/sources.html', page('Sources', 'pages/sources.html', sources_body))

print('site build complete')
