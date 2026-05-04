"""
Updated on 2026-04
Created on 2025-10

@author: NewtCode Anna Burova

Functions:
    def _divider(
        ) -> None
    def error_msg(
        *args: str,
        location: str = "Unknown",
        stop: bool = True
        ) -> None
    def validate_type(
        value: object,
        expected_type: type | tuple[type, ...],
        check_non_empty: bool = False,
        stop: bool = True,
        location: str = ""
        ) -> bool
    def _beep_boop(
        ) -> None
    def _retry_pause(
        seconds: int = 5,
        beep: bool = True
        ) -> None
    def check_location(
        dir_global: str,
        must_location: str
        ) -> None
"""

from __future__ import annotations

import sys
import os
import time

from colorama import Fore, Style

try:
    import winsound
except ImportError:  # pragma: no cover (not Windows)
    print()
    print("Hint: import winsound only works on Windows.")
    print("Function _beep_boop will make no sound.")
    print("Expected platform: win32 / Got:", sys.platform)
    print("Expected OS name:  nt    / Got:", os.name)
    print()
    winsound = None


def _divider(
        ) -> None:
    """ ## Print a visual divider between console sections.

    Displays a horizontal line to visually separate blocks of console output.
    Primarily used for readability in testing and debugging logs.
    """

    print("\n" + "-" * 50 + "\n")


def error_msg(
        *args: str,
        location: str = "Unknown",
        stop: bool = True
        ) -> None:
    """ ## Print error messages in red and optionally terminate the program.

    Displays one or more messages in bright red color using **Colorama**.
    It is intended for CLI tools and debugging utilities
    that require structured visual feedback in the console.

    Args:
        *args (str):
            One or more messages to print.
        location (str):
            Name of the function or module where the error occurred.<br>
            Defaults to "Unknown".
        stop (bool):
            If True, the program terminates with exit code 1 after printing.<br>
            Defaults to True.

    Raises:
        SystemExit:
            Raised if `stop=True`, terminating the program with exit code 1.
    """

    message = "\n".join(str(arg) for arg in args)

    print(Style.BRIGHT + Fore.RED, file=sys.stderr)
    print(f"Location: {location}", file=sys.stderr)
    print("::: ERROR :::", file=sys.stderr)
    print(message, file=sys.stderr)
    print(Style.RESET_ALL, file=sys.stderr)

    if stop:
        raise SystemExit(1)


def validate_type(
        value: object,
        expected_type: type | tuple[type, ...],
        check_non_empty: bool = False,
        stop: bool = True,
        location: str = ""
        ) -> bool:
    """ ## Validate that a given value matches the expected type.

    If the value does not match the expected type,
    logs an error message using `error_msg()`.

    Args:
        value (object):
            The value to validate.
        expected_type (type | tuple[type, ...]):
            The expected type or tuple of allowed types.
        check_non_empty (bool):
            If True, also validate that the value is not empty.<br>
            Works for str, list, tuple, dict, set and None.<br>
            Defaults to False.
        stop (bool):
            If True, stops execution after logging the error.<br>
            If False, logs the error but continues execution.<br>
            Defaults to True.
        location (str):
            Additional location context for error reporting.<br>
            Defaults to empty string.

    Returns:
        out (bool):
            True if the value matches the expected type,<br>
            otherwise False.

    Raises:
        SystemExit:
            If an error occurs and `stop=True`, terminates with exit code 1.
    """

    if location:
        location = str(location) + " > "

    value_content = value

    # Normalize to tuple for uniform check
    expected = expected_type if isinstance(expected_type, tuple) else (expected_type,)

    if type(value) is set:
        value_content = "{" + ", ".join(str(x) for x in sorted(value, key=str)) + "}"

    if not isinstance(value, expected_type):
        error_msg(
            f"Value: {value_content}",
            f"Received type: {type(value)}",
            f"Expected type: {expected_type}",
            location=location + "Newt.console.validate_type",
            stop=stop
        )
        return False

    if check_non_empty:
        is_empty = False

        if value is None and expected_type is type(None):
            is_empty = True
        elif type(value) is bool and bool in expected:
            is_empty = value is False
        elif type(value) is int and int in expected:
            is_empty = value == 0
        elif type(value) is float and float in expected:
            is_empty = value == 0.0
        elif type(value) is str and str in expected:
            is_empty = value.strip() == ""
        elif type(value) is bytes and bytes in expected:
            is_empty = len(value) == 0
        elif type(value) is list and list in expected:
            is_empty = len(value) == 0
        elif type(value) is tuple and tuple in expected:
            is_empty = len(value) == 0
        elif type(value) is dict and dict in expected:
            is_empty = len(value) == 0
        elif type(value) is set and set in expected:
            is_empty = len(value) == 0
        else:
            error_msg(
                "check_non_empty is not supported for this type",
                f"Value: {value_content}",
                f"Type: {type(value)}",
                location=location + "Newt.console.validate_type : check_non_empty",
                stop=stop
            )
            return False

        if is_empty:
            error_msg(
                "Value must not be empty",
                f"Value: {value_content}",
                f"Type: {type(value)}",
                location=location + "Newt.console.validate_type : is_empty",
                stop=stop
            )
            return False

    return True


