# Project Overview: Tirunelveli Public Transport Intelligence Platform (Nellai Transit)

## 1. Executive Summary
Public transportation networks in Tirunelveli (Nellai) serve thousands of daily passengers across student, worker, pilgrim, and regional corridors. Commuters, transport coordinators, and station managers require clear, intuitive visibility into bus and train schedules, arrival delays, platform information, and route progressions.

The **Tirunelveli Public Transport Intelligence Platform (Nellai Transit)** is a civic-technology multimodal tracking and analytics platform. Centered on the **Tirunelveli District**, it integrates city and regional buses (**TNSTC Tirunelveli**), passenger and express trains (**Southern Railway Nellai Hub**), and intercity express connections (**SETC**).

The application features the approved **Google Stitch "Austere Civic Utility" Design System (v2.5)**, providing a high-contrast municipal interface, tabular numeric alignment (`tnum`), crisp 4px rectangular geometry, custom SVG vector maps of the Thamirabarani River basin, CRIS NTES locomotive motive power telemetry, and station hub interchange schematics.

## 2. Problem Statement
Daily commuters frequently experience unpredictable wait times, missed bus and train connections, and confusion at major transit junctions:
- Is TNSTC Bus Route 1 or Route 11A running on schedule or delayed?
- Which platform at Tirunelveli Junction is my passenger or express train arriving at?
- When will the next bus arrive at Veinthaankulam New Bus Stand or Palayamkottai Market?
- How can transit systems quantify fleet health using a single, balanced **Transit Reliability Index (TRI)** without cluttering commuter interfaces with confusing academic charts?
- Why do commercial transit apps mislead commuters with synthetic "live GPS" dots when real feeds are offline?

## 3. Project Objectives
1. **Multimodal Discovery & Telemetry**: Search buses by stop or GPS landmark proximity, and track active TNSTC buses (`TN-72-N-xxxx`) with sequential waypoint progressions and civic fare displays.
2. **Train Search by Number**: Look up Indian Railways trains by 5-digit number, verifying local Tirunelveli eligibility, locomotive motive power (`WAP-7 ED 37102`, `WAP-4 ED`), block location, speed, and halt schedules.
3. **Stop-by-Stop ETAs**: Clear progression timelines displaying passed halts, approaching stops, expected arrival timestamps, and delay variance.
4. **Station Hub Interchanges & Concourse Schematics**: Interactive SVG terminal schematics and amenity counts for Tirunelveli Junction (`TEN`), MGR New Bus Stand (`VBS`), Palayamkottai (`PLM`), and Town (`TOWN`) with prepaid auto fixed tariffs.
5. **Geospatial Tracking & Vector Cartography**: High-contrast custom SVG vector plot of the Thamirabarani River basin, Sulochana Mudaliar Bridge crossing, pulsing radar beacons, and Leaflet/Folium district mapping.
6. **Google Stitch Civic Utility UI (v2.5)**: 4 uncluttered civic views (Bus Search & Telemetry, Train Search & Status, Station Hub Interchanges, About & Data Feeds) designed for everyday commuters and transit managers.
7. **Honest Data Provenance**: Strict labeling (`LIVE`, `RECENT`, `SCHEDULED`, `ESTIMATED`, `STATIC`, `UNAVAILABLE`) with isolated demonstration mode. Zero fabricated live GPS in production mode.
8. **Dual Engine Architecture**: Out-of-the-box zero-setup execution on Windows via SQLite while supporting enterprise PostgreSQL deployments.

## 4. Key Performance Indicators (KPIs)
- **Total Trips & Observations**: Overall operational volume (14,640+ station arrivals monitored, 2,880 active trips).
- **On-Time Arrival Rate (%)**: Percentage of arrivals arriving within 2 minutes of schedule ($\le 2.0\text{ min}$, baseline 86.4%).
- **Average Delay (Minutes)**: Fleet-wide arithmetic mean variance from scheduled timetables (4.8 min).
- **Severe Delay Count & Rate**: Proportion of arrivals delayed by more than 15 minutes.
- **Transit Reliability Index (TRI)**: Composite reliability score (0-100):
  $$TRI = \max(0, \min(100, (\text{On-Time \%} \times 0.70) + ((100 - \text{Severe \%}) \times 0.30) - (\text{Avg Delay} \times 1.5)))$$
- **Congestion Surge Multiplier**: Ratio of peak-hour delay to midday off-peak delay ($2.08\times$).

## 5. Scope & Geographic Boundaries
### In Scope:
- **Geographic Scope**: Tirunelveli District and key radial corridors ($8.30^\circ - 9.00^\circ\text{ N}, 77.30^\circ - 78.20^\circ\text{ E}$).
- **3 Operators**: TNSTC Tirunelveli (City & Regional Buses), Southern Railway (Nellai Hub), SETC (Intercity Express).
- **Verified Routes & Trains**: TNSTC Routes 1, 2, 3, 10, 11A, 41, 144, and Southern Railway Trains 12632, 12631, 20666, 20665, 06682, 06685, 16127, 16723, 16847, 20635.
- **20 Verified Stations & Hubs**: GPS coordinates, modal interchange indicators, terminal schematics, and auto tariffs.
- **Google Stitch Civic Utility UI**: 4 focused views with 2-column split desktop workspace, responsive mobile bottom bar, and custom SVG river/concourse schematics.
- **Dual Relational Database Schema**: Zero-setup SQLite (`data/transit.db`) + PostgreSQL DDL (`sql/postgres_setup.sql`).
- **Automated Windows Lifecycle**: `setup.bat`, `run.bat`, and `test.bat` with **37 automated unit tests across 9 test suites (100% pass rate)**.

### Out of Scope (Future Upgrade Path):
- Real-time GPS OBD transponder hardware installation across private omni buses.
- Machine Learning arrival ETA prediction models under extreme monsoon flooding.
- Native mobile app wrapper (Flutter / React Native).
