# Power BI Implementation Guide

This folder contains the complete deliverables for importing, modeling, and visualizing the **Public Transit Delay Analytics Dashboard** in Microsoft Power BI Desktop.

## 1. Deliverables Included

1. `dax_measures.dax`: 13 ready-to-copy DAX measure calculations (TRI score, On-Time %, Peak Delay Delta, Dynamic Title, etc.).
2. `power_query_m.txt`: Power Query M code for automated schema ingestion and datatype parsing.
3. `report_layout.json`: Architectural blueprint for the 4 dashboard report pages and visual configurations.
4. `../data/powerbi_export/`: Pre-processed Star-Schema CSV files:
   - `dim_routes.csv`
   - `dim_stations.csv`
   - `dim_date.csv`
   - `dim_time_period.csv`
   - `fact_transit_performance.csv`
   - `agg_route_kpis.csv`

## 2. Step-by-Step Power BI Setup

### Step 1: Open Power BI Desktop
1. Launch **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV**.
3. Navigate to `data/powerbi_export/` and import:
   - `dim_routes.csv`
   - `dim_stations.csv`
   - `dim_date.csv`
   - `dim_time_period.csv`
   - `fact_transit_performance.csv`

### Step 2: Establish Model Relationships (Star Schema)
Switch to the **Model View** tab in Power BI Desktop and create the following single-direction relationships:
- `dim_routes[route_id]` 1 ─── * `fact_transit_performance[route_id]`
- `dim_stations[station_id]` 1 ─── * `fact_transit_performance[station_id]`
- `dim_date[recorded_date]` 1 ─── * `fact_transit_performance[recorded_date]`
- `dim_time_period[hour_of_day]` 1 ─── * `fact_transit_performance[hour_of_day]`

### Step 3: Add DAX Measures
1. Create a dedicated measure table or select `fact_transit_performance`.
2. Click **New Measure** on the Home ribbon.
3. Open `powerbi/dax_measures.dax` and paste each measure (e.g., `Transit Reliability Index`, `On-Time Percentage`, `Congestion Surge Delta`).

### Step 4: Build Report Pages
Follow the page layout guidelines in `report_layout.json`:
- **Page 1 (Executive Overview)**: Card KPIs, 30-Day Delay Trend Line, Performance Donut Chart, Delay Root Causes Bar Chart.
- **Page 2 (Route Analysis)**: Route Matrix Table, TRI Comparison Bar Chart, On-Time vs Severe Delays Column Chart.
- **Page 3 (Station Bottlenecks)**: Map visual with `dim_stations[latitude]` & `[longitude]`, Top 10 Bottleneck Bar Chart.
- **Page 4 (Peak Hours)**: 24-Hour Delay Column Chart with shaded bands, Congestion Heatmap Matrix.
