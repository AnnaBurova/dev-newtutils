"""
Created on 2025-11

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.files module.

Tests cover:
- Directory operations (_ensure_dir_exists)
"""

import tempfile

import os

import newtutils.files as NewtFiles


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


class TestEnsureDirExists:
    """Tests for _ensure_dir_exists function."""

    def test_creates_nested_directory(self, capsys):
        """Test that nested directories are created."""
        print_my_func_name("test_creates_nested_directory")

        nested_path = ""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = os.path.join(tmpdir, "level1", "level2", "file.txt")
            NewtFiles._ensure_dir_exists(nested_path)
            assert os.path.exists(os.path.dirname(nested_path))

        assert not os.path.exists(os.path.dirname(nested_path))

        captured = capsys.readouterr()
        print_my_captured(captured)
