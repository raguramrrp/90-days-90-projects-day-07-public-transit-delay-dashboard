-- ============================================================================
-- Tamil Nadu Public Transport Intelligence Platform - Database Schema
-- Universal compatibility with PostgreSQL and SQLite
-- ============================================================================

-- Drop existing tables in dependency order if re-initializing
DROP TABLE IF EXISTS vehicle_positions;
DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS import_history;
DROP TABLE IF EXISTS data_sources;
DROP TABLE IF EXISTS system_settings;
DROP TABLE IF EXISTS actual_times;
DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS stations;
DROP TABLE IF EXISTS routes;
DROP TABLE IF EXISTS operators;

-- 1. Transport Operators (TNSTC Tirunelveli, Southern Railway, etc.)
CREATE TABLE operators (
    operator_id         VARCHAR(32) PRIMARY KEY,
    operator_name       VARCHAR(128) NOT NULL,
    short_code          VARCHAR(16) NOT NULL,
    transport_mode      VARCHAR(32) NOT NULL,
    city                VARCHAR(64) DEFAULT 'Tirunelveli',
    state               VARCHAR(64) DEFAULT 'Tamil Nadu',
    website             VARCHAR(256),
    color_hex           VARCHAR(16) DEFAULT '#3B82F6',
    logo_icon           VARCHAR(16) DEFAULT '🚌'
);

-- 2. Routes Table
CREATE TABLE routes (
    route_id            VARCHAR(32) PRIMARY KEY,
    route_short_name    VARCHAR(64) NOT NULL,
    route_long_name     VARCHAR(128) NOT NULL,
    route_type          VARCHAR(32) NOT NULL,
    operator_id         VARCHAR(32) REFERENCES operators(operator_id),
    agency_name         VARCHAR(128) DEFAULT 'Metropolitan Transport Corporation',
    color_hex           VARCHAR(16) DEFAULT '#3B82F6'
);

-- 3. Stations & Stops Table
CREATE TABLE stations (
    station_id          VARCHAR(32) PRIMARY KEY,
    station_code        VARCHAR(16) NOT NULL UNIQUE,
    station_name        VARCHAR(128) NOT NULL,
    latitude            DOUBLE PRECISION NOT NULL,
    longitude           DOUBLE PRECISION NOT NULL,
    zone_id             VARCHAR(64) NOT NULL,
    is_transfer_station INTEGER DEFAULT 0,
    platforms_count     INTEGER DEFAULT 2,
    accessible_modes    VARCHAR(128) DEFAULT 'Bus, Train'
);

-- 4. Trips Table
CREATE TABLE trips (
    trip_id             VARCHAR(64) PRIMARY KEY,
    route_id            VARCHAR(32) NOT NULL REFERENCES routes(route_id) ON DELETE CASCADE,
    service_id          VARCHAR(32) NOT NULL,
    trip_headsign       VARCHAR(128) NOT NULL,
    direction_id        INTEGER DEFAULT 0,
    block_id            VARCHAR(32),
    vehicle_id          VARCHAR(32)
);

-- 5. Actual Times / Arrival Observations Table
CREATE TABLE actual_times (
    record_id           INTEGER PRIMARY KEY,
    trip_id             VARCHAR(64) NOT NULL REFERENCES trips(trip_id) ON DELETE CASCADE,
    station_id          VARCHAR(32) NOT NULL REFERENCES stations(station_id) ON DELETE CASCADE,
    stop_sequence       INTEGER NOT NULL,
    scheduled_arrival   VARCHAR(32) NOT NULL,
    actual_arrival      VARCHAR(32) NOT NULL,
    scheduled_departure VARCHAR(32) NOT NULL,
    actual_departure    VARCHAR(32) NOT NULL,
    delay_minutes       DOUBLE PRECISION NOT NULL,
    status              VARCHAR(32) NOT NULL,
    delay_reason        VARCHAR(128) NOT NULL,
    recorded_date       VARCHAR(16) NOT NULL,
    hour_of_day         INTEGER NOT NULL,
    time_period         VARCHAR(32) NOT NULL,
    is_peak_hour        INTEGER NOT NULL,
    is_weekend          INTEGER NOT NULL,
    day_of_week         VARCHAR(16) NOT NULL,
    provenance          VARCHAR(32) DEFAULT 'OBSERVED'
);

