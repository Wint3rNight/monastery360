from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page


@cache_page(60 * 60 * 24)  # Cache for 24 hours
def manifest_view(request):
    """PWA manifest file"""
    manifest = {
        "name": "Monastery360 - Digital Heritage of Sikkim's Monasteries",
        "short_name": "Monastery360",
        "description": "Explore Buddhist monasteries of Sikkim through virtual tours, digital archives, and cultural experiences",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#8B4513",
        "theme_color": "#8B4513",
        "orientation": "portrait-primary",
        "scope": "/",
        "lang": "en",
        "dir": "ltr",
        "categories": ["travel", "education", "lifestyle", "religion"],
        "icons": [
            {
                "src": "/static/images/icons/icon-72x72.png",
                "sizes": "72x72",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/images/icons/icon-96x96.png",
                "sizes": "96x96",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/images/icons/icon-128x128.png",
                "sizes": "128x128",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/images/icons/icon-144x144.png",
                "sizes": "144x144",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/images/icons/icon-152x152.png",
                "sizes": "152x152",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/images/icons/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/images/icons/icon-384x384.png",
                "sizes": "384x384",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/images/icons/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ],
        "shortcuts": [
            {
                "name": "Explore Monasteries",
                "short_name": "Monasteries",
                "description": "Browse all Buddhist monasteries in Sikkim",
                "url": "/monasteries/",
                "icons": [
                    {
                        "src": "/static/images/icons/shortcut-monasteries.png",
                        "sizes": "96x96"
                    }
                ]
            },
            {
                "name": "Virtual Tours",
                "short_name": "Tours",
                "description": "Experience 360° virtual monastery tours",
                "url": "/tours/",
                "icons": [
                    {
                        "src": "/static/images/icons/shortcut-tours.png",
                        "sizes": "96x96"
                    }
                ]
            },
            {
                "name": "Map View",
                "short_name": "Map",
                "description": "Interactive map of monastery locations",
                "url": "/map/",
                "icons": [
                    {
                        "src": "/static/images/icons/shortcut-map.png",
                        "sizes": "96x96"
                    }
                ]
            },
            {
                "name": "Book Visit",
                "short_name": "Book",
                "description": "Schedule a monastery visit",
                "url": "/bookings/",
                "icons": [
                    {
                        "src": "/static/images/icons/shortcut-book.png",
                        "sizes": "96x96"
                    }
                ]
            }
        ],
        "screenshots": [
            {
                "src": "/static/images/screenshots/home-mobile.png",
                "sizes": "360x640",
                "type": "image/png",
                "platform": "narrow",
                "label": "Monastery360 mobile homepage"
            },
            {
                "src": "/static/images/screenshots/monasteries-mobile.png",
                "sizes": "360x640",
                "type": "image/png",
                "platform": "narrow",
                "label": "Monastery listings on mobile"
            },
            {
                "src": "/static/images/screenshots/tour-mobile.png",
                "sizes": "360x640",
                "type": "image/png",
                "platform": "narrow",
                "label": "Virtual tour experience on mobile"
            },
            {
                "src": "/static/images/screenshots/home-desktop.png",
                "sizes": "1280x720",
                "type": "image/png",
                "platform": "wide",
                "label": "Monastery360 desktop homepage"
            },
            {
                "src": "/static/images/screenshots/map-desktop.png",
                "sizes": "1280x720",
                "type": "image/png",
                "platform": "wide",
                "label": "Interactive monastery map on desktop"
            }
        ],
        "prefer_related_applications": False,
        "edge_side_panel": {
            "preferred_width": 400
        },
        "handle_links": "preferred",
        "launch_handler": {
            "client_mode": "navigate-existing"
        },
        "protocol_handlers": [
            {
                "protocol": "web+monastery360",
                "url": "/share/?monastery=%s"
            }
        ],
        "share_target": {
            "action": "/share/",
            "method": "POST",
            "enctype": "multipart/form-data",
            "params": {
                "title": "title",
                "text": "text",
                "url": "url",
                "files": [
                    {
                        "name": "image",
                        "accept": ["image/*"]
                    }
                ]
            }
        }
    }

    return JsonResponse(manifest)


@cache_page(60 * 60 * 24)  # Cache for 24 hours
def service_worker_view(request):
    """Service Worker for PWA functionality"""
    sw_content = """
// Monastery360 Service Worker
// Handles caching, offline functionality, and background sync

const CACHE_VERSION = 'v1';
const STATIC_CACHE = `monastery360-static-${CACHE_VERSION}`;
const DYNAMIC_CACHE = `monastery360-dynamic-${CACHE_VERSION}`;
const IMAGE_CACHE = `monastery360-images-${CACHE_VERSION}`;

// Resources to cache immediately
const STATIC_ASSETS = [
    '/static/css/styles.css',
    '/static/js/main.js',
    '/static/js/geofence.js',
    '/offline/',
    '/static/images/monastery360-icon.png',
    '/static/images/monastery-placeholder.jpg',
    // CDN resources
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
    'https://unpkg.com/react@18/umd/react.production.min.js',
    'https://unpkg.com/react-dom@18/umd/react-dom.production.min.js'
];

// Install event - cache static assets
self.addEventListener('install', event => {
    console.log('Service Worker installing...');

    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(cache => {
                console.log('Caching static assets...');
                return cache.addAll(STATIC_ASSETS);
            })
            .then(() => {
                console.log('Static assets cached successfully');
                return self.skipWaiting();
            })
            .catch(error => {
                console.error('Failed to cache static assets:', error);
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    console.log('Service Worker activating...');

    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                return Promise.all(
                    cacheNames
                        .filter(cacheName =>
                            cacheName.startsWith('monastery360-') &&
                            !cacheName.endsWith(CACHE_VERSION)
                        )
                        .map(cacheName => {
                            console.log('Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        })
                );
            })
            .then(() => {
                console.log('Old caches cleaned up');
                return self.clients.claim();
            })
    );
});

// Fetch event - serve from cache or network
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);

    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }

    // Skip external URLs (except CDN)
    if (url.origin !== location.origin && !isCDNRequest(url)) {
        return;
    }

    // Handle different resource types
    if (isImageRequest(request)) {
        event.respondWith(handleImageRequest(request));
    } else if (isAPIRequest(request)) {
        event.respondWith(handleAPIRequest(request));
    } else if (isStaticAsset(request)) {
        event.respondWith(handleStaticAsset(request));
    } else {
        event.respondWith(handlePageRequest(request));
    }
});

// Helper functions
function isCDNRequest(url) {
    const cdnHosts = [
        'cdn.jsdelivr.net',
        'cdnjs.cloudflare.com',
        'unpkg.com',
        'fonts.googleapis.com',
        'fonts.gstatic.com'
    ];
    return cdnHosts.some(host => url.hostname.includes(host));
}

function isImageRequest(request) {
    return request.destination === 'image' ||
           request.url.match(/\\.(jpg|jpeg|png|gif|webp|svg)$/i);
}

function isAPIRequest(request) {
    return request.url.includes('/api/');
}

function isStaticAsset(request) {
    return request.url.includes('/static/') ||
           request.destination === 'style' ||
           request.destination === 'script';
}

// Image caching strategy - Cache First
async function handleImageRequest(request) {
    try {
        const cache = await caches.open(IMAGE_CACHE);
        const cachedResponse = await cache.match(request);

        if (cachedResponse) {
            return cachedResponse;
        }

        const networkResponse = await fetch(request);

        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }

        return networkResponse;
    } catch (error) {
        console.error('Image request failed:', error);

        // Return placeholder image
        const cache = await caches.open(STATIC_CACHE);
        return cache.match('/static/images/monastery-placeholder.jpg');
    }
}

// API caching strategy - Network First with background sync
async function handleAPIRequest(request) {
    try {
        // Try network first
        const networkResponse = await fetch(request);

        if (networkResponse.ok) {
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put(request, networkResponse.clone());
            return networkResponse;
        }

        throw new Error('Network response not ok');
    } catch (error) {
        console.log('API network failed, trying cache:', error);

        const cache = await caches.open(DYNAMIC_CACHE);
        const cachedResponse = await cache.match(request);

        if (cachedResponse) {
            return cachedResponse;
        }

        // Return offline response for API requests
        return new Response(
            JSON.stringify({
                error: 'Offline',
                message: 'Content not available offline'
            }),
            {
                status: 503,
                headers: { 'Content-Type': 'application/json' }
            }
        );
    }
}

// Static asset strategy - Cache First
async function handleStaticAsset(request) {
    try {
        const cache = await caches.open(STATIC_CACHE);
        const cachedResponse = await cache.match(request);

        if (cachedResponse) {
            return cachedResponse;
        }

        const networkResponse = await fetch(request);

        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }

        return networkResponse;
    } catch (error) {
        console.error('Static asset request failed:', error);
        throw error;
    }
}

// Page request strategy - Network First
async function handlePageRequest(request) {
    try {
        const networkResponse = await fetch(request);

        if (networkResponse.ok) {
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put(request, networkResponse.clone());
        }

        return networkResponse;
    } catch (error) {
        console.log('Page network failed, trying cache:', error);

        const cache = await caches.open(DYNAMIC_CACHE);
        const cachedResponse = await cache.match(request);

        // Only return a cached response when the cached resource's pathname
        // exactly matches the requested pathname. This prevents the SW from
        // returning the app-shell (root '/') for unrelated routes like
        // /archives/<...> when the root page was pre-cached.
        if (cachedResponse) {
            try {
                const cachedPath = new URL(cachedResponse.url).pathname;
                const reqPath = new URL(request.url).pathname;
                if (cachedPath === reqPath) {
                    return cachedResponse;
                }
            } catch (e) {
                // If URL parsing fails for any reason, fall back to returning
                // the cached response to avoid breaking offline usage.
                return cachedResponse;
            }
        }

        // Return offline page when there is no matching cached page
        return caches.match('/offline/');
    }
}

// Background sync for form submissions
self.addEventListener('sync', event => {
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

async function doBackgroundSync() {
    console.log('Performing background sync...');

    // Handle queued form submissions, bookings, etc.
    const syncData = await getStoredSyncData();

    for (const item of syncData) {
        try {
            await fetch(item.url, {
                method: item.method,
                headers: item.headers,
                body: item.body
            });

            await removeSyncData(item.id);
            console.log('Synced item:', item.id);
        } catch (error) {
            console.error('Sync failed for item:', item.id, error);
        }
    }
}

// Push notifications
self.addEventListener('push', event => {
    const options = {
        body: event.data ? event.data.text() : 'New monastery update available!',
        icon: '/static/images/monastery360-icon.png',
        badge: '/static/images/monastery360-badge.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'explore',
                title: 'Explore',
                icon: '/static/images/actions/explore.png'
            },
            {
                action: 'close',
                title: 'Close',
                icon: '/static/images/actions/close.png'
            }
        ]
    };

    event.waitUntil(
        self.registration.showNotification('Monastery360', options)
    );
});

// Notification click handling
self.addEventListener('notificationclick', event => {
    const notification = event.notification;
    const action = event.action;

    if (action === 'close') {
        notification.close();
    } else {
        event.waitUntil(
            clients.matchAll().then(clis => {
                const client = clis.find(c => c.visibilityState === 'visible');

                if (client !== undefined) {
                    client.navigate('/');
                    client.focus();
                } else {
                    clients.openWindow('/');
                }

                notification.close();
            })
        );
    }
});

// Utility functions for IndexedDB operations
async function getStoredSyncData() {
    // Implement IndexedDB operations for offline sync
    return [];
}

async function removeSyncData(id) {
    // Implement IndexedDB removal
    return Promise.resolve();
}

console.log('Monastery360 Service Worker loaded successfully');
"""

    return HttpResponse(
        sw_content,
        content_type='application/javascript',
        headers={
            'Service-Worker-Allowed': '/',
            'Cache-Control': 'no-cache, no-store, must-revalidate'
        }
    )
