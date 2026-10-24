# Testing Strategy & Verification Report

## 1. Testing Strategy

The test suite covers unit logic, relational schema initialization, database queries, mathematical KPI boundaries, geospatial coordinate validation, vehicle tracking, modular providers, geographic eligibility enforcement, and end-to-end ETL ingestion.

Automated tests are executed using **pytest** via `test.bat`:
```cmd
.\test.bat
```

---

## 2. Test Suites (8 Suites, 30 Tests)

### `tests/test_chennai_data.py` (5 tests)
- `test_chennai_operators`: Verifies operator definitions, modes (Bus, Train), and brand color hex values for TNSTC, Southern Railway, and SETC.
- `test_chennai_stations`: Verifies all 20 stations, ensures unique IDs, checks zone mapping, and validates that GPS coordinates fall strictly within Tamil Nadu bounds ($8.00^\circ - 14.00^\circ\text{ N}, 76.00^\circ - 81.00^\circ\text{ E}$).
- `test_chennai_routes`: Validates all 10 transit routes, ensuring stops resolve to valid station IDs and all transport modes are represented.
- `test_bottleneck_stations`: Verifies chronic bottleneck stations exist in the master station catalog (Tirunelveli Junction, New Bus Stand, etc.).
- `test_chennai_data_sources`: Validates cataloged feeds (TNSTC, Southern Railway, SETC, Telemetry Engine).

### `tests/test_providers.py` (8 tests)
- `test_data_freshness_tiers`: Validates all 6 freshness enum tiers (`LIVE`, `RECENT`, `SCHEDULED`, `ESTIMATED`, `STATIC`, `UNAVAILABLE`) and their metadata badges.
- `test_haversine_distance`: Verifies distance calculations across known geographic landmarks.
- `test_bus_stop_provider_search_and_proximity`: Tests bus stop lookups by English query, Tamil query, and nearby coordinate radius filtering.
- `test_bus_route_eligibility`: Tests geographic eligibility enforcement for bus routes and stops.
- `test_train_number_format_validation`: Validates 5-digit regex rules for Indian Railways train numbering.
- `test_train_tirunelveli_eligibility_enforcement`: Tests that Tirunelveli trains (e.g. 12632 Nellai SF) are accepted and non-local trains (e.g. 12621 TN Express) are correctly identified as non-local with informative explanations.
- `test_train_running_status_honest_classification`: Verifies honest status tagging without synthetic live deception.
- `test_geocoding_landmark_resolution`: Tests geocoding resolution for prominent Tirunelveli landmarks.

### `tests/test_tracking.py` (5 tests)
- `test_get_live_feed_status`: Verifies external feeds are correctly reported.
- `test_get_vehicle_tracking_data_demo_mode`: Verifies vehicle and position retrieval under demo mode.
- `test_get_vehicle_tracking_data_live_mode`: Tests retrieval under live mode with honest static fallback.
- `test_advance_demo_vehicles`: Validates that advancing the simulation successfully updates vehicle coordinates and realistic speed bounds (10–70 km/h).
- `test_reset_demo_tracking_data`: Verifies simulation reset functionality.

### `tests/test_kpi.py` (5 tests)
- `test_classify_delay_status`: Tests delay values across boundary conditions:
  - Negative values -> `Early`
  - 0.0 to 2.0 -> `On-Time`
  - 2.1 to 5.0 -> `Minor Delay`
  - 5.1 to 15.0 -> `Moderate Delay`
  - >15.0 -> `Severe Delay`
- `test_determine_time_period`: Validates hour segmentation into Morning Peak, Midday Off-Peak, Evening Peak, and Night.
- `test_calculate_reliability_score_perfect`: Tests 100% SLA conditions producing 100.0 score.
- `test_calculate_reliability_score_bounds`: Verifies upper and lower limits ($[0.0, 100.0]$).
- `test_get_tier_info`: Validates badge and color mapping across High, Acceptable, Needs Attention, and Critical tiers.

