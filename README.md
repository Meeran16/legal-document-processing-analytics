# Legal Document Processing & Quality Analytics

A lightweight Python and SQLite pipeline for extracting, validating, structuring, and analysing text quality in regulatory PDF documents.

This repository is a portfolio reconstruction and analytics extension of the four-person Master's Research Lab project **Reconstruction of Text Hierarchy in Legal Texts** at the University of Koblenz.

The original university project included OCR, automatic structure annotation, TEI-Lite conversion, token labelling, and LayoutLMv3-based document structure recognition. This portfolio version keeps the runnable workflow intentionally lightweight and focuses on reproducible document-processing and data-quality analytics.

## What this project demonstrates

```text
Regulatory PDFs
      ↓
Embedded-text extraction
      ↓
Pages with insufficient text are flagged
as requiring OCR
      ↓
Page-level structured data
      ↓
Quality validation
      ↓
CSV + SQLite
      ↓
Python + SQL analytics
```

Core technologies:

- Python
- Pandas
- PyMuPDF
- SQLite
- SQL
- Matplotlib
- pytest

No GPU, CUDA, model download, or local Tesseract installation is required for the runnable portfolio workflow.

## Why the analytics extension matters

Document-processing systems depend heavily on input quality. Before applying downstream NLP or document-AI models, it is useful to know which pages contain usable embedded text, which pages need OCR, and which documents require additional review.

The pipeline records page-level fields including:

- document name;
- page number;
- extraction method;
- character count;
- word count;
- valid-word ratio;
- processing time;
- quality status;
- quality reason.

Pages with insufficient embedded text are recorded as:

```text
extraction_method = needs_ocr
quality_status = review
quality_reason = ocr_required
```

The portfolio pipeline does not run OCR itself.

## Repository structure

```text
legal-document-processing-analytics/
├── src/
│   └── legal_doc_analytics/
│       ├── extraction.py
│       ├── text_quality.py
│       ├── analytics.py
│       └── storage.py
├── scripts/
│   ├── run_pipeline.py
│   ├── generate_quality_report.py
│   └── validate_pipeline.py
├── sql/
│   ├── 01_schema.sql
│   └── 02_quality_analysis.sql
├── tests/
│   └── test_quality.py
├── data/
│   ├── raw/
│   └── processed/
├── reports/
│   └── figures/
└── docs/
    ├── architecture.md
    └── project_context.md
```

## Quick start

From the repository folder:

```powershell
pip install -r requirements.txt
pytest
```

Place one or more local PDF files in:

```text
data/raw/
```

Then run:

```powershell
python scripts/run_pipeline.py
python scripts/validate_pipeline.py
python scripts/generate_quality_report.py
```

Generated outputs are written locally to:

```text
data/processed/
├── page_metrics.csv
├── document_metrics.csv
├── quality_reason_summary.csv
├── summary.json
└── legal_document_quality.db
```

## Example validated run

A lightweight validation run was performed on one 43-page BIBB publication.

```text
Documents: 1
Pages: 43
Pages flagged as requiring OCR: 2
OCR-required rate: 4.7%
Review rate: 7.0%
SQLite rows: 43
Tests: 3 passed
```

These values describe only the current sample run. They are not presented as results from the historical Research Lab corpus.

The difference between the 4.7% OCR-required rate and the 7.0% review rate is expected: a page may fail another text-quality rule even if it contains enough embedded text to avoid the `needs_ocr` flag.

## SQL analysis

The generated SQLite database supports questions such as:

- Which documents contain the largest proportion of pages needing OCR?
- Which documents have the highest review rate?
- Which quality issues occur most often?
- Which pages contain unusually little usable text?
- How much processing time is required per page?

Example queries are provided in:

```text
sql/02_quality_analysis.sql
```

## Original Research Lab context

The original group project followed a broader document-AI workflow:

```text
PDF / OCR extraction
        ↓
automatic structure annotation
        ↓
Label Studio-compatible predictions
        ↓
TEI-Lite conversion
        ↓
token + bounding-box dataset
        ↓
LayoutLMv3 training
        ↓
evaluation
```

The preserved original implementation included scripts for OCR extraction, automatic annotation, TEI conversion, token labelling, Hugging Face dataset preparation, LayoutLMv3 training, and evaluation.

See `docs/project_context.md` for attribution and the relationship between the original university work and this portfolio reconstruction.

## Attribution

The original Master's Research Lab was completed collaboratively by:

- Karamchand Subash Kamaraj
- Meeran Mydeen Syed Ibrahim
- Ashwin Rajendran Appuraj
- Seshant Babu Kodamunja

Supervisor: Thomas Reiser, University of Koblenz.

Reference implementation:

`https://github.com/karamchandsubash/Reconstruction_of_Text_Hierarchy_in_Legal_Documents`

This repository is a portfolio reconstruction and analytics extension. It does not claim sole authorship of the original group project.

## Data and reproducibility

The original Research Lab corpus, historical model checkpoints, and experiment artifacts are not redistributed here.

Local PDFs and generated database/CSV outputs are excluded from Git by default. This keeps the repository lightweight and avoids publishing source material without first reviewing redistribution rights.

The original preserved OCR notebook contains output from a run over 272 PDFs, while the final Research Lab report describes 280 documents. This discrepancy is documented rather than silently converted into a portfolio claim.

## Scope

The runnable portfolio version intentionally prioritizes:

```text
document ingestion
+ data-quality checks
+ structured outputs
+ SQLite
+ SQL
+ Python analytics
+ validation
```

The heavier OCR and LayoutLMv3 components remain documented as part of the original Research Lab context rather than being required to run the portfolio project.
