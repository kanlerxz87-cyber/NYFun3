#!/usr/bin/env node
/* Execute every site HTML page in a DOM and verify dynamically rendered hosts.
 * Pages are discovered recursively so the curated pages/ dossier is included.
 * jsdom is installed by CI; a dependency-free checkout can still run the other
 * validators and reports an explicit skip here. */

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
const SKIP_DIRS = new Set(['.git', 'node_modules']);
const errors = [];

function htmlPages(dir = ROOT, rel = '') {
  const pages = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory() && !SKIP_DIRS.has(entry.name)) {
      pages.push(...htmlPages(path.join(dir, entry.name), path.join(rel, entry.name)));
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      pages.push(path.join(rel, entry.name).split(path.sep).join('/'));
    }
  }
  return pages.sort();
}

function localFile(url, baseUrl) {
  const parsed = new URL(String(url), baseUrl);
  if (parsed.origin !== 'http://localhost') throw new Error(`external asset is not loaded in the local smoke test: ${parsed.href}`);
  const relative = decodeURIComponent(parsed.pathname).replace(/^\/+/, '');
  return path.join(ROOT, relative);
}

function run(page) {
  return new Promise((resolve) => {
    const html = fs.readFileSync(path.join(ROOT, page), 'utf8');
    const pageUrl = new URL(page, 'http://localhost/').href;
    const dom = new JSDOM(html, { runScripts: 'outside-only', url: pageUrl });
    const w = dom.window;
    w.fetch = (url) => {
      try {
        const data = JSON.parse(fs.readFileSync(localFile(url, pageUrl), 'utf8'));
        return Promise.resolve({ ok: true, status: 200, json: () => Promise.resolve(data) });
      } catch (e) {
        return Promise.reject(new Error(`cannot read ${url}: ${e.message}`));
      }
    };
    for (const [, attrs, body] of html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/gi)) {
      const src = attrs.match(/src="([^"]+)"/);
      try {
        if (src) w.eval(fs.readFileSync(localFile(src[1], pageUrl), 'utf8'));
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
          errors.push(`${page}: #${host.id} still shows "${text.slice(0, 80)}"`);
        } else if (text.length < MIN_CHARS) {
          errors.push(`${page}: #${host.id} rendered only ${text.length} characters`);
        }
        if (!host.querySelector('a[href]')) errors.push(`${page}: #${host.id} rendered no source link`);
      }
      console.log(`${page}: ` + (hosts.length
        ? hosts.map((h) => `${h.id}=${h.textContent.trim().length}ch`).join(' ')
        : 'static page, no rendered hosts'));
      dom.window.close();
      resolve();
    }, 500);
  });
}

(async () => {
  const pages = htmlPages();
  for (const page of pages) await run(page);
  if (errors.length) {
    console.error(`Rendered-page smoke test FAILED with ${errors.length} error(s):`);
    for (const e of errors) console.error(` - ${e}`);
    process.exit(1);
  }
  console.log(`OK: ${pages.length} site HTML pages executed in a DOM; every dynamic host produced content`);
})();
