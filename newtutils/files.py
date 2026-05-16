"""
Updated on 2026-05
Created on 2025-10

@author: NewtCode Anna Burova

Functions:
    def _normalize_newlines(
        content: str
        ) -> str
    def _obscure_logic(
        file_path_str: str,
        obscure_list: list[str],
        mask_char: str = "*"
        ) -> str
    def ensure_dir_exists(
        file_path: str
        ) -> None
    def check_file_exists(
        file_path: str,
        obscure_list: list = [],
        stop: bool = True,
        print_log: bool = True
        ) -> bool
    def choose_file_from_folder(
        folder_path: str,
        todo_dict: dict[str, int] | None = None
        ) -> str
    === TEXT ===
    def read_text_from_file(
        file_name: str,
        obscure_list: list = [],
        stop: bool = True,
        print_log: bool = True
        ) -> str | None
    def save_text_to_file(
        file_name: str,
        content: str,
        append: bool = False,
        obscure_list: list = [],
        print_log: bool = True
        ) -> None
    === JSON ===
    def convert_str_to_json(
        content: str
        ) -> list | dict | None
    def read_json_from_file(
        file_name: str,
        stop: bool = True,
        logging: bool = True
        ) -> list | dict | None
    def save_json_to_file(
        file_name: str,
        data: list | dict,
        indent: int = 2,
        logging: bool = True
        ) -> None
    === CSV ===
    def read_csv_from_file(
        file_name: str,
        delimiter: str = ";",
        stop: bool = True,
        logging: bool = True
        ) -> list[list[str]] | None
    def save_csv_to_file(
        file_name: str,
        rows: Sequence[Sequence[object]],
        append: bool = False,
        delimiter: str = ";",
        logging: bool = True
        ) -> None
    === LOG ===
    def setup_logging(
        _dir: str
        ) -> tuple[str, TextIO, object]
    def cleanup_logging(
        setup_data: tuple[str, TextIO, object],
        file_target: str
        ) -> None
"""

from __future__ import annotations

import sys
import os
from typing import TextIO
from collections.abc import Sequence

import csv
import json
import shutil
from datetime import datetime, timedelta, timezone

import newtutils.console as NewtCons
import newtutils.utility as NewtUtil


def _normalize_newlines(
        content: str
        ) -> str:
    """ ## Normalize newline characters in a text string to Unix-style newlines.

    Converts Windows-style newlines (\\r\\n) and old Mac-style (\\r) to Unix-style (\\n).
    Strips trailing whitespace from the end of the normalized text.

    Args:
        content (str):
            Input text containing mixed newline characters.

    Returns:
        out (str):
            Normalized text with consistent Unix-style newlines (\\n).
    """

    NewtCons.validate_type(
        content, str,
        location="Newt.files._normalize_newlines"
    )

    return content.rstrip().replace("\r\n", "\n").replace("\r", "\n")+"\n"


def _obscure_logic(
        file_path_str: str,
        obscure_list: list[str],
        mask_char: str = "*"
        ) -> str:
    """ ## Replace all characters in a string except specified substrings with a mask character.

    Builds a fully masked version of `file_path_str` using `mask_char`,
    then iterates over `obscure_list` and restores each matching substring
    back to its original characters using the walrus operator `:=` for
    position lookup.

    Args:
        file_path_str (str):
            The original string (e.g. a file path) to be masked.
        obscure_list (list[str]):
            A list of substrings that should remain visible (unmasked) in the result.<br>
            All other characters will be replaced by `mask_char`.
        mask_char (str):
            The character used to mask hidden parts of the string.<br>
            Defaults to "*".

    Returns:
        out (str):
            A masked version of `file_path_str` where every character is replaced by `mask_char`,
            except for occurrences of substrings found in `show_list`.
    """

    masked_text = list(mask_char * len(file_path_str))

    for substring in obscure_list:
        start = 0
        # walrus operator :=
        while (pos := file_path_str.find(substring, start)) != -1:
            for i in range(pos, pos + len(substring)):
                masked_text[i] = file_path_str[i]
            start = pos + len(substring)

    return "".join(masked_text)


