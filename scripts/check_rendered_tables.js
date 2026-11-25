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
];
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
    appendChild() {},
    addEventListener() {},
    setAttribute() {},
  };
}

async function renderPage(page) {
  const html = fs.readFileSync(path.join(ROOT, page), 'utf8');
  const scripts = [];
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
  const document = {
    getElementById: get,
    createElement: (tag) => makeElement(tag),
    addEventListener() {},
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
  // Let all fetch().then() microtasks settle.
  await new Promise((resolve) => setTimeout(resolve, 0));
  await new Promise((resolve) => setImmediate(resolve));

  const host = get('table-host');
  const out = host.innerHTML;
  if (!out || /Could not load/i.test(out)) {
    errors.push(`${page}: table-host was not rendered (${out.slice(0, 140)})`);
    return;
  }
  if (!/<table/i.test(out)) {
    errors.push(`${page}: rendered host has no table`);
    return;
  }
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

(async () => {
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
