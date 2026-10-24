"""Analytics and KPI calculation engine for Tamil Nadu Public Transport Intelligence Platform.
Provides high-performance aggregations, transit reliability indices (TRI),
multimodal performance comparisons, bottleneck identification, and peak-hour metrics.
"""

from datetime import date
from typing import Optional, Dict, Any, List
import pandas as pd
import numpy as np
from config import RELIABILITY_TIERS
from src.db import execute_query


def calculate_reliability_score(on_time_pct: float, severe_pct: float, avg_delay: float) -> float:
    """Calculates the Transit Reliability Index (TRI) on a scale of 0 to 100.
    
    Formula:
        TRI = (On-Time % * 0.70) + ((100 - Severe %) * 0.30) - (max(0, Avg Delay) * 1.5)
    Bound between 0.0 and 100.0.
    """
    if pd.isna(on_time_pct) or on_time_pct is None:
        return 0.0
    severe_pct = 0.0 if pd.isna(severe_pct) else severe_pct
    avg_delay = 0.0 if pd.isna(avg_delay) else avg_delay

    base_score = (on_time_pct * 0.70) + ((100.0 - severe_pct) * 0.30)
    penalty = max(0.0, avg_delay) * 1.5
    final_score = max(0.0, min(100.0, base_score - penalty))
    return round(float(final_score), 1)


def get_tier_info(tri_score: float) -> Dict[str, Any]:
    """Returns tier classification, color, and description for a given TRI score."""
    for tier, info in RELIABILITY_TIERS.items():
        if tri_score >= info["min"]:
            return {
                "tier": tier,
                "color": info["color"],
                "badge": info["badge"],
                "score": tri_score
            }
    return {
        "tier": "Critical",
        "color": "#EF4444",
        "badge": "Severe Degradation",
        "score": tri_score
    }


def load_transit_facts() -> pd.DataFrame:
    """Loads all actual arrival observations joined with routes, stations, and operators."""
    sql = """
    SELECT 
        a.record_id,
        a.trip_id,
        t.route_id,
        r.route_short_name,
        r.route_long_name,
        r.route_type,
        r.operator_id,
        r.color_hex,
        a.station_id,
        s.station_code,
        s.station_name,
        s.latitude,
        s.longitude,
        s.zone_id,
        s.is_transfer_station,
        s.platforms_count,
        s.accessible_modes,
        a.stop_sequence,
        a.scheduled_arrival,
        a.actual_arrival,
        a.delay_minutes,
        a.status,
        a.delay_reason,
        a.recorded_date,
        a.hour_of_day,
        a.time_period,
        a.is_peak_hour,
        a.is_weekend,
        a.day_of_week,
        a.provenance
    FROM actual_times a
    JOIN trips t ON a.trip_id = t.trip_id
    JOIN routes r ON t.route_id = r.route_id
    JOIN stations s ON a.station_id = s.station_id
    """
    return execute_query(sql)


def filter_dataset(
    df: pd.DataFrame,
    routes: Optional[List[str]] = None,
    time_periods: Optional[List[str]] = None,
    transport_modes: Optional[List[str]] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    service_type: Optional[str] = "All"
) -> pd.DataFrame:
    """Applies interactive filter criteria to transit facts dataframe."""
    filtered = df.copy()

    if routes:
        filtered = filtered[filtered["route_short_name"].isin(routes)]

    if time_periods:
        filtered = filtered[filtered["time_period"].isin(time_periods)]

    if transport_modes and "route_type" in filtered.columns:
        filtered = filtered[filtered["route_type"].isin(transport_modes)]

    if start_date:
        filtered = filtered[pd.to_datetime(filtered["recorded_date"]).dt.date >= start_date]

    if end_date:
        filtered = filtered[pd.to_datetime(filtered["recorded_date"]).dt.date <= end_date]

    if service_type == "Weekday Only":
        filtered = filtered[filtered["is_weekend"] == 0]
    elif service_type == "Weekend Only":
        filtered = filtered[filtered["is_weekend"] == 1]

    return filtered


