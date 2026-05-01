"""
Updated on 2026-04
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
        """ Verify that NewtCons._divider() prints the expected divider line and no error message. """
        print_my_func_name()

        NewtCons._divider()

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "-----" * 10 in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


class TestErrorMsg:
    """ Tests for error_msg function. """


    def test_error_msg_with_stop(self, capsys):
        """ Ensure that NewtCons.error_msg() with stop=True raises SystemExit and prints the correct error output. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info:
            NewtCons.error_msg("Test error")
            print("This line will not be printed")
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.err
        assert "\nLocation: Unknown\n" in captured.err
        assert "\nTest error\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


    def test_error_msg_without_stop(self, capsys):
        """ Verify that NewtCons.error_msg() with stop=False prints the error message without raising SystemExit. """
        print_my_func_name()

        NewtCons.error_msg("Test error", stop=False)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.err
        assert "\nLocation: Unknown\n" in captured.err
        assert "\nTest error\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_error_msg_multiple_args(self, capsys):
        """ Check that NewtCons.error_msg() correctly prints multiple error messages when given several arguments. """
        print_my_func_name()

        NewtCons.error_msg(
            "Error 1",
            "Error 2",
            "Error 3",
            stop=False
        )

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.err
        assert "\nLocation: Unknown\n" in captured.err
        assert "\nError 1\nError 2\nError 3\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_error_msg_with_location(self, capsys):
        """ Verify that NewtCons.error_msg() prints the provided custom location in the error message output. """
        print_my_func_name()

        NewtCons.error_msg(
            "Test error",
            location="test.module",
            stop=False
        )

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.err
        assert "\nLocation: test.module\n" in captured.err
        assert "\nTest error\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


