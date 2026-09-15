import json
import sys
import requests
from datetime import datetime, timezone
from pathlib import Path

API_URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude" : -26.2041,
    "longitude": 28.0473,
    "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    "timezone": "Africa/Johannesburg",
    "forecast_days": 1,
}

RAW_DIR = Path(__file__).parent.parent / "raw"



def extract(offline_fixture): 
    if offline_fixture:
        print(f"[extract] No live network here - loading fixture: {offline_fixture}")
        with open(offline_fixture) as f:
            data = json.load(f)
            
    else:
        print(f"[extract] Calling live API: {API_URL}")
        response = requests.get(API_URL, params=PARAMS, timeout=10)
        response.raise_for_status()
        data = response.json
        
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = RAW_DIR / f"weather_{timestamp}.json"
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"[extract] Saved raw data -> {out_path}")
    return out_path
    
    
    
if __name__ == "__main__":
    fixture = sys.argv[1] if len(sys.argv) > 1 else None
    extract(offline_fixture=fixture)