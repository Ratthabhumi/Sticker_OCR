import logging
from pathlib import Path
from typing import Optional

import cv2
import numpy as np

logger = logging.getLogger(__name__)

_MIN_ASPECT = 1.2
_MAX_ASPECT = 7.0
_MIN_AREA_RATIO = 0.04


def crop_sticker(image_path: Path, padding: int = 20) -> Optional[np.ndarray]:
    """
    Detect the sticker region in the photo and return it as a numpy array.
    Falls back to the full image if detection fails.
    Returns None only if the image cannot be read at all.
    """
    img = cv2.imread(str(image_path))
    if img is None:
        logger.warning("Cannot read image: %s", image_path)
        return None

    region = _detect_sticker_region(img, padding)
    return region if region is not None else img


def _detect_sticker_region(img: np.ndarray, padding: int) -> Optional[np.ndarray]:
    h, w = img.shape[:2]
    image_area = h * w

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2,
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    best = _best_contour(contours, image_area)
    if best is None:
        return None

    x, y, cw, ch = cv2.boundingRect(best)
    x1 = max(0, x - padding)
    y1 = max(0, y - padding)
    x2 = min(w, x + cw + padding)
    y2 = min(h, y + ch + padding)

    logger.debug("Cropped sticker: (%d,%d)→(%d,%d)", x1, y1, x2, y2)
    return img[y1:y2, x1:x2]


def _best_contour(contours: list, image_area: int) -> Optional[np.ndarray]:
    candidates = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < image_area * _MIN_AREA_RATIO:
            continue
        x, y, cw, ch = cv2.boundingRect(c)
        if ch == 0:
            continue
        aspect = cw / ch
        if _MIN_ASPECT <= aspect <= _MAX_ASPECT:
            candidates.append((area, c))

    if not candidates:
        return None
    candidates.sort(key=lambda t: t[0], reverse=True)
    return candidates[0][1]
