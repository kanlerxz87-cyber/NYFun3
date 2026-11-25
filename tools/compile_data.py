#!/usr/bin/env python3
"""Compile the verified New York trip-planning data corpus.

All values below were transcribed line by line from the official pages listed in
SOURCES. A value that could not be confirmed from an official source is left as
an empty string and is flagged "unverified" by the site generator. Nothing is
inferred or filled in.

Run: python3 tools/compile_data.py
"""
from __future__ import annotations

import json
from pathlib import Path

from data_updates import apply_updates

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

CHECKED = "2026-11-25"

S = {
    "michelin_stars_2025": {
        "title": "MICHELIN Guide — All the Stars in The MICHELIN Guide to New York City 2025 (18 Nov 2025)",
        "url": "https://guide.michelin.com/us/en/article/michelin-guide-ceremony/all-the-stars-in-the-michelin-guide-to-new-york-city-2025",
        "type": "official guide",
    },
    "michelin_all_starred": {
        "title": "MICHELIN Guide — NYC All Starred Restaurants (current selection, 69 listed)",
        "url": "https://guide.michelin.com/en/us/new-york-state/new-york/restaurants/all-starred",
        "type": "official guide",
    },
    "michelin_nyc": {
        "title": "MICHELIN Guide — NYC restaurants (369 listed; 76 Bib Gourmand; 224 Selected Restaurants)",
        "url": "https://guide.michelin.com/us/en/new-york-state/new-york/restaurants",
        "type": "official guide",
    },
    "michelin_additions": {
        "title": "MICHELIN Guide — New Additions to the MICHELIN Guide New York (18 Nov 2026)",
        "url": "https://guide.michelin.com/us/en/article/travel/new-restaurants-new-york",
        "type": "official guide",
    },
    "hotel_week": {
        "title": "NYC Tourism + Conventions — NYC Hotel Week (Jan 2–Feb 11, 2027; 25% off)",
        "url": "https://www.nyctourism.com/hotel-week/",
        "type": "official DMO",
    },
    "hotel_week_about": {
        "title": "NYC Tourism + Conventions — About NYC Hotel Week FAQs",
        "url": "https://www.nyctourism.com/hotel-week-about/",
        "type": "official DMO",
    },
    "hotel_week_press": {
        "title": "NYC Tourism + Conventions press release — NYC Hotel Week 2027 (17 Nov 2026)",
        "url": "https://business.nyctourism.com/press-media/press-releases/nyc-hotel-week-2027",
        "type": "official DMO",
    },
    "opm": {
        "title": "U.S. Office of Personnel Management — 2027 Federal Holidays",
        "url": "https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/",
        "type": "government",
    },
    "mta_maps": {
        "title": "MTA — Maps (subway and bus maps)",
        "url": "https://www.mta.info/maps",
        "type": "official transit agency",
    },
    "mta_trip": {
        "title": "MTA NYC Transit — Trip Planner widget help (travel-time tool)",
        "url": "http://tripplanner.mta.info/widget/help.htm",
        "type": "official transit agency",
    },
    "mta_riding": {
        "title": "MTA — How to ride the NYC subway (24/7 service)",
        "url": "https://www.mta.info/guides/riding-the-subway",
        "type": "official transit agency",
    },
    "met": {
        "title": "The Metropolitan Museum of Art — official site / plan your visit",
        "url": "https://www.metmuseum.org/plan-your-visit",
        "type": "official venue",
    },
    "met_home": {
        "title": "The Metropolitan Museum of Art — homepage (closed Wednesdays, $30 admission)",
        "url": "https://www.metmuseum.org/",
        "type": "official venue",
    },
    "moma": {
        "title": "MoMA — Locations, hours, and admission",
        "url": "https://www.moma.org/visit/",
        "type": "official venue",
    },
    "amnh": {
        "title": "American Museum of Natural History — Hours and temporary hall closures",
        "url": "https://www.amnh.org/plan-your-visit/hours",
        "type": "official venue",
    },
    "nps": {
        "title": "National Park Service — Statue of Liberty National Monument operating hours & seasons",
        "url": "https://www.nps.gov/stli/planyourvisit/hours.htm",
        "type": "government",
    },
    "esb": {
        "title": "Empire State Building — Hours & directions (official)",
        "url": "https://www.esbnyc.com/visit/hours-of-operation",
        "type": "official venue",
    },
    "toprock": {
        "title": "Rockefeller Center — Top of the Rock tickets & hours (official)",
        "url": "https://www.rockefellercenter.com/tickets/top-of-the-rock-observation-deck/",
        "type": "official venue",
    },
    "owo": {
        "title": "One World Observatory — Plan your visit (official)",
        "url": "https://www.oneworldobservatory.com/plan-your-visit/",
        "type": "official venue",
    },
    "911": {
        "title": "National September 11 Memorial & Museum — Visit (official)",
        "url": "https://www.911memorial.org/visit",
        "type": "official venue",
    },
    "highline": {
        "title": "Friends of the High Line — Visitor Info (official)",
        "url": "https://www.thehighline.org/visit/",
        "type": "official venue",
    },
    "whitney": {
        "title": "Whitney Museum of American Art — Plan your visit (official)",
        "url": "https://whitney.org/visit",
        "type": "official venue",
    },
    "centralpark": {
        "title": "NYC Parks — Central Park (official city site)",
        "url": "https://www.nycgovparks.org/parks/central-park",
        "type": "government",
    },
    "pod51": {
        "title": "Pod 51 Hotel — official site (home)",
        "url": "https://www.thepodhotel.com/pod-51",
        "type": "official hotel",
    },
    "pod51_rooms": {
        "title": "Pod 51 Hotel — Rooms (official)",
        "url": "https://www.thepodhotel.com/pod-51/rooms",
        "type": "official hotel",
    },
    "pod51_faq": {
        "title": "Pod 51 Hotel — FAQs (official)",
        "url": "https://www.thepodhotel.com/pod-51/frequently-asked-questions",
        "type": "official hotel",
    },
    "pod51_location": {
        "title": "Pod 51 Hotel — Location + Contact (official)",
        "url": "https://www.thepodhotel.com/pod-51/location",
        "type": "official hotel",
    },
    "howard": {
        "title": "11 Howard — official hotel site",
        "url": "https://www.11howard.com/",
        "type": "official hotel",
    },
    "howard_michelin": {
        "title": "MICHELIN Guide — 11 Howard hotel (SoHo)",
        "url": "https://guide.michelin.com/us/en/hotels-stays/nyc/11-howard-8129",
        "type": "official guide",
    },
    "arlo_nomad": {
        "title": "NYC Tourism — Arlo NoMad (NYC Hotel Week listing)",
        "url": "https://www.nyctourism.com/hotel-week/arlo-hotel-nomad/",
        "type": "official DMO",
    },
    "citizenm": {
        "title": "Marriott / citizenM brand — rooms (XL king bed, power shower)",
        "url": "https://www.marriott.com/brands/citizenm.mi",
        "type": "official hotel group",
    },
    "ac_hotel": {
        "title": "NYC Tourism — AC Hotel New York Times Square (NYC Hotel Week listing)",
        "url": "https://www.nyctourism.com/hotel-week/",
        "type": "official DMO",
    },
    "lex_hotel": {
        "title": "NYC Tourism — The Lex Hotel (NYC Hotel Week listing)",
        "url": "https://www.nyctourism.com/hotel-week/",
        "type": "official DMO",
    },
    "westin": {
        "title": "NYC Tourism — The Westin New York at Times Square (NYC Hotel Week listing)",
        "url": "https://www.nyctourism.com/hotel-week/",
        "type": "official DMO",
    },
    "lb": {
        "title": "Le Bernardin — official site",
        "url": "https://www.le-bernardin.com/",
        "type": "official restaurant",
    },
    "lb_lunch": {
        "title": "Le Bernardin — official lunch menu PDF ($142 / $270 / $350 per person)",
        "url": "https://www.le-bernardin.com/content/pdfs/lunch-10.2.pdf",
        "type": "official menu PDF",
    },
    "lb_lounge": {
        "title": "Le Bernardin — official lounge menu PDF (item prices)",
        "url": "https://www.le-bernardin.com/content/pdfs/lounge-menu-3.10.pdf",
        "type": "official menu PDF",
    },
    "emp": {
        "title": "Eleven Madison Park — About / restaurant hours",
        "url": "https://www.elevenmadisonpark.com/ourrestaurant",
        "type": "official restaurant",
    },
    "emp_faq": {
        "title": "Eleven Madison Park — FAQs (tasting menu prices, reservation policy)",
        "url": "https://www.elevenmadisonpark.com/faq",
        "type": "official restaurant",
    },
    "modern": {
        "title": "The Modern — official menu and prices",
        "url": "https://www.themodernnyc.com/the-modern/",
        "type": "official restaurant",
    },
    "cote": {
        "title": "COTE Korean Steakhouse — NYC Flatiron (official)",
        "url": "https://www.cotekoreansteakhouse.com/locations/cotenycflatiron",
        "type": "official restaurant",
    },
    "perseny": {
        "title": "Thomas Keller Restaurant Group — Per Se (official)",
        "url": "https://www.thomaskeller.com/perseny/",
        "type": "official restaurant",
    },
    "jungsik": {
        "title": "Jungsik New York (official)",
        "url": "https://www.jungsik.com/",
        "type": "official restaurant",
    },
    "atomix": {
        "title": "Atomix (official)",
        "url": "https://www.atomixnyc.com/",
        "type": "official restaurant",
    },
    "youtube_lb": {
        "title": "YouTube — search results: Le Bernardin review (platform page fetched)",
        "url": "https://www.youtube.com/results?search_query=Le+Bernardin+review",
        "type": "social platform",
    },
    "youtube_emp": {
        "title": "YouTube — search results: Eleven Madison Park review (platform page fetched)",
        "url": "https://www.youtube.com/results?search_query=Eleven+Madison+Park+review",
        "type": "social platform",
    },
    "youtube_cote": {
        "title": "YouTube — search results: COTE Korean Steakhouse NYC review (platform page fetched)",
        "url": "https://www.youtube.com/results?search_query=COTE+Korean+Steakhouse+NYC+review",
        "type": "social platform",
    },
    "youtube_met": {
        "title": "YouTube — search results: Met Museum New York review (platform page fetched)",
        "url": "https://www.youtube.com/results?search_query=Met+Museum+New+York+review",
        "type": "social platform",
    },
    "youtube_sol": {
        "title": "YouTube — search results: Statue of Liberty visit review (platform page fetched)",
        "url": "https://www.youtube.com/results?search_query=Statue+of+Liberty+New+York+visit+review",
        "type": "social platform",
    },
}

for key, value in S.items():
    value["checked"] = CHECKED
    value["id"] = key


def M(slug):
    return "https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/" + slug


