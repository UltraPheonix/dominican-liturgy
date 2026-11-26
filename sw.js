/* Offline support: the site's own files are kept, and every chant, reading and page that has been
   opened once stays available without a connection. Bump VERSION when the site changes. */
var VERSION = 'propria-v120';
var SHELL = ['./', 'index.html', 'about.html', 'rubrics.html', 'style.css', 'versiculum.css', 'js/app.js', 'js/exsurge.min.js', 'js/chant.js', 'js/psalm.js', 'js/tones.js', 'js/mtones.js', 'data/chant/office.json',
  'data/masses.js', 'data/prefaces.js', 'data/ordinary.js', 'data/ordo.js', 'data/orations.js', 'data/readings33.js', 'data/introit_gp.js', 'data/holyweek.js', 'data/holyweek_text.js', 'office.html', 'holyweek.html', 'js/office.js', 'js/ui.js', 'js/cal.js', 'data/office/common.json', 'data/office/range.json', 'manifest.webmanifest', 'icon.svg', 'fonts/versiculum.ttf'];
self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(VERSION).then(function (c) { return c.addAll(SHELL); }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (ks) {
    return Promise.all(ks.filter(function (k) { return k !== VERSION; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;
  var url = new URL(req.url);
  var fonts = /fonts\.(googleapis|gstatic)\.com$/.test(url.hostname);
  if (url.origin !== location.origin && !fonts) return;
  // chants, Bible books and fonts never change: cache first; everything else: network first, cache as fallback
  var stable = fonts || /\/(gabc|bible|fonts)\//.test(url.pathname);
  if (stable) {
    e.respondWith(caches.match(req).then(function (hit) {
      return hit || fetch(req).then(function (r) {
        if (r.ok || r.type === 'opaque') { var cp = r.clone(); caches.open(VERSION).then(function (c) { c.put(req, cp); }); }
        return r;
      });
    }));
  } else {
    e.respondWith(fetch(req).then(function (r) {
      if (r.ok) { var cp = r.clone(); caches.open(VERSION).then(function (c) { c.put(req, cp); }); }
      return r;
    }).catch(function () {
      return caches.match(req, {ignoreSearch: true}).then(function (hit) { return hit || caches.match('index.html'); });
    }));
  }
});
