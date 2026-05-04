"""
Updated on 2026-05
Created on 2025-10

@author: NewtCode Anna Burova

Functions:
    def sorting_sequence(
        data_sequence: Sequence,
        stop: bool = True
        ) -> list
            def _is_valid_seq_value(
                seq_value
                ) -> bool
    def check_dict_keys(
        data_mapping: Mapping[str, object],
        expected_set: set[str],
        location: str = "",
        stop: bool = True
        ) -> bool
    def count_values_by_position(
        data_sequence: Sequence[Sequence],
        position: int = 0,
        stop: bool = False
        ) -> dict[Any, int]
    def sorting_dict_by_keys(
        data_list: list[dict[str, Any]],
        *sorting_keys: str,
        reverse: bool = False,
        stop: bool = True
        ) -> list[dict[str, Any]]
            def sort_key(
                element: dict[str, Any] | None
                ) -> list[tuple[int, Any]]
    def select_from_input(
        select_dict: dict[str, str],
        missing_values: dict[str, int] | None = None
        ) -> str
"""

from __future__ import annotations

from typing import Any
from collections import Counter
from collections.abc import Mapping, Sequence

import newtutils.console as NewtCons


def sorting_sequence(
        data_sequence: Sequence,
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
        data_sequence (Sequence):
            The data sequence to process.<br>
            Must be a non-empty list or tuple.
        stop (bool):
            If True, raises SystemExit when invalid data is detected.<br>
            If False, logs the error and returns an empty list.<br>
            Defaults to True.

    Returns:
        out (list):
            Unique elements from the data sequence, grouped and sorted:<br>
            strings > numbers > other types > tuples.

    Raises:
        SystemExit:
            If an error occurs and `stop=True`, terminates with exit code 1.
    """

    if not NewtCons.validate_type(
        data_sequence, (list, tuple), check_non_empty=True, stop=stop,
        location="Newt.utility.sorting_sequence : data_sequence"
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

    if not all(_is_valid_seq_value(isv) for isv in data_sequence):
        NewtCons.error_msg(
            "data_sequence must have only special types",
            f"data_sequence: {data_sequence}",
            location="Newt.utility.sorting_sequence : data_sequence not all",
            stop=stop
        )
        return []

    # set() thinks 1 and True are same, and saves first value it founds
    etc_val_list = [x for x in data_sequence if type(x) is bool]
    non_bool = [x for x in data_sequence if type(x) is not bool]
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
        data_mapping: Mapping[str, object],
        expected_set: set[str],
        location: str = "",
        stop: bool = True
        ) -> bool:
    """ ## Validate that a mapping contains exactly the expected keys.

    Checks for missing and unexpected keys in the provided mapping.
    Useful for validating JSON responses where key structure may change unexpectedly.

    Args:
        data_mapping (Mapping[str, object]):
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
            If an error occurs and `stop=True`, terminates with exit code 1.
    """

    if location:
        location = str(location) + " > "

    data_keys = set(data_mapping.keys())
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


def count_values_by_position(
        data_sequence: Sequence[Sequence],
        position: int = 0,
        stop: bool = False
        ) -> dict[Any, int]:
    """ ## Count occurrences of values at a specified position in a sequence of sequences.

    Args:
        data_sequence (Sequence[Sequence]):
            A sequence of sequences to analyze.
        position (int):
            The index position within each inner sequence to count values at.<br>
            Defaults to 0 (the first element).
        stop (bool):
            If True, stops execution on any error or validation failure.<br>
            Default is False.

    Returns:
        out (dict[Any, int]):
            A dictionary mapping each unique value found<br>
            at the specified position to the count of its occurrences.

    Raises:
        SystemExit:
            If an error occurs and `stop=True`, terminates with exit code 1.
    """

    # Empty sequence is valid data — return empty dict without error
    if not data_sequence:
        return {}

    if not NewtCons.validate_type(
        data_sequence, (list, tuple), check_non_empty=True, stop=stop,
        location="Newt.utility.count_values_by_position : data_sequence"
    ):
        return {}

    if not NewtCons.validate_type(
        position, int, stop=stop,
        location="Newt.utility.count_values_by_position : position"
    ):
        position = 0

    seq_len = len(data_sequence[0])
    seq_type = type(data_sequence[0])

    if seq_len <= position:
        NewtCons.error_msg(
            f"Position {position} out of range",
            location="Newt.utility.count_values_by_position : seq_len <= position",
            stop=stop
        )
        return {}

    for item in data_sequence:
        if not NewtCons.validate_type(
            item, seq_type, stop=stop,
            location="Newt.utility.count_values_by_position : seq_type"
        ):
            return {}

        if seq_len != len(item):
            NewtCons.error_msg(
                f"All items must have the same length {seq_len}",
                location="Newt.utility.count_values_by_position : seq_len",
                stop=stop
            )
            return {}

    return dict(Counter(item[position] for item in data_sequence))


def sorting_dict_by_keys(
        data_list: list[dict[str, Any]],
        *sorting_keys: str,
        reverse: bool = False,
        stop: bool = True
        ) -> list[dict[str, Any]]:
    """ ## Sort a list of dictionaries by one or more keys.

    Validates the input list and its elements,
    ensuring each entry is a dictionary or None.
    Supports sorting by multiple keys in priority order.

    Values are sorted in the following type order (ascending):
    1. Strings — sorted alphabetically, case-insensitive.
    2. Integers and floats — sorted numerically.
    3. Booleans — sorted after numbers (False < True).
    4. None value — key exists but value is None, placed before missing keys.
    5. Missing key — key does not exist in the dict.
    6. Empty dict — placed at the very end.
    7. None — placed at the very end.

    Args:
        data_list (list[dict[str, Any]]):
            List of dictionaries to sort.
            May contain None values or empty dicts.
        *sorting_keys (str):
            One or more dictionary keys to sort by, in priority order.<br>
            If omitted and every element is a single-key dict sharing the same key,
            that key is used automatically.<br>
            Otherwise, the original order is preserved.
        reverse (bool):
            If True, sorts in descending order.<br>
            Defaults to False.
        stop (bool):
            If True, raises SystemExit on invalid input.<br>
            If False, logs the error and returns an empty list.<br>
            Defaults to True.

    Returns:
        out (list[dict[str, Any]]):
            A new sorted list.<br>
            The original list is not modified.

    Raises:
        SystemExit:
            If an error occurs and `stop=True`, terminates with exit code 1.
    """

    # Empty list is valid data — return empty list without error
    if not data_list:
        return []

    # Validate that data_list is a list
    if not NewtCons.validate_type(
        data_list, list, check_non_empty=True, stop=stop,
        location="Newt.utility.sorting_dict_by_keys : data_list"
    ):
        return []

    invalid_element_type = False
    invalid_key_type = False

    # Validate that each element is a dictionary and has key type str or int
    for dl in data_list:
        if not NewtCons.validate_type(
            dl, (dict, type(None)), stop=False,
            location="Newt.utility.sorting_dict_by_keys : dl in data_list"
        ):
            invalid_element_type = True

        if dl and isinstance(dl, dict):
            for k in dl.keys():
                if not NewtCons.validate_type(
                    k, str, stop=False,
                    location="Newt.utility.sorting_dict_by_keys : k in dl.keys()"
                ):
                    invalid_key_type = True
                    break

    if invalid_element_type:
        NewtCons.error_msg(
            "Expected a list of dictionaries",
            f"data_list: {data_list}",
            location="Newt.utility.sorting_dict_by_keys : invalid_element_type",
            stop=stop
        )
        return []

    if invalid_key_type:
        NewtCons.error_msg(
            "Expected a keys of dictionaries to be str",
            f"data_list: {data_list}",
            location="Newt.utility.sorting_dict_by_keys : invalid_key_type",
            stop=stop
        )
        return []

    # Validate that each sorting key is a string or int
    if not all(NewtCons.validate_type(
        k, str, stop=False,
        location="Newt.utility.sorting_dict_by_keys : k in sorting_keys"
    ) for k in sorting_keys):
        NewtCons.error_msg(
            "Expected sorting keys to be str",
            f"sorting_keys: {sorting_keys}",
            location="Newt.utility.sorting_dict_by_keys : sorting_keys",
            stop=stop
        )
        return []

    # If no sorting keys are provided, attempt to auto-detect a single shared key.
    # Condition: every element in the list must be a non-empty dict with exactly one key,
    # and that key must be the same across all elements.
    # If the condition is not met, sorting_keys remains empty and no sorting is applied.
    if not sorting_keys:
        valid_keys = [dl for dl in data_list if dl and len(dl) == 1]
        if len(valid_keys) == len(data_list):  # all elements must pass
            common_keys = set.intersection(*[set(vk.keys()) for vk in valid_keys])
            if len(common_keys) == 1:
                sorting_keys = tuple(common_keys)

    if not sorting_keys:
        return data_list[::-1] if reverse else data_list[:]

    # --------------------------------------------------------------------------
    def sort_key(
            element: dict[str, Any] | None
            ) -> list[tuple[int, Any]]:
        """ Build a comparable sort key list from a dict item. """

        if element is None:  # None
            return [(7, None)]

        if not element:  # {}
            return [(6, element)]

        key_result = []
        for k in sorting_keys:
            val = element.get(k)

            if val is None and k in element:
                key_result.append((4, val))  # value None
            elif val is None:
                key_result.append((5, val))  # missing key
            elif type(val) is bool:
                key_result.append((2, val))
            elif type(val) in (int, float):
                key_result.append((1, val))
            elif type(val) is str:
                key_result.append((0, val.strip().lower()))  # normalize type to lowercase
            else:
                key_result.append((3, type(val).__name__+str(val)))  # group by type name, avoid TypeError

        return key_result
    # --------------------------------------------------------------------------

    sorted_list = sorted(data_list, key=sort_key, reverse=reverse)
    return sorted_list


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
