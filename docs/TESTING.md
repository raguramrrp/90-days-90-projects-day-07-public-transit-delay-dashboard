# Testing Strategy & Verification Report

## 1. Testing Strategy

The test suite covers unit logic, relational schema initialization, database queries, mathematical KPI boundaries, geospatial coordinate validation, vehicle tracking, modular providers, geographic eligibility enforcement, Google Stitch UI civic template compliance, and end-to-end ETL ingestion.

Automated tests are executed using **pytest** via `test.bat`:
```cmd
.\test.bat
```

---

## 2. Test Suites (9 Suites, 37 Tests)

### `tests/test_ui.py` (5 tests) — *New in Google Stitch v2.5*
- `test_stitch_template_exists_and_valid`: Verifies that `src/stitch_template.html` exists and contains essential civic markup tags (`<html`, `<head`, `<body`).
- `test_stitch_template_civic_palette_and_typography`: Validates the Google Stitch "Austere Civic Utility" design tokens:
  - Font families: `Inter` and `Material+Symbols+Outlined`
  - Tabular figure formatting: `tabular-nums` / `tnum`
  - Civic color palette tokens: `#00507d` (Municipal Slate), `#006a61` (Pine Teal), `#8d4f00` (Amber), `#ba1a1a` (Red)
  - 4px border geometry rule: verifies absence of generic AI rounded pill badges (`rounded-full`) in primary cards.
- `test_stitch_template_bus_search_features`: Validates origin/destination controls, GPS geolocation trigger, swap button, quick terminal chips (`Junction`, `New Bus Stand`, `Palayamkottai`), Thamirabarani River SVG vector plot, and Route 11A live telemetry card.
- `test_stitch_template_train_search_features`: Validates CRIS NTES search input, 5-digit train lookup, calling station filter (`TEN`, `TYT`, `PLM`, `ALL`), quick corridor buttons, non-local train boundary notice, and locomotive motive power (`WAP-7 ED 37102`).
- `test_stitch_template_station_hubs`: Validates terminal interchange explorer for `Tirunelveli Central Junction (TEN)`, `MGR New Bus Stand (VBS)`, `Palayamkottai Market (PLM)`, and `Town Nellaiyappar Temple (TOWN)` with SVG concourse schematics and prepaid auto fixed tariffs.

### `tests/test_providers.py` (10 tests)
- `test_data_freshness_tiers`: Validates all 6 freshness enum tiers (`LIVE`, `RECENT`, `SCHEDULED`, `ESTIMATED`, `STATIC`, `UNAVAILABLE`) and their metadata badges.
- `test_haversine_distance`: Verifies distance calculations across known geographic landmarks.
- `test_bus_stop_provider_search_and_proximity`: Tests bus stop lookups by English query, Tamil query, and nearby coordinate radius filtering.
- `test_bus_route_eligibility`: Tests geographic eligibility enforcement for bus routes and stops.
- `test_train_number_format_validation`: Validates 5-digit regex rules for Indian Railways train numbering.
- `test_train_tirunelveli_eligibility_enforcement`: Tests that Tirunelveli trains (e.g. 12632 Nellai SF) are accepted and non-local trains (e.g. 12621 TN Express) are correctly identified as non-local with informative explanations.
- `test_train_running_status_honest_classification`: Verifies honest status tagging without synthetic live deception.
- `test_geocoding_landmark_resolution`: Tests geocoding resolution for prominent Tirunelveli landmarks.
- `test_stitch_additional_trains`: Validates lookup and running status for additional corridor trains (`16127 Guruvayur Express`, `16723 Ananthapuri Express`, `16847 Sengottai Express`) with locomotive motive units (`WAP-7`, `WAP-4`).
- `test_station_hub_interchanges`: Tests station hub facilities, SVG concourse schematics, amenities, connecting buses, and prepaid auto tariffs for `TEN`, `VBS`, `PLM`, and `TOWN`.

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

