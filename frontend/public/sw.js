/* Muallim service worker: ilova qobig'ini offline ochish va ko'rilgan dars materiallarini keshlash. */
const SHELL = 'muallim-shell-v1'
const CONTENT = 'muallim-content-v1'

// Faqat hamma uchun bir xil bo'lgan kontent (dars, taqdimot, o'yinlar) keshlanadi - shaxsiy ma'lumot emas.
const CONTENT_RE = /\/api\/history\/(topics\/\d+\/(lesson|assets\/[a-z_]+)|subjects|books)\/?$/

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(SHELL).then((c) => c.addAll(['/', '/manifest.webmanifest', '/icon.svg'])))
  self.skipWaiting()
})

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => ![SHELL, CONTENT].includes(k)).map((k) => caches.delete(k)))
    )
  )
  self.clients.claim()
})

self.addEventListener('message', (e) => {
  if (e.data === 'clear-content') caches.delete(CONTENT)
})

async function networkFirst(request, cacheName) {
  const cache = await caches.open(cacheName)
  try {
    const res = await fetch(request)
    if (res.ok) cache.put(request, res.clone())
    return res
  } catch (err) {
    const hit = await cache.match(request)
    if (hit) return hit
    throw err
  }
}

self.addEventListener('fetch', (e) => {
  const { request } = e
  if (request.method !== 'GET') return
  const url = new URL(request.url)

  if (CONTENT_RE.test(url.pathname) && url.pathname.startsWith('/api/')) {
    e.respondWith(networkFirst(request, CONTENT))
    return
  }
  // API tashqi porta (8000) bo'lsa ham kontentni keshlaymiz
  if (CONTENT_RE.test(url.pathname)) {
    e.respondWith(networkFirst(request, CONTENT))
    return
  }

  if (url.origin !== self.location.origin) return

  if (request.mode === 'navigate') {
    e.respondWith(
      fetch(request).catch(() => caches.match('/').then((r) => r || Response.error()))
    )
    return
  }

  if (/\.(js|css|svg|png|woff2?)$/.test(url.pathname) || url.pathname.startsWith('/assets/')) {
    e.respondWith(
      caches.open(SHELL).then(async (cache) => {
        const hit = await cache.match(request)
        const net = fetch(request).then((res) => {
          if (res.ok) cache.put(request, res.clone())
          return res
        }).catch(() => hit)
        return hit || net
      })
    )
  }
})
