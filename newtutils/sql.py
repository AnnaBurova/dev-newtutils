"""
Updated on 2026-05
Created on 2025-10

@author: NewtCode Anna Burova

Functions:
    def db_delayed_close(
        database: str,
        print_log: bool = True
        ) -> bool
    def query_execute(
        database: str,
        query: str,
        params: tuple | list[tuple] | None = None
        ) -> list[dict] | int | None
    def query_select(
        database: str,
        table: str,
        columns: str = "*",
        query_str: str = "",
        params: tuple | None = None
        ) -> list[dict]
    def query_insert(
        database: str,
        table: str,
        insert_data: dict[str, object] | list[dict[str, object]]
        ) -> int
    def query_update(
        database: str,
        table: str,
        set_data: dict[str, object],
        where_condition: str,
        where_params: tuple | None = None
        ) -> int
    def export_sql_query_to_csv(
        database: str,
        csv_file: str,
        table: str,
        columns: str = "*",
        query_str: str = "",
        params: tuple | None = None,
        delimiter: str = ";",
        obscure_list: list = [],
        print_log: bool = True
        ) -> bool
"""

from __future__ import annotations

import gc
import sqlite3

import newtutils.console as NewtCons
import newtutils.utility as NewtUtil
import newtutils.files as NewtFiles


def db_delayed_close(
        database: str,
        print_log: bool = True
        ) -> bool:
    """ ## Trigger garbage collection to release SQLite file handles.

    Opens and closes the target database file to ensure that all
    pending transactions are committed and the file lock is released.

    Performs strict input validation, checks that the target path exists,
    then triggers Python's garbage collector to finalize any remaining
    SQLite connection or cursor objects that may still hold a file handle.
    Note: gc.collect() does not guarantee immediate file release if other
    references to connections/cursors exist.

    Args:
        database (str):
            Path to the SQLite database file.

    Returns:
        out (bool):
            True if the input is valid and garbage collection succeeds;<br>
            False if validation fails or exception occurs.
    """

    if not NewtFiles.check_file_exists(database, stop=False, print_log=print_log):
        # Nothing to release; treat as success because there is no existing file.
        return True

    try:
        # Force Python's garbage collector to finalize any remaining
        # SQLite-related objects (connections, cursors, etc.) that may
        # still hold a file handle to the database file.
        gc.collect()

        # conn = sqlite3.connect(database)
        # conn.commit()
        # conn.close()

        # gc.collect()

        return True

    except Exception as e:  # pragma: no cover
        NewtCons.error_msg(
            f"Found Error Msg: (found? write test!)",  # TODO
            f"Exception: {e}",
            location="Newt.sql.db_delayed_close : Exception"
        )

    return False  # pragma: no cover


