"""
Created on 2024-06

@author: NewtCode Anna Burova

Functions:
    def error_msg(
        *args: str,
        location: str = "Unknown",
        stop: bool = True
        ) -> None
"""

from __future__ import annotations

import sys

from colorama import Fore, Style


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
            Defaults to "Unknown".<br>
            Code:
            location=f"{__file__} > {__name__}"
        stop (bool):
            If True, the program terminates with exit code 1 after printing.<br>
            Defaults to True.

    Raises:
        SystemExit:
            If `stop=True`.
            Always exits with code 1.
    """

    message = "\n".join(str(arg) for arg in args)

    output = (
        f"\n{Style.BRIGHT}{Fore.RED}"
        f"Location: {location}\n"
        f"::: ERROR :::\n"
        f"{message}\n"
        f"{Style.RESET_ALL}"
    )
    print(output, file=sys.stderr)

    if stop:
        raise SystemExit(1)
