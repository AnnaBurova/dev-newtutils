"""
Updated on 2026-02
Created on 2025-10

@author: NewtCode Anna Burova

Functions:
    def check_dict_keys(
        data: Mapping[str, object],
        expected: set[str],
        stop: bool = True,
        location: str = ""
        ) -> bool
    def count_similar_values(
        sequence_list: Sequence[tuple[Any, ...]],
        position: int = 0
        ) -> dict[Any, int]
    def sorting_list(
        input_list: Sequence[str | int],
        stop: bool = True
        ) -> list[str | int]
    def sorting_dict_by_keys(
        data: Sequence[Mapping[str, Any]],
        *keys: str,
        reverse: bool = False,
        stop: bool = True
        ) -> list[Mapping[str, Any]]
            def sort_key(
                d: Mapping[str, object]
                ) -> tuple[object, ...]
    def select_from_input(
        select_dict: dict[str, str],
        missing_values: dict[str, int] | None = None
        ) -> str
"""

from __future__ import annotations

from collections.abc import Sequence, Mapping
from typing import Any

import newtutils.console as NewtCons


def check_dict_keys(
        data: Mapping[str, object],
        expected: set[str],
        stop: bool = True,
        location: str = ""
        ) -> bool:
    """ Validate that a mapping contains the expected keys.

    Args:
        data (Mapping[str, object]):
            Mapping to validate.
        expected (set[str]):
            Set of keys that must be present in the mapping.
        stop (bool):
            If True, stops execution on validation failure.
            Defaults to True.
        location (str):
            Additional location context for error reporting.
            Defaults to empty string.

    Returns:
        out (bool):
            True if all expected keys are present and no extra keys exist,
            False otherwise.
    """

    if location:
        location = " > " + location

    data_keys = set(data.keys())
    expected_keys = set(expected)
    missing_keys = expected_keys - data_keys
    extra_keys = data_keys - expected_keys

    if missing_keys or extra_keys:
        NewtCons.error_msg(
            f"Data keys: {', '.join(sorted(data_keys))}",
            f"Missing keys: {', '.join(sorted(missing_keys))}",
            f"Unexpected keys: {', '.join(sorted(extra_keys))}",
            location="Newt.utility.check_dict_keys : missing_keys or extra_keys" + location,
            stop=stop
        )
        return False

    return True


def count_similar_values(
        sequence_list: Sequence[tuple[Any, ...]],
        position: int = 0
        ) -> dict[Any, int]:
    """ Count occurrences of values at a specified position in a sequence of tuples.
    Args:
        sequence_list (Sequence[tuple[Any, ...]]):
            A sequence of tuples to analyze.
        position (int):
            The index position within each tuple to check for similar values.
            Defaults to 0 (the first element).
    Returns:
        out (dict[Any, int]):
            A dictionary mapping each unique value found at the specified position
            to the count of its occurrences.
    """

    # Important to not call error message for empty list, just return empty dict
    if not sequence_list:
        return {}

    if not NewtCons.validate_type(
        sequence_list, list, check_non_empty=True, stop=False,
        location="Newt.utility.count_similar_values : sequence_list"
    ):
        return {}

    NewtCons.validate_type(
        position, int,
        location="Newt.utility.count_similar_values : position"
    )

    if not all(
        NewtCons.validate_type(
            item, tuple, stop=False
        ) and len(item) > position for item in sequence_list
    ):
        NewtCons.error_msg(
            f"All items must be sequences with at least {position + 1} elements",
            f"sequence_list: {sequence_list}",
            location="Newt.utility.count_similar_values : sequence_list not all",
            stop=True
        )
        return {}

    first_values = [item[position] for item in sequence_list]
    count_values = {value: first_values.count(value) for value in set(first_values)}
    # print("Count of similar values:", count_values)
    return count_values


