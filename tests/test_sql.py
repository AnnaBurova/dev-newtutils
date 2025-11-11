"""
Comprehensive unit tests for newtutils.sql module.

Tests cover:
- Database delayed close (db_delayed_close)
- SQL query execution (sql_execute_query)
- SQL select operations (sql_select_rows)
- SQL insert operations (sql_insert_row)
- SQL update operations (sql_update_rows)
"""

import tempfile

import os
import newtutils.sql as NewtSQL


def print_my_func_name(func_name):
    """
    Print the provided function name in a structured format.

    Args:
        func_name (str):
            Name of the function to display.
    """

    print("Function:", func_name)
    print("--------------------------------------------")


def print_my_captured(captured):
    """
    Pretty-print captured standard output and error streams from pytest.

    Args:
        captured:
            A pytest `CaptureResult` object returned by `capsys.readouterr()`.
            Must provide `.out` and `.err` attributes representing captured
            standard output and standard error text.
    """

    print()
    print("START=======================================")

    print("=====captured.out=====")
    if captured.out:
        print(captured.out)
    else:
        print("(no stdout captured)")

    print("=====captured.err=====")
    if captured.err:
        print(captured.err)
    else:
        print("(no stderr captured)")

    print("END=========================================")


class TestDbDelayedClose:
    """Tests for db_delayed_close function."""

    def test_db_delayed_close_existing_db(self, capsys):
        """Test closing an existing database."""
        print_my_func_name("test_db_delayed_close_existing_db")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Create a simple database
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER)")
            result = NewtSQL.db_delayed_close(db_path)
            assert result is True

        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_db_delayed_close_nonexistent_db(self, capsys):
        """Test closing a non-existent database returns True."""
        print_my_func_name("test_db_delayed_close_nonexistent_db")

        result = NewtSQL.db_delayed_close("/nonexistent/database.db")
        assert result is True

        captured = capsys.readouterr()
        print_my_captured(captured)


class TestSqlExecuteQuery:
    """Tests for sql_execute_query function."""

    def test_sql_execute_query_create_table(self, capsys):
        """Test creating a table."""
        print_my_func_name("test_sql_execute_query_create_table")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            query = "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
            result = NewtSQL.sql_execute_query(db_path, query)
            print("result:", result)
            # CREATE returns rowcount, typically -1
            assert isinstance(result, int)
            assert result == -1

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sql_execute_query_insert(self, capsys):
        """Test INSERT query."""
        print_my_func_name("test_sql_execute_query_insert")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Create table
            query_create = "CREATE TABLE test (id INTEGER, name TEXT)"
            NewtSQL.sql_execute_query(db_path, query_create)
            # Insert row
            query_insert = "INSERT INTO test (id, name) VALUES (?, ?)"
            params_insert = (1, "Test")
            result = NewtSQL.sql_execute_query(db_path, query_insert, params_insert)
            print("result:", result)
            assert isinstance(result, int)
            assert result == 1

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sql_execute_query_select(self, capsys):
        """Test SELECT query."""
        print_my_func_name("test_sql_execute_query_select")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Create table and insert data
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER, name TEXT)")
            NewtSQL.sql_execute_query(db_path, "INSERT INTO test VALUES (1, 'Alice')")
            NewtSQL.sql_execute_query(db_path, "INSERT INTO test VALUES (2, 'Bob')")

            # Select data
            query = "SELECT * FROM test"
            result = NewtSQL.sql_execute_query(db_path, query)
            print("result:", result)
            assert isinstance(result, list)
            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[0]["name"] == "Alice"

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sql_execute_query_update(self, capsys):
        """Test UPDATE query."""
        print_my_func_name("test_sql_execute_query_update")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Create table and insert data
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER, name TEXT)")
            NewtSQL.sql_execute_query(db_path, "INSERT INTO test VALUES (1, 'Alice')")

            # Update data
            query = "UPDATE test SET name = ? WHERE id = ?"
            params = ("Alice Updated", 1)
            update_result = NewtSQL.sql_execute_query(db_path, query, params)
            print("update_result:", update_result)
            assert isinstance(update_result, int)
            assert update_result == 1

            # Verify update
            select_result = NewtSQL.sql_execute_query(db_path, "SELECT * FROM test")
            print("select_result:", select_result)
            assert isinstance(select_result, list)
            assert len(select_result) > 0
            assert select_result[0]["name"] == "Alice Updated"

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sql_execute_query_delete(self, capsys):
        """Test DELETE query."""
        print_my_func_name("test_sql_execute_query_delete")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Create table and insert data
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER, name TEXT)")
            NewtSQL.sql_execute_query(db_path, "INSERT INTO test VALUES (1, 'Alice')")
            NewtSQL.sql_execute_query(db_path, "INSERT INTO test VALUES (2, 'Bob')")

            # Delete data
            query = "DELETE FROM test WHERE id = ?"
            params = (1,)
            delete_result = NewtSQL.sql_execute_query(db_path, query, params)
            print("delete_result:", delete_result)
            assert isinstance(delete_result, int)
            assert delete_result == 1

            # Verify deletion
            select_result = NewtSQL.sql_execute_query(db_path, "SELECT * FROM test")
            print("select_result:", select_result)
            assert isinstance(select_result, list)
            assert len(select_result) == 1

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sql_execute_query_executemany(self, capsys):
        """Test executemany with list of tuples."""
        print_my_func_name("test_sql_execute_query_executemany")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Create table
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER, name TEXT)")

            # Insert multiple rows
            query = "INSERT INTO test (id, name) VALUES (?, ?)"
            params = [(1, "Alice"), (2, "Bob"), (3, "Charlie")]
            insert_result = NewtSQL.sql_execute_query(db_path, query, params)
            print("result:", insert_result)
            assert isinstance(insert_result, int)
            assert insert_result == 3

            # Verify insertion
            select_result = NewtSQL.sql_execute_query(db_path, "SELECT * FROM test")
            print("select_result:", select_result)
            assert isinstance(select_result, list)
            assert len(select_result) == 3

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sql_execute_query_invalid_input(self, capsys):
        """Test with invalid input."""
        print_my_func_name("test_sql_execute_query_invalid_input")

        result = NewtSQL.sql_execute_query(123, "SELECT 1")  # type: ignore
        assert result is None

        result = NewtSQL.sql_execute_query("test.db", 456)  # type: ignore
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)
