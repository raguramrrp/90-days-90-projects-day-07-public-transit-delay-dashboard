-- ============================================================================
-- Public Transit Delay Analytics Dashboard - Database Schema
-- Compatible with PostgreSQL and SQLite
-- ============================================================================

-- Drop existing tables if re-initializing
DROP TABLE IF EXISTS actual_times;
DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS stations;
DROP TABLE IF EXISTS routes;

-- 1. Routes Table
CREATE TABLE routes (
    route_id            VARCHAR(32) PRIMARY KEY,
    route_short_name    VARCHAR(64) NOT NULL,
    route_long_name     VARCHAR(128) NOT NULL,
    route_type          VARCHAR(32) NOT NULL,
    agency_name         VARCHAR(128) DEFAULT 'Metropolitan Transit Authority',
    color_hex           VARCHAR(16) DEFAULT '#3B82F6'
);

-- 2. Stations Table
CREATE TABLE stations (
    station_id          VARCHAR(32) PRIMARY KEY,
    station_code        VARCHAR(16) NOT NULL UNIQUE,
    station_name        VARCHAR(128) NOT NULL,
    latitude            DOUBLE PRECISION NOT NULL,
    longitude           DOUBLE PRECISION NOT NULL,
    zone_id             VARCHAR(32) NOT NULL,
    is_transfer_station INTEGER DEFAULT 0
);

-- 3. Trips Table
CREATE TABLE trips (
    trip_id             VARCHAR(64) PRIMARY KEY,
    route_id            VARCHAR(32) NOT NULL REFERENCES routes(route_id) ON DELETE CASCADE,
    service_id          VARCHAR(32) NOT NULL,
    trip_headsign       VARCHAR(128) NOT NULL,
    direction_id        INTEGER DEFAULT 0,
    block_id            VARCHAR(32),
    vehicle_id          VARCHAR(32)
);

-- 4. Actual Times / Arrival Observations Table
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
    day_of_week         VARCHAR(16) NOT NULL
);

-- Indexes for Fast Analytical Filtering and Aggregations
CREATE INDEX idx_actual_times_trip ON actual_times (trip_id);
CREATE INDEX idx_actual_times_station ON actual_times (station_id);
CREATE INDEX idx_actual_times_date ON actual_times (recorded_date);
CREATE INDEX idx_actual_times_status ON actual_times (status);
CREATE INDEX idx_actual_times_period ON actual_times (time_period);
CREATE INDEX idx_actual_times_hour ON actual_times (hour_of_day);
CREATE INDEX idx_trips_route ON trips (route_id);
