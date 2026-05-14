class MotionFilter {
    constructor() {
        this.lat = null;
        this.lon = null;
        this.vLat = 0;
        this.vLon = 0;
        this.posGain = 0.45;
        this.velGain = 0.15;
        this.damping = 0.80;
    }

    reset() {
        this.lat = null;
        this.lon = null;
        this.vLat = 0;
        this.vLon = 0;
    }

    update(lat, lon, acc) {
        if (this.lat === null) {
            this.lat = lat;
            this.lon = lon;
            return [lat, lon];
        }

        if (acc < 10) this.posGain = 0.6;
        else if (acc < 25) this.posGain = 0.4;
        else if (acc < 50) this.posGain = 0.2;
        else this.posGain = 0.1;

        let pLat = this.lat + this.vLat;
        let pLon = this.lon + this.vLon;

        let rLat = lat - pLat;
        let rLon = lon - pLon;

        this.lat += this.posGain * rLat;
        this.lon += this.posGain * rLon;

        this.vLat += this.velGain * rLat;
        this.vLon += this.velGain * rLon;

        this.vLat *= this.damping;
        this.vLon *= this.damping;

        return [this.lat, this.lon];
    }
}

const motionFilter = new MotionFilter();

// ─── Config ───
const API_BASE = 'https://abdicative-karsyn-nonamphibian.ngrok-free.dev';
const DEVICE_ID = 'android-' + getOrCreateId();

// ─── State ───
let map, marker, polyline;
let isTracking = false;
let watchId = null;
let bgWatcherId = null;
let pointsSent = 0;
let devicePk = null;
let trackPoints = [];
let mapReady = false;

function getOrCreateId() {
    let id = localStorage.getItem('device_uuid');
    if (!id) {
        id = Date.now().toString(36) + Math.random().toString(36).substr(2, 6);
        localStorage.setItem('device_uuid', id);
    }
    return id;
}

// ─── Step 1: Init map ───
function initMap() {
    const defaultPos = { lat: 20.5937, lng: 78.9629 };

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 5,
        center: defaultPos,
        disableDefaultUI: true,
        zoomControl: true,
        mapTypeId: 'roadmap'
    });

    marker = new google.maps.Marker({
        position: defaultPos,
        map: map,
        visible: false,
        icon: {
            path: google.maps.SymbolPath.CIRCLE,
            fillColor: '#3b82f6',
            fillOpacity: 1,
            strokeColor: '#ffffff',
            strokeWeight: 3,
            scale: 10
        }
    });

    polyline = new google.maps.Polyline({
        path: [],
        geodesic: true,
        strokeColor: '#3b82f6',
        strokeOpacity: 0.9,
        strokeWeight: 5,
        map: map
    });

    mapReady = true;

    // FORCE LOAD: Get approximate location immediately via WiFi/Cell (No timeout)
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                console.log("SUCCESS:", pos);
                showToast("✅ Location received");
                moveMarker(pos.coords.latitude, pos.coords.longitude, 0, false);
            },
            (err) => {
                console.log("ERROR:", err.code, err.message);

                if (err.code === 3) {
                    showToast("🛰️ Trying alternate location...");

                    // TRY AGAIN with LOW accuracy + cached data
                    navigator.geolocation.getCurrentPosition(
                        (pos) => {
                            console.log("FALLBACK SUCCESS:", pos);
                            showToast("✅ Approx location found");
                            moveMarker(pos.coords.latitude, pos.coords.longitude, 0, false);
                        },
                        (err2) => {
                            console.log("FALLBACK FAILED:", err2.message);
                            showToast("❌ Still no location. Turn ON WiFi.");
                        },
                        { enableHighAccuracy: false, timeout: 20000, maximumAge: 300000 }
                    );
                } else {
                    showToast("❌ Error: " + err.message);
                }
            },
            { enableHighAccuracy: false, timeout: 60000 }
        );
    }
}



function moveMarker(lat, lng, speed, addPoint) {
    if (!mapReady) return;
    const pos = { lat, lng };
    marker.setPosition(pos);
    marker.setVisible(true);

    // Smoothly pan to position
    map.panTo(pos);
    if (map.getZoom() < 12) map.setZoom(17);

    document.getElementById('lat-display').textContent = lat.toFixed(6);
    document.getElementById('lon-display').textContent = lng.toFixed(6);
    document.getElementById('speed-display').textContent = (speed * 3.6).toFixed(1) + ' km/h';

    if (addPoint && isTracking) {
        trackPoints.push(pos);
        polyline.setPath(trackPoints);
    }
}

async function registerDevice() {
    try {
        const res = await fetch(API_BASE + '/api/devices/', { headers: { 'ngrok-skip-browser-warning': 'true' } });
        const devices = await res.json();
        const found = devices.find(d => d.device_id === DEVICE_ID);
        if (found) { devicePk = found.id; return; }

        const reg = await fetch(API_BASE + '/api/devices/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'ngrok-skip-browser-warning': 'true' },
            body: JSON.stringify({ device_id: DEVICE_ID, name: 'OnePlus Tracker' })
        });
        if (reg.ok) { const d = await reg.json(); devicePk = d.id; }
    } catch (e) { console.error('Reg failed'); }
}

async function sendLocation(lat, lng, speed) {
    if (!devicePk) return;
    try {
        await fetch(API_BASE + '/api/locations/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'ngrok-skip-browser-warning': 'true' },
            body: JSON.stringify({ device: devicePk, latitude: lat, longitude: lng, speed: speed || 0 })
        });
        pointsSent++;
        document.getElementById('points-display').textContent = pointsSent;
    } catch (e) { console.error('Send error'); }
}


