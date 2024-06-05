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
    def validate_value(
        value: object,
        expected_type: type | tuple[type, ...],
        check_non_empty: bool = False,
        location: str = "",
        stop: bool = True
        ) -> bool
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


def validate_value(
        value: object,
        expected_type: type | tuple[type, ...],
        check_non_empty: bool = False,
        location: str = "",
        stop: bool = True
        ) -> bool:
    """ ## Validate that a given value matches the expected types.

    Checks whether a value conforms to the expected type or tuple of allowed types.
    If `check_non_empty` is enabled, also
    validates that the value is not empty according to type-specific rules.
    Reports errors via `error_msg()` and can terminate execution if validation fails.

    Args:
        value (object):
            The value to validate.
        expected_type (type | tuple[type, ...]):
            The expected type or tuple of allowed types.<br>
            Type checking uses exact `type()` matches to avoid bool/int confusion.
        check_non_empty (bool):
            If True, also validate that the value is not empty.<br>
            Defaults to False.<br>
            Supported types:
            None, bool, str, int, float, tuple, list, dict, set, frozenset.
        location (str):
            Additional location context for error reporting.<br>
            Automatically prepended with function path.<br>
            Defaults to empty string.
        stop (bool):
            If True, stops execution after reporting the error.<br>
            If False, reports the error but continues execution.<br>
            Defaults to True.

    Returns:
        out (bool):
            True if the value matches the expected type
            and passes non-empty check (if enabled),<br>
            otherwise False.

    Raises:
        SystemExit:
            If an error occurs and `stop=True`.
            Terminates with code 1.

    Examples:
        ```
        result = NewtCons.validate_value(
            42,
            int | (str, int,),
            check_non_empty = True,
            location=f"{__file__} > {__name__}",
            stop = False
        )
        ```
    """

    if location:
        location = str(location) + " > "
    location += "Newt.console.validate_value"

    value_content = format_value_to_str(value)

    # Normalize to tuple for uniform check
    expected = expected_type if isinstance(expected_type, tuple) else (expected_type,)

    if type(value) not in expected:
        error_msg(
            f"Value: {value_content}",
            f"Received type: {type(value)}",
            f"Expected type: {expected_type}",
            location=location + " : type(value) is not expected_type",
            stop=stop
        )

        return False

    is_empty = False
    if check_non_empty:

        # Use exact type checks instead of isinstance() to avoid bool being treated as int.
        # bool is a subclass of int, so isinstance(True, int) is True.

        if (
            value is None
            and expected_type is type(None)
        ):
            is_empty = True

        elif (
            type(value) is bool
            and bool in expected
        ):
            is_empty = value is False

        elif (
            type(value) is str
            and str in expected
        ):
            is_empty = value.strip() == ""

        elif (
            type(value) is int
            and int in expected
        ):
            is_empty = value == 0

        elif (
            type(value) is float
            and float in expected
        ):
            is_empty = value == 0.0

        elif (
            INTERN.is_supported_type(value)
            and type(value) is tuple
            and tuple in expected
        ):
            is_empty = len(value) == 0

        elif (
            INTERN.is_supported_type(value)
            and type(value) is list
            and list in expected
        ):
            is_empty = len(value) == 0

        elif (
            INTERN.is_supported_type(value)
            and type(value) is dict
            and dict in expected
        ):
            is_empty = len(value) == 0

        elif (
            INTERN.is_supported_type(value)
            and type(value) is set
            and set in expected
        ):
            is_empty = len(value) == 0

        elif (
            INTERN.is_supported_type(value)
            and type(value) is frozenset
            and frozenset in expected
        ):
            is_empty = len(value) == 0

        else:
            error_msg(
                "This type is not supported.",
                f"Value: {value_content}",
                f"Type: {type(value)}",
                location=location + " : check_non_empty",
                stop=stop
            )

            return False

    if is_empty:
        error_msg(
            "Value must not be empty",
            f"Value: {value_content}",
            f"Type: {type(value)}",
            location=location + " : is_empty",
            stop=stop
        )

        return False

    return True
