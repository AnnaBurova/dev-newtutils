"""
Updated on 2026-05
Created on 2025-11

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.utility module.

Tests cover:
- TestSortingSequence
- TestCheckDictKeys
- TestCountValuesByPosition
- TestSortingDictByKeys
- TestSelectFromInput
"""

import pytest
from unittest.mock import patch

from .helpers import print_my_func_name, print_my_captured, format_set_to_str
import newtutils.utility as NewtUtil


class TestSortingSequence:
    """ Tests for sorting_sequence function. """


    def test_sorting_sequence_integers(self, capsys):
        """ Test sorting_sequence removes duplicates from integers, returns unique sorted. """
        print_my_func_name()

        input_list_1 = [3, 1, 2, 3, 5, 1]
        print("input_list_1:", input_list_1)
        output_1 = NewtUtil.sorting_sequence(input_list_1)
        print("output_1:", output_1)
        assert output_1 == [1, 2, 3, 5]

        input_list_2 = [1]
        print("input_list_2:", input_list_2)
        output_2 = NewtUtil.sorting_sequence(input_list_2)
        print("output_2:", output_2)
        assert output_2 == [1]

        input_list_3 = [1, 1, 1, 1]
        print("input_list_3:", input_list_3)
        output_3 = NewtUtil.sorting_sequence(input_list_3)
        print("output_3:", output_3)
        assert output_3 == [1]

        input_list_4 = [1, 3, 2.5]
        print("input_list_4:", input_list_4)
        output_4 = NewtUtil.sorting_sequence(input_list_4)
        print("output_4:", output_4)
        assert output_4 == [1, 2.5, 3]

        input_list_5 = [100, 1, 50.0, 50, 1000, 5]
        print("input_list_5:", input_list_5)
        output_5 = NewtUtil.sorting_sequence(input_list_5)
        print("output_5:", output_5)
        assert output_5 == [1, 5, 50, 100, 1000]

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_list_1: [3, 1, 2, 3, 5, 1]\noutput_1: [1, 2, 3, 5]\n" in captured.out
        assert "\ninput_list_2: [1]\noutput_2: [1]\n" in captured.out
        assert "\ninput_list_3: [1, 1, 1, 1]\noutput_3: [1]\n" in captured.out
        assert "\ninput_list_4: [1, 3, 2.5]\noutput_4: [1, 2.5, 3]\n" in captured.out
        assert "\ninput_list_5: [100, 1, 50.0, 50, 1000, 5]\noutput_5: [1, 5, 50, 100, 1000]\n" in captured.out

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_sorting_sequence_strings(self, capsys):
        """ Test sorting_sequence removes duplicates from strings, returns unique sorted. """
        print_my_func_name()

        input_list_1 = ["c", "a", "b", "c", "z"]
        print("input_list_1:", input_list_1)
        output_1 = NewtUtil.sorting_sequence(input_list_1)
        print("output_1:", output_1)
        assert output_1 == ["a", "b", "c", "z"]

        input_list_2 = ["a"]
        print("input_list_2:", input_list_2)
        output_2 = NewtUtil.sorting_sequence(input_list_2)
        print("output_2:", output_2)
        assert output_2 == ["a"]

        input_list_3 = ["a", "a", "a", "a"]
        print("input_list_3:", input_list_3)
        output_3 = NewtUtil.sorting_sequence(input_list_3)
        print("output_3:", output_3)
        assert output_3 == ["a"]

        input_list_4 = ["ab", "a", "b", "aa"]
        print("input_list_4:", input_list_4)
        output_4 = NewtUtil.sorting_sequence(input_list_4)
        print("output_4:", output_4)
        assert output_4 == ["a", "aa", "ab", "b"]

        input_list_5 = ["ab", "a", "aaaa", "aaa", "aa"]
        print("input_list_5:", input_list_5)
        output_5 = NewtUtil.sorting_sequence(input_list_5)
        print("output_5:", output_5)
        assert output_5 == ["a", "aa", "aaa", "aaaa", "ab"]

        input_list_6 = [
            "!", ".", ",", "?", "ä", "a", "ö", "o", "ü", "u", "$", "#", "@",
            "%", "^", "(", ")", "{", "}", "[", "]", "_", "-", "+", "*", "/",
            "0", "5", "1", "10", "11", "9"
            ]
        print("input_list_6:", input_list_6)
        output_6 = NewtUtil.sorting_sequence(input_list_6)
        print("output_6:", output_6)
        assert output_6 == [
            "!", "#", "$", "%", "(", ")", "*", "+", ",", "-", ".", "/",
            "0", "1", "10", "11", "5", "9", "?", "@", "[", "]", "^", "_",
            "a", "o", "u", "{", "}", "ä", "ö", "ü"
            ]

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_list_1: ['c', 'a', 'b', 'c', 'z']\noutput_1: ['a', 'b', 'c', 'z']\n" in captured.out
        assert "\ninput_list_2: ['a']\noutput_2: ['a']\n" in captured.out
        assert "\ninput_list_3: ['a', 'a', 'a', 'a']\noutput_3: ['a']\n" in captured.out
        assert "\ninput_list_4: ['ab', 'a', 'b', 'aa']\noutput_4: ['a', 'aa', 'ab', 'b']\n" in captured.out
        assert "\ninput_list_5: ['ab', 'a', 'aaaa', 'aaa', 'aa']\noutput_5: ['a', 'aa', 'aaa', 'aaaa', 'ab']\n" in captured.out
        assert "\ninput_list_6: ['!', '.', ',', '?', 'ä', 'a', 'ö', 'o', 'ü', 'u', '$', '#', '@', '%', '^', '(', ')', '{', '}', '[', ']', '_', '-', '+', '*', '/', '0', '5', '1', '10', '11', '9']\noutput_6: ['!', '#', '$', '%', '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '10', '11', '5', '9', '?', '@', '[', ']', '^', '_', 'a', 'o', 'u', '{', '}', 'ä', 'ö', 'ü']\n" in captured.out

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_sorting_sequence_mixed(self, capsys):
        """ Test sorting_sequence handles mixed str/int, removes duplicates, sorts uniquely. """
        print_my_func_name()

        input_list_1 = ["f", 4, "a", 2, "b", 1, "a"]
        print("input_list_1:", input_list_1)
        output_1 = NewtUtil.sorting_sequence(input_list_1)
        print("output_1:", output_1)
        assert output_1 == ["a", "b", "f", 1, 2, 4]

        input_list_2 = [
            1, 4.0, True, None, "a",
            (5.0, 2, False, None, "b",
            (6, 3.0, True, None, "c"))
            ]
        print("input_list_2:", input_list_2)
        output_2 = NewtUtil.sorting_sequence(input_list_2)
        print("output_2:", output_2)
        assert output_2 == [
            "a", 1, 4, None, True,
            ("b", 2, 5, False, None,
            ("c", 3, 6, None, True))
            ]

        input_list_3 = [
            (3.0, 6.1, True, None, "c"),
            (5.0, 2, False, None, "b"),
            (6, 3, True, None, "c")
            ]
        print("input_list_3:", input_list_3)
        output_3 = NewtUtil.sorting_sequence(input_list_3)
        print("output_3:", output_3)
        assert output_3 == [
            ("b", 2, 5, False, None),
            ("c", 3, 6, None, True),
            ("c", 3, 6.1, None, True)
            ]

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_list_1: ['f', 4, 'a', 2, 'b', 1, 'a']\noutput_1: ['a', 'b', 'f', 1, 2, 4]\n" in captured.out
        assert "\ninput_list_2: [1, 4.0, True, None, 'a', (5.0, 2, False, None, 'b', (6, 3.0, True, None, 'c'))]\noutput_2: ['a', 1, 4, None, True, ('b', 2, 5, False, None, ('c', 3, 6, None, True))]\n" in captured.out
        assert "\ninput_list_3: [(3.0, 6.1, True, None, 'c'), (5.0, 2, False, None, 'b'), (6, 3, True, None, 'c')]\noutput_3: [('b', 2, 5, False, None), ('c', 3, 6, None, True), ('c', 3, 6.1, None, True)]\n" in captured.out

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_sorting_sequence_empty(self, capsys):
        """ Test sorting_sequence returns empty list for empty input. """
        print_my_func_name()

        input_list_1 = []
        print("input_list_1:", input_list_1)
        with pytest.raises(SystemExit) as exc_info:
            NewtUtil.sorting_sequence(input_list_1)
            print("This line will not be printed")
        assert exc_info.value.code == 1

        input_list_2 = []
        print("input_list_2:", input_list_2)
        output_2 = NewtUtil.sorting_sequence(input_list_2, stop=False)
        print("output_2:", output_2)
        assert output_2 == []

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_list_1: []\ninput_list_2: []\noutput_2: []\n" in captured.out

        assert captured.err.count("\n::: ERROR :::\n") == 2
        assert captured.err.count("\nLocation: Newt.utility.sorting_sequence : data_sequence > Newt.console.validate_type : is_empty\n") == 2
        assert captured.err.count("\nValue must not be empty\nValue: []\nType: <class 'list'>\n") == 2

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


    def test_sorting_sequence_not_a_list(self, capsys):
        """ Test sorting_sequence non-list input returns empty list with error logged. """
        print_my_func_name()

        input_str_1 = "not a list"
        print("input_str_1:", input_str_1)
        output_1 = NewtUtil.sorting_sequence(input_str_1, stop=False)
        print("output_1:", output_1)
        assert output_1 == []

        input_list_2 = [1, [1]]
        print("input_list_2:", input_list_2)
        output_2 = NewtUtil.sorting_sequence(input_list_2, stop=False)
        print("output_2:", output_2)
        assert output_2 == []

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_str_1: not a list\noutput_1: []\n" in captured.out
        assert "\ninput_list_2: [1, [1]]\noutput_2: []\n" in captured.out

        assert captured.err.count("\n::: ERROR :::\n") == 3
        assert "\nLocation: Newt.utility.sorting_sequence : data_sequence > Newt.console.validate_type\n" in captured.err
        assert "\nValue: not a list\nReceived type: <class 'str'>\nExpected type: (<class 'list'>, <class 'tuple'>)\n" in captured.err
        assert "\nLocation: Newt.utility.sorting_sequence.is_valid_seq_value > Newt.console.validate_type\n" in captured.err
        assert "\nValue: [1]\nReceived type: <class 'list'>\nExpected type: (<class 'NoneType'>, <class 'bool'>, <class 'int'>, <class 'float'>, <class 'str'>)\n" in captured.err
        assert "\nLocation: Newt.utility.sorting_sequence : data_sequence not all\n" in captured.err
        assert "\ndata_sequence must have only special types\ndata_sequence: [1, [1]]\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


