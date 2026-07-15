"""Command-line entry point for the file_system_analysis MVP."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from file_system_analysis.application.file_analysis_service import FileAnalysisService
from file_system_analysis.config.yaml_loader import DEFAULT_CONFIG_PATH, load_settings


def build_parser() -> argparse.ArgumentParser:
    """Create the MVP command-line parser."""
    parser = argparse.ArgumentParser(description="Scan a folder and summarize supported files.")
    parser.add_argument("path", type=Path, help="Folder path to scan")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH, help="Path to YAML configuration")
    parser.add_argument("--recursive", action="store_true", help="Scan subdirectories recursively")
    parser.add_argument("--no-summary", action="store_true", help="Only scan metadata without reading/summarizing files")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    return parser


def main() -> None:
    """Run the MVP scan/summarize pipeline and print JSON records."""
    args = build_parser().parse_args()
    settings = load_settings(args.config)
    service = FileAnalysisService(settings)
    records = service.analyze(args.path, recursive=args.recursive, summarize=not args.no_summary)
    indent = 2 if args.pretty else None
    print(json.dumps([record.to_dict() for record in records], ensure_ascii=False, indent=indent))


if __name__ == "__main__":
    main()
