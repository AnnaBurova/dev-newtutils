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
    """ Tests for _beep_boop function. """


    @patch('newtutils.console.os.name', 'nt')
    @patch('newtutils.console.winsound')
    @patch('newtutils.console.time.sleep')
    def test_beep_boop_on_windows(self, mock_sleep, mock_winsound, capsys):
        """ Test _beep_boop on Windows. """
        print_my_func_name()

        NewtCons._beep_boop()
        print("mock_sleep.call_count:", mock_sleep.call_count)
        print("mock_winsound.Beep.call_count:", mock_winsound.Beep.call_count)
        assert mock_sleep.call_count == 2
        assert mock_winsound.Beep.call_count == 2

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nmock_sleep.call_count: 2\n" in captured.out
        assert "\nmock_winsound.Beep.call_count: 2\n" in captured.out


    @patch('newtutils.console.os.name', 'posix')
    @patch('newtutils.console.winsound')
    def test_beep_boop_on_non_windows(self, mock_winsound, capsys):
        """ Test beep_boop on non-Windows (should not raise). """
        print_my_func_name()

        NewtCons._beep_boop()
        mock_winsound.Beep.assert_not_called()
        print("mock_winsound.Beep.call_count:", mock_winsound.Beep.call_count)
        assert mock_winsound.Beep.call_count == 0

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nmock_winsound.Beep.call_count: 0\n" in captured.out


    @patch('newtutils.console.os.name', 'nt')
    @patch('newtutils.console.winsound')
    @patch('newtutils.console.time.sleep')
    def test_beep_boop_invalid_pause(self, mock_sleep, mock_winsound, capsys):
        """ Test _beep_boop with invalid pause duration. """
        print_my_func_name()

        NewtCons._beep_boop(pause_s="Test")  # type: ignore
        print("mock_sleep.call_count:", mock_sleep.call_count)
        print("mock_winsound.Beep.call_count:", mock_winsound.Beep.call_count)
        assert mock_sleep.call_count == 2
        assert mock_winsound.Beep.call_count == 2

        NewtCons._beep_boop(pause_s=-1)
        print("mock_sleep.call_count:", mock_sleep.call_count)
        print("mock_winsound.Beep.call_count:", mock_winsound.Beep.call_count)
        assert mock_sleep.call_count == 4
        assert mock_winsound.Beep.call_count == 4

        NewtCons._beep_boop(pause_s=0.7)

        print("mock_sleep.call_count:", mock_sleep.call_count)
        print("mock_winsound.Beep.call_count:", mock_winsound.Beep.call_count)
        assert mock_sleep.call_count == 6
        assert mock_winsound.Beep.call_count == 6

        pause_duration = [call[0][0] for call in mock_sleep.call_args_list]
        print(f"Pause is: {pause_duration} seconds")
        assert pause_duration == [0.2, 1, 0.2, 1, 0.7, 1]

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nmock_sleep.call_count: 2\n" in captured.out
        assert "\nmock_winsound.Beep.call_count: 2\n" in captured.out
        assert "\nmock_sleep.call_count: 4\n" in captured.out
        assert "\nmock_winsound.Beep.call_count: 4\n" in captured.out
        assert "\nmock_sleep.call_count: 6\n" in captured.out
        assert "\nmock_winsound.Beep.call_count: 6\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > _beep_boop : pause_s not int or float\n" in captured.out
        assert "\nLocation: Newt.console._beep_boop : pause_s less then 0\n" in captured.out
        assert "\nExpected (<class 'int'>, <class 'float'>), got <class 'str'>\n" in captured.out
        assert "\nInvalid pause duration: -1\n" in captured.out
        assert "\nPause is: [0.2, 1, 0.2, 1, 0.7, 1] seconds\n" in captured.out


    @patch('newtutils.console.os.name', 'nt')
    @patch('newtutils.console.winsound')
    @patch('newtutils.console.time.sleep')
    def test_beep_boop_exception(self, mock_sleep, mock_winsound, capsys):
        """ Test _beep_boop with Exception. """
        print_my_func_name()

        mock_winsound.Beep.side_effect = Exception("Audio driver crash")

        NewtCons._beep_boop()

        print("mock_sleep.call_count:", mock_sleep.call_count)
        print("mock_winsound.Beep.call_count:", mock_winsound.Beep.call_count)
        assert mock_sleep.call_count == 0
        assert mock_winsound.Beep.call_count == 1

        # Be sure Beep was called
        mock_winsound.Beep.assert_called_once_with(1200, 500)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nLocation: Newt.console._beep_boop : Exception on Beep\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nException: Audio driver crash\n" in captured.out
        assert "\nmock_sleep.call_count: 0\n" in captured.out
        assert "\nmock_winsound.Beep.call_count: 1\n" in captured.out