def ensure_dir_exists(
        file_path: str
        ) -> None:
    """ ## Ensure that the directory for the given file path exists.

    Creates the target directory and any necessary parent directories if they do not exist.
    The function does not create or modify the file itself.

    Args:
        file_path (str):
            Full path to the target file (including the file name).

    Raises:
        SystemExit:
            If file_path is an empty string, terminates with exit code 1.
    """

    NewtCons.validate_type(
        file_path, str, check_non_empty=True,
        location="Newt.files.ensure_dir_exists : file_path"
    )

    dir_path = os.path.dirname(file_path)

    if not dir_path:
        # current directory, nothing to do
        return None

    if os.path.exists(dir_path):
        # directory exists, nothing to do
        return None

    try:
        os.makedirs(dir_path, exist_ok=True)
        return None

    # except OSError as e:
    except Exception as e:  # pragma: no cover
        NewtCons.error_msg(
            f"Found Error Msg: (found? write test!)",  # TODO
            f"Exception: {e}",
            location="Newt.files.ensure_dir_exists : Exception makedirs"
        )


def check_file_exists(
        file_path: str,
        obscure_list: list = [],
        stop: bool = True,
        print_log: bool = True
        ) -> bool:
    """ ## Check whether a file exists at the specified path.

    Verifies that the file exists and is readable.
    If the file is missing or unreadable, optionally logs an error
    via `NewtCons.error_msg()` and optionally stops execution.

    Args:
        file_path (str):
            Full path to the file to verify.
        obscure_list (list):
            List of substrings to keep visible in log messages.<br>
            All other characters in `file_path` will be masked with `*`.<br>
            If empty, the full path is shown as-is.<br>
            Defaults to [].
        stop (bool):
            If True, stops execution on any validation failure.<br>
            Defaults to True.
        print_log (bool):
            If True, logs an error message when the file is not found.<br>
            Note: error is also logged when `stop=True`, regardless of this parameter.<br>
            Defaults to True.

    Returns:
        out (bool):
            True if the file exists and is readable,<br>
            False otherwise.

    Raises:
        SystemExit:
            If an error occurs and `stop=True`, terminates with exit code 1.
    """

    if not NewtCons.validate_type(
        file_path, str, check_non_empty=True, stop=stop,
        location="Newt.files.check_file_exists : file_path"
    ):
        return False

    msg_file_path = file_path
    if obscure_list:
        msg_file_path = _obscure_logic(file_path, obscure_list)

    if os.path.isfile(file_path):
        if os.access(file_path, os.R_OK):
            return True

        NewtCons.error_msg(  # pragma: no cover
            f"Found Error Msg: (found? write test!)",  # TODO
            f"File is not readable: {msg_file_path}",
            location="Newt.files.check_file_exists : os.access file_path",
            stop=stop
        )
        return False  # pragma: no cover

    if print_log or stop:
        NewtCons.error_msg(
            f"File not found: {msg_file_path}",
            location="Newt.files.check_file_exists : print_log",
            stop=stop
        )

    return False


