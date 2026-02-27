import re
from pathlib import Path

DOC_CODE_REGEX = re.compile(r"\b([A-Z]{2}-\d{4}\.\d{2}-\d{4}-\d{3}-[A-Z0-9]{3}-\d{3})\b")
REV_REGEX = re.compile(r"\bREV\s*([0-9A-Z]+)\b", re.IGNORECASE)


AREA_HINTS = [
    "Oficina Elétrica",
    "Caldeiraria",
    "Tubulação",
    "Área de Vivência",
    "Administrativo",
]


def detect_document_code(text: str, filename: str) -> str | None:
    match = DOC_CODE_REGEX.search(text) or DOC_CODE_REGEX.search(filename)
    return match.group(1) if match else None


def detect_revision(text: str, filename: str) -> str:
    match = REV_REGEX.search(text) or REV_REGEX.search(filename)
    return match.group(1).upper() if match else "0"


def infer_document_type(document_code: str) -> str:
    return document_code.split("-")[0] if "-" in document_code else "UNK"


def revision_to_order(revision: str) -> int:
    if revision.isdigit():
        return int(revision)
    if len(revision) == 1 and revision.isalpha():
        return 100 + ord(revision.upper()) - ord("A")
    return 999


def safe_filename(name: str) -> str:
    return Path(name).name.replace(" ", "_")
