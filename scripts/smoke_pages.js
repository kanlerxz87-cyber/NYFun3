#!/usr/bin/env node
/* Smoke-test every root page in a real DOM.
 *
 * The other checks run the renderers against a hand-rolled DOM stub, which proves
 * the generated rows contain source links but not that a browser can actually
 * execute the page. This loads each page in jsdom, executes its scripts in
 * document order, serves data/*.json to fetch(), fires DOMContentLoaded and then
 * asserts that each rendered host contains real content instead of a
 * "Loading…" placeholder.
 *
 * jsdom is optional: without it this prints SKIP and exits 0, so a checkout with
 * no network still runs the rest of the suite. CI installs it before this step.
 */

const fs = require('fs');
const path = require('path');

let JSDOM;
try {
  ({ JSDOM } = require('jsdom'));
} catch (e) {
  console.log('SKIP: jsdom is not installed (npm install --no-save jsdom)');
  process.exit(0);
}

const ROOT = path.resolve(__dirname, '..');
const MIN_CHARS = 200;
const errors = [];

function run(page) {
  return new Promise((resolve) => {
    const html = fs.readFileSync(path.join(ROOT, page), 'utf8');
    const dom = new JSDOM(html, { runScripts: 'outside-only', url: 'http://localhost/' });
    const w = dom.window;
    w.fetch = (url) => {
      const file = path.join(ROOT, String(url).replace(/^\.?\//, ''));
      try {
        const data = JSON.parse(fs.readFileSync(file, 'utf8'));
        return Promise.resolve({ ok: true, status: 200, json: () => Promise.resolve(data) });
      } catch (e) {
        return Promise.reject(new Error(`cannot read ${url}`));
      }
    };
    for (const [, attrs, body] of html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/gi)) {
      const src = attrs.match(/src="([^"]+)"/);
      try {
        if (src) w.eval(fs.readFileSync(path.join(ROOT, src[1]), 'utf8'));
        else if (body.trim()) w.eval(body);
      } catch (e) {
        errors.push(`${page}: script ${src ? src[1] : '(inline)'} threw ${e.message}`);
      }
    }
    w.document.dispatchEvent(new w.Event('DOMContentLoaded'));
    setTimeout(() => {
      const hosts = [...w.document.querySelectorAll('[id$="-host"], #table-host')];
      for (const host of hosts) {
        const text = host.textContent.trim();
        if (/Loading|Could not load/.test(text)) {
          errors.push(`${page}: #${host.id} still shows "${text.slice(0, 60)}"`);
        } else if (text.length < MIN_CHARS) {
          errors.push(`${page}: #${host.id} rendered only ${text.length} characters`);
        }
        if (!host.querySelector('a[href]')) {
          errors.push(`${page}: #${host.id} rendered no source link`);
        }
      }
      console.log(`${page}: ` + (hosts.length
        ? hosts.map((h) => `${h.id}=${h.textContent.trim().length}ch`).join(' ')
        : 'static page, no rendered hosts'));
      resolve();
    }, 500);
  });
}

(async () => {
  const pages = fs.readdirSync(ROOT).filter((f) => f.endsWith('.html')).sort();
  for (const page of pages) await run(page);
  if (errors.length) {
    console.error(`Rendered-page smoke test FAILED with ${errors.length} error(s):`);
    for (const e of errors) console.error(` - ${e}`);
    process.exit(1);
  }
  console.log(`OK: ${pages.length} pages executed in a DOM and every rendered host produced content`);
})();
