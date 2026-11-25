#!/usr/bin/env python3
"""Apply the 2026-11-25 line-by-line verification updates to the data corpus.

This module is imported by compile_data.py. It patches the in-memory data with
facts that were verified after the first draft was written: real dated 7-night
hotel quotes, official in-window booking offers, the complete 2026 MICHELIN
Guide new-additions article, updated hotel attributes, and the resulting
analysis/questions/suggestions/flags. Every added value has an official source.
"""
from __future__ import annotations

BASE_MICHELIN = "https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/"


def M(slug: str) -> str:
    return BASE_MICHELIN + slug


def source(key: str, title: str, url: str, kind: str, checked: str) -> dict:
    return {"id": key, "title": title, "url": url, "type": kind, "checked": checked}


def gl(name, added, cuisine, area, url, *, official="", address="", zip_code="",
       days="", hours="", exceptions="", price_two="", price_basis="", price_note="",
       social=None, sources=None, flags=None, status=None):
    """Guide-listed / Selected row. Blank values are intentional and flagged."""
    return {
        "name": name,
        "status": status or "Listed in the MICHELIN Guide (Selected / New addition; no Star or Bib Gourmand distinction announced in the official new-additions article)",
        "added": added,
        "cuisine": cuisine,
        "area": area,
        "address": address,
        "zip": zip_code,
        "michelin_url": url,
        "official_url": official,
        "days_open": days,
        "hours": hours,
        "exceptions": exceptions,
        "price_two": price_two,
        "price_basis": price_basis,
        "price_note": price_note or "No numeric total for two published on the fetched official pages; left blank.",
        "social": social or [],
        "sources": sources or ["michelin_additions"],
        "flags": flags or [
            "Guide-listed / Selected only; the official new-additions article announces no Star or Bib Gourmand distinction for this entry.",
            "Individual current MICHELIN restaurant page not fetched; days, hours, address, official site, price and social links left blank.",
        ],
    }


def by_id(items, item_id):
    for item in items:
        if item.get("id") == item_id:
            return item
    raise KeyError(item_id)


