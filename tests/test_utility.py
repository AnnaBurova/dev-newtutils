"""
Updated on 2026-02
Created on 2025-11

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.utility module.

Tests cover:
- TestSortingList
- TestSortingDictByKeys
"""

import pytest

from helpers import print_my_func_name, print_my_captured
import newtutils.utility as NewtUtil


class TestSortingList:
    """ Tests for sorting_list function. """


    def test_sorting_list_integers(self, capsys):
        """ Test sorting list of integers. """
        print_my_func_name()

        input_list = [3, 1, 2, 3, 5, 1]
        print(input_list)
        result = NewtUtil.sorting_list(input_list)
        print(result)
        assert result == [1, 2, 3, 5]

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[3, 1, 2, 3, 5, 1]\n" in captured.out
        assert "\n[1, 2, 3, 5]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_list_strings(self, capsys):
        """ Test sorting list of strings. """
        print_my_func_name()

        input_list = ["c", "a", "b", "c", "z"]
        print(input_list)
        result = NewtUtil.sorting_list(input_list)
        print(result)
        assert result == ["a", "b", "c", "z"]

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n['c', 'a', 'b', 'c', 'z']\n" in captured.out
        assert "\n['a', 'b', 'c', 'z']\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_list_mixed(self, capsys):
        """ Test sorting list with mixed strings and integers. """
        print_my_func_name()

        input_list = ["f", 4, "a", 2, "b", 1, "a"]
        print(input_list)
        result = NewtUtil.sorting_list(input_list)
        print(result)
        # Strings first, then integers
        assert result == ["a", "b", "f", 1, 2, 4]

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n['f', 4, 'a', 2, 'b', 1, 'a']\n" in captured.out
        assert "\n['a', 'b', 'f', 1, 2, 4]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_list_empty(self, capsys):
        """ Test sorting empty list. """
        print_my_func_name()

        result = NewtUtil.sorting_list([])
        print(result)
        assert result == []

        captured = capsys.readouterr()
        print_my_captured(captured)

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_list_single_element(self, capsys):
        """ Test sorting list with single element. """
        print_my_func_name()

        input_list_1 = [1]
        print(input_list_1)
        result_1 = NewtUtil.sorting_list(input_list_1)
        print(result_1)
        assert result_1 == [1]

        list_2 = ["a"]
        print(list_2)
        result_2 = NewtUtil.sorting_list(list_2)
        print(result_2)
        assert result_2 == ["a"]

        captured = capsys.readouterr()
        print_my_captured(captured)

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_list_all_duplicates(self, capsys):
        """ Test sorting list with all duplicates. """
        print_my_func_name()

        input_list = [1, 1, 1, 1]
        print(input_list)
        result = NewtUtil.sorting_list(input_list)
        print(result)
        assert result == [1]

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[1, 1, 1, 1]\n[1]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_list_invalid_type_no_stop(self, capsys):
        """ Test sorting list with invalid types, stop=False. """
        print_my_func_name()

        input_list = [1, 2, 3.5]
        print(input_list)
        result = NewtUtil.sorting_list(input_list, stop=False)
        print(result)
        assert result == []

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input\n" in captured.out
        assert "\nExpected (<class 'str'>, <class 'int'>), got <class 'float'>\n" in captured.out
        assert "\nValue: 3.5\n" in captured.out
        assert "\nLocation: Newt.utility.sorting_list.input_list\n" in captured.out
        assert "\ninput_list must have only str and int types\n" in captured.out
        assert "\ninput_list: [1, 2, 3.5]\n" in captured.out


    def test_sorting_list_invalid_type_with_stop(self, capsys):
        """ Test sorting list with invalid types, stop=True. """
        print_my_func_name()

        input_list = [1, 2, 3.5]
        print(input_list)
        with pytest.raises(SystemExit) as exc_info:
            NewtUtil.sorting_list(input_list)
            print("This line will not be printed")
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input\n" in captured.out
        assert "\nExpected (<class 'str'>, <class 'int'>), got <class 'float'>\n" in captured.out
        assert "\nValue: 3.5\n" in captured.out
        assert "\nLocation: Newt.utility.sorting_list.input_list\n" in captured.out
        assert "\ninput_list must have only str and int types\n" in captured.out
        assert "\ninput_list: [1, 2, 3.5]\n" in captured.out
        # Expected absence of result
        assert "\nThis line will not be printed\n" not in captured.out


    def test_sorting_list_not_a_list(self, capsys):
        """ Test sorting list with non-list input. """
        print_my_func_name()

        input_str = "not a list"
        print(input_str)
        result_str = NewtUtil.sorting_list(input_str, stop=False)  # type: ignore
        print(result_str)
        assert result_str == []

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.utility.sorting_list.input_list\n" in captured.out
        assert "\nExpected <class 'list'>, got <class 'str'>\n" in captured.out
        assert "\nValue: not a list\n" in captured.out


    def test_sorting_list_with_none(self, capsys):
        """ Test sorting list containing None. """
        print_my_func_name()

        input_list = [1, None, "a"]
        print(input_list)
        result = NewtUtil.sorting_list(input_list, stop=False)
        print(result)
        assert result == []

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input\n" in captured.out
        assert "\nExpected (<class 'str'>, <class 'int'>), got <class 'NoneType'>\n" in captured.out
        assert "\nValue: None\n" in captured.out
        assert "\nLocation: Newt.utility.sorting_list.input_list\n" in captured.out
        assert "\ninput_list must have only str and int types\n" in captured.out
        assert "\ninput_list: [1, None, 'a']\n" in captured.out


    def test_sorting_list_large_numbers(self, capsys):
        """ Test sorting list with large numbers. """
        print_my_func_name()

        input_list = [100, 1, 50, 1000, 5]
        print(input_list)
        result = NewtUtil.sorting_list(input_list)
        print(result)
        assert result == [1, 5, 50, 100, 1000]

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[100, 1, 50, 1000, 5]\n" in captured.out
        assert "\n[1, 5, 50, 100, 1000]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


