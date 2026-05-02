"""
Updated on 2026-05
Created on 2025-10

@author: NewtCode Anna Burova

Functions:
    def sorting_sequence(
        input_sequence: Sequence,
        stop: bool = True
        ) -> list
            def _is_valid_seq_value(
                seq_value
                ) -> bool
    def check_dict_keys(
        data_dict: Mapping[str, object],
        expected_set: set[str],
        location: str = "",
        stop: bool = True
        ) -> bool
    def count_similar_values(
        sequence_list: Sequence[tuple[Any, ...]],
        position: int = 0
        ) -> dict[Any, int]
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


def sorting_sequence(
        input_sequence: Sequence,
        stop: bool = True
        ) -> list:
    """ ## Remove duplicates from a Sequence and return a sorted result as list.

    Accepts a sequence, removes duplicate entries, and returns all unique
    items sorted in the following order:
    1. Strings — sorted alphabetically.
    2. Integers and floats — sorted numerically.
    3. Everything else (None, bool, etc.) — sorted by str().
    4. Tuples — recursively processed and returned as tuples, sorted by str().

    Supported element types (at any tuple nesting depth):<br>
    `None bool int float str tuple`<br>
    Any other type triggers an error.

    Args:
        input_sequence (Sequence):
            The input sequence to process.<br>
            Must be a non-empty list or tuple.
        stop (bool):
            If True, raises SystemExit when invalid data is detected.<br>
            If False, logs the error and returns an empty list.<br>
            Defaults to True.

    Returns:
        out (list):
            Unique elements from the input sequence, grouped and sorted:<br>
            strings > numbers > other types > tuples.

    Raises:
        SystemExit:
            Raised when `stop=True` and the input contains invalid data types.
    """

    if not NewtCons.validate_type(
        input_sequence, (list, tuple), check_non_empty=True, stop=stop,
        location="Newt.utility.sorting_sequence : input_sequence"
    ):
        return []

    # --------------------------------------------------------------------------
    def _is_valid_seq_value(
            seq_value
            ) -> bool:
        """ Recursively check if value is safe to add to a set. """

        if isinstance(seq_value, tuple):
            return all(_is_valid_seq_value(sv) for sv in seq_value)

        # Validate all sub elements, else set() will not work correctly
        seq_types = (type(None), bool, int, float, str)
        if NewtCons.validate_type(
            seq_value, seq_types, stop=False,
            location="Newt.utility.sorting_sequence.is_valid_seq_value"
        ):
            return True

        return False
    # --------------------------------------------------------------------------

    if not all(_is_valid_seq_value(isv) for isv in input_sequence):
        NewtCons.error_msg(
            "input_sequence must have only special types",
            f"input_sequence: {input_sequence}",
            location="Newt.utility.sorting_sequence : input_sequence not all",
            stop=stop
        )
        return []

    # set() thinks 1 and True are same, and saves first value it founds
    etc_val_list = [x for x in input_sequence if type(x) is bool]
    non_bool = [x for x in input_sequence if type(x) is not bool]
    # Remove duplicates
    unique_values_set = set(non_bool)

    str_val_list, int_val_list, tup_val_list = [], [], []

    # Separate by type and sort
    for uvs in unique_values_set:
        if type(uvs) is str:
            str_val_list.append(uvs)
        elif type(uvs) in (int, float):
            int_val_list.append(int(uvs) if uvs == int(uvs) else uvs)
        elif isinstance(uvs, (tuple)):
            tup_val_list.append(tuple(sorting_sequence(uvs, stop=stop)))
        else:
            etc_val_list.append(uvs)

    str_val_list.sort()
    int_val_list.sort()
    etc_val_list = list(set(etc_val_list))
    etc_val_list.sort(key=str)
    tup_val_list.sort(key=str)

    # Strings first, then integers
    return str_val_list + int_val_list + etc_val_list + tup_val_list


def check_dict_keys(
        data_dict: Mapping[str, object],
        expected_set: set[str],
        location: str = "",
        stop: bool = True
        ) -> bool:
    """ ## Validate that a mapping contains exactly the expected keys.

    Checks for missing and unexpected keys in the provided mapping.
    Useful for validating JSON responses where key structure may change unexpectedly.

    Args:
        data_dict (Mapping[str, object]):
            Read-only mapping to validate (e.g. dict, defaultdict).<br>
            Keys must be strings, values can be of any type.
        expected_set (set[str]):
            Set of keys that must be present in the mapping.<br>
            Example:
            {"id", "name", "value"}
        location (str):
            Additional context appended to the error message location.<br>
            Default is empty string.
        stop (bool):
            If True, stops execution on validation failure.<br>
            Default is True.

    Returns:
        out (bool):
            True if the mapping contains exactly the expected keys,<br>
            False if any keys are missing or unexpected keys are present.

    Raises:
        SystemExit:
            Raised if `stop=True`, terminating the program with exit code 1.
    """

    if location:
        location = str(location) + " > "

    data_keys = set(data_dict.keys())
    expected_keys = set(expected_set)
    missing_keys = expected_keys - data_keys
    extra_keys = data_keys - expected_keys

    if missing_keys or extra_keys:
        NewtCons.error_msg(
            f"Data keys: {', '.join(sorted(data_keys))}",
            f"Missing keys: {', '.join(sorted(missing_keys))}",
            f"Unexpected keys: {', '.join(sorted(extra_keys))}",
            location=location + "Newt.utility.check_dict_keys",
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