def _beep_boop(
        ) -> None:
    """ ## Play a short "beep-boop" notification sound on Windows systems.

    Produces two tones using the built-in `winsound` module:
    a higher-pitched "beep" followed by a lower "boop".
    Used for alerts or indicating that user attention is required.
    """

    # Cross-platform safe beep
    if winsound is None:  # pragma: no cover (not Windows)
        print(Style.BRIGHT + Fore.GREEN)
        print("Beep Boop !!!")
        print(Style.RESET_ALL)
        time.sleep(2)
        return None

    winsound.Beep(1200, 500)
    time.sleep(0.2)
    winsound.Beep(800, 500)
    time.sleep(1)


def _retry_pause(
        seconds: int = 5,
        beep: bool = True
        ) -> None:
    """ ## Display a countdown and pause before retrying an operation.

    Used primarily by network-related functions
    to wait between retry attempts after a failed request.
    Optionally plays a short sound notification using `_beep_boop()`.

    Args:
        seconds (int):
            Total wait time in seconds.<br>
            Must be at least 1.<br>
            Defaults to 5.
        beep (bool):
            If True, plays a "beep-boop" notification before the countdown.<br>
            Defaults to True.

    Raises:
        SystemExit:
            If an error occurs and `stop=True`, terminates with exit code 1. If `KeyboardInterrupt` by user (Ctrl+C) occurs, always terminates with exit code 1.
    """

    if not validate_type(
        seconds, int, check_non_empty=True, stop=False,
        location="Newt.console.retry_pause : seconds int"
    ):
        seconds = 5

    if seconds < 1:
        error_msg(
            f"Invalid pause duration: {seconds}",
            location="Newt.console.retry_pause : seconds < 1",
            stop=False
        )
        seconds = 5

    print(f"Retrying in {seconds} seconds...")

    if beep:
        _beep_boop()

    try:
        for i in range(seconds, 0, -1):
            print(f"Time left: {i}s")
            time.sleep(1)

    except KeyboardInterrupt:
        error_msg(
            "Retry interrupted by user (Ctrl+C)",
            location="Newt.console.retry_pause : KeyboardInterrupt"
        )


def check_location(
        dir_global: str,
        must_location: str
        ) -> None:
    """ ## Check if the current directory matches the required location.

    Prints a start message if directories match,
    otherwise logs an error and stops execution.

    Args:
        dir_global (str):
            The current directory path to check.
        must_location (str):
            The required directory path.

    Raises:
        SystemExit:
            If directories do not match, terminates with exit code 1.
    """

    validate_type(
        dir_global, str, check_non_empty=True,
        location="Newt.console.check_location : dir_global"
    )

    validate_type(
        must_location, str, check_non_empty=True,
        location="Newt.console.check_location : must_location"
    )

    if dir_global == must_location:
        print("=== START ===")
        return None

    error_msg(
        f"Current position is wrong, check folder: {dir_global}",
        location="Newt.console.check_location : error_msg"
    )