class TestRetryPause:
    """ Tests for _retry_pause function. """


    @patch('newtutils.console._beep_boop')
    @patch('newtutils.console.time.sleep')
    def test_retry_pause_with_beep(self, mock_sleep, mock_beep, capsys):
        """ Test retry pause with beep enabled. """
        print_my_func_name()

        NewtCons._retry_pause(seconds=2)
        mock_beep.assert_called_once()
        print("mock_beep.call_count:", mock_beep.call_count)
        print("mock_sleep.call_count:", mock_sleep.call_count)
        assert mock_beep.call_count == 1
        assert mock_sleep.call_count == 2

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nRetrying in 2 seconds...\n" in captured.out
        assert "\nTime left: 2s\n" in captured.out
        assert "\nTime left: 1s\n" in captured.out
        assert "\nmock_beep.call_count: 1\n" in captured.out
        assert "\nmock_sleep.call_count: 2\n" in captured.out


    @patch('newtutils.console._beep_boop')
    @patch('newtutils.console.time.sleep')
    def test_retry_pause_countdown(self, mock_sleep, mock_beep, capsys):
        """ Test retry pause countdown. """
        print_my_func_name()

        NewtCons._retry_pause(seconds=3, beep=False)
        print("mock_beep.call_count:", mock_beep.call_count)
        print("mock_sleep.call_count:", mock_sleep.call_count)
        assert mock_beep.call_count == 0
        assert mock_sleep.call_count == 3

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nRetrying in 3 seconds...\n" in captured.out
        assert "\nTime left: 3s\n" in captured.out
        assert "\nTime left: 2s\n" in captured.out
        assert "\nTime left: 1s\n" in captured.out
        assert "\nmock_beep.call_count: 0\n" in captured.out
        assert "\nmock_sleep.call_count: 3\n" in captured.out


    @patch('newtutils.console.time.sleep')
    def test_retry_pause_invalid_type(self, mock_sleep, capsys):
        """ Test retry pause with invalid type. """
        print_my_func_name()

        NewtCons._retry_pause(seconds="invalid", beep=False)  # type: ignore
        # Should sleep 5 times (once per second)
        print("mock_sleep.call_count:", mock_sleep.call_count)
        assert mock_sleep.call_count == 5

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nLocation: Newt.console.validate_input > _retry_pause : seconds\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nExpected <class 'int'>, got <class 'str'>\n" in captured.out
        assert "\nValue: invalid\n" in captured.out
        assert "\nRetrying in 5 seconds...\n" in captured.out
        assert "\nTime left: 5s\n" in captured.out
        assert "\nTime left: 4s\n" in captured.out
        assert "\nTime left: 3s\n" in captured.out
        assert "\nTime left: 2s\n" in captured.out
        assert "\nTime left: 1s\n" in captured.out
        assert "\nmock_sleep.call_count: 5\n" in captured.out


    @patch('newtutils.console.time.sleep')
    def test_retry_pause_invalid_seconds(self, mock_sleep, capsys):
        """ Test retry pause with invalid seconds. """
        print_my_func_name()

        NewtCons._retry_pause(seconds=0, beep=False)
        # Should sleep 5 times (once per second)
        print("mock_sleep.call_count:", mock_sleep.call_count)
        assert mock_sleep.call_count == 5

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nLocation: Newt.console._retry_pause : seconds less then 1\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nInvalid pause duration: 0\n" in captured.out
        assert "\nRetrying in 5 seconds...\n" in captured.out
        assert "\nTime left: 5s\n" in captured.out
        assert "\nTime left: 4s\n" in captured.out
        assert "\nTime left: 3s\n" in captured.out
        assert "\nTime left: 2s\n" in captured.out
        assert "\nTime left: 1s\n" in captured.out
        assert "\nmock_sleep.call_count: 5\n" in captured.out


    @patch('newtutils.console.time.sleep')
    def test_retry_pause_negative_seconds(self, mock_sleep, capsys):
        """ Test retry pause with negative seconds. """
        print_my_func_name()

        NewtCons._retry_pause(seconds=-1, beep=False)
        # Should sleep 5 times (once per second)
        print("mock_sleep.call_count:", mock_sleep.call_count)
        assert mock_sleep.call_count == 5

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nLocation: Newt.console._retry_pause : seconds less then 1\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nInvalid pause duration: -1\n" in captured.out
        assert "\nRetrying in 5 seconds...\n" in captured.out
        assert "\nTime left: 5s\n" in captured.out
        assert "\nTime left: 4s\n" in captured.out
        assert "\nTime left: 3s\n" in captured.out
        assert "\nTime left: 2s\n" in captured.out
        assert "\nTime left: 1s\n" in captured.out
        assert "\nmock_sleep.call_count: 5\n" in captured.out


    @patch('newtutils.console._beep_boop')
    @patch('newtutils.console.time.sleep')
    def test_retry_pause_keyboard_interrupt(self, mock_sleep, mock_beep, capsys):
        """ Test KeyboardInterrupt (Ctrl+C) during countdown. """
        print_my_func_name()

        mock_sleep.side_effect = KeyboardInterrupt()

        with pytest.raises(SystemExit) as exc_info:
            NewtCons._retry_pause(seconds=5, beep=True)
        assert exc_info.value.code == 1
        print("mock_beep.call_count:", mock_beep.call_count)
        print("mock_sleep.call_count:", mock_sleep.call_count)
        assert mock_beep.call_count == 1
        assert mock_sleep.call_count == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nRetrying in 5 seconds...\n" in captured.out
        assert "\nTime left: 5s\n" in captured.out
        assert "\nLocation: Newt.console._retry_pause : KeyboardInterrupt\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nRetry interrupted by user (Ctrl+C)\n" in captured.out
        assert "\nmock_beep.call_count: 1\n" in captured.out
        assert "\nmock_sleep.call_count: 1\n" in captured.out


