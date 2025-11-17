# 🧾 Changelog — *NewtUtils (NewtCode)*

All notable changes to this project are documented here.  
This project follows [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`).

---

## 🏷️ v1.0.0 — First Stable Release

**Date:** 2025-11-17

### 🎉 Major Release

This is the first stable release of NewtUtils, marking the library as production-ready with a stable API.

### ✨ Completed

- All core modules are complete and fully tested:
  - `console.py` — console messaging, error reporting, type validation, and notification helpers.
  - `utility.py` — list and dict sorting utilities with strict input validation.
  - `files.py` — text, JSON, and CSV helpers with newline normalization and directory auto-creation.
  - `sql.py` — SQLite helpers for queries, row operations, and CSV export.
  - `network.py` — HTTP helpers with retries, configurable modes, and default headers.

- Updated all core modules to:
  - Include `from __future__ import annotations` for modern typing.
  - Provide comprehensive type hints for arguments and return values.
  - Normalize newline handling for cross-platform behavior.
  - Use centralized input validation via `newtutils.console.validate_input()`.

### ✨ Added

- New public API exports in `newtutils.__init__`:
  - Re-exported `validate_input` from `console` at the top-level.
  - Exposed `choose_file_from_folder` from `files` for interactive file selection.

- `console.py`:
  - `validate_input()` — centralized type-checking with consistent error reporting.
  - `_beep_boop()` — optional Windows-only notification sound for errors/retries.
  - `_retry_pause()` — countdown helper for retryable operations with optional sound.

- `files.py`:
  - `choose_file_from_folder()` — interactive file selection in a directory with validation and error handling.

- `network.py`:
  - `DEFAULT_HTTP_HEADERS` — shared default headers for all outbound HTTP requests.
  - Extended `fetch_data_from_url()`:
    - New `mode` options: `"auto"`, `"alert"`, `"manual"` for retry behavior.
    - Unified validation using `console.validate_input()`.
  - Extended `download_file_from_url()`:
    - Uses shared default headers.
    - Improved retry logic and clearer error reporting.

- `sql.py`:
  - Improved `export_sql_query_to_csv()` to validate SQL results and report empty or invalid output more clearly before writing CSV.

### 🛠️ Improved

- `CONTRIBUTING.md`:
  - Clarified requirement to use `from __future__ import annotations` in all modules.
  - Made type hints mandatory for all public functions.

- `INSTALL.md`:
  - Fixed indentation in example snippet for temporary usage so it matches project style.

- `README.md`:
  - Added badges:
    - License badge for MIT.
    - Python version badge (3.10+).
  - Expanded overview to state that all functions include full type hints and Google-style docstrings.
  - Split **Requirements** and **Dependencies**:
    - Requirements now state support and testing for Python 3.10-3.13 and the use of `from __future__ import annotations`.

- `LICENSE`:
  - Expanded the list of standard library modules used, grouped by purpose (core language, runtime, data processing, collections, testing, platform-specific, database).
  - Converted PSF and SQLite license references to explicit URL links.
  - Added explicit mention of `pytest` (MIT) in third-party dependencies.
  - Normalized punctuation (for example, date ranges) in third-party copyright lines.

- `files.py`:
  - Stronger input validation for paths, data structures, and delimiters.
  - Improved docstrings with explicit return semantics and normalized naming for `out`.
  - CSV writing now normalizes newlines in all cell data before saving.
  - JSON reading now guarantees a `list` or `dict` result and returns `[]` on invalid structures.

- `network.py`:
  - Refactored header handling to always start from `DEFAULT_HTTP_HEADERS` and then merge custom headers.
  - Unified error messages with clearer timing information and retry context.
  - Moved retry helpers (`_beep_boop`, `_retry_pause`) from `utility` into `console` for better responsibility separation.

- `utility.py`:
  - Removed low-level console and retry helpers (moved logic into `console`).
  - Re-focused module on pure utility logic, with `sorting_list()` and `sorting_dict_by_keys()` using `console.validate_input()` for validation.
  - Updated types to use `collections.abc` (`Sequence`, `Mapping`) where appropriate.

- `sql.py`:
  - Improved error messages when exporting to CSV (explicitly handling empty or invalid results).
  - Normalized error handling and validation before CSV generation.

- `TODO`:
  - Removed outdated internal tasks and added new item to track future GW2-related helper functions.

### 📚 Documentation

- Updated all affected modules docstrings to:
  - Use Google-style structure consistently.
  - Clarify parameter and return types, including aliases like `out`.
  - Document new helper functions and constants.

- Documentation and metadata:
  - Updated `README.md`, `INSTALL.md`, `LICENSE`, and `CONTRIBUTING.md` to reflect:
    - New type hint policy.
    - Supported Python versions.
    - Updated dependency and licensing information.

### 🧪 Testing

- Ensured that new and refactored functions integrate with existing test structure.
- Expanded coverage for:
  - File handling (newline normalization, invalid paths, invalid JSON/CSV).
  - Network utilities (retry behavior and header merging logic).
  - Input validation via `console.validate_input()`.

### 🛠️ Code Quality

- Strengthened input validation across all modules with centralized helpers.
- Improved separation of concerns:
  - Console and retry helpers live in `console.py`.
  - `utility.py` focuses on list/dict utilities only.
- Normalized docstrings and header comments across modules, including unified `Updated on` metadata.

### 📦 Stability

- API is now stable and ready for production use.
- All newly added public symbols are exported through `newtutils.__init__` for a consistent import surface.
- No breaking changes planned for the `1.x` series; behavior is fully backward compatible with `0.1.6`.

---

## 🏷️ v0.1.6 — Network Utilities

**Date:** 2025-10-26

### ✨ Added

- New module: `network.py` — external HTTP and file-download utilities:
  - `fetch_data_from_url()`
  - `download_file_from_url()`
- Added sound notification support (`NewtUtil._beep_boop()`).
- Introduced interactive and automatic retry modes for unstable APIs.

### 🧩 Dependencies

- Added `requests` (Apache 2.0 License) for HTTP communication.

### 🪪 License

- Expanded license documentation to include:
  - Python StdLib modules (`time`, `winsound`, `sqlite3`).
  - Requests (Apache 2.0).
  - Clarified SQLite Public Domain status.

---

## 🏷️ v0.1.5 — SQL Utilities

**Date:** 2025-10-24

### ✨ Added

- New module: `sql.py` — helper functions for SQLite operations:
  - `sql_execute_query()`
  - `sql_select_rows()`
  - `sql_insert_row()`
  - `sql_update_rows()`
  - `export_sql_query_to_csv()`
- New tests for `sql.py` ensuring stable query execution and CSV export.
- Added `tests/sql_output.txt` for consistent test output validation.

### 🛠️ Improved

- Added `_check_file_exists()` in `files.py` for safe file validation.
- Updated `__init__.py` to re-export SQL functions.

---

## 🏷️ v0.1.4 — Files utilities

**Date**: 2025-10-21

### ✨ Added

- New module: `files.py` — read/write helpers for text, JSON, and CSV files.

### 🛠️ Improved

- Added complete Google-style docstrings for all file functions.
- Unified metadata across project files (`__init__.py`, `pyproject.toml`).
- Updated documentation (`INSTALL.md`, `README.md`, `LICENSE`).

---

## 🏷️ v0.1.3 — Sorting utilities

**Date:** 2025-10-20

### ✨ Added

- Added `sorting_dict_by_keys()` — sort lists of dictionaries by one or more keys.
  - Handles missing keys safely.
  - Supports ascending and descending order.

### 🛠️ Improved

- Documentation updates and metadata cleanup.
- Organized project files for clarity and consistency.

---

## 🏷️ v0.1.2 — Validation and list sorting

**Date:** 2025-10-18

### ✨ Added

- Introduced `newtutils.utility` module.
- Added `sorting_list()` — removes duplicates and sorts strings before integers.
- Added `validate_input()` — validates input types with safe error feedback.

---

## 🏷️ v0.1.1 — Console utilities

**Date:** 2025-10-17

### ✨ Added

- Start of the *NewtUtils* module.
- Added `newtutils.console` with `error_msg()` for unified error output.
  - Uses **Colorama** for cross-platform colored messages.
- Added base configuration (`pyproject.toml`, module layout).

---

## 🏷️ v0.1.0 — Initial setup

**Date:** 2025-10-16

### 🧩 Initial Setup

- Created project structure (`.gitignore`, `.gitattributes`).
- Initialized the *NewtUtils* repository.
- Prepared the foundation for future modules and documentation.

> 🪄 *The very first commit of the NewtUtils project.*
