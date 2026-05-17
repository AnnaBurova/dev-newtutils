"""
Updated on 2026-05
Created on 2025-11

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.sql module.

Tests cover:
- TestDbDelayedClose
- TestQueryExecute
- TestSqlSelectRows
- TestSqlInsertRow
- TestSqlUpdateRows
- TestExportSqlQueryToCsv
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
        """ Test behavior of db_delayed_close when closing an existing database. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create a simple database
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER)")
            result = NewtSQL.db_delayed_close(file_db)
            assert result is True

        finally:
            if os.path.exists(file_db):
                os.unlink(file_db)

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


class TestQueryExecute:
    """ Tests for query_execute function. """


    def test_query_execute_create_table(self, capsys):
        """ Test creating a table. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            query = "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
            result = NewtSQL.query_execute(file_db, query)
            print("result:", result)
            # CREATE returns rowcount, typically -1
            assert isinstance(result, int)
            assert result == -1

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_query_execute_insert(self, capsys):
        """ Test INSERT query. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create table
            create_query = "CREATE TABLE test (id INTEGER, name TEXT)"
            NewtSQL.query_execute(file_db, create_query)
            # Insert row
            insert_query = "INSERT INTO test (id, name) VALUES (?, ?)"
            insert_params = (1, "Test")
            insert_result = NewtSQL.query_execute(file_db, insert_query, insert_params)
            print("result:", insert_result)
            assert isinstance(insert_result, int)
            assert insert_result == 1

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_query_execute_select(self, capsys):
        """ Test SELECT query. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create table and insert data
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT)")
            NewtSQL.query_execute(file_db, "INSERT INTO test VALUES (1, 'Alice')")
            NewtSQL.query_execute(file_db, "INSERT INTO test VALUES (2, 'Bob')")

            # Select data
            query = "SELECT * FROM test"
            result = NewtSQL.query_execute(file_db, query)
            print("result:", result)
            assert isinstance(result, list)
            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[0]["name"] == "Alice"
            assert result[1]["id"] == 2
            assert result[1]["name"] == "Bob"

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nresult: [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_query_execute_update(self, capsys):
        """ Test UPDATE query. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create table and insert data
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT)")
            NewtSQL.query_execute(file_db, "INSERT INTO test VALUES (1, 'Alice')")

            # Update data
            query = "UPDATE test SET name = ? WHERE id = ?"
            params = ("Alice Updated", 1)
            update_result = NewtSQL.query_execute(file_db, query, params)
            print("update_result:", update_result)
            assert isinstance(update_result, int)
            assert update_result == 1

            # Verify update
            select_result = NewtSQL.query_execute(file_db, "SELECT * FROM test")
            print("select_result:", select_result)
            assert isinstance(select_result, list)
            assert len(select_result) > 0
            assert select_result[0]["name"] == "Alice Updated"

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nselect_result: [{'id': 1, 'name': 'Alice Updated'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_query_execute_delete(self, capsys):
        """ Test DELETE query. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create table and insert data
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT)")
            NewtSQL.query_execute(file_db, "INSERT INTO test VALUES (1, 'Alice')")
            NewtSQL.query_execute(file_db, "INSERT INTO test VALUES (2, 'Bob')")

            # Delete data
            query = "DELETE FROM test WHERE id = ?"
            params = (1,)
            delete_result = NewtSQL.query_execute(file_db, query, params)
            print("delete_result:", delete_result)
            assert isinstance(delete_result, int)
            assert delete_result == 1

            # Verify deletion
            select_result = NewtSQL.query_execute(file_db, "SELECT * FROM test")
            print("select_result:", select_result)
            assert isinstance(select_result, list)
            assert len(select_result) == 1
            assert select_result[0]["id"] == 2
            assert select_result[0]["name"] == "Bob"

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nselect_result: [{'id': 2, 'name': 'Bob'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_query_execute_executemany(self, capsys):
        """ Test executemany with list of tuples. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create table
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT)")

            # Insert multiple rows
            query = "INSERT INTO test (id, name) VALUES (?, ?)"
            params = [(1, "Alice"), (2, "Bob"), (3, "Charlie")]
            insert_result = NewtSQL.query_execute(file_db, query, params)
            print("result:", insert_result)
            assert isinstance(insert_result, int)
            assert insert_result == 3

            # Verify insertion
            select_result = NewtSQL.query_execute(file_db, "SELECT * FROM test")
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
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nselect_result: [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}, {'id': 3, 'name': 'Charlie'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_query_execute_invalid_input(self, capsys):
        """ Test with invalid input. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info_1:
            NewtSQL.query_execute(123, "SELECT 1")  # type: ignore
            print("This line will not be printed")
        assert exc_info_1.value.code == 1
        print("exc_info_1:", exc_info_1.value.code)

        with pytest.raises(SystemExit) as exc_info_2:
            NewtSQL.query_execute("test.db", 456)  # type: ignore
            print("This line will not be printed")
        assert exc_info_2.value.code == 1
        print("exc_info_2:", exc_info_2.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\n::: ERROR :::\n") == 2
        assert "\nLocation: Newt.console.validate_input > Newt.sql.sql_execute_query : database\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.sql.sql_execute_query : query\n" in captured.out
        assert captured.out.count("\nExpected <class 'str'>, got <class 'int'>\n") == 2
        assert "\nValue: 123\n" in captured.out
        assert "\nValue: 456\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


    def test_query_execute_creates_directory(self, capsys):
        """ Test that query_execute creates parent directories. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "level1", "level2", "test.db")
            query = "CREATE TABLE test (id INTEGER)"
            result = NewtSQL.query_execute(file_path, query)
            print("result:", result)
            assert os.path.exists(file_path)
            NewtSQL.db_delayed_close(file_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


class TestSqlSelectRows:
    """ Tests for query_select function. """


    def test_query_select_basic(self, capsys):
        """ Test basic select operation. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create table and insert data
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT)")
            NewtSQL.query_execute(file_db, "INSERT INTO test VALUES (1, 'Alice')")
            NewtSQL.query_execute(file_db, "INSERT INTO test VALUES (2, 'Bob')")

            # Select rows
            result = NewtSQL.query_select(file_db, "SELECT * FROM test")
            print("result:", result)
            assert isinstance(result, list)
            assert len(result) == 2

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nresult: [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_query_select_with_params(self, capsys):
        """ Test select with parameters. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create table and insert data
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT)")
            NewtSQL.query_execute(file_db, "INSERT INTO test VALUES (1, 'Alice')")
            NewtSQL.query_execute(file_db, "INSERT INTO test VALUES (2, 'Bob')")

            # Select with WHERE clause
            result = NewtSQL.query_select(file_db, "SELECT * FROM test WHERE id = ?", (1,))
            print("result:", result)
            assert len(result) == 1
            assert result[0]["id"] == 1

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nresult: [{'id': 1, 'name': 'Alice'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_query_select_empty_result(self, capsys):
        """ Test select with no results. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create table
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER)")

            # Select with no data
            result = NewtSQL.query_select(file_db, "SELECT * FROM test")
            print("result:", result)
            assert result == []

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nresult: []\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_query_select_invalid_query(self, capsys):
        """ Test select with invalid query. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            with pytest.raises(SystemExit) as exc_info:
                NewtSQL.query_select(file_db, "INVALID SQL QUERY")
                print("This line will not be printed")
            assert exc_info.value.code == 1
            print("exc_info:", exc_info.value.code)

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\n::: ERROR :::\n") == 2
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

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create table
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT, age INTEGER)")

            # Insert single row
            data = {"id": 1, "name": "Alice", "age": 30}
            print("data:", data)

            insert_result = NewtSQL.sql_insert_row(file_db, "test", data)
            print("insert_result:", insert_result)
            assert insert_result == 1

            # Select with no data
            select_result = NewtSQL.query_select(file_db, "SELECT * FROM test")
            print("select_result:", select_result)
            assert len(select_result) == 1

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nselect_result: [{'id': 1, 'name': 'Alice', 'age': 30}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_insert_row_multiple_dicts(self, capsys):
        """ Test inserting multiple rows from list of dicts. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create table
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT)")

            # Insert multiple rows
            data = [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"},
                {"id": 3, "name": "Charlie"}
            ]
            print("data:", data)

            insert_result = NewtSQL.sql_insert_row(file_db, "test", data)
            print("insert_result:", insert_result)
            assert insert_result == 3

            # Select with no data
            select_result = NewtSQL.query_select(file_db, "SELECT * FROM test")
            print("select_result:", select_result)
            assert len(select_result) == 3
            assert select_result[0]["id"] == 1
            assert select_result[0]["name"] == "Alice"
            assert select_result[1]["id"] == 2
            assert select_result[1]["name"] == "Bob"
            assert select_result[2]["id"] == 3
            assert select_result[2]["name"] == "Charlie"

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nselect_result: [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}, {'id': 3, 'name': 'Charlie'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_insert_row_empty_data(self, capsys):
        """ Test inserting with empty data. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER)")
            result = NewtSQL.sql_insert_row(file_db, "test", {})
            print("result:", result)
            assert result == 0

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)

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
            print("This line will not be printed")
        assert exc_info_1.value.code == 1
        print("exc_info_1:", exc_info_1.value.code)
        print()

        with pytest.raises(SystemExit) as exc_info_2:
            NewtSQL.sql_insert_row("test.db", 456, {"id": 2})  # type: ignore
            print("This line will not be printed")
        assert exc_info_2.value.code == 1
        print("exc_info_2:", exc_info_2.value.code)
        print()

        result_3 = NewtSQL.sql_insert_row("test.db", "test", "not a dict")  # type: ignore
        print("result:", result_3)
        assert result_3 == 0

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\n::: ERROR :::\n") == 3
        assert "\nLocation: Newt.console.validate_input > Newt.sql.sql_execute_query : database\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.sql.sql_insert_row : table\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.sql.sql_insert_row : data\n" in captured.out
        assert captured.out.count("\nExpected <class 'str'>, got <class 'int'>\n") == 2
        assert "\nExpected (<class 'dict'>, <class 'list'>), got <class 'str'>\n" in captured.out
        assert "\nValue: 123\n" in captured.out
        assert "\nValue: 456\n" in captured.out
        assert "\nValue: not a dict\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


class TestSqlUpdateRows:
    """ Tests for sql_update_rows function. """


    def test_sql_update_rows_basic(self, capsys):
        """ Test basic update operation. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create table and insert data
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT, age INTEGER)")
            data = [
                {"id": 1, "name": "Alice", "age": 30},
                {"id": 2, "name": "Bob", "age": 35},
                {"id": 3, "name": "Charlie", "age": 40}
            ]
            print("data:", data)
            NewtSQL.sql_insert_row(file_db, "test", data)

            # Select with no data
            select_result_1 = NewtSQL.query_select(file_db, "SELECT * FROM test")
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
                file_db,
                "test",
                {"age": 31},
                "id = ?",
                (1,)
            )
            print("update_result:", update_result)
            assert update_result == 1

            # Verify update
            select_result_2 = NewtSQL.query_select(file_db, "SELECT * FROM test")
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
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)

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

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create table and insert data
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT, age INTEGER)")
            data = [
                {"id": 1, "name": "Alice", "age": 30},
                {"id": 2, "name": "Bob", "age": 35},
                {"id": 3, "name": "Charlie", "age": 40}
            ]
            print("data:", data)
            NewtSQL.sql_insert_row(file_db, "test", data)

            # Update multiple columns
            update_result = NewtSQL.sql_update_rows(
                file_db, "test",
                {"name": "Alice Updated", "age": 31},
                "id = ?",
                (1,)
            )
            print("update_result:", update_result)
            assert update_result == 1

            # Verify update
            select_result = NewtSQL.query_select(file_db, "SELECT * FROM test")
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
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nupdate_result: 1\n" in captured.out
        assert "\nselect_result: [{'id': 1, 'name': 'Alice Updated', 'age': 31}, {'id': 2, 'name': 'Bob', 'age': 35}, {'id': 3, 'name': 'Charlie', 'age': 40}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_update_rows_no_match(self, capsys):
        """ Test update with no matching rows. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create table
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT)")

            # Update with no match
            result = NewtSQL.sql_update_rows(
                file_db, "test",
                {"name": "Updated"},
                "id = ?",
                (999,)
            )
            print("result:", result)
            assert result == 0

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sql_update_rows_empty_data(self, capsys):
        """ Test update with empty data. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER)")
            result = NewtSQL.sql_update_rows(file_db, "test", {}, "id = ?", (1,))
            print("result:", result)
            assert result == 0

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)

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
        print("exc_info:", exc_info.value.code)

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

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmpfile:
            file_csv = tmpfile.name

        try:
            # Create table and insert data
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT, age INTEGER)")
            NewtSQL.query_execute(file_db, "INSERT INTO test VALUES (1, 'Alice', 30)")
            NewtSQL.query_execute(file_db, "INSERT INTO test VALUES (2, 'Bob', 25)")

            # Export to CSV
            result = NewtSQL.export_sql_query_to_csv(
                file_db,
                "SELECT * FROM test ORDER BY id",
                file_csv
            )
            print("result:", result)
            assert result is True
            assert os.path.exists(file_csv)
            print()

            # Verify CSV content
            csv_data = NewtFiles.read_csv_from_file(file_csv)
            print("csv_data:", csv_data)
            assert isinstance(csv_data, list)
            assert len(csv_data) == 3  # Header + 2 rows
            assert "id" in csv_data[0]
            assert "name" in csv_data[0]

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)
            if os.path.exists(file_csv):
                os.unlink(file_csv)

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

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmpfile:
            file_csv = tmpfile.name

        try:
            # Create empty table
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER)")

            # Export empty result
            result = NewtSQL.export_sql_query_to_csv(
                file_db,
                "SELECT * FROM test",
                file_csv
            )
            print("result:", result)
            assert result is False

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)
            if os.path.exists(file_csv):
                os.unlink(file_csv)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.sql.export_sql_query_to_csv : result\n" in captured.out
        assert "\nEmpty result: []\n" in captured.out


    def test_export_sql_query_to_csv_custom_delimiter(self, capsys):
        """ Test export with custom delimiter. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmpfile:
            file_csv = tmpfile.name

        try:
            # Create table and insert data
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT)")
            NewtSQL.query_execute(file_db, "INSERT INTO test VALUES (1, 'Alice')")

            # Export with comma delimiter
            result = NewtSQL.export_sql_query_to_csv(
                file_db,
                "SELECT * FROM test",
                file_csv,
                delimiter=","
            )
            print("result:", result)
            assert result is True
            print()

            # Verify CSV content
            csv_data = NewtFiles.read_csv_from_file(file_csv, ",")
            print("csv_data:", csv_data)

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)
            if os.path.exists(file_csv):
                os.unlink(file_csv)

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

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmpfile:
            file_csv = tmpfile.name

        try:
            # Create table and insert data
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT)")
            NewtSQL.query_execute(file_db, "INSERT INTO test VALUES (1, 'Alice')")
            NewtSQL.query_execute(file_db, "INSERT INTO test VALUES (2, 'Bob')")

            # Export with WHERE clause
            result = NewtSQL.export_sql_query_to_csv(
                file_db,
                "SELECT * FROM test WHERE id = ?",
                file_csv,
                params=(1,)
            )
            print("result:", result)
            assert result is True
            print()

            # Verify CSV content
            csv_data = NewtFiles.read_csv_from_file(file_csv)
            print("csv_data:", csv_data)

        finally:
            NewtSQL.db_delayed_close(file_db)
            if os.path.exists(file_db):
                os.unlink(file_db)
            if os.path.exists(file_csv):
                os.unlink(file_csv)

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
            print("This line will not be printed")
        assert exc_info_1.value.code == 1
        print("exc_info_1:", exc_info_1.value.code)
        print()

        with pytest.raises(SystemExit) as exc_info_2:
            NewtSQL.export_sql_query_to_csv(
                "test.db",
                456,  # type: ignore
                "test.csv"
            )
            print("This line will not be printed")
        assert exc_info_2.value.code == 1
        print("exc_info_2:", exc_info_2.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\n::: ERROR :::\n") == 2
        assert "\nLocation: Newt.console.validate_input > Newt.sql.export_sql_query_to_csv : database\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.sql.export_sql_query_to_csv : query\n" in captured.out
        assert captured.out.count("\nExpected <class 'str'>, got <class 'int'>\n") == 2
        assert "\nValue: 123\n" in captured.out
        assert "\nValue: 456\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out
