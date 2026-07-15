from pathlib import Path

from file_system_analysis.config.settings import ScannerSettings
from file_system_analysis.infrastructure.document_readers.reader_factory import ReaderFactory
from file_system_analysis.infrastructure.filesystem.scanner import FileScanner


def test_scanner_finds_supported_files_non_recursive(tmp_path: Path):
    (tmp_path / "a.txt").write_text("hello", encoding="utf-8")
    (tmp_path / "b.exe").write_text("ignored", encoding="utf-8")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "c.md").write_text("nested", encoding="utf-8")

    records = FileScanner(ScannerSettings(supported_extensions=(".txt", ".md"))).scan(tmp_path, recursive=False)

    assert [record.file_name for record in records] == ["a.txt"]


def test_scanner_finds_supported_files_recursive(tmp_path: Path):
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "c.md").write_text("nested", encoding="utf-8")

    records = FileScanner(ScannerSettings(supported_extensions=(".md",))).scan(tmp_path, recursive=True)

    assert [record.file_name for record in records] == ["c.md"]


def test_text_reader_reads_utf8_text(tmp_path: Path):
    path = tmp_path / "notes.md"
    path.write_text("# Title\nContent", encoding="utf-8")

    reader = ReaderFactory().get_reader(path)

    assert reader.read(path).startswith("# Title")