def query_execute(
        database: str,
        query: str,
        params: tuple | list[tuple] | None = None
        ) -> list[dict] | int | None:
    """ ## Execute a SQL query and return its result or affected row count.

    Automatically detects query type (SELECT, INSERT, UPDATE, DELETE)
    and executes it accordingly. SELECT queries return data as
    a list of dictionaries, while others return the affected row count.

    Args:
        database (str):
            Path to the SQLite database file.
        query (str):
            SQL query to execute.
        params (tuple | list[tuple] | None):
            Query parameters.<br>
            Use a list of tuples for batch operations (executemany).<br>
            Defaults to None.

    Returns:
        out (list[dict] | int | None):
            Query result as list of dicts for SELECT,<br>
            number of affected rows for DML,<br>
            or None if an error occurs.
    """

    NewtCons.validate_type(
        database, str, check_non_empty=True,
        location="Newt.sql.query_execute : database"
    )

    NewtCons.validate_type(
        query, str, check_non_empty=True,
        location="Newt.sql.query_execute : query"
    )

    if params is not None:
        NewtCons.validate_type(
            params, (list, tuple), check_non_empty=True,
            location="Newt.sql.query_execute : params"
        )

        # EXECUTEMANY - list of tuples
        if isinstance(params, list):
            if not all(NewtCons.validate_type(p, tuple, stop=False) for p in params):
                NewtCons.error_msg(
                    "All items in 'params' list must be tuples for executemany().",
                    f"params: {params}",
                    location="Newt.sql.query_execute : executemany"
                )

    normalized_query = query.strip()

    # Very basic multiple-statement protection
    # Reject queries with more than one non-empty segment separated by ';'
    parts_query = [p.strip() for p in normalized_query.split(";") if p.strip()]
    if len(parts_query) == 1:
        normalized_query = parts_query[0]
    else:
        NewtCons.error_msg(
            "SQL query must contain exactly one statement",
            location="Newt.sql.query_execute : parts_query"
        )

    lowered_query = normalized_query.lower()
    dangerous_tokens = (
        " drop ",
        " truncate ",
        " alter ",
        " exec ",
        " execute ",
        " grant ",
        " revoke ",
        " union ",
        ";--",
        "--",
        "/*",
        "*/",
        " xp_",
        " sp_",
        " char(",
        " concat(",
        " 0x",
    )
    for token in dangerous_tokens:
        if token in f" {lowered_query} ":
            NewtCons.error_msg(
                f"SQL query contains potentially dangerous token: {token.strip()}",
                location="Newt.sql.query_execute : dangerous_tokens"
            )

    NewtFiles.ensure_dir_exists(database)

    result = None

    try:
        with sqlite3.connect(database) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            if params:
                # EXECUTEMANY - list of tuples
                if isinstance(params, list):
                    cursor.executemany(query, params)

                # Normal single execution with params as tuple
                else:
                    cursor.execute(query, params)

            # No parameters
            else:
                cursor.execute(query)

            # DQL - SELECT
            if query.strip().lower().startswith("select"):
                result = [dict(row) for row in cursor.fetchall()]

            # DML - INSERT, UPDATE, DELETE returns affected rows 0 or more
            # DDL - CREATE, DROP, ALTER returns -1
            else:
                conn.commit()
                result = cursor.rowcount
        conn.close()

    except sqlite3.OperationalError as e:
        conn.close()
        if "syntax" in str(e).lower():
            NewtCons.error_msg(
                f"Syntax error: {e}",
                location="Newt.sql.query_execute : OperationalError in Syntax",
                stop=False
            )

        else:
            NewtCons.error_msg(  # pragma: no cover
                f"Found Error Msg: (found? write test!)",  # TODO
                f"DB error: {e}",
                location="Newt.sql.query_execute : OperationalError in DB",
                stop=False
            )

    except Exception as e:  # pragma: no cover
        conn.close()
        NewtCons.error_msg(
            f"Found Error Msg: (found? write test!)",  # TODO
            f"Exception: {e}",
            location="Newt.sql.query_execute : Exception",
            stop=False
        )

    return result


def query_select(
        database: str,
        table: str,
        columns: str = "*",
        query_str: str = "",
        params: tuple | None = None
        ) -> list[dict]:
    """ ## Build and execute a SELECT query, returning rows as a list of dictionaries.

    Constructs a SQL SELECT statement from the given table, columns, and optional
    query string, then delegates execution to `query_execute`. Returns an empty
    list if the result is invalid or no rows are found.

    Args:
        database (str):
            Path to the SQLite database file.
        table (str):
            Name of the table to query.
        columns (str):
            Comma-separated column names to select.<br>
            Defaults to `"*"` (all columns).<br>
            Example: `"id, name, email"`
        query_str (str):
            Optional SQL clause appended after the table name (e.g. WHERE, ORDER BY).<br>
            Defaults to empty string.<br>
            Example: `"WHERE id = ?" or "ORDER BY name ASC"`
        params (tuple | None):
            Positional parameters bound to `?` placeholders in `query_str`.<br>
            Defaults to None.<br>
            Example: `(1,)` or `(1, "Alice")`

    Returns:
        out (list[dict]):
            List of rows as dictionaries, where keys are column names.<br>
            Returns an empty list if no data is found or an error occurs.
    """

    NewtCons.validate_type(
        columns, str, check_non_empty=True,
        location="Newt.sql.query_select : columns"
    )

    NewtCons.validate_type(
        table, str, check_non_empty=True,
        location="Newt.sql.query_select : table"
    )

    NewtCons.validate_type(
        query_str, str,
        location="Newt.sql.query_select : query_str"
    )

    query = f"SELECT {columns} FROM {table} {query_str};"

    result = query_execute(database, query, params)

    if NewtCons.validate_type(
        result, list,
        location="Newt.sql.query_select : result"
    ):
        if isinstance(result, list):
            return result

    NewtCons.error_msg(  # pragma: no cover
        f"Found Error Msg: (found? write test!)",  # TODO
        location="Newt.sql.query_select : error_msg",
        stop=False
    )

    return []  # pragma: no cover


