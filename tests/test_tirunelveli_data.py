"""Unit tests for Tirunelveli (Nellai) master transit data definitions."""

import re
from src.tirunelveli_data import (
    TIRUNELVELI_OPERATORS,
    TIRUNELVELI_STATIONS,
    TIRUNELVELI_ROUTES,
    TIRUNELVELI_DATA_SOURCES,
    TIRUNELVELI_BOTTLENECK_STATIONS
)


def test_tirunelveli_operators():
    """Verify operator definitions, modes, and metadata for Tirunelveli."""
    assert len(TIRUNELVELI_OPERATORS) == 3
    operator_ids = {op["operator_id"] for op in TIRUNELVELI_OPERATORS}
    assert operator_ids == {"AGENCY-TNSTC", "AGENCY-SR", "AGENCY-SETC"}

    for op in TIRUNELVELI_OPERATORS:
        assert op["city"] == "Tirunelveli"
        assert op["state"] == "Tamil Nadu"
        assert re.match(r"^#[0-9A-Fa-f]{6}$", op["color_hex"])
        assert op["logo_icon"] != ""


def test_tirunelveli_stations():
    """Verify 20 master stations across Tirunelveli district, valid coordinates, and zones."""
    assert len(TIRUNELVELI_STATIONS) == 20
    station_ids = [s["station_id"] for s in TIRUNELVELI_STATIONS]
    assert len(set(station_ids)) == 20, "Station IDs must be unique"

    valid_zones = {
        "Zone 1 - Junction Core",
        "Zone 2 - Palayamkottai & New Hub",
        "Zone 3 - West Ghats Corridor",
        "Zone 4 - North & Coastal Corridors"
    }

    for s in TIRUNELVELI_STATIONS:
        assert s["station_id"].startswith("NEL-")
        assert s["zone_id"] in valid_zones
        assert s["is_transfer_station"] in (0, 1)
        assert s["platforms_count"] > 0
        # Coordinates must fall within Tirunelveli district boundaries (lat 8.3-9.0, lon 77.3-78.2)
        assert 8.30 <= s["latitude"] <= 9.00, f"Latitude {s['latitude']} out of range for {s['station_name']}"
        assert 77.30 <= s["longitude"] <= 78.20, f"Longitude {s['longitude']} out of range for {s['station_name']}"


def test_tirunelveli_routes():
    """Verify 10 multimodal transit routes, stop references, and operator mappings."""
    assert len(TIRUNELVELI_ROUTES) == 10
    station_id_set = {s["station_id"] for s in TIRUNELVELI_STATIONS}
    operator_id_set = {op["operator_id"] for op in TIRUNELVELI_OPERATORS}

    modes = set()
    for route in TIRUNELVELI_ROUTES:
        assert route["operator_id"] in operator_id_set
        modes.add(route["route_type"])
        assert len(route["stops"]) >= 2, f"Route {route['route_id']} must have at least 2 stops"
        for stop in route["stops"]:
            assert stop in station_id_set, f"Stop {stop} in route {route['route_id']} not in master stations"

    assert "Bus" in modes


def test_bottleneck_stations():
    """Verify chronic bottleneck stations exist in master station catalog."""
    station_id_set = {s["station_id"] for s in TIRUNELVELI_STATIONS}
    for b_id in TIRUNELVELI_BOTTLENECK_STATIONS:
        assert b_id in station_id_set


def test_tirunelveli_data_sources():
    """Verify external data source catalog and attributes."""
    assert len(TIRUNELVELI_DATA_SOURCES) >= 4
    for src in TIRUNELVELI_DATA_SOURCES:
        assert "source_id" in src
        assert "source_name" in src
        assert "endpoint_url" in src
        assert "connection_status" in src
        assert "coverage_scope" in src
