# 🧾 Changelog — *NewtUtils (NewtCode)*

All notable changes to this project are documented here.  
This project follows [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`).

---

## 🏷️ v1.1.1 — Input Handling Enhancements

**Date:** 2026-02-12

### ✨ Added

- NewtUtil `utility.py`:
  - New function `count_similar_values()`

### 🛠️ Improved

- NewtUtil `utility.py`:
  - Moved `select_from_input()` from `console.py`

- NewtFiles `files.py`:
  - Update `choose_file_from_folder()` to use `select_from_input()` for better input handling and validation.

---

## 🏷️ v1.1.0 — February Update

**Date:** 2026-02-10

### ✨ Added

- NewtCons `console.py`:
  - New function `check_location()`
  - New function `select_from_input()`

- NewtUtil `utility.py`:
  - New function `check_dict_keys()`

- NewtFiles `files.py`:
  - Maded `ensure_dir_exists()` public
  - Maded `check_file_exists()` public
  - New function `setup_logging()`
  - New function `cleanup_logging()`

### 🛠️ Improved

- NewtCons `console.py`:
  - Added `check_non_empty` parameter to `validate_input()` for validating non-empty values.
  - Changed `beep` parameter default from `False` to `True` in `_retry_pause()`.
  - Refactored exception handling with `# pragma: no cover` markers for Windows-only code.

- NewtUtil `utility.py`:
  - Enhanced type annotations with `Sequence` instead of concrete `list`, and `Any` for complex types.
  - Function `sorting_dict_by_keys()`:
    - Added `stop` parameter for consistent error handling behavior.
    - Improved empty key handling with special case for single-key dictionaries.

- NewtFiles `files.py`:
  - Function `check_file_exists()`:
    - Renamed `print_error` parameter to `logging` for consistency.
    - Changed `stop` parameter default from `False` to `True`.
  - Function `choose_file_from_folder()`:
    - Enhanced with max attempt limit (5),
    - improved menu format,
    - and `None` return removed, it is script stop now.
  - Functions `read_text_from_file()` `read_json_from_file()` `read_csv_from_file()`:
    - Added `stop` parameter.
    - Changed to return `None` instead of empty string on error.
  - Function `save_text_to_file()`:
    - Changed `append` parameter default from `False` to `True`

- NewtSQL `sql.py`:
  - Function `db_delayed_close()`:
    - Added `logging` parameter for controlling output messages.
  - Function `sql_execute_query()`:
    - Extended dangerous SQL token detection with new patterns: `exec`, `execute`, `grant`, `revoke`, `union`, `--`, `sp_`, `char(`, `concat(`, `0x`.
    - Added specialized error handling for `sqlite3.OperationalError` to distinguish between syntax errors and database errors.

- NewtNet `network.py`:
  - Function `fetch_data_from_url()`:
    - Improved HTTP status code comments with sections for successful (200-299), client error (400-499), and server error (500-599) responses.
  - Function `download_file_from_url()`:
    - Enhanced file size formatting with increased precision.

### 📚 Documentation

- Updated all module docstrings to unified Google-style format with improved parameter descriptions and return type documentation.
- Fixed error location reporting to use consistent, more readable format across all files (e.g., `"function : context"` instead of `"function.parameter"`).
- Reformatted multi-line function calls for improved readability and consistency throughout all modules.
- Strengthened input validation documentation with `check_non_empty` parameter usage guidance.

### 🧪 Testing

- Extracted test helper functions into dedicated `tests/helpers.py` module:
  - `print_my_func_name()` — automatically displays the name of the calling test function using frame inspection.
  - `print_my_captured()` — formats and displays pytest captured output (stdout/stderr) for easier debugging.
- Added support for new functions.

---

## 🏷️ v1.0.3 — Enhanced File I/O and Network Utilities

**Date:** 2026-01-30

### ✨ Added

- `files.py`:
  - Added `logging` parameter to all file I/O functions (`read_text_from_file`, `save_text_to_file`, `read_json_from_file`, `save_json_to_file`, `read_csv_from_file`, `save_csv_to_file`) to control debug output.
    - When `logging=True` (default), functions print confirmation messages with file paths and operation details.
    - Set `logging=False` to suppress output for silent operations.
  - Added `append` parameter to `save_csv_to_file()` for appending rows to existing CSV files.
    - When `append=True`, new rows are added to the end of the file instead of overwriting.
  - Enhanced `_check_file_exists()` with new parameters:
    - `stop` parameter — controls whether execution stops on error (defaults to `False`).
    - `print_error` parameter — controls error message output (defaults to `True`).

- `network.py`:
  - Enhanced `download_file_from_url()` with file size checking:
    - Checks file size before download using HEAD request.
    - Verifies if file already exists and compares sizes to avoid redundant downloads.
    - Automatically skips download if file exists with matching size.
  - Improved retry logic:
    - Timeout increases by 30 seconds on each retry attempt.
    - Better error handling with separate exception types for network and general errors.

### 🛠️ Improved

- `files.py`:
  - Fixed row count calculation in `save_csv_to_file()` logging output.
  - Improved debug output formatting for all file operations with consistent message structure.
  - Enhanced error handling in `_check_file_exists()` with configurable behavior.

- `network.py`:
  - Separated status code and response time into distinct print statements for better readability.
  - Improved timeout handling with separate connect and read timeouts.
  - Added `response.raise_for_status()` for better HTTP error detection.

---

## 🏷️ v1.0.2 — JSON String Parsing Utility

**Date:** 2025-11-19

### ✨ Added

- `files.py`:
  - `convert_str_to_json()` — parse a string into a JSON-compatible Python object.
    - Tries `json.loads` first, falls back to attempts single-quote to double-quote substitution before retrying `json.loads`.
    - Returns `list | dict` on success, otherwise `None`.

- `newtutils.__init__`:
  - Exported `convert_str_to_json` from `files` module for public API access.

### 🧪 Testing

- `tests/test_files.py`:
  - Added comprehensive test suite for `convert_str_to_json()` function:
    - `TestConvertStrToJson` class with 10 test cases covering:
      - Valid JSON parsing (dict and list formats)
      - Single-quote to double-quote conversion
      - Empty string and whitespace handling
      - Invalid input validation
      - Invalid JSON error handling
      - Non-list/dict JSON type filtering
      - Nested structure parsing

---

## 🏷️ v1.0.1 — Project Configuration Fix

**Date:** 2025-11-17

### 🛠️ Fixed

- `pyproject.toml`:
  - Reorganized `[project.optional-dependencies]` section to appear after `classifiers` for improved logical structure.
  - Ensures consistent formatting and readability of project metadata.

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
