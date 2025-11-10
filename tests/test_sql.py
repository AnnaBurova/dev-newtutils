"""
Comprehensive unit tests for newtutils.sql module.

Tests cover:
- Database delayed close (db_delayed_close)
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
