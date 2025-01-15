"""Script to transfer data from an old database to a new database using sqlite3."""

import sqlite3
from pathlib import Path

# Paths configuration
BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "db.sqlite3"
OLD_DB_FILE = BASE_DIR / "db_old.sqlite3"  # Replace with your apps directory


def run():
    old_db = sqlite3.connect(OLD_DB_FILE)
    new_db = sqlite3.connect(DB_FILE)

    old_cursor = old_db.cursor()
    new_cursor = new_db.cursor()

    # Get a list of tables in the old database
    old_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in old_cursor.fetchall() if table[0]
              != "sqlite_sequence"]

    # Validate and sanitize table names
    allowed_tables = set(tables)  # Fetch tables only from the database itself

    for table_name in tables:
        if table_name not in allowed_tables:
            print(f"Skipping invalid or unexpected table: {table_name}")
            continue

        print(f"Transferring data from table: {table_name}")

        # Get the schema for the table
        old_cursor.execute(f"PRAGMA table_info({table_name});")
        columns = old_cursor.fetchall()

        # Create the table in the new database if it doesn't exist
        column_definitions = ", ".join(
            [f"{col[1]} {col[2]}" for col in columns])
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions});"
        new_cursor.execute(create_table_sql)

        # Get all data from the old table
        old_cursor.execute(f"SELECT * FROM {table_name}")
        rows = old_cursor.fetchall()

        # Prepare the INSERT OR IGNORE query
        if rows:
            placeholders = ", ".join(["?" for _ in columns])
            query = f"INSERT OR IGNORE INTO {table_name} VALUES ({placeholders})"

            for row in rows:
                try:
                    new_cursor.execute(query, row)
                    new_db.commit()
                except sqlite3.IntegrityError:
                    print(f"Row ignored from table '{table_name}': {row}")

    old_db.close()
    new_db.close()
