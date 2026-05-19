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

import sys
import os
import pytest
import tempfile

from .helpers import print_my_func_name, print_my_captured
# import newtutils.console as NewtCons
# import newtutils.utility as NewtUtil
import newtutils.files as NewtFiles
import newtutils.sql as NewtSQL

obscure_list = [
    "C:\\Users\\",
    "\\AppData\\Local\\Temp\\",
    "/tmp/",
    ".csv",
    ]


class TestDbDelayedClose:
    """ Tests for db_delayed_close function. """


    def test_db_delayed_close_existing_db(self, capsys):
        """ Ensure NewtSQL.db_delayed_close() returns True for an existing database. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create a simple database
            result = NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER)")
            assert result == -1
            print("result:", result)

        finally:
            closed = NewtSQL.db_delayed_close(file_db)
            assert closed is True

            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_db_delayed_close_existing_db\n============================================\nresult: -1\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_db_delayed_close_nonexistent_db(self, capsys):
        """ Ensure NewtSQL.db_delayed_close() returns True for a nonexistent database path. """
        print_my_func_name()

        file_db = "/nonexistent/database.db"
        closed = NewtSQL.db_delayed_close(file_db)
        assert closed is True
        print("closed:", closed)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_db_delayed_close_nonexistent_db\n============================================\nclosed: True\n" == captured.out
        assert "\x1b[1m\x1b[31m\nLocation: Newt.files.check_file_exists : print_log\n::: ERROR :::\nFile not found: /nonexistent/database.db\n\x1b[0m\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


class TestQueryExecute:
    """ Tests for query_execute function. """


    def test_query_execute_creates_directory(self, capsys):
        """ Ensure NewtSQL.query_execute() creates missing nested directories automatically. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            file_db = os.path.join(tmpdir, "level1", "level2", "test.db")
            query = "CREATE TABLE test (id INTEGER)"
            result = NewtSQL.query_execute(file_db, query)
            print("result:", result)
            NewtSQL.db_delayed_close(file_db)

            dirname_exists = os.path.exists(os.path.dirname(file_db))
            assert dirname_exists is True
            print("dirname_exists:", dirname_exists)

        dirname_exists = os.path.exists(os.path.dirname(file_db))
        assert dirname_exists is False
        print("dirname_exists:", dirname_exists)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_query_execute_creates_directory\n============================================\nresult: -1\ndirname_exists: True\ndirname_exists: False\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_query_execute_crud_operations(self, capsys):
        """ Ensure NewtSQL.query_execute() handles INSERT, SELECT, UPDATE, and DELETE correctly. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create table
            create_query = "CREATE TABLE test (id INTEGER, name TEXT)"
            create_result = NewtSQL.query_execute(file_db, create_query)
            assert create_result == -1
            print("create_result:", create_result)

            # Insert row
            insert_query_1 = "INSERT INTO test (id, name) VALUES (?, ?)"
            insert_params_1 = (1, "Test")
            insert_result_1 = NewtSQL.query_execute(file_db, insert_query_1, insert_params_1)
            assert isinstance(insert_result_1, int)
            assert insert_result_1 == 1
            print("insert_result_1:", insert_result_1)
            insert_query_2 = "INSERT INTO test VALUES (2, 'Bob')"
            insert_result_2 = NewtSQL.query_execute(file_db, insert_query_2)
            assert isinstance(insert_result_2, int)
            assert insert_result_2 == 1
            print("insert_result_2:", insert_result_2)

            # Select data
            select_query = "SELECT * FROM test"
            select_result_1 = NewtSQL.query_execute(file_db, select_query)
            assert isinstance(select_result_1, list)
            assert len(select_result_1) == 2
            assert isinstance(select_result_1[0], dict)
            assert select_result_1[0]["id"] == 1
            assert select_result_1[0]["name"] == "Test"
            assert select_result_1[1]["id"] == 2
            assert select_result_1[1]["name"] == "Bob"
            print("select_result_1:", select_result_1)

            # Update data
            update_query = "UPDATE test SET name = ? WHERE id = ?"
            update_params = ("Alice", 1)
            update_result = NewtSQL.query_execute(file_db, update_query, update_params)
            assert isinstance(update_result, int)
            assert update_result == 1
            print("update_result:", update_result)

            # Verify update
            select_result_2 = NewtSQL.query_execute(file_db, select_query)
            assert isinstance(select_result_2, list)
            assert len(select_result_2) == 2
            assert isinstance(select_result_2[0], dict)
            assert select_result_2[0]["id"] == 1
            assert select_result_2[0]["name"] == "Alice"
            assert select_result_2[1]["id"] == 2
            assert select_result_2[1]["name"] == "Bob"
            print("select_result_2:", select_result_2)

            # Insert multiple rows
            insert_query_3 = "INSERT INTO test (id, name) VALUES (?, ?)"
            insert_params_3 = [(3, "Aska"), (4, "Felicia"), (5, "Grace")]
            insert_result_3 = NewtSQL.query_execute(file_db, insert_query_3, insert_params_3)
            assert isinstance(insert_result_3, int)
            assert insert_result_3 == 3
            print("insert_result_3:", insert_result_3)

            # Delete data
            delete_query = "DELETE FROM test WHERE id = ?"
            delete_params = (2,)
            delete_result = NewtSQL.query_execute(file_db, delete_query, delete_params)
            assert isinstance(delete_result, int)
            assert delete_result == 1
            print("delete_result:", delete_result)

            # Verify deletion
            select_result_3 = NewtSQL.query_execute(file_db, select_query)
            assert isinstance(select_result_3, list)
            assert len(select_result_3) == 4
            assert isinstance(select_result_3[0], dict)
            assert select_result_3[0]["id"] == 1
            assert select_result_3[0]["name"] == "Alice"
            assert select_result_3[1]["id"] == 3
            assert select_result_3[1]["name"] == "Aska"
            assert select_result_3[2]["id"] == 4
            assert select_result_3[2]["name"] == "Felicia"
            assert select_result_3[3]["id"] == 5
            assert select_result_3[3]["name"] == "Grace"
            print("select_result_3:", select_result_3)

        finally:
            closed = NewtSQL.db_delayed_close(file_db)
            assert closed is True

            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_query_execute_crud_operations\n============================================\ncreate_result: -1\ninsert_result_1: 1\ninsert_result_2: 1\nselect_result_1: [{'id': 1, 'name': 'Test'}, {'id': 2, 'name': 'Bob'}]\nupdate_result: 1\nselect_result_2: [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]\ninsert_result_3: 3\ndelete_result: 1\nselect_result_3: [{'id': 1, 'name': 'Alice'}, {'id': 3, 'name': 'Aska'}, {'id': 4, 'name': 'Felicia'}, {'id': 5, 'name': 'Grace'}]\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_query_execute_invalid_input(self, capsys):
        """ Ensure NewtSQL.query_execute() raises SystemExit on invalid argument types. """
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

        with pytest.raises(SystemExit) as exc_info_3:
            NewtSQL.query_execute("test.db", "SELECT 1", ["Test"])  # type: ignore
            print("This line will not be printed")
        assert exc_info_3.value.code == 1
        print("exc_info_3:", exc_info_3.value.code)

        with pytest.raises(SystemExit) as exc_info_4:
            NewtSQL.query_execute("test.db", "SELECT 1; SELECT 2;")
            print("This line will not be printed")
        assert exc_info_4.value.code == 1
        print("exc_info_4:", exc_info_4.value.code)

        with pytest.raises(SystemExit) as exc_info_5:
            NewtSQL.query_execute("test.db", "ALTER 1")
            print("This line will not be printed")
        assert exc_info_5.value.code == 1
        print("exc_info_5:", exc_info_5.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_query_execute_invalid_input\n============================================\nexc_info_1: 1\nexc_info_2: 1\nexc_info_3: 1\nexc_info_4: 1\nexc_info_5: 1\n" == captured.out
        assert "\x1b[1m\x1b[31m\nLocation: Newt.sql.query_execute : database > Newt.console.validate_type\n::: ERROR :::\nValue: 123\nReceived type: <class 'int'>\nExpected type: <class 'str'>\n\x1b[0m\n\x1b[1m\x1b[31m\nLocation: Newt.sql.query_execute : query > Newt.console.validate_type\n::: ERROR :::\nValue: 456\nReceived type: <class 'int'>\nExpected type: <class 'str'>\n\x1b[0m\n\x1b[1m\x1b[31m\nLocation: Newt.console.validate_type\n::: ERROR :::\nValue: Test\nReceived type: <class 'str'>\nExpected type: <class 'tuple'>\n\x1b[0m\n\x1b[1m\x1b[31m\nLocation: Newt.sql.query_execute : executemany\n::: ERROR :::\nAll items in 'params' list must be tuples for executemany().\nparams: ['Test']\n\x1b[0m\n\x1b[1m\x1b[31m\nLocation: Newt.sql.query_execute : parts_query\n::: ERROR :::\nSQL query must contain exactly one statement\n\x1b[0m\n\x1b[1m\x1b[31m\nLocation: Newt.sql.query_execute : dangerous_tokens\n::: ERROR :::\nSQL query contains potentially dangerous token: alter\n\x1b[0m\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 6

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


class TestSqlSelectRows:
    """ Tests for query_select function. """


    def test_query_select_basic(self, capsys):
        """ Ensure NewtSQL.query_select() returns all rows as a list. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create table
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT)")

            # Select empty
            select_result_1 = NewtSQL.query_select(file_db, "test")
            assert isinstance(select_result_1, list)
            assert len(select_result_1) == 0
            print("select_result_1:", select_result_1)

            # Insert multiple rows
            insert_query = "INSERT INTO test (id, name) VALUES (?, ?)"
            insert_params = [(1, 'Alice'), (2, 'Bob')]
            NewtSQL.query_execute(file_db, insert_query, insert_params)

            # Select rows
            select_result_2 = NewtSQL.query_select(file_db, "test")
            assert isinstance(select_result_2, list)
            assert len(select_result_2) == 2
            print("select_result_2:", select_result_2)

            # Select with WHERE clause
            select_result_3 = NewtSQL.query_select(
                file_db,
                "test",
                "*",
                "WHERE id = ?",
                (1,)
            )
            assert len(select_result_3) == 1
            assert select_result_3[0]["id"] == 1
            print("select_result_3:", select_result_3)

        finally:
            closed = NewtSQL.db_delayed_close(file_db)
            assert closed is True

            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_query_select_basic\n============================================\nselect_result_1: []\nselect_result_2: [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]\nselect_result_3: [{'id': 1, 'name': 'Alice'}]\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_query_select_invalid_query(self, capsys):
        """ Ensure NewtSQL.query_select() raises SystemExit on invalid SQL query. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            with pytest.raises(SystemExit) as exc_info_1:
                NewtSQL.query_select(file_db, "INVALID TABLE NAME")
                print("This line will not be printed")
            assert exc_info_1.value.code == 1
            print("exc_info_1:", exc_info_1.value.code)

            with pytest.raises(SystemExit) as exc_info_2:
                NewtSQL.query_select(file_db, "test", "*", "INVALID SQL QUERY")
                print("This line will not be printed")
            assert exc_info_2.value.code == 1
            print("exc_info_2:", exc_info_2.value.code)

        finally:
            closed = NewtSQL.db_delayed_close(file_db)
            assert closed is True

            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_query_select_invalid_query\n============================================\nexc_info_1: 1\nexc_info_2: 1\n" == captured.out
        assert "\x1b[1m\x1b[31m\nLocation: Newt.sql.query_execute : OperationalError in Syntax\n::: ERROR :::\nSyntax error: near \"TABLE\": syntax error\n\x1b[0m\n\x1b[1m\x1b[31m\nLocation: Newt.sql.query_select : result > Newt.console.validate_type\n::: ERROR :::\nValue: None\nReceived type: <class \'NoneType\'>\nExpected type: <class \'list\'>\n\x1b[0m\n\x1b[1m\x1b[31m\nLocation: Newt.sql.query_execute : OperationalError in Syntax\n::: ERROR :::\nSyntax error: near \"SQL\": syntax error\n\x1b[0m\n\x1b[1m\x1b[31m\nLocation: Newt.sql.query_select : result > Newt.console.validate_type\n::: ERROR :::\nValue: None\nReceived type: <class \'NoneType\'>\nExpected type: <class \'list\'>\n\x1b[0m\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 4

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


class TestSqlInsertRow:
    """ Tests for query_insert function. """


    def test_query_insert_dict_and_list(self, capsys):
        """ Ensure NewtSQL.query_insert() inserts a dict or list of dicts correctly. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create table
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT)")

            # Insert single row
            insert_data_1 = {"id": 1, "name": "Alice"}
            print("insert_data_1:", insert_data_1)
            insert_result_1 = NewtSQL.query_insert(file_db, "test", insert_data_1)
            assert insert_result_1 == 1
            print("insert_result_1:", insert_result_1)

            # Insert multiple rows
            insert_data_2 = [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"},
                {"id": 3, "name": "Charlie"}
            ]
            print("insert_data_2:", insert_data_2)
            insert_result_2 = NewtSQL.query_insert(file_db, "test", insert_data_2)
            assert insert_result_2 == 3
            print("insert_result_2:", insert_result_2)

            # Empty Insert
            insert_data_3 = {}
            print("insert_data_3:", insert_data_3)
            insert_result_3 = NewtSQL.query_insert(file_db, "test", insert_data_3)
            assert insert_result_3 == 0
            print("insert_result_3:", insert_result_3)

            # Select with no data
            select_result = NewtSQL.query_select(file_db, "test")
            assert len(select_result) == 4
            print("select_result:", select_result)

        finally:
            closed = NewtSQL.db_delayed_close(file_db)
            assert closed is True

            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_query_insert_dict_and_list\n============================================\ninsert_data_1: {'id': 1, 'name': 'Alice'}\ninsert_result_1: 1\ninsert_data_2: [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}, {'id': 3, 'name': 'Charlie'}]\ninsert_result_2: 3\ninsert_data_3: {}\ninsert_result_3: 0\nselect_result: [{'id': 1, 'name': 'Alice'}, {'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}, {'id': 3, 'name': 'Charlie'}]\n" == captured.out
        assert "\x1b[1m\x1b[31m\nLocation: Newt.sql.query_insert : insert_data > Newt.console.validate_type : is_empty\n::: ERROR :::\nValue must not be empty\nValue: {}\nType: <class 'dict'>\n\x1b[0m\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_query_insert_invalid_input(self, capsys):
        """ Ensure NewtSQL.query_insert() returns 0 and logs error on empty data dict. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info_1:
            NewtSQL.query_insert(123, "test", {"id": 1})  # type: ignore
            print("This line will not be printed")
        assert exc_info_1.value.code == 1
        print("exc_info_1:", exc_info_1.value.code)

        with pytest.raises(SystemExit) as exc_info_2:
            NewtSQL.query_insert("test.db", 456, {"id": 2})  # type: ignore
            print("This line will not be printed")
        assert exc_info_2.value.code == 1
        print("exc_info_2:", exc_info_2.value.code)

        result_3 = NewtSQL.query_insert("test.db", "test", "not a dict")  # type: ignore
        print("result:", result_3)
        assert result_3 == 0

        insert_data_4 = [
            {"name": "Alice"},
            "not a dict",
            {"id": 3, "name": "Charlie"}
        ]
        with pytest.raises(SystemExit) as exc_info_4:
            NewtSQL.query_insert("test.db", "test", insert_data_4)
            print("This line will not be printed")
        assert exc_info_4.value.code == 1
        print("exc_info_4:", exc_info_4.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_query_insert_invalid_input\n============================================\nexc_info_1: 1\nexc_info_2: 1\nresult: 0\nexc_info_4: 1\n" == captured.out
        assert "\x1b[1m\x1b[31m\nLocation: Newt.sql.query_execute : database > Newt.console.validate_type\n::: ERROR :::\nValue: 123\nReceived type: <class 'int'>\nExpected type: <class 'str'>\n\x1b[0m\n\x1b[1m\x1b[31m\nLocation: Newt.sql.query_insert : table > Newt.console.validate_type\n::: ERROR :::\nValue: 456\nReceived type: <class 'int'>\nExpected type: <class 'str'>\n\x1b[0m\n\x1b[1m\x1b[31m\nLocation: Newt.sql.query_insert : insert_data > Newt.console.validate_type\n::: ERROR :::\nValue: not a dict\nReceived type: <class 'str'>\nExpected type: (<class 'dict'>, <class 'list'>)\n\x1b[0m\n\x1b[1m\x1b[31m\nLocation: Newt.sql.query_insert : data_row > Newt.console.validate_type\n::: ERROR :::\nValue: not a dict\nReceived type: <class 'str'>\nExpected type: <class 'dict'>\n\x1b[0m\n\x1b[1m\x1b[31m\nLocation: Newt.sql.query_insert : data_row > Newt.utility.check_dict_keys\n::: ERROR :::\nData keys: id, name\nMissing keys: \nUnexpected keys: id\n\x1b[0m\n\x1b[1m\x1b[31m\nLocation: Newt.sql.query_insert : expected_keys\n::: ERROR :::\nAll dictionaries must have identical keys and same length\nExpected keys: name\n\x1b[0m\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 6

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


class TestSqlUpdateRows:
    """ Tests for query_update function. """


    def test_query_update_basic(self, capsys):
        """ Ensure NewtSQL.query_update() updates a row by condition and returns 1. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        try:
            # Create table and insert data
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT, age INTEGER)")
            insert_data_1 = [
                {"id": 1, "name": "Alice", "age": 30},
                {"id": 2, "name": "Bob", "age": 35},
                {"id": 3, "name": "Charlie", "age": 40}
            ]
            print("insert_data_1:", insert_data_1)
            NewtSQL.query_insert(file_db, "test", insert_data_1)

            # Select with no data
            select_result_1 = NewtSQL.query_select(file_db, "test")
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
            print("select_result_1:", select_result_1)

            # Update row
            update_result_2 = NewtSQL.query_update(
                file_db,
                "test",
                {"age": 31},
                "id = ?",
                (1,)
            )
            assert update_result_2 == 1
            print("update_result_2:", update_result_2)

            # Verify update
            select_result_2 = NewtSQL.query_select(file_db, "test")
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
            print("select_result_2:", select_result_2)

            # Update multiple columns
            update_result_3 = NewtSQL.query_update(
                file_db,
                "test",
                {"name": "Alice Updated", "age": 32},
                "id = ?",
                (1,)
            )
            print("update_result_3:", update_result_3)
            assert update_result_3 == 1

            # Update multiple columns
            update_result_4 = NewtSQL.query_update(
                file_db,
                "test",
                {"name": "Updated"},
                "id = ?",
                (999,)
            )
            print("update_result_4:", update_result_4)
            assert update_result_4 == 0

        finally:
            closed = NewtSQL.db_delayed_close(file_db)
            assert closed is True

            if os.path.exists(file_db):
                os.unlink(file_db)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_query_update_basic\n============================================\ninsert_data_1: [{'id': 1, 'name': 'Alice', 'age': 30}, {'id': 2, 'name': 'Bob', 'age': 35}, {'id': 3, 'name': 'Charlie', 'age': 40}]\nselect_result_1: [{'id': 1, 'name': 'Alice', 'age': 30}, {'id': 2, 'name': 'Bob', 'age': 35}, {'id': 3, 'name': 'Charlie', 'age': 40}]\nupdate_result_2: 1\nselect_result_2: [{'id': 1, 'name': 'Alice', 'age': 31}, {'id': 2, 'name': 'Bob', 'age': 35}, {'id': 3, 'name': 'Charlie', 'age': 40}]\nupdate_result_3: 1\nupdate_result_4: 0\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_query_update_invalid_input(self, capsys):
        """ Ensure NewtSQL.query_update() raises SystemExit on invalid argument types. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info_1:
            NewtSQL.query_update(
                "file.db",
                "test",
                {},
                "id = ?",
                (1,)
            )
            print("This line will not be printed")
        assert exc_info_1.value.code == 1
        print("exc_info_1:", exc_info_1.value.code)

        with pytest.raises(SystemExit) as exc_info_2:
            NewtSQL.query_update(
                123,  # type: ignore
                "test",
                {"name": "test"},
                "id = ?",
                (1,)
            )
            print("This line will not be printed")
        assert exc_info_2.value.code == 1
        print("exc_info_2:", exc_info_2.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_query_update_invalid_input\n============================================\nexc_info_1: 1\nexc_info_2: 1\n" == captured.out
        assert "\x1b[1m\x1b[31m\nLocation: Newt.sql.query_update : set_data > Newt.console.validate_type : is_empty\n::: ERROR :::\nValue must not be empty\nValue: {}\nType: <class 'dict'>\n\x1b[0m\n\x1b[1m\x1b[31m\nLocation: Newt.sql.query_execute : database > Newt.console.validate_type\n::: ERROR :::\nValue: 123\nReceived type: <class 'int'>\nExpected type: <class 'str'>\n\x1b[0m\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 2

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err































class TestExportSqlQueryToCsv:
    """ Tests for export_sql_query_to_csv function. """


    def test_export_sql_query_to_csv_basic(self, capsys):
        """ Ensure NewtSQL.export_sql_query_to_csv() exports query results to a CSV file. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmpfile:
            file_db = tmpfile.name

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmpfile:
            file_csv = tmpfile.name

        try:
            # Create table and insert data
            NewtSQL.query_execute(file_db, "CREATE TABLE test (id INTEGER, name TEXT, age INTEGER)")

            # Insert multiple rows
            insert_data = [
                {"id": 2, "name": "Bob", "age": 35},
                {"id": 1, "name": "Alice", "age": 30},
                {"id": 3, "name": "Charlie", "age": 40}
            ]
            NewtSQL.query_insert(file_db, "test", insert_data)

            # Export to CSV
            result = NewtSQL.export_sql_query_to_csv(
                file_db,
                file_csv,
                "test",
                "*",
                "ORDER BY id",
                obscure_list=obscure_list
            )
            assert result is True
            assert os.path.exists(file_csv)
            print("result:", result)

            # Verify CSV content
            csv_data = NewtFiles.read_csv_from_file(file_csv, obscure_list=obscure_list)
            assert isinstance(csv_data, list)
            assert len(csv_data) == 4  # Header + 3 rows
            assert csv_data[0][0] == "id"
            assert csv_data[0][1] == "name"
            assert csv_data[0][2] == "age"
            assert csv_data[1][0] == "1"
            assert csv_data[1][1] == "Alice"
            assert csv_data[1][2] == "30"
            assert csv_data[2][0] == "2"
            assert csv_data[2][1] == "Bob"
            assert csv_data[2][2] == "35"
            assert csv_data[3][0] == "3"
            assert csv_data[3][1] == "Charlie"
            assert csv_data[3][2] == "40"
            print("csv_data:", csv_data)

        finally:
            closed = NewtSQL.db_delayed_close(file_db)
            assert closed is True

            if os.path.exists(file_db):
                os.unlink(file_db)
            if os.path.exists(file_csv):
                os.unlink(file_csv)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.csv"
        else:
            file_obscure_name = "/tmp/***********.csv"

        assert "Function: test_export_sql_query_to_csv_basic\n============================================\n[Newt.files.save_csv_to_file] Saved CSV to file:\n" + file_obscure_name + "\n(rows=4, mode=write, delimiter=';')\nresult: True\n[Newt.files.read_csv_from_file] Loaded CSV from file:\n" + file_obscure_name + "\n(rows=4, delimiter=';')\ncsv_data: [['id', 'name', 'age'], ['1', 'Alice', '30'], ['2', 'Bob', '35'], ['3', 'Charlie', '40']]\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_export_sql_query_to_csv_invalid_input(self, capsys):
        """ Ensure NewtSQL.export_sql_query_to_csv() raises SystemExit on invalid argument types. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info_1:
            NewtSQL.export_sql_query_to_csv(
                123,  # type: ignore
                "test.csv",
                "SELECT 1"
            )
            print("This line will not be printed")
        assert exc_info_1.value.code == 1
        print("exc_info_1:", exc_info_1.value.code)

        with pytest.raises(SystemExit) as exc_info_2:
            NewtSQL.export_sql_query_to_csv(
                "test.db",
                "test.csv",
                456  # type: ignore
            )
            print("This line will not be printed")
        assert exc_info_2.value.code == 1
        print("exc_info_2:", exc_info_2.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_export_sql_query_to_csv_invalid_input\n============================================\nexc_info_1: 1\nexc_info_2: 1\n" == captured.out
        assert "\x1b[1m\x1b[31m\nLocation: Newt.sql.query_execute : database > Newt.console.validate_type\n::: ERROR :::\nValue: 123\nReceived type: <class 'int'>\nExpected type: <class 'str'>\n\x1b[0m\n\x1b[1m\x1b[31m\nLocation: Newt.sql.query_select : table > Newt.console.validate_type\n::: ERROR :::\nValue: 456\nReceived type: <class 'int'>\nExpected type: <class 'str'>\n\x1b[0m\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 2

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err