class TestCheckDictKeys:
    """ Tests for check_dict_keys function. """


    def test_check_dict_keys_all_present(self, capsys):
        """ Test check_dict_keys returns True for exact key match. """
        print_my_func_name()

        input_dict = {"a": 1, "b": 2}
        print("input_dict:", input_dict, "/", type(input_dict))
        input_set = {"a", "b"}
        print(f"input_set: {format_set_to_str(input_set)} /", type(input_set))
        assert NewtUtil.check_dict_keys(input_dict, input_set) is True

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_dict: {'a': 1, 'b': 2} / <class 'dict'>\ninput_set: {a, b} / <class 'set'>\n" in captured.out

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_check_dict_keys_missing_keys_no_stop(self, capsys):
        """ Test check_dict_keys missing key returns False, logs details with stop=False. """
        print_my_func_name()

        input_dict = {"a": 1, "b": 2}
        print("input_dict:", input_dict, "/", type(input_dict))
        input_set = {"a", "b", "c"}
        print(f"input_set: {format_set_to_str(input_set)} /", type(input_set))
        assert NewtUtil.check_dict_keys(input_dict, input_set, stop=False) is False

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_dict: {'a': 1, 'b': 2} / <class 'dict'>\ninput_set: {a, b, c} / <class 'set'>\n" in captured.out

        assert "\n::: ERROR :::\n" in captured.err
        assert "\nLocation: Newt.utility.check_dict_keys\n" in captured.err
        assert "\nData keys: a, b\nMissing keys: c\nUnexpected keys: \n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_check_dict_keys_extra_keys_no_stop(self, capsys):
        """ Test check_dict_keys extra key returns False, logs details with stop=False. """
        print_my_func_name()

        input_dict = {"a": 1, "b": 2, "c": 3}
        print("input_dict:", input_dict, "/", type(input_dict))
        input_set = {"a", "b"}
        print(f"input_set: {format_set_to_str(input_set)} /", type(input_set))
        assert NewtUtil.check_dict_keys(input_dict, input_set, stop=False) is False

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_dict: {'a': 1, 'b': 2, 'c': 3} / <class 'dict'>\ninput_set: {a, b} / <class 'set'>\n" in captured.out

        assert "\n::: ERROR :::\n" in captured.err
        assert "\nLocation: Newt.utility.check_dict_keys\n" in captured.err
        assert "\nData keys: a, b, c\nMissing keys: \nUnexpected keys: c\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_check_dict_keys_missing_and_extra_stop(self, capsys):
        """ Test check_dict_keys mismatch with stop=True raises SystemExit. """
        print_my_func_name()

        input_dict = {"x": 9}
        print("input_dict:", input_dict, "/", type(input_dict))
        input_set = {"a", "b"}
        print(f"input_set: {format_set_to_str(input_set)} /", type(input_set))

        with pytest.raises(SystemExit) as exc_info:
            NewtUtil.check_dict_keys(input_dict, input_set, location="TestCheckDictKeys")
            print("This line will not be printed")
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_dict: {'x': 9} / <class 'dict'>\ninput_set: {a, b} / <class 'set'>\n" in captured.out

        assert "\n::: ERROR :::\n" in captured.err
        assert "\nLocation: TestCheckDictKeys > Newt.utility.check_dict_keys\n" in captured.err
        assert "\nData keys: x\nMissing keys: a, b\nUnexpected keys: x\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


