"""
Updated on 2026-02
Created on 2025-11

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.files module.

Tests cover:
- TestEnsureDirExists
- TestCheckFileExists
- TestNormalizeNewlines
- TestChooseFileFromFolder
- TestTextFiles
- TestConvertStrToJson
- TestJsonFiles
- TestCsvFiles
"""

import pytest
import tempfile
from unittest.mock import patch

import os

from helpers import print_my_func_name, print_my_captured
import newtutils.files as NewtFiles


class TestEnsureDirExists:
    """ Tests for ensure_dir_exists function. """


    def test_creates_nested_directory(self, capsys):
        """ Test ensure_dir_exists creates nested parent directories. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = os.path.join(tmpdir, "level1", "level2", "file.txt")

            NewtFiles.ensure_dir_exists(nested_path)
            assert os.path.exists(os.path.dirname(nested_path))

        assert not os.path.exists(os.path.dirname(nested_path))

        captured = capsys.readouterr()
        print_my_captured(captured)

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_handles_current_directory(self, capsys):
        """ Verify NewtFiles.ensure_dir_exists() skips dir creation and errors for current dir files. """
        print_my_func_name()

        file_path = "file.txt"
        NewtFiles.ensure_dir_exists(file_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


class TestCheckFileExists:
    """ Tests for check_file_exists function. """


    def test_existing_file_returns(self, capsys):
        """ Test NewtFiles.check_file_exists(): True for existing, False for missing, SystemExit with stop=True. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test")
            tmp_path = tmp.name

        try:
            assert NewtFiles.check_file_exists(tmp_path) is True

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        with pytest.raises(SystemExit) as exc_info:
            NewtFiles.check_file_exists(tmp_path)
            print("This line will not be printed")
        assert exc_info.value.code == 1

        assert NewtFiles.check_file_exists(tmp_path, stop=False) is False

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.files.check_file_exists : logging\n" in captured.out
        assert "\nFile not found: C:\\Users\\" in captured.out
        # Expected absence of result
        assert "\nThis line will not be printed\n" not in captured.out


    def test_invalid_filepath_raises_exit(self, capsys):
        """ Test NewtFiles.check_file_exists() raises SystemExit or returns False for invalid input. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info:
            NewtFiles.check_file_exists(123)  # type: ignore
            print("This line will not be printed")
        assert exc_info.value.code == 1

        assert NewtFiles.check_file_exists("123", stop=False) is False

        assert NewtFiles.check_file_exists("abc", stop=False, logging=False) is False

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.files.check_file_exists : file_path\n" in captured.out
        assert "\nExpected <class 'str'>, got <class 'int'>\n" in captured.out
        assert "\nValue: 123\n" in captured.out
        assert "\nLocation: Newt.files.check_file_exists : logging\n" in captured.out
        assert "\nFile not found: 123\n" in captured.out
        # Expected absence of result
        assert "\nThis line will not be printed\n" not in captured.out
        assert "\nFile not found: abc\n" not in captured.out


class TestNormalizeNewlines:
    """ Tests for _normalize_newlines function. """


    def test_converts_windows_newlines(self, capsys):
        """ Test NewtFiles._normalize_newlines() converts Windows CRLF to Unix LF. """
        print_my_func_name()

        text = "line1\r\nline2\r\nline3\r\n"
        print(repr(text))

        result = NewtFiles._normalize_newlines(text)
        print(repr(result))
        assert result == "line1\nline2\nline3"

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n'line1\\r\\nline2\\r\\nline3\\r\\n'\n'line1\\nline2\\nline3'\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


class TestChooseFileFromFolder:
    """ Tests for choose_file_from_folder function. """


    def test_nonexistent_folder_raises_exit(self, capsys):
        """ Test NewtFiles.choose_file_from_folder() raises SystemExit for nonexistent folder. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info:
            NewtFiles.choose_file_from_folder("/nonexistent/folder")
            print("This line will not be printed")
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.files.choose_file_from_folder : folder_path not dir\n" in captured.out
        assert "\nFolder not found: /nonexistent/folder\n" in captured.out
        # Expected absence of result
        assert "\nThis line will not be printed\n" not in captured.out


    def test_empty_folder_raises_exit(self, capsys):
        """ Test NewtFiles.choose_file_from_folder() raises SystemExit for empty folder. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(SystemExit) as exc_info:
                NewtFiles.choose_file_from_folder(tmpdir)
                print("This line will not be printed")
            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.files.choose_file_from_folder : file_list empty\n" in captured.out
        assert "\nNo files found in this folder.\n" in captured.out
        # Expected absence of result
        assert "\nThis line will not be printed\n" not in captured.out


    @patch('newtutils.files.input', side_effect=["abc", "999", "X"])
    def test_user_cancel_x_raises_exit(self, mock_input, capsys):
        """ Test NewtFiles.choose_file_from_folder() raises SystemExit on user 'x' cancel. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create several files in the temporary directory
            for i in range(3):
                filepath = os.path.join(tmpdir, f"dummy_file_{i}.txt")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("dummy content\n")

            with pytest.raises(SystemExit) as exc_info:
                NewtFiles.choose_file_from_folder(tmpdir)
                print("This line will not be printed")
            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nAvailable files: 3\n" in captured.out
        assert "\n     1: dummy_file_0.txt\n" in captured.out
        assert "\n     2: dummy_file_1.txt\n" in captured.out
        assert "\n     3: dummy_file_2.txt\n" in captured.out
        assert "\n     X: Exit / Cancel\n" in captured.out
        assert "\n[INPUT]: abc\nInvalid input. Please enter a number.\n" in captured.out
        assert "\n[INPUT]: 999\nNumber out of range. Try again.\n" in captured.out
        assert "\n[INPUT]: x\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.files.choose_file_from_folder : choice = [X]\n" in captured.out
        assert "\nSelection cancelled.\n" in captured.out
        # Expected absence of result
        assert "\nThis line will not be printed\n" not in captured.out


    def test_invalid_folderpath_raises_exit(self, capsys):
        """ Test NewtFiles.choose_file_from_folder() raises SystemExit for invalid folder input. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info:
            NewtFiles.choose_file_from_folder(123)  # type: ignore
            print("This line will not be printed")
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.files.choose_file_from_folder : folder_path\n" in captured.out
        assert "\nExpected <class 'str'>, got <class 'int'>\n" in captured.out
        assert "\nValue: 123\n" in captured.out
        # Expected absence of result
        assert "\nThis line will not be printed\n" not in captured.out


class TestTextFiles:
    """ Tests for text file operations. """


    def test_save_and_read_text_file(self, capsys):
        """ Test NewtFiles.save_text_to_file() and read_text_from_file() work correctly. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
            tmp_path = tmp.name

        try:
            content = "Hello\nWorld!"
            NewtFiles.save_text_to_file(tmp_path, content, append=False)

            result = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result))

            # Note: save_text_to_file adds a newline at the end
            assert result == content + "\n"

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[Newt.files.save_text_to_file] Saved text to file:\n" in captured.out
        assert "\n(mode=write, length=13)\n" in captured.out
        assert "\n[Newt.files.read_text_from_file] Loaded text from file:\n" in captured.out
        assert "\n(length=13)\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_save_text_creates_directory(self, capsys):
        """ Test NewtFiles.save_text_to_file() creates parent directories if needed. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = os.path.join(tmpdir, "level1", "level2", "file.txt")
            NewtFiles.save_text_to_file(nested_path, "test", append=False)
            assert os.path.exists(nested_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[Newt.files.save_text_to_file] Saved text to file:\n" in captured.out
        assert "\n(mode=write, length=5)\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_save_text_append_mode(self, capsys):
        """ Test NewtFiles.save_text_to_file() append mode adds content correctly. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
            tmp_path = tmp.name

        try:
            NewtFiles.save_text_to_file(tmp_path, "Line 1\n", append=False)
            NewtFiles.save_text_to_file(tmp_path, "Line 2\n")

            result = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result))
            # New implementation normalizes and avoids extra blank lines
            assert result == "Line 1\nLine 2\n"

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[Newt.files.save_text_to_file] Saved text to file:\n" in captured.out
        assert "\n(mode=write, length=7)\n" in captured.out
        assert "\n[Newt.files.read_text_from_file] Loaded text from file:\n" in captured.out
        assert "\n(length=14)\n" in captured.out
        assert "\n'Line 1\\nLine 2\\n'\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_read_text_from_nonexistent_file(self, capsys):
        """ Test NewtFiles.read_text_from_file() raises SystemExit for nonexistent file. """
        print_my_func_name()

        result = NewtFiles.read_text_from_file("/nonexistent/file.txt", stop=False)
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.files.check_file_exists : logging\n" in captured.out
        assert "\nFile not found: /nonexistent/file.txt\n" in captured.out
        # Expected absence of result
        assert "\nThis line will not be printed\n" not in captured.out


    def test_save_text_normalizes_newlines(self, capsys):
        """ Test NewtFiles.save_text_to_file() normalizes Windows newlines to Unix LF. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
            tmp_path = tmp.name

        try:
            content = "line1\r\nline2\r\n"
            print(repr(content))

            NewtFiles.save_text_to_file(tmp_path, content, append=False)

            result = NewtFiles.read_text_from_file(tmp_path, logging=False)
            print(repr(result))
            # Should have Unix newlines
            assert result is not None
            assert "\r\n" not in result

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[Newt.files.save_text_to_file] Saved text to file:\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "\n[Newt.files.read_text_from_file] Loaded text from file:\n" not in captured.out


    def test_save_text_invalid_input(self, capsys):
        """ Test NewtFiles.save_text_to_file() raises SystemExit for invalid file/text inputs. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
            tmp_path = tmp.name

        try:
            with pytest.raises(SystemExit) as exc_info_1:
                # Invalid file_name
                NewtFiles.save_text_to_file(123, "test")  # type: ignore
                print("This line will not be printed 01")
            assert exc_info_1.value.code == 1

            with pytest.raises(SystemExit) as exc_info_2:
                # Invalid text
                NewtFiles.save_text_to_file(tmp_path, 456)  # type: ignore
                print("This line will not be printed 02")
            assert exc_info_2.value.code == 1

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.files.ensure_dir_exists : file_path\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.files.save_text_to_file : text\n" in captured.out
        assert "\nExpected <class 'str'>, got <class 'int'>\n" in captured.out
        assert "\nValue: 123\n" in captured.out
        assert "\nValue: 456\n" in captured.out
        # Expected absence of result
        assert "\nThis line will not be printed 01\n" not in captured.out
        assert "\nThis line will not be printed 02\n" not in captured.out


