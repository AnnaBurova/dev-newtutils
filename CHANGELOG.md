# 🧾 Changelog — *NewtUtils (NewtCode)*

All notable changes to this project are documented here.
This project follows [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`).

---

## 🏷️ v0.1.4 — Files utilities

**Date**: 2025-10-21

### ✨ Added

- New module: `files.py` — read/write helpers for **text**, **JSON**, and **CSV** files.

### 🛠️ Improved

- Added complete Google-style docstrings for all file functions.
- Unified metadata across project files (`__init__.py`, `pyproject.toml`).
- Updated documentation (`INSTALL.md`, `README.md`, `LICENSE`).

---

## 🏷️ v0.1.3 — Sorting utilities

**Date:** 2025-10-20

### ✨ Added

- Added `sorting_dict_by_keys()` — sort lists of dictionaries by one or more keys.

  - Handles missing keys safely.
  - Supports ascending and descending order.

### 🛠️ Improved

- Documentation updates and metadata cleanup.
- Organized project files for clarity and consistency.

---

## 🏷️ v0.1.2 — Validation and list sorting

**Date:** 2025-10-18

### ✨ Added

- Introduced `newtutils.utility` module.
- Added `sorting_list()` — removes duplicates and sorts strings before integers.
- Added `validate_input()` — validates input types with safe error feedback.

---

## 🏷️ v0.1.1 — Console utilities

**Date:** 2025-10-17

### ✨ Added

- Start of the *NewtUtils* module.
- Added `newtutils.console` with `error_msg()` for unified error output.
  - Uses **Colorama** for cross-platform colored messages.
- Added base configuration (`pyproject.toml`, module layout).

---

## 🏷️ v0.1.0 — Initial setup

**Date:** 2025-10-16

### 🧩 Initial Setup

- Created project structure (`.gitignore`, `.gitattributes`).
- Initialized the *NewtUtils* repository.
- Prepared the foundation for future modules and documentation.

> 🪄 *The very first commit of the NewtUtils project.*
