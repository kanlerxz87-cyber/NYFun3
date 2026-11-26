/* Decide page: renders the measured ranking and the journey-time matrix.
   Pure DOM + fetch, no dependencies. Every rendered number carries its
   provenance; nothing is computed here that is not already in the JSON. */
(function () {
  "use strict";

  var NYF = window.NYF || {};
  var esc = NYF.esc || function (s) { return String(s == null ? "" : s); };
  var money0 = NYF.money0 || function (v) { return v == null ? "" : "$" + v; };
  var link = NYF.srcLink || function (url, label) {
    return url ? '<a href="' + esc(url) + '" target="_blank" rel="noopener noreferrer">' + esc(label) + "</a>" : "";
  };
  var unver = NYF.unverified || function (t) { return '<span class="unver">unverified</span>'; };

  function pill(text, kind) {
    return '<span class="pill' + (kind ? " " + kind : "") + '">' + esc(text) + "</span>";
  }

  // "The Mayfair Hotel" must not become the column header "The".
  // 19 must not read as 19.0 in one row and 18.5 in the next.
  function one(v) {
    return v == null ? "" : (Math.round(v * 10) / 10).toFixed(1);
  }

  function shortName(name) {
    return String(name || "").replace(/^The\s+/, "").split(/[\s/]+/)[0];
  }

  function minutesCell(v) {
    if (!v || v.minutes === null || v.minutes === undefined) return unver("not measured");
    var cls = v.minutes <= 45 ? "ok" : (v.minutes <= 60 ? "" : "warn");
    return '<span class="pill ' + cls + '">' + Math.round(v.minutes) + " min</span>";
  }

  function hostOf(url) {
    try { return new URL(url).hostname.replace(/^www\./, ""); } catch (e) { return ""; }
  }

  // ---------------------------------------------------------------- ranking
  function renderRanking(data) {
    var host = document.getElementById("ranking-host");
    if (!host) return;
    var meta = data._meta;
    // A gap under 0.8 min is inside the model's own resolution, so consecutive
    // hotels that close are shown as tied and named by rank.
    var TIE_MIN = 0.8;
    var groups = [];
    data.ranking.forEach(function (r, i) {
      var prev = data.ranking[i - 1];
      var sameAsPrev = prev && Math.abs(prev.restaurants.median_minutes - r.restaurants.median_minutes) < TIE_MIN;
      if (sameAsPrev) groups[groups.length - 1].push(r.rank_by_median);
      else groups.push([r.rank_by_median]);
    });
    var groupOf = {};
    groups.forEach(function (g) { g.forEach(function (rank) { groupOf[rank] = g; }); });
    var rows = data.ranking.map(function (r) {
      var stars = r.starred_restaurants_within_60_min;
      var spread = r.median_spread_between_windows_min;
      var group = groupOf[r.rank_by_median] || [r.rank_by_median];
      var tie = group.length > 1
        ? ' <span class="pill ok">tied #' + group[0] + "–#" + group[group.length - 1] + "</span>"
        : "";
      var unstable = spread !== null && spread >= 1.5
        ? ' <span class="pill warn">moves ' + one(spread) + " min by time of day</span>"
        : "";
      return "<tr>" +
        "<td><strong>#" + r.rank_by_median + "</strong></td>" +
        "<td><strong>" + esc(r.name) + "</strong><br><span class='small muted'>" + esc(r.area || "") + "</span></td>" +
        "<td class='num'><strong>" + one(r.restaurants.median_minutes) + " min</strong>" + tie + unstable +
          "<br><span class='small muted'>spread " + (spread === null ? "—" : one(spread) + " min") +
          " over four departures</span></td>" +
        "<td class='num'>" + stars.three_star + " / " + stars.two_star + " / " + stars.one_star +
          "<br><span class='small muted'>" + r.starred_restaurants_within_60_min_total + " total</span></td>" +
        "<td class='num'>" + (r.activities.measured
          ? r.activities.within_60_min + " of " + r.activities.measured
          : unver("n/a")) + "</td>" +
        "<td class='num'>" + (r.hotel_quote_total_before_tax_usd
          ? money0(r.hotel_quote_total_before_tax_usd)
          : unver("no tier captured")) +
          "<br><span class='small muted'>before tax, 7 nights</span></td>" +
        "<td class='small'>" + link("hotels.html", "hotels page") + "</td>" +
        "</tr>";
    }).join("");
    host.innerHTML =
      '<div class="scroll"><table><thead><tr>' +
      "<th>Rank</th><th>Hotel</th><th class='num'>Median to starred</th>" +
      "<th class='num'>★★★ / ★★ / ★ within 60 min</th>" +
      "<th class='num'>Activities within 60 min</th>" +
      "<th class='num'>7-night total</th><th>Source</th></tr></thead><tbody>" + rows + "</tbody></table></div>" +
      '<p class="small muted" style="margin:10px 0 0">Ranked by <strong>' + esc(meta.ranking_metric) +
      "</strong>, measured on " + esc(meta.sample_used_for_the_rank) + ". " + esc(meta.ranking_metric_explained) +
      "</p>";
  }

  // ------------------------------------------------------- the 1-hour result
  function renderOneHourFinding(data) {
    var host = document.getElementById("onehour-host");
    if (!host) return;
    var counts = data.ranking.map(function (r) { return r.starred_restaurants_within_60_min_total; });
    var same = counts.every(function (c) { return c === counts[0]; });
    host.innerHTML =
      '<p class="lede">' + (same
        ? "Every hotel reaches <strong>the same " + counts[0] + "</strong> measured starred restaurants inside 60 minutes, so the raw count you asked for cannot separate them. That is a measured result, not a gap."
        : "The counts differ between hotels; see the table.") + "</p>" +
      '<ul class="tight">' +
      "<li><strong>What is measured:</strong> door-to-door time from each hotel to each starred restaurant with a resolvable address, using the official MTA subway + Manhattan/Brooklyn bus timetable.</li>" +
      "<li><strong>What is not measured:</strong> " + data._meta.coverage.starred_restaurants_unmeasured +
        " of " + data._meta.coverage.starred_restaurants_in_dataset + " starred restaurants, because the record has no street address or the Census geocoder could not resolve it. They are listed with reasons.</li>" +
      "<li><strong>So the tie is broken by:</strong> the median door-to-door time to those restaurants, which does vary — from " +
        data.ranking[0].restaurants.median_minutes + " to " +
        data.ranking[data.ranking.length - 1].restaurants.median_minutes + " minutes.</li>" +
      "<li><strong>Resolution limit:</strong> ranks 1–5 span 0.8 minutes in total (18.5 to 19.3), which is smaller than the model can honestly distinguish. They are shown as one tied group: choose among them on price, room and area instead.</li>" +
      "</ul>" +
      '<p class="small muted">Measurement: <a href="data/transit_hotels.json">data/transit_hotels.json</a> · ' +
      "ranking: <a href=\"data/hotel_ranking.json\">data/hotel_ranking.json</a> · " +
      "method and its limits: <a href=\"decide.html#blockers\">section 6</a>, " +
      '<a href="EVIDENCE_AUDIT.md">EVIDENCE_AUDIT.md</a>.</p>';
  }

  // ------------------------------------------------------------ the matrix
  function renderMatrix(transit) {
    var host = document.getElementById("matrix-host");
    if (!host) return;
    var sample = transit.results.filter(function (r) {
      return r.service === "wednesday" && r.depart_after_local === "12:00";
    });
    if (!sample.length) { host.innerHTML = '<p class="loading">No weekday sample in the measurement.</p>'; return; }
    var names = Object.keys(sample[0].destinations).sort();
    var head = "<tr><th>Destination</th>" +
      sample.map(function (r) {
        return "<th class='num' title='" + esc(r.hotel_name) + "'>" + esc(shortName(r.hotel_name)) + "</th>";
      }).join("") +
      "<th>Source</th></tr>";
    var body = names.map(function (n) {
      return "<tr><td>" + esc(n) + "</td>" +
        sample.map(function (r) { return "<td class='num'>" + minutesCell(r.destinations[n]) + "</td>"; }).join("") +
        "<td class='small'>" + link(transit._meta.feed_index_url, "MTA GTFS") + "</td></tr>";
    }).join("");
    host.innerHTML = '<div class="scroll"><table><thead>' + head + "</thead><tbody>" + body + "</tbody></table></div>";
    var toggle = document.getElementById("matrix-toggle");
    if (toggle) {
      toggle.addEventListener("click", function () {
        var panel = document.getElementById("matrix-panel");
        panel.hidden = !panel.hidden;
        toggle.textContent = panel.hidden ? "Show the full door-to-door matrix" : "Hide the matrix";
      });
    }
  }

  function renderModelNote(transit) {
    var host = document.getElementById("model-host");
    if (!host) return;
    var a = transit._meta.assumptions;
    host.innerHTML =
      '<table><tbody>' +
      "<tr><td><strong>What produced these numbers</strong></td><td>" + esc(transit._meta.what_this_is) + "</td></tr>" +
      "<tr><td><strong>Algorithm</strong></td><td>" + esc(a.algorithm) + "</td></tr>" +
      "<tr><td><strong>Walking</strong></td><td>" + esc(a.walk_speed_kmh) + " km/h; up to " +
        esc(a.max_walk_door_to_stop_m) + " m between a door and a stop; " +
        esc(a.station_transfer_allowance_min) + " min to change inside a station</td></tr>" +
      "<tr><td><strong>Timetable dates</strong></td><td>Wednesday " +
        esc(transit._meta.service_dates.wednesday) + " and Saturday " +
        esc(transit._meta.service_dates.saturday) + ", departing at " +
        esc(a.departure_windows_local_time.join(" and ")) + " local</td></tr>" +
      "<tr><td><strong>Feed range published by the feed</strong></td><td>" +
        esc(transit._meta.service_dates.feed_first_date) + " to " +
        esc(transit._meta.service_dates.feed_last_date) + "</td></tr>" +
      "<tr><td><strong>Feeds</strong></td><td>" +
        Object.keys(transit._meta.feeds).map(function (k) {
          return link(transit._meta.feeds[k].url, k) + " (" +
            transit._meta.feeds[k].connections.toLocaleString("en-US") + " connections)";
        }).join("<br>") + "</td></tr>" +
      "<tr><td><strong>Geocoder</strong></td><td>" + link(transit._meta.geocoder.url, transit._meta.geocoder.name) +
        " (" + esc(transit._meta.geocoder.benchmark) + ")</td></tr>" +
      "<tr><td><strong>What this is not</strong></td><td>" +
        transit._meta.what_this_is_not.map(function (t) { return "• " + esc(t); }).join("<br>") + "</td></tr>" +
      "</tbody></table>";
  }

  // --------------------------------------------------------------- blockers
  function renderBlockers(blockers) {
    var host = document.getElementById("blockers-host");
    if (!host) return;
    var rows = blockers.blockers.map(function (b) {
      var p = b.status === "open" ? pill(b.status, "warn") : pill(b.status, "ok");
      return "<tr><td><strong>" + esc(b.id) + "</strong></td><td>" + esc(b.title) + p + "</td>" +
        "<td class='small'>" + esc(b.why_it_matters) + "</td>" +
        "<td class='small'>" + esc(b.next_action) + "</td>" +
        "<td class='small'>" + (b.sources || []).map(function (s) { return link(s.url, s.label); }).join("<br>") + "</td></tr>";
    }).join("");
    host.innerHTML = '<div class="scroll"><table><thead><tr><th>ID</th><th>Blocker</th>' +
      "<th>Why it matters</th><th>What would clear it</th><th>Source</th></tr></thead><tbody>" +
      rows + "</tbody></table></div>";
  }

  // ---------------------------------------------------------- suggestions
  function renderSuggestions(state) {
    var host = document.getElementById("suggestions-host");
    if (!host) return;
    var rows = state.suggestions.map(function (s) {
      return "<tr><td><strong>" + esc(s.id) + "</strong></td>" +
        "<td><strong>" + esc(s.title) + "</strong><br><span class='small muted'>" + esc(s.decision_it_unblocks) + "</span></td>" +
        "<td class='small'>" + esc(s.what_changes) + "</td>" +
        "<td class='small'>" + esc(s.effort) + "</td>" +
        "<td class='small'>" + (s.source ? link(s.source, hostOf(s.source) || "source") : unver("no source")) + "</td></tr>";
    }).join("");
    host.innerHTML = '<div class="scroll"><table><thead><tr><th>ID</th><th>Suggestion</th>' +
      "<th>What changes on the site</th><th>Effort</th><th>Source</th></tr></thead><tbody>" + rows + "</tbody></table></div>";
    var picks = document.getElementById("suggestion-picks");
    if (picks) {
      var store = {};
      try { store = JSON.parse(localStorage.getItem("nyf-suggestions") || "{}"); } catch (e) { store = {}; }
      picks.innerHTML = state.suggestions.map(function (s) {
        var checked = store[s.id] ? " checked" : "";
        return '<label class="small" style="display:block;margin:4px 0"><input type="checkbox" data-sug="' +
          esc(s.id) + '"' + checked + "> " + esc(s.id) + " — " + esc(s.title) + "</label>";
      }).join("");
      picks.addEventListener("change", function (e) {
        var id = e.target.getAttribute("data-sug");
        if (!id) return;
        store[id] = e.target.checked;
        try { localStorage.setItem("nyf-suggestions", JSON.stringify(store)); } catch (err) { /* ignore */ }
      });
    }
  }

  // --------------------------------------------------------- review links
  function renderReviewLinks(data) {
    var host = document.getElementById("review-host");
    if (!host) return;
    var rows = data.venues.map(function (v) {
      var links = v.links.map(function (l) {
        var meta = [l.uploader, l.length, l.views_as_shown && l.views_as_shown !== "unknown" ? l.views_as_shown + " views" : null]
          .filter(Boolean).join(" · ");
        var label = esc(l.title || l.url);
        var tag = l.kind === "channel" ? "official channel" : "one venue, filmed";
        // A specific post is only worth calling verified if the page names the venue.
        var proof = l.venue_named_in_title === false
          ? '<span class="pill warn">venue not in the title</span>'
          : '<span class="pill ok">' + esc(tag) + "</span>";
        return "<div style='margin:0 0 10px'>" + link(l.url, label) +
          "<br><span class='small muted'>" + esc(l.platform) + (meta ? " · " + esc(meta) : "") + " · " + proof + "</span>" +
          (l.note ? "<br><span class='small muted'>" + esc(l.note) + "</span>" : "") +
          "</div>";
      }).join("");
      return "<tr><td><strong>" + esc(v.venue) + "</strong>" +
        (v.stars ? "<br><span class='small muted'>" + esc(v.stars) + (v.stars === 1 ? " MICHELIN star" : " MICHELIN stars") + "</span>" : "") +
        "</td><td class='small'>" + esc(v.type) + "</td><td class='small'>" + links + "</td></tr>";
    }).join("");
    var cov = data._meta.coverage;
    host.innerHTML = '<p class="small muted">' +
      esc(cov.venues_with_a_specific_link) + " venues have at least one specific link; " +
      esc(cov.venues_with_only_search_links) + " still have search links only. A search page can show any venue and changes over time, so it is not counted here.</p>" +
      '<div class="scroll"><table><thead><tr><th>Venue</th><th>Type</th><th>Verified link — title, uploader, length, views as published</th></tr></thead><tbody>' +
      rows + "</tbody></table></div>" +
      '<p class="small muted">Record: <a href="data/review_links.json">data/review_links.json</a>. Defects list: <a href="FLAGS.md">FLAGS.md</a>.</p>';
  }

  document.addEventListener("DOMContentLoaded", function () {
    fetch("data/hotel_ranking.json").then(function (r) { return r.json(); }).then(function (d) {
      renderRanking(d);
      renderOneHourFinding(d);
    }).catch(function (e) {
      var host = document.getElementById("ranking-host");
      if (host) host.innerHTML = '<p class="loading">Could not load the ranking (' + esc(e.message) + ").</p>";
    });

    fetch("data/transit_hotels.json").then(function (r) { return r.json(); }).then(function (d) {
      renderMatrix(d);
      renderModelNote(d);
    }).catch(function () { /* the matrix is optional if the fetch fails */ });

    fetch("data/blockers.json").then(function (r) { return r.json(); }).then(renderBlockers)
      .catch(function () { /* section simply stays empty */ });

    fetch("data/suggestions.json").then(function (r) { return r.json(); }).then(renderSuggestions)
      .catch(function () { /* section simply stays empty */ });

    fetch("data/review_links.json").then(function (r) { return r.json(); }).then(renderReviewLinks)
      .catch(function (e) {
        var host = document.getElementById("review-host");
        if (host) host.innerHTML = '<p class="loading">Could not load the review-link register (' + esc(e.message) + ").</p>";
      });
  });
})();
