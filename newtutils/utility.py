"""
Updated on 2026-02
Created on 2025-10

@author: NewtCode Anna Burova

Functions:
    def sorting_list(
        input_list: list,
        stop: bool = True
        ) -> list[str | int]
    def sorting_dict_by_keys(
        data: Sequence[Mapping[str, object]],
        *keys: str,
        reverse: bool = False
        ) -> list[dict[str, object]]
    def check_dict_keys(
        data: dict,
        expected: set[str],
        stop: bool = True
        ) -> bool
"""

from __future__ import annotations

from collections.abc import Sequence, Mapping
import newtutils.console as NewtCons


def sorting_list(
        input_list: list,
        stop: bool = True
        ) -> list[str | int]:
    """
    Remove duplicates from a list and return a sorted result.

    The function accepts a list containing only strings and integers,
    removes duplicate entries, and returns all unique items in ascending order:
    1. Strings (sorted alphabetically)
    2. Integers (sorted numerically)

    If the list contains elements of other types,
    an error message is logged using `NewtCons.error_msg()`.
    The function stops execution if `stop=True`.

    Args:
        input_list (list):
            The input list to process.
            Must contain only `str` or `int` values.
        stop (bool):
            If True, stops execution when invalid data is detected.
            If False, logs the error and returns an empty list.
            Defaults to True.

    Returns:
        out (list[str | int]):
            Unique elements from the input list,
            sorted alphabetically (strings) and numerically (integers).

    Raises:
        SystemExit:
            Raised when `stop=True` and the input contains invalid data types.
    """

    if not NewtCons.validate_input(
        input_list, list, stop=stop,
        location="Newt.utility.sorting_list.input_list"
    ):
        return []

    try:
        # Validate all elements
        if not all(NewtCons.validate_input(
            x, (str, int), stop=False
        ) for x in input_list):
            NewtCons.error_msg(
                "input_list must have only str and int types",
                f"input_list: {input_list}",
                location="Newt.utility.sorting_list.input_list",
                stop=stop
            )
            return []

        # Remove duplicates
        unique_values = set(input_list)

        # Separate by type and sort
        str_values = sorted([x for x in unique_values if isinstance(x, str)])
        int_values = sorted([x for x in unique_values if isinstance(x, int)])

        # Strings first, then integers
        return str_values + int_values

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.utility.sorting_list",
            stop=stop
        )
        return []


def sorting_dict_by_keys(
        data: Sequence[Mapping[str, object]],
        *keys: str,
        reverse: bool = False
        ) -> list[dict[str, object]]:
    """
    Sort a sequence of mappings (dictionaries) by one or more keys.

    This function validates the input sequence and its elements,
    ensuring each entry is a mapping with string keys.
    It supports sorting by multiple keys in priority order.
    Missing or None-valued keys are placed at the end of the sorted list.

    Args:
        data (Sequence[Mapping[str, object]]):
            Sequence of mapping-like objects to sort.
        *keys (str):
            One or more keys to sort by, in priority order.
        reverse (bool):
            If True, sorts in descending order.
            Defaults to False.

    Returns:
        out (list[dict[str, object]]):
            A new list of dictionaries sorted by the specified keys.
            Items with missing or None-valued keys are placed at the end.

    Raises:
        SystemExit:
            Raised when validation fails and `NewtCons.error_msg()` is called
            with `stop=True` (if configured that way).
    """

    if not data:
        return []

    # Validate that data is a list
    if not NewtCons.validate_input(
        data, list,
        location="Newt.utility.sorting_dict_by_keys.data"
    ):
        return []

    # Validate that each element is a dictionary
    if not all(isinstance(d, dict) for d in data):
        NewtCons.error_msg(
            "Expected a list of dictionaries",
            f"Data: {data}",
            location="Newt.utility.sorting_dict_by_keys"
        )
        return []

    # If no keys provided — return the data as a list (no sorting)
    if not keys:
        return [dict(d) for d in data]

    # Validate that all keys are strings
    if not all(isinstance(k, str) for k in keys):
        NewtCons.error_msg(
            "Keys must be strings",
            f"Keys: {keys}",
            location="Newt.utility.sorting_dict_by_keys"
        )
        return []

    try:
        def sort_key(d: Mapping[str, object]) -> tuple[object, ...]:
            """
            Generate a sorting key that moves missing or None values to the end.
            """
            return tuple((d.get(k) is None, d.get(k)) for k in keys)

        # sorted() always returns a new list
        return [dict(d) for d in sorted(data, key=sort_key, reverse=reverse)]

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.utility.sorting_dict_by_keys",
            stop=False
        )
        return [dict(d) for d in data]


def check_dict_keys(
        data: dict,
        expected: set[str],
        stop: bool = True
        ) -> bool:
    """
    Validate that a dictionary contains the expected keys.

    Args:
        data (dict):
            Dictionary to validate.
        expected (set[str]):
            Set of keys that must be present in the dictionary.

    Returns:
        bool:
            True if all expected keys are present and no extra keys exist,
            False otherwise.
            Default True.

    Example:
        >>> sample = {"a": 1, "b": 2}
        >>> check_dict_keys(sample, {"a", "b"})
        True
        >>> check_dict_keys(sample, {"a", "b", "c"})
        False
    """

    data_keys = set(data.keys())
    expected_keys = set(expected)
    missing_keys = expected_keys - data_keys
    extra_keys = data_keys - expected_keys

    if missing_keys or extra_keys:
        NewtCons.error_msg(
            f"Data keys: {', '.join(sorted(data_keys))}",
            f"Missing keys: {', '.join(sorted(missing_keys))}",
            f"Unexpected keys: {', '.join(sorted(extra_keys))}",
            location="mwparser.check_dict_keys",
            stop=stop
        )
        return False
    return True
