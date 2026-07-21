import re
from typing import Optional

_SN_PATTERN = re.compile(r"\b([A-Z0-9]{8})\b")
_ID_PATTERN = re.compile(r"\b(\d{2}S-[A-Z]\d{3})\b")


def extract_serial_number(text: str) -> Optional[str]:
    match = _SN_PATTERN.search(text.upper())
    return match.group(1) if match else None


def extract_device_id(text: str) -> Optional[str]:
    match = _ID_PATTERN.search(text.upper())
    return match.group(1) if match else None


def validate_serial_number(sn: str) -> bool:
    return bool(_SN_PATTERN.fullmatch(sn.strip().upper()))


def validate_device_id(device_id: str) -> bool:
    return bool(_ID_PATTERN.fullmatch(device_id.strip().upper()))


def build_folder_name(sn: str, device_id: str) -> str:
    return f"{sn.strip().upper()}({device_id.strip().upper()})"
