from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd

from legal_doc_analytics.analytics import (
    document_summary,
    summary_metrics,
    validate_page_metrics,
)
from legal_doc_analytics.text_quality import quality_status


def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "document": "a.pdf",
                "page_number": 1,
                "extraction_method": "direct_text",
                "text": "Valid German document text with enough words for quality checks.",
                "character_count": 64,
                "word_count": 10,
                "valid_word_ratio": 0.90,
                "ocr_mean_confidence": None,
                "processing_seconds": 0.10,
                "quality_status": "pass",
                "quality_reason": "quality_checks_passed",
            },
            {
                "document": "a.pdf",
                "page_number": 2,
                "extraction_method": "needs_ocr",
                "text": "bad",
                "character_count": 3,
                "word_count": 1,
                "valid_word_ratio": 1.0,
                "ocr_mean_confidence": None,
                "processing_seconds": 0.08,
                "quality_status": "review",
                "quality_reason": "ocr_required",
            },
            {
                "document": "b.pdf",
                "page_number": 1,
                "extraction_method": "direct_text",
                "text": "Another sufficiently long page with structured regulatory text.",
                "character_count": 61,
                "word_count": 8,
                "valid_word_ratio": 0.88,
                "ocr_mean_confidence": None,
                "processing_seconds": 0.12,
                "quality_status": "pass",
                "quality_reason": "quality_checks_passed",
            },
        ]
    )


def test_quality_status_flags_short_text():
    status, reason = quality_status("short")
    assert status == "review"
    assert reason == "low_character_count"


def test_summary_metrics():
    df = sample_df()
    validate_page_metrics(df)
    summary = summary_metrics(df)

    assert summary["documents"] == 2
    assert summary["pages"] == 3
    assert summary["ocr_required_pages"] == 1
    assert summary["review_pages"] == 1


def test_document_summary():
    result = document_summary(sample_df())
    assert set(result["document"]) == {"a.pdf", "b.pdf"}
    row = result[result["document"] == "a.pdf"].iloc[0]
    assert row["pages"] == 2
    assert row["ocr_required_pages"] == 1
