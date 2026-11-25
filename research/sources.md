# Official source ledger

Last updated: 2026-11-25 UTC
Verification rule: a row is **verified** only when its value is read from an official source listed here or in `generated/*.json`. Unconfirmed values are blank and flagged `unverified`. Search snippets are used only to discover URLs; factual values are taken from the linked official page itself.

## Canonical official sources

| ID | Official source | URL | Used for | Access check |
|---|---|---|---|---|
| SRC-MICHELIN-NYC | MICHELIN Guide — NYC and surroundings restaurant directory | https://guide.michelin.com/us/en/new-york-state/new-york/restaurants | Current guide category counts: 3 stars 5, 2 stars 14, 1 star 50, Bib Gourmand 76, Selected Restaurants 224; total 369 | Opened 2026-11-25 |
| SRC-MICHELIN-STARRED | MICHELIN Guide — all starred NYC restaurants | https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred | Starred status and star level | Opened 2026-11-25 |
| SRC-MICHELIN-RESTAURANT | MICHELIN Guide individual restaurant pages | `https://guide.michelin.com/us/en/new-york-state/new-york/restaurant/<slug>` | Name, address, coordinates, cuisine, price category, official description | Diagnostics pending |
| SRC-MTA-HOME | Metropolitan Transportation Authority | https://www.mta.info/ | Official MTA identity and current service information | Opened 2026-11-25 |
| SRC-MTA-APPS | MTA official apps and trip planning | https://www.mta.info/guides/apps | Official trip planning across subway and bus | Opened 2026-11-25 |
| SRC-MTA-TRIP-HELP | MTA NYC Transit Trip Planner help | http://tripplanner.mta.info/widget/help.htm | Official description of subway/bus trip-planning options | Search-indexed 2026-11-25; direct fetch failed and is flagged |
| SRC-MTA-GTFS | MTA Developer Resources / static GTFS feeds | https://www.mta.info/developers | Official subway and bus schedule data; current-feed limitation | Opened 2026-11-25 |
| SRC-MTA-GTFS-TRANSITION | MTA schedule-transition guidance | https://www.mta.info/developers/gtfs-schedules-transition | Current GTFS feeds are not 2027 service guarantees | Opened 2026-11-25 |
| SRC-HYATT-MIDTOWN | Hyatt Place New York/Midtown-South official hotel page | https://www.hyatt.com/hyatt-place/en-US/nyczm-hyatt-place-new-york-midtown-south | Address, room types, amenities, official hotel source | Opened 2026-11-25 |
| SRC-HYATT-TIMES-SQUARE | Hyatt Place New York City / Times Square official hotel page | https://www.hyatt.com/hyatt-place/en-US/nyczt-hyatt-place-new-york-city-times-square | Address, room types, amenities, official hotel source | Opened 2026-11-25 |
| SRC-HYATT-RATES | Hyatt official dated room-shop pages | `https://www.hyatt.com/shop/rooms/<spiritCode>?checkinDate=YYYY-MM-DD&checkoutDate=YYYY-MM-DD&rooms=1&adults=2&kids=0&rate=Standard&accessibilityCheck=false` | Actual dated rates for 1 room / 2 adults | Opened 2026-11-25; structured-rate extraction pending |
| SRC-HILTON-TIMES-SQUARE-CENTRAL | Hilton Garden Inn New York/Times Square Central official hotel page | https://www.hilton.com/en/hotels/nycssgi-hilton-garden-inn-new-york-times-square-central/ | Address, room types, amenities | Search-indexed 2026-11-25 |
| SRC-MARRIOTT-FAIRFIELD | Fairfield by Marriott Times Square South official hotel page | https://www.marriott.com/hotels/travel/nycmw-fairfield-inn-and-suites-new-york-manhattan-times-square-south/ | Address, room types, amenities | Search-indexed 2026-11-25 |
| SRC-IHG-HIE | Holiday Inn Express Manhattan Times Square South official rooms page | https://www.ihg.com/holidayinnexpress/hotels/us/en/new-york/nycts/hoteldetail/rooms | Bed types and room amenities | Opened 2026-11-25 |
| SRC-GITHUB-PAGES | GitHub repository Pages configuration API | https://api.github.com/repos/kanlerxz87-cyber/NYFun3/pages | Existing Pages source and URL | Opened 2026-11-25 |
| SRC-CENSUS-GEOCODER | U.S. Census Bureau geocoder | https://geocoding.geo.census.gov/geocoder/locations/onelineaddress | Official address-to-coordinate lookup for transit analysis | Diagnostics pending |

## Source-use notes

- MICHELIN Guide category counts are a snapshot accessed on 2026-11-25 and can change when the Guide updates.
- MTA static GTFS feeds represent current schedules, not guaranteed February–March 2027 service. Any 2027 travel-time ranking built from them is labeled with that limitation.
- Hotel prices are dynamic. Each published price must carry the exact check-in/check-out dates, guest count, rate name, currency, and access timestamp from the official booking page.
- Social media links are supplementary. A link found on YouTube, TikTok, or Instagram is not used to verify a venue's hours, price, address, or Michelin status.
- Third-party social reviews are opinions, not official venue facts; the official venue/Michelin source verifies each table row.
- Jina Reader (`https://r.jina.ai/`) is used only as a browser-rendering/retrieval proxy for official public pages that block plain HTTP clients. Its returned HTML or text is not itself an authoritative source; every diagnostic record preserves the original official URL, and published rows cite the official venue/Michelin/MTA/hotel URL.

## Final-integration first-party values (2026-11-25, session `ed92e764`)

These pages were fetched during final integration and are the official sources behind newly published values. A fetched page is a **current baseline**, not a 2027 calendar or price guarantee. Social videos, search snippets, blogs and aggregators are never used as factual sources.

