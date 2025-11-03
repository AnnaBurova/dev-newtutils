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
        print_my_func_name("test_sorting_list_integers")

        input_list = [3, 1, 2, 3, 5, 1]
        print(input_list)
        result = NewtUtil.sorting_list(input_list)
        print(result)
        assert result == [1, 2, 3, 5]

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sorting_list_strings(self, capsys):
        """Test sorting list of strings."""
        print_my_func_name("test_sorting_list_strings")

        input_list = ["c", "a", "b", "c", "z"]
        print(input_list)
        result = NewtUtil.sorting_list(input_list)
        print(result)
        assert result == ["a", "b", "c", "z"]

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sorting_list_mixed(self, capsys):
        """Test sorting list with mixed strings and integers."""
        print_my_func_name("test_sorting_list_mixed")

        input_list = ["f", 4, "a", 2, "b", 1, "a"]
        print(input_list)
        result = NewtUtil.sorting_list(input_list)
        print(result)
        # Strings first, then integers
        assert result == ["a", "b", "f", 1, 2, 4]

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sorting_list_empty(self, capsys):
        """Test sorting empty list."""
        print_my_func_name("test_sorting_list_empty")

        result = NewtUtil.sorting_list([])
        print(result)
        assert result == []

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sorting_list_single_element(self, capsys):
        """Test sorting list with single element."""
        print_my_func_name("test_sorting_list_single_element")

        print(NewtUtil.sorting_list([1]))
        assert NewtUtil.sorting_list([1]) == [1]
        print(NewtUtil.sorting_list(["a"]))
        assert NewtUtil.sorting_list(["a"]) == ["a"]

        captured = capsys.readouterr()
        print_my_captured(captured)
