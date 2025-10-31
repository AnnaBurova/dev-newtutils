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


def test_error_with_stop() -> None:
    """
    Test error message with stop=True (should raise SystemExit).
    """

    print("Test 3: error_msg with stop=True default (should raise SystemExit)")

    try:
        NewtCons.error_msg("This error will stop the program")  # Expected to exit
        print("This line will not be printed")

    except SystemExit as e:
        print(f"Caught SystemExit with code: {e}")

    except Exception as e:
        print(f"Caught other exception: {e}")

    finally:
        print("Program continues after catching SystemExit")


if __name__ == "__main__":
    """Run all tests in sequence."""
    NewtCons._divider()
    test_multiline_error_without_stop()
    NewtCons._divider()
    test_error_with_stop()
    NewtCons._divider()

    print("Test passed")
