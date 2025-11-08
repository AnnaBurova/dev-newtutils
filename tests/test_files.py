"""
Created on 2025-11

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.files module.

Tests cover:
- Directory operations (_ensure_dir_exists)
- File existence checks (_check_file_exists)
- Newline normalization (_normalize_newlines)
- File selection (choose_file_from_folder)
"""

import pytest
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

        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = os.path.join(tmpdir, "level1", "level2", "file.txt")
            NewtFiles._ensure_dir_exists(nested_path)
            assert os.path.exists(os.path.dirname(nested_path))

        assert not os.path.exists(os.path.dirname(nested_path))

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_handles_existing_directory(self, capsys):
        """Test that existing directories don't cause errors."""
        print_my_func_name("test_handles_existing_directory")

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "file.txt")
            NewtFiles._ensure_dir_exists(file_path)
            # Call again - should not raise
            NewtFiles._ensure_dir_exists(file_path)
            assert os.path.exists(tmpdir)

        assert not os.path.exists(os.path.dirname(file_path))

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_handles_current_directory(self, capsys):
        """Test that empty dir_path (current dir) is handled."""
        print_my_func_name("test_handles_current_directory")

        file_path = "file.txt"
        # Should not raise
        NewtFiles._ensure_dir_exists(file_path)

        captured = capsys.readouterr()
        print_my_captured(captured)


class TestCheckFileExists:
    """Tests for _check_file_exists function."""

    def test_returns_true_for_existing_file(self, capsys):
        """Test that existing files return True."""
        print_my_func_name("test_returns_true_for_existing_file")

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test")
            tmp_path = tmp.name

        try:
            assert NewtFiles._check_file_exists(tmp_path) is True
        finally:
            os.unlink(tmp_path)

        assert NewtFiles._check_file_exists(tmp_path) is False

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_returns_false_for_invalid_input(self, capsys):
        """Test that invalid input returns False."""
        print_my_func_name("test_returns_false_for_invalid_input")

        assert NewtFiles._check_file_exists(123) is False  # type: ignore

        captured = capsys.readouterr()
        print_my_captured(captured)


class TestNormalizeNewlines:
    """Tests for _normalize_newlines function."""

    def test_converts_windows_newlines(self, capsys):
        """Test that Windows newlines are converted."""
        print_my_func_name("test_converts_windows_newlines")

        text = "line1\r\nline2\r\nline3"
        print(repr(text))
        result = NewtFiles._normalize_newlines(text)
        print(repr(result))
        assert result == "line1\nline2\nline3"

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_preserves_unix_newlines(self, capsys):
        """Test that Unix newlines are preserved."""
        print_my_func_name("test_preserves_unix_newlines")

        text = "line1\nline2\nline3"
        print(repr(text))
        result = NewtFiles._normalize_newlines(text)
        print(repr(result))
        assert result == text

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_handles_mixed_newlines(self, capsys):
        """Test that mixed newlines are normalized."""
        print_my_func_name("test_handles_mixed_newlines")

        text = "line1\r\nline2\nline3\r\n"
        print(repr(text))
        result = NewtFiles._normalize_newlines(text)
        print(repr(result))
        assert result == "line1\nline2\nline3\n"

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_handles_empty_string(self, capsys):
        """Test that empty string is handled."""
        print_my_func_name("test_handles_empty_string")

        assert NewtFiles._normalize_newlines("") == ""

        captured = capsys.readouterr()
        print_my_captured(captured)


class TestChooseFileFromFolder:
    """Tests for choose_file_from_folder function."""

    def test_returns_none_for_nonexistent_folder(self, capsys):
        """Test that non-existent folder returns None."""
        print_my_func_name("test_returns_none_for_nonexistent_folder")

        with pytest.raises(SystemExit):
            result = NewtFiles.choose_file_from_folder("/nonexistent/folder")
            print("This line will not be printed:", result)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_returns_none_for_empty_folder(self, capsys):
        """Test that empty folder returns None."""
        print_my_func_name("test_returns_none_for_empty_folder")

        with tempfile.TemporaryDirectory() as tmpdir:
            result = NewtFiles.choose_file_from_folder(tmpdir)
            assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)