class TestSortingDictByKeys:
    """ Tests for sorting_dict_by_keys function. """


    def test_sorting_dict_by_single_key(self, capsys):
        """ Test sorting by a single key. """
        print_my_func_name()

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
        assert result[0]["name"] == "Bob"
        assert result[1]["name"] == "Charlie"
        assert result[2]["name"] == "Alice"

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[{'name': 'Charlie', 'age': 25}, {'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 20}]\n" in captured.out
        assert "\n[{'name': 'Bob', 'age': 20}, {'name': 'Charlie', 'age': 25}, {'name': 'Alice', 'age': 30}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_dict_by_multiple_keys(self, capsys):
        """ Test sorting by multiple keys. """
        print_my_func_name()

        input_dict = [
            {"name": "Charlie", "age": 25},
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 20}
        ]
        print(input_dict)
        result = NewtUtil.sorting_dict_by_keys(input_dict, "age", "name")
        print(result)
        assert result[0]["age"] == 20
        assert result[1]["age"] == 25
        assert result[2]["age"] == 25
        assert result[0]["name"] == "Bob"
        assert result[1]["name"] == "Alice"
        assert result[2]["name"] == "Charlie"

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[{'name': 'Charlie', 'age': 25}, {'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 20}]\n" in captured.out
        assert "\n[{'name': 'Bob', 'age': 20}, {'name': 'Alice', 'age': 25}, {'name': 'Charlie', 'age': 25}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_dict_reverse(self, capsys):
        """ Test sorting in reverse order. """
        print_my_func_name()

        input_dict = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 20},
            {"name": "Charlie", "age": 25}
        ]
        print(input_dict)
        result = NewtUtil.sorting_dict_by_keys(input_dict, "age", reverse=True)
        print(result)
        assert result[0]["age"] == 30
        assert result[1]["age"] == 25
        assert result[2]["age"] == 20
        assert result[0]["name"] == "Alice"
        assert result[1]["name"] == "Charlie"
        assert result[2]["name"] == "Bob"
        assert result[-1]["age"] == 20

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 20}, {'name': 'Charlie', 'age': 25}]\n" in captured.out
        assert "\n[{'name': 'Alice', 'age': 30}, {'name': 'Charlie', 'age': 25}, {'name': 'Bob', 'age': 20}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_dict_missing_keys(self, capsys):
        """ Test sorting with missing keys (should be placed at end). """
        print_my_func_name()

        input_dict = [
            {"name": "Alice", "age": 30},
            {"name": "Bob"},  # Missing age
            {"name": "Charlie", "age": 25}
        ]
        print(input_dict)
        result = NewtUtil.sorting_dict_by_keys(input_dict, "age")
        print(result)
        assert result[0]["age"] == 25
        assert result[1]["age"] == 30
        assert "age" not in result[2]  # Expected absence of result
        assert result[0]["name"] == "Charlie"
        assert result[1]["name"] == "Alice"
        assert result[2]["name"] == "Bob"
        # Items with missing keys should be at the end
        assert result[-1]["name"] == "Bob"

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[{'name': 'Alice', 'age': 30}, {'name': 'Bob'}, {'name': 'Charlie', 'age': 25}]\n" in captured.out
        assert "\n[{'name': 'Charlie', 'age': 25}, {'name': 'Alice', 'age': 30}, {'name': 'Bob'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_dict_none_values(self, capsys):
        """ Test sorting with None values (should be placed at end). """
        print_my_func_name()

        input_dict = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": None},
            {"name": "Charlie", "age": 25}
        ]
        print(input_dict)
        result = NewtUtil.sorting_dict_by_keys(input_dict, "age")
        print(result)
        assert result[0]["age"] == 25
        assert result[1]["age"] == 30
        assert result[2]["age"] == None
        assert result[0]["name"] == "Charlie"
        assert result[1]["name"] == "Alice"
        assert result[2]["name"] == "Bob"
        # Items with None should be at the end
        assert result[-1]["name"] == "Bob"

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': None}, {'name': 'Charlie', 'age': 25}]\n" in captured.out
        assert "\n[{'name': 'Charlie', 'age': 25}, {'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': None}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_dict_empty_list(self, capsys):
        """ Test sorting empty list. """
        print_my_func_name()

        result = NewtUtil.sorting_dict_by_keys([])
        print(result)
        assert result == []

        captured = capsys.readouterr()
        print_my_captured(captured)

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_dict_no_keys(self, capsys):
        """ Test sorting without keys (should return original order). """
        print_my_func_name()

        input_dict = [
            {"name": "Charlie"},
            {"name": "Alice"},
            {"name": "Bob"}
        ]
        print(input_dict)
        result = NewtUtil.sorting_dict_by_keys(input_dict)
        print(result)
        assert result[0]["name"] == "Charlie"
        assert result[1]["name"] == "Alice"
        assert result[2]["name"] == "Bob"
        # Should return same order (no sorting keys provided)
        assert len(result) == 3

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[{'name': 'Charlie'}, {'name': 'Alice'}, {'name': 'Bob'}]\n[{'name': 'Charlie'}, {'name': 'Alice'}, {'name': 'Bob'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_dict_not_list(self, capsys):
        """ Test sorting with non-list input. """
        print_my_func_name()

        input_str = "not a list"
        print(input_str)
        with pytest.raises(SystemExit) as exc_info:
            NewtUtil.sorting_dict_by_keys(input_str, "key")  # type: ignore
            print("This line will not be printed")
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.utility.sorting_dict_by_keys.data\n" in captured.out
        assert "\nExpected <class 'list'>, got <class 'str'>\n" in captured.out
        assert "\nValue: not a list\n" in captured.out
        # Expected absence of result
        assert "\nThis line will not be printed\n" not in captured.out


    def test_sorting_dict_not_dicts(self, capsys):
        """ Test sorting with list containing non-dicts. """
        print_my_func_name()

        input_list = [1, 2, 3]
        print(input_list)
        with pytest.raises(SystemExit) as exc_info:
            NewtUtil.sorting_dict_by_keys(input_list, "key")  # type: ignore
            print("This line will not be printed")
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.utility.sorting_dict_by_keys\n" in captured.out
        assert "\nExpected a list of dictionaries\n" in captured.out
        assert "\nData: [1, 2, 3]\n" in captured.out
        # Expected absence of result
        assert "\nThis line will not be printed\n" not in captured.out


    def test_sorting_dict_invalid_key_type(self, capsys):
        """ Test sorting with invalid key type. """
        print_my_func_name()

        input_dict = [{"name": "Alice"}]
        print(input_dict)
        with pytest.raises(SystemExit) as exc_info:
            NewtUtil.sorting_dict_by_keys(input_dict, 123)  # type: ignore
            print("This line will not be printed")
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.utility.sorting_dict_by_keys\n" in captured.out
        assert "\nKeys must be strings\n" in captured.out
        assert "\nKeys: (123,)\n" in captured.out
        # Expected absence of result
        assert "\nThis line will not be printed\n" not in captured.out


    def test_sorting_dict_complex_sorting(self, capsys):
        """ Test complex multi-key sorting. """
        print_my_func_name()

        input_dict = [
            {"category": "A", "priority": 2, "name": "Item2"},
            {"category": "B", "priority": 1, "name": "Item1"},
            {"category": "A", "priority": 1, "name": "Item1"},
            {"category": "A", "priority": 2, "name": "Item1"}
        ]
        print(input_dict)
        result = NewtUtil.sorting_dict_by_keys(input_dict, "category", "priority", "name")
        print(result)
        assert result[0]["category"] == "A"
        assert result[1]["category"] == "A"
        assert result[2]["category"] == "A"
        assert result[3]["category"] == "B"
        assert result[0]["priority"] == 1
        assert result[1]["priority"] == 2
        assert result[2]["priority"] == 2
        assert result[3]["priority"] == 1
        assert result[0]["name"] == "Item1"
        assert result[1]["name"] == "Item1"
        assert result[2]["name"] == "Item2"
        assert result[3]["name"] == "Item1"

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[{'category': 'A', 'priority': 2, 'name': 'Item2'}, {'category': 'B', 'priority': 1, 'name': 'Item1'}, {'category': 'A', 'priority': 1, 'name': 'Item1'}, {'category': 'A', 'priority': 2, 'name': 'Item1'}]\n" in captured.out
        assert "\n[{'category': 'A', 'priority': 1, 'name': 'Item1'}, {'category': 'A', 'priority': 2, 'name': 'Item1'}, {'category': 'A', 'priority': 2, 'name': 'Item2'}, {'category': 'B', 'priority': 1, 'name': 'Item1'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
