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
