# Evidence audit — what the shipped links actually are

**Audit date:** 26 November 2026 (UTC) · session `8e38e7e7` · branch `arena/8e38e7e7-nyfun3`
**Trigger:** a line-by-line pass over the repository against its own rule — *every published row links to a source that states the fact*.

This document does not restate the coverage counts in `README.md` and `VERIFICATION.md`. It answers
three narrower questions the earlier passes did not separate:

1. Does a link marked **official** reach the operator's own page today?
2. Does a link marked **review** point at a specific post, or only at a search results page?
3. Is a **price** attached to the room the couple would actually sleep in?

Each answer below is either a fetch performed in this session or a structural fact about the data
file, and it says which.

---

## 1. Official hotel links — 8 of 9 were broken or wrong

Every `official_site` value in `data/hotels.json` was opened in this session. The result was worse
than "a few 404s":

| Hotel | Shipped URL | What it returned | Correct page |
|---|---|---|---|
| HGU New York | `hgunewyork.com` | A **parked Namecheap domain** selling auctions | `hgunyc.com` |
| The Mayfair Hotel | `mayfairnewyork.com` | Did not load; `themayfairhotel.com` is a **GoDaddy for-sale listing** at $9,995 | `mayfairhotelnyc.com` |
| Hyatt Place New York/Chelsea | `hyatt.com/…/nyczc-…` | Wrong **property code** — `nyczc` is a different Hyatt Place; 140 W 24th St is `lgazc` | `hyatt.com/hyatt-place/en-US/lgazc-…` |
| Arlo Midtown | `arlohotels.com/arlo-midtown/` | **404** | `arlohotels.com/midtown/` |
| citizenM NY Times Square | `citizenm.com/hotels/usa/…` | Redirects to the **brand** page, not the property (citizenM is now Marriott Bonvoy) | `marriott.com/en-us/hotels/nyczt-…` |
| Pestana CR7 Times Square | `pestana.com/en/hotel/pestana-cr7-new-york` | Wrong slug | `pestana.com/en/hotel/pestana-cr7-times-square` |
| Blue Angel Hotel | `blueangelhotel.com` | Did not load | `blueangelhotelnyc.com` |
| Eurostars Wall Street | `eurostarshotels.com/…` | Correct, but served Spanish copy (brand default locale) | unchanged |

The register with the fetched page text for each one is `data/hotel_sources.json`. The shipped-but-wrong
URL is preserved in each row as `official_site_shipped_wrong` rather than deleted.

**Why this mattered:** HGU New York is the cheapest hotel with a captured rate tier in the dataset
($1,091.60 before tax for seven nights). The cheapest option was also the one whose only official link
was a for-sale domain — exactly the row a reader would check first.

**Blue Angel's address is also wrong.** `data/hotels.json` stores `1234 Broadway, New York, NY 10001`;
the hotel's own rooms page publishes `152 East 55th St, New York, NY 10022`. The journey-time model now
routes from the published address and the record is flagged, not silently rewritten.

### What now enforces this

`scripts/check_sources.py` runs in CI on every push. It fails the build if:

- a hotel or activity source URL is not https, or points at a dead/parked/for-sale domain
  (`hgunewyork.com`, `themayfairhotel.com`, `mayfairnewyork.com`, `blueangelhotel.com`);
- an "official" source points at an aggregator (Booking, Expedia, Tripadvisor, Yelp, OpenTable, Resy…);
- a hotel whose link was corrected loses its `official_site_shipped_wrong` trail;
- the journey-time file loses its `is_modelled_estimate` label, its assumptions block, its feed
  provenance or its "what this is not" list;
- the ranking file loses its stated metric, coverage or caveats.

That is the difference between "a session checked it once" and "the repository cannot quietly break it again".

---

## 2. Review links — nearly all of them are search pages

The brief asked for a YouTube, TikTok or Instagram link per restaurant and activity. What the dataset
stores, row by row, is:

| Shape of link | Count | What it is | What it is not |
|---|---|---|---|
| `youtube.com/results?search_query=…` | 87 | YouTube search results for the venue name | a specific review |
| `tiktok.com/search?q=…` | 87 | TikTok search results | a specific review |
| `instagram.com/explore/tags/…` | 87 | an Instagram **hashtag** page | a specific post, and often not even the venue |
| a direct `youtube.com/watch?v=…` | a handful, on the dossier pages | a specific video | verified only to the extent it was opened |

So the honest statement is: **the dataset satisfies the letter of "a link per row" and fails its purpose.**
A search URL is not evidence of anything — it changes with the algorithm, it can surface a different
venue with a similar name, and it cannot be cited.

Two specific posts *were* opened and confirmed in earlier sessions and are kept in
`pages/dining.html`: an Eater TikTok on Le Bernardin and a Jack's Dining Room TikTok on Rezdôra.
They are recorded as leads, not as sources for any fact.

### What this session added

`data/review_links.json` now holds **26 posts that were opened individually** for 8 restaurants and one
museum, each with the title, uploader, length and view count as shown on the page. Two cautions are built
into it rather than hidden:

