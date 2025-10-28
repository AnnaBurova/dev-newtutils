"""
Created on 2025-10

@author: NewtCode Anna Burova

Functions:
    def _divider(
        ) -> None
    def error_msg(
        *args: object,
        location: str = "Unknown",
        stop: bool = True
        ) -> None
    def validate_input(
        value: object,
        expected_type: type | tuple[type, ...],
        stop: bool = True
        ) -> bool
    def _beep_boop(
        pause_s: float = 0.2
        ) -> None
"""

import os
import time
from colorama import Fore, Style

try:
    import winsound
except ImportError:
    winsound = None


def _divider(
        ) -> None:
    """
    Print a visual divider between console sections.

    This helper function displays a horizontal line to visually separate blocks of console output.
    Primarily used for readability in testing and debugging logs.
    """

    print("\n" + "-" * 50 + "\n")


def error_msg(
        *args: object,
        location: str = "Unknown",
        stop: bool = True
        ) -> None:
    """
    Print error messages in red and optionally terminate the program.

    This function displays one or more messages in bright red color using Colorama.
    It is intended for CLI tools and debugging utilities
    that require structured visual feedback in the console.
    The `location` parameter identifies where the error originated.

    Args:
        *args (object):
            One or more messages or objects to print.
        location (str):
            Name of the function or module where the error occurred.
            Defaults to "Unknown".
            Example:
            Newt.console.error_msg
        stop (bool):
            If True, the program terminates with exit code 1 after printing.
            Defaults to True.

    Raises:
        SystemExit:
            Raised if `stop=True`, terminating the program with exit code 1.
    """

    message = "\n".join(str(arg) for arg in args)

    print(Style.BRIGHT, Fore.RED)
    print("Location:", location)
    print("::: ERROR :::")
    print(message)
    print(Style.RESET_ALL)

    if stop:
        raise SystemExit(1)


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
            True if the value matches the expected type,
            otherwise False.

    Raises:
        SystemExit:
            Raised when `stop=True` and the value type is invalid.
    """

    if not isinstance(value, expected_type):
        error_msg(
            f"Expected {expected_type}, got {type(value)}",
            location="Newt.console.validate_input",
            stop=stop
        )
        return False

    return True


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
            Delay between tones in seconds.
            Defaults to 0.2.
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
        error_msg(
            f"Exception: {e}",
            location="Newt.console._beep_boop",
            stop=False
        )
