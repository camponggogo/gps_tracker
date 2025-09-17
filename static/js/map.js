// GPS Area Tracking Map Application
class GPSTrackingMap {
    constructor() {
        this.map = null;
        this.vehicleMarkers = new Map();
        this.areaLayers = new Map();
        this.routeLayers = new Map();
        this.drawControl = null;
        this.currentVehicle = null;
        this.showAreas = true;
        this.showRoutes = true;
        this.refreshInterval = null;
        
        this.init();
    }
    
    init() {
        this.initMap();
        this.initEventListeners();
        this.loadInitialData();
        this.startAutoRefresh();
    }
    
    initMap() {
        // Initialize map centered on Thailand
        this.map = L.map('map').setView([13.7563, 100.5018], 10);
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(this.map);
        
        // Initialize draw control
        this.initDrawControl();
    }
    
    initDrawControl() {
        const drawnItems = new L.FeatureGroup();
        this.map.addLayer(drawnItems);
        
        this.drawControl = new L.Control.Draw({
            edit: {
                featureGroup: drawnItems,
                remove: true
            },
            draw: {
                polygon: {
                    allowIntersection: false,
                    showArea: true,
                    drawError: {
                        color: '#e1e100',
                        message: '<strong>Error:</strong> Shape edges cannot cross!'
                    },
                    shapeOptions: {
                        color: '#667eea',
                        fillColor: '#667eea',
                        fillOpacity: 0.3
                    }
                },
                rectangle: {
                    shapeOptions: {
                        color: '#667eea',
                        fillColor: '#667eea',
                        fillOpacity: 0.3
                    }
                },
                circle: {
                    shapeOptions: {
                        color: '#667eea',
                        fillColor: '#667eea',
                        fillOpacity: 0.3
                    }
                },
                marker: false,
                polyline: false,
                circlemarker: false
            }
        });
        
        this.map.addControl(this.drawControl);
        
        // Handle draw events
        this.map.on(L.Draw.Event.CREATED, (event) => {
            const layer = event.layer;
            drawnItems.addLayer(layer);
            this.showAreaCreationModal(layer);
        });
    }
    
