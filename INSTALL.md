# Creating the NewtUtils Python Module

This guide describes how to structure, configure, and test the **NewtUtils** Python module.

---

## 1. Project Structure

```
dev-newtutils/         # Root repository
│
├── newtutils/         # Python package
│   ├── __init__.py
│   ├── console.py
│   └── (other utility files)
│
├── tests/             # Folder for tests
│   ├── console.py
│   └── (other test files)
│
├── LICENSE            # License file
├── README.md          # Project description
└── pyproject.toml     # Build and metadata configuration
```

---

## 2. Configuring `pyproject.toml`

The `pyproject.toml` file defines build tools, dependencies, and metadata.

* `requires-python` specifies the minimum supported Python version.
* `dependencies` lists all required packages.
* `tool.setuptools.packages.find` ensures the package folder is correctly recognized during installation.

---

## 3. Configuring `__init__.py`

To make the module accessible and maintain clean imports:

* Import only selected functions or classes intended for external use.
* Include metadata such as `__author__`, `__description__`, and `__version__`.

---

## 4. Installing NewtUtils Locally

To install **NewtUtils** in *editable mode* (so changes are applied immediately):

1. Open PowerShell or any terminal.
2. Navigate to the repository folder.
3. Run the installation command:

```powershell
cd D:\VS_Code\dev-newtutils
C:/ProgramData/anaconda3/python.exe -m pip install --user -e .
```

* `-m pip` ensures that pip runs within the chosen Python environment.
* `--user` installs the module for the current account (no administrator rights required).
* `-e .` installs in **editable mode**, enabling immediate access to any code changes within `newtutils/`.

---

## 5. VS Code Configuration for Local Python Modules

When working in **VS Code**, local modules such as `newtutils` can be recognized automatically with the following setup:

1. Open the project folder in VS Code.
2. Create the `.vscode` directory inside the project (if not already present).
3. Inside `.vscode`, create or edit the `settings.json` file.
4. Add the configuration below:

```json
{
  "python.analysis.extraPaths": [
    "D:/VS_Code/dev-newtutils"
  ],
  "python.defaultInterpreterPath": "C:/ProgramData/anaconda3/python.exe"
}
```

5. Save the file and reload VS Code
(`Ctrl + Shift + P` → `Developer: Reload Window`).

Pylance will now correctly resolve imports from `newtutils`.

---

## 6. Using the Module in Other Projects

Once installed, **NewtUtils** can be imported into any Python project as a standard module.

Example:

```python
# WORKS ONLY WITH CORRECT __init__.py
# Examples of importing functions directly from the package (requires re-export in __init__.py)

from newtutils import error_msg
error_msg("Error1", stop=False)
import newtutils as Newt
Newt.error_msg("Error4", stop=False)
Newt.console.error_msg("Error5", stop=False)
```

```python
# Direct import from the submodule (does not depend on __init__.py)
# Alternative ways to access the same function directly from 'newtutils.console'

from newtutils.console import error_msg as err
err("Error2", stop=False)
import newtutils.console as Newt_console
Newt_console.error_msg("Error3", stop=False)
```

If the module is not installed system-wide but is available locally, add its path dynamically at runtime:

```python
import sys
sys.path.append(r"D:\VS_Code\dev-newtutils")
from newtutils.console import error_msg
```