def query_insert(
        database: str,
        table: str,
        insert_data: dict[str, object] | list[dict[str, object]]
        ) -> int:
    """ ## Insert one or more rows into a database table.

    Args:
        database (str):
            Path to the SQLite database file.
        table (str):
            Name of the target table.
        insert_data (dict[str, object] | list[dict[str, object]]):
            One dictionary or a list of dictionaries containing column-value pairs:
            [{"id": 1, "name": "Alice", "age": 30}]

    Returns:
        out (int):
            Number of inserted rows,<br>
            or 0 on failure.
    """

    NewtCons.validate_type(
        table, str, check_non_empty=True,
        location="Newt.sql.query_insert : table"
    )

    if not NewtCons.validate_type(
        insert_data, (dict, list), check_non_empty=True, stop=False,
        location="Newt.sql.query_insert : insert_data"
    ):
        return 0

    # Normalize input to list[dict]
    if isinstance(insert_data, dict):
        insert_data = [insert_data]

    NewtCons.validate_type(
        insert_data, list,
        location="Newt.sql.query_insert : insert_data"
    )

    NewtCons.validate_type(
        insert_data[0], dict, check_non_empty=True,
        location="Newt.sql.query_insert : insert_data"
    )

    # Validate that all dictionaries have the same keys and length
    expected_keys = set(insert_data[0].keys())

    keys_ok = True
    for data_row in insert_data:
        if not NewtCons.validate_type(
            data_row, dict, check_non_empty=True, stop=False,
            location="Newt.sql.query_insert : data_row"
        ):
            keys_ok = False
            continue

        if not NewtUtil.check_dict_keys(
            data_row, expected_keys,
            location="Newt.sql.query_insert : data_row",
            stop=False
        ):
            keys_ok = False

    if keys_ok is False:
        NewtCons.error_msg(
            "All dictionaries must have identical keys and same length",
            f"Expected keys: {', '.join(sorted(expected_keys))}",
            location="Newt.sql.query_insert : expected_keys"
        )

    # Build SQL template
    columns = ", ".join(insert_data[0].keys())
    placeholders = ", ".join(["?"] * len(insert_data[0]))
    params = [tuple(row.values()) for row in insert_data]

    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders});"

    if len(params) == 1:
        result = query_execute(database, query, params[0])
    else:
        result = query_execute(database, query, params)

    if NewtCons.validate_type(
        result, int,
        location="Newt.sql.query_insert : result"
    ):
        if isinstance(result, int):
            return result

    NewtCons.error_msg(  # pragma: no cover
        f"Found Error Msg: (found? write test!)",  # TODO
        location="Newt.sql.query_insert : error_msg",
        stop=False
    )

    # Default return value if no rows are inserted
    return 0  # pragma: no cover


