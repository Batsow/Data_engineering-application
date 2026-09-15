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