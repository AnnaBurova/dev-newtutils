"""
Created on 2025-11

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.utility module.

Tests cover:
- List sorting (sorting_list)
- Dictionary sorting (sorting_dict_by_keys)
"""

import pytest

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

    def test_sorting_list_all_duplicates(self, capsys):
        """Test sorting list with all duplicates."""
        print_my_func_name("test_sorting_list_all_duplicates")

        input_list = [1, 1, 1, 1]
        print(input_list)
        result = NewtUtil.sorting_list(input_list)
        print(result)
        assert result == [1]

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sorting_list_invalid_type_no_stop(self, capsys):
        """Test sorting list with invalid types, stop=False."""
        print_my_func_name("test_sorting_list_invalid_type_no_stop")

        input_list = [1, 2, 3.5]
        print(input_list)
        result = NewtUtil.sorting_list(input_list, stop=False)
        print(result)
        assert result == []

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "::: ERROR :::" in captured.out
        assert "must have only str and int types:" in captured.out

    def test_sorting_list_invalid_type_with_stop(self, capsys):
        """Test sorting list with invalid types, stop=True."""
        print_my_func_name("test_sorting_list_invalid_type_with_stop")

        input_list = [1, 2, 3.5]
        print(input_list)
        with pytest.raises(SystemExit):
            NewtUtil.sorting_list(input_list, stop=True)

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sorting_list_not_a_list(self, capsys):
        """Test sorting list with non-list input."""
        print_my_func_name("test_sorting_list_not_a_list")

        input_str = "not a list"
        print(input_str)
        result = NewtUtil.sorting_list(input_str, stop=False)  # type: ignore
        print(result)
        assert result == []

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sorting_list_with_none(self, capsys):
        """Test sorting list containing None."""
        print_my_func_name("test_sorting_list_with_none")

        input_list = [1, None, "a"]
        print(input_list)
        result = NewtUtil.sorting_list(input_list, stop=False)
        print(result)
        assert result == []

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sorting_list_large_numbers(self, capsys):
        """Test sorting list with large numbers."""
        print_my_func_name("test_sorting_list_large_numbers")

        input_list = [100, 1, 50, 1000, 5]
        print(input_list)
        result = NewtUtil.sorting_list(input_list)
        print(result)
        assert result == [1, 5, 50, 100, 1000]

        captured = capsys.readouterr()
        print_my_captured(captured)


class TestSortingDictByKeys:
    """Tests for sorting_dict_by_keys function."""

    def test_sorting_dict_by_single_key(self, capsys):
        """Test sorting by a single key."""
        print_my_func_name("test_sorting_dict_by_single_key")

        input_dict = [
            {"name": "Charlie", "age": 25},
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 20}
        ]
        print(input_dict)
        result = NewtUtil.sorting_dict_by_keys(input_dict, "age")
        print(result)
        assert result[0]["age"] == 20
        assert result[1]["age"] == 25
        assert result[2]["age"] == 30

        captured = capsys.readouterr()
        print_my_captured(captured)

    def test_sorting_dict_by_multiple_keys(self, capsys):
        """Test sorting by multiple keys."""
        print_my_func_name("test_sorting_dict_by_multiple_keys")

        input_dict = [
            {"name": "Charlie", "age": 25},
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 20}
        ]
        print(input_dict)
        result = NewtUtil.sorting_dict_by_keys(input_dict, "age", "name")
        print(result)
        assert result[0]["age"] == 20
        assert result[1]["name"] == "Alice"  # Same age, sorted by name
        assert result[2]["name"] == "Charlie"

        captured = capsys.readouterr()
        print_my_captured(captured)
