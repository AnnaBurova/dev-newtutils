"""
Updated on 2026-02
Created on 2025-10

@author: NewtCode Anna Burova

Functions:
    def ensure_dir_exists(
        file_path: str
        ) -> None
    def check_file_exists(
        file_path: str,
        stop: bool = True,
        print_error: bool = True
        ) -> bool
    def _normalize_newlines(
        text: str
        ) -> str
    def choose_file_from_folder(
        folder_path: str
        ) -> str
    === TEXT ===
    def read_text_from_file(
        file_name: str,
        logging: bool = True
        ) -> str
    def save_text_to_file(
        file_name: str,
        text: str,
        append: bool = True,
        logging: bool = True
        ) -> None
    === JSON ===
    def convert_str_to_json(
        text: str
        ) -> list | dict | None
    def read_json_from_file(
        file_name: str,
        logging: bool = True
        ) -> list | dict
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
        logging: bool = True
        ) -> list[list[str]]
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


def ensure_dir_exists(
        file_path: str
        ) -> None:
    """
    Ensure that the directory for a given file path exists.

    Creates the target directory if it does not exist.
    The function does not create or modify the file itself.

    Args:
        file_path (str):
            Full path to the target file (including the file name).
    """

    NewtCons.validate_input(
        file_path, str,
        location="Newt.files.ensure_dir_exists : file_path"
    )

    dir_path = os.path.dirname(file_path)

    if not dir_path:
        # current directory, nothing to do
        return

    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)


def check_file_exists(
        file_path: str,
        stop: bool = True,
        print_error: bool = True
        ) -> bool:
    """
    Check whether a file exists at the specified path.

    Verifies file existence and accessibility.
    If missing, logs an error message
    via `NewtCons.error_msg()` without stopping execution.

    Args:
        file_path (str):
            Full path to the file to verify.
        stop (bool):
            If True, stops execution on error.
            If False, continues execution.
            Defaults to True.
        print_error (bool):
            If True, prints an error message when the file is not found.
            If False, silently returns False without logging.
            Defaults to True.

    Returns:
        out (bool):
            True if the file exists,
            otherwise False.
    """

    NewtCons.validate_input(
        file_path, str,
        location="Newt.files.check_file_exists : file_path"
    )

    if os.path.isfile(file_path):
        return True

    if print_error:
        NewtCons.error_msg(
            f"File not found: {file_path}",
            location="Newt.files.check_file_exists : print_error",
            stop=stop
        )
    return False


def _normalize_newlines(
        text: str
        ) -> str:
    """
    Normalize newline characters in a text string.

    Converts Windows-style newlines (`\\r\\n`)
    to Unix-style (`\\n`)
    for consistent text formatting across platforms.

    Args:
        text (str):
            Input text to normalize.

    Returns:
        out (str):
            Normalized text with Unix-style newlines.
    """

    NewtCons.validate_input(
        text, str,
        location="Newt.files._normalize_newlines : text"
    )

    return text.replace("\r\n", "\n").rstrip()


def choose_file_from_folder(
        folder_path: str
        ) -> str:
    """
    Display files in a folder and allow the user to choose one.

    Lists all files in the given directory, assigns numeric indices,
    and prompts the user to select a file by number.
    Returns the selected file name
    or None if cancelled.

    Args:
        folder_path (str):
            Path to the folder containing files.

    Returns:
        out (str):
            The selected file name,
            or None if cancelled or an error occurred.
    """

    NewtCons.validate_input(
        folder_path, str,
        location="Newt.files.choose_file_from_folder : folder_path"
    )

    if not os.path.isdir(folder_path):
        NewtCons.error_msg(
            f"Folder not found: {folder_path}",
            location="Newt.files.choose_file_from_folder : folder_path not dir"
        )

    # Get file list
    try:
        file_list = sorted([
            f for f in os.listdir(folder_path)
            if check_file_exists(os.path.join(folder_path, f))
        ])
    except Exception as e:
        NewtCons.error_msg(
            f"Failed to list directory: {e}",
            location="Newt.files.choose_file_from_folder : Exception file_list sorted"
        )

    if not file_list:
        NewtCons.error_msg(
            "No files found in this folder.",
            location="Newt.files.choose_file_from_folder : file_list empty"
        )

    # Display numbered list
    print("\nAvailable files:", len(file_list))
    for idx, name in enumerate(file_list, start=1):
        print(f"{idx:>3}: {name}")
    print("  0: Exit / Cancel")

    # Loop until valid input
    while True:
        try:
            choice = input("\nEnter file number (0 to exit): ").strip()
            print(f"[INPUT]: {choice}")

            if choice == "0":
                print("Selection cancelled.")
                return None

            if not choice.isdigit():
                print("Invalid input. Please enter a number.")
                continue

            index = int(choice)

            if 1 <= index <= len(file_list):
                selected_file = file_list[index - 1]
                print(f"Selected file: {selected_file}\n")
                return selected_file

            else:
                print("Number out of range. Try again.")

        except KeyboardInterrupt:
            print("\nSelection cancelled by user.")
            return None

        except Exception as e:
            NewtCons.error_msg(
                f"Exception: {e}",
                location="Newt.files.choose_file_from_folder : Exception while choice"
            )


# === TEXT ===

def read_text_from_file(
        file_name: str,
        logging: bool = True
        ) -> str:
    """
    Read UTF-8 text content from a file.

    Opens a text file and returns its content.
    Returns an empty string if the file does not exist or cannot be read.

    Args:
        file_name (str):
            Full path to the text file.
        logging (bool):
            If True, prints a confirmation message after saving.
            Defaults to True.

    Returns:
        out (str):
            Text content of the file, or an empty string if reading fails.
    """

    if not check_file_exists(file_name):
        return ""

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            content = f.read()

        if logging:
            print("[Newt.files.read_text_from_file] Loaded text from file:")
            print(file_name)
            print(f"(length={len(content)})")

        return content

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.files.read_text_from_file : Exception"
        )
        return ""


def save_text_to_file(
        file_name: str,
        text: str,
        append: bool = True,
        logging: bool = True
        ) -> None:
    """
    Write or append text content to a UTF-8 file.

    Automatically creates the target directory if it does not exist.
    All newline characters are normalized to Unix-style (`\\n`).

    Args:
        file_name (str):
            Full path to the target file.
        text (str):
            Text content to write.
        append (bool):
            If True, appends instead of overwriting.
            Defaults to True.
        logging (bool):
            If True, prints a confirmation message after saving.
            Defaults to True.
    """

    NewtCons.validate_input(
        text, str,
        location="Newt.files.save_text_to_file : text"
    )

    ensure_dir_exists(file_name)
    text = normalize_newlines(text)
    mode = "a" if append else "w"

    try:
        with open(file_name, mode, encoding="utf-8", newline="\n") as f:
            f.write(text)
            f.write("\n")

        if logging:
            print("[Newt.files.save_text_to_file] Saved text to file:")
            print(file_name)
            print(f"(mode={'append' if append else 'write'}, length={len(text)})")

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.files.save_text_to_file : Exception",
            stop=False
        )


# === JSON ===

def convert_str_to_json(
        text: str
        ) -> list | dict | None:
    """
    Parse a string into a JSON-compatible Python object.

    Tries `json.loads` first, falls back to `ast.literal_eval`,
    and as a last resort attempts a simple single-quote -> double-quote
    substitution before retrying `json.loads`.

    Args:
        text (str): Input string containing JSON-like data.

    Returns:
        out (list | dict | None): Parsed Python object on success, otherwise None.
    """

    NewtCons.validate_input(
        text, str,
        location="Newt.files.convert_str_to_json : text"
    )

    text_strip = text.strip()
    if not text_strip:
        return None

    # Try standard JSON first
    try:
        data = json.loads(text_strip)
        if isinstance(data, (list, dict)):
            return data
        return None
    except Exception as e:
        NewtCons.error_msg(
            f"Failed to parse string to JSON: {e}",
            location="Newt.files.convert_str_to_json : Exception standard JSON",
            stop=False
        )

    # Try to replace single quotes with double quotes and try JSON again
    try:
        text_replace = text_strip.replace("'", '"')
        data = json.loads(text_replace)
        if isinstance(data, (list, dict)):
            return data
    except Exception as e:
        NewtCons.error_msg(
            f"Failed to parse string to JSON: {e}",
            location="Newt.files.convert_str_to_json : Exception replace single quotes with double quotes",
            stop=False
        )
        NewtCons.validate_input(text_replace, (list, dict),
                                location="Newt.files.str_to_json.validate_input", stop=False)

    return None


def read_json_from_file(
        file_name: str,
        logging: bool = True
        ) -> list | dict:
    """
    Read and parse JSON data from a file.

    Opens and deserializes JSON content from a UTF-8 encoded file.
    Supports both list and dict structures.
    Returns an empty list if the file is missing or invalid.

    Args:
        file_name (str):
            Path to the JSON file.
        logging (bool):
            If True, prints a confirmation message after saving.
            Defaults to True.

    Returns:
        out (list | dict):
            Parsed JSON data,
            or an empty list if missing or invalid.
    """

    if not check_file_exists(file_name):
        return []

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Normalize output to always be a list or dict
        if NewtCons.validate_input(data, (dict, list),
                                   location="Newt.files.read_json_from_file.data"):
            if logging:
                print("[Newt.files.read_json_from_file] Loaded JSON from file:")
                print(file_name)
                print(f"(type={type(data)})")

            return data

        # If data is not a list or dict, return empty list
        if logging:
            print("[Newt.files.read_json_from_file] JSON content is not list/dict, returning empty list:")
            print(file_name)
        return []

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.files.read_json_from_file : Exception"
        )
        return []


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

    NewtCons.validate_input(
        data, (list, dict),
        location="Newt.files.save_json_to_file : data"
    )

    NewtCons.validate_input(
        indent, int,
        location="Newt.files.save_json_to_file : indent"
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

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.files.save_json_to_file : Exception",
            stop=False
        )


# === CSV ===

def read_csv_from_file(
        file_name: str,
        delimiter: str = ";",
        logging: bool = True
        ) -> list[list[str]]:
    """
    Read CSV data from a UTF-8 file.

    Loads CSV content into a list of string lists.
    Each sublist represents one row of data.
    Returns an empty list if reading fails.

    Args:
        file_name (str):
            Path to the CSV file.
        delimiter (str):
            Column separator character.
            Defaults to `;`.
        logging (bool):
            If True, prints a confirmation message after saving.
            Defaults to True.

    Returns:
        out (list[list[str]]):
            List of CSV rows,
            or an empty list on failure.
    """

    NewtCons.validate_input(
        delimiter, str,
        location="Newt.files.read_csv_from_file : delimiter"
    )

    if not check_file_exists(file_name):
        return []

    try:
        with open(file_name, "r", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f, delimiter=delimiter))

        if logging:
            print("[Newt.files.read_csv_from_file] Loaded CSV from file:")
            print(file_name)
            print(f"(rows={len(rows)}, delimiter='{delimiter}')")

        return rows

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.files.read_csv_from_file : Exception",
            stop=False
        )
        return []


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

    NewtCons.validate_input(
        rows, (list, tuple),
        location="Newt.files.save_csv_to_file : rows"
    )

    NewtCons.validate_input(
        delimiter, str,
        location="Newt.files.save_csv_to_file : delimiter"
    )

    ensure_dir_exists(file_name)

    mode = "a" if append else "w"

    try:
        # Normalize newlines in cell data
        normalized_rows = [
            [normalize_newlines(str(cell)) for cell in row]
            for row in rows
        ]

        with open(file_name, mode, encoding="utf-8", newline="\n") as f:
            writer = csv.writer(f, delimiter=delimiter, lineterminator="\n")
            writer.writerows(normalized_rows)

        if logging:
            print("[Newt.files.save_csv_to_file] Saved CSV to file:")
            print(file_name)
            print(f"(rows={len(normalized_rows)+1}, mode={'append' if append else 'write'}, delimiter='{delimiter}')")

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
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

    NewtCons.validate_input(
        _dir, str,
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

    NewtCons.validate_input(
        setup_data, tuple,
        location="Newt.files.cleanup_logging : setup_data"
    )

    time_file, file_content, origin_stdout = setup_data

    sys.stdout = origin_stdout
    file_content.close()
    print("Log moved to", file_target)
    ensure_dir_exists(file_target)
    shutil.move(time_file, file_target)
