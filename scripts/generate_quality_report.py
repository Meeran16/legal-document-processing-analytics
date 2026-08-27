from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt
import pandas as pd

from legal_doc_analytics.analytics import summary_metrics, validate_page_metrics


def save_bar(series: pd.Series, title: str, xlabel: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.8))
    series.plot(kind="bar", ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Pages")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


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

    save_bar(
        df["extraction_method"].value_counts(),
        "Extraction method distribution",
        "Method",
        figures / "extraction_method_distribution.png",
    )
    save_bar(
        df["quality_status"].value_counts(),
        "Page quality status",
        "Status",
        figures / "quality_status_distribution.png",
    )
    save_bar(
        df["quality_reason"].value_counts().head(10),
        "Top page-quality outcomes",
        "Reason",
        figures / "quality_reason_distribution.png",
    )

    report = ROOT / "reports" / "quality_summary.md"
    report.write_text(
        "\n".join(
            [
                "# Document Quality Summary",
                "",
                f"- Documents: {summary['documents']}",
                f"- Pages: {summary['pages']}",
                f"- Pages flagged as needing OCR: {summary['ocr_required_pages']}",
                f"- OCR-required rate: {summary['ocr_required_rate']:.1%}",
                f"- Pages requiring review: {summary['review_pages']}",
                f"- Review rate: {summary['review_rate']:.1%}",
                f"- Average character count: {summary['average_character_count']}",
                f"- Average word count: {summary['average_word_count']}",
                f"- Average processing time per page: {summary['average_processing_seconds']} seconds",
                "",
                "This is the lightweight portfolio mode: OCR-required pages are flagged rather than processed with Tesseract.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"Quality report written to -> {report}")
    print(f"Figures written to -> {figures}")


if __name__ == "__main__":
    main()