def query_update(
        database: str,
        table: str,
        set_data: dict[str, object],
        where_condition: str,
        where_params: tuple | None = None
        ) -> int:
    """ ## Update rows in a database table using a WHERE condition.

    Args:
        database (str):
            Path to the SQLite database file.
        table (str):
            Table name.
        set_data (dict[str, object]):
            Specifies which columns to update and their new values.<br>
            Column-value pairs to update:
            {"age": 31}
        where_condition (str):
            SQL WHERE clause:
            id = ? AND name = ?
        where_params (tuple | None):
            Parameters for the WHERE clause.<br>
            Defaults to None:
            (1, "Alice")
    Returns:
        out (int):
            Number of updated rows,<br>
            or 0 on failure.
    """

    NewtCons.validate_type(
        table, str, check_non_empty=True,
        location="Newt.sql.query_update : table"
    )

    NewtCons.validate_type(
        set_data, dict, check_non_empty=True,
        location="Newt.sql.query_update : set_data"
    )

    NewtCons.validate_type(
        where_condition, str, check_non_empty=True,
        location="Newt.sql.query_update : where_condition"
    )

    NewtCons.validate_type(
        where_params, (tuple, type(None)),
        location="Newt.sql.query_update : where_params"
    )

    set_clause = ", ".join([f"{k} = ?" for k in set_data])
    # set_clause = "age = ?"

    query = f"UPDATE {table} SET {set_clause} WHERE {where_condition};"
    # UPDATE table SET age = ? WHERE id = ? AND name = ?

    params = tuple(set_data.values()) + (where_params or ())
    # params = (31, 1, 'Alice')

    result = query_execute(database, query, params)

    if NewtCons.validate_type(
        result, int,
        location="Newt.sql.query_update : result"
    ):
        if isinstance(result, int):
            return result

    NewtCons.error_msg(  # pragma: no cover
        f"Found Error Msg: (found? write test!)",  # TODO
        location="Newt.sql.query_update : error_msg",
        stop=False
    )

    # Default return value if no rows are updated
    return 0  # pragma: no cover


def export_sql_query_to_csv(
        database: str,
        csv_file: str,
        table: str,
        columns: str = "*",
        query_str: str = "",
        params: tuple | None = None,
        delimiter: str = ";",
        obscure_list: list = [],
        print_log: bool = True
        ) -> bool:
    """ ## Run a SQL SELECT query and export the result to a CSV file.

    Args:
        database (str):
            Path to the SQLite database file.
        csv_file (str):
            Path to the CSV output file.
        table (str):
            Name of the table to query.
        columns (str):
            Comma-separated column names to select.<br>
            Defaults to `"*"` (all columns).<br>
            Example: `"id, name, email"`
        query_str (str):
            Optional SQL clause appended after the table name (e.g. WHERE, ORDER BY).<br>
            Defaults to empty string.<br>
            Example: `"WHERE id = ?" or "ORDER BY name ASC"`
        params (tuple | None):
            Query parameters.<br>
            Defaults to None:
            (1,) or (1, 2, 3)
        delimiter (str):
            Column separator character used in the CSV file.<br>
            Defaults to ";".
        obscure_list (list):
            List of substrings to keep visible in log messages.<br>
            All other characters in `file_path` will be masked with `*`.<br>
            If empty, the full path is shown as-is.<br>
            Defaults to [].
        print_log (bool):
            If True, prints a confirmation message with row count and mode after saving.<br>
            Defaults to True.

    Returns:
        out (bool):
            True if export succeeded,<br>
            otherwise False.
    """

    NewtCons.validate_type(
        csv_file, str, check_non_empty=True,
        location="Newt.sql.export_sql_query_to_csv : csv_file"
    )

    NewtCons.validate_type(
        delimiter, str, check_non_empty=True,
        location="Newt.sql.export_sql_query_to_csv : delimiter"
    )

    try:
        # Step 1: run select query
        result = query_select(database, table, columns, query_str, params)

        NewtCons.validate_type(
            result, list, check_non_empty=True,
            location="Newt.sql.export_sql_query_to_csv : result"
        )

        # Step 2: extract headers and rows for CSV
        headers = list(result[0].keys())
        rows = [list(row.values()) for row in result]

        # Step 3: save using newtutils/files.py
        NewtFiles.save_csv_to_file(
            csv_file,
            [headers] + rows,
            delimiter=delimiter,
            obscure_list=obscure_list,
            print_log=print_log
        )

        return True

    except Exception as e:  # pragma: no cover
        NewtCons.error_msg(
            f"Found Error Msg: (found? write test!)",  # TODO
            f"Exception: {e}",
            location="Newt.sql.export_sql_query_to_csv : Exception",
            stop=False
        )
        return False
