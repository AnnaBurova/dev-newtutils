"""
Updated on 2026-02
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
        save_path: str | None = None,
        max_mb_size: int = 2,
        mode: str = "auto",
        timeout: int = 45,
        repeat_on_fail: bool = True,
        logging: bool = True
        ) -> str | bool
"""

from __future__ import annotations

import os
import time
import requests
from urllib.parse import unquote

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
        save_path: str | None = None,
        max_mb_size: int = 2,
        mode: str = "auto",
        timeout: int = 45,
        repeat_on_fail: bool = True,
        logging: bool = True
        ) -> str | bool:
    """
    Fetch data from a URL with retry logic and console feedback.

    Sends a GET request to the specified URL
    using optional query parameters and headers.
    Supports optional file download with size limits.

    Args:
        base_url (str):
            Target URL for the request.
        params (dict[str, object] | None):
            Query parameters to include in the request.
            Defaults to None.
        headers (dict[str, str] | None):
            Custom HTTP headers.
            If None, uses `DEFAULT_HTTP_HEADERS`.
        save_path (str | None):
            If provided, saves the response to this path.
            Defaults to None.
        max_mb_size (int):
            Maximum allowed download size in MB when saving to file.
            Defaults to 2.
        mode (str):
            Controls retry behavior and notifications.
            Defaults to "auto".
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
        out (str | bool):
            Response text if save_path is None and successful,
            True if saved successfully,
            False otherwise.
    """

    if not NewtCons.validate_type(
        base_url, str, check_non_empty=True, stop=False,
        location="Newt.network.fetch_data_from_url : base_url"
    ):
        return False

    params_to_send = None
    if params is not None:
        if not NewtCons.validate_type(
            params, dict, check_non_empty=True, stop=False,
            location="Newt.network.fetch_data_from_url : params"
        ):
            return False

        # Ensure params are in a requests-compatible form (mapping of str->str)
        params_to_send = {str(k): str(v) for k, v in params.items()}

    # Assign safe default headers
    custom_headers = DEFAULT_HTTP_HEADERS.copy()
    if headers is not None:
        custom_headers.update(headers)

    if save_path is not None:
        if not NewtCons.validate_type(
            save_path, str, check_non_empty=True, stop=False,
            location="Newt.network.fetch_data_from_url : save_path"
        ):
            return False

    if not NewtCons.validate_type(
        max_mb_size, int, check_non_empty=True, stop=False,
        location="Newt.network.fetch_data_from_url : max_mb_size"
    ):
        return False
    # make it to pseudo-byte
    max_mb_size = max_mb_size * 1024 * 1024

    beep_boop = mode in ("alert", "manual")

    # Prepare the request without sending it
    prepared_request = requests.Request(
        'GET',
        base_url,
        headers=custom_headers,
        params=params_to_send
    ).prepare()

    # Print the full URL
    if prepared_request.url is not None:
        decoded_url = unquote(prepared_request.url)
        print("Original URL:", prepared_request.url)
        if decoded_url != prepared_request.url:
            print(" Decoded URL:", decoded_url)

    # Stop on empty or wrong URL
    else:
        print("Full URL: URL is None")
        return False

    # If it is file to save local
    if save_path is not None:
        header_size_b = 0
        header_retry_count = 0
        while header_retry_count < 5:
            head_content = requests.head(
                base_url,
                headers=custom_headers
            )
            header_size_b = int(head_content.headers.get('Content-Length', 0))
            size_mb = header_size_b / (1024*1024)
            print(f"File size: {size_mb:.8f} Mb")

            if header_size_b == 0:
                NewtCons.error_msg(
                    "Warning: Content-Length header is missing or zero.",
                    location="Newt.network.fetch_data_from_url : size_mb",
                    stop=False
                )
                if beep_boop:
                    NewtCons._beep_boop()

                header_retry_count += 1
                continue

            break

        if header_retry_count >= 5:
            print("Content-Length header is missing or zero.")
            return False

        if NewtFiles.check_file_exists(save_path, logging=False):
            # get file size and compare
            existing_size_b = os.path.getsize(save_path)
            custom_headers["Range"] = f"bytes={existing_size_b}-"

            if existing_size_b == header_size_b:
                print(f"File already exists: {save_path}")
                return True

        if header_size_b > max_mb_size:
            NewtCons.error_msg(
                "Warning: File to big to download",
                location="Newt.network.fetch_data_from_url : max_mb_size",
                stop=False
            )
            return False

    global_retry_count = 0
    while global_retry_count < 5:
        start_time = time.perf_counter()
        try:
            response = requests.get(
                base_url,
                params=params_to_send,
                headers=custom_headers,
                timeout=(10, timeout),
                stream=True
            )
            status = response.status_code
            print(f"Status: {status}")
            elapsed = time.perf_counter() - start_time
            if logging:
                print(f"Response time: {elapsed:.3f} seconds")

            bad_status_dict = {
                400: "unable to use 'all' keyword for this API",  # TODO
                401: "Invalid access token / Unauthorized",  # TODO
                403: "Forbidden",  # TODO
                404: "Not Found",  # TODO
                500: "Internal Server Error",  # TODO
                502: "Bad Gateway",  # TODO
                503: "Service Unavailable",  # TODO
                525: "SSL Handshake Failed",  # TODO
            }

            # Successful responses (200-299)
            if status in (
                    200,  # Normal success
                    206,  # Partial content or recoverable response
                    ):
                if save_path is None:
                    return response.text

                content_type = response.headers.get("Content-Type", "").lower()
                print(f"Content-Type: {content_type}")

                if "text" in content_type or "json" in content_type:
                    NewtFiles.save_text_to_file(save_path, response.text)

                # Binary save
                else:
                    NewtFiles.ensure_dir_exists(save_path)

                    bin_mode = "ab" if "Range" in custom_headers else "wb"
                    with open(save_path, bin_mode) as f:
                        # f.write(response.content)
                        chunk_size = 1024 * 1024
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)

                print(f"Saved to: {save_path}")
                return True

            # Client error responses (400-499)
            # Server error responses (500-599)
            elif status in bad_status_dict:
                NewtCons.error_msg(
                    f"HTTP {status} = {bad_status_dict[status]}",
                    f"for {base_url}",
                    location="Newt.network.fetch_data_from_url : HTTP error responses",
                    stop=False
                )

                # MANUAL DECISION MODE
                if mode == "manual":
                    NewtCons._beep_boop()
                    repeat_code = input("Repeat request? (y/N): ").strip().lower()
                    if repeat_code in ("y"):
                        print("Repeating request...")
                        continue

                    continue_code = input("Return False? Else stop (Y/n): ").strip().lower()
                    if continue_code in ("y", ""):
                        print("Continuing execution without data...")
                        return False

                    NewtCons.error_msg(
                        "Aborting execution",
                        location="Newt.network.fetch_data_from_url : Stopping on manual decision"
                    )

            else:
                NewtCons.error_msg(
                    f"Unexpected HTTP {status} for {base_url}",
                    location="Newt.network.fetch_data_from_url : Unexpected HTTP status"
                )

            # AUTO MODES
            if not repeat_on_fail:
                return False

        except requests.exceptions.ReadTimeout as e:
            elapsed = time.perf_counter() - start_time
            NewtCons.error_msg(
                f"ReadTimeout: {e}",
                f"Timeout ({timeout}s) for {base_url}",
                f"Request failed after {elapsed:.2f}s",
                location="Newt.network.fetch_data_from_url : ReadTimeout",
                stop=False
            )

        except requests.exceptions.RequestException as e:
            NewtCons.error_msg(
                f"RequestException: {e}",
                location="Newt.network.fetch_data_from_url : RequestException",
                stop=False
            )

        except Exception as e:
            NewtCons.error_msg(
                f"Exception: {e}",
                location="Newt.network.fetch_data_from_url : Exception",
                stop=False
            )

        global_retry_count += 1
        print(f"Attempt {global_retry_count} / 5")
        NewtCons._retry_pause(beep=beep_boop)
        print()

    if beep_boop:
        NewtCons._beep_boop()
    return False
