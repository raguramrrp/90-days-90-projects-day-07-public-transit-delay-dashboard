# Quick Start Guide: Tirunelveli Public Transport Intelligence Platform (Nellai Transit)

Get the platform running on Windows in under 2 minutes.

---

## ⚡ Option 1: 1-Click Automated Windows Setup (Recommended)

### Step 1: Run Automated Setup
Double-click `setup.bat` or run:
```cmd
setup.bat
```
*This automatically checks your Python installation, creates a `.venv` virtual environment, installs dependencies, and seeds `data/transit.db` with verified Tirunelveli bus and train transit records.*

### Step 2: Start the Platform
Double-click `run.bat` or run:
```cmd
run.bat
```
*Your browser will launch automatically at `http://localhost:8501` displaying the approved Google Stitch Civic Utility interface.*

### Step 3: Run Automated Tests
Double-click `test.bat` or run:
```cmd
test.bat
```
*Executes all **37 automated unit tests across 9 test suites** (100% pass rate) verifying UI templates, providers, tracking, database, ETL, and KPI calculations.*

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

## 🧭 Exploring the Google Stitch Civic Workspace (v2.5)

Once launched, use the municipal header tabs to explore:

### 1. 🚏 Bus Search & Live Telemetry
- **Origin / Destination Search**: Type stops in English or Tamil (e.g. `Junction`, `Palayamkottai`, `நெல்லை சந்திப்பு`).
- **One-Touch Actions**: Click the GPS icon for proximity detection, or click the Swap button to reverse direction.
- **Quick Terminals**: One-tap shortcut chips for `Junction`, `New Bus Stand`, `Palayamkottai`, and `Town`.
- **Thamirabarani River Vector Map**: Custom SVG cartography with Sulochana Mudaliar Bridge crossing and pulsing radar beacon on bus `TN-72-N-1842`.
- **Route 11A Inspector**: Live speed (28 km/h), AIS-140 transponder signal, and 5-stop progression timeline with ETAs.

### 2. 🚆 Train Search & CRIS NTES Live Status
- **5-Digit Search**: Query any Indian Railways train number (e.g., `16127`, `12632`, `20666`, `06682`, `16847`).
- **Station Scope**: Filter calling stations (`TEN`, `TYT`, `PLM`, `ALL`).
- **Boundary Verification**: Checks geographic eligibility—non-local trains (e.g. `12626 Kerala Express`) trigger an informative civic notice explaining route bounds outside Tirunelveli.
- **CRIS NTES Telemetry**: Motive power unit (`WAP-7 ED 37102`), speed (68 km/h), Gangaikondan block position, assigned platform (PF 1), and 8-halt progression line.

### 3. 🏢 Station Hub Interchanges
- **Intermodal Terminals**: Select between Tirunelveli Junction (`TEN`), MGR New Bus Stand (`VBS`), Palayamkottai (`PLM`), and Town (`TOWN`).
- **SVG Terminal Schematics**: Visual layout of railway platforms, bus bays, waiting rooms, and taxi ranks.
- **Synchronized Feeders**: Connecting city bus timetable with immediate departures.
- **Prepaid Auto Tariffs**: Official Tirunelveli Traffic Police fixed tariff cards protecting passengers from fare gouging.

### 4. ℹ️ About & Data Feeds
- **Operations Summary**: 2,880 active monitored trips, 86.4% on-time reliability, 4.8 min average delay.
- **Data Provenance**: Clear 6-tier classification (`LIVE`, `RECENT`, `SCHEDULED`, `ESTIMATED`, `STATIC`, `UNAVAILABLE`).
- **Civic Privacy**: Strict in-memory proximity computation with zero location persistence.
