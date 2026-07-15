# User Interface Design Specification

## 1. Design Goal

The desktop UI should feel familiar to Windows users by following the visual and interaction model of Windows File Explorer. The application is not a full file manager, but the primary file listing area should look and behave like File Explorer's Details view: a toolbar at the top, a path/address area, optional navigation pane, sortable columns, row selection, context actions, status bar, and clear progress feedback while scanning and summarizing files.

## 2. Target UI Technology

The planned implementation should use PySide6 / Qt for Python.

Recommended Qt widgets:

| UI Area | Recommended Widget |
|---|---|
| Main window | `QMainWindow` |
| Menus and toolbar | `QMenuBar`, `QToolBar` |
| Path/address bar | `QLineEdit` with `QPushButton` browse action |
| Recursive option | `QCheckBox` or two `QRadioButton` options |
| Main layout split | `QSplitter` |
| Optional navigation pane | `QTreeView` |
| File details table | `QTableView` with `QAbstractTableModel` |
| Status/progress | `QStatusBar`, `QProgressBar` |
| Long-running work | `QThreadPool`, `QRunnable`, Qt signals |

## 3. Window Layout

The main window should be arranged like File Explorer:

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Menu: File | View | Tools | Help                                             │
├──────────────────────────────────────────────────────────────────────────────┤
│ Toolbar: [Back] [Up] [Refresh] [Scan] [Summarize] [Stop] [Export]            │
├──────────────────────────────────────────────────────────────────────────────┤
│ Address: [ C:\Users\User\Documents                              ] [Browse]  │
│ Options: [ ] Include subdirectories   Filter: [ All supported files     v ]  │
├───────────────────────┬──────────────────────────────────────────────────────┤
│ Navigation Pane        │ Details Table                                       │
│ - Quick access         │ ┌────┬──────────────┬──────┬──────┬─────────────┐  │
│ - Desktop              │ │Icon│ File name    │Type  │Size  │Modified     │  │
│ - Documents            │ ├────┼──────────────┼──────┼──────┼─────────────┤  │
│ - This PC              │ │    │ report.pdf   │PDF   │2 MB  │2026-07-15   │  │
│ - Selected folder      │ └────┴──────────────┴──────┴──────┴─────────────┘  │
├───────────────────────┴──────────────────────────────────────────────────────┤
│ Status: 120 files | 90 summarized | 3 failed              [progress 75%]     │
└──────────────────────────────────────────────────────────────────────────────┘
```

The navigation pane may be implemented in a later phase, but the layout should reserve space for it so the application can evolve toward a full Explorer-like experience.

## 4. Main Toolbar

The toolbar should contain common File Explorer-style actions:

| Action | Behavior |
|---|---|
| Back | Navigate to the previous folder path in the session history. |
| Up | Navigate to the parent folder of the current path. |
| Refresh | Re-scan the current folder using the current recursive setting. |
| Scan | Discover supported files and load metadata into the table. |
| Summarize | Read supported file contents and generate summaries. |
| Stop | Cancel active scan or summarization tasks. |
| Export | Future action for exporting the table to CSV/XLSX. |

Toolbar buttons should use icons plus short text labels where space allows. Disabled actions should be visibly greyed out when not available.

## 5. Address and Options Area

The address area should include:

- A Windows path input field.
- A Browse button that opens `QFileDialog.getExistingDirectory`.
- A recursive scanning option.
- A file-type filter dropdown.
- Optional quick search field for filtering visible rows.

Recommended fields:

```text
Address: [ C:\Users\User\Documents ] [Browse]
Options: [ ] Include subdirectories    Type: [All supported files v]    Search: [______]
```

Validation behavior:

- If the path is empty, the Scan button should be disabled.
- If the path does not exist, show an inline validation message and keep the table unchanged.
- If the path exists but access is denied, show a recoverable error dialog and status-bar message.

## 6. File Explorer-Style Details Table

The central table is the most important UI element and should mimic File Explorer Details view.

### 6.1 Columns

| Column | Description | Recommended Alignment |
|---|---|---|
| Icon | File-type icon or processing status icon | Center |
| File name | Base file name without folder path | Right for RTL UI, left for LTR content |
| Extension | File extension such as `.pdf` or `.docx` | Center |
| Type | Human-readable type, for example PDF Document | Left or right by UI direction |
| Size | Human-readable size, for example `1.4 MB` | Right |
| Created | Creation date and time | Center |
| Modified | Last modification date and time | Center |
| Owner | Windows file owner | Left or right by UI direction |
| Status | Pending, Reading, Summarizing, Done, Failed | Center |
| Summary | LLM-generated summary in the source language | Dynamic by text language |
| Full path | Hidden by default; optional column | Left |

The original required columns are preserved: file name, extension, size, creation date/time, update date/time, owner, and summary. Additional Explorer-like columns such as icon, type, status, and full path are optional but recommended.

### 6.2 Table Interactions

The table should support:

- Single-row selection.
- Multi-row selection with Ctrl/Shift.
- Column sorting by clicking headers.
- Column resizing and reordering.
- Horizontal scrolling for long summaries.
- Tooltips for truncated file names, paths, errors, and summaries.
- Context menu on right click.
- Double-click row behavior to open a details/preview dialog rather than modifying the file.

### 6.3 Row Status Visuals

| Status | Suggested Indicator |
|---|---|
| Pending | Neutral grey icon/text |
| Reading | Blue spinner or blue status text |
| Summarizing | Purple or blue progress indicator |
| Done | Green check icon |
| Failed | Red warning icon and tooltip with error message |
| Skipped | Yellow/grey icon for unsupported or oversized files |

Failures must be per-file. One failed file must not stop the whole batch.

## 7. Context Menu

Right-clicking a row should open a File Explorer-style context menu:

```text
Open file
Open containing folder
Copy full path
Copy summary
Re-summarize selected file
Show details
Exclude from batch
```

Potential future actions:

```text
Export selected rows
Compare summaries
Add manual note
```

## 8. Details / Preview Panel

A preview area can be implemented as either:

1. A collapsible right-side details panel, or
2. A modal details dialog opened by double-clicking a row.

Recommended fields:

- File icon and name.
- Full path.
- Metadata fields.
- Extracted text preview, limited to a safe number of characters.
- Generated summary.
- Error details if processing failed.

The preview should not attempt to be a full PDF/Office renderer in the initial version. It should display extracted text and summary only.

## 9. Status Bar and Progress

The bottom status bar should show:

- Current folder path or last action.
- Number of discovered files.
- Number of files summarized.
- Number of failed/skipped files.
- Current operation label.
- Progress bar for scan/summarization batch.

Example:

```text
120 files | 82 summarized | 3 failed | Summarizing: report_2026.pdf      [██████░░░░] 68%
```

## 10. RTL and Hebrew Support

The UI must support RTL layout.

PySide6 implementation guidance:

```python
app.setLayoutDirection(Qt.RightToLeft)
main_window.setLayoutDirection(Qt.RightToLeft)
```

Recommended behavior:

- Hebrew UI labels should align naturally to the right.
- Hebrew summaries should align right.
- English-only summaries may align left even when the overall UI is RTL.
- Numeric values, sizes, and dates should remain readable and can be center/right aligned.
- File paths should generally remain left-to-right because Windows paths are LTR strings.

## 11. Accessibility and Usability

The UI should support:

- Keyboard navigation in the table.
- Tab order from path input to Browse, recursive option, Scan, Summarize, and table.
- High-contrast-friendly status colors plus icons, not color alone.
- Resizable columns and persistent user layout preferences.
- Clear error messages that do not expose API keys or full document content.

## 12. Empty, Loading, and Error States

### Empty State

Before scanning:

```text
Choose a folder path and click Scan to display supported files.
```

### Loading State

During scanning:

```text
Scanning folder... 38 files found
```

During summarization:

```text
Summarizing 12 of 120: report.pdf
```

### Error State

For invalid path:

```text
The selected folder does not exist or cannot be accessed.
```

For LLM failure:

```text
Summary generation failed for this file. See row tooltip for details.
```

## 13. Suggested Implementation Classes

| Class | Responsibility |
|---|---|
| `MainWindow` | Owns the main UI shell, toolbar, address bar, table, and status bar. |
| `PathSelectorWidget` | Encapsulates path input, browse button, and validation display. |
| `ScanOptionsWidget` | Encapsulates recursive checkbox and file-type filter. |
| `FileTableModel` | Qt table model backed by `FileRecord` objects. |
| `FileTableView` | QTableView configuration, context menu, sorting, and selection behavior. |
| `StatusBarWidget` | Displays counts, operation text, and progress. |
| `FileDetailsDialog` | Shows metadata, extracted text preview, summary, and errors. |
| `AppController` | Connects UI signals to scanning and summarization services. |

## 14. MVP UI Scope

The first implementation should include:

- Main window.
- Path input and Browse button.
- Recursive checkbox.
- Scan button.
- Summarize button.
- Stop button.
- Explorer-like details table.
- Status bar with progress.
- RTL support.
- Per-file status and error indication.

The navigation pane, export action, and details preview panel can be added after the core scan/summarize flow works reliably.