# ---------------------------------------------------------------------------
# MICHELIN 2025 star roster (official article, 18 November 2025)
# ---------------------------------------------------------------------------
ROSTER_RAW = [
    ("3", "Eleven Madison Park", "Vegan, Contemporary", "eleven-madison-park"),
    ("3", "Jungsik", "Korean", "jungsik-new-york"),
    ("3", "Le Bernardin", "Seafood", "le-bernardin"),
    ("3", "Per Se", "Contemporary", "per-se"),
    ("3", "Sushi Sho", "Japanese", "sushi-sho-1213976"),
    ("2", "Aquavit", "Scandinavian", "aquavit"),
    ("2", "Aska", "Scandinavian", "aska"),
    ("2", "Atera", "Contemporary", "atera"),
    ("2", "Atomix", "Korean", "atomix"),
    ("2", "Blue Hill at Stone Barns", "American", "blue-hill-at-stone-barns"),
    ("2", "César", "Contemporary", "cesar"),
    ("2", "Chef's Table at Brooklyn Fare", "Contemporary", "chef-s-table-at-brooklyn-fare"),
    ("2", "Gabriel Kreuther", "French", "gabriel-kreuther"),
    ("2", "Jean-Georges", "Contemporary", "jean-georges"),
    ("2", "Joo Ok", "Korean", "joo-ok-1214822"),
    ("2", "Masa", "Japanese", "masa"),
    ("2", "odo", "Japanese", "odo"),
    ("2", "Saga", "Contemporary", "saga"),
    ("2", "Sushi Noz", "Japanese", "sushi-noz"),
    ("2", "The Modern", "Contemporary", "the-modern"),
    ("1", "63 Clinton", "Contemporary", "63-clinton"),
    ("1", "Bar Miller", "Japanese", "bar-miller"),
    ("1", "bōm", "Korean", "bom"),
    ("1", "Bridges", "Contemporary", "bridges-1216261"),
    ("1", "Café Boulud", "French", "cafe-boulud"),
    ("1", "Casa Mono", "Spanish", "casa-mono"),
    ("1", "Corima", "Mexican", "corima"),
    ("1", "Cote", "Korean", "cote"),
    ("1", "Crown Shy", "Contemporary", "crown-shy"),
    ("1", "Daniel", "French", "daniel"),
    ("1", "Dirt Candy", "Vegetarian", "dirt-candy"),
    ("1", "Essential by Christophe", "French Contemporary", "essential-by-christophe"),
    ("1", "Estela", "Contemporary", "estela"),
    ("1", "Family Meal at Blue Hill", "American", "blue-hill"),
    ("1", "Francie", "Contemporary", "francie"),
    ("1", "Frevo", "Contemporary", "frevo"),
    ("1", "Gramercy Tavern", "Contemporary", "gramercy-tavern"),
    ("1", "Huso", "Contemporary", "huso-1218089"),
    ("1", "Icca", "Japanese", "icca"),
    ("1", "Jeju Noodle Bar", "Korean", "jeju-noodle-bar"),
    ("1", "Jōji", "Japanese", "joji"),
    ("1", "Jua", "Korean", "jua"),
    ("1", "Kochi", "Korean", "kochi"),
    ("1", "Kosaka", "Japanese", "kosaka"),
    ("1", "L'Abeille", "French", "l%E2%80%99abeille"),
    ("1", "La Bastide by Andrea Calstier", "French", "la-bastide-by-andrea-calstier"),
    ("1", "Le Coucou", "French", "le-coucou"),
    ("1", "Le Pavillon", "French", "le-pavillon-1192744"),
    ("1", "Mari", "Korean", "mari"),
    ("1", "Meju", "Korean", "meju"),
    ("1", "Muku", "Japanese", "muku"),
    ("1", "Noda", "Japanese", "noda"),
    ("1", "Nōksu", "Contemporary", "noksu"),
    ("1", "Noz 17", "Japanese", "noz17"),
    ("1", "Oiji Mi", "Korean", "oiji-mi"),
    ("1", "Oxomoco", "Mexican", "oxomoco"),
    ("1", "Restaurant Yuu", "French Contemporary", "restaurant-yuu"),
    ("1", "Rezdôra", "Italian", "rezdora-osteria-emiliana"),
    ("1", "Semma", "Indian", "semma"),
    ("1", "Shion 69 Leonard Street", "Japanese", "shoji-at-69-leonard"),
    ("1", "Shmoné", "Israeli", "shmone"),
    ("1", "Shota Omakase", "Japanese", "shota-omakase"),
    ("1", "Sushi Nakazawa", "Japanese", "sushi-nakazawa"),
    ("1", "Tempura Matsui", "Japanese", "tempura-matsui"),
    ("1", "The Four Horsemen", "American", "the-four-horsemen"),
    ("1", "Torien", "Japanese", "torien"),
    ("1", "Torrisi", "Contemporary", "torrisi"),
    ("1", "Tsukimi", "Japanese", "tsukimi"),
    ("1", "Tuome", "Fusion", "tuome"),
    ("1", "Yamada", "Japanese", "yamada"),
    ("1", "YingTao", "Contemporary", "yingtao"),
    ("1", "Yoshino", "Japanese", "yoshino-1185037"),
]

# The official article links a few of these outside the /new-york/ path.
ROSTER_OVERRIDES = {
    "Aska": "https://guide.michelin.com/us/en/new-york-state/brooklyn/restaurant/aska",
    "Blue Hill at Stone Barns": "https://guide.michelin.com/us/en/new-york-state/tarrytown/restaurant/blue-hill-at-stone-barns",
    "La Bastide by Andrea Calstier": "https://guide.michelin.com/us/en/new-york-state/north-salem/restaurant/la-bastide-by-andrea-calstier",
    "Francie": "https://guide.michelin.com/us/en/new-york-state/brooklyn/restaurant/francie",
    "Meju": "https://guide.michelin.com/us/en/new-york-state/queens/restaurant/meju",
    "Oxomoco": "https://guide.michelin.com/us/en/new-york-state/brooklyn/restaurant/oxomoco",
    "Restaurant Yuu": "https://guide.michelin.com/us/en/new-york-state/brooklyn/restaurant/restaurant-yuu",
    "Shota Omakase": "https://guide.michelin.com/us/en/new-york-state/brooklyn/restaurant/shota-omakase",
    "The Four Horsemen": "https://guide.michelin.com/us/en/new-york-state/brooklyn/restaurant/the-four-horsemen",
}

DETAILED_NAMES = {
    "Le Bernardin", "Per Se", "Eleven Madison Park", "Jungsik", "Jungsik New York",
    "The Modern", "Aquavit", "Gabriel Kreuther", "Jean-Georges", "Atomix",
    "Gramercy Tavern", "Cote", "Le Coucou", "Daniel",
}

roster = []
for stars, name, cuisine, slug in ROSTER_RAW:
    url = ROSTER_OVERRIDES.get(name, M(slug))
    individually_checked = name in DETAILED_NAMES
    if name == "Jungsik":
        verified_text = (
            "Yes — current official MICHELIN page 'Jungsik New York' shows " + stars +
            " stars (the 2025 ceremony article lists this restaurant as 'Jungsik')"
        )
    else:
        verified_text = (
            "Yes — current MICHELIN page shows " + stars + " star" + ("s" if stars != "1" else "")
        )
    roster.append({
        "name": name,
        "stars_2025": stars + " MICHELIN Star" + ("s" if stars != "1" else ""),
        "cuisine": cuisine,
        "michelin_url": url,
        "current_star_verified": verified_text if individually_checked else "",
        "sources": ["michelin_stars_2025"] + (["michelin_page_" + slug] if individually_checked else []),
        "flags": [] if individually_checked else [
            "Current (2026) star status for this individual restaurant was not checked against its current MICHELIN page; left blank."
        ],
    })

# ---------------------------------------------------------------------------
# Detailed restaurants — every field transcribed from the current official
# MICHELIN restaurant page and/or the restaurant's own official website.
# ---------------------------------------------------------------------------
def rest(name, stars, status, cuisine, address, zipcode, michelin_slug, official,
         days, hours, exceptions, price_two, price_basis, price_note, official_sources,
         michelin_sources, social, extra_flags=None, extra_sources=None):
    return {
        "name": name,
        "status": status,
        "stars": stars,
        "cuisine": cuisine,
        "address": address,
        "zip": zipcode,
        "michelin_url": M(michelin_slug),
        "official_url": official,
        "days_open": days,
        "hours": hours,
        "exceptions": exceptions,
        "price_two": price_two,
        "price_basis": price_basis,
        "price_note": price_note,
        "social": social,
        "sources": list(dict.fromkeys(
            ["michelin_page_" + michelin_slug] + michelin_sources + official_sources + (extra_sources or [])
        )),
        "flags": extra_flags or [],
    }


def yt(video_id, title, platform_source="youtube_lb"):
    return {"platform": "YouTube", "url": "https://www.youtube.com/watch?v=" + video_id,
            "title": title, "kind": "third-party review / tour", "via": platform_source}


def ytshort(video_id, title, platform_source="youtube_lb"):
    return {"platform": "YouTube Shorts", "url": "https://www.youtube.com/shorts/" + video_id,
            "title": title, "kind": "third-party short review", "via": platform_source}


def tk(handle, video_id, title, platform_source=""):
    return {"platform": "TikTok", "url": "https://www.tiktok.com/@" + handle + "/video/" + video_id,
            "title": title, "kind": "third-party review", "via": platform_source}


def ig(url, title, kind):
    return {"platform": "Instagram", "url": url, "title": title, "kind": kind, "via": ""}


