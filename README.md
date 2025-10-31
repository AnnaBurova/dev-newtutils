# 🦎 NewtUtils — Developer Utilities by `NewtCode`

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

A collection of utility functions for common programming tasks.

---

## 📖 Overview

**NewtUtils** is designed as a small but extendable utility library to simplify common scripting and development tasks — such as structured console output, safe type validation, file management, SQL access, and API communication.

The project follows clean, documented, and predictable function behavior for maintainable and testable code. All functions include comprehensive type hints and Google-style docstrings for better IDE support and code clarity.

---

## 🧩 Features

- 🖥️ **Console tools** — styled error messages, clean visual dividers
- 🧮 **Validation helpers** — safe type checking with non-blocking feedback
- 📑 **Sorting utilities** — deterministic and stable multi-key sorting
- 🗂️ **File utilities** — simple read/write support for text, JSON, and CSV
- 🧠 **Error-tolerant design** — no data loss even during exceptions
- 🗄️ **SQL utilities** — safe and simple SQLite operations (execute, select, insert, update, export)
- 🌐 **Network utilities** — safe API requests and file downloading with retry logic

---

## ⚙️ Requirements

- **Python 3.10+** (tested with Python 3.10, 3.11, 3.12, 3.13)
- Full type hint support with `from __future__ import annotations`

## 📦 Dependencies

- [**Colorama**](https://pypi.org/project/colorama/) — cross-platform colored terminal output.  
  Licensed under the [BSD 3-Clause License](https://github.com/tartley/colorama/blob/master/LICENSE.txt).

- [**Requests**](https://pypi.org/project/requests/) — HTTP library for API communication.  
  Licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).

All other modules rely only on the Python Standard Library.

---

## 🚀 Getting Started

- [Installation Guide](INSTALL.md) — setup instructions and configuration details.

---

## 📋 Development Notes

- [TODO list](TODO) — Planned improvements
- [CHANGELOG](CHANGELOG.md) — Version history
- [CONTRIBUTING](CONTRIBUTING.md) — Style and contribution rules

---

## 🪪 License

- [COPYRIGHT](COPYRIGHT) — Copyright information for original and included materials.
- [LICENSE](LICENSE) — The license governing the use of this repository (MIT).
- [AUTHORS](AUTHORS) — List of contributors and credits for external resources.
