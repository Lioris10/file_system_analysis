from pathlib import Path

from file_system_analysis.application.file_analysis_service import FileAnalysisService
from file_system_analysis.config.settings import AppSettings, ScannerSettings, SummarizationSettings


def test_file_analysis_service_scans_and_summarizes_text(tmp_path: Path):
    path = tmp_path / "report.txt"
    path.write_text("This is the first sentence. This is the second sentence.", encoding="utf-8")
    settings = AppSettings(
        scanner=ScannerSettings(supported_extensions=(".txt",)),
        summarization=SummarizationSettings(output_max_chars=2000),
    )

    records = FileAnalysisService(settings).analyze(tmp_path)

    assert len(records) == 1
    assert records[0].status == "summarized"
    assert "first sentence" in records[0].summary