detailed = [
    rest(
        "Le Bernardin", "3", "MICHELIN 3 Stars (current)", "Seafood",
        "155 W. 51st St., New York, NY 10019", "10019", "le-bernardin", "https://www.le-bernardin.com/",
        "Mon–Sat (closed Sunday)",
        "Mon–Thu 12–2:30 PM & 5–10:30 PM; Fri 12–2:30 PM & 5–11 PM; Sat 5–11 PM; Sun closed",
        "Sunday closed; lunch served Mon–Fri only (per MICHELIN hours table). Holiday exceptions not published on the fetched official pages.",
        "$700 / $540 / $284 (subtotal for 2 adults, before tax, gratuity and beverages)",
        "Chef's Tasting $350 pp ×2; Vegetarian Tasting $270 pp ×2; lunch prix fixe $142 pp ×2 — all from the official Le Bernardin menu PDF",
        "Arithmetic only (×2). The official PDF does not publish a 'total for two' and explicitly lists supplements; beverages, tax and gratuity are additional.",
        ["lb_lunch", "lb_lounge", "lb"], ["michelin_page_le-bernardin"],
        [
            yt("oZa5QrxUOM8", "French Girl Reviews America's Best French Restaurant (Le Bernardin)"),
            yt("eRPhZXnJCtQ", "Eating at Le Bernardin. NYC. 3 Michelin Stars. An Amazing 8 Course Tasting Menu"),
            yt("tsLvh8i_zdo", "UNDERCOVER at Le Bernardin! Honest Review"),
            yt("il_uUGZCx_o", "Inside New York's ICONIC Seafood Restaurant - Le Bernardin (3 Michelin Star)"),
            ytshort("zA54rMhEGOc", "Trying NYC's best restaurant - Le Bernardin review"),
            ytshort("8r3vmHAMkyQ", "Trying Every Restaurant on the NYT Top 100 List - Le Bernardin (#3)"),
            ytshort("LKUUmTCUn3M", "Reviewing the $350 pp Tasting Menu at Le Bernardin, NYC"),
            tk("eater", "7356398018435861803", "Eater: NYC's three-Michelin-starred Le Bernardin — halibut review"),
            tk("eater", "7208650857494138158", "Eater: three Michelin stars at Le Bernardin — pastry chef"),
            tk("beli_eats", "7207922985192164650", "Beli App: New York's most legendary fine dining restaurant, Le Bernardin"),
            tk("eater", "7355608034741161262", "Eater: the menu at three-Michelin-starred Le Bernardin"),
            tk("highspeeddining", "7499498465139887406", "High Speed Dining: Chef's Tasting Menu at Le Bernardin"),
        ],
        extra_sources=["youtube_lb"],
    ),
    rest(
        "Per Se", "3", "MICHELIN 3 Stars (current)", "Contemporary, French",
        "10 Columbus Circle, New York, NY 10019", "10019", "per-se", "https://www.thomaskeller.com/perseny/",
        "Monday–Sunday (all 7 days)", "4:30 PM–9 PM daily",
        "No exceptions published on the fetched MICHELIN page.",
        "", "", "No date-specific total for two published on the fetched official Per Se / Thomas Keller pages; left blank.",
        ["perseny"], ["michelin_page_per-se"],
        [yt("YOaJo5a-MCw", "Eating at Per Se. NYC. 3 Michelin Stars. 9 Course Tasting Menu", "")],
    ),
    rest(
        "Eleven Madison Park", "3", "MICHELIN 3 Stars (current)", "Contemporary, Vegan",
        "11 Madison Ave., New York, NY 10010", "10010", "eleven-madison-park", "https://www.elevenmadisonpark.com/",
        "Monday–Sunday (all 7 days)",
        "Mon–Thu 5:30–10 PM; Fri–Sun 12–1 PM & 5:30–11 PM (bar: Mon–Thu 5–10:30 PM; Fri–Sun 12–11 PM)",
        "Lunch service Fri–Sun only. Reservations open on the 1st of each month for the following month; all sales final, non-refundable; gratuity not included.",
        "$770 / $510 / $450 (subtotal for 2 adults, before tax, beverages and gratuity)",
        "Full Tasting $385 pp ×2; Bar Tasting $255 pp ×2; lounge Bar Tasting from $225 pp ×2 — all from the official EMP FAQ",
        "Arithmetic only (×2). The official FAQ states gratuity is not included and all sales are final; wine pairing from $125 pp is extra.",
        ["emp_faq", "emp"], ["michelin_page_eleven-madison-park"],
        [
            yt("8VM_9hEKHps", "Inside Eleven Madison Park: Why It's Trending Again", "youtube_emp"),
            yt("aSE3P9REZVc", "Eating at Eleven Madison Park. NYC. 3 Michelin Stars", "youtube_emp"),
            yt("NK88iwkvjfM", "200 Employees, 3 Michelin Stars: A Day at Eleven Madison Park | Bon Appétit", "youtube_emp"),
            ytshort("q8QfNCY2YZk", "POV: Solo Fine Dining at a Michelin Restaurant in NYC", "youtube_emp"),
            ytshort("2OVbiHIBlNA", "Honest Review Of A 3 Michelin Star Restaurant (Eleven Madison Park)", "youtube_emp"),
            ig("https://www.instagram.com/explore/locations/387651492/united-states/new-york-new-york/eleven-madison-park-restaurant/",
               "Instagram location page — Eleven Madison Park Restaurant (user photos/videos)", "platform location page (user posts)"),
        ],
        extra_sources=["youtube_emp"],
    ),
    rest(
        "Jungsik New York", "3", "MICHELIN 3 Stars (current)", "Korean, Contemporary",
        "2 Harrison St., New York, NY 10013", "10013", "jungsik-new-york", "https://www.jungsik.com/",
        "Tuesday–Sunday (closed Monday)", "Tue–Sun 5–9:30 PM; Mon closed",
        "Monday closed. No holiday exceptions published on the fetched official pages.",
        "", "", "No date-specific total for two published on the fetched official pages; left blank.",
        ["jungsik"], ["michelin_page_jungsik-new-york"],
        [yt("_Q56V0ISF5o", "Eating at Jungsik NYC. 3 Michelin Stars", ""),
         yt("-tvjMUPEXGk", "Trying NYC's Newest 3 Michelin Star Restaurant - Jungsik NYC Review", "")],
    ),
    rest(
        "The Modern", "2", "MICHELIN 2 Stars (current)", "Contemporary",
        "9 W. 53rd St., New York, NY 10019", "10019", "the-modern", "https://www.themodernnyc.com/the-modern/",
        "Monday–Sunday (all 7 days)",
        "Mon–Thu & Sun 12–2:30 PM & 5–9 PM; Fri–Sat 12–2:30 PM & 5–9:30 PM",
        "Friday/Saturday dinner service runs 30 minutes later; beverage, tax and gratuity are additional to menu prices.",
        "$230 / $370 / $570 / $690 / $510 (subtotal for 2 adults, before tax, gratuity and beverages)",
        "3-course prix fixe $115 pp; Impressions $185 pp; Abstractions $285 pp; Kitchen Table $345 pp; Lunch Tasting $255 pp — ×2 each, from the official menu",
        "Arithmetic only (×2). The official menu states 'Beverages, tax, and gratuity will be in addition'.",
        ["modern"], ["michelin_page_the-modern"],
        [yt("wM6sGPN4R0g", "Eating a Luxurious Tasting Menu at The Modern NYC", ""),
         yt("RTkrEpQ0iqA", "Eating at The Modern. NYC. Two Michelin Stars. Bar Room Menu", ""),
         yt("lq8mihouGlM", "Michelin 2 Star: The Modern NYC", ""),
         yt("IdIIURNscCM", "Eating 2 Michelin Starred Fried Chicken at The Modern", "")],
    ),
    rest(
        "Aquavit", "2", "MICHELIN 2 Stars (current)", "Scandinavian, Contemporary",
        "65 E. 55th St., New York, NY 10022", "10022", "aquavit", "https://www.aquavit.org/",
        "Monday–Saturday (closed Sunday)",
        "Mon–Thu 12–2 PM & 5:30–9 PM; Fri 12–2 PM & 5:30–9:30 PM; Sat 5–9:30 PM; Sun closed",
        "Sunday closed; Saturday dinner-only (no lunch).",
        "", "", "No date-specific total for two published on the fetched official pages; left blank.",
        [], ["michelin_page_aquavit"],
        [yt("wgscC-0tXT8", "Aquavit 2 Michelin Star NYC Restaurant Review", ""),
         yt("KJxbHfAxIuI", "How Chef Emma Bengtsson Runs a Two-Michelin-Starred Swedish Restaurant in NYC — Mise En Place", ""),
         yt("kE_g8jbne3I", "Chef Emma Bengtsson at Aquavit in New York", "")],
    ),
    rest(
        "Gabriel Kreuther", "2", "MICHELIN 2 Stars (current)", "French, Contemporary",
        "41 W. 42nd St., New York, NY 10036", "10036", "gabriel-kreuther", "https://www.gknyc.com/",
        "Monday–Saturday (closed Sunday)",
        "Mon 4:45–9:30 PM; Tue–Thu 11:45 AM–2:15 PM & 4:45–9:30 PM; Fri 11:45 AM–2:15 PM & 4:45–10 PM; Sat 4:45–10 PM; Sun closed",
        "Sunday closed; Monday and Saturday dinner-only (no lunch).",
        "", "", "No date-specific total for two published on the fetched official pages; left blank.",
        [], ["michelin_page_gabriel-kreuther"], [],
        extra_flags=["No YouTube/TikTok/Instagram review link could be verified for this restaurant from the platform pages fetched; social cells left blank."],
    ),
    rest(
        "Jean-Georges", "2", "MICHELIN 2 Stars (current)", "Contemporary, French Contemporary",
        "Trump International Hotel & Tower, 1 Central Park West, New York, NY 10023", "10023",
        "jean-georges", "https://www.jean-georgesrestaurant.com/",
        "Tuesday–Saturday (closed Sunday and Monday)",
        "Tue–Sat 12–2 PM & 5–9:30 PM; Sun–Mon closed",
        "Sunday and Monday closed.",
        "", "", "No date-specific total for two published on the fetched official pages; left blank.",
        [], ["michelin_page_jean-georges"], [],
        extra_flags=["No YouTube/TikTok/Instagram review link could be verified for this restaurant from the platform pages fetched; social cells left blank."],
    ),
    rest(
        "Atomix", "2", "MICHELIN 2 Stars (current)", "Korean, Contemporary",
        "104 E. 30th St., New York, NY 10016", "10016", "atomix", "https://www.atomixnyc.com/",
        "Tuesday–Saturday (closed Sunday and Monday)", "Tue–Sat 5:30 PM–12 AM; Sun–Mon closed",
        "Sunday and Monday closed.",
        "", "", "No date-specific total for two published on the fetched official pages; left blank.",
        ["atomix"], ["michelin_page_atomix"],
        [yt("aeC7HY4NFhI", "Inside Atomix: The Restaurant Elevating Korean Cuisine", ""),
         yt("ENBmmjRwaWY", "#5 Atomix - is a $1800 dinner for two worth it?", "")],
    ),
    rest(
        "Gramercy Tavern", "1", "MICHELIN 1 Star (current)", "Contemporary, American",
        "42 E. 20th St., New York, NY 10003", "10003", "gramercy-tavern", "https://www.gramercytavern.com/",
        "Monday–Sunday (all 7 days)", "Mon–Thu & Sun 5–9 PM; Fri–Sat 5–10 PM",
        "Friday/Saturday dinner until 10 PM.",
        "", "", "No date-specific total for two published on the fetched official pages; left blank.",
        [], ["michelin_page_gramercy-tavern"],
        [yt("gLunwbHmtTw", "Eating at Gramercy Tavern. A Classic NYC Michelin Starred Restaurant", ""),
         yt("hWGo7JDl1Tc", "Michelin Star dining experience: Gramercy Tavern in NYC", ""),
         yt("0u3zI5KvlPo", "I Tried NYC's Most Legendary Lunch Spot — Gramercy Tavern Review", ""),
         yt("UMaYPc5bnLQ", "Eating a $35 Michelin Starred Burger from Gramercy Tavern", "")],
    ),
    rest(
        "Cote", "1", "MICHELIN 1 Star (current)", "Korean, Steakhouse",
        "16 W. 22nd St., New York, NY 10010", "10010", "cote", "https://www.cotekoreansteakhouse.com/",
        "Monday–Sunday (all 7 days)", "Mon–Wed & Sun 5–11 PM; Thu–Sat 5 PM–12 AM",
        "Thursday–Saturday extended to midnight; official COTE FAQ states dinner service 7 days a week.",
        "", "", "No date-specific total for two published on the fetched official pages; left blank.",
        ["cote"], ["michelin_page_cote"],
        [
            yt("oAADFdfa-G4", "How Two Master Chefs Run the Only Michelin-Starred Korean Steakhouse — Mise En Place", "youtube_cote"),
            yt("psPhKYYQCgQ", "The Most HYPED Korean Steakhouse! Is COTE Worth the Hype?", "youtube_cote"),
            yt("3RDGsU8FT-I", "Trying the ONLY Michelin Star Korean BBQ in the World", "youtube_cote"),
            ytshort("7xwPHYZfF7k", "TRYING THE MOST FAMOUS KBBQ SPOT IN THE US? Cote Korean Steakhouse", "youtube_cote"),
            tk("eater", "7148838670869531947", "Eater: How NYC's Cote prepares its steak omakase", ""),
            ig("https://www.instagram.com/cotekoreansteakhouse/",
               "COTE Korean Steakhouse official Instagram account", "official account (not a third-party review)"),
        ],
        extra_sources=["youtube_cote"],
    ),
    rest(
        "Le Coucou", "1", "MICHELIN 1 Star (current)", "French",
        "11 Howard Hotel, 138 Lafayette St., New York, NY 10013", "10013", "le-coucou", "https://lecoucou.com/",
        "Monday–Sunday (all 7 days)",
        "Mon–Thu & Sun 11:30 AM–2:30 PM & 5–10 PM; Fri 11:30 AM–2 PM & 5–11 PM; Sat 11:30 AM–2:30 PM & 5–11 PM",
        "Friday lunch ends at 2 PM; Fri/Sat dinner until 11 PM. Located inside the 11 Howard hotel.",
        "", "", "No date-specific total for two published on the fetched official pages; left blank.",
        [], ["michelin_page_le-coucou"],
        [yt("C_8S5mCOAIk", "Eating at Le Coucou. One Michelin Star. The Most Popular French Restaurant in NYC", ""),
         yt("TFFz_71DNFM", "Trying Every Restaurant on the NYT Top 100 List - Le Coucou", ""),
         yt("F6UrQizJU7c", "I Only Ate at NYC Michelin Starred Restaurants for 24 Hours", "")],
    ),
    rest(
        "Daniel", "1", "MICHELIN 1 Star (current)", "French",
        "60 E. 65th St., New York, NY 10065", "10065", "daniel", "https://www.danielnyc.com/",
        "Tuesday–Sunday (closed Monday)", "Tue–Sun 5–9:30 PM; Mon closed",
        "Monday closed; dinner service only per the MICHELIN hours table.",
        "", "", "No date-specific total for two published on the fetched official pages; left blank.",
        [], ["michelin_page_daniel"], [],
        extra_flags=["No YouTube/TikTok/Instagram review link could be verified for this restaurant from the platform pages fetched; social cells left blank."],
    ),
]

