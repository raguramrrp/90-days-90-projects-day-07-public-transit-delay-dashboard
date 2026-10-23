"""Power BI Export & Star Schema Generator.
Exports structured dimensional models (Fact and Dimension tables),
DAX measures, and Power Query M transformations for seamless Power BI Desktop ingestion.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from config import POWERBI_EXPORT_DIR, POWERBI_DIR
from src.db import execute_query


def export_powerbi_star_schema() -> dict:
    """Extracts data from the database and exports star-schema CSVs for Power BI."""
    POWERBI_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    POWERBI_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Dim Routes
    df_routes = execute_query("SELECT * FROM routes")
    routes_file = POWERBI_EXPORT_DIR / "dim_routes.csv"
    df_routes.to_csv(routes_file, index=False)

    # 2. Dim Stations
    df_stations = execute_query("SELECT * FROM stations")
    stations_file = POWERBI_EXPORT_DIR / "dim_stations.csv"
    df_stations.to_csv(stations_file, index=False)

    # 3. Dim Date
    df_date = execute_query("""
    SELECT DISTINCT 
        recorded_date,
        day_of_week,
        is_weekend,
        CASE WHEN is_weekend = 1 THEN 'Weekend' ELSE 'Weekday' END AS weekend_desc
    FROM actual_times
    ORDER BY recorded_date
    """)
    df_date["date_dt"] = pd.to_datetime(df_date["recorded_date"])
    df_date["year"] = df_date["date_dt"].dt.year
    df_date["month"] = df_date["date_dt"].dt.month
    df_date["month_name"] = df_date["date_dt"].dt.month_name()
    df_date["day"] = df_date["date_dt"].dt.day
    df_date["week_of_year"] = df_date["date_dt"].dt.isocalendar().week
    df_date = df_date.drop(columns=["date_dt"])
    date_file = POWERBI_EXPORT_DIR / "dim_date.csv"
    df_date.to_csv(date_file, index=False)

    # 4. Dim Time Period
    df_period = execute_query("""
    SELECT DISTINCT 
        hour_of_day,
        time_period,
        is_peak_hour,
        CASE WHEN is_peak_hour = 1 THEN 'Peak Hour' ELSE 'Off-Peak' END AS peak_status
    FROM actual_times
    ORDER BY hour_of_day
    """)
    period_file = POWERBI_EXPORT_DIR / "dim_time_period.csv"
    df_period.to_csv(period_file, index=False)

    # 5. Fact Transit Performance
    df_fact = execute_query("""
    SELECT 
        a.record_id,
        a.trip_id,
        t.route_id,
        a.station_id,
        a.stop_sequence,
        a.scheduled_arrival,
        a.actual_arrival,
        a.delay_minutes,
        a.status,
        a.delay_reason,
        a.recorded_date,
        a.hour_of_day,
        a.is_peak_hour,
        a.is_weekend
    FROM actual_times a
    JOIN trips t ON a.trip_id = t.trip_id
    """)
    fact_file = POWERBI_EXPORT_DIR / "fact_transit_performance.csv"
    df_fact.to_csv(fact_file, index=False)

    # 6. Aggregated KPI Summary
    df_kpi = execute_query("SELECT * FROM v_route_performance")
    kpi_file = POWERBI_EXPORT_DIR / "agg_route_kpis.csv"
    df_kpi.to_csv(kpi_file, index=False)

    return {
        "dim_routes": len(df_routes),
        "dim_stations": len(df_stations),
        "dim_date": len(df_date),
        "dim_time_period": len(df_period),
        "fact_transit_performance": len(df_fact),
        "export_dir": str(POWERBI_EXPORT_DIR)
    }


def generate_dax_file() -> Path:
    """Generates the official DAX measures file for Power BI Desktop."""
    dax_content = """// ============================================================================
// Public Transit Delay Analytics Dashboard - DAX Measure Definitions
// Model: Star Schema with Fact: fact_transit_performance
// ============================================================================

// 1. Total Trip Count
Total Trips = 
DISTINCTCOUNT(fact_transit_performance[trip_id])

// 2. Total Stop Observations
Total Observations = 
COUNTROWS(fact_transit_performance)

