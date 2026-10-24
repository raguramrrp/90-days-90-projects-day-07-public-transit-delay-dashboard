"""Unit tests for the modular provider architecture.
Verifies geographic eligibility, stop search, train number validation,
Tirunelveli coverage checks, honest data freshness classification, and geocoding.
"""

import pytest
from src.providers import (
    DataFreshness,
    BusStopProvider,
    BusRouteProvider,
    BusTrackingProvider,
    TrainScheduleProvider,
    TrainRunningStatusProvider,
    GeocodingProvider,
    haversine_distance_km
)
from src.tirunelveli_data import TIRUNELVELI_BOUNDS


def test_data_freshness_tiers():
    """Verify all required freshness classification tiers exist with correct metadata."""
    assert DataFreshness.LIVE.value == "LIVE"
    assert DataFreshness.RECENT.value == "RECENT"
    assert DataFreshness.SCHEDULED.value == "SCHEDULED"
    assert DataFreshness.ESTIMATED.value == "ESTIMATED"
    assert DataFreshness.STATIC.value == "STATIC"
    assert DataFreshness.UNAVAILABLE.value == "UNAVAILABLE"

    for tier in DataFreshness:
        assert tier.label
        assert tier.color.startswith("#")
        assert tier.description


def test_haversine_distance():
    """Verify distance calculation between known Tirunelveli coordinates."""
    # Junction (8.7303, 77.6946) to Vannarpettai (8.7270, 77.7120) is approx 1.95 - 2.05 km
    dist = haversine_distance_km(8.7303, 77.6946, 8.7270, 77.7120)
    assert 1.5 <= dist <= 2.5


def test_bus_stop_provider_search_and_proximity():
    """Verify bus stop provider search by English, Tamil, and proximity."""
    provider = BusStopProvider()
    stops = provider.get_all_stops()
    assert len(stops) == 20

    # Search by English keyword
    results_jct = provider.search_stops("Junction")
    assert len(results_jct) >= 1
    assert any("Junction" in s["station_name"] for s in results_jct)

    # Search by Tamil keyword
    results_ta = provider.search_stops("மருத்துவக்")
    assert len(results_ta) >= 1
    assert "Medical College" in results_ta[0]["station_name"]

    # Proximity query near Vannarpettai
    nearest = provider.find_nearest_stops(8.7270, 77.7120, limit=3)
    assert len(nearest) == 3
    assert nearest[0]["station_code"] == "VNR"
    assert nearest[0]["distance_km"] < 0.2

    # Geographic boundary check
    assert provider.is_stop_in_tirunelveli(8.7303, 77.6946) is True
    # Chennai coordinates (13.08, 80.27) must return False
    assert provider.is_stop_in_tirunelveli(13.08, 80.27) is False


def test_bus_route_eligibility():
    """Verify bus routes enforce geographic eligibility within Tirunelveli."""
    route_provider = BusRouteProvider()
    routes = route_provider.get_all_routes()
    assert len(routes) == 6

    for r in routes:
        assert route_provider.is_route_eligible(r["route_id"]) is True

    # Check routes serving Tirunelveli Junction (NEL-01)
    jct_routes = route_provider.get_routes_for_stop("NEL-01")
    assert len(jct_routes) >= 3
    route_ids = [r["route_id"] for r in jct_routes]
    assert "TNSTC-R1" in route_ids
    assert "TNSTC-R2" in route_ids

    # Check direct route between Junction (NEL-01) and Palayamkottai (NEL-07)
    direct_routes = route_provider.find_routes_between("NEL-01", "NEL-07")
    assert len(direct_routes) >= 1
    assert direct_routes[0]["route_id"] == "TNSTC-R1"


def test_train_number_format_validation():
    """Verify train number input validation rules."""
    tp = TrainScheduleProvider()

    # Valid 5-digit inputs
    valid, res = tp.validate_train_number_format("12632")
    assert valid is True
    assert res == "12632"

    valid, res = tp.validate_train_number_format(" 20666 ")
    assert valid is True
    assert res == "20666"

    # Invalid inputs
    valid, err = tp.validate_train_number_format("12")
    assert valid is False
    assert "5-digit" in err

    valid, err = tp.validate_train_number_format("ABCDE")
    assert valid is False
    assert "5-digit" in err

    valid, err = tp.validate_train_number_format("")
    assert valid is False


