# About NewtUtils — Developer Utilities (NewtCode)

[![Version](https://img.shields.io/badge/version-v0.3.0-orange.svg)](https://github.com/AnnaBurova/dev-newtutils)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Python](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)

A collection of utility functions for common programming tasks.

---

## Overview

**NewtUtils** is designed as a small but extendable utility library to simplify common scripting and development tasks — such as structured console output, safe type validation, file management, SQL access, and API communication.

The project follows clean, documented, and predictable function behavior for maintainable and testable code. All functions include comprehensive type hints and Google-style docstrings for better IDE support and code clarity.

---

## Features

| Path | Purpose |
|------|---------|
| `Console tools` | Console input/output operations, including error messages, input validation, and location checking. |
| `Utility functions` | General purpose utilities, including dictionary key validation, value counting, sorting operations, and input selection. |
| `File operations` | File system operations, including directory and file creation, reading, writing, and deletion |
| `SQL operations` | Database access, including connection management, query execution, and transaction handling. |
| `Network operations` | Network request handling, including HTTP request sending, response handling, and error management. |
| `Testing` | Automated and manual test scripts, including test output logs and automated testing with pytest. |

---

## Requirements

- Python 3.10
- Python 3.11
- Python 3.12
- Python 3.13
- Python 3.14
- Full type hint support with `from __future__ import annotations`

---

## Dependencies

This project uses the following third-party libraries:

- [NewtUtils](https://github.com/AnnaBurova/dev-newtutils)
- [Colorama](https://github.com/tartley/colorama) (BSD 3-Clause License)
- [PyTest](https://github.com/pytest-dev/pytest) (MIT License)
- [Requests](https://github.com/psf/requests) (Apache License 2.0)

All other modules rely only on the Python Standard Library.

For more details on dependencies, see the [LICENSE](LICENSE) file.

---

## Getting Started

- [Installation Guide](INSTALLATION.md) — Instructions for installing and setting up the project for development.

---

## Development Notes

- [TODO list](TODO) — Planned improvements and features for this repository.
- [CHANGELOG](CHANGELOG.md) — Version history and release notes.
- [CONTRIBUTING](CONTRIBUTING.md) — Guidelines for contributing to the project.
- [Testing Guide](tests/README.md) — Instructions for running tests and contributing test cases.

---

## License

- [AUTHORS](AUTHORS) — Credits to contributors and external resources.
- [COPYRIGHT](COPYRIGHT) — Copyright information for original and included materials.
- [LICENSE](LICENSE) — The license governing repository use.

---

## Development Workflow

1. Fork and clone the repository.
2. Read [CHANGELOG.md](CHANGELOG.md) for recent changes.
3. Review [CONTRIBUTING.md](CONTRIBUTING.md) before opening PRs.
4. Explore `tests/` for usage examples.
5. Create feature branch: `git checkout -b feature/short-description`.
6. Make changes in `newtutils/` or `tests/`.
7. Run tests: `pytest tests/`.
8. Commit: Follow [Conventional Commits](https://www.conventionalcommits.org).
9. Push and open PR.
