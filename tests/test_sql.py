"""
Comprehensive unit tests for newtutils.sql module.

Tests cover:
- Database delayed close (db_delayed_close)
- SQL query execution (sql_execute_query)
- SQL select operations (sql_select_rows)
- SQL insert operations (sql_insert_row)
- SQL update operations (sql_update_rows)
"""

import pytest
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
            create_query = "CREATE TABLE test (id INTEGER, name TEXT)"
            NewtSQL.sql_execute_query(db_path, create_query)
            # Insert row
            insert_query = "INSERT INTO test (id, name) VALUES (?, ?)"
            insert_params = (1, "Test")
            insert_result = NewtSQL.sql_execute_query(db_path, insert_query, insert_params)
            print("result:", insert_result)
            assert isinstance(insert_result, int)
            assert insert_result == 1

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

    def test_sql_execute_query_creates_directory(self, capsys):
        """Test that sql_execute_query creates parent directories."""
        print_my_func_name("test_sql_execute_query_creates_directory")

        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = os.path.join(tmpdir, "level1", "level2", "test.db")
            query = "CREATE TABLE test (id INTEGER)"
            result = NewtSQL.sql_execute_query(nested_path, query)
            print("result:", result)
            assert os.path.exists(nested_path)
            NewtSQL.db_delayed_close(nested_path)

        captured = capsys.readouterr()
        print_my_captured(captured)


class TestSqlSelectRows:
    """Tests for sql_select_rows function."""

    def test_sql_select_rows_basic(self, capsys):
        """Test basic select operation."""
        print_my_func_name("test_sql_select_rows_basic")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Create table and insert data
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER, name TEXT)")
            NewtSQL.sql_execute_query(db_path, "INSERT INTO test VALUES (1, 'Alice')")
            NewtSQL.sql_execute_query(db_path, "INSERT INTO test VALUES (2, 'Bob')")

            # Select rows
            result = NewtSQL.sql_select_rows(db_path, "SELECT * FROM test")
            print("result:", result)
            assert isinstance(result, list)
            assert len(result) == 2

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sql_select_rows_with_params(self, capsys):
        """Test select with parameters."""
        print_my_func_name("test_sql_select_rows_with_params")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Create table and insert data
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER, name TEXT)")
            NewtSQL.sql_execute_query(db_path, "INSERT INTO test VALUES (1, 'Alice')")
            NewtSQL.sql_execute_query(db_path, "INSERT INTO test VALUES (2, 'Bob')")

            # Select with WHERE clause
            result = NewtSQL.sql_select_rows(db_path, "SELECT * FROM test WHERE id = ?", (1,))
            print("result:", result)
            assert len(result) == 1
            assert result[0]["id"] == 1

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sql_select_rows_empty_result(self, capsys):
        """Test select with no results."""
        print_my_func_name("test_sql_select_rows_empty_result")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Create table
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER)")

            # Select with no data
            result = NewtSQL.sql_select_rows(db_path, "SELECT * FROM test")
            print("result:", result)
            assert result == []

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sql_select_rows_invalid_query(self, capsys):
        """Test select with invalid query."""
        print_my_func_name("test_sql_select_rows_invalid_query")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            with pytest.raises(SystemExit):
                result = NewtSQL.sql_select_rows(db_path, "INVALID SQL QUERY")
                print("This line will not be printed:", result)

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)


class TestSqlInsertRow:
    """Tests for sql_insert_row function."""

    def test_sql_insert_row_single_dict(self, capsys):
        """Test inserting a single row from dict."""
        print_my_func_name("test_sql_insert_row_single_dict")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Create table
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER, name TEXT, age INTEGER)")

            # Insert single row
            data = {"id": 1, "name": "Alice", "age": 30}
            print("data:", data)

            insert_result = NewtSQL.sql_insert_row(db_path, "test", data)
            print("insert_result:", insert_result)
            assert insert_result == 1

            # Select with no data
            select_result = NewtSQL.sql_select_rows(db_path, "SELECT * FROM test")
            print("select_result:", select_result)
            assert len(select_result) == 1

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sql_insert_row_multiple_dicts(self, capsys):
        """Test inserting multiple rows from list of dicts."""
        print_my_func_name("test_sql_insert_row_multiple_dicts")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Create table
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER, name TEXT)")

            # Insert multiple rows
            data = [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"},
                {"id": 3, "name": "Charlie"}
            ]
            print("data:", data)

            insert_result = NewtSQL.sql_insert_row(db_path, "test", data)
            print("insert_result:", insert_result)
            assert insert_result == 3

            # Select with no data
            select_result = NewtSQL.sql_select_rows(db_path, "SELECT * FROM test")
            print("select_result:", select_result)
            assert len(select_result) == 3

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sql_insert_row_empty_data(self, capsys):
        """Test inserting with empty data."""
        print_my_func_name("test_sql_insert_row_empty_data")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER)")
            result = NewtSQL.sql_insert_row(db_path, "test", {})
            print("result:", result)
            assert result == 0

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sql_insert_row_invalid_input(self, capsys):
        """Test inserting with invalid input."""
        print_my_func_name("test_sql_insert_row_invalid_input")

        result_1 = NewtSQL.sql_insert_row(123, "test", {"id": 1})  # type: ignore
        print("result_1:", result_1)
        assert result_1 == 0

        result_2 = NewtSQL.sql_insert_row("test.db", 456, {"id": 2})  # type: ignore
        print("result:", result_2)
        assert result_2 == 0

        result_3 = NewtSQL.sql_insert_row("test.db", "test", "not a dict")  # type: ignore
        print("result:", result_3)
        assert result_3 == 0

        captured = capsys.readouterr()
        print_my_captured(captured)