async function requestLocationPermission() {
    try {
        console.log("Requesting permission...");

        if (navigator.permissions) {
            const result = await navigator.permissions.query({ name: 'geolocation' });
            console.log("Permission state:", result.state);
        }

        navigator.geolocation.getCurrentPosition(
            (pos) => {
                console.log("Permission granted, got position");
            },
            (err) => {
                console.log("Permission error:", err.code, err.message);
            }
        );

    } catch (e) {
        console.log("Permission exception:", e);
    }
}

async function startTracking() {

    console.log("BG Plugin:", window.Capacitor?.Plugins?.BackgroundGeolocation);
    showToast('🔄 Initializing...');

    const BG_new = window.Capacitor?.Plugins?.BackgroundGeolocation;

    if (BG_new) {
        showToast("✅ BG Plugin FOUND");
    } else {
        showToast("❌ BG Plugin NOT FOUND");
    }

    await requestLocationPermission(); // 👈 ADD THIS
    await new Promise(res => setTimeout(res, 2000)); // 👈 ADD THIS

    await registerDevice();

    isTracking = true;
    motionFilter.reset();
    trackPoints = [];

    navigator.geolocation.getCurrentPosition(
        (pos) => {
            console.log("INITIAL SUCCESS:", pos);
            showToast("📍 Initial location found");
            moveMarker(pos.coords.latitude, pos.coords.longitude, 0, false);
        },
        (err) => {
            console.log("INITIAL ERROR:", err.message);
        },
        { enableHighAccuracy: false, maximumAge: 60000, timeout: 10000 }
    );

    pointsSent = 0;
    polyline.setPath([]);

    document.getElementById('track-btn').classList.add('tracking');
    document.getElementById('btn-icon').textContent = '⏹';
    document.getElementById('btn-text').textContent = 'Stop Tracking';
    setStatus('Tracking', 'badge-tracking');

    // Use BOTH Native and Web-view watchers for maximum reliability
    const BG = window.Capacitor?.Plugins?.BackgroundGeolocation;

    if (BG) {
        BG.addWatcher({
            backgroundMessage: 'Tracking movement...',
            backgroundTitle: 'Routehawk Active',
            requestPermissions: true,
            distanceFilter: 0,
            stale: false
        }, (location, error) => {

            if (error) {
                console.log("BG ERROR:", error);
                return;
            }

            if (location) {
                console.log("BG LOCATION:", location);

                const acc = location.accuracy || 50;

                if (acc < 100) {
                    const [fLat, fLon] = motionFilter.update(location.latitude, location.longitude, acc);

                    moveMarker(fLat, fLon, location.speed, true);
                }
                sendLocation(location.latitude, location.longitude, location.speed);
            }

        }).then(id => {
            bgWatcherId = id;
        });
    }

    // Web Fallback (Always run this as well for faster indoor updates)
    watchId = navigator.geolocation.watchPosition(
        (pos) => {
            console.log("WATCH SUCCESS:", pos); // 👈 ADD
            showToast("📍 Got location");       // 👈 ADD

            const lat = pos.coords.latitude;
            const lon = pos.coords.longitude;
            const acc = pos.coords.accuracy || 50;

            // ❌ Ignore garbage GPS
            if (acc > 100) {
                console.log("Ignoring low accuracy:", acc);
                return;
            }

            const [fLat, fLon] = motionFilter.update(lat, lon, acc);

            if (trackPoints.length > 0) {
                const last = trackPoints[trackPoints.length - 1];

                const dist = Math.sqrt(
                    Math.pow(fLat - last.lat, 2) +
                    Math.pow(fLon - last.lng, 2)
                );

                if (dist < 0.00002) {
                    return;
                }
            }

            moveMarker(fLat, fLon, pos.coords.speed, true);
            
            sendLocation(pos.coords.latitude, pos.coords.longitude, pos.coords.speed);
        },
        (err) => {
            console.log("WATCH ERROR:", err.code, err.message);
            showToast("❌ Watch Error: " + err.message);
        },
        { enableHighAccuracy: false, maximumAge: 0, timeout: 20000 }
    );
}

function stopTracking() {
    isTracking = false;
    if (watchId !== null) { navigator.geolocation.clearWatch(watchId); watchId = null; }

    const BG = window.Capacitor?.Plugins?.BackgroundGeolocation;

    if (bgWatcherId !== null && BG) {
        BG.removeWatcher({ id: bgWatcherId });
        bgWatcherId = null;
    }
    document.getElementById('track-btn').classList.remove('tracking');
    document.getElementById('btn-icon').textContent = '▶';
    document.getElementById('btn-text').textContent = 'Start Tracking';
    setStatus('Idle', 'badge-idle');
}

function toggleTracking() {
    if (isTracking) stopTracking(); else startTracking();
}

function setStatus(text, cls) {
    const b = document.getElementById('status-badge');
    b.textContent = text;
    b.className = 'badge ' + cls;
}

function showToast(msg) {
    let t = document.getElementById('toast');
    if (!t) {
        t = document.createElement('div');
        t.id = 'toast';
        t.style.cssText = 'position:fixed;bottom:100px;left:50%;transform:translateX(-50%);background:#1e293b;color:#f1f5f9;padding:10px 20px;border-radius:20px;font-size:0.85rem;z-index:9999;border:1px solid #334155;max-width:88%;text-align:center';
        document.body.appendChild(t);
    }
    t.textContent = msg;
    t.style.display = 'block';
    setTimeout(() => { t.style.display = 'none'; }, 4000);
}

document.addEventListener('DOMContentLoaded', () => { initMap(); });
