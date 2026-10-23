"""Realistic Transit Data and GTFS Generator.
Generates comprehensive synthetic metropolitan transit feeds (routes, stations, trips, actual arrival times)
with realistic peak-hour delays, bottleneck propagation, and operational incident patterns.
"""

import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import numpy as np
from config import RAW_DATA_DIR, DELAY_REASONS, TIME_PERIODS

# Fixed master transit entities
MASTER_ROUTES = [
    {
        "route_id": "RT-RED",
        "route_short_name": "Red Line (Subway)",
        "route_long_name": "Downtown Central <-> Tech Hub Innovation Park",
        "route_type": "Subway / Rail",
        "agency_name": "Metropolitan Transit Authority",
        "color_hex": "#DC2626",
        "stops": ["ST-01", "ST-02", "ST-03", "ST-04", "ST-05", "ST-06"]
    },
    {
        "route_id": "RT-BLUE",
        "route_short_name": "Blue Line (Subway)",
        "route_long_name": "West Harbor <-> Airport Terminals Express",
        "route_type": "Subway / Rail",
        "agency_name": "Metropolitan Transit Authority",
        "color_hex": "#2563EB",
        "stops": ["ST-07", "ST-08", "ST-01", "ST-03", "ST-15", "ST-16"]
    },
    {
        "route_id": "RT-GREEN",
        "route_short_name": "Green Line (Light Rail)",
        "route_long_name": "Riverfront Plaza <-> University Heights",
        "route_type": "Light Rail",
        "agency_name": "Metropolitan Transit Authority",
        "color_hex": "#16A34A",
        "stops": ["ST-10", "ST-08", "ST-09", "ST-11", "ST-05"]
    },
    {
        "route_id": "RT-ORANGE",
        "route_short_name": "Orange Line (BRT)",
        "route_long_name": "South Gateway <-> North Suburban Mall",
        "route_type": "Bus Rapid Transit",
        "agency_name": "Metropolitan Transit Authority",
        "color_hex": "#EA580C",
        "stops": ["ST-12", "ST-14", "ST-01", "ST-09", "ST-17"]
    },
    {
        "route_id": "RT-BUS-101",
        "route_short_name": "Bus 101 (Civic Express)",
        "route_long_name": "Civic Center <-> Eastgate Terminal",
        "route_type": "Express Bus",
        "agency_name": "Metropolitan Transit Authority",
        "color_hex": "#9333EA",
        "stops": ["ST-08", "ST-01", "ST-04", "ST-13"]
    },
    {
        "route_id": "RT-CR-305",
        "route_short_name": "Commuter Rail 305",
        "route_long_name": "Union Station <-> Mountain Foothills Regional",
        "route_type": "Commuter Rail",
        "agency_name": "Metropolitan Transit Authority",
        "color_hex": "#0D9488",
        "stops": ["ST-03", "ST-09", "ST-13", "ST-17", "ST-18"]
    }
]

