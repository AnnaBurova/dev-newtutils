"""
Created on 2024-06

@author: NewtCode Anna Burova

Functions:
    def format_value_to_str(
        value: object
        ) -> str
    def error_msg(
        *args: object,
        location: str = "Unknown",
        stop: bool = True
        ) -> None
"""

from __future__ import annotations

import sys

from colorama import Fore, Style

import newtutils._intern as INTERN


def format_value_to_str(
        value: object
        ) -> str:
    """ ## Convert a value to a formatted string representation.

    Recursively formats supported types into consistent string output.
    Sets and frozensets receive special handling:
    elements are sorted lexicographically, formatted recursively,
    and wrapped in curly braces with comma separation.

    Args:
        value (object):
            The value to convert to string.
            Can be any object type.
            Supported types are processed with special formatting;
            others fall back to standard `str()` conversion.

    Returns:
        out (str):
            String representation of the input value.
            Sets and frozensets are formatted as `{item1, item2, ...}`
            with items sorted and recursively formatted.<br>
            Other types use standard string conversion.

    Examples:
        ```
        >>> NewtCons.format_value_to_str({3, 1, 2})
        '{1, 2, 3}'
        ```
    """

    if (
        INTERN.is_supported_type(value)
        and isinstance(value, (set, frozenset))
    ):
        items = ", ".join(format_value_to_str(item) for item in sorted(value, key=str))
        return "{" + items + "}"

    return str(value)


def error_msg(
        *args: object,
        location: str = "Unknown",
        stop: bool = True
        ) -> None:
    """ ## Print error messages in red and optionally terminate the program.

    Displays one or more messages in bright red color using **Colorama**.
    It is intended for CLI tools and debugging utilities
    that require structured visual feedback in the console.

    Args:
        *args (object):
            One or more messages to print.
        location (str):
            Name of the function or module where the error occurred.<br>
            Defaults to "Unknown".
        stop (bool):
            If True, the program terminates with exit code 1 after printing.<br>
            Defaults to True.

    Raises:
        SystemExit:
            If `stop=True`.
            Terminates with code 1.

    Examples:
        ```
        NewtCons.error_msg(
            "Test error",
            location=f"{__file__} > {__name__}",
            stop=False
        )
        ```
    """

    message = "\n".join(format_value_to_str(arg) for arg in args)

    output = (
        f"{Style.BRIGHT}{Fore.RED}\n"
        f"Location: {location}\n"
        f"::: ERROR :::\n"
        f"{message}\n"
        f"{Style.RESET_ALL}"
    )
    print(output, file=sys.stderr)

    if stop:
        raise SystemExit(1)
