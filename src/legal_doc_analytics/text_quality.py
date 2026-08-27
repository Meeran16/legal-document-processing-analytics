from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿÄÖÜäöüß0-9]+", re.UNICODE)


@dataclass(frozen=True)
class QualityThresholds:
    min_characters: int = 50
    min_words: int = 5
    min_valid_word_ratio: float = 0.60


def tokenize_words(text: str) -> list[str]:
    return WORD_RE.findall(text or "")


def valid_word_ratio(words: Iterable[str]) -> float:
    words = list(words)
    if not words:
        return 0.0
    valid = [
        word
        for word in words
        if any(ch.isalpha() for ch in word) and len(word) >= 2
    ]
    return len(valid) / len(words)


def quality_status(
    text: str,
    thresholds: QualityThresholds | None = None,
) -> tuple[str, str]:
    thresholds = thresholds or QualityThresholds()
    words = tokenize_words(text)
    ratio = valid_word_ratio(words)

    if len(text or "") < thresholds.min_characters:
        return "review", "low_character_count"
    if len(words) < thresholds.min_words:
        return "review", "low_word_count"
    if ratio < thresholds.min_valid_word_ratio:
        return "review", "low_valid_word_ratio"

    return "pass", "quality_checks_passed"
