"""
Updated on 2025-11
Created on 2025-10

@author: NewtCode Anna Burova

Functions:
    def db_delayed_close(
        database: str
        ) -> bool
    def sql_execute_query(
        database: str,
        query: str,
        params: tuple | list[tuple] | None = None
        ) -> list[dict] | int | None
    def sql_select_rows(
        database: str,
        query: str,
        params: tuple | None = None
        ) -> list[dict]
    def sql_insert_row(
        database: str,
        table: str,
        data: dict[str, object] | list[dict[str, object]]
        ) -> int
    def sql_update_rows(
        database: str,
        table: str,
        set_data: dict[str, object],
        where_condition: str,
        where_params: tuple | None = None
        ) -> int
    def export_sql_query_to_csv(
        database: str,
        query: str,
        csv_file: str,
        params: tuple | None = None,
        delimiter: str = ";"
        ) -> bool
"""

from __future__ import annotations

import sqlite3
import gc
import newtutils.console as NewtCons
import newtutils.files as NewtFiles


def db_delayed_close(
        database: str
        ) -> bool:
    """
    Safely close a SQLite database and release all file handles.

    Performs strict input validation, checks that the target path exists,
    then triggers Python's garbage collector to finalize any remaining
    SQLite connection or cursor objects that may still hold a file handle.

    Args:
        database (str):
            Path to the SQLite database file.

    Returns:
        out (bool):
            True if the input is valid and
            the database path either does not exist or appears to be released;
            False if validation fails.
    """

    if not NewtFiles._check_file_exists(database):
        # Nothing to release; treat as success because there is no existing file.
        return True

    try:
        # Force Python's garbage collector to finalize any remaining
        # SQLite-related objects (connections, cursors, etc.) that may
        # still hold a file handle to the database file.
        gc.collect()

        return True

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.sql.db_delayed_close",
            stop=False
        )
        return False


def sql_execute_query(
        database: str,
        query: str,
        params: tuple | list[tuple] | None = None
        ) -> list[dict] | int | None:
    """
    Execute a SQL query and return its result or affected row count.

    Automatically detects query type (SELECT, INSERT, UPDATE, DELETE)
    and executes it accordingly. SELECT queries return data as
    a list of dictionaries, while others return the affected row count.

    Args:
        database (str):
            Path to the SQLite database file.
        query (str):
            SQL query to execute.
        params (tuple | list[tuple] | None):
            Query parameters.
            Use a list of tuples for batch operations (executemany).
            Defaults to None.

    Returns:
        out (list[dict] | int | None):
            Query result as list of dicts for SELECT,
            number of affected rows for DML,
            or None if an error occurs.
    """

    if not NewtCons.validate_input(database, str, stop=False):
        return None
    if not NewtCons.validate_input(query, str, stop=False):
        return None
    if params:
        if not NewtCons.validate_input(params, (list, tuple), stop=False):
            return None

    normalized_query = query.strip()

    if not normalized_query:
        NewtCons.error_msg(
            "SQL query is empty after stripping whitespace",
            location="Newt.sql.sql_execute_query",
            stop=False,
        )
        return None

    # Very basic multiple-statement protection
    # Reject queries with more than one non-empty segment separated by ';'
    parts_query = [p.strip() for p in normalized_query.split(";") if p.strip()]
    if len(parts_query) != 1:
        NewtCons.error_msg(
            "SQL query must contain exactly one statement",
            location="Newt.sql.sql_execute_query",
            stop=False,
        )
        return None

    lowered_query = normalized_query.lower()
    dangerous_tokens = (
        " drop ",
        " truncate ",
        " alter ",
        ";--",
        "/*",
        "*/",
        " xp_",
    )
    for token in dangerous_tokens:
        if token in f" {lowered_query} ":
            NewtCons.error_msg(
                f"SQL query contains potentially dangerous token: {token.strip()}",
                location="Newt.sql.sql_execute_query",
                stop=False,
            )
            return None

    # EXECUTEMANY - list of tuples
    if isinstance(params, list):
        if not all(NewtCons.validate_input(p, tuple, stop=False) for p in params):
            NewtCons.error_msg(
                "All items in 'params' list must be tuples for executemany().",
                f"params: {params}",
                location="Newt.sql.sql_execute_query"
            )
            return None

    NewtFiles._ensure_dir_exists(database)
    result = None

    try:
        with sqlite3.connect(database) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            if params:
                # EXECUTEMANY - list of tuples
                if isinstance(params, list):
                    cursor.executemany(query, params)

                # Normal single execution
                else:
                    cursor.execute(query, params)
            else:
                cursor.execute(query)

            if query.strip().lower().startswith("select"):
                result = [dict(row) for row in cursor.fetchall()]

            # DML/DLL
            else:
                conn.commit()
                result = cursor.rowcount

        return result

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.sql.sql_execute_query"
        )
        return None


