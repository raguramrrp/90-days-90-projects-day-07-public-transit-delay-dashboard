# Project Overview: Tirunelveli Public Transport Intelligence Platform (Nellai Transit)

## 1. Executive Summary
Public transportation networks in Tirunelveli (Nellai) serve thousands of daily passengers across student, worker, pilgrim, and regional corridors. Commuters, transport coordinators, and station managers require clear, intuitive visibility into bus and train schedules, arrival delays, platform information, and route progressions.

The **Tirunelveli Public Transport Intelligence Platform (Nellai Transit)** is a civic-technology multimodal tracking and analytics platform. Centered on the **Tirunelveli District**, it integrates city and regional buses (**TNSTC Tirunelveli**), passenger and express trains (**Southern Railway Nellai Hub**), and intercity express connections (**SETC**).

## 2. Problem Statement
Daily commuters frequently experience unpredictable wait times, missed bus and train connections, and confusion at major transit junctions:
- Is TNSTC Bus Route 1 or Route 3 running on schedule or delayed?
- Which platform at Tirunelveli Junction is my passenger or express train arriving at?
- When will the next bus arrive at Veinthaankulam New Bus Stand or Palayamkottai Market?
- How can transit systems quantify fleet health using a single, balanced **Transit Reliability Index (TRI)** without cluttering commuter interfaces with confusing academic charts?

## 3. Project Objectives
1. **Multimodal Discovery & Tracking**: Search buses by stop or GPS landmark proximity, and track active TNSTC buses (`TN-72-N-xxxx`).
2. **Train Search by Number**: Look up Indian Railways trains by 5-digit number, verifying local Tirunelveli eligibility and halt schedules.
3. **Stop-by-Stop ETAs**: Clear progression timelines displaying passed halts, approaching stops, expected arrival timestamps, and delay variance.
4. **Station Departure Boards**: High-contrast digital departure boards for Tirunelveli Junction, New Bus Stand, Palayamkottai, Town, Ambasamudram, and Tenkasi.
5. **Geospatial Tracking & Map (Leaflet / Folium)**: Render an interactive map of Tirunelveli transit corridors, Thamirabarani River basin, station nodes, and vehicles.
6. **Clean Civic UI**: 6 uncluttered tabs designed for everyday commuters and transit managers.
7. **Honest Data Freshness**: Strict labeling (`LIVE`, `RECENT`, `SCHEDULED`, `ESTIMATED`, `STATIC`, `UNAVAILABLE`) with isolated demonstration mode.
8. **Dual Engine Architecture**: Out-of-the-box zero-setup execution on Windows via SQLite while supporting enterprise PostgreSQL deployments.

## 4. Key Performance Indicators (KPIs)
- **Total Trips & Observations**: Overall operational volume (14,640+ station arrivals monitored).
- **On-Time Arrival Rate (%)**: Percentage of arrivals arriving within 2 minutes of schedule ($\le 2.0\text{ min}$).
- **Average Delay (Minutes)**: Fleet-wide arithmetic mean variance from scheduled timetables.
- **Severe Delay Count & Rate**: Proportion of arrivals delayed by more than 15 minutes.
- **Transit Reliability Index (TRI)**: Composite reliability score (0-100):
  $$TRI = \max(0, \min(100, (\text{On-Time \%} \times 0.70) + ((100 - \text{Severe \%}) \times 0.30) - (\text{Avg Delay} \times 1.5)))$$
- **Congestion Surge Multiplier**: Ratio of peak-hour delay to midday off-peak delay ($2.08\times$).

## 5. Scope & Geographic Boundaries
### In Scope:
- Geographic scope: Tirunelveli District and key radial corridors ($8.30^\circ - 9.00^\circ\text{ N}, 77.30^\circ - 78.20^\circ\text{ E}$).
- 3 operators: TNSTC Tirunelveli (City & Regional Buses), Southern Railway (Nellai Hub), SETC (Intercity Express).
- 10 authentic routes: TNSTC Routes 1, 2, 3, 10, 41, 144, and Southern Railway Trains 12632, 20666, 06682, 06685.
- 20 verified stations with GPS coordinates and modal interchange indicators.
- 30-day historical analysis with over 14,000 arrival observations.
- Interactive 6-tab Streamlit web platform with Folium/Leaflet maps and Plotly charts.
- Dual relational database schema (SQLite + PostgreSQL DDL).
- Automated Windows setup (`setup.bat`, `run.bat`, `test.bat`) with 30 automated unit tests.

### Out of Scope (Future Upgrade Path):
- Real-time GPS OBD hardware integration across all private omni buses.
- Machine Learning arrival ETA prediction models under extreme monsoon weather.
- Mobile native application wrapper (Flutter / React Native).