def get_executive_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Computes headline executive KPIs from filtered transit dataframe."""
    total_stops = len(df)
    if total_stops == 0:
        return {
            "total_trips": 0,
            "total_stops": 0,
            "avg_delay_minutes": 0.0,
            "on_time_pct": 0.0,
            "severe_delay_count": 0,
            "severe_delay_pct": 0.0,
            "tri_score": 0.0,
            "tier_info": get_tier_info(0.0),
            "status_counts": {}
        }

    total_trips = df["trip_id"].nunique()
    avg_delay = round(float(df["delay_minutes"].mean()), 2)
    on_time_mask = df["status"].isin(["On-Time", "Early"])
    on_time_count = int(on_time_mask.sum())
    on_time_pct = round(100.0 * on_time_count / total_stops, 1)

    severe_mask = df["status"] == "Severe Delay"
    severe_count = int(severe_mask.sum())
    severe_pct = round(100.0 * severe_count / total_stops, 1)

    tri = calculate_reliability_score(on_time_pct, severe_pct, avg_delay)
    tier = get_tier_info(tri)

    status_counts = df["status"].value_counts().to_dict()

    return {
        "total_trips": total_trips,
        "total_stops": total_stops,
        "avg_delay_minutes": avg_delay,
        "on_time_pct": on_time_pct,
        "severe_delay_count": severe_count,
        "severe_delay_pct": severe_pct,
        "tri_score": tri,
        "tier_info": tier,
        "status_counts": status_counts
    }


def get_multimodal_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Computes comparative metrics across transport modes (Bus, Metro, Suburban)."""
    if df.empty or "route_type" not in df.columns:
        return pd.DataFrame()

    def agg_mode(group):
        total = len(group)
        on_time = int(group["status"].isin(["On-Time", "Early"]).sum())
        severe = int((group["status"] == "Severe Delay").sum())
        on_time_pct = round(100.0 * on_time / total, 1)
        severe_pct = round(100.0 * severe / total, 1)
        avg_delay = round(float(group["delay_minutes"].mean()), 2)
        tri = calculate_reliability_score(on_time_pct, severe_pct, avg_delay)
        return pd.Series({
            "Trips Operated": group["trip_id"].nunique(),
            "Arrivals Monitored": total,
            "Avg Delay (min)": avg_delay,
            "On-Time SLA %": on_time_pct,
            "Severe Delays": severe,
            "Reliability Score (TRI)": tri
        })

    summary = df.groupby("route_type", as_index=False).apply(agg_mode, include_groups=False)
    return summary


