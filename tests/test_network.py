"""
Updated on 2026-02
Created on 2025-11

@author: NewtCode Anna Burova

Comprehensive unit tests for newtutils.network module.

Tests cover:
- TestFetchDataFromUrl
- TestDownloadFileFromUrl
"""

import pytest
from unittest.mock import patch, Mock, MagicMock

import requests

from helpers import print_my_func_name, print_my_captured
import newtutils.network as NewtNet


class TestFetchDataFromUrl:
    """ Tests for fetch_data_from_url function. """


    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_success(self, mock_get, capsys):
        """ Test successful data fetch. """
        print_my_func_name()

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

        assert "\nFull URL: https://example.com\n" in captured.out
        assert "\nStatus: 200\n" in captured.out
        assert "\nResponse time: 0.000 seconds\n" in captured.out
        assert "\nresult: Lorem ipsum dolor sit ame\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_with_params(self, mock_get, capsys):
        """ Test fetch with query parameters. """
        print_my_func_name()

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

        assert "\nFull URL: https://example.com?key=value\n" in captured.out
        assert "\nStatus: 200\n" in captured.out
        assert "\nResponse time: 0.000 seconds\n" in captured.out
        assert "\nresult: Lorem ipsum dolor sit ame\n" in captured.out
        assert "\ncall_kwargs: {'params': {'key': 'value', 'num': '123'}, 'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'}, 'timeout': 45}\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_with_custom_headers(self, mock_get, capsys):
        """ Test fetch with custom headers. """
        print_my_func_name()

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

        assert "\nFull URL: https://example.com\n" in captured.out
        assert "\nStatus: 200\n" in captured.out
        assert "\nResponse time: 0.000 seconds\n" in captured.out
        assert "\nresult: Lorem ipsum dolor sit ame\n" in captured.out
        assert "\ncall_kwargs: {'params': None, 'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36', 'Authorization': 'Bearer token'}, 'timeout': 45}\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_status_206(self, mock_get, capsys):
        """ Test fetch with status 206 (Partial Content) ."""
        print_my_func_name()

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

        assert "\nFull URL: https://example.com\n" in captured.out
        assert "\nStatus: 206\n" in captured.out
        assert "\nResponse time: 0.000 seconds\n" in captured.out
        assert "\nresult: Partial Lorem ipsum dolor sit ame\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_status_404(self, mock_get, capsys):
        """ Test fetch with 404 status. """
        print_my_func_name()

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

        assert "\nFull URL: https://example.com/notfound\n" in captured.out
        assert "\nStatus: 404\n" in captured.out
        assert "\nResponse time: 0.000 seconds\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.network.fetch_data_from_url : HTTP error responses\n" in captured.out
        assert "\nHTTP 404 for https://example.com/notfound\n" in captured.out
        assert "\nresult: None\n" in captured.out


    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_status_500(self, mock_get, capsys):
        """ Test fetch with 500 status. """
        print_my_func_name()

        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Server Error Lorem ipsum dolor sit ame"
        mock_response.url = "https://example.com"
        mock_get.return_value = mock_response

        result = NewtNet.fetch_data_from_url("https://example.com", repeat_on_fail=False)
        print("result:", result)
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nFull URL: https://example.com\n" in captured.out
        assert "\nStatus: 500\n" in captured.out
        assert "\nResponse time: 0.000 seconds\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.network.fetch_data_from_url : HTTP error responses\n" in captured.out
        assert "\nHTTP 500 for https://example.com\n" in captured.out
        assert "\nresult: None\n" in captured.out


    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_timeout(self, mock_get, capsys):
        """ Test fetch with timeout error. """
        print_my_func_name()

        mock_get.side_effect = requests.exceptions.ReadTimeout("Timeout")

        result = NewtNet.fetch_data_from_url("https://example.com", repeat_on_fail=False)
        print("result:", result)
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.network.fetch_data_from_url : ReadTimeout\n" in captured.out
        assert "\nReadTimeout: Timeout\n" in captured.out
        assert "\nTimeout (45s) for https://example.com\n" in captured.out
        assert "\nRequest failed after 0.00s\n" in captured.out
        assert "\nresult: None\n" in captured.out


    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_request_exception(self, mock_get, capsys):
        """ Test fetch with general request exception. """
        print_my_func_name()

        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        result = NewtNet.fetch_data_from_url("https://example.com", repeat_on_fail=False)
        print("result:", result)
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.network.fetch_data_from_url : RequestException\n" in captured.out
        assert "\nRequest failed after 0.00s\n" in captured.out
        assert "\nRequestException: Connection error\n" in captured.out
        assert "\nresult: None\n" in captured.out


    @patch('newtutils.network.requests.get')
    @patch('newtutils.console._retry_pause')
    def test_fetch_data_from_url_retry_on_fail(self, mock_retry, mock_get, capsys):
        """ Test retry behavior on failure. """
        print_my_func_name()

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
        assert mock_retry.call_count == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\nFull URL: https://example.com\n") == 2
        assert captured.out.count("\nResponse time: 0.000 seconds\n") == 2
        assert "\nStatus: 500\n" in captured.out
        assert "\nStatus: 200\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.network.fetch_data_from_url : HTTP error responses\n" in captured.out
        assert "\nHTTP 500 for https://example.com\n" in captured.out
        assert "\nresult: Success\n" in captured.out


    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_custom_timeout(self, mock_get, capsys):
        """ Test fetch with custom timeout. """
        print_my_func_name()

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

        assert "\nFull URL: https://example.com\n" in captured.out
        assert "\nStatus: 200\n" in captured.out
        assert "\nResponse time: 0.000 seconds\n" in captured.out
        assert "\nresult: Lorem ipsum dolor sit ame\n" in captured.out
        assert "\ncall_kwargs: {'params': None, 'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'}, 'timeout': 60}\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    def test_fetch_data_from_url_invalid_input(self, capsys):
        """ Test fetch with invalid input. """
        print_my_func_name()

        result = NewtNet.fetch_data_from_url(123, repeat_on_fail=False)  # type: ignore
        print("result:", result)
        assert result is None

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.network.fetch_data_from_url : base_url\n" in captured.out
        assert "\nExpected <class 'str'>, got <class 'int'>\n" in captured.out
        assert "\nValue: 123\n" in captured.out
        assert "\nresult: None\n" in captured.out
        # Expected absence of result
        assert "This line will not be printed" not in captured.out


    @patch('newtutils.network.requests.get')
    def test_fetch_data_from_url_mode_alert(self, mock_get, capsys):
        """ Test fetch with alert mode. """
        print_my_func_name()

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
            assert mock_beep.call_count == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nFull URL: https://example.com\n" in captured.out
        assert "\nStatus: 500\n" in captured.out
        assert "\nResponse time: 0.000 seconds\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.network.fetch_data_from_url : HTTP error responses\n" in captured.out
        assert "\nHTTP 500 for https://example.com\n" in captured.out
        assert "\nresult: None\n" in captured.out