class TestSqlUpdateRows:
    """Tests for sql_update_rows function."""

    def test_sql_update_rows_basic(self, capsys):
        """Test basic update operation."""
        print_my_func_name("test_sql_update_rows_basic")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Create table and insert data
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER, name TEXT, age INTEGER)")
            data = [
                {"id": 1, "name": "Alice", "age": 30},
                {"id": 2, "name": "Bob", "age": 35},
                {"id": 3, "name": "Charlie", "age": 40}
            ]
            print("data:", data)
            NewtSQL.sql_insert_row(db_path, "test", data)

            # Select with no data
            select_result = NewtSQL.sql_select_rows(db_path, "SELECT * FROM test")
            print("select_result:", select_result)
            assert len(select_result) == 3

            # Update row
            update_result = NewtSQL.sql_update_rows(
                db_path,
                "test",
                {"age": 31},
                "id = ?",
                (1,)
            )
            print("update_result:", update_result)
            assert update_result == 1

            # Verify update
            select_result_1 = NewtSQL.sql_select_rows(db_path, "SELECT * FROM test WHERE id = 1")
            print("select_result_1:", select_result_1)
            assert select_result_1[0]["age"] == 31
            assert len(select_result_1) == 1

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sql_update_rows_multiple_columns(self, capsys):
        """Test updating multiple columns."""
        print_my_func_name("test_sql_update_rows_multiple_columns")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Create table and insert data
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER, name TEXT, age INTEGER)")
            data = [
                {"id": 1, "name": "Alice", "age": 30},
                {"id": 2, "name": "Bob", "age": 35},
                {"id": 3, "name": "Charlie", "age": 40}
            ]
            print("data:", data)
            NewtSQL.sql_insert_row(db_path, "test", data)

            # Update multiple columns
            result = NewtSQL.sql_update_rows(
                db_path, "test",
                {"name": "Alice Updated", "age": 31},
                "id = ?",
                (1,)
            )
            print("result:", result)
            assert result == 1

            # Verify update
            select_result = NewtSQL.sql_select_rows(db_path, "SELECT * FROM test WHERE id = 1")
            print("select_result:", select_result)
            assert select_result[0]["age"] == 31
            assert select_result[0]["name"] == "Alice Updated"
            assert len(select_result) == 1

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sql_update_rows_no_match(self, capsys):
        """Test update with no matching rows."""
        print_my_func_name("test_sql_update_rows_no_match")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            # Create table
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER, name TEXT)")

            # Update with no match
            result = NewtSQL.sql_update_rows(
                db_path, "test",
                {"name": "Updated"},
                "id = ?",
                (999,)
            )
            print("result:", result)
            assert result == 0

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sql_update_rows_empty_data(self, capsys):
        """Test update with empty data."""
        print_my_func_name("test_sql_update_rows_empty_data")

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER)")
            result = NewtSQL.sql_update_rows(db_path, "test", {}, "id = ?", (1,))
            print("result:", result)
            assert result == 0

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sql_update_rows_invalid_input(self, capsys):
        """Test update with invalid input."""
        print_my_func_name("test_sql_update_rows_invalid_input")

        result = NewtSQL.sql_update_rows(
            123,  # type: ignore
            "test",
            {"name": "test"},
            "id = ?",
            (1,)
            )
        print("result:", result)
        assert result == 0

        captured = capsys.readouterr()
        print_my_captured(captured)
