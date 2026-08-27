from __future__ import annotations

from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd

from legal_doc_analytics.analytics import validate_page_metrics


def main() -> None:
    processed = ROOT / "data" / "processed"
    page_csv = processed / "page_metrics.csv"
    document_csv = processed / "document_metrics.csv"
    database = processed / "legal_document_quality.db"

    for path in [page_csv, document_csv, database]:
        if not path.exists():
            raise FileNotFoundError(f"Missing expected output: {path}")

    pages = pd.read_csv(page_csv)
    documents = pd.read_csv(document_csv)
    validate_page_metrics(pages)

    assert documents["document"].nunique() == pages["document"].nunique()
    assert int(documents["pages"].sum()) == len(pages)
    assert pages["valid_word_ratio"].between(0, 1).all()
    assert (pages["processing_seconds"] >= 0).all()

    with sqlite3.connect(database) as conn:
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        assert {"page_metrics", "document_metrics"} <= tables

        db_pages = conn.execute(
            "SELECT COUNT(*) FROM page_metrics"
        ).fetchone()[0]
        assert db_pages == len(pages)

    print("Pipeline validation passed:")
    print(f"  documents: {pages['document'].nunique()}")
    print(f"  pages: {len(pages)}")
    print(f"  page rows in SQLite: {db_pages}")
    print("  quality ratios: valid")
    print("  required tables: present")


if __name__ == "__main__":
    main()
