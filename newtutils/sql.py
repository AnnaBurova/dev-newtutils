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
    Safely close a SQLite database connection and release all file handles.

    This helper opens and closes the given SQLite database file to ensure that all pending transactions are committed
    and the operating system releases the file lock completely.

    Args:
        database (str):
            Path to the SQLite database file.

    Returns:
        bool:
            True if the database was successfully closed and released,
            otherwise False.
    """

    if not NewtFiles._check_file_exists(database):
        return True

    try:
        conn = sqlite3.connect(database)
        conn.commit()
        conn.close()

        # Force Python's garbage collector to immediately destroy any remaining SQLite connection or cursor objects that may still hold a file handle.
        # This ensures that the database file is fully released by the operating system before deletion.
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
    Execute a SQL query (SELECT, INSERT, UPDATE, or DELETE).

    Automatically detects query type based on its first keyword.
    SELECT queries return a list of dictionaries.
    Other queries return the number of affected rows.

    Args:
        database (str):
            Path to the SQLite database file.
        query (str):
            SQL query to execute.
        params (tuple | list[tuple] | None, optional):
            Query parameters (single or multiple sets).
            Use a list of tuples for batch operations (executemany).
            Defaults to None.

    Returns:
        list[dict] | int | None:
            For SELECT queries - a list of dictionaries representing rows.
            For INSERT/UPDATE/DELETE - the number of affected rows.
            Returns None if an error occurs.
    """

    # Ensure directory exists
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

            else:
                # DML/DLL
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
    Run a SELECT query and return all matching rows as a list of dictionaries.

    Args:
        database (str):
            Path to the SQLite database file.
        query (str):
            SELECT query string.
        params (tuple | None, optional):
            Query parameters. Defaults to None.

    Returns:
        list[dict]:
            A list of rows as dictionaries, or an empty list if no results or errors.
    """

    result = sql_execute_query(database, query, params)
    return result if isinstance(result, list) else []


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
