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

#This checks something different — actual value sanity 
#(humidity can't be negative or over 100%, wind can't be negative) — at the database itself, after loading
def run_data_quality_checks(conn):
    row_count = conn.execute("SELECT COUNT(*) FROM hourly_weather").fetchone()[0]
    print(f"[query] Row count: {row_count}")

    if row_count == 0:
        raise ValueError("[query] Data quality check failed: table is empty")

    bad_humidity = conn.execute(
        "SELECT COUNT(*) FROM hourly_weather WHERE humidity_pct < 0 OR humidity_pct > 100"
    ).fetchone()[0]
    if bad_humidity > 0:
        raise ValueError(f"[query] Data quality check failed: {bad_humidity} rows with humidity out of range")

    negative_wind = conn.execute(
        "SELECT COUNT(*) FROM hourly_weather WHERE wind_speed_kmh < 0"
    ).fetchone()[0]
    if negative_wind > 0:
        raise ValueError(f"[query] Data quality check failed: {negative_wind} rows with negative wind speed")

    print("[query] Data quality checks passed: row count > 0, humidity in range, wind non-negative")
    

def print_summary(conn):
    hot = get_hottest_hour(conn)
    cold = get_coldest_hour(conn)
    windy = get_windiest_hour(conn)
    avg = get_average_conditions(conn)
    
    print()
    print("=== Weather Summary ===")
    print(f"Hottest hour:  {hot['timestamp']} - {hot['temperature_c']} C")
    print(f"Coldest hour:  {cold['timestamp']} - {cold['temperature_c']} C")
    print(f"Windiest hour: {windy['timestamp']} - {windy['wind_speed_kmh']} km/h")
    print(f"Averages:      {avg['avg_temp']} C, {avg['avg_humidity']}%, {avg['avg_wind']} km/h")

if __name__ == "__main__":
    conn = get_connection()
    run_data_quality_checks(conn)
    print_summary(conn)
    conn.close()