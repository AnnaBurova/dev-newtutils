"""
Created on 2025-11

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.console module.

Tests cover:
- Error messaging (error_msg)
- Input validation (validate_input)
- Beep notification (_beep_boop)
- Retry pause (_retry_pause)
- Divider (_divider)
"""

import pytest
from unittest.mock import patch

import newtutils.console as NewtCons


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


class TestErrorMsg:
    """Tests for error_msg function."""

    def test_error_msg_without_stop(self, capsys):
        """Test error message without stopping execution."""
        print_my_func_name("test_error_msg_without_stop")

        NewtCons.error_msg("Test error", stop=False)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Location: Unknown" in captured.out
        assert "::: ERROR :::" in captured.out
        assert "Test error" in captured.out

    def test_error_msg_with_stop(self, capsys):
        """Test error message with stop=True raises SystemExit."""
        print_my_func_name("test_error_msg_with_stop")

        with pytest.raises(SystemExit) as exc_info:
            NewtCons.error_msg("Test error", stop=True)
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_error_msg_multiple_args(self, capsys):
        """Test error message with multiple arguments."""
        print_my_func_name("test_error_msg_multiple_args")

        NewtCons.error_msg("Error 1", "Error 2", "Error 3", stop=False)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Error 1" in captured.out
        assert "Error 2" in captured.out
        assert "Error 3" in captured.out

    def test_error_msg_with_location(self, capsys):
        """Test error message with custom location."""
        print_my_func_name("test_error_msg_with_location")

        NewtCons.error_msg("Test error", location="test.module", stop=False)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Location: test.module" in captured.out


class TestValidateInput:
    """Tests for validate_input function."""

    def test_validate_input_correct_type(self, capsys):
        """Test validation with correct type."""
        print_my_func_name("test_validate_input_correct_type")

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

    def test_validate_input_incorrect_type_no_stop(self, capsys):
        """Test validation with incorrect type, stop=False."""
        print_my_func_name("test_validate_input_incorrect_type_no_stop")

        result = NewtCons.validate_input("hello", int, stop=False)
        assert result is False

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "::: ERROR :::" in captured.out
        assert "Expected <class 'int'>, got <class 'str'>" in captured.out

    def test_validate_input_incorrect_type_with_stop(self, capsys):
        """Test validation with incorrect type, stop=True."""
        print_my_func_name("test_validate_input_incorrect_type_with_stop")

        with pytest.raises(SystemExit):
            result = NewtCons.validate_input("hello", int, stop=True)
            print("This line will not be printed:", result)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_validate_input_multiple_types(self, capsys):
        """Test validation with tuple of allowed types."""
        print_my_func_name("test_validate_input_multiple_types")

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

    def test_validate_input_list_type(self, capsys):
        """Test validation with list type."""
        print_my_func_name("test_validate_input_list_type")

        input_1 = [1, 2, 3]

        print(input_1, list)
        assert NewtCons.validate_input(input_1, list, stop=False) is True

        print(input_1, dict, "not")
        assert NewtCons.validate_input(input_1, dict, stop=False) is False

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_validate_input_dict_type(self, capsys):
        """Test validation with dict type."""
        print_my_func_name("test_validate_input_dict_type")

        input_1 = {"key": "value"}

        print(input_1, dict)
        assert NewtCons.validate_input(input_1, dict, stop=False) is True

        print(input_1, list, "not")
        assert NewtCons.validate_input(input_1, list, stop=False) is False

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_validate_input_none_value(self, capsys):
        """Test validation with None value."""
        print_my_func_name("test_validate_input_none_value")

        print(None, type(None))
        assert NewtCons.validate_input(None, type(None), stop=False) is True

        print(None, int, "not")
        assert NewtCons.validate_input(None, int, stop=False) is False

        captured = capsys.readouterr()
        print_my_captured(captured)


class TestBeepBoop:
    """Tests for _beep_boop function."""

    @patch('newtutils.console.os.name', 'nt')
    @patch('newtutils.console.winsound')
    @patch('newtutils.console.time.sleep')
    def test_beep_boop_on_windows(self, mock_sleep, mock_winsound, capsys):
        """Test beep_boop on Windows."""
        print_my_func_name("test_beep_boop_on_windows")

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
        print_my_func_name("test_beep_boop_on_non_windows")

        NewtCons._beep_boop()
        mock_winsound.Beep.assert_not_called()
        print("mock_winsound.Beep.call_count:", mock_winsound.Beep.call_count)

        captured = capsys.readouterr()
        print_my_captured(captured)

    @patch('newtutils.console.winsound')
    @patch('newtutils.console.time.sleep')
    def test_beep_boop_invalid_pause(self, mock_sleep, mock_winsound, capsys):
        """Test beep_boop with invalid pause duration."""
        print_my_func_name("test_beep_boop_invalid_pause")

        NewtCons._beep_boop(pause_s=-1)
        print("mock_sleep.call_count:", mock_sleep.call_count)
        print("mock_winsound.Beep.call_count:", mock_winsound.Beep.call_count)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_beep_boop_custom_pause(self, capsys):
        """Test beep_boop with custom pause duration."""
        print_my_func_name("test_beep_boop_custom_pause")

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
        print_my_func_name("test_retry_pause_countdown")

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
        print_my_func_name("test_retry_pause_with_beep")

        NewtCons._retry_pause(seconds=2, beep=True)
        mock_beep.assert_called_once()
        print("mock_sleep.call_count:", mock_sleep.call_count)
        print("mock_beep.call_count:", mock_beep.call_count)

        captured = capsys.readouterr()
        print_my_captured(captured)

    @patch('newtutils.console.time.sleep')
    def test_retry_pause_invalid_seconds(self, mock_sleep, capsys):
        """Test retry pause with invalid seconds."""
        print_my_func_name("test_retry_pause_invalid_seconds")

        NewtCons._retry_pause(seconds=0, beep=False)
        # Should sleep 5 times (once per second)
        assert mock_sleep.call_count == 5
        print("mock_sleep.call_count:", mock_sleep.call_count)

        captured = capsys.readouterr()
        print_my_captured(captured)

    @patch('newtutils.console.time.sleep')
    def test_retry_pause_negative_seconds(self, mock_sleep, capsys):
        """Test retry pause with negative seconds."""
        print_my_func_name("test_retry_pause_negative_seconds")

        NewtCons._retry_pause(seconds=-1, beep=False)
        # Should sleep 5 times (once per second)
        assert mock_sleep.call_count == 5
        print("mock_sleep.call_count:", mock_sleep.call_count)

        captured = capsys.readouterr()
        print_my_captured(captured)

    @patch('newtutils.console.time.sleep')
    def test_retry_pause_invalid_type(self, mock_sleep, capsys):
        """Test retry pause with invalid type."""
        print_my_func_name("test_retry_pause_invalid_type")

        NewtCons._retry_pause(seconds="invalid", beep=False)  # type: ignore
        # Should sleep 5 times (once per second)
        assert mock_sleep.call_count == 5
        print("mock_sleep.call_count:", mock_sleep.call_count)

        captured = capsys.readouterr()
        print_my_captured(captured)


class TestDivider:
    """Tests for _divider function."""

    def test_divider_output(self, capsys):
        """Test that divider prints correctly."""
        print_my_func_name("test_divider_output")

        NewtCons._divider()

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "-" in captured.out
        assert "\n" in captured.out
