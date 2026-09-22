import json
import sys
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "raw"  #read from
DATA_DIR = Path(__file__). parent.parent / "data"  #wrute to

def load_raw(raw_path):
    print(f"[transform] loading raw file: {raw_path}")
    with open(raw_path) as f:
        return json.load(f)
    

def transform(data):
    hourly = data["hourly"]
    
    df = pd.DataFrame({
        "timestamp": hourly["time"],
        "temperature_c": hourly["temperature_2m"],
        "humidity_pct": hourly["relative_humidity_2m"],
        "wind_speed_kmh": hourly["wind_speed_10m"],
    })
    
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop =True)
    
    print(f"[transform] Built {len(df)} rows")
    return df