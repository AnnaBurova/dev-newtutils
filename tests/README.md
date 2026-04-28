# Tests for NewtUtils

This directory contains comprehensive unit tests for the **NewtUtils** package.

## Test Files

- `test_console.py` - Tests for console utilities (error messages, validation)
- `test_utility.py` - Tests for utility functions (sorting)
- `test_files.py` - Tests for file operations (text, JSON, CSV)
- `test_sql.py` - Tests for SQL operations
- `test_network.py` - Tests for network operations

## Helper Scripts

`_list.sh` — Batch Test Runner

The `_list.sh` script automatically runs all test modules with different pytest and virtual environments options and saves the output to text files.
This is useful for generating reference output files or batch testing.

### What it does

- Runs pytest for all listed modules and virtual environments
- Executes each module with 4 different pytest configurations:
    - 1). Default mode
    - 2). Verbose mode (`-v`)
    - 3). Show print statements (`-s`)
    - 4). Verbose + show print statements (`-s -v`)
- Saves output to `*_test_*_output_*.txt` files in the tests directory
- Converts line endings to LF format (requires `dos2unix` if available)

### Requirements

- `pytest` must be installed
- Optional: `dos2unix` (for line ending conversion; script will continue without it)

### Usage

```bash
# Navigate to the tests directory first:
$ cd dev-newtutils/tests/

# (Linux) Make it executable:
$ chmod +x _list.sh

# Run the script:
# (Windows) Run the script using Git Bash or WSL (Windows Subsystem for Linux)
$ ./_list.sh
# or
$ sh _list.sh
# or
$ bash _list.sh
```

## Running Tests Using PyTest

```bash
# Install pytest:
$ pip install pytest

# Navigate to the tests directory:
$ cd dev-newtutils/

# Run all tests:
$ pytest tests/
# Run a specific test file:
$ pytest tests/test_console.py

# or
# Navigate to the tests directory first:
$ cd dev-newtutils/tests/
# Run all tests:
$ pytest .
# Run a specific test file:
$ pytest ./test_console.py
```

Run with verbose output:

```bash
$ pytest tests/
$ pytest tests/ -v
$ pytest tests/ -s
$ pytest tests/ -s -v
$ pytest tests/ -s -v > test_results.txt 2>&1
```

## Test Coverage

**Code Coverage** is a metric that shows what percentage of your code is tested.

```bash
# Install pytest-cov:
$ pip install pytest-cov

# Navigate to the tests directory:
$ cd dev-newtutils/

# Run all tests with code coverage analysis:
$ pytest tests/ --cov=newtutils --cov-report=html
# Run a specific test file with code coverage analysis:
$ pytest tests/test_console.py --cov=newtutils --cov-report=html
```

### What is coverage?

Code coverage measures how much of your source code is executed by tests. It shows:

- Which lines of code were run during tests
- Which functions were called
- Which branches (if/else) were tested
- Overall percentage of code covered

After running the command above folder `htmlcov/` will be generated. Open `htmlcov/index.html` in your browser to see a detailed coverage report with highlighted lines (green = covered, red = not covered).

## Notes

- All tests are designed to be isolated and can run in any order.
- File tests use temporary files and directories.
- SQL tests create temporary databases that are cleaned up after tests.
- Network tests use mocked HTTP requests to avoid actual network calls.
