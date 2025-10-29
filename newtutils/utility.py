"""
Created on 2025-10

@author: NewtCode Anna Burova

Functions:
    def sorting_list(
        json_input: list,
        stop: bool = True
        ) -> list[str | int]
    def sorting_dict_by_keys(
        data: list[dict[str, object]],
        *keys: str,
        reverse: bool = False
        ) -> list[dict[str, object]]
"""

import newtutils.console as NewtCons


def sorting_list(
        json_input: list,
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
        json_input (list):
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

    if not NewtCons.validate_input(json_input, list, stop=stop):
        return []

    try:
        # Validate all elements
        if not all(isinstance(x, (str, int)) for x in json_input):
            NewtCons.error_msg(
                f"json_input must have only str and int types: {json_input}",
                location="Newt.utility.sorting_list",
                stop=stop
            )
            return []

        # Remove duplicates
        unique_values = set(json_input)

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
        data: list[dict[str, object]],
        *keys: str,
        reverse: bool = False
        ) -> list[dict[str, object]]:
    """
    Sort a list of dictionaries by one or more keys.

    Missing or None-valued keys are placed at the end of the result.

    Args:
        data (list[dict[str, object]]):
            The list of dictionaries to sort.
        *keys (str):
            One or more keys to sort by, in priority order.
        reverse (bool):
            If True, sort in descending order. Defaults to False.

    Returns:
        out (list[dict[str, object]]):
            A new list sorted by the specified keys,
            with entries missing those keys placed at the end.
    """

    if not NewtCons.validate_input(data, list):
        return []

    if not all(isinstance(d, dict) for d in data):
        NewtCons.error_msg(
            "Expected a list of dictionaries",
            data,
            location="Newt.utility.sorting_dict_by_keys"
        )
        return []

    if not all(isinstance(k, str) for k in keys):
        NewtCons.error_msg(
            "Keys must be strings",
            keys,
            location="Newt.utility.sorting_dict_by_keys"
        )
        return []

    try:
        def sort_key(d: dict[str, object]) -> tuple[object, ...]:
            """
            Generate a sorting key that moves missing values to the end.
            """
            return tuple((d.get(k) is None, d.get(k)) for k in keys)

        return sorted(data, key=sort_key, reverse=reverse)

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.utility.sorting_dict_by_keys",
            stop=False
        )
        return data