class TestCheckLocation:
    """ Tests for check_location function. """


    def test_check_location_match(self, capsys):
        """ When directories match, prints start message. """
        print_my_func_name()

        location_1 = "/home/user/project"
        print(location_1)
        NewtCons.check_location(location_1, location_1)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n/home/user/project\n" in captured.out
        assert "\n=== START ===\n" in captured.out


    def test_check_location_mismatch(self, capsys):
        """ When directories differ, raises SystemExit and prints error. """
        print_my_func_name()

        location_1 = "/home/user/project"
        location_2 = "/other/place"
        print(location_1, location_2)

        with pytest.raises(SystemExit) as exc_info:
            NewtCons.check_location(location_1, location_2)
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n/home/user/project /other/place\n" in captured.out
        assert "\nLocation: Newt.console.check_location\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation is wrong, check folder: /home/user/project\n" in captured.out


    def test_check_location_invalid_type(self, capsys):
        """ Passing non-string `dir_` triggers validate_input SystemExit. """
        print_my_func_name()

        location_1 = 123
        location_2 = "/home/user/project"
        print(location_1, location_2)

        with pytest.raises(SystemExit):
            NewtCons.check_location(location_1, location_2)  # type: ignore

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n123 /home/user/project\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > check_location : dir_\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nExpected <class 'str'>, got <class 'int'>\n" in captured.out
        assert "\nValue: 123\n" in captured.out


