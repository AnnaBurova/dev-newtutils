"""
Comprehensive unit tests for newtutils.network module.

Tests cover:
- URL data fetching (fetch_data_from_url)
- File downloading (download_file_from_url)
"""

import pytest
from unittest.mock import patch, Mock, MagicMock

import requests
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

    @patch('newtutils.network.requests.get')
    @patch('newtutils.console._retry_pause')
    def test_fetch_data_from_url_retry_on_fail(self, mock_retry, mock_get, capsys):
        """Test retry behavior on failure."""
        print_my_func_name("test_fetch_data_from_url_retry_on_fail")

        # First call fails, second succeeds
        mock_response_fail = Mock()
        mock_response_fail.status_code = 500
        mock_response_fail.url = "https://example.com"

        mock_response_success = Mock()
        mock_response_success.status_code = 200
        mock_response_success.text = "Success"
        mock_response_success.url = "https://example.com"

        mock_get.side_effect = [mock_response_fail, mock_response_success]

        result = NewtNet.fetch_data_from_url("https://example.com", repeat_on_fail=True)
        print("result:", result)
        # Should retry and eventually succeed
        assert result == "Success"
        assert mock_get.call_count == 2

        print("mock_retry:", mock_retry.call_count)
        assert mock_retry.call_count == 1

        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "Status: 500" in captured.out
        assert "Status: 200" in captured.out

    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_custom_timeout(self, mock_get, capsys):
        """Test fetch with custom timeout."""
        print_my_func_name("test_fetch_data_from_url_custom_timeout")

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Lorem ipsum dolor sit ame"
        mock_response.url = "https://example.com"
        mock_get.return_value = mock_response

        result = NewtNet.fetch_data_from_url("https://example.com", timeout=60, repeat_on_fail=False)
        print("result:", result)
        assert result == "Lorem ipsum dolor sit ame"

        call_kwargs = mock_get.call_args[1]
        print("call_kwargs:", call_kwargs)
        assert call_kwargs["timeout"] == 60

        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "Status: 200" in captured.out

    def test_fetch_data_from_url_invalid_input(self, capsys):
        """Test fetch with invalid input."""
        print_my_func_name("test_fetch_data_from_url_invalid_input")

        with pytest.raises(SystemExit):
            result = NewtNet.fetch_data_from_url(123, repeat_on_fail=False)  # type: ignore
            print("This line will not be printed:", result)

        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "::: ERROR :::" in captured.out
        assert "Expected <class 'str'>, got <class 'int'>" in captured.out
        assert "Value: 123" in captured.out

    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_mode_alert(self, mock_get, capsys):
        """Test fetch with alert mode."""
        print_my_func_name("test_fetch_data_from_url_mode_alert")

        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.url = "https://example.com"
        mock_get.return_value = mock_response

        with patch('newtutils.console._beep_boop') as mock_beep:
            result = NewtNet.fetch_data_from_url(
                "https://example.com",
                mode="alert",
                repeat_on_fail=False
            )
            print("result:", result)
            assert result is None
            # Should call beep on error
            print("mock_beep:", mock_beep.call_count)
            assert mock_beep.call_count == 1

        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "Status: 500" in captured.out
        assert "::: ERROR :::" in captured.out
        assert "HTTP 500 for" in captured.out


class TestDownloadFileFromUrl:
    """Tests for download_file_from_url function."""

    @patch('newtutils.network.requests.get')
    @patch('newtutils.files.save_text_to_file')
    def test_download_file_from_url_text(self, mock_save, mock_get, capsys):
        """Test downloading a text file."""
        print_my_func_name("test_download_file_from_url_text")

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "File content"
        mock_response.content = b"File content"
        mock_response.headers = {"Content-Type": "text/plain"}
        mock_get.return_value = mock_response

        result = NewtNet.download_file_from_url(
            "https://example.com/file.txt",
            "tmp_file.txt",
            repeat_on_fail=False
        )
        print("result:", result)
        assert result is True

        mock_save.assert_called_once()
        print("mock_save:", mock_save.call_count)
        assert mock_save.call_count == 1

        print("mock_get:", mock_get.call_count)
        assert mock_get.call_count == 1

        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "Downloading from: https://example.com/file.txt" in captured.out
        assert "Status: 200" in captured.out
        assert "Content-Type: text/plain" in captured.out
        assert "Saved to: tmp_file.txt" in captured.out

    @patch('newtutils.network.requests.get')
    @patch('builtins.open', create=True)
    def test_download_file_from_url_binary(self, mock_open, mock_get, capsys):
        """Test downloading a binary file."""
        print_my_func_name("test_download_file_from_url_binary")

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"Binary content"
        mock_response.headers = {"Content-Type": "application/octet-stream"}
        mock_get.return_value = mock_response

        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        result = NewtNet.download_file_from_url(
            "https://example.com/file.bin",
            "tmp_file.bin",
            repeat_on_fail=False
        )
        print("result:", result)
        assert result is True

        mock_file.write.assert_called_once_with(b"Binary content")

        print("mock_open:", mock_open.call_count)
        assert mock_open.call_count == 1

        print("mock_get:", mock_get.call_count)
        assert mock_get.call_count == 1

        captured = capsys.readouterr()
        print_my_captured(captured)
        assert "Downloading from: https://example.com/file.bin" in captured.out
        assert "Status: 200" in captured.out
        assert "Content-Type: application/octet-stream" in captured.out
        assert "Saved to: tmp_file.bin" in captured.out

    @patch('newtutils.network.requests.get')
    def test_download_file_from_url_status_404(self, mock_get, capsys):
        """Test download with 404 status."""
        print_my_func_name("test_download_file_from_url_status_404")

        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.url = "https://example.com/file.txt"
        mock_get.return_value = mock_response

        with patch('newtutils.console._beep_boop'):
            result = NewtNet.download_file_from_url(
                "https://example.com/file.txt",
                "tmp_file.txt",
                repeat_on_fail=False
            )
            print("result:", result)
            assert result is False

        print("mock_get:", mock_get.call_count)
        assert mock_get.call_count == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Downloading from: https://example.com/file.txt" in captured.out
        assert "Status: 404" in captured.out
        assert "::: ERROR :::" in captured.out
        assert "HTTP 404 while downloading" in captured.out