class TestValidateType:
    """ Tests for validate_type function. """


    def test_validate_type_correct_type_not_empty(self, capsys):
        """ Test that NewtCons.validate_type() returns True for inputs matching the expected types. """
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

        assert "\ninput_None: None / <class 'NoneType'>\n" in captured.out
        assert "\ninput_bool: False / <class 'bool'>\n" in captured.out
        assert "\ninput_int: 123 / <class 'int'>\n" in captured.out
        assert "\ninput_float: 3.14 / <class 'float'>\n" in captured.out
        assert "\ninput_str: Hello / <class 'str'>\n" in captured.out
        assert "\ninput_bytes: b'Hello' / <class 'bytes'>\n" in captured.out
        assert "\ninput_list: [False, 123, 3.14, 'Hello'] / <class 'list'>\n" in captured.out
        assert "\ninput_tuple: (False, 123, 3.14, 'Hello') / <class 'tuple'>\n" in captured.out
        assert "\ninput_dict: {1: False, 2: 123, 3: 3.14, 4: 'Hello'} / <class 'dict'>\n" in captured.out
        assert "\ninput_set: {123, 3.14, False, Hello} / <class 'set'>\n" in captured.out

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_validate_type_incorrect_type_no_stop(self, capsys):
        """ Verify that NewtCons.validate_type() returns False and prints error for incorrect type when stop=False. """
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

        assert "\ninput_None: None / <class 'NoneType'>\n" in captured.out
        assert "\ninput_bool: False / <class 'bool'>\n" in captured.out
        assert "\ninput_int: 123 / <class 'int'>\n" in captured.out
        assert "\ninput_float: 3.14 / <class 'float'>\n" in captured.out
        assert "\ninput_str: Hello / <class 'str'>\n" in captured.out
        assert "\ninput_bytes: b'Hello' / <class 'bytes'>\n" in captured.out
        assert "\ninput_list: [False, 123, 3.14, 'Hello'] / <class 'list'>\n" in captured.out
        assert "\ninput_tuple: (False, 123, 3.14, 'Hello') / <class 'tuple'>\n" in captured.out
        assert "\ninput_dict: {1: False, 2: 123, 3: 3.14, 4: 'Hello'} / <class 'dict'>\n" in captured.out
        assert "\ninput_set: {123, 3.14, False, Hello} / <class 'set'>\n" in captured.out

        assert captured.err.count("\n::: ERROR :::\n") == 10
        assert captured.err.count("\nLocation: Newt.console.validate_type\n") == 10
        assert "\nValue: None\nReceived type: <class 'NoneType'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: False\nReceived type: <class 'bool'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: 123\nReceived type: <class 'int'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: 3.14\nReceived type: <class 'float'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: Hello\nReceived type: <class 'str'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: b'Hello'\nReceived type: <class 'bytes'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: [False, 123, 3.14, 'Hello']\nReceived type: <class 'list'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: (False, 123, 3.14, 'Hello')\nReceived type: <class 'tuple'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: {1: False, 2: 123, 3: 3.14, 4: 'Hello'}\nReceived type: <class 'dict'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: {123, 3.14, False, Hello}\nReceived type: <class 'set'>\nExpected type: <class 'frozenset'>\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_validate_type_incorrect_type_with_stop(self, capsys):
        """ Test that NewtCons.validate_type() raises SystemExit with correct error output for invalid type when stop=True. """
        print_my_func_name()

        input_None = None
        print("input_None:", input_None, "/", type(input_None))
        with pytest.raises(SystemExit) as exc_info_None:
            NewtCons.validate_type(input_None, frozenset)
            print("This line will not be printed")
        assert exc_info_None.value.code == 1

        input_bool = False
        print("input_bool:", input_bool, "/", type(input_bool))
        with pytest.raises(SystemExit) as exc_info_bool:
            NewtCons.validate_type(input_bool, frozenset)
            print("This line will not be printed")
        assert exc_info_bool.value.code == 1

        input_int = 123
        print("input_int:", input_int, "/", type(input_int))
        with pytest.raises(SystemExit) as exc_info_int:
            NewtCons.validate_type(input_int, frozenset)
            print("This line will not be printed")
        assert exc_info_int.value.code == 1

        input_float = 3.14
        print("input_float:", input_float, "/", type(input_float))
        with pytest.raises(SystemExit) as exc_info_float:
            NewtCons.validate_type(input_float, frozenset)
            print("This line will not be printed")
        assert exc_info_float.value.code == 1

        input_str = "Hello"
        print("input_str:", input_str, "/", type(input_str))
        with pytest.raises(SystemExit) as exc_info_str:
            NewtCons.validate_type(input_str, frozenset)
            print("This line will not be printed")
        assert exc_info_str.value.code == 1

        input_bytes = b"Hello"
        print("input_bytes:", input_bytes, "/", type(input_bytes))
        with pytest.raises(SystemExit) as exc_info_bytes:
            NewtCons.validate_type(input_bytes, frozenset)
            print("This line will not be printed")
        assert exc_info_bytes.value.code == 1

        input_list = [input_bool, input_int, input_float, input_str]
        print("input_list:", input_list, "/", type(input_list))
        with pytest.raises(SystemExit) as exc_info_list:
            NewtCons.validate_type(input_list, frozenset)
            print("This line will not be printed")
        assert exc_info_list.value.code == 1

        input_tuple = (input_bool, input_int, input_float, input_str)
        print("input_tuple:", input_tuple, "/", type(input_tuple))
        with pytest.raises(SystemExit) as exc_info_tuple:
            NewtCons.validate_type(input_tuple, frozenset)
            print("This line will not be printed")
        assert exc_info_tuple.value.code == 1

        input_dict = {1: input_bool, 2: input_int, 3: input_float, 4: input_str}
        print("input_dict:", input_dict, "/", type(input_dict))
        with pytest.raises(SystemExit) as exc_info_dict:
            NewtCons.validate_type(input_dict, frozenset)
            print("This line will not be printed")
        assert exc_info_dict.value.code == 1

        input_set = {input_bool, input_int, input_float, input_str}
        print(f"input_set: {format_set_to_str(input_set)} / {type(input_set)}")
        with pytest.raises(SystemExit) as exc_info_set:
            NewtCons.validate_type(input_set, frozenset)
            print("This line will not be printed")
        assert exc_info_set.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_None: None / <class 'NoneType'>\n" in captured.out
        assert "\ninput_bool: False / <class 'bool'>\n" in captured.out
        assert "\ninput_int: 123 / <class 'int'>\n" in captured.out
        assert "\ninput_float: 3.14 / <class 'float'>\n" in captured.out
        assert "\ninput_str: Hello / <class 'str'>\n" in captured.out
        assert "\ninput_bytes: b'Hello' / <class 'bytes'>\n" in captured.out
        assert "\ninput_list: [False, 123, 3.14, 'Hello'] / <class 'list'>\n" in captured.out
        assert "\ninput_tuple: (False, 123, 3.14, 'Hello') / <class 'tuple'>\n" in captured.out
        assert "\ninput_dict: {1: False, 2: 123, 3: 3.14, 4: 'Hello'} / <class 'dict'>\n" in captured.out
        assert "\ninput_set: {123, 3.14, False, Hello} / <class 'set'>\n" in captured.out

        assert captured.err.count("\n::: ERROR :::\n") == 10
        assert captured.err.count("\nLocation: Newt.console.validate_type\n") == 10
        assert "\nValue: None\nReceived type: <class 'NoneType'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: False\nReceived type: <class 'bool'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: 123\nReceived type: <class 'int'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: 3.14\nReceived type: <class 'float'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: Hello\nReceived type: <class 'str'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: b'Hello'\nReceived type: <class 'bytes'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: [False, 123, 3.14, 'Hello']\nReceived type: <class 'list'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: (False, 123, 3.14, 'Hello')\nReceived type: <class 'tuple'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: {1: False, 2: 123, 3: 3.14, 4: 'Hello'}\nReceived type: <class 'dict'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: {123, 3.14, False, Hello}\nReceived type: <class 'set'>\nExpected type: <class 'frozenset'>\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


    def test_validate_type_multiple_types(self, capsys):
        """ Verify NewtCons.validate_type() handles tuple of allowed types correctly, accepting valid ones and rejecting invalid. """
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

        assert "\ninput_int: 123 / <class 'int'>\n" in captured.out
        assert "\ninput_float: 3.14 / <class 'float'>\n" in captured.out
        assert "\ninput_str: Hello / <class 'str'>\n" in captured.out

        assert "\n::: ERROR :::\n" in captured.err
        assert "\nLocation: Newt.console.validate_type\n" in captured.err
        assert "\nValue: 3.14\nReceived type: <class 'float'>\nExpected type: (<class 'int'>, <class 'str'>)\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_validate_type_with_location(self, capsys):
        """ Test NewtCons.validate_type() returns False and prints error with custom location for incorrect type when stop=False. """
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

        assert "\ninput_int: 123 / <class 'int'>\n" in captured.out
        assert "\ninput_float: 3.14 / <class 'float'>\n" in captured.out
        assert "\ninput_str: Hello / <class 'str'>\n" in captured.out

        assert captured.err.count("\n::: ERROR :::\n") == 3
        assert "\nLocation: test.input_int > Newt.console.validate_type\n" in captured.err
        assert "\nLocation: test.input_float > Newt.console.validate_type\n" in captured.err
        assert "\nLocation: test.input_str > Newt.console.validate_type\n" in captured.err
        assert "\nValue: 123\nReceived type: <class 'int'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: 3.14\nReceived type: <class 'float'>\nExpected type: <class 'frozenset'>\n" in captured.err
        assert "\nValue: Hello\nReceived type: <class 'str'>\nExpected type: <class 'frozenset'>\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_validate_type_correct_type_but_empty(self, capsys):
        """ Test that NewtCons.validate_type() returns True for inputs matching the expected types, but false if inputs are empty. """
        print_my_func_name()

        input_None = None
        print("input_None:", input_None, "/", type(input_None))
        assert NewtCons.validate_type(input_None, type(None), check_non_empty=True, stop=False) is False

        input_bool = False
        print("input_bool:", input_bool, "/", type(input_bool))
        assert NewtCons.validate_type(input_bool, bool, check_non_empty=True, stop=False) is False

        input_int = 0
        print("input_int:", input_int, "/", type(input_int))
        assert NewtCons.validate_type(input_int, int, check_non_empty=True, stop=False) is False

        input_float = 0.0
        print("input_float:", input_float, "/", type(input_float))
        assert NewtCons.validate_type(input_float, float, check_non_empty=True, stop=False) is False

        input_str = ""
        print("input_str:", input_str, "/", type(input_str))
        assert NewtCons.validate_type(input_str, str, check_non_empty=True, stop=False) is False

        input_bytes = b""
        print("input_bytes:", input_bytes, "/", type(input_bytes))
        assert NewtCons.validate_type(input_bytes, bytes, check_non_empty=True, stop=False) is False

        input_list = []
        print("input_list:", input_list, "/", type(input_list))
        assert NewtCons.validate_type(input_list, list, check_non_empty=True, stop=False) is False

        input_tuple = ()
        print("input_tuple:", input_tuple, "/", type(input_tuple))
        assert NewtCons.validate_type(input_tuple, tuple, check_non_empty=True, stop=False) is False

        input_dict = {}
        print("input_dict:", input_dict, "/", type(input_dict))
        assert NewtCons.validate_type(input_dict, dict, check_non_empty=True, stop=False) is False

        input_set = set()
        print("input_set:", input_set, "/", type(input_set))
        assert NewtCons.validate_type(input_set, set, check_non_empty=True, stop=False) is False

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_None: None / <class 'NoneType'>\n" in captured.out
        assert "\ninput_bool: False / <class 'bool'>\n" in captured.out
        assert "\ninput_int: 0 / <class 'int'>\n" in captured.out
        assert "\ninput_float: 0.0 / <class 'float'>\n" in captured.out
        assert "\ninput_str:  / <class 'str'>\n" in captured.out
        assert "\ninput_bytes: b'' / <class 'bytes'>\n" in captured.out
        assert "\ninput_list: [] / <class 'list'>\n" in captured.out
        assert "\ninput_tuple: () / <class 'tuple'>\n" in captured.out
        assert "\ninput_dict: {} / <class 'dict'>\n" in captured.out
        assert "\ninput_set: set() / <class 'set'>\n" in captured.out

        assert captured.err.count("\n::: ERROR :::\n") == 10
        assert captured.err.count("\nLocation: Newt.console.validate_type : is_empty\n") == 10
        assert "\nValue must not be empty\nValue: None\nType: <class 'NoneType'>\n" in captured.err
        assert "\nValue must not be empty\nValue: False\nType: <class 'bool'>\n" in captured.err
        assert "\nValue must not be empty\nValue: 0\nType: <class 'int'>\n" in captured.err
        assert "\nValue must not be empty\nValue: 0.0\nType: <class 'float'>\n" in captured.err
        assert "\nValue must not be empty\nValue: \nType: <class 'str'>\n" in captured.err
        assert "\nValue must not be empty\nValue: b''\nType: <class 'bytes'>\n" in captured.err
        assert "\nValue must not be empty\nValue: []\nType: <class 'list'>\n" in captured.err
        assert "\nValue must not be empty\nValue: ()\nType: <class 'tuple'>\n" in captured.err
        assert "\nValue must not be empty\nValue: {}\nType: <class 'dict'>\n" in captured.err
        assert "\nValue must not be empty\nValue: {}\nType: <class 'set'>\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_validate_type_unknown_type_and_empty(self, capsys):
        """ Test that NewtCons.validate_type() returns True for inputs matching the expected types, but false if inputs are empty. """
        print_my_func_name()

        input_frozenset = frozenset()
        print("input_frozenset:", input_frozenset, "/", type(input_frozenset))
        assert NewtCons.validate_type(input_frozenset, frozenset, check_non_empty=True, stop=False) is False

        input_frozenset_stop = frozenset()
        print("input_frozenset_stop:", input_frozenset_stop, "/", type(input_frozenset_stop))
        with pytest.raises(SystemExit) as exc_info_frozenset:
            NewtCons.validate_type(input_frozenset_stop, frozenset, check_non_empty=True)
            print("This line will not be printed")
        assert exc_info_frozenset.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_frozenset: frozenset() / <class 'frozenset'>\n" in captured.out
        assert "\ninput_frozenset_stop: frozenset() / <class 'frozenset'>\n" in captured.out

        assert captured.err.count("\n::: ERROR :::\n") == 2
        assert captured.err.count("\nLocation: Newt.console.validate_type : check_non_empty\n") == 2
        assert captured.err.count("\ncheck_non_empty is not supported for this type\nValue: frozenset()\nType: <class 'frozenset'>\n") == 2

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


