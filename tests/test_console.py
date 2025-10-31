"""
Created on 2025-11

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.console module.

Tests cover:
- Error messaging (error_msg)
"""

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