def sorting_list(
        input_list: Sequence[str | int],
        stop: bool = True
        ) -> list[str | int]:
    """ Remove duplicates from a list and return a sorted result.

    The function accepts a sequence containing only strings and integers,
    removes duplicate entries, and returns all unique items in ascending order:
    1. Strings (sorted alphabetically)
    2. Integers (sorted numerically)

    If the sequence contains elements of other types,
    an error message is logged using `NewtCons.error_msg()`.
    The function stops execution if `stop=True`.

    Args:
        input_list (Sequence[str | int]):
            The input sequence to process.
            Must contain only `str` or `int` values.
        stop (bool):
            If True, stops execution when invalid data is detected.
            If False, logs the error and returns an empty list.
            Defaults to True.

    Returns:
        out (list[str | int]):
            Unique elements from the input sequence,
            sorted alphabetically (strings) and numerically (integers).

    Raises:
        SystemExit:
            Raised when `stop=True` and the input contains invalid data types.
    """

    if not NewtCons.validate_type(
        input_list, (list, tuple), check_non_empty=True, stop=stop,
        location="Newt.utility.sorting_list : input_list"
    ):
        return []

    try:
        # Validate all elements
        if not all(
            NewtCons.validate_type(
                x, (str, int), stop=False
            ) for x in input_list
        ):
            NewtCons.error_msg(
                "input_list must have only str and int types",
                f"input_list: {input_list}",
                location="Newt.utility.sorting_list : input_list not all",
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

    except Exception as e:  # pragma: no cover
        NewtCons.error_msg(
            f"Exception: {e} (found? write test!)",  # TODO
            location="Newt.utility.sorting_list : Exception",
            stop=stop
        )
        return []


def sorting_dict_by_keys(
        data: Sequence[Mapping[str, Any]],
        *keys: str,
        reverse: bool = False,
        stop: bool = True
        ) -> list[Mapping[str, Any]]:
    """ Sort a sequence of mappings (dictionaries) by one or more keys.

    This function validates the input sequence and its elements,
    ensuring each entry is a mapping with string keys.
    It supports sorting by multiple keys in priority order.
    Missing or None-valued keys are placed at the end of the sorted list.

    Args:
        data (Sequence[Mapping[str, Any]]):
            Sequence of mapping-like objects to sort.
        *keys (str):
            One or more keys to sort by, in priority order.
        reverse (bool):
            If True, sorts in descending order.
            Defaults to False.
        stop (bool):
            If True, stops execution when invalid data is detected.
            If False, logs the error and returns an empty list.
            Defaults to True.

    Returns:
        out (list[Mapping[str, Any]]):
            A new list of mappings sorted by the specified keys.
            Items with missing or None-valued keys are placed at the end.

    Raises:
        SystemExit:
            Raised when validation fails and `NewtCons.error_msg()` is called
            with `stop=True` (if configured that way).
    """

    # Validate that data is a sequence
    if not NewtCons.validate_type(
        data, (list, tuple), check_non_empty=True, stop=stop,
        location="Newt.utility.sorting_dict_by_keys : data"
    ):
        return []

    # Validate that each element is a dictionary
    if not all(
        NewtCons.validate_type(
            d, dict, stop=False
        ) for d in data
    ):
        NewtCons.error_msg(
            "Expected a list of dictionaries",
            f"Data: {data}",
            location="Newt.utility.sorting_dict_by_keys : data not all",
            stop=stop
        )
        return []

    # If no keys provided — return the data as a list (no sorting)
    if not keys:
        all_have_single_key = all(len(d) == 1 for d in data) and len(set(next(iter(d)) for d in data if d)) == 1
        if all_have_single_key:
            single_key = next(iter(data[0]))
            return sorted(data, key=lambda x: x[single_key], reverse=reverse)

        return [dict(d) for d in data]

    # Validate that all keys are strings
    if not all(
        NewtCons.validate_type(
            k, str, stop=False
        ) for k in keys
    ):
        NewtCons.error_msg(
            "Keys must be strings",
            f"Keys: {keys}",
            location="Newt.utility.sorting_dict_by_keys : keys not all",
            stop=stop
        )
        return []

    try:
        def sort_key(
                d: Mapping[str, object]
                ) -> tuple[object, ...]:
            """
            Generate a sorting key that moves missing or None values to the end.
            """
            return tuple((d.get(k) is None, d.get(k)) for k in keys)

        # sorted() always returns a new list
        return [dict(d) for d in sorted(data, key=sort_key, reverse=reverse)]

    except Exception as e:  # pragma: no cover
        NewtCons.error_msg(
            f"Exception: {e} (found? write test!)",  # TODO
            location="Newt.utility.sorting_dict_by_keys : Exception",
            stop=stop
        )
        return [dict(d) for d in data]


def select_from_input(
        select_dict: dict[str, str],
        missing_values: dict[str, int] | None = None
        ) -> str:
    """ Display a numbered list of options and prompt user to select one.

    Loops until a valid choice is made or user cancels with 'x'.

    Args:
        select_dict (dict[str, str]):
            Dictionary mapping string keys (numbers) to option names.

    Returns:
        out (str):
            The selected key if valid choice made.

    Raises:
        SystemExit:
            Raised if selection cancelled (user enters 'x' or presses Ctrl+C).
    """

    NewtCons.validate_type(
        select_dict, dict, check_non_empty=True,
        location="Newt.utility.select_from_input : select_dict"
    )

    # Display numbered list
    print("Available list:", len(select_dict))
    max_key_len = len(max(select_dict.keys(), key=len)) + 2
    for nr, name in select_dict.items():
        if missing_values and name in missing_values:
            name += f" ({missing_values[name]})"
        print(f"{nr:>{max_key_len}}: {name}")
    print(f"{'X':>{max_key_len}}: Exit / Cancel")

    choice = "x"

    attempt = 0
    # Loop until valid input
    while choice not in select_dict:
        if attempt > 5:
            break
        attempt += 1

        try:
            choice = input(
                "\nEnter number from list ([X] to exit): "
            ).strip().lower()
            print(f"[INPUT]: {choice}")

            if choice == "x":
                NewtCons.error_msg(
                    "Selection cancelled.",
                    location="Newt.utility.select_from_input : choice = [X]"
                )

            if not choice.isdigit():
                print("Invalid input. Please enter a number.")
                continue

            if choice in select_dict:
                print(f"Selected option: {select_dict[choice]}")
                print()
                return choice

            print("Number out of range. Try again.")

        except KeyboardInterrupt:
            NewtCons.error_msg(
                "Selection cancelled.",
                location="Newt.utility.select_from_input : KeyboardInterrupt"
            )

        except Exception as e:  # pragma: no cover
            NewtCons.error_msg(
                f"Exception: {e} (found? write test!)",  # TODO
                location="Newt.utility.select_from_input : Exception"
            )

    NewtCons.error_msg(
        f"No correct selection after {attempt} attempt.",
        location="Newt.utility.select_from_input : while attempt"
    )
    return choice
