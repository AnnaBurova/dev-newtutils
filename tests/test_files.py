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
from unittest.mock import patch
import tempfile
import json

from .helpers import print_my_func_name, print_my_captured
# import newtutils.console as NewtCons
import newtutils.utility as NewtUtil
import newtutils.files as NewtFiles

obscure_list = [
    "C:\\Users\\",
    "\\AppData\\Local\\Temp\\",
    "/tmp/",
    "\\level1\\level2\\file",
    "/level1/level2/file",
    ".txt",
    ".json",
    ".csv",
    ]


class TestNormalizeNewlines:
    """ Tests for _normalize_newlines function. """


    def test_normalize_newlines_mixed_endings(self, capsys):
        """ Ensure NewtFiles._normalize_newlines() handles mixed line endings correctly. """
        print_my_func_name()

        text_1 = "line1\r\nline2\r\nline3\r\nline4\r\nline5\r\n"
        print("text_1:", repr(text_1))

        result_1 = NewtFiles._normalize_newlines(text_1)
        assert result_1 == "line1\nline2\nline3\nline4\nline5"
        print("result_1:", repr(result_1))

        text_2 = "    line1\r\nline2\nline3\r\nline4\rline5\r\n"
        print("text_2:", repr(text_2))

        result_2 = NewtFiles._normalize_newlines(text_2)
        assert result_2 == "    line1\nline2\nline3\nline4\nline5"
        print("result_2:", repr(result_2))

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_normalize_newlines_mixed_endings" \
        "\n============================================" \
        "\ntext_1: 'line1\\r\\nline2\\r\\nline3\\r\\nline4\\r\\nline5\\r\\n'" \
        "\nresult_1: 'line1\\nline2\\nline3\\nline4\\nline5'" \
        "\ntext_2: '    line1\\r\\nline2\\nline3\\r\\nline4\\rline5\\r\\n'" \
        "\nresult_2: '    line1\\nline2\\nline3\\nline4\\nline5'" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


class TestObscureLogic:
    """ Tests for _obscure_logic function. """


    def test_obscure_logic_path_segments(self, capsys):
        """ Ensure NewtFiles._obscure_logic() masks path segments from obscure list. """
        print_my_func_name()

        if sys.platform == "win32" and os.name == "nt":
            file_name = "C:\\Users\\abcdefg\\AppData\\Local\\Temp\\1234567890"
        else:
            file_name = "/tmp/1234567890"

        file_obscure_name = NewtFiles._obscure_logic(file_name, obscure_list)
        print("file_obscure_name:", file_obscure_name)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\**********"
        else:
            file_obscure_name = "/tmp/**********"

        assert "Function: test_obscure_logic_path_segments" \
        "\n============================================" \
        "\nfile_obscure_name: " + file_obscure_name + \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


class TestEnsureDirExists:
    """ Tests for ensure_dir_exists function. """


    def test_ensure_dir_exists_empty_string_exit(self, capsys):
        """ Ensure NewtFiles.ensure_dir_exists() raises SystemExit(1) for empty string. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info:
            NewtFiles.ensure_dir_exists("")
            print("This line will not be printed")
        assert exc_info.value.code == 1
        print("exc_info:", exc_info.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_ensure_dir_exists_empty_string_exit" \
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


    def test_ensure_dir_exists_no_dir_created(self, capsys):
        """ Ensure NewtFiles.ensure_dir_exists() skips creation for filename-only path. """
        print_my_func_name()

        file_path = "file.txt"
        NewtFiles.ensure_dir_exists(file_path)

        dirname_exists = os.path.exists(os.path.dirname(file_path))
        assert dirname_exists is False
        print("dirname_exists:", dirname_exists)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_ensure_dir_exists_no_dir_created" \
        "\n============================================" \
        "\ndirname_exists: False" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_ensure_dir_exists_existing_dir(self, capsys):
        """ Ensure NewtFiles.ensure_dir_exists() passes when directory already exists. """
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

        assert "Function: test_ensure_dir_exists_existing_dir" \
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


    def test_ensure_dir_exists_nested_dirs_created(self, capsys):
        """ Ensure NewtFiles.ensure_dir_exists() creates nested directories as needed. """
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

        assert "Function: test_ensure_dir_exists_nested_dirs_created" \
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


    def test_check_file_exists_invalid_input(self, capsys):
        """ Ensure NewtFiles.check_file_exists() exits or returns False for invalid input. """
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

        assert "Function: test_check_file_exists_invalid_input" \
        "\n============================================" \
        "\nfile_name_1: 123" \
        "\nexc_info_1: 1" \
        "\ncheck_1: False" \
        "\nfile_name_2: " \
        "\nexc_info_2: 1" \
        "\ncheck_2: False" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.check_file_exists : file_path > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: 123\nReceived type: <class 'int'>" \
        "\nExpected type: <class 'str'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.check_file_exists : file_path > Newt.console.validate_type" \
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


    def test_check_file_exists_missing_file(self, capsys):
        """ Ensure NewtFiles.check_file_exists() handles missing file with stop/print flags. """
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

        assert "Function: test_check_file_exists_missing_file" \
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


    def test_check_file_exists_temp_file_lifecycle(self, capsys):
        """ Ensure NewtFiles.check_file_exists() detects file presence and absence correctly. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmpfile:
            file_txt = tmpfile.name

            check_1 = NewtFiles.check_file_exists(file_txt)
            assert check_1 is True
            print("check_1:", check_1)

        try:
            check_2 = NewtFiles.check_file_exists(file_txt)
            assert check_2 is True
            print("check_2:", check_2)

        finally:
            if os.path.exists(file_txt):
                os.unlink(file_txt)

        check_3 = NewtFiles.check_file_exists(file_txt, obscure_list=obscure_list, stop=False)
        assert check_3 is False
        print("check_3:", check_3)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.txt"
        else:
            file_obscure_name = "/tmp/***********.txt"

        assert "Function: test_check_file_exists_temp_file_lifecycle" \
        "\n============================================" \
        "\ncheck_1: True" \
        "\ncheck_2: True" \
        "\ncheck_3: False" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.check_file_exists : print_log" \
        "\n::: ERROR :::" \
        "\nFile not found: " + file_obscure_name + \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


