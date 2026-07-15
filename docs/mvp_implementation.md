# MVP Implementation Notes

## Scope Implemented

The current MVP implements a non-UI backend and CLI that can:

1. Load runtime settings from YAML.
2. Scan a folder for supported file extensions.
3. Read file metadata including size, timestamps, and best-effort owner.
4. Extract content from TXT, MD, and CSV files without optional third-party readers.
5. Provide optional reader hooks for PDF, DOCX, PPTX, XLS, and XLSX when their dependencies are installed.
6. Mark legacy DOC and PPT files as failed until a conversion backend is added.
7. Generate a deterministic extractive summary capped by the configured `summarization.output_max_chars` value.
8. Print JSON records that contain the table fields required by the future desktop UI.

## CLI Usage

If PyYAML is not installed and the default config path is used, the MVP falls back to built-in defaults so local scans can still run. A custom YAML path requires PyYAML.


Run a non-recursive scan with summaries:

```powershell
poetry run file_system_analysis C:\Users\User\Documents --pretty
```

Run a recursive scan:

```powershell
poetry run file_system_analysis C:\Users\User\Documents --recursive --pretty
```

Only collect metadata without reading file contents:

```powershell
poetry run file_system_analysis C:\Users\User\Documents --no-summary --pretty
```

Use a custom YAML file:

```powershell
poetry run file_system_analysis C:\Users\User\Documents --config C:\config\file_system_analysis.yaml --pretty
```

## LangChain Integration Point

The MVP includes `ModelFactory` under `src/file_system_analysis/infrastructure/llm/model_factory.py`. It creates LangChain chat models from YAML provider blocks using lazy imports. The deterministic summarizer is intentionally kept as a fallback so local scanning and tests can run without API keys or network access.

The next implementation step is to add a LangGraph node that calls a LangChain model produced by `ModelFactory` when the user enables live LLM summarization.

## Current Reader Behavior

| Extension | MVP Behavior |
|---|---|
| `.txt` | Implemented with encoding fallback. |
| `.md` | Implemented with encoding fallback. |
| `.csv` | Implemented with the Python standard library. |
| `.pdf` | Implemented when `pypdf` is installed. |
| `.docx` | Implemented when `python-docx` is installed. |
| `.pptx` | Implemented when `python-pptx` is installed. |
| `.xls`, `.xlsx` | Implemented when `pandas` plus spreadsheet engines are installed. |
| `.doc`, `.ppt` | Reported as failed until Word/PowerPoint or LibreOffice conversion support is added. |


## Initial Desktop UI

The MVP now includes a first PySide6 desktop UI under `src/file_system_analysis/ui`. The UI can be launched with:

```powershell
poetry run file_system_analysis --gui
```

If no folder path is supplied to the entry point, the application also attempts to launch the GUI. The UI provides a File Explorer-style starting point with a toolbar, folder path field, Browse button, recursive scanning option, details table, progress bar, and status bar. The current implementation runs the backend pipeline synchronously and should later be moved to `QThreadPool`/worker signals as described in the UI specification.
