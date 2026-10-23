# Data Directory Documentation

This directory contains the synthetic and processed transit feeds for the **Public Transit Delay Analytics Dashboard**.

## 1. Directory Structure

```
data/
├── README.md               # Data dictionary and schema specifications
├── transit.db              # SQLite database (auto-generated during setup)
├── raw/                    # Raw transit datasets (GTFS-compatible CSVs)
│   ├── routes.csv
│   ├── stations.csv
│   ├── trips.csv
│   └── actual_times.csv
├── processed/              # Cleaned and validated analytical datasets
│   ├── routes_clean.csv
│   ├── stations_clean.csv
│   ├── trips_clean.csv
│   └── actual_times_clean.csv
└── powerbi_export/         # Dimensional Star-Schema tables for Power BI
    ├── dim_routes.csv
    ├── dim_stations.csv
    ├── dim_date.csv
    ├── dim_time_period.csv
    ├── fact_transit_performance.csv
    └── agg_route_kpis.csv
```

## 2. Table Schemas & Data Dictionary

### Table: `routes` (`dim_routes`)
Represents transit lines across the metropolitan network.
- `route_id` (TEXT, PK): Unique route identifier (e.g., `RT-RED`, `RT-BLUE`, `RT-BUS-101`).
- `route_short_name` (TEXT): Display name (e.g., `Red Line (Subway)`, `Bus 101 Express`).
- `route_long_name` (TEXT): Terminal-to-terminal description (e.g., `Downtown Central <-> Tech Hub`).
- `route_type` (TEXT): Transit modality (`Subway / Rail`, `Light Rail`, `Bus Rapid Transit`, `Express Bus`, `Commuter Rail`).
- `agency_name` (TEXT): Operating transit authority.
- `color_hex` (TEXT): Line visualization color hex code.

### Table: `stations` (`dim_stations`)
Represents physical passenger stations and intermodal terminals.
- `station_id` (TEXT, PK): Unique station identifier (e.g., `ST-01`, `ST-03`).
- `station_code` (TEXT, UNIQUE): 4-letter station acronym (e.g., `DWTN`, `UNON`).
- `station_name` (TEXT): Full station facility name.
- `latitude` (REAL): Geographic latitude coordinate for map plotting.
- `longitude` (REAL): Geographic longitude coordinate for map plotting.
- `zone_id` (TEXT): Fare and operational zone (`Zone 1`, `Zone 2`, `Zone 3`).
- `is_transfer_station` (INTEGER): Flag `1` if passenger transfer interchange exists; `0` otherwise.

### Table: `trips`
Represents individual scheduled vehicle runs.
- `trip_id` (TEXT, PK): Unique trip identifier (e.g., `TRIP-20261001-1001`).
- `route_id` (TEXT, FK): Foreign key referencing `routes(route_id)`.
- `service_id` (TEXT): Schedule regime (`WEEKDAY-REG`, `WEEKEND-REG`).
- `trip_headsign` (TEXT): Destination display text.
- `direction_id` (INTEGER): `0` = Outbound, `1` = Inbound.
- `block_id` (TEXT): Vehicle block scheduling group.
- `vehicle_id` (TEXT): Physical vehicle unit identifier.

### Table: `actual_times` (`fact_transit_performance`)
Observation records of scheduled versus actual arrival/departure times at stations.
- `record_id` (INTEGER, PK): Primary key record counter.
- `trip_id` (TEXT, FK): Foreign key referencing `trips(trip_id)`.
- `station_id` (TEXT, FK): Foreign key referencing `stations(station_id)`.
- `stop_sequence` (INTEGER): Ordered sequence index along the route.
- `scheduled_arrival` (TEXT): Timetabled arrival timestamp (`YYYY-MM-DD HH:MM:SS`).
- `actual_arrival` (TEXT): Recorded arrival timestamp (`YYYY-MM-DD HH:MM:SS`).
- `scheduled_departure` (TEXT): Timetabled departure timestamp (`YYYY-MM-DD HH:MM:SS`).
- `actual_departure` (TEXT): Recorded departure timestamp (`YYYY-MM-DD HH:MM:SS`).
- `delay_minutes` (REAL): Difference between actual and scheduled arrival in minutes.
- `status` (TEXT): Performance category (`Early`, `On-Time`, `Minor Delay`, `Moderate Delay`, `Severe Delay`).
- `delay_reason` (TEXT): Primary root cause (`Normal Operations`, `Signal / Switch Malfunction`, etc.).
- `recorded_date` (TEXT): Calendar date (`YYYY-MM-DD`).
- `hour_of_day` (INTEGER): 24-hour clock hour (`0` to `23`).
- `time_period` (TEXT): Categorical period (`Morning Peak`, `Off-Peak (Midday)`, `Evening Peak`, `Night / Early Morning`).
- `is_peak_hour` (INTEGER): `1` if 07:00-09:59 or 16:00-19:59; `0` otherwise.
- `is_weekend` (INTEGER): `1` if Saturday/Sunday; `0` if Monday-Friday.
- `day_of_week` (TEXT): Full day name (`Monday`, `Tuesday`, etc.).

## 3. Data Generation & Reproducibility

The dataset is generated algorithmically via `src/generator.py` with fixed random seeds (`random_seed=42`).
To re-generate or modify the dataset parameters (e.g. number of days or trips per day):

```bash
# In the virtual environment:
python src/generator.py
python src/etl.py
python src/powerbi_export.py
```