class TestChooseFileFromFolder:
    """ Tests for choose_file_from_folder function. """


    def test_choose_file_from_folder_invalid_input(self, capsys):
        """ Ensure NewtFiles.choose_file_from_folder() exits for empty or non-string input. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info_1:
            NewtFiles.choose_file_from_folder("")
            print("This line will not be printed")
        assert exc_info_1.value.code == 1
        print("exc_info_1:", exc_info_1.value.code)

        with pytest.raises(SystemExit) as exc_info_2:
            NewtFiles.choose_file_from_folder(123)  # type: ignore
            print("This line will not be printed")
        assert exc_info_2.value.code == 1
        print("exc_info_2:", exc_info_2.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_choose_file_from_folder_invalid_input" \
        "\n============================================" \
        "\nexc_info_1: 1" \
        "\nexc_info_2: 1" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.choose_file_from_folder : folder_path" \
        " > Newt.console.validate_type : is_empty" \
        "\n::: ERROR :::" \
        "\nValue must not be empty" \
        "\nValue: \nType: <class 'str'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.choose_file_from_folder : folder_path" \
        " > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: 123\nReceived type: <class 'int'>" \
        "\nExpected type: <class 'str'>" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 2

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


    def test_choose_file_from_folder_missing_folder(self, capsys):
        """ Ensure NewtFiles.choose_file_from_folder() exits for nonexistent folder path. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info:
            NewtFiles.choose_file_from_folder("/nonexistent/folder")
            print("This line will not be printed")
        assert exc_info.value.code == 1
        print("exc_info:", exc_info.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_choose_file_from_folder_missing_folder" \
        "\n============================================" \
        "\nexc_info: 1" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.choose_file_from_folder : not isdir folder_path" \
        "\n::: ERROR :::" \
        "\nFolder not found: /nonexistent/folder" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


    def test_choose_file_from_folder_empty_folder(self, capsys):
        """ Ensure NewtFiles.choose_file_from_folder() exits when folder has no files. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(SystemExit) as exc_info:
                NewtFiles.choose_file_from_folder(tmpdir)
                print("This line will not be printed")
            assert exc_info.value.code == 1
            print("exc_info:", exc_info.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_choose_file_from_folder_empty_folder" \
        "\n============================================" \
        "\nexc_info: 1" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.choose_file_from_folder : file_list empty" \
        "\n::: ERROR :::" \
        "\nNo files found in this folder." \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


    @patch('newtutils.utility.input')
    def test_choose_file_from_folder_user_input(self, mock_input, capsys):
        """ Ensure NewtFiles.choose_file_from_folder() handles user input and invalid choices. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create several files in the temporary directory
            dir_files = []
            for i in range(3):
                file_name = f"dummy_file_{i}.txt"
                file_path = os.path.join(tmpdir, file_name)
                dir_files.append([file_name])
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("dummy content\n")

            todo_dict = NewtUtil.count_values_by_position(dir_files)

            mock_input.side_effect = ["abc", "999", "X"]

            with pytest.raises(SystemExit) as exc_info:
                NewtFiles.choose_file_from_folder(tmpdir)
                print("This line will not be printed")
            assert exc_info.value.code == 1
            print("exc_info:", exc_info.value.code)

            mock_input.side_effect = ["1"]

            selected_file = NewtFiles.choose_file_from_folder(tmpdir)
            assert selected_file == "dummy_file_0.txt"

            mock_input.side_effect = ["2"]

            selected_file = NewtFiles.choose_file_from_folder(tmpdir, todo_dict)
            assert selected_file == "dummy_file_1.txt"

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_choose_file_from_folder_user_input" \
        "\n============================================" \
        "\n\n3 Available options to choose from:" \
        "\n  1: dummy_file_0.txt" \
        "\n  2: dummy_file_1.txt" \
        "\n  3: dummy_file_2.txt" \
        "\n  X: Exit / Cancel" \
        "\n[INPUT]: abc" \
        "\nOption not in list. Try again." \
        "\n[INPUT]: 999" \
        "\nOption not in list. Try again." \
        "\n[INPUT]: x" \
        "\nexc_info: 1" \
        "\n\n3 Available options to choose from:" \
        "\n  1: dummy_file_0.txt" \
        "\n  2: dummy_file_1.txt" \
        "\n  3: dummy_file_2.txt" \
        "\n  X: Exit / Cancel" \
        "\n[INPUT]: 1" \
        "\nSelected option: dummy_file_0.txt\n" \
        "\n\n3 Available options to choose from:" \
        "\n  1: (1) dummy_file_0.txt" \
        "\n  2: (1) dummy_file_1.txt" \
        "\n  3: (1) dummy_file_2.txt" \
        "\n  X: Exit / Cancel" \
        "\n[INPUT]: 2" \
        "\nSelected option: dummy_file_1.txt\n" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.utility.select_from_input : choice = [X]" \
        "\n::: ERROR :::" \
        "\nSelection cancelled." \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


class TestTextFiles:
    """ Tests for read_text_from_file and save_text_to_file functions. """


    def test_save_and_read_text_from_file(self, capsys):
        """ Ensure NewtFiles.save_text_to_file() and read_text_from_file() round-trip correctly. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmpfile:
            file_txt = tmpfile.name

        try:
            content = "Hello\nWorld!"
            print("content:", repr(content))

            NewtFiles.save_text_to_file(file_txt, content, obscure_list=obscure_list)

            result = NewtFiles.read_text_from_file(file_txt, obscure_list=obscure_list)
            assert result == content + "\n"
            print("result:", repr(result))

        finally:
            if os.path.exists(file_txt):
                os.unlink(file_txt)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.txt"
        else:
            file_obscure_name = "/tmp/***********.txt"

        assert "Function: test_save_and_read_text_from_file" \
        "\n============================================" \
        "\ncontent: 'Hello\\nWorld!'" \
        "\n[Newt.files.save_text_to_file] Saved text to file:" \
        "\n" + file_obscure_name + \
        "\n(length=13, mode=write)" \
        "\n[Newt.files.read_text_from_file] Loaded text from file:" \
        "\n" + file_obscure_name + \
        "\n(length=13)" \
        "\nresult: 'Hello\\nWorld!\\n'" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_save_text_to_file_creates_nested_dirs(self, capsys):
        """ Ensure NewtFiles.save_text_to_file() creates nested dirs and saves content. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "level1", "level2", "file.txt")

            content = "Hello\nWorld!\n"
            print("content:", repr(content))

            NewtFiles.save_text_to_file(file_path, content, obscure_list=obscure_list)

            result = NewtFiles.read_text_from_file(file_path, obscure_list=obscure_list)
            assert result == content
            print("result:", repr(result))

            file_exists = os.path.exists(file_path)
            assert file_exists is True
            print("file_exists:", file_exists)

        file_exists = os.path.exists(file_path)
        assert file_exists is False
        print("file_exists:", file_exists)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********\\level1\\level2\\file.txt"
        else:
            file_obscure_name = "/tmp/***********/level1/level2/file.txt"

        assert "Function: test_save_text_to_file_creates_nested_dirs" \
        "\n============================================" \
        "\ncontent: 'Hello\\nWorld!\\n'" \
        "\n[Newt.files.save_text_to_file] Saved text to file:" \
        "\n" + file_obscure_name + \
        "\n(length=13, mode=write)" \
        "\n[Newt.files.read_text_from_file] Loaded text from file:" \
        "\n" + file_obscure_name + \
        "\n(length=13)" \
        "\nresult: 'Hello\\nWorld!\\n'" \
        "\nfile_exists: True" \
        "\nfile_exists: False" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_save_text_to_file_append_mode(self, capsys):
        """ Ensure NewtFiles.save_text_to_file() appends content correctly to existing file. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmpfile:
            file_txt = tmpfile.name

        try:
            content_1 = "Line 1"
            NewtFiles.save_text_to_file(
                file_txt, content_1, append=False, obscure_list=obscure_list
            )

            content_2 = "Line 2"
            NewtFiles.save_text_to_file(
                file_txt, content_2, append=True, obscure_list=obscure_list
            )

            result = NewtFiles.read_text_from_file(file_txt, obscure_list=obscure_list)
            assert result == "Line 1\nLine 2\n"
            print("result:", repr(result))

        finally:
            if os.path.exists(file_txt):
                os.unlink(file_txt)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.txt"
        else:
            file_obscure_name = "/tmp/***********.txt"

        assert "Function: test_save_text_to_file_append_mode" \
        "\n============================================" \
        "\n[Newt.files.save_text_to_file] Saved text to file:" \
        "\n" + file_obscure_name + \
        "\n(length=7, mode=write)" \
        "\n[Newt.files.save_text_to_file] Saved text to file:" \
        "\n" + file_obscure_name + \
        "\n(length=7, mode=append)" \
        "\n[Newt.files.read_text_from_file] Loaded text from file:" \
        "\n" + file_obscure_name + \
        "\n(length=14)" \
        "\nresult: 'Line 1\\nLine 2\\n'" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_read_text_from_file_missing_file(self, capsys):
        """ Ensure NewtFiles.read_text_from_file() returns None for nonexistent file. """
        print_my_func_name()

        result = NewtFiles.read_text_from_file("/nonexistent/file.txt", stop=False)
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_read_text_from_file_missing_file" \
        "\n============================================" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.check_file_exists : print_log" \
        "\n::: ERROR :::" \
        "\nFile not found: /nonexistent/file.txt" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_save_text_to_file_invalid_args(self, capsys):
        """ Ensure NewtFiles.save_text_to_file() exits for invalid filename or text type. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmpfile:
            file_txt = tmpfile.name

        try:
            with pytest.raises(SystemExit) as exc_info_1:
                # Invalid file_name
                NewtFiles.save_text_to_file(123, "test")  # type: ignore
                print("This line will not be printed")
            assert exc_info_1.value.code == 1
            print("exc_info_1:", exc_info_1.value.code)

            with pytest.raises(SystemExit) as exc_info_2:
                # Invalid text
                NewtFiles.save_text_to_file(file_txt, 456)  # type: ignore
                print("This line will not be printed")
            assert exc_info_2.value.code == 1
            print("exc_info_2:", exc_info_2.value.code)

        finally:
            if os.path.exists(file_txt):
                os.unlink(file_txt)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_save_text_to_file_invalid_args" \
        "\n============================================" \
        "\nexc_info_1: 1" \
        "\nexc_info_2: 1" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.ensure_dir_exists : file_path > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: 123\nReceived type: <class 'int'>" \
        "\nExpected type: <class 'str'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.save_text_to_file : content > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: 456\nReceived type: <class 'int'>" \
        "\nExpected type: <class 'str'>" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 2

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


