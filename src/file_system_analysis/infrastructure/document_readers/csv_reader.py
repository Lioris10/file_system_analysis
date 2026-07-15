"""CSV reader using the Python standard library."""

from __future__ import annotations

import csv
from pathlib import Path


class CsvReader:
    """Read CSV files into a compact text representation."""

    supported_extensions = {".csv"}

    def read(self, path: Path) -> str:
        rows: list[str] = []
        with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as csv_file:
            reader = csv.reader(csv_file)
            for index, row in enumerate(reader):
                if index >= 200:
                    rows.append("...")
                    break
                rows.append(" | ".join(cell.strip() for cell in row))
        return "\n".join(rows)