def test_train_tirunelveli_eligibility_enforcement():
    """Verify primary local results include ONLY trains serving Tirunelveli."""
    tp = TrainScheduleProvider()

    # 1. Eligible Tirunelveli Train: Nellai Superfast Express (12632)
    t12632 = tp.lookup_train("12632")
    assert t12632["success"] is True
    assert t12632["serves_tirunelveli"] is True
    assert "Nellai" in t12632["train_name"]
    assert t12632["origin_code"] == "TEN"
    assert t12632["dest_code"] == "MS"
    assert t12632["default_platform"] == "1"
    assert len(t12632["key_halts"]) > 0

    # 2. Eligible Vande Bharat Express (20666)
    t20666 = tp.lookup_train("20666")
    assert t20666["success"] is True
    assert t20666["serves_tirunelveli"] is True
    assert "Vande Bharat" in t20666["train_name"]

    # 3. Eligible Tiruchendur Passenger Special (06682)
    t06682 = tp.lookup_train("06682")
    assert t06682["success"] is True
    assert t06682["serves_tirunelveli"] is True

    # 4. Valid Indian Railways train outside Tirunelveli: Tamil Nadu Express (12621)
    t12621 = tp.lookup_train("12621")
    assert t12621["success"] is True
    assert t12621["serves_tirunelveli"] is False
    assert "Tamil Nadu" in t12621["train_name"]
    assert "outside" in t12621["coverage_message"].lower() or "not" in t12621["coverage_message"].lower()

    # 5. Non-local Shatabdi Express (12007)
    t12007 = tp.lookup_train("12007")
    assert t12007["success"] is True
    assert t12007["serves_tirunelveli"] is False

    # 6. Unknown train number (99999)
    t_unknown = tp.lookup_train("99999")
    assert t_unknown["success"] is False
    assert t_unknown["is_unknown"] is True


def test_train_running_status_honest_classification():
    """Verify train running status does NOT fabricate fake live data in production mode."""
    rsp = TrainRunningStatusProvider()

    # Production mode: Must return SCHEDULED
    prod_status = rsp.get_running_status("12632", demo_mode=False)
    assert prod_status["success"] is True
    assert prod_status["data_freshness"] == DataFreshness.SCHEDULED
    assert "timetable" in prod_status["freshness_note"].lower() or "official" in prod_status["freshness_note"].lower()

    # Demo mode: Returns ESTIMATED / SIMULATED
    demo_status = rsp.get_running_status("12632", demo_mode=True)
    assert demo_status["success"] is True
    assert demo_status["data_freshness"] == DataFreshness.ESTIMATED


def test_geocoding_landmark_resolution():
    """Verify local landmark geocoding resolution."""
    jct = GeocodingProvider.resolve_location("Tirunelveli Junction")
    assert jct is not None
    assert round(jct[0], 2) == 8.73
    assert round(jct[1], 2) == 77.69

    vbs = GeocodingProvider.resolve_location("New Bus Stand")
    assert vbs is not None
    assert round(vbs[0], 2) == 8.70
    assert round(vbs[1], 2) == 77.73

    assert GeocodingProvider.resolve_location("Unknown Place In Another State") is None


def test_stitch_additional_trains():
    """Verify Stitch-specific train routes and coverage exceptions."""
    tp = TrainScheduleProvider()
    rsp = TrainRunningStatusProvider(tp)

    # 1. 16847 Mayiladuturai - Sengottai Express
    t16847 = tp.lookup_train("16847")
    assert t16847["success"] is True
    assert t16847["serves_tirunelveli"] is True
    assert "Mayiladuturai" in t16847["train_name"]

    # Running status includes motive power and block location
    status_16847 = rsp.get_running_status("16847", demo_mode=True)
    assert "WAP-4" in status_16847["motive_unit"]

    # 2. 20635 Ananthapuri SF
    t20635 = tp.lookup_train("20635")
    assert t20635["success"] is True
    assert t20635["serves_tirunelveli"] is True
    assert "Ananthapuri" in t20635["train_name"]

    # 3. 12626 Kerala Express (Non-local exception)
    t12626 = tp.lookup_train("12626")
    assert t12626["success"] is True
    assert t12626["serves_tirunelveli"] is False
    assert "Kerala" in t12626["train_name"]
    assert "12626" in t12626["coverage_message"]


def test_station_hub_interchanges():
    """Verify Station Hub Explorer metadata and schematic details."""
    provider = BusStopProvider()
    hubs = provider.get_all_station_hubs()
    assert len(hubs) >= 4

    ten_hub = provider.get_station_hub("TEN")
    assert ten_hub is not None
    assert ten_hub["train_pfs"] == 5
    assert ten_hub["bus_bays"] == 32
    assert ten_hub["prepaid_auto"] is True
    assert ten_hub["cloakroom"] is True

    vbs_hub = provider.get_station_hub("NEL-02")
    assert vbs_hub is not None
    assert vbs_hub["bus_bays"] == 48