class TestConvertStrToJson:
    """ Tests for convert_str_to_json function. """


    def test_convert_str_to_json_invalid_input(self, capsys):
        """ Ensure NewtFiles.convert_str_to_json() returns None for invalid input types. """
        print_my_func_name()

        result_1 = NewtFiles.convert_str_to_json("")
        assert result_1 is None
        print("result_1:", result_1)

        result_2 = NewtFiles.convert_str_to_json("   ")
        assert result_2 is None
        print("result_2:", result_2)

        result_3 = NewtFiles.convert_str_to_json(None)  # type: ignore
        assert result_3 is None
        print("result_3:", result_3)

        result_4 = NewtFiles.convert_str_to_json(123)  # type: ignore
        assert result_4 is None
        print("result_4:", result_4)

        result_5 = NewtFiles.convert_str_to_json(["not", "a", "string"])  # type: ignore
        assert result_5 is None
        print("result_5:", result_5)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_convert_str_to_json_invalid_input" \
        "\n============================================" \
        "\nresult_1: None" \
        "\nresult_2: None" \
        "\nresult_3: None" \
        "\nresult_4: None" \
        "\nresult_5: None" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.convert_str_to_json : content" \
        " > Newt.console.validate_type : is_empty" \
        "\n::: ERROR :::" \
        "\nValue must not be empty" \
        "\nValue: \nType: <class 'str'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.convert_str_to_json : content" \
        " > Newt.console.validate_type : is_empty" \
        "\n::: ERROR :::" \
        "\nValue must not be empty" \
        "\nValue:    \nType: <class 'str'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.convert_str_to_json : content > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: None\nReceived type: <class 'NoneType'>" \
        "\nExpected type: <class 'str'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.convert_str_to_json : content > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: 123\nReceived type: <class 'int'>" \
        "\nExpected type: <class 'str'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.convert_str_to_json : content > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: ['not', 'a', 'string']\nReceived type: <class 'list'>" \
        "\nExpected type: <class 'str'>" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 5

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_convert_str_to_json_valid_input(self, capsys):
        """ Ensure NewtFiles.convert_str_to_json() parses valid JSON strings correctly. """
        print_my_func_name()

        json_str_1 = '{"name": "test", "value": 123, "items": [1, 2, 3]}'
        print("json_str_1:", repr(json_str_1))

        result_1 = NewtFiles.convert_str_to_json(json_str_1)
        assert isinstance(result_1, dict)
        assert result_1 == {"name": "test", "value": 123, "items": [1, 2, 3]}
        print("result_1:", result_1)

        json_str_2 = '[1, 2, 3, {"key": "value"}]'
        print("json_str_2:", repr(json_str_2))

        result_2 = NewtFiles.convert_str_to_json(json_str_2)
        assert isinstance(result_2, list)
        assert result_2 == [1, 2, 3, {"key": "value"}]
        print("result_2:", result_2)

        json_str_3 = '{"outer": {"inner": {"deep": [1, 2, 3]}}}'
        print("json_str_3:", repr(json_str_3))

        result_3 = NewtFiles.convert_str_to_json(json_str_3)
        assert isinstance(result_3, dict)
        assert result_3 == {"outer": {"inner": {"deep": [1, 2, 3]}}}
        print("result_3:", result_3)

        json_str_4 = '   {"key": "value"}   '
        print("json_str_4:", repr(json_str_4))

        result_4 = NewtFiles.convert_str_to_json(json_str_4)
        assert isinstance(result_4, dict)
        assert result_4 == {"key": "value"}
        print("result_4:", result_4)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_convert_str_to_json_valid_input" \
        "\n============================================" \
        "\njson_str_1: \'{\"name\": \"test\", \"value\": 123, \"items\": [1, 2, 3]}\'" \
        "\nresult_1: {\'name\': \'test\', \'value\': 123, \'items\': [1, 2, 3]}" \
        "\njson_str_2: \'[1, 2, 3, {\"key\": \"value\"}]\'" \
        "\nresult_2: [1, 2, 3, {\'key\': \'value\'}]" \
        "\njson_str_3: \'{\"outer\": {\"inner\": {\"deep\": [1, 2, 3]}}}\'" \
        "\nresult_3: {\'outer\': {\'inner\': {\'deep\': [1, 2, 3]}}}" \
        "\njson_str_4: \'   {\"key\": \"value\"}   \'" \
        "\nresult_4: {\'key\': \'value\'}" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_convert_str_to_json_literals(self, capsys):
        """ Ensure NewtFiles.convert_str_to_json() parses dict and list strings. """
        print_my_func_name()

        json_str_1 = "{'name': 'test', 'value': 123}"
        print("json_str_1:", repr(json_str_1))

        result_1 = NewtFiles.convert_str_to_json(json_str_1)
        assert isinstance(result_1, dict)
        assert result_1 == {"name": "test", "value": 123}
        print("result_1:", result_1)

        json_str_2 = "['item1', 'item2', 'item3']"
        print("json_str_2:", repr(json_str_2))

        result_2 = NewtFiles.convert_str_to_json(json_str_2)
        assert isinstance(result_2, list)
        assert result_2 == ["item1", "item2", "item3"]
        print("result_2:", result_2)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_convert_str_to_json_literals" \
        "\n============================================" \
        "\njson_str_1: \"{\'name\': \'test\', \'value\': 123}\"" \
        "\nTrying to replace single quotes with double quotes..." \
        "\nresult_1: {\'name\': \'test\', \'value\': 123}" \
        "\njson_str_2: \"[\'item1\', \'item2\', \'item3\']\"" \
        "\nTrying to replace single quotes with double quotes..." \
        "\nresult_2: [\'item1\', \'item2\', \'item3\']" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.convert_str_to_json : Exception standard JSON" \
        "\n::: ERROR :::" \
        "\nFailed to parse string to JSON:" \
        " Expecting property name enclosed in double quotes: line 1 column 2 (char 1)" \
        "\nText size: 30" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.convert_str_to_json : Exception standard JSON" \
        "\n::: ERROR :::" \
        "\nFailed to parse string to JSON: Expecting value: line 1 column 2 (char 1)" \
        "\nText size: 27" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 2

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_convert_str_to_json_malformed_str(self, capsys):
        """ Ensure NewtFiles.convert_str_to_json() returns None for malformed JSON strings. """
        print_my_func_name()

        json_str_1 = "{ invalid json }"
        print("json_str_1:", repr(json_str_1))

        result_1 = NewtFiles.convert_str_to_json(json_str_1)
        assert result_1 is None
        print("result_1:", result_1)

        json_str_2 = "not json at all"
        print("json_str_2:", repr(json_str_2))

        result_2 = NewtFiles.convert_str_to_json(json_str_2)
        assert result_2 is None
        print("result_2:", result_2)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_convert_str_to_json_malformed_str" \
        "\n============================================" \
        "\njson_str_1: '{ invalid json }'" \
        "\nTrying to replace single quotes with double quotes..." \
        "\nresult_1: None" \
        "\njson_str_2: 'not json at all'" \
        "\nTrying to replace single quotes with double quotes..." \
        "\nresult_2: None" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.convert_str_to_json : Exception standard JSON" \
        "\n::: ERROR :::" \
        "\nFailed to parse string to JSON:" \
        " Expecting property name enclosed in double quotes: line 1 column 3 (char 2)" \
        "\nText size: 16" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.convert_str_to_json : Exception replace quotes" \
        "\n::: ERROR :::" \
        "\nFailed to parse string to JSON:" \
        " Expecting property name enclosed in double quotes: line 1 column 3 (char 2)" \
        "\nText size: 16" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.convert_str_to_json : Unknown type" \
        "\n::: ERROR :::" \
        "\nCannot convert STR to JSON." \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.convert_str_to_json : Exception standard JSON" \
        "\n::: ERROR :::" \
        "\nFailed to parse string to JSON: Expecting value: line 1 column 1 (char 0)" \
        "\nText size: 15" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.convert_str_to_json : Exception replace quotes" \
        "\n::: ERROR :::" \
        "\nFailed to parse string to JSON: Expecting value: line 1 column 1 (char 0)" \
        "\nText size: 15" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.convert_str_to_json : Unknown type" \
        "\n::: ERROR :::" \
        "\nCannot convert STR to JSON." \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 6

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


