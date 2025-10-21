"""
NewtUtils — A collection of developer utilities and helpers by NewtCode.

This package provides console and data utilities designed for safe,
human-readable feedback and reliable sorting operations.

Created on 2025-10

@author: NewtCode Anna Burova
"""

from .console import error_msg
from .utility import (
    validate_input,
    sorting_list,
    sorting_dict_by_keys,
)

__all__ = [
    "error_msg",
    "validate_input",
    "sorting_list",
    "sorting_dict_by_keys",
]

__author__: str = "NewtCode Anna Burova"
__description__: str = (
    "NewtUtils — A collection of developer utilities and helpers "
    "for console messaging and structured data handling."
)
__version__: str = "0.1.3"
__license__: str = "MIT"
__url__: str = "https://github.com/AnnaBurova/dev-newtutils"