class TestBeepBoop:
    """ Tests for _beep_boop function. """


    @patch('newtutils.console.time.sleep')
    def test_beep_boop(self, mock_sleep, capsys):
        """ Test that _beep_boop on Windows triggers two beeps and two sleeps without error output or message at other OS. """
        print_my_func_name()

        if sys.platform == "win32" and os.name == "nt":
            # On Windows: mock only Beep (module exists)
            with patch('newtutils.console.winsound.Beep') as mock_beep:
                NewtCons._beep_boop()
                assert mock_beep.call_count == 2
                assert mock_sleep.call_count == 2
        else:
            NewtCons._beep_boop()

        captured = capsys.readouterr()
        print_my_captured(captured)

        if sys.platform == "win32" and os.name == "nt":
            pass
        else:
            assert "\nBeep Boop !!!\n" in captured.out

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


class TestRetryPause:
    """ Tests for _retry_pause function. """


    @patch('newtutils.console._beep_boop')
    @patch('newtutils.console.time.sleep')
    def test_retry_pause_with_beep(self, mock_sleep, mock_beep, capsys):
        """ Test _retry_pause(2) calls _beep_boop once, two sleeps, prints countdown. """
        print_my_func_name()

        NewtCons._retry_pause(seconds=2)
        mock_beep.assert_called_once()
        assert mock_beep.call_count == 1
        assert mock_sleep.call_count == 2

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nRetrying in 2 seconds...\nTime left: 2s\nTime left: 1s\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err
        assert "Time left: 3s" not in captured.out


    @patch('newtutils.console._beep_boop')
    @patch('newtutils.console.time.sleep')
    def test_retry_pause_countdown(self, mock_sleep, mock_beep, capsys):
        """ Test _retry_pause(3, beep=False) skips beep, does three sleeps, prints countdown. """
        print_my_func_name()

        NewtCons._retry_pause(seconds=3, beep=False)
        assert mock_beep.call_count == 0
        assert mock_sleep.call_count == 3

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nRetrying in 3 seconds...\nTime left: 3s\nTime left: 2s\nTime left: 1s\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err
        assert "Time left: 4s" not in captured.out


    @patch('newtutils.console.time.sleep')
    def test_retry_pause_invalid_type(self, mock_sleep, capsys):
        """ Test _retry_pause invalid seconds str uses default 5s countdown with error. """
        print_my_func_name()

        NewtCons._retry_pause(seconds="invalid", beep=False)  # type: ignore
        # Should sleep 5 times (once per second)
        assert mock_sleep.call_count == 5

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nRetrying in 5 seconds...\nTime left: 5s\nTime left: 4s\nTime left: 3s\nTime left: 2s\nTime left: 1s\n" in captured.out

        assert "\n::: ERROR :::\n" in captured.err
        assert "\nLocation: Newt.console.retry_pause : seconds int > Newt.console.validate_type\n" in captured.err
        assert "\nValue: invalid\nReceived type: <class 'str'>\nExpected type: <class 'int'>\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    @patch('newtutils.console.time.sleep')
    def test_retry_pause_invalid_seconds(self, mock_sleep, capsys):
        """ Test _retry_pause(0) falls back to 5s countdown, logs invalid duration error. """
        print_my_func_name()

        NewtCons._retry_pause(seconds=0, beep=False)
        # Should sleep 5 times (once per second)
        assert mock_sleep.call_count == 5

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nRetrying in 5 seconds...\nTime left: 5s\nTime left: 4s\nTime left: 3s\nTime left: 2s\nTime left: 1s\n" in captured.out

        assert "\n::: ERROR :::\n" in captured.err
        assert "\nLocation: Newt.console.retry_pause : seconds int > Newt.console.validate_type : is_empty\n" in captured.err
        assert "\nValue must not be empty\nValue: 0\nType: <class 'int'>\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    @patch('newtutils.console.time.sleep')
    def test_retry_pause_negative_seconds(self, mock_sleep, capsys):
        """ Test _retry_pause(-1) defaults to 5s countdown, logs invalid duration error. """
        print_my_func_name()

        NewtCons._retry_pause(seconds=-1, beep=False)
        # Should sleep 5 times (once per second)
        assert mock_sleep.call_count == 5

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nRetrying in 5 seconds...\nTime left: 5s\nTime left: 4s\nTime left: 3s\nTime left: 2s\nTime left: 1s\n" in captured.out

        assert "\n::: ERROR :::\n" in captured.err
        assert "\nLocation: Newt.console.retry_pause : seconds < 1\n" in captured.err
        assert "\nInvalid pause duration: -1\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    @patch('newtutils.console._beep_boop')
    @patch('newtutils.console.time.sleep')
    def test_retry_pause_keyboard_interrupt(self, mock_sleep, mock_beep, capsys):
        """ Test _retry_pause raises SystemExit on KeyboardInterrupt during sleep. """
        print_my_func_name()

        mock_sleep.side_effect = KeyboardInterrupt()

        with pytest.raises(SystemExit) as exc_info:
            NewtCons._retry_pause(seconds=5, beep=True)
            print("This line will not be printed")
        assert exc_info.value.code == 1
        assert mock_beep.call_count == 1
        assert mock_sleep.call_count == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nRetrying in 5 seconds...\nTime left: 5s\n" in captured.out

        assert "\n::: ERROR :::\n" in captured.err
        assert "\nLocation: Newt.console.retry_pause : KeyboardInterrupt\n" in captured.err
        assert "\nRetry interrupted by user (Ctrl+C)\n" in captured.err

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


    def test_check_location_match(self, capsys):
        """ Test check_location matching paths prints START message. """
        print_my_func_name()

        location_1 = "/home/user/project"
        print(location_1, "==", location_1)
        NewtCons.check_location(location_1, location_1)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n/home/user/project == /home/user/project\n=== START ===\n" in captured.out

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_check_location_mismatch(self, capsys):
        """ Test check_location mismatch raises SystemExit with error message. """
        print_my_func_name()

        location_1 = "/home/user/project"
        location_2 = "/home/other/project"
        print(location_1, "==", location_2)

        with pytest.raises(SystemExit) as exc_info:
            NewtCons.check_location(location_1, location_2)
            print("This line will not be printed")
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n/home/user/project == /home/other/project\n" in captured.out

        assert "\n::: ERROR :::\n" in captured.err
        assert "\nLocation: Newt.console.check_location : error_msg\n" in captured.err
        assert "\nCurrent position is wrong, check folder: /home/user/project\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


    def test_check_location_invalid_type(self, capsys):
        """ Test check_location non-str arg triggers validate_type SystemExit. """
        print_my_func_name()

        location_1 = 123
        location_2 = "/home/user/project"
        print(location_1, "==", location_2)

        with pytest.raises(SystemExit) as exc_info:
            NewtCons.check_location(location_1, location_2)  # type: ignore
            print("This line will not be printed")
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n123 == /home/user/project\n" in captured.out

        assert "\n::: ERROR :::\n" in captured.err
        assert "\nLocation: Newt.console.check_location : dir_global > Newt.console.validate_type\n" in captured.err
        assert "\nValue: 123\nReceived type: <class 'int'>\nExpected type: <class 'str'>\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err
