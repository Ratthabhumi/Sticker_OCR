import logging
from pathlib import Path

from app.models.result import FolderResult

logger = logging.getLogger(__name__)


class FolderService:
    def create_job_folder(self, usb_root: Path, folder_name: str) -> FolderResult:
        """
        Create <usb_root>/<folder_name>/Picture/.
        Returns a FolderResult describing success, duplicate, or failure.
        """
        job_folder = usb_root / folder_name
        picture_folder = job_folder / "Picture"

        if job_folder.exists():
            logger.info("Duplicate detected: %s", job_folder)
            return FolderResult(success=False, folder_path=job_folder, is_duplicate=True)

        try:
            picture_folder.mkdir(parents=True, exist_ok=False)
            logger.info("Created: %s", picture_folder)
            return FolderResult(success=True, folder_path=job_folder)
        except PermissionError as exc:
            logger.error("Permission denied: %s — %s", job_folder, exc)
            return FolderResult(success=False, error_message=f"Permission denied: {exc}")
        except OSError as exc:
            logger.error("OS error: %s — %s", job_folder, exc)
            return FolderResult(success=False, error_message=str(exc))
