# Changelog — *NewtUtils (NewtCode)*

All notable changes to this project are documented here.  
This project follows [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`).

---

## [vNext] — Upcoming

### Added

- *(add new features here)*

### Changed

- refactor(utility): rename sorting_list to sorting_sequence

### Testing

- New helper function format_set_to_str(input_set: set) -> str in tests/helpers.py — sorts elements by string representation and returns them wrapped in curly braces (e.g. {1, 2, abc})

### Fixed

- fix(console): support tuple of types in validate_type emptiness checks

### Removed

- chore(tests): remove outdated pytest output snapshots from tests/output

---

## [0.3.1] — Reworked Module Console

**Date:** 2026-04-30

### Added

- Added **pytest-cov** to dependencies and license.

### Changed

- `newtutils/__init__.py` - Updated public export `validate_input` to `validate_type`.
- `newtutils/console.py`:
  - `error_msg()` - Redirected output to stderr.
  - `error_msg()` - Argument `*args` has been changed to string.
  - Renamed `validate_input()` to `validate_type()` for more accurate naming that reflects its purpose (type checking, not input validation).
  - `validate_type()` - Reversed the order of `location` prefix: changed from `" > " + location` to `location + " > "` so the caller's location appears before the function location.
  - `validate_type()` - Rewrote `check_non_empty` logic: replaced loosely typed `isinstance()` checks with strict `type(value) is T and expected_type is T` comparisons for each type. Extended support to `bool`, `float`, and `bytes` types.
  - `_beep_boop()` - No longer accepts a `pause_s` parameter, delay between tones is now hardcoded (0.2s after first beep, 1s after second to have time to react).
  - `_beep_boop()` - Cross-platform fallback changed: instead of silently returning on non-Windows, now prints a colored `"Beep Boop !!!"` message to stdout using **colorama**, to see a message at least.
  - `_retry_pause()` - Rewrite error hints. Beep happens after message of Retrying, to have extra 1s to react.
  - `check_location()` - Renamed parameter `dir_` to `dir_global` and all internal usages.

### Testing

- `tests/_list.sh` - Added multi-venv **pytest** runner loop.
- `tests/output/` - Added **pytest** results for console module across venv310-venv314 and venvLinux312.
- `tests/test_console.py` - Added `assert "::: ERROR :::" not in captured.out` checks to multiple tests for stricter stdout/stderr separation.
- `tests/test_console.py` - Renamed test class `TestValidateInput` to `TestValidateType`.
- `tests/test_console.py` - `TestValidateType`: expanded coverage to all core types (`NoneType`, `bool`, `int`, `float`, `str`, `bytes`, `list`, `tuple`, `dict`, `set`).
- `tests/test_console.py` - Rewritten `test_beep_boop` to be platform-aware: on Windows it patches winsound.Beep directly and asserts call counts; on non-Windows it verifies "Beep Boop !!!" message appears in stdout.
- `tests/test_console.py` - Updated all error location string assertions to use the new naming conventions.

### Fixed

- `README.md` - Fixed badge formatting by removing stray leading plus sign.
- `newtutils/console.py` - Updated docstrings.
- Updated all usages of `validate_input()` to `validate_type()` across other modules.
- `newtutils/console.py` - `validate_type()` - Now renders `set` values using a custom sorted string format ({val1, val2, ...}), ensures consistent, deterministic output across all Python versions.
- `tests/README.md` - Updated test usage documentation.
- `tests/helpers.py` - Updated docstrings and signatures.

---

## [0.3.0] — Reworked CHANGELOG and Migrated build backend

**Date:** 2026-04-27

### Changed

- `CHANGELOG.md` - Completly rewrote history from broad version-based entries to granular per feature releases following `[0.x.x]` semantic version. Removed emoji decorators from headings and section labels. Edit tages and releases numbers.
- `README.md` - Updated badge to v0.3.0. Updated links and added Development Workflow section.
- `CONTRIBUTING.md` - Updated contribution guidelines to include a contributor checklist and PR rules. Removed emoji formatting.
- `newtutils/__init__.py` - Updated timestamp, set __version__ to 0.3.0, and shorten package description.
- `pyproject.toml` - Changed package name to "NewtUtils", set version to 0.3.0, and adjust the project description.
- `pyproject.toml` - Migrated build backend from `setuptools` to `hatchling`.

---

## [0.2.19] — Merged download_file_from_url into fetch_data_from_url

**Date:** 2026-02-22

### Added

- `newtutils/files.py` - Function `choose_file_from_folder()` now accepts `missing_values` as argument and passes it to `utility.select_from_input`.

### Changed

- `newtutils/files.py` - Function `convert_str_to_json()` error messages now include text size for both standard and single-quote-replace parse attempts.
- `newtutils/network.py` - Function `fetch_data_from_url()` now accepts `save_path` parameter to optionally save the response to a local file.
- `newtutils/network.py` - Function `fetch_data_from_url()` now accepts `max_mb_size` parameter to limit file download size (default: 2 MB).
- `newtutils/network.py` - Function `fetch_data_from_url()` now accepts `logging` parameter to control response time output.

### Fixed

- `newtutils/network.py` - Streamed binary downloads using chunked `iter_content` (1 MB chunks) instead of loading full content into memory.

---

## [0.2.18] — Function count_similar_values in Utility

**Date:** 2026-02-11

### Added

- `newtutils/utility.py` - Added `count_similar_values()` function to count occurrences of values at a specified position in a sequence of tuples.
- `newtutils/__init__.py` - Exported `count_similar_values` and included it in `__all__` for direct package-level imports.

### Testing

- Moved `select_from_input()` test coverage out of `tests/test_console.py` into `tests/test_utility.py`.

---

## [0.2.17] — Moved Function select_from_input from Console to Utility

**Date:** 2026-02-11

### Added

- Added Python 3.14 support in project metadata.

### Changed

- Moved `select_from_input()` from `newtutils.console` to `newtutils.utility`.
- `newtutils/files.py` - Updated file selection logic in `choose_file_from_folder()` to reuse `utility.select_from_input()`.

### Testing

- Refreshed stored test output logs for all modules.

### Fixed

- `newtutils/files.py` - Updated `read_text_from_file()`, `read_json_from_file()`, and `read_csv_from_file()` to return `None` on default.

---

## [0.2.16] — Testing helpers in Network

**Date:** 2026-02-10

### Changed

- `newtutils/network.py` - Improved input validation in functions by requiring non-empty string inputs, disabling hard stops, and updating validation location labels for clearer error output.
- Refined network error reporting by using more specific location messages for HTTP errors, timeouts, request exceptions, and generic exceptions.

### Testing

- `tests/test_network.py` - Refactored to use shared helper utilities instead of old local `print_my_func_name` and `print_my_captured` functions.
- Expanded network tests to assert full printed output, including full URLs, response times, result values, request kwargs, precise file sizes, and detailed error locations.
- Refreshed stored pytest output snapshots for files and network tests to match the new formatting, plugin list, error locations, separator lines, result lines, and rounded file-size values.

---

## [0.2.15] — Testing helpers in SQL

**Date:** 2026-02-09

### Changed

- `newtutils/console.py` - Improved error location messages in `validate_input()` by appending the caller location to `check_non_empty` validation errors.
- `newtutils/sql.py` - Updated functions for handling SQL queries and added more comprehensive error handling.

### Testing

- `tests/test_sql.py` - Refactored to use shared helper utilities instead of old local `print_my_func_name` and `print_my_captured` functions.

---

## [0.2.14] — Argument check_non_empty in Function validate_input

**Date:** 2026-02-09

### Added

- `newtutils/console.py` - Added a new `check_non_empty` argument to the `validate_input()` function to also validate that the value is not empty.

### Changed

- Updated Modules to use `check_non_empty=True` in `validate_input()` function, ensuring that empty inputs are rejected.
- `newtutils/files.py` - Changed `convert_str_to_json()` to return `None` for invalid or empty input instead of relying on earlier exit behavior.
- `newtutils/files.py` - Changed `check_file_exists()` to return `False` immediately when validation fails.

### Testing

- Updated test fixtures and expected output files to match the new error messages and return values.

### Fixed

- `newtutils/files.py` - Fixed `save_json_to_file()` to report negative indentation as an error.

---

## [0.2.13] — Reorder Function check_dict_keys in Utility

**Date:** 2026-02-08

### Changed

- `newtutils/utility.py` - Moved `check_dict_keys()` to the top, placing it before the sorting helpers and matching the module's function list in the docstring.
- `newtutils/__init__.py` - Reordered `check_dict_keys` in `newtutils.__init__.py` so the utility imports and exported names now follow the same sequence as the function definitions.

---

## [0.2.12] — Reworked Functions in SQL

**Date:** 2026-02-08

### Changed

- `newtutils/sql.py` - Updated several validation and error `location` strings to use a more specific `function : context` format for easier tracing.

### Fixed

- `newtutils/sql.py` - Clarified `db_delayed_close()` documentation to explain that it triggers garbage collection to help release SQLite file handles, rather than guaranteeing a safe immediate close.

### Removed

- `newtutils/sql.py` - Removed several early `return` branches that depended directly on `NewtCons.validate_input(..., stop=False)`.

---

## [0.2.11] — Testing helpers in Files

**Date:** 2026-02-07

### Changed

- `newtutils/utility.py` - Expanded `sorting_list()` to accept sequences of strings and integers, not just lists, and updated validation to allow both lists and tuples.
- `newtutils/utility.py` - Expanded `sorting_dict_by_keys()` to accept sequence inputs and more general mapping types, with updated type hints and docstrings.
- `newtutils/utility.py` - Updated `check_dict_keys()` documentation to refer to mappings instead of only dictionaries, and removed embedded usage examples from some docstrings.

### Testing

- `tests/test_files.py` - Refactored to use shared helper utilities instead of old local `print_my_func_name` and `print_my_captured` functions.
- Updated existing tests to match new APIs and behaviors, especially `logging` parameter naming, `None`-on-failure returns, revised validation locations, and combined output formatting. Rewrote docstrings to be more descriptive and behavior-focused.
- Marked generic exception branches in console and utility helpers as `pragma: no cover` and updated their error text to include a testing note.

### Fixed

- `newtutils/files.py` - Corrected CSV save logging so the reported row count matches the actual number of written rows.

---

## [0.2.10] — Reworked Functions in Files

**Date:** 2026-02-03

### Changed

- Standardized many validation and error location strings across `newtutils/console.py`, `newtutils/files.py`, and `newtutils/utility.py` for clearer diagnostics.
- `newtutils/files.py` - Renamed public function `normalize_newlines` to underscore‑prefixed private name `_normalize_newlines` to indicate that this is intended for internal use only and not part of the public API.
- `newtutils/files.py` - Changed `check_file_exists()` default behavior to `stop=True` to indicate that it should stop on first error.
- `newtutils/files.py` - Changed `save_text_to_file()` default behavior to `append=True` to indicate that it should append to file instead of overwriting existing content.
- `newtutils/files.py` - Changed `save_text_to_file()` default behavior to `append=True` to indicate that it should append to file instead of overwriting existing content.
- `newtutils/files.py` - Revised CLI flow of `choose_file_from_folder()` to use `X` for cancel.
- `newtutils/utility.py` - Added a default argument `stop=True` to `sorting_dict_by_keys()` to stops execution when invalid data is detected.

### Testing

- Renamed stored test output snapshots for all modules from the old `tests/test_<module>_<n>.txt` to the new `tests/output/test_<module>_<n>.txt` location.

### Removed

- `newtutils/__init__.py` - Removed renamed function `_normalize_newlines` from `__all__` since this is now intended for internal use only and not part of the public API.

---

## [0.2.9] — Function check_dict_keys in Utility

**Date:** 2026-02-03

### Added

- `newtutils/utility.py` - Added `check_dict_keys()` function to check if a dictionary has all required keys.
- `newtutils/__init__.py` - Exported `check_dict_keys` and included it in `__all__` for direct package-level imports.

### Testing

- `tests/test_utility.py` - Added tests for `check_dict_keys()` function.

---

## [0.2.8] — Testing helpers in Utility

**Date:** 2026-02-03

### Testing

- `tests/test_console.py` - Expanded with stricter assertions for expected output and explicit checks that unwanted output is absent.
- `tests/test_utility.py` - Refactore to import shared helper functions instead of defining local print helpers.

### Fixed

- `newtutils/utility.py` - Refined `sorting_dict_by_keys()` so empty input returns an empty list immediately before further validation, preventing unnecessary processing and potential errors with empty data.
- `newtutils/utility.py` - Adjusted `sorting_dict_by_keys()` to return a copy of the original list when no sorting keys are provided, with this behavior handled earlier in the function flow.

---

## [0.2.7] — Function select_from_input in Console

**Date:** 2026-02-02

### Added

- `newtutils/console.py` - Added `select_from_input()` function to allow users to select from a list of options via console input.
  - The selection flow supports canceling with `x` or `X`, and it handles `KeyboardInterrupt` and other exceptions with error output.
- `newtutils/__init__.py` - Exported `select_from_input` and included it in `__all__` for direct package-level imports.

### Testing

- `tests/test_console.py` - Added tests for `select_from_input()` including valid selection, invalid input recovery, cancel behavior, whitespace handling, type validation, `KeyboardInterrupt`, and generic exceptions.

---

## [0.2.6] — Testing helper functions

**Date:** 2026-02-02

### Changed

- Renamed public functions from clean public names to underscore‑prefixed private names to indicate they are intended for internal use only and not part of the public API:
  - in `newtutils/console.py`:
    - `_divider` => `divider`
    - `_beep_boop` => `beep_boop`
    - `_retry_pause` => `retry_pause`

### Testing

- `tests/helpers.py` - Created file with `print_my_func_name` (using `inspect.currentframe`) and `print_my_captured` helpers to reuse across tests.
- `newtutils\console.py` - Reworked tests to use the new `print_my_func_name` and `print_my_captured` helpers for cleaner output and easier debugging.

### Removed

- `newtutils/__init__.py` - Removed renamed functions from `__all__` since they are now intended for internal use only and not part of the public API.

---

## [0.2.5] — Functions setup_logging and cleanup_logging in Files

**Date:** 2026-01-30

### Added

- `newtutils/files.py` - Added `setup_logging()` and `cleanup_logging()` functions for managing log file creation and cleanup.
- `newtutils/__init__.py` - Exported `setup_logging` and `cleanup_logging` and included them in `__all__` for direct package-level imports.

---

## [0.2.4] — Function check_location in Console

**Date:** 2026-01-30

### Added

- `newtutils/console.py` - Added `check_location()` function to validate the current directory.
- `newtutils/__init__.py` - Exported `check_location` and included it in `__all__` for direct package-level imports.

---

## [0.2.3] — Renamed some internal functions to public names

**Date:** 2026-01-30

### Changed

- Renamed internal functions from underscore‑prefixed private names to clean public names:
  - in `newtutils/console.py`:
    - `_divider` => `divider`
    - `_beep_boop` => `beep_boop`
    - `_retry_pause` => `retry_pause`
  - in `newtutils/files.py`:
    - `_ensure_dir_exists` => `ensure_dir_exists`
    - `_check_file_exists` => `check_file_exists`
    - `_normalize_newlines` => `normalize_newlines`
- `newtutils/__init__.py` - Updated `__all__` to reflect the renamed functions.
- Updated all internal calls across other modules to use the new function names.

---

## [0.2.2] — Enhanced logging features in Files and Network modules

**Date:** 2026-01-30

### Changed

- `newtutils/files.py` - Added `logging` parameter to all file I/O functions for debug output control.
  - When `logging=True` (default), functions print confirmation messages with file paths and operation details.
  - Set `logging=False` to suppress output for silent operations.
- `newtutils/files.py` - Added `append` parameter to `save_csv_to_file()` for appending rows to existing CSV files.
  - When `append=False` (default), the file is overwritten or new.
  - Set `append=True` to preserve existing data and add new rows without losing previous content.
- `newtutils/files.py` - Enhanced `_check_file_exists()` with new parameters `stop` and `print_error` for error handling.
- `newtutils/network.py` - Enhanced `download_file_from_url()` with file size checking using HEAD requests, improved retry logic with timeout backoff, and better error handling.
  - `stop` (default `False`) controls whether execution stops on error.
  - `print_error` (default `True`) controls whether error messages are printed.
- `COPYRIGHT` - Updated copyright year range.
- `LICENSE` - Updated copyright years.

### Testing

- `tests/test_files.py` - Extended tests for file I/O operations with various scenarios and edge cases.
- `tests/test_network.py` - Extended tests for `download_file_from_url` with more mocks and scenarios, including file size checks, existence checks, and various response types.
- `INSTALL.md` - Added `pytest` to dependencies and installation instructions, including editable mode in virtual environments.
- `README.md` - Added `pytest` to dependencies.

### Fixed

- `newtutils/files.py` - Updated `_normalize_newlines()` to strip trailing newlines in addition to normalizing line endings.

---

## [0.2.1] — Function convert_str_to_json in Files

**Date:** 2025-11-19

### Added

- `newtutils/files.py` - Added `convert_str_to_json()` function for parsing JSON-like strings.
- `newtutils/__init__.py` - Added `convert_str_to_json()` to the public API.

### Changed

- `LICENSE` - Updated Python standard library module descriptions and regrouped them for better organization.
- `AUTHORS` - Updated author email.

### Testing

- `tests/test_files.py` - Added comprehensive test suite for `convert_str_to_json()` covering valid/invalid JSON, single quotes, empty strings, whitespace, nested structures, and non-list/dict results.

### Fixed

- `pyproject.toml` - Corrected the optional dependencies section.

---

## [0.2.0] — Testing with PyTest

**Date:** 2025-11-17

### Changed

- Updated all core modules to use `from __future__ import annotations`, expanded type hints, and refreshed module headers/docstrings.
- `newtutils/console.py` - Added `location` parameter to `validate_input()` calls for better error context. Implemented `validate_input()` using in other modules for consistent input validation and error handling.
- `newtutils/files.py` - Updated to use `collections.abc` types for better type hinting.
- `newtutils/utility.py` - Updated to use `collections.abc` types and added input validation to sorting functions, improving robustness and error handling.
- `newtutils/sql.py` - Strengthened with input validation, empty-query checks, basic multi-statement protection, dangerous token checks, better result validation, and clearer CSV export handling.
- Revised documentation across `README.md`, `INSTALL.md`, `CONTRIBUTING.md`, and `LICENSE` to reflect stable release status, required type hints, testing workflow, and dependency/license details.
- `pyproject.toml` - Updated project description and set project status to `Production/Stable`.

### Testing

- Replaced older script-style test workflow with pytest-based test modules and documented how to run them.
- Expanded test coverage for console, utility, files, SQL, and network behavior, including mocked HTTP requests and validation edge cases.
- Added generated pytest output files for multiple test runs and verbosity modes.
- `tests/_list.sh` - Reworked to run pytest-based test modules in multiple modes and save per-module output files.
- `tests/README.md` - Added documentation with pytest usage, helper script instructions, and coverage guidance.
- `pyproject.toml` - Added optional test dependencies with `pytest>=7.0.0`.

### Removed

- Deleted legacy standalone test scripts and old generated output files such as `tests/console.py`, `tests/console_output.txt`, and earlier plain output snapshots.

---

## [0.1.13] — Function choose_file_from_folder in Files

**Date:** 2025-10-29

### Added

- `newtutils/files.py` - Added `choose_file_from_folder()` function for interactive file selection in a directory.
- `newtutils/__init__.py` - Added `choose_file_from_folder()` to the public API.

### Changed

- `newtutils/files.py` - Updated `read_json_from_file()` to include stricter input validation and JSON structure checking, improving error handling and robustness when reading JSON files.
- `newtutils/utility.py` - Updated `validate_input()` and `sorting_list()` to support a `stop` flag that halts sorting and returns the original list if any invalid input is encountered.
- `newtutils/console.py` - Moved `validate_input()`, `_retry_pause()` and `_beep_boop()` from `utility.py` since they are more related to console interactions. Updated docstrings and internal calls accordingly.
- `newtutils/__init__.py` - Moved `validate_input` from `utility` to `console` and updated internal imports to use the new location.

### Fixed

- Refined docstrings and error messages across modules.

---

## [0.1.12] — Function _retry_pause in Utility

**Date:** 2025-10-26

### Added

- `newtutils/utility.py` - Extended with `_retry_pause()` helper function.
- `newtutils/network.py` - Response time and failure timing details added to network request logging.

### Changed

- `newtutils/network.py` - Refactored to use the new `_retry_pause()` helper for retry handling instead of duplicated countdown logic.
- `newtutils/__init__.py` - Updated to export the new network functions and refreshed documentation.
- `README.md` - Simplified project description to a concise general-purpose summary.
- `pyproject.toml` - Updated project description and project status to Beta.

### Testing

- `tests/utility.py` - Added test cases for the new `_retry_pause()` and `_beep_boop()` functions, including timing verification for retries.
- `tests/network.py` - Added test cases to cover invalid and valid URL fetch scenarios.
- `tests/_list.sh` - Updated to include the new network test scripts.
- Added cleanup verification messages to all current tests.

### Fixed

- `newtutils/sql.py` - `db_delayed_close()` now returns early when the target database file does not exist, preventing unnecessary operations and potential errors.

### Removed

- `TODO` - Removed outdated TODO items about splitting the old module and basic documentation/working checks.

---

## [0.1.11] — Module Network and Function _beep_boop in Utility

**Date:** 2025-10-25

### Added

- `newtutils/utility.py` - Added **winsound**-backed function `_beep_boop()` for audible alerts on Windows.
- `newtutils/network.py` - New module with HTTP helpers for fetching remote data and downloading files.
- `newtutils/__init__.py` - Exported all network utilities (`fetch_data_from_url`, `download_file_from_url`) and included it in `__all__` for direct package-level imports.
- `pyproject.toml` - Added **requests** as a dependency.
- `LICENSE` - Added **requests** third-party license notice for the new network module.
- `LICENSE` - Noted usage of Python standard library module **winsound** and **time** under the PSF license.
- `README.md` - Updated features list to include the new network utilities.

### Changed

- `newtutils/console.py` - Simplified formatting by standardizing the `_divider()` signature layout.
- `INSTALL.md` - Updated project structure diagram to include the new `network` module, as well as documentation files.

### Fixed

- `newtutils/files.py` - Improved `_check_file_exists()` to check if the path is a file and is accessible, preventing directory paths from being treated as files.

---

## [0.1.10] — Module SQL

**Date:** 2025-10-24

### Added

- `newtutils/sql.py` - New module with robust SQL utilities for database connectivity, query execution, and result handling.
- `newtutils/__init__.py` - Exported all SQL utilities (`db_delayed_close`, `sql_execute_query`, `sql_select_rows`, `sql_insert_row`, `sql_update_rows`, `export_sql_query_to_csv`) and included it in `__all__` for direct package-level imports.
- `README.md` - Updated features list to include the new SQL utilities.
- `pyproject.toml` - Added "sql" keyword for better packaging and discoverability.

### Changed

- `LICENSE` - Noted usage of Python standard library modules (**gc**, **sqlite3**) under the PSF license.
- `LICENSE` - Added **SQLite engine** third-party license notice for the new SQL module.

### Testing

- `tests/sql.py` - Comprehensive test suite for the new SQL utilities, covering database connection, query execution, result retrieval, and CSV export functionality. Tests include setup and teardown of a temporary SQLite database for isolation and cleanup.
- `tests/_list.sh` - Updated to include execution of the new SQL test suite.

### Fixed

- `newtutils/files.py` - Improved `_ensure_dir_exists()` to safely skip empty directory paths and only create missing folders.

---

## [0.1.9] — Private Function _check_file_exists in Files

**Date:** 2025-10-23

### Added

- `newtutils/files.py` - Private Function `_check_file_exists()` to check if a file exists and is accessible, used internally by all file I/O functions for robust error handling.

### Changed

- `INSTALL.md` - Removed numeric prefixes from section headings to simplify the document structure.

---

## [0.1.8] — Renamed and refined documentation

**Date:** 2025-10-23

### Changed

- Renamed `CHANGELOG` to `CHANGELOG.md`.
- `CHANGELOG.md` - Enhanced with tag emojis, structured headlines, and detailed release notes for all versions.
- Renamed `CONTRIBUTING` to `CONTRIBUTING.md`.
- `CONTRIBUTING.md` - Removed "Versioning and Releases" section and rebranded to **NewtCode**.
- `INSTALL.md` - Adjusted project structure and changed alias in code examples.
- `LICENSE` - Added link to **Python Software Foundation License**.
- `README.md` - Updated links to documentation files and removed example usage sections.
- `newtutils/console.py` - Improved Google-style docstring about `location` parameter in `error_msg()`.
- `newtutils/utility.py` - Removed `location` parameter from `validate_input()` signature and calls. Added `location` to all `error_msg()` calls.
- `pyproject.toml` - Fixed changelog URL to `CHANGELOG.md`.

### Testing

- `tests/_list.sh` - Echo statements for output file paths; changed final message.
- `tests/utility.py` - Edited test cases to reflect changes in `validate_input()` calls.

---

## [0.1.7] — Module Files

**Date:** 2025-10-21

### Added

- `newtutils/files.py` - New module with robust file I/O utilities for text, JSON, and CSV formats, including error-tolerant handling and directory creation.
- `newtutils/__init__.py` - Exported all file I/O functions (`read_text_from_file`, `save_text_to_file`, `read_json_from_file`, `save_json_to_file`, `read_csv_from_file`, `save_csv_to_file`) and included it in `__all__` for direct package-level imports.
- `pyproject.toml` - Added "files" keyword, **OS Independent** classifier, changelog URL, and `zip-safe=false` for better packaging and discoverability.
- `LICENSE` - Noted usage of Python standard library modules (**os**, **csv**, **json**) under the PSF license.

### Changed

- `INSTALL.md` - Updated project structure diagram to include the new `files` module and its associated tests, as well as documentation files.
- `README.md` - Updated features list to include the new file utilities.

### Testing

- `tests/files.py` - Comprehensive test suite for the new file I/O utilities, covering text append, JSON serialization, CSV tabular data, and automatic cleanup.
- `tests/_list.sh` - Updated to include execution of the new files test suite.

---

## [0.1.6] — Rename function sorting_ids to sorting_list in Utility

**Date:** 2025-10-21

### Changed

- `newtutils/utility.py` - Renamed `sorting_ids()` to `sorting_list()` across the package API, internal implementation, documentation, and examples.
- `CONTRIBUTING` - Expanded into a more complete contributor guide with branch naming, Conventional Commits, testing rules, code style expectations, versioning, and review workflow.

---

## [0.1.5] — Function validate_input in Utility

**Date:** 2025-10-21

### Added

- `newtutils/utility.py` - Function `validate_input()` to validate input values against expected types. Error messages printed using `NewtCons.error_msg()`.
- `newtutils/__init__.py` - Exported `validate_input` and included it in `__all__` for direct package-level imports.
- `newtutils/__init__.py` - Added typed metadata fields: `__license__` and `__url__`.
- `pyproject.toml` - Added project metadata fields: `keywords`, `classifiers`, `[project.urls]` and `[tool.setuptools.packages.find] > exclude` for better packaging and discoverability.
- `README.md` - Added project description, feature overview and usage examples.

### Changed

- `newtutils/utility.py` - Enhanced `sorting_ids()` and `sorting_dict_by_keys()` with input validation using `validate_input()`. Functions now handle invalid inputs gracefully by printing error messages instead of raising exceptions.
- `CHANGELOG.md` - Updated to follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format with semantic versioning links and categorized entries.

### Testing

- `tests/utility.py` - Added test cases for `validate_input()` with various valid and invalid inputs, verifying that error messages are printed correctly without exceptions.
- `tests/_list.sh` - Updated to run both console and utility tests, generating separate output files (`console_output.txt` and `utility_output.txt`) for easier review and debugging.

### Fixed

- `newtutils/utility.py` - Refactored code in `sorting_ids()` and `sorting_dict_by_keys()` for better readability and maintainability.
- `INSTALL.md` - Improved wording and formatting for better readability, including clearer import examples for both package-level and submodule imports.

### Removed

- `import typing` - Removed type hints to avoid circular dependencies and reduce overhead.

---

## [0.1.4] — Private Function _divider in Console

**Date:** 2025-10-20

### Added

- `newtutils/console.py` - Private Function `_divider()` to print a visual separator line in the console output.
- `.gitattributes` - Added a rule to treat `.toml` files as text with a TOML diff driver for better version control handling.

### Changed

- `newtutils/console.py` - Extended `error_msg()` with a new `location` parameter that prints the error source location, defaulting to `"Unknown"`.

### Testing

- `tests/console.py` - Refactored into separate functions with clearer structure and docstrings. Added a `__main__` entry point to run tests sequentially with clear output and internal `_divider()`s for readability.
- `tests/console.py` - Updated `error_msg()` tests to use the new `location=__file__` argument and verify location-aware output.
- `tests/_list.sh` - Script to run tests and write output to a text file for easier review and debugging.

---

## [0.1.3] — Function sorting_dict_by_keys in Utility

**Date:** 2025-10-17

### Added

- `newtutils/utility.py` - Function `sorting_dict_by_keys()` to sort a list of dictionaries by one or more keys. Dictionaries with missing keys placed at the end. Reverse sorting supported.
- `newtutils/__init__.py` - Exported `sorting_dict_by_keys` and included it in `__all__` for direct package-level imports.

### Changed

- `INSTALL.md` - Improved wording and formatting for better readability, including clearer import examples for both package-level and submodule imports.

### Testing

- `tests/utility.py` - Test suite for `sorting_dict_by_keys()` with various key combinations and sorting orders.

---

## [0.1.2] — Function sorting_ids in Utility

**Date:** 2025-10-17

### Added

- `newtutils/utility.py` - Function `sorting_ids()` to remove duplicates and return a sorted list of unique values.
- `newtutils/__init__.py` - Exported `sorting_ids` and included it in `__all__` for direct package-level imports.

### Testing

- `tests/utility.py` - Test suite for `sorting_ids()` with deduplication and sorting behavior for integers, strings, and mixed lists.

---

## [0.1.1] — Function error_msg in Console

**Date:** 2025-10-17

### Added

- `newtutils/console.py` - Function `error_msg()` using **colorama** for colored error output.
- `newtutils/__init__.py` - Package initializer with metadata, author info, and public export of `error_msg`.
- `pyproject.toml` - Project configuration for packaging, dependencies (**colorama**), and metadata.
- `INSTALL.md` - Comprehensive installation guide, project structure, VS Code setup, and usage examples.
- `README.md` - Added **colorama** dependency info.
- `LICENSE` - Added **colorama** third-party license notice.

### Testing

- `tests/console.py` - Test suite for `error_msg()` with stop/no-stop scenarios and exception handling.

---

## [0.1.0] — Initial setup

**Date:** 2025-10-16

### Added

- Created the *NewtUtils* repository.
- Defined the initial project structure.
- Added initial documentation and configuration files.

> 🪄 *The very first commit of the NewtUtils project.*
