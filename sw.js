---
layout: null
sitemap: false
---
/* Σ Sigma — service worker (site et application Android).
   - pages HTML : réseau d'abord (délai court), puis copie locale, puis page hors ligne ;
   - CSS, JS, images, index de recherche : copie locale immédiate, mise à jour en arrière-plan ;
   - PDF : réseau d'abord (un PDF corrigé est donc toujours récupéré), copie gardée pour la relecture
     hors ligne si sa taille reste raisonnable (plafond par fichier et en nombre de fichiers) ;
   - jamais interceptés : les requêtes vers d'autres sites (GeoGebra, Basthon, polices, statistiques…),
     Python dans le navigateur (/assets/pyodide/, laissé au cache du navigateur), les requêtes partielles.
   La version change à chaque publication du site : les anciens caches de ressources sont supprimés,
   et la nouvelle version ne s'active que lorsque l'élève touche « Actualiser ». */
const VERSION = '{{ site.time | date: "%Y%m%d%H%M%S" }}';
const STATIC = 'sigma-static-' + VERSION;
const PAGES = 'sigma-pages-v2';          // pages déjà vues : conservées d'une version à l'autre (réseau d'abord)
const PDFS = 'sigma-pdf-v2';
const PAGES_MAX = 150;
const PDF_MAX_FILES = 40;
const PDF_MAX_BYTES = 8 * 1024 * 1024;   // un PDF plus lourd n'est pas gardé
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

async function trim(name, max) {
  const c = await caches.open(name);
  const keys = await c.keys();
  for (let i = 0; i < keys.length - max; i++) await c.delete(keys[i]);
}

async function keepPdf(c, url, res) {
  const len = Number(res.headers.get('content-length') || 0);
  if (len > PDF_MAX_BYTES) return;
  const blob = await res.blob();
  if (blob.size > PDF_MAX_BYTES) return;
  await c.put(url, new Response(blob, { headers: { 'Content-Type': 'application/pdf' } }));
  await trim(PDFS, PDF_MAX_FILES);
}

async function pdf(e) {
  const req = e.request;
  const c = await caches.open(PDFS);
  try {
    const res = await Promise.race([fetch(req), timeout(8000)]);
    if (res && res.ok && res.status === 200) e.waitUntil(keepPdf(c, req.url, res.clone()).catch(() => {}));
    return res;
  } catch (err) {
    return (await c.match(req.url)) || (await caches.match('/offline/')) || Response.error();
  }
}

async function page(e) {
  const req = e.request;
  const c = await caches.open(PAGES);
  try {
    const res = await Promise.race([fetch(req), timeout(4000)]);
    if (res && res.ok && res.status === 200 && !res.redirected) {
      e.waitUntil(c.put(req, res.clone()).then(() => trim(PAGES, PAGES_MAX)).catch(() => {}));
    }
    return res;
  } catch (err) {
    return (await c.match(req)) || (await caches.match(req)) || (await caches.match(req, { ignoreSearch: true }))
      || (await caches.match('/offline/')) || Response.error();
  }
}

async function swr(e) {
  const req = e.request;
  const c = await caches.open(STATIC);
  const hit = await c.match(req);
  const net = fetch(req).then((res) => { if (res && res.ok && res.status === 200) c.put(req, res.clone()).catch(() => {}); return res; }).catch(() => null);
  if (hit) { e.waitUntil(net); return hit; }
  return (await net) || Response.error();
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;                 // GeoGebra, Basthon, Google, GoatCounter…
  if (req.headers.has('range')) return;
  if (url.pathname.startsWith('/assets/pyodide/')) return;    // Python : gros fichiers, cache du navigateur
  if (url.pathname === '/sw.js' || url.pathname.startsWith('/.well-known/')) return;
  if (url.pathname.endsWith('.pdf')) { e.respondWith(pdf(e)); return; }
  if (req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html')) { e.respondWith(page(e)); return; }
  if (/\.(css|js|mjs|json|svg|png|webp|jpg|jpeg|gif|ico|woff2?|webmanifest)$/.test(url.pathname)) { e.respondWith(swr(e)); return; }
});
