# User Guide: Tirunelveli Public Transport Intelligence Platform (Nellai Transit)

## 1. Getting Started

### Launching the Platform on Windows
1. Double-click `run.bat` or run in PowerShell:
   ```cmd
   .\run.bat
   ```
2. Your default web browser will open at `http://localhost:8501`.

### Operational Mode Selection
At the top of the screen in the header bar, you can toggle between:
- **Production Mode (Verified Timetables)**: Real-world operational baseline. All arrivals and tracking records are marked as `[SCHEDULED]` or `[STATIC]` timetables, with zero synthetic GPS coordinates.
- **Demonstration Mode (Simulated GPS)**: Evaluator mode with simulated live movement and progress animations, clearly identified by a prominent yellow warning banner.

---

## 2. Navigating the 6 Clean Tabs

The platform features an uncluttered civic-technology interface designed for everyday commuters and transit planners:

### Tab 1: 🚏 Find a Bus
- **Find by Stop**: Search any bus stop by English or Tamil name (e.g. *Junction*, *Palayamkottai*, *நெல்லை சந்திப்பு*). Displays all passing routes, terminal stops, and frequencies.
- **Find by Proximity / Landmark**: Pick a well-known Tirunelveli landmark (e.g., *Anna Stadium*, *Vannarpettai*, *Nellaiyappar Temple*) or use GPS coordinates to discover nearest stops within walking distance, sorted by distance in meters.
- **Filter by Route**: Select an origin and destination to list matching direct bus routes.

---

### Tab 2: 🚌 Track a Bus (TNSTC Nellai)
- **Select Bus**: Choose from authentic TNSTC city and regional routes:
  - `TNSTC Route 1 (TN-72-N-1042)`: Veinthaankulam New Bus Stand ↔ Tirunelveli Junction
  - `TNSTC Route 2 (TN-72-N-2104)`: Junction ↔ Town Nellaiyappar Temple
  - `TNSTC Route 3 (TN-72-N-3011)`: Junction ↔ Palayamkottai Market
  - `TNSTC Route 10 (TN-72-N-1090)`: Town Nellaiyappar ↔ High Ground Medical College
  - `TNSTC Route 41 (TN-72-N-4105)`: Junction ↔ Cheranmahadevi & Ambasamudram
  - `TNSTC Route 144 (TN-72-N-1442)`: New Bus Stand ↔ Nanguneri & Valliyur
- **Live Status Card**: Instantly see honest data freshness, on-time status, approaching next stop, expected arrival time, vehicle speed, and delay in minutes.
- **Stop-by-Stop Route Timeline**: Passed stops appear in green, current approaching stop in amber with ETA, and upcoming stops with arrival projections.
- **Route Map**: Displays an interactive Leaflet route map showing current vehicle location and stop markers.

---

### Tab 3: 🚆 Find a Train (Southern Railway)
- **Search by Train Number**: Enter any 5-digit Indian Railways train number (e.g., `12632`, `20666`, `06682`, `06685`).
- **Geographic Eligibility Enforcement**:
  - For trains serving Tirunelveli Hub (e.g., `12632 Nellai Superfast Express`), view assigned platform at Tirunelveli Junction, current location, delay variance, and full halt timetable.
  - If a user enters a valid train that does not operate in Tirunelveli (e.g., `12621 Tamil Nadu Express`), the platform clearly informs the user that the train runs between New Delhi and Chennai and does not serve Tirunelveli, preventing confusion.

---

### Tab 4: 🗺️ Tirunelveli Map
- **Interactive District Map**: Leaflet map centered at Tirunelveli (`[8.7285, 77.7050]`).
- **Geographic Context**: View the Thamirabarani River, transit corridors, station nodes, and live vehicle positions.
- **Mode Filter**: Toggle between viewing All Vehicles, Buses Only, or Trains Only.

---

### Tab 5: 📋 Station Departure Board
- **Choose Station**: Select from major transit stations:
  - Tirunelveli Junction (TEN)
  - New Bus Stand Veinthaankulam (VBS)
  - Palayamkottai Market (PLM)
  - Town Nellaiyappar Temple (TOWN)
  - Ambasamudram (ASD)
  - Tenkasi Junction (TSI)
- **Departure Table**: View upcoming departures, vehicle/train numbers, platforms, scheduled arrival times, delay variance, and real-time status.

---

### Tab 6: 📊 Network Analytics
- **Executive KPIs**: Monitored Trips, On-Time Arrival Rate (≤ 2 mins), Fleet Average Delay, and Transit Reliability Index (TRI).
- **30-Day Delay Trend**: Daily average delay compared against a 7-day moving average.
- **Delay Root Causes**: Breakdown of delay causes across Traffic Congestion, Railway Crossing, Peak Dwell Time, Signal Clearance, and Passenger Rush.
