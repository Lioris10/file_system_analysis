"""Initial PySide6 desktop UI for file_system_analysis."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QStatusBar,
    QTableView,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from file_system_analysis.application.file_analysis_service import FileAnalysisService
from file_system_analysis.config.settings import AppSettings
from file_system_analysis.ui.file_table_model import FileTableModel


class MainWindow(QMainWindow):
    """File Explorer-style MVP window."""

    def __init__(self, settings: AppSettings) -> None:
        super().__init__()
        self.settings = settings
        self.service = FileAnalysisService(settings)
        self.table_model = FileTableModel()
        self.setWindowTitle("file_system_analysis")
        self.resize(1200, 700)
        self.setLayoutDirection(Qt.RightToLeft)
        self._build_toolbar()
        self._build_body()
        self._build_status_bar()

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Main")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        self.scan_action = toolbar.addAction("Scan")
        self.scan_action.triggered.connect(self.scan_folder)
        self.summarize_action = toolbar.addAction("Scan + Summarize")
        self.summarize_action.triggered.connect(self.scan_and_summarize)
        self.refresh_action = toolbar.addAction("Refresh")
        self.refresh_action.triggered.connect(self.scan_folder)

    def _build_body(self) -> None:
        container = QWidget(self)
        layout = QVBoxLayout(container)

        path_row = QHBoxLayout()
        path_row.addWidget(QLabel("Folder path:"))
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText(r"C:\Users\User\Documents")
        self.path_input.setLayoutDirection(Qt.LeftToRight)
        path_row.addWidget(self.path_input, stretch=1)
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_folder)
        path_row.addWidget(browse_button)
        layout.addLayout(path_row)

        options_row = QHBoxLayout()
        self.recursive_checkbox = QCheckBox("Include subdirectories")
        self.recursive_checkbox.setChecked(self.settings.scanner.recursive_default)
        options_row.addWidget(self.recursive_checkbox)
        options_row.addStretch(1)
        layout.addLayout(options_row)

        self.table = QTableView()
        self.table.setModel(self.table_model)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table, stretch=1)

        self.setCentralWidget(container)

    def _build_status_bar(self) -> None:
        status_bar = QStatusBar(self)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        status_bar.addPermanentWidget(self.progress_bar)
        self.setStatusBar(status_bar)
        self.statusBar().showMessage("Ready")

    def browse_folder(self) -> None:
        """Open a folder picker and place the selected path in the address field."""
        selected = QFileDialog.getExistingDirectory(self, "Select folder", self.path_input.text() or str(Path.home()))
        if selected:
            self.path_input.setText(selected)

    def scan_folder(self) -> None:
        """Scan metadata without reading/summarizing files."""
        self._run_analysis(summarize=False)

    def scan_and_summarize(self) -> None:
        """Scan files and create summaries."""
        self._run_analysis(summarize=True)

    def _run_analysis(self, summarize: bool) -> None:
        folder = self.path_input.text().strip()
        if not folder:
            QMessageBox.warning(self, "Missing folder", "Enter or browse to a folder path before scanning.")
            return
        self.statusBar().showMessage("Processing...")
        self.progress_bar.setRange(0, 0)
        QApplication.processEvents()
        try:
            records = self.service.analyze(folder, recursive=self.recursive_checkbox.isChecked(), summarize=summarize)
        except Exception as exc:
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(0)
            QMessageBox.critical(self, "Scan failed", str(exc))
            self.statusBar().showMessage("Scan failed")
            return
        self.table_model.set_records(records)
        self.table.resizeColumnsToContents()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)
        summarized = sum(1 for record in records if record.status == "summarized")
        failed = sum(1 for record in records if record.status == "failed")
        self.statusBar().showMessage(f"{len(records)} files | {summarized} summarized | {failed} failed")
