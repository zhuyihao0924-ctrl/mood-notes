const CACHE_NAME = 'mood-notes-pwa-v15';
const APP_SHELL = [
  '/',
  '/manifest.webmanifest?v=photo5',
  '/static/app-icon-192.png?v=photo5',
  '/static/app-icon-512.png?v=photo5',
  '/static/theme-polish.css?v=skin8',
  '/static/themes/templates/milk-bg.png?v=skin8',
  '/static/themes/templates/milk-wall.png?v=skin8',
  '/static/themes/templates/milk-left.png?v=skin8',
  '/static/themes/templates/milk-right.png?v=skin8',
  '/static/themes/templates/milk-bottom.png?v=skin8',
  '/static/themes/templates/night-bg.png?v=skin8',
  '/static/themes/templates/night-wall.png?v=skin8',
  '/static/themes/templates/night-left.png?v=skin8',
  '/static/themes/templates/night-right.png?v=skin8',
  '/static/themes/templates/night-bottom.png?v=skin8',
  '/static/themes/templates/blue-bg.png?v=skin8',
  '/static/themes/templates/blue-wall.png?v=skin8',
  '/static/themes/templates/blue-left.png?v=skin8',
  '/static/themes/templates/blue-right.png?v=skin8',
  '/static/themes/templates/blue-bottom.png?v=skin8',
  '/static/themes/templates/berry-bg.png?v=skin8',
  '/static/themes/templates/berry-wall.png?v=skin8',
  '/static/themes/templates/berry-left.png?v=skin8',
  '/static/themes/templates/berry-right.png?v=skin8',
  '/static/themes/templates/berry-bottom.png?v=skin8',
  '/static/splash.svg'
];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL)));
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))))
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);

  if (request.method !== 'GET' || url.pathname.startsWith('/api/') || url.pathname === '/login') {
    return;
  }

  event.respondWith(
    fetch(request)
      .then(response => {
        const copy = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(request, copy));
        return response;
      })
      .catch(() => caches.match(request).then(cached => cached || caches.match('/')))
  );
});
