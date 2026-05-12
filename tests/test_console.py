"""
Updated on 2026-05
Created on 2025-11

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.console module.

Tests cover:
- TestDivider
- TestErrorMsg
- TestValidateType
- TestBeepBoop
- TestRetryPause
- TestCheckLocation
"""

import sys
import os
import pytest
from unittest.mock import patch

from .helpers import print_my_func_name, print_my_captured, format_set_to_str
import newtutils.console as NewtCons


class TestDivider:
    """ Tests for divider function. """


    def test_divider_output(self, capsys):
        """ Ensure NewtCons._divider() prints the expected divider line and no error message. """
        print_my_func_name()

        NewtCons._divider()

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_divider_output" \
        "\n============================================" \
        "\n\n--------------------------------------------------\n" \
        "\n" == captured.out
        assert "" == captured.err

        assert "\n" + "-----" * 10 + "\n" in captured.out

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


class TestErrorMsg:
    """ Tests for error_msg function. """


    def test_error_msg_with_stop(self, capsys):
        """ Ensure NewtCons.error_msg() with stop=True raises SystemExit and prints the correct error output. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info:
            NewtCons.error_msg("Test error")
            print("This line will not be printed")
        assert exc_info.value.code == 1
        print("exc_info:", exc_info.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_error_msg_with_stop" \
        "\n============================================" \
        "\nexc_info: 1" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Unknown" \
        "\n::: ERROR :::" \
        "\nTest error" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


    def test_error_msg_without_stop(self, capsys):
        """ Ensure NewtCons.error_msg() with stop=False prints error to stderr without raising SystemExit. """
        print_my_func_name()

        NewtCons.error_msg("Test error", stop=False)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_error_msg_without_stop" \
        "\n============================================" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Unknown" \
        "\n::: ERROR :::" \
        "\nTest error" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_error_msg_multiple_args(self, capsys):
        """ Ensure NewtCons.error_msg() with multiple args prints all messages to stderr correctly. """
        print_my_func_name()

        NewtCons.error_msg(
            "Error 1",
            "Error 2",
            "Error 3",
            stop=False
        )

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_error_msg_multiple_args" \
        "\n============================================" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Unknown" \
        "\n::: ERROR :::" \
        "\nError 1\nError 2\nError 3" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_error_msg_with_location(self, capsys):
        """ Ensure NewtCons.error_msg() with a custom location prints it correctly to stderr. """
        print_my_func_name()

        NewtCons.error_msg(
            "Test error",
            location="test.module",
            stop=False
        )

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_error_msg_with_location" \
        "\n============================================" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: test.module" \
        "\n::: ERROR :::" \
        "\nTest error" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


class TestValidateType:
    """ Tests for validate_type function. """


    def test_validate_type_returns_true_for_all_basic_types(self, capsys):
        """ Ensure NewtCons.validate_type() returns True for all basic Python types with valid inputs. """
        print_my_func_name()

        input_None = None
        print("input_None:", input_None, "/", type(input_None))
        assert NewtCons.validate_type(input_None, type(None)) is True

        input_bool = False
        print("input_bool:", input_bool, "/", type(input_bool))
        assert NewtCons.validate_type(input_bool, bool) is True

        input_int = 123
        print("input_int:", input_int, "/", type(input_int))
        assert NewtCons.validate_type(input_int, int) is True

        input_float = 3.14
        print("input_float:", input_float, "/", type(input_float))
        assert NewtCons.validate_type(input_float, float) is True

        input_str = "Hello"
        print("input_str:", input_str, "/", type(input_str))
        assert NewtCons.validate_type(input_str, str) is True

        input_bytes = b"Hello"
        print("input_bytes:", input_bytes, "/", type(input_bytes))
        assert NewtCons.validate_type(input_bytes, bytes) is True

        input_list = [input_bool, input_int, input_float, input_str]
        print("input_list:", input_list, "/", type(input_list))
        assert NewtCons.validate_type(input_list, list) is True

        input_tuple = (input_bool, input_int, input_float, input_str)
        print("input_tuple:", input_tuple, "/", type(input_tuple))
        assert NewtCons.validate_type(input_tuple, tuple) is True

        input_dict = {1: input_bool, 2: input_int, 3: input_float, 4: input_str}
        print("input_dict:", input_dict, "/", type(input_dict))
        assert NewtCons.validate_type(input_dict, dict) is True

        input_set = {input_bool, input_int, input_float, input_str}
        print(f"input_set: {format_set_to_str(input_set)} / {type(input_set)}")
        assert NewtCons.validate_type(input_set, set) is True

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_validate_type_returns_true_for_all_basic_types" \
        "\n============================================" \
        "\ninput_None: None / <class 'NoneType'>" \
        "\ninput_bool: False / <class 'bool'>" \
        "\ninput_int: 123 / <class 'int'>" \
        "\ninput_float: 3.14 / <class 'float'>" \
        "\ninput_str: Hello / <class 'str'>" \
        "\ninput_bytes: b'Hello' / <class 'bytes'>" \
        "\ninput_list: [False, 123, 3.14, 'Hello'] / <class 'list'>" \
        "\ninput_tuple: (False, 123, 3.14, 'Hello') / <class 'tuple'>" \
        "\ninput_dict: {1: False, 2: 123, 3: 3.14, 4: 'Hello'} / <class 'dict'>" \
        "\ninput_set: {123, 3.14, False, Hello} / <class 'set'>" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_validate_type_incorrect_type_no_stop(self, capsys):
        """ Ensure NewtCons.validate_type() returns False and outputs error to stderr for all mismatched types with stop=False. """
        print_my_func_name()

        input_None = None
        print("input_None:", input_None, "/", type(input_None))
        assert NewtCons.validate_type(input_None, frozenset, stop=False) is False

        input_bool = False
        print("input_bool:", input_bool, "/", type(input_bool))
        assert NewtCons.validate_type(input_bool, frozenset, stop=False) is False

        input_int = 123
        print("input_int:", input_int, "/", type(input_int))
        assert NewtCons.validate_type(input_int, frozenset, stop=False) is False

        input_float = 3.14
        print("input_float:", input_float, "/", type(input_float))
        assert NewtCons.validate_type(input_float, frozenset, stop=False) is False

        input_str = "Hello"
        print("input_str:", input_str, "/", type(input_str))
        assert NewtCons.validate_type(input_str, frozenset, stop=False) is False

        input_bytes = b"Hello"
        print("input_bytes:", input_bytes, "/", type(input_bytes))
        assert NewtCons.validate_type(input_bytes, frozenset, stop=False) is False

        input_list = [input_bool, input_int, input_float, input_str]
        print("input_list:", input_list, "/", type(input_list))
        assert NewtCons.validate_type(input_list, frozenset, stop=False) is False

        input_tuple = (input_bool, input_int, input_float, input_str)
        print("input_tuple:", input_tuple, "/", type(input_tuple))
        assert NewtCons.validate_type(input_tuple, frozenset, stop=False) is False

        input_dict = {1: input_bool, 2: input_int, 3: input_float, 4: input_str}
        print("input_dict:", input_dict, "/", type(input_dict))
        assert NewtCons.validate_type(input_dict, frozenset, stop=False) is False

        input_set = {input_bool, input_int, input_float, input_str}
        print(f"input_set: {format_set_to_str(input_set)} / {type(input_set)}")
        assert NewtCons.validate_type(input_set, frozenset, stop=False) is False

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_validate_type_incorrect_type_no_stop" \
        "\n============================================" \
        "\ninput_None: None / <class 'NoneType'>" \
        "\ninput_bool: False / <class 'bool'>" \
        "\ninput_int: 123 / <class 'int'>" \
        "\ninput_float: 3.14 / <class 'float'>" \
        "\ninput_str: Hello / <class 'str'>" \
        "\ninput_bytes: b'Hello' / <class 'bytes'>" \
        "\ninput_list: [False, 123, 3.14, 'Hello'] / <class 'list'>" \
        "\ninput_tuple: (False, 123, 3.14, 'Hello') / <class 'tuple'>" \
        "\ninput_dict: {1: False, 2: 123, 3: 3.14, 4: 'Hello'} / <class 'dict'>" \
        "\ninput_set: {123, 3.14, False, Hello} / <class 'set'>" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: None\nReceived type: <class 'NoneType'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: False\nReceived type: <class 'bool'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: 123\nReceived type: <class 'int'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: 3.14\nReceived type: <class 'float'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: Hello\nReceived type: <class 'str'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: b'Hello'\nReceived type: <class 'bytes'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: [False, 123, 3.14, 'Hello']\nReceived type: <class 'list'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: (False, 123, 3.14, 'Hello')\nReceived type: <class 'tuple'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: {1: False, 2: 123, 3: 3.14, 4: 'Hello'}\nReceived type: <class 'dict'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: {123, 3.14, False, Hello}\nReceived type: <class 'set'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 10

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_validate_type_incorrect_type_with_stop(self, capsys):
        """ Ensure NewtCons.validate_type() raises SystemExit for all mismatched types and prints errors to stderr with stop=True. """
        print_my_func_name()

        input_None = None
        print("input_None:", input_None, "/", type(input_None))
        with pytest.raises(SystemExit) as exc_info_None:
            NewtCons.validate_type(input_None, frozenset)
            print("This line will not be printed")
        assert exc_info_None.value.code == 1
        print("exc_info_None:", exc_info_None.value.code)

        input_bool = False
        print("input_bool:", input_bool, "/", type(input_bool))
        with pytest.raises(SystemExit) as exc_info_bool:
            NewtCons.validate_type(input_bool, frozenset)
            print("This line will not be printed")
        assert exc_info_bool.value.code == 1
        print("exc_info_bool:", exc_info_bool.value.code)

        input_int = 123
        print("input_int:", input_int, "/", type(input_int))
        with pytest.raises(SystemExit) as exc_info_int:
            NewtCons.validate_type(input_int, frozenset)
            print("This line will not be printed")
        assert exc_info_int.value.code == 1
        print("exc_info_int:", exc_info_int.value.code)

        input_float = 3.14
        print("input_float:", input_float, "/", type(input_float))
        with pytest.raises(SystemExit) as exc_info_float:
            NewtCons.validate_type(input_float, frozenset)
            print("This line will not be printed")
        assert exc_info_float.value.code == 1
        print("exc_info_float:", exc_info_float.value.code)

        input_str = "Hello"
        print("input_str:", input_str, "/", type(input_str))
        with pytest.raises(SystemExit) as exc_info_str:
            NewtCons.validate_type(input_str, frozenset)
            print("This line will not be printed")
        assert exc_info_str.value.code == 1
        print("exc_info_str:", exc_info_str.value.code)

        input_bytes = b"Hello"
        print("input_bytes:", input_bytes, "/", type(input_bytes))
        with pytest.raises(SystemExit) as exc_info_bytes:
            NewtCons.validate_type(input_bytes, frozenset)
            print("This line will not be printed")
        assert exc_info_bytes.value.code == 1
        print("exc_info_bytes:", exc_info_bytes.value.code)

        input_list = [input_bool, input_int, input_float, input_str]
        print("input_list:", input_list, "/", type(input_list))
        with pytest.raises(SystemExit) as exc_info_list:
            NewtCons.validate_type(input_list, frozenset)
            print("This line will not be printed")
        assert exc_info_list.value.code == 1
        print("exc_info_list:", exc_info_list.value.code)

        input_tuple = (input_bool, input_int, input_float, input_str)
        print("input_tuple:", input_tuple, "/", type(input_tuple))
        with pytest.raises(SystemExit) as exc_info_tuple:
            NewtCons.validate_type(input_tuple, frozenset)
            print("This line will not be printed")
        assert exc_info_tuple.value.code == 1
        print("exc_info_tuple:", exc_info_tuple.value.code)

        input_dict = {1: input_bool, 2: input_int, 3: input_float, 4: input_str}
        print("input_dict:", input_dict, "/", type(input_dict))
        with pytest.raises(SystemExit) as exc_info_dict:
            NewtCons.validate_type(input_dict, frozenset)
            print("This line will not be printed")
        assert exc_info_dict.value.code == 1
        print("exc_info_dict:", exc_info_dict.value.code)

        input_set = {input_bool, input_int, input_float, input_str}
        print(f"input_set: {format_set_to_str(input_set)} / {type(input_set)}")
        with pytest.raises(SystemExit) as exc_info_set:
            NewtCons.validate_type(input_set, frozenset)
            print("This line will not be printed")
        assert exc_info_set.value.code == 1
        print("exc_info_set:", exc_info_set.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_validate_type_incorrect_type_with_stop" \
        "\n============================================" \
        "\ninput_None: None / <class 'NoneType'>" \
        "\nexc_info_None: 1" \
        "\ninput_bool: False / <class 'bool'>" \
        "\nexc_info_bool: 1" \
        "\ninput_int: 123 / <class 'int'>" \
        "\nexc_info_int: 1" \
        "\ninput_float: 3.14 / <class 'float'>" \
        "\nexc_info_float: 1" \
        "\ninput_str: Hello / <class 'str'>" \
        "\nexc_info_str: 1" \
        "\ninput_bytes: b'Hello' / <class 'bytes'>" \
        "\nexc_info_bytes: 1" \
        "\ninput_list: [False, 123, 3.14, 'Hello'] / <class 'list'>" \
        "\nexc_info_list: 1" \
        "\ninput_tuple: (False, 123, 3.14, 'Hello') / <class 'tuple'>" \
        "\nexc_info_tuple: 1" \
        "\ninput_dict: {1: False, 2: 123, 3: 3.14, 4: 'Hello'} / <class 'dict'>" \
        "\nexc_info_dict: 1" \
        "\ninput_set: {123, 3.14, False, Hello} / <class 'set'>" \
        "\nexc_info_set: 1" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: None\nReceived type: <class 'NoneType'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: False\nReceived type: <class 'bool'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: 123\nReceived type: <class 'int'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: 3.14\nReceived type: <class 'float'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: Hello\nReceived type: <class 'str'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: b'Hello'\nReceived type: <class 'bytes'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: [False, 123, 3.14, 'Hello']\nReceived type: <class 'list'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: (False, 123, 3.14, 'Hello')\nReceived type: <class 'tuple'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: {1: False, 2: 123, 3: 3.14, 4: 'Hello'}\nReceived type: <class 'dict'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: {123, 3.14, False, Hello}\nReceived type: <class 'set'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 10

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


    def test_validate_type_multiple_types(self, capsys):
        """ Ensure NewtCons.validate_type() accepts values matching a tuple of allowed types and rejects others with stop=False. """
        print_my_func_name()

        input_int = 123
        print("input_int:", input_int, "/", type(input_int))
        assert NewtCons.validate_type(input_int, (int, str), stop=False) is True

        input_float = 3.14
        print("input_float:", input_float, "/", type(input_float))
        assert NewtCons.validate_type(input_float, (int, str), stop=False) is False

        input_str = "Hello"
        print("input_str:", input_str, "/", type(input_str))
        assert NewtCons.validate_type(input_str, (int, str), stop=False) is True

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_validate_type_multiple_types" \
        "\n============================================" \
        "\ninput_int: 123 / <class 'int'>" \
        "\ninput_float: 3.14 / <class 'float'>" \
        "\ninput_str: Hello / <class 'str'>" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: 3.14\nReceived type: <class 'float'>" \
        "\nExpected type: (<class 'int'>, <class 'str'>)" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_validate_type_with_location(self, capsys):
        """ Ensure NewtCons.validate_type() with stop=False outputs custom location in error message to stderr on type mismatch. """
        print_my_func_name()

        input_int = 123
        print("input_int:", input_int, "/", type(input_int))
        assert NewtCons.validate_type(
            input_int, frozenset, stop=False,
            location="test.input_int"
        ) is False

        input_float = 3.14
        print("input_float:", input_float, "/", type(input_float))
        assert NewtCons.validate_type(
            input_float, frozenset, stop=False,
            location="test.input_float"
        ) is False

        input_str = "Hello"
        print("input_str:", input_str, "/", type(input_str))
        assert NewtCons.validate_type(
            input_str, frozenset, stop=False,
            location="test.input_str"
        ) is False

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_validate_type_with_location" \
        "\n============================================" \
        "\ninput_int: 123 / <class 'int'>" \
        "\ninput_float: 3.14 / <class 'float'>" \
        "\ninput_str: Hello / <class 'str'>" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: test.input_int > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: 123\nReceived type: <class 'int'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: test.input_float > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: 3.14\nReceived type: <class 'float'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: test.input_str > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: Hello\nReceived type: <class 'str'>" \
        "\nExpected type: <class 'frozenset'>" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 3

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_validate_type_empty_values_with_check_non_empty(self, capsys):
        """ Ensure NewtCons.validate_type() returns False for all falsy/empty values when check_non_empty=True. """
        print_my_func_name()

        input_None = None
        print("input_None:", input_None, "/", type(input_None))
        assert NewtCons.validate_type(input_None, type(None),
            check_non_empty=True, stop=False) is False

        input_bool = False
        print("input_bool:", input_bool, "/", type(input_bool))
        assert NewtCons.validate_type(input_bool, bool,
            check_non_empty=True, stop=False) is False

        input_int = 0
        print("input_int:", input_int, "/", type(input_int))
        assert NewtCons.validate_type(input_int, int,
            check_non_empty=True, stop=False) is False

        input_float = 0.0
        print("input_float:", input_float, "/", type(input_float))
        assert NewtCons.validate_type(input_float, float,
            check_non_empty=True, stop=False) is False

        input_str = ""
        print("input_str:", input_str, "/", type(input_str))
        assert NewtCons.validate_type(input_str, str,
            check_non_empty=True, stop=False) is False

        input_bytes = b""
        print("input_bytes:", input_bytes, "/", type(input_bytes))
        assert NewtCons.validate_type(input_bytes, bytes,
            check_non_empty=True, stop=False) is False

        input_list = []
        print("input_list:", input_list, "/", type(input_list))
        assert NewtCons.validate_type(input_list, list,
            check_non_empty=True, stop=False) is False

        input_tuple = ()
        print("input_tuple:", input_tuple, "/", type(input_tuple))
        assert NewtCons.validate_type(input_tuple, tuple,
            check_non_empty=True, stop=False) is False

        input_dict = {}
        print("input_dict:", input_dict, "/", type(input_dict))
        assert NewtCons.validate_type(input_dict, dict,
            check_non_empty=True, stop=False) is False

        input_set = set()
        print("input_set:", input_set, "/", type(input_set))
        assert NewtCons.validate_type(input_set, set,
            check_non_empty=True, stop=False) is False

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_validate_type_empty_values_with_check_non_empty" \
        "\n============================================" \
        "\ninput_None: None / <class 'NoneType'>" \
        "\ninput_bool: False / <class 'bool'>" \
        "\ninput_int: 0 / <class 'int'>" \
        "\ninput_float: 0.0 / <class 'float'>" \
        "\ninput_str:  / <class 'str'>" \
        "\ninput_bytes: b'' / <class 'bytes'>" \
        "\ninput_list: [] / <class 'list'>" \
        "\ninput_tuple: () / <class 'tuple'>" \
        "\ninput_dict: {} / <class 'dict'>" \
        "\ninput_set: set() / <class 'set'>" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type : is_empty" \
        "\n::: ERROR :::" \
        "\nValue must not be empty\nValue: None\nType: <class 'NoneType'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type : is_empty" \
        "\n::: ERROR :::" \
        "\nValue must not be empty\nValue: False\nType: <class 'bool'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type : is_empty" \
        "\n::: ERROR :::" \
        "\nValue must not be empty\nValue: 0\nType: <class 'int'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type : is_empty" \
        "\n::: ERROR :::" \
        "\nValue must not be empty\nValue: 0.0\nType: <class 'float'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type : is_empty" \
        "\n::: ERROR :::" \
        "\nValue must not be empty\nValue: \nType: <class 'str'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type : is_empty" \
        "\n::: ERROR :::" \
        "\nValue must not be empty\nValue: b''\nType: <class 'bytes'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type : is_empty" \
        "\n::: ERROR :::" \
        "\nValue must not be empty\nValue: []\nType: <class 'list'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type : is_empty" \
        "\n::: ERROR :::" \
        "\nValue must not be empty\nValue: ()\nType: <class 'tuple'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type : is_empty" \
        "\n::: ERROR :::" \
        "\nValue must not be empty\nValue: {}\nType: <class 'dict'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type : is_empty" \
        "\n::: ERROR :::" \
        "\nValue must not be empty\nValue: {}\nType: <class 'set'>" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 10

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_validate_type_unsupported_type_check_non_empty(self, capsys):
        """ Ensure NewtCons.validate_type() errors when check_non_empty=True is used with an unsupported type like frozenset. """
        print_my_func_name()

        input_frozenset = frozenset()
        print("input_frozenset:", input_frozenset, "/", type(input_frozenset))
        assert NewtCons.validate_type(input_frozenset, frozenset,
            check_non_empty=True, stop=False) is False

        input_frozenset_stop = frozenset()
        print("input_frozenset_stop:", input_frozenset_stop, "/", type(input_frozenset_stop))
        with pytest.raises(SystemExit) as exc_info_frozenset:
            NewtCons.validate_type(input_frozenset_stop, frozenset, check_non_empty=True)
            print("This line will not be printed")
        assert exc_info_frozenset.value.code == 1
        print("exc_info_frozenset:", exc_info_frozenset.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_validate_type_unsupported_type_check_non_empty" \
        "\n============================================" \
        "\ninput_frozenset: frozenset() / <class 'frozenset'>" \
        "\ninput_frozenset_stop: frozenset() / <class 'frozenset'>" \
        "\nexc_info_frozenset: 1" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type : check_non_empty" \
        "\n::: ERROR :::" \
        "\ncheck_non_empty is not supported for this type" \
        "\nValue: frozenset()\nType: <class 'frozenset'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.validate_type : check_non_empty" \
        "\n::: ERROR :::" \
        "\ncheck_non_empty is not supported for this type" \
        "\nValue: frozenset()\nType: <class 'frozenset'>" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 2

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


class TestBeepBoop:
    """ Tests for _beep_boop function. """


    @patch("newtutils.console.time.sleep")
    def test_beep_boop_platform_behavior(self, mock_sleep, capsys):
        """ Ensure NewtCons._beep_boop() calls Beep and sleep twice on Windows, or prints a message on other platforms. """
        print_my_func_name()

        if sys.platform == "win32" and os.name == "nt":
            # On Windows: mock only Beep (module exists)
            with patch("newtutils.console.winsound.Beep") as mock_beep:
                NewtCons._beep_boop()
                assert mock_beep.call_count == 2
                assert mock_sleep.call_count == 2
        else:
            NewtCons._beep_boop()

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            assert "Function: test_beep_boop_platform_behavior" \
            "\n============================================" \
            "\n" == captured.out
        else:
            assert "Function: test_beep_boop_platform_behavior" \
            "\n============================================" \
            "\n\x1b[1m\x1b[32m" \
            "\nBeep Boop !!!" \
            "\n\x1b[0m" \
            "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


class TestRetryPause:
    """ Tests for _retry_pause function. """


    @patch("newtutils.console._beep_boop")
    @patch("newtutils.console.time.sleep")
    def test_retry_pause_two_seconds(self, mock_sleep, mock_beep, capsys):
        """ Ensure NewtCons._retry_pause(2) calls _beep_boop once, sleeps twice, and prints a 2-second countdown to stdout. """
        print_my_func_name()

        NewtCons._retry_pause(seconds=2)
        mock_beep.assert_called_once()
        assert mock_beep.call_count == 1
        assert mock_sleep.call_count == 2

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_retry_pause_two_seconds" \
        "\n============================================" \
        "\nRetrying in 2 seconds..." \
        "\nTime left: 2s" \
        "\nTime left: 1s" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err
        assert "Time left: 5s" not in captured.out
        assert "Time left: 4s" not in captured.out
        assert "Time left: 3s" not in captured.out


    @patch("newtutils.console._beep_boop")
    @patch("newtutils.console.time.sleep")
    def test_retry_pause_three_seconds_no_beep(self, mock_sleep, mock_beep, capsys):
        """ Ensure NewtCons._retry_pause(3, beep=False) skips _beep_boop, sleeps three times, and prints a 3-second countdown. """
        print_my_func_name()

        NewtCons._retry_pause(seconds=3, beep=False)
        assert mock_beep.call_count == 0
        assert mock_sleep.call_count == 3

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_retry_pause_three_seconds_no_beep" \
        "\n============================================" \
        "\nRetrying in 3 seconds..." \
        "\nTime left: 3s" \
        "\nTime left: 2s" \
        "\nTime left: 1s" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err
        assert "Time left: 5s" not in captured.out
        assert "Time left: 4s" not in captured.out


    @patch("newtutils.console.time.sleep")
    def test_retry_pause_falls_back_to_default_on_invalid_type(self, mock_sleep, capsys):
        """ Ensure NewtCons._retry_pause() defaults to 5s countdown and outputs a type error to stderr when seconds is not an int. """
        print_my_func_name()

        NewtCons._retry_pause(seconds="invalid", beep=False)  # type: ignore
        # Should sleep 5 times (once per second)
        assert mock_sleep.call_count == 5

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_retry_pause_falls_back_to_default_on_invalid_type" \
        "\n============================================" \
        "\nRetrying in 5 seconds..." \
        "\nTime left: 5s" \
        "\nTime left: 4s" \
        "\nTime left: 3s" \
        "\nTime left: 2s" \
        "\nTime left: 1s" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.retry_pause : seconds int" \
        " > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: invalid\nReceived type: <class 'str'>" \
        "\nExpected type: <class 'int'>" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    @patch("newtutils.console.time.sleep")
    def test_retry_pause_invalid_seconds(self, mock_sleep, capsys):
        """ Ensure NewtCons._retry_pause(0, beep=False) defaults to 5s countdown and outputs an is_empty error to stderr. """
        print_my_func_name()

        NewtCons._retry_pause(seconds=0, beep=False)
        # Should sleep 5 times (once per second)
        assert mock_sleep.call_count == 5

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_retry_pause_invalid_seconds" \
        "\n============================================" \
        "\nRetrying in 5 seconds..." \
        "\nTime left: 5s" \
        "\nTime left: 4s" \
        "\nTime left: 3s" \
        "\nTime left: 2s" \
        "\nTime left: 1s" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.retry_pause : seconds int" \
        " > Newt.console.validate_type : is_empty" \
        "\n::: ERROR :::" \
        "\nValue must not be empty" \
        "\nValue: 0\nType: <class 'int'>" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    @patch("newtutils.console.time.sleep")
    def test_retry_pause_negative_seconds(self, mock_sleep, capsys):
        """ Ensure NewtCons._retry_pause(-1, beep=False) defaults to 5s countdown and outputs an invalid duration error to stderr. """
        print_my_func_name()

        NewtCons._retry_pause(seconds=-1, beep=False)
        # Should sleep 5 times (once per second)
        assert mock_sleep.call_count == 5

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_retry_pause_negative_seconds" \
        "\n============================================" \
        "\nRetrying in 5 seconds..." \
        "\nTime left: 5s" \
        "\nTime left: 4s" \
        "\nTime left: 3s" \
        "\nTime left: 2s" \
        "\nTime left: 1s" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.retry_pause : seconds < 1" \
        "\n::: ERROR :::" \
        "\nInvalid pause duration: -1" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    @patch("newtutils.console._beep_boop")
    @patch("newtutils.console.time.sleep")
    def test_retry_pause_keyboard_interrupt(self, mock_sleep, mock_beep, capsys):
        """ Ensure NewtCons._retry_pause() raises SystemExit and prints a Ctrl+C error to stderr when sleep is interrupted by KeyboardInterrupt. """
        print_my_func_name()

        mock_sleep.side_effect = KeyboardInterrupt()

        with pytest.raises(SystemExit) as exc_info:
            NewtCons._retry_pause(seconds=5, beep=True)
            print("This line will not be printed")
        assert exc_info.value.code == 1
        print("exc_info:", exc_info.value.code)
        assert mock_beep.call_count == 1
        assert mock_sleep.call_count == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_retry_pause_keyboard_interrupt" \
        "\n============================================" \
        "\nRetrying in 5 seconds..." \
        "\nTime left: 5s" \
        "\nexc_info: 1" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.retry_pause : KeyboardInterrupt" \
        "\n::: ERROR :::" \
        "\nRetry interrupted by user (Ctrl+C)" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "Time left: 4s" not in captured.out
        assert "Time left: 3s" not in captured.out
        assert "Time left: 2s" not in captured.out
        assert "Time left: 1s" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


class TestCheckLocation:
    """ Tests for check_location function. """


    def test_check_location_invalid_type_both_args(self, capsys):
        """ Ensure NewtCons.check_location() raises SystemExit via validate_type when either argument is a non-str value. """
        print_my_func_name()

        location_1 = 123
        location_2 = "/home/user/project"
        print(location_1, "==", location_2)

        with pytest.raises(SystemExit) as exc_info_1:
            NewtCons.check_location(location_1, location_2)  # type: ignore
            print("This line will not be printed")
        assert exc_info_1.value.code == 1
        print("exc_info_1:", exc_info_1.value.code)

        location_3 = "/home/user/project"
        location_4 = 123
        print(location_3, "==", location_4)

        with pytest.raises(SystemExit) as exc_info_2:
            NewtCons.check_location(location_3, location_4)  # type: ignore
            print("This line will not be printed")
        assert exc_info_2.value.code == 1
        print("exc_info_2:", exc_info_2.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_check_location_invalid_type_both_args" \
        "\n============================================" \
        "\n123 == /home/user/project" \
        "\nexc_info_1: 1" \
        "\n/home/user/project == 123" \
        "\nexc_info_2: 1" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.check_location : dir_global > Newt.console.validate_type" \
        "\n::: ERROR :::" \
        "\nValue: 123\nReceived type: <class 'int'>" \
        "\nExpected type: <class 'str'>" \
        "\n\x1b[0m\n\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.check_location : must_location > Newt.console.validate_type" \
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


    def test_check_location_match(self, capsys):
        """ Ensure NewtCons.check_location() prints '=== START ===' to stdout when both location paths match. """
        print_my_func_name()

        location_1 = "/home/user/project"
        print(location_1, "==", location_1)
        NewtCons.check_location(location_1, location_1)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_check_location_match" \
        "\n============================================" \
        "\n/home/user/project == /home/user/project" \
        "\n=== START ===" \
        "\n" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_check_location_mismatch(self, capsys):
        """ Ensure NewtCons.check_location() raises SystemExit and prints a mismatch error to stderr when paths differ. """
        print_my_func_name()

        location_1 = "/home/user/project"
        location_2 = "/home/other/project"
        print(location_1, "==", location_2)

        with pytest.raises(SystemExit) as exc_info:
            NewtCons.check_location(location_1, location_2)
            print("This line will not be printed")
        assert exc_info.value.code == 1
        print("exc_info:", exc_info.value.code)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function: test_check_location_mismatch" \
        "\n============================================" \
        "\n/home/user/project == /home/other/project" \
        "\nexc_info: 1" \
        "\n" == captured.out
        assert "\x1b[1m\x1b[31m" \
        "\nLocation: Newt.console.check_location : error_msg" \
        "\n::: ERROR :::" \
        "\nCurrent position is wrong, check folder: /home/user/project" \
        "\n\x1b[0m" \
        "\n" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err
