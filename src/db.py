"""Database management module for Tamil Nadu Public Transport Intelligence Platform.
Supports SQLite (local 1-click execution) and PostgreSQL (production).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from config import DATABASE_URL, SQL_DIR, SQLITE_DB_PATH, DATA_DIR


def get_engine() -> Engine:
    """Creates and returns the SQLAlchemy engine."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    return engine


def init_db(drop_first: bool = False) -> None:
    """Initializes tables and views from SQL schema scripts."""
    engine = get_engine()
    is_sqlite = DATABASE_URL.startswith("sqlite")

    schema_file = SQL_DIR / "01_schema.sql"
    views_file = SQL_DIR / "02_views_kpis.sql"

    with open(schema_file, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    with open(views_file, "r", encoding="utf-8") as f:
        views_sql = f.read()

    if is_sqlite:
        schema_sql = schema_sql.replace("DOUBLE PRECISION", "REAL")
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.executescript(schema_sql)
        cursor.executescript(views_sql)
        conn.commit()
        conn.close()
    else:
        with engine.connect() as conn:
            for statement in schema_sql.split(";"):
                stmt = statement.strip()
                if stmt:
                    conn.execute(text(stmt))
            for statement in views_sql.split(";"):
                stmt = statement.strip()
                if stmt:
                    conn.execute(text(stmt))
            conn.commit()


def execute_query(sql_query: str, params: dict = None) -> pd.DataFrame:
    """Executes a SQL SELECT query and returns the results as a pandas DataFrame."""
    engine = get_engine()
    with engine.connect() as conn:
        if params:
            df = pd.read_sql_query(text(sql_query), conn, params=params)
        else:
            df = pd.read_sql_query(text(sql_query), conn)
    return df


def execute_non_query(sql_stmt: str, params: dict = None) -> None:
    """Executes an INSERT, UPDATE, or DELETE SQL statement."""
    engine = get_engine()
    with engine.begin() as conn:
        if params:
            conn.execute(text(sql_stmt), params)
        else:
            conn.execute(text(sql_stmt))


def check_health() -> dict:
    """Checks database connectivity and table row counts."""
    engine = get_engine()
    status = {"connected": False, "tables": {}, "engine_type": engine.name}
    try:
        with engine.connect() as conn:
            status["connected"] = True
            tables = [
                "operators", "routes", "stations", "trips",
                "actual_times", "vehicles", "vehicle_positions",
                "data_sources", "import_history"
            ]
            for table in tables:
                try:
                    res = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                    status["tables"][table] = res
                except Exception:
                    status["tables"][table] = 0
    except Exception as e:
        status["error"] = str(e)
    return status
