"""Directory scanner for supported files."""

from __future__ import annotations

from pathlib import Path

from file_system_analysis.config.settings import ScannerSettings
from file_system_analysis.domain.models import FileRecord
from file_system_analysis.infrastructure.filesystem.metadata_reader import read_file_metadata


class FileScanner:
    """Scan a directory for supported files and collect metadata."""

    def __init__(self, settings: ScannerSettings) -> None:
        self.settings = settings
        self.supported_extensions = {ext.lower() for ext in settings.supported_extensions}
        self.max_file_size_bytes = settings.max_file_size_mb * 1024 * 1024

    def scan(self, folder: Path | str, recursive: bool | None = None) -> list[FileRecord]:
        """Scan a folder and return metadata records for supported files."""
        root = Path(folder).expanduser().resolve()
        if not root.exists():
            raise FileNotFoundError(f"Folder does not exist: {root}")
        if not root.is_dir():
            raise NotADirectoryError(f"Path is not a folder: {root}")

        use_recursive = self.settings.recursive_default if recursive is None else recursive
        paths = root.rglob("*") if use_recursive else root.iterdir()
        records: list[FileRecord] = []
        for path in sorted(paths, key=lambda item: str(item).lower()):
            if not path.is_file() or path.suffix.lower() not in self.supported_extensions:
                continue
            record = read_file_metadata(path)
            if record.size_bytes > self.max_file_size_bytes:
                record.status = "skipped"
                record.error_message = f"File exceeds {self.settings.max_file_size_mb} MB limit"
            records.append(record)
        return records
