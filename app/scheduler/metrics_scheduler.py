import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.metrics.metrics_collector import collect_metrics


def start_scheduler():

    interval_minutes = int(os.getenv("METRICS_SCHEDULER_INTERVAL_MINUTES", "60"))

    def metrics_job():
        collect_metrics()
        print(f"Zadanie uruchomione (co {interval_minutes} minut)!")

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        metrics_job,
        IntervalTrigger(minutes=interval_minutes),
        max_instances=1,   # Nie pozwól uruchomić więcej niż jednej instancji
        coalesce=True      # Jeśli zadanie się spóźni, połącz je z następnym i wykonaj tylko jedno
    )   
    scheduler.start()

    print(f"Scheduler uruchomiony. Zadanie co {interval_minutes} minut.")
