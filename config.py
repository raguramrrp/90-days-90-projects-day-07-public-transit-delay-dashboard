"""Configuration settings for the Tamil Nadu Public Transport Intelligence Platform.
Supports multimodal transit (MTC Buses, CMRL Metro, Southern Railway Suburban)
with initial geographic coverage focused on Chennai metropolitan area.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
POWERBI_EXPORT_DIR = DATA_DIR / "powerbi_export"
SQL_DIR = BASE_DIR / "sql"
POWERBI_DIR = BASE_DIR / "powerbi"
DOCS_DIR = BASE_DIR / "docs"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

# Ensure runtime directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
POWERBI_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Database URL (defaults to local SQLite database in data/transit.db)
SQLITE_DB_PATH = DATA_DIR / "transit.db"
DEFAULT_DB_URL = f"sqlite:///{SQLITE_DB_PATH.as_posix()}"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)

# Application metadata
APP_NAME = os.getenv("APP_NAME", "Nellai Public Transport Live Tracker (Tirunelveli)")
REGION_NAME = "Tamil Nadu (Tirunelveli Metropolitan Region)"
TIMEZONE = "Asia/Kolkata"
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
PORT = int(os.getenv("PORT", 8501))

# Map Center Coordinates (Tirunelveli Center: Junction / Vannarpettai)
TIRUNELVELI_MAP_CENTER = [8.7285, 77.7050]
CHENNAI_MAP_CENTER = TIRUNELVELI_MAP_CENTER  # Alias for backward compatibility
DEFAULT_ZOOM_LEVEL = 13

# Delay Thresholds (in minutes) - FTA & Indian Urban Transit Standard
DELAY_THRESHOLDS = {
    "EARLY": 0.0,            # < 0.0 mins (ahead of schedule)
    "ON_TIME": 2.0,          # 0.0 to 2.0 mins
    "MINOR_DELAY": 5.0,      # > 2.0 to 5.0 mins
    "MODERATE_DELAY": 15.0,  # > 5.0 to 15.0 mins
}

# Time Periods (24h clock hours in Asia/Kolkata)
TIME_PERIODS = {
    "Morning Peak": (7, 10),       # 07:00 - 09:59 (Nellai morning school & office rush)
    "Off-Peak (Midday)": (10, 16), # 10:00 - 15:59 (Normal flow)
    "Evening Peak": (16, 20),      # 16:00 - 19:59 (Nellai evening return rush)
    "Night / Early Morning": (20, 7) # 20:00 - 06:59 (Night express schedules)
}

# Transport Operators & Modes
TRANSPORT_MODES = ["Bus", "Superfast & Express Rail", "Intercity Express Bus"]

OPERATORS = {
    "AGENCY-TNSTC": {
        "name": "Tamil Nadu State Transport Corporation (TNSTC Tirunelveli)",
        "short_name": "TNSTC Nellai",
        "mode": "Bus",
        "city": "Tirunelveli",
        "color": "#059669",  # TNSTC Emerald Green
        "icon": "🚌"
    },
    "AGENCY-SR": {
        "name": "Southern Railway - Madurai Division (Nellai Hub)",
        "short_name": "Southern Railway (TEN)",
        "mode": "Superfast & Express Rail",
        "city": "Tirunelveli",
        "color": "#DC2626",  # Indian Railways Crimson
        "icon": "🚆"
    },
    "AGENCY-SETC": {
        "name": "State Express Transport Corporation (SETC)",
        "short_name": "SETC Nellai",
        "mode": "Intercity Express Bus",
        "city": "Tirunelveli",
        "color": "#D97706",  # Gold / Amber
        "icon": "🚍"
    }
}

# Vehicle Tracking Data Statuses
VEHICLE_DATA_STATUS = {
    "LIVE": {"label": "LIVE", "badge": "Verified Real-time Feed", "color": "#10B981"},
    "STATIC": {"label": "STATIC", "badge": "Scheduled Timetable Position", "color": "#64748B"},
    "HISTORICAL": {"label": "HISTORICAL", "badge": "Past Trip Observation", "color": "#3B82F6"},
    "SIMULATED": {"label": "SIMULATED", "badge": "Demo Synthetic Movement", "color": "#F59E0B"}
}

# Realistic Delay Root Causes for Chennai Transit
DELAY_REASONS = [
    "Normal Operations",
    "Mount Road (Anna Salai) Heavy Traffic",
    "Guindy Flyover Traffic Bottle-Neck",
    "Koyambedu CMBT Passenger Dwell Crowding",
    "Central Station Signal Interlocking Hold",
    "Track Maintenance Work",
    "Heavy Monsoon Rains & Water Logging",
    "High Boarding Volume at Interchange",
    "Rolling Stock / EMU Brake Inspection",
    "Door Sensor Re-Verification"
]

# Reliability Score (TRI) Classification Tiers
RELIABILITY_TIERS = {
    "High": {"min": 85.0, "color": "#10B981", "badge": "Optimal Performance"},
    "Acceptable": {"min": 70.0, "color": "#3B82F6", "badge": "Standard Service"},
    "Needs Attention": {"min": 50.0, "color": "#F59E0B", "badge": "Elevated Delays"},
    "Critical": {"min": 0.0, "color": "#EF4444", "badge": "Severe Degradation"}
}
