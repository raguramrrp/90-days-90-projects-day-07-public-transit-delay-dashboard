-- ============================================================================
-- Tirunelveli Public Transport Intelligence Platform (Nellai Transit)
-- Advanced SQL Queries & Bottleneck Detection (v2.5)
-- Demonstrating CTEs, Window Functions, Rolling Averages, and Bottleneck Detection
-- ============================================================================

-- Query 1: Top 5 Worst Bottleneck Stations by Average Delay (Ranked via Window Function)
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

-- Query 2: Route Reliability League Table with Transit Reliability Index (TRI)
SELECT 
    r.route_short_name,
    r.route_type,
    COUNT(a.record_id) AS total_stops,
    ROUND(AVG(a.delay_minutes), 2) AS avg_delay,
    ROUND(100.0 * SUM(CASE WHEN a.status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) / COUNT(a.record_id), 1) AS on_time_rate,
    ROUND(
        MAX(0.0, MIN(100.0, 
            (100.0 * SUM(CASE WHEN a.status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) / COUNT(a.record_id)) * 0.70
            + (100.0 - (100.0 * SUM(CASE WHEN a.status = 'Severe Delay' THEN 1 ELSE 0 END) / COUNT(a.record_id))) * 0.30
            - (AVG(CASE WHEN a.delay_minutes > 0 THEN a.delay_minutes ELSE 0 END) * 1.5)
        )), 1
    ) AS tri_score,
    RANK() OVER (
        ORDER BY (100.0 * SUM(CASE WHEN a.status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) / COUNT(a.record_id)) DESC
    ) AS punctuality_rank
FROM routes r
JOIN trips t ON r.route_id = t.route_id
JOIN actual_times a ON t.trip_id = a.trip_id
GROUP BY r.route_id, r.route_short_name, r.route_type
ORDER BY tri_score DESC;

-- Query 3: 7-Day Rolling Moving Average Delay Profile
WITH daily_metrics AS (
    SELECT 
        recorded_date,
        ROUND(AVG(delay_minutes), 2) AS daily_avg_delay,
        COUNT(record_id) AS total_arrivals
    FROM actual_times
    GROUP BY recorded_date
)
SELECT 
    recorded_date,
    daily_avg_delay,
    total_arrivals,
    ROUND(
        AVG(daily_avg_delay) OVER (
            ORDER BY recorded_date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 
        2
    ) AS rolling_7day_avg_delay
FROM daily_metrics
ORDER BY recorded_date;

-- Query 4: Peak vs. Off-Peak Congestion Surge Multiplier
SELECT 
    time_period,
    is_peak_hour,
    COUNT(record_id) AS total_observations,
    ROUND(AVG(delay_minutes), 2) AS avg_delay_minutes,
    ROUND(100.0 * SUM(CASE WHEN status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) / COUNT(record_id), 2) AS on_time_pct,
    ROUND(100.0 * SUM(CASE WHEN status = 'Severe Delay' THEN 1 ELSE 0 END) / COUNT(record_id), 2) AS severe_pct
FROM actual_times
GROUP BY time_period, is_peak_hour
ORDER BY avg_delay_minutes DESC;

-- Query 5: Chronic Delay Propagation & Cascade per Route
SELECT 
    r.route_short_name,
    s.station_name,
    a.stop_sequence,
    ROUND(AVG(a.delay_minutes), 2) AS avg_delay_at_stop,
    ROUND(
        AVG(a.delay_minutes) - LAG(AVG(a.delay_minutes), 1, 0.0) OVER (
            PARTITION BY r.route_id 
            ORDER BY a.stop_sequence
        ),
        2
    ) AS incremental_delay_added
FROM routes r
JOIN trips t ON r.route_id = t.route_id
JOIN actual_times a ON t.trip_id = a.trip_id
JOIN stations s ON a.station_id = s.station_id
GROUP BY r.route_id, r.route_short_name, s.station_name, a.stop_sequence
ORDER BY r.route_id, a.stop_sequence;
