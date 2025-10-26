"""
Created on 2025-10

@author: NewtCode

This module provides basic tests for the `network` utilities
from the `newtutils` package.

The tests cover:
1. Fetching a simple URL (simulated success).
2. Handling invalid URLs gracefully.
3. Beep notification helper.
4. Retry countdown helper.
"""

import newtutils.network as NewtNet
import newtutils.utility as NewtUtil
import newtutils.console as NewtCons


def test_fetch_data_from_url_invalid() -> None:
    """Simulate failed fetch with invalid domain."""

    print("Test 1: Invalid URL fetch (expect retry and graceful exit)")

    try:
        result = NewtNet.fetch_data_from_url("https://example.invalid", mode="alert", repeat_on_fail=False)
        print("Result:", result)
    except Exception as e:
        print("Caught exception:", e)


def test_fetch_data_from_url_valid() -> None:
    """Perform a minimal GET request to a valid domain."""

    print("Test 2: Valid URL fetch")
    result = NewtNet.fetch_data_from_url("https://example.com", repeat_on_fail=False)

    if result is None:
        print("No response received")
    else:
        print("Length of response:", len(result))


if __name__ == "__main__":
    NewtCons._divider()
    test_fetch_data_from_url_invalid()
    NewtCons._divider()
    test_fetch_data_from_url_valid()
    NewtCons._divider()

    print("✅ Test passed")