class TestSelectFromInput:
    """ Tests for select_from_input function. """


    @patch('newtutils.console.input', side_effect=["1"])
    def test_select_from_input_valid_choice(self, mock_input, capsys):
        """ Test valid selection from list. """
        print_my_func_name()

        select_dict = {"1": "Option A", "2": "Option B", "3": "Option C"}
        print(select_dict)

        result = NewtCons.select_from_input(select_dict)
        assert result == "1"

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n{'1': 'Option A', '2': 'Option B', '3': 'Option C'}\n" in captured.out
        assert "\nAvailable list: 3\n" in captured.out
        assert "\n     1: Option A\n" in captured.out
        assert "\n     2: Option B\n" in captured.out
        assert "\n     3: Option C\n" in captured.out
        assert "\n     X: Exit / Cancel\n" in captured.out
        assert "\n[INPUT]: 1\n" in captured.out
        assert "\nSelected option: Option A\n" in captured.out


    @patch('newtutils.console.input', side_effect=["abc", "999", "2"])
    def test_select_from_input_invalid_then_valid(self, mock_input, capsys):
        """ Test invalid inputs followed by valid selection. """
        print_my_func_name()

        select_dict = {"1": "Option A", "2": "Option B"}
        print(select_dict)

        result = NewtCons.select_from_input(select_dict)
        assert result == "2"

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n{'1': 'Option A', '2': 'Option B'}\n" in captured.out
        assert "\nAvailable list: 2\n" in captured.out
        assert "\n     1: Option A\n" in captured.out
        assert "\n     2: Option B\n" in captured.out
        assert "\n     X: Exit / Cancel\n" in captured.out
        assert "\n[INPUT]: abc\n" in captured.out
        assert "\nInvalid input. Please enter a number.\n" in captured.out
        assert "\n[INPUT]: 999\n" in captured.out
        assert "\nNumber out of range. Try again.\n" in captured.out
        assert "\n[INPUT]: 2\n" in captured.out
        assert "\nSelected option: Option B\n" in captured.out


    @patch('newtutils.console.input', side_effect=["x"])
    def test_select_from_input_cancel(self, mock_input, capsys):
        """ Test cancellation with 'x' raises SystemExit. """
        print_my_func_name()

        select_dict = {"1": "Option A", "2": "Option B"}
        print(select_dict)

        with pytest.raises(SystemExit) as exc_info:
            NewtCons.select_from_input(select_dict)
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n{'1': 'Option A', '2': 'Option B'}\n" in captured.out
        assert "\nAvailable list: 2\n" in captured.out
        assert "\n     1: Option A\n" in captured.out
        assert "\n     2: Option B\n" in captured.out
        assert "\n     X: Exit / Cancel\n" in captured.out
        assert "\n[INPUT]: x\n" in captured.out
        assert "\nLocation: Newt.console.select_from_input : choice = [X]\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nSelection cancelled.\n" in captured.out


    @patch('newtutils.console.input', side_effect=["X"])
    def test_select_from_input_cancel_uppercase(self, mock_input, capsys):
        """ Test cancellation with uppercase 'X' raises SystemExit. """
        print_my_func_name()

        select_dict = {"1": "Option A"}
        print(select_dict)

        with pytest.raises(SystemExit):
            NewtCons.select_from_input(select_dict)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n{'1': 'Option A'}\n" in captured.out
        assert "\nAvailable list: 1\n" in captured.out
        assert "\n     1: Option A\n" in captured.out
        assert "\n     X: Exit / Cancel\n" in captured.out
        assert "\n[INPUT]: x\n" in captured.out
        assert "\nLocation: Newt.console.select_from_input : choice = [X]\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nSelection cancelled.\n" in captured.out


    def test_select_from_input_invalid_type(self, capsys):
        """ Test invalid type for select_dict triggers validate_input. """
        print_my_func_name()

        invalid_input = "not a dict"
        print(invalid_input)

        with pytest.raises(SystemExit):
            NewtCons.select_from_input(invalid_input)  # type: ignore

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nnot a dict\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > select_from_input : select_dict\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nExpected <class 'dict'>, got <class 'str'>\n" in captured.out
        assert "\nValue: not a dict\n" in captured.out


    @patch('newtutils.console.input')
    def test_select_from_input_keyboard_interrupt(self, mock_input, capsys):
        """ Test KeyboardInterrupt raises SystemExit. """
        print_my_func_name()

        mock_input.side_effect = KeyboardInterrupt()

        select_dict = {"1": "Option A", "2": "Option B"}
        print(select_dict)

        with pytest.raises(SystemExit):
            NewtCons.select_from_input(select_dict)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n{'1': 'Option A', '2': 'Option B'}\n" in captured.out
        assert "\nAvailable list: 2\n" in captured.out
        assert "\n     1: Option A\n" in captured.out
        assert "\n     2: Option B\n" in captured.out
        assert "\n     X: Exit / Cancel\n" in captured.out
        assert "\nLocation: Newt.console.select_from_input : KeyboardInterrupt\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nSelection cancelled.\n" in captured.out


    @patch('newtutils.console.input')
    def test_select_from_input_exception(self, mock_input, capsys):
        """ Test general Exception is caught and raises SystemExit. """
        print_my_func_name()

        mock_input.side_effect = RuntimeError("Input device error")

        select_dict = {"1": "Option A"}
        print(select_dict)

        with pytest.raises(SystemExit):
            NewtCons.select_from_input(select_dict)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n{'1': 'Option A'}\n" in captured.out
        assert "\nAvailable list: 1\n" in captured.out
        assert "\n     1: Option A\n" in captured.out
        assert "\n     X: Exit / Cancel\n" in captured.out
        assert "\nLocation: Newt.console.select_from_input : Exception\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nException: Input device error\n" in captured.out


    @patch('newtutils.console.input', return_value=" 2 ")
    def test_select_from_input_spaces(self, mock_input, capsys):
        """ Test input with leading/trailing spaces is handled correctly. """
        print_my_func_name()

        select_dict = {"1": "Option A", "2": "Option B"}
        print(select_dict)

        result = NewtCons.select_from_input(select_dict)
        assert result == "2"

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n{'1': 'Option A', '2': 'Option B'}\n" in captured.out
        assert "\nAvailable list: 2\n" in captured.out
        assert "\n     1: Option A\n" in captured.out
        assert "\n     2: Option B\n" in captured.out
        assert "\n     X: Exit / Cancel\n" in captured.out
        assert "\n[INPUT]: 2\n" in captured.out
        assert "\nSelected option: Option B\n" in captured.out
