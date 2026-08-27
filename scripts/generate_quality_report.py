from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt
import pandas as pd

from legal_doc_analytics.analytics import summary_metrics, validate_page_metrics


def save_count_chart(series: pd.Series, title: str, xlabel: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    series.plot(kind="bar", ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Pages")
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_text_volume_chart(df: pd.DataFrame, path: Path) -> None:
    ordered = df.sort_values(["document", "page_number"]).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.plot(
        range(1, len(ordered) + 1),
        ordered["character_count"],
        marker="o",
        markersize=3,
        linewidth=1.2,
    )
    ax.set_title("Extracted text volume by page")
    ax.set_xlabel("Page sequence")
    ax.set_ylabel("Characters")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"

    headers = list(df.columns)
    rows = [
        "| " + " | ".join(str(h) for h in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]

    for _, row in df.iterrows():
        rows.append("| " + " | ".join(str(row[h]) for h in headers) + " |")

    return "\n".join(rows)


def main() -> None:
    processed = ROOT / "data" / "processed"
    figures = ROOT / "reports" / "figures"
    figures.mkdir(parents=True, exist_ok=True)

    page_csv = processed / "page_metrics.csv"
    if not page_csv.exists():
        raise FileNotFoundError(
            "Missing data/processed/page_metrics.csv. "
            "Run python scripts/run_pipeline.py first."
        )

    df = pd.read_csv(page_csv)
    validate_page_metrics(df)
    summary = summary_metrics(df)

    extraction_counts = df["extraction_method"].value_counts()
    quality_counts = df["quality_status"].value_counts()

    save_count_chart(
        extraction_counts,
        "Text extraction outcome",
        "Extraction method",
        figures / "extraction_method_distribution.png",
    )

    save_count_chart(
        quality_counts,
        "Page quality status",
        "Status",
        figures / "quality_status_distribution.png",
    )

    save_text_volume_chart(
        df,
        figures / "text_volume_by_page.png",
    )

    lowest_text = (
        df.sort_values(["character_count", "document", "page_number"])
        .loc[
            :,
            [
                "document",
                "page_number",
                "extraction_method",
                "character_count",
                "quality_status",
                "quality_reason",
            ],
        ]
        .head(5)
        .copy()
    )

    lowest_text.columns = [
        "Document",
        "Page",
        "Method",
        "Characters",
        "Status",
        "Reason",
    ]

    direct_pages = int((df["extraction_method"] == "direct_text").sum())

    report = ROOT / "reports" / "quality_summary.md"
    report.write_text(
        "\n".join(
            [
                "# Document Quality Analytics",
                "",
                "## Snapshot",
                "",
                "| Metric | Value |",
                "| --- | ---: |",
                f"| Documents | {summary['documents']} |",
                f"| Pages | {summary['pages']} |",
                f"| Direct-text pages | {direct_pages} |",
                f"| Pages flagged as needing OCR | {summary['ocr_required_pages']} |",
                f"| OCR-required rate | {summary['ocr_required_rate']:.1%} |",
                f"| Pages requiring review | {summary['review_pages']} |",
                f"| Review rate | {summary['review_rate']:.1%} |",
                f"| Average characters per page | {summary['average_character_count']} |",
                f"| Average words per page | {summary['average_word_count']} |",
                "",
                "## Lowest-text pages",
                "",
                markdown_table(lowest_text),
                "",
                "## Portfolio figures",
                "",
                "![Extraction outcome](figures/extraction_method_distribution.png)",
                "",
                "![Page quality status](figures/quality_status_distribution.png)",
                "",
                "![Text volume by page](figures/text_volume_by_page.png)",
                "",
                "The runnable portfolio workflow flags OCR-required pages instead of installing or running a local OCR engine.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("Analytics report generated.")
    print(f"  documents: {summary['documents']}")
    print(f"  pages: {summary['pages']}")
    print(f"  direct-text pages: {direct_pages}")
    print(f"  OCR-required pages: {summary['ocr_required_pages']}")
    print(f"  review pages: {summary['review_pages']}")
    print(f"  report -> {report}")
    print(f"  figures -> {figures}")


if __name__ == "__main__":
    main()
