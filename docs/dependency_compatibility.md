# Dependency Compatibility Plan

## Python Runtime Decision

The project targets Python 3.12 or newer. For practical dependency resolution, the initial Poetry constraint is:

```toml
requires-python = ">=3.12,<3.14"
```

This allows Python 3.12 and Python 3.13 while avoiding accidental installation on a future Python release before the UI, document-processing, and LLM provider packages have confirmed wheel support for that release.

## Poetry Build Files

The project uses `pyproject.toml` as the source of truth for package metadata, runtime dependencies, development dependencies, console entry points, and build-system configuration.

The stale lock file from the previous placeholder project should not be reused because the project name, Python version, and dependencies changed significantly. A fresh lock file should be generated in the target development environment with:

```powershell
poetry lock
poetry install
```

## Compatibility Groups

| Area | Dependency Constraint | Reason |
|---|---|---|
| Desktop UI | `PySide6>=6.7,<7.0` | Qt 6 desktop UI with RTL support and Python 3.12+ support. |
| Configuration | `PyYAML>=6.0.2,<7.0` | Stable YAML parsing API. |
| LangChain Core | `langchain>=0.2,<0.4` | Keeps the implementation within the modern LangChain package family while avoiding unreviewed major API changes. |
| Workflow | `langgraph>=0.2,<0.4` | Aligns with the LangChain orchestration approach planned for per-file workflows. |
| OpenAI Provider | `langchain-openai>=0.1,<0.4` | Enables OpenAI and Azure OpenAI chat models through LangChain. |
| Gemini Provider | `langchain-google-genai>=1.0,<3.0` | Enables Google Gemini chat models through LangChain. |
| Anthropic Provider | `langchain-anthropic>=0.1,<0.4` | Enables Anthropic Claude chat models through LangChain. |
| Local Provider | `langchain-ollama>=0.1,<0.4` | Enables local Ollama models through LangChain. |
| PDF | `pypdf>=4.0,<6.0` | Text extraction from PDF files. |
| Word | `python-docx>=1.1,<2.0` | Text extraction from DOCX files. |
| PowerPoint | `python-pptx>=0.6.23,<2.0` | Text extraction from PPTX files. |
| Spreadsheets | `pandas>=2.2,<3.0`, `openpyxl>=3.1,<4.0`, `xlrd>=2.0.1,<3.0` | CSV, XLSX, and XLS reading. |
| Encoding | `charset-normalizer>=3.3,<4.0` | Text encoding detection for TXT and MD files. |
| Windows Metadata | `pywin32>=306,<400; sys_platform == 'win32'` | Windows file owner and security metadata. |

## Provider Switching Rule

Application code must depend on LangChain interfaces and a YAML-driven model factory. Switching from OpenAI to Gemini, Anthropic, Azure OpenAI, or Ollama must require only configuration changes and installed dependencies.
