"""
Updated on 2026-02
Created on 2025-11

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.console module.

Tests cover:
- Divider (_divider)
- Error messaging (error_msg)
- Input validation (validate_input)
- Beep notification (_beep_boop)
- Retry pause (_retry_pause)
"""

import pytest
from unittest.mock import patch

from helpers import print_my_func_name, print_my_captured
import newtutils.console as NewtCons


class TestDivider:
    """ Tests for divider function. """


    def test_divider_output(self, capsys):
        """ Test that divider prints correctly. """
        print_my_func_name()

        NewtCons._divider()

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "-----" * 10 in captured.out
        assert "\n" in captured.out


class TestErrorMsg:
    """ Tests for error_msg function. """


    def test_error_msg_with_stop(self, capsys):
        """ Test error message with default stop=True raises SystemExit. """
        print_my_func_name()

        with pytest.raises(SystemExit) as exc_info:
            NewtCons.error_msg("Test error")
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nLocation: Unknown\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nTest error\n" in captured.out


    def test_error_msg_without_stop(self, capsys):
        """ Test error message without stopping execution. """
        print_my_func_name()

        NewtCons.error_msg("Test error", stop=False)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nLocation: Unknown\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nTest error\n" in captured.out


    def test_error_msg_multiple_args(self, capsys):
        """ Test error message with multiple arguments. """
        print_my_func_name()

        NewtCons.error_msg(
            "Error 1",
            "Error 2",
            "Error 3",
            stop=False
        )

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nLocation: Unknown\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nError 1\n" in captured.out
        assert "\nError 2\n" in captured.out
        assert "\nError 3\n" in captured.out


    def test_error_msg_with_location(self, capsys):
        """ Test error message with custom location. """
        print_my_func_name()

        NewtCons.error_msg(
            "Test error",
            location="test.module",
            stop=False
        )

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nLocation: test.module\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nTest error\n" in captured.out


class TestValidateInput:
    """ Tests for validate_input function. """


    def test_validate_input_correct_type(self, capsys):
        """ Test validation with correct type. """
        print_my_func_name()

        input_1 = 123
        print(input_1)
        assert NewtCons.validate_input(input_1, int, stop=False) is True

        input_2 = "hello"
        print(input_2)
        assert NewtCons.validate_input(input_2, str, stop=False) is True

        input_3 = 3.14
        print(input_3)
        assert NewtCons.validate_input(input_3, float, stop=False) is True

        input_4 = False
        print(input_4)
        assert NewtCons.validate_input(input_4, bool, stop=False) is True

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n123\n" in captured.out
        assert "\nhello\n" in captured.out
        assert "\n3.14\n" in captured.out
        assert "\nFalse\n" in captured.out


    def test_validate_input_incorrect_type_no_stop(self, capsys):
        """ Test validation with incorrect type, stop=False. """
        print_my_func_name()

        result = NewtCons.validate_input("hello", int, stop=False)
        assert result is False

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nLocation: Newt.console.validate_input\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nExpected <class 'int'>, got <class 'str'>\n" in captured.out
        assert "\nValue: hello\n" in captured.out


    def test_validate_input_incorrect_type_with_stop(self, capsys):
        """ Test validation with incorrect type, stop=True. """
        print_my_func_name()

        with pytest.raises(SystemExit):
            result = NewtCons.validate_input("hello", int)
            print("This line will not be printed:", result)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nLocation: Newt.console.validate_input\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nExpected <class 'int'>, got <class 'str'>\n" in captured.out
        assert "\nValue: hello\n" in captured.out

        assert "This line will not be printed" not in captured.out


    def test_validate_input_multiple_types(self, capsys):
        """ Test validation with tuple of allowed types. """
        print_my_func_name()

        input_1 = 123
        print(input_1)
        assert NewtCons.validate_input(input_1, (int, str), stop=False) is True

        input_2 = "hello"
        print(input_2)
        assert NewtCons.validate_input(input_2, (int, str), stop=False) is True

        input_3 = 3.14
        print(input_3)
        assert NewtCons.validate_input(input_3, (int, str), stop=False) is False

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n123\n" in captured.out
        assert "\nhello\n" in captured.out
        assert "\n3.14\n" in captured.out
        assert "\nLocation: Newt.console.validate_input\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nExpected (<class 'int'>, <class 'str'>), got <class 'float'>\n" in captured.out
        assert "\nValue: 3.14\n" in captured.out


    def test_validate_input_list_type(self, capsys):
        """ Test validation with list type. """
        print_my_func_name()

        input_1 = [1, 2, 3]

        print(input_1, list, "yes")
        assert NewtCons.validate_input(input_1, list, stop=False) is True

        print(input_1, dict, "not")
        assert NewtCons.validate_input(input_1, dict, stop=False) is False

        input_2 = {"key": "value"}

        print(input_2, dict, "yes")
        assert NewtCons.validate_input(input_2, dict, stop=False) is True

        print(input_2, list, "not")
        assert NewtCons.validate_input(input_2, list, stop=False) is False

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[1, 2, 3] <class 'list'> yes\n" in captured.out
        assert "\n[1, 2, 3] <class 'dict'> not\n" in captured.out
        assert "\n{'key': 'value'} <class 'dict'> yes\n" in captured.out
        assert "\n{'key': 'value'} <class 'list'> not\n" in captured.out
        assert "\nLocation: Newt.console.validate_input\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nExpected <class 'dict'>, got <class 'list'>\n" in captured.out
        assert "\nValue: [1, 2, 3]\n" in captured.out
        assert "\nExpected <class 'list'>, got <class 'dict'>\n" in captured.out
        assert "\nValue: {'key': 'value'}\n" in captured.out


    def test_validate_input_none_value(self, capsys):
        """ Test validation with None value. """
        print_my_func_name()

        input_1 = None

        print(input_1, type(None), "yes")
        assert NewtCons.validate_input(input_1, type(None), stop=False) is True

        print(input_1, int, "not")
        assert NewtCons.validate_input(input_1, int, stop=False) is False

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nNone <class 'NoneType'> yes\n" in captured.out
        assert "\nNone <class 'int'> not\n" in captured.out
        assert "\nLocation: Newt.console.validate_input\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nExpected <class 'int'>, got <class 'NoneType'>\n" in captured.out
        assert "\nValue: None\n" in captured.out


    def test_validate_input_with_location(self, capsys):
        """ Test validation with custom location. """
        print_my_func_name()

        input_1 = "hello"

        assert NewtCons.validate_input(
            input_1, int, stop=False,
            location="custom.validator"
        ) is False

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nLocation: Newt.console.validate_input > custom.validator\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out