def choose_file_from_folder(
        folder_path: str,
        todo_dict: dict[str, int] | None = None
        ) -> str:
    """ ## Display files in a folder and let user interactively select one.

    Lists existing files in the directory (sorted alphabetically), shows numbered menu,
    prompts for selection (1-N or X to cancel), with 5 attempts max before timeout.
    Uses check_file_exists() to verify files are accessible.

    Args:
        folder_path (str):
            Path to directory containing files to choose from.
        todo_dict (dict[str, int] | None):
            Maps option names to a count displayed as prefix.<br>
            See `NewtUtil.count_values_by_position()`.<br>
            Defaults to None.

    Returns:
        out (str):
            Selected filename if valid choice made.
            Empty string if cancelled, no files found, or selection failed.

    Raises:
        SystemExit:
            Raised if folder not found, no files in folder, selection cancelled,
            or max attempts exceeded.
    """

    NewtCons.validate_type(
        folder_path, str, check_non_empty=True,
        location="Newt.files.choose_file_from_folder : folder_path"
    )

    if not os.path.isdir(folder_path):
        NewtCons.error_msg(
            f"Folder not found: {folder_path}",
            location="Newt.files.choose_file_from_folder : not isdir folder_path"
        )

    # Get file list
    try:
        file_list = [
            f for f in os.listdir(folder_path)
            if check_file_exists(os.path.join(folder_path, f), stop=False)
        ]
    except Exception as e:  # pragma: no cover
        NewtCons.error_msg(
            f"Found Error Msg: (found? write test!)",  # TODO
            f"Exception Failed to list directory: {e}",
            location="Newt.files.choose_file_from_folder : Exception file_list"
        )

    if not file_list:
        NewtCons.error_msg(
            "No files found in this folder.",
            location="Newt.files.choose_file_from_folder : file_list empty"
        )

    sorted_file_list = sorted(file_list)
    sorted_file_dict = {}
    for idx, name in enumerate(sorted_file_list, start=1):
        sorted_file_dict[str(idx)] = name
    choice = NewtUtil.select_from_input(sorted_file_dict, todo_dict)
    selected_file = sorted_file_dict[choice]

    return selected_file


# === TEXT ===

def read_text_from_file(
        file_name: str,
        obscure_list: list = [],
        stop: bool = True,
        print_log: bool = True
        ) -> str | None:
    """ ## Read UTF-8 text content from a file.

    Opens a text file and returns its full content as a string.
    If the file does not exist or cannot be read, returns None.
    Uses check_file_exists() to verify files are accessible.

    Args:
        file_name (str):
            Full path to the text file to read.
        obscure_list (list):
            List of substrings to keep visible in log messages.<br>
            All other characters in `file_path` will be masked with `*`.<br>
            If empty, the full path is shown as-is.<br>
            Defaults to [].
        stop (bool):
            If True, terminates execution when the file is not found.<br>
            Defaults to True.
        print_log (bool):
            If True, prints a confirmation message with file path and
            content length after successful loading.<br>
            Defaults to True.

    Returns:
        out (str | None):
            The full UTF-8 text content of the file,<br>
            or None if the file does not exist or reading fails.

    Raises:
        SystemExit:
            If `stop=True` and the file is not found, terminates with exit code 1.
    """

    if not check_file_exists(file_name, stop=stop, print_log=print_log):
        return None

    msg_file_path = file_name
    if obscure_list:
        msg_file_path = _obscure_logic(file_name, obscure_list)

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            content = f.read()

    except Exception as e:  # pragma: no cover
        NewtCons.error_msg(
            f"Found Error Msg: (found? write test!)",  # TODO
            f"Exception: {e}",
            location="Newt.files.read_text_from_file : Exception"
        )
        return None

    if print_log:
        print("[Newt.files.read_text_from_file] Loaded text from file:")
        print(msg_file_path)
        print(f"(length={len(content)})")

    return content