def get_route_performance_table(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates route performance and ranks routes by Reliability Index."""
    if df.empty:
        return pd.DataFrame()

    def agg_route(group):
        total = len(group)
        on_time = int(group["status"].isin(["On-Time", "Early"]).sum())
        severe = int((group["status"] == "Severe Delay").sum())
        on_time_pct = round(100.0 * on_time / total, 1)
        severe_pct = round(100.0 * severe / total, 1)
        avg_delay = round(float(group["delay_minutes"].mean()), 2)
        tri = calculate_reliability_score(on_time_pct, severe_pct, avg_delay)
        return pd.Series({
            "Route Type": group["route_type"].iloc[0],
            "Color": group["color_hex"].iloc[0],
            "Total Stops": total,
            "Avg Delay (min)": avg_delay,
            "On-Time %": on_time_pct,
            "Severe Delays": severe,
            "Severe %": severe_pct,
            "Reliability Index (TRI)": tri
        })

    summary = df.groupby("route_short_name", as_index=False).apply(agg_route, include_groups=False)
    summary = summary.sort_values(by="Reliability Index (TRI)", ascending=False).reset_index(drop=True)
    summary["Rank"] = range(1, len(summary) + 1)
    return summary


def get_station_ranking_table(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Ranks stations by average delay to identify transit bottlenecks."""
    if df.empty:
        return pd.DataFrame()

    def agg_station(group):
        total = len(group)
        on_time = int(group["status"].isin(["On-Time", "Early"]).sum())
        severe = int((group["status"] == "Severe Delay").sum())
        avg_delay = round(float(group["delay_minutes"].mean()), 2)
        peak_records = group[group["is_peak_hour"] == 1]
        peak_delay = round(float(peak_records["delay_minutes"].mean()), 2) if not peak_records.empty else avg_delay

        return pd.Series({
            "Station Code": group["station_code"].iloc[0],
            "Zone": group["zone_id"].iloc[0],
            "Latitude": group["latitude"].iloc[0],
            "Longitude": group["longitude"].iloc[0],
            "Transfer Station": "Yes" if group["is_transfer_station"].iloc[0] == 1 else "No",
            "Total Arrivals": total,
            "Avg Delay (min)": avg_delay,
            "Peak Delay (min)": peak_delay,
            "On-Time %": round(100.0 * on_time / total, 1),
            "Severe Incidents": severe
        })

    summary = df.groupby("station_name", as_index=False).apply(agg_station, include_groups=False)
    summary = summary.sort_values(by="Avg Delay (min)", ascending=False).reset_index(drop=True)
    summary["Bottleneck Rank"] = range(1, len(summary) + 1)
    return summary.head(top_n)


def get_peak_hour_breakdown(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generates hourly delay progression and peak vs off-peak comparison table."""
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()

    hourly = df.groupby("hour_of_day").agg(
        total_trips=("trip_id", "nunique"),
        total_stops=("record_id", "count"),
        avg_delay=("delay_minutes", "mean"),
        on_time_pct=("status", lambda s: round(100.0 * s.isin(["On-Time", "Early"]).mean(), 1)),
        severe_count=("status", lambda s: (s == "Severe Delay").sum())
    ).reset_index()
    hourly["avg_delay"] = hourly["avg_delay"].round(2)

    period_summary = df.groupby("time_period").agg(
        total_stops=("record_id", "count"),
        avg_delay=("delay_minutes", "mean"),
        on_time_pct=("status", lambda s: round(100.0 * s.isin(["On-Time", "Early"]).mean(), 1)),
        severe_count=("status", lambda s: (s == "Severe Delay").sum())
    ).reset_index()
    period_summary["avg_delay"] = period_summary["avg_delay"].round(2)
    period_summary["severe_pct"] = (100.0 * period_summary["severe_count"] / period_summary["total_stops"]).round(1)

    return hourly, period_summary


def get_daily_trends(df: pd.DataFrame) -> pd.DataFrame:
    """Generates daily timeline with 7-day rolling moving average of delays."""
    if df.empty:
        return pd.DataFrame()

    daily = df.groupby("recorded_date").agg(
        day_of_week=("day_of_week", "first"),
        is_weekend=("is_weekend", "first"),
        total_trips=("trip_id", "nunique"),
        total_stops=("record_id", "count"),
        avg_delay=("delay_minutes", "mean"),
        on_time_pct=("status", lambda s: round(100.0 * s.isin(["On-Time", "Early"]).mean(), 1)),
        severe_pct=("status", lambda s: round(100.0 * (s == "Severe Delay").mean(), 1))
    ).reset_index()

    daily["avg_delay"] = daily["avg_delay"].round(2)
    daily["recorded_date"] = pd.to_datetime(daily["recorded_date"])
    daily = daily.sort_values(by="recorded_date").reset_index(drop=True)
    daily["rolling_7day_delay"] = daily["avg_delay"].rolling(window=7, min_periods=1).mean().round(2)
    daily["tri_score"] = [
        calculate_reliability_score(r["on_time_pct"], r["severe_pct"], r["avg_delay"])
        for _, r in daily.iterrows()
    ]
    return daily


def get_delay_reasons(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates delay root causes excluding normal operations."""
    if df.empty:
        return pd.DataFrame()

    incident_df = df[df["delay_reason"] != "Normal Operations"]
    if incident_df.empty:
        return pd.DataFrame()

    reasons = incident_df.groupby("delay_reason").agg(
        incidents=("record_id", "count"),
        avg_delay=("delay_minutes", "mean"),
        total_delay=("delay_minutes", "sum")
    ).reset_index()

    total_incidents = len(incident_df)
    reasons["pct_of_incidents"] = (100.0 * reasons["incidents"] / total_incidents).round(1)
    reasons["avg_delay"] = reasons["avg_delay"].round(2)
    reasons["total_delay"] = reasons["total_delay"].round(1)
    return reasons.sort_values(by="total_delay", ascending=False).reset_index(drop=True)
