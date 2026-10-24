# Demo Script: Tirunelveli Public Transport Intelligence Platform (Nellai Transit)

**Target Audience:** Technical Recruiters, Data Analytics & Engineering Hiring Managers, Transport Planners  
**Duration:** 90–120 seconds  
**Objective:** Demonstrate an authentic, high-contrast civic public transport tracker for Tirunelveli (Nellai), featuring the approved Google Stitch Civic Design System (v2.5), TNSTC buses, Southern Railway trains, Thamirabarani River vector maps, CRIS NTES locomotive telemetry, station concourse schematics, and prepaid auto tariffs.

---

## 00:00 – 00:20 | Introduction & Purpose
> "Hello! Today I'm presenting the **Tirunelveli Public Transport Intelligence Platform (Nellai Transit)**, built as Day 7 of my **90 Days – 90 Projects Challenge**.
>
> In Tirunelveli, thousands of daily commuters rely on **TNSTC City Buses** and **Southern Railway Trains** to commute between Tirunelveli Junction, Veinthaankulam New Bus Stand, Palayamkottai, Town, and regional towns like Ambasamudram, Tenkasi, and Tiruchendur.
>
> I implemented the approved **Google Stitch 'Austere Civic Utility' Design System (v2.5)** — delivering a crisp municipal interface with strict 4px borders, zero startup glow, tabular numeric alignment, and zero synthetic live GPS deception in production mode."

---

## 00:20 – 00:50 | View 1: Bus Search & Live Telemetry
> *(Open browser to `http://localhost:8501` - View 1: 🚏 Bus Search & Telemetry)*
>
> "Notice the 2-column desktop split workspace:
> - On the left, commuters can enter origins and destinations in English or Tamil, tap the **GPS icon** to auto-detect nearest stops, or use the **Swap button** to reverse trips with one touch.
> - One-tap shortcut chips provide instant access to major terminals like *Tirunelveli Junction* and *Palayamkottai*.
> - Each route card displays civic fares — such as **₹12** for Ordinary Route 11A or **₹14** for Express Route 1 — alongside live crowd occupancy.
>
> On the right:
> - A high-contrast **custom SVG vector map** illustrates the Thamirabarani River basin and the Sulochana Mudaliar Bridge crossing.
> - An active radar beacon pulses on bus `TN-72-N-1842`, accompanied by real-time speed, heading, and a sequential 5-stop progression timeline."

---

## 00:50 – 01:15 | View 2: Train Search & CRIS NTES Live Status
> *(Switch to View 2: 🚆 Train Search & Status)*
>
> "Under **Train Search & Status**, commuters can look up any 5-digit Indian Railways train number:
> - For Tirunelveli corridor trains like `16127 Guruvayur Express`, the inspector displays authenticated **CRIS NTES telemetry**, including the electric locomotive motive power unit — `WAP-7 ED 37102` from Erode Shed, speed at 68 km/h, current position passing Gangaikondan Block Section, and assigned Platform 1 at Junction.
> - Below, an 8-halt progression line shows full waypoint timings from Madurai down to Nagercoil.
> - Crucially, the platform enforces **geographic boundaries**: searching an out-of-area train like `12626 Kerala Express` displays a clear civic notice explaining that the train operates via Kottayam without serving the Tirunelveli Division."

---

## 01:15 – 01:40 | View 3: Station Hub Interchanges & Auto Tariffs
> *(Switch to View 3: 🏢 Station Hubs)*
>
> "Under **Station Hub Interchanges**, commuters can explore Tirunelveli Central Junction, MGR New Bus Stand, Palayamkottai, and Town:
> - An interactive **SVG terminal concourse schematic** maps out railway platforms, bus boarding bays, pedestrian subways, and waiting halls.
> - Commuters can view immediate connecting city bus departures synchronized with arriving trains.
> - To prevent passenger exploitation, we integrated the official **Tirunelveli Traffic Police Prepaid Auto Fixed Tariff Card** — establishing regulated fares such as ₹70 to Palayamkottai or ₹90 to New Bus Stand."

---

## 01:40 – 02:00 | Architecture & Engineering Rigor
> "Under the hood, the system is powered by:
> - A modular Python provider layer (`src/providers.py`) enforcing honest data provenance (`LIVE`, `RECENT`, `SCHEDULED`, `STATIC`).
> - Dual relational database engines supporting zero-configuration SQLite for Windows and PostgreSQL for enterprise scale.
> - **37 automated pytest unit tests across 9 test suites with a 100% pass rate**, covering UI templates, providers, tracking, and mathematical delay variance.
> - 1-click Windows setup scripts (`setup.bat`, `run.bat`, `test.bat`). Thank you!"
