# Testing Strategy & Verification Report

## 1. Testing Strategy

The test suite covers unit logic, relational schema initialization, database queries, mathematical KPI boundaries, and end-to-end ETL ingestion.

Automated tests are executed using **pytest** via `test.bat`:
```cmd
.\test.bat
```

## 2. Test Suites

### `tests/test_kpi.py`
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

### `tests/test_generator.py`
- `test_generate_transit_data_schemas`: Verifies that all 4 generated DataFrames contain all mandatory columns and valid types.
- `test_referential_integrity`: Ensures all trips reference valid route IDs and all observations reference valid trip and station IDs.

### `tests/test_db.py`
- `test_init_db_and_health`: Validates SQL DDL table creation and health check reporting.
- `test_execute_query_and_non_query`: Tests parameterized INSERT and SELECT queries.

### `tests/test_etl.py`
- `test_etl_transform_and_load`: Tests full ETL pipeline execution from raw extraction through SQLite loading and view querying (`v_route_performance`, `v_station_bottlenecks`).

### `tests/test_analytics.py`
- `test_analytics_kpi_workflow`: Validates full analytical pipeline, filtering, KPI generation, route league table, station rankings, peak curves, and daily trends.
- `test_empty_dataframe_handling`: Ensures graceful zero-handling when filters return no records.

## 3. Test Execution Results

```
============================= test session starts =============================
platform win32 -- Python 3.12.6, pytest-9.1.1, pluggy-1.7.0
rootdir: D:\90 days\90-days-90-projects-day-07-public-transit-delay-dashboard
configfile: pyproject.toml
testpaths: tests
collected 12 items

tests/test_analytics.py::test_analytics_kpi_workflow PASSED              [  8%]
tests/test_analytics.py::test_empty_dataframe_handling PASSED            [ 16%]
tests/test_db.py::test_init_db_and_health PASSED                         [ 25%]
tests/test_db.py::test_execute_query_and_non_query PASSED                [ 33%]
tests/test_etl.py::test_etl_transform_and_load PASSED                    [ 41%]
tests/test_generator.py::test_generate_transit_data_schemas PASSED       [ 50%]
tests/test_generator.py::test_referential_integrity PASSED               [ 58%]
tests/test_kpi.py::test_classify_delay_status PASSED                     [ 66%]
tests/test_kpi.py::test_determine_time_period PASSED                     [ 75%]
tests/test_kpi.py::test_calculate_reliability_score_perfect PASSED       [ 83%]
tests/test_kpi.py::test_calculate_reliability_score_bounds PASSED        [ 91%]
tests/test_kpi.py::test_get_tier_info PASSED                             [100%]

============================= 12 passed in 4.34s ==============================
```
**Status: PASS (100% passing, 0 failures, 0 warnings)**
