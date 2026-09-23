import sys
import time
import schedule
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pipeline import run_pipeline, logger

def start_scheduler(offline_fixture: str | None = None, interval_seconds: int = 30, max_runs: int | None = None) -> None:
    run_count = 0

    def job():
        nonlocal run_count
        run_count += 1
        logger.info(f"Schedular triggered run #{run_count}")
        try:
            run_pipeline(offline_fixture=offline_fixture)
        except Exception:
            logger.error("Scheduled run failed - see log above for details")
    
    schedule.every(interval_seconds).seconds.do(job)
    
    logger.info("Scheduler started - running every {interval_seconds}s. Press Ctrl+C to stop.")
    job() # run once immediately, don't wait for the first interval
    
    while max_runs is None or run_count < max_runs:
        schedule.run_pending()
        time.sleep(1)

    logger.info(f"Scheduler stopped after {run_count} runs (max_runs reached)")


if __name__ == "__main__":
    fixture = sys.argv[1] if len(sys.argv) > 1 else None
    start_scheduler(offline_fixture=fixture, interval_seconds=10, max_runs=3)
