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
    test_sorting_dict_by_keys()
    NewtCons._divider()

    print("Test passed")