| ID | Official source | URL | Published use |
|---|---|---|---|
| SRC-EMP-FAQ | Eleven Madison Park FAQ | https://www.elevenmadisonpark.com/faq | Full Tasting $385/guest, Bar Tasting $255/guest, lounge from $225/guest; couple figures rendered as 2 × the official per-guest amount. |
| SRC-LB-DINNER | Le Bernardin official dinner PDF | https://www.le-bernardin.com/content/pdfs/dinner-1.2.pdf | Four-course dinner $218/person. |
| SRC-LB-LUNCH | Le Bernardin official lunch PDF | https://www.le-bernardin.com/content/pdfs/lunch-2.191.pdf | Three-course lunch $137/person. |
| SRC-DANIEL-PF | Daniel official prix-fixe page | https://www.danielnyc.com/cuisine/prix-fixe | Three-course $195/person and five-course $255/person. |
| SRC-DANIEL-TASTING | Daniel official tasting-menu page | https://www.danielnyc.com/cuisine/tasting-menu | Seven-course and vegetarian tasting $295/person. |
| SRC-COTE-MENU | COTE NYC official dinner menu | https://www.cotekoreansteakhouse.com/nycdinnermenu | Butcher's Feast $84/person and Steak Omakase $225/person. |
| SRC-GRAMERCY-MENU | Gramercy Tavern official Dining Room menu | https://www.gramercytavern.com/dining-room-menu/ | Seasonal menu $178/person. |
| SRC-MASA-MENU | Masa official menus | https://www.masanyc.com/menus | Lunch starting $495/person, Hinoki $950/person, Table $750/person; official exclusions for beverages/tax/optional gratuity. |
| SRC-COUCOU | Le Coucou official menu page | https://lecoucou.com/ | Dinner prix fixe and lunch/Clock Strikes/Very Coucou per-person prices. |
| SRC-AQUAVIT-MENU | Aquavit official November 2026 dinner PDF | https://www.aquavit.org/s/DR-112026.pdf | Tasting menu 195PP. |
| SRC-AQUAVIT-CHEF | Aquavit official November 2026 chef's PDF | https://www.aquavit.org/s/DR-112026-Chefs.pdf | Chef's tasting 305PP. |
| SRC-MODERN-MENU | The Modern official menu page | https://www.themodernnyc.com/the-modern/ | Three-course lunch $115/person, Impressions $185/person, Abstractions $285/person, and other per-person menu amounts. |
| SRC-REZDORA-MENU | Rezdôra official menus | https://www.rezdora.nyc/menus/ | Regional pasta tasting $110/person; optional $90/person wine pairing is listed but excluded from the base couple subtotal. |
| SRC-JUNGSIK-MENU | Jungsik official menu | https://www.jungsik.com/menu/ | Checked but left UNVERIFIED in the root dataset because the fetched text prints “SIGNATURE MENU:335” without a currency symbol or explicit per-person wording. |
| SRC-CROWNSHY-MENU | Crown Shy official menus | https://www.crownshy.nyc/menus/ | Checked à la carte prices; left UNVERIFIED as a fixed couple price because no fixed per-person menu was published. |
| SRC-NPS-HOURS | NPS Statue of Liberty official hours | https://www.nps.gov/stli/planyourvisit/hours.htm | Park 09:00–16:30, Info Center 09:30–16:30, last statue entrance 15:30, ferry-only access; not ferry sailings. |
| SRC-HIGHLINE-VISIT | High Line official visit page | https://www.thehighline.org/visit/ | Seasonal winter hours 1 Dec–31 Mar 07:00–20:00. |
| SRC-CENTRALPARK-VISIT | Central Park Conservancy official visit page | https://www.centralparknyc.org/visit | 06:00–01:00, 365 days/year; weather alerts can change access. |
| SRC-GRANDCENTRAL-VISIT | Grand Central Terminal official visit page | https://grandcentralterminal.com/visit/ | Public terminal hours 05:15–02:00 daily; individual businesses may differ. |
| SRC-MOMA-VISIT | MoMA official visit page | https://www.moma.org/visit/ | Adult $30 and weekday hours; galleries close about 15 minutes before museum closing. |
| SRC-AMNH-HOURS | AMNH official hours page | https://www.amnh.org/plan-your-visit/hours | Daily 10:00–17:30 baseline; holiday extensions are not 2027 confirmations. |
| SRC-WHITNEY-VISIT | Whitney official visit page | https://whitney.org/visit | Adult $30, Tuesday closed, Friday until 22:00. |
| SRC-GUGGENHEIM-VISIT | Guggenheim official plan-your-visit page | https://www.guggenheim.org/plan-your-visit | Adult $30 and daily 10:30–17:30 baseline. |
| SRC-911-VISIT | 9/11 Memorial & Museum official visit page | https://www.911memorial.org/visit/visit-museum-1 | Museum Wed–Mon/select Tuesdays 09:00–19:00, Memorial daily 08:00–20:00, timed tickets. |
| SRC-INTREPID-TICKETS | Intrepid Museum official tickets page | https://intrepidmuseum.org/plan-your-visit/visitor-information/tickets | Adult $38 and Oct–Mar daily 10:00–17:00 winter baseline. |
| SRC-CITYPASS | New York CityPASS official page | https://www.citypass.com/new-york | Adult $149, child $129, nine-day validity and box-office comparison. |

**Unwritten constraints:** no 2027 MICHELIN stars, subway/bus journey counts, hotel all-in totals, date-specific admission prices, restaurant holiday exceptions, or 2027 calendar confirmations were inferred. Blank + `unverified` remains the published state wherever an official source does not state the value.
