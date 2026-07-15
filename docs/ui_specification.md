# User Interface Specification

## Main Window

The main window should provide:

- A text input for a Windows folder path.
- A browse button that opens a folder picker.
- A scan mode selector:
  - Current folder only.
  - Include subdirectories recursively.
- A scan button.
- A summarize button.
- A stop/cancel button.
- A File Explorer-style table.
- A status bar.

## Table Columns

| Column | Description |
|---|---|
| File name | Base file name without folder path |
| Extension | File extension |
| Size | Human-readable file size |
| Created | Creation date and time |
| Modified | Last modification date and time |
| Owner | Windows file owner |
| Summary | LLM-generated summary |

## RTL Support

The application must support RTL layout for Hebrew users and Hebrew summaries. With PySide6 this should be applied at the application and window levels by setting `Qt.RightToLeft`. Table text alignment can be dynamic: Hebrew content should align right, while English-only content may align left.

## Responsiveness

Scanning and summarization must run outside the UI thread. Recommended implementation options are `QThreadPool`, `QRunnable`, and Qt signals for progress updates.