MASTER_STATIONS = [
    {"station_id": "ST-01", "station_code": "DWTN", "station_name": "Downtown Central", "latitude": 40.7128, "longitude": -74.0060, "zone_id": "Zone 1", "is_transfer_station": 1},
    {"station_id": "ST-02", "station_code": "FIND", "station_name": "Financial District", "latitude": 40.7075, "longitude": -74.0090, "zone_id": "Zone 1", "is_transfer_station": 0},
    {"station_id": "ST-03", "station_code": "UNON", "station_name": "Union Station Hub", "latitude": 40.7180, "longitude": -73.9980, "zone_id": "Zone 1", "is_transfer_station": 1},
    {"station_id": "ST-04", "station_code": "HOSP", "station_name": "City Hospital & Medical Ctr", "latitude": 40.7250, "longitude": -73.9900, "zone_id": "Zone 1", "is_transfer_station": 0},
    {"station_id": "ST-05", "station_code": "UNIV", "station_name": "University Heights Campus", "latitude": 40.7350, "longitude": -73.9850, "zone_id": "Zone 2", "is_transfer_station": 1},
    {"station_id": "ST-06", "station_code": "TECH", "station_name": "Tech Hub Innovation Park", "latitude": 40.7480, "longitude": -73.9750, "zone_id": "Zone 2", "is_transfer_station": 0},
    {"station_id": "ST-07", "station_code": "WHRB", "station_name": "West Harbor Terminal", "latitude": 40.7100, "longitude": -74.0200, "zone_id": "Zone 1", "is_transfer_station": 0},
    {"station_id": "ST-08", "station_code": "CIVC", "station_name": "Civic Center & City Hall", "latitude": 40.7150, "longitude": -74.0050, "zone_id": "Zone 1", "is_transfer_station": 1},
    {"station_id": "ST-09", "station_code": "MDWN", "station_name": "Midtown Interchange", "latitude": 40.7300, "longitude": -73.9950, "zone_id": "Zone 1", "is_transfer_station": 1},
    {"station_id": "ST-10", "station_code": "RIVR", "station_name": "Riverfront Promenade", "latitude": 40.7400, "longitude": -74.0100, "zone_id": "Zone 2", "is_transfer_station": 0},
    {"station_id": "ST-11", "station_code": "ARTS", "station_name": "Arts & Museum District", "latitude": 40.7380, "longitude": -73.9920, "zone_id": "Zone 2", "is_transfer_station": 0},
    {"station_id": "ST-12", "station_code": "SGAT", "station_name": "South Gateway Terminal", "latitude": 40.6950, "longitude": -74.0000, "zone_id": "Zone 2", "is_transfer_station": 0},
    {"station_id": "ST-13", "station_code": "EGAT", "station_name": "Eastgate Transfer Terminal", "latitude": 40.7200, "longitude": -73.9650, "zone_id": "Zone 2", "is_transfer_station": 1},
    {"station_id": "ST-14", "station_code": "SMKT", "station_name": "South Market Square", "latitude": 40.7000, "longitude": -73.9800, "zone_id": "Zone 2", "is_transfer_station": 0},
    {"station_id": "ST-15", "station_code": "APR1", "station_name": "International Airport Term 1", "latitude": 40.6450, "longitude": -73.7850, "zone_id": "Zone 3", "is_transfer_station": 1},
    {"station_id": "ST-16", "station_code": "APR2", "station_name": "International Airport Term 2", "latitude": 40.6400, "longitude": -73.7780, "zone_id": "Zone 3", "is_transfer_station": 0},
    {"station_id": "ST-17", "station_code": "NMAL", "station_name": "North Suburban Mall", "latitude": 40.7800, "longitude": -73.9500, "zone_id": "Zone 3", "is_transfer_station": 0},
    {"station_id": "ST-18", "station_code": "MTNF", "station_name": "Mountain Foothills Regional", "latitude": 40.8100, "longitude": -73.9200, "zone_id": "Zone 3", "is_transfer_station": 0}
]

# Bottleneck stations with higher intrinsic passenger volume & dwell delay probability
BOTTLENECK_STATIONS = {"ST-01", "ST-03", "ST-08", "ST-09", "ST-13", "ST-15"}


def classify_delay_status(delay_min: float) -> str:
    """Classifies delay minutes into standard transit performance status."""
    if delay_min < 0.0:
        return "Early"
    elif delay_min <= 2.0:
        return "On-Time"
    elif delay_min <= 5.0:
        return "Minor Delay"
    elif delay_min <= 15.0:
        return "Moderate Delay"
    else:
        return "Severe Delay"


def determine_time_period(hour: int) -> tuple[str, int]:
    """Determines time period name and peak flag (1=Peak, 0=Off-Peak)."""
    if 7 <= hour < 10:
        return "Morning Peak", 1
    elif 10 <= hour < 16:
        return "Off-Peak (Midday)", 0
    elif 16 <= hour < 20:
        return "Evening Peak", 1
    else:
        return "Night / Early Morning", 0


