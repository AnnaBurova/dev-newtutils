"""
Updated on 2026-02
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
    def select_from_input(
        select_dict: dict[str, str]
        ) -> str | None
"""

from __future__ import annotations

import os
import time

from colorama import Fore, Style

try:
    import winsound
except ImportError:  # pragma: no cover (Unix-only)
    winsound = None


def _divider(
        ) -> None:
    """ Print a visual divider between console sections.

    Displays a horizontal line to visually separate blocks of console output.
    Primarily used for readability in testing and debugging logs.
    """

    print("\n" + "-" * 50 + "\n")


def error_msg(
        *args: object,
        location: str = "Unknown",
        stop: bool = True
        ) -> None:
    """ Print error messages in red and optionally terminate the program.

    Displays one or more messages in bright red color using Colorama.
    It is intended for CLI tools and debugging utilities
    that require structured visual feedback in the console.
    The `location` parameter identifies where the error originated.

    Args:
        *args (object):
            One or more messages or objects to print.
        location (str):
            Name of the function or module where the error occurred.
            Defaults to "Unknown".
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
        stop: bool = True,
        location: str = ""
        ) -> bool:
    """ Validate that a given value matches the expected type.

    If the value does not match the expected type,
    logs an error message using `error_msg()`.
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
        location (str):
            Additional location context for error reporting.
            Defaults to empty string.

    Returns:
        out (bool):
            True if the value matches the expected type,
            otherwise False.

    Raises:
        SystemExit:
            Raised when `stop=True` and the value type is invalid.
    """

    if location:
        location = " > "+location

    if not isinstance(value, expected_type):
        error_msg(
            f"Expected {expected_type}, got {type(value)}",
            f"Value: {value}",
            location="Newt.console.validate_input"+location,
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

    if not validate_input(
        pause_s, (int, float), stop=False,
        location="_beep_boop : pause_s not int or float"
    ):
        pause_s = 0.2

    if pause_s < 0:
        error_msg(
            f"Invalid pause duration: {pause_s}",
            location="Newt.console._beep_boop : pause_s less then 0",
            stop=False
        )
        pause_s = 0.2

    try:
        winsound.Beep(1200, 500)
        time.sleep(pause_s)
        winsound.Beep(800, 500)
        time.sleep(1)

    except Exception as e:
        error_msg(
            f"Exception: {e}",
            location="Newt.console._beep_boop : Exception on Beep",
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
            Minimal 1.
            Defaults to 5.
        beep (bool):
            If True, plays a "beep-boop" notification before the countdown.
            Defaults to True.

    Raises:
        SystemExit:
            Raised if interrupted by user (Ctrl+C).
    """

    if not validate_input(
        seconds, int, stop=False,
        location="_retry_pause : seconds"
    ):
        seconds = 5

    if seconds < 1:
        error_msg(
            f"Invalid pause duration: {seconds}",
            location="Newt.console._retry_pause : seconds less then 1",
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

    validate_input(
        dir_, str,
        location="check_location : dir_"
    )
    validate_input(
        must_location, str,
        location="check_location : must_location"
    )

    if dir_ == must_location:
        print("=== START ===")
        return

    error_msg(
        f"Location is wrong, check folder: {dir_}",
        location="Newt.console.check_location"
    )


def select_from_input(
        select_dict: dict[str, str]
        ) -> str | None:
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

    Example:
        >>> options = {"1": "Option A", "2": "Option B"}
        >>> select_from_input(options)
        Available list: 2
            1: Option A
            2: Option B
            X: Exit / Cancel
        Enter number from list ([X] to exit): 1
        [INPUT]: 1
        Selected option: Option A
        returns '1'
    """

    validate_input(
        select_dict, dict,
        location="select_from_input : select_dict"
    )

    # Display numbered list
    print("Available list:", len(select_dict))
    for nr, name in select_dict.items():
        print(f"{nr:>6}: {name}")
    print("     X: Exit / Cancel")

    choice = "x"

    # Loop until valid input
    while choice not in select_dict:
        try:
            choice = input(
                "\nEnter number from list ([X] to exit): "
            ).strip().lower()
            print(f"[INPUT]: {choice}")

            if choice == "x":
                error_msg(
                    "Selection cancelled.",
                    location="Newt.console.select_from_input : choice = [X]"
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
            error_msg(
                "Selection cancelled.",
                location="Newt.console.select_from_input : KeyboardInterrupt"
            )

        except Exception as e:
            error_msg(
                f"Exception: {e}",
                location="Newt.console.select_from_input : Exception"
            )
