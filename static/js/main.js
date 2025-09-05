/**
 * Monastery360 - Main JavaScript
 * Handles PWA functionality, interactive features, and React component integration
 */

// Global app state and utilities
window.Monastery360 = {
    // Configuration
    config: {
        mapCenter: [27.3389, 88.6065], // Gangtok, Sikkim
        mapZoom: 10,
        apiBase: '/api/v1/',
        searchDebounceMs: 300,
        animationDuration: 300
    },

    // Utility functions
    utils: {
        // Debounce function for search
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        // Format distance
        formatDistance: function(meters) {
            if (meters < 1000) {
                return `${Math.round(meters)}m`;
            }
            return `${(meters / 1000).toFixed(1)}km`;
        },

        // Get user's location
        getUserLocation: function() {
            return new Promise((resolve, reject) => {
                if (!navigator.geolocation) {
                    reject(new Error('Geolocation not supported'));
                    return;
                }

                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        resolve({
                            lat: position.coords.latitude,
                            lng: position.coords.longitude,
                            accuracy: position.coords.accuracy
                        });
                    },
                    (error) => {
                        reject(error);
                    },
                    {
                        enableHighAccuracy: true,
                        timeout: 10000,
                        maximumAge: 300000 // 5 minutes
                    }
                );
            });
        },

        // Show notification
        showNotification: function(message, type = 'info') {
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
            alertDiv.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;

            const container = document.querySelector('.container') || document.body;
            container.insertBefore(alertDiv, container.firstChild);

            // Auto-dismiss after 5 seconds
            setTimeout(() => {
                if (alertDiv && alertDiv.parentNode) {
                    alertDiv.remove();
                }
            }, 5000);
        },

        // API helper
        api: async function(endpoint, options = {}) {
            const url = window.Monastery360.config.apiBase + endpoint;
            const defaultOptions = {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
                }
            };

            try {
                const response = await fetch(url, { ...defaultOptions, ...options });
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return await response.json();
            } catch (error) {
                console.error('API Error:', error);
                throw error;
            }
        }
    },

    // Initialize application
    init: function() {
        this.initPWA();
        this.initEventListeners();
        this.initBackToTop();
        this.initLazyLoading();
        this.initPerformanceMonitoring();
    },

    // PWA functionality
    initPWA: function() {
        // Install prompt
        let deferredPrompt;
        const installButton = document.getElementById('install-pwa');

        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            if (installButton) {
                installButton.classList.remove('d-none');
            }
        });

        if (installButton) {
            installButton.addEventListener('click', async () => {
                if (deferredPrompt) {
                    deferredPrompt.prompt();
                    const { outcome } = await deferredPrompt.userChoice;
                    if (outcome === 'accepted') {
                        installButton.classList.add('d-none');
                    }
                    deferredPrompt = null;
                }
            });
        }

        // Service worker update notification
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.addEventListener('controllerchange', () => {
                this.utils.showNotification(
                    'App updated! Refresh to see the latest version.',
                    'info'
                );
            });
        }
    },

    // Event listeners
    initEventListeners: function() {
        // Search functionality
        this.initSearch();

        // Form enhancements
        this.initForms();

        // Image lazy loading
        this.initImageLazyLoading();

        // Keyboard navigation
        this.initKeyboardNavigation();

        // Touch gestures for mobile
        this.initTouchGestures();
    },

    // Search functionality
    initSearch: function() {
        const searchInput = document.querySelector('input[name="q"]');
        if (!searchInput) return;

        const debouncedSearch = this.utils.debounce((query) => {
            if (query.length >= 2) {
                this.performLiveSearch(query);
            } else {
                this.clearSearchResults();
            }
        }, this.config.searchDebounceMs);

        searchInput.addEventListener('input', (e) => {
            debouncedSearch(e.target.value.trim());
        });

        // Search suggestions dropdown
        this.createSearchDropdown(searchInput);
    },

    // Live search implementation
    performLiveSearch: async function(query) {
        try {
            const results = await this.utils.api(`search/?q=${encodeURIComponent(query)}`);
            this.displaySearchResults(results);
        } catch (error) {
            console.error('Search error:', error);
        }
    },

    // Create search dropdown
    createSearchDropdown: function(searchInput) {
        const dropdown = document.createElement('div');
        dropdown.className = 'search-dropdown position-absolute bg-white border rounded shadow-lg d-none';
        dropdown.style.cssText = `
            top: 100%;
            left: 0;
            right: 0;
            z-index: 1000;
            max-height: 300px;
            overflow-y: auto;
        `;

        searchInput.parentNode.style.position = 'relative';
        searchInput.parentNode.appendChild(dropdown);

        // Hide dropdown on outside click
        document.addEventListener('click', (e) => {
            if (!searchInput.parentNode.contains(e.target)) {
                dropdown.classList.add('d-none');
            }
        });

        this.searchDropdown = dropdown;
    },

    // Display search results
    displaySearchResults: function(results) {
        if (!this.searchDropdown) return;

        if (results.length === 0) {
            this.searchDropdown.innerHTML = '<div class="p-3 text-muted">No results found</div>';
        } else {
            this.searchDropdown.innerHTML = results.map(result => `
                <a href="${result.url}" class="d-block p-3 text-decoration-none border-bottom">
                    <div class="fw-semibold">${result.title}</div>
                    <div class="text-muted small">${result.description}</div>
                </a>
            `).join('');
        }

        this.searchDropdown.classList.remove('d-none');
    },

    // Clear search results
    clearSearchResults: function() {
        if (this.searchDropdown) {
            this.searchDropdown.classList.add('d-none');
        }
    },

    // Form enhancements
    initForms: function() {
        // Add loading states to forms
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', (e) => {
                const submitBtn = form.querySelector('[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<span class="loading me-2"></span>Submitting...';
                }
            });
        });

        // Form validation feedback
        document.querySelectorAll('.form-control').forEach(input => {
            input.addEventListener('blur', () => {
                this.validateField(input);
            });
        });
    },

    // Field validation
    validateField: function(field) {
        const feedback = field.parentNode.querySelector('.invalid-feedback');
        if (field.checkValidity()) {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
        } else {
            field.classList.remove('is-valid');
            field.classList.add('is-invalid');
            if (feedback) {
                feedback.textContent = field.validationMessage;
            }
        }
    },

    // Image lazy loading
    initImageLazyLoading: function() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('loading');
                        imageObserver.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                img.classList.add('loading');
                imageObserver.observe(img);
            });
        }
    },

    // Back to top functionality
    initBackToTop: function() {
        const backToTopBtn = document.getElementById('back-to-top');
        if (!backToTopBtn) return;

        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        });

        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    },

    // Lazy loading for content
    initLazyLoading: function() {
        if ('IntersectionObserver' in window) {
            const lazyObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const element = entry.target;
                        element.classList.add('animate-in');
                        lazyObserver.unobserve(element);
                    }
                });
            });

            document.querySelectorAll('.lazy-load').forEach(el => {
                lazyObserver.observe(el);
            });
        }
    },

    // Keyboard navigation
    initKeyboardNavigation: function() {
        // ESC key to close modals/dropdowns
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.clearSearchResults();
                // Close any open modals
                document.querySelectorAll('.modal.show').forEach(modal => {
                    const modalInstance = bootstrap.Modal.getInstance(modal);
                    if (modalInstance) modalInstance.hide();
                });
            }
        });

        // Search shortcut (Ctrl/Cmd + K)
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.querySelector('input[name="q"]');
                if (searchInput) {
                    searchInput.focus();
                    searchInput.select();
                }
            }
        });
    },

    // Touch gestures for mobile
    initTouchGestures: function() {
        // Swipe to navigate in galleries
        document.querySelectorAll('.swipeable').forEach(element => {
            let startX = 0;
            let startY = 0;

            element.addEventListener('touchstart', (e) => {
                startX = e.touches[0].clientX;
                startY = e.touches[0].clientY;
            });

            element.addEventListener('touchend', (e) => {
                const endX = e.changedTouches[0].clientX;
                const endY = e.changedTouches[0].clientY;
                const diffX = startX - endX;
                const diffY = startY - endY;

                // Horizontal swipe (threshold: 50px)
                if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                    if (diffX > 0) {
                        // Swipe left
                        element.dispatchEvent(new CustomEvent('swipeleft'));
                    } else {
                        // Swipe right
                        element.dispatchEvent(new CustomEvent('swiperight'));
                    }
                }
            });
        });
    },

    // Performance monitoring
    initPerformanceMonitoring: function() {
        // Monitor Core Web Vitals
        if ('web-vital' in window) {
            // This would integrate with Web Vitals library if loaded
            return;
        }

        // Basic performance logging
        window.addEventListener('load', () => {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData) {
                console.log('Page Load Time:', perfData.loadEventEnd - perfData.loadEventStart);
            }
        });
    }
};

