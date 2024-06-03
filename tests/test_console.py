"""
Created on 2024-06

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.console module.

Tests cover:
    - TestErrorMsg
"""

import pytest

from .helpers import (
    newt_print_function_name,
    newt_print_captured,
)
import newtutils.console as NewtCons


class TestErrorMsg:
    """ Tests for error_msg function. """


    def test_error_msg_without_stop(
            self,
            capsys: pytest.CaptureFixture[str]
            ) -> None:
        """ Ensure NewtCons.error_msg() with stop=False prints error to stderr
        without raising SystemExit.
        """
        newt_print_function_name()

        NewtCons.error_msg("Test error", stop=False)

        captured = capsys.readouterr()
        newt_print_captured(captured, False)

        assert (
            "Function: test_error_msg_without_stop\n"
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