def save_text_to_file(
        file_name: str,
        content: str,
        append: bool = False,
        obscure_list: list = [],
        print_log: bool = True
        ) -> None:
    """ ## Write or append UTF-8 text content to a file.

    Automatically creates the target directory if it does not exist.
    All newline characters are normalized to Unix-style (`\\n`) before writing.
    If `append=True` and the file exists, content is appended;
    otherwise the file is created or overwritten.
    Uses check_file_exists() to verify files are accessible.

    Args:
        file_name (str):
            Full path to the target file to write or append to.
        content (str):
            Text content to save.
        append (bool):
            If True, appends to the existing file when it exists;<br>
            otherwise overwrites or creates a new file.<br>
            Defaults to False.
        obscure_list (list):
            List of substrings to keep visible in log messages.<br>
            All other characters in `file_path` will be masked with `*`.<br>
            If empty, the full path is shown as-is.<br>
            Defaults to [].
        print_log (bool):
            If True, prints a confirmation message with file path,
            content length, and write mode after saving.<br>
            Defaults to True.

    Returns:
        out (None):
            The function does not return a value.
    """

    NewtCons.validate_type(
        content, str,
        location="Newt.files.save_text_to_file : content"
    )

    content = _normalize_newlines(content)

    ensure_dir_exists(file_name)

    msg_file_path = file_name
    if obscure_list:
        msg_file_path = _obscure_logic(file_name, obscure_list)

    if append and check_file_exists(file_name, stop=False, print_log=print_log):
        mode_file, mode_text = "a", "append"
    else:
        mode_file, mode_text = "w", "write"

    try:
        with open(file_name, mode_file, encoding="utf-8", newline="\n") as f:
            f.write(content)

    except Exception as e:  # pragma: no cover
        NewtCons.error_msg(
            f"Found Error Msg: (found? write test!)",  # TODO
            f"Exception: {e}",
            location="Newt.files.save_text_to_file : Exception"
        )
        return None

    if print_log:
        print("[Newt.files.save_text_to_file] Saved text to file:")
        print(msg_file_path)
        print(f"(length={len(content)}, mode={mode_text})")


# === JSON ===

def convert_str_to_json(
        content: str
        ) -> list | dict | None:
    """ ## Parse a string into a JSON-compatible Python object.

    Tries `json.loads` on the stripped input first.
    If that fails, replaces all single quotes with double quotes and retries `json.loads`.
    Returns None if all attempts fail.

    Args:
        content (str):
            Input string containing JSON-like data.

    Returns:
        out (list | dict | None):
            Parsed Python `list` or `dict` on success,<br>
            or None if all parsing attempts fail or input is invalid.
    """

    if not NewtCons.validate_type(
        content, str, check_non_empty=True, stop=False,
        location="Newt.files.convert_str_to_json : content"
    ):
        return None

    content_strip = content.strip()

    # Try standard JSON first
    try:
        data = json.loads(content_strip)

        if NewtCons.validate_type(
            data, (list, dict), stop=False,
            location="Newt.files.convert_str_to_json : json.loads content_strip"
        ):
            return data

    except Exception as e:
        NewtCons.error_msg(
            f"Failed to parse string to JSON: {e}",
            f"Text size: {len(content_strip)}",
            location="Newt.files.convert_str_to_json : Exception standard JSON",
            stop=False
        )

    print("Trying to replace single quotes with double quotes...")

    # Try to replace single quotes with double quotes and try JSON again
    try:
        content_replace = content_strip.replace("'", '"')
        data = json.loads(content_replace)

        if NewtCons.validate_type(
            data, (list, dict), stop=False,
            location="Newt.files.convert_str_to_json : json.loads content_replace"
        ):
            return data

    except Exception as e:
        NewtCons.error_msg(
            f"Failed to parse string to JSON: {e}",
            f"Text size: {len(content_replace)}",
            location="Newt.files.convert_str_to_json : Exception replace quotes",
            stop=False
        )

    NewtCons.error_msg(
        "Cannot convert STR to JSON.",
        location="Newt.files.convert_str_to_json : Unknown type",
        stop=False
    )

    return None


def read_json_from_file(
        file_name: str,
        stop: bool = True,
        logging: bool = True
        ) -> list | dict | None:
    """
    Read and parse JSON data from a file.

    Opens and deserializes JSON content from a UTF-8 encoded file.
    Supports both list and dict structures.
    Returns None if the file is missing or invalid.

    Args:
        file_name (str):
            Path to the JSON file.
        stop (bool):
            If True, stops execution when file not found.
            Defaults to True.
        logging (bool):
            If True, prints a confirmation message after loading.
            Defaults to True.

    Returns:
        out (list | dict | None):
            Parsed JSON data,
            or None if missing or invalid.

    Raises:
        SystemExit:
            Raised when `stop=True` and file not found.
    """

    if not check_file_exists(file_name, stop=stop, logging=logging):
        return None

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Normalize output to always be a list or dict
        if NewtCons.validate_type(
            data, (list, dict), stop=False,
            location="Newt.files.read_json_from_file : data"
        ):
            if logging:
                print("[Newt.files.read_json_from_file] Loaded JSON from file:")
                print(file_name)
                print(f"(type={type(data)})")

            return data

        return None

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.files.read_json_from_file : Exception"
        )

    return None


