"""Public Transit Delay Analytics Dashboard - Main Application.
Interactive transportation analytics platform providing route reliability,
station bottleneck identification, and peak-hour congestion intelligence.
"""

from datetime import datetime, date
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from config import APP_NAME, RELIABILITY_TIERS, TIME_PERIODS
from src.db import check_health, execute_query
from src.etl import TransitETLPipeline
from src.analytics import (
    load_transit_facts,
    filter_dataset,
    get_executive_kpis,
    get_route_performance_table,
    get_station_ranking_table,
    get_peak_hour_breakdown,
    get_daily_trends,
    get_delay_reasons,
    get_tier_info
)
from src.powerbi_export import export_powerbi_star_schema, generate_dax_file

# Streamlit Page Configuration
st.set_page_config(
    page_title="Transit Delay Analytics Dashboard",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Corporate CSS Styling
st.markdown("""
<style>
    /* Top Header */
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 1.4rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.0rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .main-header p {
        margin: 0.25rem 0 0 0;
        color: #94A3B8;
        font-size: 0.92rem;
    }
    .header-pill {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 6px 14px;
        color: #E2E8F0;
        font-size: 0.82rem;
        font-weight: 500;
    }

    /* Cards */
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 1.1rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-label {
        color: #64748B;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-val {
        font-size: 1.85rem;
        font-weight: 700;
        color: #0F172A;
        margin: 0.3rem 0;
    }
    .metric-sub {
        font-size: 0.78rem;
        color: #64748B;
    }

    /* Hero Scorecard */
    .hero-scorecard {
        background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%);
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.4rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        height: 100%;
    }

    /* Quick Diagnostic Box */
    .diagnostic-box {
        background-color: #F8FAFC;
        border-left: 4px solid #3B82F6;
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        margin-top: 1rem;
    }
    .diagnostic-box h4 {
        margin: 0 0 0.4rem 0;
        font-size: 0.9rem;
        color: #1E293B;
    }
    .diagnostic-box p {
        margin: 0;
        font-size: 0.82rem;
        color: #475569;
        line-height: 1.4;
    }

    /* Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 22px;
        font-weight: 600;
        font-size: 0.95rem;
        border-radius: 8px 8px 0 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner="Loading transit performance records...")
def get_cached_transit_data():
    """Fetches transit facts with caching to ensure high responsiveness."""
    health = check_health()
    if not health.get("connected") or health.get("tables", {}).get("actual_times", 0) == 0:
        pipeline = TransitETLPipeline()
        pipeline.run()
    return load_transit_facts()


def refresh_data():
    """Triggers ETL pipeline to reload transit data and refreshes cache."""
    pipeline = TransitETLPipeline()
    pipeline.run()
    st.cache_data.clear()


# Clean Header Banner without live engine / dual engine badges
st.markdown("""
<div class="main-header">
    <div>
        <h1>🚆 Public Transit Delay Analytics Dashboard</h1>
        <p>Metropolitan Transit Authority • Route Reliability, Station Bottlenecks & Peak-Hour Congestion Intelligence</p>
    </div>
    <div>
        <span class="header-pill">📍 Network Status: 6 Corridors • 18 Stations</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Load master transit records
try:
    df_facts = get_cached_transit_data()
except Exception as e:
    st.error(f"Error loading transit database: {e}")
    refresh_data()
    df_facts = get_cached_transit_data()

# ============================================================================
# Sidebar Controls & Global Filters (Database Engine: SQLITE removed)
# ============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/subway.png", width=64)
    st.title("Filters & Controls")
    st.markdown("---")

    all_routes = sorted(df_facts["route_short_name"].unique())
    all_periods = list(TIME_PERIODS.keys())
    min_date = pd.to_datetime(df_facts["recorded_date"]).dt.date.min()
    max_date = pd.to_datetime(df_facts["recorded_date"]).dt.date.max()

    # Route filter
    selected_routes = st.multiselect(
        "Select Transit Routes:",
        options=all_routes,
        default=all_routes,
        help="Filter dashboard metrics to specific metro lines or bus corridors."
    )

    # Time Period filter
    selected_periods = st.multiselect(
        "Select Time Periods:",
        options=all_periods,
        default=all_periods,
        help="Analyze peak vs off-peak performance windows."
    )

    # Service Window filter
    service_type = st.radio(
        "Service Window:",
        options=["All", "Weekday Only", "Weekend Only"],
        horizontal=True
    )

    # Date Range filter
    date_range = st.date_input(
        "Analysis Date Window:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            refresh_data()
            st.rerun()
    with col_btn2:
        if st.button("⚡ Export Data", use_container_width=True):
            export_powerbi_star_schema()
            generate_dax_file()
            st.success("Exported Data Models!")

    st.markdown("---")
    st.caption(f"**Monitored Observations:** `{len(df_facts):,} Records`")
    st.caption(f"**Tracked Trips:** `{df_facts['trip_id'].nunique():,} Trips`")


# Apply Filters
df_filtered = filter_dataset(
    df_facts,
    routes=selected_routes,
    time_periods=selected_periods,
    start_date=start_date,
    end_date=end_date,
    service_type=service_type
)

if df_filtered.empty:
    st.warning("No transit records match the selected filter criteria. Please broaden your filter selections.")
    st.stop()

# Compute Executive KPIs
kpis = get_executive_kpis(df_filtered)

# ============================================================================
# Main Navigation Tabs (4 Core Pages - Power BI & SQL Hub tab removed)
# ============================================================================
tabs = st.tabs([
    "📊 Overview",
    "🚏 Route Analysis",
    "📍 Station Bottlenecks",
    "⏰ Peak Hours & Congestion"
])

# ----------------------------------------------------------------------------
# PAGE 1: OVERVIEW (Redesigned Layout & Rearranged Positions)
# ----------------------------------------------------------------------------
with tabs[0]:
    # Section A: Prominent Top Split (Reliability Scorecard on Left, 30-Day Trend on Right)
    col_hero, col_trend = st.columns([4, 8])

    with col_hero:
        tier = kpis['tier_info']
        st.markdown(f"""
        <div class="hero-scorecard" style="border-top: 5px solid {tier['color']};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="metric-label">Transit Reliability Index</span>
                <span style="background-color: {tier['color']}18; color: {tier['color']}; padding: 3px 8px; border-radius: 6px; font-weight: 600; font-size: 0.78rem;">
                    {tier['tier'].upper()}
                </span>
            </div>
            <div style="font-size: 3.2rem; font-weight: 800; color: {tier['color']}; margin: 0.5rem 0;">
                {kpis['tri_score']}<span style="font-size: 1.2rem; color: #94A3B8; font-weight: 500;"> / 100</span>
            </div>
            <div style="font-size: 0.88rem; color: #475569; font-weight: 500;">
                {tier['badge']} • Target SLA: ≥ 85.0
            </div>
            <div class="diagnostic-box">
                <h4>⚡ Fleet Quick Diagnostics</h4>
                <p>• <strong>Fleet On-Time Rate:</strong> {kpis['on_time_pct']}% of arrivals on schedule.</p>
                <p>• <strong>Average Delay:</strong> {kpis['avg_delay_minutes']} mins mean deviation.</p>
                <p>• <strong>Severe Incidents:</strong> {kpis['severe_delay_count']} occurrences (>15m).</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_trend:
        st.markdown("##### 📈 30-Day Fleet Delay Trend & Moving Average Timeline")
        daily_trend = get_daily_trends(df_filtered)
        if not daily_trend.empty:
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Bar(
                x=daily_trend["recorded_date"],
                y=daily_trend["avg_delay"],
                name="Daily Avg Delay (mins)",
                marker_color="#CBD5E1",
                opacity=0.75
            ))
            fig_trend.add_trace(go.Scatter(
                x=daily_trend["recorded_date"],
                y=daily_trend["rolling_7day_delay"],
                mode="lines",
                name="7-Day Moving Avg",
                line=dict(color="#2563EB", width=3)
            ))
            fig_trend.add_hline(y=3.0, line_dash="dash", line_color="#10B981", annotation_text="Target SLA (3.0m)")
            fig_trend.update_layout(
                xaxis_title="Recorded Date",
                yaxis_title="Delay (Minutes)",
                hovermode="x unified",
                template="plotly_white",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=20, r=20, t=10, b=20),
                height=310
            )
            st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Section B: Rearranged Metric Cards Ribbon
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Volume Monitored</div>
            <div class="metric-val">{kpis['total_trips']:,}</div>
            <div class="metric-sub">{kpis['total_stops']:,} Stop Arrivals Recorded</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        ot_col = "#10B981" if kpis['on_time_pct'] >= 80 else "#F59E0B"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">On-Time Arrival SLA</div>
            <div class="metric-val" style="color: {ot_col};">{kpis['on_time_pct']}%</div>
            <div class="metric-sub">≤ 2 mins of Scheduled Timetable</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        avg_col = "#10B981" if kpis['avg_delay_minutes'] <= 3.0 else "#EF4444"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Fleet Average Delay</div>
            <div class="metric-val" style="color: {avg_col};">{kpis['avg_delay_minutes']} <span style="font-size: 1rem;">min</span></div>
            <div class="metric-sub">Mean Variance Across Network</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Severe Delays (>15m)</div>
            <div class="metric-val" style="color: #EF4444;">{kpis['severe_delay_count']:,}</div>
            <div class="metric-sub">{kpis['severe_delay_pct']}% Critical Incident Share</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Section C: Performance Breakdown & Delay Root Causes (Side-by-Side)
    col_dist, col_reasons = st.columns([5, 7])

    with col_dist:
        st.markdown("##### 🎯 Arrival Performance Distribution")
        status_counts = df_filtered["status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]

        status_color_map = {
            "Early": "#059669",
            "On-Time": "#10B981",
            "Minor Delay": "#FBBF24",
            "Moderate Delay": "#F97316",
            "Severe Delay": "#EF4444"
        }
        fig_donut = px.pie(
            status_counts,
            values="Count",
            names="Status",
            hole=0.6,
            color="Status",
            color_discrete_map=status_color_map
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label')
        fig_donut.update_layout(
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
            annotations=[dict(text=f"{kpis['on_time_pct']}%<br><span style='font-size:11px;color:#64748B;'>On-Time</span>", x=0.5, y=0.5, font_size=18, showarrow=False)]
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_reasons:
        st.markdown("##### 🔍 Primary Delay Root Causes (Minutes Lost)")
        reasons_df = get_delay_reasons(df_filtered)
        if not reasons_df.empty:
            fig_reasons = px.bar(
                reasons_df,
                x="total_delay",
                y="delay_reason",
                orientation="h",
                text="total_delay",
                color="avg_delay",
                color_continuous_scale="Reds",
                labels={"total_delay": "Cumulative Minutes Lost", "delay_reason": "Identified Cause", "avg_delay": "Avg Delay/Incident"}
            )
            fig_reasons.update_traces(texttemplate='%{text:.1f}m', textposition='outside')
            fig_reasons.update_layout(
                template="plotly_white",
                yaxis=dict(autorange="reversed"),
                height=320,
                margin=dict(l=20, r=20, t=10, b=20)
            )
            st.plotly_chart(fig_reasons, use_container_width=True)


# ----------------------------------------------------------------------------
# PAGE 2: ROUTE ANALYSIS (Redesigned Layout & Rearranged Positions)
# ----------------------------------------------------------------------------
with tabs[1]:
    st.subheader("🚏 Transit Route Reliability & Performance Ranking")

    route_table = get_route_performance_table(df_filtered)

    if not route_table.empty:
        # Top Interactive Route Inspector Ribbon
        st.markdown("##### 🔎 Route Deep-Dive Inspector")
        sel_c1, sel_c2, sel_c3, sel_c4 = st.columns([4, 2.5, 2.5, 3])
        
        with sel_c1:
            selected_route_inspect = st.selectbox(
                "Select Route to Inspect:",
                options=route_table["route_short_name"].tolist(),
                key="route_inspector_redesign"
            )
        
        route_specific_df = df_filtered[df_filtered["route_short_name"] == selected_route_inspect]
        
        with sel_c2:
            st.metric("Route Avg Delay", f"{route_specific_df['delay_minutes'].mean():.2f} min")
        with sel_c3:
            r_ot = 100.0 * route_specific_df['status'].isin(['On-Time', 'Early']).mean()
            st.metric("On-Time SLA", f"{r_ot:.1f}%")
        with sel_c4:
            st.metric("Trips Monitored", f"{route_specific_df['trip_id'].nunique():,}")

        # Stop-by-Stop Delay Cascading Profile placed prominently right below the selector!
        st.markdown("##### 🌊 Stop-by-Stop Delay Cascading Profile Along Selected Corridor")
        stop_cascade = route_specific_df.groupby(["stop_sequence", "station_name"]).agg(
            avg_delay=("delay_minutes", "mean"),
            trips_count=("record_id", "count")
        ).reset_index().sort_values(by="stop_sequence")

        fig_cascade = px.area(
            stop_cascade,
            x="station_name",
            y="avg_delay",
            markers=True,
            line_shape="spline",
            text="avg_delay",
            labels={"station_name": "Station Stop Sequence", "avg_delay": "Cumulative Avg Delay (min)"}
        )
        fig_cascade.update_traces(
            texttemplate='%{text:.2f}m',
            textposition='top center',
            line_color="#2563EB",
            fillcolor="rgba(37, 99, 235, 0.12)"
        )
        fig_cascade.update_layout(
            template="plotly_white",
            height=280,
            margin=dict(l=20, r=20, t=20, b=30)
        )
        st.plotly_chart(fig_cascade, use_container_width=True)

        st.markdown("---")

        # Bottom Split: TRI Leaderboard & League Table
        col_bar, col_tbl = st.columns([5, 7])

        with col_bar:
            st.markdown("##### 📊 Route Reliability Index (TRI) Leaderboard")
            fig_routes = px.bar(
                route_table,
                x="Reliability Index (TRI)",
                y="route_short_name",
                orientation="h",
                text="Reliability Index (TRI)",
                color="Reliability Index (TRI)",
                color_continuous_scale="Tealgrn",
                labels={"route_short_name": "Route"}
            )
            fig_routes.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            fig_routes.update_layout(
                yaxis=dict(autorange="reversed"),
                template="plotly_white",
                height=320,
                margin=dict(l=10, r=20, t=10, b=10)
            )
            st.plotly_chart(fig_routes, use_container_width=True)

        with col_tbl:
            st.markdown("##### 📋 Route Performance League Matrix")
            st.dataframe(
                route_table[[
                    "Rank", "route_short_name", "Route Type", "Total Stops",
                    "Avg Delay (min)", "On-Time %", "Severe %", "Reliability Index (TRI)"
                ]].rename(columns={"route_short_name": "Route Name"}),
                hide_index=True,
                use_container_width=True
            )


# ----------------------------------------------------------------------------
# PAGE 3: STATION BOTTLENECKS (Redesigned Layout & Rearranged Positions)
# ----------------------------------------------------------------------------
with tabs[2]:
    st.subheader("📍 Station Bottleneck Identification & Network Hotspots")

    top_stations = get_station_ranking_table(df_filtered, top_n=12)

    if not top_stations.empty:
        # Top Fare Zone Metric Cards
        z1 = df_filtered[df_filtered["zone_id"] == "Zone 1"]["delay_minutes"].mean()
        z2 = df_filtered[df_filtered["zone_id"] == "Zone 2"]["delay_minutes"].mean()
        z3 = df_filtered[df_filtered["zone_id"] == "Zone 3"]["delay_minutes"].mean()

        zc1, zc2, zc3 = st.columns(3)
        zc1.metric("Zone 1 (Core Urban Downtown)", f"{z1:.2f} min avg", "High Dwell & Transfer Congestion")
        zc2.metric("Zone 2 (Inner Ring / Suburbs)", f"{z2:.2f} min avg", "Midway Transit Corridors")
        zc3.metric("Zone 3 (Perimeter / Airport)", f"{z3:.2f} min avg", "Terminal & Express Lines")

        st.markdown("<br>", unsafe_allow_html=True)

        # Middle Split: Map on Left, Bottleneck Hotspot Bars on Right
        col_map, col_bar = st.columns([5, 5])

        with col_map:
            st.markdown("##### 🗺️ Geographic Station Delay Map")
            fig_map = px.scatter(
                top_stations,
                x="Longitude",
                y="Latitude",
                size="Avg Delay (min)",
                color="Zone",
                hover_name="station_name",
                hover_data={"Avg Delay (min)": True, "On-Time %": True, "Total Arrivals": True, "Latitude": False, "Longitude": False},
                size_max=36,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig_map.update_layout(
                template="plotly_white",
                height=380,
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_map, use_container_width=True)

        with col_bar:
            st.markdown("##### 🏆 Bottleneck Stations Ranked by Average Delay")
            fig_stn_bar = px.bar(
                top_stations.sort_values(by="Avg Delay (min)", ascending=True),
                x="Avg Delay (min)",
                y="station_name",
                orientation="h",
                text="Avg Delay (min)",
                color="Peak Delay (min)",
                color_continuous_scale="OrRd",
                labels={"station_name": "Station"}
            )
            fig_stn_bar.update_traces(texttemplate='%{text:.2f}m', textposition='outside')
            fig_stn_bar.update_layout(
                template="plotly_white",
                height=380,
                margin=dict(l=10, r=20, t=10, b=10)
            )
            st.plotly_chart(fig_stn_bar, use_container_width=True)

        st.markdown("---")
        st.markdown("##### 📋 Granular Station Bottleneck SLA Compliance Table")
        st.dataframe(
            top_stations[[
                "Bottleneck Rank", "station_name", "Station Code", "Zone",
                "Transfer Station", "Total Arrivals", "Avg Delay (min)", "Peak Delay (min)", "On-Time %", "Severe Incidents"
            ]].rename(columns={"station_name": "Station Name"}),
            hide_index=True,
            use_container_width=True
        )


# ----------------------------------------------------------------------------
# PAGE 4: PEAK HOURS & CONGESTION (Redesigned Layout & Rearranged Positions)
# ----------------------------------------------------------------------------
with tabs[3]:
    st.subheader("⏰ Peak-Hour Surge & Hourly Congestion Dynamics")

    hourly_df, period_df = get_peak_hour_breakdown(df_filtered)

    if not hourly_df.empty:
        # Top Dynamic Congestion Metric Ribbon
        peak_delay = df_filtered[df_filtered["is_peak_hour"] == 1]["delay_minutes"].mean()
        off_peak_delay = df_filtered[df_filtered["is_peak_hour"] == 0]["delay_minutes"].mean()
        surge_delta = peak_delay - off_peak_delay
        surge_ratio = peak_delay / max(0.1, off_peak_delay)
        peak_ontime = 100.0 * df_filtered[df_filtered["is_peak_hour"] == 1]["status"].isin(["On-Time", "Early"]).mean()

        p1, p2, p3, p4 = st.columns(4)
        p1.metric("Peak Hour Delay", f"{peak_delay:.2f} min", delta=f"+{surge_delta:.2f}m vs Off-Peak", delta_color="inverse")
        p2.metric("Off-Peak Average Delay", f"{off_peak_delay:.2f} min")
        p3.metric("Congestion Surge Ratio", f"{surge_ratio:.2f}x", help="Ratio of peak delay to off-peak delay")
        p4.metric("Peak On-Time SLA", f"{peak_ontime:.1f}%")

        st.markdown("<br>", unsafe_allow_html=True)

        # Day-of-Week vs. Hour Congestion Heatmap Matrix placed FIRST for immediate pattern recognition!
        st.markdown("##### 🔥 Day of Week vs. Hour Congestion Heatmap Matrix")
        dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow_pivot = df_filtered.pivot_table(
            index="day_of_week",
            columns="hour_of_day",
            values="delay_minutes",
            aggfunc="mean"
        ).reindex(dow_order)

        fig_heatmap = px.imshow(
            dow_pivot,
            labels=dict(x="Hour of Day", y="Day of Week", color="Avg Delay (min)"),
            x=[f"{h:02d}:00" for h in dow_pivot.columns],
            y=dow_pivot.index,
            color_continuous_scale="YlOrRd",
            aspect="auto"
        )
        fig_heatmap.update_layout(height=310, margin=dict(l=20, r=20, t=10, b=20))
        st.plotly_chart(fig_heatmap, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 24-Hour Congestion Curve with shaded bands
        st.markdown("##### 📊 24-Hour Fleet Congestion Progression Curve")
        fig_hourly = go.Figure()

        fig_hourly.add_vrect(x0=6.5, x1=9.5, fillcolor="#FEF3C7", opacity=0.45, line_width=0, annotation_text="Morning Peak (07-10h)", annotation_position="top left")
        fig_hourly.add_vrect(x0=15.5, x1=19.5, fillcolor="#FEE2E2", opacity=0.45, line_width=0, annotation_text="Evening Peak (16-20h)", annotation_position="top left")

        fig_hourly.add_trace(go.Scatter(
            x=hourly_df["hour_of_day"],
            y=hourly_df["avg_delay"],
            mode="lines+markers",
            name="Avg Delay (min)",
            line=dict(color="#DC2626", width=3),
            marker=dict(size=8, color="#DC2626")
        ))
        fig_hourly.add_trace(go.Bar(
            x=hourly_df["hour_of_day"],
            y=hourly_df["total_trips"],
            name="Trips Scheduled",
            yaxis="y2",
            marker_color="#94A3B8",
            opacity=0.35
        ))
        fig_hourly.update_layout(
            xaxis=dict(title="Hour of Day (24-Hour Clock)", tickmode="linear", dtick=1),
            yaxis=dict(title="Average Delay (Minutes)"),
            yaxis2=dict(title="Trips Scheduled", overlaying="y", side="right", showgrid=False),
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=360,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_hourly, use_container_width=True)


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 10px 0;">
    <strong>90 Days – 90 Projects Challenge</strong> • Day 7: Public Transit Delay Analytics Dashboard • Author: <strong>raguramrrp</strong><br>
    Transportation Analytics, Route Reliability & Peak-Hour Congestion Intelligence
</div>
""", unsafe_allow_html=True)
