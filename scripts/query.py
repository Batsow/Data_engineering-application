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


def get_coldest_hour(conn):
    sql = """
        SELECT timestamp, temperature_c
        FROM hourly_weather
        ORDER BY temperature_c ASC
        LIMIT 1
    """
    return conn.execute(sql).fetchone()


def get_windiest_hour(conn):
    sql = """
        SELECT timestamp, wind_speed_kmh
        FROM hourly_weather
        ORDER BY wind_speed_kmh DESC
        LIMIT 1
    """
    return conn.execute(sql).fetchone()


def get_average_conditions(conn):
    sql = """
        SELECT
            ROUND(AVG(temperature_c), 1) AS avg_temp,
            ROUND(AVG(humidity_pct), 1) AS avg_humidity,
            ROUND(AVG(wind_speed_kmh), 1) AS avg_wind
        FROM hourly_weather
    """
    return conn.execute(sql).fetchone()
    
