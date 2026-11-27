#!/usr/bin/env node
/* Execute the root pages' inline renderers with a tiny DOM stub and verify the
 * generated table rows. This catches source columns/links that a static HTML
 * scan cannot see because they are produced from data/*.json at runtime. */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const PAGES = [
  'activities.html',
  'restaurants.html',
  'michelin.html',
  'hotels.html',
  'itinerary.html',
  'decide.html',
];
// Pages whose renderer lives in a separate file (loaded with <script src>).
const EXTRA_SCRIPTS = {
  'activities.html': ['assets/activity_access.js'],
  'decide.html': ['assets/cockpit.js'],
};
// Rendered hosts to verify, other than the page's own table-host.
const EXTRA_HOSTS = {
  'activities.html': ['activity-access-host'],
  'decide.html': ['ranking-host', 'matrix-host', 'activity-matrix-host', 'review-host'],
};
const APP = fs.readFileSync(path.join(ROOT, 'assets/app.js'), 'utf8');
const INLINE = /<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;
const errors = [];
let rowCount = 0;
let pricedRowCount = 0;

function makeElement(id) {
  return {
    id,
    innerHTML: '',
    value: '',
    textContent: '',
    options: [],
    selectedOptions: [],
    children: [],
    listeners: {},
    appendChild(child) {
      this.children.push(child);
      if (child && typeof child.value !== 'undefined') this.options.push(child);
    },
    addEventListener(type, fn) {
      (this.listeners[type] = this.listeners[type] || []).push(fn);
    },
    fire(type) {
      (this.listeners[type] || []).forEach((fn) => fn({ type }));
    },
    setAttribute() {},
  };
}

