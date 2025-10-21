"""
NewtUtils — A collection of developer utilities and helpers by NewtCode.

This package provides console and data utilities designed for safe,
human-readable feedback and reliable sorting operations.

Created on 2025-10

@author: NewtCode Anna Burova
"""

# === Imports from modules ===
from .console import error_msg
from .utility import (
    validate_input,
    sorting_list,
    sorting_dict_by_keys,
)
from .files import (
    read_text_from_file, save_text_to_file,
    read_json_from_file, save_json_to_file,
    read_csv_from_file, save_csv_to_file,
)

__all__ = [
    # Console
    "error_msg",
    # Utility
    "validate_input",
    "sorting_list",
    "sorting_dict_by_keys",
    # Files
    "read_text_from_file", "save_text_to_file",
    "read_json_from_file", "save_json_to_file",
    "read_csv_from_file", "save_csv_to_file",
]

__author__: str = "NewtCode Anna Burova"
__description__: str = (
    "NewtUtils — A collection of developer utilities and helpers "
    "for console messaging and structured data handling."
)
__version__: str = "0.1.4"
__license__: str = "MIT"
__url__: str = "https://github.com/AnnaBurova/dev-newtutils"
