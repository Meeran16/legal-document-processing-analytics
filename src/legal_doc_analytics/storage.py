from __future__ import annotations

from pathlib import Path
import sqlite3
import pandas as pd


def build_database(
    page_metrics: pd.DataFrame,
    document_metrics: pd.DataFrame,
    database_path: str | Path,
) -> Path:
    database_path = Path(database_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(database_path) as conn:
        page_metrics.to_sql("page_metrics", conn, if_exists="replace", index=False)
        document_metrics.to_sql("document_metrics", conn, if_exists="replace", index=False)

        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_page_document "
            "ON page_metrics(document, page_number)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_page_quality "
            "ON page_metrics(quality_status, extraction_method)"
        )

    return database_path
