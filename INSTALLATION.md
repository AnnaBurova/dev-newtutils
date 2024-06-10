```text
Author: NewtCode Anna Burova
Created: 2024-06
Updated: 2026-11
```

# Installing the NewtUtils Package (NewtCode)

## Project Structure Overview

```text
dev-newtutils/                    # Root repository
│
├── src/
│   └── newtutils/                # Main Python package
│       ├── __init__.py           # Defines the package's public import interface
│       ├── console.py
│       ├── utility.py
│       ├── files.py
│       ├── sql.py
│       ├── network.py
│       └── (other modules)
│
├── tests/                        # Manual and automated test scripts
│   ├── output/                   # Test output logs
│   │   ├── venv_test_module_1.txt
│   │   ├── venv_test_module_2.txt
│   │   ├── venv_test_module_3.txt
│   │   ├── venv_test_module_4.txt
│   │   └── (other test logs)
│   │
│   ├── README_TESTING.md         # Instructions for running tests across Python versions
│   ├── _run_tests.sh             # (Optional) Test runner script
│   ├── _update_venv.ps1          # (Optional) Updates packages in virtual environments
│   ├── __init__.py               # Marks the tests directory as a package
│   ├── helpers.py                # Helper functions for tests
│   ├── test_console.py
│   ├── test_utility.py
│   ├── test_files.py
│   ├── test_sql.py
│   ├── test_network.py
│   └── (other tests)
│
├── .gitignore                    # Excludes local environments, caches, and build output
├── LICENSE                       # Terms for using and distributing the package
├── CHANGELOG.md                  # Optional record of changes between releases
├── CONTRIBUTING.md               # Optional baseline for project contributions
├── INSTALLATION.md               # Local setup instructions
├── pyproject.toml                # Build configuration and package metadata
├── requirements.txt              # Runtime dependencies for using the package
└── README.md                     # Project overview and first-use instructions
```

## Requirements

NewtUtils supports the following Python versions:

- Python 3.15
- Python 3.14
- Python 3.13
- Python 3.12
- Python 3.11

Other dependencies are listed in `requirements.txt`.

**Note:** For distribution as a package, dependencies should also be specified in
`pyproject.toml` under `[project] dependencies`.
The `requirements.txt` file is kept here for local development convenience.

## Installation Mode: Local Installation (No PyPI)

The **NewtUtils** project is a local development package and is not published on PyPI.
Installation should be performed directly from the project folder.

---

### Regular Local Installation (Static Copy)

Installs a copy of the package into the active virtual environment.
Recommended when the project is only intended to be used
and its source code does not need to be edited.

```sh
# Activate Virtual Environment

# Navigate to the project directory:
cd ./dev-newtutils/

# Install dependencies first (if requirements.txt exists)
python -m pip install -r requirements.txt

# Install the NewtUtils package
python -m pip install .
```

---

### Editable Local Installation (Recommended for Development)

To update all configured development virtual environments
and install the optional `test` dependencies defined in `pyproject.toml`,
use the PowerShell helper script:

```pwsh
& '.\dev-newtutils\tests\_update_venv.ps1'
```

Recommended when the project is intended to be used and tested.

---

ALTERNATIVELY, install the package in editable mode MANUALLY.

This links the project source folder directly to the Python environment.
Changes made in `src/newtutils/` take effect immediately.
No reinstallation is required after each edit.

- `--editable` or `-e` creates a link to the local project
instead of copying its files into the environment.

```sh
# Activate Virtual Environment

# Navigate to the project directory:
cd ./dev-newtutils/

# Install dependencies first (if requirements.txt exists)
python -m pip install -r requirements.txt

# Install the NewtUtils package in editable mode, including test dependencies
python -m pip install -e ".[test]"
```

---

### Temporary Local Usage (Without Installation)

To run or test functions directly from the downloaded source.
This approach does not install anything globally;
it only extends the Python path for the current session.

```python
# Import required modules
import sys
from pathlib import Path

# Adjust this path to the actual project location
proj_root = Path("D:/") / "VS_Code" / "dev-newtutils" / "src"

if str(proj_root) not in sys.path:
    sys.path.append(str(proj_root))

import newtutils as Newt
```

---

### VS Code Settings

To make VS Code recognize the local package:

1. Create or open `.vscode/settings.json` in the VS Code workspace root.

2. Add or extend the following:
    ```jsonc
    {
        "python.analysis.extraPaths": [
            "./dev-newtutils/src",
        ],
    }
    ```

    - Adjust the path so that it points to the `src` directory of the project.
    - The path must be relative to the VS Code workspace root.
    - Do not include `newtutils` at the end of the path.

3. Reload VS Code (`Ctrl + Shift + P` -> "Developer: Reload Window").

## Uninstalling

To remove the package from the active virtual environment:

```sh
# Check whether the package is installed
python -m pip show newtutils

# Uninstall the package
python -m pip uninstall newtutils
```

## Usage Examples

After installation, the **NewtUtils** package can be imported from anywhere:

```python
# Import the package
import newtutils as Newt

# Or import specific modules
import newtutils.console as NewtCons
import newtutils.utility as NewtUtil
import newtutils.files as NewtFiles
import newtutils.sql as NewtSQL
import newtutils.network as NewtNet

# Usage examples:
Newt.error_msg("Something went wrong", stop=False)
Newt.console.error_msg("Something went wrong", stop=False)
NewtCons.error_msg("Something went wrong", stop=False)
```