class TestDownloadFileFromUrl:
    """ Tests for download_file_from_url function. """


    @patch('newtutils.network.os.path.getsize')
    @patch('newtutils.network.NewtFiles._check_file_exists')
    @patch('newtutils.network.requests.get')
    @patch('newtutils.network.requests.head')
    @patch('newtutils.files.save_text_to_file')
    def test_download_file_from_url_text(self, mock_save, mock_head, mock_get, mock_check_file, mock_getsize, capsys):
        """ Test downloading a text file. """
        print_my_func_name()

        mock_check_file.return_value = False  # File doesn't exist

        mock_head_response = Mock()
        mock_head_response.headers = {"Content-Length": "12"}
        mock_head.return_value = mock_head_response

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
        assert mock_save.call_count == 1
        assert mock_get.call_count == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nDownloading from: https://example.com/file.txt\n" in captured.out
        assert "\nFile size: 0.00001144 Mb\n" in captured.out
        assert "\nStatus: 200\n" in captured.out
        assert "\nContent-Type: text/plain\n" in captured.out
        assert "\nSaved to: tmp_file.txt\n" in captured.out
        assert "\nresult: True\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    @patch('newtutils.network.os.path.getsize')
    @patch('newtutils.network.NewtFiles._check_file_exists')
    @patch('newtutils.network.requests.get')
    @patch('newtutils.network.requests.head')
    @patch('builtins.open', create=True)
    def test_download_file_from_url_binary(self, mock_open, mock_head, mock_get, mock_check_file, mock_getsize, capsys):
        """ Test downloading a binary file. """
        print_my_func_name()

        mock_check_file.return_value = False  # File doesn't exist

        mock_head_response = Mock()
        mock_head_response.headers = {"Content-Length": "14"}
        mock_head.return_value = mock_head_response

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
        assert mock_open.call_count == 1
        assert mock_get.call_count == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nDownloading from: https://example.com/file.bin\n" in captured.out
        assert "\nFile size: 0.00001335 Mb\n" in captured.out
        assert "\nStatus: 200\n" in captured.out
        assert "\nContent-Type: application/octet-stream\n" in captured.out
        assert "\nSaved to: tmp_file.bin\n" in captured.out
        assert "\nresult: True\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    @patch('newtutils.network.os.path.getsize')
    @patch('newtutils.network.NewtFiles._check_file_exists')
    @patch('newtutils.network.requests.get')
    @patch('newtutils.network.requests.head')
    def test_download_file_from_url_status_404(self, mock_head, mock_get, mock_check_file, mock_getsize, capsys):
        """ Test download with 404 status. """
        print_my_func_name()

        mock_check_file.return_value = False  # File doesn't exist

        mock_head_response = Mock()
        mock_head_response.headers = {}
        mock_head.return_value = mock_head_response

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

        assert mock_get.call_count == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nDownloading from: https://example.com/file.txt\n" in captured.out
        assert "\nFile size: 0.00000000 Mb\n" in captured.out
        assert "\nStatus: 404\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.network.download_file_from_url : Not Success\n" in captured.out
        assert "\nHTTP 404 while downloading https://example.com/file.txt\n" in captured.out
        assert "\nresult: False\n" in captured.out


    @patch('newtutils.network.os.path.getsize')
    @patch('newtutils.network.NewtFiles._check_file_exists')
    @patch('newtutils.network.requests.get')
    @patch('newtutils.network.requests.head')
    def test_download_file_from_url_timeout(self, mock_head, mock_get, mock_check_file, mock_getsize, capsys):
        """ Test download with timeout. """
        print_my_func_name()

        mock_check_file.return_value = False  # File doesn't exist

        mock_head_response = Mock()
        mock_head_response.headers = {}
        mock_head.return_value = mock_head_response

        mock_get.side_effect = requests.exceptions.ReadTimeout("Timeout")

        with patch('newtutils.console._beep_boop'):
            result = NewtNet.download_file_from_url(
                "https://example.com/file.txt",
                "tmp_file.txt",
                repeat_on_fail=False
            )
            print("result:", result)
            assert result is False

        assert mock_get.call_count == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nDownloading from: https://example.com/file.txt\n" in captured.out
        assert "\nFile size: 0.00000000 Mb\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.network.download_file_from_url : ReadTimeout\n" in captured.out
        assert "\nReadTimeout: Timeout\n" in captured.out
        assert "\nTimeout (60s) while downloading https://example.com/file.txt\n" in captured.out
        assert "\nresult: False\n" in captured.out


    @patch('newtutils.network.os.path.getsize')
    @patch('newtutils.network.NewtFiles._check_file_exists')
    @patch('newtutils.network.requests.get')
    @patch('newtutils.network.requests.head')
    def test_download_file_from_url_request_exception(self, mock_head, mock_get, mock_check_file, mock_getsize, capsys):
        """ Test download with request exception. """
        print_my_func_name()

        mock_check_file.return_value = False  # File doesn't exist

        mock_head_response = Mock()
        mock_head_response.headers = {}
        mock_head.return_value = mock_head_response

        mock_get.side_effect = requests.exceptions.RequestException("Error test text")

        with patch('newtutils.console._beep_boop'):
            result = NewtNet.download_file_from_url(
                "https://example.com/file.txt",
                "tmp_file.txt",
                repeat_on_fail=False
            )
            print("result:", result)
            assert result is False

        assert mock_get.call_count == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nDownloading from: https://example.com/file.txt\n" in captured.out
        assert "\nFile size: 0.00000000 Mb\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.network.download_file_from_url : RequestException\n" in captured.out
        assert "\nRequestException: Error test text\n" in captured.out
        assert "\nresult: False\n" in captured.out


    @patch('newtutils.network.os.path.getsize')
    @patch('newtutils.network.NewtFiles._check_file_exists')
    @patch('newtutils.network.requests.get')
    @patch('newtutils.network.requests.head')
    @patch('newtutils.console._retry_pause')
    @patch('newtutils.files.save_text_to_file')
    def test_download_file_from_url_retry(self, mock_save, mock_retry, mock_head, mock_get, mock_check_file, mock_getsize, capsys):
        """ Test download with retry on failure. """
        print_my_func_name()

        mock_check_file.return_value = False  # File doesn't exist

        mock_head_response = Mock()
        mock_head_response.headers = {"Content-Length": "7"}
        mock_head.return_value = mock_head_response

        # First call fails, second succeeds
        mock_response_fail = Mock()
        mock_response_fail.status_code = 500

        mock_response_success = Mock()
        mock_response_success.status_code = 200
        mock_response_success.text = "Success"
        mock_response_success.content = b"Success"
        mock_response_success.headers = {"Content-Type": "text/plain"}

        mock_get.side_effect = [mock_response_fail, mock_response_success]

        with patch('newtutils.console._beep_boop'):
            result = NewtNet.download_file_from_url(
                "https://example.com/file.txt",
                "tmp_file.txt",
                repeat_on_fail=True
            )
            print("result:", result)
            assert result is True

        assert mock_save.call_count == 1
        assert mock_retry.call_count == 1
        assert mock_get.call_count == 2

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\nDownloading from: https://example.com/file.txt\n") == 2
        assert captured.out.count("\nFile size: 0.00000668 Mb\n") == 2
        assert "\nStatus: 500\n" in captured.out
        assert "\n::: ERROR :::\n" in captured.out
        assert "\nLocation: Newt.network.download_file_from_url : Not Success\n" in captured.out
        assert "\nHTTP 500 while downloading https://example.com/file.txt\n" in captured.out
        assert "\nStatus: 200\n" in captured.out
        assert "\nContent-Type: text/plain\n" in captured.out
        assert "\nSaved to: tmp_file.txt\n" in captured.out
        assert "\nresult: True\n" in captured.out


    def test_download_file_from_url_invalid_input(self, capsys):
        """ Test download with invalid input. """
        print_my_func_name()

        result_1 = NewtNet.download_file_from_url(
            123,  # type: ignore
            "tmp_file.txt",
            repeat_on_fail=False
        )
        print("result_1:", result_1)
        assert result_1 is False
        print()

        result_2 = NewtNet.download_file_from_url(
            "https://example.com",
            456,  # type: ignore
            repeat_on_fail=False
        )
        print("result_2:", result_2)
        assert result_2 is False

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert captured.out.count("\n::: ERROR :::\n") == 2
        assert "\nLocation: Newt.console.validate_input > Newt.network.download_file_from_url : file_url\n" in captured.out
        assert "\nLocation: Newt.console.validate_input > Newt.network.download_file_from_url : save_path\n" in captured.out
        assert captured.out.count("\nExpected <class 'str'>, got <class 'int'>\n") == 2
        assert "\nValue: 123\n" in captured.out
        assert "\nValue: 456\n" in captured.out
        assert "\nresult_1: False\n" in captured.out
        assert "\nresult_2: False\n" in captured.out


    @patch('newtutils.network.os.path.getsize')
    @patch('newtutils.network.NewtFiles._check_file_exists')
    @patch('newtutils.network.requests.get')
    @patch('newtutils.network.requests.head')
    @patch('newtutils.files.save_text_to_file')
    def test_download_file_from_url_json_content_type(self, mock_save, mock_head, mock_get, mock_check_file, mock_getsize, capsys):
        """ Test download with JSON content type. """
        print_my_func_name()

        mock_check_file.return_value = False  # File doesn't exist

        mock_head_response = Mock()
        mock_head_response.headers = {"Content-Length": "16"}
        mock_head.return_value = mock_head_response

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"key": "value"}'
        mock_response.content = b'{"key": "value"}'
        mock_response.headers = {"Content-Type": "application/json"}
        mock_get.return_value = mock_response

        result = NewtNet.download_file_from_url(
            "https://example.com/data.json",
            "tmp_data.json",
            repeat_on_fail=False
        )
        print("result:", result)
        assert result is True

        mock_save.assert_called_once()
        assert mock_save.call_count == 1
        assert mock_get.call_count == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nDownloading from: https://example.com/data.json\n" in captured.out
        assert "\nFile size: 0.00001526 Mb\n" in captured.out
        assert "\nStatus: 200\n" in captured.out
        assert "\nContent-Type: application/json\n" in captured.out
        assert "\nSaved to: tmp_data.json\n" in captured.out
        assert "\nresult: True\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out


    @patch('newtutils.network.os.path.getsize')
    @patch('newtutils.network.NewtFiles._check_file_exists')
    @patch('newtutils.network.requests.get')
    @patch('newtutils.network.requests.head')
    def test_download_file_from_url_custom_headers(self, mock_head, mock_get, mock_check_file, mock_getsize, capsys):
        """ Test download with custom headers. """
        print_my_func_name()

        mock_check_file.return_value = False  # File doesn't exist

        mock_head_response = Mock()
        mock_head_response.headers = {"Content-Length": "7"}
        mock_head.return_value = mock_head_response

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"Content"
        mock_response.headers = {"Content-Type": "application/octet-stream"}
        mock_get.return_value = mock_response

        custom_headers = {"Authorization": "Bearer token"}
        with patch('builtins.open', create=True):
            result = NewtNet.download_file_from_url(
                "https://example.com/file.bin",
                "tmp_file.bin",
                headers=custom_headers,
                repeat_on_fail=False
            )
            print("result:", result)
            assert result is True
            call_kwargs = mock_get.call_args[1]
            print("call_kwargs:", call_kwargs)
            assert call_kwargs["headers"]["Authorization"] == "Bearer token"

        assert mock_get.call_count == 1

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "\nDownloading from: https://example.com/file.bin\n" in captured.out
        assert "\nFile size: 0.00000668 Mb\n" in captured.out
        assert "\nStatus: 200\n" in captured.out
        assert "\nContent-Type: application/octet-stream\n" in captured.out
        assert "\nSaved to: tmp_file.bin\n" in captured.out
        assert "\nresult: True\n" in captured.out
        assert "\ncall_kwargs: {'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36', 'Authorization': 'Bearer token'}, 'timeout': (5, 60)}\n" in captured.out
        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
