"""
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

import sqlite3
import gc
import newtutils.console as NewtCons
import newtutils.utility as NewtUtil
import newtutils.files as NewtFiles


def db_delayed_close(
        database: str
        ) -> bool:
    """
    Safely close a SQLite database and release all file handles.

    Opens and closes the target database file to ensure that all
    pending transactions are committed and the file lock is released.

    Args:
        database (str):
            Path to the SQLite database file.

    Returns:
        out (bool):
            True if the database was successfully closed and released,
            otherwise False.
    """

    if not NewtFiles._check_file_exists(database):
        return True

    try:
        conn = sqlite3.connect(database)
        conn.commit()
        conn.close()

        # Force Python's garbage collector to immediately destroy
        # any remaining SQLite connection or cursor objects
        # that may still hold a file handle.
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

    NewtFiles._ensure_dir_exists(database)
    result = None

    try:
        with sqlite3.connect(database) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            if params:
                # EXECUTEMANY - list of tuples
                if isinstance(params, list):
                    if NewtCons.validate_input(params[0], tuple):
                        cursor.executemany(query, params)
                    else:
                        raise TypeError("Invalid parameter format for executemany()")
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
    if NewtCons.validate_input(result, list, stop=False):
        return result
    return []


def sql_insert_row(
        database: str,
        table: str,
        data: dict[str, object] | list[dict[str, object]]
        ) -> int:
    """
    Insert one or multiple rows into a given table.

    Args:
        database (str):
            Path to the SQLite database file.
        table (str):
            Table name.
        data (dict[str, object] | list[dict[str, object]]):
            A single dictionary
            or a list of dictionaries
            containing column-value pairs to insert.

    Returns:
        int:
            Number of inserted rows.
            Returns 0 if an error occurs or no rows were inserted.
    """

    if not data:
        NewtCons.error_msg(
            "Empty data",
            location="Newt.sql.sql_insert_row",
            stop=False
            )
        return 0

    # Normalize input to list[dict]
    if isinstance(data, dict):
        data = [data]

    # Build SQL template
    columns = ", ".join(data[0].keys())
    placeholders = ", ".join(["?"] * len(data[0]))
    params = [tuple(row.values()) for row in data]

    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

    if len(params) == 1:
        result = sql_execute_query(database, query, params[0])
    else:
        result = sql_execute_query(database, query, params)

    return result if isinstance(result, int) else 0


def sql_update_rows(
        database: str,
        table: str,
        set_data: dict[str, object],
        where_condition: str,
        where_params: tuple | None = None
        ) -> int:
    """
    Update existing rows in a table based on a WHERE condition.

    Args:
        database (str):
            Path to the SQLite database file.
        table (str):
            Table name.
        set_data (dict[str, object]):
            Column-value pairs to update.
        where_condition (str):
            WHERE condition
            (e.g., "id = ? AND name = ?").
        where_params (tuple | None, optional):
            Parameters for the WHERE clause.
            Defaults to None.

    Returns:
        int:
            Number of inserted rows.
            Returns 0 if an error occurs or no rows were inserted.
    """

    if not set_data:
        NewtCons.error_msg(
            "Empty data",
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
    Execute a SQL SELECT query and export the result to a CSV file.

    Args:
        database (str):
            Path to the SQLite database file.
        query (str):
            SQL SELECT query to execute.
        csv_file (str):
            Path to the CSV file where the result will be saved.
        params (tuple | None, optional):
            Query parameters. Defaults to None.
        delimiter (str, optional):
            CSV delimiter, defaults to ';'.

    Returns:
        bool:
            True if export succeeded, otherwise False.
    """

    try:
        # Step 1: run select query
        result = sql_select_rows(database, query, params)

        if not result:
            NewtCons.error_msg(
                "Empty result",
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
