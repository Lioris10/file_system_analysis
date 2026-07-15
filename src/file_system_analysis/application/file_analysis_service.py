"""Application service that scans files and creates summaries."""

from __future__ import annotations

from pathlib import Path

from file_system_analysis.config.settings import AppSettings
from file_system_analysis.domain.exceptions import FileReadError
from file_system_analysis.domain.models import FileRecord
from file_system_analysis.infrastructure.document_readers.reader_factory import ReaderFactory
from file_system_analysis.infrastructure.filesystem.scanner import FileScanner
from file_system_analysis.application.summarization_service import SummarizationService


class FileAnalysisService:
    """Coordinate scanner, readers, and summarizer for the MVP."""

    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings
        self.scanner = FileScanner(settings.scanner)
        self.reader_factory = ReaderFactory()
        self.summarizer = SummarizationService(settings.summarization)

    def analyze(self, folder: Path | str, recursive: bool | None = None, summarize: bool = True) -> list[FileRecord]:
        """Scan a folder and optionally summarize discovered files."""
        records = self.scanner.scan(folder, recursive=recursive)
        if not summarize:
            return records

        for record in records:
            if record.status == "skipped":
                continue
            try:
                record.status = "reading"
                reader = self.reader_factory.get_reader(record.path)
                content = reader.read(record.path)
                record.status = "summarizing"
                record.summary = self.summarizer.summarize(content)
                record.status = "summarized"
            except FileReadError as exc:
                record.status = "failed"
                record.error_message = str(exc)
            except Exception as exc:  # defensive per-file failure isolation
                record.status = "failed"
                record.error_message = f"Unexpected processing error: {exc}"
        return records
