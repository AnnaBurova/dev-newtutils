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
        pause_s: float = 0.2
        ) -> None
    def _retry_pause(
        seconds: int = 5,
        beep: bool = True
        ) -> None
    def check_location(
        dir_: str,
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
except ImportError:
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
            Raised when `stop=True` and the value type is invalid.
    """

    if location:
        location = str(location) + " > "

    value_content = value

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
        elif type(value) is bool and expected_type is bool:
            is_empty = value is False
        elif type(value) is int and expected_type is int:
            is_empty = value == 0
        elif type(value) is float and expected_type is float:
            is_empty = value == 0.0
        elif type(value) is str and expected_type is str:
            is_empty = value.strip() == ""
        elif type(value) is bytes and expected_type is bytes:
            is_empty = len(value) == 0
        elif type(value) is list and expected_type is list:
            is_empty = len(value) == 0
        elif type(value) is tuple and expected_type is tuple:
            is_empty = len(value) == 0
        elif type(value) is dict and expected_type is dict:
            is_empty = len(value) == 0
        elif type(value) is set and expected_type is set:
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
        pause_s: float = 0.2
        ) -> None:
    """ Play a short "beep-boop" notification sound on Windows systems.

    Produces two tones using the built-in `winsound` module:
    a higher-pitched "beep" followed by a lower "boop".
    Used for alerts or indicating that user attention is required.

    Args:
        pause_s (float):
            Delay between tones in seconds.
            Defaults to 0.2.
    """

    # Cross-platform safe beep
    if os.name != "nt" or winsound is None:
        return

    if not validate_type(
        pause_s, (int, float), stop=False,
        location="_beep_boop : pause_s"
    ):
        pause_s = 0.2

    if pause_s < 0:
        error_msg(
            f"Invalid pause duration: {pause_s}",
            location="Newt.console._beep_boop : pause_s < 0",
            stop=False
        )
        pause_s = 0.2

    try:
        winsound.Beep(1200, 500)
        time.sleep(pause_s)
        winsound.Beep(800, 500)
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        error_msg(
            f"Exception: {e} (found? write test!)",  # TODO
            location="Newt.console._beep_boop : Exception",
            stop=False
        )


def _retry_pause(
        seconds: int = 5,
        beep: bool = True
        ) -> None:
    """ Display a countdown and pause before retrying an operation.

    Used primarily by network-related functions
    to wait between retry attempts after a failed request.
    Optionally plays a short sound notification using `_beep_boop()`.

    Args:
        seconds (int):
            Total wait time in seconds.
            Must be at least 1.
            Defaults to 5.
        beep (bool):
            If True, plays a "beep-boop" notification before the countdown.
            Defaults to True.

    Raises:
        SystemExit:
            Raised if interrupted by user (Ctrl+C).
    """

    if not validate_type(
        seconds, int, check_non_empty=True, stop=False,
        location="_retry_pause : seconds"
    ):
        seconds = 5

    if seconds < 1:
        error_msg(
            f"Invalid pause duration: {seconds}",
            location="Newt.console._retry_pause : seconds < 1",
            stop=False
        )
        seconds = 5

    if beep:
        _beep_boop()

    print(f"Retrying in {seconds} seconds...")

    try:
        for i in range(seconds, 0, -1):
            print(f"Time left: {i}s")
            time.sleep(1)

    except KeyboardInterrupt:
        error_msg(
            "Retry interrupted by user (Ctrl+C)",
            location="Newt.console._retry_pause : KeyboardInterrupt"
        )


def check_location(
        dir_: str,
        must_location: str
        ) -> None:
    """ Check if the current directory matches the required location.

    Prints a start message if directories match,
    otherwise logs an error and stops execution.

    Args:
        dir_ (str):
            The current directory path to check.
        must_location (str):
            The required directory path.

    Raises:
        SystemExit:
            Raised if directories do not match.
    """

    validate_type(
        dir_, str, check_non_empty=True,
        location="check_location : dir_"
    )

    validate_type(
        must_location, str, check_non_empty=True,
        location="check_location : must_location"
    )

    if dir_ == must_location:
        print("=== START ===")
        return

    error_msg(
        f"Current position is wrong, check folder: {dir_}",
        location="Newt.console.check_location : no return"
    )