def sql_select_rows(
        database: str,
        query: str,
        params: tuple | None = None
        ) -> list[dict]:
    """
    Execute a SELECT query and return rows as a list of dictionaries.

    Args:
        database (str):
            Path to the SQLite database file.
        query (str):
            SQL SELECT query to execute.
        params (tuple | None):
            Query parameters. Defaults to None.

    Returns:
        out (list[dict]):
            List of rows as dictionaries,
            or an empty list if no data or errors.
    """

    result = sql_execute_query(database, query, params)
    if isinstance(result, list):
        return result

    if not NewtCons.validate_input(result, list, stop=False):
        print(result)

    return []


def sql_insert_row(
        database: str,
        table: str,
        data: dict[str, object] | list[dict[str, object]]
        ) -> int:
    """
    Insert one or more rows into a database table.

    Args:
        database (str):
            Path to the SQLite database file.
        table (str):
            Name of the target table.
        data (dict[str, object] | list[dict[str, object]]):
            One dictionary or a list of dictionaries
            containing column-value pairs.

    Returns:
        out (int):
            Number of inserted rows, or 0 on failure.
    """

    if not NewtCons.validate_input(database, str, stop=False):
        return 0
    if not NewtCons.validate_input(table, str, stop=False):
        return 0

    if not data:
        NewtCons.error_msg(
            f"Empty data: {data}",
            location="Newt.sql.sql_insert_row",
            stop=False
        )
        return 0

    # Normalize input to list[dict]
    if isinstance(data, dict):
        data = [data]

    if not NewtCons.validate_input(data, list, stop=False):
        NewtCons.error_msg(
            "Data must be dict or list[dict]",
            f"Data: {data}",
            location="Newt.sql.sql_insert_row",
            stop=False
        )
        return 0

    # Build SQL template
    columns = ", ".join(data[0].keys())
    placeholders = ", ".join(["?"] * len(data[0]))
    params = [tuple(row.values()) for row in data]

    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

    if len(params) == 1:
        result = sql_execute_query(database, query, params[0])
    else:
        result = sql_execute_query(database, query, params)

    if isinstance(result, int):
        return result

    if not NewtCons.validate_input(result, int, stop=False):
        print(result)

    return 0


def sql_update_rows(
        database: str,
        table: str,
        set_data: dict[str, object],
        where_condition: str,
        where_params: tuple | None = None
        ) -> int:
    """
    Update rows in a database table using a WHERE condition.

    Args:
        database (str):
            Path to the SQLite database file.
        table (str):
            Table name.
        set_data (dict[str, object]):
            Column-value pairs to update.
        where_condition (str):
            SQL WHERE clause:
            id = ? AND name = ?
        where_params (tuple | None):
            Parameters for the WHERE clause.
            Defaults to None.

    Returns:
        out (int):
            Number of updated rows,
            or 0 on failure.
    """

    if not NewtCons.validate_input(database, str, stop=False):
        return 0
    if not NewtCons.validate_input(table, str, stop=False):
        return 0
    if not NewtCons.validate_input(where_condition, str, stop=False):
        return 0

    if not set_data:
        NewtCons.error_msg(
            f"Empty data: {set_data}",
            location="Newt.sql.sql_update_rows",
            stop=False
        )
        return 0

    set_clause = ", ".join([f"{k} = ?" for k in set_data])
    params = tuple(set_data.values()) + (where_params or ())
    query = f"UPDATE {table} SET {set_clause} WHERE {where_condition}"

    result = sql_execute_query(database, query, params)
    return result if isinstance(result, int) else 0


def export_sql_query_to_csv(
        database: str,
        query: str,
        csv_file: str,
        params: tuple | None = None,
        delimiter: str = ";"
        ) -> bool:
    """
    Run a SQL SELECT query and export the result to a CSV file.

    Args:
        database (str):
            Path to the SQLite database file.
        query (str):
            SQL SELECT query to execute.
        csv_file (str):
            Path to the CSV output file.
        params (tuple | None):
            Query parameters. Defaults to None.
        delimiter (str):
            CSV delimiter character.
            Defaults to `;`.

    Returns:
        out (bool):
            True if export succeeded,
            otherwise False.
    """

    if not NewtCons.validate_input(database, str, stop=False):
        return False
    if not NewtCons.validate_input(query, str, stop=False):
        return False
    if not NewtCons.validate_input(csv_file, str, stop=False):
        return False
    if not NewtCons.validate_input(delimiter, str, stop=False):
        return False

    try:
        # Step 1: run select query
        result = sql_select_rows(database, query, params)

        if not result:
            NewtCons.error_msg(
                f"Empty result: {result}",
                location="Newt.sql.export_sql_query_to_csv",
                stop=False
            )
            return False

        # Step 2: extract headers and rows for CSV
        headers = list(result[0].keys())
        rows = [list(row.values()) for row in result]

        # Step 3: save using newtutils/files.py
        NewtFiles.save_csv_to_file(csv_file, [headers] + rows, delimiter=delimiter)

        return True

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.sql.export_sql_query_to_csv",
            stop=False
        )
        return False
