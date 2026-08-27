# Project Context and Attribution

## Original university project

This repository is a **portfolio reconstruction and analytics extension** of the Master's Research Lab project:

**Reconstruction of Text Hierarchy in Legal Texts**

The original work was completed as a four-person Research Lab project at the University of Koblenz.

Original team:

- Karamchand Subash Kamaraj
- Meeran Mydeen Syed Ibrahim
- Ashwin Rajendran Appuraj
- Seshant Babu Kodamunja

Supervisor: Thomas Reiser.

The original group implementation included PDF/OCR extraction, heuristic document annotation, Label Studio-compatible outputs, TEI conversion, token labelling, Hugging Face dataset preparation, LayoutLMv3 training, and evaluation.

Reference implementation:

`https://github.com/karamchandsubash/Reconstruction_of_Text_Hierarchy_in_Legal_Documents`

## Why this repository is separate

The original group repository was created for the university project rather than as a polished portfolio project. It also contains machine-specific paths and does not package the historical datasets, model checkpoints, or all intermediate experiment outputs needed for complete reproduction.

This repository therefore does **not** claim to be the untouched original submission.

Instead, it:

1. reconstructs the document-ingestion and data-quality workflow in portable Python;
2. adds page-level quality metrics and SQLite analytics;
3. separates local data from source code;
4. adds validation and tests;
5. documents which parts are historical project context and which parts are portfolio extensions.

## Historical evidence

The preserved OCR notebook in the original repository contains output from a batch run over **272 PDF files**. The final Research Lab report describes a dataset of **280 documents**.

Because those two preserved sources differ, this portfolio repository does not present either number as a newly reproduced pipeline result. Current metrics are generated from whichever local corpus is actually processed.

## Results policy

A metric is described as a reproducible result in this repository only when it can be regenerated from available code and data.

Historical report values may be discussed as project context, but they should not be relabelled as newly reproduced results unless the original experiment artifacts are available.
