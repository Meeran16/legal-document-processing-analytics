CREATE TABLE page_metrics (
    document TEXT NOT NULL,
    page_number INTEGER NOT NULL,
    extraction_method TEXT NOT NULL,
    text TEXT,
    character_count INTEGER NOT NULL,
    word_count INTEGER NOT NULL,
    valid_word_ratio REAL NOT NULL,
    ocr_mean_confidence REAL,
    processing_seconds REAL NOT NULL,
    quality_status TEXT NOT NULL,
    quality_reason TEXT NOT NULL
);

CREATE TABLE document_metrics (
    document TEXT PRIMARY KEY,
    pages INTEGER NOT NULL,
    ocr_required_pages INTEGER NOT NULL,
    review_pages INTEGER NOT NULL,
    average_character_count REAL NOT NULL,
    average_word_count REAL NOT NULL,
    average_processing_seconds REAL NOT NULL,
    ocr_required_rate REAL NOT NULL,
    review_rate REAL NOT NULL
);
