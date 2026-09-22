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


def validate(df):
    n_nulls = df.isnull().sum().sum()
    n_duplicates = df["timestamp"].duplicated().sum()
    
    if n_nulls > 0:
        raise ValueError(
                         f"[transform] Found {n_nulls} null values - arborting")
   
    if n_duplicates > 0:
        raise ValueError(
            f"[transfrm] Found {n_duplicates} duplicate timestamps - aborting"
        )
        
    print("[transform] Validationpassed: no nulls, no duplicate timestamps")
    
    
def save(df, source_raw_path):
    raw_stem = Path(source_raw_path).stem
    out_path =DATA_DIR / f"{raw_stem} _clean.csv"
    df.to_csv(out_path, index=False)
    print(f"[transform] Saved clean data -> {out_path}")
    return out_path

if __name__ == "__main__":
    raw_path = sys.argv[1]
    data = load_raw(raw_path)
    df = transform(data)
    validate(df)
    save(df, raw_path)
    