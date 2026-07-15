# file_system_analysis

file_system_analysis is a planned Windows desktop application for analyzing files in a local folder, extracting supported document content, and generating concise LLM summaries through a provider-neutral LangChain integration orchestrated by LangGraph.

## Core Requirements

- Runtime: Python 3.12 or newer.
- Operating system target: Windows PC.
- UI: desktop interface with RTL support for Hebrew content and labels.
- User input: local folder path.
- Scan mode: current directory only or recursive scanning of subdirectories.
- File table columns:
  - File name
  - Extension
  - Size
  - Created date and time
  - Last modified date and time
  - File owner
  - Summary
- Supported readable file formats:
  - TXT
  - MD
  - PDF
  - DOC
  - DOCX
  - PPT
  - PPTX
  - CSV
  - XLS
  - XLSX
- Summaries must be written in the source language of the file content.
- Default summary length is externally configured as 2,000 characters.
- LLM provider, model, credentials, and generation options must be configured only through YAML.

## Documentation

- [Architecture specification](docs/architecture.md)
- [Configuration specification](docs/configuration.md)
- [YAML configuration guide](docs/yaml_configuration_guide.md)
- [Model version review](docs/model_version_review.md)
- [Dependency compatibility plan](docs/dependency_compatibility.md)
- [User interface specification](docs/ui_specification.md)
- [LangGraph workflow specification](docs/langgraph_workflow.md)
- [Supported file readers](docs/supported_file_readers.md)

## Project Structure

```text
file_system_analysis/
├── config/
│   └── config.example.yaml
├── docs/
│   ├── architecture.md
│   ├── configuration.md
│   ├── langgraph_workflow.md
│   ├── supported_file_readers.md
│   └── ui_specification.md
├── scripts/
│   ├── build_exe.ps1
│   └── run_app.ps1
├── src/
│   └── file_system_analysis/
│       ├── application/
│       ├── config/
│       ├── domain/
│       ├── graph/
│       ├── infrastructure/
│       │   ├── document_readers/
│       │   ├── filesystem/
│       │   └── llm/
│       ├── ui/
│       └── utils/
└── tests/
    ├── integration/
    └── unit/
```

## Configuration-Driven LLM Selection

The application must not hard-code an LLM provider or model. The YAML file selects the provider and model, for example OpenAI, Google Gemini, Anthropic, Azure OpenAI, or a local provider supported through LangChain.

See `config/config.example.yaml` for examples.