class TestCountValuesByPosition:
    """ Tests for count_values_by_position function. """


    def test_count_values_by_position_no_errors(self, capsys):
        """ Test count_values_by_position returns correct counts for valid input. """
        print_my_func_name()

        input_list_1 = [
            ("admin", 1, "Stockholm"),
            ("user", 2, "Oslo"),
            ("admin", 3, "Stockholm"),
            ("user", 4, "Berlin"),
            ("admin", 5, "Oslo"),
        ]
        print("input_list_1:", input_list_1)

        output_1 = NewtUtil.count_values_by_position(input_list_1)
        print("output_1:", output_1)
        assert output_1 == {"admin": 3, "user": 2}

        output_2 = NewtUtil.count_values_by_position(input_list_1, 0)
        print("output_2:", output_2)
        assert output_2 == {"admin": 3, "user": 2}
        assert output_1 == output_2

        output_3 = NewtUtil.count_values_by_position(input_list_1, 1)
        print("output_3:", output_3)
        assert output_3 == {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}

        output_4 = NewtUtil.count_values_by_position(input_list_1, 2)
        print("output_4:", output_4)
        assert output_4 == {"Stockholm": 2, "Oslo": 2, "Berlin": 1}

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_list_1: [('admin', 1, 'Stockholm'), ('user', 2, 'Oslo'), ('admin', 3, 'Stockholm'), ('user', 4, 'Berlin'), ('admin', 5, 'Oslo')]\n" in captured.out
        assert "\noutput_1: {'admin': 3, 'user': 2}\n" in captured.out
        assert "\noutput_2: {'admin': 3, 'user': 2}\n" in captured.out
        assert "\noutput_3: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}\n" in captured.out
        assert "\noutput_4: {'Stockholm': 2, 'Oslo': 2, 'Berlin': 1}\n" in captured.out

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_count_values_by_position_edge_cases(self, capsys):
        """ Test count_values_by_position handles edge cases: empty input, single element, tuple outer sequence. """
        print_my_func_name()

        input_list_1 = []
        print("input_list_1:", input_list_1)
        output_1 = NewtUtil.count_values_by_position(input_list_1)
        print("output_1:", output_1)
        assert output_1 == {}

        input_list_2 = [("only", 1)]
        print("input_list_2:", input_list_2)
        output_2 = NewtUtil.count_values_by_position(input_list_2)
        print("output_2:", output_2)
        assert output_2 == {"only": 1}

        print("input_list_2:", input_list_2)
        output_3 = NewtUtil.count_values_by_position(input_list_2, 1)
        print("output_3:", output_3)
        assert output_3 == {1: 1}

        input_list_4 = ()
        print("input_list_4:", input_list_4)
        output_4 = NewtUtil.count_values_by_position(input_list_4)
        print("output_4:", output_4)
        assert output_4 == {}

        input_list_5 = (["only", 1],)
        print("input_list_5:", input_list_5)
        output_5 = NewtUtil.count_values_by_position(input_list_5)
        print("output_5:", output_5)
        assert output_5 == {"only": 1}

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_list_1: []\noutput_1: {}\n" in captured.out
        assert "\ninput_list_2: [('only', 1)]\noutput_2: {'only': 1}\n" in captured.out
        assert "\ninput_list_2: [('only', 1)]\noutput_3: {1: 1}\n" in captured.out
        assert "\ninput_list_4: ()\noutput_4: {}\n" in captured.out
        assert "\ninput_list_5: (['only', 1],)\noutput_5: {'only': 1}\n" in captured.out

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_count_values_by_position_invalid_input_no_stop(self, capsys):
        """ Test count_values_by_position returns empty dict on invalid input without stopping execution. """
        print_my_func_name()

        input_list_1 = [("a", "b"), ("c", "d")]
        print("input_list_1:", input_list_1)
        output_1 = NewtUtil.count_values_by_position(input_list_1, 5)
        print("output_1:", output_1)
        assert output_1 == {}

        input_list_2 = [("a", "b"), ("c",)]
        print("input_list_2:", input_list_2)
        output_2 = NewtUtil.count_values_by_position(input_list_2)
        print("output_2:", output_2)
        assert output_2 == {}

        input_list_3 = [("a", 1), [("b", 2)]]
        print("input_list_3:", input_list_3)
        output_3 = NewtUtil.count_values_by_position(input_list_3)
        print("output_3:", output_3)
        assert output_3 == {}

        input_list_4 = "not a sequence of sequences"
        print("input_list_4:", input_list_4)
        output_4 = NewtUtil.count_values_by_position(input_list_4)
        print("output_4:", output_4)
        assert output_4 == {}

        input_list_5 = [("a", "b"), ("c", "d")]
        print("input_list_5:", input_list_5)
        output_5 = NewtUtil.count_values_by_position(input_list_5, "5")  # type: ignore
        print("output_5:", output_5)
        assert output_5 == {"a": 1, "c": 1}

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_list_1: [('a', 'b'), ('c', 'd')]\noutput_1: {}\n" in captured.out
        assert "\ninput_list_2: [('a', 'b'), ('c',)]\noutput_2: {}\n" in captured.out
        assert "\ninput_list_3: [('a', 1), [('b', 2)]]\noutput_3: {}\n" in captured.out
        assert "\ninput_list_4: not a sequence of sequences\noutput_4: {}\n" in captured.out
        assert "\ninput_list_5: [('a', 'b'), ('c', 'd')]\noutput_5: {'a': 1, 'c': 1}\n" in captured.out

        assert captured.err.count("\n::: ERROR :::\n") == 5
        assert "\nLocation: Newt.utility.count_values_by_position : seq_len <= position\n" in captured.err
        assert "\nPosition 5 out of range\n" in captured.err
        assert "\nLocation: Newt.utility.count_values_by_position : seq_len\n" in captured.err
        assert "\nAll items must have the same length 2\n" in captured.err
        assert "\nLocation: Newt.utility.count_values_by_position : seq_type > Newt.console.validate_type\n" in captured.err
        assert "\nValue: [('b', 2)]\nReceived type: <class 'list'>\nExpected type: <class 'tuple'>\n" in captured.err
        assert "\nLocation: Newt.utility.count_values_by_position : data_sequence > Newt.console.validate_type\n" in captured.err
        assert "\nValue: not a sequence of sequences\nReceived type: <class 'str'>\nExpected type: (<class 'list'>, <class 'tuple'>)\n" in captured.err
        assert "\nLocation: Newt.utility.count_values_by_position : position > Newt.console.validate_type\n" in captured.err
        assert "\nValue: 5\nReceived type: <class 'str'>\nExpected type: <class 'int'>\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_count_values_by_position_invalid_input_with_stop(self, capsys):
        """ Test count_values_by_position raises SystemExit on invalid input when stop=True. """
        print_my_func_name()

        input_list_1 = [("a", "b"), ("c", "d")]
        print("input_list_1:", input_list_1)
        with pytest.raises(SystemExit) as exc_info_1:
            NewtUtil.count_values_by_position(input_list_1, 5, True)
            print("This line will not be printed")
        assert exc_info_1.value.code == 1

        input_list_2 = [("a", "b"), ("c",)]
        print("input_list_2:", input_list_2)
        with pytest.raises(SystemExit) as exc_info_2:
            NewtUtil.count_values_by_position(input_list_2, stop=True)
            print("This line will not be printed")
        assert exc_info_2.value.code == 1

        input_list_3 = [("a", 1), [("b", 2)]]
        print("input_list_3:", input_list_3)
        with pytest.raises(SystemExit) as exc_info_3:
            NewtUtil.count_values_by_position(input_list_3, stop=True)
            print("This line will not be printed")
        assert exc_info_3.value.code == 1

        input_list_4 = "not a sequence of sequences"
        print("input_list_4:", input_list_4)
        with pytest.raises(SystemExit) as exc_info_4:
            NewtUtil.count_values_by_position(input_list_4, stop=True)
            print("This line will not be printed")
        assert exc_info_4.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_list_1: [('a', 'b'), ('c', 'd')]\n" in captured.out
        assert "\ninput_list_2: [('a', 'b'), ('c',)]\n" in captured.out
        assert "\ninput_list_3: [('a', 1), [('b', 2)]]\n" in captured.out
        assert "\ninput_list_4: not a sequence of sequences\n" in captured.out

        assert captured.err.count("\n::: ERROR :::\n") == 4
        assert "\nLocation: Newt.utility.count_values_by_position : seq_len <= position\n" in captured.err
        assert "\nPosition 5 out of range\n" in captured.err
        assert "\nLocation: Newt.utility.count_values_by_position : seq_len\n" in captured.err
        assert "\nAll items must have the same length 2\n" in captured.err
        assert "\nLocation: Newt.utility.count_values_by_position : seq_type > Newt.console.validate_type\n" in captured.err
        assert "\nValue: [('b', 2)]\nReceived type: <class 'list'>\nExpected type: <class 'tuple'>\n" in captured.err
        assert "\nLocation: Newt.utility.count_values_by_position : data_sequence > Newt.console.validate_type\n" in captured.err
        assert "\nValue: not a sequence of sequences\nReceived type: <class 'str'>\nExpected type: (<class 'list'>, <class 'tuple'>)\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