// Map functionality
window.Monastery360.maps = {
    instances: new Map(),

    // Initialize a Leaflet map
    initMap: function(containerId, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) return null;

        const defaultOptions = {
            center: window.Monastery360.config.mapCenter,
            zoom: window.Monastery360.config.mapZoom,
            scrollWheelZoom: false
        };

        const map = L.map(containerId, { ...defaultOptions, ...options });

        // Add tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        this.instances.set(containerId, map);
        return map;
    },

    // Add monastery markers
    addMonasteryMarkers: async function(mapId, monasteries = null) {
        const map = this.instances.get(mapId);
        if (!map) return;

        try {
            const data = monasteries || await window.Monastery360.utils.api('monasteries/');
            const markers = L.layerGroup();

            data.forEach(monastery => {
                if (monastery.location) {
                    const marker = L.marker([
                        monastery.location.coordinates[1],
                        monastery.location.coordinates[0]
                    ]).bindPopup(`
                        <div class="map-popup">
                            <h6>${monastery.name}</h6>
                            <p class="mb-2">${monastery.location_description}</p>
                            <a href="/monasteries/${monastery.id}/" class="btn btn-primary btn-sm">
                                View Details
                            </a>
                        </div>
                    `);
                    markers.addLayer(marker);
                }
            });

            markers.addTo(map);

            // Fit map to markers
            if (data.length > 0) {
                map.fitBounds(markers.getBounds(), { padding: [20, 20] });
            }
        } catch (error) {
            console.error('Error loading monastery markers:', error);
        }
    },

    // Enable user location
    enableUserLocation: function(mapId) {
        const map = this.instances.get(mapId);
        if (!map) return;

        window.Monastery360.utils.getUserLocation()
            .then(position => {
                const userMarker = L.marker([position.lat, position.lng], {
                    icon: L.icon({
                        iconUrl: '/static/images/user-location.png',
                        iconSize: [25, 25],
                        iconAnchor: [12, 12]
                    })
                }).bindPopup('Your location');

                userMarker.addTo(map);
                map.setView([position.lat, position.lng], 12);
            })
            .catch(error => {
                console.warn('Could not get user location:', error);
            });
    }
};

