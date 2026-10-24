# Demo Script: Tirunelveli Public Transport Intelligence Platform (Nellai Transit)

**Target Audience:** Technical Recruiters, Data Analytics & Engineering Hiring Managers, Transport Planners  
**Duration:** 90–120 seconds  
**Objective:** Demonstrate an authentic, human-friendly public transport tracker and delay analytics platform for Tirunelveli (Nellai), featuring TNSTC buses, Southern Railway trains, stop-by-stop ETAs, live station departure boards, and geospatial maps.

---

## 00:00 – 00:20 | Introduction & Purpose
> "Hello! Today I'm presenting the **Tirunelveli Public Transport Intelligence Platform (Nellai Transit)**, built as Day 7 of my **90 Days – 90 Projects Challenge**.
>
> In Tirunelveli, thousands of daily commuters rely on **TNSTC City Buses** and **Southern Railway Trains** to commute between Tirunelveli Junction, Veinthaankulam New Bus Stand, Palayamkottai, Town, and regional towns like Ambasamudram, Tenkasi, and Tiruchendur.
>
> I built this platform to provide a clean, human-friendly civic tracker where anyone can discover buses, track live positions, search trains by number, and check departure boards without getting overwhelmed by confusing academic jargon."

---

## 00:20 – 00:50 | Tab 1: Find a Bus & Tab 2: Track a Bus
> *(Open browser to `http://localhost:8501` - Tab 1: 🚏 Find a Bus, then Tab 2: 🚌 Track a Bus)*
>
> "Notice the neat, civic-technology interface designed with clean typography, high contrast, and 6 focused tabs.
>
> Under **Find a Bus**, commuters can:
> - Search stops in English or Tamil (such as *Palayamkottai* or *நெல்லை சந்திப்பு*).
> - Pick a landmark like *Anna Stadium* or *Vannarpettai* to instantly view nearby bus stops within walking distance.
>
> Next, on **Track a Bus**, commuters select any TNSTC bus — for example, `TNSTC Route 1 (TN-72-N-1042)` running between New Bus Stand and Junction:
> - A status card displays honest data freshness, on-time status, approaching stop, and expected arrival time.
> - Below, the **Stop-by-Stop Route Timeline** shows passed stops, current position, and arrival projections across every stage."

---

## 00:50 – 01:15 | Tab 3: Find a Train & Tab 5: Station Departure Board
> *(Switch to Tab 3: 🚆 Find a Train, then Tab 5: 📋 Station Departure Board)*
>
> "Under **Find a Train**, users can enter any 5-digit Indian Railways train number:
> - For Tirunelveli trains like `12632 Nellai Superfast Express` or `20666 Vande Bharat`, it displays the assigned platform at Tirunelveli Junction, current location, and full halt timetable.
> - Importantly, the system enforces **geographic eligibility**: if a user searches a valid non-local train like `12621 Tamil Nadu Express`, it explains that the train runs between New Delhi and Chennai and does not serve Tirunelveli, rather than displaying fabricated local data.
>
> Under **Station Departure Board**, commuters at Tirunelveli Junction or New Bus Stand can see upcoming departures, platforms, and schedule variance on a digital station board."

---

## 01:15 – 01:40 | Tab 4: Tirunelveli Map & Tab 6: Network Analytics
> *(Switch to Tab 4: 🗺️ Tirunelveli Map, then Tab 6: 📊 Network Analytics)*
>
> "Under **Tirunelveli Map**, an interactive Leaflet map shows the district's transit corridors, Thamirabarani River basin, station nodes, and vehicles with modal toggles for buses and trains.
>
> Under **Network Analytics**, transport planners have high-level KPIs:
> - Over 14,000 monitored station arrivals with an **On-Time Arrival Rate of 82.4%** and an average delay of 2.85 minutes.
> - 30-day delay trend charts and root cause breakdowns including level crossings and market road congestion."

---

## 01:40 – 02:00 | Architecture & Engineering Rigor
> "Under the hood, the system is powered by a modular Provider architecture (`src/providers.py`), dual SQLite / PostgreSQL database support, parameterized queries, and strict privacy protection with zero location logging.
>
> The entire platform is backed by **30 automated pytest unit tests with a 100% pass rate**, and includes 1-click Windows setup scripts (`setup.bat`, `run.bat`, `test.bat`). Thank you!"