class TestSortingDictByKeys:
    """ Tests for sorting_dict_by_keys function. """


    def test_sorting_dict_by_keys_no_error(self, capsys):
        """ Test sorting_dict_by_keys with single key, multiple keys, reverse, and no keys. """
        print_my_func_name()

        input_list_dict = [
            {"name": "Charlie", "age": 25},
            {"name": "Bob", "age": 25},
            {"name": "Alice", "age": 20},
            {"name": "Aska", "age": 30},
            {"name": "Bob", "age": 20},
        ]
        print("input_list_dict:", input_list_dict)

        # One key
        output_dict_1 = NewtUtil.sorting_dict_by_keys(input_list_dict, "name")
        print("output_dict_1:", output_dict_1)
        assert output_dict_1[0]["age"] == 20
        assert output_dict_1[1]["age"] == 30
        assert output_dict_1[2]["age"] == 25
        assert output_dict_1[3]["age"] == 20
        assert output_dict_1[4]["age"] == 25
        assert output_dict_1[0]["name"] == "Alice"
        assert output_dict_1[1]["name"] == "Aska"
        assert output_dict_1[2]["name"] == "Bob"
        assert output_dict_1[3]["name"] == "Bob"
        assert output_dict_1[4]["name"] == "Charlie"

        # More keys
        output_dict_2 = NewtUtil.sorting_dict_by_keys(input_list_dict, "age", "name")
        print("output_dict_2:", output_dict_2)
        assert output_dict_2[0]["age"] == 20
        assert output_dict_2[1]["age"] == 20
        assert output_dict_2[2]["age"] == 25
        assert output_dict_2[3]["age"] == 25
        assert output_dict_2[4]["age"] == 30
        assert output_dict_2[0]["name"] == "Alice"
        assert output_dict_2[1]["name"] == "Bob"
        assert output_dict_2[2]["name"] == "Bob"
        assert output_dict_2[3]["name"] == "Charlie"
        assert output_dict_2[4]["name"] == "Aska"

        # More keys + reverse
        output_dict_3 = NewtUtil.sorting_dict_by_keys(input_list_dict, "age", "name", reverse=True)
        print("output_dict_3:", output_dict_3)
        assert output_dict_3[4]["age"] == 20
        assert output_dict_3[3]["age"] == 20
        assert output_dict_3[2]["age"] == 25
        assert output_dict_3[1]["age"] == 25
        assert output_dict_3[0]["age"] == 30
        assert output_dict_3[4]["name"] == "Alice"
        assert output_dict_3[3]["name"] == "Bob"
        assert output_dict_3[2]["name"] == "Bob"
        assert output_dict_3[1]["name"] == "Charlie"
        assert output_dict_3[0]["name"] == "Aska"
        assert output_dict_2 == output_dict_3[::-1]

        # No keys
        output_dict_4 = NewtUtil.sorting_dict_by_keys(input_list_dict)
        print("output_dict_4:", output_dict_4)
        assert output_dict_4[0]["age"] == 25
        assert output_dict_4[1]["age"] == 25
        assert output_dict_4[2]["age"] == 20
        assert output_dict_4[3]["age"] == 30
        assert output_dict_4[4]["age"] == 20
        assert output_dict_4[0]["name"] == "Charlie"
        assert output_dict_4[1]["name"] == "Bob"
        assert output_dict_4[2]["name"] == "Alice"
        assert output_dict_4[3]["name"] == "Aska"
        assert output_dict_4[4]["name"] == "Bob"

        # No keys + reverse
        output_dict_5 = NewtUtil.sorting_dict_by_keys(input_list_dict, reverse=True)
        print("output_dict_5:", output_dict_5)
        assert output_dict_5[0]["name"] == "Bob"
        assert output_dict_5[1]["name"] == "Aska"
        assert output_dict_5[2]["name"] == "Alice"
        assert output_dict_5[3]["name"] == "Bob"
        assert output_dict_5[4]["name"] == "Charlie"
        assert output_dict_5[0]["age"] == 20
        assert output_dict_5[1]["age"] == 30
        assert output_dict_5[2]["age"] == 20
        assert output_dict_5[3]["age"] == 25
        assert output_dict_5[4]["age"] == 25

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_list_dict: [{'name': 'Charlie', 'age': 25}, {'name': 'Bob', 'age': 25}, {'name': 'Alice', 'age': 20}, {'name': 'Aska', 'age': 30}, {'name': 'Bob', 'age': 20}]\n" in captured.out
        assert "\noutput_dict_1: [{'name': 'Alice', 'age': 20}, {'name': 'Aska', 'age': 30}, {'name': 'Bob', 'age': 25}, {'name': 'Bob', 'age': 20}, {'name': 'Charlie', 'age': 25}]\n" in captured.out
        assert "\noutput_dict_2: [{'name': 'Alice', 'age': 20}, {'name': 'Bob', 'age': 20}, {'name': 'Bob', 'age': 25}, {'name': 'Charlie', 'age': 25}, {'name': 'Aska', 'age': 30}]\n" in captured.out
        assert "\noutput_dict_3: [{'name': 'Aska', 'age': 30}, {'name': 'Charlie', 'age': 25}, {'name': 'Bob', 'age': 25}, {'name': 'Bob', 'age': 20}, {'name': 'Alice', 'age': 20}]\n" in captured.out
        assert "\noutput_dict_4: [{'name': 'Charlie', 'age': 25}, {'name': 'Bob', 'age': 25}, {'name': 'Alice', 'age': 20}, {'name': 'Aska', 'age': 30}, {'name': 'Bob', 'age': 20}]\n" in captured.out
        assert "\noutput_dict_5: [{'name': 'Bob', 'age': 20}, {'name': 'Aska', 'age': 30}, {'name': 'Alice', 'age': 20}, {'name': 'Bob', 'age': 25}, {'name': 'Charlie', 'age': 25}]\n" in captured.out

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_sorting_dict_missing_keys(self, capsys):
        """ Test sorting_dict_by_keys places missing key dicts at end. """
        print_my_func_name()

        input_list_dict = [
            {"name": "Charlie", "age": 25},
            {"name": "Bob"},  # Missing age
            {},
            {"name": "Alice", "age": 20},
            {"name": "Aska", "age": None},
            None,
            {"name": "Bob", "age": 20},
        ]
        print("input_list_dict:", input_list_dict)

        output_dict_1 = NewtUtil.sorting_dict_by_keys(input_list_dict, "age")
        print("output_dict_1:", output_dict_1)
        assert output_dict_1[0]["age"] == 20
        assert output_dict_1[1]["age"] == 20
        assert output_dict_1[2]["age"] == 25
        assert output_dict_1[3]["age"] is None
        assert "age" not in output_dict_1[4]  # Expected absence of result
        assert output_dict_1[0]["name"] == "Alice"
        assert output_dict_1[1]["name"] == "Bob"
        assert output_dict_1[2]["name"] == "Charlie"
        assert output_dict_1[3]["name"] == "Aska"
        assert output_dict_1[4]["name"] == "Bob"
        assert output_dict_1[5] == {}
        assert output_dict_1[6] is None

        output_dict_2 = NewtUtil.sorting_dict_by_keys(input_list_dict, "age", reverse=True)
        print("output_dict_2:", output_dict_2)
        assert output_dict_2[0] is None
        assert output_dict_2[1] == {}
        assert "age" not in output_dict_2[2]  # Expected absence of result
        assert output_dict_2[3]["age"] is None
        assert output_dict_2[4]["age"] == 25
        assert output_dict_2[5]["age"] == 20
        assert output_dict_2[6]["age"] == 20
        assert output_dict_2[2]["name"] == "Bob"
        assert output_dict_2[3]["name"] == "Aska"
        assert output_dict_2[4]["name"] == "Charlie"
        assert output_dict_2[5]["name"] == "Alice"
        assert output_dict_2[6]["name"] == "Bob"

        output_dict_3 = NewtUtil.sorting_dict_by_keys(input_list_dict, reverse=True)
        print("output_dict_3:", output_dict_3)
        assert output_dict_3[0]["age"] == 20
        assert output_dict_3[1] is None
        assert output_dict_3[2]["age"] is None
        assert output_dict_3[3]["age"] == 20
        assert output_dict_3[4] == {}
        assert "age" not in output_dict_3[5]  # Expected absence of result
        assert output_dict_3[6]["age"] == 25
        assert output_dict_3[0]["name"] == "Bob"
        assert output_dict_3[2]["name"] == "Aska"
        assert output_dict_3[3]["name"] == "Alice"
        assert output_dict_3[5]["name"] == "Bob"
        assert output_dict_3[6]["name"] == "Charlie"

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_list_dict: [{'name': 'Charlie', 'age': 25}, {'name': 'Bob'}, {}, {'name': 'Alice', 'age': 20}, {'name': 'Aska', 'age': None}, None, {'name': 'Bob', 'age': 20}]\n" in captured.out
        assert "\noutput_dict_1: [{'name': 'Alice', 'age': 20}, {'name': 'Bob', 'age': 20}, {'name': 'Charlie', 'age': 25}, {'name': 'Aska', 'age': None}, {'name': 'Bob'}, {}, None]\n" in captured.out
        assert "\noutput_dict_2: [None, {}, {'name': 'Bob'}, {'name': 'Aska', 'age': None}, {'name': 'Charlie', 'age': 25}, {'name': 'Alice', 'age': 20}, {'name': 'Bob', 'age': 20}]\n" in captured.out
        assert "\noutput_dict_3: [{'name': 'Bob', 'age': 20}, None, {'name': 'Aska', 'age': None}, {'name': 'Alice', 'age': 20}, {}, {'name': 'Bob'}, {'name': 'Charlie', 'age': 25}]\n" in captured.out

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_sorting_dict_single_key(self, capsys):
        """ Test sorting_dict_by_keys with single-key dicts: wrong key, correct key, no key. """
        print_my_func_name()

        input_list_dict = [
            {"name": "Charlie"},
            {"name": "Alice"},
            {"name": "Bob"},
            {"name": "Aska"},
        ]
        print("input_list_dict:", input_list_dict)

        # Wrong key
        output_dict_1 = NewtUtil.sorting_dict_by_keys(input_list_dict, "age")
        print("output_dict_1:", output_dict_1)
        assert output_dict_1[0]["name"] == "Charlie"
        assert output_dict_1[1]["name"] == "Alice"
        assert output_dict_1[2]["name"] == "Bob"
        assert output_dict_1[3]["name"] == "Aska"

        # Wrong key + reverse
        output_dict_2 = NewtUtil.sorting_dict_by_keys(input_list_dict, "age", reverse=True)
        print("output_dict_2:", output_dict_2)
        assert output_dict_2[0]["name"] == "Charlie"
        assert output_dict_2[1]["name"] == "Alice"
        assert output_dict_2[2]["name"] == "Bob"
        assert output_dict_2[3]["name"] == "Aska"
        assert input_list_dict == output_dict_2
        assert output_dict_1 == output_dict_2

        # Single key
        output_dict_3 = NewtUtil.sorting_dict_by_keys(input_list_dict, "name")
        print("output_dict_3:", output_dict_3)
        assert output_dict_3[0]["name"] == "Alice"
        assert output_dict_3[1]["name"] == "Aska"
        assert output_dict_3[2]["name"] == "Bob"
        assert output_dict_3[3]["name"] == "Charlie"

        # Single key + reverse
        output_dict_4 = NewtUtil.sorting_dict_by_keys(input_list_dict, "name", reverse=True)
        print("output_dict_4:", output_dict_4)
        assert output_dict_4[0]["name"] == "Charlie"
        assert output_dict_4[1]["name"] == "Bob"
        assert output_dict_4[2]["name"] == "Aska"
        assert output_dict_4[3]["name"] == "Alice"

        # No key
        output_dict_5 = NewtUtil.sorting_dict_by_keys(input_list_dict)
        print("output_dict_5:", output_dict_5)
        assert output_dict_5[0]["name"] == "Alice"
        assert output_dict_5[1]["name"] == "Aska"
        assert output_dict_5[2]["name"] == "Bob"
        assert output_dict_5[3]["name"] == "Charlie"
        assert output_dict_3 == output_dict_5

        # No key + reverse
        output_dict_6 = NewtUtil.sorting_dict_by_keys(input_list_dict, reverse=True)
        print("output_dict_6:", output_dict_6)
        assert output_dict_6[0]["name"] == "Charlie"
        assert output_dict_6[1]["name"] == "Bob"
        assert output_dict_6[2]["name"] == "Aska"
        assert output_dict_6[3]["name"] == "Alice"
        assert output_dict_4 == output_dict_6

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_list_dict: [{'name': 'Charlie'}, {'name': 'Alice'}, {'name': 'Bob'}, {'name': 'Aska'}]\n" in captured.out
        assert "\noutput_dict_1: [{'name': 'Charlie'}, {'name': 'Alice'}, {'name': 'Bob'}, {'name': 'Aska'}]\n" in captured.out
        assert "\noutput_dict_2: [{'name': 'Charlie'}, {'name': 'Alice'}, {'name': 'Bob'}, {'name': 'Aska'}]\n" in captured.out
        assert "\noutput_dict_3: [{'name': 'Alice'}, {'name': 'Aska'}, {'name': 'Bob'}, {'name': 'Charlie'}]\n" in captured.out
        assert "\noutput_dict_4: [{'name': 'Charlie'}, {'name': 'Bob'}, {'name': 'Aska'}, {'name': 'Alice'}]\n" in captured.out
        assert "\noutput_dict_5: [{'name': 'Alice'}, {'name': 'Aska'}, {'name': 'Bob'}, {'name': 'Charlie'}]\n" in captured.out
        assert "\noutput_dict_6: [{'name': 'Charlie'}, {'name': 'Bob'}, {'name': 'Aska'}, {'name': 'Alice'}]\n" in captured.out

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err


    def test_sorting_dict_by_keys_with_errors_no_stop(self, capsys):
        """ Test sorting_dict_by_keys handles invalid input without raising exceptions. """
        print_my_func_name()

        # Not a list
        input_dict = {"name": "Alice"}
        print("input_dict:", input_dict)
        output_1 = NewtUtil.sorting_dict_by_keys(input_dict, stop=False)  # type: ignore
        print("output_1:", output_1)

        # List with non-dict elements
        input_list = [1, 2, 3]
        print("input_list:", input_list)
        output_2 = NewtUtil.sorting_dict_by_keys(input_list, stop=False)  # type: ignore
        print("output_2:", output_2)

        # List with mixed valid and invalid elements
        input_list_mix = [{"name": "Alice"}, 42, "string"]
        print("input_list_mix:", input_list_mix)
        output_3 = NewtUtil.sorting_dict_by_keys(input_list_mix, stop=False)
        print("output_3:", output_3)

        # Invalid key type
        input_list_dict = [{123: "Alice"}]
        print("input_list_dict:", input_list_dict)
        output_4 = NewtUtil.sorting_dict_by_keys(input_list_dict, 123, stop=False)  # type: ignore
        print("output_4:", output_4)

        # Empty input
        input_list_empty = []
        print("input_list_empty:", input_list_empty)
        output_5 = NewtUtil.sorting_dict_by_keys(input_list_empty)
        print("output_5:", output_5)

        # None as input
        input_None = None
        print("input_None:", input_None)
        output_6 = NewtUtil.sorting_dict_by_keys(input_None)  # type: ignore
        print("output_6:", output_6)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_dict: {'name': 'Alice'}\noutput_1: []\n" in captured.out
        assert "\ninput_list: [1, 2, 3]\noutput_2: []\n" in captured.out
        assert "\ninput_list_mix: [{'name': 'Alice'}, 42, 'string']\noutput_3: []\n" in captured.out
        assert "\ninput_list_dict: [{123: 'Alice'}]\noutput_4: []\n" in captured.out
        assert "\ninput_list_empty: []\noutput_5: []\n" in captured.out
        assert "\ninput_None: None\noutput_6: []\n" in captured.out

        assert captured.err.count("\n::: ERROR :::\n") == 10
        assert "\nLocation: Newt.utility.sorting_dict_by_keys : data_list > Newt.console.validate_type\n" in captured.err
        assert "\nValue: {'name': 'Alice'}\nReceived type: <class 'dict'>\nExpected type: <class 'list'>\n" in captured.err
        assert "\nLocation: Newt.utility.sorting_dict_by_keys : k in dl.keys() > Newt.console.validate_type\n" in captured.err
        assert "\nValue: 123\nReceived type: <class 'int'>\nExpected type: <class 'str'>\n" in captured.err
        assert captured.err.count("\nLocation: Newt.utility.sorting_dict_by_keys : dl in data_list > Newt.console.validate_type\n") == 5
        assert "\nValue: 1\nReceived type: <class 'int'>\nExpected type: (<class 'dict'>, <class 'NoneType'>)\n" in captured.err
        assert "\nValue: 2\nReceived type: <class 'int'>\nExpected type: (<class 'dict'>, <class 'NoneType'>)\n" in captured.err
        assert "\nValue: 3\nReceived type: <class 'int'>\nExpected type: (<class 'dict'>, <class 'NoneType'>)\n" in captured.err
        assert "\nValue: 42\nReceived type: <class 'int'>\nExpected type: (<class 'dict'>, <class 'NoneType'>)\n" in captured.err
        assert "\nValue: string\nReceived type: <class 'str'>\nExpected type: (<class 'dict'>, <class 'NoneType'>)\n" in captured.err
        assert captured.err.count("\nLocation: Newt.utility.sorting_dict_by_keys : invalid_element_type\n") == 2
        assert "\nExpected a list of dictionaries\ndata_list: [1, 2, 3]\n" in captured.err
        assert "\nExpected a list of dictionaries\ndata_list: [{'name': 'Alice'}, 42, 'string']\n" in captured.err
        assert "\nLocation: Newt.utility.sorting_dict_by_keys : invalid_key_type\n" in captured.err
        assert "\nExpected a keys of dictionaries to be str\ndata_list: [{123: 'Alice'}]\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_dict_by_keys_with_errors_and_stop(self, capsys):
        """ Test sorting_dict_by_keys handles invalid input with raising exceptions. """
        print_my_func_name()

        # Not a list
        input_dict = {"name": "Alice"}
        print("input_dict:", input_dict)
        with pytest.raises(SystemExit) as exc_info_1:
            NewtUtil.sorting_dict_by_keys(input_dict)  # type: ignore
            print("This line will not be printed")
        assert exc_info_1.value.code == 1

        # List with non-dict elements
        input_list = [1, 2, 3]
        print("input_list:", input_list)
        with pytest.raises(SystemExit) as exc_info_2:
            NewtUtil.sorting_dict_by_keys(input_list)  # type: ignore
            print("This line will not be printed")
        assert exc_info_2.value.code == 1

        # List with mixed valid and invalid elements
        input_list_mix = [{"name": "Alice"}, 42, "string"]
        print("input_list_mix:", input_list_mix)
        with pytest.raises(SystemExit) as exc_info_3:
            NewtUtil.sorting_dict_by_keys(input_list_mix)
            print("This line will not be printed")
        assert exc_info_3.value.code == 1

        # Invalid key type
        input_list_dict = [{123: "Alice"}]
        print("input_list_dict:", input_list_dict)
        with pytest.raises(SystemExit) as exc_info_4:
            NewtUtil.sorting_dict_by_keys(input_list_dict, 123)  # type: ignore
            print("This line will not be printed")
        assert exc_info_4.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninput_dict: {'name': 'Alice'}\n" in captured.out
        assert "\ninput_list: [1, 2, 3]\n" in captured.out
        assert "\ninput_list_mix: [{'name': 'Alice'}, 42, 'string']\n" in captured.out
        assert "\ninput_list_dict: [{123: 'Alice'}]\n" in captured.out

        assert captured.err.count("\n::: ERROR :::\n") == 10
        assert "\nLocation: Newt.utility.sorting_dict_by_keys : data_list > Newt.console.validate_type\n" in captured.err
        assert "\nValue: {'name': 'Alice'}\nReceived type: <class 'dict'>\nExpected type: <class 'list'>\n" in captured.err
        assert "\nLocation: Newt.utility.sorting_dict_by_keys : k in dl.keys() > Newt.console.validate_type\n" in captured.err
        assert "\nValue: 123\nReceived type: <class 'int'>\nExpected type: <class 'str'>\n" in captured.err
        assert captured.err.count("\nLocation: Newt.utility.sorting_dict_by_keys : dl in data_list > Newt.console.validate_type\n") == 5
        assert "\nValue: 1\nReceived type: <class 'int'>\nExpected type: (<class 'dict'>, <class 'NoneType'>)\n" in captured.err
        assert "\nValue: 2\nReceived type: <class 'int'>\nExpected type: (<class 'dict'>, <class 'NoneType'>)\n" in captured.err
        assert "\nValue: 3\nReceived type: <class 'int'>\nExpected type: (<class 'dict'>, <class 'NoneType'>)\n" in captured.err
        assert "\nValue: 42\nReceived type: <class 'int'>\nExpected type: (<class 'dict'>, <class 'NoneType'>)\n" in captured.err
        assert "\nValue: string\nReceived type: <class 'str'>\nExpected type: (<class 'dict'>, <class 'NoneType'>)\n" in captured.err
        assert captured.err.count("\nLocation: Newt.utility.sorting_dict_by_keys : invalid_element_type\n") == 2
        assert "\nExpected a list of dictionaries\ndata_list: [1, 2, 3]\n" in captured.err
        assert "\nExpected a list of dictionaries\ndata_list: [{'name': 'Alice'}, 42, 'string']\n" in captured.err
        assert "\nLocation: Newt.utility.sorting_dict_by_keys : invalid_key_type\n" in captured.err
        assert "\nExpected a keys of dictionaries to be str\ndata_list: [{123: 'Alice'}]\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


