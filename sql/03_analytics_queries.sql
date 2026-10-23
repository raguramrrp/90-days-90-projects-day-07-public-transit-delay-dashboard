-- ============================================================================
-- Public Transit Delay Analytics Dashboard - Interview & Portfolio SQL Queries
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

-- Query 3: 7-Day Moving Average of Daily Delays (Rolling Window Analytics)
WITH daily_agg AS (
    SELECT 
        recorded_date,
        COUNT(record_id) AS daily_records,
        ROUND(AVG(delay_minutes), 2) AS daily_avg_delay
    FROM actual_times
    GROUP BY recorded_date
)
SELECT 
    recorded_date,
    daily_records,
    daily_avg_delay,
    ROUND(
        AVG(daily_avg_delay) OVER (
            ORDER BY recorded_date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 2
    ) AS rolling_7day_avg_delay
FROM daily_agg
ORDER BY recorded_date ASC;

-- Query 4: Peak-Hour Delay Surge Analysis (Comparing Peak to Off-Peak Delay Ratios)
WITH period_stats AS (
    SELECT 
        r.route_short_name,
        AVG(CASE WHEN a.is_peak_hour = 1 THEN a.delay_minutes ELSE NULL END) AS peak_delay,
        AVG(CASE WHEN a.is_peak_hour = 0 THEN a.delay_minutes ELSE NULL END) AS off_peak_delay
    FROM routes r
    JOIN trips t ON r.route_id = t.route_id
    JOIN actual_times a ON t.trip_id = a.trip_id
    GROUP BY r.route_short_name
)
SELECT 
    route_short_name,
    ROUND(peak_delay, 2) AS avg_peak_delay,
    ROUND(off_peak_delay, 2) AS avg_off_peak_delay,
    ROUND((peak_delay - off_peak_delay), 2) AS peak_delay_delta,
    ROUND((peak_delay / NULLIF(off_peak_delay, 0)), 2) AS congestion_surge_ratio
FROM period_stats
ORDER BY congestion_surge_ratio DESC;

-- Query 5: Delay Cascading Analysis (Stop-to-Stop Propagation using LAG)
WITH trip_delays AS (
    SELECT 
        a.trip_id,
        a.stop_sequence,
        s.station_name,
        a.delay_minutes,
        LAG(a.delay_minutes, 1) OVER (
            PARTITION BY a.trip_id 
            ORDER BY a.stop_sequence
        ) AS previous_stop_delay
    FROM actual_times a
    JOIN stations s ON a.station_id = s.station_id
)
SELECT 
    station_name,
    COUNT(*) AS times_serviced,
    ROUND(AVG(delay_minutes - previous_stop_delay), 2) AS avg_delay_added_at_stop
FROM trip_delays
WHERE previous_stop_delay IS NOT NULL
GROUP BY station_name
ORDER BY avg_delay_added_at_stop DESC
LIMIT 10;

-- Query 6: Hourly Congestion Heatmap Matrix
SELECT 
    hour_of_day,
    time_period,
    COUNT(record_id) AS total_trips,
    ROUND(AVG(delay_minutes), 2) AS avg_delay_minutes,
    ROUND(100.0 * SUM(CASE WHEN status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) / COUNT(record_id), 1) AS on_time_rate,
    ROUND(100.0 * SUM(CASE WHEN status = 'Severe Delay' THEN 1 ELSE 0 END) / COUNT(record_id), 1) AS severe_rate
FROM actual_times
GROUP BY hour_of_day, time_period
ORDER BY hour_of_day ASC;

-- Query 7: Primary Delay Root Causes and Impact Analysis
SELECT 
    delay_reason,
    COUNT(record_id) AS occurrence_count,
    ROUND(100.0 * COUNT(record_id) / (SELECT COUNT(*) FROM actual_times), 2) AS occurrence_percentage,
    ROUND(AVG(delay_minutes), 2) AS avg_delay_when_triggered,
    ROUND(SUM(delay_minutes), 1) AS total_delay_minutes_lost
FROM actual_times
WHERE delay_reason != 'Normal Operations'
GROUP BY delay_reason
ORDER BY total_delay_minutes_lost DESC;

-- Query 8: Weekday vs Weekend Reliability Disparity
SELECT 
    CASE WHEN is_weekend = 1 THEN 'Weekend' ELSE 'Weekday' END AS service_window,
    COUNT(record_id) AS total_stops,
    ROUND(AVG(delay_minutes), 2) AS avg_delay,
    ROUND(100.0 * SUM(CASE WHEN status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) / COUNT(record_id), 1) AS on_time_rate,
    ROUND(100.0 * SUM(CASE WHEN status = 'Severe Delay' THEN 1 ELSE 0 END) / COUNT(record_id), 1) AS severe_delay_rate
FROM actual_times
GROUP BY is_weekend;

-- Query 9: Station Reliability Classification (Tier Allocation)
SELECT 
    s.station_name,
    s.zone_id,
    ROUND(AVG(a.delay_minutes), 2) AS avg_delay,
    ROUND(100.0 * SUM(CASE WHEN a.status IN ('On-Time', 'Early') THEN 1 ELSE 0 END) / COUNT(a.record_id), 1) AS on_time_pct,
    CASE 
        WHEN AVG(a.delay_minutes) <= 2.5 THEN 'Tier 1 - High Reliability'
        WHEN AVG(a.delay_minutes) <= 5.0 THEN 'Tier 2 - Moderate Reliability'
        WHEN AVG(a.delay_minutes) <= 8.0 THEN 'Tier 3 - Chronic Congestion'
        ELSE 'Tier 4 - Severe Bottleneck'
    END AS station_tier
FROM stations s
JOIN actual_times a ON s.station_id = a.station_id
GROUP BY s.station_name, s.zone_id
ORDER BY avg_delay ASC;

-- Query 10: Trip Outlier Detection (>3 Standard Deviations from Route Mean)
WITH route_delay_stats AS (
    SELECT 
        t.route_id,
        AVG(a.delay_minutes) AS mean_delay,
        -- Approximate sample standard deviation
        AVG(a.delay_minutes * a.delay_minutes) - (AVG(a.delay_minutes) * AVG(a.delay_minutes)) AS variance_delay
    FROM trips t
    JOIN actual_times a ON t.trip_id = a.trip_id
    GROUP BY t.route_id
)
SELECT 
    a.trip_id,
    r.route_short_name,
    s.station_name,
    a.recorded_date,
    a.delay_minutes,
    a.delay_reason
FROM actual_times a
JOIN trips t ON a.trip_id = t.trip_id
JOIN routes r ON t.route_id = r.route_id
JOIN stations s ON a.station_id = s.station_id
JOIN route_delay_stats rds ON r.route_id = rds.route_id
WHERE a.delay_minutes > (rds.mean_delay + 2.5 * NULLIF(rds.variance_delay, 0))
ORDER BY a.delay_minutes DESC
LIMIT 10;
