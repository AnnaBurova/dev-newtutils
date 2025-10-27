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
"""

from colorama import Fore, Style


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
                Newt.files.read_csv_from_file
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
