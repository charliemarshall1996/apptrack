import os
import shutil
import subprocess
from pathlib import Path

# Paths configuration
BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "db.sqlite3"
OLD_DB_FILE = BASE_DIR / "db_old.sqlite3"  # Replace with your apps directory


def backup_database():
    if DB_FILE.exists():
        print("Backing up the old database...")
        shutil.move(str(DB_FILE), str(OLD_DB_FILE))

        if DB_FILE.exists():
            os.remove(DB_FILE)
        print("Database backup created as 'db_old.sqlite3'.")
    else:
        print("No database file found to back up.")


def remove_migrations():
    print("Removing migration files...")
    for app in BASE_DIR.iterdir():
        migrations_folder = app / "migrations"
        if migrations_folder.exists():
            for file in migrations_folder.iterdir():
                if file.name != "__init__.py":
                    if file.name == "__pycache__":
                        try:
                            subprocess.call(["rm", "-f", file.name])
                        except:
                            continue
                    else:
                        file.unlink()
            print(f"Cleared migrations for app: {app.name}")


def create_new_database():
    print("Creating new database...")
    try:
        subprocess.run(
            ["python", "manage.py", "makemigrations"], check=True)
    except Exception as e:
        print("FAILED to create migrations:", e)

    try:
        subprocess.run(["python", "manage.py", "migrate"], check=True)
    except Exception as e:
        print("FAILED to apply migrations:", e)
    print("New database structure created.")


def run():
    print(f"BASE DIRECTORY: {BASE_DIR}")

    try:
        backup_database()
    except subprocess.CalledProcessError:
        print("Failed to back up the database.")

    try:
        remove_migrations()
    except subprocess.CalledProcessError:
        print("Failed to remove migrations.")


if __name__ == "__main__":
    run()
