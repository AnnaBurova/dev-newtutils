# Tests for NewtUtils

This directory contains comprehensive unit tests for the `newtutils` package.

## Test Files

- `test_console.py` - Tests for console utilities (error messages, validation)
- `test_utility.py` - Tests for utility functions (sorting)
- `test_files.py` - Tests for file operations (text, JSON, CSV)
- `test_sql.py` - Tests for SQL operations
- `test_network.py` - Tests for network operations

## Helper Scripts

`_list.sh` — Batch Test Runner

The `_list.sh` script automatically runs all test modules with different pytest options and saves the output to text files. This is useful for generating reference output files or batch testing.

**What it does:**

- Runs pytest for all modules (console, utility, files, sql, network)
- Executes each module with 4 different pytest configurations:
    - 1). Default mode
    - 2). Verbose mode (`-v`)
    - 3). Show print statements (`-s`)
    - 4). Verbose + show print statements (`-s -v`)
- Saves output to `test_*_output_*.txt` files in the tests directory
- Converts line endings to LF format (requires `dos2unix` if available)

**Requirements:**

- `pytest` must be installed
- Optional: `dos2unix` (for line ending conversion; script will continue without it)

**Usage:**

Navigate to the tests directory first:
```bash
cd tests
```

Then run the script:

**Linux/macOS:**

```bash
sh _list.sh
# or
bash _list.sh
# or make it executable and run directly:
chmod +x _list.sh
./_list.sh
```

**Windows:**

For Windows users, run the script using Git Bash or WSL (Windows Subsystem for Linux):

```bash
bash _list.sh
```

**Note:** The script contains a hardcoded path (`D:/VS_Code/dev-newtutils/tests/`).
If your project is located elsewhere, you may need to edit the script or adjust the path.

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

## Test Coverage

**Code Coverage** is a metric that shows what percentage of your code is tested.
The new pytest-based tests provide comprehensive coverage of:

- **Console module**: Error messaging, input validation, beep notifications, retry pauses
- **Utility module**: List sorting, dictionary sorting by keys
- **Files module**: Directory operations, file existence checks, text/JSON/CSV read/write operations
- **SQL module**: Database operations, queries, inserts, updates, CSV exports
- **Network module**: URL fetching, file downloading (with mocked HTTP requests)

Run with code coverage analysis:

```bash
pip install pytest-cov
pytest tests/ --cov=newtutils --cov-report=html
```

**What is coverage?**

Code coverage measures how much of your source code is executed by tests. It shows:

- Which lines of code were run during tests
- Which functions were called
- Which branches (if/else) were tested
- Overall percentage of code covered

After running the command above, open `htmlcov/index.html` in your browser to see a detailed coverage report with highlighted lines (green = covered, red = not covered).

## Notes

- All tests are designed to be isolated and can run in any order
- File tests use temporary files and directories
- SQL tests create temporary databases that are cleaned up after tests
- Network tests use mocked HTTP requests to avoid actual network calls
