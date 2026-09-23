import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__). parent.parent / "data"  #wrute to
DB_PATH = DATA_DIR / "weather.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_hottest_hour(conn):
    sql = """
        SELECT timestamp, temperature_c
        FROM hourly_weather
        ORDER BY temperature_c DESC
        LIMIT 1
    """
    return conn.execute(sql).fetchone()