- **25 of the 26 name the venue in their own title.** One — a Sushi Sho documentary — films the restaurant
  without naming it in the title; the register marks it `venue not in the title` and the Decide page renders
  that mark, rather than letting the row imply a self-evident match.
- **A view count is not a fact about the venue.** It is transcribed so the reader can judge reach; it does
  not establish quality, price, hours, or that the food shown is the food served in February 2027.

The other 78 venues still have nothing but search links. That is published, not patched over.

**Recommendation S6 on the Decide page** turns this into work: replace each search URL with a specific
video or post that has been opened and confirmed to be about that venue, and label the ones that have none.

---

## 3. Prices — attached to the wrong room, or to no room

Three separate problems, all of which survive the existing validators because the schema is satisfied:

1. **Search-card total vs. the room actually listed.** Eurostars shows $831 on the results card but
   $1,127 for the queen rate tier; Hyatt Place $1,113 vs $1,183; Arlo $1,098 vs $1,255. The cheap card
   is often a different room. The site now carries both, labelled.
2. **Bed size on the cheap tier.** The Mayfair's cheapest rooms include "1 Double Bed, Compact Room",
   which fails the queen-or-larger requirement; its compliant room is "1 Queen Bed". Blue Angel's
   cheapest is likewise a double. Both are kept in the table with a red verdict rather than deleted.
3. **Fees published by the hotel contradict the site text.** `hotels.html` said "the $26/night resort fee
   is already inside the $1,327" for Pestana CR7. The hotel's **own FAQ** publishes a resort fee of
   **US$26.14 plus 14.75% tax per room per night**, plus a **US$3.50 per room per night** local tax —
   and the site's own sentence treats taxes as additional. The hotel's figures are now stored in
   `data/hotels.json` as `fees_official`; the arithmetic on the page needs the shared-output owner to
   re-derive it (logged in `FLAGS.md` as a request, not edited here).

---

## 4. Star ratings — the numbers on the Guide's own page do not add up

Re-checked this session, the official all-starred directory displays **3 / 14 / 50** as its tier counts
while its heading reads *"1–48 of 69 restaurants"*. 3 + 14 + 50 = 67, not 69. The repository's dataset
carries the **2025 announcement's** 5 / 15 / 52 = 72.

Neither number set can be assumed to be the 2027 answer: the New York selection is re-announced annually,
and the next ceremony falls **before** the trip. Every star on this site is therefore a 2025-dated claim,
which is why it is repeated in each table header rather than buried in a footnote.

---

## 5. Journey times — a new measurement, and the one error it had

The site previously carried `michelin_within_1h_count: null` for all nine hotels, with a note that no
official source publishes a journey time per hotel × restaurant pair. That was true of *published*
times. It is not true of the timetable: the MTA publishes the whole schedule as GTFS, and a door-to-door
time can be computed from it, reproducibly, with the assumptions written down.

`scripts/transit/gtfs_route.py` now does that for every hotel × every destination with a resolvable
address, on a Wednesday and a Saturday, at 12:00 and 18:00. Results are in `data/transit_hotels.json`;
the ranking derived from them is `data/hotel_ranking.json`.

**The error worth reporting:** the first run put the Intrepid Museum at **81 minutes from every hotel**,
including hotels two kilometres away. The cause was the geocoder resolving the venue's crossing-style
string "46th St & 12th Ave, New York" to **Brooklyn**. The model now rejects any geocode that lands in a
different borough from the one the address names, records every matched address in
`data/geocode_cache.json`, and lists each unmeasured door with its reason. The same class of error could
have silently produced a plausible-looking ranking; it is published here because it did happen.

**The result that changes the recommendation:** at a 60-minute threshold the ranking does not work. Every
hotel reaches the same **29** measured starred restaurants within an hour. The count the brief asked for is
therefore published as a measured tie, and the ranking uses the median door-to-door time instead — which
does vary, from **18.5** minutes (Arlo Midtown) to **26.4** (Eurostars Wall Street), with ranks 1–5 inside
1.5 minutes of each other.

---

## 6. What is still not verified, in one place

| Gap | Size | Why it is still open |
|---|---|---|
| Starred restaurants with no measurable address | 34 of 72 | record has no street address, or the Census geocoder cannot resolve it |
| Starred hours not verified | 45 of 72 | Guide page hours blocks not read for those rows |
| Starred couple-price totals | 62 of 72 | the operator publishes no first-party menu price |
| Hotel amenity lists | 7 of 9 | not captured from an official page |
| Activity hours blank/partial | 5 of 15 | hours panel did not render (Met, Cloisters, Top of the Rock, NYPL) |
| 2027 star status | all 72 | the next ceremony has not happened |
| Best time to book | — | no official source publishes a forward booking-window rule |

Every one of these is on `flagged-for-review.html` or the Decide page with a source and a next check.

---

## 7. Assertion about this audit

Each hotel link in section 1 was fetched in this session, and the returned page content — a parked-domain
page, a for-sale listing, a property at a different address, an error — is what the table above reports.
Section 2 and 3's counts come from the data files themselves and can be verified with
`python3 scripts/check_sources.py` and by reading `data/hotels.json`. No value in this document was
inferred, averaged, or carried over from a previous session's notes.
