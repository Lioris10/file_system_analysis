"""Document reader factory."""

from __future__ import annotations

from pathlib import Path

from file_system_analysis.domain.exceptions import FileReadError
from file_system_analysis.infrastructure.document_readers.csv_reader import CsvReader
from file_system_analysis.infrastructure.document_readers.office_readers import (
    DocxReader,
    PdfReader,
    PowerPointReader,
    SpreadsheetReader,
    UnsupportedLegacyOfficeReader,
)
from file_system_analysis.infrastructure.document_readers.text_reader import TextReader


class ReaderFactory:
    """Select a reader by file extension."""

    def __init__(self) -> None:
        self._readers = [
            TextReader(),
            CsvReader(),
            PdfReader(),
            DocxReader(),
            PowerPointReader(),
            SpreadsheetReader(),
            UnsupportedLegacyOfficeReader(),
        ]

    def get_reader(self, path: Path):
        """Return a reader for the file path."""
        extension = path.suffix.lower()
        for reader in self._readers:
            if extension in reader.supported_extensions:
                return reader
        raise FileReadError(f"Unsupported file extension: {extension}")
