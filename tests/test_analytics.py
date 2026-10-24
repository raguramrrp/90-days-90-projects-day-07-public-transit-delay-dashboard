"""Analytical aggregations and filtering tests for Tirunelveli transit data."""

import pandas as pd
from datetime import date
from src.etl import TransitETLPipeline
from src.analytics import (
    load_transit_facts,
    filter_dataset,
    get_executive_kpis,
    get_route_performance_table,
    get_station_ranking_table,
    get_peak_hour_breakdown,
    get_daily_trends,
    get_delay_reasons
)


def test_analytics_kpi_workflow():
    """Verify analytical functions against seeded database."""
    # Ensure database is loaded
    pipeline = TransitETLPipeline()
    pipeline.run()

    df = load_transit_facts()
    assert not df.empty

    # Test filtering by route
    sample_route = df["route_short_name"].iloc[0]
    filtered_df = filter_dataset(df, routes=[sample_route])
    assert not filtered_df.empty
    assert (filtered_df["route_short_name"] == sample_route).all()

    # Test KPIs calculation
    kpis = get_executive_kpis(filtered_df)
    assert kpis["total_trips"] > 0
    assert 0.0 <= kpis["on_time_pct"] <= 100.0
    assert 0.0 <= kpis["tri_score"] <= 100.0
    assert kpis["tier_info"]["tier"] in ["High", "Acceptable", "Needs Attention", "Critical"]

    # Test Route performance table
    r_table = get_route_performance_table(df)
    assert not r_table.empty
    assert "Reliability Index (TRI)" in r_table.columns

    # Test Station rankings
    s_table = get_station_ranking_table(df, top_n=5)
    assert not s_table.empty
    assert len(s_table) <= 5
    assert "Avg Delay (min)" in s_table.columns

    # Test Peak breakdown
    hourly, period = get_peak_hour_breakdown(df)
    assert not hourly.empty
    assert not period.empty

    # Test Daily trends
    daily = get_daily_trends(df)
    assert not daily.empty
    assert "rolling_7day_delay" in daily.columns

    # Test Delay reasons
    reasons = get_delay_reasons(df)
    assert not reasons.empty
    assert "total_delay" in reasons.columns


def test_empty_dataframe_handling():
    """Verify that analytics gracefully handle empty filtered dataframes."""
    empty_df = pd.DataFrame(columns=["record_id", "trip_id", "delay_minutes", "status", "route_short_name", "time_period"])
    kpis = get_executive_kpis(empty_df)
    assert kpis["total_trips"] == 0
    assert kpis["avg_delay_minutes"] == 0.0
    assert kpis["tri_score"] == 0.0

    r_table = get_route_performance_table(empty_df)
    assert r_table.empty

    s_table = get_station_ranking_table(empty_df)
    assert s_table.empty
