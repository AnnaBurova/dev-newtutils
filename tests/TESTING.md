# Testing NewtUtils

This directory contains comprehensive unit tests for the **NewtUtils** package.

## Test Files

- test_console.py
- test_utility.py
- test_files.py
- test_sql.py
- test_network.py

## Test Environment

Before running the tests, install the package and test dependencies
in the available virtual environments.

The script updates the package in the configured virtual environments
using editable installation and installs the test dependencies from the `test` group.

Use the PowerShell helper script:

```bash
$ ./dev-newtutils/tests/_update_venv.ps1
```

OR:

```bash
$ cd ./dev-newtutils/tests
$ ./_update_venv.ps1
```

If you do not want to use the helper script,
install the dependencies manually in the currently active virtual environment:

```bash
$ python -m pip install -e ".[test]"
```

The `test` group should provide the required testing packages, including:

- `pytest`
- `pytest-cov`

## Running Tests using PyTest

```bash
# Navigate to the project directory:
$ cd dev-newtutils/

# Run all tests:
$ pytest tests/
# OR Run a specific test file:
$ pytest tests/test_console.py
$ pytest tests/test_utility.py
$ pytest tests/test_files.py
$ pytest tests/test_sql.py
$ pytest tests/test_network.py
```

OR run pytest from inside the `tests` directory:

```bash
# Navigate to the tests directory:
$ cd dev-newtutils/tests/

# Run all tests:
$ pytest .
# OR Run a specific test file:
$ pytest ./test_console.py
$ pytest ./test_utility.py
$ pytest ./test_files.py
$ pytest ./test_sql.py
$ pytest ./test_network.py
```

### Pytest Options

- `-v` — enables verbose pytest output
- `-vv` — enables extra verbose pytest output
- `-s` — shows output from print() statements
- `> test_results.txt` — saves standard output to a file.
- `>` — Creates (or overwrites) the output.txt file.
- `>>` — Appends output to the end of an existing file.
- `2>&1` — Redirects stderr to the same destination as stdout

Run with different options:

```bash
# Navigate to the project directory:
$ cd dev-newtutils/

$ pytest tests/
$ pytest tests/ -vv
$ pytest tests/ -s
$ pytest tests/ -s -vv
$ pytest tests/ -s -vv > test_results.txt 2>&1
```

## Batch Test Runner

### `_run_tests.sh`

`_run_tests.sh` runs selected test modules in the configured virtual environments.

The script uses the virtual environments configured inside `_run_tests.sh`.
Run `_update_venv.ps1` first if the environments need to be updated
with the project and test dependencies.

It runs each module with four pytest configurations:

1. Default mode.
2. Verbose mode (`-v`).
3. Show `print()` output (`-s`).
4. Verbose mode with `print()` output (`-s -v`).

Test results are saved in the `dev-newtutils/tests/output/` directory.

Example output files:

```text
output/venv314_test_console_1.txt
output/venv314_test_console_2.txt
output/venv314_test_console_3.txt
output/venv314_test_console_4.txt
```

The filename format is:

```text
<virtual-environment>_test_<module>_<mode>.txt
```

If pytest is not found in a virtual environment, that environment is skipped.

### Run the Batch Test Runner

The script is intended to be run from Git Bash or WSL on Windows,
or directly from a Bash-compatible shell on Linux.

```bash
# Navigate to the tests directory:
$ cd dev-newtutils/tests/

# On Linux or WSL, make the script executable:
$ chmod +x _run_tests.sh

# Run the script:
$ ./_run_tests.sh
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

```bash
# Navigate to the project directory:
$ cd dev-newtutils/

# Run all tests with code coverage analysis:
$ pytest tests/ --cov=newtutils --cov-report=html --cov-report=term-missing
# OR Run a specific test file with code coverage analysis:
$ pytest tests/test_console.py --cov=newtutils --cov-report=html --cov-report=term-missing
$ pytest tests/test_utility.py --cov=newtutils --cov-report=html --cov-report=term-missing
$ pytest tests/test_files.py --cov=newtutils --cov-report=html --cov-report=term-missing
$ pytest tests/test_sql.py --cov=newtutils --cov-report=html --cov-report=term-missing
$ pytest tests/test_network.py --cov=newtutils --cov-report=html --cov-report=term-missing
```

These commands create an `htmlcov/` directory containing the report.
The report highlights covered and uncovered lines.
(green = covered, red = not covered)
Open the report in a browser:

```bash
$ start htmlcov/index.html
```

## Helper Functions

The `helpers.py` file contains reusable functions for tests.

These helpers can be used to:

- print the name of the current test function;
- display captured standard output and standard error;
- format test output for easier debugging.

Example:

```python
from helpers import newt_print_captured

captured = capsys.readouterr()
newt_print_captured(captured)
```

The helper functions are optional.
Tests can also use `capsys.readouterr()` and normal `print()` statements directly.

## Notes

- All tests are designed to be independent and can run in any order.
- File tests use temporary files and directories.
- SQL tests create temporary databases that are cleaned up after tests.
- Network tests use mocked HTTP requests to avoid actual network calls.
