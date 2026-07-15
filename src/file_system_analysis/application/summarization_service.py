"""Summarization service used by the MVP pipeline."""

from __future__ import annotations

import re

from file_system_analysis.config.settings import SummarizationSettings


class SummarizationService:
    """Create a concise summary.

    The MVP includes a deterministic extractive fallback so the scan/summarize flow works
    without network credentials. A later implementation can replace this method with a
    LangChain model call while preserving the same public interface.
    """

    def __init__(self, settings: SummarizationSettings) -> None:
        self.settings = settings

    def summarize(self, text: str) -> str:
        """Return a compact summary capped by the configured character length."""
        cleaned = _normalize_whitespace(text)
        if not cleaned:
            return ""
        max_chars = max(1, self.settings.output_max_chars)
        if len(cleaned) <= max_chars:
            return cleaned

        sentences = _split_sentences(cleaned)
        summary_parts: list[str] = []
        current_length = 0
        for sentence in sentences:
            addition = len(sentence) + (1 if summary_parts else 0)
            if current_length + addition > max_chars:
                break
            summary_parts.append(sentence)
            current_length += addition
        summary = " ".join(summary_parts).strip()
        if not summary:
            summary = cleaned[:max_chars].rstrip()
        return summary


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _split_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?。؟])\s+", text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]
