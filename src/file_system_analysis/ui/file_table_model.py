"""Qt table model for File Explorer-style file records."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from file_system_analysis.domain.models import FileRecord


class FileTableModel(QAbstractTableModel):
    """Expose `FileRecord` values to a `QTableView`."""

    COLUMNS = (
        "File name",
        "Extension",
        "Size",
        "Created",
        "Modified",
        "Owner",
        "Status",
        "Summary",
    )

    def __init__(self, records: list[FileRecord] | None = None) -> None:
        super().__init__()
        self._records = records or []

    def rowCount(self, parent: QModelIndex | None = None) -> int:  # noqa: N802 - Qt API
        return 0 if parent and parent.isValid() else len(self._records)

    def columnCount(self, parent: QModelIndex | None = None) -> int:  # noqa: N802 - Qt API
        return 0 if parent and parent.isValid() else len(self.COLUMNS)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid() or not 0 <= index.row() < len(self._records):
            return None
        record = self._records[index.row()]
        if role in (Qt.DisplayRole, Qt.ToolTipRole):
            return self._value_for_column(record, index.column())
        if role == Qt.TextAlignmentRole:
            if index.column() in {1, 2, 3, 4, 6}:
                return Qt.AlignCenter
            if index.column() == 7:
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:  # noqa: N802
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.COLUMNS[section]
        return None

    def set_records(self, records: list[FileRecord]) -> None:
        """Replace all table records."""
        self.beginResetModel()
        self._records = records
        self.endResetModel()

    def record_at(self, row: int) -> FileRecord | None:
        """Return the record at the requested row."""
        if 0 <= row < len(self._records):
            return self._records[row]
        return None

    def _value_for_column(self, record: FileRecord, column: int) -> str:
        values = (
            record.file_name,
            record.extension,
            _format_size(record.size_bytes),
            record.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            record.modified_at.strftime("%Y-%m-%d %H:%M:%S"),
            record.owner or "",
            record.status,
            record.summary or record.error_message or "",
        )
        return values[column]


def _format_size(size_bytes: int) -> str:
    units = ("B", "KB", "MB", "GB", "TB")
    size = float(size_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} {unit}"
        size /= 1024
    return f"{size_bytes} B"
