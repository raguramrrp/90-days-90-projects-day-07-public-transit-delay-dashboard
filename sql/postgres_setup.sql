-- ============================================================================
-- Tirunelveli Public Transport Intelligence Platform (Nellai Transit)
-- PostgreSQL Enterprise Database DDL & Schema Setup (v2.5)
-- Optimized DDL with SERIAL keys, foreign key constraints, and vacuum analyze
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS transit;
SET search_path TO transit, public;

-- Drop existing tables
DROP TABLE IF EXISTS vehicle_positions CASCADE;
DROP TABLE IF EXISTS vehicles CASCADE;
DROP TABLE IF EXISTS import_history CASCADE;
DROP TABLE IF EXISTS data_sources CASCADE;
DROP TABLE IF EXISTS system_settings CASCADE;
DROP TABLE IF EXISTS actual_times CASCADE;
DROP TABLE IF EXISTS trips CASCADE;
DROP TABLE IF EXISTS stations CASCADE;
DROP TABLE IF EXISTS routes CASCADE;
DROP TABLE IF EXISTS operators CASCADE;

-- 1. Operators
CREATE TABLE operators (
    operator_id         VARCHAR(32) PRIMARY KEY,
    operator_name       VARCHAR(128) NOT NULL,
    short_code          VARCHAR(16) NOT NULL,
    transport_mode      VARCHAR(32) NOT NULL,
    city                VARCHAR(64) DEFAULT 'Tirunelveli',
    state               VARCHAR(64) DEFAULT 'Tamil Nadu',
    website             VARCHAR(256),
    color_hex           VARCHAR(16) DEFAULT '#0D9488',
    logo_icon           VARCHAR(16) DEFAULT '🚌'
);

-- 2. Routes
CREATE TABLE routes (
    route_id            VARCHAR(32) PRIMARY KEY,
    route_short_name    VARCHAR(64) NOT NULL,
    route_long_name     VARCHAR(128) NOT NULL,
    route_type          VARCHAR(32) NOT NULL,
    operator_id         VARCHAR(32) REFERENCES operators(operator_id),
    agency_name         VARCHAR(128) DEFAULT 'TNSTC Tirunelveli',
    color_hex           VARCHAR(16) DEFAULT '#0D9488'
);

-- 3. Stations
CREATE TABLE stations (
    station_id          VARCHAR(32) PRIMARY KEY,
    station_code        VARCHAR(16) NOT NULL UNIQUE,
    station_name        VARCHAR(128) NOT NULL,
    latitude            DOUBLE PRECISION NOT NULL,
    longitude           DOUBLE PRECISION NOT NULL,
    zone_id             VARCHAR(64) NOT NULL,
    is_transfer_station SMALLINT DEFAULT 0,
    platforms_count     SMALLINT DEFAULT 2,
    accessible_modes    VARCHAR(128) DEFAULT 'Bus, Train'
);

-- 4. Trips
CREATE TABLE trips (
    trip_id             VARCHAR(64) PRIMARY KEY,
    route_id            VARCHAR(32) NOT NULL REFERENCES routes(route_id) ON DELETE CASCADE,
    service_id          VARCHAR(32) NOT NULL,
    trip_headsign       VARCHAR(128) NOT NULL,
    direction_id        SMALLINT DEFAULT 0,
    block_id            VARCHAR(32),
    vehicle_id          VARCHAR(32)
);

-- 5. Actual Times (Arrival Observation Records)
CREATE TABLE actual_times (
    record_id           SERIAL PRIMARY KEY,
    trip_id             VARCHAR(64) NOT NULL REFERENCES trips(trip_id) ON DELETE CASCADE,
    station_id          VARCHAR(32) NOT NULL REFERENCES stations(station_id) ON DELETE CASCADE,
    stop_sequence       SMALLINT NOT NULL,
    scheduled_arrival   TIMESTAMP NOT NULL,
    actual_arrival      TIMESTAMP NOT NULL,
    scheduled_departure TIMESTAMP NOT NULL,
    actual_departure    TIMESTAMP NOT NULL,
    delay_minutes       NUMERIC(5, 2) NOT NULL,
    status              VARCHAR(32) NOT NULL,
    delay_reason        VARCHAR(128),
    recorded_date       DATE NOT NULL,
    hour_of_day         SMALLINT NOT NULL,
    time_period         VARCHAR(32) NOT NULL,
    is_peak_hour        SMALLINT DEFAULT 0,
    is_weekend          SMALLINT DEFAULT 0,
    day_of_week         VARCHAR(16) NOT NULL,
    provenance          VARCHAR(32) DEFAULT 'OBSERVED'
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_actual_times_trip ON actual_times (trip_id);
CREATE INDEX IF NOT EXISTS idx_actual_times_station ON actual_times (station_id);
CREATE INDEX IF NOT EXISTS idx_actual_times_date ON actual_times (recorded_date);
CREATE INDEX IF NOT EXISTS idx_actual_times_status ON actual_times (status);
CREATE INDEX IF NOT EXISTS idx_stations_zone ON stations (zone_id);

ANALYZE;
