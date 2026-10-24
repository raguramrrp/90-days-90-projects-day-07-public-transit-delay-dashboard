# User Guide: Tirunelveli Public Transport Intelligence Platform (Nellai Transit)

## 1. Getting Started

### Launching the Platform on Windows
1. Double-click `run.bat` or run in PowerShell:
   ```cmd
   .\run.bat
   ```
2. Your default web browser will open at `http://localhost:8501`.
3. The platform instantly presents the approved **Google Stitch Civic Utility Workspace (v2.5)** with zero initial lag or startup glows.

### Civic Header & Telemetry Sync Status
Across the top municipal header bar, commuters can inspect:
- **Platform Identity**: `TIRUNELVELI TRANSPORT TRACKER` — Municipal Transit & Rail Division.
- **Data Telemetry Pill**: Displays `TNSTC & SR Live Telemetry: ONLINE (30s sync)` indicating healthy transponder connections.
- **Operational Mode Banner**: Distinguishes verified real-world timetables (`[SCHEDULED]`, `[STATIC]`) from active AIS-140/CRIS NTES telemetry with zero synthetic live GPS deception in production mode.
- **Municipal Help & Settings**: Direct access to local emergency contacts, transport helpline (`1800-425-6151`), and display preferences.

---

## 2. Exploring the 4 Civic Workspace Views

Navigation between views is located directly in the civic navigation header (and on the bottom navigation bar for mobile devices):

```
[ 🚏 Bus Search & Telemetry ]   [ 🚆 Train Search & Status ]   [ 🏢 Station Hubs ]   [ ℹ️ About & Data Feeds ]
```

---

### View 1: 🚏 Bus Search & Live Telemetry
A 2-column split workspace designed for fast, accessible local bus tracking:

#### Left Column (Search & Route Cards)
- **Origin / Destination Input**:
  - Enter stops in English or Tamil (e.g. *Tirunelveli Junction*, *Palayamkottai*, *நெல்லை சந்திப்பு*).
  - Click the **GPS Geolocation Icon** (`my_location`) to automatically detect your nearest bus stop.
  - Click the **Swap Button** (`swap_vert`) to invert departure and arrival locations with a single touch.
- **Quick Terminal Shortcut Chips**:
  - One-tap selection of major transit terminals: `Tirunelveli Junction`, `MGR New Bus Stand`, `Palayamkottai Market`, `Town Nellaiyappar`.
- **Service Tier & Civic Fare Cards**:
  - Inspect authentic TNSTC city and regional routes:
    - `Route 11A (Ordinary)`: Veinthaankulam NBS ↔ High Ground Med College — Fare **₹12** (Crowd: Low 🟢)
    - `Route 1 (Express)`: Junction ↔ New Bus Stand — Fare **₹14** (Crowd: Moderate 🟡)
    - `Route 144 (Deluxe)`: New Bus Stand ↔ Ambasamudram — Fare **₹18** (Crowd: High 🔴)

#### Right Column (Vector SVG Map & Vehicle Inspector)
- **Thamirabarani River Vector Map (SVG)**:
  - Custom vector canvas depicting the path of the Thamirabarani River, transit corridors, and the Sulochana Mudaliar Bridge crossing.
  - **Live Vehicle Radar Beacon**: High-visibility radar dot with radiating pulse displaying live bus `TN-72-N-1842` traversing Sulochana Mudaliar Bridge.
- **Vehicle Telemetry Inspector**:
  - Selected vehicle details: `Route 11A` (`TN-72-N-1842`)
  - Speed: `28 km/h` | Heading: `East (094°)` | Transponder: `AIS-140 Dual-band GNSS`
- **Sequential 5-Stop Progression Timeline**:
  - `Tirunelveli Junction` (Departed on time)
  - `Vannarpettai Bridge` (Passed +1 min)
  - `Murugankurichi Signal` (Approaching in 2 mins — LIVE)
  - `Palayamkottai Bus Stop` (ETA 14:18)
  - `High Ground Medical College` (ETA 14:28)

---

### View 2: 🚆 Train Search & CRIS NTES Live Status
A unified rail intelligence workspace providing real-time Indian Railways status without commercial app clutter:

