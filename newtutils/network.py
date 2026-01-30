"""
Updated on 2025-11
Created on 2025-10

@author: NewtCode Anna Burova

Constants:
    DEFAULT_HTTP_HEADERS (dict[str, str]):
        Default HTTP headers used by all outgoing HTTP requests.

Functions:
    def fetch_data_from_url(
        base_url: str,
        params: dict[str, object] | None = None,
        headers: dict[str, str] | None = None,
        mode: str = "auto",
        timeout: int = 45,
        repeat_on_fail: bool = True
        ) -> str | None
    def download_file_from_url(
        file_url: str,
        save_path: str,
        headers: dict[str, str] | None = None,
        timeout: int = 60,
        repeat_on_fail: bool = True
        ) -> bool
"""

from __future__ import annotations

import sys
import os
import time
import requests
import newtutils.console as NewtCons
import newtutils.files as NewtFiles


# === CONSTANTS ===

"""
Default HTTP request headers for external API calls.

These headers are applied to all HTTP requests unless overridden.
They mimic a modern Chrome browser to minimize blocking by remote servers.

Notes:
    - Always use `.copy()` when modifying headers locally.
    - Never modify this constant directly.
"""
DEFAULT_HTTP_HEADERS: dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}


def fetch_data_from_url(
        base_url: str,
        params: dict[str, object] | None = None,
        headers: dict[str, str] | None = None,
        mode: str = "auto",
        timeout: int = 45,
        repeat_on_fail: bool = True
        ) -> str | None:
    """
    Fetch data from a URL with retry logic and console feedback.

    Sends a GET request to the specified URL using optional query parameters and headers.
    The function can automatically retry after temporary failures
    depending on the selected mode and retry settings.

    Args:
        base_url (str):
            Target URL for the request.
        params (dict[str, object] | None):
            Query parameters to include in the request.
            Defaults to None.
        headers (dict[str, str] | None):
            Custom HTTP headers.
            If None, uses `DEFAULT_HTTP_HEADERS`.
        mode (str):
            Controls retry behavior and notifications
            Defaults to "auto"
            - "auto": automatic retries without user input.
            - "alert": auto retries with sound alerts.
            - "manual": prompts user for each retry decision.
        timeout (int):
            Timeout for the request in seconds.
            Defaults to 45.
        repeat_on_fail (bool):
            If True, automatically retries after recoverable errors.
            Defaults to True.

    Returns:
        out (str | None):
            Response text if successful, otherwise None.
    """

    if not NewtCons.validate_input(base_url, str,
                                   location="Newt.network.fetch_data_from_url.base_url"):
        return None

    params_to_send = None
    if params is not None:
        if not NewtCons.validate_input(params, dict,
                                       location="Newt.network.fetch_data_from_url.params"):
            return None

        # Ensure params are in a requests-compatible form (mapping of str->str)
        params_to_send = {str(k): str(v) for k, v in params.items()}

    # Assign safe default headers
    custom_headers = DEFAULT_HTTP_HEADERS.copy()
    if headers is not None:
        custom_headers.update(headers)

    beep_boop = mode in ("alert", "manual")

    while True:
        start_time = time.perf_counter()
        try:
            response = requests.get(
                base_url,
                params=params_to_send,
                headers=custom_headers,
                timeout=timeout
            )
            elapsed = time.perf_counter() - start_time
            status = response.status_code

            print(f"Full URL: {response.url}")
            print(f"Status: {status}")
            print(f"Response time: {elapsed:.3f} seconds")

            if status in (
                    200,  # Normal success
                    206,  # Partial content or recoverable response
                    ):
                return response.text

            # Known error statuses
            elif status in (
                    400,  # unable to use 'all' keyword for this API
                    401,  # Invalid access token / Unauthorized
                    403,  # Forbidden
                    404,  # Not Found
                    500,  # Internal Server Error
                    502,  # Bad Gateway
                    503,  # API not active
                    ):
                NewtCons.error_msg(
                    f"HTTP {status} for {base_url}",
                    location="Newt.network.fetch_data_from_url",
                    stop=False
                )
                if beep_boop:
                    NewtCons.beep_boop()

                # MANUAL DECISION MODE
                if mode == "manual":
                    repeat_code = input("Repeat request? (Y/n): ").strip().lower()
                    if repeat_code in ("y", ""):
                        print("Repeating request...")
                        continue

                    continue_code = input("Continue anyway? (Y/n): ").strip().lower()
                    if continue_code in ("y", ""):
                        print("Continuing execution without data...")
                        return None

                    sys.exit(0)

                # AUTO MODES
                if not repeat_on_fail:
                    return None

        except requests.exceptions.ReadTimeout as e:
            elapsed = time.perf_counter() - start_time
            NewtCons.error_msg(
                f"ReadTimeout: {e}",
                f"Timeout ({timeout}s) for {base_url}",
                f"Request failed after {elapsed:.2f}s",
                location="Newt.network.fetch_data_from_url",
                stop=False
            )
            if beep_boop:
                NewtCons.beep_boop()

        except requests.exceptions.RequestException as e:
            elapsed = time.perf_counter() - start_time
            NewtCons.error_msg(
                f"Request failed after {elapsed:.2f}s",
                f"RequestException: {e}",
                location="Newt.network.fetch_data_from_url",
                stop=False
            )
            if beep_boop:
                NewtCons.beep_boop()

        if not repeat_on_fail:
            return None

        NewtCons.retry_pause(beep=beep_boop)


