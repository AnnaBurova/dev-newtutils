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
        file_obscure_name = NewtFiles._obscure_logic(file_name, obscure_list)

        if sys.platform == "win32" and os.name == "nt":
            assert file_obscure_name == "C:\\Users\\*******\\AppData\\Local\\Temp\\**********"
        else:
            assert file_obscure_name == "/tmp/**********"
        print("file_obscure_name:", file_obscure_name)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_obscure_logic_masks_path_segments" \
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

        obscure_list = [
            "C:\\Users\\",
            "\\AppData\\Local\\Temp\\",
            "/tmp/",
            ]
        check_3 = NewtFiles.check_file_exists(file_txt, obscure_list, stop=False)
        assert check_3 is False
        print("check_3:", check_3)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***************"
        else:
            file_obscure_name = "/tmp/***************"

        assert "Function: test_check_file_exists_obscure" \
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
        """ Ensure NewtFiles.choose_file_from_folder() raises SystemExit(1) for invalid folder path. """
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


    def test_choose_file_from_folder_nonexistent_folder_raises_exit(self, capsys):
        """ Ensure NewtFiles.choose_file_from_folder() raises SystemExit for nonexistent folder. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info:
            NewtFiles.choose_file_from_folder("/nonexistent/folder")
            print("This line will not be printed")
        assert exc_info.value.code == 1
        print("exc_info:", exc_info.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_choose_file_from_folder_nonexistent_folder_raises_exit" \
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


    def test_choose_file_from_folder_empty_folder_exit(self, capsys):
        """ Ensure NewtFiles.choose_file_from_folder() raises SystemExit for empty folder. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(SystemExit) as exc_info:
                NewtFiles.choose_file_from_folder(tmpdir)
                print("This line will not be printed")
            assert exc_info.value.code == 1
            print("exc_info:", exc_info.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_choose_file_from_folder_empty_folder_exit" \
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
    def test_choose_file_from_folder_cancel_x_raises_exit(self, mock_input, capsys):
        """ Ensure NewtFiles.choose_file_from_folder() raises SystemExit when user inputs 'X'. """
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

        assert "Function: test_choose_file_from_folder_cancel_x_raises_exit" \
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


    def test_save_and_read_text_file(self, capsys):
        """ Ensure NewtFiles.save_text_to_file() and NewtFiles.read_text_from_file() work correctly. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmpfile:
            file_txt = tmpfile.name

        obscure_list = [
            "C:\\Users\\",
            "\\AppData\\Local\\Temp\\",
            "/tmp/",
            ".txt",
            ]

        try:
            content = "Hello\nWorld!"
            NewtFiles.save_text_to_file(file_txt, content, obscure_list=obscure_list)

            result = NewtFiles.read_text_from_file(file_txt, obscure_list=obscure_list)
            print("result:", repr(result))

            # Note: save_text_to_file() uses _normalize_newlines()
            assert result == content + "\n"

        finally:
            if os.path.exists(file_txt):
                os.unlink(file_txt)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            # On Windows
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.txt"
        else:
            file_obscure_name = "/tmp/***********.txt"

        assert "Function: test_save_and_read_text_file" \
        "\n============================================" \
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


    def test_save_text_creates_directory(self, capsys):
        """ Ensure NewtFiles.save_text_to_file() creates nested parent directories automatically. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "level1", "level2", "file.txt")

            obscure_list = [
                "C:\\Users\\",
                "\\AppData\\Local\\Temp\\",
                "/tmp/",
                "\\level1\\level2\\file.txt",
                "/level1/level2/file.txt",
                ]

            content = "Hello\nWorld!\n"
            NewtFiles.save_text_to_file(file_path, content, obscure_list=obscure_list)

            result = NewtFiles.read_text_from_file(file_path, obscure_list=obscure_list)
            print("result:", repr(result))

            assert result == content

            file_exists = os.path.exists(file_path)
            assert file_exists is True
            print("file_exists:", file_exists)

        file_exists = os.path.exists(file_path)
        assert file_exists is False
        print("file_exists:", file_exists)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            # On Windows
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********\\level1\\level2\\file.txt"
        else:
            file_obscure_name = "/tmp/***********/level1/level2/file.txt"

        assert "Function: test_save_text_creates_directory" \
        "\n============================================" \
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


    def test_save_text_append_mode(self, capsys):
        """ Ensure NewtFiles.save_text_to_file() appends content correctly with append=True. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmpfile:
            file_txt = tmpfile.name

        obscure_list = [
            "C:\\Users\\",
            "\\AppData\\Local\\Temp\\",
            "/tmp/",
            ".txt",
            ]

        try:
            content_1 = "Line 1"
            NewtFiles.save_text_to_file(
                file_txt, content_1, append=False, obscure_list=obscure_list)

            content_2 = "Line 2"
            NewtFiles.save_text_to_file(
                file_txt, content_2, append=True, obscure_list=obscure_list)

            result = NewtFiles.read_text_from_file(file_txt, obscure_list=obscure_list)
            print("result:", repr(result))

            assert result == "Line 1\nLine 2\n"

        finally:
            if os.path.exists(file_txt):
                os.unlink(file_txt)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            # On Windows
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.txt"
        else:
            file_obscure_name = "/tmp/***********.txt"

        assert "Function: test_save_text_append_mode" \
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


    def test_read_text_from_nonexistent_file(self, capsys):
        """ Ensure NewtFiles.read_text_from_file() returns None if file not found and stop=False. """
        print_my_func_name()

        result = NewtFiles.read_text_from_file("/nonexistent/file.txt", stop=False)
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_read_text_from_nonexistent_file" \
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


    def test_save_text_invalid_input(self, capsys):
        """ Ensure NewtFiles.save_text_to_file() raises SystemExit on invalid file or text input. """
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

        assert "Function: test_save_text_invalid_input" \
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


    def test_convert_str_to_json_returns_none_invalid(self, capsys):
        """ Ensure NewtFiles.convert_str_to_json() returns None for invalid or empty inputs. """
        print_my_func_name()

        result_1 = NewtFiles.convert_str_to_json("")
        print("result_1:", repr(result_1))
        assert result_1 is None

        result_2 = NewtFiles.convert_str_to_json("   ")
        print("result_2:", repr(result_2))
        assert result_2 is None

        result_3 = NewtFiles.convert_str_to_json(None)  # type: ignore
        print("result_3:", repr(result_3))
        assert result_3 is None

        result_4 = NewtFiles.convert_str_to_json(123)  # type: ignore
        print("result_4:", repr(result_4))
        assert result_4 is None

        result_5 = NewtFiles.convert_str_to_json(["not", "a", "string"])  # type: ignore
        print("result_5:", repr(result_5))
        assert result_5 is None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_convert_str_to_json_returns_none_invalid" \
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


    def test_convert_str_to_json_valid_json(self, capsys):
        """ Ensure NewtFiles.convert_str_to_json() parses valid JSON dict and list strings. """
        print_my_func_name()

        json_str_1 = '{"name": "test", "value": 123, "items": [1, 2, 3]}'
        print("json_str_1:", repr(json_str_1))

        result_1 = NewtFiles.convert_str_to_json(json_str_1)
        print("result_1:", repr(result_1))

        assert isinstance(result_1, dict)
        assert result_1 == {"name": "test", "value": 123, "items": [1, 2, 3]}

        json_str_2 = '[1, 2, 3, {"key": "value"}]'
        print("json_str_2:", repr(json_str_2))

        result_2 = NewtFiles.convert_str_to_json(json_str_2)
        print("result_2:", repr(result_2))

        assert isinstance(result_2, list)
        assert result_2 == [1, 2, 3, {"key": "value"}]

        json_str_3 = '{"outer": {"inner": {"deep": [1, 2, 3]}}}'
        print("json_str_3:", repr(json_str_3))

        result_3 = NewtFiles.convert_str_to_json(json_str_3)
        print("result_3:", repr(result_3))

        assert isinstance(result_3, dict)
        assert result_3 == {"outer": {"inner": {"deep": [1, 2, 3]}}}

        json_str_4 = '   {"key": "value"}   '
        print("json_str_4:", repr(json_str_4))

        result_4 = NewtFiles.convert_str_to_json(json_str_4)
        print("result_4:", repr(result_4))

        assert isinstance(result_4, dict)
        assert result_4 == {"key": "value"}

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_convert_str_to_json_valid_json" \
        "\n============================================" \
        "\njson_str_1: \'{\"name\": \"test\", \"value\": 123, \"items\": [1, 2, 3]}\'" \
        "\nresult_1: {\'name\': \'test\', \'value\': 123, \'items\': [1, 2, 3]}" \
        "\njson_str_2: \'[1, 2, 3, {\"key\": \"value\"}]\'" \
        "\nresult_2: [1, 2, 3, {\'key\': \'value\'}]" \
        "\njson_str_3: \'{\"outer\": {\"inner\": {\"deep\": [1, 2, 3]}}}\'" \
        "\nresult_3: {\'outer\': {\'inner\': {\'deep\': [1, 2, 3]}}}" \
        "\njson_str_4: '   {\"key\": \"value\"}   '" \
        "\nresult_4: {'key': 'value'}" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_convert_str_to_json_single_quotes(self, capsys):
        """ Ensure NewtFiles.convert_str_to_json() parses single-quoted dict and list strings. """
        print_my_func_name()

        json_str_1 = "{'name': 'test', 'value': 123}"
        print("json_str_1:", repr(json_str_1))

        result_1 = NewtFiles.convert_str_to_json(json_str_1)
        print("result_1:", repr(result_1))

        assert isinstance(result_1, dict)
        assert result_1 == {"name": "test", "value": 123}

        json_str_2 = "['item1', 'item2', 'item3']"
        print("json_str_2:", repr(json_str_2))

        result_2 = NewtFiles.convert_str_to_json(json_str_2)
        print("result_2:", repr(result_2))

        assert isinstance(result_2, list)
        assert result_2 == ["item1", "item2", "item3"]

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_convert_str_to_json_single_quotes" \
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


    def test_invalid_json_prints_errors(self, capsys):
        """ Ensure invalid JSON returns None and prints expected error messages. """
        print_my_func_name()

        json_str_1 = "{ invalid json }"
        print("json_str_1:", repr(json_str_1))

        result_1 = NewtFiles.convert_str_to_json(json_str_1)
        print("result_1:", repr(result_1))
        assert result_1 is None

        json_str_2 = "not json at all"
        print("json_str_2:", repr(json_str_2))

        result_2 = NewtFiles.convert_str_to_json(json_str_2)
        print("result_2:", repr(result_2))
        assert result_2 is None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_invalid_json_prints_errors" \
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


    def test_save_and_read_json_file_dict(self, capsys):
        """ Ensure NewtFiles.save_json_to_file() and NewtFiles.read_json_from_file() work with dict. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmpfile:
            file_json = tmpfile.name

        obscure_list = [
            "C:\\Users\\",
            "\\AppData\\Local\\Temp\\",
            "/tmp/",
            ".json",
            ]

        try:
            content = {"name": "test", "value": 123, "items": [1, 2, 3]}
            print("content:", repr(content))
            NewtFiles.save_json_to_file(file_json, content, obscure_list=obscure_list)

            result_dict = NewtFiles.read_json_from_file(file_json, obscure_list=obscure_list)
            print("result_dict:", repr(result_dict))
            assert isinstance(result_dict, dict)

            assert result_dict == content

            result_txt = NewtFiles.read_text_from_file(file_json, obscure_list=obscure_list)
            print("result_txt:", repr(result_txt))

        finally:
            if os.path.exists(file_json):
                os.unlink(file_json)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            # On Windows
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.json"
        else:
            file_obscure_name = "/tmp/***********.json"

        assert "Function: test_save_and_read_json_file_dict" \
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
        "\nresult_txt: \'{\\n  \"name\": \"test\",\\n  \"value\": 123,\\n  \"items\":" \
        " [\\n    1,\\n    2,\\n    3\\n  ]\\n}\\n\'" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_save_and_read_json_file_list(self, capsys):
        """ Ensure NewtFiles.save_json_to_file() and NewtFiles.read_json_from_file() work with list. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmpfile:
            file_json = tmpfile.name

        obscure_list = [
            "C:\\Users\\",
            "\\AppData\\Local\\Temp\\",
            "/tmp/",
            ".json",
            ]

        try:
            content = [1, 2, 3, {"key": "value"}]
            print("content:", repr(content))
            NewtFiles.save_json_to_file(file_json, content, obscure_list=obscure_list)

            result_list = NewtFiles.read_json_from_file(file_json, obscure_list=obscure_list)
            print("result_list:", repr(result_list))
            assert isinstance(result_list, list)

            assert result_list == content

            result_txt = NewtFiles.read_text_from_file(file_json, obscure_list=obscure_list)
            print("result_txt:", repr(result_txt))

        finally:
            if os.path.exists(file_json):
                os.unlink(file_json)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            # On Windows
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.json"
        else:
            file_obscure_name = "/tmp/***********.json"

        assert "Function: test_save_and_read_json_file_list" \
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
        "\nresult_txt: \'[\\n  1,\\n  2,\\n  3,\\n  {\\n    \"key\": \"value\"\\n  }\\n]\\n\'" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_save_and_read_json_file_nested_dirs(self, capsys):
        """ Ensure NewtFiles.save_json_to_file() works with nested directories. """
        print_my_func_name()

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "level1", "level2", "file.json")

            obscure_list = [
                "C:\\Users\\",
                "\\AppData\\Local\\Temp\\",
                "/tmp/",
                "\\level1\\level2\\file.json",
                "/level1/level2/file.json",
                ]

            content = {"test": "data"}
            print("content:", repr(content))
            NewtFiles.save_json_to_file(file_path, content, indent=4, obscure_list=obscure_list)

            result_dict = NewtFiles.read_json_from_file(file_path, obscure_list=obscure_list)
            print("result_dict:", repr(result_dict))
            assert isinstance(result_dict, dict)

            assert result_dict == content

            result_txt = NewtFiles.read_text_from_file(file_path, obscure_list=obscure_list)
            print("result_txt:", repr(result_txt))

            file_exists = os.path.exists(file_path)
            assert file_exists is True
            print("file_exists:", file_exists)

        file_exists = os.path.exists(file_path)
        assert file_exists is False
        print("file_exists:", file_exists)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            # On Windows
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********\\level1\\level2\\file.json"
        else:
            file_obscure_name = "/tmp/***********/level1/level2/file.json"

        assert "Function: test_save_and_read_json_file_nested_dirs" \
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
        "\nresult_txt: \'{\\n    \"test\": \"data\"\\n}\\n\'" \
        "\nfile_exists: True" \
        "\nfile_exists: False" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_read_json_from_nonexistent_file(self, capsys):
        """ Ensure NewtFiles.read_json_from_file() returns None for nonexistent file. """
        print_my_func_name()

        result = NewtFiles.read_json_from_file("/nonexistent/file.json", stop=False)
        print("result:", repr(result))
        assert result == None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_read_json_from_nonexistent_file" \
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


    def test_read_json_invalid_file_content(self, capsys):
        """ Ensure NewtFiles.read_json_from_file() raises SystemExit on invalid JSON. """
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
            print("result:", repr(result))
            assert result == None

        finally:
            if os.path.exists(file_json):
                os.unlink(file_json)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_read_json_invalid_file_content" \
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


    def test_read_json_from_file_non_dict(self, capsys):
        """ Ensure NewtFiles.read_json_from_file() returns None for non-dict JSON. """
        print_my_func_name()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmpfile:
            json.dump("just a string", tmpfile)
            file_json = tmpfile.name

        obscure_list = [
            "C:\\Users\\",
            "\\AppData\\Local\\Temp\\",
            "/tmp/",
            ".json",
            ]

        try:
            result = NewtFiles.read_json_from_file(file_json)
            print("result:", repr(result))
            assert result == None

            content = {"test": "data"}
            NewtFiles.save_json_to_file(
                file_json, content, indent="text",  # type: ignore
                obscure_list=obscure_list
            )
            NewtFiles.save_json_to_file(
                file_json, content, indent=-8,
                obscure_list=obscure_list
            )

        finally:
            if os.path.exists(file_json):
                os.unlink(file_json)

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            # On Windows
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********.json"
        else:
            file_obscure_name = "/tmp/***********.json"

        assert "Function: test_read_json_from_file_non_dict" \
        "\n============================================" \
        "\nresult: None" \
        "\n[Newt.files.save_json_to_file] Saved JSON to file:" \
        "\n" + file_obscure_name + \
        "\n(type=<class 'dict'>, indent=2)" \
        "\n[Newt.files.save_json_to_file] Saved JSON to file:" \
        "\n" + file_obscure_name + \
        "\n(type=<class 'dict'>, indent=2)" \
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
