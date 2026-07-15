"""Entry points for the file_system_analysis MVP."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

from file_system_analysis.application.file_analysis_service import FileAnalysisService
from file_system_analysis.config.yaml_loader import DEFAULT_CONFIG_PATH, load_settings


def build_parser() -> argparse.ArgumentParser:
    """Create the MVP command-line parser."""
    parser = argparse.ArgumentParser(description="Scan a folder and summarize supported files.")
    parser.add_argument("path", type=Path, nargs="?", help="Folder path to scan. If omitted, the GUI is launched.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH, help="Path to YAML configuration")
    parser.add_argument("--recursive", action="store_true", help="Scan subdirectories recursively")
    parser.add_argument("--no-summary", action="store_true", help="Only scan metadata without reading/summarizing files")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    parser.add_argument("--gui", action="store_true", help="Launch the PySide6 desktop UI")
    return parser


def main() -> None:
    """Run either the desktop GUI or CLI scan/summarize pipeline."""
    args = build_parser().parse_args()
    settings = load_settings(args.config)
    if args.gui or args.path is None:
        _run_gui_or_exit(settings)
        return

    service = FileAnalysisService(settings)
    records = service.analyze(args.path, recursive=args.recursive, summarize=not args.no_summary)
    indent = 2 if args.pretty else None
    print(json.dumps([record.to_dict() for record in records], ensure_ascii=False, indent=indent))


def _run_gui_or_exit(settings) -> None:
    if importlib.util.find_spec("PySide6") is None:
        raise SystemExit("PySide6 is required to launch the GUI. Install project dependencies with Poetry first.")
    from file_system_analysis.ui.app import run_gui

    raise SystemExit(run_gui(settings))


if __name__ == "__main__":
    main()