class TestConvertStrToJson:
    """Tests for convert_str_to_json function."""

    def test_parses_valid_json_dict(self, capsys):
        """Test parsing a valid JSON dictionary string."""
        print_my_func_name()

        json_str = '{"name": "test", "value": 123, "items": [1, 2, 3]}'
        print(repr(json_str))

        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert isinstance(result, dict)
        assert result == {"name": "test", "value": 123, "items": [1, 2, 3]}

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_parses_valid_json_list(self, capsys):
        """Test parsing a valid JSON list string."""
        print_my_func_name()

        json_str = '[1, 2, 3, {"key": "value"}]'
        print(repr(json_str))

        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert isinstance(result, list)
        assert result == [1, 2, 3, {"key": "value"}]

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_parses_single_quotes_dict(self, capsys):
        """Test parsing a dictionary string with single quotes."""
        print_my_func_name()

        json_str = "{'name': 'test', 'value': 123}"
        print(repr(json_str))

        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert isinstance(result, dict)
        assert result == {"name": "test", "value": 123}

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_parses_single_quotes_list(self, capsys):
        """Test parsing a list string with single quotes."""
        print_my_func_name()

        json_str = "['item1', 'item2', 'item3']"
        print(repr(json_str))

        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert isinstance(result, list)
        assert result == ["item1", "item2", "item3"]

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_returns_none_for_empty_string(self, capsys):
        """Test that empty string returns None."""
        print_my_func_name()

        result = NewtFiles.convert_str_to_json("")
        print(repr(result))
        assert result is None

        result = NewtFiles.convert_str_to_json("   ")
        print(repr(result))
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_returns_none_for_invalid_input(self, capsys):
        """Test that invalid input (not a string) returns None."""
        print_my_func_name()

        result = NewtFiles.convert_str_to_json(123)  # type: ignore
        print(repr(result))
        assert result is None

        result = NewtFiles.convert_str_to_json(None)  # type: ignore
        print(repr(result))
        assert result is None

        result = NewtFiles.convert_str_to_json(["not", "a", "string"])  # type: ignore
        print(repr(result))
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_returns_none_for_invalid_json(self, capsys):
        """Test that invalid JSON string returns None."""
        print_my_func_name()

        invalid_json = "{ invalid json }"
        print(repr(invalid_json))
        result = NewtFiles.convert_str_to_json(invalid_json)
        print(repr(result))
        assert result is None

        invalid_json = "not json at all"
        print(repr(invalid_json))
        result = NewtFiles.convert_str_to_json(invalid_json)
        print(repr(result))
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_returns_none_for_non_list_or_dict_json(self, capsys):
        """Test that JSON that is not a list or dict returns None."""
        print_my_func_name()

        json_str = '"just a string"'
        print(repr(json_str))
        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert result is None

        json_str = "123"
        print(repr(json_str))
        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert result is None

        json_str = "true"
        print(repr(json_str))
        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_handles_whitespace(self, capsys):
        """Test that whitespace around JSON is handled correctly."""
        print_my_func_name()

        json_str = '   {"key": "value"}   '
        print(repr(json_str))

        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert isinstance(result, dict)
        assert result == {"key": "value"}

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_handles_nested_structures(self, capsys):
        """Test parsing nested JSON structures."""
        print_my_func_name()

        json_str = '{"outer": {"inner": {"deep": [1, 2, 3]}}}'
        print(repr(json_str))

        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert isinstance(result, dict)
        assert result == {"outer": {"inner": {"deep": [1, 2, 3]}}}

        captured = capsys.readouterr()
        print_my_captured(captured)


