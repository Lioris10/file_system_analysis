"""Domain models for file discovery and summarization."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class FileRecord:
    """Metadata and processing result for one discovered file."""

    path: Path
    file_name: str
    extension: str
    size_bytes: int
    created_at: datetime
    modified_at: datetime
    owner: str | None
    summary: str | None = None
    status: str = "pending"
    error_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation of the record."""
        data = asdict(self)
        data["path"] = str(self.path)
        data["created_at"] = self.created_at.isoformat(timespec="seconds")
        data["modified_at"] = self.modified_at.isoformat(timespec="seconds")
        return data