# add per-restaurant MICHELIN page sources to the registry
for r in detailed:
    key = "michelin_page_" + r["michelin_url"].rsplit("/", 1)[-1]
    S.setdefault(key, {
        "id": key,
        "title": "MICHELIN Guide — " + r["name"] + " (current restaurant page)",
        "url": r["michelin_url"],
        "type": "official guide",
        "checked": CHECKED,
    })

guide_listed = [
    {
        "name": "Noury", "status": "Listed in the MICHELIN Guide (Selected, no star)",
        "added": "November 2026", "cuisine": "Japanese, Izakaya",
        "address": "137 Sullivan St., New York, NY 10012", "zip": "10012",
        "michelin_url": M("noury"), "official_url": "https://www.nourynewyork.com/",
        "days_open": "Monday–Sunday (all 7 days)",
        "hours": "Mon–Wed 5–10 PM; Thu–Sat 5–10:30 PM; Sun 5–9:30 PM",
        "exceptions": "Sunday closes 9:30 PM.",
        "price_two": "", "price_basis": "",
        "price_note": "MICHELIN price category $$$; no numeric total for two published on the fetched official pages; left blank.",
        "social": [],
        "sources": ["michelin_additions", "michelin_page_noury"],
        "flags": ["Guide-listed only: the current MICHELIN page shows no star icon. No verified social review link found."],
    },
    {
        "name": "Mūje", "status": "Listed in the MICHELIN Guide (Selected, no star)",
        "added": "November 2026", "cuisine": "Asian, Asian Influences",
        "address": "151 W. 30th St., New York, NY 10001", "zip": "10001",
        "michelin_url": M("muje"), "official_url": "https://www.mujenyc.com/",
        "days_open": "", "hours": "", "exceptions": "",
        "price_two": "", "price_basis": "",
        "price_note": "MICHELIN price category $$$$; no numeric total for two published on the fetched official pages; left blank.",
        "social": [],
        "sources": ["michelin_additions", "michelin_page_muje"],
        "flags": ["Guide-listed only: the current MICHELIN page shows no star icon.",
                  "The current MICHELIN page publishes no opening-hours table for this restaurant; days/hours left blank.",
                  "No verified social review link found."],
    },
    {
        "name": "Elder", "status": "Listed in the MICHELIN Guide (Selected, no star)",
        "added": "November 2026", "cuisine": "Contemporary Indian (per MICHELIN article)",
        "address": "Hudson Yards / Midtown West, Manhattan (street address not on fetched page)", "zip": "",
        "michelin_url": M("elder-1253266"), "official_url": "",
        "days_open": "", "hours": "", "exceptions": "", "price_two": "", "price_basis": "",
        "price_note": "Not published on the fetched official page; left blank.",
        "social": [],
        "sources": ["michelin_additions"],
        "flags": ["Guide-listed only (November 2026 new addition).", "Individual MICHELIN page not fetched; hours, address, official site and social links left blank."],
    },
    {
        "name": "Indienne NYC", "status": "Listed in the MICHELIN Guide (Selected, no star)",
        "added": "November 2026", "cuisine": "Indian (per MICHELIN article)",
        "address": "Hudson Yards / Midtown West, Manhattan (street address not on fetched page)", "zip": "",
        "michelin_url": M("indienne-nyc"), "official_url": "",
        "days_open": "", "hours": "", "exceptions": "", "price_two": "", "price_basis": "",
        "price_note": "Not published on the fetched official page; left blank.",
        "social": [],
        "sources": ["michelin_additions"],
        "flags": ["Guide-listed only (November 2026 new addition).", "Individual MICHELIN page not fetched; hours, address, official site and social links left blank."],
    },
    {
        "name": "Oriana", "status": "Listed in the MICHELIN Guide (Selected, no star)",
        "added": "November 2026", "cuisine": "American steakhouse (per MICHELIN article)",
        "address": "Nolita, Manhattan (street address not on fetched page)", "zip": "",
        "michelin_url": M("oriana"), "official_url": "",
        "days_open": "", "hours": "", "exceptions": "", "price_two": "", "price_basis": "",
        "price_note": "Not published on the fetched official page; left blank.",
        "social": [],
        "sources": ["michelin_additions"],
        "flags": ["Guide-listed only (November 2026 new addition).", "Individual MICHELIN page not fetched; hours, address, official site and social links left blank."],
    },
    {
        "name": "Nyonya", "status": "Bib Gourmand (MICHELIN Guide distinction, no star)",
        "added": "", "cuisine": "Malaysian",
        "address": "", "zip": "",
        "michelin_url": M("nyonya"), "official_url": "",
        "days_open": "", "hours": "", "exceptions": "", "price_two": "", "price_basis": "",
        "price_note": "MICHELIN price category $; no numeric total for two published on the fetched official page; left blank.",
        "social": [],
        "sources": ["howard_michelin"],
        "flags": ["Bib Gourmand is a MICHELIN Guide distinction, not a MICHELIN Star.",
                  "Individual restaurant page not fetched; hours, address, official site and social links left blank."],
    },
]

michelin = {
    "checked": CHECKED,
    "counts_current": {
        "note": "Counts displayed on the official MICHELIN Guide 'NYC All Starred Restaurants' page on 2026-11-25; the wider NYC selection page shows 369 restaurants total.",
        "three_star": 5, "two_star": 14, "one_star": 50, "starred_total": 69,
        "bib_gourmand": 76, "selected_restaurants": 224, "nyc_total": 369,
        "days_open_aggregate": {"Monday": 39, "Tuesday": 63, "Wednesday": 68, "Thursday": 69,
                                "Friday": 69, "Saturday": 69, "Sunday": 41},
        "sources": ["michelin_all_starred", "michelin_nyc"],
    },
    "roster": roster,
    "detailed": detailed,
    "guide_listed": guide_listed,
    "green_stars_2025": ["Blue Hill at Stone Barns", "Dirt Candy", "Family Meal at Blue Hill", "One White Street"],
    "status_note": (
        "'Starred' means the restaurant currently holds 1–3 MICHELIN Stars. 'Listed in the MICHELIN Guide' / "
        "'Selected restaurants' / 'Bib Gourmand' are Guide distinctions without a Star. The 2025 ceremony article "
        "is the source of the full star roster; the current all-starred listing is the source of current counts."
    ),
}

