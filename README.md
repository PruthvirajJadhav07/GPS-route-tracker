# RouteHawk: Enterprise GPS & Live Tracking Engine

RouteHawk is a comprehensive, production-ready live GPS route tracking platform. It consists of a robust **Django backend** and a cross-platform **Capacitor frontend** designed for both mobile devices and desktop browsers. Built with a premium glassmorphism UI, RouteHawk leverages the full power of Google Maps APIs to deliver highly accurate, enterprise-grade telematics.

## 🌟 Key Features

### 📍 Core Tracking & Mapping
*   **Google Maps Engine:** Transitioned from Leaflet to a fully integrated Google Maps implementation, featuring a sleek, custom dark mode (`DARK_MAP_STYLE`).
*   **Real-Time Motion Smoothing:** Employs advanced Kalman-style motion filtering and "Drift Anchor" logic to prevent GPS jitter and "drunk-walking" when stationary.
*   **Perfect Road Snapping:** Integrates the Google Roads API to algorithmically snap raw GPS points to the exact center of roads, preventing corner-cutting on turns.
*   **Capacitor Native GPS:** On mobile, utilizes native background geolocation plugins for highly accurate, battery-efficient tracking even when the screen is locked.

### 🌐 Offline-First Architecture
*   **IndexedDB Local Storage:** Drivers can track routes entirely offline (e.g., in remote areas or dead zones). GPS data is cached seamlessly in the browser's IndexedDB.
*   **One-Click Syncing:** When internet is restored, the "Offline Routes" modal allows drivers to sync massive batches of route data directly to the Django backend.

### 🏢 Advanced Telematics & Enterprise Tools
*   **Dynamic Geofencing & Spatial Triggers:** Managers can use the Drawing Manager to create custom polygons on the map. The system actively mathematically checks coordinates against these geometries, triggering instant `Entered Zone` / `Exited Zone` alerts.
*   **Indoor Positioning Systems (IPS):** Tracks the Z-axis (altitude). Converts GPS altitude telemetry into estimated building floor levels (e.g., L1, L2). Includes manual UI overrides for deep indoor environments without barometric pressure.
*   **Anti-Spoofing Security:** Actively detects if a driver is attempting to use a "Mock Location" or fake GPS app, instantly dropping the fake data and silently alerting the admin.
*   **Emergency SOS Protocol:** A persistent SOS button tied to native `tel:` protocols allows drivers to instantly trigger emergency calls with a single tap.

### 🗺️ Navigation & POI
*   **Places & Directions:** Full integration with Google Places and Google Directions API. Search for destinations, render turn-by-turn routes on the map, and track progress relative to the destination.

### 🛡️ Admin Dashboard & History
*   **Live Monitoring:** Superadmins can monitor employee (e.g., drivers, couriers) locations in real-time.
*   **Historical Playback:** Admins can filter by date and employee to instantly reconstruct exact routes driven in the past, viewing total distance, trip duration, and snapped polylines.

---

## 🛠️ Technology Stack

*   **Backend:** Python, Django, SQLite (ready for PostgreSQL transition)
*   **Frontend UI:** Vanilla JavaScript, HTML5, Vanilla CSS (Glassmorphism & Micro-animations)
*   **Mobile Wrapper:** Capacitor JS (iOS / Android)
*   **APIs:** Google Maps (JavaScript API, Roads API, Places API, Directions API, Geometry Library, Drawing Library)
*   **Storage:** IndexedDB (Frontend Cache)

---

## 🚀 Deployment State
*(Current Project Phase)*
RouteHawk has evolved from its initial Leaflet-based MVP into a complete, enterprise-ready architecture. The application is actively in its **Deploy State**, featuring full synchronization between the cross-platform Capacitor mobile client and the centralized Django administration portal.

### Quick Start (Local Dev)
1. Ensure `GOOGLE_MAPS_API_KEY` is configured in your Django settings.
2. Run migrations: `python manage.py migrate`
3. Start the server: `python manage.py runserver`
4. Access the tracker at `http://127.0.0.1:8000/` and the admin panel at `http://127.0.0.1:8000/admin/`.
