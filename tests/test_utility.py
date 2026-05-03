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
            ("user", 2,  "Oslo"),
            ("admin", 3, "Stockholm"),
            ("user", 4,  "Berlin"),
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
        assert "\nLocation: Newt.utility.count_values_by_position : input_sequence > Newt.console.validate_type\n" in captured.err
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
        assert "\nLocation: Newt.utility.count_values_by_position : input_sequence > Newt.console.validate_type\n" in captured.err
        assert "\nValue: not a sequence of sequences\nReceived type: <class 'str'>\nExpected type: (<class 'list'>, <class 'tuple'>)\n" in captured.err

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err


class TestSortingDictByKeys:
    """ Tests for sorting_dict_by_keys function. """


    def test_sorting_dict_single_key(self, capsys):
        """ Test sorting_dict_by_keys sorts list of dicts ascending by single key. """
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

        assert "\n[{'name': 'Charlie', 'age': 25}, {'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 20}]\n[{'name': 'Bob', 'age': 20}, {'name': 'Charlie', 'age': 25}, {'name': 'Alice', 'age': 30}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_dict_multiple_keys(self, capsys):
        """ Test sorting_dict_by_keys sorts list of dicts by age then name. """
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

        assert "\n[{'name': 'Charlie', 'age': 25}, {'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 20}]\n[{'name': 'Bob', 'age': 20}, {'name': 'Alice', 'age': 25}, {'name': 'Charlie', 'age': 25}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_dict_reverse_order(self, capsys):
        """ Test sorting_dict_by_keys with reverse=True sorts descending by age. """
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

        assert "\n[{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 20}, {'name': 'Charlie', 'age': 25}]\n[{'name': 'Alice', 'age': 30}, {'name': 'Charlie', 'age': 25}, {'name': 'Bob', 'age': 20}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_dict_missing_key(self, capsys):
        """ Test sorting_dict_by_keys places missing key dicts at end. """
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

        assert "\n[{'name': 'Alice', 'age': 30}, {'name': 'Bob'}, {'name': 'Charlie', 'age': 25}]\n[{'name': 'Charlie', 'age': 25}, {'name': 'Alice', 'age': 30}, {'name': 'Bob'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_dict_none_values(self, capsys):
        """ Test sorting_dict_by_keys places None values at end. """
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

        assert "\n[{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': None}, {'name': 'Charlie', 'age': 25}]\n[{'name': 'Charlie', 'age': 25}, {'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': None}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_dict_empty_list(self, capsys):
        """ Test sorting_dict_by_keys returns empty list for empty input. """
        print_my_func_name()

        result = NewtUtil.sorting_dict_by_keys([], stop=False)
        print(result)
        assert result == []

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input : is_empty > Newt.utility.sorting_dict_by_keys : data\n" in captured.out
        assert "\nValue must be non-empty\n" in captured.out
        assert "\nValue: []\n" in captured.out


    def test_sorting_dict_no_keys(self, capsys):
        """ Test sorting_dict_by_keys no args sorts list by dict value order. """
        print_my_func_name()

        input_dict = [
            {"name": "Charlie"},
            {"name": "Alice"},
            {"name": "Bob"}
        ]
        print(input_dict)
        result = NewtUtil.sorting_dict_by_keys(input_dict)
        print(result)
        assert result[0]["name"] == "Alice"
        assert result[1]["name"] == "Bob"
        assert result[2]["name"] == "Charlie"
        assert len(result) == 3

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[{'name': 'Charlie'}, {'name': 'Alice'}, {'name': 'Bob'}]\n[{'name': 'Alice'}, {'name': 'Bob'}, {'name': 'Charlie'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_dict_multi_keys_no_args(self, capsys):
        """ Test sorting_dict_by_keys no args returns unchanged multi-key dict list. """
        print_my_func_name()

        input_dict = [
            {"name": "Charlie", "age": 25},
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 20}
        ]
        print(input_dict)
        result = NewtUtil.sorting_dict_by_keys(input_dict)
        print(result)
        # Should return in original order since no keys specified and dicts have multiple keys
        assert result[0]["age"] == 25
        assert result[1]["age"] == 30
        assert result[2]["age"] == 20
        assert result[0]["name"] == "Charlie"
        assert result[1]["name"] == "Alice"
        assert result[2]["name"] == "Bob"
        assert len(result) == 3

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[{'name': 'Charlie', 'age': 25}, {'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 20}]\n[{'name': 'Charlie', 'age': 25}, {'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 20}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_dict_mixed_struct_no_keys(self, capsys):
        """ Test sorting_dict_by_keys no args unchanged for mixed dict structures. """
        print_my_func_name()

        input_dict = [
            {"name": "Charlie"},
            {"name": "Alice", "age": 30},
            {"name": "Bob"}
        ]
        print(input_dict)
        result = NewtUtil.sorting_dict_by_keys(input_dict)
        print(result)
        # Should return in original order since no keys specified and dicts have different structures
        assert "age" not in result[0]  # Expected absence of result
        assert result[1]["age"] == 30
        assert "age" not in result[2]  # Expected absence of result
        assert result[0]["name"] == "Charlie"
        assert result[1]["name"] == "Alice"
        assert result[2]["name"] == "Bob"
        assert len(result) == 3

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n[{'name': 'Charlie'}, {'name': 'Alice', 'age': 30}, {'name': 'Bob'}]\n[{'name': 'Charlie'}, {'name': 'Alice', 'age': 30}, {'name': 'Bob'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_sorting_dict_not_list(self, capsys):
        """ Test sorting_dict_by_keys non-list input raises SystemExit or returns result. """
        print_my_func_name()

        input_str = "not a list"
        print(input_str)

        with pytest.raises(SystemExit) as exc_info:
            NewtUtil.sorting_dict_by_keys(input_str, "key")  # type: ignore
            print("This line will not be printed")
        assert exc_info.value.code == 1

        result = NewtUtil.sorting_dict_by_keys(input_str, "key", stop=False)  # type: ignore
        print(result)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\n::: ERROR :::\n") == 2
        assert captured.out.count("\nLocation: Newt.console.validate_input > Newt.utility.sorting_dict_by_keys : data\n") == 2
        assert captured.out.count("\nExpected (<class 'list'>, <class 'tuple'>), got <class 'str'>\n") == 2
        assert captured.out.count("\nValue: not a list\n") == 2
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


    def test_sorting_dict_not_dicts(self, capsys):
        """ Test sorting_dict_by_keys non-dict list items raise SystemExit. """
        print_my_func_name()

        input_list = [1, 2, 3]
        print(input_list)
        with pytest.raises(SystemExit) as exc_info:
            NewtUtil.sorting_dict_by_keys(input_list, "key")  # type: ignore
            print("This line will not be printed")
        assert exc_info.value.code == 1

        result = NewtUtil.sorting_dict_by_keys(input_list, "key", stop=False)  # type: ignore
        print(result)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\n::: ERROR :::\n") == 4
        assert captured.out.count("\nLocation: Newt.console.validate_input\n") == 2
        assert captured.out.count("\nExpected <class 'dict'>, got <class 'int'>\n") == 2
        assert captured.out.count("\nValue: 1\n") == 2
        assert captured.out.count("\nLocation: Newt.utility.sorting_dict_by_keys : data not all\n") == 2
        assert captured.out.count("\nExpected a list of dictionaries\n") == 2
        assert captured.out.count("\nData: [1, 2, 3]\n") == 2
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


    def test_sorting_dict_invalid_key_type(self, capsys):
        """ Test sorting_dict_by_keys non-str key raises SystemExit. """
        print_my_func_name()

        input_dict = [{"name": "Alice"}]
        print(input_dict)
        with pytest.raises(SystemExit) as exc_info:
            NewtUtil.sorting_dict_by_keys(input_dict, 123)  # type: ignore
            print("This line will not be printed")
        assert exc_info.value.code == 1

        result = NewtUtil.sorting_dict_by_keys(input_dict, 123, stop=False)  # type: ignore
        print(result)

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\n::: ERROR :::\n") == 4
        assert captured.out.count("\nLocation: Newt.console.validate_input\n") == 2
        assert captured.out.count("\nExpected <class 'str'>, got <class 'int'>\n") == 2
        assert captured.out.count("\nValue: 123\n") == 2
        assert captured.out.count("\nLocation: Newt.utility.sorting_dict_by_keys : keys not all\n") == 2
        assert captured.out.count("\nKeys must be strings\n") == 2
        assert captured.out.count("\nKeys: (123,)\n") == 2
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


    def test_sorting_dict_complex_keys(self, capsys):
        """ Test sorting_dict_by_keys multi-level sort: category, priority, name. """
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

        assert "\n[{'category': 'A', 'priority': 2, 'name': 'Item2'}, {'category': 'B', 'priority': 1, 'name': 'Item1'}, {'category': 'A', 'priority': 1, 'name': 'Item1'}, {'category': 'A', 'priority': 2, 'name': 'Item1'}]\n[{'category': 'A', 'priority': 1, 'name': 'Item1'}, {'category': 'A', 'priority': 2, 'name': 'Item1'}, {'category': 'A', 'priority': 2, 'name': 'Item2'}, {'category': 'B', 'priority': 1, 'name': 'Item1'}]\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


class TestSelectFromInput:
    """ Tests for select_from_input function. """


    @patch('newtutils.utility.input', side_effect=["1"])
    def test_select_from_input_valid_choice(self, mock_input, capsys):
        """ Test select_from_input returns key for valid numbered user choice. """
        print_my_func_name()

        select_dict = {"1": "Option A", "2": "Option B", "3": "Option C"}
        print(select_dict)

        result = NewtUtil.select_from_input(select_dict)
        assert result == "1"

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nAvailable list: 3\n" in captured.out
        assert "\n  1: Option A\n" in captured.out
        assert "\n  2: Option B\n" in captured.out
        assert "\n  3: Option C\n" in captured.out
        assert "\n  X: Exit / Cancel\n" in captured.out
        assert "\n[INPUT]: 1\n" in captured.out
        assert "\nSelected option: Option A\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    @patch('newtutils.utility.input', side_effect=["abc", "999", "2"])
    def test_select_from_input_invalid_then_valid(self, mock_input, capsys):
        """ Test select_from_input handles invalid input followed by valid choice. """
        print_my_func_name()

        select_dict = {"1": "Option A", "2": "Option B"}
        print(select_dict)

        result = NewtUtil.select_from_input(select_dict)
        assert result == "2"

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nAvailable list: 2\n" in captured.out
        assert "\n  1: Option A\n" in captured.out
        assert "\n  2: Option B\n" in captured.out
        assert "\n  X: Exit / Cancel\n" in captured.out
        assert "\n[INPUT]: abc\nInvalid input. Please enter a number.\n" in captured.out
        assert "\n[INPUT]: 999\nNumber out of range. Try again.\n" in captured.out
        assert "\n[INPUT]: 2\nSelected option: Option B\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    @patch('newtutils.utility.input', side_effect=["X"])
    def test_select_from_input_cancel_uppercase(self, mock_input, capsys):
        """ Test select_from_input handles uppercase cancel input correctly. """
        print_my_func_name()

        select_dict = {"1": "Option A"}
        print(select_dict)

        with pytest.raises(SystemExit) as exc_info:
            NewtUtil.select_from_input(select_dict)
            print("This line will not be printed")
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nAvailable list: 1\n" in captured.out
        assert "\n  1: Option A\n" in captured.out
        assert "\n  X: Exit / Cancel\n" in captured.out
        assert "\n[INPUT]: x\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.utility.select_from_input : choice = [X]\n" in captured.out
        assert "\nSelection cancelled.\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


    def test_select_from_input_invalid_type(self, capsys):
        """ Test select_from_input non-dict arg triggers validate_input SystemExit. """
        print_my_func_name()

        invalid_input = "not a dict"
        print(invalid_input)

        with pytest.raises(SystemExit) as exc_info:
            NewtUtil.select_from_input(invalid_input)  # type: ignore
            print("This line will not be printed")
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.utility.select_from_input : select_dict\n" in captured.out
        assert "\nExpected <class 'dict'>, got <class 'str'>\n" in captured.out
        assert "\nValue: not a dict\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


    @patch('newtutils.utility.input')
    def test_select_from_input_keyboard_interrupt(self, mock_input, capsys):
        """ Test select_from_input raises SystemExit on KeyboardInterrupt. """
        print_my_func_name()

        mock_input.side_effect = KeyboardInterrupt()

        select_dict = {"1": "Option A", "2": "Option B"}
        print(select_dict)

        with pytest.raises(SystemExit) as exc_info:
            NewtUtil.select_from_input(select_dict)
            print("This line will not be printed")
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nAvailable list: 2\n" in captured.out
        assert "\n  1: Option A\n" in captured.out
        assert "\n  2: Option B\n" in captured.out
        assert "\n  X: Exit / Cancel\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.utility.select_from_input : KeyboardInterrupt\n" in captured.out
        assert "\nSelection cancelled.\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


    @patch('newtutils.utility.input', return_value=" 2 ")
    def test_select_from_input_spaces(self, mock_input, capsys):
        """ Test select_from_input handles input with leading and trailing spaces correctly. """
        print_my_func_name()

        select_dict = {"1": "Option A", "2": "Option B"}
        print(select_dict)

        result = NewtUtil.select_from_input(select_dict)
        assert result == "2"

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nAvailable list: 2\n" in captured.out
        assert "\n  1: Option A\n" in captured.out
        assert "\n  2: Option B\n" in captured.out
        assert "\n  X: Exit / Cancel\n" in captured.out
        assert "\n[INPUT]: 2\n" in captured.out
        assert "\nSelected option: Option B\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out

