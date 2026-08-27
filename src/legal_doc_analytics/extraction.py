from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter

import pandas as pd
import pymupdf

from .text_quality import (
    QualityThresholds,
    quality_status,
    tokenize_words,
    valid_word_ratio,
)


@dataclass
class PageRecord:
    document: str
    page_number: int
    extraction_method: str
    text: str
    character_count: int
    word_count: int
    valid_word_ratio: float
    ocr_mean_confidence: float | None
    processing_seconds: float
    quality_status: str
    quality_reason: str


def extract_pdf(
    pdf_path: str | Path,
    *,
    direct_text_min_characters: int = 50,
    thresholds: QualityThresholds | None = None,
    **_: object,
) -> list[PageRecord]:
    """
    Lightweight portfolio extractor.

    It reads embedded PDF text only. Pages with too little embedded text are
    flagged as 'needs_ocr' instead of invoking Tesseract or downloading OCR
    models/software.
    """
    pdf_path = Path(pdf_path)
    records: list[PageRecord] = []

    with pymupdf.open(pdf_path) as document:
        for page_index, page in enumerate(document):
            started = perf_counter()

            text = page.get_text("text").strip()
            words = tokenize_words(text)

            if len(text) < direct_text_min_characters:
                extraction_method = "needs_ocr"
                status = "review"
                reason = "ocr_required"
            else:
                extraction_method = "direct_text"
                status, reason = quality_status(text, thresholds)

            elapsed = perf_counter() - started

            records.append(
                PageRecord(
                    document=pdf_path.name,
                    page_number=page_index + 1,
                    extraction_method=extraction_method,
                    text=text,
                    character_count=len(text),
                    word_count=len(words),
                    valid_word_ratio=round(valid_word_ratio(words), 4),
                    ocr_mean_confidence=None,
                    processing_seconds=round(elapsed, 4),
                    quality_status=status,
                    quality_reason=reason,
                )
            )

    return records


def extract_directory(
    input_dir: str | Path,
    **kwargs,
) -> pd.DataFrame:
    input_dir = Path(input_dir)
    pdfs = sorted(input_dir.glob("*.pdf"))

    if not pdfs:
        raise FileNotFoundError(
            f"No PDF files found in {input_dir}. "
            "Add local PDF documents to data/raw or pass --input-dir."
        )

    rows: list[dict] = []

    for pdf in pdfs:
        for record in extract_pdf(pdf, **kwargs):
            rows.append(asdict(record))

    return pd.DataFrame(rows)