#### Calling Station Filter & Train Search
- **5-Digit Train Search Input**:
  - Enter any Indian Railways train number (e.g., `16127`, `12632`, `20666`, `06682`, `16847`).
- **Station Scope Selector**:
  - Filter departures and arrivals: `TEN - All Hub Services`, `TYT - Thazhaiyuthu Stoppages`, `PLM - Palayamkottai Passenger`, `ALL - All Stations`.
- **Quick Corridor Buttons**:
  - Instant lookup shortcuts: `16127 Guruvayur Exp`, `12632 Nellai SF`, `20666 Vande Bharat`, `06682 TCN Special`.

#### Geographic Boundary Verification (Out-of-Area Check)
- If a commuter searches a train that does not halt or operate in Tirunelveli (e.g., `12626 Kerala Express` New Delhi ↔ Trivandrum):
  - The platform displays an **Informative Civic Boundary Notice** explaining that the train operates via Kottayam/Ernakulam without entering the Tirunelveli Division, preventing confusion and synthetic stop errors.

#### CRIS NTES Motive Power & Stoppage Inspector
- **Locomotive Motive Power**:
  - Displays authenticated electric/diesel locomotive motive power unit: `WAP-7 ED 37102` (Erode Electric Loco Shed) or `WAP-4 ED`.
- **Real-Time Block Location & Speed**:
  - Speed: `68 km/h` | Position: `Passing Gangaikondan Block Section`
  - Assigned Platform at TEN: **Platform 1** | Delay Variance: **+12 min (Recovering)**
- **8-Halt Progression Timetable**:
  - Full stop-by-stop progression timeline from Madurai Junction through Virudhunagar, Satur, Kovilpatti, Kadambur, Vanchi Maniyachchi, Tirunelveli Junction, to Nagercoil Junction.

---

### View 3: 🏢 Station Hubs & Intermodal Interchanges
Comprehensive multimodal interchange guides for Tirunelveli's key passenger terminals:

- **Hub Selector**: Select between:
  1. `Tirunelveli Central Junction (TEN)`
  2. `MGR New Bus Stand (Veinthaankulam - VBS)`
  3. `Palayamkottai Market Terminal (PLM)`
  4. `Town Nellaiyappar Temple (TOWN)`
- **SVG Terminal Schematics**:
  - Visual floor layout showing railway platforms (PF 1-5), city bus bays, auto-rickshaw prepaid counter, foot overbridges, and waiting lounges.
- **Connecting City Bus Timetable**:
  - Real-time departure board of synchronized TNSTC city feeder buses departing directly outside the station concourse.
- **Immediate Rail Departures**:
  - Digital departure screen showing next train departures, platforms, delays, and destination stations.
- **Prepaid Auto Fixed Tariffs (Tirunelveli Traffic Police)**:
  - Official municipal tariff chart protecting passengers:
    - *Junction ↔ Palayamkottai Market*: **₹70**
    - *Junction ↔ MGR New Bus Stand*: **₹90**
    - *Junction ↔ Town Nellaiyappar*: **₹50**
    - *Junction ↔ Government Medical College*: **₹110**

---

### View 4: ℹ️ About & Data Feeds
Transparency, data provenance, and public safety audit policies:

- **Operational KPI Cards**:
  - **Monitored Trips**: `2,880 active trips` across 10 bus & rail corridors.
  - **On-Time Reliability**: `86.4%` meeting municipal SLA standards.
  - **Average Fleet Delay**: `4.8 minutes`.
- **Data Provenance Hierarchy**:
  - Transparent labeling rules: `LIVE` (GPS active < 60s), `RECENT` (60s-5m), `SCHEDULED` (timetables), `ESTIMATED` (calculated headway), `STATIC` (fixed stop info), `UNAVAILABLE` (offline feed).
- **Public Privacy Safeguards**:
  - User device location coordinates are calculated strictly in-memory for local distance ordering and are never stored in databases, logged to disk, or sent to external ad networks.

---

## 3. Responsive Mobile Usage
On smartphones and tablets:
- The 2-column workspace smoothly wraps into a vertical mobile layout.
- Quick terminal chips scroll horizontally for rapid thumb access.
- A persistent **Bottom Navigation Bar** provides one-touch switching between `Buses`, `Trains`, `Hubs`, and `About`.
