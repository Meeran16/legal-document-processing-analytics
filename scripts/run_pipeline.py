from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from legal_doc_analytics.analytics import (
    document_summary,
    quality_reason_summary,
    summary_metrics,
    validate_page_metrics,
)
from legal_doc_analytics.extraction import extract_directory
from legal_doc_analytics.storage import build_database


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build lightweight PDF text-quality analytics."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=ROOT / "data" / "raw",
        help="Directory containing PDF documents.",
    )
    args = parser.parse_args()

    processed = ROOT / "data" / "processed"
    processed.mkdir(parents=True, exist_ok=True)

    print(f"Reading PDFs from -> {args.input_dir.resolve()}")
    pages = extract_directory(args.input_dir.resolve())

    validate_page_metrics(pages)

    documents = document_summary(pages)
    reasons = quality_reason_summary(pages)
    summary = summary_metrics(pages)

    page_csv = processed / "page_metrics.csv"
    document_csv = processed / "document_metrics.csv"
    reason_csv = processed / "quality_reason_summary.csv"
    summary_json = processed / "summary.json"
    database = processed / "legal_document_quality.db"

    pages.to_csv(page_csv, index=False)
    documents.to_csv(document_csv, index=False)
    reasons.to_csv(reason_csv, index=False)
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    build_database(pages, documents, database)

    print("Pipeline complete.")
    print(f"  documents: {summary['documents']}")
    print(f"  pages: {summary['pages']}")
    print(f"  OCR-required pages: {summary['ocr_required_pages']}")
    print(f"  OCR-required rate: {summary['ocr_required_rate']:.1%}")
    print(f"  review rate: {summary['review_rate']:.1%}")
    print(f"  SQLite database -> {database}")


if __name__ == "__main__":
    main()