### `tests/test_chennai_data.py` (5 tests)
- `test_chennai_operators`: Verifies operator definitions, modes (Bus, Train), and brand color hex values for TNSTC, Southern Railway, and SETC.
- `test_chennai_stations`: Verifies all 20 stations, ensures unique IDs, checks zone mapping, and validates that GPS coordinates fall strictly within Tamil Nadu bounds ($8.00^\circ - 14.00^\circ\text{ N}, 76.00^\circ - 81.00^\circ\text{ E}$).
- `test_chennai_routes`: Validates all 10 transit routes, ensuring stops resolve to valid station IDs and all transport modes are represented.
- `test_bottleneck_stations`: Verifies chronic bottleneck stations exist in the master station catalog (Tirunelveli Junction, New Bus Stand, etc.).
- `test_chennai_data_sources`: Validates cataloged feeds (TNSTC, Southern Railway, SETC, Telemetry Engine).

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

## 3. Verified Test Execution Results (37/37 Passed)

```
============================= test session starts =============================
platform win32 -- Python 3.12.6, pytest-9.1.1, pluggy-1.7.0
rootdir: D:\90 days\90-days-90-projects-day-07-public-transit-delay-dashboard
configfile: pyproject.toml
testpaths: tests
collected 37 items

tests/test_analytics.py::test_analytics_kpi_workflow PASSED              [  2%]
tests/test_analytics.py::test_empty_dataframe_handling PASSED            [  5%]
tests/test_chennai_data.py::test_chennai_operators PASSED                [  8%]
tests/test_chennai_data.py::test_chennai_stations PASSED                 [ 10%]
tests/test_chennai_data.py::test_chennai_routes PASSED                   [ 13%]
tests/test_chennai_data.py::test_bottleneck_stations PASSED              [ 16%]
tests/test_chennai_data.py::test_chennai_data_sources PASSED             [ 18%]
tests/test_db.py::test_init_db_and_health PASSED                         [ 21%]
tests/test_db.py::test_execute_query_and_non_query PASSED                [ 24%]
tests/test_etl.py::test_etl_transform_and_load PASSED                    [ 27%]
tests/test_generator.py::test_generate_transit_data_schemas PASSED       [ 29%]
tests/test_generator.py::test_referential_integrity PASSED               [ 32%]
tests/test_kpi.py::test_classify_delay_status PASSED                     [ 35%]
tests/test_kpi.py::test_determine_time_period PASSED                     [ 37%]
tests/test_kpi.py::test_calculate_reliability_score_perfect PASSED       [ 40%]
tests/test_kpi.py::test_calculate_reliability_score_bounds PASSED        [ 43%]
tests/test_kpi.py::test_get_tier_info PASSED                             [ 45%]
tests/test_providers.py::test_data_freshness_tiers PASSED                [ 48%]
tests/test_providers.py::test_haversine_distance PASSED                  [ 51%]
tests/test_providers.py::test_bus_stop_provider_search_and_proximity PASSED [ 54%]
tests/test_providers.py::test_bus_route_eligibility PASSED               [ 56%]
tests/test_providers.py::test_train_number_format_validation PASSED      [ 59%]
tests/test_providers.py::test_train_tirunelveli_eligibility_enforcement PASSED [ 62%]
tests/test_providers.py::test_train_running_status_honest_classification PASSED [ 64%]
tests/test_providers.py::test_geocoding_landmark_resolution PASSED       [ 67%]
tests/test_providers.py::test_stitch_additional_trains PASSED            [ 70%]
tests/test_providers.py::test_station_hub_interchanges PASSED            [ 72%]
tests/test_tracking.py::test_get_live_feed_status PASSED                 [ 75%]
tests/test_tracking.py::test_get_vehicle_tracking_data_demo_mode PASSED  [ 78%]
tests/test_tracking.py::test_get_vehicle_tracking_data_live_mode PASSED  [ 81%]
tests/test_tracking.py::test_advance_demo_vehicles PASSED                [ 83%]
tests/test_tracking.py::test_reset_demo_tracking_data PASSED             [ 86%]
tests/test_ui.py::test_stitch_template_exists_and_valid PASSED           [ 89%]
tests/test_ui.py::test_stitch_template_civic_palette_and_typography PASSED [ 91%]
tests/test_ui.py::test_stitch_template_bus_search_features PASSED        [ 94%]
tests/test_ui.py::test_stitch_template_train_search_features PASSED      [ 97%]
tests/test_ui.py::test_stitch_template_station_hubs PASSED               [100%]

============================= 37 passed in 4.40s ==============================
```
**Test Status:** `PASS` (37 passed, 0 failures, 100% success rate).
