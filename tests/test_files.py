"""
Created on 2025-11

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.files module.

Tests cover:
- Directory operations (_ensure_dir_exists)
- File existence checks (_check_file_exists)
- Newline normalization (_normalize_newlines)
- File selection (choose_file_from_folder)
- Text file operations (read_text_from_file, save_text_to_file)
- JSON file operations (read_json_from_file, save_json_to_file)
- CSV file operations (read_csv_from_file, save_csv_to_file)
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

    def test_returns_none_for_input_zero(self, monkeypatch, capsys):
        """Test that non empty folder returns on input zero."""
        print_my_func_name("test_returns_none_for_input_zero")

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create several files in the temporary directory
            for i in range(3):
                filepath = os.path.join(tmpdir, f"dummy_file_{i}.txt")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("dummy content\n")

            # Mock input to cancel immediately
            monkeypatch.setattr('builtins.input', lambda _: "0")

            result = NewtFiles.choose_file_from_folder(tmpdir)
            assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_returns_none_for_invalid_input(self, capsys):
        """Test that invalid input returns None."""
        print_my_func_name("test_returns_none_for_invalid_input")

        with pytest.raises(SystemExit):
            result = NewtFiles.choose_file_from_folder(123)  # type: ignore
            print("This line will not be printed:", result)

        captured = capsys.readouterr()
        print_my_captured(captured)


class TestTextFiles:
    """Tests for text file operations."""

    def test_save_and_read_text_file(self, capsys):
        """Test saving and reading a text file."""
        print_my_func_name("test_save_and_read_text_file")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
            tmp_path = tmp.name

        try:
            content = "Hello\nWorld!"
            NewtFiles.save_text_to_file(tmp_path, content)

            result = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result))

            # Note: save_text_to_file adds a newline at the end
            assert result == content + "\n"

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_save_text_creates_directory(self, capsys):
        """Test that save_text_to_file creates parent directories."""
        print_my_func_name("test_save_text_creates_directory")

        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = os.path.join(tmpdir, "level1", "level2", "file.txt")
            NewtFiles.save_text_to_file(nested_path, "test")
            assert os.path.exists(nested_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_save_text_append_mode(self, capsys):
        """Test appending to a text file."""
        print_my_func_name("test_save_text_append_mode")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
            tmp_path = tmp.name

        try:
            NewtFiles.save_text_to_file(tmp_path, "Line 1\n")
            NewtFiles.save_text_to_file(tmp_path, "Line 2\n", append=True)

            result = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result))
            assert "Line 1" in result
            assert "Line 2" in result
            assert result == "Line 1\n\nLine 2\n\n"

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_read_text_from_nonexistent_file(self, capsys):
        """Test reading from non-existent file returns empty string."""
        print_my_func_name("test_read_text_from_nonexistent_file")

        result = NewtFiles.read_text_from_file("/nonexistent/file.txt")
        print(repr(result))
        assert result == ""

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_save_text_normalizes_newlines(self, capsys):
        """Test that save_text_to_file normalizes newlines."""
        print_my_func_name("test_save_text_normalizes_newlines")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
            tmp_path = tmp.name

        try:
            content = "line1\r\nline2\r\n"
            print(repr(content))

            NewtFiles.save_text_to_file(tmp_path, content)

            result = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result))
            # Should have Unix newlines
            assert "\r\n" not in result

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_save_text_invalid_input(self, capsys):
        """Test that invalid input is handled gracefully."""
        print_my_func_name("test_save_text_invalid_input")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
            tmp_path = tmp.name

        try:
            # Invalid file_name
            NewtFiles.save_text_to_file(123, "test")  # type: ignore
            # Invalid text
            NewtFiles.save_text_to_file(tmp_path, 456)  # type: ignore
            # Should not raise, but file should not be edited with invalid input

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)


class TestJsonFiles:
    """Tests for JSON file operations."""

    def test_save_and_read_json_dict(self, capsys):
        """Test saving and reading a JSON dictionary."""
        print_my_func_name("test_save_and_read_json_dict")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name

        try:
            data = {"name": "test", "value": 123, "items": [1, 2, 3]}
            print(repr(data))

            NewtFiles.save_json_to_file(tmp_path, data)

            result_json = NewtFiles.read_json_from_file(tmp_path)
            print(repr(result_json))
            assert result_json == data

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            print(result_text)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_save_and_read_json_list(self, capsys):
        """Test saving and reading a JSON list."""
        print_my_func_name("test_save_and_read_json_list")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name

        try:
            data = [1, 2, 3, {"key": "value"}]
            print(repr(data))

            NewtFiles.save_json_to_file(tmp_path, data)

            result_json = NewtFiles.read_json_from_file(tmp_path)
            print(repr(result_json))
            assert result_json == data

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            print(result_text)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_read_json_from_nonexistent_file(self, capsys):
        """Test reading from non-existent JSON file returns empty list."""
        print_my_func_name("test_read_json_from_nonexistent_file")

        result = NewtFiles.read_json_from_file("/nonexistent/file.json")
        print(repr(result))
        assert result == []

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_save_json_creates_directory(self, capsys):
        """Test that save_json_to_file creates parent directories."""
        print_my_func_name("test_save_json_creates_directory")

        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = os.path.join(tmpdir, "level1", "level2", "file.json")

            data = {"test": "data"}
            print(repr(data))

            NewtFiles.save_json_to_file(nested_path, data)
            assert os.path.exists(nested_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_save_json_custom_indent(self, capsys):
        """Test saving JSON with custom indent."""
        print_my_func_name("test_save_json_custom_indent")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name

        try:
            data = {"a": 1, "b": 2}
            print(repr(data))
            NewtFiles.save_json_to_file(tmp_path, data, indent=4)

            result_json = NewtFiles.read_json_from_file(tmp_path)
            print(repr(result_json))
            assert result_json == data

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            print(result_text)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_read_json_invalid_file(self, capsys):
        """Test reading invalid JSON returns empty list."""
        print_my_func_name("test_read_json_invalid_file")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp.write("{ invalid json }")
            tmp_path = tmp.name

        try:
            with pytest.raises(SystemExit):
                result = NewtFiles.read_json_from_file(tmp_path)
                print("This line will not be printed:", result)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_save_json_invalid_input(self, capsys):
        """Test that invalid input is handled gracefully."""
        print_my_func_name("test_save_json_invalid_input")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name

        try:
            # Invalid file_name
            NewtFiles.save_json_to_file(123, {"test": "data"})  # type: ignore
            # Invalid data (not list or dict)
            NewtFiles.save_json_to_file(tmp_path, "not a dict or list")  # type: ignore
            # Should not raise

            with pytest.raises(SystemExit):
                result_json = NewtFiles.read_json_from_file(tmp_path)
                print("This line will not be printed:", result_json)

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            assert result_text == ""

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)


class TestCsvFiles:
    """Tests for CSV file operations."""

    def test_save_and_read_csv(self, capsys):
        """Test saving and reading a CSV file."""
        print_my_func_name("test_save_and_read_csv")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp_path = tmp.name

        try:
            rows = [
                ["Name", "Age", "City"],
                ["Alice", "30", "New York"],
                ["Bob", "25", "London"]
            ]
            print(repr(rows))

            NewtFiles.save_csv_to_file(tmp_path, rows)

            result_csv = NewtFiles.read_csv_from_file(tmp_path)
            print(repr(result_csv))
            assert result_csv == rows

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            print(result_text)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_save_and_read_csv_custom_delimiter(self, capsys):
        """Test saving and reading CSV with custom delimiter."""
        print_my_func_name("test_save_and_read_csv_custom_delimiter")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp_path = tmp.name

        try:
            rows = [["A", "B"], ["1", "2"]]
            print(repr(rows))

            NewtFiles.save_csv_to_file(tmp_path, rows, delimiter=",")

            result_csv = NewtFiles.read_csv_from_file(tmp_path, delimiter=",")
            print(repr(result_csv))
            assert result_csv == rows

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            print(result_text)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_read_csv_from_nonexistent_file(self, capsys):
        """Test reading from non-existent CSV file returns empty list."""
        print_my_func_name("test_read_csv_from_nonexistent_file")

        result = NewtFiles.read_csv_from_file("/nonexistent/file.csv")
        print(repr(result))
        assert result == []

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_save_csv_creates_directory(self, capsys):
        """Test that save_csv_to_file creates parent directories."""
        print_my_func_name("test_save_csv_creates_directory")

        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = os.path.join(tmpdir, "level1", "level2", "file.csv")

            rows = [["Header"], ["Data"]]
            print(repr(rows))

            NewtFiles.save_csv_to_file(nested_path, rows)
            assert os.path.exists(nested_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_save_csv_normalizes_newlines_in_cells(self, capsys):
        """Test that CSV cells with Windows newlines are normalized."""
        print_my_func_name("test_save_csv_normalizes_newlines_in_cells")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp_path = tmp.name

        try:
            rows = [["Cell1\r\nLine2", "Cell2"]]
            print(repr(rows))

            NewtFiles.save_csv_to_file(tmp_path, rows)

            result_csv = NewtFiles.read_csv_from_file(tmp_path)
            print(repr(result_csv))
            # Check that newlines are normalized
            assert "\r\n" not in result_csv[0][0]

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            print(result_text)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_save_csv_with_various_types(self, capsys):
        """Test saving CSV with various data types."""
        print_my_func_name("test_save_csv_with_various_types")

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp_path = tmp.name

        try:
            rows = [["String", 123, 45.67, True]]
            print(repr(rows))

            NewtFiles.save_csv_to_file(tmp_path, rows)

            result_csv = NewtFiles.read_csv_from_file(tmp_path)
            print(repr(result_csv))
            # All values should be strings in CSV
            assert all(isinstance(cell, str) for row in result_csv for cell in row)

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            print(result_text)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)
