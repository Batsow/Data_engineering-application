import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from extract import extract
from transform import load_raw, transform as transform_data, validate, save
from load import load_clean_csv, insert_rows
from query import get_connection, run_data_quality_checks, print_summary

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("pipeline")