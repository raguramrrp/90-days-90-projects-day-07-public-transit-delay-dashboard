# Quick Start Guide: Public Transit Delay Analytics Dashboard

Get the project running on Windows in under 2 minutes.

---

## ⚡ Option 1: 1-Click Automated Windows Setup (Recommended)

### Step 1: Run Automated Setup
Double-click `setup.bat` or run:
```cmd
setup.bat
```
*This automatically checks your Python installation, creates a `.venv` virtual environment, installs dependencies, seeds the database with transit records, and exports Power BI datasets.*

### Step 2: Start the Dashboard
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
python src\powerbi_export.py
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

## 📊 Opening in Microsoft Power BI Desktop
1. Launch **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV**.
3. Select files from `data/powerbi_export/`:
   - `dim_routes.csv`
   - `dim_stations.csv`
   - `dim_date.csv`
   - `dim_time_period.csv`
   - `fact_transit_performance.csv`
4. Copy the DAX measures from `powerbi/dax_measures.dax`.
5. Build visuals following `docs/POWERBI_GUIDE.md`.
