"""
Created on 2025-10

@author: NewtCode Anna Burova

Functions:
    def _ensure_dir_exists(
        file_path: str
        ) -> None
    def _normalize_newlines(
        text: str
        ) -> str
    === TEXT ===
    def read_text_from_file(
        file_name: str
        ) -> str
    def save_text_to_file(
        file_name: str,
        text: str,
        append: bool = False
        ) -> None
    === JSON ===
    def read_json_from_file(
        file_name: str
        ) -> list | dict
    def save_json_to_file(
        file_name: str,
        data,
        indent: int = 2
        ) -> None
    === CSV ===
    def read_csv_from_file(
        file_name: str,
        delimiter: str = ";"
        ) -> list[list[str]]
    def save_csv_to_file(
        file_name: str,
        rows: list[list],
        delimiter: str = ";"
        ) -> None
"""

import os
import csv
import json
import newtutils.console as NewtCons


def _ensure_dir_exists(
        file_path: str
        ) -> None:
    """
    Ensure that the directory for a given file path exists.

    This function checks whether the directory part of the given file path exists
    and creates it if necessary.
    It does not modify or create the file itself.

    Args:
        file_path (str):
            Full path to the file (including the file name).

    Returns:
        None
    """

    os.makedirs(os.path.dirname(file_path), exist_ok=True)


def _normalize_newlines(
        text: str
        ) -> str:
    """
    Normalize newline characters in a text string.

    This function replaces all Windows-style newline sequences (`\r\n`)
    with Unix-style newlines (`\n`)
    to ensure consistent formatting across platforms.

    Args:
        text (str):
            The input text to normalize.

    Returns:
        str:
            The normalized text string with Unix-style line endings.
    """

    return text.replace("\r\n", "\n")


# === TEXT ===

def read_text_from_file(
        file_name: str
        ) -> str:
    """
    Read text content from a file.

    This function opens a text file in UTF-8 encoding and returns its content.
    If the file does not exist or cannot be read, an empty string is returned.

    Args:
        file_name (str):
            The full path to the text file to read.

    Returns:
        str:
            The text content of the file, or an empty string
            if the file is not found or an error occurs during reading.
    """

    if not os.path.exists(file_name):
        return ""

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return f.read()

    except Exception as e:
        NewtCons.error_msg(
            f"read_text_from_file: {e}",
            location=file_name,
            stop=False
            )
        return ""


def save_text_to_file(
        file_name: str,
        text: str,
        append: bool = False
        ) -> None:
    """
    Write text content to a file.

    This function writes or appends text to a UTF-8 encoded file.
    If necessary, the target directory is automatically created.
    Newline characters are normalized to Unix-style (`\n`) for consistency.

    Args:
        file_name (str):
            The full path to the file where the text will be written.
        text (str):
            The text content to write to the file.
        append (bool, optional):
            If True, appends the text to the existing file instead of overwriting it.
            Defaults to False.

    Returns:
        None
    """

    _ensure_dir_exists(file_name)
    text = _normalize_newlines(text)

    mode = "a" if append else "w"

    try:
        with open(file_name, mode, encoding="utf-8", newline="\n") as f:
            f.write(text)
            f.write("\n")

    except Exception as e:
        NewtCons.error_msg(
            f"save_text_to_file: {e}",
            location=file_name,
            stop=False
            )


# === JSON ===

def read_json_from_file(
        file_name: str
        ) -> list | dict:
    """
    Read JSON data from a file.

    This function reads and parses JSON data from a UTF-8 encoded file.
    If the file does not exist or cannot be parsed, an empty list is returned.
    The function automatically handles both JSON arrays and objects.

    Args:
        file_name (str):
            The full path to the JSON file to read.

    Returns:
        list | dict:
            The parsed JSON data.
            Returns a list or dictionary depending on the JSON structure,
            or an empty list if the file is missing or invalid.
    """

    if not os.path.exists(file_name):
        return []

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception as e:
        NewtCons.error_msg(
            f"read_json_from_file: {e}",
            location=file_name,
            stop=False
            )
        return []


def save_json_to_file(
        file_name: str,
        data,
        indent: int = 2
        ) -> None:
    """
    Write JSON data to a file.

    This function serializes and saves Python data as JSON into a UTF-8 encoded file.
    The file's parent directories are created automatically if they do not exist.
    A final newline is appended to the output for compatibility with text file standards.

    Args:
        file_name (str):
            The full path to the JSON file to write.
        data:
            The Python data structure (list or dict) to serialize as JSON.
        indent (int, optional):
            The indentation level for pretty-printing the JSON output.
            Defaults to 2.

    Returns:
        None
    """

    _ensure_dir_exists(file_name)

    try:
        with open(file_name, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
            f.write("\n")

    except Exception as e:
        NewtCons.error_msg(
            f"save_json_to_file: {e}",
            location=file_name,
            stop=False
            )


# === CSV ===

def read_csv_from_file(
        file_name: str,
        delimiter: str = ";"
        ) -> list[list[str]]:
    """
    Read CSV data from a file.

    This function reads the contents of a CSV file encoded in UTF-8
    and returns all rows as a list of string lists.
    Each sublist represents one row.
    If the file does not exist or cannot be read, an empty list is returned.

    Args:
        file_name (str):
            The full path to the CSV file to read.
        delimiter (str, optional):
            The character used to separate columns in the CSV file.
            Defaults to ';'.

    Returns:
        list[list[str]]:
            A list of rows from the CSV file.
            Each row is represented as a list of strings.
            Returns an empty list if the file is not found
            or an error occurs during reading.
    """

    if not os.path.exists(file_name):
        return []

    try:
        with open(file_name, "r", encoding="utf-8", newline="") as f:
            return list(csv.reader(f, delimiter=delimiter))

    except Exception as e:
        NewtCons.error_msg(
            f"read_csv_from_file: {e}",
            location=file_name,
            stop=False
            )
        return []


def save_csv_to_file(
        file_name: str,
        rows: list[list],
        delimiter: str = ";"
        ) -> None:
    """
    Write CSV data to a file.

    This function writes tabular data (a list of rows) into a CSV file encoded in UTF-8.
    Each inner list represents a single row of values.
    The target directory is created automatically if it does not exist.

    Args:
        file_name (str):
            The full path to the CSV file to write.
        rows (list[list]):
            The tabular data to write.
            Each sublist represents one row of values to be written to the CSV file.
        delimiter (str, optional):
            The character used to separate columns in the CSV file.
            Defaults to ';'.

    Returns:
        None
    """

    _ensure_dir_exists(file_name)

    try:
        # Normalize newlines in cell data
        normalized_rows = [
            [str(cell).replace("\r\n", "\n") for cell in row]
            for row in rows
        ]

        with open(file_name, "w", encoding="utf-8", newline="\n") as f:
            writer = csv.writer(f, delimiter=delimiter, lineterminator="\n")
            writer.writerows(normalized_rows)

    except Exception as e:
        NewtCons.error_msg(
            f"save_csv_to_file: {e}",
            location=file_name,
            stop=False
            )
