import re
from typing import Optional

_SN_PATTERN = re.compile(r"\b([A-Z0-9]{8})\b")
_ID_PATTERN = re.compile(r"\b(\d{2}S-[A-Z]\d{3})\b")


def extract_serial_number(text: str) -> Optional[str]:
    cleaned = text.upper().replace(" ", "").replace("—", "-").replace(":", "")
    match = _SN_PATTERN.search(cleaned)
    if match:
        return match.group(1)
    
    # Try fallback regex for 8-char alphanumeric string with slight character swap
    # e.g., O -> 0, I -> 1
    fallback = cleaned.replace("O", "0").replace("I", "1").replace("Z", "2")
    match_fallback = _SN_PATTERN.search(fallback)
    if match_fallback:
        return match_fallback.group(1)
        
    return None


def extract_device_id(text: str) -> Optional[str]:
    cleaned = text.upper().replace(" ", "").replace("—", "-").replace(":", "")
    match = _ID_PATTERN.search(cleaned)
    if match:
        return match.group(1)
        
    # Handle OCR common misread where 'S' looks like '5' or 'A' looks like '4'
    # Try regex finding 2 digits + (S or 5) + hyphen + (A-Z) + 3 digits
    flex_match = re.search(r"(\d{2})[S5]-([A-Z0-9])(\d{3})", cleaned)
    if flex_match:
        d1, char1, d2 = flex_match.group(1), flex_match.group(2), flex_match.group(3)
        # Fix char1 if OCR read letter as digit
        char_clean = "A" if char1 == "4" else ("B" if char1 == "8" else char1)
        return f"{d1}S-{char_clean}{d2}"
        
    return None


def validate_serial_number(sn: str) -> bool:
    return bool(_SN_PATTERN.fullmatch(sn.strip().upper()))


def validate_device_id(device_id: str) -> bool:
    return bool(_ID_PATTERN.fullmatch(device_id.strip().upper()))


def build_folder_name(sn: str, device_id: str) -> str:
    return f"{sn.strip().upper()}({device_id.strip().upper()})"

