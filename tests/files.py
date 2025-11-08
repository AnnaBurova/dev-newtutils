"""
Created on 2025-10

@author: NewtCode Anna Burova

This module provides basic tests for the `files` utilities
from the `newtutils` package.

The tests cover:
1. Directory setup and cleanup.
3. Reading and writing JSON files.
4. Reading and writing CSV files.
"""

import os
import newtutils.console as NewtCons
import newtutils.files as NewtFiles


def test_json_files(
        test_dir: str
        ) -> None:
    """
    Test reading and writing JSON files using the provided test directory.

    This test validates saving and loading JSON data to and from UTF-8 encoded files.

    Args:
        test_dir (str):
            The path to the test directory created by `setup_test_directory()`.

    Returns:
        None
    """

    print("Test 2: JSON file operations")

    json_file = os.path.join(test_dir, "example.json")

    data = {"name": "NewtCode", "version": 0.1, "features": ["json", "csv", "text"]}
    NewtFiles.save_json_to_file(json_file, data)

    loaded = NewtFiles.read_json_from_file(json_file)
    print("Loaded JSON:", loaded)


def test_csv_files(
        test_dir: str
        ) -> None:
    """
    Test reading and writing CSV files using the provided test directory.

    This test writes tabular data to a CSV file and reads it back, verifying
    consistent structure and content.

    Args:
        test_dir (str):
            The path to the test directory created by `setup_test_directory()`.

    Returns:
        None
    """

    print("Test 3: CSV file operations")

    csv_file = os.path.join(test_dir, "example.csv")

    rows = [
        ["Name", "Age", "Language"],
        ["Anna", "30", "Python"],
        ["John", "28", "Go"]
    ]

    NewtFiles.save_csv_to_file(csv_file, rows)
    loaded_rows = NewtFiles.read_csv_from_file(csv_file)
    print("Loaded CSV:", loaded_rows)


def cleanup_test_directory(
        test_dir: str
        ) -> None:
    """
    Remove all test files and the test directory after tests complete.

    This function deletes all files within the test directory and removes
    the directory itself if it becomes empty.

    Args:
        test_dir (str):
            The path to the test directory to be cleaned up.

    Returns:
        None
    """

    print("--- CLEANUP ---")

    for f in os.listdir(test_dir):
        file_path = os.path.join(test_dir, f)

        if os.path.isfile(file_path):
            print("Deleting", file_path)
            os.remove(file_path)

    if not os.listdir(test_dir):
        os.rmdir(test_dir)
        print("Removed test directory:", test_dir)


if __name__ == "__main__":
    """Run all tests in sequence."""
    NewtCons._divider()
    test_json_files(test_dir)
    NewtCons._divider()
    test_csv_files(test_dir)
    NewtCons._divider()
    cleanup_test_directory(test_dir)
    NewtCons._divider()

    if not os.path.exists(test_dir):
        print("Test directory successfully cleaned up")
    else:
        print("Directory not fully deleted:", test_dir)

    print("Test passed")
