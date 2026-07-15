# Supported File Readers

## Supported Extensions

| Extension | Reader Strategy |
|---|---|
| `.txt` | Plain text reader with encoding detection |
| `.md` | Plain text / Markdown reader |
| `.pdf` | pypdf or pdfplumber |
| `.docx` | python-docx |
| `.doc` | Microsoft Word COM or LibreOffice headless conversion |
| `.pptx` | python-pptx |
| `.ppt` | PowerPoint COM or LibreOffice headless conversion |
| `.csv` | pandas or csv module |
| `.xlsx` | pandas with openpyxl |
| `.xls` | pandas with xlrd |

## Reader Factory

The document reader factory should select a reader based on file extension. Unsupported extensions should be excluded during scanning or marked as unsupported before summarization.

## Large Files

Large documents should be chunked before summarization. Chunk size and overlap are configured through YAML.