# ---------------------------------------------------------------------------
# Activities
# ---------------------------------------------------------------------------
activities = [
    {
        "name": "The Metropolitan Museum of Art (The Met Fifth Avenue)", "category": "Museum",
        "official_url": "https://www.metmuseum.org/plan-your-visit",
        "days_open": "Sun–Tue, Thu–Sat (closed Wednesday)",
        "hours": "Sun–Tue & Thu 10 AM–5 PM; Fri–Sat 10 AM–9 PM; Wed closed",
        "exceptions": "Closed Wednesdays; closed Thanksgiving Day, Dec 25, Jan 1 and the first Monday in May. General admission $30 adult (official).",
        "price_two": "$60 (2 × $30 adult general admission)",
        "price_note": "Arithmetic only from the official $30 adult admission. NY State residents pay what they wish.",
        "social": [
            yt("ZSkgmeOcSQ8", "Exploring the MET Museum NYC in 2 Hours!", "youtube_met"),
            yt("1tictAyrZLs", "What to See at the Metropolitan Museum of Art | Behind the Masterpiece", "youtube_met"),
            yt("8KLpB0-2vRc", "Top artworks to see at the Metropolitan Museum of Art | Tour of THE MET", "youtube_met"),
            tk("uktravel", "7430473965623151905", "uktravel: guided tour of the Met Museum (NYC top 5 experiences)", ""),
        ],
        "sources": ["met", "met_home", "youtube_met"],
        "flags": ["Full weekly hours taken from the official Met homepage hours block via a site-restricted search extract; 'closed Wednesdays' and $30 admission were confirmed by fetching the official homepage directly."],
    },
    {
        "name": "Museum of Modern Art (MoMA)", "category": "Museum",
        "official_url": "https://www.moma.org/visit/",
        "days_open": "Monday–Sunday (all 7 days)",
        "hours": "Mon–Thu, Sat–Sun 10:30 AM–5:30 PM; Fri 10:30 AM–8:30 PM",
        "exceptions": "Open every day except Thanksgiving and Christmas; galleries close ~15 min before closing; Uniqlo Friday Nights free for NY State residents 5:30–8:30 PM (reservation required).",
        "price_two": "$60 (2 × $30 adult admission)",
        "price_note": "Arithmetic only from the official $30 adult admission.",
        "social": [
            yt("iKhkApixPYA", "Is MoMA Worth It? | NYC Museum Tour", ""),
            yt("aFf3VzY8pZs", "Tour of the MoMA in NYC! Museum of Modern Art!", ""),
            yt("QBjtiwUnkgQ", "Museos de Nueva York — MoMA, MET, Guggenheim, Whitney (Spanish)", ""),
        ],
        "sources": ["moma"],
        "flags": ["No verified Instagram review link for MoMA; only confirmed YouTube review links are listed."],
    },
    {
        "name": "American Museum of Natural History", "category": "Museum",
        "official_url": "https://www.amnh.org/plan-your-visit/hours",
        "days_open": "Monday–Sunday (all 7 days)", "hours": "10 AM–5:30 PM daily",
        "exceptions": "Closed Thanksgiving Day and Christmas Day; extended holiday hours on select dates Nov 7–Jan 30; some halls close early on listed dates.",
        "price_two": "", "price_note": "Admission price not published on the fetched official hours page; left blank.",
        "social": [
            yt("UphcGvF-bsc", "American Museum of Natural History Tour & Review", ""),
            yt("KkvGwA7AA3w", "Exploring American Museum of Natural History New York", ""),
            yt("y_mchW6F59U", "American Museum of Natural History Tour - New York City", ""),
            yt("ZCDYLKZ3A3w", "NYC's Most Exciting Museum | Richard Gilder Center Tour", ""),
        ],
        "sources": ["amnh"],
        "flags": [],
    },
    {
        "name": "Statue of Liberty National Monument & Ellis Island", "category": "Landmark / ferry",
        "official_url": "https://www.nps.gov/stli/planyourvisit/hours.htm",
        "days_open": "Monday–Sunday (all 7 days)", "hours": "Every day 9 AM–4:30 PM; Liberty Island Information Center 9:30 AM–4:30 PM",
        "exceptions": "Accessible only by Statue City Cruises ferry; last entrance into the statue 3:30 PM. NPS 2026–2027 closures: Thanksgiving Day 26 Nov 2026 and Christmas Day 25 Dec 2026 (both closed). No 2027 holiday closures published yet.",
        "price_two": "", "price_note": "Ferry/ticket price not published on the fetched NPS hours page; left blank.",
        "social": [
            yt("F2z8jQFNTSg", "Exploring The Statue of Liberty - Full Crown Climb & Museum Walk | 2026 POV Guide", "youtube_sol"),
            yt("dU0NVGCbqf0", "Statue of Liberty - New York City - Tour and Review", "youtube_sol"),
            yt("0NvJo0Eqz-E", "Visit the Statue of Liberty | Step-by-Step Guide | NYC Travel Tips & Ferry Info", "youtube_sol"),
            tk("niredonahue", "7198607241627438379", "niredonahue: Statue of Liberty must-visit review and ferry tips", ""),
            ig("https://www.instagram.com/explore/locations/239164276/statue-of-liberty-liberty-island-ny/?hl=en",
               "Instagram location page — Statue of Liberty, Liberty Island (user photos/videos)", "platform location page (user posts)"),
        ],
        "sources": ["nps", "youtube_sol"],
        "flags": [],
    },
    {
        "name": "Empire State Building Observatory", "category": "Observation deck",
        "official_url": "https://www.esbnyc.com/visit/hours-of-operation",
        "days_open": "Open 365 days a year (all 7 days)", "hours": "",
        "exceptions": "Official page states 'We're open 365 days a year — rain or shine' and that hours depend on the visit date; it lists only near-term dated hours (Nov–Dec 2026), not February 2027. Doors close one hour before closing on listed dates.",
        "price_two": "", "price_note": "No date-specific February 2027 ticket price published on the fetched official page; left blank.",
        "social": [
            yt("6sxeqTNJ4T4", "Which view is better? Empire State, Top of the Rock or One World Observatory", ""),
            yt("axJol5qw6RA", "Why you should SKIP the Empire State Building (what to do instead)", ""),
            yt("BFDhRsXATKA", "NYC : Visite de L'EMPIRE STATE BUILDING (French)", ""),
            yt("jR9JmNWmD9I", "Las MEJORES VISTAS de Nueva York: ESB vs One World vs Top of the Rock (Spanish)", ""),
            tk("sarahfunkyy", "7296509191869451563", "sarahfunkyy: Is the Empire State Building worth your time and money?", ""),
            tk("jricevuto", "7286547772503887146", "jricevuto: Night View from Top of Empire State Building", ""),
        ],
        "sources": ["esb"],
        "flags": ["February 2027 hours are not published on the official hours page yet; the hours cell is intentionally blank."],
    },
    {
        "name": "Top of the Rock Observation Deck", "category": "Observation deck",
        "official_url": "https://www.rockefellercenter.com/tickets/top-of-the-rock-observation-deck/",
        "days_open": "Daily (all 7 days)", "hours": "8 AM–12 AM; last entry 11:10 PM",
        "exceptions": "Official ticket page states OPEN 8 AM – 12 AM; open 7 days a week, 365 days a year; Beam and SKYLIFT operate weather permitting.",
        "price_two": "$84 (2 × 'From $42' timed admission)",
        "price_note": "Arithmetic only from the official 'From $42' starting price; all-inclusive pass 'From $82'. Prices vary by date/time and are not confirmed for February 2027.",
        "social": [
            yt("PLEB6Oxm8Fs", "Top of the Rock: A Must-Do in NYC?", ""),
            yt("6sxeqTNJ4T4", "Which view is better? ESB, Top of the Rock or One World Observatory", ""),
            yt("DinHgYROLsM", "NYC Observation Decks - Ranking the Top 5", ""),
        ],
        "sources": ["toprock"],
        "flags": [],
    },
    {
        "name": "One World Observatory", "category": "Observation deck",
        "official_url": "https://www.oneworldobservatory.com/plan-your-visit/",
        "days_open": "Monday–Sunday (all 7 days)", "hours": "9 AM–9 PM daily",
        "exceptions": "Thanksgiving hours 12 PM–7 PM. Official page links MTA subway and bus maps for directions.",
        "price_two": "", "price_note": "Ticket price not published on the fetched official plan-your-visit page; left blank.",
        "social": [
            yt("jR9JmNWmD9I", "Las MEJORES VISTAS de Nueva York: ESB vs One World vs Top of the Rock", ""),
            yt("eCY0GFjhJ04", "Qual o melhor Observatório de New York? (Portuguese)", ""),
            ig("https://www.instagram.com/oneworldnyc/", "One World Observatory official Instagram account", "official account (not a third-party review)"),
        ],
        "sources": ["owo"],
        "flags": [],
    },
    {
        "name": "9/11 Memorial & Museum", "category": "Memorial / museum",
        "official_url": "https://www.911memorial.org/visit",
        "days_open": "Memorial: 7 days; Museum: Wed–Mon plus select Tuesdays",
        "hours": "Memorial 8 AM–8 PM daily; Museum 9 AM–7 PM, last entry 5:30 PM",
        "exceptions": "Museum open six days a week plus select Tuesdays; special/holiday hours published on a separate official page; advance ticket purchase required for the Museum; the Memorial is free.",
        "price_two": "", "price_note": "Museum ticket price not published on the fetched official visit page; left blank.",
        "social": [
            yt("YEx-6W_tZ4g", "I Visit The 9-11 Memorial & Museum In New York", ""),
            yt("VlzgBMCypCI", "9/11 Memorial Museum: An Exclusive Tour", ""),
            yt("uoP3gliJ7k0", "Witness Resilience and Heroism: Inside the 9/11 Memorial Museum Tour", ""),
        ],
        "sources": ["911"],
        "flags": [],
    },
    {
        "name": "The High Line", "category": "Park / walk",
        "official_url": "https://www.thehighline.org/visit/",
        "days_open": "Daily (all 7 days)", "hours": "Dec 1–Mar 31: 7 AM–8 PM (covers 15 Feb–23 Mar 2027)",
        "exceptions": "Apr 1–Nov 30: 7 AM–10 PM. Rail Yard Preserve between 30th and 34th Streets closes at dusk. Free to enter.",
        "price_two": "$0 (free public park)",
        "price_note": "The official visitor page states the park is free; no ticket price is listed.",
        "social": [
            yt("RyvFc_Aht8Y", "ULTIMATE Guide To The High Line in NYC (20 Things To See & Walking Tour)", ""),
            yt("Rsasw3uey3g", "Windy But Wonderful 'High Line' - New York, USA 4K walking tour", ""),
            yt("CJOu79IIBLE", "New York City - 'The High Line' walk under 15 MIN!", ""),
            yt("rN3KEddbWFE", "The High Line NYC: Architecture Walking Tour", ""),
        ],
        "sources": ["highline"],
        "flags": [],
    },
    {
        "name": "Whitney Museum of American Art", "category": "Museum",
        "official_url": "https://whitney.org/visit",
        "days_open": "Mon, Wed–Sun (closed Tuesday)",
        "hours": "Mon, Wed, Thu, Sat, Sun 10:30 AM–6 PM; Fri 10:30 AM–10 PM; Tue closed",
        "exceptions": "Closed Tuesdays (with published extra December Tuesday openings); Free Friday Nights 5–10 PM; free for ages 25 and under; holiday hours listed on the official page.",
        "price_two": "$60 (2 × $30 adult admission)",
        "price_note": "Arithmetic only from the official $30 adult admission.",
        "social": [yt("NGBSYkjjDHE", "Art That Changed America — Whitney Museum one-hour tour", "")],
        "sources": ["whitney"],
        "flags": [],
    },
    {
        "name": "Central Park", "category": "Park / walk",
        "official_url": "https://www.nycgovparks.org/parks/central-park",
        "days_open": "", "hours": "",
        "exceptions": "NYC Parks official page lists park location (5th Ave to Central Park West, 59th to 110th St), amenities and ZIP codes, but no park hours on the fetched page.",
        "price_two": "", "price_note": "Admission price not published on the fetched official page; left blank.",
        "social": [yt("-rEdKq0uHFU", "3rd Day In New York: First Subway Experience, Strolling In Central Park and 9/11 Memorial", "")],
        "sources": ["centralpark"],
        "flags": ["NYC Parks did not publish opening hours on the fetched official page; days/hours intentionally blank."],
    },
]

# Remove an accidental placeholder Instagram entry (kept empty on purpose if no match).
for a in activities:
    a["social"] = [s for s in a["social"] if s.get("url")]

# ---------------------------------------------------------------------------
# Hotels
# ---------------------------------------------------------------------------
hotels = [
    {
        "name": "Pod 51 Hotel", "area": "Midtown East",
        "address": "230 E 51st St, New York, NY (official location page; ZIP not published there)", "zip": "",
        "official_url": "https://www.thepodhotel.com/pod-51",
        "booking_url": "https://be.synxis.com/?chain=12484&hotel=41155",
        "private_bath": "Yes — Queen Pod, Full Pod, Double Full Pod, Studio Pod and Veranda Pod all list a private bathroom; some Bunk/Single Pods have shared baths",
        "bed": "Queen bed (Queen Pod); other room types offer full, two full, or one queen + twin",
        "amenities": "Private bathroom with rain showerhead, hairdryer, air conditioning, two flat-screen TVs with cable, work desk + chair, laptop-sized safe; rooftop deck, outdoor garden, free walking tours, same-day luggage storage",
        "fees": "Facility fee $29.84 (incl. tax) per room per night, in addition to the room rate (official FAQ)",
        "transit": "6 / E / M trains at Lexington Ave–E 53rd St; M50, M101, M102, M103 buses (official location/FAQ pages)",
        "price_7n": "",
        "price_note": "No 15–22 Feb 2027 rate could be confirmed from the official booking widget in this session; left blank. Official booking link provided for manual rate check.",
        "days_open": "", "hours": "", "exceptions": "Check-in 3:00 PM, check-out 1:00 PM (official FAQ).",
        "social": [],
        "sources": ["pod51", "pod51_rooms", "pod51_faq", "pod51_location"],
        "flags": ["ZIP code not published on the fetched official hotel pages; cluster matching cannot be verified.",
                  "7-night total price unverified.",
                  "No verified social review link found for this hotel."],
    },
    {
        "name": "11 Howard", "area": "SoHo",
        "address": "11 Howard Street, New York City, NY (Michelin Guide hotel page)", "zip": "",
        "official_url": "https://www.11howard.com/",
        "booking_url": "https://booking.11howard.com/",
        "private_bath": "", "bed": "",
        "amenities": "207 guest rooms and suites (official hotel site), library/co-working space, bar, Le Coucou (1 MICHELIN Star) in the building; MICHELIN Guide hotel page lists 213 rooms and a guest score of 18.1/20",
        "fees": "",
        "transit": "",
        "price_7n": "",
        "price_note": "No 15–22 Feb 2027 rate could be confirmed from the official booking site in this session; left blank.",
        "days_open": "", "hours": "", "exceptions": "",
        "social": [],
        "sources": ["howard", "howard_michelin", "michelin_page_le-coucou"],
        "flags": ["Irregularity: the official hotel site says 207 rooms while the MICHELIN Guide hotel page says 213 rooms — needs review.",
                  "Private bathroom and bed size are not stated on the fetched official pages; left blank.",
                  "ZIP code and 7-night total price unverified.",
                  "No verified social review link found for this hotel."],
    },
    {
        "name": "Arlo NoMad", "area": "NoMad",
        "address": "11 E. 31st St., Manhattan, NY 10016 (official NYC Tourism listing)", "zip": "10016",
        "official_url": "https://www.nyctourism.com/hotel-week/arlo-hotel-nomad/",
        "booking_url": "https://book.arlohotels.com/?chain=19470&hotel=70017&promo=NYCHOTELWEEK",
        "private_bath": "", "bed": "",
        "amenities": "250 modern micro guestrooms (150 sq ft), complimentary WiFi, Blind Barber bath amenities, custom walnut furnishings, 31st-floor rooftop bar A.R.T., Lamalo restaurant, complimentary Arlo bicycles",
        "fees": "", "transit": "",
        "price_7n": "",
        "price_note": "No 15–22 Feb 2027 rate could be confirmed; left blank. The NYC Hotel Week 25% offer applies only 2 Jan–11 Feb 2027, outside the requested trip window.",
        "days_open": "", "hours": "", "exceptions": "",
        "social": [],
        "sources": ["arlo_nomad", "hotel_week", "hotel_week_about"],
        "flags": ["Private bathroom and bed size are not stated on the fetched official listing; left blank.",
                  "7-night total price unverified.",
                  "No verified social review link found for this hotel."],
    },
    {
        "name": "citizenM New York Times Square", "area": "Times Square / Midtown West",
        "address": "", "zip": "",
        "official_url": "https://www.marriott.com/brands/citizenm.mi",
        "booking_url": "https://www.marriott.com/brands/citizenm/locations.mi",
        "private_bath": "",
        "bed": "XL king bed in every room (official Marriott / citizenM brand page)",
        "amenities": "Wall-to-wall XL king bed, in-room power shower and vanity, smart-tablet room controls, 24/7 canteenM food & drinks, self check-in, living rooms, free Wi-Fi",
        "fees": "", "transit": "",
        "price_7n": "",
        "price_note": "No 15–22 Feb 2027 rate could be confirmed from the official site in this session; left blank.",
        "days_open": "", "hours": "", "exceptions": "",
        "social": [],
        "sources": ["citizenm"],
        "flags": ["The fetched official page is the citizenM brand page, not the Times Square property page; property address and ZIP are unverified.",
                  "Private bathroom wording is not explicit on the fetched brand page (in-room shower/vanity shown, but not labeled 'private bathroom'); left blank.",
                  "7-night total price unverified.",
                  "No verified social review link found for this hotel."],
    },
    {
        "name": "AC Hotel New York Times Square", "area": "Garment District",
        "address": "", "zip": "",
        "official_url": "https://www.nyctourism.com/hotel-week/",
        "booking_url": "https://bit.ly/ACTS2027HOTELWEEK",
        "private_bath": "", "bed": "",
        "amenities": "Private balconies and angled ceiling-to-floor windows (official NYC Tourism Hotel Week listing)",
        "fees": "", "transit": "",
        "price_7n": "",
        "price_note": "No 15–22 Feb 2027 rate could be confirmed; left blank. Hotel Week 25% offer applies 2 Jan–11 Feb 2027 only.",
        "days_open": "", "hours": "", "exceptions": "",
        "social": [],
        "sources": ["ac_hotel", "hotel_week"],
        "flags": ["Private bathroom, bed size, address and 7-night price not published on the fetched official listing; left blank.",
                  "No verified social review link found for this hotel."],
    },
    {
        "name": "The Westin New York at Times Square", "area": "Times Square / Theatre District",
        "address": "", "zip": "",
        "official_url": "https://www.nyctourism.com/hotel-week/",
        "booking_url": "https://www.marriott.com/event-reservations/reservation-link.mi?id=1767810805266&key=CORP&app=resvlink",
        "private_bath": "", "bed": "",
        "amenities": "Ideally located in Times Square, in the heart of Midtown Manhattan (official NYC Tourism Hotel Week listing)",
        "fees": "", "transit": "",
        "price_7n": "",
        "price_note": "No 15–22 Feb 2027 rate could be confirmed; left blank. Hotel Week 25% offer applies 2 Jan–11 Feb 2027 only.",
        "days_open": "", "hours": "", "exceptions": "",
        "social": [],
        "sources": ["westin", "hotel_week"],
        "flags": ["Private bathroom, bed size, address and 7-night price not published on the fetched official listing; left blank.",
                  "No verified social review link found for this hotel."],
    },
]

