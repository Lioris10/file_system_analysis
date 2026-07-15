from file_system_analysis.config.settings import SummarizationSettings
from file_system_analysis.application.summarization_service import SummarizationService


def test_summary_is_capped_to_configured_length():
    service = SummarizationService(SummarizationSettings(output_max_chars=20))

    summary = service.summarize("First sentence. Second sentence. Third sentence.")

    assert len(summary) <= 20
    assert summary == "First sentence."


def test_summary_preserves_short_hebrew_text():
    service = SummarizationService(SummarizationSettings(output_max_chars=2000))

    summary = service.summarize("זהו מסמך בדיקה בעברית. הוא צריך להישאר בעברית.")

    assert "עברית" in summary
