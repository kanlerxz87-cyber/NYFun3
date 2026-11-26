/* Small helpers shared by every page. No dependencies, no build step. */
(function () {
  "use strict";

  window.NYF = {
    money: function (v) {
      if (v === null || v === undefined || v === "") return "";
      return "$" + Number(v).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
    money0: function (v) {
      if (v === null || v === undefined || v === "") return "";
      return "$" + Number(v).toLocaleString("en-US", { maximumFractionDigits: 0 });
    },
    esc: function (s) {
      return String(s === null || s === undefined ? "" : s)
        .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    },
    unverified: function (note) {
      var t = '<span class="unver">unverified</span>';
      if (!note) return t;
      return t + '<span class="flag">' + window.NYF.esc(note.replace(/^UNVERIFIED\s*[—-]\s*/i, "")) + "</span>";
    },
    hoursCell: function (hours, flag) {
      var order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
      var validDays = hours ? order.filter(function (d) { return hours[d] && String(hours[d]).trim(); }) : [];
      if (!validDays.length) return window.NYF.unverified(flag || "Hours not published on the official page.");
      var parts = validDays.map(function (d) {
        var v = hours[d];
        var closed = /closed/i.test(v);
        return '<span class="hours"><b>' + d + "</b> " +
          (closed ? '<span class="closed">' + window.NYF.esc(v) + "</span>" : window.NYF.esc(v)) + "</span>";
      });
      var html = parts.join("<br>");
      if (flag) html += '<span class="flag">' + window.NYF.esc(flag.replace(/^UNVERIFIED\s*[—-]\s*/i, "")) + "</span>";
      return html;
    },
    reviewCell: function (entity) {
      var out = [];
      var found = (entity && entity.review_links) || [];
      found.forEach(function (l) {
        out.push('<a href="' + window.NYF.esc(l.url) + '" target="_blank" rel="noopener noreferrer" title="' +
          window.NYF.esc(l.title || l.platform) + '">' + window.NYF.esc(l.platform) + "</a>");
      });
      var s = (entity && entity.social) || {};
      var keys = ["youtube_search", "tiktok_search", "instagram_search"];
      var labels = ["YouTube", "TikTok", "Instagram"];
      var searchLinks = keys.map(function (k, i) {
        return s[k] ? '<a href="' + window.NYF.esc(s[k]) + '" target="_blank" rel="noopener noreferrer">' + labels[i] + "</a>" : "";
      }).filter(Boolean).join(" · ");
      if (searchLinks) {
        out.push((found.length ? "<br>" : "") + '<span class="muted">search: ' + searchLinks + "</span>");
      }
      return out.join("") || '<span class="muted">—</span>';
    },
    srcLink: function (url, label) {
      if (!url) return "";
      return '<a href="' + window.NYF.esc(url) + '" target="_blank" rel="noopener noreferrer">' +
        window.NYF.esc(label || "source") + "</a>";
    },
    priceForTwo: function (r) {
      var options = (r && r.price_options) || [];
      if (!options.length) {
        return window.NYF.unverified(
          (r && (r.price_for_two_note || r.price_flag)) ||
          "No first-party dollar price — MICHELIN publishes a band only."
        );
      }
      var html = options.map(function (o) {
        var pp = Number(o.per_person_usd), pair = Number(o.for_two_usd);
        return '<div class="small"><strong>2 × ' + window.NYF.money0(pp) + " = " + window.NYF.money0(pair) + "</strong>" +
          '<br><span class="muted">' + window.NYF.esc(o.label || "Official menu") + "</span>" +
          (o.source_url ? "<br>" + window.NYF.srcLink(o.source_url, "official menu / FAQ / PDF") : "") +
          "</div>";
      }).join("<hr style='border:none;border-top:1px solid #eef1f5;margin:6px 0'>");
      if (r.price_caveat) html += '<span class="flag">' + window.NYF.esc(r.price_caveat) + "</span>";
      return html;
    },
    sourceCell: function (r) {
      if (!r) return window.NYF.unverified("No official source link captured.");
      var links = [];
      if (r.michelin_url) links.push(window.NYF.srcLink(r.michelin_url, "Guide page"));
      (r.price_sources || []).forEach(function (s, i) {
        if (s && s.url) links.push(window.NYF.srcLink(s.url, s.label || ("official menu " + (i + 1))));
      });
      if (!links.length && r.price_source_url) links.push(window.NYF.srcLink(r.price_source_url, "official menu / FAQ / PDF"));
      return links.length ? links.join("<br>") : window.NYF.unverified("No official source link captured.");
    },
    load: function (path, render) {
      var host = document.getElementById("table-host");
      if (!host) return;
      fetch(path)
        .then(function (r) { if (!r.ok) throw new Error(r.status + " " + r.statusText); return r.json(); })
        .then(function (json) { host.innerHTML = ""; render(json); })
        .catch(function (e) {
          host.innerHTML = '<p class="loading">Could not load <code>' + window.NYF.esc(path) +
            "</code> (" + window.NYF.esc(e.message) + "). If you opened this file directly from disk, " +
            "run a local server or use the published GitHub Pages URL — browsers block local JSON reads.</p>";
        });
    }
  };
})();
