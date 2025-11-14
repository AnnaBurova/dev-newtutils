"""
Comprehensive unit tests for newtutils.network module.

Tests cover:
- URL data fetching (fetch_data_from_url)
"""

from unittest.mock import patch, Mock

import newtutils.network as NewtNet


def print_my_func_name(func_name):
    """
    Print the provided function name in a structured format.

    Args:
        func_name (str):
            Name of the function to display.
    """

    print("Function:", func_name)
    print("--------------------------------------------")


def print_my_captured(captured):
    """
    Pretty-print captured standard output and error streams from pytest.

    Args:
        captured:
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


class TestFetchDataFromUrl:
    """Tests for fetch_data_from_url function."""

    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_success(self, mock_get, capsys):
        """Test successful data fetch."""
        print_my_func_name("test_fetch_data_from_url_success")

        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Test response data"
        mock_response.url = "https://example.com"
        mock_get.return_value = mock_response

        result = NewtNet.fetch_data_from_url("https://example.com", repeat_on_fail=False)
        print("result:", result)
        assert result == "Test response data"
        mock_get.assert_called_once()

        captured = capsys.readouterr()
        print_my_captured(captured)
