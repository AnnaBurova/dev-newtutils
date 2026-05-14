"""
Updated on 2026-05
Created on 2025-11

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.files module.

Tests cover:
- TestNormalizeNewlines
- TestObscureLogic
- TestEnsureDirExists
- TestCheckFileExists
- TestChooseFileFromFolder
- TestTextFiles
- TestConvertStrToJson
- TestJsonFiles
- TestCsvFiles
"""

import sys
import os
import pytest
import tempfile
from unittest.mock import patch

from .helpers import print_my_func_name, print_my_captured
import newtutils.files as NewtFiles


class TestNormalizeNewlines:
    """ Tests for _normalize_newlines function. """


    def test_normalize_newlines_converts_windows(self, capsys):
        """ Ensure NewtFiles._normalize_newlines() converts Windows CRLF to Unix LF. """
        print_my_func_name()

        text_1 = "line1\r\nline2\r\nline3\r\nline4\r\nline5\r\n"
        print("text_1:", repr(text_1))

        result_1 = NewtFiles._normalize_newlines(text_1)
        print("result_1:", repr(result_1))
        assert result_1 == "line1\nline2\nline3\nline4\nline5\n"

        text_2 = "    line1\r\nline2\nline3\r\nline4\rline5\r\n"
        print("text_2:", repr(text_2))

        result_2 = NewtFiles._normalize_newlines(text_2)
        print("result_2:", repr(result_2))
        assert result_2 == "    line1\nline2\nline3\nline4\nline5\n"

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_normalize_newlines_converts_windows" \
        "\n============================================" \
        "\ntext_1: 'line1\\r\\nline2\\r\\nline3\\r\\nline4\\r\\nline5\\r\\n'" \
        "\nresult_1: 'line1\\nline2\\nline3\\nline4\\nline5\\n'" \
        "\ntext_2: '    line1\\r\\nline2\\nline3\\r\\nline4\\rline5\\r\\n'" \
        "\nresult_2: '    line1\\nline2\\nline3\\nline4\\nline5\\n'" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


class TestObscureLogic:
    """ Tests for _obscure_logic function. """

    def test_obscure_logic_masks_path_segments(self, capsys):
        """ Ensure NewtFiles._obscure_logic() masks path segments with asterisks. """
        print_my_func_name()

        if sys.platform == "win32" and os.name == "nt":
            file_name = "C:\\Users\\abcdefg\\AppData\\Local\\Temp\\1234567890"
        else:
            file_name = "/tmp/1234567890"

        obscure_list = [
            "C:\\Users\\",
            "\\AppData\\Local\\Temp\\",
            "/tmp/",
            ]
        file_not_found = NewtFiles._obscure_logic(file_name, obscure_list)

        if sys.platform == "win32" and os.name == "nt":
            assert file_not_found == "C:\\Users\\*******\\AppData\\Local\\Temp\\**********"
        else:
            assert file_not_found == "/tmp/**********"
        print("file_not_found:", file_not_found)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_obscure_logic_masks_path_segments" \
        "\n============================================" \
        "\nfile_not_found: " + file_not_found + \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


