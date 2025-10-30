"""
Created on 2025-10

@author: NewtCode Anna Burova

Functions:
    def _ensure_dir_exists(
        file_path: str
        ) -> None
    def _check_file_exists(
        file_path: str
        ) -> bool
    def _normalize_newlines(
        text: str
        ) -> str
    def choose_file_from_folder(
        folder_path: str
        ) -> str | None
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
import newtutils.utility as NewtUtil


def _ensure_dir_exists(
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

    dir_path = os.path.dirname(file_path)

    if not dir_path:
        # current directory, nothing to do
        return

    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)


def _check_file_exists(
        file_path: str
        ) -> bool:
    """
    Check whether a file exists at the specified path.

    Verifies file existence and accessibility.
    If missing, logs an error message
    via `NewtCons.error_msg()` without stopping execution.

    Args:
        file_path (str):
            Full path to the file to verify.

    Returns:
        out (bool):
            True if the file exists,
            otherwise False.
    """

    if os.path.isfile(file_path):
        return True

    NewtCons.error_msg(
        f"File not found: {file_path}",
        location="Newt.files._check_file_exists",
        stop=False
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

    return text.replace("\r\n", "\n")


def choose_file_from_folder(
        folder_path: str
        ) -> str | None:
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
        out (str | None):
            The selected file name,
            or None if cancelled or an error occurred.
    """

    # Validate folder path
    if not NewtCons.validate_input(folder_path, str):
        return None

    if not os.path.isdir(folder_path):
        NewtCons.error_msg(
            f"Folder not found: {folder_path}",
            location="Newt.files.choose_file_from_folder"
        )
        return None

    # Get file list
    try:
        file_list = sorted([
            f for f in os.listdir(folder_path)
            if _check_file_exists(os.path.join(folder_path, f))
        ])
    except Exception as e:
        NewtCons.error_msg(
            f"Failed to list directory: {e}",
            location="Newt.files.choose_file_from_folder",
            stop=False
        )
        return None

    if not file_list:
        print("No files found in this folder.")
        return None

    # Display numbered list
    print("\nAvailable files:", len(file_list))
    for idx, name in enumerate(file_list, start=1):
        print(f"{idx:>3}: {name}")
    print("  0: Exit / Cancel")

    # Loop until valid input
    while True:
        try:
            choice = input("\nEnter file number (0 to exit): ").strip()

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
                location="Newt.files.choose_file_from_folder",
                stop=False
            )
            return None


# === TEXT ===

def read_text_from_file(
        file_name: str
        ) -> str:
    """
    Read UTF-8 text content from a file.

    Opens a text file and returns its content.
    Returns an empty string if the file does not exist or cannot be read.

    Args:
        file_name (str):
            Full path to the text file.

    Returns:
        out (str):
            Text content of the file, or an empty string if reading fails.
    """

    if not _check_file_exists(file_name):
        return ""

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return f.read()

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.files.read_text_from_file",
            stop=False
        )
        return ""


def save_text_to_file(
        file_name: str,
        text: str,
        append: bool = False
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
            Defaults to False.

    Returns:
        out (None):
            No return value.
            Writes text to file.
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
            f"Exception: {e}",
            location="Newt.files.save_text_to_file",
            stop=False
        )


# === JSON ===

def read_json_from_file(
        file_name: str
        ) -> list | dict:
    """
    Read and parse JSON data from a file.

    Opens and deserializes JSON content from a UTF-8 encoded file.
    Supports both list and dict structures.
    Returns an empty list if the file is missing or invalid.

    Args:
        file_name (str):
            Path to the JSON file.

    Returns:
        out (list | dict):
            Parsed JSON data,
            or an empty list if missing or invalid.
    """

    if not NewtCons.validate_input(file_name, str):
        return []

    if not _check_file_exists(file_name):
        return []

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Normalize output to always be a list or dict
        if NewtCons.validate_input(data, (dict, list)):
            return data

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.files.read_json_from_file"
        )
        return []


def save_json_to_file(
        file_name: str,
        data,
        indent: int = 2
        ) -> None:
    """
    Write JSON data to a file.

    Serializes a Python object as formatted JSON and saves it to disk.
    Creates parent directories if they do not exist.
    Appends a final newline for text file compatibility.

    Args:
        file_name (str):
            Path to the output JSON file.
        data:
            Python data (list or dict) to serialize.
        indent (int):
            Indentation level for pretty-printing.
            Defaults to 2.
    """

    _ensure_dir_exists(file_name)

    try:
        with open(file_name, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
            f.write("\n")

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.files.save_json_to_file",
            stop=False
        )


# === CSV ===

def read_csv_from_file(
        file_name: str,
        delimiter: str = ";"
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

    Returns:
        out (list[list[str]]):
            List of CSV rows,
            or an empty list on failure.
    """

    if not _check_file_exists(file_name):
        return []

    try:
        with open(file_name, "r", encoding="utf-8", newline="") as f:
            return list(csv.reader(f, delimiter=delimiter))

    except Exception as e:
        NewtCons.error_msg(
            f"Exception: {e}",
            location="Newt.files.read_csv_from_file",
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
            f"Exception: {e}",
            location="Newt.files.save_csv_to_file",
            stop=False
            )
