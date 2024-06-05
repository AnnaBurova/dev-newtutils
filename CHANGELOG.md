# Changelog for *NewtUtils* (NewtCode)

All notable changes to this project are documented here.
This project follows [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`).

---

## [0.4.0] Function validate_value in module Console

**Date:** 2024-06-06

### Added

- Add `validate_value()` to the console and package-level APIs
for exact type validation against a type or tuple of allowed types.
- Add optional `check_non_empty` validation to reject `False`,
numeric zeros, blank strings, empty built-in containers,
and `None` when the expected type is `type(None)`.
- Add validation error reporting with location context and configurable termination;
return `False` on failure when `stop=False`.

### Changed

- Change `error_msg()` argument type hints from `str` to `object`
to reflect support for non-string messages.

### Notes

- `validate_value()` uses exact type matching: subclasses are not accepted automatically,
and `bool` is distinct from `int`.
- Validation failures raise `SystemExit(1)` by default;
use `stop=False` to report errors without terminating execution.

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
