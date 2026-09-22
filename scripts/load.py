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


def load_clean_csv(csv_path):
    print(f"[load] Reading clean CSV: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"[load]  {len(df)} rows to insert")
    return df

def insert_rows(df):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(CREATE_TABLE_SQL)
    
    rows_before = conn.execute("SELECT COUNT(*) FROM hourly_weather").fetchone()[0]
    
    insert_sql = """
        INSERT OR IGNORE INTO hourly_weather
        (timestamp, temperature_c, humidity_pct, wind_speed_kmh)
        VALUES (?, ?, ?, ?)
    """
    records = df[["timestamp", "temperature_c", "humidity_pct", "wind_speed_kmh"]].values.tolist()
    conn.executemany(insert_sql, records)
    conn.commit()
    
    rows_after = conn.execute("SELECT COUNT(*) FROM hourly_weather").fetchone()[0]
    conn.close()
    
    inserted = rows_after - rows_before
    print(f"[load] Inserted {inserted} new rows ({len(df) - inserted} already existed)")
    return inserted