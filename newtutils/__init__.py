"""
Updated on 2026-02
Created on 2025-10

@author: NewtCode Anna Burova

NewtUtils - A collection of utility functions for common programming tasks by NewtCode.

Modules:
    console: Console input/output operations
    utility: General purpose utilities
    files: File system operations
    sql: Database operations
    network: Network request handling
"""

# === Imports from modules ===

# Console
from .console import (
    error_msg,
    validate_input,
    check_location,
)

# Utility
from .utility import (
    check_dict_keys,
    count_similar_values,
    sorting_list,
    sorting_dict_by_keys,
    select_from_input,
)

# Files
from .files import (
    ensure_dir_exists, check_file_exists,
    choose_file_from_folder,
    read_text_from_file, save_text_to_file,
    convert_str_to_json,
    read_json_from_file, save_json_to_file,
    read_csv_from_file, save_csv_to_file,
    setup_logging, cleanup_logging,
)

# SQL
from .sql import (
    db_delayed_close,
    sql_execute_query,
    sql_select_rows,
    sql_insert_row,
    sql_update_rows,
    export_sql_query_to_csv,
)

# Network
from .network import (
    fetch_data_from_url,
    download_file_from_url,
)

# === Metadata ===

__all__ = [
    # Console ----------
    "error_msg",
    "validate_input",
    "check_location",
    # Utility ----------
    "check_dict_keys",
    "count_similar_values",
    "sorting_list",
    "sorting_dict_by_keys",
    "select_from_input",
    # Files ----------
    "ensure_dir_exists", "check_file_exists",
    "choose_file_from_folder",
    "read_text_from_file", "save_text_to_file",
    "convert_str_to_json",
    "read_json_from_file", "save_json_to_file",
    "read_csv_from_file", "save_csv_to_file",
    "setup_logging", "cleanup_logging",
    # SQL ----------
    "db_delayed_close",
    "sql_execute_query",
    "sql_select_rows",
    "sql_insert_row",
    "sql_update_rows",
    "export_sql_query_to_csv",
    # Network ----------
    "fetch_data_from_url",
    "download_file_from_url",
]

__version__ = "1.1.0"
__author__ = "NewtCode Anna Burova"
__description__ = (
    "NewtUtils — A modular Python toolkit providing reusable utilities "
    "for console messaging, input validation, sorting, file I/O, SQL, and network operations."
)
__license__ = "MIT"
__url__ = "https://github.com/AnnaBurova/dev-newtutils"
