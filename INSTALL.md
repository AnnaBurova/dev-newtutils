# 🧰 Installing and Developing the NewtUtils Module

This guide explains how to set up, install, and use **NewtUtils** — a collection of developer utilities by *NewtCode*.

---

## 1. Project Structure

```
dev-newtutils/         # Root repository
│
├── newtutils/         # Main Python package (module source)
│   ├── __init__.py
│   ├── console.py
│   ├── files.py
│   ├── utility.py
│   └── (other utility files)
│
├── tests/             # Manual and automated test scripts
│   ├── _list.sh       # Optional helper script to list or run tests
│   ├── console.py
│   ├── files.py
│   ├── utility.py
│   └── (other test files)
│
├── CHANGELOG          # Version history and release notes
├── CONTRIBUTING.md    # Guidelines for contributors
├── INSTALL.md         # Installation and development setup guide
├── LICENSE            # License file (MIT)
├── README.md          # Project overview and usage instructions
└── pyproject.toml     # Build system configuration and project metadata
```

---

## 2. `pyproject.toml` Overview

The `pyproject.toml` file defines how the package is built and installed.

Key fields:

* `requires-python` — the minimum supported Python version.
* `dependencies` — required third-party libraries.
* `[tool.setuptools.packages.find]` — tells setuptools where to find your package.

---

## 3. `__init__.py` Setup

Keep `__init__.py` minimal and clean.

Example:

```python
from .console import error_msg
from .utility import (
    validate_input,
    sorting_list,
    sorting_dict_by_keys,
)

__author__ = "Name"
__version__ = "0.0.0"
__description__ = "Description"
```

---

## 4. Local Installation (Editable Mode)

To make code changes available immediately without reinstalling:

```powershell
cd D:\VS_Code\dev-newtutils
C:/ProgramData/anaconda3/python.exe -m pip install --user -e .
```

**Explanation:**

* `-m pip` ensures that pip runs within the chosen Python environment.
* `--user` — install for the current user only (no admin rights needed).
* `-e .` — install in *editable mode* (links directly to your source folder).
* You can now import `newtutils` in any project, and edits will take effect instantly.

To uninstall later:

```powershell
pip uninstall newtutils
```

---

## 5. VS Code Configuration

To help VS Code (and Pylance) detect your local package:

1. Create `.vscode/settings.json` inside your project.
2. Add:

```json
{
  "python.analysis.extraPaths": [
    "D:/VS_Code/dev-newtutils"
  ],
  "python.defaultInterpreterPath": "C:/ProgramData/anaconda3/python.exe"
}
```

Reload VS Code (`Ctrl + Shift + P` > "Developer: Reload Window").

---

## 6. Using NewtUtils in Other Projects

Once installed (even in editable mode), you can import it anywhere:

```python
# WORKS ONLY WITH CORRECT __init__.py
# Examples of importing functions directly from the package (requires re-export in __init__.py)

from newtutils import error_msg
error_msg("Something went wrong", stop=False)

import newtutils as Newt
Newt.error_msg("Something went wrong", stop=False)
```

Alternative imports:

```python
# Direct import from the submodule (does not depend on __init__.py)
# Alternative ways to access the same function directly from 'newtutils.console'

import newtutils as Newt
Newt.console.error_msg("Something went wrong", stop=False)

from newtutils.console import error_msg as err
err("Something went wrong", stop=False)

import newtutils.console as Newt_console
Newt_console.error_msg("Something went wrong", stop=False)
```

If you prefer not to install at all, just add the path at runtime:

```python
import sys
sys.path.append(r"D:\VS_Code\dev-newtutils")
from newtutils.console import error_msg
```

---

## 7. Updating the Package

Because the package is installed in editable mode,
any file changes under `newtutils/` are applied immediately — no reinstall needed.

If you modify the project metadata (e.g., version or dependencies) in `pyproject.toml`,
re-run the install command:

```powershell
python -m pip install -e .
```
