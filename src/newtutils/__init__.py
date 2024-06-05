"""
Created on 2024-06

@author: NewtCode Anna Burova

NewtUtils is a collection of utility functions for common programming tasks by NewtCode.

Modules:
    console: Console input/output operations
    utility: General purpose utilities
    files: File system operations
    sql: Database operations
    network: Network request handling
"""

# ===== Imports from modules ========================================== ======= =================== ====================

# ----- Console ------------------------------------------------------- ------- ------------------- --------------------
from .console import (
    format_value_to_str,
    error_msg,
    validate_value,
)

# ===== Metadata ====================================================== ======= =================== ====================

__all__ = [
    # ----- Console --------------------------------------------------- ------- ------------------- --------------------
    "format_value_to_str",
    "error_msg",
    "validate_value",
]

# ===== Project ======================================================= ======= =================== ====================

__version__ = "0.3.0"
__author__ = "Anna Burova <burova.anna+git@gmail.com>"
__description__ = "NewtUtils is a collection of utility functions for common programming tasks."
__license__ = "MIT"
__url__ = "https://github.com/AnnaBurova/dev-newtutils"
