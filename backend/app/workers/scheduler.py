from apscheduler.schedulers.background import BackgroundScheduler

from app.core.config import settings
from app.db.session import SessionLocal
from app.ingestion.pipeline import run_ingestion

scheduler = BackgroundScheduler()


def scheduled_ingestion():
    db = SessionLocal()
    try:
        run_ingestion(db)
    finally:
        db.close()


def start_scheduler():
    if not settings.scheduler_enabled:
        return
    scheduler.add_job(scheduled_ingestion, "interval", minutes=settings.scheduler_interval_minutes, id="ingestion", replace_existing=True)
    scheduler.start()
