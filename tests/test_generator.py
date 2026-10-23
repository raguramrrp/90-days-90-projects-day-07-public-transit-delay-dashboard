"""Test suite for synthetic transit dataset generation."""

import pandas as pd
from src.generator import generate_transit_data, MASTER_ROUTES, MASTER_STATIONS


def test_generate_transit_data_schemas():
    """Verify that generated dataframes contain all required columns and non-empty rows."""
    routes_df, stations_df, trips_df, actual_df = generate_transit_data(num_days=2, trips_per_day=10, random_seed=123)

    assert len(routes_df) == len(MASTER_ROUTES)
    assert len(stations_df) == len(MASTER_STATIONS)
    assert len(trips_df) > 0
    assert len(actual_df) > len(trips_df)

    # Routes schema
    for col in ["route_id", "route_short_name", "route_long_name", "route_type", "agency_name", "color_hex"]:
        assert col in routes_df.columns

    # Stations schema
    for col in ["station_id", "station_code", "station_name", "latitude", "longitude", "zone_id", "is_transfer_station"]:
        assert col in stations_df.columns

    # Trips schema
    for col in ["trip_id", "route_id", "service_id", "trip_headsign", "direction_id"]:
        assert col in trips_df.columns

    # Actual times schema
    for col in [
        "record_id", "trip_id", "station_id", "stop_sequence",
        "scheduled_arrival", "actual_arrival", "delay_minutes",
        "status", "delay_reason", "recorded_date", "hour_of_day",
        "time_period", "is_peak_hour", "is_weekend", "day_of_week"
    ]:
        assert col in actual_df.columns


def test_referential_integrity():
    """Ensure trips reference valid routes and actual times reference valid trips and stations."""
    routes_df, stations_df, trips_df, actual_df = generate_transit_data(num_days=2, trips_per_day=5, random_seed=99)

    valid_routes = set(routes_df["route_id"])
    valid_stations = set(stations_df["station_id"])
    valid_trips = set(trips_df["trip_id"])

    assert trips_df["route_id"].isin(valid_routes).all()
    assert actual_df["trip_id"].isin(valid_trips).all()
    assert actual_df["station_id"].isin(valid_stations).all()
