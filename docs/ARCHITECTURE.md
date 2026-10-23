# System Architecture & Technical Specifications

## 1. Architectural Blueprint

The **Public Transit Delay Analytics Dashboard** follows a modular, decoupled architecture consisting of Data Ingestion, Relational Storage, Analytical Modeling, and Dual-Frontend Presentation layers.

```mermaid
flowchart TD
    subgraph Data_Layer ["Data Ingestion & ETL"]
        RAW["Raw Transit Feed / GTFS<br/>(routes, stations, trips, actual_times)"] --> ETL["TransitETLPipeline (src/etl.py)"]
        GEN["Synthetic Data Generator<br/>(src/generator.py)"] -.-> RAW
        ETL --> VAL["Validation & Cleaning<br/>- Timestamp Parser<br/>- Delay Derivation<br/>- Peak Period Tagging"]
    end

    subgraph Storage_Layer ["Storage & Relational Schema"]
        VAL --> DB{{"SQL Database Engine<br/>(SQLAlchemy)"}}
        DB --> SQLITE["SQLite (Local 1-Click)<br/>data/transit.db"]
        DB --> PG["PostgreSQL (Enterprise)<br/>transit schema"]
        
        VIEWS["Analytical Views & Indices<br/>- v_route_performance<br/>- v_station_bottlenecks<br/>- v_peak_hour_performance<br/>- v_daily_reliability"] --- DB
    end

    subgraph Analytics_Layer ["Analytics & Export Engine"]
        DB --> ANALYTICS["Analytics Engine (src/analytics.py)<br/>- KPI Calculations<br/>- TRI Score Formula<br/>- Filtering & Slicing"]
        DB --> EXPORT["Power BI Exporter (src/powerbi_export.py)"]
        EXPORT --> PBI_CSV["Star Schema CSVs<br/>(dim_*, fact_*)"]
        EXPORT --> DAX["DAX Measures File<br/>(powerbi/dax_measures.dax)"]
    end

    subgraph Presentation_Layer ["Presentation & Visualization"]
        ANALYTICS --> STREAMLIT["Streamlit Interactive Web App (app.py)<br/>- Overview (KPIs, Trends)<br/>- Route Analysis<br/>- Station Bottlenecks<br/>- Peak Hours & Congestion"]
        PBI_CSV --> PBI_DESKTOP["Microsoft Power BI Desktop / Service<br/>- Executive Report Pages<br/>- Interactive Cross-filtering"]
        DAX --> PBI_DESKTOP
    end
```

## 2. Component Descriptions

### Ingestion & Transformation (`src/etl.py` & `src/generator.py`)
- **Stochastic Transit Generator**: Creates realistic timetable departures across 30 days with time-of-day travel densities, passenger dwell times, bottleneck dwell spikes, and incident shocks.
- **Data Cleaner**: Cleans and normalizes foreign key constraints, calculates delay minutes accurately as $(\text{actual} - \text{scheduled})$, and tags peak hours, weekdays, and status classes.

### Database Layer (`src/db.py` & `sql/`)
- Relational schema enforcing primary keys and foreign key cascades across:
  - `routes`
  - `stations`
  - `trips`
  - `actual_times`
- Analytical views pre-computing route punctuality, station rankings, and daily reliability indices.
- Dual-compatibility: SQLite for instant local Windows evaluation without external server overhead, and PostgreSQL DDL (`sql/postgres_setup.sql`) for enterprise cloud environments.

### Analytics Engine (`src/analytics.py`)
- Computes multi-level KPIs and filters dataframes dynamically across user-selected routes, date windows, time periods, and service regimes.
- Computes Transit Reliability Index (TRI) using the standardized weighted formulation.

### Visual Presentation Layer (`app.py` & `powerbi/`)
- **Streamlit Web Dashboard**: Fully interactive with Plotly charts, metric cards, bubble maps, heatmaps, and data download utilities.
- **Power BI Deliverables**: Complete dimensional star schema with fact and dimension tables, DAX measures, and Power Query M transformations.
