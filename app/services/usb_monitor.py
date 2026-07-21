import logging
import threading
from pathlib import Path
from typing import Callable, Optional, Set

import psutil

logger = logging.getLogger(__name__)

_POLL_INTERVAL = 1.0


class USBMonitor:
    def __init__(
        self,
        on_inserted: Callable[[Path], None],
        on_removed: Callable[[Path], None],
    ) -> None:
        self._on_inserted = on_inserted
        self._on_removed = on_removed
        self._known: Set[str] = set()
        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()

    def start(self) -> None:
        self._known = self._removable_drives()
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._loop, daemon=True, name="USBMonitor"
        )
        self._thread.start()
        logger.info("USB monitor started. Drives: %s", self._known)

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=3)

    def get_current(self) -> Optional[Path]:
        drives = self._removable_drives()
        return Path(next(iter(drives))) if drives else None

    def _loop(self) -> None:
        while not self._stop.is_set():
            current = self._removable_drives()

            for d in current - self._known:
                logger.info("USB inserted: %s", d)
                try:
                    self._on_inserted(Path(d))
                except Exception:
                    logger.exception("USB inserted callback error")

            for d in self._known - current:
                logger.info("USB removed: %s", d)
                try:
                    self._on_removed(Path(d))
                except Exception:
                    logger.exception("USB removed callback error")

            self._known = current
            self._stop.wait(timeout=_POLL_INTERVAL)

    @staticmethod
    def _removable_drives() -> Set[str]:
        result: Set[str] = set()
        try:
            for part in psutil.disk_partitions(all=False):
                opts = part.opts.lower()
                if "removable" in opts or part.fstype.upper() in {"FAT32", "EXFAT", "FAT"}:
                    result.add(part.mountpoint)
        except Exception:
            logger.exception("Failed to enumerate disk partitions")
        return result