// Panorama functionality
window.Monastery360.panorama = {
    viewers: new Map(),

    // Initialize Pannellum viewer
    initViewer: function(containerId, config = {}) {
        if (!window.pannellum) {
            console.error('Pannellum not loaded');
            return null;
        }

        const defaultConfig = {
            type: 'equirectangular',
            autoLoad: true,
            compass: true,
            northOffset: 0,
            showControls: true,
            showFullscreenCtrl: true,
            showZoomCtrl: true,
            mouseZoom: true,
            keyboardZoom: true,
            draggable: true
        };

        const viewer = pannellum.viewer(containerId, { ...defaultConfig, ...config });
        this.viewers.set(containerId, viewer);

        return viewer;
    },

    // Add hotspots to panorama
    addHotspots: function(viewerId, hotspots) {
        const viewer = this.viewers.get(viewerId);
        if (!viewer || !hotspots) return;

        hotspots.forEach(hotspot => {
            viewer.addHotSpot({
                id: hotspot.id,
                pitch: hotspot.pitch,
                yaw: hotspot.yaw,
                type: hotspot.type || 'info',
                text: hotspot.text || '',
                URL: hotspot.url || '',
                sceneId: hotspot.sceneId || '',
                clickHandlerFunc: hotspot.clickHandler || null
            });
        });
    }
};

