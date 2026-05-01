"""
Updated on 2026-04
Created on 2026-02

@author: NewtCode Anna Burova

Functions:
    def print_my_func_name(
        ) -> None
    def print_my_captured(
        captured
        ) -> None
    def format_set_to_str(
        input_set: set
        ) -> str
"""

import inspect


def print_my_func_name(
        ) -> None:
    """ Print name of the current function. """

    frame = inspect.currentframe()

    if frame and frame.f_back:
        print("Function:", frame.f_back.f_code.co_name)
    else:
        print("Function: <unknown>")

    print("============================================")


def print_my_captured(
        captured
        ) -> None:
    """ ## Pretty-print captured standard output and error streams from pytest.

    Args:
        captured (CaptureResult):
            A pytest `CaptureResult` object returned by `capsys.readouterr()`.
            Must provide `.out` and `.err` attributes representing captured
            standard output and standard error text.
    """

    print()
    print("START=======================================")

    print("=====captured.out=====")
    if captured.out:
        print(captured.out)
    else:
        print("(no stdout captured)")

    print("=====captured.err=====")
    if captured.err:
        print(captured.err)
    else:
        print("(no stderr captured)")

    print("END=========================================")


def format_set_to_str(
        input_set: set
        ) -> str:
    """ ## Format a set into a sorted, human-readable string.

    Sorts elements by their string representation
    and wraps them in curly braces, similar to set literal syntax.

    Args:
        input_set (set):
            The set to format.<br>
            Elements can be of any type that supports str() conversion.

    Returns:
        out (str):
            A string of sorted elements wrapped in curly braces.<br>
            Example: `{1, 2, abc}` or `{}` for an empty set.
    """

    return "{" + ", ".join(str(x) for x in sorted(input_set, key=str)) + "}"