class TestEnsureDirExists:
    """ Tests for ensure_dir_exists function. """


    def test_ensure_dir_exists_empty_path(self, capsys):
        """ Ensure NewtFiles.ensure_dir_exists() raises SystemExit on empty path. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info:
            NewtFiles.ensure_dir_exists("")
            print("This line will not be printed")
        assert exc_info.value.code == 1
        print("exc_info:", exc_info.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_ensure_dir_exists_empty_path" \
        "\n============================================" \
        "\nexc_info: 1" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.ensure_dir_exists : file_path" \
        " > Newt.console.validate_type : is_empty" \
        "\n::: ERROR :::" \
        "\nValue must not be empty" \
        "\nValue: \nType: <class 'str'>" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


    def test_ensure_dir_exists_current_directory(self, capsys):
        """ Ensure NewtFiles.ensure_dir_exists() handles current-directory file paths without errors. """
        print_my_func_name()

        file_path = "file.txt"
        NewtFiles.ensure_dir_exists(file_path)

        dirname_exists = os.path.exists(os.path.dirname(file_path))
        assert dirname_exists is False
        print("dirname_exists:", dirname_exists)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_ensure_dir_exists_current_directory" \
        "\n============================================" \
        "\ndirname_exists: False" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_ensure_dir_exists_directory_exists(self, capsys):
        """ Ensure NewtFiles.ensure_dir_exists() skips makedirs when directory already exists. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "file.txt")

            dirname_exists = os.path.exists(os.path.dirname(file_path))
            assert dirname_exists is True
            print("dirname_exists:", dirname_exists)

            NewtFiles.ensure_dir_exists(file_path)

            dirname_exists = os.path.exists(os.path.dirname(file_path))
            assert dirname_exists is True
            print("dirname_exists:", dirname_exists)

        dirname_exists = os.path.exists(os.path.dirname(file_path))
        assert dirname_exists is False
        print("dirname_exists:", dirname_exists)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_ensure_dir_exists_directory_exists" \
        "\n============================================" \
        "\ndirname_exists: True" \
        "\ndirname_exists: True" \
        "\ndirname_exists: False" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_ensure_dir_exists_nested_directory(self, capsys):
        """ Ensure NewtFiles.ensure_dir_exists() creates nested parent directories. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "level1", "level2", "file.txt")

            dirname_exists = os.path.exists(os.path.dirname(file_path))
            assert dirname_exists is False
            print("dirname_exists:", dirname_exists)

            NewtFiles.ensure_dir_exists(file_path)

            dirname_exists = os.path.exists(os.path.dirname(file_path))
            assert dirname_exists is True
            print("dirname_exists:", dirname_exists)

        dirname_exists = os.path.exists(os.path.dirname(file_path))
        assert dirname_exists is False
        print("dirname_exists:", dirname_exists)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_ensure_dir_exists_nested_directory" \
        "\n============================================" \
        "\ndirname_exists: False" \
        "\ndirname_exists: True" \
        "\ndirname_exists: False" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


class TestCheckFileExists:
    """ Tests for check_file_exists function. """


    def test_check_file_exists_invalid_file_name(self, capsys):
        """ Ensure NewtFiles.check_file_exists() raises SystemExit for invalid file names. """
        print_my_func_name()

        file_name_1 = 123
        print("file_name_1:", file_name_1)

        with pytest.raises(SystemExit) as exc_info_1:
            NewtFiles.check_file_exists(file_name_1)  # type: ignore
            print("This line will not be printed")
        assert exc_info_1.value.code == 1
        print("exc_info_1:", exc_info_1.value.code)

        check_1 = NewtFiles.check_file_exists(file_name_1, stop=False)  # type: ignore
        assert check_1 is False
        print("check_1:", check_1)

        file_name_2 = ""
        print("file_name_2:", file_name_2)

        with pytest.raises(SystemExit) as exc_info_2:
            NewtFiles.check_file_exists(file_name_2)
            print("This line will not be printed")
        assert exc_info_2.value.code == 1
        print("exc_info_2:", exc_info_2.value.code)

        check_2 = NewtFiles.check_file_exists(file_name_2, stop=False)
        assert check_2 is False
        print("check_2:", check_2)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_check_file_exists_invalid_file_name" \
        "\n============================================" \
        "\nfile_name_1: 123\nexc_info_1: 1\ncheck_1: False" \
        "\nfile_name_2: \nexc_info_2: 1\ncheck_2: False" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.check_file_exists : file_path" \
        " > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: 123\nReceived type: <class 'int'>" \
        "\nExpected type: <class 'str'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.check_file_exists : file_path" \
        " > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: 123\nReceived type: <class 'int'>" \
        "\nExpected type: <class 'str'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.check_file_exists : file_path" \
        " > Newt.console.validate_type : is_empty" \
        "\n::: ERROR :::" \
        "\nValue must not be empty" \
        "\nValue: \nType: <class 'str'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.check_file_exists : file_path" \
        " > Newt.console.validate_type : is_empty" \
        "\n::: ERROR :::" \
        "\nValue must not be empty" \
        "\nValue: \nType: <class 'str'>" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 4

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


    def test_check_file_exists_not_found(self, capsys):
        """ Ensure NewtFiles.check_file_exists() returns False and exits for missing file. """
        print_my_func_name()

        file_name = "file.txt"
        print("file_name:", file_name)

        check_1 = NewtFiles.check_file_exists(file_name, stop=False, print_log=False)
        assert check_1 is False
        print("check_1:", check_1)

        with pytest.raises(SystemExit) as exc_info_2:
            NewtFiles.check_file_exists(file_name, stop=True, print_log=False)
            print("This line will not be printed")
        assert exc_info_2.value.code == 1
        print("exc_info_2:", exc_info_2.value.code)

        check_3 = NewtFiles.check_file_exists(file_name, stop=False, print_log=True)
        assert check_3 is False
        print("check_3:", check_3)

        with pytest.raises(SystemExit) as exc_info_4:
            NewtFiles.check_file_exists(file_name, stop=True, print_log=True)
            print("This line will not be printed")
        assert exc_info_4.value.code == 1
        print("exc_info_4:", exc_info_4.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_check_file_exists_not_found" \
        "\n============================================" \
        "\nfile_name: file.txt" \
        "\ncheck_1: False" \
        "\nexc_info_2: 1" \
        "\ncheck_3: False" \
        "\nexc_info_4: 1" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.check_file_exists : print_log" \
        "\n::: ERROR :::" \
        "\nFile not found: file.txt" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.check_file_exists : print_log" \
        "\n::: ERROR :::" \
        "\nFile not found: file.txt" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.check_file_exists : print_log" \
        "\n::: ERROR :::" \
        "\nFile not found: file.txt" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 3

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


    def test_check_file_exists_obscure(self, capsys):
        """ Ensure NewtFiles.check_file_exists() obscures path in error output for missing file. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmpfile:
            tmpfile.write("test")
            tmpfile_path = tmpfile.name

            check_1 = NewtFiles.check_file_exists(tmpfile_path)
            assert check_1 is True
            print("check_1:", check_1)

        try:
            check_2 = NewtFiles.check_file_exists(tmpfile_path)
            assert check_2 is True
            print("check_2:", check_2)

        finally:
            if os.path.exists(tmpfile_path):
                os.unlink(tmpfile_path)

        obscure_list = [
            "C:\\Users\\",
            "\\AppData\\Local\\Temp\\",
            "/tmp/",
            ]
        check_3 = NewtFiles.check_file_exists(tmpfile_path, obscure_list, stop=False)
        assert check_3 is False
        print("check_3:", check_3)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_not_found = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********"
        else:
            file_not_found = "/tmp/***********"

        assert "Function: test_check_file_exists_obscure" \
        "\n============================================" \
        "\ncheck_1: True" \
        "\ncheck_2: True" \
        "\ncheck_3: False" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.check_file_exists : print_log" \
        "\n::: ERROR :::" \
        "\nFile not found: " + file_not_found + \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

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
        assert "This line will not be printed" not in captured.out


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
        assert "This line will not be printed" not in captured.out


    @patch('newtutils.utility.input', side_effect=["abc", "999", "X"])
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

        assert "\nAvailable list: 3\n" in captured.out
        assert "\n  1: dummy_file_0.txt\n" in captured.out
        assert "\n  2: dummy_file_1.txt\n" in captured.out
        assert "\n  3: dummy_file_2.txt\n" in captured.out
        assert "\n  X: Exit / Cancel\n" in captured.out
        assert "\n[INPUT]: abc\nInvalid input. Please enter a number.\n" in captured.out
        assert "\n[INPUT]: 999\nNumber out of range. Try again.\n" in captured.out
        assert "\n[INPUT]: x\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.utility.select_from_input : choice = [X]\n" in captured.out
        assert "\nSelection cancelled.\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


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
        assert "This line will not be printed" not in captured.out


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
            print()

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
        assert "\n'Hello\\nWorld!\\n'\n" in captured.out
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
        assert "\\level1\\level2\\file.txt\n" in captured.out
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
            print()

            NewtFiles.save_text_to_file(tmp_path, "Line 2\n")
            print()

            result = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result))
            # New implementation normalizes and avoids extra blank lines
            assert result == "Line 1\nLine 2\n"

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\n[Newt.files.save_text_to_file] Saved text to file:\n") == 2
        assert "\n(mode=write, length=7)\n" in captured.out
        assert "\n(mode=append, length=7)\n" in captured.out
        assert "\n[Newt.files.read_text_from_file] Loaded text from file:\n" in captured.out
        assert "\n(length=14)\n" in captured.out
        assert "\n'Line 1\\nLine 2\\n'\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_read_text_from_nonexistent_file(self, capsys):
        """ Test NewtFiles.read_text_from_file() returns None for nonexistent file with stop=False. """
        print_my_func_name()

        result = NewtFiles.read_text_from_file("/nonexistent/file.txt", stop=False)
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.files.check_file_exists : logging\n" in captured.out
        assert "\nFile not found: /nonexistent/file.txt\n" in captured.out


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
        assert "[Newt.files.read_text_from_file] Loaded text from file:" not in captured.out


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
            print()

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

        assert captured.out.count("\n::: ERROR :::\n") == 2
        assert "\nLocation: Newt.console.validate_input > Newt.files.ensure_dir_exists : file_path\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.files.save_text_to_file : text\n" in captured.out
        assert captured.out.count("\nExpected <class 'str'>, got <class 'int'>\n") == 2
        assert "\nValue: 123\n" in captured.out
        assert "\nValue: 456\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


