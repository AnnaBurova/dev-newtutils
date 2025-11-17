# ⚙️ Installing and Developing the NewtUtils Module

This guide explains how to install, use, update, and remove **NewtUtils** — a collection of developer utilities by *NewtCode*.

---

## 🧱 Project Structure (for reference)

```
dev-newtutils/
│
├── newtutils/         # Main Python package (module source)
│   ├── __init__.py
│   ├── console.py
│   ├── utility.py
│   ├── files.py
│   ├── sql.py
│   ├── network.py
│   └── (other files)
│
├── tests/             # Manual and automated test scripts
│   ├── README.md      # Testing overview and usage instructions
│   ├── _list.sh       # Optional helper script to list or run tests
│   ├── test_*.py      # Pytest test files for each module
│   └── (test files)
│
├── pyproject.toml     # Build system configuration and project metadata
├── CHANGELOG.md       # Version history and release notes
├── CONTRIBUTING.md    # Guidelines for contributors
├── INSTALL.md         # Installation and development setup guide
├── LICENSE            # License file (MIT)
└── README.md          # Project overview and usage instructions
```

---

## 📦 Requirements

- **Python 3.10 - 3.13**
- **pip** or **conda** (Anaconda users supported)
- Dependencies (installed automatically):
  - `colorama` — for colored console output
  - `requests` — for HTTP/network utilities

---

## 🧰 Local Installation Options (No PyPI)

Since **NewtUtils** is a local development library and not published on PyPI, installation should be done directly from your project folder.

### Option 🟢 — Regular local installation (static copy)

Installs a copy of the package.

```powershell
# Navigate to your project directory
cd D:\VS_Code\dev-newtutils

python -m pip install --user .
# OR for Anaconda
C:/ProgramData/anaconda3/python.exe -m pip install --user .
```

> 🧩 Recommended when you only want to use **NewtUtils**, not actively edit its source code.

> Safe for non-admin users.
> `--user` — installs into your personal environment instead of `C:\ProgramData`.

### Option 🔵 — Editable installation (recommended for development)

Links the library directly to your working folder.
Any code changes in `newtutils/` will take effect immediately.
No reinstall needed.

```powershell
# Navigate to your project directory
cd D:\VS_Code\dev-newtutils

# Install in editable mode (user environment)
python -m pip install --user -e .
# OR for Anaconda
C:/ProgramData/anaconda3/python.exe -m pip install --user -e .
```

> `--editable` or `-e` — link the project folder directly for live development

### Option 🟣 — Temporary usage (without installation)

If you just want to run or test functions directly from source:

```python
import sys
import os

# Adjust this path to your actual project location
newt_root = os.path.join("D:", "VS_Code", "dev-newtutils")
# Or use absolute path:
# newt_root = r"D:\VS_Code\dev-newtutils"

if newt_root not in sys.path:
    sys.path.append(newt_root)

import newtutils as Newt
```

This approach doesn't install anything globally, it only extends your Python path for the current session.

---

## 📚 Usage Examples

After installation (regular or editable), you can import **NewtUtils** anywhere:

```python
# Import the main package (recommended - exports common functions)
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

---

## 🧿 VS Code + Anaconda Setup

To make VS Code recognize your local package:

1. Create or open `.vscode/settings.json`

2. Add the following:

```json
{
  "python.analysis.extraPaths": [
    "D:/VS_Code/dev-newtutils"
  ],
  "python.defaultInterpreterPath": "C:/ProgramData/anaconda3/python.exe"
}
```

> **Note:** Adjust the paths above to match your actual project location and Python interpreter path.

3. Reload VS Code (`Ctrl + Shift + P` > "Developer: Reload Window").

---

## 🗑️ Uninstalling

To remove the package completely:

```powershell
pip uninstall newtutils
# OR for Anaconda global install (requires admin rights)
C:/ProgramData/anaconda3/python.exe -m pip uninstall newtutils
```

If installed with `--user`, you can also manually delete:

```
%APPDATA%\Python\Python313\site-packages\newtutils*
```
