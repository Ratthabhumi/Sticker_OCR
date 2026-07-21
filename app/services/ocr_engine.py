import logging
from typing import Optional, List

import numpy as np

from app.models.result import OCRResult
from app.services.crop_service import get_image_rotations
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
    """Run PaddleOCR with multi-orientation scan until both S/N and ID are extracted."""
    if image is None:
        return OCRResult()

    rotations = get_image_rotations(image)
    best_result = OCRResult()

    for idx, rot_img in enumerate(rotations):
        res = _single_pass_ocr(rot_img, language, use_gpu)
        logger.info("OCR Pass %d (rotation %d°): SN=%s, ID=%s", idx + 1, idx * 90, res.serial_number, res.device_id)

        if res.is_complete:
            return res

        # Keep best partial result
        if res.serial_number and not best_result.serial_number:
            best_result.serial_number = res.serial_number
        if res.device_id and not best_result.device_id:
            best_result.device_id = res.device_id
        if res.raw_text:
            best_result.raw_text += f"\n--- Rotation {idx * 90}° ---\n" + res.raw_text

        if best_result.is_complete:
            return best_result

    return best_result


def _single_pass_ocr(image: np.ndarray, language: str, use_gpu: bool) -> OCRResult:
    try:
        ocr = _get_ocr(language, use_gpu)
        results = ocr.ocr(image, cls=True)
    except Exception:
        logger.exception("PaddleOCR execution failed")
        return OCRResult()

    if not results or not results[0]:
        return OCRResult()

    lines: list[str] = []
    for item in results[0]:
        if item and len(item) >= 2:
            text, _conf = item[1]
            lines.append(str(text))

    full_text = "\n".join(lines)

    return OCRResult(
        serial_number=_find_serial_number(lines),
        device_id=_find_device_id(lines),
        raw_text=full_text,
    )


def _clean_ocr_confusion(text: str) -> str:
    """Clean common OCR typos (e.g., 'O' vs '0', 'I' vs '1')."""
    text = text.upper().strip()
    text = text.replace(" ", "").replace("—", "-").replace("–", "-")
    return text


def _find_serial_number(lines: list[str]) -> Optional[str]:
    for i, line in enumerate(lines):
        upper = line.upper().strip()
        if "S/N" in upper or "SN" in upper or "SERIAL" in upper:
            inline = upper.replace("S/N:", "").replace("S/N", "").replace("SN:", "").replace("SN", "").strip()
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
        if "ID NO" in upper or "ID:" in upper or "ID" in upper:
            inline = (
                upper.replace("ID NO.", "")
                .replace("ID NO", "")
                .replace("ID:", "")
                .replace("ID", "")
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

