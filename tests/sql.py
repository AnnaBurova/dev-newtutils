"""
Created on 2025-10

@author: NewtCode Anna Burova

This module provides basic tests for the `sql` utilities
from the `newtutils` package.

The tests cover:
1. Database setup and cleanup.
2. Insert and select operations.
3. Update operations.
4. Export query results to CSV.
"""

import os
import newtutils.console as NewtCons
import newtutils.files as NewtFiles
import newtutils.sql as NewtSQL


def setup_test_database() -> str:
    """
    Create a temporary SQLite database for testing SQL operations.

    Returns:
        str:
            The full path to the test database file.
    """

    dir_ = os.path.dirname(os.path.realpath(__file__))
    db_path = os.path.join(dir_, "sql_data", "test.db")

    print(f"Setup test database: {db_path}")

    # Create a new table
    query = """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER,
            name TEXT,
            price REAL,
            PRIMARY KEY("id")
        );
    """
    result = NewtSQL.sql_execute_query(db_path, query)
    print("Table creation result (-1=ok):", result)

    return db_path


def test_insert_and_select(
        db_path: str
        ) -> None:
    """
    Test inserting rows and selecting them from the database.

    Args:
        db_path (str):
            Path to the test database created by setup_test_database().

    Returns:
        None
    """

    print("Test 1: Insert and Select operations")

    insert_rows = [
        {"name": "Apple", "price": 1.5},
        {"name": "Banana", "price": 2.0},
        {"name": "Cherry", "price": 3.2},
    ]

    insert_many = NewtSQL.sql_insert_row(db_path, "items", insert_rows)
    print("Inserted rows:", insert_many)
    for row in insert_rows:
        print(row)

    print()

    for row in insert_rows:
        # Insert row
        insert_one = NewtSQL.sql_insert_row(db_path, "items", row)
        print("Inserted rows:", insert_one)
        print(row)

    print()

    # Select rows
    query = """
        SELECT *
        FROM items
        ORDER BY id ASC;
    """
    select_rows = NewtSQL.sql_select_rows(db_path, query)
    print("Selected rows:", len(select_rows))
    for row in select_rows:
        print(row)


def test_update_rows(
        db_path: str
        ) -> None:
    """
    Test updating rows in the database.

    Args:
        db_path (str):
            Path to the test database created by setup_test_database().

    Returns:
        None
    """

    print("Test 2: Update operation")

    updated = NewtSQL.sql_update_rows(
        db_path,
        "items",
        {"price": 2.5},
        "name = ?",
        ("Banana",)
    )
    print(f"Updated rows: {updated}")

    # Select rows
    query = """
        SELECT *
        FROM items
        WHERE name = 'Banana'
        ORDER BY id ASC;
    """
    select_rows = NewtSQL.sql_select_rows(db_path, query)
    print("After update:", len(select_rows))
    for row in select_rows:
        print(row)


def test_export_to_csv(
        db_path: str
        ) -> None:
    """
    Test exporting query results to a CSV file.

    Args:
        db_path (str):
            Path to the test database created by setup_test_database().

    Returns:
        None
    """

    print("Test 3: Export query to CSV")

    dir_ = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(dir_, "sql_data", "items.csv")

    query = """
        SELECT *
        FROM items
        ORDER BY id ASC;
    """
    NewtSQL.export_sql_query_to_csv(db_path, query, csv_path)

    if NewtFiles._check_file_exists(csv_path):
        print(f"CSV file created successfully: {csv_path}")


def cleanup_test_database(
        db_path: str
        ) -> None:
    """
    Remove the test database and its directory.

    Args:
        db_path (str):
            Path to the test database file.

    Returns:
        None
    """

    print("--- CLEANUP ---")

    db_dir = os.path.dirname(db_path)

    if NewtFiles._check_file_exists(db_path):
        print("Deleting", db_path)

        if NewtSQL.db_delayed_close(db_path):
            os.remove(db_path)

    for f in os.listdir(db_dir):
        file_path = os.path.join(db_dir, f)

        if os.path.isfile(file_path):
            print("Deleting", file_path)
            os.remove(file_path)

    if not os.listdir(db_dir):
        os.rmdir(db_dir)
        print("Removed test directory:", db_dir)


if __name__ == "__main__":
    """Run all SQL tests in sequence."""
    NewtCons._divider()
    db_path = setup_test_database()
    NewtCons._divider()
    test_insert_and_select(db_path)
    NewtCons._divider()
    test_update_rows(db_path)
    NewtCons._divider()
    test_export_to_csv(db_path)
    NewtCons._divider()
    cleanup_test_database(db_path)
    NewtCons._divider()

    if not os.path.exists(os.path.dirname(db_path)):
        print("Database directory successfully cleaned up")
    else:
        print("Directory not fully deleted:", os.path.dirname(db_path))

    print("Test passed")
