# Verification

Checked 2026-11-25. Full verification page: [`docs/verification.html`](docs/verification.html). Automated report: [`docs/verification-report.txt`](docs/verification-report.txt).

## Rules

- Every rendered table row carries at least one link to an official source (MICHELIN Guide, the venue's own site, a government/DMO site, the hotel's own site, or an MTA page).
- A value that could not be confirmed from an official source is left blank, rendered as '— unverified', and listed on the Flagged for Review page.
- No value is inferred, estimated, or copied from a third-party travel blog. Third-party content is used only as social-media review links on the platform's own domain.
- Prices labelled 'subtotal for 2' are pure arithmetic (official per-person price × 2) and are explicitly marked as excluding tax, gratuity and beverages where the official source says so.
- Weekday values are computed with Python datetime from ISO dates, not estimated.
- Social links were obtained either by fetching a YouTube/TikTok platform page directly or via a site-restricted search of that platform's domain; the video content is never used as a factual data source.

## Checks

| Check | Result | Sources |
| --- | --- | --- |
| Official MICHELIN 2025 star article fetched in 5 chunks; all star names and URLs transcribed. | pass | michelin_stars_2025 |
| Current official all-starred NYC listing fetched; counts 5/14/50 = 69 recorded. | pass | michelin_all_starred |
| Current official NYC selection listing fetched; 76 Bib Gourmand, 224 Selected, 369 total recorded. | pass | michelin_nyc |
| 13 individual current MICHELIN restaurant pages fetched for address, star level, cuisine and per-day hours. | pass | michelin_all_starred |
| Official restaurant menu/FAQ pages fetched for per-person prices (Le Bernardin PDF, EMP FAQ, The Modern menu). | pass | lb_lunch, emp_faq, modern |
| Official venue hours pages fetched for MoMA, AMNH, NPS, 9/11 Memorial, High Line, Whitney, One World Observatory, Top of the Rock, ESB, Met, NYC Parks. | pass with exceptions logged | moma, amnh, nps, 911, highline, whitney, owo, toprock, esb, met, centralpark |
| Official NYC Tourism Hotel Week pages + press release fetched for dates, discount and booking opening. | pass | hotel_week, hotel_week_about, hotel_week_press |
| OPM 2027 federal holiday schedule fetched for 15 Feb 2027. | pass | opm |
| Official hotel pages fetched for Pod 51 (rooms/FAQ/location), 11 Howard, Arlo NoMad (DMO), citizenM (Marriott brand). | pass with blanks logged | pod51_rooms, pod51_faq, howard, arlo_nomad, citizenm |
| MTA official maps / Trip Planner / subway guide located; no static travel-time matrix exists. | travel-time values intentionally blank | mta_maps, mta_trip, mta_riding |
| Hilton / Hyatt / SynXis / some Marriott rate pages returned JS shells, redirects or errors; no price was captured. | no price invented | hotel_week |
| Official hotel 7-night totals could not be confirmed; all price cells left blank. | unverified by design | hotel_week |
| Site generator validates each row has >=1 official source, flags blanks, and checks internal links resolve. | automated in tools/build_site.py | repo |
| Official MICHELIN new-additions article fetched in all 6 chunks; November, July and April 2026 Selection additions transcribed with exact official URLs. | pass | michelin_additions |
| Official Pod 51 SynXis booking page fetched with correct arrive/depart parameters; Queen Pod 7-night totals incl taxes and fees captured ($1,109 member / $1,310 Stay 4 & Save). | pass | pod51_booking_7n |
| Official Arlo NoMad booking page fetched for 15–22 Feb 2027; Queen 7-night totals incl urban fee / excl taxes captured ($1,296 / $1,985 / $2,195). | pass | arlo_booking_7n |
| Official Arlo Cyber Exclusive Access page fetched; 40% off, sale ends 3 Dec 2026, NYC stays through 31 Oct 2027, code CYBER. | pass | arlo_cyber |
| Official Marriott CYBER SALE offer page fetched; 15%/25% off, code QRI, book by Tuesday 1 Dec, valid stay dates 29 Nov 2026–2 May 2027. | pass | marriott_cyber |
| Official Marriott citizenM New York Times Square property and rooms pages fetched for address, ZIP, XL king bed and amenities. | pass with private-bathroom wording still blank | citizenm_property, citizenm_rooms |
| Official 11 Howard booking/availability page fetched; dated query did not return a quote, so the 7-night total remains blank. | no price invented | howard_booking |
| Official Met weekly hours confirmed by a site-restricted official-domain search extract; closed Wednesdays and $30 admission confirmed by direct homepage fetch. | pass | met_hours, met_home, met |
| Official 2025 star article re-fetched; the roster name 'Jungsik' resolves to the current MICHELIN page 'Jungsik New York' (3 stars), fixing the name/status mismatch. | pass | michelin_stars_2025, michelin_page_jungsik-new-york |
| MICHELIN new-additions article chunks 0–5 re-fetched line by line; all November, July and April 2026 names, months and exact restaurant-page URLs revalidated against the article. | pass | michelin_additions |
| Current MICHELIN pages and official restaurant websites fetched for Noury, Mūje and Nyonya; Noury/Nyonya hours and Nyonya address/ZIP/cash-only exception verified, Mūje hours remain blank. | pass with Mūje hours blank | michelin_page_noury, noury_official, michelin_page_muje, muje_official, michelin_page_nyonya, nyonya_official |
| Unrelated Statue of Liberty Instagram location placeholder removed from the MoMA row; only verified MoMA YouTube review links remain. | pass | moma, repo |

Every table row on the site carries at least one official source link; blank values are rendered as unverified and listed on the Flagged for Review page.
