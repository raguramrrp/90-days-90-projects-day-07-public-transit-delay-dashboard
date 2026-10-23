# Project Overview: Public Transit Delay Analytics Dashboard

## 1. Executive Summary
Urban public transportation networks face intense operational pressures. Commuters, transit dispatchers, and urban mobility planners require rapid, granular visibility into recurring delay patterns, bottleneck stations, and peak-hour congestion cascades.

The **Public Transit Delay Analytics Dashboard** is a data analytics and business intelligence platform built to calculate, monitor, and visualize transit reliability across bus rapid transit, metro subways, light rail, and regional commuter rail services.

## 2. Problem Statement
Transit passengers frequently experience unpredictable wait times and cascading delays without clear explanation. Concurrently, transit planners lack unified dashboards connecting raw GTFS timetable observations with actionable business KPIs, such as:
- Which routes consistently fail service-level agreements (SLAs)?
- Which intermodal stations act as chronic bottlenecks causing dwell-time delays?
- What is the exact delay penalty introduced by morning and evening peak traffic hours?
- How do we calculate a fair, single-number **Transit Reliability Index (TRI)** that balances on-time rates with severe delay penalties?

## 3. Project Objectives
1. **Automated ETL Ingestion**: Extract scheduled and actual arrival/departure feeds, validate timestamps, and calculate precise arrival deviations in minutes.
2. **Standardized Delay Classification**: Segment operations into 5 clear tiers: Early (<0m), On-Time (0-2m), Minor Delay (2-5m), Moderate Delay (5-15m), and Severe Delay (>15m).
3. **KPI & Reliability Modeling**: Compute the Transit Reliability Index (TRI, 0-100 scale), SLA on-time percentages, and peak-to-off-peak delay surge ratios.
4. **Dual Engine Architecture**: Provide out-of-the-box zero-setup execution on Windows via SQLite while supporting enterprise PostgreSQL deployments.
5. **Multi-Platform Analytics**: Deliver an interactive Streamlit web dashboard alongside complete Microsoft Power BI Star-Schema assets, DAX measure definitions, and SQL analytics scripts.

## 4. Key Performance Indicators (KPIs)
- **Total Trips & Observations**: Overall operational volume.
- **On-Time Arrival Rate (%)**: Percentage of arrivals arriving within 2 minutes of schedule.
- **Average Delay (Minutes)**: Fleet-wide arithmetic mean variance from scheduled timetables.
- **Severe Delay Count & Rate**: Proportion of arrivals delayed by more than 15 minutes.
- **Transit Reliability Index (TRI)**: Composite reliability score (0-100):
  $$TRI = \max(0, \min(100, (\text{On-Time \%} \times 0.70) + ((100 - \text{Severe \%}) \times 0.30) - (\text{Avg Delay} \times 1.5)))$$
- **Congestion Surge Multiplier**: Ratio of peak-hour delay to midday off-peak delay.

## 5. Scope & MVP Boundaries
### In Scope:
- Ingestion of 6 transit routes (Subway, Light Rail, BRT, Express Bus, Commuter Rail) and 18 stations across 3 metropolitan zones.
- 30-day historical analysis with over 11,000 arrival observations.
- Interactive multi-page dashboard (Overview, Routes, Stations, Peak Hours, Power BI/SQL Hub).
- Production-grade SQL queries with CTEs, window functions, and moving averages.
- Star-schema Power BI export datasets and DAX measure files.
- Automated Windows setup (`setup.bat`, `run.bat`, `test.bat`).

### Out of Scope (Future Upgrade Path):
- Real-time GPS stream ingestion via Kafka / GTFS-RT.
- Machine Learning predictive arrival ETA models.
- Automated SMS/Push commuter alerts.
