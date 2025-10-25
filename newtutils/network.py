"""
Created on 2025-10

@author: NewtCode Anna Burova

Functions:
    DEFAULT_HTTP_HEADERS: dict[str, str]
        "User-Agent"
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

import sys
import requests
import newtutils.console as NewtCons
import newtutils.utility as NewtUtil
import newtutils.files as NewtFiles


# === CONSTANTS ===

# Default HTTP request headers for external API communication.
# Used by all outgoing HTTP requests from NewtUtils.
# Mimics a modern Chrome browser to reduce blocking by remote servers.
# Usage:
#     headers = DEFAULT_HTTP_HEADERS.copy()
#     response = requests.get(url, headers=headers)
# Notes:
#     - Always use `.copy()` when modifying headers locally.
#     - Never reassign or mutate this constant directly.
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
        mode: str = "auto",  # "auto" / "alert" (auto) / "manual"
        timeout: int = 45,
        repeat_on_fail: bool = True
        ) -> str | None:
    """
    Fetch data from an external URL with retry logic and colored console feedback.

    This function performs a GET request to the specified URL with optional parameters.
    If a recoverable error occurs (timeout, temporary unavailability, etc.),
    it optionally retries the request until a valid response (HTTP 200|206) is received.

    Args:
        base_url (str):
            The base URL for the request.
        params (dict[str, object] | None, optional):
            Dictionary of query parameters. Defaults to None.
        headers (dict[str, str] | None, optional):
            Optional HTTP headers for the request.
            If None, a copy of DEFAULT_HTTP_HEADERS is used.
        mode (str, optional):
            Controls retry and notification behavior.
            Available options:
                - "auto": automatic retries without prompts.
                - "alert": same as auto, but plays sound on failure.
                - "manual": interactive prompts (ask to repeat or continue).
        timeout (int, optional):
            Timeout for the request in seconds. Defaults to 45.
        repeat_on_fail (bool, optional):
            If True, the function retries the request after recoverable errors.
            Defaults to True.

    Returns:
        str | None:
            The response text if successful, otherwise None.
    """

    if not NewtUtil.validate_input(base_url, str):
        return None

    params_to_send = None
    if params is not None:
        if not NewtUtil.validate_input(params, dict):
            return None

        # Ensure params are in a requests-compatible form (mapping of str->str)
        params_to_send = {str(k): str(v) for k, v in params.items()}

    # Assign safe default headers
    headers = DEFAULT_HTTP_HEADERS.copy() if headers is None else headers.copy()

    beep_boop = mode in ("alert", "manual")

    while True:
        try:
            response = requests.get(
                base_url,
                params=params_to_send,
                headers=headers,
                timeout=timeout
                )
            status = response.status_code

            print(f"Full URL: {response.url}")
            print(f"Status: {status}")

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
                    NewtUtil._beep_boop()

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
            NewtCons.error_msg(
                f"ReadTimeout: {e}",
                f"Timeout ({timeout}s) for {base_url}",
                location="Newt.network.fetch_data_from_url",
                stop=False
            )
            if beep_boop:
                NewtUtil._beep_boop()

        except requests.exceptions.RequestException as e:
            NewtCons.error_msg(
                f"RequestException: {e}",
                location="Newt.network.fetch_data_from_url",
                stop=False
            )
            if beep_boop:
                NewtUtil._beep_boop()

        if not repeat_on_fail:
            return None

        NewtUtil._retry_pause(beep=beep_boop)


def download_file_from_url(
        file_url: str,
        save_path: str,
        headers: dict[str, str] | None = None,
        timeout: int = 60,
        repeat_on_fail: bool = True
        ) -> bool:
    """
    Download a text or binary file from a given URL and save it locally.

    This function sends a GET request to the specified URL and writes the
    downloaded content to the provided file path.
    It automatically creates the destination directory if missing and retries
    failed downloads when allowed.

    Args:
        file_url (str):
            The full URL of the file to download.
        save_path (str):
            Local file path where the downloaded content will be saved.
        headers (dict[str, str] | None, optional):
            Optional HTTP headers for the request.
            If None, a copy of DEFAULT_HTTP_HEADERS is used.
        timeout (int, optional):
            Request timeout in seconds. Defaults to 60.
        repeat_on_fail (bool, optional):
            If True, retry after recoverable errors.
            Defaults to True.

    Returns:
        bool:
            True if the file was successfully downloaded and saved,
            otherwise False.
    """

    if not NewtUtil.validate_input(file_url, str):
        return False

    if not NewtUtil.validate_input(save_path, str):
        return False

    # Assign safe default headers
    headers = DEFAULT_HTTP_HEADERS.copy() if headers is None else headers.copy()

    while True:
        try:
            response = requests.get(
                file_url,
                headers=headers,
                timeout=timeout
                )
            status = response.status_code

            print(f"Downloading from: {file_url}")
            print(f"Status: {status}")

            if status in (
                    200,  # Normal success
                    ):
                # Detect binary vs text
                content_type = response.headers.get("Content-Type", "").lower()

                if "text" in content_type or "json" in content_type:
                    content = response.text
                    NewtFiles.save_text_to_file(save_path, content)

                else:
                    # Binary save
                    NewtFiles._ensure_dir_exists(save_path)
                    with open(save_path, "wb") as f:
                        f.write(response.content)

                print(f"Saved to: {save_path}")
                return True

            else:
                NewtCons.error_msg(
                    f"HTTP {status} while downloading {file_url}",
                    location="Newt.network.download_file_from_url",
                    stop=False
                )
                NewtUtil._beep_boop()

        except requests.exceptions.ReadTimeout as e:
            NewtCons.error_msg(
                f"ReadTimeout: {e}",
                f"Timeout ({timeout}s) while downloading {file_url}",
                location="Newt.network.download_file_from_url",
                stop=False
            )
            NewtUtil._beep_boop()

        except requests.exceptions.RequestException as e:
            NewtCons.error_msg(
                f"RequestException: {e}",
                location="Newt.network.download_file_from_url",
                stop=False
            )
            NewtUtil._beep_boop()

        if not repeat_on_fail:
            return False

        NewtUtil._retry_pause(beep=True)
