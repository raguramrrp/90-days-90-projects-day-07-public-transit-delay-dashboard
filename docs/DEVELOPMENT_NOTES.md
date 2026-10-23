# Development Notes: Design Decisions & Technical Trade-offs

## 1. Technical Choices

### Dual-Database Architecture (SQLite + PostgreSQL)
- **Decision**: Provide native SQLite support (`data/transit.db`) as the default local engine while supplying complete PostgreSQL schemas (`sql/postgres_setup.sql`) and SQLAlchemy multi-dialect connection management.
- **Rationale**: For final-year student evaluation and GitHub recruiters, requiring a pre-installed, running PostgreSQL daemon on Windows adds immediate friction and potential setup failures. SQLite allows a 1-click Windows demonstration (`setup.bat` -> `run.bat`) while proving enterprise PostgreSQL competency through schema scripts, views, and index optimization.

### Transit Reliability Index (TRI) Formula
- **Decision**: Implement a balanced composite index:
  $$\text{TRI} = \max\left(0, \min\left(100, (\text{On-Time \%} \times 0.70) + ((100 - \text{Severe \%}) \times 0.30) - (\max(0, \text{Avg Delay}) \times 1.5)\right)\right)$$
- **Rationale**: Measuring solely on-time rate overlooks the severity of catastrophic delays (e.g. 45-minute signal failures), while measuring solely average delay masks high-volume punctuality. Combining on-time rate, severe delay avoidance, and an average delay penalty yields a single, intuitive 0-100 score aligned with transit industry best practices.

### Streamlit + Plotly Frontend Choice
- **Decision**: Develop an interactive Streamlit application with customized CSS and Plotly charts rather than a static reporting notebook or complex React front-end.
- **Rationale**: Allows rapid delivery of dynamic filtering, high-frame-rate cross-filtering, interactive bubble maps, and instant CSV/Power BI exports with zero npm/node dependency overhead.

### Realistic Stochastic Delay Modeling
- **Decision**: Rather than using uniform random numbers, `src/generator.py` uses:
  - Time-of-day trip density weighting (matching real morning and evening commute volumes).
  - Exponential delay distributions for peak hours.
  - Bottleneck station multipliers for major interchange stations (e.g., Downtown Central, Union Station).
  - Markovian delay cascading: delays at stop $N$ propagate to stop $N+1$ with partial inter-station schedule buffer recovery.
  - Random 3.5% shock shocks with real operational root causes.

## 2. Key Assumptions
1. An arrival within 2.0 minutes of the timetable is categorized as **On-Time**, matching Federal Transit Administration (FTA) standards.
2. Negative delay values represent early arrivals (vehicles reaching stops ahead of schedule).
3. The metropolitan service operates 3 fare zones: Zone 1 (Core Urban), Zone 2 (Inner Ring), Zone 3 (Outer Perimeter & Regional).
4. Weekends have approximately 30% reduced trip density compared to weekdays.