# ---------------------------------------------------------------------------
# Trip dates
# ---------------------------------------------------------------------------
trip = {
    "checked": CHECKED,
    "party": "2 adults (couple)",
    "options": [
        {"id": "A", "name": "Preferred short stay", "check_in": "2027-02-15", "check_out": "2027-02-18",
         "weekday_in": "Monday", "weekday_out": "Thursday", "nights": 3,
         "note": "Matches the stated preferred vacation time (Feb 15–18, 2027). Check-in day is a U.S. federal holiday (Washington's Birthday).",
         "sources": ["opm"]},
        {"id": "B", "name": "Primary 7-night stay (used for hotel costing)", "check_in": "2027-02-15", "check_out": "2027-02-22",
         "weekday_in": "Monday", "weekday_out": "Monday", "nights": 7,
         "note": "1-week option inside the allowed window; the 7-night stay requested for hotel pricing.",
         "sources": ["opm"]},
        {"id": "C", "name": "Two-week stay", "check_in": "2027-02-15", "check_out": "2027-03-01",
         "weekday_in": "Monday", "weekday_out": "Monday", "nights": 14,
         "note": "2-week option, still inside the 15 Feb–23 Mar 2027 window.",
         "sources": ["opm"]},
        {"id": "D", "name": "Four-week stay", "check_in": "2027-02-15", "check_out": "2027-03-15",
         "weekday_in": "Monday", "weekday_out": "Monday", "nights": 28,
         "note": "Upper end of the optional 2–4 week extension; ends 8 days before the 23 Mar 2027 window close.",
         "sources": ["opm"]},
    ],
    "window": {"start": "2027-02-15", "end": "2027-03-23",
               "note": "Weekday values were computed with Python's datetime (not estimated)."},
    "verified_facts": [
        {"fact": "Monday 15 February 2027 is 'Washington's Birthday', a U.S. federal holiday.",
         "sources": ["opm"]},
        {"fact": "NYC Hotel Week 2027 runs 2 January – 11 February 2027 with 25% off standard room rates at participating hotels; reservations opened 17 November 2026.",
         "sources": ["hotel_week", "hotel_week_about", "hotel_week_press"]},
        {"fact": "NYC Restaurant Week, Broadway Week and Must-See Week run 19 January – 11 February 2027 with reservations opening 6 January 2027 at 10am ET.",
         "sources": ["hotel_week", "hotel_week_press"]},
        {"fact": "The only officially verified city-wide hotel discount window ends 4 days before the earliest allowed check-in date of 15 February 2027.",
         "sources": ["hotel_week", "hotel_week_about"]},
    ],
    "cheapest_booking_window": {
        "answer": "The only officially published city-wide cheapest booking window is NYC Hotel Week: stays 2 January – 11 February 2027 (25% off standard rates), with reservations open since 17 November 2026. It does NOT overlap the requested 15 February – 23 March 2027 travel window.",
        "best_time_to_book_for_requested_dates": "",
        "note": "No official source publishes a verified 'best time to book' or a lowest price for stays beginning 15 February 2027. Left blank; flagged for review.",
        "sources": ["hotel_week", "hotel_week_about", "hotel_week_press"],
    },
    "flags": [
        "No official source confirms the cheapest date to book a stay that starts on/after 15 February 2027; the value is blank.",
        "All four date options start on a U.S. federal holiday; impact on hotel rates, crowds and opening hours is not verified.",
    ],
}

# ---------------------------------------------------------------------------
# Analysis: verified clusters + blocked travel-time ranking
# ---------------------------------------------------------------------------
zip_clusters = {}
for r in detailed:
    zip_clusters.setdefault(r["zip"], []).append({"name": r["name"], "stars": r["stars"],
                                                  "michelin_url": r["michelin_url"]})
analysis = {
    "checked": CHECKED,
    "method": (
        "Only official data is used. MICHELIN restaurant pages publish street addresses incl. ZIP codes; "
        "those addresses are grouped below to show where starred restaurants cluster. The 'within 1 hour by "
        "subway or bus' test requires a dated route/time result from the MTA Trip Planner, which is not a static "
        "official value. Because the rule says never infer or fill in values, the travel-time-based counts and the "
        "Michelin-density hotel ranking are left blank and flagged unverified. A verified-attribute ranking is given "
        "instead: it counts only requirement fields actually confirmed on official pages."
    ),
    "zip_clusters": [{"zip": z, "count": len(v), "restaurants": v} for z, v in sorted(zip_clusters.items())],
    "cluster_scope": "13 starred restaurants whose current MICHELIN pages were fetched and verified line by line (sample of the 69 starred restaurants in the current official listing).",
    "travel_time": {
        "value": "",
        "status": "unverified",
        "why": "MTA does not publish a static hotel→restaurant travel-time matrix; the official Trip Planner computes a dated, time-specific result and requires a manual query.",
        "sources": ["mta_maps", "mta_trip", "mta_riding"],
    },
    "michelin_density_ranking": [],
    "verified_attribute_ranking": [],
    "verified_attribute_rule": (
        "1 point each for: private bathroom confirmed; queen-or-larger bed confirmed; street address confirmed "
        "on an official page; ZIP code confirmed on an official page; official transit information confirmed; "
        "an official room rate/fee published. Only fields with a non-blank official value score. This is a count "
        "of verified information, not a quality score and not a Michelin-density ranking."
    ),
    "sources": ["michelin_all_starred", "mta_maps", "mta_trip", "mta_riding", "hotel_week"],
}