def apply_updates(FILES, S, CHECKED):
    # -----------------------------------------------------------------------
    # Source registry additions (all directly fetched or platform-restricted)
    # -----------------------------------------------------------------------
    new_sources = [
        source("pod51_booking_7n",
               "Pod 51 official SynXis booking page — 15–22 Feb 2027, 2 adults, 1 room; Queen Pod 7-night totals incl taxes & fees",
               "https://be.synxis.com/?adult=2&arrive=2027-02-15&chain=12484&child=0&currency=USD&depart=2027-02-22&hotel=41155&level=hotel&locale=en-US&productcurrency=USD&rooms=1",
               "official hotel booking engine", CHECKED),
        source("arlo_booking_7n",
               "Arlo NoMad official booking page — 15–22 Feb 2027, 2 adults, 1 room; Queen 7-night totals incl urban fee, excl taxes",
               "https://book.arlohotels.com/?adult=2&arrive=2027-02-15&chain=19470&child=0&currency=USD&depart=2027-02-22&hotel=70017&level=hotel&locale=en-US&productcurrency=USD&rooms=1",
               "official hotel booking engine", CHECKED),
        source("arlo_cyber",
               "Arlo Hotels — Cyber Exclusive Access (40% off Book Direct rates; sale ends 3 Dec 2026; NYC stay dates through 31 Oct 2027; code CYBER)",
               "https://arlohotels.com/cyber-exclusive-access/",
               "official hotel offer", CHECKED),
        source("marriott_cyber",
               "Marriott — CYBER SALE at citizenM New York Times Square (15% off here / 25% members in app; code QRI; book by Tuesday 1 Dec; valid stays 29 Nov 2026–2 May 2027)",
               "https://www.marriott.com/offers/cyber-sale-2026-hws-us-canada-cala-off-257932/nyczt-citizenm-new-york-times-square",
               "official hotel offer", CHECKED),
        source("citizenm_property",
               "Marriott — citizenM New York Times Square official property page (address 218 W 50th St, NY 10019; XL king beds; eight subway lines)",
               "https://www.marriott.com/en-us/hotels/nyczt-citizenm-new-york-times-square/overview/",
               "official hotel", CHECKED),
        source("citizenm_rooms",
               "Marriott — citizenM New York Times Square rooms page (XL king bed, power shower, tablet room controls)",
               "https://www.marriott.com/en-us/hotels/nyczt-citizenm-new-york-times-square/rooms/",
               "official hotel", CHECKED),
        source("howard_booking",
               "11 Howard official booking page root (default 25–26 Nov 2026 search form fetched; no 2027 dated quote returned)",
               "https://booking.11howard.com/",
               "official hotel booking engine", CHECKED),
        source("repo",
               "Official GitHub repository — kanlerxz87-cyber/NYFun3 (governance, coordination and build artifacts)",
               "https://github.com/kanlerxz87-cyber/NYFun3",
               "official repository", CHECKED),
        source("met_hours",
               "The Met official homepage hours block (site-restricted search extract: Sun–Tue & Thu 10 am–5 pm; Fri–Sat 10 am–9 pm; closed Wed)",
               "https://www.metmuseum.org/?mod=article_inline",
               "official venue (search extract)", CHECKED),
        source("michelin_page_noury",
               "MICHELIN Guide — Noury (current restaurant page; Selected, no star icon)",
               M("noury"), "official guide", CHECKED),
        source("michelin_page_muje",
               "MICHELIN Guide — Mūje (current restaurant page; Selected, no star icon)",
               M("muje"), "official guide", CHECKED),
        source("michelin_page_nyonya",
               "MICHELIN Guide — Nyonya (current restaurant page; Bib Gourmand distinction, no star icon)",
               M("nyonya"), "official guide", CHECKED),
        source("noury_official",
               "Noury New York — official restaurant website (linked as 'Visit Website' on the current MICHELIN page)",
               "https://www.nourynewyork.com/",
               "official restaurant website", CHECKED),
        source("muje_official",
               "MUJE — official restaurant website (linked as 'Visit Website' on the current MICHELIN page)",
               "https://www.mujenyc.com/",
               "official restaurant website", CHECKED),
        source("nyonya_official",
               "Nyonya — official restaurant website (linked as 'Visit Website' on the current MICHELIN page; says cash only)",
               "https://nyonya.res-menu.com/",
               "official restaurant website", CHECKED),
    ]
    for s in new_sources:
        S.setdefault(s["id"], s)

    S["michelin_additions"]["title"] = (
        "MICHELIN Guide — New Additions to the MICHELIN Guide New York "
        "(18 Nov 2026; chunks 0–5 fetched; November, July and April 2026 Selection additions)"
    )
    S["met_home"]["title"] = (
        "The Metropolitan Museum of Art — homepage (closed Wednesdays, $30 general admission; "
        "weekly hours also confirmed by official site-restricted search extract met_hours)"
    )

    # -----------------------------------------------------------------------
    # Activities: remove an accidental unrelated Instagram link on MoMA,
    # and record the official source for the Met weekly hours.
    # -----------------------------------------------------------------------
    for a in FILES["activities.json"]:
        if a["name"].startswith("Museum of Modern Art"):
            a["social"] = [s for s in a["social"] if "statue-of-liberty" not in s["url"]]
            a["flags"] = list(dict.fromkeys(a.get("flags", []) + [
                "An unrelated Statue of Liberty Instagram location placeholder was removed from this row; no verified Instagram review link for MoMA was found.",
            ]))
        if a["name"].startswith("The Metropolitan Museum"):
            a["sources"] = list(dict.fromkeys(a["sources"] + ["met_hours"]))
            a["flags"] = [
                "Full weekly hours were confirmed by an official Met site-restricted search extract "
                "(source met_hours); 'closed Wednesdays' and $30 general admission were confirmed by "
                "fetching the official homepage and plan-your-visit pages directly."
            ]

    # -----------------------------------------------------------------------
    # MICHELIN Guide-listed / Selected catalogue
    # -----------------------------------------------------------------------
    michelin = FILES["michelin.json"]
    michelin["status_note"] = (
        "'Starred' means the restaurant currently holds 1–3 MICHELIN Stars. 'Listed in the MICHELIN Guide' / "
        "'Selected restaurants' / 'Bib Gourmand' are Guide distinctions without a Star. The 2025 ceremony "
        "article is the source of the full star roster; the current all-starred listing is the source of "
        "current counts. The November/July/April 2026 new-additions article states that Stars and Bib "
        "Gourmands are revealed only at the annual ceremony, while new restaurants are added to the "
        "Selection twice a year and marked 'New'. Those entries are therefore catalogued as Guide-listed, "
        "not starred, with blank hours/price/social cells where no individual official page was fetched."
    )

    base_guide = [
        {
            "name": "Noury", "status": "Listed in the MICHELIN Guide (Selected, no star)",
            "added": "November 2026", "cuisine": "Japanese, Izakaya", "area": "SoHo",
            "address": "137 Sullivan St., New York, NY 10012", "zip": "10012",
            "michelin_url": M("noury"), "official_url": "https://www.nourynewyork.com/",
            "days_open": "Monday–Sunday (all 7 days)",
            "hours": "Mon–Wed 5–10 PM; Thu–Sat 5–10:30 PM; Sun 5–9:30 PM",
            "exceptions": "Sunday closes 9:30 PM.",
            "price_two": "", "price_basis": "",
            "price_note": "MICHELIN price category $$$; no numeric total for two published on the fetched official pages; left blank.",
            "social": [],
            "sources": ["michelin_additions", "michelin_page_noury", "noury_official"],
            "flags": [
                "Guide-listed / Selected only: the current MICHELIN page shows a 'New' label and no star icon.",
                "Official restaurant website fetched and linked; no numeric menu total for two adults was published on the fetched page.",
                "No verified social review link found.",
            ],
        },
        {
            "name": "Mūje", "status": "Listed in the MICHELIN Guide (Selected, no star)",
            "added": "November 2026", "cuisine": "Asian, Asian Influences", "area": "NoMad",
            "address": "151 W. 30th St., New York, NY 10001", "zip": "10001",
            "michelin_url": M("muje"), "official_url": "https://www.mujenyc.com/",
            "days_open": "", "hours": "", "exceptions": "",
            "price_two": "", "price_basis": "",
            "price_note": "MICHELIN price category $$$$; no numeric total for two published on the fetched official pages; left blank.",
            "social": [],
            "sources": ["michelin_additions", "michelin_page_muje", "muje_official"],
            "flags": [
                "Guide-listed / Selected only: the current MICHELIN page shows a 'New' label and no star icon.",
                "Official restaurant website fetched and linked; no numeric menu total for two adults was published on the fetched page.",
                "The current MICHELIN page publishes no opening-hours table for this restaurant; days/hours left blank.",
                "No verified social review link found.",
            ],
        },
        {
            "name": "Nyonya", "status": "Bib Gourmand (MICHELIN Guide distinction, no star)",
            "added": "", "cuisine": "Malaysian", "area": "",
            "address": "199 Grand St., New York, NY 10013", "zip": "10013",
            "michelin_url": M("nyonya"), "official_url": "https://nyonya.res-menu.com/",
            "days_open": "Monday–Sunday (all 7 days)",
            "hours": "Mon–Thu & Sun 11 AM–10 PM; Fri–Sat 11 AM–11 PM",
            "exceptions": "Cash only (official restaurant website).", "price_two": "", "price_basis": "",
            "price_note": "MICHELIN price category $; cash only; no numeric total for two published on the fetched official pages; left blank.",
            "social": [],
            "sources": ["howard_michelin", "michelin_page_nyonya", "nyonya_official"],
            "flags": [
                "Bib Gourmand is a MICHELIN Guide distinction, not a MICHELIN Star.",
                "Current official MICHELIN restaurant page and official restaurant website fetched; address, ZIP, weekly hours and cash-only exception verified.",
                "Neighborhood is not stated on the fetched official pages; area left blank.",
                "No verified social review link found; no numeric total for two adults was published.",
            ],
        },
    ]

    # Exact names, months, areas, cuisines and URLs transcribed from the official
    # MICHELIN new-additions article (chunks 0–3). No values are invented.
    additions = [
        ("Border Town", "November 2026", "Northern Mexican", "Brooklyn – Greenpoint",
         "https://guide.michelin.com/us/en/new-york-state/brooklyn/restaurant/border-town"),
        ("Elder", "November 2026", "Contemporary Indian", "New York – Midtown West / Hudson Yards", M("elder-1253266")),
        ("Indienne NYC", "November 2026", "Regional Indian", "New York – Midtown West / Hudson Yards", M("indienne-nyc")),
        ("Oriana", "November 2026", "American steakhouse", "New York – Nolita", M("oriana")),
        ("Or'esh", "November 2026", "Levantine / Middle Eastern", "New York – SoHo", M("or-esh")),
        ("Humm", "November 2026", "Contemporary, vegetable-focused", "New York – Hudson Square", M("humm")),
        ("Graciela", "November 2026", "Argentine", "New York – West Village", M("graciela")),
        ("Roscioli", "November 2026", "Roman / Italian", "New York – West Village", M("roscioli-1205936")),
        ("Levant", "November 2026", "Middle Eastern / Egyptian", "Queens – Astoria",
         "https://guide.michelin.com/us/en/new-york-state/queens/restaurant/levant"),
        ("Little Banchan Shop", "November 2026", "Korean", "Queens – Long Island City",
         "https://guide.michelin.com/us/en/new-york-state/queens/restaurant/little-banchan-shop"),
        ("Confidant", "July 2026", "", "Brooklyn – Brooklyn Heights",
         "https://guide.michelin.com/us/en/new-york-state/brooklyn/restaurant/confidant"),
        ("arthur", "July 2026", "Modern French bistro", "Brooklyn – Greenpoint",
         "https://guide.michelin.com/us/en/new-york-state/brooklyn/restaurant/arthur"),
        ("Balera", "July 2026", "Pizza", "Brooklyn – Williamsburg",
         "https://guide.michelin.com/us/en/new-york-state/brooklyn/restaurant/balera"),
        ("Odo East Village", "July 2026", "Japanese izakaya", "New York – East Village", M("odo-east-village")),
        ("Len Len", "July 2026", "Thai", "New York – Flatiron", M("len-len")),
        ("Bistrot Ha", "July 2026", "Vietnamese / French-influenced", "New York – Lower East Side", M("bistrot-ha")),
        ("Kjun", "July 2026", "Korean / Cajun", "New York – Murray Hill", M("kjun")),
        ("Oyatte", "July 2026", "Seasonal, farm-driven", "New York – Murray Hill", M("oyatte")),
        ("Marcel", "July 2026", "French café / brasserie", "New York – Upper East Side", M("marcel-1247960")),
        ("Yugin", "July 2026", "Omakase / Japanese", "New York – Upper East Side", M("yugin")),
        ("Wild Cherry", "July 2026", "Contemporary / raw bar", "New York – West Village", M("wild-cherry")),
        ("Cynthia", "July 2026", "French, Asian and Latin influences", "New York – West Village", M("cynthia")),
        ("AbuQir", "July 2026", "Egyptian seafood", "Queens – Astoria",
         "https://guide.michelin.com/us/en/new-york-state/queens/restaurant/abuqir"),
        ("Bolivian Llama Party", "July 2026", "Bolivian", "Queens – Sunnyside",
         "https://guide.michelin.com/us/en/new-york-state/ny-woodside/restaurant/bolivian-llama-party"),
        ("Pierogi Boys", "July 2026", "Polish", "Queens – Ridgewood",
         "https://guide.michelin.com/us/en/new-york-state/ridgewood/restaurant/pierogi-boys"),
        ("Entre Nous", "April 2026", "Wine bar / natural wine", "Brooklyn – Clinton Hill",
         "https://guide.michelin.com/us/en/new-york-state/brooklyn/restaurant/entre-nous-1217771"),
        ("Los Burritos Juárez", "April 2026", "Mexican burritos", "Brooklyn – Fort Greene",
         "https://guide.michelin.com/us/en/new-york-state/brooklyn/restaurant/los-burritos-juarez"),
        ("Bong", "April 2026", "Cambodian", "Brooklyn – Crown Heights",
         "https://guide.michelin.com/us/en/new-york-state/brooklyn/restaurant/bong"),
        ("Vato", "April 2026", "Tortilleria / burritos", "Brooklyn – Park Slope",
         "https://guide.michelin.com/us/en/new-york-state/brooklyn/restaurant/vato"),
        ("I Cavallini", "April 2026", "Italian", "Brooklyn – Williamsburg",
         "https://guide.michelin.com/us/en/new-york-state/brooklyn/restaurant/i-cavallini"),
        ("Le Chêne", "April 2026", "French", "New York – Greenwich Village", M("le-chene")),
        ("Hwaro", "April 2026", "Korean / French", "New York – Midtown West", M("hwaro")),
        ("Elcielo New York", "April 2026", "Colombian / Latin American", "New York – NoMad", M("elcielo-new-york")),
        ("Cove", "April 2026", "Contemporary / tasting", "New York – SoHo", M("cove-1244899")),
    ]
    michelin["guide_listed"] = base_guide + [gl(*row) for row in additions]
    michelin["guide_listed_count"] = len(michelin["guide_listed"])

    # -----------------------------------------------------------------------
    # Hotels with real dated 7-night quotes and updated official attributes
    # -----------------------------------------------------------------------
    hotels = [
        {
            "name": "Pod 51 Hotel", "area": "Midtown East",
            "address": "230 E 51st St, New York, NY 10022 (official SynXis booking page)", "zip": "10022",
            "official_url": "https://www.thepodhotel.com/pod-51",
            "booking_url": "https://be.synxis.com/?adult=2&arrive=2027-02-15&chain=12484&child=0&currency=USD&depart=2027-02-22&hotel=41155&level=hotel&locale=en-US&productcurrency=USD&rooms=1",
            "private_bath": "Yes — Queen Pod official booking page: 'private bathroom with rainfall shower'; some other room types have shared baths",
            "bed": "1 Queen bed (Queen Pod, sleeps 2, 150 sq ft)",
            "amenities": "Queen Pod: private bathroom with rainfall shower, safe, desk/workplace, hair dryer, air conditioning, free Wi-Fi, flat-screen TV; rooftop deck, outdoor garden, free walking tours, same-day luggage storage",
            "fees": "Official FAQ lists a facility fee of $29.84 (incl. tax) per room per night, in addition to the room rate. The 7-night booking page says its totals are 'Including taxes and fees' but does not itemize the facility fee; do not add it again.",
            "transit": "6 / E / M at Lexington Ave–E 53rd St; M50, M101, M102, M103 buses (official location/FAQ pages)",
            "price_7n": "$1,109 (Pod Member Rate, incl taxes & fees); $1,310 (Stay 4 & Save, incl taxes & fees)",
            "price_quotes": [
                {"hotel": "Pod 51 Hotel", "room": "Queen Pod", "rate": "Pod Member Rate", "total": "$1,109",
                 "basis": "15–22 Feb 2027, 2 adults, 1 room; official page states 'Total for 7 nights', 'Including taxes and fees'; free cancellation up to 3:00 PM 2 days before arrival; displayed $159/night.",
                 "source": "pod51_booking_7n"},
                {"hotel": "Pod 51 Hotel", "room": "Queen Pod", "rate": "Stay 4 & Save", "total": "$1,310",
                 "basis": "15–22 Feb 2027, 2 adults, 1 room; official page states 'Total for 7 nights', 'Including taxes and fees'; free cancellation up to 3:00 PM 2 days before arrival; displayed $188/night.",
                 "source": "pod51_booking_7n"},
            ],
            "price_note": "Real dated official 7-night totals for 2 adults. Pod Member Rate requires the hotel's member rate; no official page states whether membership is free.",
            "days_open": "", "hours": "", "exceptions": "Check-in 3:00 PM, check-out 1:00 PM (official FAQ).",
            "social": [],
            "sources": ["pod51", "pod51_rooms", "pod51_faq", "pod51_location", "pod51_booking_7n"],
            "flags": [
                "Lowest verified all-in 7-night total among the official quotes captured, but no market-wide price comparison exists.",
                "Facility fee is listed separately by the official FAQ; the booking total says taxes and fees are included but does not itemize that fee.",
                "7-night quote verified for 15–22 Feb 2027 only; other date options were not quoted.",
                "No verified social review link found for this hotel.",
            ],
        },
        {
            "name": "Arlo NoMad", "area": "NoMad",
            "address": "11 E. 31st St., Manhattan, NY 10016 (official NYC Tourism listing)", "zip": "10016",
            "official_url": "https://www.nyctourism.com/hotel-week/arlo-hotel-nomad/",
            "booking_url": "https://book.arlohotels.com/?adult=2&arrive=2027-02-15&chain=19470&child=0&currency=USD&depart=2027-02-22&hotel=70017&level=hotel&locale=en-US&productcurrency=USD&rooms=1",
            "private_bath": "",
            "bed": "1 Queen bed in the Queen room (sleeps 2; 145 sq ft) — official booking page",
            "amenities": "250 modern micro guestrooms (150 sq ft), complimentary WiFi, Blind Barber bath amenities, custom walnut furnishings, 31st-floor rooftop bar A.R.T., Lamalo restaurant, complimentary Arlo bicycles; official booking page also lists Queen, Essential Queen, City Queen, King, Corner Queen, Sky View and Terrace room types",
            "fees": "Booking totals state 'Including the urban fee, excluding taxes'.",
            "transit": "",
            "price_7n": "$1,296 (The Steal Deal); $1,985 (Plain & Simple); $2,195 (Start Your Morning Right) — all incl urban fee, excl taxes",
            "price_quotes": [
                {"hotel": "Arlo NoMad", "room": "Queen", "rate": "The Steal Deal", "total": "$1,296",
                 "basis": "15–22 Feb 2027, 2 adults, 1 room; 'Total for 7 nights', 'Including the urban fee, excluding taxes'; non-refundable, deposit required; book by December 3; displayed $185/night.",
                 "source": "arlo_booking_7n"},
                {"hotel": "Arlo NoMad", "room": "Queen", "rate": "Plain & Simple", "total": "$1,985",
                 "basis": "15–22 Feb 2027, 2 adults, 1 room; 'Total for 7 nights', 'Including the urban fee, excluding taxes'; free cancellation up to 1 day before arrival; displayed $283/night.",
                 "source": "arlo_booking_7n"},
                {"hotel": "Arlo NoMad", "room": "Queen", "rate": "Start Your Morning Right", "total": "$2,195",
                 "basis": "15–22 Feb 2027, 2 adults, 1 room; 'Total for 7 nights', 'Including the urban fee, excluding taxes'; breakfast included; free cancellation up to 1 day before arrival; displayed $313/night.",
                 "source": "arlo_booking_7n"},
            ],
            "price_note": "Real dated official 7-night subtotals for 2 adults, but they EXCLUDE taxes. No official tax amount was published on the fetched booking page, so the final all-in total is blank.",
            "days_open": "", "hours": "", "exceptions": "Hotel alert on official booking page: check-in age is 21 years old.",
            "social": [],
            "sources": ["arlo_nomad", "hotel_week", "hotel_week_about", "arlo_booking_7n", "arlo_cyber"],
            "flags": [
                "Displayed 7-night totals exclude taxes; not like-for-like with Pod 51's taxes-and-fees-included total.",
                "Private bathroom wording is not explicit on the fetched official pages; cell left blank.",
                "Irregularity: official Cyber Exclusive Access page says NYC stay dates through 31 Oct 2027, while the booking page rate description says 'stay dates through December 2027'.",
                "No verified transit statement and no verified social review link found.",
            ],
        },
        {
            "name": "11 Howard", "area": "SoHo",
            "address": "11 Howard Street, New York City, NY (official hotel page / MICHELIN Guide hotel page)", "zip": "",
            "official_url": "https://www.11howard.com/",
            "booking_url": "https://booking.11howard.com/",
            "private_bath": "", "bed": "",
            "amenities": "207 guest rooms and suites (official hotel site), library/co-working space, bar, Le Coucou (1 MICHELIN Star) in the building; MICHELIN Guide hotel page lists 213 rooms and a guest score of 18.1/20",
            "fees": "", "transit": "",
            "price_7n": "", "price_quotes": [],
            "price_note": "No 15–22 Feb 2027 rate could be confirmed; the official booking/availability page fetched returned only a default date search, not a dated quote. Left blank.",
            "days_open": "", "hours": "", "exceptions": "",
            "social": [],
            "sources": ["howard", "howard_michelin", "michelin_page_le-coucou", "howard_booking"],
            "flags": [
                "Irregularity: official hotel site says 207 rooms; MICHELIN Guide hotel page says 213 rooms.",
                "Private bathroom and bed size are not stated on the fetched official pages; left blank.",
                "ZIP code and 7-night total price unverified.",
                "No verified social review link found for this hotel.",
            ],
        },
        {
            "name": "citizenM New York Times Square", "area": "Times Square / Midtown West",
            "address": "218 West 50th Street, New York, NY 10019 (official Marriott property page)", "zip": "10019",
            "official_url": "https://www.marriott.com/en-us/hotels/nyczt-citizenm-new-york-times-square/overview/",
            "booking_url": "https://www.marriott.com/en-us/hotels/nyczt-citizenm-new-york-times-square/overview/",
            "private_bath": "",
            "bed": "XL king-size bed in every room (official Marriott property and rooms pages)",
            "amenities": "XL king-size beds, blackout blinds, rain showers / high-pressure power shower, mood lighting, Chromecast, tablet-controlled temperature/TV, 24/7 canteenM, cloudM rooftop bar, gym, free Wi-Fi, contactless check-in; official page says eight subway lines are just outside the door",
            "fees": "",
            "transit": "Eight subway lines just outside the door (official Marriott property page; no specific lines named).",
            "price_7n": "", "price_quotes": [],
            "price_note": "No 15–22 Feb 2027 7-night total confirmed. The official CYBER SALE offer gives 15% off here / 25% off for members in the Marriott Bonvoy app with code QRI, 5-day advance prepaid non-refundable rate, book by Tuesday 1 Dec, valid stay dates 29 Nov 2026–2 May 2027; no dated total is published.",
            "days_open": "", "hours": "", "exceptions": "",
            "social": [],
            "sources": ["citizenm", "citizenm_property", "citizenm_rooms", "marriott_cyber"],
            "flags": [
                "Private bathroom wording is not explicit on the fetched official property/rooms pages (in-room shower is described, but not labeled 'private bathroom'); cell left blank.",
                "7-night total price unverified; the official Cyber Sale publishes a discount, not a total.",
                "No verified social review link found for this hotel.",
            ],
        },
        {
            "name": "AC Hotel New York Times Square", "area": "Garment District",
            "address": "", "zip": "",
            "official_url": "https://www.nyctourism.com/hotel-week/",
            "booking_url": "https://bit.ly/ACTS2027HOTELWEEK",
            "private_bath": "", "bed": "",
            "amenities": "Private balconies and angled ceiling-to-floor windows (official NYC Tourism Hotel Week listing)",
            "fees": "", "transit": "",
            "price_7n": "", "price_quotes": [],
            "price_note": "No 15–22 Feb 2027 rate could be confirmed; left blank. Hotel Week 25% offer applies 2 Jan–11 Feb 2027 only.",
            "days_open": "", "hours": "", "exceptions": "",
            "social": [],
            "sources": ["ac_hotel", "hotel_week"],
            "flags": ["Private bathroom, bed size, address, ZIP and 7-night price not published on the fetched official listing; left blank.",
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
            "price_7n": "", "price_quotes": [],
            "price_note": "No 15–22 Feb 2027 rate could be confirmed; left blank. Hotel Week 25% offer applies 2 Jan–11 Feb 2027 only.",
            "days_open": "", "hours": "", "exceptions": "",
            "social": [],
            "sources": ["westin", "hotel_week"],
            "flags": ["Private bathroom, bed size, address, ZIP and 7-night price not published on the fetched official listing; left blank.",
                      "No verified social review link found for this hotel."],
        },
    ]
    FILES["hotels.json"] = hotels

    # -----------------------------------------------------------------------
    # Trip dates and cheapest / best upcoming booking window
    # -----------------------------------------------------------------------
    trip = FILES["trip.json"]
    trip["verified_facts"].extend([
        {"fact": "Arlo Hotels Cyber Exclusive Access: 40% off Book Direct rates; sale ends 3 December 2026; NYC stay dates through 31 October 2027; code CYBER. Subject to black-out dates and availability.",
         "sources": ["arlo_cyber"]},
        {"fact": "Marriott CYBER SALE at citizenM New York Times Square: 15% off when booked on the offer page, 25% off for members booking in the Marriott Bonvoy app; 5-day advance prepaid non-refundable rate; promotional code QRI; book by Tuesday, December 1; valid stay dates 29 November 2026 – 2 May 2027.",
         "sources": ["marriott_cyber"]},
        {"fact": "Two official 7-night quotes were captured for 15–22 February 2027, 2 adults, 1 room: Pod 51 Queen Pod Pod Member Rate $1,109 total including taxes and fees; Arlo NoMad Queen The Steal Deal $1,296 total including the urban fee but excluding taxes.",
         "sources": ["pod51_booking_7n", "arlo_booking_7n"]},
    ])
    trip["cheapest_booking_window"] = {
        "answer": (
            "NYC Hotel Week 2027 (2 Jan–11 Feb 2027, 25% off) remains the only official city-wide hotel "
            "discount, but it ends before the requested 15 Feb–23 Mar 2027 travel window. Two additional "
            "official offers DO apply to the requested window: Arlo Hotels' Cyber Exclusive Access (40% off, "
            "book by 3 Dec 2026, code CYBER, NYC stays through 31 Oct 2027) and Marriott's CYBER SALE at "
            "citizenM New York Times Square (15%/25% off, book by Tuesday 1 Dec, code QRI, stays 29 Nov 2026–2 May 2027)."
        ),
        "best_time_to_book_for_requested_dates": (
            "Best verified upcoming booking deadlines: Arlo Hotels Cyber Exclusive Access — book by 3 December 2026 "
            "(40% off; code CYBER); Marriott CYBER SALE — book by Tuesday, December 1 (15% off here / 25% members in app; code QRI)."
        ),
        "note": (
            "These are the highest verified discounts among the official offers checked, not a market-wide "
            "'cheapest price' proof: no official source compares all NYC hotels or publishes a best time to book. "
            "Pod 51's $1,109 all-in 7-night quote is the lowest verified all-in total among the two captured quotes; "
            "Arlo's $1,296 excludes taxes and is not directly comparable."
        ),
        "sources": ["hotel_week", "hotel_week_about", "hotel_week_press", "arlo_cyber", "marriott_cyber",
                    "pod51_booking_7n", "arlo_booking_7n"],
    }
    trip["flags"] = [
        "No official source proves a market-wide cheapest date or best time to book; two in-window discounts and two dated 7-night quotes are recorded, with the limitations shown.",
        "All four date options start on a U.S. federal holiday; impact on hotel rates, crowds and opening hours is not verified.",
        "Arlo Hotels' official promo page says NYC stay dates through 31 October 2027, while the official booking rate description says through December 2027; needs review.",
        "Arlo 7-night totals exclude taxes; they cannot be compared like-for-like with Pod 51's taxes-and-fees-included total.",
    ]

    # -----------------------------------------------------------------------
    # Analysis: ZIP clusters, same-ZIP hotel counts, price ranking, attribute score
    # -----------------------------------------------------------------------
    detailed = michelin["detailed"]
    zip_clusters = {}
    for r in detailed:
        zip_clusters.setdefault(r["zip"], []).append({"name": r["name"], "stars": r["stars"],
                                                      "michelin_url": r["michelin_url"]})

    hotel_zip_clusters = []
    for h in hotels:
        z = h.get("zip", "")
        matches = [r["name"] for r in detailed if r.get("zip") == z] if z else []
        hotel_zip_clusters.append({
            "hotel": h["name"], "zip": z,
            "same_zip_count": len(matches) if z else "",
            "restaurants": matches,
            "note": "Same-ZIP count from official MICHELIN street addresses; NOT a 1-hour transit count.",
            "sources": ["michelin_all_starred"] + h["sources"],
        })

    price_quotes = []
    for h in hotels:
        for q in h.get("price_quotes", []):
            amount = int(q["total"].replace("$", "").replace(",", ""))
            price_quotes.append({**q, "amount": amount, "taxes_included": "taxes" in q["basis"].lower() and "fees" in q["basis"].lower()})
    price_quotes.sort(key=lambda x: x["amount"])

    def attribute_score(h):
        fields = []
        for key, label in [
            ("private_bath", "private bathroom confirmed"),
            ("bed", "queen-or-larger bed confirmed"),
            ("address", "street address confirmed"),
            ("zip", "ZIP code confirmed"),
            ("transit", "official transit statement confirmed"),
            ("fees", "fee / price basis published"),
            ("price_7n", "dated 7-night total published"),
        ]:
            if h.get(key):
                fields.append(label)
        return {"hotel": h["name"], "score": len(fields), "fields": fields,
                "sources": h["sources"]}

    verified_attribute_ranking = sorted(
        [attribute_score(h) for h in hotels], key=lambda x: (-x["score"], x["hotel"])
    )

    analysis = FILES["analysis.json"]
    analysis["method"] = (
        "Only official data is used. MICHELIN restaurant pages publish street addresses incl. ZIP codes; "
        "those addresses are grouped below to show where starred restaurants cluster, and hotels with a verified "
        "ZIP are matched to same-ZIP restaurants. Same-ZIP counts are a static, verifiable cluster view, NOT the "
        "requested 'within 1 hour by subway or bus' count. That travel-time test requires a dated route/time result "
        "from the MTA Trip Planner, which is not a static official value. Because the rule says never infer or fill "
        "in values, the travel-time-based counts and the Michelin-density hotel ranking remain blank and flagged "
        "unverified. A verified-attribute ranking and a real dated price ranking are supplied instead, using only "
        "values actually published on official pages."
    )
    analysis["zip_clusters"] = [
        {"zip": z, "count": len(v), "restaurants": v} for z, v in sorted(zip_clusters.items())
    ]
    analysis["cluster_scope"] = (
        "13 starred restaurants whose current MICHELIN pages were fetched and verified line by line "
        "(sample of the 69 starred restaurants in the current official listing)."
    )
    analysis["hotel_zip_clusters"] = hotel_zip_clusters
    analysis["same_zip_note"] = (
        "citizenM New York Times Square (10019) shares a ZIP with 3 of the 13 detailed starred restaurants "
        "(Le Bernardin, Per Se, The Modern); Pod 51 (10022) shares with Aquavit; Arlo NoMad (10016) shares with "
        "Atomix. These are address-equality counts, not transit times, and must not be used as the requested "
        "1-hour Michelin-density ranking."
    )
    analysis["travel_time"] = {
        "value": "", "status": "unverified",
        "why": "MTA does not publish a static hotel→restaurant travel-time matrix; the official Trip Planner computes a dated, time-specific result and requires a manual query.",
        "sources": ["mta_maps", "mta_trip", "mta_riding"],
    }
    analysis["michelin_density_ranking"] = []
    analysis["michelin_density_ranking_status"] = "unverified — intentionally blank"
    analysis["price_rank"] = price_quotes
    analysis["best_price_verified"] = (
        "Pod 51 Queen Pod Pod Member Rate — $1,109 total for 7 nights including taxes and fees "
        "(15–22 Feb 2027, 2 adults, 1 room). Lowest verified all-in total among the official quotes captured; "
        "no market-wide comparison exists."
    )
    analysis["price_comparison_caveat"] = (
        "Arlo NoMad's $1,296 'The Steal Deal' total includes the urban fee but excludes taxes; the final all-in "
        "amount is blank. Pod 51's total includes taxes and fees. No tax amount was published for Arlo, so the two "
        "figures are not like-for-like and no arithmetic adjustment was made."
    )
    analysis["verified_attribute_ranking"] = verified_attribute_ranking
    analysis["verified_attribute_rule"] = (
        "1 point each for: private bathroom confirmed; queen-or-larger bed confirmed; street address confirmed "
        "on an official page; ZIP code confirmed on an official page; official transit information confirmed; "
        "an official fee/price basis published; a dated 7-night total published. Only fields with a non-blank "
        "official value score. This is a count of verified information, not a quality score and not a "
        "Michelin-density ranking."
    )
    analysis["sources"] = ["michelin_all_starred", "mta_maps", "mta_trip", "mta_riding", "hotel_week",
                           "pod51_booking_7n", "arlo_booking_7n", "arlo_cyber", "marriott_cyber",
                           "citizenm_property", "citizenm_rooms"]

    # -----------------------------------------------------------------------
    # Questions / information / answers
    # -----------------------------------------------------------------------
    questions = FILES["questions.json"]
    q = by_id(questions, "Q02")
    q.update({
        "have": "Two real official 7-night quotes for 15–22 Feb 2027, 2 adults, 1 room: Pod 51 Queen Pod $1,109 incl taxes & fees; Arlo NoMad Queen $1,296 incl urban fee, excl taxes. Official hotel pages, official booking links and one published fee (Pod 51 $29.84/room/night) are also verified.",
        "answer": "Partially answered. The lowest verified all-in total is Pod 51 at $1,109 for 7 nights. Arlo's displayed total excludes taxes, so its final total is blank. Four other candidate hotels have no verified 7-night total.",
        "missing": "A dated, official, all-in quote (room + taxes + fees) for 15–22 Feb 2027 for the remaining hotels, and Arlo's confirmed tax amount.",
        "discover": "Use each hotel's official booking link with 2 adults and the exact dates; save a dated screenshot/quote and link it in the row. For Arlo, proceed to the checkout step where taxes are itemized.",
        "sources": ["pod51_booking_7n", "arlo_booking_7n", "pod51_faq"],
        "blocks_decision": True,
    })
    q = by_id(questions, "Q03")
    q.update({
        "have": "NYC Hotel Week 2027 (2 Jan–11 Feb 2027, 25% off, reservations open 17 Nov 2026); Arlo Cyber Exclusive Access (40% off, book by 3 Dec 2026, NYC stays through 31 Oct 2027, code CYBER); Marriott CYBER SALE at citizenM (15%/25% off, book by Tuesday 1 Dec, code QRI, stays 29 Nov 2026–2 May 2027).",
        "answer": "Partially answered. The only official city-wide discount remains Hotel Week, which ends before the requested window. The best verified in-window booking deadlines are Arlo by 3 Dec 2026 (40% off) and Marriott by Tuesday 1 Dec (15%/25% off). No official source proves these are the market-wide cheapest or publishes a single 'best time to book'.",
        "missing": "A 2027 rate calendar or official statement comparing price movements and discounts across all NYC hotels for stays after 15 Feb 2027.",
        "discover": "Ask NYC Tourism and the hotels directly; record dated official quotes across several booking dates; do not rely on third-party 'best time to book' claims.",
        "sources": ["hotel_week", "hotel_week_about", "hotel_week_press", "arlo_cyber", "marriott_cyber"],
        "blocks_decision": True,
    })
    q = by_id(questions, "Q04")
    q.update({
        "have": "Pod 51 Queen Pod: queen bed + private bathroom (official booking page). Arlo NoMad Queen: 1 queen bed (official booking page). citizenM: XL king bed (official Marriott property/rooms pages).",
        "answer": "Partially answered. Three hotels have a queen-or-larger bed verified; only Pod 51 has an explicit private bathroom. citizenM's private-bathroom wording is not explicit, and three hotels have both fields blank.",
        "missing": "Room-type specifications for the other hotels from their own official room pages.",
        "discover": "Fetch each hotel's official room-type page and quote the bed and bathroom wording verbatim.",
        "sources": ["pod51_booking_7n", "arlo_booking_7n", "citizenm_property", "citizenm_rooms"],
        "blocks_decision": True,
    })
    q = by_id(questions, "Q05")
    q["answer"] = (
        "Blank / unverified. Static same-ZIP counts are published as a separate verified cluster view "
        "(citizenM 10019 = 3; Pod 51 10022 = 1; Arlo 10016 = 1), but MTA travel time is date/time-specific and "
        "no static official value exists; the rule forbids inference."
    )
    q["sources"] = ["michelin_all_starred", "mta_maps", "mta_trip", "mta_riding", "pod51_location",
                    "pod51_booking_7n", "arlo_booking_7n", "citizenm_property"]
    q = by_id(questions, "Q12")
    q["have"] = "Official activity locations, official MTA subway/bus route information on several venue pages, and verified hotel ZIPs/addresses for Pod 51, Arlo NoMad and citizenM."
    q["sources"] = ["mta_trip", "mta_maps", "centralpark", "owo", "pod51_booking_7n", "arlo_booking_7n", "citizenm_property"]

    # -----------------------------------------------------------------------
    # Suggestions
    # -----------------------------------------------------------------------
    suggestions = FILES["suggestions.json"]
    s = by_id(suggestions, "S01")
    s.update({
        "title": "Complete the dated 'official quote' workflow for the remaining hotels",
        "problem": "Two of six hotels now have real dated 7-night quotes; four are still blank, and Arlo's total excludes taxes.",
        "proposal": "Add a quote-capture table (hotel, dates, 2 adults, quoted total incl. taxes/fees, official URL, capture timestamp) and fill it from official booking pages; capture Arlo's tax amount at checkout.",
        "decision_needed": "Approve a rate-check cadence (daily/weekly) and who records quotes; choose whether to permit screenshots as evidence.",
        "effort": "Medium", "priority": "P0", "status": "proposed — awaiting review",
    })
    suggestions.extend([
        {"id": "S11", "title": "Add a tax-equivalent hotel price comparison",
         "problem": "Pod 51's $1,109 includes taxes and fees; Arlo NoMad's $1,296 includes the urban fee but excludes taxes, so the cheapest hotel cannot be confirmed like-for-like.",
         "proposal": "Add an 'all-in confirmed total' column populated only from an official checkout page that itemizes taxes; keep subtotals in a separate column.",
         "decision_needed": "Approve capturing checkout-step quotes (not just the room-list page) for every hotel.",
         "effort": "Low", "priority": "P0", "status": "proposed — awaiting review"},
        {"id": "S12", "title": "Resolve the Arlo Cyber Sale stay-date conflict",
         "problem": "The official Arlo promo page says NYC stay dates through 31 October 2027; the official booking rate description says through December 2027.",
         "proposal": "Ask Arlo or check a newer official terms page; keep both cited values until one is confirmed and add a check date.",
         "decision_needed": "Choose which official source is authoritative for the site.",
         "effort": "Low", "priority": "P2", "status": "proposed — awaiting review"},
    ])

    # -----------------------------------------------------------------------
    # Flags for review
    # -----------------------------------------------------------------------
    flags = FILES["flags.json"]
    f = by_id(flags, "F04")
    f["detail"] = (
        "The official 2025 ceremony article lists 5 three-star, 15 two-star and 52 one-star restaurants "
        "(72 names, including Westchester, Brooklyn and Queens entries). The current official all-starred "
        "listing shows 69 starred (5/14/50). Per-name current status was verified only for 13 restaurants; "
        "the remaining names are flagged unverified."
    )
    f = by_id(flags, "F08")
    f.update({
        "title": "Instagram review coverage incomplete; MoMA placeholder removed",
        "detail": "Instagram site-restricted searches returned official accounts/location pages rather than third-party reviews. Such links are labeled 'official account' and are not presented as reviews. An unrelated Statue of Liberty Instagram location placeholder accidentally attached to MoMA was removed; no verified Instagram review link for MoMA remains.",
        "sources": ["youtube_lb", "moma", "repo"],
        "page": "social.html",
    })
    f = by_id(flags, "F01")
    f.update({
        "severity": "medium",
        "title": "Four of six hotel 7-night totals remain unverified",
        "detail": "Real dated official 7-night quotes were captured for Pod 51 and Arlo NoMad. 11 Howard, citizenM New York Times Square, AC Hotel New York Times Square and The Westin New York at Times Square still have blank totals; no estimate was substituted. Arlo's displayed total also excludes taxes.",
        "sources": ["pod51_booking_7n", "arlo_booking_7n", "howard_booking", "citizenm_property"],
        "page": "hotels.html",
    })
    flags.extend([
        {"id": "F13", "severity": "medium", "title": "Arlo Cyber Sale stay-date end conflict",
         "detail": "Official Arlo Cyber Exclusive Access page: 40% off, sale ends 3 Dec 2026, NYC stay dates through 31 Oct 2027. Official Arlo booking page rate description: 'Book by December 3 ... stay dates through December 2027'. Both cited; neither corrected.",
         "sources": ["arlo_cyber", "arlo_booking_7n"], "page": "dates.html"},
        {"id": "F14", "severity": "medium", "title": "Hotel 7-night totals are not like-for-like",
         "detail": "Pod 51 Queen Pod $1,109 states 'Including taxes and fees'. Arlo NoMad Queen $1,296 states 'Including the urban fee, excluding taxes'. No official Arlo tax amount was published on the fetched page, so the final Arlo total and the true cheapest hotel cannot be confirmed.",
         "sources": ["pod51_booking_7n", "arlo_booking_7n"], "page": "hotels.html"},
        {"id": "F15", "severity": "low", "title": "No market-wide cheapest booking time is officially verified",
         "detail": "Arlo 40% off (book by 3 Dec 2026) and Marriott 15%/25% off (book by Tuesday 1 Dec) are the highest verified in-window discounts among the offers checked. No official source compares all NYC hotels or publishes a single best time to book; the claim is qualified, not presented as market-wide proof.",
         "sources": ["arlo_cyber", "marriott_cyber", "hotel_week"], "page": "dates.html"},
        {"id": "F16", "severity": "low", "title": "Pod 51 facility fee not itemized in booking total",
         "detail": "Official FAQ lists a $29.84 incl-tax facility fee per room per night. The 7-night booking page says totals include taxes and fees but does not itemize that facility fee; no amount was added or subtracted manually.",
         "sources": ["pod51_faq", "pod51_booking_7n"], "page": "hotels.html"},
    ])

    # -----------------------------------------------------------------------
    # Verification log
    # -----------------------------------------------------------------------
    verification = FILES["verification.json"]
    verification["checks"].extend([
        {"check": "Official MICHELIN new-additions article fetched in all 6 chunks; November, July and April 2026 Selection additions transcribed with exact official URLs.", "result": "pass", "sources": ["michelin_additions"]},
        {"check": "Official Pod 51 SynXis booking page fetched with correct arrive/depart parameters; Queen Pod 7-night totals incl taxes and fees captured ($1,109 member / $1,310 Stay 4 & Save).", "result": "pass", "sources": ["pod51_booking_7n"]},
        {"check": "Official Arlo NoMad booking page fetched for 15–22 Feb 2027; Queen 7-night totals incl urban fee / excl taxes captured ($1,296 / $1,985 / $2,195).", "result": "pass", "sources": ["arlo_booking_7n"]},
        {"check": "Official Arlo Cyber Exclusive Access page fetched; 40% off, sale ends 3 Dec 2026, NYC stays through 31 Oct 2027, code CYBER.", "result": "pass", "sources": ["arlo_cyber"]},
        {"check": "Official Marriott CYBER SALE offer page fetched; 15%/25% off, code QRI, book by Tuesday 1 Dec, valid stay dates 29 Nov 2026–2 May 2027.", "result": "pass", "sources": ["marriott_cyber"]},
        {"check": "Official Marriott citizenM New York Times Square property and rooms pages fetched for address, ZIP, XL king bed and amenities.", "result": "pass with private-bathroom wording still blank", "sources": ["citizenm_property", "citizenm_rooms"]},
        {"check": "Official 11 Howard booking/availability page fetched; dated query did not return a quote, so the 7-night total remains blank.", "result": "no price invented", "sources": ["howard_booking"]},
        {"check": "Official Met weekly hours confirmed by a site-restricted official-domain search extract; closed Wednesdays and $30 admission confirmed by direct homepage fetch.", "result": "pass", "sources": ["met_hours", "met_home", "met"]},
        {"check": "Official 2025 star article re-fetched; the roster name 'Jungsik' resolves to the current MICHELIN page 'Jungsik New York' (3 stars), fixing the name/status mismatch.", "result": "pass", "sources": ["michelin_stars_2025", "michelin_page_jungsik-new-york"]},
        {"check": "MICHELIN new-additions article chunks 0–5 re-fetched line by line; all November, July and April 2026 names, months and exact restaurant-page URLs revalidated against the article.", "result": "pass", "sources": ["michelin_additions"]},
        {"check": "Current MICHELIN pages and official restaurant websites fetched for Noury, Mūje and Nyonya; Noury/Nyonya hours and Nyonya address/ZIP/cash-only exception verified, Mūje hours remain blank.", "result": "pass with Mūje hours blank", "sources": ["michelin_page_noury", "noury_official", "michelin_page_muje", "muje_official", "michelin_page_nyonya", "nyonya_official"]},
        {"check": "Unrelated Statue of Liberty Instagram location placeholder removed from the MoMA row; only verified MoMA YouTube review links remain.", "result": "pass", "sources": ["moma", "repo"]},
    ])

    # -----------------------------------------------------------------------
    # Executive summary
    # -----------------------------------------------------------------------
    es = FILES["executive_summary.json"]
    es["headline"] = (
        "A verified evidence base for a 15 February – 23 March 2027 New York trip for 2 adults, "
        "with two real dated 7-night hotel quotes, official in-window booking deadlines, and every "
        "remaining unconfirmed value left blank and flagged."
    )
    kp = {k["title"]: k for k in es["key_points"]}
    kp["Cheapest verified booking window"]["text"] = (
        "NYC Hotel Week 2027 (2 Jan–11 Feb 2027, 25% off) ends before the requested window. Two official "
        "in-window offers were verified instead: Arlo Hotels Cyber Exclusive Access (40% off, book by 3 Dec 2026, "
        "code CYBER, NYC stays through 31 Oct 2027) and Marriott CYBER SALE at citizenM (15%/25% off, book by "
        "Tuesday 1 Dec, code QRI, stays 29 Nov 2026–2 May 2027). No official source proves a market-wide cheapest price."
    )
    kp["Cheapest verified booking window"]["sources"] = ["hotel_week", "hotel_week_about", "arlo_cyber", "marriott_cyber"]
    kp["MICHELIN picture"]["text"] = (
        "The current official NYC listing shows 69 starred restaurants: 5 three-star, 14 two-star, 50 one-star; "
        "plus 76 Bib Gourmand and 224 Selected (no star). The full 2025 star roster, 13 individually re-verified "
        "starred restaurants, and the November/July/April 2026 Guide-listed new additions are catalogued with "
        "official links and explicit star-vs-listed status."
    )
    kp["MICHELIN picture"]["sources"] = ["michelin_all_starred", "michelin_nyc", "michelin_stars_2025", "michelin_additions"]
    kp["Hotels"]["text"] = (
        "6 candidate hotels are documented with official sources. Two real 7-night quotes for 15–22 Feb 2027 "
        "were captured: Pod 51 Queen Pod $1,109 incl taxes & fees (Pod Member Rate) and Arlo NoMad Queen $1,296 "
        "incl urban fee but excl taxes (The Steal Deal). Pod 51 is the only hotel with both a queen bed and a "
        "private bathroom confirmed verbatim, and the lowest verified all-in total. Four totals remain blank."
    )
    kp["Hotels"]["sources"] = ["pod51_booking_7n", "arlo_booking_7n", "pod51_rooms", "pod51_faq", "citizenm_property", "arlo_nomad"]
    kp["Cluster / travel analysis"]["text"] = (
        "Starred restaurants are grouped into clusters using ZIP codes on official MICHELIN pages; a verified "
        "same-ZIP view puts citizenM (10019) at 3, Pod 51 (10022) at 1 and Arlo (10016) at 1 of the 13 detailed "
        "starred restaurants. The requested 'within 1 hour by subway or bus' count cannot be verified from a "
        "static official source; those numbers and the resulting hotel ranking remain blank, with an MTA Trip "
        "Planner workflow supplied instead."
    )
    kp["Cluster / travel analysis"]["sources"] = ["michelin_all_starred", "mta_trip", "mta_maps", "pod51_booking_7n", "arlo_booking_7n", "citizenm_property"]
    kp["Decision status"]["text"] = (
        "7 of 12 questions still block a decision (dates, complete hotel totals, market-wide booking timing, "
        "room requirements, transit counts, star-list currency, itinerary feasibility). Two hotel quotes and two "
        "official booking deadlines are now partially answered; none of the remaining gaps were filled with guesses."
    )
    kp["Site & governance"]["text"] = (
        "A mobile-friendly static dashboard with category subpages, a machine-readable data corpus, an automated "
        "build/verification script, a dedicated Suggestions page and a Flagged for Review page. Parallel-session "
        "scopes are recorded in COORDINATION.md; the other session's root site is preserved as a separate artifact."
    )
    es["decision_gates"] = [
        {"gate": "Choose dates", "status": "blocked", "blocking": ["Q01", "Q03"]},
        {"gate": "Set hotel budget", "status": "partial", "blocking": ["Q02", "Q03"]},
        {"gate": "Shortlist hotels", "status": "blocked", "blocking": ["Q04", "Q05"]},
        {"gate": "Lock restaurant list", "status": "partial", "blocking": ["Q06", "Q07"]},
        {"gate": "Build daily itinerary", "status": "blocked", "blocking": ["Q09", "Q12"]},
        {"gate": "Publish final plan", "status": "blocked", "blocking": ["Q10", "Q11"]},
    ]
    es["verified_numbers"] = {
        "starred_restaurants_current": 69,
        "three_star": 5, "two_star": 14, "one_star": 50,
        "bib_gourmand": 76, "selected_restaurants": 224,
        "detailed_starred_restaurants": 13,
        "guide_listed_catalogued": len(michelin["guide_listed"]),
        "activities": len(FILES["activities.json"]),
        "hotels": len(hotels),
        "hotels_with_7n_quotes": 2,
        "lowest_verified_all_in_7n_total": "$1,109 (Pod 51 Queen Pod, 15–22 Feb 2027)",
        "official_sources": len(S),
        "checked": CHECKED,
    }

    # -----------------------------------------------------------------------
    # Repo review: record that the parallel root site now exists
    # -----------------------------------------------------------------------
    rr = FILES["repo_review.json"]
    rr["findings"].append({
        "item": "origin/arena/7386fd81-nyfun3 root site",
        "verified": "Yes — git fetch / git ls-tree / git show FETCH_HEAD:COORDINATION.md on 2026-11-25.",
        "irregularity": "That branch now contains index.html, assets/style.css and pages/*.html and marks its task 'needs review'. It reports no comparable hotel prices or routes and a Met Thursday source conflict. This session does not edit those files; the final integration request is logged in COORDINATION.md.",
        "source": "git show FETCH_HEAD:COORDINATION.md (origin/arena/7386fd81-nyfun3)",
    })

    # Governance / derived-analysis rows still need an official source link on
    # every published table row. The repository itself is the official source
    # for those governance statements.
    by_id(flags, "F12")["sources"] = ["repo"]
    for kp in es["key_points"]:
        if not kp.get("sources"):
            kp["sources"] = ["repo"]
    for s in suggestions:
        s.setdefault("sources", ["repo"])
    for finding in rr["findings"]:
        finding.setdefault("sources", ["repo"])
    for check in verification["checks"]:
        if not check.get("sources"):
            check["sources"] = ["repo"]
    for gate in es["decision_gates"]:
        gate.setdefault("sources", ["repo"])
    for z in analysis["zip_clusters"]:
        z.setdefault("sources", ["michelin_all_starred"])

    return FILES
