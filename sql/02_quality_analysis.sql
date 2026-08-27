-- Documents with the largest share of pages that would need OCR.
SELECT
    document,
    pages,
    ocr_required_pages,
    ROUND(100.0 * ocr_required_rate, 1) AS ocr_required_pct
FROM document_metrics
ORDER BY ocr_required_rate DESC, pages DESC;

-- Documents with the highest review rate.
SELECT
    document,
    pages,
    review_pages,
    ROUND(100.0 * review_rate, 1) AS review_pct
FROM document_metrics
ORDER BY review_rate DESC, review_pages DESC;

-- Most common page-quality outcomes.
SELECT
    quality_reason,
    COUNT(*) AS pages,
    ROUND(
        100.0 * COUNT(*) / (SELECT COUNT(*) FROM page_metrics),
        1
    ) AS pct_pages
FROM page_metrics
GROUP BY quality_reason
ORDER BY pages DESC;

-- Pages flagged as needing OCR.
SELECT
    document,
    page_number,
    character_count,
    word_count,
    quality_status,
    quality_reason
FROM page_metrics
WHERE extraction_method = 'needs_ocr'
ORDER BY character_count ASC, document, page_number;
