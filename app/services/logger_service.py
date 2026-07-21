import csv
import logging
import threading
from datetime import date
from pathlib import Path

from app.models.job import ProcessingJob

logger = logging.getLogger(__name__)

_FIELDS = ["Time", "SN", "ID", "Folder", "USB", "Status", "Error"]


class CSVLogger:
    def __init__(self, log_folder: Path) -> None:
        self._folder = log_folder
        self._lock = threading.Lock()

    def log_job(self, job: ProcessingJob) -> None:
        self._folder.mkdir(parents=True, exist_ok=True)
        log_file = self._folder / f"log_{date.today().strftime('%Y-%m-%d')}.csv"

        with self._lock:
            needs_header = not log_file.exists()
            try:
                with open(log_file, "a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=_FIELDS)
                    if needs_header:
                        writer.writeheader()
                    ts = job.processed_at or job.created_at
                    writer.writerow({
                        "Time": ts.strftime("%H:%M:%S"),
                        "SN": job.serial_number or "",
                        "ID": job.device_id or "",
                        "Folder": job.folder_name,
                        "USB": str(job.usb_path) if job.usb_path else "",
                        "Status": job.status.label(),
                        "Error": job.error_message or "",
                    })
            except OSError as exc:
                logger.error("CSV write failed: %s", exc)
