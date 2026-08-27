from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {
    "document",
    "page_number",
    "extraction_method",
    "character_count",
    "word_count",
    "valid_word_ratio",
    "ocr_mean_confidence",
    "processing_seconds",
    "quality_status",
    "quality_reason",
}


def validate_page_metrics(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if df.empty:
        raise ValueError("Page metrics dataset is empty.")

    if df[["document", "page_number"]].duplicated().any():
        raise ValueError("Duplicate document/page records found.")

    if (df["page_number"] < 1).any():
        raise ValueError("Invalid page number found.")

    if (~df["extraction_method"].isin(["direct_text", "needs_ocr"])).any():
        raise ValueError("Unknown extraction method found.")

    if (~df["quality_status"].isin(["pass", "review"])).any():
        raise ValueError("Unknown quality status found.")


def summary_metrics(df: pd.DataFrame) -> dict[str, float | int]:
    validate_page_metrics(df)

    total_pages = len(df)
    needs_ocr = int((df["extraction_method"] == "needs_ocr").sum())
    review_pages = int((df["quality_status"] == "review").sum())

    return {
        "documents": int(df["document"].nunique()),
        "pages": int(total_pages),
        "ocr_required_pages": needs_ocr,
        "ocr_required_rate": round(needs_ocr / total_pages, 4),
        "review_pages": review_pages,
        "review_rate": round(review_pages / total_pages, 4),
        "average_character_count": round(float(df["character_count"].mean()), 2),
        "average_word_count": round(float(df["word_count"].mean()), 2),
        "average_processing_seconds": round(float(df["processing_seconds"].mean()), 4),
    }


def document_summary(df: pd.DataFrame) -> pd.DataFrame:
    validate_page_metrics(df)

    grouped = (
        df.groupby("document", as_index=False)
        .agg(
            pages=("page_number", "count"),
            ocr_required_pages=(
                "extraction_method",
                lambda s: int((s == "needs_ocr").sum()),
            ),
            review_pages=("quality_status", lambda s: int((s == "review").sum())),
            average_character_count=("character_count", "mean"),
            average_word_count=("word_count", "mean"),
            average_processing_seconds=("processing_seconds", "mean"),
        )
    )

    grouped["ocr_required_rate"] = (
        grouped["ocr_required_pages"] / grouped["pages"]
    ).round(4)
    grouped["review_rate"] = (
        grouped["review_pages"] / grouped["pages"]
    ).round(4)

    return grouped.sort_values(
        ["review_rate", "ocr_required_rate", "document"],
        ascending=[False, False, True],
    )


def quality_reason_summary(df: pd.DataFrame) -> pd.DataFrame:
    validate_page_metrics(df)

    return (
        df["quality_reason"]
        .value_counts(dropna=False)
        .rename_axis("quality_reason")
        .reset_index(name="pages")
    )
