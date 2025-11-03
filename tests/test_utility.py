"""
Created on 2025-11

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.utility module.

Tests cover:
- List sorting (sorting_list)
- Dictionary sorting (sorting_dict_by_keys)
"""

import newtutils.utility as NewtUtil


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


class TestSortingList:
    """Tests for sorting_list function."""

    def test_sorting_list_integers(self, capsys):
        """Test sorting list of integers."""
        print_my_func_name("test_error_msg_without_stop")

        input_list = [3, 1, 2, 3, 5, 1]
        print(input_list)
        result = NewtUtil.sorting_list(input_list)
        print(result)
        assert result == [1, 2, 3, 5]

        captured = capsys.readouterr()
        print_my_captured(captured)

