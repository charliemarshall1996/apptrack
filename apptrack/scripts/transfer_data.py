"""Script to transfer data from an old database to a new database using sqlite3."""

import sqlite3
from pathlib import Path

# Paths configuration
BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "db.sqlite3"
OLD_DB_FILE = BASE_DIR / "db_old.sqlite3"  # Replace with your apps directory


def run():
    # Connect to the old and new databases
    """Transfers data from an old database to a new database using sqlite3.

    Connects to the old and new databases, creates a cursor for each database, gets a
    list of tables in the old database, excludes the sqlite_sequence table, loops
    through the tables and transfers data from the old table to the new table,
    committing each insert individually to see if it was ignored.

    Raises:
        sqlite3.IntegrityError: If a row is ignored from the new database
    """
    old_db = sqlite3.connect(OLD_DB_FILE)
    new_db = sqlite3.connect(DB_FILE)

    # Create a cursor for each database
    old_cursor = old_db.cursor()
    new_cursor = new_db.cursor()

    # Get a list of tables in the old database
    old_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = old_cursor.fetchall()

    # Exclude the sqlite_sequence table
    tables = [table for table in tables if table[0] != "sqlite_sequence"]

    # Loop through the tables in the old database
    for table in tables:
        table_name = table[0]

        print(f"Transferring data from table: {table_name}")

        # Get the schema for the table
        old_cursor.execute(f"PRAGMA table_info({table_name});")
        columns = old_cursor.fetchall()

        # Create the table in the new database if it doesn't exist
        column_definitions = ", ".join([f"{col[1]} {col[2]}" for col in columns])
        create_table_sql = (
            f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions});"
        )
        new_cursor.execute(create_table_sql)

        query = "SELECT * FROM ?"
        args = [table_name]
        # Get all data from the old table
        old_cursor.execute(query, args)
        rows = old_cursor.fetchall()

        # Prepare the INSERT OR IGNORE query to avoid conflicts
        if rows:
            # Placeholder for each column
            placeholders = ", ".join(["?" for _ in columns])
            args = [table_name, placeholders]
            query = "INSERT OR IGNORE INTO ? VALUES (?);"

            # Check for ignored rows
            for row in rows:
                try:
                    new_cursor.execute(query, args)
                    # Commit each insert individually to see if it was ignored
                    new_db.commit()
                except sqlite3.IntegrityError:
                    # If IntegrityError occurs, the row was ignored, print it
                    print(f"Row ignored from table '{table_name}': {row}")

    # Close the cursors and database connections
    old_db.close()
    new_db.close()