class TestConvertStrToJson:
    """ Tests for convert_str_to_json function. """


    def test_parses_valid_json_dict(self, capsys):
        """ Test NewtFiles.convert_str_to_json() parses valid JSON dict correctly. """
        print_my_func_name()

        json_str = '{"name": "test", "value": 123, "items": [1, 2, 3]}'
        print(repr(json_str))

        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert isinstance(result, dict)
        assert result == {"name": "test", "value": 123, "items": [1, 2, 3]}

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n'{\"name\": \"test\", \"value\": 123, \"items\": [1, 2, 3]}'\n{'name': 'test', 'value': 123, 'items': [1, 2, 3]}\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_parses_valid_json_list(self, capsys):
        """ Test NewtFiles.convert_str_to_json() parses valid JSON list correctly. """
        print_my_func_name()

        json_str = '[1, 2, 3, {"key": "value"}]'
        print(repr(json_str))

        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert isinstance(result, list)
        assert result == [1, 2, 3, {"key": "value"}]

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n'[1, 2, 3, {\"key\": \"value\"}]'\n[1, 2, 3, {'key': 'value'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_parses_single_quotes_dict(self, capsys):
        """ Test NewtFiles.convert_str_to_json() handles single quotes in dict string. """
        print_my_func_name()

        json_str = "{'name': 'test', 'value': 123}"
        print(repr(json_str))

        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert isinstance(result, dict)
        assert result == {"name": "test", "value": 123}

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.files.convert_str_to_json : Exception standard JSON\n" in captured.out
        assert "\nFailed to parse string to JSON: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)\n" in captured.out
        assert "\nTrying to replace single quotes with double quotes...\n" in captured.out


    def test_parses_single_quotes_list(self, capsys):
        """ Test NewtFiles.convert_str_to_json() handles single quotes in list string. """
        print_my_func_name()

        json_str = "['item1', 'item2', 'item3']"
        print(repr(json_str))

        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert isinstance(result, list)
        assert result == ["item1", "item2", "item3"]

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.files.convert_str_to_json : Exception standard JSON\n" in captured.out
        assert "\nFailed to parse string to JSON: Expecting value: line 1 column 2 (char 1)\n" in captured.out
        assert "\nTrying to replace single quotes with double quotes...\n" in captured.out


    def test_returns_none_for_empty_string(self, capsys):
        """ Test NewtFiles.convert_str_to_json() returns None for empty/whitespace strings. """
        print_my_func_name()

        result_1 = NewtFiles.convert_str_to_json("")
        print(repr(result_1))
        assert result_1 is None
        print()

        result_2 = NewtFiles.convert_str_to_json("   ")
        print(repr(result_2))
        assert result_2 is None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\n::: ERROR :::\n") == 2
        assert captured.out.count("\nLocation: Newt.console.validate_input : is_empty > Newt.files.convert_str_to_json : text\n") == 2
        assert captured.out.count("\nValue must be non-empty\n") == 2
        assert "\nValue: \n" in captured.out
        assert "\nValue:    \n" in captured.out


    def test_invalid_json_input_raises_exit(self, capsys):
        """ Test NewtFiles.convert_str_to_json() raises SystemExit for non-string inputs. """
        print_my_func_name()

        result_1 = NewtFiles.convert_str_to_json(123)  # type: ignore
        print(repr(result_1))
        assert result_1 is None
        print()

        result_2 = NewtFiles.convert_str_to_json(None)  # type: ignore
        print(repr(result_2))
        assert result_2 is None
        print()

        result_3 = NewtFiles.convert_str_to_json(["not", "a", "string"])  # type: ignore
        print(repr(result_3))
        assert result_3 is None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\n::: ERROR :::\n") == 3
        assert captured.out.count("\nLocation: Newt.console.validate_input > Newt.files.convert_str_to_json : text\n") == 3
        assert "\nExpected <class 'str'>, got <class 'int'>\n" in captured.out
        assert "\nExpected <class 'str'>, got <class 'NoneType'>\n" in captured.out
        assert "\nExpected <class 'str'>, got <class 'list'>\n" in captured.out
        assert "\nValue: 123\n" in captured.out
        assert "\nValue: None\n" in captured.out
        assert "\nValue: ['not', 'a', 'string']\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


    def test_invalid_json_prints_errors(self, capsys):
        """ Ensure invalid JSON returns None and prints expected error messages. """
        print_my_func_name()

        invalid_json = "{ invalid json }"
        print(repr(invalid_json))
        result = NewtFiles.convert_str_to_json(invalid_json)
        print(repr(result))
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\n::: ERROR :::\n") == 3
        assert "\nLocation: Newt.files.convert_str_to_json : Exception standard JSON\n" in captured.out
        assert "\nFailed to parse string to JSON: Expecting property name enclosed in double quotes: line 1 column 3 (char 2)\n" in captured.out
        assert "\nTrying to replace single quotes with double quotes...\n" in captured.out
        assert "\nLocation: Newt.files.convert_str_to_json : Exception replace single quotes with double quotes\n" in captured.out
        assert "\nLocation: Newt.files.convert_str_to_json : Unknown type\n" in captured.out
        assert "\nCannot convert STR to JSON.\n" in captured.out


    def test_nonjson_str_prints_errors(self, capsys):
        """ Ensure non-JSON strings return None and print expected errors. """
        print_my_func_name()

        invalid_json = "not json at all"
        print(repr(invalid_json))
        result = NewtFiles.convert_str_to_json(invalid_json)
        print(repr(result))
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\n::: ERROR :::\n") == 3
        assert "\nLocation: Newt.files.convert_str_to_json : Exception standard JSON\n" in captured.out
        assert "\nTrying to replace single quotes with double quotes...\n" in captured.out
        assert "\nLocation: Newt.files.convert_str_to_json : Exception replace single quotes with double quotes\n" in captured.out
        assert captured.out.count("\nFailed to parse string to JSON: Expecting value: line 1 column 1 (char 0)\n") == 2
        assert "\nLocation: Newt.files.convert_str_to_json : Unknown type\n" in captured.out
        assert "\nCannot convert STR to JSON.\n" in captured.out


    def test_returns_none_for_non_list_or_dict_json(self, capsys):
        """ Test NewtFiles.convert_str_to_json() returns None for non-list/dict JSON. """
        print_my_func_name()

        json_str = '"just a string"'
        print(repr(json_str))
        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert result is None
        print()

        json_str = "123"
        print(repr(json_str))
        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert result is None
        print()

        json_str = "true"
        print(repr(json_str))
        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\n::: ERROR :::\n") == 9
        assert captured.out.count("\nLocation: Newt.console.validate_input > Newt.files.convert_str_to_json : json.loads(text_strip)\n") == 3
        assert captured.out.count("\nTrying to replace single quotes with double quotes...\n") == 3
        assert captured.out.count("\nLocation: Newt.console.validate_input > Newt.files.convert_str_to_json : json.loads(text_replace)\n") == 3
        assert captured.out.count("\nExpected (<class 'list'>, <class 'dict'>), got <class 'str'>\n") == 2
        assert captured.out.count("\nExpected (<class 'list'>, <class 'dict'>), got <class 'int'>\n") == 2
        assert captured.out.count("\nExpected (<class 'list'>, <class 'dict'>), got <class 'bool'>\n") == 2
        assert captured.out.count("\nValue: just a string\n") == 2
        assert captured.out.count("\nValue: 123\n") == 2
        assert captured.out.count("\nValue: True\n") == 2
        assert captured.out.count("\nLocation: Newt.files.convert_str_to_json : Unknown type\n") == 3
        assert captured.out.count("\nCannot convert STR to JSON.\n") == 3


    def test_handles_whitespace(self, capsys):
        """ Test NewtFiles.convert_str_to_json() trims whitespace correctly. """
        print_my_func_name()

        json_str = '   {"key": "value"}   '
        print(repr(json_str))

        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert isinstance(result, dict)
        assert result == {"key": "value"}

        captured = capsys.readouterr()
        print_my_captured(captured)

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_handles_nested_structures(self, capsys):
        """ Test NewtFiles.convert_str_to_json() parses nested dict/list structures. """
        print_my_func_name()

        json_str = '{"outer": {"inner": {"deep": [1, 2, 3]}}}'
        print(repr(json_str))

        result = NewtFiles.convert_str_to_json(json_str)
        print(repr(result))
        assert isinstance(result, dict)
        assert result == {"outer": {"inner": {"deep": [1, 2, 3]}}}

        captured = capsys.readouterr()
        print_my_captured(captured)

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


class TestJsonFiles:
    """ Tests for JSON file operations. """


    def test_save_and_read_json_dict(self, capsys):
        """ Test NewtFiles.save_json_to_file() and read_json_from_file() correctly persist JSON dict. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name

        try:
            data = {"name": "test", "value": 123, "items": [1, 2, 3]}
            print(repr(data))
            print()

            NewtFiles.save_json_to_file(tmp_path, data)
            print()

            result_json = NewtFiles.read_json_from_file(tmp_path)
            print(repr(result_json))
            assert result_json == data
            print()

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            print(result_text)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[Newt.files.save_json_to_file] Saved JSON to file:\n" in captured.out
        assert "\n(type=<class 'dict'>, indent=2)\n" in captured.out
        assert "\n[Newt.files.read_json_from_file] Loaded JSON from file:\n" in captured.out
        assert "\n(type=<class 'dict'>)\n" in captured.out
        assert "\n[Newt.files.read_text_from_file] Loaded text from file:\n" in captured.out
        assert "\n(length=75)\n" in captured.out
        assert "\n\'{\\n  \"name\": \"test\",\\n  \"value\": 123,\\n  \"items\": [\\n    1,\\n    2,\\n    3\\n  ]\\n}\\n\'\n" in captured.out
        assert "\n{\n  \"name\": \"test\",\n  \"value\": 123,\n  \"items\": [\n    1,\n    2,\n    3\n  ]\n}\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_save_and_read_json_list(self, capsys):
        """ Test NewtFiles.save_json_to_file() and read_json_from_file() correctly persist JSON list. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name

        try:
            data = [1, 2, 3, {"key": "value"}]
            print(repr(data))

            NewtFiles.save_json_to_file(tmp_path, data)
            print()

            result_json = NewtFiles.read_json_from_file(tmp_path)
            print(repr(result_json))
            assert result_json == data
            print()

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            print(result_text)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[Newt.files.save_json_to_file] Saved JSON to file:\n" in captured.out
        assert "\n(type=<class 'list'>, indent=2)\n" in captured.out
        assert "\n[Newt.files.read_json_from_file] Loaded JSON from file:\n" in captured.out
        assert "\n(type=<class 'list'>)\n" in captured.out
        assert "\n[Newt.files.read_text_from_file] Loaded text from file:\n" in captured.out
        assert "\n(length=46)\n" in captured.out
        assert "\n\'[\\n  1,\\n  2,\\n  3,\\n  {\\n    \"key\": \"value\"\\n  }\\n]\\n'\n" in captured.out
        assert "\n[\n  1,\n  2,\n  3,\n  {\n    \"key\": \"value\"\n  }\n]\n" in captured.out

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_read_json_from_nonexistent_file(self, capsys):
        """ Test NewtFiles.read_json_from_file(stop=False) returns None for nonexistent file. """
        print_my_func_name()

        result = NewtFiles.read_json_from_file("/nonexistent/file.json", stop=False)
        print(repr(result))
        assert result == None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.files.check_file_exists : logging\n" in captured.out
        assert "\nFile not found: /nonexistent/file.json\n" in captured.out


    def test_save_json_creates_directory(self, capsys):
        """ Test that save_json_to_file creates parent directories. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = os.path.join(tmpdir, "level1", "level2", "file.json")

            data = {"test": "data"}
            print(repr(data))

            NewtFiles.save_json_to_file(nested_path, data)
            assert os.path.exists(nested_path)

            result = NewtFiles.read_json_from_file(nested_path)
            print(repr(result))
            assert result == {"test": "data"}

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[Newt.files.save_json_to_file] Saved JSON to file:\n" in captured.out
        assert "\n(type=<class 'dict'>, indent=2)\n" in captured.out
        assert "\n[Newt.files.read_json_from_file] Loaded JSON from file:\n" in captured.out
        assert "\n(type=<class 'dict'>)\n" in captured.out
        assert captured.out.count("\\level1\\level2\\file.json\n") == 2
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_save_json_custom_indent(self, capsys):
        """ Test saving JSON with custom indent. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name

        try:
            data = {"a": 1, "b": 2}
            print(repr(data))
            NewtFiles.save_json_to_file(tmp_path, data, indent=4)
            print()

            result_json = NewtFiles.read_json_from_file(tmp_path)
            print(repr(result_json))
            assert result_json == data
            print()

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            print(result_text)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[Newt.files.save_json_to_file] Saved JSON to file:\n" in captured.out
        assert "\n[Newt.files.read_json_from_file] Loaded JSON from file:\n" in captured.out
        assert "\n[Newt.files.read_text_from_file] Loaded text from file:\n" in captured.out
        assert "'{\\n    \"a\": 1,\\n    \"b\": 2\\n}\\n'\n{\n    \"a\": 1,\n    \"b\": 2\n}\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_read_json_invalid_file(self, capsys):
        """ Test reading invalid JSON raises SystemExit. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp.write("{ invalid json }")
            tmp_path = tmp.name

        try:
            with pytest.raises(SystemExit) as exc_info:
                result = NewtFiles.read_json_from_file(tmp_path)
                print("This line will not be printed")
            assert exc_info.value.code == 1

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.files.read_json_from_file : Exception\n" in captured.out
        assert "\nException: Expecting property name enclosed in double quotes: line 1 column 3 (char 2)\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


    def test_save_json_invalid_input(self, capsys):
        """ Test that invalid input is handled gracefully. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name

        try:
            with pytest.raises(SystemExit) as exc_info_1:
                # Invalid file_name
                NewtFiles.save_json_to_file(123, {"test": "data"})  # type: ignore
                print("This line will not be printed 01")
            assert exc_info_1.value.code == 1
            print()

            with pytest.raises(SystemExit) as exc_info_2:
                # Invalid data (not list or dict)
                NewtFiles.save_json_to_file(tmp_path, "not a dict or list")  # type: ignore
                print("This line will not be printed 02")
            assert exc_info_2.value.code == 1
            print()

            with pytest.raises(SystemExit) as exc_info_3:
                NewtFiles.read_json_from_file(tmp_path)
                print("This line will not be printed 03")
            assert exc_info_3.value.code == 1

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            assert result_text == ""

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\n::: ERROR :::\n") == 3
        assert "\nLocation: Newt.console.validate_input > Newt.files.ensure_dir_exists : file_path\n" in captured.out
        assert "\nExpected <class 'str'>, got <class 'int'>\n" in captured.out
        assert "\nValue: 123\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.files.save_json_to_file : data\n" in captured.out
        assert "\nExpected (<class 'list'>, <class 'dict'>), got <class 'str'>\n" in captured.out
        assert "\nValue: not a dict or list\n" in captured.out
        assert "\nLocation: Newt.files.read_json_from_file : Exception\n" in captured.out
        assert "\nException: Expecting value: line 1 column 1 (char 0)\n" in captured.out
        assert "\n[Newt.files.read_text_from_file] Loaded text from file:\n" in captured.out
        assert "\n(length=0)\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


class TestCsvFiles:
    """ Tests for CSV file operations. """


    def test_save_and_read_csv_basic_settings(self, capsys):
        """ Test saving and reading a CSV file. """
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
            print()

            NewtFiles.save_csv_to_file(tmp_path, rows)
            print()

            result_csv = NewtFiles.read_csv_from_file(tmp_path)
            print(repr(result_csv))
            assert result_csv == rows
            print()

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            print(result_text)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[Newt.files.save_csv_to_file] Saved CSV to file:\n" in captured.out
        assert "\n(rows=3, mode=write, delimiter=';')\n" in captured.out
        assert "\n[Newt.files.read_csv_from_file] Loaded CSV from file:\n" in captured.out
        assert "\n(rows=3, delimiter=';')\n" in captured.out
        assert "\n[Newt.files.read_text_from_file] Loaded text from file:\n" in captured.out
        assert "\n(length=46)\n" in captured.out
        assert "\n'Name;Age;City\\nAlice;30;New York\\nBob;25;London\\n'\nName;Age;City\nAlice;30;New York\nBob;25;London\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_save_and_read_csv_custom_delimiter(self, capsys):
        """ Test saving and reading CSV with custom delimiter. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp_path = tmp.name

        try:
            rows = [["A", "B"], ["1", "2"]]
            print(repr(rows))
            print()

            NewtFiles.save_csv_to_file(tmp_path, rows, delimiter=",")
            print()

            result_csv = NewtFiles.read_csv_from_file(tmp_path, delimiter=",")
            print(repr(result_csv))
            assert result_csv == rows
            print()

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            print(result_text)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[Newt.files.save_csv_to_file] Saved CSV to file:\n" in captured.out
        assert "\n(rows=2, mode=write, delimiter=',')\n" in captured.out
        assert "\n[Newt.files.read_csv_from_file] Loaded CSV from file:\n" in captured.out
        assert "\n(rows=2, delimiter=',')\n" in captured.out
        assert "\n[Newt.files.read_text_from_file] Loaded text from file:\n" in captured.out
        assert "\n(length=8)\n" in captured.out
        assert "\n'A,B\\n1,2\\n'\nA,B\n1,2\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_read_csv_from_nonexistent_file(self, capsys):
        """ Test reading from non-existent CSV file returns empty list. """
        print_my_func_name()

        result = NewtFiles.read_csv_from_file("/nonexistent/file.csv", stop=False)
        print(repr(result))
        assert result == None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.files.check_file_exists : logging\n" in captured.out
        assert "\nFile not found: /nonexistent/file.csv\n" in captured.out


    def test_save_csv_creates_directory(self, capsys):
        """ Test that save_csv_to_file creates parent directories. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = os.path.join(tmpdir, "level1", "level2", "file.csv")

            rows = [["Header"], ["Data"]]
            print(repr(rows))

            NewtFiles.save_csv_to_file(nested_path, rows)
            assert os.path.exists(nested_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[Newt.files.save_csv_to_file] Saved CSV to file:\n" in captured.out
        assert "\\level1\\level2\\file.csv\n" in captured.out
        assert "\n(rows=2, mode=write, delimiter=';')\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_save_csv_normalizes_newlines_in_cells(self, capsys):
        """ Test that CSV cells with Windows newlines are normalized. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp_path = tmp.name

        try:
            rows = [["Cell1\r\nLine2", "Cell2"]]
            print(repr(rows))
            print()

            NewtFiles.save_csv_to_file(tmp_path, rows)
            print()

            result_csv = NewtFiles.read_csv_from_file(tmp_path)
            print(repr(result_csv))
            # Check that newlines are normalized
            assert result_csv is not None
            assert "\r\n" not in result_csv[0][0]
            print()

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            print(result_text)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[Newt.files.save_csv_to_file] Saved CSV to file:\n" in captured.out
        assert "\n(rows=1, mode=write, delimiter=';')\n" in captured.out
        assert "\n[Newt.files.read_csv_from_file] Loaded CSV from file:\n" in captured.out
        assert "\n(rows=1, delimiter=';')\n" in captured.out
        assert "\n[Newt.files.read_text_from_file] Loaded text from file:\n" in captured.out
        assert "\n(length=20)\n" in captured.out
        assert "\n'\"Cell1\\nLine2\";Cell2\\n'\n\"Cell1\nLine2\";Cell2\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_save_csv_with_various_types(self, capsys):
        """ Test saving CSV with various data types. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp_path = tmp.name

        try:
            rows = [["String", 123, 45.67, True]]
            print(repr(rows))
            print()

            NewtFiles.save_csv_to_file(tmp_path, rows)
            print()

            result_csv = NewtFiles.read_csv_from_file(tmp_path)
            print(repr(result_csv))
            # All values should be strings in CSV
            assert result_csv is not None
            assert all(isinstance(cell, str) for row in result_csv for cell in row)
            print()

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            print(result_text)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[Newt.files.save_csv_to_file] Saved CSV to file:\n" in captured.out
        assert "\n(rows=1, mode=write, delimiter=';')\n" in captured.out
        assert "\n[Newt.files.read_csv_from_file] Loaded CSV from file:\n" in captured.out
        assert "\n(rows=1, delimiter=';')\n" in captured.out
        assert "\n[Newt.files.read_text_from_file] Loaded text from file:\n" in captured.out
        assert "\n(length=22)\n" in captured.out
        assert "\n'String;123;45.67;True\\n'\nString;123;45.67;True\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_save_csv_invalid_input(self, capsys):
        """ Test that invalid input is handled gracefully. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp_path = tmp.name

        try:
            with pytest.raises(SystemExit) as exc_info_1:
                # Invalid file_name
                NewtFiles.save_csv_to_file(123, [["test"]])  # type: ignore
                print("This line will not be printed 01")
            assert exc_info_1.value.code == 1
            print()

            with pytest.raises(SystemExit) as exc_info_2:
                # Invalid rows (not a list)
                NewtFiles.save_csv_to_file(tmp_path, "not a list")
                print("This line will not be printed 02")
            assert exc_info_2.value.code == 1
            print()

            with pytest.raises(SystemExit) as exc_info_3:
                # Invalid delimiter
                NewtFiles.save_csv_to_file(tmp_path, [["test"]], delimiter=123)  # type: ignore
                print("This line will not be printed 03")
            assert exc_info_3.value.code == 1

            result_text = NewtFiles.read_text_from_file(tmp_path)
            print(repr(result_text))
            assert result_text == ""

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\n::: ERROR :::\n") == 3
        assert "\nLocation: Newt.console.validate_input > Newt.files.ensure_dir_exists : file_path\n" in captured.out
        assert captured.out.count("\nExpected <class 'str'>, got <class 'int'>\n") == 2
        assert "\nLocation: Newt.console.validate_input > Newt.files.save_csv_to_file : rows\n" in captured.out
        assert "\nExpected (<class 'list'>, <class 'tuple'>), got <class 'str'>\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.files.save_csv_to_file : delimiter\n" in captured.out
        assert "\n[Newt.files.read_text_from_file] Loaded text from file:\n" in captured.out
        assert "\n(length=0)\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


    def test_read_csv_invalid_delimiter(self, capsys):
        """ Test reading CSV with invalid delimiter still parses but with wrong splitting. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp.write("A;B\n1;2")
            tmp_path = tmp.name

        try:
            # Wrong delimiter
            result = NewtFiles.read_csv_from_file(tmp_path, delimiter=",")
            print(repr(result))
            assert result is not None
            print(repr(result[0][0]))
            # Should still read but with wrong parsing
            assert isinstance(result, list)
            assert isinstance(result[0][0], str)
            assert result[0][0] == "A;B"

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[Newt.files.read_csv_from_file] Loaded CSV from file:\n" in captured.out
        assert "\n(rows=2, delimiter=',')\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
