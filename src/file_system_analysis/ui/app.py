"""PySide6 application bootstrap."""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from file_system_analysis.config.settings import AppSettings
from file_system_analysis.ui.main_window import MainWindow


def run_gui(settings: AppSettings) -> int:
    """Run the desktop GUI and return the Qt exit code."""
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.RightToLeft)
    window = MainWindow(settings)
    window.show()
    return app.exec()
