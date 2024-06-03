"""
Created on 2024-06

@author: NewtCode Anna Burova

NewtUtils is a collection of utility functions for common programming tasks by NewtCode.

Modules:
    console: Console input/output operations
"""

# ===== Imports from modules ========================================== ======= =================== ====================

# ----- Console ------------------------------------------------------- ------- ------------------- --------------------
from .console import (
    error_msg,
)

# ===== Metadata ====================================================== ======= =================== ====================

__all__ = [
    # ----- Console --------------------------------------------------- ------- ------------------- --------------------
    "error_msg",
]

# ===== Project ======================================================= ======= =================== ====================

__version__ = "0.1.0"
__author__ = "Anna Burova <burova.anna+git@gmail.com>"
__description__ = "NewtUtils is a collection of utility functions for common programming tasks."
__license__ = "MIT"
__url__ = "https://github.com/AnnaBurova/dev-newtutils"
