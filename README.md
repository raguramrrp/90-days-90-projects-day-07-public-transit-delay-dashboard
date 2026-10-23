# 🚆 Public Transit Delay Analytics Dashboard

[![Day 7 of 90](https://img.shields.io/badge/90_Days_Challenge-Day_07-blue.svg)](https://github.com/raguramrrp)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Power BI](https://img.shields.io/badge/Power_BI-Desktop_%26_Service-F2C811.svg?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16.0-4169E1.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLite](https://img.shields.io/badge/SQLite-Dual_Engine-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Tests Passing](https://img.shields.io/badge/Tests-12%20Passed-10B981.svg)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Day 7 Project — 90 Days – 90 Projects Challenge**  
> An enterprise-grade transit reliability intelligence platform analyzing scheduled versus actual arrival feeds, station bottlenecks, peak-hour congestion multipliers, and composite reliability scores.

---

## 1. Problem Statement & Motivation
Urban transit authorities, dispatch coordinators, and commuters struggle with recurring, unexplained delay cascades. Disjointed timetables and raw sensor feeds prevent planners from answering fundamental operational questions:
- Which transit corridors and routes systematically fail their Service Level Agreements (SLAs)?
- Which intermodal stations act as chronic bottlenecks causing dwell-time compounding?
- What is the exact delay penalty introduced during morning and evening rush hours?
- How can transit systems quantify fleet health using a single, balanced **Transit Reliability Index (TRI)**?

The **Public Transit Delay Analytics Dashboard** resolves these challenges by providing an automated ETL ingestion pipeline, relational SQL schema, composite KPI calculations, and interactive visualizations across both **Streamlit** and **Microsoft Power BI**.

---

## 2. Objectives & Intended Users

### Primary Objectives
1. **Automated GTFS/Timetable Ingestion**: Ingest and clean timetabled vs. actual arrival/departure observations.
2. **Standardized Delay Classification**: Segment operations into 5 standard classes: *Early (<0m)*, *On-Time (0-2m)*, *Minor Delay (2-5m)*, *Moderate Delay (5-15m)*, and *Severe Delay (>15m)*.
3. **KPI & Composite Index Calculation**: Model fleet on-time percentages, peak surge ratios, and the **Transit Reliability Index (TRI)**.
4. **Dual SQL Database Architecture**: Provide immediate 1-click Windows execution via SQLite while offering full PostgreSQL production DDL.
5. **Business Intelligence Deliverables**: Supply ready-to-use Star-Schema CSVs, official DAX measure formulas, and CTE-driven SQL interview queries.

### Intended Users
- **Transit Planners & Schedule Engineers**: Optimize runtimes, timetables, and headway buffers.
- **Operations & Fleet Dispatchers**: Monitor real-time SLA compliance and incident root causes.
- **Urban Mobility Analysts & Data Analysts**: Query historical trends and build executive stakeholder dashboards.
- **Technical Recruiters & Hiring Managers**: Review end-to-end data analytics, SQL, Power BI, and Python engineering portfolio evidence.

---

## 3. Key Features

- **📊 Executive Overview Dashboard**: Real-time KPI cards (Total Trips, On-Time %, Fleet Average Delay, Severe Delay Count, and Transit Reliability Index), 30-day delay trend with 7-day moving average, performance donut breakdown, and root cause analysis.
- **🚏 Route Reliability League Table**: Ranked route performance matrix, on-time SLA rates, TRI score comparisons, and interactive stop-by-stop delay cascading profiles.
- **📍 Station Bottleneck Identification**: Top 10 delay hotspots, geographic interactive bubble maps (bubble size = average delay, color = fare zone), and station SLA compliance metrics.
- **⏰ Peak-Hour Surge & Congestion Dynamics**: 24-hour congestion curves with shaded Morning Peak (07-10h) and Evening Peak (16-20h) bands, Day-versus-Hour congestion heatmap matrix, and congestion surge multipliers.
- **💼 Power BI & SQL Portfolio Hub**: Embedded dimensional Star Schema ER diagrams, 13 official DAX measures, and 10 production SQL analytics queries.
- **🎛️ Dynamic Cross-Filtering**: Global sidebar controls for routes, time periods, service windows (Weekday vs Weekend), and custom date ranges.

---

## 4. Dashboard Screenshots

### Executive Overview & KPIs
![Executive Overview](screenshots/dashboard_overview.png)
*Executive summary displaying total trips, on-time arrival rate, fleet average delay, severe delay count, 30-day moving average trend line, and delay root causes.*

### Route Reliability League Table & Delay Cascades
![Route Analysis](screenshots/route_analysis.png)
*Route rankings sorted by Transit Reliability Index (TRI), comparative bar charts, and stop-by-stop delay cascading profile.*

### Station Bottleneck Identification & Geographic Map
![Station Bottlenecks](screenshots/station_bottlenecks.png)
*Geographic delay bubble map and top bottleneck stations ranked by average delay.*

### Peak-Hour Congestion Dynamics & Heatmap
![Peak Hours & Congestion](screenshots/peak_hours_surge.png)
*24-hour fleet delay progression with shaded rush-hour bands, peak vs off-peak comparative metrics, and Day-of-Week vs Hour congestion heatmap.*

---

## 5. Architecture & Data Flow

```mermaid
flowchart TD
    RAW["Raw GTFS / Transit Data<br/>(routes, stations, trips, actual_times)"] --> ETL["TransitETLPipeline (src/etl.py)"]
    GEN["Transit Generator (src/generator.py)"] -.-> RAW
    ETL --> VAL["Validation & Cleaning<br/>- Timestamp Parser<br/>- Delay Derivation<br/>- Peak Classification"]
    
    VAL --> DB{{"Relational Engine<br/>(SQLAlchemy)"}}
    DB --> SQLITE["SQLite (Local Windows 1-Click)<br/>data/transit.db"]
    DB --> PG["PostgreSQL (Enterprise)<br/>transit schema"]
    
    DB --> ANALYTICS["Analytics Engine (src/analytics.py)<br/>- KPI Aggregations<br/>- TRI Formulation<br/>- Multi-Filter Slicing"]
    DB --> EXPORT["Power BI Exporter (src/powerbi_export.py)"]
    EXPORT --> PBI_CSV["Star Schema Datasets<br/>(dim_*, fact_*)"]
    EXPORT --> DAX["DAX Measures (powerbi/dax_measures.dax)"]
    
    ANALYTICS --> STREAMLIT["Streamlit Dashboard (app.py)<br/>Overview • Routes • Stations • Peak Hours"]
    PBI_CSV --> PBI["Power BI Desktop / Service"]
    DAX --> PBI
```

---

## 6. Technology Stack

| Domain | Technology | Version / Specification | Purpose |
| :--- | :--- | :--- | :--- |
| **Frontend** | Streamlit | `>=1.35.0` | Interactive web dashboard & reactive filtering |
| **Visualizations** | Plotly & Plotly Express | `>=5.22.0` | High-resolution interactive charts, heatmaps & maps |
| **Backend & ETL** | Python | `3.12` | Data extraction, cleaning, validation, and analytics |
| **Database** | SQLite & PostgreSQL | Standard SQL / PG 16 | Relational tables, foreign keys, analytical views, and indexes |
| **ORM / Connection** | SQLAlchemy | `>=2.0.0` | Dual-engine database abstraction and pooling |
| **BI Tooling** | Microsoft Power BI | Desktop & Service | Star-schema modeling, DAX measures, M-code ingestion |
| **Data Processing** | Pandas & NumPy | `>=2.2.0`, `>=1.26.0` | High-performance vectorized dataset manipulation |
| **Testing** | Pytest | `>=8.2.0` | Automated test suite (12 passed tests) |

---

## 7. Project Directory Structure

```
90-days-90-projects-day-07-public-transit-delay-dashboard/
├── .env                              # Environment configuration (local)
├── .env.example                      # Configuration template
├── .gitignore                        # Git exclusion rules
├── LICENSE                           # MIT License
├── README.md                         # Comprehensive documentation
├── QUICKSTART.md                     # Fast setup guide
├── DEMO_SCRIPT.md                    # 90-120s presentation script
├── pyproject.toml                    # Python project configuration
├── requirements.txt                  # Pinned dependencies
├── setup.bat                         # 1-click Windows automated setup
├── run.bat                           # 1-click Windows application launcher
├── test.bat                          # 1-click Windows test execution script
├── app.py                            # Streamlit multi-page web application
├── config.py                         # Paths, thresholds, and operational constants
├── src/
│   ├── __init__.py
│   ├── db.py                         # SQLAlchemy database manager (SQLite + Postgres)
│   ├── generator.py                  # Stochastic transit feed and GTFS generator
│   ├── etl.py                        # Extract, Transform, Load pipeline
│   ├── analytics.py                  # Analytical queries and KPI calculation engine
│   └── powerbi_export.py             # Star-schema CSV and DAX generator
├── sql/
│   ├── 01_schema.sql                 # Universal table definitions & indexes
│   ├── 02_views_kpis.sql             # Pre-aggregated analytical views
│   ├── 03_analytics_queries.sql      # 10 production interview SQL queries
│   └── postgres_setup.sql            # PostgreSQL specific schema & vacuum scripts
├── powerbi/
│   ├── dax_measures.dax              # 13 official DAX measures
│   ├── power_query_m.txt             # Power Query M ingestion script
│   ├── report_layout.json            # Power BI page and visual specifications
│   └── README.md                     # Step-by-step Power BI Desktop instructions
├── data/
│   ├── README.md                     # Data dictionary and schema documentation
│   ├── raw/                          # Raw generated CSV files
│   ├── processed/                    # Cleaned analytical CSV files
│   └── powerbi_export/               # Ready-to-import Star Schema tables
├── docs/
│   ├── PROJECT_OVERVIEW.md           # Business context, problem, scope
│   ├── ARCHITECTURE.md               # Technical architecture & Mermaid diagrams
│   ├── USER_GUIDE.md                 # Complete feature walkthrough
│   ├── DEVELOPMENT_NOTES.md          # Design decisions and trade-offs
│   ├── TESTING.md                    # Test cases and verification log
│   ├── TROUBLESHOOTING.md            # Windows error resolutions and FAQ
│   └── POWERBI_GUIDE.md              # In-depth Power BI modeling guide
├── screenshots/
│   ├── generate_screenshots.py       # Automated screenshot generator script
│   ├── dashboard_overview.png
│   ├── route_analysis.png
│   ├── station_bottlenecks.png
│   └── peak_hours_surge.png
└── tests/
    ├── __init__.py
    ├── test_db.py                    # Database connection & view tests
    ├── test_etl.py                   # Ingestion and cleaning tests
    ├── test_analytics.py             # KPI calculations and filter tests
    ├── test_kpi.py                   # Delay thresholds and TRI score tests
    └── test_generator.py             # Feed generator schema & integrity tests
```

---

## 8. Prerequisites

- **Operating System**: Windows 10 or 11 (also runs on Linux / macOS).
- **Python**: Version `3.10`, `3.11`, or `3.12` installed.
- **Git**: Installed for version control.
- **Power BI Desktop** *(Optional)*: Required only if customizing or viewing `.pbix` reports natively.

---

## 9. Step-by-Step Windows Installation

### Option A: Automated 1-Click Setup (Recommended)
1. Clone the repository:
   ```cmd
   git clone https://github.com/raguramrrp/90-days-90-projects-day-07-public-transit-delay-dashboard.git
   cd 90-days-90-projects-day-07-public-transit-delay-dashboard
   ```
2. Double-click `setup.bat`. This automatically:
   - Validates your Python runtime.
   - Creates an isolated `.venv` environment.
   - Installs dependencies from `requirements.txt`.
   - Copies `.env.example` to `.env`.
   - Runs `src/etl.py` to seed the database with 11,000+ observations.
   - Generates Star-Schema CSVs in `data/powerbi_export/`.
3. Launch the application:
   ```cmd
   run.bat
   ```

### Option B: Manual Setup
```powershell
# 1. Create and activate virtual environment
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Upgrade pip and install packages
python -m pip install --upgrade pip
pip install -r requirements.txt

# 3. Initialize environment variables
copy .env.example .env

# 4. Run data ingestion and export
python src\etl.py
python src\powerbi_export.py

# 5. Launch dashboard
streamlit run app.py
```

---

## 10. Environment Variables (`.env.example`)

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `DATABASE_URL` | `sqlite:///data/transit.db` | Database connection string (SQLite or PostgreSQL) |
| `APP_NAME` | `Public Transit Delay Analytics Dashboard` | Application display title |
| `DEBUG` | `True` | Debug mode toggle |
| `PORT` | `8501` | Local port for Streamlit web server |
| `SAMPLE_DAYS` | `30` | Number of historical days to generate |
| `SAMPLE_TRIPS_PER_DAY` | `80` | Average daily trips simulated |

To connect to PostgreSQL:
```ini
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/transit_analytics
```

---

## 11. Core Mathematical Formulations

### 1. Delay Minutes
$$\text{Delay (Minutes)} = \frac{\text{Actual Arrival Timestamp} - \text{Scheduled Arrival Timestamp}}{60}$$

### 2. On-Time Arrival Percentage
$$\text{On-Time \%} = \frac{\text{Count}(\text{Arrivals with Delay} \le 2.0\text{ min})}{\text{Total Monitored Arrivals}} \times 100$$

### 3. Transit Reliability Index (TRI)
A unified composite performance metric on a $0 - 100$ scale:
$$\text{TRI} = \max\left(0, \min\left(100, (\text{On-Time \%} \times 0.70) + ((100 - \text{Severe \%}) \times 0.30) - (\max(0, \text{Avg Delay}) \times 1.5)\right)\right)$$

| TRI Range | Service Quality Tier | Operational Meaning |
| :--- | :--- | :--- |
| **85.0 – 100.0** | 🟢 **High (Optimal)** | Excellent punctuality; minimal schedule disruption |
| **70.0 – 84.9** | 🔵 **Acceptable (Standard)** | Normal metropolitan operations within SLA tolerance |
| **50.0 – 69.9** | 🟡 **Needs Attention** | Chronic delays requiring headway adjustments |
| **0.0 – 49.9** | 🔴 **Critical** | Severe infrastructure or corridor failure |

---

## 12. Production SQL Analytics Queries

The project includes 10 production SQL queries (`sql/03_analytics_queries.sql`) testing key data analyst interview competencies:

```sql
-- Example: Top 5 Bottleneck Stations Ranked by Average Delay
WITH station_stats AS (
    SELECT 
        s.station_id,
        s.station_name,
        s.zone_id,
        COUNT(a.record_id) AS arrival_count,
        AVG(a.delay_minutes) AS raw_avg_delay,
        ROUND(AVG(a.delay_minutes), 2) AS avg_delay_minutes,
        ROUND(100.0 * SUM(CASE WHEN a.status = 'Severe Delay' THEN 1 ELSE 0 END) / COUNT(a.record_id), 2) AS severe_pct
    FROM stations s
    JOIN actual_times a ON s.station_id = a.station_id
    GROUP BY s.station_id, s.station_name, s.zone_id
)
SELECT 
    DENSE_RANK() OVER (ORDER BY raw_avg_delay DESC) AS delay_rank,
    station_name,
    zone_id,
    arrival_count,
    avg_delay_minutes,
    severe_pct
FROM station_stats
WHERE arrival_count >= 10
LIMIT 5;
```

---

## 13. Testing & Quality Assurance

Automated testing is configured using **pytest**. Run all tests via:
```cmd
test.bat
```

### Actual Test Results
```
tests/test_analytics.py::test_analytics_kpi_workflow PASSED              [  8%]
tests/test_analytics.py::test_empty_dataframe_handling PASSED            [ 16%]
tests/test_db.py::test_init_db_and_health PASSED                         [ 25%]
tests/test_db.py::test_execute_query_and_non_query PASSED                [ 33%]
tests/test_etl.py::test_etl_transform_and_load PASSED                    [ 41%]
tests/test_generator.py::test_generate_transit_data_schemas PASSED       [ 50%]
tests/test_generator.py::test_referential_integrity PASSED               [ 58%]
tests/test_kpi.py::test_classify_delay_status PASSED                     [ 66%]
tests/test_kpi.py::test_determine_time_period PASSED                     [ 75%]
tests/test_kpi.py::test_calculate_reliability_score_perfect PASSED       [ 83%]
tests/test_kpi.py::test_calculate_reliability_score_bounds PASSED        [ 91%]
tests/test_kpi.py::test_get_tier_info PASSED                             [100%]

============================= 12 passed in 4.34s ==============================
```
**Test Status:** `PASS` (12 passed, 0 failures, 0 warnings).

---

## 14. Known Limitations

1. **Simulated Timetables**: Historical feeds are realistically generated using stochastic delay distributions rather than live GTFS-RT APIs.
2. **Static Network Graph**: Stop sequence cascading assumes fixed station routing without dynamic track switching or express bypass paths.
3. **Power BI Desktop Native Engine**: While CSV dimensional exports and DAX scripts are 100% complete, viewing native `.pbix` files requires a Windows installation of Microsoft Power BI Desktop.

---

## 15. Future Roadmap

- [ ] **Real-time GTFS-RT Ingestion**: Connect live Protobuf feeds from public transit agencies via Apache Kafka or WebSockets.
- [ ] **Predictive Delay Forecasting**: Train LightGBM / XGBoost regression models to forecast arrival delay 30 minutes in advance.
- [ ] **Passenger Crowding Density**: Correlate passenger card tap-in volume with dwell-time delays.
- [ ] **Commuter Push Alerts**: Webhook alerts to Discord / Telegram when route delays exceed 10 minutes.

---

## 16. Learning Outcomes & Resume Keywords

### What Was Learned:
- End-to-end data engineering pipeline design (Extract, Transform, Load) for transportation domain datasets.
- Advanced SQL analytics using Common Table Expressions (CTEs), Window functions (`RANK`, `DENSE_RANK`, `LAG`), rolling 7-day moving averages, and grouped aggregations.
- Star-schema dimensional modeling connecting fact tables with dimension tables.
- DAX measure formulation including branching logic, time intelligence, and composite indexing.
- Interactive multi-page dashboard engineering with Streamlit, Plotly Express, and responsive UI design.

### Resume Keywords:
`Power BI`, `SQL (PostgreSQL & SQLite)`, `Data Modeling`, `Star Schema`, `DAX Measures`, `Data Visualization`, `ETL Pipelines`, `KPI Formulation`, `Streamlit`, `Plotly`, `Python`, `Transit Analytics`, `Pytest`.

---

## 17. License & Attribution

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.  
Developed as part of the **90 Days – 90 Projects Challenge** by **raguramrrp**.
