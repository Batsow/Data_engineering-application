import sqlite3
import sys
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__). parent.parent / "data"  #wrute to
DB_PATH = DATA_DIR / "weather.db"

CREATE_TABLE_SQL ="""
CREATE TABLE IF NOT EXISTS hourly_weather(
    timestamp TEXT PRIMARY KEY,
    temperature_c REAL NOT NULL,
    humidity_pct INTEGER NOT NULL,
    wind_speed_kmh REAL NOT NULL
);
"""
