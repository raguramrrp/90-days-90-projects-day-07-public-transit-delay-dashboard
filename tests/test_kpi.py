"""Test suite for KPI thresholds, delay classification, and Reliability Score."""

import pytest
from src.generator import classify_delay_status, determine_time_period
from src.analytics import calculate_reliability_score, get_tier_info


def test_classify_delay_status():
    """Verify standard transit delay classifications."""
    assert classify_delay_status(-2.5) == "Early"
    assert classify_delay_status(-0.1) == "Early"
    assert classify_delay_status(0.0) == "On-Time"
    assert classify_delay_status(1.5) == "On-Time"
    assert classify_delay_status(2.0) == "On-Time"
    assert classify_delay_status(2.1) == "Minor Delay"
    assert classify_delay_status(5.0) == "Minor Delay"
    assert classify_delay_status(5.1) == "Moderate Delay"
    assert classify_delay_status(15.0) == "Moderate Delay"
    assert classify_delay_status(15.1) == "Severe Delay"
    assert classify_delay_status(45.0) == "Severe Delay"


def test_determine_time_period():
    """Verify peak vs off-peak window classifications."""
    period, is_peak = determine_time_period(7)
    assert period == "Morning Peak"
    assert is_peak == 1

    period, is_peak = determine_time_period(9)
    assert period == "Morning Peak"
    assert is_peak == 1

    period, is_peak = determine_time_period(12)
    assert period == "Off-Peak (Midday)"
    assert is_peak == 0

    period, is_peak = determine_time_period(17)
    assert period == "Evening Peak"
    assert is_peak == 1

    period, is_peak = determine_time_period(22)
    assert period == "Night / Early Morning"
    assert is_peak == 0


def test_calculate_reliability_score_perfect():
    """100% on-time, 0% severe, 0 avg delay should yield 100 TRI."""
    score = calculate_reliability_score(100.0, 0.0, 0.0)
    assert score == 100.0


def test_calculate_reliability_score_bounds():
    """Score should always stay bounded between 0.0 and 100.0."""
    # Extreme worst case
    worst_score = calculate_reliability_score(0.0, 100.0, 45.0)
    assert worst_score == 0.0
    assert worst_score >= 0.0

    # Normal case
    normal_score = calculate_reliability_score(85.0, 2.0, 2.5)
    assert 70.0 <= normal_score <= 100.0


def test_get_tier_info():
    """Verify tier assignments based on TRI score."""
    high_tier = get_tier_info(92.0)
    assert high_tier["tier"] == "High"
    assert high_tier["color"] == "#10B981"

    acc_tier = get_tier_info(75.0)
    assert acc_tier["tier"] == "Acceptable"

    attn_tier = get_tier_info(55.0)
    assert attn_tier["tier"] == "Needs Attention"

    crit_tier = get_tier_info(35.0)
    assert crit_tier["tier"] == "Critical"
