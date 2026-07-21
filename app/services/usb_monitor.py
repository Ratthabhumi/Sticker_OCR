import ctypes
import logging
import os
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
        system_drive = os.environ.get("SystemDrive", "C:").upper().rstrip("\\") + "\\"
        app_drive = Path(__file__).anchor.upper()

        try:
            for part in psutil.disk_partitions(all=False):
                mount = part.mountpoint.upper()
                opts = part.opts.lower()

                # Skip system drive (C:\) and app drive
                if mount.startswith(system_drive) or mount.startswith(app_drive):
                    continue

                # Check Windows Drive Type API
                if hasattr(ctypes, "windll"):
                    try:
                        dt = ctypes.windll.kernel32.GetDriveTypeW(part.mountpoint)
                        # 2 = DRIVE_REMOVABLE, 3 = DRIVE_FIXED, 4 = DRIVE_REMOTE, 5 = DRIVE_CDROM
                        if dt in (4, 5):  # Skip network & CD-ROM
                            continue
                        if dt in (2, 3):  # Accept Removable & External USB Drives (F:\, H:\, etc.)
                            result.add(part.mountpoint)
                            continue
                    except Exception:
                        pass

                # Fallback checks
                if "removable" in opts or part.fstype.upper() in {"FAT32", "EXFAT", "FAT", "NTFS"}:
                    result.add(part.mountpoint)
        except Exception:
            logger.exception("Failed to enumerate disk partitions")
        return result
