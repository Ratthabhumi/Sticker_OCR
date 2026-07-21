import logging
from typing import Optional

import numpy as np

from app.models.result import OCRResult
from app.services.validator import extract_serial_number, extract_device_id

logger = logging.getLogger(__name__)

_paddle_ocr = None


def _get_ocr(language: str, use_gpu: bool):
    global _paddle_ocr
    if _paddle_ocr is None:
        from paddleocr import PaddleOCR
        logger.info("Initialising PaddleOCR (lang=%s, gpu=%s)", language, use_gpu)
        _paddle_ocr = PaddleOCR(
            use_angle_cls=True,
            lang=language,
            use_gpu=use_gpu,
            show_log=False,
        )
    return _paddle_ocr


def run_ocr(image: np.ndarray, language: str = "en", use_gpu: bool = False) -> OCRResult:
    """Run PaddleOCR on a numpy image; return extracted S/N and ID."""
    try:
        ocr = _get_ocr(language, use_gpu)
        results = ocr.ocr(image, cls=True)
    except Exception:
        logger.exception("PaddleOCR execution failed")
        return OCRResult()

    if not results or not results[0]:
        logger.warning("PaddleOCR returned empty result")
        return OCRResult()

    lines: list[str] = []
    for item in results[0]:
        if item and len(item) >= 2:
            text, _conf = item[1]
            lines.append(str(text))

    full_text = "\n".join(lines)
    logger.debug("OCR raw output:\n%s", full_text)

    return OCRResult(
        serial_number=_find_serial_number(lines),
        device_id=_find_device_id(lines),
        raw_text=full_text,
    )


def _find_serial_number(lines: list[str]) -> Optional[str]:
    for i, line in enumerate(lines):
        upper = line.upper().strip()
        if "S/N" in upper or upper.startswith("SN"):
            inline = upper.replace("S/N:", "").replace("S/N", "").strip()
            sn = extract_serial_number(inline)
            if sn:
                return sn
            if i + 1 < len(lines):
                sn = extract_serial_number(lines[i + 1])
                if sn:
                    return sn

    for line in lines:
        sn = extract_serial_number(line)
        if sn:
            return sn
    return None


def _find_device_id(lines: list[str]) -> Optional[str]:
    for i, line in enumerate(lines):
        upper = line.upper().strip()
        if "ID NO" in upper or "ID:" in upper:
            inline = (
                upper.replace("ID NO.", "")
                .replace("ID NO", "")
                .replace("ID:", "")
                .strip()
            )
            did = extract_device_id(inline)
            if did:
                return did
            if i + 1 < len(lines):
                did = extract_device_id(lines[i + 1])
                if did:
                    return did

    for line in lines:
        did = extract_device_id(line)
        if did:
            return did
    return None
