from __future__ import annotations

import fitz
import pdfplumber


def extract_text_from_pdf(file_path: str) -> str:
    text_parts: list[str] = []

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                if page_text:
                    text_parts.append(page_text)
    except Exception:
        pass

    if text_parts:
        return "\n".join(text_parts)

    with fitz.open(file_path) as doc:
        for page in doc:
            text_parts.append(page.get_text("text"))

    return "\n".join(text_parts)
