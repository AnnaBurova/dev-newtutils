# Tests for NewtUtils

This directory contains comprehensive unit tests for the `newtutils` package.

## Test Files

- `test_console.py` - Tests for console utilities (error messages, validation)
- `test_utility.py` - Tests for utility functions (sorting)
- `test_files.py` - Tests for file operations (text, JSON, CSV)
- `test_sql.py` - Tests for SQL operations
- `test_network.py` - Tests for network operations

## Running Tests

### Using pytest (recommended)

Install pytest:
```bash
pip install pytest
```

Run all tests:
```bash
pytest tests/
```

Run a specific test file:
```bash
pytest tests/test_files.py
```

Run with verbose output:
```bash
pytest tests/ -v
pytest tests/ -v > test_results.txt 2>&1

```

Run with coverage:
```bash
pip install pytest-cov
pytest tests/ --cov=newtutils --cov-report=html
```

### Using the original test scripts

The original test scripts (`files.py`, `console.py`, etc.) can still be run directly:
```bash
python tests/files.py
python tests/console.py
```

## Helper Scripts

In addition to the test scripts, you can run the helper script `_list.sh` from the tests directory. 
To execute the script, use the following command:

```bash
sh _list.sh
```

### Windows Usage

For Windows users, you can run the script using Git Bash or WSL (Windows Subsystem for Linux):

```bash
bash _list.sh
```

## Test Coverage

The new pytest-based tests provide comprehensive coverage of:

- **Console module**: Error messaging, input validation, beep notifications, retry pauses
- **Utility module**: List sorting, dictionary sorting by keys
- **Files module**: Directory operations, file existence checks, text/JSON/CSV read/write operations
- **SQL module**: Database operations, queries, inserts, updates, CSV exports
- **Network module**: URL fetching, file downloading (with mocked HTTP requests)

## Notes

- All tests are designed to be isolated and can run in any order
- File tests use temporary files and directories
- SQL tests create temporary databases that are cleaned up after tests
- Network tests use mocked HTTP requests to avoid actual network calls
