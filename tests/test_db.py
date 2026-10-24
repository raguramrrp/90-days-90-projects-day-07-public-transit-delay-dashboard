"""Database schema initialization and SQL operation tests for Tirunelveli transit repository."""

import pytest
import pandas as pd
from src.db import init_db, check_health, execute_query, execute_non_query


def test_init_db_and_health():
    """Verify that database schema and views initialize properly."""
    init_db(drop_first=True)
    health = check_health()
    assert health["connected"] is True
    assert "routes" in health["tables"]
    assert "stations" in health["tables"]
    assert "trips" in health["tables"]
    assert "actual_times" in health["tables"]


def test_execute_query_and_non_query():
    """Verify INSERT and SELECT SQL operations."""
    init_db(drop_first=True)

    # Insert test route
    execute_non_query(
        "INSERT INTO routes (route_id, route_short_name, route_long_name, route_type) VALUES (:rid, :sname, :lname, :rtype)",
        {"rid": "TEST-RT", "sname": "Test Line", "lname": "Test Long Name", "rtype": "Bus"}
    )

    df = execute_query("SELECT * FROM routes WHERE route_id = 'TEST-RT'")
    assert len(df) == 1
    assert df.iloc[0]["route_short_name"] == "Test Line"
