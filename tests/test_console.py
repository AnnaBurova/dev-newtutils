"""
Created on 2024-06

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.console module.

Tests cover:
    - TestFormatValueToStr
    - TestErrorMsg
    - TestValidateValue
"""

import pytest

from .helpers import (
    EXAMPLE_LIST,
    newt_print_function_name,
    newt_print_captured,
)
import newtutils.console as NewtCons


class TestFormatValueToStr:
    """ Tests for format_value_to_str function. """


    def test_format_value_to_str_types(
            self,
            capsys: pytest.CaptureFixture[str]
            ) -> None:
        """Ensure NewtCons.format_value_to_str() returns a string for various types."""

        newt_print_function_name()

        for example_input in EXAMPLE_LIST:
            print()
            if example_input == {3, 1, 2}:
                print("input    =  {3, 1, 2}")
            else:
                print("input    = ", repr(example_input))
            print("intype   = ", type(example_input))
            example_output = NewtCons.format_value_to_str(example_input)
            print("output   = ", repr(example_output))
            print("outtype  = ", type(example_output))
            assert isinstance(example_output, str)

        captured = capsys.readouterr()
        newt_print_captured(captured, False)

        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


class TestErrorMsg:
    """ Tests for error_msg function. """


    def test_error_msg_without_stop(
            self,
            capsys: pytest.CaptureFixture[str]
            ) -> None:
        """Ensure NewtCons.error_msg() prints an error without stopping execution."""

        func_name = newt_print_function_name()

        NewtCons.error_msg("Test error", stop=False)

        captured = capsys.readouterr()
        newt_print_captured(captured, False)

        assert (
            f"Function: {func_name}\n"
            f"{'-' * 72}"
            "\n"
        ) == captured.out

        assert (
            "\x1b[1m\x1b[31m"
            "\nLocation: Unknown"
            "\n::: ERROR :::"
            "\nTest error"
            "\n\x1b[0m"
            "\n"
        ) == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        # assert "::: ERROR :::" not in captured.err


    def test_error_msg_with_stop(
            self,
            capsys: pytest.CaptureFixture[str]
            ) -> None:
        """Ensure NewtCons.error_msg() stops execution with exit code 1."""

        func_name = newt_print_function_name()

        with pytest.raises(SystemExit) as exc_info:
            NewtCons.error_msg("Test error")
            print("This line will not be printed")
        assert exc_info.value.code == 1
        print("exc_info:", exc_info.value.code)

        captured = capsys.readouterr()
        newt_print_captured(captured, False)

        assert (
            f"Function: {func_name}\n"
            f"{'-' * 72}"
            "\nexc_info: 1"
            "\n"
        ) == captured.out

        assert (
            "\x1b[1m\x1b[31m"
            "\nLocation: Unknown"
            "\n::: ERROR :::"
            "\nTest error"
            "\n\x1b[0m"
            "\n"
        ) == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        # assert "::: ERROR :::" not in captured.err
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


    def test_error_msg_multiple_args(
            self,
            capsys: pytest.CaptureFixture[str]
            ) -> None:
        """Ensure NewtCons.error_msg() displays multiple error messages."""

        func_name = newt_print_function_name()

        NewtCons.error_msg(
            "Error 1",
            "Error 2",
            "Error 3",
            stop=False
        )

        captured = capsys.readouterr()
        newt_print_captured(captured, False)

        assert (
            f"Function: {func_name}\n"
            f"{'-' * 72}"
            "\n"
        ) == captured.out

        assert (
            "\x1b[1m\x1b[31m"
            "\nLocation: Unknown"
            "\n::: ERROR :::"
            "\nError 1"
            "\nError 2"
            "\nError 3"
            "\n\x1b[0m"
            "\n"
        ) == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        # assert "::: ERROR :::" not in captured.err


    def test_error_msg_with_location(
            self,
            capsys: pytest.CaptureFixture[str]
            ) -> None:
        """Ensure NewtCons.error_msg() displays the specified location."""
        func_name = newt_print_function_name()

        NewtCons.error_msg(
            "Test error",
            location=f"{__name__} > {func_name}",
            stop=False
        )

        captured = capsys.readouterr()
        newt_print_captured(captured, False)

        assert (
            f"Function: {func_name}\n"
            f"{'-' * 72}"
            "\n"
        ) == captured.out

        assert (
            "\x1b[1m\x1b[31m"
            "\nLocation: tests.test_console > test_error_msg_with_location"
            "\n::: ERROR :::"
            "\nTest error"
            "\n\x1b[0m"
            "\n"
        ) == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        # assert "::: ERROR :::" not in captured.err


class TestValidateValue:
    """ Tests for validate_value function. """


    def test_validate_value_correct_types(
            self,
            capsys: pytest.CaptureFixture[str]
            ) -> None:
        """Ensure NewtCons.validate_value() accepts values of their matching types."""
        newt_print_function_name()

        for example_input in EXAMPLE_LIST:
            print()
            if example_input == {3, 1, 2}:
                print("input   =  {3, 1, 2}")
            else:
                print("input   = ", repr(example_input))
            print("intype  = ", type(example_input))

            example_output = NewtCons.validate_value(example_input, type(example_input))
            print("output  = ", example_output)
            assert example_output is True

        captured = capsys.readouterr()
        newt_print_captured(captured, False)

        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 0

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err
