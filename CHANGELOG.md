# Changelog for *NewtUtils* (NewtCode)

All notable changes to this project are documented here.
This project follows [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`).

---

## [0.3.0] Function format_value_to_str in module Console

**Date:** 2024-06-04

### Added

- Add `format_value_to_str()` for converting supported values to strings
with special formatting for sets and frozensets.
- Add recursive formatting of set and frozenset values with lexicographically sorted items.
- Add `format_value_to_str()` to the package-level public API.

### Changed

- Change `error_msg()` to format message arguments with `format_value_to_str()`.

---

## [0.2.0] Function error_msg in module Console

**Date:** 2024-06-04

### Added

- Add `error_msg()` for displaying red console error messages
with an optional location and configurable program termination.
- Add `colorama` as a runtime dependency for colored console output.
- Add optional `pytest` and `pytest-cov` dependencies for testing and coverage reporting.
- Add automated CI testing across Python 3.10-3.14.

### Notes

- Install the new runtime dependency with the package; `colorama>=0.4.6` is now required.
- The package metadata name is now normalized to `newtutils`.

---

## [0.1.0] Initial setup

**Date:** 2024-06-03

### Added

- Created initial project structure.
- Initialized the *dev-newtutils* repository.
- Prepared the foundation for future modules and documentation.

> *The very first commit of NewtUtils project.*
