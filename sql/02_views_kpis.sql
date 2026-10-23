-- ============================================================================
-- Public Transit Delay Analytics Dashboard - Analytical Views & KPI Metrics
-- Compatible with PostgreSQL and SQLite
-- ============================================================================

-- 1. Route Performance Summary View
DROP VIEW IF EXISTS v_route_performance;
CREATE VIEW v_route_performance AS
SELECT 
    r.route_id,
    r.route_short_name,
    r.route_long_name,
    r.route_type,
    r.color_hex,
    COUNT(a.record_id) AS total_observations,
    ROUND(AVG(a.delay_minutes), 2) AS avg_delay_minutes,
    MAX(a.delay_minutes) AS max_delay_minutes,
    SUM(CASE WHEN a.status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) AS on_time_count,
    SUM(CASE WHEN a.status = 'Minor Delay' THEN 1 ELSE 0 END) AS minor_delay_count,
    SUM(CASE WHEN a.status = 'Moderate Delay' THEN 1 ELSE 0 END) AS moderate_delay_count,
    SUM(CASE WHEN a.status = 'Severe Delay' THEN 1 ELSE 0 END) AS severe_delay_count,
    ROUND(
        100.0 * SUM(CASE WHEN a.status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) / COUNT(a.record_id),
        2
    ) AS on_time_percentage,
    ROUND(
        100.0 * SUM(CASE WHEN a.status = 'Severe Delay' THEN 1 ELSE 0 END) / COUNT(a.record_id),
        2
    ) AS severe_delay_percentage,
    -- Transit Reliability Index (TRI) Formula: Scale 0 to 100
    ROUND(
        MAX(0.0, MIN(100.0, 
            (100.0 * SUM(CASE WHEN a.status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) / COUNT(a.record_id)) * 0.70
            + (100.0 - (100.0 * SUM(CASE WHEN a.status = 'Severe Delay' THEN 1 ELSE 0 END) / COUNT(a.record_id))) * 0.30
            - (AVG(CASE WHEN a.delay_minutes > 0 THEN a.delay_minutes ELSE 0 END) * 1.5)
        )),
        1
    ) AS reliability_score
FROM routes r
JOIN trips t ON r.route_id = t.route_id
JOIN actual_times a ON t.trip_id = a.trip_id
GROUP BY r.route_id, r.route_short_name, r.route_long_name, r.route_type, r.color_hex;

-- 2. Station Bottleneck Ranking View
DROP VIEW IF EXISTS v_station_bottlenecks;
CREATE VIEW v_station_bottlenecks AS
SELECT 
    s.station_id,
    s.station_code,
    s.station_name,
    s.zone_id,
    s.latitude,
    s.longitude,
    s.is_transfer_station,
    COUNT(a.record_id) AS total_arrivals,
    ROUND(AVG(a.delay_minutes), 2) AS avg_delay_minutes,
    ROUND(AVG(CASE WHEN a.is_peak_hour = 1 THEN a.delay_minutes ELSE NULL END), 2) AS peak_avg_delay_minutes,
    SUM(CASE WHEN a.status = 'Severe Delay' THEN 1 ELSE 0 END) AS severe_delays,
    ROUND(
        100.0 * SUM(CASE WHEN a.status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) / COUNT(a.record_id),
        2
    ) AS on_time_percentage
FROM stations s
JOIN actual_times a ON s.station_id = a.station_id
GROUP BY s.station_id, s.station_code, s.station_name, s.zone_id, s.latitude, s.longitude, s.is_transfer_station;

-- 3. Peak Hour vs Off-Peak Performance View
DROP VIEW IF EXISTS v_peak_hour_performance;
CREATE VIEW v_peak_hour_performance AS
SELECT 
    a.time_period,
    a.is_peak_hour,
    a.is_weekend,
    COUNT(a.record_id) AS total_observations,
    ROUND(AVG(a.delay_minutes), 2) AS avg_delay_minutes,
    ROUND(
        100.0 * SUM(CASE WHEN a.status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) / COUNT(a.record_id),
        2
    ) AS on_time_percentage,
    SUM(CASE WHEN a.status = 'Severe Delay' THEN 1 ELSE 0 END) AS severe_delays
FROM actual_times a
GROUP BY a.time_period, a.is_peak_hour, a.is_weekend;

-- 4. Daily Fleet Reliability Trend View
DROP VIEW IF EXISTS v_daily_reliability;
CREATE VIEW v_daily_reliability AS
SELECT 
    a.recorded_date,
    a.day_of_week,
    a.is_weekend,
    COUNT(DISTINCT a.trip_id) AS total_trips,
    COUNT(a.record_id) AS total_stops_serviced,
    ROUND(AVG(a.delay_minutes), 2) AS avg_delay_minutes,
    ROUND(
        100.0 * SUM(CASE WHEN a.status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) / COUNT(a.record_id),
        2
    ) AS on_time_percentage,
    ROUND(
        MAX(0.0, MIN(100.0, 
            (100.0 * SUM(CASE WHEN a.status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) / COUNT(a.record_id)) * 0.70
            + (100.0 - (100.0 * SUM(CASE WHEN a.status = 'Severe Delay' THEN 1 ELSE 0 END) / COUNT(a.record_id))) * 0.30
            - (AVG(CASE WHEN a.delay_minutes > 0 THEN a.delay_minutes ELSE 0 END) * 1.5)
        )),
        1
    ) AS reliability_score
FROM actual_times a
GROUP BY a.recorded_date, a.day_of_week, a.is_weekend;