// React Components for dynamic content
window.Monastery360.React = {
    // Monastery List Component
    MonasteryList: function({ monasteries, filters }) {
        const [filteredMonasteries, setFilteredMonasteries] = React.useState(monasteries);
        const [currentPage, setCurrentPage] = React.useState(1);
        const itemsPerPage = 6;

        React.useEffect(() => {
            let filtered = monasteries;

            if (filters.search) {
                filtered = filtered.filter(m =>
                    m.name.toLowerCase().includes(filters.search.toLowerCase()) ||
                    m.description.toLowerCase().includes(filters.search.toLowerCase())
                );
            }

            if (filters.type && filters.type !== 'all') {
                filtered = filtered.filter(m => m.monastery_type === filters.type);
            }

            setFilteredMonasteries(filtered);
            setCurrentPage(1);
        }, [filters, monasteries]);

        const paginatedMonasteries = filteredMonasteries.slice(
            (currentPage - 1) * itemsPerPage,
            currentPage * itemsPerPage
        );

        const totalPages = Math.ceil(filteredMonasteries.length / itemsPerPage);

        return React.createElement('div', { className: 'monastery-react-list' },
            React.createElement('div', { className: 'monastery-grid' },
                paginatedMonasteries.map(monastery =>
                    React.createElement(window.Monastery360.React.MonasteryCard, {
                        key: monastery.id,
                        monastery: monastery
                    })
                )
            ),
            totalPages > 1 && React.createElement(window.Monastery360.React.Pagination, {
                currentPage: currentPage,
                totalPages: totalPages,
                onPageChange: setCurrentPage
            })
        );
    },

    // Monastery Card Component
    MonasteryCard: function({ monastery }) {
        return React.createElement('div', { className: 'monastery-card' },
            React.createElement('div', {
                className: 'monastery-image',
                style: { backgroundImage: `url(${monastery.main_image || '/static/images/monastery-placeholder.jpg'})` }
            }),
            React.createElement('div', { className: 'monastery-content' },
                React.createElement('h3', { className: 'monastery-title' }, monastery.name),
                React.createElement('p', { className: 'monastery-location' },
                    React.createElement('i', { className: 'fas fa-map-marker-alt me-1' }),
                    monastery.location_description
                ),
                React.createElement('p', { className: 'monastery-description' },
                    monastery.description.substring(0, 150) + '...'
                ),
                React.createElement('div', { className: 'monastery-meta' },
                    React.createElement('span', null,
                        React.createElement('i', { className: 'fas fa-calendar me-1' }),
                        `Est. ${monastery.established_year || 'Unknown'}`
                    ),
                    React.createElement('span', null,
                        React.createElement('i', { className: 'fas fa-user me-1' }),
                        `${monastery.monk_count || 0} monks`
                    )
                ),
                React.createElement('div', { className: 'monastery-actions' },
                    React.createElement('a', {
                        href: `/monasteries/${monastery.id}/`,
                        className: 'btn btn-primary btn-sm'
                    }, 'View Details'),
                    monastery.has_virtual_tour && React.createElement('a', {
                        href: `/tours/monastery/${monastery.id}/`,
                        className: 'btn btn-outline-primary btn-sm'
                    }, 'Virtual Tour')
                )
            )
        );
    },

    // Pagination Component
    Pagination: function({ currentPage, totalPages, onPageChange }) {
        const pages = Array.from({ length: totalPages }, (_, i) => i + 1);

        return React.createElement('nav', { className: 'mt-4' },
            React.createElement('ul', { className: 'pagination justify-content-center' },
                React.createElement('li', {
                    className: `page-item ${currentPage === 1 ? 'disabled' : ''}`
                },
                    React.createElement('button', {
                        className: 'page-link',
                        onClick: () => currentPage > 1 && onPageChange(currentPage - 1)
                    }, 'Previous')
                ),
                pages.map(page =>
                    React.createElement('li', {
                        key: page,
                        className: `page-item ${currentPage === page ? 'active' : ''}`
                    },
                        React.createElement('button', {
                            className: 'page-link',
                            onClick: () => onPageChange(page)
                        }, page)
                    )
                ),
                React.createElement('li', {
                    className: `page-item ${currentPage === totalPages ? 'disabled' : ''}`
                },
                    React.createElement('button', {
                        className: 'page-link',
                        onClick: () => currentPage < totalPages && onPageChange(currentPage + 1)
                    }, 'Next')
                )
            )
        );
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.Monastery360.init();
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = window.Monastery360;
}
