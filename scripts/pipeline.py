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


def run_pipeline(offline_fixture):
    logger.info("Pipeline run started")
    try:
        raw_path = extract(offline_fixture=offline_fixture)
        
        data = load_raw(str(raw_path))
        df = transform_data(data)
        validate(df)
        csv_path = save(df, str(raw_path))
        
        clean_df = load_clean_csv(str(csv_path))
        inserted = insert_rows(clean_df)
        
        conn = get_connection()
        run_data_quality_checks(conn)
        print_summary(conn)
        conn.close()
        
        logger.info(f"Pipeline run completed  successfully - {inserted} new rows inserted")
    except  Exception as e:
        logger.error(f"Pipeline run failed: {e}")
        raise
    
    
if __name__ == "__main__":
    fixture = sys.argv[1] if len(sys.argv) > 1 else None
    run_pipeline(offline_fixture=fixture)
    