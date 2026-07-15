# file_system_analysis Architecture Specification

## 1. Purpose

file_system_analysis is a Python 3.12+ Windows desktop application that scans a user-selected folder, displays file metadata in a File Explorer-style table, extracts text from supported documents, and creates a concise summary for each file by using an externally configured LLM through LangChain and LangGraph.

## 2. Technology Stack

| Area | Planned Technology |
|---|---|
| Language | Python 3.12+ |
| Desktop UI | PySide6 / Qt for Python |
| LLM abstraction | LangChain |
| Workflow orchestration | LangGraph |
| Configuration | YAML |
| Packaging | PyInstaller |
| Windows metadata | pywin32 |
| Tabular data | pandas, openpyxl, xlrd |
| PDF | pypdf or pdfplumber |
| Word DOCX | python-docx |
| PowerPoint PPTX | python-pptx |

## 3. Layered Design

### UI Layer

Located under `src/file_system_analysis/ui`.

Responsibilities:

- Render the main window.
- Accept a Windows folder path.
- Allow the user to choose recursive or non-recursive scanning.
- Display the file table.
- Support RTL layout.
- Show progress and per-file errors.

### Application Layer

Located under `src/file_system_analysis/application`.

Responsibilities:

- Coordinate UI events with scanning and summarization services.
- Manage background execution so the UI remains responsive.
- Convert workflow results into table updates.

### Domain Layer

Located under `src/file_system_analysis/domain`.

Responsibilities:

- Define `FileRecord`, processing statuses, exceptions, and value objects.
- Keep business entities independent from UI, LangChain, and filesystem implementation details.

### Infrastructure Layer

Located under `src/file_system_analysis/infrastructure`.

Responsibilities:

- Scan the local filesystem.
- Read Windows file owner metadata.
- Extract text from documents.
- Create provider-specific LangChain chat model instances from YAML configuration.

### LangGraph Layer

Located under `src/file_system_analysis/graph`.

Responsibilities:

- Define the workflow state.
- Define graph nodes for metadata reading, content extraction, chunking, summarization, and finalization.
- Route failures to explicit error nodes.

### Configuration Layer

Located under `src/file_system_analysis/config`.

Responsibilities:

- Load YAML configuration.
- Validate required settings.
- Provide typed settings objects to the rest of the application.

## 4. Provider-Neutral LLM Design

The application must never instantiate OpenAI, Gemini, Anthropic, Azure OpenAI, or local LLM clients directly in business logic. Instead, the `ModelFactory` reads the YAML configuration and creates a LangChain-compatible chat model.

The active provider is selected by:

```yaml
llm:
  provider: "openai"
  model_name: "gpt-4o-mini"
```

Changing the provider to Gemini or Anthropic should require only a YAML change and dependency availability, not code changes.

## 5. Runtime Flow

1. The user enters or selects a Windows folder path.
2. The user chooses whether scanning is recursive.
3. The scanner discovers files with supported extensions.
4. Metadata is read for every file.
5. The table is populated.
6. The user starts summarization.
7. Each file is processed by the LangGraph workflow.
8. Extracted text is summarized through the configured LangChain model.
9. The summary column is updated in the UI.

## 6. Project Directory Tree

```text
file_system_analysis/
├── README.md
├── pyproject.toml
├── config/
│   └── config.example.yaml
├── docs/
├── scripts/
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
```
