```text
Author: NewtCode Anna Burova
Created: 2024-06
Updated: 2026-11
```

# Testing the NewtUtils Package (NewtCode)

This directory contains comprehensive unit tests for the **NewtUtils** package.

## Test Environment

Before running the tests, install the package and test dependencies
in the available virtual environments.

To update all configured development virtual environments
and install the optional `test` dependencies defined in `pyproject.toml`,
use the PowerShell helper script:

```pwsh
& '.\dev-newtutils\tests\_update_venv.ps1'
```

ALTERNATIVELY, install the package in editable mode MANUALLY.

```sh
# Activate Virtual Environment

# Navigate to the project directory:
cd ./dev-newtutils/

# Install the NewtUtils package in editable mode, including test dependencies
python -m pip install -e ".[test]"
```

## Running Tests using PyTest

```sh
# Activate Virtual Environment

# Navigate to the project directory:
cd ./dev-newtutils/

# Run all tests:
python -m pytest tests/

# OR Run a specific test file:
python -m pytest tests/test_module.py
```

### PyTest Options

- `-v` — Enables verbose pytest output (with truncated diffs).
- `-vv` — Enables extra-verbose pytest output (without truncation).
- `-s` — Shows output from `print()` statements.
- `> test_results.txt` — Saves standard output to a file.
- `>` — Creates (or overwrites) the output file.
- `>>` — Appends output to the end of an existing file.
- `2>&1` — Redirects `stderr` to the same destination as `stdout`.

Run with different options:

```sh
# Navigate to the project directory:
cd ./dev-newtutils/

pytest tests/
pytest tests/ -v
pytest tests/ -vv
pytest tests/ -s
pytest tests/ -s -vv
pytest tests/ -s -vv > 'test_results.txt' 2>&1
```

### Batch Test Runner `_run_tests.ps1` or `_run_tests.sh`

The script uses the virtual environments configured inside file.
If pytest is not found in a virtual environment, that environment is skipped.

It runs each module with four pytest configurations:

1. Default mode.
2. Verbose mode (`-vv`).
3. Show `print()` output (`-s`).
4. Verbose mode with `print()` output (`-s -vv`).

Test results are saved in the `dev-newtutils/tests/output/` directory.

Example output files:

```text
output/venv315_test_module_function_1.txt
output/venv315_test_module_function_2.txt
output/venv315_test_module_function_3.txt
output/venv315_test_module_function_4.txt
```

The filename format is:

```text
<virtual-environment>_test_<module>_<mode>.txt
```

## Test Coverage

### What Is Coverage?

Code coverage shows which parts of the source code are executed by the tests.
It can help identify:

- untested lines;
- untested functions;
- untested logic branches (if/else);
- the overall coverage percentage.

### Run Coverage

```sh
# Activate Virtual Environment

# Navigate to the project directory:
cd ./dev-newtutils/

# Run all tests:
python -m pytest tests/ --cov=new_python_package --cov-report=html --cov-report=term-missing

# OR Run a specific test file:
python -m pytest tests/test_module.py --cov=new_python_package --cov-report=html --cov-report=term-missing
```

These commands create an `htmlcov/` directory containing the report.
The report highlights covered and uncovered lines.
(green = covered, red = not covered)

Open the report in a browser:

```pwsh
start '.\htmlcov\index.html'
```

## Helper Functions

The `helpers.py` file contains reusable functions for tests.

These helpers can be used to:

- print the name of the current test function;
- display captured standard output and standard error;
- format test output for easier debugging.

The helper functions are optional.
Tests can also use `capsys.readouterr()` and normal `print()` statements directly.

## Notes

- All tests are designed to be independent and can run in any order.
- File tests use temporary files and directories.
- SQL tests create temporary databases that are cleaned up after tests.
- Network tests use mocked HTTP requests to avoid actual network calls.
