"""Public Transit Delay Analytics Dashboard - Main Application.
Interactive multi-page transportation analytics platform providing route reliability,
station bottleneck identification, peak-hour delay analytics, and Power BI integration.
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

# Custom CSS Styling for a Modern Corporate Transit Look
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .main-header p {
        margin: 0.3rem 0 0 0;
        color: #94A3B8;
        font-size: 0.95rem;
    }
    .kpi-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 1.2rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
    .kpi-label {
        color: #64748B;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 2.0rem;
        font-weight: 700;
        color: #0F172A;
        margin: 0.4rem 0;
    }
    .kpi-sub {
        font-size: 0.8rem;
        color: #475569;
    }
    .badge-high {
        background-color: #ECFDF5;
        color: #065F46;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
    }
    .badge-warning {
        background-color: #FFFBEB;
        color: #92400E;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
    }
    .badge-critical {
        background-color: #FEF2F2;
        color: #991B1B;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        font-weight: 600;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner="Loading transit performance records...")
def get_cached_transit_data():
    """Fetches transit facts with caching to ensure high responsiveness."""
    health = check_health()
    if not health.get("connected") or health.get("tables", {}).get("actual_times", 0) == 0:
        # Run pipeline if DB is not yet populated
        pipeline = TransitETLPipeline()
        pipeline.run()
    return load_transit_facts()


def refresh_data():
    """Triggers ETL pipeline to reload synthetic data and refreshes cache."""
    pipeline = TransitETLPipeline()
    pipeline.run()
    st.cache_data.clear()


# Header Banner
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1>🚆 Public Transit Delay Analytics Dashboard</h1>
            <p>Metropolitan Transit Authority • Route Reliability, Station Bottlenecks & Peak-Hour Congestion Intelligence</p>
        </div>
        <div style="text-align: right;">
            <span class="badge-high">● LIVE ANALYTICS ENGINE</span>
            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 5px;">PostgreSQL / SQLite Dual Engine</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Load master transit records
try:
    df_facts = get_cached_transit_data()
except Exception as e:
    st.error(f"Error loading transit database: {e}")
    st.info("Initializing database with synthetic transit feed...")
    refresh_data()
    df_facts = get_cached_transit_data()

# ============================================================================
# Sidebar Controls & Global Filters
# ============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/subway.png", width=64)
    st.title("Filters & Controls")
    st.markdown("---")

    # Available options
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
        if st.button("⚡ Export PBI", use_container_width=True):
            export_powerbi_star_schema()
            generate_dax_file()
            st.success("Exported Power BI CSVs!")

    st.markdown("---")
    # Health and Metadata
    db_health = check_health()
    st.caption(f"**Database Engine:** `{db_health.get('engine_type', 'sqlite').upper()}`")
    st.caption(f"**Active Records:** `{len(df_facts):,} Observations`")
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
# Main Navigation Tabs (4 Core Pages + Power BI / SQL Deliverables)
# ============================================================================
tabs = st.tabs([
    "📊 Overview",
    "🚏 Route Analysis",
    "📍 Station Bottlenecks",
    "⏰ Peak Hours & Congestion",
    "💼 Power BI & SQL Hub"
])

# ----------------------------------------------------------------------------
# PAGE 1: OVERVIEW
# ----------------------------------------------------------------------------
with tabs[0]:
    # Top KPI Metric Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Trips</div>
            <div class="kpi-value">{kpis['total_trips']:,}</div>
            <div class="kpi-sub">{kpis['total_stops']:,} Stop Arrivals</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        on_time_color = "#10B981" if kpis['on_time_pct'] >= 80 else "#F59E0B"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">On-Time Arrival Rate</div>
            <div class="kpi-value" style="color: {on_time_color};">{kpis['on_time_pct']}%</div>
            <div class="kpi-sub">≤ 2 mins or Early</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        avg_delay_color = "#10B981" if kpis['avg_delay_minutes'] < 3.0 else "#EF4444"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Average Delay</div>
            <div class="kpi-value" style="color: {avg_delay_color};">{kpis['avg_delay_minutes']} <span style="font-size: 1rem;">min</span></div>
            <div class="kpi-sub">Mean Fleet Variance</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Severe Delays (>15m)</div>
            <div class="kpi-value" style="color: #EF4444;">{kpis['severe_delay_count']:,}</div>
            <div class="kpi-sub">{kpis['severe_delay_pct']}% of Total Arrivals</div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        tier = kpis['tier_info']
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid {tier['color']};">
            <div class="kpi-label">Reliability Index (TRI)</div>
            <div class="kpi-value" style="color: {tier['color']};">{kpis['tri_score']}<span style="font-size: 1rem;">/100</span></div>
            <div class="kpi-sub" style="font-weight: 600; color: {tier['color']};">{tier['tier']} ({tier['badge']})</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: 30-Day Trend Chart & Delay Distribution
    col_trend, col_dist = st.columns([7, 3])

    with col_trend:
        st.subheader("📈 Fleet Delay Trend & 7-Day Rolling Average")
        daily_trend = get_daily_trends(df_filtered)
        if not daily_trend.empty:
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Bar(
                x=daily_trend["recorded_date"],
                y=daily_trend["avg_delay"],
                name="Daily Avg Delay (mins)",
                marker_color="#94A3B8",
                opacity=0.65
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
                margin=dict(l=20, r=20, t=30, b=20),
                height=350
            )
            st.plotly_chart(fig_trend, use_container_width=True)

    with col_dist:
        st.subheader("🎯 Arrival Performance")
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
            hole=0.55,
            color="Status",
            color_discrete_map=status_color_map
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label')
        fig_donut.update_layout(
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
            height=350
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # Row 3: Root Cause Analysis
    st.subheader("🔍 Primary Delay Root Causes (Excluding Normal Operations)")
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
            labels={"total_delay": "Cumulative Delay Lost (mins)", "delay_reason": "Identified Cause", "avg_delay": "Avg Delay/Incident"}
        )
        fig_reasons.update_traces(texttemplate='%{text:.1f}m', textposition='outside')
        fig_reasons.update_layout(
            template="plotly_white",
            yaxis=dict(autorange="reversed"),
            height=320,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_reasons, use_container_width=True)


# ----------------------------------------------------------------------------
# PAGE 2: ROUTE ANALYSIS
# ----------------------------------------------------------------------------
with tabs[1]:
    st.subheader("🚆 Transit Route Performance & Reliability Ranking")
    route_table = get_route_performance_table(df_filtered)

    if not route_table.empty:
        col_tbl, col_chart = st.columns([6, 4])

        with col_tbl:
            st.markdown("##### Route League Table")
            st.dataframe(
                route_table[[
                    "Rank", "route_short_name", "Route Type", "Total Stops",
                    "Avg Delay (min)", "On-Time %", "Severe %", "Reliability Index (TRI)"
                ]].rename(columns={"route_short_name": "Route Name"}),
                hide_index=True,
                use_container_width=True
            )

        with col_chart:
            st.markdown("##### Transit Reliability Index (TRI) Comparison")
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

        st.markdown("---")
        st.subheader("🔎 Route Deep-Dive & Delay Composition")
        selected_route_inspect = st.selectbox(
            "Select Route to Inspect:",
            options=route_table["route_short_name"].tolist(),
            key="route_inspector"
        )

        route_specific_df = df_filtered[df_filtered["route_short_name"] == selected_route_inspect]
        
        c_r1, c_r2, c_r3 = st.columns(3)
        with c_r1:
            st.metric("Route Avg Delay", f"{route_specific_df['delay_minutes'].mean():.2f} min")
        with c_r2:
            r_on_time = 100.0 * route_specific_df['status'].isin(['On-Time', 'Early']).mean()
            st.metric("Route On-Time Rate", f"{r_on_time:.1f}%")
        with c_r3:
            st.metric("Total Monitored Trips", f"{route_specific_df['trip_id'].nunique():,}")

        # Route stop sequence progression
        st.markdown("##### Stop-by-Stop Delay Cascading Profile")
        stop_cascade = route_specific_df.groupby(["stop_sequence", "station_name"]).agg(
            avg_delay=("delay_minutes", "mean"),
            trips_count=("record_id", "count")
        ).reset_index().sort_values(by="stop_sequence")

        fig_cascade = px.line(
            stop_cascade,
            x="station_name",
            y="avg_delay",
            markers=True,
            line_shape="spline",
            text="avg_delay",
            labels={"station_name": "Station Stop Order", "avg_delay": "Cumulative Avg Delay (min)"}
        )
        fig_cascade.update_traces(texttemplate='%{text:.2f}m', textposition='top center', line_color="#EA580C", line_width=3)
        fig_cascade.update_layout(template="plotly_white", height=300, margin=dict(l=20, r=20, t=20, b=30))
        st.plotly_chart(fig_cascade, use_container_width=True)


# ----------------------------------------------------------------------------
# PAGE 3: STATION BOTTLENECKS
# ----------------------------------------------------------------------------
with tabs[2]:
    st.subheader("📍 Station Bottleneck Identification & Delay Hotspots")
    
    top_stations = get_station_ranking_table(df_filtered, top_n=12)

    if not top_stations.empty:
        col_map, col_bar = st.columns([5, 5])

        with col_map:
            st.markdown("##### Geographic Delay Map (Bubble Size = Average Delay)")
            fig_map = px.scatter(
                top_stations,
                x="Longitude",
                y="Latitude",
                size="Avg Delay (min)",
                color="Zone",
                hover_name="station_name",
                hover_data={"Avg Delay (min)": True, "On-Time %": True, "Total Arrivals": True, "Latitude": False, "Longitude": False},
                size_max=35,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig_map.update_layout(
                template="plotly_white",
                height=400,
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_map, use_container_width=True)

        with col_bar:
            st.markdown("##### Top Bottleneck Stations by Average Delay")
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
                height=400,
                margin=dict(l=10, r=20, t=10, b=10)
            )
            st.plotly_chart(fig_stn_bar, use_container_width=True)

        st.markdown("---")
        st.markdown("##### Station Bottleneck Rankings & SLA Compliance")
        st.dataframe(
            top_stations[[
                "Bottleneck Rank", "station_name", "Station Code", "Zone",
                "Transfer Station", "Total Arrivals", "Avg Delay (min)", "Peak Delay (min)", "On-Time %", "Severe Incidents"
            ]].rename(columns={"station_name": "Station Name"}),
            hide_index=True,
            use_container_width=True
        )


# ----------------------------------------------------------------------------
# PAGE 4: PEAK HOURS & CONGESTION
# ----------------------------------------------------------------------------
with tabs[3]:
    st.subheader("⏰ Peak-Hour Surge & Hourly Congestion Dynamics")

    hourly_df, period_df = get_peak_hour_breakdown(df_filtered)

    if not hourly_df.empty:
        # Comparison metric cards
        peak_delay = df_filtered[df_filtered["is_peak_hour"] == 1]["delay_minutes"].mean()
        off_peak_delay = df_filtered[df_filtered["is_peak_hour"] == 0]["delay_minutes"].mean()
        surge_delta = peak_delay - off_peak_delay
        surge_ratio = peak_delay / max(0.1, off_peak_delay)

        p1, p2, p3, p4 = st.columns(4)
        p1.metric("Morning & Evening Peak Delay", f"{peak_delay:.2f} min", delta=f"+{surge_delta:.2f} min vs Off-Peak", delta_color="inverse")
        p2.metric("Off-Peak Average Delay", f"{off_peak_delay:.2f} min")
        p3.metric("Peak Congestion Surge Ratio", f"{surge_ratio:.2f}x", help="Ratio of peak delay to off-peak delay")
        
        peak_ontime = 100.0 * df_filtered[df_filtered["is_peak_hour"] == 1]["status"].isin(["On-Time", "Early"]).mean()
        p4.metric("Peak On-Time SLA", f"{peak_ontime:.1f}%")

        st.markdown("<br>", unsafe_allow_html=True)

        # 24-Hour Congestion Curve
        st.markdown("##### 24-Hour Fleet Delay Curve")
        fig_hourly = go.Figure()

        # Add shaded peak hour bands
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
            name="Trips Operated",
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
            height=380,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_hourly, use_container_width=True)

        # Day of Week vs Hour Heatmap
        st.markdown("##### Day of Week vs. Hour Congestion Heatmap Matrix")
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
        fig_heatmap.update_layout(height=320, margin=dict(l=20, r=20, t=10, b=20))
        st.plotly_chart(fig_heatmap, use_container_width=True)


# ----------------------------------------------------------------------------
# PAGE 5: POWER BI & SQL HUB
# ----------------------------------------------------------------------------
with tabs[4]:
    st.subheader("💼 Recruiter & Analyst Deliverables: Power BI & SQL Portfolio")
    st.markdown("""
    This section provides production-grade deliverables for data analytics technical interviews,
    including star-schema data models, official DAX measure formulas, and CTE-driven SQL queries.
    """)

    sub_t1, sub_t2, sub_t3 = st.tabs(["📐 Star Schema & Power BI Guide", "🧮 DAX Measures", "⚡ Top 10 SQL Queries"])

    with sub_t1:
        st.markdown("#### Dimensional Star-Schema Data Model")
        st.markdown("""
        ```mermaid
        erDiagram
            dim_routes ||--o{ fact_transit_performance : "1 to Many (route_id)"
            dim_stations ||--o{ fact_transit_performance : "1 to Many (station_id)"
            dim_date ||--o{ fact_transit_performance : "1 to Many (recorded_date)"
            dim_time_period ||--o{ fact_transit_performance : "1 to Many (hour_of_day)"

            dim_routes {
                string route_id PK
                string route_short_name
                string route_type
                string color_hex
            }
            dim_stations {
                string station_id PK
                string station_code
                string station_name
                float latitude
                float longitude
                string zone_id
            }
            dim_date {
                string recorded_date PK
                string day_of_week
                int is_weekend
            }
            dim_time_period {
                int hour_of_day PK
                string time_period
                int is_peak_hour
            }
            fact_transit_performance {
                int record_id PK
                string trip_id FK
                string route_id FK
                string station_id FK
                float delay_minutes
                string status
                string delay_reason
            }
        ```
        """)
        st.info("💡 You can export the Star-Schema CSV files anytime using the 'Export PBI' button in the sidebar.")

    with sub_t2:
        st.markdown("#### Official DAX Measures for Power BI Desktop")
        dax_file_path = generate_dax_file()
        with open(dax_file_path, "r", encoding="utf-8") as f:
            dax_code = f.read()
        st.code(dax_code, language="sql")

    with sub_t3:
        st.markdown("#### Production SQL Analytics Queries (Window Functions & CTEs)")
        sql_file_path = "sql/03_analytics_queries.sql"
        try:
            with open(sql_file_path, "r", encoding="utf-8") as f:
                sql_content = f.read()
            st.code(sql_content, language="sql")
        except Exception:
            st.info("Query script located at sql/03_analytics_queries.sql")


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 10px 0;">
    <strong>90 Days – 90 Projects Challenge</strong> • Day 7: Public Transit Delay Analytics Dashboard • Author: <strong>raguramrrp</strong><br>
    Built with Python, Streamlit, PostgreSQL/SQLite, SQLAlchemy & Power BI • Free and Open-Source
</div>
""", unsafe_allow_html=True)