### `tests/test_generator.py` (2 tests)
- `test_generate_transit_data_schemas`: Verifies that generated DataFrames contain all mandatory columns and valid types.
- `test_referential_integrity`: Ensures all trips reference valid route IDs and all observations reference valid trip and station IDs.

### `tests/test_db.py` (2 tests)
- `test_init_db_and_health`: Validates SQL DDL table creation and health check reporting for all 9 tables.
- `test_execute_query_and_non_query`: Tests parameterized INSERT and SELECT queries.

### `tests/test_etl.py` (1 test)
- `test_etl_transform_and_load`: Tests full multimodal ETL pipeline execution from raw extraction through SQLite loading, coordinate validation, and view querying (`v_route_performance`, `v_station_bottlenecks`).

### `tests/test_analytics.py` (2 tests)
- `test_analytics_kpi_workflow`: Validates full analytical pipeline, filtering, KPI generation, route league table, station rankings, peak curves, and daily trends.
- `test_empty_dataframe_handling`: Ensures graceful zero-handling when filters return no records.

---

## 3. Test Execution Results

```
============================= test session starts =============================
platform win32 -- Python 3.12.6, pytest-9.1.1, pluggy-1.7.0
rootdir: D:\90 days\90-days-90-projects-day-07-public-transit-delay-dashboard
configfile: pyproject.toml
testpaths: tests
collected 30 items

tests/test_analytics.py::test_analytics_kpi_workflow PASSED              [  3%]
tests/test_analytics.py::test_empty_dataframe_handling PASSED            [  6%]
tests/test_chennai_data.py::test_chennai_operators PASSED                [ 10%]
tests/test_chennai_data.py::test_chennai_stations PASSED                 [ 13%]
tests/test_chennai_data.py::test_chennai_routes PASSED                   [ 16%]
tests/test_bottleneck_stations PASSED                                    [ 20%]
tests/test_chennai_data.py::test_chennai_data_sources PASSED             [ 23%]
tests/test_db.py::test_init_db_and_health PASSED                         [ 26%]
tests/test_db.py::test_execute_query_and_non_query PASSED                [ 30%]
tests/test_etl.py::test_etl_transform_and_load PASSED                    [ 33%]
tests/test_generator.py::test_generate_transit_data_schemas PASSED       [ 36%]
tests/test_generator.py::test_referential_integrity PASSED               [ 40%]
tests/test_kpi.py::test_classify_delay_status PASSED                     [ 43%]
tests/test_kpi.py::test_determine_time_period PASSED                     [ 46%]
tests/test_kpi.py::test_calculate_reliability_score_perfect PASSED       [ 50%]
tests/test_kpi.py::test_calculate_reliability_score_bounds PASSED        [ 53%]
tests/test_kpi.py::test_get_tier_info PASSED                             [ 56%]
tests/test_providers.py::test_data_freshness_tiers PASSED                [ 60%]
tests/test_providers.py::test_haversine_distance PASSED                  [ 63%]
tests/test_providers.py::test_bus_stop_provider_search_and_proximity PASSED [ 66%]
tests/test_providers.py::test_bus_route_eligibility PASSED               [ 70%]
tests/test_providers.py::test_train_number_format_validation PASSED      [ 73%]
tests/test_providers.py::test_train_tirunelveli_eligibility_enforcement PASSED [ 76%]
tests/test_providers.py::test_train_running_status_honest_classification PASSED [ 80%]
tests/test_providers.py::test_geocoding_landmark_resolution PASSED       [ 83%]
tests/test_tracking.py::test_get_live_feed_status PASSED                 [ 86%]
tests/test_tracking.py::test_get_vehicle_tracking_data_demo_mode PASSED  [ 90%]
tests/test_tracking.py::test_get_vehicle_tracking_data_live_mode PASSED  [ 93%]
tests/test_tracking.py::test_advance_demo_vehicles PASSED                [ 96%]
tests/test_tracking.py::test_reset_demo_tracking_data PASSED             [100%]

============================= 30 passed in 17.98s =============================
```
**Test Status:** `PASS` (30 passed, 0 failures, 100% success rate).