async function renderPage(page) {
  const html = fs.readFileSync(path.join(ROOT, page), 'utf8');
  const scripts = [];
  for (const extra of EXTRA_SCRIPTS[page] || []) {
    scripts.push(fs.readFileSync(path.join(ROOT, extra), 'utf8'));
  }
  let m;
  INLINE.lastIndex = 0;
  while ((m = INLINE.exec(html)) !== null) {
    if (m[1].trim()) scripts.push(m[1]);
  }
  if (!scripts.length) {
    errors.push(`${page}: no inline renderer found`);
    return;
  }

  const elements = new Map();
  function get(id) {
    if (!elements.has(id)) elements.set(id, makeElement(id));
    return elements.get(id);
  }
  const listeners = {};
  const document = {
    getElementById: get,
    createElement: (tag) => makeElement(tag),
    addEventListener(type, fn) { (listeners[type] = listeners[type] || []).push(fn); },
    __fire(type) { (listeners[type] || []).forEach((fn) => fn({ type })); },
  };
  const fetch = (url) => {
    const rel = url.replace(/^\/+/, '');
    const file = path.join(ROOT, rel);
    let data;
    try {
      data = JSON.parse(fs.readFileSync(file, 'utf8'));
    } catch (e) {
      return Promise.reject(new Error(`cannot read ${url}: ${e.message}`));
    }
    return Promise.resolve({
      ok: true,
      status: 200,
      statusText: 'OK',
      json: () => Promise.resolve(data),
    });
  };
  const sandbox = {
    console,
    document,
    fetch,
    setTimeout,
    clearTimeout,
  };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(APP, sandbox, { filename: 'assets/app.js' });
  sandbox.NYF = sandbox.window.NYF;
  if (!sandbox.NYF) {
    errors.push(`${page}: assets/app.js did not define window.NYF`);
    return;
  }
  for (let i = 0; i < scripts.length; i++) {
    try {
      vm.runInContext(scripts[i], sandbox, { filename: `${page} inline #${i + 1}` });
    } catch (e) {
      errors.push(`${page}: inline renderer #${i + 1} threw: ${e.message}`);
      return;
    }
  }
  if (typeof sandbox.document.__fire === 'function') sandbox.document.__fire('DOMContentLoaded');
  // Let all fetch().then() microtasks settle.
  await new Promise((resolve) => setTimeout(resolve, 0));
  await new Promise((resolve) => setImmediate(resolve));

  const host = get('table-host');
  const out = host.innerHTML;
  const hasMainHost = !!out && !/Could not load/i.test(out);
  if (!hasMainHost && !EXTRA_HOSTS[page]) {
    errors.push(`${page}: table-host was not rendered (${out.slice(0, 140)})`);
    return;
  }
  if (hasMainHost && !/<table/i.test(out)) {
    errors.push(`${page}: rendered host has no table`);
    return;
  }
  if (EXTRA_HOSTS[page]) {
    for (const id of EXTRA_HOSTS[page]) {
      const extra = get(id).innerHTML;
      if (!/<table/i.test(extra)) {
        errors.push(`${page}: #${id} did not render a table (${extra.slice(0, 140)})`);
        continue;
      }
      const extraHeader = extra.match(/<thead[\s\S]*?<\/thead>/i);
      const extraRows = [...extra.replace(/<thead[\s\S]*?<\/thead>/i, '').matchAll(/<tr[\s\S]*?<\/tr>/gi)]
        .filter((r) => /<td[\s>]/i.test(r[0]));
      if (!extraRows.length) errors.push(`${page}: #${id} rendered no body rows`);
      if (page === 'activities.html' && id === 'activity-access-host') {
        if (!extraHeader || !/<th[^>]*>\s*Source\s*<\/th>/i.test(extraHeader[0])) {
          errors.push(`${page}: activity access table has no singular Source column`);
        }
        const activities = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/activities.json'), 'utf8')).activities;
        const hotelData = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/hotels.json'), 'utf8')).hotels;
        const transit = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/transit_hotels.json'), 'utf8'));
        const firstHotel = hotelData.slice().sort((a, b) => a.name.localeCompare(b.name))[0];
        const sampleRoute = transit.results
          .filter((r) => r.hotel_id === firstHotel.id)
          .sort((a, b) => a.service_date.localeCompare(b.service_date) || a.depart_after_local.localeCompare(b.depart_after_local))[0];
        if (extraRows.length !== activities.length) {
          errors.push(`${page}: activity access table has ${extraRows.length} rows; data has ${activities.length}`);
        }
        const sampleMinutes = [];
        extraRows.forEach((row, i) => {
          const url = String(activities[i].source_url || '').replace(/&/g, '&amp;').replace(/"/g, '&quot;');
          if (!url || !row[0].includes(`href="${url}"`)) {
            errors.push(`${page}: activity access row ${i + 1} is missing its official activity source`);
          }
          const routeDestination = sampleRoute && sampleRoute.destinations[activities[i].name];
          if (routeDestination && routeDestination.kind === 'activity') {
            if (!row[0].includes('MTA GTFS source')) errors.push(`${page}: measured activity row ${i + 1} is missing its MTA source`);
            if (!row[0].includes('Census geocoder query')) errors.push(`${page}: measured activity row ${i + 1} is missing its geocoder source`);
            if (typeof routeDestination.minutes === 'number') {
              sampleMinutes.push(routeDestination);
              if (!row[0].includes(`~${routeDestination.minutes.toFixed(1)} min`)) {
                errors.push(`${page}: activity row ${i + 1} does not show the saved modelled minute value`);
              }
            }
          } else if (/^Digital ticket/i.test(String(activities[i].address || ''))) {
            if (!row[0].includes('No single destination')) errors.push(`${page}: pass row ${i + 1} is not labelled as a non-place`);
          } else if (!row[0].includes('Unmeasured')) {
            errors.push(`${page}: unmeasured activity row ${i + 1} is not clearly flagged`);
          }
        });
        const expectedWithin = sampleMinutes.filter((d) => d.within_1h === true).length;
        const expectedSummary = `${expectedWithin} of ${sampleMinutes.length} measured activities`;
        if (!get('activity-access-summary').innerHTML.includes(expectedSummary)) {
          errors.push(`${page}: activity access summary does not match the saved sample route data`);
        }
        const hotelControl = get('activity-access-hotel');
        const serviceControl = get('activity-access-service');
        const departureControl = get('activity-access-departure');
        if (hotelControl.options.length > 1) {
          hotelControl.value = hotelControl.options[1].value;
          hotelControl.fire('change');
          if (!get('activity-access-summary').innerHTML.includes(hotelControl.options[1].textContent)) {
            errors.push(`${page}: changing the hotel filter did not update the access summary`);
          }
        } else {
          errors.push(`${page}: hotel filter has fewer than two options`);
        }
        if (serviceControl.options.length > 1) {
          serviceControl.value = serviceControl.options[1].value;
          serviceControl.fire('change');
          const [service, date] = serviceControl.value.split('|');
          const expected = `${service[0].toUpperCase()}${service.slice(1)} service · ${date.slice(0, 4)}-${date.slice(4, 6)}-${date.slice(6, 8)} sample`;
          if (!get('activity-access-summary').innerHTML.includes(expected)) {
            errors.push(`${page}: changing the sample service day did not update the access summary`);
          }
        } else {
          errors.push(`${page}: service-day filter has fewer than two options`);
        }
        if (departureControl.options.length > 1) {
          departureControl.value = departureControl.options[1].value;
          departureControl.fire('change');
          if (!get('activity-access-summary').innerHTML.includes(`depart ${departureControl.value}`)) {
            errors.push(`${page}: changing the departure time did not update the access summary`);
          }
        } else {
          errors.push(`${page}: departure-time filter has fewer than two options`);
        }
      }
      for (const [i, r] of extraRows.entries()) {
        if (!/href=/i.test(r[0])) errors.push(`${page}: #${id} body row ${i + 1} has no link`);
      }
      rowCount += extraRows.length;
      console.log(`${page}: #${id} ${extraRows.length} rendered rows`);
    }
  }
  if (hasMainHost) {
  const headerMatch = out.match(/<thead[\s\S]*?<\/thead>/i) || out.match(/<tr[\s\S]*?<\/tr>/i);
  const header = headerMatch ? headerMatch[0] : '';
  if (!/<th[^>]*>\s*Source\s*<\/th>/i.test(header)) {
    errors.push(`${page}: rendered table has no Source header`);
  }
  const body = out.replace(/<thead[\s\S]*?<\/thead>/i, '');
  const rows = [...body.matchAll(/<tr[\s\S]*?<\/tr>/gi)]
    .map((r) => r[0])
    .filter((r) => /<td[\s>]/i.test(r));
  if (!rows.length) {
    errors.push(`${page}: rendered table has no body rows`);
    return;
  }
  let pricedRowsOnPage = 0;
  rows.forEach((row, i) => {
    rowCount++;
    if (!/<a\s/i.test(row) || !/href=/i.test(row)) {
      errors.push(`${page}: rendered body row ${i + 1} has no source link`);
    }
    const priced = /2\s*×\s*\$/.test(row);
    if (priced) {
      pricedRowCount++;
      pricedRowsOnPage++;
      if (!/official menu \/ FAQ \/ PDF/i.test(row)) {
        errors.push(`${page}: priced rendered row ${i + 1} has no official menu link`);
      }
      if (!/excludes beverages, tax, and gratuity/i.test(row)) {
        errors.push(`${page}: priced rendered row ${i + 1} has no exclusions caveat`);
      }
    }
  });
  for (const a of out.matchAll(/<a\s+[^>]*href="([^"]+)"[^>]*>/gi)) {
    const href = a[1];
    const tag = a[0];
    if (!href || href === '#' || /^javascript:/i.test(href)) {
      errors.push(`${page}: rendered anchor has invalid href=${JSON.stringify(href)}`);
    }
    if (/target="_blank"/i.test(tag) && !/rel="[^"]*noopener[^"]*noreferrer/i.test(tag)) {
      errors.push(`${page}: rendered new-tab anchor lacks noopener/noreferrer: ${href}`);
    }
  }
  console.log(`${page}: ${rows.length} rendered rows, ${pricedRowsOnPage} priced rows`);
  }
}

