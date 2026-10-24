"""Unit tests for vehicle tracking engine and demo simulation."""

import pytest
import pandas as pd
from src.tracking import (
    get_live_feed_status,
    get_vehicle_tracking_data,
    advance_demo_vehicles,
    reset_demo_tracking_data
)
from src.etl import TransitETLPipeline


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Ensure database has data loaded before running tracking tests."""
    pipeline = TransitETLPipeline()
    pipeline.run()


def test_get_live_feed_status():
    """Verify live feed statuses reflect verified telemetry sources."""
    status = get_live_feed_status()
    assert isinstance(status, dict)
    assert "TNSTC Tirunelveli AIS-140 Feed" in status
    assert "Southern Railway CRIS NTES (TEN)" in status
    assert "SETC Intercity Operations Feed" in status
    assert "Local Demo Engine" in status

    # Verify external feeds are marked not authorized / non-live
    assert status["TNSTC Tirunelveli AIS-140 Feed"]["authorized_live"] is False
    assert status["Southern Railway CRIS NTES (TEN)"]["authorized_live"] is False
    assert status["SETC Intercity Operations Feed"]["authorized_live"] is False
    # Local demo engine is active
    assert status["Local Demo Engine"]["authorized_live"] is True


def test_get_vehicle_tracking_data_demo_mode():
    """Verify retrieving vehicles and positions in demo mode."""
    df_vehicles, df_positions = get_vehicle_tracking_data(demo_mode=True)

    assert not df_vehicles.empty
    assert "vehicle_id" in df_vehicles.columns
    assert "operator_id" in df_vehicles.columns
    assert "vehicle_label" in df_vehicles.columns

    assert not df_positions.empty
    assert "position_id" in df_positions.columns
    assert "vehicle_id" in df_positions.columns
    assert "latitude" in df_positions.columns
    assert "longitude" in df_positions.columns
    assert "speed_kmh" in df_positions.columns
    assert "data_status" in df_positions.columns

    # In demo mode, all returned positions should have SIMULATED status
    assert (df_positions["data_status"] == "SIMULATED").all()

    # Latitudes and longitudes must be within Tamil Nadu bounds (lat 8.0-14.0, lon 76.0-81.0)
    assert (df_positions["latitude"] >= 8.0).all()
    assert (df_positions["latitude"] <= 14.0).all()
    assert (df_positions["longitude"] >= 76.0).all()
    assert (df_positions["longitude"] <= 81.0).all()


def test_get_vehicle_tracking_data_live_mode():
    """Verify retrieving vehicles and positions in live mode."""
    df_vehicles, df_positions = get_vehicle_tracking_data(demo_mode=False)
    assert not df_vehicles.empty
    # Live positions will only contain verified LIVE feeds (empty if none authorized)
    if not df_positions.empty:
        assert (df_positions["data_status"] == "LIVE").all()


def test_advance_demo_vehicles():
    """Verify demo vehicle progression updates coordinates and timestamps."""
    updated = advance_demo_vehicles()
    assert updated > 0

    _, df_positions = get_vehicle_tracking_data(demo_mode=True)
    assert not df_positions.empty
    # Ensure speeds are within realistic transit bounds (10 - 70 km/h)
    assert (df_positions["speed_kmh"] >= 10.0).all()
    assert (df_positions["speed_kmh"] <= 70.0).all()


def test_reset_demo_tracking_data():
    """Verify reset function executes cleanly."""
    reset_demo_tracking_data()
    _, df_positions = get_vehicle_tracking_data(demo_mode=True)
    assert not df_positions.empty
