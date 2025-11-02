"""
Created on 2025-11

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.console module.

Tests cover:
- Error messaging (error_msg)
- Input validation (validate_input)
- Beep notification (_beep_boop)
"""

import pytest
from unittest.mock import patch

import newtutils.console as NewtCons


def print_my_captured(
        captured
        ) -> None:
    """Pretty-print captured stdout and stderr from pytest capsys."""
    print()

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

    print("======================")


class TestErrorMsg:
    """Tests for error_msg function."""

    def test_error_msg_without_stop(self, capsys):
        """Test error message without stopping execution."""
        NewtCons.error_msg("Test error", stop=False)
        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "Location: Unknown" in captured.out
        assert "::: ERROR :::" in captured.out
        assert "Test error" in captured.out

    def test_error_msg_with_stop(self):
        """Test error message with stop=True raises SystemExit."""
        print()
        with pytest.raises(SystemExit) as exc_info:
            NewtCons.error_msg("Test error", stop=True)
        assert exc_info.value.code == 1

    def test_error_msg_multiple_args(self, capsys):
        """Test error message with multiple arguments."""
        NewtCons.error_msg("Error 1", "Error 2", "Error 3", stop=False)
        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "Error 1" in captured.out
        assert "Error 2" in captured.out
        assert "Error 3" in captured.out

    def test_error_msg_with_location(self, capsys):
        """Test error message with custom location."""
        NewtCons.error_msg("Test error", location="test.module", stop=False)
        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "Location: test.module" in captured.out


class TestValidateInput:
    """Tests for validate_input function."""

    def test_validate_input_correct_type(self):
        """Test validation with correct type."""
        print()
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

    def test_validate_input_incorrect_type_no_stop(self, capsys):
        """Test validation with incorrect type, stop=False."""
        result = NewtCons.validate_input("hello", int, stop=False)
        assert result is False
        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "::: ERROR :::" in captured.out
        assert "Expected <class 'int'>, got <class 'str'>" in captured.out

    def test_validate_input_incorrect_type_with_stop(self):
        """Test validation with incorrect type, stop=True."""
        print()
        with pytest.raises(SystemExit):
            NewtCons.validate_input("hello", int, stop=True)

    def test_validate_input_multiple_types(self):
        """Test validation with tuple of allowed types."""
        print()
        input_1 = 123
        print(input_1)
        assert NewtCons.validate_input(input_1, (int, str), stop=False) is True
        input_2 = "hello"
        print(input_2)
        assert NewtCons.validate_input(input_2, (int, str), stop=False) is True
        input_3 = 3.14
        print(input_3)
        assert NewtCons.validate_input(input_3, (int, str), stop=False) is False

    def test_validate_input_list_type(self):
        """Test validation with list type."""
        print()
        input_1 = [1, 2, 3]
        print(input_1, list)
        assert NewtCons.validate_input(input_1, list, stop=False) is True
        print(input_1, dict, "not")
        assert NewtCons.validate_input(input_1, dict, stop=False) is False

    def test_validate_input_dict_type(self):
        """Test validation with dict type."""
        print()
        input_1 = {"key": "value"}
        print(input_1, dict)
        assert NewtCons.validate_input(input_1, dict, stop=False) is True
        print(input_1, list, "not")
        assert NewtCons.validate_input(input_1, list, stop=False) is False

    def test_validate_input_none_value(self):
        """Test validation with None value."""
        print()
        print(None, type(None))
        assert NewtCons.validate_input(None, type(None), stop=False) is True
        print(None, int, "not")
        assert NewtCons.validate_input(None, int, stop=False) is False


class TestBeepBoop:
    """Tests for _beep_boop function."""

    @patch('newtutils.console.winsound')
    @patch('newtutils.console.os.name', 'nt')
    @patch('time.sleep')
    def test_beep_boop_on_windows(self, mock_sleep, mock_winsound):
        """Test beep_boop on Windows."""
        print()
        NewtCons._beep_boop()
        print("mock_winsound.Beep.call_count:", mock_winsound.Beep.call_count)
        assert mock_winsound.Beep.call_count == 2
        print("mock_sleep.call_count:", mock_sleep.call_count)

    @patch('newtutils.console.winsound')
    @patch('newtutils.console.os.name', 'posix')
    def test_beep_boop_on_non_windows(self, mock_winsound):
        """Test beep_boop on non-Windows (should not raise)."""
        # Should not raise on non-Windows
        print()
        NewtCons._beep_boop()
        print("mock_winsound.Beep.call_count:", mock_winsound.Beep.call_count)
        mock_winsound.Beep.assert_not_called()

    def test_beep_boop_invalid_pause(self, capsys):
        """Test beep_boop with invalid pause duration."""
        with pytest.raises(SystemExit):
            NewtCons._beep_boop(pause_s=-1)
        # Should handle gracefully without raising
        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_beep_boop_custom_pause(self):
        """Test beep_boop with custom pause duration."""
        print()
        with patch('newtutils.console.winsound') as mock_winsound, \
             patch('newtutils.console.os.name', 'nt'), \
             patch('time.sleep'):
            NewtCons._beep_boop(pause_s=0.5)
            print("mock_winsound.Beep.called:", mock_winsound.Beep.called)
            assert mock_winsound.Beep.called
