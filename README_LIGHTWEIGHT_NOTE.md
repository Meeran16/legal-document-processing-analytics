# Lightweight portfolio mode

This portfolio reconstruction intentionally avoids heavy local dependencies.

It does **not** require:

- Tesseract installation
- LayoutLMv3 model downloads
- CUDA
- GPU training
- the original large Research Lab corpus

The original university project included OCR and LayoutLMv3; that history remains documented.

The runnable portfolio version uses:

```text
PDF
↓
embedded text extraction
↓
flag pages that would need OCR
↓
page-level quality metrics
↓
CSV + SQLite
↓
Python / SQL analysis
```

A low-text page is recorded as:

```text
extraction_method = needs_ocr
quality_status = review
quality_reason = ocr_required
```

This keeps the project small, fast, and interview-defensible.
