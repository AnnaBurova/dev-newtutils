"""
Created on 2025-10

@author: NewtCode Anna Burova

Functions:
    def sql_execute_query(
        database: str,
        query: str,
        params: tuple | None = None
        ) -> list[dict] | int | None
    def sql_select_rows(
        database: str,
        query: str,
        params: tuple | None = None
        ) -> list[dict]
    def sql_insert_row(
        database: str,
        table: str,
        data: dict[str, object]
        ) -> int
    def sql_update_rows(
        database: str,
        table: str,
        data: dict[str, object],
        where: str,
        params: tuple | None = None
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
import newtutils.console as NewtCons
import newtutils.files as NewtFiles


def sql_execute_query(
        database: str,
        query: str,
        params: tuple | None = None
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
        params (tuple | None, optional):
            Query parameters (if any).
            Defaults to None.

    Returns:
        list[dict] | int | None:
            For SELECT queries, a list of dictionaries representing rows.
            For INSERT/UPDATE/DELETE, the number of affected rows.
            Returns None if an error occurs.
    """

    if not NewtFiles._check_file_exists(database):
        return None

    try:
        with sqlite3.connect(database) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)

            else:
                cursor.execute(query)

            if query.strip().lower().startswith("select"):
                return [dict(row) for row in cursor.fetchall()]

            else:
                conn.commit()
                return cursor.rowcount

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.sql.execute_query"
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
        data: dict[str, object]
        ) -> int:
    """
    Insert a new row into a given table.

    Args:
        database (str):
            Path to the SQLite database file.
        table (str):
            Table name.
        data (dict[str, object]):
            Column-value pairs to insert.

    Returns:
        int:
            Number of inserted rows.
            Returns 0 if an error occurs or no rows were inserted.
    """

    if not data:
        NewtCons.error_msg(
            "Empty data",
            location="Newt.sql.insert_row",
            stop=False
            )
        return 0

    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

    result = sql_execute_query(database, query, tuple(data.values()))
    return result if isinstance(result, int) else 0


def sql_update_rows(
        database: str,
        table: str,
        data: dict[str, object],
        where: str,
        params: tuple | None = None
        ) -> int:
    """
    Update existing rows in a table based on a WHERE condition.

    Args:
        database (str):
            Path to the SQLite database file.
        table (str):
            Table name.
        data (dict[str, object]):
            Column-value pairs to update.
        where (str):
            WHERE condition
            (e.g., "id = ? AND name = ?").
        params (tuple | None, optional):
            Parameters for the WHERE clause.
            Defaults to None.

    Returns:
        int:
            Number of inserted rows.
            Returns 0 if an error occurs or no rows were inserted.
    """

    if not data:
        NewtCons.error_msg(
            "Empty data",
            location="Newt.sql.update_rows",
            stop=False
            )
        return 0

    set_clause = ", ".join([f"{k} = ?" for k in data])
    values = tuple(data.values()) + (params or ())
    query = f"UPDATE {table} SET {set_clause} WHERE {where}"

    result = sql_execute_query(database, query, values)
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
        # Step 1: run query
        result = sql_select_rows(database, query, params)

        if not result:
            NewtCons.error_msg(
                "Empty result",
                location="Newt.sql.export_sql_query_to_csv",
                stop=False
                )
            return False

        # Step 2: extract headers and rows
        headers = list(result[0].keys())
        rows = [list(row.values()) for row in result]

        # Step 3: save using files.py
        NewtFiles.save_csv_to_file(csv_file, [headers] + rows, delimiter=delimiter)

        return True

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.sql.export_sql_query_to_csv",
            stop=False
            )
        return False
