# Data Directory Documentation

This directory contains the authentic multimodal transit data feeds, raw CSV extracts, cleaned analytical datasets, and SQLite relational database for the **Tirunelveli Public Transport Intelligence Platform (Nellai Transit)**.

## 1. Directory Structure

```
data/
├── README.md               # Data dictionary and schema specifications
├── transit.db              # SQLite relational database (auto-generated during setup)
├── raw/                    # Raw transit datasets (GTFS-compatible CSVs)
│   ├── routes.csv
│   ├── stations.csv
│   ├── trips.csv
│   └── actual_times.csv
└── processed/              # Cleaned and validated analytical datasets
    ├── routes_clean.csv
    ├── stations_clean.csv
    ├── trips_clean.csv
    └── actual_times_clean.csv
```

## 2. Table Schemas & Data Dictionary

### Table: `routes`
Represents authentic transit lines across the Tirunelveli district and connected transport corridors.
- `route_id` (TEXT, PK): Unique route identifier (e.g., `TNSTC-R1`, `TNSTC-R11A`, `SR-TRAIN-12632`).
- `route_short_name` (TEXT): Display name (e.g., `Route 1 (Junction <-> Palayamkottai)`, `Train 16127 (Guruvayur Express)`).
- `route_long_name` (TEXT): Terminal-to-terminal description (e.g., `Tirunelveli Junction <-> Palayamkottai Market via Vannarpettai`).
- `route_type` (TEXT): Transit modality (`Bus`, `Superfast & Express Rail`, `Intercity Express Bus`).
- `operator_id` (TEXT, FK): Operating transit authority (`AGENCY-TNSTC`, `AGENCY-SR`, `AGENCY-SETC`).
- `agency_name` (TEXT): Full authority name (e.g., `TNSTC Tirunelveli`, `Southern Railway`).
- `color_hex` (TEXT): Line visualization color hex code.

### Table: `stations`
Represents verified passenger stations, bus terminals, and multimodal interchange hubs across Tirunelveli.
- `station_id` (TEXT, PK): Unique station identifier (e.g., `NEL-01`, `NEL-02`).
- `station_code` (TEXT, UNIQUE): Station code (e.g., `TEN`, `VBS`, `PLM`, `TOWN`).
- `station_name` (TEXT): Full station facility name (e.g., `Tirunelveli Junction Railway Station`).
- `latitude` (REAL): Geographic latitude coordinate (bounds: 8.30° to 9.00° N).
- `longitude` (REAL): Geographic longitude coordinate (bounds: 77.30° to 78.20° E).
- `zone_id` (TEXT): Geographic zone (`Zone 1 - Junction Core`, `Zone 2 - Palayamkottai & New Hub`, `Zone 3 - West Ghats Corridor`, `Zone 4 - North & Coastal Corridors`).
- `is_transfer_station` (INTEGER): Flag `1` if multimodal passenger transfer interchange exists; `0` otherwise.

### Table: `trips`
Represents individual scheduled vehicle runs.
- `trip_id` (TEXT, PK): Unique trip identifier (e.g., `TRIP-NEL-20261001-1001`).
- `route_id` (TEXT, FK): Foreign key referencing `routes(route_id)`.
- `service_id` (TEXT): Schedule regime (`WEEKDAY-REG`, `WEEKEND-REG`).
- `trip_headsign` (TEXT): Destination display text.
- `direction_id` (INTEGER): `0` = Outbound, `1` = Inbound.
- `block_id` (TEXT): Vehicle block scheduling group.
- `vehicle_id` (TEXT): Physical vehicle unit identifier.

### Table: `actual_times`
Observation records of scheduled versus actual arrival and departure events across stations.
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
- `delay_reason` (TEXT): Primary root cause (`Normal Operations`, `Vannarpettai Bridge Traffic Congestion`, etc.).
- `recorded_date` (TEXT): Calendar date (`YYYY-MM-DD`).
- `hour_of_day` (INTEGER): 24-hour clock hour (`0` to `23`).
- `time_period` (TEXT): Categorical period (`Morning Peak`, `Off-Peak (Midday)`, `Evening Peak`, `Night / Early Morning`).
- `is_peak_hour` (INTEGER): `1` if 07:00-09:59 or 16:00-19:59; `0` otherwise.
- `is_weekend` (INTEGER): `1` if Saturday/Sunday; `0` if Monday-Friday.
- `day_of_week` (TEXT): Full day name (`Monday`, `Tuesday`, etc.).

## 3. Data Generation & Pipeline Execution

The datasets are generated algorithmically via `src/generator.py` and validated through `src/etl.py`:

```bash
# In the virtual environment:
python src/generator.py
python src/etl.py
```