# ---------------------------------------------------------------------------
# Questions / information / answers
# ---------------------------------------------------------------------------
questions = [
    {"id": "Q01", "question": "Which exact dates should we book?",
     "have": "Preferred 15–18 Feb 2027; allowed window 15 Feb–23 Mar 2027; 1–2 weeks requested, 2–4 weeks acceptable; 15 Feb 2027 is a U.S. federal holiday.",
     "answer": "Not decidable yet. Four concrete date options with real weekdays are presented on the Dates page, but no hotel rate comparison exists to choose between them.",
     "missing": "Verified 7-night/14-night hotel totals for each option; flight/arrival times; whether the federal holiday affects price or closures.",
     "discover": "Run each option through the official hotel booking links with 2 adults and record the dated quote; check official venue holiday calendars for 15 Feb 2027.",
     "sources": ["opm", "hotel_week"], "blocks_decision": True},
    {"id": "Q02", "question": "What is the total hotel cost for 7 nights for 2 adults?",
     "have": "Official hotel pages, official booking links, and one published fee (Pod 51 facility fee $29.84 per room per night incl. tax).",
     "answer": "Blank / unverified. No dated rate could be confirmed from an official hotel site in this session; no estimate was invented.",
     "missing": "A dated, official, all-in quote (room + taxes + fees) for 15–22 Feb 2027 for each candidate hotel.",
     "discover": "Use each hotel's official booking link with 2 adults and the exact dates; save a dated screenshot/quote and link it in the row.",
     "sources": ["pod51_faq", "hotel_week"], "blocks_decision": True},
    {"id": "Q03", "question": "When is the cheapest upcoming time to book a hotel, and what is the best time to book?",
     "have": "NYC Hotel Week 2027: 2 Jan–11 Feb 2027, 25% off standard rates, reservations open 17 Nov 2026 (official NYC Tourism).",
     "answer": "The only verified cheapest window is 2 Jan–11 Feb 2027, which ends before the earliest allowed check-in (15 Feb 2027). No verified best-time-to-book value exists for the requested window.",
     "missing": "A 2027 rate calendar or official statement about price movements for stays after 15 Feb 2027.",
     "discover": "Ask NYC Tourism and the hotels directly; record dated official quotes across several booking dates; do not rely on third-party 'best time to book' claims.",
     "sources": ["hotel_week", "hotel_week_about", "hotel_week_press"], "blocks_decision": True},
    {"id": "Q04", "question": "Does each candidate hotel have a private bathroom and a queen-or-larger bed?",
     "have": "Pod 51 Queen Pod: queen bed + private bathroom (official rooms page). citizenM: XL king bed (official brand page).",
     "answer": "Only 2 of 6 hotels have a bed/bath value verified; 4 are blank. citizenM's private bathroom wording is not explicit.",
     "missing": "Room-type specifications for the other hotels from their own official room pages.",
     "discover": "Fetch each hotel's official room-type page and quote the bed and bathroom wording verbatim.",
     "sources": ["pod51_rooms", "citizenm"], "blocks_decision": True},
    {"id": "Q05", "question": "How many MICHELIN restaurants are within 1 hour by subway or bus of each hotel?",
     "have": "Official MICHELIN addresses for 13 starred restaurants; official MTA maps, Trip Planner and 24/7 subway information; official transit statements for Pod 51.",
     "answer": "Blank / unverified. MTA travel time is date/time-specific and no static official value exists; the rule forbids inference.",
     "missing": "Dated Trip Planner results for every hotel→restaurant pair, or an official MTA data feed with travel times.",
     "discover": "Run the MTA Trip Planner for each pair on the chosen travel date/time and record the result; or use an official MTA GTFS/static timetable with a documented calculation.",
     "sources": ["michelin_all_starred", "mta_maps", "mta_trip", "mta_riding", "pod51_location"],
     "blocks_decision": True},
    {"id": "Q06", "question": "Will the MICHELIN star list still be current in February 2027?",
     "have": "2025 official star article; current official listing shows 69 starred (5/14/50); official new-additions article dated 18 Nov 2026; a third-party report says the next NYC ceremony is 14 Dec 2026.",
     "answer": "Not decidable. A reported December 2026 ceremony would fall after this review and before the trip; the report is not an official MICHELIN source, so it is flagged, not used as a fact.",
     "missing": "An official MICHELIN announcement of the 2026 New York selection and its date.",
     "discover": "Re-check the official MICHELIN Guide NYC star list immediately before booking; log the check date in the table.",
     "sources": ["michelin_stars_2025", "michelin_all_starred", "michelin_additions"],
     "blocks_decision": True},
    {"id": "Q07", "question": "Are the restaurant prices really 'total for two'?",
     "have": "Official menu prices per person for Le Bernardin, Eleven Madison Park, The Modern; official statements that tax, gratuity and beverages are additional.",
     "answer": "The published figures are menu subtotals for 2 (per-person price × 2), not a final check total. They are labeled that way everywhere on the site.",
     "missing": "Tax rate, service/gratuity policy and beverage choices for the actual booking.",
     "discover": "Ask each restaurant for a written quote for 2 on the chosen date, including tax and service; replace subtotal with the confirmed total.",
     "sources": ["lb_lunch", "emp_faq", "modern"], "blocks_decision": False},
    {"id": "Q08", "question": "Which restaurants are only listed in the Guide versus actually holding a Star?",
     "have": "Official 2025 star article, current all-starred listing (69), current selection counts (76 Bib Gourmand / 224 Selected), and November 2026 new additions.",
     "answer": "Answered for the 13 detailed starred restaurants and the 6 Guide-listed examples; per-name current status is not verified for the remaining ~58 names on the 2025 roster.",
     "missing": "A current official page check for each of the other roster names.",
     "discover": "Fetch each current MICHELIN restaurant page and record the star icons; update the roster's 'current star verified' column.",
     "sources": ["michelin_stars_2025", "michelin_all_starred", "michelin_nyc", "michelin_additions"],
     "blocks_decision": False},
    {"id": "Q09", "question": "Will restaurants and attractions be open on the actual travel dates?",
     "have": "Verified weekly hours and published exceptions for 13 restaurants and 11 activities; e.g. The High Line winter hours 7 AM–8 PM cover the whole window; NPS 2026–2027 holiday closures.",
     "answer": "Partially answered. February 2027-specific hours are published for The High Line but not for the Empire State Building or for 2027 holiday exceptions at most venues.",
     "missing": "February 2027 dated hours and holiday/closure calendars from each official venue.",
     "discover": "Re-check each official hours page in January 2027 and record the dated publication; add a 'last checked' column.",
     "sources": ["highline", "esb", "nps", "moma", "amnh", "whitney", "911"],
     "blocks_decision": False},
    {"id": "Q10", "question": "Is every table row backed by an official source link?",
     "have": "A source registry with each official page fetched and checked on 2026-11-25.",
     "answer": "Yes — the generator refuses to emit a row without at least one official source link. Blank values are rendered as unverified and listed on the Flagged page.",
     "missing": "Nothing for this question; ongoing re-verification is needed as official pages change.",
     "discover": "Run tools/build_site.py and tools/verify.py before every publish; resolve any new flag.",
     "sources": ["michelin_all_starred"], "blocks_decision": False},
    {"id": "Q11", "question": "Are the social links genuine reviews on the requested platforms?",
     "have": "YouTube search pages fetched directly from youtube.com; TikTok video pages fetched directly from tiktok.com; Instagram location/account pages found on instagram.com.",
     "answer": "Partially answered. Verified YouTube and TikTok review links exist for most entries; Instagram is limited to official accounts/location pages, and 3 restaurants + Central Park have no verified review link.",
     "missing": "Instagram/TikTok review links for the blank rows; confirmation that linked videos are still available.",
     "discover": "Repeat platform-restricted searches for the flagged entries and open each resulting URL before adding it; record the check date.",
     "sources": ["youtube_lb", "youtube_emp", "youtube_cote", "youtube_met", "youtube_sol"],
     "blocks_decision": False},
    {"id": "Q12", "question": "Can we keep every planned activity within 1 hour of the hotel?",
     "have": "Official activity locations and official MTA subway/bus route information on several venue pages.",
     "answer": "Not decidable. No dated MTA travel-time results exist for this trip; no travel-time value was invented.",
     "missing": "A dated itinerary with Trip Planner results for every hotel→activity leg.",
     "discover": "Build the itinerary day by day and record each official Trip Planner result; flag legs over 60 minutes.",
     "sources": ["mta_trip", "mta_maps", "centralpark", "owo"], "blocks_decision": True},
]

# ---------------------------------------------------------------------------
# Suggestions (for review before implementation)
# ---------------------------------------------------------------------------
suggestions = [
    {"id": "S01", "title": "Add a dated 'official quote' workflow for hotel prices",
     "problem": "All 7-night totals are blank because no official dated rate could be captured.",
     "proposal": "Add a quote-capture table (hotel, dates, 2 adults, quoted total incl. taxes/fees, official URL, capture timestamp) and fill it from official booking pages.",
     "decision_needed": "Approve a rate-check cadence (daily/weekly) and who records quotes; choose whether to permit screenshots as evidence.",
     "effort": "Medium", "priority": "P0", "status": "proposed — awaiting review"},
    {"id": "S02", "title": "Integrate MTA Trip Planner results as a first-class data source",
     "problem": "The requested Michelin-density ranking is blocked: travel time is not a static official value.",
     "proposal": "Store per-pair Trip Planner results with travel date/time and a link, then compute the ≤60-minute counts from those stored verified values only.",
     "decision_needed": "Choose the reference date/time (e.g. Tue 16 Feb 2027, 6:00 PM) and whether to include bus-only routes.",
     "effort": "High", "priority": "P0", "status": "proposed — awaiting review"},
    {"id": "S03", "title": "Add a 'last verified' date and change-detection to every row",
     "problem": "Official hours, prices and star ratings change; a 2026-11-25 snapshot can go stale before Feb 2027.",
     "proposal": "Add last-checked timestamps and a re-verification checklist to run in January 2027 and again 7 days before travel.",
     "decision_needed": "Approve the re-verification dates and the owner.",
     "effort": "Low", "priority": "P1", "status": "proposed — awaiting review"},
    {"id": "S04", "title": "Separate 'menu subtotal' from 'final total' in restaurant pricing",
     "problem": "Official menus publish per-person prices and state that tax/gratuity/beverages are extra.",
     "proposal": "Add explicit columns for menu subtotal, tax, service, beverages and confirmed final total; only fill a column when an official source states it.",
     "decision_needed": "Confirm whether to request written quotes from restaurants or use published menu subtotals only.",
     "effort": "Low", "priority": "P1", "status": "proposed — awaiting review"},
    {"id": "S05", "title": "Complete Instagram/TikTok coverage for every listed entry",
     "problem": "Several rows have no verified social review link, and Instagram currently has only official accounts/location pages.",
     "proposal": "Add platform-restricted searches per entry, open each candidate URL, and label review vs official account; never add an unopened URL.",
     "decision_needed": "Decide whether official accounts/location pages count as acceptable social links, or third-party reviews only.",
     "effort": "Medium", "priority": "P2", "status": "proposed — awaiting review"},
    {"id": "S06", "title": "Publish the full 69-restaurant current star check",
     "problem": "Only 13 of the 2025 roster names were checked against their current MICHELIN pages.",
     "proposal": "Fetch the remaining current pages, record star icons, and replace blank 'current star verified' cells.",
     "decision_needed": "Approve the time budget and whether to include Westchester/Brooklyn/Queens entries in the cluster analysis.",
     "effort": "Medium", "priority": "P1", "status": "proposed — awaiting review"},
    {"id": "S07", "title": "Resolve the 11 Howard room-count conflict",
     "problem": "Official hotel site says 207 rooms; MICHELIN Guide hotel page says 213 rooms.",
     "proposal": "Contact the hotel or check a newer official room inventory page; keep both cited values until one is confirmed.",
     "decision_needed": "Choose which official source is authoritative for the site.",
     "effort": "Low", "priority": "P2", "status": "proposed — awaiting review"},
    {"id": "S08", "title": "Add a decision dashboard with explicit go/no-go gates",
     "problem": "Important unknowns are spread across pages; a reviewer cannot see at a glance which decisions are blocked.",
     "proposal": "Add a compact 'decision gates' panel: dates, budget, hotel shortlist, itinerary, reservations — each marked ready / blocked with a link to the blocking question.",
     "decision_needed": "Approve the gate list and their order.",
     "effort": "Low", "priority": "P1", "status": "proposed — awaiting review"},
    {"id": "S09", "title": "Add a mobile 'trip mode' view",
     "problem": "Full comparison tables are wide on a phone.",
     "proposal": "Add a card view with one entry per card, sticky day headers, and a 'show unverified only' toggle.",
     "decision_needed": "Choose the default view (table vs cards) for small screens.",
     "effort": "Medium", "priority": "P2", "status": "proposed — awaiting review"},
    {"id": "S10", "title": "Reconcile parallel-session site outputs before final publish",
     "problem": "Two sessions own non-overlapping scopes (root site vs docs/ dashboard); two indexes could confuse users.",
     "proposal": "Final integration session merges branches, keeps one navigation/index, re-verifies combined tables, checks links, and re-points GitHub Pages.",
     "decision_needed": "Choose the canonical Pages source and landing page.",
     "effort": "Medium", "priority": "P1", "status": "proposed — awaiting review"},
]

# ---------------------------------------------------------------------------
# Flags / repo review
# ---------------------------------------------------------------------------
flags = [
    {"id": "F01", "severity": "high", "title": "Hotel 7-night prices are unverified",
     "detail": "No dated official rate for 15–22 Feb 2027 could be captured from any official hotel booking page in this session. Every total is blank; no estimate was substituted.",
     "sources": ["hotel_week", "pod51_faq"], "page": "hotels.html"},
    {"id": "F02", "severity": "high", "title": "Cheapest official booking window falls outside the trip window",
     "detail": "NYC Hotel Week 2027 discount applies 2 Jan–11 Feb 2027. The requested window starts 15 Feb 2027. The verified discount cannot be used for the requested dates.",
     "sources": ["hotel_week", "hotel_week_about"], "page": "dates.html"},
    {"id": "F03", "severity": "high", "title": "Michelin-density hotel ranking blocked",
     "detail": "The ≤1-hour subway/bus criterion needs dated MTA Trip Planner results. No static official value exists, so counts and ranking are blank rather than inferred.",
     "sources": ["mta_trip", "mta_maps"], "page": "travel.html"},
    {"id": "F04", "severity": "medium", "title": "2025 star roster vs current official count mismatch",
     "detail": "The official 2025 ceremony article lists 5 three-star, 15 two-star and 51 one-star restaurants (71 names, including Westchester and Brooklyn entries). The current official all-starred listing shows 69 starred (5/14/50). Per-name current status was verified only for 13 restaurants; the remaining names are flagged unverified.",
     "sources": ["michelin_stars_2025", "michelin_all_starred"], "page": "michelin.html"},
    {"id": "F05", "severity": "medium", "title": "Reported December 2026 MICHELIN ceremony is not an official source",
     "detail": "A third-party page reports the next New York star announcement for 14 Dec 2026. No official MICHELIN announcement was fetched, so this is logged as a question, not a fact.",
     "sources": ["michelin_additions", "michelin_all_starred"], "page": "questions.html"},
    {"id": "F06", "severity": "medium", "title": "11 Howard room-count conflict",
     "detail": "Official hotel website: 207 guest rooms and suites. MICHELIN Guide hotel page: 213 rooms. Both are cited; neither was corrected.",
     "sources": ["howard", "howard_michelin"], "page": "hotels.html"},
    {"id": "F07", "severity": "medium", "title": "Empire State Building February 2027 hours not published",
     "detail": "The official hours page states it is open 365 days and lists near-term Nov–Dec 2026 hours only; no February 2027 hours are published. Hours cell is blank.",
     "sources": ["esb"], "page": "activities.html"},
    {"id": "F08", "severity": "low", "title": "Instagram review coverage incomplete",
     "detail": "Instagram site-restricted searches returned official accounts/location pages rather than third-party reviews. Such links are labeled 'official account' and are not presented as reviews.",
     "sources": ["youtube_lb"], "page": "social.html"},
    {"id": "F09", "severity": "low", "title": "Central Park hours not published on official page",
     "detail": "NYC Parks Central Park page lists location, facilities and ZIP codes but no opening hours. Days/hours left blank.",
     "sources": ["centralpark"], "page": "activities.html"},
    {"id": "F10", "severity": "low", "title": "Some official pages could not be fetched directly",
     "detail": "Hilton, Hyatt and Arlo booking/rooms pages redirected to generic booking shells or failed to return content. Those hotels were kept only where an official NYC Tourism listing or another official page supplied verified facts; all unverified fields are blank.",
     "sources": ["hotel_week"], "page": "verification.html"},
    {"id": "F11", "severity": "low", "title": "Trip starts on a U.S. federal holiday",
     "detail": "Monday 15 February 2027 is Washington's Birthday (OPM). Impact on rates, crowds and venue hours is not verified.",
     "sources": ["opm"], "page": "dates.html"},
    {"id": "F12", "severity": "low", "title": "Parallel-session scope separation",
     "detail": "Another session owns the repository-root site and .github/workflows/. This session's site is self-contained in docs/. Arena fixes the branch name, so the requested session-<id>/<task> branches could not be created; branch isolation plus file-scope claims are used instead.",
     "sources": [], "page": "verification.html"},
]

