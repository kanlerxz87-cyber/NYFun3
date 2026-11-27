/* Decision cockpit renderers. Values come directly from committed evidence JSON. */
(function () {
  "use strict";

  var NYF = window.NYF || {};
  var esc = NYF.esc || function (s) { return String(s == null ? "" : s); };
  var link = NYF.srcLink || function (url, label) {
    return url ? '<a href="' + esc(url) + '" target="_blank" rel="noopener noreferrer">' + esc(label || "source") + "</a>" : "";
  };
  var unver = NYF.unverified || function () { return '<span class="unver">unverified</span>'; };
  var GUIDE_URL = "https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred";
  var GEOCODER_URL = "https://geocoding.geo.census.gov/geocoder";
  var GEOGUIDE_URL = "https://geosearch.planninglabs.nyc/";

  function one(v) { return v == null ? "—" : (Math.round(Number(v) * 10) / 10).toFixed(1); }
  function pill(text, kind) {
    return '<span class="pill' + (kind ? " " + kind : "") + '">' + esc(text) + "</span>";
  }
  function minutesCell(minutes) {
    if (minutes === null || minutes === undefined) return unver("No route value in the source dataset.");
    var cls = minutes <= 45 ? "ok" : (minutes <= 60 ? "" : "warn");
    return '<span class="pill ' + cls + '">' + one(minutes) + " min</span>";
  }

  function renderRanking(data) {
    var host = document.getElementById("ranking-host");
    if (!host) return;
    var rows = data.ranking.map(function (r) {
      return "<tr><td><strong>#" + esc(r.rank) + "</strong></td>" +
        "<td><strong>" + esc(r.name) + "</strong><br><span class='small muted'>" + esc(r.address || "") + "</span></td>" +
        "<td class='num'><strong>" + one(r.median_minutes) + " min</strong></td>" +
        "<td class='num'>" + esc(r.within_60_min_count) + " / " + esc(r.universe_count) + "</td>" +
        "<td class='num'>" + esc(r.within_30_min_count) + " / " + esc(r.universe_count) + "</td>" +
        "<td class='small'>" + link(data._meta.gtfs_source, "MTA Subway GTFS") + "<br>" + link(GUIDE_URL, "MICHELIN directory") + "</td></tr>";
    }).join("");
    host.innerHTML = '<div class="scroll"><table><thead><tr>' +
      "<th>Order</th><th>Hotel</th><th class='num'>Median to starred</th>" +
      "<th class='num'>Within 60 min</th><th class='num'>Within 30 min</th><th>Official source</th>" +
      "</tr></thead><tbody>" + rows + "</tbody></table></div>" +
      '<p class="small muted">Ordered by the measured median door-to-door time. This is a model comparison, not a 2027 service guarantee; price, bed and bathroom fit remain on the <a href="hotels.html">Hotels page</a>.</p>';
  }

  function renderOneHourFinding(data) {
    var host = document.getElementById("onehour-host");
    if (!host) return;
    var counts = data.ranking.map(function (r) { return Number(r.within_60_min_count); });
    var same = counts.length && counts.every(function (c) { return c === counts[0]; });
    var first = data.ranking[0];
    host.innerHTML =
      '<p class="lede">' + (same
        ? "All " + data.ranking.length + " hotels reach the same <strong>" + counts[0] + " of " + first.universe_count + "</strong> active NYC starred restaurants within 60 minutes in this model. The one-hour count does not distinguish the hotels; the median travel time does."
        : "The measured one-hour counts vary by hotel; see the table and route matrix below.") + "</p>" +
      '<ul class="tight">' +
      "<li><strong>Population:</strong> " + esc(data._meta.active_nyc_restaurants) + " active NYC MICHELIN-starred venues in the current directory snapshot used for this model. The two out-of-city venues and closed Shion are excluded; see the data record.</li>" +
      "<li><strong>Mode and snapshot:</strong> subway plus walking, using the MTA static subway feed and a weekday 18:30 departure. No bus route is modeled in this dataset because the published bus feed ended before the full requested travel window.</li>" +
      "<li><strong>Not a guarantee:</strong> actual Feb–Mar 2027 service, the Presidents’ Day schedule, planned works, and live disruptions need a fresh route check.</li>" +
      "</ul><p class='small muted'>Current comparison: <a href='research/generated/transit_1h.json'>transit_1h.json</a> · " +
      link(data._meta.gtfs_source, "official MTA GTFS") + " · " + link(GUIDE_URL, "official MICHELIN directory") +
      " · generated " + esc(data._meta.generated_utc) + " UTC.</p>";
  }

  function renderMatrix(data) {
    var host = document.getElementById("matrix-host");
    if (!host) return;
    var hotels = data.hotels || [];
    if (!hotels.length) { host.innerHTML = '<p class="loading">No current route matrix is available.</p>'; return; }
    var journeyMaps = hotels.map(function (h) {
      var map = {};
      (h.journeys || []).forEach(function (j) { map[j.restaurant] = j; });
      return map;
    });
    var first = hotels[0].journeys || [];
    var rows = first.map(function (j) {
      return "<tr><td><strong>" + esc(j.restaurant) + "</strong></td><td>" +
        (j.stars ? esc(j.stars) + "★" : "—") + "</td>" +
        hotels.map(function (h, i) {
          var route = journeyMaps[i][j.restaurant];
          return "<td class='num'>" + minutesCell(route ? route.minutes : null) + "</td>";
        }).join("") +
        "<td class='small'>" + link(data._meta.gtfs_source, "MTA GTFS") + "<br>" + link(GUIDE_URL, "MICHELIN") + "</td></tr>";
    }).join("");
    var head = "<tr><th>Restaurant</th><th>Stars</th>" + hotels.map(function (h) {
      return "<th class='num' title='" + esc(h.name) + "'>" + esc(h.name.replace(/^The\s+/, "").split(/[\s/]+/)[0]) + "</th>";
    }).join("") + "<th>Source</th></tr>";
    host.innerHTML = '<div class="scroll"><table><thead>' + head + "</thead><tbody>" + rows + "</tbody></table></div>" +
      '<p class="small muted">' + first.length + " active NYC starred-venue routes; horizontal scrolling is available on small screens. The full row-level route details and geocoded door coordinates are in " +
      '<a href="research/generated/transit_1h.json">the committed route dataset</a>.</p>';
  }

  function renderModelNote(data) {
    var host = document.getElementById("model-host");
    if (!host) return;
    var meta = data._meta;
    var exclusions = (meta.excluded_from_nyc_transit || []).map(function (x) {
      return esc(x.name) + ": " + esc(x.reason);
    }).join("<br>");
    host.innerHTML = '<table><tbody>' +
      "<tr><td><strong>Generated</strong></td><td>" + esc(meta.generated_utc) + " UTC</td></tr>" +
      "<tr><td><strong>Method</strong></td><td>" + esc(meta.methodology) + "</td></tr>" +
      "<tr><td><strong>Official transit input</strong></td><td>" + link(meta.gtfs_source, "MTA Subway GTFS feed") + "</td></tr>" +
      "<tr><td><strong>Geocoding</strong></td><td>" + link(GEOGUIDE_URL, "NYC Planning GeoSearch") + " · " + link(GEOCODER_URL, "U.S. Census Geocoder") + "</td></tr>" +
      "<tr><td><strong>Star universe</strong></td><td>" + esc(meta.active_nyc_restaurants) + " active NYC venues from the " + link(GUIDE_URL, "official MICHELIN directory") + " snapshot. Exclusions:<br>" + exclusions + "</td></tr>" +
      "<tr><td><strong>Schedule limitation</strong></td><td>" + esc(meta.schedule_caveat) + "</td></tr>" +
      "</tbody></table>";
  }

  function renderActivityMatrix(transit, activityData) {
    var host = document.getElementById("activity-matrix-host");
    if (!host) return;
    var sample = transit.results.filter(function (r) {
      return r.service === "wednesday" && r.depart_after_local === "12:00";
    });
    if (!sample.length) { host.innerHTML = '<p class="loading">No saved activity-route baseline.</p>'; return; }
    var activities = activityData.activities || [];
    var rows = activities.map(function (a) {
      var routeSource = link(a.source_url, "venue official page");
      return "<tr><td><strong>" + esc(a.name) + "</strong></td>" +
        sample.map(function (hotel) {
          var journey = hotel.destinations[a.name];
          return "<td class='num'>" + minutesCell(journey ? journey.minutes : null) + "</td>";
        }).join("") +
        "<td class='small'>" + routeSource + "<br>" + link(transit._meta.feed_index_url, "MTA GTFS") + "</td></tr>";
    }).join("");
    var head = "<tr><th>Activity</th>" + sample.map(function (hotel) {
      return "<th class='num' title='" + esc(hotel.hotel_name) + "'>" + esc(hotel.hotel_name.replace(/^The\s+/, "").split(/[\s/]+/)[0]) + "</th>";
    }).join("") + "<th>Official source</th></tr>";
    host.innerHTML = '<div class="scroll"><table><thead>' + head + "</thead><tbody>" + rows + "</tbody></table></div>" +
      '<p class="small muted">This is a separate earlier route-model snapshot (weekday Wednesday 12:00, including subway/bus where covered), not the current star-ranking methodology above. Empty cells mean no route value was captured; do not infer zero. See <a href="data/transit_hotels.json">the measurement and feed dates</a>. Actual 2027 trips need a new MTA check.</p>';
  }

  function renderBlockers(blockers) {
    var host = document.getElementById("blockers-host");
    if (!host) return;
    var rows = blockers.blockers.map(function (b) {
      return "<tr><td><strong>" + esc(b.id) + "</strong></td><td><strong>" + esc(b.title) + "</strong></td>" +
        "<td class='small'>" + esc(b.why_it_matters) + "</td><td class='small'>" + esc(b.next_action) + "</td>" +
        "<td class='small'>" + (b.sources || []).map(function (s) { return link(s.url, s.label); }).join("<br>") + "</td></tr>";
    }).join("");
    host.innerHTML = '<div class="scroll"><table><thead><tr><th>ID</th><th>Question</th><th>Why it matters</th><th>What would clear it</th><th>Source</th></tr></thead><tbody>' + rows + "</tbody></table></div>";
  }

  function hostOf(url) {
    try { return new URL(url).hostname.replace(/^www\./, ""); } catch (e) { return ""; }
  }
  function renderSuggestions(state) {
    var host = document.getElementById("suggestions-host");
    if (!host) return;
    var rows = state.suggestions.map(function (s) {
      return "<tr><td><strong>" + esc(s.id) + "</strong></td><td><strong>" + esc(s.title) +
        "</strong><br><span class='small muted'>" + esc(s.decision_it_unblocks) + "</span></td><td class='small'>" +
        esc(s.what_changes) + "</td><td class='small'>" + esc(s.effort) + "</td><td class='small'>" +
        (s.source ? link(s.source, hostOf(s.source) || "source") : unver("No source captured.")) + "</td></tr>";
    }).join("");
    host.innerHTML = '<div class="scroll"><table><thead><tr><th>ID</th><th>Suggestion</th><th>What changes</th><th>Effort</th><th>Source</th></tr></thead><tbody>' + rows + "</tbody></table></div>";
    var picks = document.getElementById("suggestion-picks");
    if (picks) {
      var store = {};
      try { store = JSON.parse(localStorage.getItem("nyf-suggestions") || "{}"); } catch (e) { store = {}; }
      picks.innerHTML = state.suggestions.map(function (s) {
        return '<label class="small" style="display:block;margin:4px 0"><input type="checkbox" data-sug="' +
          esc(s.id) + '"' + (store[s.id] ? " checked" : "") + "> " + esc(s.id) + " — " + esc(s.title) + "</label>";
      }).join("");
      picks.addEventListener("change", function (e) {
        var id = e.target.getAttribute("data-sug");
        if (!id) return;
        store[id] = e.target.checked;
        try { localStorage.setItem("nyf-suggestions", JSON.stringify(store)); } catch (err) { /* local storage is optional */ }
      });
    }
  }

  function renderReviewLinks(data) {
    var host = document.getElementById("review-host");
    if (!host) return;
    var rows = data.venues.map(function (v) {
      var links = v.links.map(function (l) {
        var meta = [l.uploader, l.length, l.views_as_shown && l.views_as_shown !== "unknown" ? l.views_as_shown + " views" : null].filter(Boolean).join(" · ");
        var proof = l.venue_named_in_title === false
          ? pill("venue not in the title", "warn")
          : pill(l.kind === "channel" ? "official channel" : "one venue, filmed", "ok");
        return "<div style='margin:0 0 10px'>" + link(l.url, l.title || l.url) +
          "<br><span class='small muted'>" + esc(l.platform) + (meta ? " · " + esc(meta) : "") + " · " + proof + "</span>" +
          (l.note ? "<br><span class='small muted'>" + esc(l.note) + "</span>" : "") + "</div>";
      }).join("");
      return "<tr><td><strong>" + esc(v.venue) + "</strong></td><td class='small'>" + esc(v.type) + "</td><td class='small'>" + links + "</td></tr>";
    }).join("");
    host.innerHTML = '<p class="small muted">' + esc(data._meta.coverage.venues_with_a_specific_link) +
      " venues have a specific verified content link; " + esc(data._meta.coverage.venues_with_only_search_links) +
      " still have search links only. Search pages are discovery links, not proof.</p>" +
      '<div class="scroll"><table><thead><tr><th>Venue</th><th>Type</th><th>Specific link evidence</th></tr></thead><tbody>' + rows + "</tbody></table></div>" +
      '<p class="small muted">Registry: <a href="data/review_links.json">review_links.json</a>. Related audit: <a href="EVIDENCE_AUDIT.md">EVIDENCE_AUDIT.md</a>.</p>';
  }

  document.addEventListener("DOMContentLoaded", function () {
    fetch("research/generated/transit_1h.json").then(function (r) { return r.json(); }).then(function (d) {
      renderRanking(d);
      renderOneHourFinding(d);
      renderMatrix(d);
      renderModelNote(d);
    }).catch(function (e) {
      ["ranking-host", "onehour-host", "matrix-host", "model-host"].forEach(function (id) {
        var host = document.getElementById(id);
        if (host) host.innerHTML = '<p class="loading">Could not load the current transit model (' + esc(e.message) + ").</p>";
      });
    });
    Promise.all([fetch("data/transit_hotels.json").then(function (r) { return r.json(); }),
      fetch("data/activities.json").then(function (r) { return r.json(); })])
      .then(function (pair) { renderActivityMatrix(pair[0], pair[1]); })
      .catch(function (e) {
        var host = document.getElementById("activity-matrix-host");
        if (host) host.innerHTML = '<p class="loading">Could not load the activity route baseline (' + esc(e.message) + ").</p>";
      });
    fetch("data/blockers.json").then(function (r) { return r.json(); }).then(renderBlockers)
      .catch(function () { /* section stays visibly empty rather than inventing content */ });
    fetch("data/suggestions.json").then(function (r) { return r.json(); }).then(renderSuggestions)
      .catch(function () { /* section stays visibly empty rather than inventing content */ });
    fetch("data/review_links.json").then(function (r) { return r.json(); }).then(renderReviewLinks)
      .catch(function () { /* link register remains available from its official local JSON file */ });
  });
})();
