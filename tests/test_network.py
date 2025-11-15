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
        mock_response.text = "Lorem ipsum dolor sit ame"
        mock_response.url = "https://example.com"
        mock_get.return_value = mock_response

        result = NewtNet.fetch_data_from_url("https://example.com", repeat_on_fail=False)
        print("result:", result)
        assert result == "Lorem ipsum dolor sit ame"
        mock_get.assert_called_once()

        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "Status: 200" in captured.out

    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_with_params(self, mock_get, capsys):
        """Test fetch with query parameters."""
        print_my_func_name("test_fetch_data_from_url_with_params")

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Lorem ipsum dolor sit ame"
        mock_response.url = "https://example.com?key=value"
        mock_get.return_value = mock_response

        params = {"key": "value", "num": 123}
        result = NewtNet.fetch_data_from_url(
            "https://example.com",
            params=params,
            repeat_on_fail=False
        )
        print("result:", result)
        assert result == "Lorem ipsum dolor sit ame"

        # Check that params were converted to strings
        call_kwargs = mock_get.call_args[1]
        print("call_kwargs:", call_kwargs)
        assert "key" in call_kwargs["params"]
        assert call_kwargs["params"]["num"] == "123"

        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "Status: 200" in captured.out

    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_with_custom_headers(self, mock_get, capsys):
        """Test fetch with custom headers."""
        print_my_func_name("test_fetch_data_from_url_with_custom_headers")

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Lorem ipsum dolor sit ame"
        mock_response.url = "https://example.com"
        mock_get.return_value = mock_response

        custom_headers = {"Authorization": "Bearer token"}
        result = NewtNet.fetch_data_from_url(
            "https://example.com",
            headers=custom_headers,
            repeat_on_fail=False
        )
        print("result:", result)
        assert result == "Lorem ipsum dolor sit ame"

        call_kwargs = mock_get.call_args[1]
        print("call_kwargs:", call_kwargs)
        assert call_kwargs["headers"]["Authorization"] == "Bearer token"

        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "Status: 200" in captured.out
        assert "User-Agent" in captured.out

    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_status_206(self, mock_get, capsys):
        """Test fetch with status 206 (Partial Content)."""
        print_my_func_name("test_fetch_data_from_url_status_206")

        mock_response = Mock()
        mock_response.status_code = 206
        mock_response.text = "Partial Lorem ipsum dolor sit ame"
        mock_response.url = "https://example.com"
        mock_get.return_value = mock_response

        result = NewtNet.fetch_data_from_url("https://example.com", repeat_on_fail=False)
        print("result:", result)
        assert result == "Partial Lorem ipsum dolor sit ame"

        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "Status: 206" in captured.out

    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_status_404(self, mock_get, capsys):
        """Test fetch with 404 status."""
        print_my_func_name("test_fetch_data_from_url_status_404")

        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found Lorem ipsum dolor sit ame"
        mock_response.url = "https://example.com/notfound"
        mock_get.return_value = mock_response

        result = NewtNet.fetch_data_from_url("https://example.com/notfound", repeat_on_fail=False)
        print("result:", result)
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "Status: 404" in captured.out
        assert "::: ERROR :::" in captured.out
        assert "HTTP 404 for" in captured.out

    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_status_500(self, mock_get, capsys):
        """Test fetch with 500 status."""
        print_my_func_name("test_fetch_data_from_url_status_500")

        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Server Error Lorem ipsum dolor sit ame"
        mock_response.url = "https://example.com"
        mock_get.return_value = mock_response

        result = NewtNet.fetch_data_from_url("https://example.com", repeat_on_fail=False)
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "Status: 500" in captured.out
        assert "::: ERROR :::" in captured.out
        assert "HTTP 500 for" in captured.out

    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_timeout(self, mock_get, capsys):
        """Test fetch with timeout error."""
        print_my_func_name("test_fetch_data_from_url_timeout")

        mock_get.side_effect = requests.exceptions.ReadTimeout("Timeout")

        result = NewtNet.fetch_data_from_url("https://example.com", repeat_on_fail=False)
        print("result:", result)
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "::: ERROR :::" in captured.out
        assert "ReadTimeout: Timeout" in captured.out
        assert "Timeout (45s)" in captured.out
        assert "Request failed after" in captured.out

    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_request_exception(self, mock_get, capsys):
        """Test fetch with general request exception."""
        print_my_func_name("test_fetch_data_from_url_request_exception")

        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        result = NewtNet.fetch_data_from_url("https://example.com", repeat_on_fail=False)
        print("result:", result)
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "::: ERROR :::" in captured.out
        assert "Request failed after" in captured.out
        assert "RequestException: Connection error" in captured.out
