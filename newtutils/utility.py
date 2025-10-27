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
        expected_type: type | tuple[type, ...]
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
        expected_type: type | tuple[type, ...]
        ) -> bool:
    """
    Validate that a given value matches the expected type.

    If validation fails, an error message is printed using NewtCons.error_msg()
    but the program continues to run.

    Args:
        value (object):
            The input value to validate.
        expected_type (type | tuple[type, ...]):
            The expected data type or tuple of types.

    Returns:
        bool:
            True if the value matches the expected type, otherwise False.
    """

    if not isinstance(value, expected_type):
        NewtCons.error_msg(
            f"Expected {expected_type}, got {type(value)}",
            location="Newt.utility.validate_input",
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

    if not validate_input(json_input, list):
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

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.utility.sorting_list",
            stop=False
            )
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

    if not validate_input(data, list):
        return []

    if not all(isinstance(d, dict) for d in data):
        NewtCons.error_msg(
            "Expected a list of dicts",
            location="Newt.utility.sorting_dict_by_keys",
            stop=False
            )
        return []

    if not all(isinstance(k, str) for k in keys):
        NewtCons.error_msg(
            "Keys must be strings",
            location="Newt.utility.sorting_dict_by_keys",
            stop=False
            )
        return data

    try:
        def sort_key(d: dict[str, object]) -> tuple[object, ...]:
            """
            Generate a sorting key that places missing values (None) at the end.
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
