/* Casa Escondida report — service worker (offline-capable PWA) */
const CACHE = 'casa-escondida-v6';
const CORE = [
  './',
  'index.html',
  'ai-blackbox.html',
  'ai-build-playbook.html',
  'accounting-revamp.html',
  'requirements.html',
  'quotation.html',
  'stakeholder-questions.html',
  'staff-guides.html',
  'odoo-sales.html',
  'odoo-demo-guide.html',
  'owner-faq.html',
  'profit-estimator.html',
  'manifest.webmanifest',
  'icon-192.png',
  'icon-512.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(CORE)).then(() => self.skipWaiting()).catch(() => {})
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

function cachePut(req, res) {
  if (res && res.status === 200 && req.url.startsWith(self.location.origin)) {
    const copy = res.clone();
    caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
  }
  return res;
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;

  const accept = req.headers.get('accept') || '';
  const isHTML = req.mode === 'navigate' || accept.includes('text/html') || /\.html?($|\?)/.test(req.url);

  if (isHTML) {
    // network-first: always try fresh HTML, fall back to cache (offline), then shell
    e.respondWith(
      fetch(req).then((res) => cachePut(req, res))
        .catch(() => caches.match(req).then((hit) => hit || caches.match('index.html')))
    );
    return;
  }

  // cache-first for static assets (icons, manifest, etc.)
  e.respondWith(
    caches.match(req).then((hit) => hit || fetch(req).then((res) => cachePut(req, res)).catch(() => caches.match('index.html')))
  );
});