def generate_transit_data(num_days: int = 30, trips_per_day: int = 80, random_seed: int = 42) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Generates synthetic GTFS datasets: routes, stations, trips, actual_times.
    
    Returns:
        tuple: (df_routes, df_stations, df_trips, df_actual_times)
    """
    random.seed(random_seed)
    np.random.seed(random_seed)

    # 1. Routes DataFrame
    df_routes = pd.DataFrame([
        {
            "route_id": r["route_id"],
            "route_short_name": r["route_short_name"],
            "route_long_name": r["route_long_name"],
            "route_type": r["route_type"],
            "agency_name": r["agency_name"],
            "color_hex": r["color_hex"]
        }
        for r in MASTER_ROUTES
    ])

    # 2. Stations DataFrame
    df_stations = pd.DataFrame(MASTER_STATIONS)

    # 3. Trips and Actual Times Generation
    trips_list = []
    actual_times_list = []
    record_id_counter = 1

    # End date: today; Start date: (num_days ago)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=num_days - 1)

    trip_counter = 1000

    # Hours distribution: Peak hours have heavier trip density
    hour_weights = [
        1, 1, 1, 1, 2, 4, 8, 14, 16, 12,  # 00:00 to 09:00 (morning ramp & peak)
        8, 8, 9, 8, 8, 10, 16, 18, 15, 11, # 10:00 to 19:00 (midday & evening peak)
        8, 5, 3, 2                        # 20:00 to 23:00 (night)
    ]
    total_w = sum(hour_weights)
    hour_probs = [w / total_w for w in hour_weights]

    for day_offset in range(num_days):
        current_date = start_date + timedelta(days=day_offset)
        day_of_week = current_date.strftime("%A")
        is_weekend = 1 if current_date.weekday() >= 5 else 0
        service_id = "WEEKEND-REG" if is_weekend else "WEEKDAY-REG"

        # Daily trips count slightly lower on weekends
        daily_target = int(trips_per_day * 0.7) if is_weekend else trips_per_day

        for _ in range(daily_target):
            trip_counter += 1
            trip_id = f"TRIP-{current_date.strftime('%Y%m%d')}-{trip_counter}"
            route = random.choice(MASTER_ROUTES)
            route_id = route["route_id"]
            direction_id = random.choice([0, 1])
            stops_order = list(route["stops"]) if direction_id == 0 else list(reversed(route["stops"]))
            
            # Pick initial departure hour based on probabilistic transit schedule
            departure_hour = np.random.choice(range(24), p=hour_probs)
            departure_minute = random.randint(0, 59)
            base_time = datetime.combine(current_date, datetime.min.time()) + timedelta(
                hours=int(departure_hour), minutes=int(departure_minute)
            )

            trip_headsign = f"{'Inbound to' if direction_id == 1 else 'Outbound to'} {stops_order[-1]}"
            block_id = f"BLK-{route_id[-3:]}-{random.randint(10, 99)}"
            vehicle_id = f"VEH-{random.randint(100, 999)}"

            trips_list.append({
                "trip_id": trip_id,
                "route_id": route_id,
                "service_id": service_id,
                "trip_headsign": trip_headsign,
                "direction_id": direction_id,
                "block_id": block_id,
                "vehicle_id": vehicle_id
            })

            # Cumulative cascading delay along this trip
            accumulated_delay = 0.0

            # Generate arrival & departure records for each station in trip
            for seq_idx, station_id in enumerate(stops_order):
                stop_seq = seq_idx + 1
                travel_minutes = 0 if seq_idx == 0 else random.randint(4, 7)
                dwell_minutes = 1 if seq_idx == 0 or seq_idx == len(stops_order) - 1 else 2

                sched_arr_time = base_time + timedelta(minutes=travel_minutes)
                sched_dep_time = sched_arr_time + timedelta(minutes=dwell_minutes)
                base_time = sched_dep_time

                hour = sched_arr_time.hour
                time_period, is_peak = determine_time_period(hour)

                # Stochastic Delay Modeling:
                # 1. Base normal jitter (-1 to +2 mins)
                jitter = np.random.normal(loc=0.5, scale=1.0)

                # 2. Peak hour congestion factor
                peak_factor = np.random.exponential(scale=2.8) if is_peak else np.random.exponential(scale=0.8)
                
                # 3. Bottleneck station extra dwell/crowding
                bottleneck_factor = np.random.uniform(1.5, 4.0) if station_id in BOTTLENECK_STATIONS else 0.0

                # 4. Weekend relief
                weekend_factor = -0.5 if is_weekend else 0.0

                # Incremental delay introduced at this stop
                stop_delay_increment = jitter + peak_factor + bottleneck_factor + weekend_factor

                # Partial recovery factor if driver can make up time between stations
                recovery = random.uniform(0.3, 0.9) if accumulated_delay > 2.0 else 0.0
                accumulated_delay = max(-2.0, (accumulated_delay * (1.0 - recovery * 0.4)) + stop_delay_increment)

                # 5. Outlier severe delay shock (~3% probability)
                delay_reason = "Normal Operations"
                if random.random() < 0.035:
                    severe_boost = random.uniform(14.0, 32.0)
                    accumulated_delay += severe_boost
                    delay_reason = random.choice([r for r in DELAY_REASONS if r != "Normal Operations"])
                elif accumulated_delay > 5.0:
                    delay_reason = random.choice([
                        "High Passenger Boarding Volume",
                        "Traffic Congestion",
                        "Door Sensor Irregularity",
                        "Signal / Switch Malfunction"
                    ])

                final_delay_minutes = round(float(accumulated_delay), 2)
                status = classify_delay_status(final_delay_minutes)

                actual_arr_time = sched_arr_time + timedelta(minutes=final_delay_minutes)
                # Departure delay follows arrival delay with minor dwell variation
                actual_dep_time = actual_arr_time + timedelta(minutes=dwell_minutes + random.randint(0, 1))

                actual_times_list.append({
                    "record_id": record_id_counter,
                    "trip_id": trip_id,
                    "station_id": station_id,
                    "stop_sequence": stop_seq,
                    "scheduled_arrival": sched_arr_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "actual_arrival": actual_arr_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "scheduled_departure": sched_dep_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "actual_departure": actual_dep_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "delay_minutes": final_delay_minutes,
                    "status": status,
                    "delay_reason": delay_reason,
                    "recorded_date": sched_arr_time.strftime("%Y-%m-%d"),
                    "hour_of_day": hour,
                    "time_period": time_period,
                    "is_peak_hour": is_peak,
                    "is_weekend": is_weekend,
                    "day_of_week": day_of_week
                })
                record_id_counter += 1

    df_trips = pd.DataFrame(trips_list)
    df_actual_times = pd.DataFrame(actual_times_list)

    return df_routes, df_stations, df_trips, df_actual_times


def save_raw_datasets(df_routes: pd.DataFrame, df_stations: pd.DataFrame, df_trips: pd.DataFrame, df_actual_times: pd.DataFrame) -> None:
    """Saves raw transit datasets to CSV files in data/raw/."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df_routes.to_csv(RAW_DATA_DIR / "routes.csv", index=False)
    df_stations.to_csv(RAW_DATA_DIR / "stations.csv", index=False)
    df_trips.to_csv(RAW_DATA_DIR / "trips.csv", index=False)
    df_actual_times.to_csv(RAW_DATA_DIR / "actual_times.csv", index=False)


if __name__ == "__main__":
    print("Generating synthetic metropolitan transit datasets...")
    routes_df, stations_df, trips_df, actual_df = generate_transit_data(num_days=30, trips_per_day=80)
    save_raw_datasets(routes_df, stations_df, trips_df, actual_df)
    print(f"Generated {len(routes_df)} routes, {len(stations_df)} stations, {len(trips_df)} trips, {len(actual_df)} arrival records.")
