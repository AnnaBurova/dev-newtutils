"""
Created on 2025-10

@author: NewtCode Anna Burova

Functions:
    def validate_input(
        value: object,
        expected_type: type | tuple[type, ...],
        location: str
        ) -> bool
    def sorting_list(
        json_input: list
        ) -> list[int | str]
    def sorting_dict_by_keys(
        data: list[dict[str, object]],
        *keys: str,
        reverse: bool = False
        ) -> list[dict[str, object]]
"""

import newtutils.console as NewtCons


def validate_input(
        value: object,
        expected_type: type | tuple[type, ...],
        location: str
        ) -> bool:
    """
    Validate that a given value matches the expected type.

    If validation fails, an error message is printed using Newt.error_msg()
    but the program continues to run.

    Args:
        value (object):
            The input value to validate.
        expected_type (type | tuple[type, ...]):
            The expected data type or tuple of types.
        location (str):
            The name of the function performing validation.

    Returns:
        bool:
            True if the value matches the expected type, otherwise False.
    """

    if not isinstance(value, expected_type):
        NewtCons.error_msg(
            f"Expected {expected_type}, got {type(value)}",
            location=location,
            stop=False
        )
        return False
    return True


def sorting_list(
        json_input: list
        ) -> list[int | str]:
    """
    Remove duplicates from a list and return a sorted result.

    This function accepts a list of comparable values, removes any
    duplicate entries, and returns a new list sorted in ascending order.
    Strings are listed first, followed by integers.

    Args:
        json_input (list[object]):
            A list of items that support comparison.

    Returns:
        list[int | str]:
            A new list containing unique items from `json_input`,
            sorted alphabetically (strings) and numerically (integers).
    """

    if not validate_input(json_input, list, "Newt.utility.sorting_list"):
        return []

    try:
        # Remove duplicates
        unique_values = set(json_input)

        # Separate by type for deterministic ordering
        str_values = sorted(x for x in unique_values if isinstance(x, str))
        int_values = sorted(x for x in unique_values if isinstance(x, int))

        # Combine strings first, then integers
        json_output = str_values + int_values

        return json_output

    except Exception as e_:
        NewtCons.error_msg(f"sorting_list: Unexpected error: {e_}", stop=False)
        return []


def sorting_dict_by_keys(
        data: list[dict[str, object]],
        *keys: str,
        reverse: bool = False
        ) -> list[dict[str, object]]:
    """
    Sort a list of dictionaries by one or more keys.

    Dictionaries missing a sorting key are placed at the end.

    Args:
        data (list[dict[str, object]]):
            The list of dictionaries to sort.
        *keys (str):
            One or more dictionary keys to sort by, in priority order.
        reverse (bool, optional):
            If True, sort in descending order. Defaults to False.

    Returns:
        list[dict[str, object]]:
            A new list sorted by the specified keys,
            with dictionaries missing a key placed at the end.
    """

    if not validate_input(data, list, "Newt.utility.sorting_dict_by_keys"):
        return []

    if not all(isinstance(d, dict) for d in data):
        NewtCons.error_msg("sorting_dict_by_keys: Expected a list of dicts", stop=False)
        return []

    if not all(isinstance(k, str) for k in keys):
        NewtCons.error_msg("sorting_dict_by_keys: Keys must be strings", stop=False)
        return data

    try:
        def sort_key(d: dict[str, object]) -> tuple[object, ...]:
            """
            Generate a sorting key that places missing values (None) at the end.
            """
            return tuple((d.get(k) is None, d.get(k)) for k in keys)

        return sorted(data, key=sort_key, reverse=reverse)

    except Exception as e:
        NewtCons.error_msg(f"sorting_dict_by_keys: Unexpected error: {e}", stop=False)
        return data
