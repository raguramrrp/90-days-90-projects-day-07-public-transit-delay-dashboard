# User Guide: Public Transit Delay Analytics Dashboard

## 1. Getting Started

### Launching the Dashboard
To start the dashboard on Windows:
1. Double-click `run.bat` or open PowerShell in the project directory:
   ```cmd
   .\run.bat
   ```
2. Your default web browser will open at `http://localhost:8501`.

---

## 2. Global Slicers & Filters (Sidebar)

The left sidebar provides global controls that dynamically filter every chart, table, and KPI across the dashboard:

- **Transit Route Slicer**: Select one, multiple, or all routes (e.g. Red Line, Blue Line, Bus 101).
- **Time Period Slicer**: Filter by operational windows:
  - `Morning Peak` (07:00 - 09:59)
  - `Off-Peak (Midday)` (10:00 - 15:59)
  - `Evening Peak` (16:00 - 19:59)
  - `Night / Early Morning` (20:00 - 06:59)
- **Service Window Radio**:
  - `All`: Full 7-day operations.
  - `Weekday Only`: Monday through Friday operations.
  - `Weekend Only`: Saturday and Sunday schedules.
- **Analysis Date Window**: Select a custom start and end date within the 30-day monitoring window.
- **Refresh Data Button**: Re-runs the ETL pipeline to generate a fresh dataset and refresh the cache.
- **Export PBI Button**: Generates updated Star-Schema CSV files and DAX measures.

---

## 3. Dashboard Pages & Features

### Page 1: Overview
- **Executive Metric Cards**: Instant high-level summary of Total Trips, On-Time Arrival %, Average Delay, Severe Delays (>15 mins), and the composite Transit Reliability Index (TRI).
- **30-Day Fleet Delay Trend**: Combined bar and line chart displaying daily average delay against a 7-day moving average and SLA target line (3.0 minutes).
- **Arrival Performance Donut Chart**: Breakdown of all arrivals into Early, On-Time, Minor Delay, Moderate Delay, and Severe Delay.
- **Primary Root Causes**: Horizontal bar chart highlighting total delay minutes lost to passenger crowding, signal faults, maintenance, or traffic congestion.

### Page 2: Route Analysis
- **Route League Table**: Full performance matrix sorted by Reliability Index (TRI), showing on-time percentages and severe delay counts.
- **Route TRI Comparison Chart**: Horizontal bar chart comparing all 6 transit routes.
- **Route Deep-Dive Inspector**: Select any route from the dropdown to view its dedicated average delay, on-time SLA rate, and **Stop-by-Stop Delay Cascading Profile** to see where delays accumulate along the line.

### Page 3: Station Bottlenecks
- **Geographic Station Delay Map**: Interactive Plotly bubble map showing station facilities. Bubble size corresponds to average delay, and color indicates fare zone.
- **Top Bottleneck Stations Bar Chart**: Ranks the top delay hotspots across the network.
- **Station SLA Compliance Table**: Granular metrics including transfer status, peak-hour delay vs off-peak delay, and incident counts.

### Page 4: Peak Hours & Congestion
- **Comparative Metrics**: Displays Morning & Evening Peak delay versus Off-Peak delay, calculating the exact **Congestion Surge Ratio** (multiplier).
- **24-Hour Fleet Congestion Curve**: Line chart tracing hourly average delay with shaded yellow and red vertical bands representing Morning Peak (07-10h) and Evening Peak (16-20h).
- **Day of Week vs. Hour Heatmap**: Visual 7x24 matrix highlighting exact days and hours with acute congestion hotspots.

### Page 5: Power BI & SQL Hub
- **Star-Schema Blueprint**: View the ER diagram connecting `dim_routes`, `dim_stations`, `dim_date`, `dim_time_period`, and `fact_transit_performance`.
- **Official DAX Measures**: Review and copy all 13 DAX measures directly.
- **Top 10 SQL Analytics Queries**: Inspect production SQL interview queries utilizing CTEs, Window functions (`RANK`, `DENSE_RANK`, `LAG`), and rolling aggregations.
