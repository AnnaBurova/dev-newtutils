# dev-newtutils

![CI](https://github.com/AnnaBurova/dev-newtutils/actions/workflows/ci.yml/badge.svg?branch=main)
[![Python](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.6.2-orange.svg)](https://github.com/AnnaBurova/dev-newtutils)

NewtUtils is a collection of utility functions for common programming tasks.

## Overview

**NewtUtils** is designed as a small but extendable utility library
to simplify common scripting and development tasks:
- structured console output
- safe type validation
- file management
- SQL access
- API communication

The project follows clean, documented, and predictable function behavior
for maintainable and testable code.
All functions include comprehensive type hints and Google-style docstrings
for better IDE support and code clarity.

## Features

| Path | Purpose |
|------|---------|
| `Console tools` | Console input/output operations, including error messages, input validation, and location checking. |
| `Utility functions` | General purpose utilities, including dictionary key validation, value counting, sorting operations, and input selection. |
| `File operations` | File system operations, including directory and file creation, reading, writing, and deletion. |
| `SQL operations` | Database access, including connection management, query execution, and transaction handling. |
| `Network operations` | Network request handling, including HTTP request sending, response handling, and error management. |

## Requirements

- Python 3.14
- Python 3.13
- Python 3.12
- Python 3.11
- Python 3.10
- Full type hint support with `from __future__ import annotations`

## Dependencies

This project uses the following third-party libraries:

- [NewtUtils](https://github.com/AnnaBurova/dev-newtutils)
- [Colorama](https://github.com/tartley/colorama) (BSD 3-Clause License)
- [PyTest](https://github.com/pytest-dev/pytest) (MIT License)
- [PyTest-Cov](https://github.com/pytest-dev/pytest-cov) (MIT License)

All other modules rely only on the Python Standard Library.

For more details on dependencies, see the [LICENSE](LICENSE) file.

## Getting Started

- [Installation Guide](INSTALLATION.md) — Instructions for installing and setting up the project for development.

## Development Notes

- [TODO list](TODO) — Planned improvements and features for this repository.
- [CHANGELOG](CHANGELOG.md) — Version history and release notes.
- [CONTRIBUTING](CONTRIBUTING.md) — Guidelines for contributing to the project.
- [Testing Guide](tests/TESTING.md) — Instructions for running tests and contributing test cases.

## License

- [AUTHORS](AUTHORS) — Credits to contributors and external resources.
- [COPYRIGHT](COPYRIGHT) — Copyright information for original and included materials.
- [LICENSE](LICENSE) — The license governing repository use.
