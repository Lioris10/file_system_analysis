"""Typed runtime settings loaded from YAML."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ScannerSettings:
    """Filesystem scanner configuration."""

    recursive_default: bool = False
    max_file_size_mb: int = 50
    supported_extensions: tuple[str, ...] = (
        ".txt",
        ".md",
        ".pdf",
        ".doc",
        ".docx",
        ".ppt",
        ".pptx",
        ".csv",
        ".xls",
        ".xlsx",
    )


@dataclass(frozen=True, slots=True)
class LlmSettings:
    """LLM provider configuration."""

    provider: str = "openai"
    model_name: str = "gpt-5.6-terra"
    api_key_env: str | None = "OPENAI_API_KEY"
    temperature: float = 0.2
    timeout_seconds: int = 60
    max_retries: int = 2
    providers: dict[str, dict] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class SummarizationSettings:
    """Summarization configuration."""

    output_max_chars: int = 2000
    preserve_source_language: bool = True
    chunk_size_chars: int = 12000
    chunk_overlap_chars: int = 500
    prompt_template: str = ""


@dataclass(frozen=True, slots=True)
class AppSettings:
    """Complete application settings needed by the MVP."""

    scanner: ScannerSettings = field(default_factory=ScannerSettings)
    llm: LlmSettings = field(default_factory=LlmSettings)
    summarization: SummarizationSettings = field(default_factory=SummarizationSettings)

    @classmethod
    def from_mapping(cls, data: dict) -> "AppSettings":
        """Build settings from a parsed YAML mapping."""
        scanner_data = data.get("scanner", {}) or {}
        llm_data = data.get("llm", {}) or {}
        summarization_data = data.get("summarization", {}) or {}

        scanner = ScannerSettings(
            recursive_default=bool(scanner_data.get("recursive_default", False)),
            max_file_size_mb=int(scanner_data.get("max_file_size_mb", 50)),
            supported_extensions=tuple(
                ext.lower() for ext in scanner_data.get("supported_extensions", ScannerSettings().supported_extensions)
            ),
        )
        llm = LlmSettings(
            provider=str(llm_data.get("provider", "openai")),
            model_name=str(llm_data.get("model_name", "gpt-5.6-terra")),
            api_key_env=llm_data.get("api_key_env"),
            temperature=float(llm_data.get("temperature", 0.2)),
            timeout_seconds=int(llm_data.get("timeout_seconds", 60)),
            max_retries=int(llm_data.get("max_retries", 2)),
            providers=dict(llm_data.get("providers", {}) or {}),
        )
        summarization = SummarizationSettings(
            output_max_chars=int(summarization_data.get("output_max_chars", 2000)),
            preserve_source_language=bool(summarization_data.get("preserve_source_language", True)),
            chunk_size_chars=int(summarization_data.get("chunk_size_chars", 12000)),
            chunk_overlap_chars=int(summarization_data.get("chunk_overlap_chars", 500)),
            prompt_template=str(summarization_data.get("prompt_template", "")),
        )
        return cls(scanner=scanner, llm=llm, summarization=summarization)
