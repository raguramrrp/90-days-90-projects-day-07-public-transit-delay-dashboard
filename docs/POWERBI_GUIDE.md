# Power BI Modeling & Report Development Guide

## 1. Overview
This guide provides complete technical instructions for building the **Public Transit Delay Analytics Dashboard** in Microsoft Power BI Desktop or publishing to Power BI Service.

## 2. Dimensional Model Architecture (Star Schema)

The reporting data model is configured as a high-performance Star Schema:

| Table Name | Role | Primary Key | Description |
| :--- | :--- | :--- | :--- |
| `fact_transit_performance` | Fact Table | `record_id` | Granular arrival observations (11,000+ rows) |
| `dim_routes` | Dimension | `route_id` | Transit route names, modalities, and color schemes |
| `dim_stations` | Dimension | `station_id` | Facility codes, names, coordinates, and fare zones |
| `dim_date` | Dimension | `recorded_date` | Date dimension with day-of-week, weekend flags |
| `dim_time_period` | Dimension | `hour_of_day` | 24-hour dimension with peak/off-peak classification |

### Model Relationships
- `dim_routes[route_id]` (1) ───< (*) `fact_transit_performance[route_id]` (Single Direction)
- `dim_stations[station_id]` (1) ───< (*) `fact_transit_performance[station_id]` (Single Direction)
- `dim_date[recorded_date]` (1) ───< (*) `fact_transit_performance[recorded_date]` (Single Direction)
- `dim_time_period[hour_of_day]` (1) ───< (*) `fact_transit_performance[hour_of_day]` (Single Direction)

---

## 3. Key DAX Measures

### On-Time Arrival Percentage
```dax
On-Time Percentage = 
DIVIDE(
    CALCULATE(
        COUNTROWS(fact_transit_performance),
        fact_transit_performance[status] IN {"On-Time", "Early"}
    ),
    COUNTROWS(fact_transit_performance),
    0
) * 100
```

### Transit Reliability Index (TRI)
```dax
Transit Reliability Index = 
VAR BaseScore = ([On-Time Percentage] * 0.70) + ((100 - [Severe Delay Percentage]) * 0.30)
VAR DelayPenalty = MAX(0, [Average Delay]) * 1.5
VAR CalculatedTRI = BaseScore - DelayPenalty
RETURN
    ROUND(
        MAX(0, MIN(100, CalculatedTRI)),
        1
    )
```

### Congestion Surge Delta
```dax
Congestion Surge Delta = 
CALCULATE([Average Delay], fact_transit_performance[is_peak_hour] = 1) - 
CALCULATE([Average Delay], fact_transit_performance[is_peak_hour] = 0)
```

---

## 4. Visual Layout Specifications

### Page 1: Executive Overview
- **Header**: Metropolitan Transit Authority Banner.
- **Top Metrics**: Multi-row card or 5 single KPI cards showing Total Trips, On-Time %, Avg Delay, Severe Delays, and TRI Score.
- **Visual 1**: Line and Clustered Column Chart (`recorded_date` vs `[Average Delay]` & `[Rolling 7-Day Delay]`).
- **Visual 2**: Donut Chart (`status` vs `[Total Observations]`).
- **Visual 3**: Clustered Bar Chart (`delay_reason` vs `[Total Observations]`).

### Page 2: Route Analysis
- **Visual 1**: Matrix visual showing `route_short_name`, `route_type`, `[Total Observations]`, `[Average Delay]`, `[On-Time Percentage]`, and `[Transit Reliability Index]`.
- **Visual 2**: Horizontal Bar Chart (`route_short_name` vs `[Transit Reliability Index]`).
- **Visual 3**: Stacked Column Chart showing delay status distribution by route.

### Page 3: Station Bottlenecks
- **Visual 1**: Azure Map / Map Visual plotting `dim_stations[latitude]` & `[longitude]` with bubble size driven by `[Average Delay]`.
- **Visual 2**: Top 10 Clustered Bar Chart of stations sorted by `[Average Delay]` descending.

### Page 4: Peak Hours
- **Visual 1**: Area / Column Chart showing `dim_time_period[hour_of_day]` vs `[Average Delay]`.
- **Visual 2**: Matrix / Heatmap with conditional formatting (Rows: `day_of_week`, Columns: `hour_of_day`, Values: `[Average Delay]`).
