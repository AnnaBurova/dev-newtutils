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
    """Print a visual divider between tests."""

    print("\n" + "-" * 50 + "\n")


def error_msg(
        *args: object,
        location: str = "Unknown",
        stop: bool = True
        ) -> None:
    """
    Print error messages in red to the console and optionally stop the program.

    This function displays one or more messages in bright red color using Colorama.
    It is designed for CLI tools, scripts, and any console-based feedback system.
    The `location` argument helps identify where the error originated.

    Args:
        *args (object):
            One or more messages or objects to print.
        location (str, optional):
            Name of the function or module where the error occurred.
            Defaults to "Unknown".
            Example: "Newt.files.read_csv_from_file"
        stop (bool, optional):
            If True, the program terminates with exit code 1 after printing.
            Defaults to True.

    Returns:
        None

    Raises:
        SystemExit:
            Raised if stop=True,
            terminating the program with exit code 1.
    """

    message = "\n".join(str(arg) for arg in args)

    print(Style.BRIGHT, Fore.RED)
    print("Location:", location)
    print("::: ERROR :::")
    print(message)
    print(Style.RESET_ALL)

    if stop:
        raise SystemExit(1)
