"""ETL Pipeline for Public Transit Delay Analytics Dashboard.
Handles transit data ingestion, cleaning, validation, delay derivation,
and loading into relational SQL databases (SQLite/PostgreSQL) and Power BI exports.
"""

import sys
from datetime import datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from src.db import init_db, get_engine, check_health
from src.generator import generate_transit_data, save_raw_datasets, classify_delay_status, determine_time_period


class TransitETLPipeline:
    """End-to-End ETL Pipeline for transit delay analytics."""

    def __init__(self, raw_dir: Path = RAW_DATA_DIR, processed_dir: Path = PROCESSED_DATA_DIR):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.audit_log = {}

    def extract(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Extracts transit datasets from CSV files or generates them if absent."""
        routes_path = self.raw_dir / "routes.csv"
        stations_path = self.raw_dir / "stations.csv"
        trips_path = self.raw_dir / "trips.csv"
        actual_path = self.raw_dir / "actual_times.csv"

        if not (routes_path.exists() and stations_path.exists() and trips_path.exists() and actual_path.exists()):
            # Generate sample dataset
            df_routes, df_stations, df_trips, df_actual = generate_transit_data(num_days=30, trips_per_day=80)
            save_raw_datasets(df_routes, df_stations, df_trips, df_actual)
        else:
            df_routes = pd.read_csv(routes_path)
            df_stations = pd.read_csv(stations_path)
            df_trips = pd.read_csv(trips_path)
            df_actual = pd.read_csv(actual_path)

        self.audit_log["extracted_counts"] = {
            "routes": len(df_routes),
            "stations": len(df_stations),
            "trips": len(df_trips),
            "actual_times": len(df_actual),
        }
        return df_routes, df_stations, df_trips, df_actual

    def transform(
        self,
        df_routes: pd.DataFrame,
        df_stations: pd.DataFrame,
        df_trips: pd.DataFrame,
        df_actual: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Cleans, formats, validates, and enriches transit datasets."""
        # Clean Routes
        df_routes = df_routes.drop_duplicates(subset=["route_id"]).copy()
        df_routes["route_short_name"] = df_routes["route_short_name"].astype(str).str.strip()
        df_routes["route_long_name"] = df_routes["route_long_name"].astype(str).str.strip()
        df_routes["agency_name"] = df_routes["agency_name"].fillna("Metropolitan Transit Authority")

        # Clean Stations
        df_stations = df_stations.drop_duplicates(subset=["station_id"]).copy()
        df_stations["station_code"] = df_stations["station_code"].astype(str).str.strip().str.upper()
        df_stations["station_name"] = df_stations["station_name"].astype(str).str.strip()
        df_stations["latitude"] = pd.to_numeric(df_stations["latitude"], errors="coerce")
        df_stations["longitude"] = pd.to_numeric(df_stations["longitude"], errors="coerce")
        df_stations["is_transfer_station"] = df_stations["is_transfer_station"].fillna(0).astype(int)

        # Filter valid routes
        valid_route_ids = set(df_routes["route_id"])
        df_trips = df_trips[df_trips["route_id"].isin(valid_route_ids)].drop_duplicates(subset=["trip_id"]).copy()
        df_trips["direction_id"] = df_trips["direction_id"].fillna(0).astype(int)

        # Filter valid trips and stations
        valid_trip_ids = set(df_trips["trip_id"])
        valid_station_ids = set(df_stations["station_id"])
        df_actual = df_actual[
            df_actual["trip_id"].isin(valid_trip_ids) & df_actual["station_id"].isin(valid_station_ids)
        ].copy()

        # Timestamp parsing and delay recalculation
        sched_arr = pd.to_datetime(df_actual["scheduled_arrival"], errors="coerce")
        actual_arr = pd.to_datetime(df_actual["actual_arrival"], errors="coerce")

        # Calculate exact delay in minutes: (actual - scheduled)
        computed_delay = (actual_arr - sched_arr).dt.total_seconds() / 60.0
        # If timestamp parsing failed or NaN, fallback to existing or 0.0
        df_actual["delay_minutes"] = computed_delay.fillna(df_actual.get("delay_minutes", 0.0)).round(2)

        # Re-derive standard categorical fields
        df_actual["status"] = df_actual["delay_minutes"].apply(classify_delay_status)
        df_actual["hour_of_day"] = sched_arr.dt.hour.fillna(0).astype(int)
        df_actual["recorded_date"] = sched_arr.dt.strftime("%Y-%m-%d").fillna("2026-01-01")
        df_actual["day_of_week"] = sched_arr.dt.day_name().fillna("Monday")
        df_actual["is_weekend"] = sched_arr.dt.day_of_week.apply(lambda w: 1 if w >= 5 else 0).fillna(0).astype(int)

        # Time period & Peak assignment
        period_and_peak = df_actual["hour_of_day"].apply(determine_time_period)
        df_actual["time_period"] = [p[0] for p in period_and_peak]
        df_actual["is_peak_hour"] = [p[1] for p in period_and_peak]

        df_actual["delay_reason"] = df_actual["delay_reason"].fillna("Normal Operations").astype(str).str.strip()
        df_actual["stop_sequence"] = df_actual["stop_sequence"].fillna(1).astype(int)

        # Ensure unique record_id
        df_actual["record_id"] = range(1, len(df_actual) + 1)

        # Save processed files
        df_routes.to_csv(self.processed_dir / "routes_clean.csv", index=False)
        df_stations.to_csv(self.processed_dir / "stations_clean.csv", index=False)
        df_trips.to_csv(self.processed_dir / "trips_clean.csv", index=False)
        df_actual.to_csv(self.processed_dir / "actual_times_clean.csv", index=False)

        self.audit_log["cleaned_counts"] = {
            "routes": len(df_routes),
            "stations": len(df_stations),
            "trips": len(df_trips),
            "actual_times": len(df_actual),
        }
        return df_routes, df_stations, df_trips, df_actual

    def load(
        self,
        df_routes: pd.DataFrame,
        df_stations: pd.DataFrame,
        df_trips: pd.DataFrame,
        df_actual: pd.DataFrame,
    ) -> dict:
        """Loads cleaned dataframes into the SQL database."""
        engine = get_engine()
        # Ensure schema and views are initialized
        init_db(drop_first=True)

        with engine.begin() as conn:
            # Load in relational dependency order
            df_routes.to_sql("routes", conn, if_exists="append", index=False)
            df_stations.to_sql("stations", conn, if_exists="append", index=False)
            df_trips.to_sql("trips", conn, if_exists="append", index=False)
            df_actual.to_sql("actual_times", conn, if_exists="append", index=False)

        health = check_health()
        self.audit_log["database_status"] = health
        return self.audit_log

    def run(self) -> dict:
        """Executes full ETL pipeline: Extract -> Transform -> Load."""
        start_time = datetime.now()
        df_r, df_s, df_t, df_a = self.extract()
        df_r_clean, df_s_clean, df_t_clean, df_a_clean = self.transform(df_r, df_s, df_t, df_a)
        audit = self.load(df_r_clean, df_s_clean, df_t_clean, df_a_clean)
        elapsed = (datetime.now() - start_time).total_seconds()
        audit["duration_seconds"] = round(elapsed, 2)
        return audit


if __name__ == "__main__":
    print("Running Transit ETL Pipeline...")
    pipeline = TransitETLPipeline()
    result = pipeline.run()
    print("ETL execution completed successfully:")
    print(result)