class TestJsonFiles:
    """Tests for JSON file operations."""

    def test_save_and_read_json_dict(self, capsys):
        """Test saving and reading a JSON dictionary."""
        print_my_func_name()

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
        print_my_func_name()

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
        print_my_func_name()

        result = NewtFiles.read_json_from_file("/nonexistent/file.json")
        print(repr(result))
        assert result == []

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_save_json_creates_directory(self, capsys):
        """Test that save_json_to_file creates parent directories."""
        print_my_func_name()

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
        print_my_func_name()

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
        print_my_func_name()

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
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name

        try:
            with pytest.raises(SystemExit):
                # Invalid file_name
                NewtFiles.save_json_to_file(123, {"test": "data"})  # type: ignore

            with pytest.raises(SystemExit):
                # Invalid data (not list or dict)
                NewtFiles.save_json_to_file(tmp_path, "not a dict or list")  # type: ignore

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
        print_my_func_name()

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
        print_my_func_name()

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
        print_my_func_name()

        result = NewtFiles.read_csv_from_file("/nonexistent/file.csv")
        print(repr(result))
        assert result == []

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_save_csv_creates_directory(self, capsys):
        """Test that save_csv_to_file creates parent directories."""
        print_my_func_name()

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
        print_my_func_name()

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
        print_my_func_name()

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

    def test_save_csv_invalid_input(self, capsys):
        """Test that invalid input is handled gracefully."""
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp_path = tmp.name

        try:
            with pytest.raises(SystemExit):
                # Invalid file_name
                NewtFiles.save_csv_to_file(123, [["test"]])  # type: ignore

            with pytest.raises(SystemExit):
                # Invalid rows (not a list)
                NewtFiles.save_csv_to_file(tmp_path, "not a list")

            with pytest.raises(SystemExit):
                # Invalid delimiter
                NewtFiles.save_csv_to_file(tmp_path, [["test"]], delimiter=123)  # type: ignore

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            assert result_text == ""

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_read_csv_invalid_delimiter(self, capsys):
        """Test reading CSV with invalid delimiter returns empty list."""
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp.write("A;B\n1;2")
            tmp_path = tmp.name

        try:
            # Wrong delimiter
            result = NewtFiles.read_csv_from_file(tmp_path, delimiter=",")
            print(repr(result))
            print(repr(result[0][0]))
            # Should still read but with wrong parsing
            assert isinstance(result, list)
            assert isinstance(result[0][0], str)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)