    initEventListeners() {
        // Header controls
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.refreshData();
        });
        
        document.getElementById('toggleAreasBtn').addEventListener('click', () => {
            this.toggleAreas();
        });
        
        document.getElementById('toggleRoutesBtn').addEventListener('click', () => {
            this.toggleRoutes();
        });
        
        // Area management
        document.getElementById('addAreaBtn').addEventListener('click', () => {
            this.showAreaCreationModal();
        });
        
        document.getElementById('closeAreaModal').addEventListener('click', () => {
            this.hideAreaModal();
        });
        
        document.getElementById('cancelAreaModal').addEventListener('click', () => {
            this.hideAreaModal();
        });
        
        document.getElementById('areaForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.createArea();
        });
        
        // Vehicle info panel
        document.getElementById('closeVehicleInfo').addEventListener('click', () => {
            this.hideVehicleInfo();
        });
        
        // Modal click outside to close
        document.getElementById('areaModal').addEventListener('click', (e) => {
            if (e.target.id === 'areaModal') {
                this.hideAreaModal();
            }
        });
    }
    
    async loadInitialData() {
        try {
            await Promise.all([
                this.loadVehicleLocations(),
                this.loadAreas(),
                this.loadAlerts(),
                this.loadDashboardStats()
            ]);
        } catch (error) {
            console.error('Error loading initial data:', error);
            this.showNotification('Error loading data', 'error');
        }
    }
    
    async loadVehicleLocations() {
        try {
            const response = await fetch('/api/dashboard/vehicle-locations');
            const locations = await response.json();
            
            this.updateVehicleMarkers(locations);
        } catch (error) {
            console.error('Error loading vehicle locations:', error);
        }
    }
    
    async loadAreas() {
        try {
            const response = await fetch('/api/areas/');
            const data = await response.json();
            
            this.updateAreaLayers(data.items);
            this.updateAreaList(data.items);
        } catch (error) {
            console.error('Error loading areas:', error);
        }
    }
    
    async loadAlerts() {
        try {
            const response = await fetch('/api/dashboard/alerts?limit=10');
            const alerts = await response.json();
            
            this.updateAlertsList(alerts);
        } catch (error) {
            console.error('Error loading alerts:', error);
        }
    }
    
    async loadDashboardStats() {
        try {
            const response = await fetch('/api/dashboard/stats');
            const stats = await response.json();
            
            this.updateDashboardStats(stats);
        } catch (error) {
            console.error('Error loading dashboard stats:', error);
        }
    }
    
    updateVehicleMarkers(locations) {
        // Clear existing markers
        this.vehicleMarkers.forEach(marker => {
            this.map.removeLayer(marker);
        });
        this.vehicleMarkers.clear();
        
        // Add new markers
        locations.forEach(location => {
            const marker = this.createVehicleMarker(location);
            this.vehicleMarkers.set(location.vehicle_id, marker);
        });
    }
    
    createVehicleMarker(location) {
        const status = location.status.toLowerCase();
        const isIdle = location.is_idle;
        
        let iconClass = 'vehicle-marker';
        if (isIdle) {
            iconClass += ' idle';
        } else {
            iconClass += ` ${status}`;
        }
        
        const icon = L.divIcon({
            className: iconClass,
            html: `<div style="width: 20px; height: 20px; border-radius: 50%; background: inherit; border: 3px solid white; box-shadow: 0 2px 10px rgba(0,0,0,0.3);"></div>`,
            iconSize: [26, 26],
            iconAnchor: [13, 13]
        });
        
        const marker = L.marker([location.latitude, location.longitude], { icon })
            .addTo(this.map);
        
        // Add popup
        const popupContent = this.createVehiclePopup(location);
        marker.bindPopup(popupContent);
        
        // Add click event
        marker.on('click', () => {
            this.showVehicleInfo(location);
        });
        
        return marker;
    }
    
    createVehiclePopup(location) {
        const speed = location.speed ? `${location.speed.toFixed(1)} km/h` : 'N/A';
        const heading = location.heading ? `${location.heading.toFixed(0)}°` : 'N/A';
        const timestamp = new Date(location.timestamp).toLocaleString('th-TH');
        
        return `
            <div class="vehicle-popup">
                <h4>${location.vehicle_id}</h4>
                <p><strong>Status:</strong> ${location.status}</p>
                <p><strong>Speed:</strong> ${speed}</p>
                <p><strong>Heading:</strong> ${heading}</p>
                <p><strong>Idle:</strong> ${location.is_idle ? 'Yes' : 'No'}</p>
                <p><strong>Last Update:</strong> ${timestamp}</p>
            </div>
        `;
    }
    
    updateAreaLayers(areas) {
        // Clear existing area layers
        this.areaLayers.forEach(layer => {
            this.map.removeLayer(layer);
        });
        this.areaLayers.clear();
        
        if (!this.showAreas) return;
        
        // Add new area layers
        areas.forEach(area => {
            const layer = this.createAreaLayer(area);
            this.areaLayers.set(area.id, layer);
        });
    }
    
    createAreaLayer(area) {
        let layer;
        const coordinates = area.coordinates;
        
        switch (area.shape) {
            case 'polygon':
                const polygonCoords = coordinates.points.map(point => [point.lat, point.lng]);
                layer = L.polygon(polygonCoords, {
                    color: this.getAreaColor(area.area_type),
                    fillColor: this.getAreaColor(area.area_type),
                    fillOpacity: 0.3,
                    weight: 2
                });
                break;
                
            case 'circle':
                const center = [coordinates.center.lat, coordinates.center.lng];
                layer = L.circle(center, {
                    radius: coordinates.radius,
                    color: this.getAreaColor(area.area_type),
                    fillColor: this.getAreaColor(area.area_type),
                    fillOpacity: 0.3,
                    weight: 2
                });
                break;
                
            case 'rectangle':
                const bounds = [
                    [coordinates.bounds.south, coordinates.bounds.west],
                    [coordinates.bounds.north, coordinates.bounds.east]
                ];
                layer = L.rectangle(bounds, {
                    color: this.getAreaColor(area.area_type),
                    fillColor: this.getAreaColor(area.area_type),
                    fillOpacity: 0.3,
                    weight: 2
                });
                break;
        }
        
        if (layer) {
            layer.addTo(this.map);
            
            // Add popup
            const popupContent = this.createAreaPopup(area);
            layer.bindPopup(popupContent);
        }
        
        return layer;
    }
    
    getAreaColor(areaType) {
        const colors = {
            'entrance': '#007bff',
            'alert': '#ffc107',
            'critical': '#dc3545',
            'checkpoint': '#6f42c1'
        };
        return colors[areaType] || '#667eea';
    }
    
    createAreaPopup(area) {
        return `
            <div class="area-popup">
                <h4>${area.name}</h4>
                <p><strong>Type:</strong> ${area.area_type}</p>
                <p><strong>Shape:</strong> ${area.shape}</p>
                <p><strong>Buffer:</strong> ${area.buffer_distance}m</p>
                <p><strong>Status:</strong> ${area.is_active ? 'Active' : 'Inactive'}</p>
            </div>
        `;
    }
    
    updateAreaList(areas) {
        const areaList = document.getElementById('areaList');
        areaList.innerHTML = '';
        
        areas.forEach(area => {
            const areaItem = document.createElement('div');
            areaItem.className = `area-item ${area.area_type}`;
            areaItem.innerHTML = `
                <div class="area-name">${area.name}</div>
                <div class="area-type">${area.area_type}</div>
            `;
            
            areaItem.addEventListener('click', () => {
                this.focusOnArea(area);
            });
            
            areaList.appendChild(areaItem);
        });
    }
    
    updateAlertsList(alerts) {
        const alertsList = document.getElementById('alertsList');
        alertsList.innerHTML = '';
        
        alerts.forEach(alert => {
            const alertItem = document.createElement('div');
            alertItem.className = `alert-item ${alert.is_resolved ? 'resolved' : ''}`;
            alertItem.innerHTML = `
                <div class="alert-message">${alert.message}</div>
                <div class="alert-time">${new Date(alert.created_at).toLocaleString('th-TH')}</div>
            `;
            
            alertsList.appendChild(alertItem);
        });
    }
    
    updateDashboardStats(stats) {
        document.getElementById('totalVehicles').textContent = stats.total_vehicles;
        document.getElementById('activeVehicles').textContent = stats.active_vehicles;
        document.getElementById('idleVehicles').textContent = stats.vehicles_in_checkpoint;
    }
    
    showVehicleInfo(location) {
        const vehicleInfo = document.getElementById('vehicleInfo');
        const vehicleInfoTitle = document.getElementById('vehicleInfoTitle');
        const vehicleInfoContent = document.getElementById('vehicleInfoContent');
        
        vehicleInfoTitle.textContent = `Vehicle: ${location.vehicle_id}`;
        
        const speed = location.speed ? `${location.speed.toFixed(1)} km/h` : 'N/A';
        const heading = location.heading ? `${location.heading.toFixed(0)}°` : 'N/A';
        const timestamp = new Date(location.timestamp).toLocaleString('th-TH');
        
        vehicleInfoContent.innerHTML = `
            <div class="info-item">
                <div class="info-label">Status</div>
                <div class="info-value">${location.status}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Speed</div>
                <div class="info-value">${speed}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Heading</div>
                <div class="info-value">${heading}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Idle</div>
                <div class="info-value">${location.is_idle ? 'Yes' : 'No'}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Last Update</div>
                <div class="info-value">${timestamp}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Coordinates</div>
                <div class="info-value">${location.latitude.toFixed(6)}, ${location.longitude.toFixed(6)}</div>
            </div>
        `;
        
        vehicleInfo.style.display = 'block';
        this.currentVehicle = location;
    }
    
    hideVehicleInfo() {
        document.getElementById('vehicleInfo').style.display = 'none';
        this.currentVehicle = null;
    }
    
    showAreaCreationModal(layer = null) {
        const modal = document.getElementById('areaModal');
        modal.style.display = 'flex';
        
        if (layer) {
            // Store the drawn layer for area creation
            this.drawnLayer = layer;
        }
    }
    
    hideAreaModal() {
        document.getElementById('areaModal').style.display = 'none';
        document.getElementById('areaForm').reset();
        this.drawnLayer = null;
    }
    
    async createArea() {
        try {
            const formData = new FormData(document.getElementById('areaForm'));
            const areaData = {
                name: formData.get('areaName') || document.getElementById('areaName').value,
                area_type: document.getElementById('areaType').value,
                shape: document.getElementById('areaShape').value,
                buffer_distance: parseFloat(document.getElementById('bufferDistance').value) || 0
            };
            
            // Extract coordinates from drawn layer
            if (this.drawnLayer) {
                areaData.coordinates = this.extractCoordinatesFromLayer(this.drawnLayer, areaData.shape);
            } else {
                throw new Error('No area drawn on map');
            }
            
            const response = await fetch('/api/areas/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(areaData)
            });
            
            if (response.ok) {
                this.showNotification('Area created successfully', 'success');
                this.hideAreaModal();
                this.loadAreas(); // Reload areas
            } else {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to create area');
            }
        } catch (error) {
            console.error('Error creating area:', error);
            this.showNotification(`Error creating area: ${error.message}`, 'error');
        }
    }
    
    extractCoordinatesFromLayer(layer, shape) {
        if (shape === 'polygon' && layer instanceof L.Polygon) {
            const latLngs = layer.getLatLngs()[0];
            return {
                points: latLngs.map(latLng => ({
                    lat: latLng.lat,
                    lng: latLng.lng
                }))
            };
        } else if (shape === 'circle' && layer instanceof L.Circle) {
            const center = layer.getLatLng();
            return {
                center: {
                    lat: center.lat,
                    lng: center.lng
                },
                radius: layer.getRadius()
            };
        } else if (shape === 'rectangle' && layer instanceof L.Rectangle) {
            const bounds = layer.getBounds();
            return {
                bounds: {
                    north: bounds.getNorth(),
                    south: bounds.getSouth(),
                    east: bounds.getEast(),
                    west: bounds.getWest()
                }
            };
        }
        
        throw new Error('Invalid layer type for shape');
    }
    
    focusOnArea(area) {
        // Focus map on the area
        if (area.shape === 'circle') {
            const center = area.coordinates.center;
            this.map.setView([center.lat, center.lng], 15);
        } else if (area.shape === 'rectangle') {
            const bounds = area.coordinates.bounds;
            const boundsArray = [
                [bounds.south, bounds.west],
                [bounds.north, bounds.east]
            ];
            this.map.fitBounds(boundsArray);
        } else if (area.shape === 'polygon') {
            const points = area.coordinates.points;
            const bounds = L.latLngBounds(points.map(p => [p.lat, p.lng]));
            this.map.fitBounds(bounds);
        }
    }
    
    toggleAreas() {
        this.showAreas = !this.showAreas;
        
        this.areaLayers.forEach(layer => {
            if (this.showAreas) {
                this.map.addLayer(layer);
            } else {
                this.map.removeLayer(layer);
            }
        });
        
        const btn = document.getElementById('toggleAreasBtn');
        btn.textContent = this.showAreas ? 'Hide Areas' : 'Show Areas';
    }
    
    toggleRoutes() {
        this.showRoutes = !this.showRoutes;
        
        this.routeLayers.forEach(layer => {
            if (this.showRoutes) {
                this.map.addLayer(layer);
            } else {
                this.map.removeLayer(layer);
            }
        });
        
        const btn = document.getElementById('toggleRoutesBtn');
        btn.textContent = this.showRoutes ? 'Hide Routes' : 'Show Routes';
    }
    
    async refreshData() {
        try {
            await this.loadInitialData();
            this.showNotification('Data refreshed', 'success');
        } catch (error) {
            console.error('Error refreshing data:', error);
            this.showNotification('Error refreshing data', 'error');
        }
    }
    
    startAutoRefresh() {
        // Refresh data every 30 seconds
        this.refreshInterval = setInterval(() => {
            this.loadVehicleLocations();
            this.loadAlerts();
            this.loadDashboardStats();
        }, 30000);
    }
    
    showNotification(message, type = 'info') {
        // Simple notification system
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 4px;
            color: white;
            font-weight: 500;
            z-index: 3000;
            animation: slideIn 0.3s ease;
        `;
        
        if (type === 'success') {
            notification.style.background = '#28a745';
        } else if (type === 'error') {
            notification.style.background = '#dc3545';
        } else {
            notification.style.background = '#667eea';
        }
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new GPSTrackingMap();
});

// Add CSS animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
