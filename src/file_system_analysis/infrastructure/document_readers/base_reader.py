"""Document reader protocol."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol


class DocumentReader(Protocol):
    """Protocol implemented by all document readers."""

    supported_extensions: set[str]

    def read(self, path: Path) -> str:
        """Extract text from a document."""