// The Decide page's headline cards are static text; the numbers they print come
// from data files other sessions update. Compare them with the data.
function checkHeroNumbers() {
  const html = fs.readFileSync(path.join(ROOT, 'decide.html'), 'utf8');
  const ranking = JSON.parse(fs.readFileSync(path.join(ROOT, 'research/generated/transit_1h.json'), 'utf8'));
  const expect = [
    ['hotels compared', String(ranking.ranking.length)],
    ['starred restaurants within an hour', String(ranking.ranking[0].within_60_min_count)],
    ['open questions', String(JSON.parse(fs.readFileSync(path.join(ROOT, 'data/blockers.json'), 'utf8')).blockers.length)],
    ['suggestions to review', String(JSON.parse(fs.readFileSync(path.join(ROOT, 'data/suggestions.json'), 'utf8')).suggestions.length)],
  ];
  for (const [label, want] of expect) {
    const re = new RegExp('<span class="count">(\\d+)</span><h3>[^<]*' + label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i');
    const m = html.match(re);
    if (!m) { errors.push(`decide.html: no headline card for "${label}"`); continue; }
    if (m[1] !== want) errors.push(`decide.html: headline card "${label}" says ${m[1]}, data says ${want}`);
  }
}

(async () => {
  checkHeroNumbers();
  for (const page of PAGES) {
    await renderPage(page);
  }
  if (errors.length) {
    console.error(`Rendered-table check FAILED with ${errors.length} error(s):`);
    for (const e of errors) console.error(` - ${e}`);
    process.exit(1);
  }
  console.log(`OK: ${PAGES.length} dynamic renderers produced ${rowCount} source-linked rows (${pricedRowCount} priced rows)`);
})().catch((e) => {
  console.error(e.stack || e.message);
  process.exit(1);
});
