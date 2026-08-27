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

Core technologies: **Python · Pandas · PyMuPDF · SQLite · SQL · Matplotlib · pytest**

No GPU, CUDA, model download, or local Tesseract installation is required for the runnable portfolio workflow.

## Sample analytics

A validated sample run was performed on one 43-page BIBB publication.

| Metric | Result |
| --- | ---: |
| Documents | 1 |
| Pages | 43 |
| Direct-text pages | 41 |
| Pages flagged as needing OCR | 2 |
| OCR-required rate | 4.7% |
| Pages requiring review | 3 |
| Review rate | 7.0% |
| Automated tests | 3 passed |

The sample demonstrates a simple data-quality question: **which pages can be used directly and which should be routed for additional processing or review?**

![Extraction method distribution](reports/figures/extraction_method_distribution.png)

![Page quality status](reports/figures/quality_status_distribution.png)

![Extracted text volume by page](reports/figures/text_volume_by_page.png)

The complete generated snapshot, including the lowest-text pages, is available in [`reports/quality_summary.md`](reports/quality_summary.md).

These values describe only the portfolio sample run. They are not presented as results from the historical Research Lab corpus.

## Data-quality fields

The pipeline records page-level fields including:

- document and page number;
- extraction method;
- character and word counts;
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

The portfolio pipeline flags these pages but does not run OCR itself.

## Repository structure

```text
legal-document-processing-analytics/
├── src/legal_doc_analytics/
│   ├── extraction.py
│   ├── text_quality.py
│   ├── analytics.py
│   └── storage.py
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
├── reports/
│   ├── quality_summary.md
│   └── figures/
└── docs/
```

## Quick start

```powershell
pip install -r requirements.txt
pytest
```

Place one or more PDFs in:

```text
data/raw/
```

Then run:

```powershell
python scripts/run_pipeline.py
python scripts/validate_pipeline.py
python scripts/generate_quality_report.py
```

Generated CSV and SQLite files stay local under `data/processed/`. Only the small portfolio figures and summary are committed.

## SQL analysis

The generated SQLite database supports questions such as:

- Which documents contain the largest share of pages needing OCR?
- Which documents have the highest review rate?
- Which quality issues occur most often?
- Which pages contain unusually little usable text?

Example queries are provided in `sql/02_quality_analysis.sql`.

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

The preserved original implementation included OCR extraction, automatic annotation, TEI conversion, token labelling, Hugging Face dataset preparation, LayoutLMv3 training, and evaluation.

See `docs/project_context.md` for the relationship between the original university work and this portfolio reconstruction.

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

Local PDFs and generated database/CSV outputs are excluded from Git. This keeps the repository lightweight and avoids publishing source material without first reviewing redistribution rights.

The preserved original OCR notebook contains output from a run over 272 PDFs, while the final Research Lab report describes 280 documents. This discrepancy is documented rather than converted into a portfolio claim.
