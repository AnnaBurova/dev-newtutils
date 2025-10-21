# 🦎 NewtUtils — Developer Utilities by NewtCode

A lightweight Python toolkit providing reusable **console**, **validation**, and **sorting** utilities for developers.

---

## 📖 Overview

**NewtUtils** is designed as a small but extendable utility library to simplify common scripting and development tasks — such as structured console output, safe type validation, and flexible list or dictionary sorting.

The project uses clean, documented, and predictable function behavior.

---

## 🧩 Features

- 🖥️ **Console tools** — styled error messages, clean visual dividers
- 🧮 **Validation helpers** — safe type checking with non-blocking feedback
- 📑 **Sorting utilities** — deterministic and stable multi-key sorting
- 🧠 **Error-tolerant design** — no data loss even during exceptions

---

## ⚙️ Dependencies

- [**Colorama**](https://pypi.org/project/colorama/) — cross-platform colored terminal output.  
  Licensed under the [BSD License](https://github.com/tartley/colorama/blob/master/LICENSE.txt).

All other functions use only Python’s standard library.

---

## 🚀 Getting Started

Follow the [Installation Guide](INSTALL.md) for setup and editable installation details.

Example usage:

```python
from newtutils.console import error_msg
from newtutils.utility import sorting_list

error_msg("Example error", stop=False)
print(sorting_list(["z", 2, "a", 1, 1]))
```

---

## 📋 Development Notes

* Planned features and future improvements: see [TODO](TODO)
* Version history and updates: see [CHANGELOG](CHANGELOG)

## 🪪 License

- [COPYRIGHT](COPYRIGHT) — Copyright information for original and included materials.
- [LICENSE](LICENSE) — The license governing the use of this repository (MIT).
- [AUTHORS](AUTHORS) — List of contributors and credit for external resources.
- [CONTRIBUTING](CONTRIBUTING) — Guidelines for contributing to this repository.