class TestBeepBoop:
    """Tests for _beep_boop function."""

    @patch('newtutils.console.os.name', 'nt')
    @patch('newtutils.console.winsound')
    @patch('newtutils.console.time.sleep')
    def test_beep_boop_on_windows(self, mock_sleep, mock_winsound, capsys):
        """Test beep_boop on Windows."""
        print_my_func_name()

        NewtCons._beep_boop()
        assert mock_winsound.Beep.call_count == 2
        print("mock_sleep.call_count:", mock_sleep.call_count)
        print("mock_winsound.Beep.call_count:", mock_winsound.Beep.call_count)

        captured = capsys.readouterr()
        print_my_captured(captured)

    @patch('newtutils.console.os.name', 'posix')
    @patch('newtutils.console.winsound')
    def test_beep_boop_on_non_windows(self, mock_winsound, capsys):
        """Test beep_boop on non-Windows (should not raise)."""
        print_my_func_name()

        NewtCons._beep_boop()
        mock_winsound.Beep.assert_not_called()
        print("mock_winsound.Beep.call_count:", mock_winsound.Beep.call_count)

        captured = capsys.readouterr()
        print_my_captured(captured)

    @patch('newtutils.console.winsound')
    @patch('newtutils.console.time.sleep')
    def test_beep_boop_invalid_pause(self, mock_sleep, mock_winsound, capsys):
        """Test beep_boop with invalid pause duration."""
        print_my_func_name()

        NewtCons._beep_boop(pause_s=-1)
        print("mock_sleep.call_count:", mock_sleep.call_count)
        print("mock_winsound.Beep.call_count:", mock_winsound.Beep.call_count)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_beep_boop_custom_pause(self, capsys):
        """Test beep_boop with custom pause duration."""
        print_my_func_name()

        with patch('newtutils.console.winsound') as mock_winsound, \
             patch('newtutils.console.os.name', 'nt'), \
             patch('newtutils.console.time.sleep') as mock_sleep:
            NewtCons._beep_boop(pause_s=0.5)
            assert mock_winsound.Beep.called
            print("mock_sleep.call_count:", mock_sleep.call_count)
            print("mock_winsound.Beep.call_count:", mock_winsound.Beep.call_count)

            captured = capsys.readouterr()
            print_my_captured(captured)


class TestRetryPause:
    """Tests for _retry_pause function."""

    @patch('newtutils.console.time.sleep')
    def test_retry_pause_countdown(self, mock_sleep, capsys):
        """Test retry pause countdown."""
        print_my_func_name()

        NewtCons._retry_pause(seconds=3, beep=False)
        # Should sleep 3 times (once per second)
        assert mock_sleep.call_count == 3
        print("mock_sleep.call_count:", mock_sleep.call_count)

        captured = capsys.readouterr()
        print_my_captured(captured)

    @patch('newtutils.console._beep_boop')
    @patch('newtutils.console.time.sleep')
    def test_retry_pause_with_beep(self, mock_sleep, mock_beep, capsys):
        """Test retry pause with beep enabled."""
        print_my_func_name()

        NewtCons._retry_pause(seconds=2, beep=True)
        mock_beep.assert_called_once()
        print("mock_sleep.call_count:", mock_sleep.call_count)
        print("mock_beep.call_count:", mock_beep.call_count)

        captured = capsys.readouterr()
        print_my_captured(captured)

    @patch('newtutils.console.time.sleep')
    def test_retry_pause_invalid_seconds(self, mock_sleep, capsys):
        """Test retry pause with invalid seconds."""
        print_my_func_name()

        NewtCons._retry_pause(seconds=0, beep=False)
        # Should sleep 5 times (once per second)
        assert mock_sleep.call_count == 5
        print("mock_sleep.call_count:", mock_sleep.call_count)

        captured = capsys.readouterr()
        print_my_captured(captured)

    @patch('newtutils.console.time.sleep')
    def test_retry_pause_negative_seconds(self, mock_sleep, capsys):
        """Test retry pause with negative seconds."""
        print_my_func_name()

        NewtCons._retry_pause(seconds=-1, beep=False)
        # Should sleep 5 times (once per second)
        assert mock_sleep.call_count == 5
        print("mock_sleep.call_count:", mock_sleep.call_count)

        captured = capsys.readouterr()
        print_my_captured(captured)

    @patch('newtutils.console.time.sleep')
    def test_retry_pause_invalid_type(self, mock_sleep, capsys):
        """Test retry pause with invalid type."""
        print_my_func_name()

        NewtCons._retry_pause(seconds="invalid", beep=False)  # type: ignore
        # Should sleep 5 times (once per second)
        assert mock_sleep.call_count == 5
        print("mock_sleep.call_count:", mock_sleep.call_count)

        captured = capsys.readouterr()
        print_my_captured(captured)
