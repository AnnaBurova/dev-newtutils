"""
Created on 2025-10

@author: NewtCode Anna Burova

This module provides basic tests for the `error_msg` function
from the `newtutils` package.

The tests cover:
2. Multi-line error without stopping the program.
3. Error with `stop=True` that triggers SystemExit.
"""

import newtutils.console as NewtCons


def test_multiline_error_without_stop() -> None:
    """
    Test multi-line error message without stopping the program.
    """

    print("Test 2: multiline error_msg without stop")
    NewtCons.error_msg(
        "This is a test error message",
        "This is a test error message",
        "This is a test error message",
        location=__file__,
        stop=False,
    )
    print("This line will be printed")


if __name__ == "__main__":
    """Run all tests in sequence."""
    NewtCons._divider()
    test_multiline_error_without_stop()
    NewtCons._divider()

    print("Test passed")
