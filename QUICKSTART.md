# Quick Start Guide: Tirunelveli Public Transport Intelligence Platform (Nellai Transit)

Get the platform running on Windows in under 2 minutes.

---

## ⚡ Option 1: 1-Click Automated Windows Setup (Recommended)

### Step 1: Run Automated Setup
Double-click `setup.bat` or run:
```cmd
setup.bat
```
*This automatically checks your Python installation, creates a `.venv` virtual environment, installs dependencies (including Folium and Streamlit), and seeds `data/transit.db` with Tirunelveli bus and train transit records.*

### Step 2: Start the Platform
Double-click `run.bat` or run:
```cmd
run.bat
```
*Your browser will launch automatically at `http://localhost:8501`.*

### Step 3: Run Automated Tests
Double-click `test.bat` or run:
```cmd
test.bat
```
*Executes all 30 automated unit tests across data, tracking, DB, ETL, providers, and KPI calculations.*

---

## 🛠️ Option 2: Manual Step-by-Step Setup

If you prefer manual terminal execution:

### 1. Open Terminal & Navigate to Project
```powershell
cd "d:\90 days\90-days-90-projects-day-07-public-transit-delay-dashboard"
```

### 2. Create and Activate Virtual Environment
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment
```powershell
copy .env.example .env
```

### 5. Run ETL Data Pipeline
```powershell
python src\etl.py
```

### 6. Start Application
```powershell
streamlit run app.py
```

### 7. Run Pytest Suite
```powershell
pytest -v
```

---

## ⚙️ Operational Mode Toggle

Located right in the header bar:
- **Production Mode (Verified Timetables)**: Displays honest `[SCHEDULED]` and `[STATIC]` timetables with zero fabricated live GPS telemetry.
- **Demonstration Mode (Simulated GPS)**: Emulates real-time telemetry with a prominent yellow warning banner so evaluators can inspect live animations and ETA progression safely without deception.

---

## 🧭 Exploring the 6 Clean Tabs

Once launched, use the top tabs to explore:

1. **🚏 Find a Bus**:
   - **Find by Stop**: Search by stop name in English or Tamil (e.g. `Junction`, `Palayamkottai`, `நெல்லை சந்திப்பு`).
   - **Find by Proximity / Landmark**: Select a well-known Tirunelveli landmark (Vannarpettai, Anna Stadium, Nellaiyappar Temple) or input device GPS coordinates to discover nearby bus stops within walking distance.
   - **Filter by Route**: View all bus services connecting an origin and destination stop.

2. **🚌 Track a Bus (TNSTC Nellai)**:
   - Select any Nellai city bus from the dropdown:
     - `TNSTC Route 1 (TN-72-N-1042)`: Veinthaankulam New Bus Stand ↔ Tirunelveli Junction
     - `TNSTC Route 2 (TN-72-N-2104)`: Junction ↔ Town Nellaiyappar Temple
     - `TNSTC Route 3 (TN-72-N-3011)`: Junction ↔ Palayamkottai Market
     - `TNSTC Route 10 (TN-72-N-1090)`: Town Nellaiyappar ↔ High Ground Medical College
     - `TNSTC Route 41 (TN-72-N-4105)`: Junction ↔ Cheranmahadevi & Ambasamudram
     - `TNSTC Route 144 (TN-72-N-1442)`: New Bus Stand ↔ Nanguneri & Valliyur
   - Check real-time on-time/delay status, next stop ETA, vehicle speed, and stop-by-stop route timeline.
   - View focused Leaflet route map with vehicle position.

3. **🚆 Find a Train (Southern Railway)**:
   - Search by 5-digit Indian Railways train number (e.g., `12632`, `20666`, `06682`, `06685`).
   - **Geographic Scope Enforcement**: Verifies whether the train serves Tirunelveli Hub. If searching a valid non-local train (e.g., `12621 Tamil Nadu Express`), the system clearly explains it operates outside Tirunelveli rather than showing fake local stops.
   - View assigned platform number, current running status, delay variance, and full halt timetable.

4. **🗺️ Tirunelveli Map**:
   - District-wide interactive Leaflet map centered at Tirunelveli (`[8.7285, 77.7050]`).
   - View Thamirabarani River, transit corridors, station nodes, and live vehicle markers.
   - Filter vehicles by mode: All, Buses only, or Trains only.

5. **📋 Station Departure Board**:
   - Select any major Tirunelveli station: Tirunelveli Junction, New Bus Stand, Palayamkottai, Town, Ambasamudram, or Tenkasi.
   - Clean arrival schedule showing incoming services, platforms, scheduled times, delay variance, and honest status.

6. **📊 Network Analytics**:
   - High-level KPIs: Monitored Trips, On-Time Arrival Rate (≤ 2 mins), Average Delay, and Transit Reliability Index.
   - 30-day delay trend with 7-day moving average.
   - Primary delay root causes (Traffic Congestion, Railway Crossing, Peak Dwell Time, Signal Clearance, Passenger Rush).
