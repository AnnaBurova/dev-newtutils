"""
Created on 2025-10

@author: NewtCode Anna Burova

This module provides basic tests for the `utility` functions
from the `newtutils` package.

The tests cover:
1. validate_input with various inputs.
2. sorting_list with various inputs.
3. sorting_dict_by_keys with different key combinations.
"""

import newtutils.utility as NewtUtil
import newtutils.console as NewtCons


def test_validate_input() -> None:
    """
    Run a series of basic, interactive checks for the helper function `validate_input`.
    This function is written as a lightweight, printed-output test (not using assertions)
    and is intended to exercise common input-type validation scenarios.
    """

    print("Test 1: validate_input basic tests")

    # Test: correct type
    print("Input: 123, expected int")
    result = NewtUtil.validate_input(123, int)
    print("Output: ", result)
    print()

    # Test: incorrect type
    print("Input: 'hello', expected int")
    result = NewtUtil.validate_input("hello", int)
    print("Output: ", result)
    print()

    # Test: multiple allowed types
    print("Input: 3.14, expected (int, float)")
    result = NewtUtil.validate_input(3.14, (int, float))
    print("Output: ", result)
    print()

    # Test: invalid type again (should trigger error_msg)
    print("Input: [1,2,3], expected (dict, set)")
    result = NewtUtil.validate_input([1, 2, 3], (dict, set))
    print("Output: ", result)


def test_sorting_list() -> None:
    """
    Test sorting_list with different input types.
    """

    print("Test 2: sorting_list with different input types")

    numbers_input = [3, 1, 2, 3]
    numbers_output = NewtUtil.sorting_list(numbers_input)
    print("Numbers:")
    print(f"Input: {numbers_input}")
    print(f"Output: {numbers_output}")

    words_input = ["b", "a", "b"]
    words_output = NewtUtil.sorting_list(words_input)
    print("Words:")
    print(f"Input: {words_input}")
    print(f"Output: {words_output}")

    mixed_input = ["f", 4, "a", 2, "b", 1, "a"]
    mixed_output = NewtUtil.sorting_list(mixed_input)
    print("Mixed:")
    print(f"Input: {mixed_input}")
    print(f"Output: {mixed_output}")


def test_sorting_dict_by_keys() -> None:
    """
    Test sorting_dict_by_keys with different sorting key options.
    """

    print("Test 3: sorting_dict_by_keys with different sorting key options")

    data_dict = [
        {"name": "Bob"},
        {"name": "Alice", "age": 30},
        {"name": "Charlie", "age": 25},
        {"name": "Aska", "age": 25},
    ]

    for item in data_dict:
        print(item)

    print("\nExpected: same order as input (no sort keys provided)")
    dict_default = NewtUtil.sorting_dict_by_keys(data_dict)
    for item in dict_default:
        print(item)

    print("\nExpected: sorted by age ascending, missing values last")
    dict_age = NewtUtil.sorting_dict_by_keys(data_dict, "age")
    for item in dict_age:
        print(item)

    print("\nExpected: sorted alphabetically by name")
    dict_name = NewtUtil.sorting_dict_by_keys(data_dict, "name")
    for item in dict_name:
        print(item)

    print("\nExpected: sorted by age, and by name for equal ages")
    dict_age_name = NewtUtil.sorting_dict_by_keys(data_dict, "age", "name")
    for item in dict_age_name:
        print(item)

    print("\nExpected: reversed order of previous result")
    dict_reverse = NewtUtil.sorting_dict_by_keys(data_dict, "age", "name", reverse=True)
    for item in dict_reverse:
        print(item)

if __name__ == "__main__":
    """Run all tests in sequence."""
    NewtCons._divider()
    test_validate_input()
    NewtCons._divider()
    test_sorting_list()
    NewtCons._divider()
    test_sorting_dict_by_keys()
    NewtCons._divider()
