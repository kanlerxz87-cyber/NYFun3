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
      if (!hours || !Object.keys(hours).length) return window.NYF.unverified(flag || "Hours not published on the official page.");
      var order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
      var parts = order.filter(function (d) { return hours[d]; }).map(function (d) {
        var v = hours[d];
        var closed = /closed/i.test(v);
        return '<span class="hours"><b>' + d + "</b> " +
          (closed ? '<span class="closed">' + window.NYF.esc(v) + "</span>" : window.NYF.esc(v)) + "</span>";
      });
      var html = parts.join("<br>");
      if (flag) html += '<span class="flag">' + window.NYF.esc(flag.replace(/^UNVERIFIED\s*[—-]\s*/i, "")) + "</span>";
      return html;
    },
    srcLink: function (url, label) {
      if (!url) return "";
      return '<a href="' + window.NYF.esc(url) + '" target="_blank" rel="noopener noreferrer">' +
        window.NYF.esc(label || "source") + "</a>";
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