// 3. Average Delay (Minutes)
Average Delay = 
ROUND(AVERAGE(fact_transit_performance[delay_minutes]), 2)

// 4. On-Time Arrivals Count (On-Time <= 2 mins or Early < 0 mins)
On-Time Count = 
CALCULATE(
    COUNTROWS(fact_transit_performance),
    fact_transit_performance[status] IN {"On-Time", "Early"}
)

// 5. On-Time Arrival Percentage
On-Time Percentage = 
DIVIDE([On-Time Count], [Total Observations], 0) * 100

// 6. Severe Delay Count (Delay > 15 minutes)
Severe Delay Count = 
CALCULATE(
    COUNTROWS(fact_transit_performance),
    fact_transit_performance[status] = "Severe Delay"
)

// 7. Severe Delay Percentage
Severe Delay Percentage = 
DIVIDE([Severe Delay Count], [Total Observations], 0) * 100

// 8. Transit Reliability Index (TRI) - 0 to 100 Scale
Transit Reliability Index = 
VAR BaseScore = ([On-Time Percentage] * 0.70) + ((100 - [Severe Delay Percentage]) * 0.30)
VAR DelayPenalty = MAX(0, [Average Delay]) * 1.5
VAR CalculatedTRI = BaseScore - DelayPenalty
RETURN
    ROUND(
        MAX(0, MIN(100, CalculatedTRI)),
        1
    )

// 9. Reliability Tier KPI
Reliability Tier = 
SWITCH(
    TRUE(),
    [Transit Reliability Index] >= 85, "High (Optimal)",
    [Transit Reliability Index] >= 70, "Acceptable (Standard)",
    [Transit Reliability Index] >= 50, "Needs Attention",
    "Critical (Severe Delays)"
)

// 10. Peak Hour Delay (Minutes)
Peak Hour Average Delay = 
CALCULATE(
    [Average Delay],
    fact_transit_performance[is_peak_hour] = 1
)

// 11. Off-Peak Average Delay (Minutes)
Off-Peak Average Delay = 
CALCULATE(
    [Average Delay],
    fact_transit_performance[is_peak_hour] = 0
)

// 12. Congestion Surge Delta
Congestion Surge Delta = 
[Peak Hour Average Delay] - [Off-Peak Average Delay]

// 13. Dynamic Title
Dynamic Dashboard Title = 
"Transit Reliability Dashboard | " & 
SELECTEDVALUE(dim_routes[route_short_name], "All Routes") & 
" (" & FORMAT([On-Time Percentage], "0.0") & "% On-Time)"
"""
    POWERBI_DIR.mkdir(parents=True, exist_ok=True)
    dax_path = POWERBI_DIR / "dax_measures.dax"
    with open(dax_path, "w", encoding="utf-8") as f:
        f.write(dax_content)
    return dax_path


def generate_power_query_file() -> Path:
    """Generates Power Query M transformation code for Power BI."""
    m_content = """// ============================================================================
// Power Query M Script: Public Transit Analytics Ingestion
// Paste into Power BI Desktop -> Advanced Editor
// ============================================================================

let
    Source = Csv.Document(File.Contents("data/powerbi_export/fact_transit_performance.csv"),[Delimiter=",", Columns=14, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Types" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"record_id", Int64.Type}, 
        {"trip_id", type text}, 
        {"route_id", type text}, 
        {"station_id", type text}, 
        {"stop_sequence", Int64.Type}, 
        {"scheduled_arrival", type datetime}, 
        {"actual_arrival", type datetime}, 
        {"delay_minutes", type number}, 
        {"status", type text}, 
        {"delay_reason", type text}, 
        {"recorded_date", type date}, 
        {"hour_of_day", Int64.Type}, 
        {"is_peak_hour", Int64.Type}, 
        {"is_weekend", Int64.Type}
    })
in
    #"Changed Types"
"""
    m_path = POWERBI_DIR / "power_query_m.txt"
    with open(m_path, "w", encoding="utf-8") as f:
        f.write(m_content)
    return m_path


if __name__ == "__main__":
    print("Exporting Power BI Star-Schema datasets and DAX files...")
    res = export_powerbi_star_schema()
    dax = generate_dax_file()
    m_file = generate_power_query_file()
    print("Power BI files generated successfully:", res)
