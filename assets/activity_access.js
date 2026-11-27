/* Selected-hotel transit estimates for the Activities page.
 * Values are read from data/transit_hotels.json; this renderer never derives a
 * route, geocode, or missing value in the browser.
 */
(function () {
  "use strict";

  var hotelSelect = document.getElementById("activity-access-hotel");
  var serviceSelect = document.getElementById("activity-access-service");
  var departureSelect = document.getElementById("activity-access-departure");
  var summary = document.getElementById("activity-access-summary");
  var host = document.getElementById("activity-access-host");
  if (!hotelSelect || !serviceSelect || !departureSelect || !summary || !host) return;

  var activityData;
  var hotelData;
  var transitData;
  var activities;
  var hotels;
  var routes;
  var meta;

  function esc(value) {
    return window.NYF.esc(value);
  }

  function sourceLink(url, label) {
    return url ? window.NYF.srcLink(url, label) : "";
  }

  function dateLabel(compact) {
    var text = String(compact || "");
    if (!/^\d{8}$/.test(text)) return "date not recorded";
    return text.slice(0, 4) + "-" + text.slice(4, 6) + "-" + text.slice(6, 8);
  }

  function serviceKey(row) {
    return row.service + "|" + row.service_date;
  }

  function serviceLabel(row) {
    var day = String(row.service || "service");
    day = day.charAt(0).toUpperCase() + day.slice(1);
    return day + " service · " + dateLabel(row.service_date) + " sample";
  }

  function renderAssumptions() {
    var target = document.getElementById("activity-access-assumptions");
    var a = meta.assumptions || {};
    if (!target) return;
    var parts = [];
    if (a.walk_speed_kmh !== undefined) parts.push("walking speed " + a.walk_speed_kmh + " km/h");
    if (a.max_walk_door_to_stop_m !== undefined) parts.push("up to " + a.max_walk_door_to_stop_m + " m from a door to a stop");
    if (a.max_walk_between_stops_m !== undefined) parts.push("up to " + a.max_walk_between_stops_m + " m for walking transfers");
    if (a.station_transfer_allowance_min !== undefined) parts.push(a.station_transfer_allowance_min + " min station-transfer allowance");
    if (a.search_window_min !== undefined) parts.push(a.search_window_min + " min model search window");
    target.textContent = "Model assumptions: " + parts.join("; ") +
      ". Hotel choices are alphabetical; the initial selection is a display example, not a recommendation.";
  }

  function routeAddress(activity, unmeasuredByName) {
    var override = (meta.address_overrides || {})[activity.name];
    if (override && override.address) return override.address;
    var unmeasured = unmeasuredByName[activity.name];
    if (unmeasured && unmeasured.address) return unmeasured.address;
    var text = String(activity.address || "");
    var match = text.match(/(\d+[^,]*),?\s*(New York|Brooklyn|Queens|Bronx),?\s*NY/i);
    return match ? match[0] : text;
  }

  function addOption(select, value, label) {
    var option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    select.appendChild(option);
  }

  function findRoute() {
    var selectedService = serviceSelect.value.split("|");
    return routes.find(function (row) {
      return row.hotel_id === hotelSelect.value &&
        row.service === selectedService[0] &&
        row.service_date === selectedService[1] &&
        row.depart_after_local === departureSelect.value;
    });
  }

  function resultCell(activity, route, unmeasuredByName) {
    var destination = route && route.destinations && route.destinations[activity.name];
    if (destination && typeof destination.minutes === "number" && Number.isFinite(destination.minutes)) {
      var mins = destination.minutes.toFixed(1);
      var within = destination.within_1h === true;
      return {
        minutes: destination.minutes,
        within: within,
        html: '<strong class="activity-access-time">~' + esc(mins) + ' min</strong>',
        status: '<span class="pill ' + (within ? "ok" : "warn") + '">' +
          (within ? "Within 60 min · model" : "Over 60 min · model") + "</span>"
      };
    }

    if (destination && destination.minutes === null) {
      return {
        minutes: null,
        html: '<span class="unver">No route found in model</span>' +
          '<span class="flag">No itinerary was found within the model search window; this is not evidence that no real-world route exists.</span>',
        status: '<span class="pill warn">Not confirmed</span>'
      };
    }

    var note = unmeasuredByName[activity.name];
    if (/^Digital ticket\b/i.test(String(activity.address || ""))) {
      return {
        minutes: null,
        html: '<span class="unver">No single destination</span>' +
          '<span class="flag">This is an attraction pass, not one physical address; route time depends on the selected attraction.</span>',
        status: '<span class="pill warn">Not a place</span>'
      };
    }
    return {
      minutes: null,
      html: '<span class="unver">Unmeasured</span>' +
        '<span class="flag">' + esc((note && note.reason) || "No official route point is available; no location was inferred.") + "</span>",
      status: '<span class="pill warn">Unverified point</span>'
    };
  }

  function rowSources(activity, address, unmeasuredByName, route) {
    var links = [];
    var override = (meta.address_overrides || {})[activity.name];
    var unmeasured = unmeasuredByName[activity.name];
    var geo = (meta.geocode_register || {})[address];
    var mta = meta.feed_index_url || "https://www.mta.info/developers";

    links.push(sourceLink(activity.source_url, "official activity page"));
    if (override && override.source_url && override.source_url !== activity.source_url) {
      links.push(sourceLink(override.source_url, "official address"));
    }
    if (geo && geo.source) links.push(sourceLink(geo.source, "Census geocoder query"));
    if (!geo && unmeasured && unmeasured.address) {
      var failedGeo = (meta.geocode_register || {})[unmeasured.address];
      if (failedGeo && failedGeo.source) links.push(sourceLink(failedGeo.source, "Census geocoder query"));
    }
    if (route && route.destinations && route.destinations[activity.name]) {
      links.push(sourceLink(mta, "MTA GTFS source"));
    }
    return links.filter(Boolean).join("<br>");
  }

  function render() {
    var route = findRoute();
    if (!route) {
      summary.innerHTML = '<span class="unver">Route sample unavailable</span> No matching hotel/service/time row exists in the published measurement.';
      host.innerHTML = '<p class="loading">The selected combination is not covered by the saved route data. No estimate is inferred.</p>';
      return;
    }

    var unmeasuredByName = {};
    (meta.unmeasured_destinations || []).forEach(function (row) {
      if (row.kind === "activity" && row.name) unmeasuredByName[row.name] = row;
    });

    var selectedHotel = hotels.find(function (hotel) { return hotel.id === route.hotel_id; }) || {};
    var override = (meta.address_overrides || {})[route.hotel_name];
    var originAddress = route.address_used || selectedHotel.address || "";
    var originGeo = (meta.geocode_register || {})[originAddress];
    var resultRows = activities.map(function (activity) {
      var address = routeAddress(activity, unmeasuredByName);
      var result = resultCell(activity, route, unmeasuredByName);
      var activityOverride = (meta.address_overrides || {})[activity.name];
      var detail = activityOverride && activity.address !== address
        ? '<br><span class="small muted">Official route address used: ' + esc(address) + "</span>"
        : "";
      return {
        result: result,
        html: "<tr>" +
          '<td><strong>' + esc(activity.name) + "</strong>" +
            '<br><span class="small muted">' + esc(activity.address || "") + "</span>" + detail + "</td>" +
          '<td class="num">' + result.html + "</td>" +
          "<td>" + result.status + "</td>" +
          '<td class="small activity-access-sources">' + rowSources(activity, address, unmeasuredByName, route) + "</td>" +
        "</tr>"
      };
    });

    var hasMinuteValue = function (row) { return typeof row.result.minutes === "number"; };
    var measured = resultRows.filter(hasMinuteValue).length;
    var within = resultRows.filter(function (row) { return row.result.within === true; }).length;
    var missing = activities.length - measured;
    var selectedService = serviceSelect.selectedOptions[0] ? serviceSelect.selectedOptions[0].textContent : serviceLabel(route);
    var selectedHotelSource = override && override.source_url ? override.source_url : selectedHotel.official_site;
    var origin = '<strong>Origin:</strong> ' + esc(route.hotel_name) +
      (originAddress ? " · " + esc(originAddress) : "") +
      (selectedHotelSource ? " · " + sourceLink(selectedHotelSource, "official hotel page") : "") +
      (originGeo && originGeo.source ? " · " + sourceLink(originGeo.source, "Census geocoder query") : "");
    var overrideNote = override && override.reason
      ? '<span class="flag">Routing uses the documented official address override: ' + esc(override.reason) + "</span>"
      : "";

    summary.innerHTML =
      '<strong>' + within + " of " + measured + " measured activities</strong> are estimated within " +
      esc(meta.assumptions.report_limit_min || 60) + " minutes for this sample; " + missing +
      " of " + activities.length + " listed activities have no numeric route estimate (reasons are shown per row)." +
      '<br><span class="small">' + origin + "<br><strong>Sample:</strong> " + esc(selectedService) +
      " · depart " + esc(route.depart_after_local) + " local time</span>" + overrideNote;

    host.innerHTML =
      '<div class="scroll activity-access-scroll"><table class="activity-access-table"><thead><tr>' +
      "<th>Activity / listed location</th><th class='num'>Estimated transit + walk</th>" +
      "<th>60-minute test</th><th>Source</th></tr></thead><tbody>" +
      resultRows.map(function (row) { return row.html; }).join("") +
      "</tbody></table></div>";
  }

  function load() {
    Promise.all([
      fetch("data/activities.json").then(function (response) {
        if (!response.ok) throw new Error("activities.json: " + response.status);
        return response.json();
      }),
      fetch("data/hotels.json").then(function (response) {
        if (!response.ok) throw new Error("hotels.json: " + response.status);
        return response.json();
      }),
      fetch("data/transit_hotels.json").then(function (response) {
        if (!response.ok) throw new Error("transit_hotels.json: " + response.status);
        return response.json();
      })
    ]).then(function (payload) {
      activityData = payload[0];
      hotelData = payload[1];
      transitData = payload[2];
      activities = activityData.activities || [];
      hotels = (hotelData.hotels || []).slice().sort(function (a, b) {
        return String(a.name).localeCompare(String(b.name));
      });
      routes = transitData.results || [];
      meta = transitData._meta || {};
      renderAssumptions();

      var uniqueServices = {};
      var departures = {};
      routes.forEach(function (row) {
        uniqueServices[serviceKey(row)] = row;
        departures[row.depart_after_local] = true;
      });
      Object.keys(uniqueServices).sort(function (a, b) {
        return uniqueServices[a].service_date.localeCompare(uniqueServices[b].service_date);
      }).forEach(function (key) {
        var row = uniqueServices[key];
        addOption(serviceSelect, key, serviceLabel(row));
      });
      Object.keys(departures).sort().forEach(function (time) { addOption(departureSelect, time, time); });
      hotels.forEach(function (hotel) { addOption(hotelSelect, hotel.id, hotel.name); });

      if (!hotels.length || !routes.length || !activities.length) {
        throw new Error("the source data does not contain hotels, activities, and route samples");
      }
      hotelSelect.value = hotels[0].id;
      serviceSelect.value = serviceSelect.options[0].value;
      departureSelect.value = departureSelect.options[0].value;
      [hotelSelect, serviceSelect, departureSelect].forEach(function (select) {
        select.addEventListener("change", render);
      });
      render();
    }).catch(function (error) {
      summary.innerHTML = '<span class="unver">Access estimate unavailable</span> The saved official-source data could not be loaded.';
      host.innerHTML = '<p class="loading">Could not load route data: ' + esc(error.message) +
        '. Values remain blank rather than inferred.</p>';
    });
  }

  load();
})();
