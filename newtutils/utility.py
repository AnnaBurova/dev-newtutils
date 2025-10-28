"""
Created on 2025-10

@author: NewtCode Anna Burova

Functions:
    def _beep_boop(
        pause_s: float = 0.2
        ) -> None
    def _retry_pause(
        seconds: int = 5,
        beep: bool = False
        ) -> None
    def validate_input(
        value: object,
        expected_type: type | tuple[type, ...],
        stop: bool = True
        ) -> bool
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

import os
import time

try:
    import winsound
except ImportError:
    winsound = None

import newtutils.console as NewtCons


def _beep_boop(
        pause_s: float = 0.2
        ) -> None:
    """
    Play a short "beep-boop" notification sound on Windows systems.

    Produces two tones using the built-in `winsound` module:
    a higher-pitched "beep" followed by a lower "boop".
    Used for alerts or indicating that user attention is required.

    Args:
        pause_s (float):
            Delay between tones in seconds. Defaults to 0.2.
    """

    # Cross-platform safe beep.
    if os.name != "nt" or winsound is None:
        return

    try:
        winsound.Beep(1200, 500)
        time.sleep(pause_s)
        winsound.Beep(800, 500)
        time.sleep(1)

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.utility._beep_boop",
            stop=False
        )


def _retry_pause(
        seconds: int = 5,
        beep: bool = False
        ) -> None:
    """
    Display a countdown and pause before retrying an operation.

    Used primarily by network-related functions
    to wait between retry attempts after a failed request.
    Optionally plays a short sound notification using `_beep_boop()`.

    Args:
        seconds (int):
            Total wait time in seconds. Defaults to 5.
        beep (bool):
            If True, plays a "beep-boop" notification before the countdown.
            Defaults to False.
    """

    if not isinstance(seconds, int) or seconds <= 0:
        NewtCons.error_msg(
            f"Invalid pause duration: {seconds}",
            location="Newt.utility._retry_pause"
        )
        return

    if beep:
        _beep_boop()

    print(f"Retrying in {seconds} seconds...")

    try:
        for i in range(seconds, 0, -1):
            print(f"Time left: {i}s")
            time.sleep(1)
    except KeyboardInterrupt:
        NewtCons.error_msg(
            "Retry interrupted by user (Ctrl+C)",
            location="Newt.utility._retry_pause"
        )


def validate_input(
        value: object,
        expected_type: type | tuple[type, ...],
        stop: bool = True
        ) -> bool:
    """
    Validate that a given value matches the expected type.

    If the value does not match the expected type,
    logs an error message using `NewtCons.error_msg()`.
    The function can optionally stop execution depending on the `stop` flag.

    Args:
        value (object):
            The value to validate.
        expected_type (type | tuple[type, ...]):
            The expected type or tuple of allowed types.
        stop (bool):
            If True, stops execution after logging the error.
            If False, logs the error but continues execution.
            Defaults to True.

    Returns:
        out (bool):
            True if the value matches the expected type, otherwise False.

    Raises:
        SystemExit:
            Raised when `stop=True` and the value type is invalid.
    """

    if not isinstance(value, expected_type):
        NewtCons.error_msg(
            f"Expected {expected_type}, got {type(value)}",
            location="Newt.utility.validate_input",
            stop=stop
        )
        return False

    return True


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

    if not validate_input(json_input, list, stop=stop):
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

    if not validate_input(data, list):
        return []

    if not all(isinstance(d, dict) for d in data):
        NewtCons.error_msg(
            "Expected a list of dictionaries",
            location="Newt.utility.sorting_dict_by_keys"
        )
        return []

    if not all(isinstance(k, str) for k in keys):
        NewtCons.error_msg(
            "Keys must be strings",
            location="Newt.utility.sorting_dict_by_keys"
        )
        return data

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
