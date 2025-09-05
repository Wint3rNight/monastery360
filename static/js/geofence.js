/**
 * Monastery360 - Geofencing and Location Services
 * Handles location-based features, proximity detection, and location context
 */

window.Monastery360.geofence = {
    // Configuration
    config: {
        proximityRadius: 100, // meters
        updateInterval: 30000, // 30 seconds
        enableBackground: false,
        maxAccuracy: 50 // meters
    },

    // State
    state: {
        isTracking: false,
        currentPosition: null,
        watchId: null,
        nearbyMonasteries: [],
        activeGeofences: new Map()
    },

    // Initialize geofencing
    init: function() {
        this.checkPermissions();
        this.bindEvents();

        // Start tracking if permission granted
        if (this.hasPermission()) {
            this.startTracking();
        }
    },

    // Check location permissions
    checkPermissions: function() {
        if (!navigator.geolocation) {
            console.warn('Geolocation not supported');
            return false;
        }

        if ('permissions' in navigator) {
            navigator.permissions.query({ name: 'geolocation' })
                .then(result => {
                    console.log('Geolocation permission:', result.state);
                    if (result.state === 'granted') {
                        this.startTracking();
                    } else if (result.state === 'prompt') {
                        this.requestPermission();
                    }
                });
        }

        return true;
    },

    // Request location permission
    requestPermission: function() {
        const modal = this.createPermissionModal();
        document.body.appendChild(modal);

        const modalInstance = new bootstrap.Modal(modal);
        modalInstance.show();

        modal.querySelector('.btn-primary').addEventListener('click', () => {
            modalInstance.hide();
            this.startTracking();
        });

        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    },

    // Create permission request modal
    createPermissionModal: function() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-map-marker-alt me-2"></i>
                            Location Access
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>Monastery360 would like to access your location to:</p>
                        <ul class="list-unstyled">
                            <li><i class="fas fa-check text-success me-2"></i>Show nearby monasteries</li>
                            <li><i class="fas fa-check text-success me-2"></i>Provide audio guides when you visit</li>
                            <li><i class="fas fa-check text-success me-2"></i>Enhance your virtual tour experience</li>
                            <li><i class="fas fa-check text-success me-2"></i>Suggest relevant events and activities</li>
                        </ul>
                        <p class="text-muted small">Your location data is never stored or shared.</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Not Now</button>
                        <button type="button" class="btn btn-primary">Allow Location</button>
                    </div>
                </div>
            </div>
        `;
        return modal;
    },

    // Check if has permission
    hasPermission: function() {
        return navigator.geolocation &&
               (!('permissions' in navigator) ||
                localStorage.getItem('geolocation-permitted') === 'true');
    },

    // Start location tracking
    startTracking: function() {
        if (this.state.isTracking) return;

        const options = {
            enableHighAccuracy: true,
            timeout: 15000,
            maximumAge: this.config.updateInterval
        };

        this.state.watchId = navigator.geolocation.watchPosition(
            (position) => this.onPositionUpdate(position),
            (error) => this.onPositionError(error),
            options
        );

        this.state.isTracking = true;
        localStorage.setItem('geolocation-permitted', 'true');

        console.log('Geofencing started');
        this.loadMonasteryGeofences();
    },

    // Stop location tracking
    stopTracking: function() {
        if (this.state.watchId) {
            navigator.geolocation.clearWatch(this.state.watchId);
            this.state.watchId = null;
        }

        this.state.isTracking = false;
        this.state.activeGeofences.clear();

        console.log('Geofencing stopped');
    },

    // Handle position updates
    onPositionUpdate: function(position) {
        const newPosition = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
            accuracy: position.coords.accuracy,
            timestamp: Date.now()
        };

        // Ignore low accuracy readings
        if (newPosition.accuracy > this.config.maxAccuracy) {
            return;
        }

        const previousPosition = this.state.currentPosition;
        this.state.currentPosition = newPosition;

        // Check for significant movement
        if (previousPosition && this.calculateDistance(previousPosition, newPosition) < 10) {
            return; // Less than 10 meters, ignore
        }

        // Update geofences
        this.checkGeofences(newPosition);

        // Find nearby monasteries
        this.findNearbyMonasteries(newPosition);

        // Trigger location update event
        this.triggerLocationEvent('positionUpdate', newPosition);
    },

    // Handle position errors
    onPositionError: function(error) {
        console.error('Geolocation error:', error);

        let message = 'Location access failed.';
        switch (error.code) {
            case error.PERMISSION_DENIED:
                message = 'Location access denied by user.';
                this.stopTracking();
                break;
            case error.POSITION_UNAVAILABLE:
                message = 'Location information unavailable.';
                break;
            case error.TIMEOUT:
                message = 'Location request timed out.';
                break;
        }

        this.triggerLocationEvent('positionError', { error, message });
    },

    // Load monastery geofences
    loadMonasteryGeofences: async function() {
        try {
            const monasteries = await window.Monastery360.utils.api('monasteries/');

            monasteries.forEach(monastery => {
                if (monastery.location) {
                    this.addGeofence(monastery.id, {
                        lat: monastery.location.coordinates[1],
                        lng: monastery.location.coordinates[0],
                        radius: this.config.proximityRadius,
                        name: monastery.name,
                        type: 'monastery',
                        data: monastery
                    });
                }
            });

            console.log(`Loaded ${monasteries.length} monastery geofences`);
        } catch (error) {
            console.error('Failed to load monastery geofences:', error);
        }
    },

    // Add geofence
    addGeofence: function(id, geofence) {
        this.state.activeGeofences.set(id, {
            ...geofence,
            isInside: false,
            lastTriggered: null
        });
    },

    // Remove geofence
    removeGeofence: function(id) {
        this.state.activeGeofences.delete(id);
    },

    // Check geofences against current position
    checkGeofences: function(position) {
        this.state.activeGeofences.forEach((geofence, id) => {
            const distance = this.calculateDistance(position, geofence);
            const isInside = distance <= geofence.radius;
            const wasInside = geofence.isInside;

            if (isInside !== wasInside) {
                geofence.isInside = isInside;
                geofence.lastTriggered = Date.now();

                if (isInside) {
                    this.onGeofenceEnter(id, geofence, distance);
                } else {
                    this.onGeofenceExit(id, geofence, distance);
                }
            }
        });
    },

    // Handle geofence entry
    onGeofenceEnter: function(id, geofence, distance) {
        console.log(`Entered geofence: ${geofence.name} (${Math.round(distance)}m)`);

        if (geofence.type === 'monastery') {
            this.handleMonasteryEntry(geofence);
        }

        this.triggerLocationEvent('geofenceEnter', {
            id,
            geofence,
            distance
        });
    },

    // Handle geofence exit
    onGeofenceExit: function(id, geofence, distance) {
        console.log(`Exited geofence: ${geofence.name}`);

        if (geofence.type === 'monastery') {
            this.handleMonasteryExit(geofence);
        }

        this.triggerLocationEvent('geofenceExit', {
            id,
            geofence,
            distance
        });
    },

    // Handle monastery entry
    handleMonasteryEntry: function(geofence) {
        const monastery = geofence.data;

        // Show entry notification
        this.showLocationNotification(
            `Welcome to ${monastery.name}`,
            'Explore the virtual tour and audio guides for this sacred place.',
            `/monasteries/${monastery.id}/`,
            'monastery'
        );

        // Check for available audio guides
        this.checkAudioGuides(monastery);

        // Update visit statistics
        this.recordVisit(monastery.id);
    },

    // Handle monastery exit
    handleMonasteryExit: function(geofence) {
        const monastery = geofence.data;

        // Show exit notification with feedback option
        this.showLocationNotification(
            `Thank you for visiting ${monastery.name}`,
            'Share your experience and help others discover this sacred place.',
            `/monasteries/${monastery.id}/feedback/`,
            'feedback'
        );
    },

    // Show location-based notification
    showLocationNotification: function(title, message, actionUrl = null, type = 'info') {
        // Check if notifications are supported and permitted
        if (!('Notification' in window)) return;

        if (Notification.permission === 'granted') {
            const notification = new Notification(title, {
                body: message,
                icon: '/static/images/monastery360-icon.png',
                badge: '/static/images/monastery360-badge.png',
                tag: `monastery360-${type}`,
                requireInteraction: true
            });

            if (actionUrl) {
                notification.onclick = () => {
                    window.focus();
                    window.location.href = actionUrl;
                    notification.close();
                };
            }
        } else {
            // Fallback to in-app notification
            window.Monastery360.utils.showNotification(
                `<strong>${title}</strong><br>${message}${
                    actionUrl ? `<br><a href="${actionUrl}" class="btn btn-primary btn-sm mt-2">Learn More</a>` : ''
                }`,
                'info'
            );
        }
    },

    // Find nearby monasteries
    findNearbyMonasteries: async function(position) {
        const nearby = [];

        this.state.activeGeofences.forEach((geofence, id) => {
            if (geofence.type === 'monastery') {
                const distance = this.calculateDistance(position, geofence);
                if (distance <= 5000) { // Within 5km
                    nearby.push({
                        id,
                        monastery: geofence.data,
                        distance: Math.round(distance)
                    });
                }
            }
        });

        // Sort by distance
        nearby.sort((a, b) => a.distance - b.distance);
        this.state.nearbyMonasteries = nearby;

        // Update nearby monasteries display
        this.updateNearbyDisplay(nearby);

        this.triggerLocationEvent('nearbyMonasteriesUpdate', nearby);
    },

    // Update nearby monasteries display
    updateNearbyDisplay: function(nearby) {
        const container = document.getElementById('nearby-monasteries');
        if (!container) return;

        if (nearby.length === 0) {
            container.innerHTML = '<p class="text-muted">No monasteries nearby</p>';
            return;
        }

        container.innerHTML = `
            <h6>Nearby Monasteries</h6>
            ${nearby.slice(0, 5).map(item => `
                <div class="nearby-item d-flex justify-content-between align-items-center mb-2">
                    <div>
                        <strong>${item.monastery.name}</strong><br>
                        <small class="text-muted">${item.distance}m away</small>
                    </div>
                    <a href="/monasteries/${item.id}/" class="btn btn-outline-primary btn-sm">View</a>
                </div>
            `).join('')}
        `;
    },

    // Check for available audio guides
    checkAudioGuides: async function(monastery) {
        try {
            const audioPoints = await window.Monastery360.utils.api(
                `monasteries/${monastery.id}/audio-points/`
            );

            if (audioPoints.length > 0) {
                this.showLocationNotification(
                    'Audio Guide Available',
                    `Discover ${audioPoints.length} audio points around ${monastery.name}`,
                    `/monasteries/${monastery.id}/audio/`,
                    'audio'
                );
            }
        } catch (error) {
            console.error('Failed to check audio guides:', error);
        }
    },

    // Record visit for analytics
    recordVisit: function(monasteryId) {
        const visits = JSON.parse(localStorage.getItem('monastery-visits') || '[]');
        visits.push({
            monasteryId,
            timestamp: Date.now(),
            coordinates: this.state.currentPosition
        });

        // Keep only last 100 visits
        if (visits.length > 100) {
            visits.splice(0, visits.length - 100);
        }

        localStorage.setItem('monastery-visits', JSON.stringify(visits));
    },

    // Calculate distance between two points (Haversine formula)
    calculateDistance: function(point1, point2) {
        const R = 6371e3; // Earth's radius in meters
        const φ1 = point1.lat * Math.PI / 180;
        const φ2 = point2.lat * Math.PI / 180;
        const Δφ = (point2.lat - point1.lat) * Math.PI / 180;
        const Δλ = (point2.lng - point1.lng) * Math.PI / 180;

        const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
                  Math.cos(φ1) * Math.cos(φ2) *
                  Math.sin(Δλ/2) * Math.sin(Δλ/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

        return R * c;
    },

    // Get current position
    getCurrentPosition: function() {
        return this.state.currentPosition;
    },

    // Get nearby monasteries
    getNearbyMonasteries: function() {
        return this.state.nearbyMonasteries;
    },

    // Check if inside any monastery
    isInsideMonastery: function() {
        for (let [id, geofence] of this.state.activeGeofences) {
            if (geofence.type === 'monastery' && geofence.isInside) {
                return { id, monastery: geofence.data };
            }
        }
        return null;
    },

    // Bind event listeners
    bindEvents: function() {
        // Request notification permission on first user interaction
        document.addEventListener('click', this.requestNotificationPermission, { once: true });

        // Handle page visibility changes
        document.addEventListener('visibilitychange', () => {
            if (document.hidden && !this.config.enableBackground) {
                this.pauseTracking();
            } else if (!document.hidden && this.hasPermission()) {
                this.resumeTracking();
            }
        });

        // Handle online/offline status
        window.addEventListener('online', () => {
            if (this.hasPermission()) {
                this.resumeTracking();
            }
        });

        window.addEventListener('offline', () => {
            this.pauseTracking();
        });
    },

    // Request notification permission
    requestNotificationPermission: function() {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission().then(permission => {
                console.log('Notification permission:', permission);
            });
        }
    },

    // Pause tracking
    pauseTracking: function() {
        if (this.state.watchId) {
            navigator.geolocation.clearWatch(this.state.watchId);
            this.state.watchId = null;
        }
    },

    // Resume tracking
    resumeTracking: function() {
        if (!this.state.watchId && this.state.isTracking) {
            this.startTracking();
        }
    },

    // Trigger custom location events
    triggerLocationEvent: function(type, data) {
        const event = new CustomEvent(`monastery360:${type}`, {
            detail: data
        });
        document.dispatchEvent(event);
    },

    // Get visit history
    getVisitHistory: function() {
        return JSON.parse(localStorage.getItem('monastery-visits') || '[]');
    },

    // Clear visit history
    clearVisitHistory: function() {
        localStorage.removeItem('monastery-visits');
    },

    // Export location data
    exportLocationData: function() {
        return {
            currentPosition: this.state.currentPosition,
            nearbyMonasteries: this.state.nearbyMonasteries,
            visitHistory: this.getVisitHistory(),
            isTracking: this.state.isTracking
        };
    }
};

// Auto-initialize if geolocation is available
document.addEventListener('DOMContentLoaded', function() {
    if ('geolocation' in navigator) {
        window.Monastery360.geofence.init();
    }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = window.Monastery360.geofence;
}