class TestSelectFromInput:
    """ Tests for select_from_input function. """


    @patch('newtutils.utility.input')
    def test_select_from_input_all_flows(self, mock_input, capsys):
        """
        Test select_from_input behavior across multiple input scenarios.

        Covers:
        - Returns key for valid numbered choice (with and without counts).
        - Retries on invalid input until valid choice or 'X' to exit.
        - Strips whitespace from user input before validation.
        - Raises SystemExit(1) on 'X' input (exit/cancel).
        - Raises SystemExit(1) on KeyboardInterrupt.
        """
        print_my_func_name()

        missing_values_list = [
            (1, "admin", "Stockholm"),
            (2, "user", "Oslo"),
            (3, "user", "Stockholm"),
            (4, "user", "Berlin"),
            (5, "admin", "Oslo"),
        ]
        print("missing_values_list:", missing_values_list)

        missing_values_count = NewtUtil.count_values_by_position(missing_values_list, 2)
        print("missing_values_count:", missing_values_count)

        input_dict = {
            "1": "Oslo",
            "2": "Stockholm",
            "3": "Berlin",
        }
        print("input_dict:", input_dict)

        mock_input.side_effect = ["1"]

        result_1 = NewtUtil.select_from_input(input_dict)
        print("result_1:", result_1)
        assert result_1 == "1"

        mock_input.side_effect = ["1"]

        result_2 = NewtUtil.select_from_input(input_dict, missing_values_count)
        print("result_2:", result_2)
        assert result_2 == "1"

        mock_input.side_effect = ["abc", "999", "2"]

        result_3 = NewtUtil.select_from_input(input_dict)
        print("result_3:", result_3)
        assert result_3 == "2"

        # Check .strip()
        mock_input.side_effect = ["abc", " 999 ", " 2 "]

        result_4 = NewtUtil.select_from_input(input_dict, missing_values_count)
        print("result_4:", result_4)
        assert result_4 == "2"

        mock_input.side_effect = ["x"]

        with pytest.raises(SystemExit) as exc_info_5:
            NewtUtil.select_from_input(input_dict)
            print("This line will not be printed")
        assert exc_info_5.value.code == 1

        mock_input.side_effect = ["x"]

        with pytest.raises(SystemExit) as exc_info_6:
            NewtUtil.select_from_input(input_dict, missing_values_count)
            print("This line will not be printed")
        assert exc_info_6.value.code == 1

        mock_input.side_effect = KeyboardInterrupt()

        with pytest.raises(SystemExit) as exc_info_7:
            NewtUtil.select_from_input(input_dict)
            print("This line will not be printed")
        assert exc_info_7.value.code == 1

        mock_input.side_effect = KeyboardInterrupt()

        with pytest.raises(SystemExit) as exc_info_8:
            NewtUtil.select_from_input(input_dict, missing_values_count)
            print("This line will not be printed")
        assert exc_info_8.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nmissing_values_list: [(1, 'admin', 'Stockholm'), (2, 'user', 'Oslo'), (3, 'user', 'Stockholm'), (4, 'user', 'Berlin'), (5, 'admin', 'Oslo')]\n" in captured.out
        assert "\nmissing_values_count: {'Stockholm': 2, 'Oslo': 2, 'Berlin': 1}\n" in captured.out
        assert "\ninput_dict: {'1': 'Oslo', '2': 'Stockholm', '3': 'Berlin'}\n" in captured.out
        assert "\n\n3 Available options to choose from:\n  1: Oslo\n  2: Stockholm\n  3: Berlin\n  X: Exit / Cancel\n[INPUT]: 1\nSelected option: Oslo\n\nresult_1: 1\n" in captured.out
        assert "\n\n3 Available options to choose from:\n  1: (2) Oslo\n  2: (2) Stockholm\n  3: (1) Berlin\n  X: Exit / Cancel\n[INPUT]: 1\nSelected option: Oslo\n\nresult_2: 1\n" in captured.out
        assert "\n\n3 Available options to choose from:\n  1: Oslo\n  2: Stockholm\n  3: Berlin\n  X: Exit / Cancel\n[INPUT]: abc\nOption not in list. Try again.\n[INPUT]: 999\nOption not in list. Try again.\n[INPUT]: 2\nSelected option: Stockholm\n\nresult_3: 2\n" in captured.out
        assert "\n\n3 Available options to choose from:\n  1: (2) Oslo\n  2: (2) Stockholm\n  3: (1) Berlin\n  X: Exit / Cancel\n[INPUT]: abc\nOption not in list. Try again.\n[INPUT]: 999\nOption not in list. Try again.\n[INPUT]: 2\nSelected option: Stockholm\n\nresult_4: 2\n" in captured.out
        assert "\n\n3 Available options to choose from:\n  1: Oslo\n  2: Stockholm\n  3: Berlin\n  X: Exit / Cancel\n[INPUT]: x\n\n" in captured.out
        assert "\n\n3 Available options to choose from:\n  1: (2) Oslo\n  2: (2) Stockholm\n  3: (1) Berlin\n  X: Exit / Cancel\n[INPUT]: x\n\n" in captured.out
        assert "\n\n3 Available options to choose from:\n  1: Oslo\n  2: Stockholm\n  3: Berlin\n  X: Exit / Cancel\n\n" in captured.out
        assert "\n\n3 Available options to choose from:\n  1: (2) Oslo\n  2: (2) Stockholm\n  3: (1) Berlin\n  X: Exit / Cancel\n\n" in captured.out

        assert captured.err.count("\n::: ERROR :::\n") == 4
        assert captured.err.count("\nLocation: Newt.utility.select_from_input : choice = [X]\n::: ERROR :::\nSelection cancelled.\n") == 2
        assert captured.err.count("\nLocation: Newt.utility.select_from_input : KeyboardInterrupt\n::: ERROR :::\nSelection cancelled.\n") == 2

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


    def test_select_from_input_invalid_type(self, capsys):
        """ Test select_from_input non-dict arg triggers validate_type SystemExit. """
        print_my_func_name()

        invalid_input = "not a dict"
        print("invalid_input:", invalid_input)

        with pytest.raises(SystemExit) as exc_info:
            NewtUtil.select_from_input(invalid_input)  # type: ignore
            print("This line will not be printed")
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\ninvalid_input: not a dict\n" in captured.out

        assert "\n::: ERROR :::\n" in captured.err
        assert "\nLocation: Newt.utility.select_from_input : select_dict > Newt.console.validate_type\n" in captured.err
        assert "\nValue: not a dict\nReceived type: <class 'str'>\nExpected type: <class 'dict'>\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err
