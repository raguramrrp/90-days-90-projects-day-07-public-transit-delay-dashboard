"""ETL data extraction, coordinate validation, and loading tests for Tirunelveli transit pipeline."""

import pandas as pd
from src.etl import TransitETLPipeline
from src.db import check_health, execute_query


def test_etl_transform_and_load(tmp_path):
    """Test full ETL pipeline on small dataset."""
    pipeline = TransitETLPipeline()
    audit = pipeline.run()

    assert audit["duration_seconds"] >= 0
    assert "database_status" in audit
    health = check_health()
    assert health["connected"] is True
    assert health["tables"]["routes"] > 0
    assert health["tables"]["stations"] > 0
    assert health["tables"]["trips"] > 0
    assert health["tables"]["actual_times"] > 0

    # Verify that views are queryable
    v_routes = execute_query("SELECT * FROM v_route_performance")
    assert not v_routes.empty
    assert "reliability_score" in v_routes.columns

    v_stations = execute_query("SELECT * FROM v_station_bottlenecks")
    assert not v_stations.empty
    assert "avg_delay_minutes" in v_stations.columns
