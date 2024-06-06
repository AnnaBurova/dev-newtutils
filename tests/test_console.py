"""
Created on 2024-06

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.console module.

Tests cover:
    - TestFormatValueToStr
    - TestErrorMsg
    - TestSuccessMsg
    - TestValidateValue
"""

import pytest

from .helpers import (
    EXAMPLE_LIST,
    EMPTY_LIST,
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

        assert len(captured.out) == 1146
        assert len(captured.err) == 0

        # Expected absence of result
        assert captured.out.count("::: ERROR :::") == 0
        assert captured.err.count("::: ERROR :::") == 0


class TestErrorMsg:
    """ Tests for error_msg function. """


    def test_error_msg_without_stop(
            self,
            capsys: pytest.CaptureFixture[str]
            ) -> None:
        """Ensure NewtCons.error_msg() prints an error without stopping execution."""

        newt_print_function_name()

        NewtCons.error_msg("Test error", stop=False)

        captured = capsys.readouterr()
        newt_print_captured(captured, False)

        assert len(captured.out) == 111
        assert len(captured.err) == 58

        assert captured.err.count("::: ERROR :::") == 1

        # Expected absence of result
        assert captured.out.count("::: ERROR :::") == 0


    def test_error_msg_with_stop(
            self,
            capsys: pytest.CaptureFixture[str]
            ) -> None:
        """Ensure NewtCons.error_msg() stops execution with exit code 1."""

        newt_print_function_name()

        change_variable = False

        exc_info = 0
        with pytest.raises(SystemExit) as exc_info:
            NewtCons.error_msg("Test error")
            change_variable = True
        assert exc_info.value.code == 1
        print("exc_info:", exc_info.value.code)

        captured = capsys.readouterr()
        newt_print_captured(captured, False)

        assert len(captured.out) == 120
        assert len(captured.err) == 58

        assert captured.err.count("::: ERROR :::") == 1

        # Expected absence of result
        assert change_variable is False
        assert captured.out.count("::: ERROR :::") == 0


    def test_error_msg_multiple_args(
            self,
            capsys: pytest.CaptureFixture[str]
            ) -> None:
        """Ensure NewtCons.error_msg() displays multiple error messages."""

        newt_print_function_name()

        NewtCons.error_msg(
            "Error 1",
            "Error 2",
            "Error 3",
            stop=False
        )

        captured = capsys.readouterr()
        newt_print_captured(captured, False)

        assert len(captured.out) == 112
        assert len(captured.err) == 71

        assert captured.err.count("::: ERROR :::") == 1

        # Expected absence of result
        assert captured.out.count("::: ERROR :::") == 0


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

        assert len(captured.out) == 112
        assert len(captured.err) == 100

        assert captured.err.count("::: ERROR :::") == 1

        # Expected absence of result
        assert captured.out.count("::: ERROR :::") == 0


class TestSuccessMsg:
    """ Tests for success_msg function. """


    def test_success_msg_different_options(
            self,
            capsys: pytest.CaptureFixture[str]
            ) -> None:
        """Ensure NewtCons.success_msg() prints default, symbol-decorated, and multiple messages."""
        newt_print_function_name()

        NewtCons.success_msg()
        NewtCons.success_msg("File saved successfully.", add_symbols=True)
        NewtCons.success_msg("Files saved.", "Upload completed.")

        captured = capsys.readouterr()
        newt_print_captured(captured, False)

        assert len(captured.out) == 249
        assert len(captured.err) == 0

        # Expected absence of result
        assert captured.out.count("::: ERROR :::") == 0
        assert captured.err.count("::: ERROR :::") == 0


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

        assert len(captured.out) == 778
        assert len(captured.err) == 0

        # Expected absence of result
        assert captured.out.count("::: ERROR :::") == 0
        assert captured.err.count("::: ERROR :::") == 0


    def test_validate_value_incorrect_types_without_stop(
            self,
            capsys: pytest.CaptureFixture[str]
            ) -> None:
        """Ensure NewtCons.validate_value() rejects incorrect types without stopping."""
        newt_print_function_name()

        for example_input in EXAMPLE_LIST:
            print()
            if example_input == {3, 1, 2}:
                print("input     =  {3, 1, 2}")
            else:
                print("input     = ", repr(example_input))
            print("intype    = ", type(example_input))

            testing_type = type(None)
            if example_input is None:
                testing_type = bool
            print("testtype  = ", testing_type)

            example_output = NewtCons.validate_value(
                example_input,
                testing_type,
                stop=False
            )
            print("output    = ", example_output)
            assert example_output is False

        captured = capsys.readouterr()
        newt_print_captured(captured, False)

        assert len(captured.out) == 1179
        assert len(captured.err) == 1845

        assert captured.err.count("::: ERROR :::") == len(EXAMPLE_LIST)

        # Expected absence of result
        assert captured.out.count("::: ERROR :::") == 0


    def test_validate_value_incorrect_types_with_stop_and_location(
            self,
            capsys: pytest.CaptureFixture[str]
            ) -> None:
        """Ensure NewtCons.validate_value() stops on incorrect types with a location."""
        func_name = newt_print_function_name()

        change_variable = False

        for example_input in EXAMPLE_LIST:
            print()
            if example_input == {3, 1, 2}:
                print("input     =  {3, 1, 2}")
            else:
                print("input     = ", repr(example_input))
            print("intype    = ", type(example_input))

            testing_type = type(None)
            if example_input is None:
                testing_type = bool
            print("testtype  = ", testing_type)

            exc_info = 0
            with pytest.raises(SystemExit) as exc_info:
                NewtCons.validate_value(
                    example_input,
                    testing_type,
                    location=f"{__name__} > {func_name}",
                    stop=True
                )
                change_variable = True
            assert exc_info.value.code == 1
            print("exc_info  = ", exc_info.value.code)

        captured = capsys.readouterr()
        newt_print_captured(captured, False)

        assert len(captured.out) == 1149
        assert len(captured.err) == 2665

        assert captured.err.count("::: ERROR :::") == len(EXAMPLE_LIST)

        # Expected absence of result
        assert change_variable is False
        assert captured.out.count("::: ERROR :::") == 0


    def test_validate_value_empty_without_stop(
            self,
            capsys: pytest.CaptureFixture[str]
            ) -> None:
        """Ensure NewtCons.validate_value() rejects empty values without stopping."""
        newt_print_function_name()

        for example_input in EMPTY_LIST:
            print()
            print("input   = ", repr(example_input))
            print("intype  = ", type(example_input))

            example_output = NewtCons.validate_value(
                example_input,
                type(example_input),
                check_non_empty=True,
                stop=False
            )
            print("output  = ", example_output)
            assert example_output is False

        captured = capsys.readouterr()
        newt_print_captured(captured, False)

        assert len(captured.out) == 727
        assert len(captured.err) == 1341

        assert captured.err.count("::: ERROR :::") == len(EMPTY_LIST)

        # Expected absence of result
        assert captured.out.count("::: ERROR :::") == 0
