# Architecture

## Lightweight portfolio workflow

```text
Local regulatory PDFs
        |
        v
PyMuPDF embedded-text extraction
        |
        +-----------------------------+
        | enough embedded text?       |
        |                             |
      yes                             no
        |                             |
        v                             v
direct_text                       needs_ocr
        |                             |
        +-------------+---------------+
                      |
                      v
              page-level metrics
                      |
            +---------+----------+
            |                    |
            v                    v
          CSV                SQLite
            |                    |
            +---------+----------+
                      |
                      v
              quality analytics
                      |
          +-----------+-----------+
          |                       |
          v                       v
   Python reporting          SQL analysis
```

## Design choice

The original Research Lab included Tesseract OCR and LayoutLMv3. The portfolio reconstruction deliberately does not require those heavier dependencies.

Pages that would require OCR are flagged rather than processed locally. This keeps the project easy to run while preserving the core data-quality problem.

## Historical document-AI workflow

```text
PDF / OCR
    ↓
automatic annotation
    ↓
TEI-Lite
    ↓
token + bounding-box dataset
    ↓
LayoutLMv3
    ↓
evaluation
```

That historical workflow is documented separately from the lightweight runnable analytics layer.