def download_file_from_url(
        file_url: str,
        save_path: str,
        headers: dict[str, str] | None = None,
        timeout: int = 60,
        repeat_on_fail: bool = True
        ) -> bool:
    """
    Download a file from a URL and save it locally.

    Sends a GET request to download a file and saves it to the specified path.
    The target directory is created automatically if missing.
    Retries may occur after temporary errors depending on configuration.

    Args:
        file_url (str):
            URL of the file to download.
        save_path (str):
            Local path where the file will be saved.
        headers (dict[str, str] | None):
            Custom HTTP headers.
            If None, uses `DEFAULT_HTTP_HEADERS`.
        timeout (int):
            Request timeout in seconds.
            Defaults to 60.
        repeat_on_fail (bool):
            If True, automatically retries after recoverable errors.
            Defaults to True.

    Returns:
        out (bool):
            True if successfully downloaded and saved,
            otherwise False.
    """

    if not NewtCons.validate_input(file_url, str,
                                   location="Newt.network.download_file_from_url.file_url"):
        return False

    if not NewtCons.validate_input(save_path, str,
                                   location="Newt.network.download_file_from_url.save_path"):
        return False

    # Assign safe default headers
    custom_headers = DEFAULT_HTTP_HEADERS.copy()
    if headers is not None:
        custom_headers.update(headers)

    while True:
        try:
            print(f"Downloading from: {file_url}")
            head_content = requests.head(file_url, headers=custom_headers, timeout=10)
            size_b = int(head_content.headers.get('Content-Length', 0))
            size_mb = size_b / (1024*1024)
            print(f"File size: {size_mb} Mb")

            if NewtFiles.check_file_exists(save_path, print_error=False):
                # get file size and compare
                existing_size_b = os.path.getsize(save_path)

                if existing_size_b == size_b:
                    print(f"File already exists: {save_path}")
                    return True

            response = requests.get(
                file_url,
                headers=custom_headers,
                timeout=(5, timeout)
                )
            response.raise_for_status()
            status = response.status_code
            print(f"Status: {status}")

            if status in (
                    200,  # Normal success
                    ):
                # Detect binary vs text
                content_type = response.headers.get("Content-Type", "").lower()
                print(f"Content-Type: {content_type}")

                if "text" in content_type or "json" in content_type:
                    NewtFiles.save_text_to_file(save_path, response.text)

                # Binary save
                else:
                    NewtFiles.ensure_dir_exists(save_path)
                    with open(save_path, "wb") as f:
                        f.write(response.content)

                print(f"Saved to: {save_path}")
                return True

            NewtCons.error_msg(
                f"HTTP {status} while downloading {file_url}",
                location="Newt.network.download_file_from_url",
                stop=False
            )
            NewtCons.beep_boop()

        except requests.exceptions.ReadTimeout as e:
            NewtCons.error_msg(
                f"ReadTimeout: {e}",
                f"Timeout ({timeout}s) while downloading {file_url}",
                location="Newt.network.download_file_from_url",
                stop=False
            )
            NewtCons.beep_boop()
            timeout += 30

        except requests.exceptions.RequestException as e:
            NewtCons.error_msg(
                f"RequestException: {e}",
                location="Newt.network.download_file_from_url",
                stop=False
            )
            NewtCons.beep_boop()

        except Exception as e:
            NewtCons.error_msg(
                f"General error: {e}",
                location="Newt.network.download_file_from_url",
                stop=False
            )
            NewtCons.beep_boop()

        if not repeat_on_fail:
            return False

        NewtCons.retry_pause(beep=True)
