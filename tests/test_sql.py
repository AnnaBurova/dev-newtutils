"""
Comprehensive unit tests for newtutils.sql module.

Tests cover:
TestDbDelayedClose
TestSqlExecuteQuery
TestSqlSelectRows
TestSqlInsertRow
TestSqlUpdateRows
TestExportSqlQueryToCsv
"""

import pytest
import tempfile

import os

from helpers import print_my_func_name, print_my_captured
import newtutils.files as NewtFiles
import newtutils.sql as NewtSQL


class TestDbDelayedClose:
    """ Tests for db_delayed_close function. """


    def test_db_delayed_close_existing_db(self, capsys):
        """ Test closing an existing database. """
        print_my_func_name()

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

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_db_delayed_close_nonexistent_db(self, capsys):
        """ Test closing a non-existent database returns True. """
        print_my_func_name()

        result = NewtSQL.db_delayed_close("/nonexistent/database.db")
        assert result is True

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.files.check_file_exists : logging\n" in captured.out
        assert "\nFile not found: /nonexistent/database.db\n" in captured.out


class TestSqlExecuteQuery:
    """ Tests for sql_execute_query function. """


    def test_sql_execute_query_create_table(self, capsys):
        """ Test creating a table. """
        print_my_func_name()

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

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_execute_query_insert(self, capsys):
        """ Test INSERT query. """
        print_my_func_name()

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

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_execute_query_select(self, capsys):
        """ Test SELECT query. """
        print_my_func_name()

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
            assert result[1]["id"] == 2
            assert result[1]["name"] == "Bob"

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nresult: [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_execute_query_update(self, capsys):
        """ Test UPDATE query. """
        print_my_func_name()

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

        assert "\nselect_result: [{'id': 1, 'name': 'Alice Updated'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_execute_query_delete(self, capsys):
        """ Test DELETE query. """
        print_my_func_name()

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
            assert select_result[0]["id"] == 2
            assert select_result[0]["name"] == "Bob"

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nselect_result: [{'id': 2, 'name': 'Bob'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_execute_query_executemany(self, capsys):
        """ Test executemany with list of tuples. """
        print_my_func_name()

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
            assert select_result[0]["id"] == 1
            assert select_result[0]["name"] == "Alice"
            assert select_result[1]["id"] == 2
            assert select_result[1]["name"] == "Bob"
            assert select_result[2]["id"] == 3
            assert select_result[2]["name"] == "Charlie"

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nselect_result: [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}, {'id': 3, 'name': 'Charlie'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_execute_query_invalid_input(self, capsys):
        """ Test with invalid input. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info_1:
            NewtSQL.sql_execute_query(123, "SELECT 1")  # type: ignore
            print("This line will not be printed 01")
        assert exc_info_1.value.code == 1

        with pytest.raises(SystemExit) as exc_info_2:
            NewtSQL.sql_execute_query("test.db", 456)  # type: ignore
            print("This line will not be printed 02")
        assert exc_info_2.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.sql.sql_execute_query : database\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.sql.sql_execute_query : query\n" in captured.out
        assert "\nExpected <class 'str'>, got <class 'int'>\n" in captured.out
        assert "\nValue: 123\n" in captured.out
        assert "\nValue: 456\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


    def test_sql_execute_query_creates_directory(self, capsys):
        """ Test that sql_execute_query creates parent directories. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = os.path.join(tmpdir, "level1", "level2", "test.db")
            query = "CREATE TABLE test (id INTEGER)"
            result = NewtSQL.sql_execute_query(nested_path, query)
            print("result:", result)
            assert os.path.exists(nested_path)
            NewtSQL.db_delayed_close(nested_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


class TestSqlSelectRows:
    """ Tests for sql_select_rows function. """


    def test_sql_select_rows_basic(self, capsys):
        """ Test basic select operation. """
        print_my_func_name()

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

        assert "\nresult: [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_select_rows_with_params(self, capsys):
        """ Test select with parameters. """
        print_my_func_name()

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

        assert "\nresult: [{'id': 1, 'name': 'Alice'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_select_rows_empty_result(self, capsys):
        """ Test select with no results. """
        print_my_func_name()

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

        assert "\nresult: []\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_select_rows_invalid_query(self, capsys):
        """ Test select with invalid query. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        try:
            with pytest.raises(SystemExit) as exc_info:
                NewtSQL.sql_select_rows(db_path, "INVALID SQL QUERY")
                print("This line will not be printed")
            assert exc_info.value.code == 1

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.sql.sql_execute_query : OperationalError in Syntax\n" in captured.out
        assert "\nSyntax error: near \"INVALID\": syntax error\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.sql.sql_select_rows : result\n" in captured.out
        assert "\nExpected <class 'list'>, got <class 'NoneType'>\n" in captured.out
        assert "\nValue: None\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


class TestSqlInsertRow:
    """ Tests for sql_insert_row function. """


    def test_sql_insert_row_single_dict(self, capsys):
        """ Test inserting a single row from dict. """
        print_my_func_name()

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

        assert "\nselect_result: [{'id': 1, 'name': 'Alice', 'age': 30}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_insert_row_multiple_dicts(self, capsys):
        """ Test inserting multiple rows from list of dicts. """
        print_my_func_name()

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
            assert select_result[0]["id"] == 1
            assert select_result[0]["name"] == "Alice"
            assert select_result[1]["id"] == 2
            assert select_result[1]["name"] == "Bob"
            assert select_result[2]["id"] == 3
            assert select_result[2]["name"] == "Charlie"

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nselect_result: [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}, {'id': 3, 'name': 'Charlie'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_insert_row_empty_data(self, capsys):
        """ Test inserting with empty data. """
        print_my_func_name()

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

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input : is_empty > Newt.sql.sql_insert_row : data\n" in captured.out
        assert "\nValue must be non-empty\n" in captured.out
        assert "\nValue: {}\n" in captured.out


    def test_sql_insert_row_invalid_input(self, capsys):
        """ Test inserting with invalid input. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info_1:
            NewtSQL.sql_insert_row(123, "test", {"id": 1})  # type: ignore
            print("This line will not be printed 01")
        assert exc_info_1.value.code == 1
        print()

        with pytest.raises(SystemExit) as exc_info_2:
            NewtSQL.sql_insert_row("test.db", 456, {"id": 2})  # type: ignore
            print("This line will not be printed 02")
        assert exc_info_2.value.code == 1
        print()

        result_3 = NewtSQL.sql_insert_row("test.db", "test", "not a dict")  # type: ignore
        print("result:", result_3)
        assert result_3 == 0

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.sql.sql_execute_query : database\n" in captured.out
        assert "\nExpected <class 'str'>, got <class 'int'>\n" in captured.out
        assert "\nValue: 123\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.sql.sql_insert_row : table\n" in captured.out
        assert "\nValue: 456\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.sql.sql_insert_row : data\n" in captured.out
        assert "\nExpected (<class 'dict'>, <class 'list'>), got <class 'str'>\n" in captured.out
        assert "\nValue: not a dict\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


class TestSqlUpdateRows:
    """ Tests for sql_update_rows function. """


    def test_sql_update_rows_basic(self, capsys):
        """ Test basic update operation. """
        print_my_func_name()

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
            select_result_1 = NewtSQL.sql_select_rows(db_path, "SELECT * FROM test")
            print("select_result_1:", select_result_1)
            assert len(select_result_1) == 3
            assert select_result_1[0]["id"] == 1
            assert select_result_1[0]["name"] == "Alice"
            assert select_result_1[0]["age"] == 30
            assert select_result_1[1]["id"] == 2
            assert select_result_1[1]["name"] == "Bob"
            assert select_result_1[1]["age"] == 35
            assert select_result_1[2]["id"] == 3
            assert select_result_1[2]["name"] == "Charlie"
            assert select_result_1[2]["age"] == 40


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
            select_result_2 = NewtSQL.sql_select_rows(db_path, "SELECT * FROM test")
            print("select_result_2:", select_result_2)
            assert len(select_result_2) == 3
            assert select_result_2[0]["id"] == 1
            assert select_result_2[0]["name"] == "Alice"
            assert select_result_2[0]["age"] == 31
            assert select_result_2[1]["id"] == 2
            assert select_result_2[1]["name"] == "Bob"
            assert select_result_2[1]["age"] == 35
            assert select_result_2[2]["id"] == 3
            assert select_result_2[2]["name"] == "Charlie"
            assert select_result_2[2]["age"] == 40

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nselect_result_1: [{'id': 1, 'name': 'Alice', 'age': 30}, {'id': 2, 'name': 'Bob', 'age': 35}, {'id': 3, 'name': 'Charlie', 'age': 40}]\n" in captured.out
        assert "\nupdate_result: 1\n" in captured.out
        assert "\nselect_result_2: [{'id': 1, 'name': 'Alice', 'age': 31}, {'id': 2, 'name': 'Bob', 'age': 35}, {'id': 3, 'name': 'Charlie', 'age': 40}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_update_rows_multiple_columns(self, capsys):
        """ Test updating multiple columns. """
        print_my_func_name()

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
            update_result = NewtSQL.sql_update_rows(
                db_path, "test",
                {"name": "Alice Updated", "age": 31},
                "id = ?",
                (1,)
            )
            print("update_result:", update_result)
            assert update_result == 1

            # Verify update
            select_result = NewtSQL.sql_select_rows(db_path, "SELECT * FROM test")
            print("select_result:", select_result)
            assert len(select_result) == 3
            assert select_result[0]["id"] == 1
            assert select_result[0]["name"] == "Alice Updated"
            assert select_result[0]["age"] == 31
            assert select_result[1]["id"] == 2
            assert select_result[1]["name"] == "Bob"
            assert select_result[1]["age"] == 35
            assert select_result[2]["id"] == 3
            assert select_result[2]["name"] == "Charlie"
            assert select_result[2]["age"] == 40
        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nupdate_result: 1\n" in captured.out
        assert "\nselect_result: [{'id': 1, 'name': 'Alice Updated', 'age': 31}, {'id': 2, 'name': 'Bob', 'age': 35}, {'id': 3, 'name': 'Charlie', 'age': 40}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_update_rows_no_match(self, capsys):
        """ Test update with no matching rows. """
        print_my_func_name()

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

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_update_rows_empty_data(self, capsys):
        """ Test update with empty data. """
        print_my_func_name()

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

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input : is_empty > Newt.sql.sql_update_rows : set_data\n" in captured.out
        assert "\nValue must be non-empty\n" in captured.out
        assert "\nValue: {}\n" in captured.out


    def test_sql_update_rows_invalid_input(self, capsys):
        """ Test update with invalid input. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info:
            NewtSQL.sql_update_rows(
                123,  # type: ignore
                "test",
                {"name": "test"},
                "id = ?",
                (1,)
            )
            print("This line will not be printed")
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.sql.sql_execute_query : database\n" in captured.out
        assert "\nExpected <class 'str'>, got <class 'int'>\n" in captured.out
        assert "\nValue: 123\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


class TestExportSqlQueryToCsv:
    """ Tests for export_sql_query_to_csv function. """


    def test_export_sql_query_to_csv_basic(self, capsys):
        """ Test basic CSV export. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as csv_tmp:
            csv_path = csv_tmp.name

        try:
            # Create table and insert data
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER, name TEXT, age INTEGER)")
            NewtSQL.sql_execute_query(db_path, "INSERT INTO test VALUES (1, 'Alice', 30)")
            NewtSQL.sql_execute_query(db_path, "INSERT INTO test VALUES (2, 'Bob', 25)")

            # Export to CSV
            result = NewtSQL.export_sql_query_to_csv(
                db_path,
                "SELECT * FROM test ORDER BY id",
                csv_path
            )
            print("result:", result)
            assert result is True
            assert os.path.exists(csv_path)
            print()

            # Verify CSV content
            csv_data = NewtFiles.read_csv_from_file(csv_path)
            print("csv_data:", csv_data)
            assert isinstance(csv_data, list)
            assert len(csv_data) == 3  # Header + 2 rows
            assert "id" in csv_data[0]
            assert "name" in csv_data[0]

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)
            if os.path.exists(csv_path):
                os.unlink(csv_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[Newt.files.save_csv_to_file] Saved CSV to file:\n" in captured.out
        assert "\n(rows=3, mode=write, delimiter=';')\n" in captured.out
        assert "\n[Newt.files.read_csv_from_file] Loaded CSV from file:\n" in captured.out
        assert "\n(rows=3, delimiter=';')\n" in captured.out
        assert "\ncsv_data: [['id', 'name', 'age'], ['1', 'Alice', '30'], ['2', 'Bob', '25']]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_export_sql_query_to_csv_empty_result(self, capsys):
        """ Test export with empty query result. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as csv_tmp:
            csv_path = csv_tmp.name

        try:
            # Create empty table
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER)")

            # Export empty result
            result = NewtSQL.export_sql_query_to_csv(
                db_path,
                "SELECT * FROM test",
                csv_path
            )
            print("result:", result)
            assert result is False

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)
            if os.path.exists(csv_path):
                os.unlink(csv_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.sql.export_sql_query_to_csv : result\n" in captured.out
        assert "\nEmpty result: []\n" in captured.out


    def test_export_sql_query_to_csv_custom_delimiter(self, capsys):
        """ Test export with custom delimiter. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as csv_tmp:
            csv_path = csv_tmp.name

        try:
            # Create table and insert data
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER, name TEXT)")
            NewtSQL.sql_execute_query(db_path, "INSERT INTO test VALUES (1, 'Alice')")

            # Export with comma delimiter
            result = NewtSQL.export_sql_query_to_csv(
                db_path,
                "SELECT * FROM test",
                csv_path,
                delimiter=","
            )
            print("result:", result)
            assert result is True
            print()

            # Verify CSV content
            csv_data = NewtFiles.read_csv_from_file(csv_path, ",")
            print("csv_data:", csv_data)

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)
            if os.path.exists(csv_path):
                os.unlink(csv_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[Newt.files.save_csv_to_file] Saved CSV to file:\n" in captured.out
        assert "\n(rows=2, mode=write, delimiter=',')\n" in captured.out
        assert "\n[Newt.files.read_csv_from_file] Loaded CSV from file:\n" in captured.out
        assert "\n(rows=2, delimiter=',')\n" in captured.out
        assert "\ncsv_data: [['id', 'name'], ['1', 'Alice']]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_export_sql_query_to_csv_with_params(self, capsys):
        """ Test export with query parameters. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name

        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as csv_tmp:
            csv_path = csv_tmp.name

        try:
            # Create table and insert data
            NewtSQL.sql_execute_query(db_path, "CREATE TABLE test (id INTEGER, name TEXT)")
            NewtSQL.sql_execute_query(db_path, "INSERT INTO test VALUES (1, 'Alice')")
            NewtSQL.sql_execute_query(db_path, "INSERT INTO test VALUES (2, 'Bob')")

            # Export with WHERE clause
            result = NewtSQL.export_sql_query_to_csv(
                db_path,
                "SELECT * FROM test WHERE id = ?",
                csv_path,
                params=(1,)
            )
            print("result:", result)
            assert result is True
            print()

            # Verify CSV content
            csv_data = NewtFiles.read_csv_from_file(csv_path)
            print("csv_data:", csv_data)

        finally:
            NewtSQL.db_delayed_close(db_path)
            if os.path.exists(db_path):
                os.unlink(db_path)
            if os.path.exists(csv_path):
                os.unlink(csv_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[Newt.files.save_csv_to_file] Saved CSV to file:\n" in captured.out
        assert "\n(rows=2, mode=write, delimiter=';')\n" in captured.out
        assert "\n[Newt.files.read_csv_from_file] Loaded CSV from file:\n" in captured.out
        assert "\n(rows=2, delimiter=';')\n" in captured.out
        assert "\ncsv_data: [['id', 'name'], ['1', 'Alice']]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_export_sql_query_to_csv_invalid_input(self, capsys):
        """ Test export with invalid input. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info_1:
            NewtSQL.export_sql_query_to_csv(
                123,  # type: ignore
                "SELECT 1",
                "test.csv"
            )
            print("This line will not be printed 01")
        assert exc_info_1.value.code == 1
        print()

        with pytest.raises(SystemExit) as exc_info_2:
            NewtSQL.export_sql_query_to_csv(
                "test.db",
                456,  # type: ignore
                "test.csv"
            )
            print("This line will not be printed 02")
        assert exc_info_2.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.sql.export_sql_query_to_csv : database\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.sql.export_sql_query_to_csv : query\n" in captured.out
        assert "\nExpected <class 'str'>, got <class 'int'>\n" in captured.out
        assert "\nValue: 123\n" in captured.out
        assert "\nValue: 456\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out