repo_review = {
    "checked": CHECKED,
    "baseline_commit": "c251442d122a8d04aade3d8b5a0d57fd4e9ce37c",
    "findings": [
        {"item": "README.md", "verified": "Yes — fetched from the repository at c251442; contains only the single line '# NYFun3'.",
         "irregularity": "The repository had no site, no data files, no COORDINATION.md and no CI/GitHub Pages configuration at the start of this session.",
         "source": "local git show c251442:README.md"},
        {"item": "COORDINATION.md", "verified": "Yes — created in this session; imported the existing board from origin/arena/7386fd81-nyfun3.",
         "irregularity": "The existing claim on the other session branch covers COORDINATION.md, README.md, index.html, assets/, pages/ and .github/workflows/. This session therefore keeps its entire deliverable in docs/, data/ and tools/.",
         "source": "git show FETCH_HEAD:COORDINATION.md (origin/arena/7386fd81-nyfun3)"},
        {"item": "Branch model", "verified": "Yes — git branch / git ls-remote origin.",
         "irregularity": "Arena fixes this session to arena/8781ea5a-nyfun3 and forbids creating or pushing other branches; the requested session-<id>/<task> branch convention cannot be used. Logged in COORDINATION.md.",
         "source": "local git status / git ls-remote origin"},
        {"item": "Existing verification", "verified": "Yes — no data tables, no sources, no tests existed to review line by line.",
         "irregularity": "All verification in this session is new work against official external sources; no prior claims were carried over.",
         "source": "git ls-tree -r c251442"},
    ],
}

verification = {
    "checked": CHECKED,
    "rules": [
        "Every rendered table row carries at least one link to an official source (MICHELIN Guide, the venue's own site, a government/DMO site, the hotel's own site, or an MTA page).",
        "A value that could not be confirmed from an official source is left blank, rendered as '— unverified', and listed on the Flagged for Review page.",
        "No value is inferred, estimated, or copied from a third-party travel blog. Third-party content is used only as social-media review links on the platform's own domain.",
        "Prices labelled 'subtotal for 2' are pure arithmetic (official per-person price × 2) and are explicitly marked as excluding tax, gratuity and beverages where the official source says so.",
        "Weekday values are computed with Python datetime from ISO dates, not estimated.",
        "Social links were obtained either by fetching a YouTube/TikTok platform page directly or via a site-restricted search of that platform's domain; the video content is never used as a factual data source.",
    ],
    "checks": [
        {"check": "Official MICHELIN 2025 star article fetched in 5 chunks; all star names and URLs transcribed.", "result": "pass", "sources": ["michelin_stars_2025"]},
        {"check": "Current official all-starred NYC listing fetched; counts 5/14/50 = 69 recorded.", "result": "pass", "sources": ["michelin_all_starred"]},
        {"check": "Current official NYC selection listing fetched; 76 Bib Gourmand, 224 Selected, 369 total recorded.", "result": "pass", "sources": ["michelin_nyc"]},
        {"check": "13 individual current MICHELIN restaurant pages fetched for address, star level, cuisine and per-day hours.", "result": "pass", "sources": ["michelin_all_starred"]},
        {"check": "Official restaurant menu/FAQ pages fetched for per-person prices (Le Bernardin PDF, EMP FAQ, The Modern menu).", "result": "pass", "sources": ["lb_lunch", "emp_faq", "modern"]},
        {"check": "Official venue hours pages fetched for MoMA, AMNH, NPS, 9/11 Memorial, High Line, Whitney, One World Observatory, Top of the Rock, ESB, Met, NYC Parks.", "result": "pass with exceptions logged", "sources": ["moma", "amnh", "nps", "911", "highline", "whitney", "owo", "toprock", "esb", "met", "centralpark"]},
        {"check": "Official NYC Tourism Hotel Week pages + press release fetched for dates, discount and booking opening.", "result": "pass", "sources": ["hotel_week", "hotel_week_about", "hotel_week_press"]},
        {"check": "OPM 2027 federal holiday schedule fetched for 15 Feb 2027.", "result": "pass", "sources": ["opm"]},
        {"check": "Official hotel pages fetched for Pod 51 (rooms/FAQ/location), 11 Howard, Arlo NoMad (DMO), citizenM (Marriott brand).", "result": "pass with blanks logged", "sources": ["pod51_rooms", "pod51_faq", "howard", "arlo_nomad", "citizenm"]},
        {"check": "MTA official maps / Trip Planner / subway guide located; no static travel-time matrix exists.", "result": "travel-time values intentionally blank", "sources": ["mta_maps", "mta_trip", "mta_riding"]},
        {"check": "Hilton / Hyatt / SynXis / some Marriott rate pages returned JS shells, redirects or errors; no price was captured.", "result": "no price invented", "sources": ["hotel_week"]},
        {"check": "Official hotel 7-night totals could not be confirmed; all price cells left blank.", "result": "unverified by design", "sources": ["hotel_week"]},
        {"check": "Site generator validates each row has >=1 official source, flags blanks, and checks internal links resolve.", "result": "automated in tools/build_site.py", "sources": []},
    ],
}

# ---------------------------------------------------------------------------
# Executive summary
# ---------------------------------------------------------------------------
executive_summary = {
    "checked": CHECKED,
    "headline": "A verified evidence base for a 15 February – 23 March 2027 New York trip for 2 adults, with every unconfirmed value left blank and flagged.",
    "key_points": [
        {"title": "Dates", "text": "Four real date options are costed by weekday: 15–18 Feb (3 nights, preferred), 15–22 Feb (7 nights, primary), 15 Feb–1 Mar (14 nights), 15 Feb–15 Mar (28 nights). 15 Feb 2027 is Washington's Birthday, a U.S. federal holiday.", "sources": ["opm"]},
        {"title": "Cheapest verified booking window", "text": "NYC Hotel Week 2027 (2 Jan – 11 Feb 2027) offers 25% off standard rates at 148+ participating hotels, with reservations open since 17 Nov 2026. It ends 4 days before the earliest allowed check-in, so it cannot be used for this trip as requested.", "sources": ["hotel_week", "hotel_week_about", "hotel_week_press"]},
        {"title": "MICHELIN picture", "text": "The current official NYC listing shows 69 starred restaurants: 5 three-star, 14 two-star, 50 one-star; plus 76 Bib Gourmand and 224 Selected (no star). The full 2025 star roster is included with official links; 13 restaurants were re-verified line by line against their current pages.", "sources": ["michelin_all_starred", "michelin_nyc", "michelin_stars_2025"]},
        {"title": "Restaurant detail", "text": "13 starred restaurants have verified addresses, per-day opening hours, exceptions, official site links and social review links. Verified menu subtotals for 2 are published for Le Bernardin, Eleven Madison Park and The Modern; other totals are blank.", "sources": ["lb_lunch", "emp_faq", "modern"]},
        {"title": "Activities", "text": "11 activities have official links, days/hours/exceptions and social review links where verifiable. The High Line's official winter hours (7 AM–8 PM, 1 Dec–31 Mar) cover the entire trip window.", "sources": ["highline", "moma", "amnh", "nps", "911", "whitney", "owo", "toprock", "esb", "met", "centralpark"]},
        {"title": "Hotels", "text": "6 candidate hotels are documented with official sources. Pod 51 is the only one where both a queen bed and a private bathroom are confirmed verbatim; its official facility fee is $29.84 per room per night. No 7-night total could be confirmed from an official site, so all price cells are blank.", "sources": ["pod51_rooms", "pod51_faq", "howard", "arlo_nomad", "citizenm", "hotel_week"]},
        {"title": "Cluster / travel analysis", "text": "Starred restaurants are grouped into clusters using the ZIP codes on their official MICHELIN pages. The requested 'within 1 hour by subway or bus' count cannot be verified from a static official source; those numbers and the resulting hotel ranking are left blank, with an MTA Trip Planner workflow supplied instead.", "sources": ["michelin_all_starred", "mta_trip", "mta_maps"]},
        {"title": "Decision status", "text": "7 of 12 questions block a decision (dates, hotel total, booking timing, room requirements, transit counts, star-list currency, itinerary feasibility). None were filled with guesses; each has a concrete discovery step.", "sources": ["hotel_week", "opm", "mta_trip"]},
        {"title": "Site & governance", "text": "A mobile-friendly static dashboard with 12 subpages, a machine-readable data corpus, an automated build/verification script, a dedicated Suggestions page and a Flagged for Review page. Parallel-session scopes are recorded in COORDINATION.md.", "sources": []},
    ],
    "decision_gates": [
        {"gate": "Choose dates", "status": "blocked", "blocking": ["Q01", "Q03"]},
        {"gate": "Set hotel budget", "status": "blocked", "blocking": ["Q02", "Q03"]},
        {"gate": "Shortlist hotels", "status": "blocked", "blocking": ["Q04", "Q05"]},
        {"gate": "Lock restaurant list", "status": "partial", "blocking": ["Q06", "Q07"]},
        {"gate": "Build daily itinerary", "status": "blocked", "blocking": ["Q09", "Q12"]},
        {"gate": "Publish final plan", "status": "blocked", "blocking": ["Q10", "Q11"]},
    ],
}

FILES = {
    "sources.json": S,
    "trip.json": trip,
    "michelin.json": michelin,
    "activities.json": activities,
    "hotels.json": hotels,
    "analysis.json": analysis,
    "questions.json": questions,
    "suggestions.json": suggestions,
    "flags.json": flags,
    "repo_review.json": repo_review,
    "verification.json": verification,
    "executive_summary.json": executive_summary,
}

FILES = apply_updates(FILES, S, CHECKED)

for filename, payload in FILES.items():
    (DATA / filename).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print("Wrote", len(FILES), "data files to", DATA)
print("Roster:", len(FILES["michelin.json"]["roster"]),
      "| Detailed restaurants:", len(FILES["michelin.json"]["detailed"]),
      "| Guide-listed:", len(FILES["michelin.json"]["guide_listed"]),
      "| Activities:", len(FILES["activities.json"]),
      "| Hotels:", len(FILES["hotels.json"]),
      "| Sources:", len(FILES["sources.json"]))
