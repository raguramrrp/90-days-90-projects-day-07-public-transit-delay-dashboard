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
- **Fleet Reliability Scorecard**: Prominent Transit Reliability Index (TRI) hero card with tier badge and quick diagnostic summary.
- **30-Day Fleet Delay Trend**: Combined bar and line chart displaying daily average delay against a 7-day moving average and SLA target line (3.0 minutes).
- **Executive Metric Cards**: Network volume, on-time SLA rate, average delay, and severe incident counts.
- **Arrival Performance Donut Chart**: Breakdown of all arrivals into Early, On-Time, Minor Delay, Moderate Delay, and Severe Delay.
- **Primary Root Causes**: Horizontal bar chart highlighting total delay minutes lost to passenger crowding, signal faults, maintenance, or traffic congestion.

### Page 2: Route Analysis
- **Route Deep-Dive Inspector**: Route selector with instant performance ribbon.
- **Stop-by-Stop Delay Cascading Profile**: Spline area progression displaying cumulative delay accumulation across stations along the selected corridor.
- **Route TRI Leaderboard**: Horizontal bar chart ranking routes by the Transit Reliability Index.
- **Route Performance League Matrix**: Detailed performance table with on-time %, severe delay %, and TRI rankings.

### Page 3: Station Bottlenecks
- **Fare Zone Performance Ribbon**: Comparative delay cards across Zone 1 (Core Urban), Zone 2 (Inner Ring), and Zone 3 (Perimeter/Airport).
- **Geographic Station Delay Map**: Interactive Plotly bubble map showing station facilities with bubble size indicating average delay and color indicating fare zone.
- **Top Bottleneck Stations Bar Chart**: Ranks the top delay hotspots across the network.
- **Station SLA Compliance Table**: Granular metrics including transfer status, peak-hour delay vs off-peak delay, and incident counts.

### Page 4: Peak Hours & Congestion
- **Congestion Surge Metrics**: Morning & Evening Peak delay versus Off-Peak delay, and the **Congestion Surge Ratio** ($2.11\times$).
- **Day of Week vs. Hour Heatmap Matrix**: Full 7x24 matrix highlighting exact days and hours with acute congestion hotspots.
- **24-Hour Fleet Congestion Curve**: Line chart tracing hourly average delay with shaded yellow and red vertical bands representing Morning Peak (07-10h) and Evening Peak (16-20h).
