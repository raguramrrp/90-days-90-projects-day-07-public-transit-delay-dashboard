# Demo Script: Public Transit Delay Analytics Dashboard

**Target Audience:** Technical Recruiters, Data Analytics Hiring Managers, BI Leads  
**Duration:** 90–120 seconds  
**Objective:** Demonstrate end-to-end data engineering, SQL analytics, KPI modeling, and BI visualization.

---

## 00:00 – 00:20 | Introduction & Problem Context
> "Hello! Today I'm presenting the **Public Transit Delay Analytics Dashboard**, built as Day 7 of my **90 Days – 90 Projects Challenge**.
>
> In urban transportation, both commuters and transit planners struggle with recurring delay cascades and unpredictable travel times. I designed this full-stack analytics platform to ingest scheduled versus actual transit arrival feeds, compute industry-standard reliability KPIs, and pinpoint chronic route and station bottlenecks."

---

## 00:20 – 00:45 | Architecture & Executive Overview
> *(Open browser to `http://localhost:8501` - Overview Tab)*
>
> "The platform runs on a dual-database architecture supporting both SQLite for instant zero-configuration local runs and enterprise PostgreSQL.
>
> On the **Executive Overview** page, our automated ETL pipeline has processed over 11,000 arrival records across 6 transit lines.
> - We track fleet-wide volume: **2,140 trips**.
> - An **On-Time Arrival Rate of 82.4%** meeting our SLA benchmark.
> - An average delay variance of **2.85 minutes**.
> - And our core composite metric: the **Transit Reliability Index (TRI)** at **84.2 out of 100**, achieving an 'Optimal Performance' tier.
>
> Notice the 30-day delay trend with a 7-day rolling moving average, and our root-cause breakdown showing high passenger boarding as the primary delay driver."

---

## 00:45 – 01:10 | Route Reliability & Bottleneck Drill-Down
> *(Click to 'Route Analysis' Tab)*
>
> "Switching to the **Route Analysis** view, we see a ranked league table. The Red Subway Line leads our network with an 89.1 TRI score, while Bus 101 Express experiences heavier traffic interference.
>
> Using our Route Deep-Dive inspector, we can trace the exact stop-by-stop delay cascading profile, identifying where dwell times compound along the corridor."

---

## 01:10 – 01:35 | Station Bottlenecks & Peak-Hour Dynamics
> *(Click to 'Station Bottlenecks' Tab, then 'Peak Hours' Tab)*
>
> "On the **Station Bottlenecks** page, our interactive bubble map visualizes facility delays across 3 metropolitan zones. **Downtown Central** and **Eastgate Terminal** emerge as key transfer bottlenecks with average delays exceeding 4.4 minutes.
>
> Over on the **Peak Hours** screen, we analyze our 24-hour congestion curve. The data reveals a **2.11x Congestion Surge Multiplier** during Morning Peak (7-10 AM) and Evening Peak (4-8 PM), corroborated by our 7x24 Day-versus-Hour congestion heatmap."

---

## 01:35 – 02:00 | Power BI Star Schema, SQL & Portfolio Value
> *(Reference the repository deliverables & documentation)*
>
> "Finally, alongside our interactive dashboard, the project includes complete deliverables:
> 1. Exported dimensional Star-Schema CSVs in `data/powerbi_export/` ready for Power BI Desktop.
> 2. Official DAX measures in `powerbi/dax_measures.dax` including our Transit Reliability Index formula.
> 3. Production-grade SQL queries in `sql/03_analytics_queries.sql` using CTEs, window functions like `DENSE_RANK()`, and moving averages.
>
> The repository includes automated Windows batch scripts (`setup.bat`, `run.bat`, `test.bat`) with 100% automated test coverage. Thank you!"
