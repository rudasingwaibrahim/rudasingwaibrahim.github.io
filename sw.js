---
layout: null
sitemap: false
---
/* Σ Sigma — service worker
   - pages HTML : réseau d'abord (délai court), puis copie locale, puis page hors ligne ;
   - CSS, JS, images, index de recherche : copie locale immédiate, mise à jour en arrière-plan ;
   - PDF : gardés après la première ouverture pour être relus hors ligne (plafond de taille).
   La version change à chaque publication du site : les anciens caches sont supprimés,
   et la nouvelle version ne s'active que lorsque l'élève accepte « Actualiser ». */
const VERSION = '{{ site.time | date: "%Y%m%d%H%M%S" }}';
const STATIC = 'sigma-static-' + VERSION;
const PAGES = 'sigma-pages-' + VERSION;
const PDFS = 'sigma-pdf-v1';
const PDF_MAX_FILES = 40;
const PDF_MAX_BYTES = 15 * 1024 * 1024;   // un PDF plus lourd n'est pas gardé
const PRECACHE = ['/', '/offline/', '/assets/css/style.css?v=5', '/assets/js/sigma.js?v=3',
  '/assets/images/favicon.svg', '/assets/images/icon-192.png', '/manifest.webmanifest'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(STATIC).then((c) => Promise.all(PRECACHE.map((u) => c.add(u).catch(() => null)))));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys
    .filter((k) => k.startsWith('sigma-') && ![STATIC, PAGES, PDFS].includes(k))
    .map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('message', (e) => { if (e.data && e.data.type === 'SKIP_WAITING') self.skipWaiting(); });

function timeout(ms) { return new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), ms)); }

async function trimPdfs() {
  const c = await caches.open(PDFS);
  const keys = await c.keys();
  for (let i = 0; i < keys.length - PDF_MAX_FILES; i++) await c.delete(keys[i]);
}

async function pdf(req) {
  const c = await caches.open(PDFS);
  const hit = await c.match(req.url);
  if (hit) return hit;
  const res = await fetch(req);
  const len = Number(res.headers.get('content-length') || 0);
  if (res.ok && res.status === 200 && (!len || len <= PDF_MAX_BYTES)) {
    c.put(req.url, res.clone()).then(trimPdfs).catch(() => {});
  }
  return res;
}

async function page(req) {
  const c = await caches.open(PAGES);
  try {
    const res = await Promise.race([fetch(req), timeout(4000)]);
    if (res && res.ok) c.put(req, res.clone()).catch(() => {});
    return res;
  } catch (err) {
    return (await c.match(req)) || (await caches.match(req)) || (await caches.match('/offline/')) || Response.error();
  }
}

async function swr(req) {
  const c = await caches.open(STATIC);
  const hit = await c.match(req);
  const net = fetch(req).then((res) => { if (res && res.ok) c.put(req, res.clone()).catch(() => {}); return res; }).catch(() => null);
  return hit || (await net) || Response.error();
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;
  if (req.headers.has('range')) return;
  if (url.pathname.endsWith('.pdf')) { e.respondWith(pdf(req)); return; }
  if (req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html')) { e.respondWith(page(req)); return; }
  if (/\.(css|js|json|svg|png|webp|jpg|jpeg|woff2?|webmanifest)$/.test(url.pathname)) { e.respondWith(swr(req)); return; }
});
