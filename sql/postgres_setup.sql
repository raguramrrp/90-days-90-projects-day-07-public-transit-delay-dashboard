-- ============================================================================
-- Public Transit Delay Analytics Dashboard - PostgreSQL Enterprise Setup
-- Optimized DDL with SERIAL keys, foreign key constraints, and vacuum analyze
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS transit;
SET search_path TO transit, public;

-- Drop existing tables
DROP TABLE IF EXISTS actual_times CASCADE;
DROP TABLE IF EXISTS trips CASCADE;
DROP TABLE IF EXISTS stations CASCADE;
DROP TABLE IF EXISTS routes CASCADE;

-- 1. Routes
CREATE TABLE routes (
    route_id            VARCHAR(32) PRIMARY KEY,
    route_short_name    VARCHAR(64) NOT NULL,
    route_long_name     VARCHAR(128) NOT NULL,
    route_type          VARCHAR(32) NOT NULL,
    agency_name         VARCHAR(128) DEFAULT 'Metropolitan Transit Authority',
    color_hex           VARCHAR(16) DEFAULT '#3B82F6'
);

-- 2. Stations
CREATE TABLE stations (
    station_id          VARCHAR(32) PRIMARY KEY,
    station_code        VARCHAR(16) NOT NULL UNIQUE,
    station_name        VARCHAR(128) NOT NULL,
    latitude            DOUBLE PRECISION NOT NULL,
    longitude           DOUBLE PRECISION NOT NULL,
    zone_id             VARCHAR(32) NOT NULL,
    is_transfer_station SMALLINT DEFAULT 0
);

-- 3. Trips
CREATE TABLE trips (
    trip_id             VARCHAR(64) PRIMARY KEY,
    route_id            VARCHAR(32) NOT NULL REFERENCES routes(route_id) ON DELETE CASCADE,
    service_id          VARCHAR(32) NOT NULL,
    trip_headsign       VARCHAR(128) NOT NULL,
    direction_id        SMALLINT DEFAULT 0,
    block_id            VARCHAR(32),
    vehicle_id          VARCHAR(32)
);

-- 4. Actual Times (Arrival Observation Records)
CREATE TABLE actual_times (
    record_id           SERIAL PRIMARY KEY,
    trip_id             VARCHAR(64) NOT NULL REFERENCES trips(trip_id) ON DELETE CASCADE,
    station_id          VARCHAR(32) NOT NULL REFERENCES stations(station_id) ON DELETE CASCADE,
    stop_sequence       INTEGER NOT NULL,
    scheduled_arrival   TIMESTAMP NOT NULL,
    actual_arrival      TIMESTAMP NOT NULL,
    scheduled_departure TIMESTAMP NOT NULL,
    actual_departure    TIMESTAMP NOT NULL,
    delay_minutes       DOUBLE PRECISION NOT NULL,
    status              VARCHAR(32) NOT NULL,
    delay_reason        VARCHAR(128) NOT NULL,
    recorded_date       DATE NOT NULL,
    hour_of_day         SMALLINT NOT NULL,
    time_period         VARCHAR(32) NOT NULL,
    is_peak_hour        SMALLINT NOT NULL,
    is_weekend          SMALLINT NOT NULL,
    day_of_week         VARCHAR(16) NOT NULL
);

-- Performance Indexes
CREATE INDEX idx_actual_times_trip ON actual_times (trip_id);
CREATE INDEX idx_actual_times_station ON actual_times (station_id);
CREATE INDEX idx_actual_times_date ON actual_times (recorded_date);
CREATE INDEX idx_actual_times_status ON actual_times (status);
CREATE INDEX idx_actual_times_period ON actual_times (time_period);
CREATE INDEX idx_actual_times_hour ON actual_times (hour_of_day);
CREATE INDEX idx_trips_route ON trips (route_id);

-- Run query optimization statistics
VACUUM ANALYZE;
