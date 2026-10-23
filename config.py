"""Configuration settings for the Public Transit Delay Analytics Dashboard."""

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
APP_NAME = os.getenv("APP_NAME", "Public Transit Delay Analytics Dashboard")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
PORT = int(os.getenv("PORT", 8501))

# Delay Thresholds (in minutes)
DELAY_THRESHOLDS = {
    "EARLY": 0.0,            # < 0.0 mins
    "ON_TIME": 2.0,          # 0.0 to 2.0 mins
    "MINOR_DELAY": 5.0,      # > 2.0 to 5.0 mins
    "MODERATE_DELAY": 15.0,  # > 5.0 to 15.0 mins
    # > 15.0 mins is classified as SEVERE_DELAY
}

# Time Periods (24h clock hours)
TIME_PERIODS = {
    "Morning Peak": (7, 10),     # 07:00 - 09:59
    "Off-Peak (Midday)": (10, 16), # 10:00 - 15:59
    "Evening Peak": (16, 20),    # 16:00 - 19:59
    "Night / Early Morning": (20, 7) # 20:00 - 06:59
}

# Delay Reasons Catalog
DELAY_REASONS = [
    "Normal Operations",
    "High Passenger Boarding Volume",
    "Signal / Switch Malfunction",
    "Traffic Congestion",
    "Track Maintenance Work",
    "Mechanical / Vehicle Fault",
    "Inclement Weather Conditions",
    "Crew Scheduling Hold",
    "Emergency Medical Response",
    "Door Sensor Irregularity"
]

# Reliability Score (TRI) Classification Tiers
RELIABILITY_TIERS = {
    "High": {"min": 85.0, "color": "#10B981", "badge": "Optimal Performance"},
    "Acceptable": {"min": 70.0, "color": "#3B82F6", "badge": "Standard Service"},
    "Needs Attention": {"min": 50.0, "color": "#F59E0B", "badge": "Elevated Delays"},
    "Critical": {"min": 0.0, "color": "#EF4444", "badge": "Severe Degradation"}
}