class TestJsonFiles:
    """ Tests for read_json_from_file and save_json_to_file functions. """


    def test_save_and_read_json_from_file(self, capsys):
        """ Ensure NewtFiles.save_json_to_file() and read_json_from_file() round-trip correctly. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmpfile:
            file_json = tmpfile.name

        try:
            content = {"name": "test", "value": 123, "items": [1, 2, 3]}
            print("content:", content)

            NewtFiles.save_json_to_file(file_json, content, obscure_list=obscure_list)

            result_dict = NewtFiles.read_json_from_file(file_json, obscure_list=obscure_list)
            assert isinstance(result_dict, dict)
            assert result_dict == content
            print("result_dict:", result_dict)

            result_txt = NewtFiles.read_text_from_file(file_json, obscure_list=obscure_list)
            print("result_txt:", result_txt)

        finally:
            if os.path.exists(file_json):
                os.unlink(file_json)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.json"
        else:
            file_obscure_name = "/tmp/***********.json"

        assert "Function: test_save_and_read_json_from_file" \
        "\n============================================" \
        "\ncontent: {\'name\': \'test\', \'value\': 123, \'items\': [1, 2, 3]}" \
        "\n[Newt.files.save_json_to_file] Saved JSON to file:" \
        "\n" + file_obscure_name + \
        "\n(type=<class \'dict\'>, indent=2)" \
        "\n[Newt.files.read_json_from_file] Loaded JSON from file:" \
        "\n" + file_obscure_name + \
        "\n(type=<class \'dict\'>)" \
        "\nresult_dict: {\'name\': \'test\', \'value\': 123, \'items\': [1, 2, 3]}" \
        "\n[Newt.files.read_text_from_file] Loaded text from file:" \
        "\n" + file_obscure_name + \
        "\n(length=75)" \
        "\nresult_txt: {\n  \"name\": \"test\",\n  \"value\": 123,\n  \"items\": [\n    1,\n    2,\n    3\n  ]\n}\n" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_save_and_read_json_list_from_file(self, capsys):
        """ Ensure NewtFiles.save_json_to_file() and read_json_from_file() handle list content. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmpfile:
            file_json = tmpfile.name

        try:
            content = [1, 2, 3, {"key": "value"}]
            print("content:", content)

            NewtFiles.save_json_to_file(file_json, content, obscure_list=obscure_list)

            result_list = NewtFiles.read_json_from_file(file_json, obscure_list=obscure_list)
            assert isinstance(result_list, list)
            assert result_list == content
            print("result_list:", result_list)

            result_txt = NewtFiles.read_text_from_file(file_json, obscure_list=obscure_list)
            print("result_txt:", result_txt)

        finally:
            if os.path.exists(file_json):
                os.unlink(file_json)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.json"
        else:
            file_obscure_name = "/tmp/***********.json"

        assert "Function: test_save_and_read_json_list_from_file" \
        "\n============================================" \
        "\ncontent: [1, 2, 3, {\'key\': \'value\'}]" \
        "\n[Newt.files.save_json_to_file] Saved JSON to file:" \
        "\n" + file_obscure_name + \
        "\n(type=<class \'list\'>, indent=2)" \
        "\n[Newt.files.read_json_from_file] Loaded JSON from file:" \
        "\n" + file_obscure_name + \
        "\n(type=<class \'list\'>)" \
        "\nresult_list: [1, 2, 3, {\'key\': \'value\'}]" \
        "\n[Newt.files.read_text_from_file] Loaded text from file:" \
        "\n" + file_obscure_name + \
        "\n(length=46)" \
        "\nresult_txt: [\n  1,\n  2,\n  3,\n  {\n    \"key\": \"value\"\n  }\n]\n" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_save_json_to_file_creates_nested_dirs(self, capsys):
        """ Ensure NewtFiles.save_json_to_file() creates nested dirs and saves JSON correctly. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "level1", "level2", "file.json")

            content = {"test": "data"}
            print("content:", content)

            NewtFiles.save_json_to_file(file_path, content, indent=4, obscure_list=obscure_list)

            result_dict = NewtFiles.read_json_from_file(file_path, obscure_list=obscure_list)
            assert isinstance(result_dict, dict)
            assert result_dict == content
            print("result_dict:", result_dict)

            result_txt = NewtFiles.read_text_from_file(file_path, obscure_list=obscure_list)
            print("result_txt:", result_txt)

            file_exists = os.path.exists(file_path)
            assert file_exists is True
            print("file_exists:", file_exists)

        file_exists = os.path.exists(file_path)
        assert file_exists is False
        print("file_exists:", file_exists)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********\\level1\\level2\\file.json"
        else:
            file_obscure_name = "/tmp/***********/level1/level2/file.json"

        assert "Function: test_save_json_to_file_creates_nested_dirs" \
        "\n============================================" \
        "\ncontent: {\'test\': \'data\'}" \
        "\n[Newt.files.save_json_to_file] Saved JSON to file:" \
        "\n" + file_obscure_name + \
        "\n(type=<class \'dict\'>, indent=4)" \
        "\n[Newt.files.read_json_from_file] Loaded JSON from file:" \
        "\n" + file_obscure_name + \
        "\n(type=<class \'dict\'>)" \
        "\nresult_dict: {\'test\': \'data\'}" \
        "\n[Newt.files.read_text_from_file] Loaded text from file:" \
        "\n" + file_obscure_name + \
        "\n(length=23)" \
        "\nresult_txt: {\n    \"test\": \"data\"\n}\n" \
        "\nfile_exists: True" \
        "\nfile_exists: False" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_read_json_from_file_missing_file(self, capsys):
        """ Ensure NewtFiles.read_json_from_file() returns None for nonexistent file. """
        print_my_func_name()

        result = NewtFiles.read_json_from_file("/nonexistent/file.json", stop=False)
        assert result is None
        print("result:", result)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_read_json_from_file_missing_file" \
        "\n============================================" \
        "\nresult: None" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.check_file_exists : print_log" \
        "\n::: ERROR :::" \
        "\nFile not found: /nonexistent/file.json" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_read_json_from_file_invalid_json(self, capsys):
        """ Ensure NewtFiles.read_json_from_file() exits or returns None for invalid JSON. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmpfile:
            tmpfile.write("{ invalid json }")
            file_json = tmpfile.name

        try:
            with pytest.raises(SystemExit) as exc_info:
                NewtFiles.read_json_from_file(file_json)
                print("This line will not be printed")
            assert exc_info.value.code == 1
            print("exc_info:", exc_info.value.code)

            result = NewtFiles.read_json_from_file(file_json, stop=False)
            assert result is None
            print("result:", result)

        finally:
            if os.path.exists(file_json):
                os.unlink(file_json)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_read_json_from_file_invalid_json" \
        "\n============================================" \
        "\nexc_info: 1" \
        "\nresult: None" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.read_json_from_file : json.load file" \
        "\n::: ERROR :::" \
        "\nFailed to parse content to JSON:" \
        " Expecting property name enclosed in double quotes: line 1 column 3 (char 2)" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.read_json_from_file : json.load file" \
        "\n::: ERROR :::" \
        "\nFailed to parse content to JSON:" \
        " Expecting property name enclosed in double quotes: line 1 column 3 (char 2)" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 2

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


    def test_read_json_from_file_non_dict_or_list(self, capsys):
        """ Ensure NewtFiles.read_json_from_file() returns None for non-dict/list JSON content. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmpfile:
            json.dump("just a string", tmpfile)
            file_json = tmpfile.name

        try:
            result_1 = NewtFiles.read_json_from_file(file_json)
            assert result_1 is None
            print("result_1:", result_1)

            content = {"test": "data"}
            print("content:", content)

            NewtFiles.save_json_to_file(
                file_json, content, indent="text",  # type: ignore
                obscure_list=obscure_list
            )
            NewtFiles.save_json_to_file(
                file_json, content, indent=-8, obscure_list=obscure_list
            )

            result_2 = NewtFiles.read_json_from_file(file_json, obscure_list=obscure_list)
            assert result_2 == content
            print("result_2:", result_2)

        finally:
            if os.path.exists(file_json):
                os.unlink(file_json)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.json"
        else:
            file_obscure_name = "/tmp/***********.json"

        assert "Function: test_read_json_from_file_non_dict_or_list" \
        "\n============================================" \
        "\nresult_1: None" \
        "\ncontent: {'test': 'data'}" \
        "\n[Newt.files.save_json_to_file] Saved JSON to file:" \
        "\n" + file_obscure_name + \
        "\n(type=<class 'dict'>, indent=2)" \
        "\n[Newt.files.save_json_to_file] Saved JSON to file:" \
        "\n" + file_obscure_name + \
        "\n(type=<class 'dict'>, indent=2)" \
        "\n[Newt.files.read_json_from_file] Loaded JSON from file:" \
        "\n" + file_obscure_name + \
        "\n(type=<class 'dict'>)" \
        "\nresult_2: {'test': 'data'}" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.read_json_from_file : content > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: just a string\nReceived type: <class 'str'>" \
        "\nExpected type: (<class 'list'>, <class 'dict'>)" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.save_json_to_file : indent > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: text\nReceived type: <class 'str'>" \
        "\nExpected type: <class 'int'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.save_json_to_file : indent < 0" \
        "\n::: ERROR :::" \
        "\nIndent must be a non-negative integer." \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 3

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


class TestCsvFiles:
    """ Tests for read_csv_from_file and save_csv_to_file functions. """


    def test_save_and_read_csv_multirow(self, capsys):
        """ Ensure NewtFiles.save_csv_to_file() and read_csv_from_file() handle multiple rows. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmpfile:
            file_csv = tmpfile.name

        try:
            rows = [
                ["Name", "Age", "City"],
                ["Alice", "30", "New York"],
                ["Bob", "25", "London"]
            ]
            print("rows:", rows)

            NewtFiles.save_csv_to_file(file_csv, rows, obscure_list=obscure_list)

            result_csv = NewtFiles.read_csv_from_file(file_csv, obscure_list=obscure_list)
            assert result_csv == rows
            print("result_csv:", result_csv)

            result_text = NewtFiles.read_text_from_file(file_csv, obscure_list=obscure_list)
            print("result_text_repr:", repr(result_text))
            print("result_text:")
            print(result_text)

        finally:
            if os.path.exists(file_csv):
                os.unlink(file_csv)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.csv"
        else:
            file_obscure_name = "/tmp/***********.csv"

        assert "Function: test_save_and_read_csv_multirow" \
        "\n============================================" \
        "\nrows: [['Name', 'Age', 'City'], ['Alice', '30', 'New York'], ['Bob', '25', 'London']]" \
        "\n[Newt.files.save_csv_to_file] Saved CSV to file:" \
        "\n" + file_obscure_name + \
        "\n(rows=3, mode=write, delimiter=';')" \
        "\n[Newt.files.read_csv_from_file] Loaded CSV from file:" \
        "\n" + file_obscure_name + \
        "\n(rows=3, delimiter=';')" \
        "\nresult_csv:" \
        " [['Name', 'Age', 'City']," \
        " ['Alice', '30', 'New York']," \
        " ['Bob', '25', 'London']]" \
        "\n[Newt.files.read_text_from_file] Loaded text from file:" \
        "\n" + file_obscure_name + \
        "\n(length=46)" \
        "\nresult_text_repr: 'Name;Age;City\\nAlice;30;New York\\nBob;25;London\\n'" \
        "\nresult_text:\nName;Age;City\nAlice;30;New York\nBob;25;London\n" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_save_and_read_csv_from_file(self, capsys):
        """ Ensure NewtFiles.save_csv_to_file() and read_csv_from_file() round-trip correctly. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmpfile:
            file_csv = tmpfile.name

        try:
            rows_1 = [["A", "B"], ["1", "2"]]
            print("rows_1:", rows_1)

            NewtFiles.save_csv_to_file(file_csv, rows_1, delimiter=",", obscure_list=obscure_list)

            result_csv_1 = NewtFiles.read_csv_from_file(
                file_csv, delimiter=",", obscure_list=obscure_list
            )
            assert result_csv_1 == rows_1
            print("result_csv_1:", result_csv_1)

            result_text_1 = NewtFiles.read_text_from_file(file_csv, obscure_list=obscure_list)
            print("result_text_1:", repr(result_text_1))

            rows_2 = [["C", "D"], ["3", "4"]]
            print("rows_2:", rows_2)

            NewtFiles.save_csv_to_file(
                file_csv, rows_2, append=True, delimiter=",", obscure_list=obscure_list
            )

            result_csv_2 = NewtFiles.read_csv_from_file(
                file_csv, delimiter=",", obscure_list=obscure_list
            )
            assert result_csv_2 == rows_1 + rows_2
            print("result_csv_2:", result_csv_2)

            result_text_2 = NewtFiles.read_text_from_file(file_csv, obscure_list=obscure_list)
            print("result_text_2:", repr(result_text_2))

        finally:
            if os.path.exists(file_csv):
                os.unlink(file_csv)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.csv"
        else:
            file_obscure_name = "/tmp/***********.csv"

        assert "Function: test_save_and_read_csv_from_file" \
        "\n============================================" \
        "\nrows_1: [['A', 'B'], ['1', '2']]" \
        "\n[Newt.files.save_csv_to_file] Saved CSV to file:" \
        "\n" + file_obscure_name + \
        "\n(rows=2, mode=write, delimiter=',')" \
        "\n[Newt.files.read_csv_from_file] Loaded CSV from file:" \
        "\n" + file_obscure_name + \
        "\n(rows=2, delimiter=',')" \
        "\nresult_csv_1: [['A', 'B'], ['1', '2']]" \
        "\n[Newt.files.read_text_from_file] Loaded text from file:" \
        "\n" + file_obscure_name + \
        "\n(length=8)" \
        "\nresult_text_1: 'A,B\\n1,2\\n'" \
        "\nrows_2: [['C', 'D'], ['3', '4']]" \
        "\n[Newt.files.save_csv_to_file] Saved CSV to file:" \
        "\n" + file_obscure_name + \
        "\n(rows=2, mode=append, delimiter=',')" \
        "\n[Newt.files.read_csv_from_file] Loaded CSV from file:" \
        "\n" + file_obscure_name + \
        "\n(rows=4, delimiter=',')" \
        "\nresult_csv_2: [['A', 'B'], ['1', '2'], ['C', 'D'], ['3', '4']]" \
        "\n[Newt.files.read_text_from_file] Loaded text from file:" \
        "\n" + file_obscure_name + \
        "\n(length=16)" \
        "\nresult_text_2: 'A,B\\n1,2\\nC,D\\n3,4\\n'" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_read_csv_from_file_missing_file(self, capsys):
        """ Ensure NewtFiles.read_csv_from_file() returns None for nonexistent file. """
        print_my_func_name()

        result = NewtFiles.read_csv_from_file("/nonexistent/file.csv", stop=False)
        assert result is None
        print("result:", result)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_read_csv_from_file_missing_file" \
        "\n============================================" \
        "\nresult: None" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.check_file_exists : print_log" \
        "\n::: ERROR :::" \
        "\nFile not found: /nonexistent/file.csv" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_save_csv_to_file_creates_nested_dirs(self, capsys):
        """ Ensure NewtFiles.save_csv_to_file() creates nested directories as needed. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "level1", "level2", "file.csv")

            rows = [["Header"], ["Data"]]
            print("rows:", rows)

            NewtFiles.save_csv_to_file(file_path, rows, obscure_list=obscure_list)
            assert os.path.exists(file_path)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********\\level1\\level2\\file.csv"
        else:
            file_obscure_name = "/tmp/***********/level1/level2/file.csv"

        assert "Function: test_save_csv_to_file_creates_nested_dirs" \
        "\n============================================" \
        "\nrows: [['Header'], ['Data']]" \
        "\n[Newt.files.save_csv_to_file] Saved CSV to file:" \
        "\n" + file_obscure_name + \
        "\n(rows=2, mode=write, delimiter=';')" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_save_csv_to_file_normalizes_newlines(self, capsys):
        """ Ensure NewtFiles.save_csv_to_file() strips embedded newlines from cell values. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmpfile:
            file_csv = tmpfile.name

        try:
            rows = [["Cell1\r\nLine2", "Cell2"]]
            print("rows:", rows)

            NewtFiles.save_csv_to_file(file_csv, rows, obscure_list=obscure_list)

            result_csv = NewtFiles.read_csv_from_file(file_csv, obscure_list=obscure_list)
            assert result_csv is not None
            assert "\r\n" not in result_csv[0][0]
            print("result_csv:", repr(result_csv))
            print("result_csv:", result_csv)

            result_text = NewtFiles.read_text_from_file(file_csv, obscure_list=obscure_list)
            print("result_text:", repr(result_text))
            print("result_text:", result_text)

        finally:
            if os.path.exists(file_csv):
                os.unlink(file_csv)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.csv"
        else:
            file_obscure_name = "/tmp/***********.csv"

        assert "Function: test_save_csv_to_file_normalizes_newlines" \
        "\n============================================" \
        "\nrows: [[\'Cell1\\r\\nLine2\', \'Cell2\']]" \
        "\n[Newt.files.save_csv_to_file] Saved CSV to file:" \
        "\n" + file_obscure_name + \
        "\n(rows=1, mode=write, delimiter=\';\')" \
        "\n[Newt.files.read_csv_from_file] Loaded CSV from file:" \
        "\n" + file_obscure_name + \
        "\n(rows=1, delimiter=\';\')" \
        "\nresult_csv: [[\'Cell1\\nLine2\', \'Cell2\']]" \
        "\nresult_csv: [[\'Cell1\\nLine2\', \'Cell2\']]" \
        "\n[Newt.files.read_text_from_file] Loaded text from file:" \
        "\n" + file_obscure_name + \
        "\n(length=20)" \
        "\nresult_text: \'\"Cell1\\nLine2\";Cell2\\n\'" \
        "\nresult_text: \"Cell1\nLine2\";Cell2\n" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_save_csv_to_file_mixed_types(self, capsys):
        """ Ensure NewtFiles.save_csv_to_file() converts mixed-type row values to strings. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmpfile:
            file_csv = tmpfile.name

        try:
            rows = [["String", 123, 45.67, True]]
            print("rows:", rows)

            NewtFiles.save_csv_to_file(file_csv, rows, obscure_list=obscure_list)

            result_csv = NewtFiles.read_csv_from_file(file_csv, obscure_list=obscure_list)
            assert result_csv is not None
            assert all(isinstance(cell, str) for row in result_csv for cell in row)
            print("result_csv:", result_csv)

            result_text = NewtFiles.read_text_from_file(file_csv, obscure_list=obscure_list)
            print("result_text:", repr(result_text))

        finally:
            if os.path.exists(file_csv):
                os.unlink(file_csv)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.csv"
        else:
            file_obscure_name = "/tmp/***********.csv"

        assert "Function: test_save_csv_to_file_mixed_types" \
        "\n============================================" \
        "\nrows: [['String', 123, 45.67, True]]" \
        "\n[Newt.files.save_csv_to_file] Saved CSV to file:" \
        "\n" + file_obscure_name + \
        "\n(rows=1, mode=write, delimiter=';')" \
        "\n[Newt.files.read_csv_from_file] Loaded CSV from file:" \
        "\n" + file_obscure_name + \
        "\n(rows=1, delimiter=';')" \
        "\nresult_csv: [['String', '123', '45.67', 'True']]" \
        "\n[Newt.files.read_text_from_file] Loaded text from file:" \
        "\n" + file_obscure_name + \
        "\n(length=22)" \
        "\nresult_text: 'String;123;45.67;True\\n'" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_save_csv_to_file_invalid_args(self, capsys):
        """ Ensure NewtFiles.save_csv_to_file() exits for invalid filename, rows, or delimiter. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmpfile:
            file_csv = tmpfile.name

        try:
            with pytest.raises(SystemExit) as exc_info_1:
                # Invalid file_name
                NewtFiles.save_csv_to_file(123, [["test"]])  # type: ignore
                print("This line will not be printed")
            assert exc_info_1.value.code == 1
            print("exc_info_1:", exc_info_1.value.code)

            with pytest.raises(SystemExit) as exc_info_2:
                # Invalid rows (not a list)
                NewtFiles.save_csv_to_file(file_csv, "not a list")  # type: ignore
                print("This line will not be printed")
            assert exc_info_2.value.code == 1
            print("exc_info_2:", exc_info_2.value.code)

            with pytest.raises(SystemExit) as exc_info_3:
                # Invalid delimiter
                NewtFiles.save_csv_to_file(file_csv, [["test"]], delimiter=123)  # type: ignore
                print("This line will not be printed")
            assert exc_info_3.value.code == 1
            print("exc_info_3:", exc_info_3.value.code)

            result_text = NewtFiles.read_text_from_file(file_csv, obscure_list=obscure_list)
            assert result_text == ""

        finally:
            if os.path.exists(file_csv):
                os.unlink(file_csv)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.csv"
        else:
            file_obscure_name = "/tmp/***********.csv"

        assert "Function: test_save_csv_to_file_invalid_args" \
        "\n============================================" \
        "\nexc_info_1: 1" \
        "\nexc_info_2: 1" \
        "\nexc_info_3: 1" \
        "\n[Newt.files.read_text_from_file] Loaded text from file:" \
        "\n" + file_obscure_name + \
        "\n(length=0)" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.ensure_dir_exists : file_path > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: 123\nReceived type: <class 'int'>" \
        "\nExpected type: <class 'str'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.save_csv_to_file : rows > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: not a list\nReceived type: <class 'str'>" \
        "\nExpected type: <class 'list'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.files.save_csv_to_file : delimiter > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: 123\nReceived type: <class 'int'>" \
        "\nExpected type: <class 'str'>" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 3

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


    def test_read_csv_from_file_wrong_delimiter(self, capsys):
        """ Ensure NewtFiles.read_csv_from_file() handles wrong delimiter without splitting. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmpfile:
            tmpfile.write("A;B\n1;2")
            file_csv = tmpfile.name

        try:
            # Wrong delimiter
            result = NewtFiles.read_csv_from_file(
                file_csv, delimiter=",", obscure_list=obscure_list
            )
            assert result is not None
            assert isinstance(result, list)
            print("result:", result)
            assert isinstance(result[0][0], str)
            assert result[0][0] == "A;B"
            print("result[0][0]:", repr(result[0][0]))

        finally:
            if os.path.exists(file_csv):
                os.unlink(file_csv)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.csv"
        else:
            file_obscure_name = "/tmp/***********.csv"

        assert "Function: test_read_csv_from_file_wrong_delimiter" \
        "\n============================================" \
        "\n[Newt.files.read_csv_from_file] Loaded CSV from file:" \
        "\n" + file_obscure_name + \
        "\n(rows=2, delimiter=',')" \
        "\nresult: [['A;B'], ['1;2']]" \
        "\nresult[0][0]: 'A;B'" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err