def save_json_to_file(
        file_name: str,
        data: list | dict,
        indent: int = 2,
        logging: bool = True
        ) -> None:
    """
    Write JSON data to a file.

    Serializes a Python object as formatted JSON and saves it to disk.
    Creates parent directories if they do not exist.
    Appends a final newline for text file compatibility.

    Args:
        file_name (str):
            Path to the output JSON file.
        data (list | dict):
            Python data to serialize.
        indent (int):
            Indentation level for pretty-printing.
            Defaults to 2.
        logging (bool):
            If True, prints a confirmation message after saving.
            Defaults to True.
    """

    NewtCons.validate_type(
        data, (list, dict),
        location="Newt.files.save_json_to_file : data"
    )

    NewtCons.validate_type(
        indent, int, check_non_empty=True,
        location="Newt.files.save_json_to_file : indent"
    )

    if indent < 0:
        NewtCons.error_msg(
            "Indent must be a non-negative integer.",
            location="Newt.files.save_json_to_file : indent < 0"
        )

    ensure_dir_exists(file_name)

    try:
        with open(file_name, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
            f.write("\n")

        if logging:
            print("[Newt.files.save_json_to_file] Saved JSON to file:")
            print(file_name)
            print(f"(type={type(data)}, indent={indent})")

    except Exception as e:  # pragma: no cover
        NewtCons.error_msg(
            f"Exception: {e} (found? write test!)",  # TODO
            location="Newt.files.save_json_to_file : Exception",
            stop=False
        )


# === CSV ===

def read_csv_from_file(
        file_name: str,
        delimiter: str = ";",
        stop: bool = True,
        logging: bool = True
        ) -> list[list[str]] | None:
    """
    Read CSV data from a UTF-8 file.

    Loads CSV content into a list of string lists.
    Each sublist represents one row of data.
    Returns None if reading fails.

    Args:
        file_name (str):
            Path to the CSV file.
        delimiter (str):
            Column separator character.
            Defaults to `;`.
        stop (bool):
            If True, stops execution when file not found.
            Defaults to True.
        logging (bool):
            If True, prints a confirmation message after loading.
            Defaults to True.

    Returns:
        out (list[list[str]] | None):
            List of CSV rows,
            or None on failure.

    Raises:
        SystemExit:
            Raised when `stop=True` and file not found.
    """

    NewtCons.validate_type(
        delimiter, str, check_non_empty=True,
        location="Newt.files.read_csv_from_file : delimiter"
    )

    if not check_file_exists(file_name, stop=stop, logging=logging):
        return None

    try:
        with open(file_name, "r", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f, delimiter=delimiter))

        if logging:
            print("[Newt.files.read_csv_from_file] Loaded CSV from file:")
            print(file_name)
            print(f"(rows={len(rows)}, delimiter='{delimiter}')")

        return rows

    except Exception as e:  # pragma: no cover
        NewtCons.error_msg(
            f"Exception: {e} (found? write test!)",  # TODO
            location="Newt.files.read_csv_from_file : Exception",
            stop=False
        )

    return None


