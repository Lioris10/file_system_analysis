"""Plain text and Markdown readers."""

from __future__ import annotations

from pathlib import Path


class TextReader:
    """Read UTF text-like files with fallback encodings."""

    supported_extensions = {".txt", ".md"}

    def read(self, path: Path) -> str:
        for encoding in ("utf-8", "utf-8-sig", "cp1255", "cp1252", "latin-1"):
            try:
                return path.read_text(encoding=encoding)
            except UnicodeDecodeError:
                continue
        return path.read_text(errors="replace")
