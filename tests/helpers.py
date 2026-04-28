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