def save_csv_to_file(
        file_name: str,
        rows: Sequence[Sequence[object]],
        append: bool = False,
        delimiter: str = ";",
        logging: bool = True
        ) -> None:
    """
    Write tabular data to a CSV file.

    Saves a list of rows (lists of values) into a UTF-8 encoded CSV file.
    Automatically creates directories if necessary.
    Normalizes newlines in all cell data.

    Args:
        file_name (str):
            Path to the output CSV file.
        rows (Sequence[Sequence[object]]):
            Tabular data, where each row is a sequence of values.
        append (bool):
            If True, appends to the file instead of overwriting.
            Defaults to False.
        delimiter (str):
            Column separator character. Defaults to `;`.
        logging (bool):
            If True, prints a confirmation message after saving.
            Defaults to True.
    """

    NewtCons.validate_type(
        rows, (list, tuple),
        location="Newt.files.save_csv_to_file : rows"
    )

    NewtCons.validate_type(
        delimiter, str, check_non_empty=True,
        location="Newt.files.save_csv_to_file : delimiter"
    )

    ensure_dir_exists(file_name)

    mode_file = "a" if append else "w"
    mode_text = "append" if append else "write"

    try:
        # Normalize newlines in cell data
        normalized_rows = [
            [_normalize_newlines(str(cell)) for cell in row]
            for row in rows
        ]

        with open(file_name, mode_file, encoding="utf-8", newline="\n") as f:
            writer = csv.writer(f, delimiter=delimiter, lineterminator="\n")
            writer.writerows(normalized_rows)

        if logging:
            print("[Newt.files.save_csv_to_file] Saved CSV to file:")
            print(file_name)
            print(f"(rows={len(normalized_rows)}, mode={mode_text}, delimiter='{delimiter}')")

    except Exception as e:  # pragma: no cover
        NewtCons.error_msg(
            f"Exception: {e} (found? write test!)",  # TODO
            repr(file_name),
            location="Newt.files.save_csv_to_file : Exception",
            stop=False
        )


# === LOG ===

def setup_logging(
        _dir: str
        ) -> tuple[str, TextIO, object]:
    """
    Set up logging by redirecting stdout and stderr to both console and a timestamped log file.

    Creates a log file with a name based on current UTC time in the specified directory,
    defines a Tee class to duplicate output to both console and file,
    replaces sys.stdout and sys.stderr with Tee instances.

    Args:
        _dir (str):
            Directory path where the timestamped log file will be created.

    Returns:
        tuple[str, TextIO, object]:
            Tuple containing log filename (str),
            open file object (TextIO),
            and original sys.stdout (object).

    Example:
        >>> setup_data = setup_logging(_dir="path/to/log/directory")
        >>> cleanup_logging(setup_data, "path/to/target/logfile.txt")
    """

    NewtCons.validate_type(
        _dir, str, check_non_empty=True,
        location="Newt.files.setup_logging : _dir"
    )

    time_now = datetime.now(timezone.utc)
    time_file_name = time_now.strftime('%Y-%m-%d-%H-%M-%S') + ".txt"

    class Tee:
        def __init__(self, a, b):
            self.a, self.b = a, b

        def write(self, s: str) -> None:
            self.a.write(s)
            self.b.write(s)

        def flush(self) -> None:
            self.a.flush()
            try:
                self.b.flush()
            except ValueError:
                pass  # File already closed

    origin_stdout = sys.stdout
    time_file = os.path.join(_dir, time_file_name)
    file_content: TextIO = open(time_file, "a", encoding="utf-8", newline="\n")
    sys.stdout = Tee(origin_stdout, file_content)
    sys.stderr = sys.stdout

    return (time_file, file_content, origin_stdout)


def cleanup_logging(
        setup_data: tuple[str, TextIO, object],
        file_target: str
        ) -> None:
    """
    Restore original stdout/stderr and move log file to target path file.

    Closes the log file, restores original sys.stdout, moves the timestamped log
    to the specified target path, ensuring target directory exists.

    Args:
        setup_data (tuple[str, TextIO, object]):
            Tuple returned from setup_logging() containing (log_filename, file, old_stdout).
        file_target (str):
            Target path where the log file should be moved.
    """

    NewtCons.validate_type(
        setup_data, tuple, check_non_empty=True,
        location="Newt.files.cleanup_logging : setup_data"
    )

    time_file, file_content, origin_stdout = setup_data

    sys.stdout = origin_stdout
    file_content.close()
    print("Log moved to", file_target)
    ensure_dir_exists(file_target)
    shutil.move(time_file, file_target)
