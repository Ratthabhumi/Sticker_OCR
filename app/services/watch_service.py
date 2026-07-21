import logging
import threading
from pathlib import Path
from typing import Callable, Optional

from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileMovedEvent
from watchdog.observers import Observer

from app.constants import SUPPORTED_IMAGE_EXTENSIONS

logger = logging.getLogger(__name__)


class _ImageHandler(FileSystemEventHandler):
    def __init__(self, callback: Callable[[Path], None]) -> None:
        super().__init__()
        self._callback = callback
        self._seen: set[Path] = set()
        self._lock = threading.Lock()

    def on_created(self, event: FileCreatedEvent) -> None:
        if not event.is_directory:
            self._dispatch(Path(event.src_path))

    def on_moved(self, event: FileMovedEvent) -> None:
        if not event.is_directory:
            self._dispatch(Path(event.dest_path))

    def _dispatch(self, path: Path) -> None:
        if path.suffix.lower() not in SUPPORTED_IMAGE_EXTENSIONS:
            return
        with self._lock:
            if path in self._seen:
                return
            self._seen.add(path)
        logger.info("New image: %s", path.name)
        self._callback(path)


class WatchService:
    def __init__(self, watch_folder: Path, callback: Callable[[Path], None]) -> None:
        self._folder = watch_folder
        self._handler = _ImageHandler(callback)
        self._observer: Optional[Observer] = None

    def start(self) -> None:
        self._folder.mkdir(parents=True, exist_ok=True)
        self._observer = Observer()
        self._observer.schedule(self._handler, str(self._folder), recursive=False)
        self._observer.start()
        logger.info("Watching: %s", self._folder)

    def stop(self) -> None:
        if self._observer:
            self._observer.stop()
            self._observer.join()

    def scan_existing(self) -> list[Path]:
        return [
            p for p in self._folder.iterdir()
            if p.is_file() and p.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
        ]