-- 6. Vehicles Master
CREATE TABLE vehicles (
    vehicle_id          VARCHAR(32) PRIMARY KEY,
    operator_id         VARCHAR(32) REFERENCES operators(operator_id),
    route_id            VARCHAR(32) REFERENCES routes(route_id),
    vehicle_label       VARCHAR(64) NOT NULL,
    transport_mode      VARCHAR(32) NOT NULL,
    capacity            INTEGER DEFAULT 65,
    is_accessible       INTEGER DEFAULT 1,
    current_status      VARCHAR(32) DEFAULT 'IN_SERVICE'
);

-- 7. Vehicle Real-Time & Simulated Positions
CREATE TABLE vehicle_positions (
    position_id         VARCHAR(64) PRIMARY KEY,
    vehicle_id          VARCHAR(32) NOT NULL,
    route_id            VARCHAR(32) NOT NULL,
    trip_id             VARCHAR(64),
    latitude            DOUBLE PRECISION NOT NULL,
    longitude           DOUBLE PRECISION NOT NULL,
    speed_kmh           DOUBLE PRECISION DEFAULT 25.0,
    bearing             INTEGER DEFAULT 0,
    recorded_at         VARCHAR(32) NOT NULL,
    data_status         VARCHAR(16) NOT NULL, -- 'LIVE', 'STATIC', 'HISTORICAL', 'SIMULATED'
    raw_source          VARCHAR(64) NOT NULL,
    confidence_score    DOUBLE PRECISION DEFAULT 1.0
);

-- 8. Data Sources & Quality Registry
CREATE TABLE data_sources (
    source_id           VARCHAR(32) PRIMARY KEY,
    source_name         VARCHAR(128) NOT NULL,
    operator_id         VARCHAR(32),
    feed_type           VARCHAR(32) NOT NULL,
    endpoint_url        VARCHAR(256),
    auth_type           VARCHAR(64),
    connection_status   VARCHAR(32) DEFAULT 'ACCESSIBLE',
    last_refresh_at     VARCHAR(32),
    record_count        INTEGER DEFAULT 0,
    update_frequency    VARCHAR(64)
);

-- 9. Import History Audit
CREATE TABLE import_history (
    import_id           INTEGER PRIMARY KEY,
    source_id           VARCHAR(32) NOT NULL,
    started_at          VARCHAR(32) NOT NULL,
    completed_at        VARCHAR(32) NOT NULL,
    status              VARCHAR(32) NOT NULL, -- 'SUCCESS', 'WARNING', 'FAILED'
    records_accepted    INTEGER DEFAULT 0,
    records_rejected    INTEGER DEFAULT 0,
    records_skipped     INTEGER DEFAULT 0,
    duration_seconds    DOUBLE PRECISION DEFAULT 0.0,
    error_log           TEXT
);

-- 10. System Settings & Configuration
CREATE TABLE system_settings (
    setting_key         VARCHAR(64) PRIMARY KEY,
    setting_value       TEXT NOT NULL,
    updated_at          VARCHAR(32) NOT NULL
);

-- Performance Indexes
CREATE INDEX idx_actual_times_trip ON actual_times (trip_id);
CREATE INDEX idx_actual_times_station ON actual_times (station_id);
CREATE INDEX idx_actual_times_date ON actual_times (recorded_date);
CREATE INDEX idx_actual_times_status ON actual_times (status);
CREATE INDEX idx_actual_times_period ON actual_times (time_period);
CREATE INDEX idx_actual_times_hour ON actual_times (hour_of_day);
CREATE INDEX idx_trips_route ON trips (route_id);
CREATE INDEX idx_vehicle_pos_route ON vehicle_positions (route_id);
CREATE INDEX idx_vehicle_pos_status ON vehicle_positions (data_status);
